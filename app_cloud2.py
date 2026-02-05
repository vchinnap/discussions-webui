import re
import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="GitHub Discussions Viewer (Cloud v2)", layout="wide")
st.title("📘 GitHub Discussions Web UI (Cloud v2)")

# ----------------------------
# GitHub GraphQL helpers
# ----------------------------

GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

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
        return s

def contains(hay: str, needle: str) -> bool:
    if not needle:
        return True
    if hay is None:
        return False
    return needle.lower() in hay.lower()

def clean_text(t: str) -> str:
    if not t:
        return ""
    t = re.sub(r"\s+", " ", t).strip()
    return t

# ----------------------------
# GraphQL queries
# ----------------------------

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

DETAIL_QUERY = """
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

# ----------------------------
# Data fetchers (cached)
# ----------------------------

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
    # tag each discussion with repo name
    for d in out:
        d["repo"] = repo
    return out

@st.cache_data(ttl=180)
def fetch_discussion_full(token: str, owner: str, repo: str, number: int):
    cursor = None
    all_comments = []
    discussion = None
    while True:
        data = gh_graphql(token, DETAIL_QUERY, {"owner": owner, "name": repo, "number": number, "after": cursor})
        discussion = data["data"]["repository"]["discussion"]
        cblock = discussion["comments"]
        all_comments.extend(cblock["nodes"])
        if not cblock["pageInfo"]["hasNextPage"]:
            break
        cursor = cblock["pageInfo"]["endCursor"]
    discussion["comments"]["nodes"] = all_comments
    return discussion

# ----------------------------
# Sidebar (like your local app.py)
# ----------------------------

TOKEN = st.secrets.get("GITHUB_TOKEN")
if not TOKEN:
    st.error("Missing GITHUB_TOKEN in Streamlit secrets.")
    st.stop()

with st.sidebar:
    st.header("Source")

    owner = st.text_input("Owner", "vchinnap")

    mode = st.radio("Mode", ["Single repo", "All repos under owner"], index=1)

    include_private = st.checkbox("Include private repos", value=False)
    exclude_forks = st.checkbox("Exclude forks", value=True)

    max_repos = st.slider("Max repos to scan (All repos mode)", 1, 300, 50)
    st.caption("Tip: keep this lower at first (25–50) to avoid rate limits.")

    st.divider()
    st.header("Filters")

    title_q = st.text_input("Title contains", "")
    author_q = st.text_input("Author login", "")
    content_q = st.text_input("Content contains (body/comments)", "")

    min_upvotes = st.slider("Min upvotes", 0, 500, 0)
    min_comments = st.slider("Min comments", 0, 500, 0)

    deep_search_comments = st.checkbox("Include comments in content filter (slower)", value=False)
    deep_max_discussions = st.slider("Deep scan max discussions", 1, 300, 50)
    deep_max_comments_per_discussion = st.slider("Deep scan max comments per discussion", 10, 500, 100)

    st.divider()
    refresh = st.button("Refresh / clear cache")

if refresh:
    st.cache_data.clear()

# ----------------------------
# Load repos if needed
# ----------------------------

repo_list = []
selected_repo = None

if mode == "Single repo":
    selected_repo = st.text_input("Repo name", "vchinnap-discussions")
else:
    try:
        repos = fetch_repos(TOKEN, owner)
    except Exception as e:
        st.error("Failed to fetch repos for this owner.")
        st.code(str(e))
        st.stop()

    # filter forks/private
    if exclude_forks:
        repos = [r for r in repos if not r.get("isFork")]
    if not include_private:
        repos = [r for r in repos if not r.get("isPrivate")]

    repos = repos[:max_repos]
    repo_list = [r["name"] for r in repos]
    st.caption(f"Scanning {len(repo_list)} repos under `{owner}`")

# ----------------------------
# Fetch discussions
# ----------------------------

all_discussions = []

try:
    if mode == "Single repo":
        with st.spinner(f"Fetching discussions from {owner}/{selected_repo} ..."):
            all_discussions = fetch_discussions_for_repo(TOKEN, owner, selected_repo)
    else:
        progress = st.progress(0)
        status = st.empty()

        for i, repo in enumerate(repo_list, start=1):
            status.write(f"Fetching discussions from `{repo}` ({i}/{len(repo_list)}) ...")
            try:
                all_discussions.extend(fetch_discussions_for_repo(TOKEN, owner, repo))
            except Exception:
                # If discussions disabled/no access, just skip
                pass
            progress.progress(int(i * 100 / max(1, len(repo_list))))

        status.empty()
        progress.empty()

except Exception as e:
    st.error("Failed while fetching discussions.")
    st.code(str(e))
    st.stop()

# ----------------------------
# Apply FAST filters (title/author/upvotes/comments/body)
# ----------------------------

filtered = []
for d in all_discussions:
    if title_q and not contains(d.get("title", ""), title_q):
        continue
    if author_q and (not d.get("author") or d["author"]["login"].lower() != author_q.lower()):
        continue
    if (d.get("upvoteCount") or 0) < min_upvotes:
        continue
    if (d.get("comments") or {}).get("totalCount", 0) < min_comments:
        continue

    # content filter (FAST mode: body only)
    if content_q and not deep_search_comments:
        if not contains(d.get("body", "") or "", content_q):
            continue

    filtered.append(d)

# ----------------------------
# OPTIONAL: Deep scan comments for content filter
# ----------------------------

if content_q and deep_search_comments:
    st.info("Deep scan enabled: checking body + comments content (slower).")
    deep = []
    subset = filtered[:deep_max_discussions]

    prog = st.progress(0)
    msg = st.empty()

    for idx, d in enumerate(subset, start=1):
        msg.write(f"Deep scanning: {d.get('repo','')}/#{d['number']} ({idx}/{len(subset)}) ...")
        try:
            repo = d.get("repo") if mode == "All repos under owner" else selected_repo
            full = fetch_discussion_full(TOKEN, owner, repo, d["number"])

            body_text = full.get("body") or ""
            comments = full.get("comments", {}).get("nodes", [])[:deep_max_comments_per_discussion]
            comments_text = "\n\n".join((c.get("body") or "") for c in comments)

            combined = body_text + "\n\n" + comments_text
            if contains(combined, content_q):
                # keep the fast fields + attach small snippet
                d["content_snippet"] = clean_text(combined)[:240]
                deep.append(d)

        except Exception:
            # skip errors gracefully
            pass

        prog.progress(int(idx * 100 / max(1, len(subset))))

    msg.empty()
    prog.empty()
    filtered = deep

# ----------------------------
# Show results table
# ----------------------------

filtered.sort(key=lambda x: (x.get("repo",""), x.get("number",0)))

st.subheader(f"Results: {len(filtered)} discussions")

rows = []
for d in filtered:
    rows.append({
        "Repo": d.get("repo", selected_repo),
        "Number": d["number"],
        "Title": d["title"],
        "Author": (d.get("author") or {}).get("login", ""),
        "Created": fmt_dt(d.get("createdAt","")),
        "Upvotes": d.get("upvoteCount", 0),
        "Comments": (d.get("comments") or {}).get("totalCount", 0),
        "URL": d.get("url", ""),
        "Snippet": clean_text(d.get("content_snippet") or d.get("body") or "")[:140],
    })

st.dataframe(rows, use_container_width=True, hide_index=True)

if not filtered:
    st.stop()

# ----------------------------
# Open a discussion
# ----------------------------

st.divider()
st.header("Open discussion")

pick = st.selectbox(
    "Select",
    [f"{d.get('repo', selected_repo)}/#{d['number']} — {d['title']}" for d in filtered]
)

pick_repo, rest = pick.split("/#", 1)
pick_number = int(rest.split("—", 1)[0].strip())

try:
    full = fetch_discussion_full(TOKEN, owner, pick_repo, pick_number)
except Exception as e:
    st.error("Failed to load full discussion details.")
    st.code(str(e))
    st.stop()

st.markdown(f"## {pick_repo}/#{full['number']} — {full['title']}")
st.markdown(f"**Author:** {full['author']['login'] if full.get('author') else ''}")
st.markdown(f"**Upvotes:** {full.get('upvoteCount',0)} | **Comments:** {len(full['comments']['nodes'])}")
st.markdown(f"[Open on GitHub]({full['url']})")

st.subheader("Body")
st.markdown(full.get("body") or "_(empty)_")

st.subheader("Comments (all)")
for c in full["comments"]["nodes"]:
    who = c["author"]["login"] if c.get("author") else "unknown"
    st.markdown(f"**{who}** — {fmt_dt(c.get('createdAt',''))}")
    st.markdown(c.get("body") or "")
    st.markdown("---")

