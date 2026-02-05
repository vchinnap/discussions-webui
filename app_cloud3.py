import re
import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="GitHub Discussions Viewer", layout="wide")
st.title("📘 GitHub Discussions Web UI (Cloud)")

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# ---------- Helpers ----------
def gh_graphql(token: str, query: str, variables: dict):
    r = requests.post(
        GITHUB_GRAPHQL_URL,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        json={"query": query, "variables": variables},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    if "errors" in data:
        raise RuntimeError(str(data["errors"]))
    return data

def fmt_dt(s: str) -> str:
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return s or ""

def contains(hay: str, needle: str) -> bool:
    if not needle:
        return True
    if not hay:
        return False
    return needle.lower() in hay.lower()

def clean_text(t: str) -> str:
    if not t:
        return ""
    t = re.sub(r"\s+", " ", t).strip()
    return t


# ---------- Queries ----------
REPOS_QUERY = """
query($owner:String!, $after:String) {
  repositoryOwner(login: $owner) {
    repositories(first: 100, after: $after, orderBy: {field: UPDATED_AT, direction: DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes { name isPrivate isFork }
    }
  }
}
"""

DISCUSSIONS_QUERY = """
query($owner:String!, $name:String!, $after:String) {
  repository(owner:$owner, name:$name) {
    discussions(first:50, after:$after, orderBy:{field:CREATED_AT, direction:DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        title
        url
        createdAt
        updatedAt
        author { login }
        upvoteCount
        comments { totalCount }
        body
      }
    }
  }
}
"""

# Comments pagination: fetch 100 at a time, loop using after cursor
DISCUSSION_DETAIL_QUERY = """
query($owner:String!, $name:String!, $number:Int!, $after:String) {
  repository(owner:$owner, name:$name) {
    discussion(number:$number) {
      number
      title
      url
      createdAt
      updatedAt
      author { login }
      upvoteCount
      body
      comments(first:100, after:$after) {
        totalCount
        pageInfo { hasNextPage endCursor }
        nodes {
          author { login }
          createdAt
          body
        }
      }
    }
  }
}
"""


# ---------- Cached fetchers ----------
@st.cache_data(ttl=180)
def fetch_repos(token: str, owner: str):
    repos = []
    cursor = None
    while True:
        data = gh_graphql(token, REPOS_QUERY, {"owner": owner, "after": cursor})
        block = data["data"]["repositoryOwner"]["repositories"]
        repos.extend(block["nodes"])
        if not block["pageInfo"]["hasNextPage"]:
            break
        cursor = block["pageInfo"]["endCursor"]
    return repos


@st.cache_data(ttl=180)
def fetch_discussions_for_repo(token: str, owner: str, repo: str):
    out = []
    cursor = None
    while True:
        data = gh_graphql(token, DISCUSSIONS_QUERY, {"owner": owner, "name": repo, "after": cursor})
        block = data["data"]["repository"]["discussions"]
        out.extend(block["nodes"])
        if not block["pageInfo"]["hasNextPage"]:
            break
        cursor = block["pageInfo"]["endCursor"]
    for d in out:
        d["repo"] = repo
    return out


@st.cache_data(ttl=180)
def fetch_discussion_full(token: str, owner: str, repo: str, number: int, max_comments: int = 500):
    """
    Fetch full discussion body + up to max_comments comments (supports >100 via pagination).
    """
    cursor = None
    all_comments = []
    discussion = None

    while True:
        data = gh_graphql(
            token,
            DISCUSSION_DETAIL_QUERY,
            {"owner": owner, "name": repo, "number": number, "after": cursor},
        )
        discussion = data["data"]["repository"]["discussion"]
        cblock = discussion["comments"]
        all_comments.extend(cblock["nodes"])

        if len(all_comments) >= max_comments:
            all_comments = all_comments[:max_comments]
            break

        if not cblock["pageInfo"]["hasNextPage"]:
            break
        cursor = cblock["pageInfo"]["endCursor"]

    discussion["comments"]["nodes"] = all_comments
    return discussion


# ---------- Secrets ----------
TOKEN = st.secrets.get("GITHUB_TOKEN")
if not TOKEN:
    st.error("Missing GITHUB_TOKEN in Streamlit secrets.")
    st.stop()


# ---------- Sidebar UI ----------
with st.sidebar:
    st.header("Source")

    owner = st.text_input("Owner", "vchinnap")

    mode = st.radio("Mode", ["Single repo", "All repos under owner"], index=0)

    default_repo = st.text_input("Repo (single repo mode)", "discussions-webui")

    include_private = st.checkbox("Include private repos (all-repos mode)", value=False)
    exclude_forks = st.checkbox("Exclude forks (all-repos mode)", value=True)
    max_repos = st.slider("Max repos to scan", 1, 300, 50)

    st.divider()
    st.header("Filters")

    title_q = st.text_input("Title contains", "")
    author_q = st.text_input("Author login contains", "")
    content_q = st.text_input("Content contains (body/comments)", "")

    min_upvotes = st.slider("Min upvotes", 0, 500, 0)
    min_comments = st.slider("Min comments", 0, 500, 0)

    st.divider()
    st.header("Content search options")

    deep_search_comments = st.checkbox("Search comments too (slower)", value=False)
    deep_scan_max_discussions = st.slider("Deep scan max discussions", 1, 300, 50)
    deep_scan_max_comments = st.slider("Deep scan max comments per discussion", 50, 2000, 500)

    st.divider()
    refresh = st.button("Refresh (clear cache)")


if refresh:
    st.cache_data.clear()
    st.rerun()


# ---------- Fetch discussions ----------
all_discussions = []

try:
    if mode == "Single repo":
        with st.spinner(f"Fetching discussions from {owner}/{default_repo} ..."):
            all_discussions = fetch_discussions_for_repo(TOKEN, owner, default_repo)

    else:
        repos = fetch_repos(TOKEN, owner)

        if exclude_forks:
            repos = [r for r in repos if not r.get("isFork")]
        if not include_private:
            repos = [r for r in repos if not r.get("isPrivate")]

        repos = repos[:max_repos]
        repo_names = [r["name"] for r in repos]

        st.caption(f"Scanning {len(repo_names)} repos under `{owner}`")

        prog = st.progress(0)
        status = st.empty()

        for i, repo in enumerate(repo_names, start=1):
            status.write(f"Fetching `{repo}` ({i}/{len(repo_names)}) ...")
            try:
                all_discussions.extend(fetch_discussions_for_repo(TOKEN, owner, repo))
            except Exception:
                # no access / discussions off / etc.
                pass
            prog.progress(int(i * 100 / max(1, len(repo_names))))

        status.empty()
        prog.empty()

except Exception as e:
    st.error("Failed while fetching discussions.")
    st.code(str(e))
    st.stop()


# ---------- Fast filtering (body only unless deep mode enabled) ----------
filtered = []
for d in all_discussions:
    if title_q and not contains(d.get("title", ""), title_q):
        continue

    if author_q:
        a = (d.get("author") or {}).get("login", "")
        if not contains(a, author_q):
            continue

    if (d.get("upvoteCount") or 0) < min_upvotes:
        continue

    if (d.get("comments") or {}).get("totalCount", 0) < min_comments:
        continue

    if content_q and not deep_search_comments:
        if not contains(d.get("body") or "", content_q):
            continue

    filtered.append(d)


# ---------- Deep content filter: body + comments ----------
if content_q and deep_search_comments:
    st.info("Deep scan enabled: searching in body + comments (slower).")
    subset = filtered[:deep_scan_max_discussions]
    deep = []

    prog = st.progress(0)
    msg = st.empty()

    for idx, d in enumerate(subset, start=1):
        repo = d.get("repo", default_repo)
        msg.write(f"Deep scanning {repo}/#{d['number']} ({idx}/{len(subset)}) ...")

        try:
            full = fetch_discussion_full(
                TOKEN, owner, repo, int(d["number"]),
                max_comments=deep_scan_max_comments
            )
            comments_text = "\n\n".join((c.get("body") or "") for c in full["comments"]["nodes"])
            combined = (full.get("body") or "") + "\n\n" + comments_text

            if contains(combined, content_q):
                d["content_snippet"] = clean_text(combined)[:300]
                deep.append(d)

        except Exception:
            pass

        prog.progress(int(idx * 100 / max(1, len(subset))))

    msg.empty()
    prog.empty()
    filtered = deep


# ---------- Display results ----------
filtered.sort(key=lambda x: (x.get("repo", ""), x.get("number", 0)))

st.subheader(f"Results: {len(filtered)} discussions")

rows = []
for d in filtered:
    rows.append({
        "Repo": d.get("repo", default_repo),
        "Number": d["number"],
        "Title": d["title"],
        "Author": (d.get("author") or {}).get("login", ""),
        "Created": fmt_dt(d.get("createdAt", "")),
        "Upvotes": d.get("upvoteCount", 0),
        "Comments": (d.get("comments") or {}).get("totalCount", 0),
        "URL": d.get("url", ""),
        "Snippet": clean_text(d.get("content_snippet") or d.get("body") or "")[:160],
    })

st.dataframe(rows, use_container_width=True, hide_index=True)

if not filtered:
    st.stop()


# ---------- Open selected discussion (loads all comments up to max) ----------
st.divider()
st.header("Open discussion")

pick = st.selectbox(
    "Select a discussion",
    [f"{d.get('repo', default_repo)}/#{d['number']} — {d['title']}" for d in filtered]
)

pick_repo, rest = pick.split("/#", 1)
pick_number = int(rest.split("—", 1)[0].strip())

try:
    full = fetch_discussion_full(
        TOKEN, owner, pick_repo, pick_number,
        max_comments=deep_scan_max_comments
    )
except Exception as e:
    st.error("Failed to load discussion details.")
    st.code(str(e))
    st.stop()

st.markdown(f"## {pick_repo}/#{full['number']} — {full['title']}")
st.markdown(f"**Author:** {(full.get('author') or {}).get('login','')}")
st.markdown(f"**Created:** {fmt_dt(full.get('createdAt',''))} | **Updated:** {fmt_dt(full.get('updatedAt',''))}")
st.markdown(f"**Upvotes:** {full.get('upvoteCount',0)} | **Loaded comments:** {len(full['comments']['nodes'])} / {full['comments']['totalCount']}")
st.markdown(f"[Open on GitHub]({full['url']})")

st.subheader("Body")
st.markdown(full.get("body") or "_(empty)_")

st.subheader("Comments")
for c in full["comments"]["nodes"]:
    who = (c.get("author") or {}).get("login", "unknown")
    st.markdown(f"**{who}** — {fmt_dt(c.get('createdAt',''))}")
    st.markdown(c.get("body") or "")
    st.markdown("---")

