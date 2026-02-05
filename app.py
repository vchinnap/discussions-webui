import json
import re
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

import streamlit as st

OWNER_DEFAULT = "vchinnap"
REPO_DEFAULT = "vchinnap-discussions"

# -------------------------
# GraphQL queries
# -------------------------

LIST_QUERY = """
query($owner:String!,$name:String!,$after:String){
  repository(owner:$owner,name:$name){
    discussions(first:50, after:$after, orderBy:{field:CREATED_AT, direction:DESC}){
      pageInfo{hasNextPage endCursor}
      nodes{
        number
        title
        url
        author { login }
        createdAt
        updatedAt
        upvoteCount
        comments { totalCount }
      }
    }
  }
}
"""

DETAIL_QUERY = """
query($owner:String!,$name:String!,$number:Int!,$after:String){
  repository(owner:$owner,name:$name){
    discussion(number:$number){
      number
      title
      url
      author{login}
      createdAt
      updatedAt
      upvoteCount
      body
      comments(first:100, after:$after){
        totalCount
        pageInfo{hasNextPage endCursor}
        nodes{
          author{login}
          createdAt
          body
        }
      }
    }
  }
}
"""

# -------------------------
# Helpers
# -------------------------

def run_gh(query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
    args = ["gh", "api", "graphql", "--raw-field", f"query={query}"]
    for k, v in variables.items():
        args.extend(["-F", f"{k}={v}"])

    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr or p.stdout)
    return json.loads(p.stdout)


def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def fmt(s: str) -> str:
    return parse_dt(s).strftime("%Y-%m-%d %H:%M")


def summarize_local(text: str, n: int = 5) -> List[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return ["(No content)"]

    sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = [s for s in sentences if len(s) > 30]

    words = re.findall(r"[a-zA-Z]{3,}", text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    def score(s):
        return sum(freq.get(w, 0) for w in s.lower().split())

    ranked = sorted(sentences, key=score, reverse=True)
    return ranked[:n] if ranked else sentences[:n]


# -------------------------
# Fetchers
# -------------------------

@st.cache_data(ttl=180)
def fetch_discussions(owner: str, repo: str):
    out = []
    cursor = None
    while True:
        vars = {"owner": owner, "name": repo}
        if cursor:
            vars["after"] = cursor
        data = run_gh(LIST_QUERY, vars)
        block = data["data"]["repository"]["discussions"]
        out.extend(block["nodes"])
        if not block["pageInfo"]["hasNextPage"]:
            break
        cursor = block["pageInfo"]["endCursor"]
    return out


@st.cache_data(ttl=180)
def fetch_discussion_full(owner: str, repo: str, number: int):
    all_comments = []
    cursor = None
    while True:
        vars = {"owner": owner, "name": repo, "number": number}
        if cursor:
            vars["after"] = cursor
        data = run_gh(DETAIL_QUERY, vars)
        d = data["data"]["repository"]["discussion"]
        c = d["comments"]
        all_comments.extend(c["nodes"])
        if not c["pageInfo"]["hasNextPage"]:
            d["comments"]["nodes"] = all_comments
            return d
        cursor = c["pageInfo"]["endCursor"]


# -------------------------
# UI
# -------------------------

st.set_page_config(page_title="GitHub Discussions Web UI", layout="wide")
st.title("GitHub Discussions – Full Viewer")

with st.sidebar:
    owner = st.text_input("Owner", OWNER_DEFAULT)
    repo = st.text_input("Repo", REPO_DEFAULT)

    st.divider()
    st.header("Filters")
    title_q = st.text_input("Title contains")
    author_q = st.text_input("Author")
    min_upvotes = st.slider("Min upvotes", 0, 200, 0)
    min_comments = st.slider("Min comments", 0, 200, 0)

    refresh = st.button("Refresh")

if refresh:
    st.cache_data.clear()

try:
    discussions = fetch_discussions(owner, repo)
except Exception as e:
    st.error(e)
    st.stop()

filtered = []
for d in discussions:
    if title_q and title_q.lower() not in d["title"].lower():
        continue
    if author_q and d["author"]["login"].lower() != author_q.lower():
        continue
    if d["upvoteCount"] < min_upvotes:
        continue
    if d["comments"]["totalCount"] < min_comments:
        continue
    filtered.append(d)

filtered.sort(key=lambda x: x["comments"]["totalCount"], reverse=True)

st.subheader(f"{len(filtered)} discussions")

st.dataframe(
    [{
        "Number": d["number"],
        "Title": d["title"],
        "Author": d["author"]["login"],
        "Created": fmt(d["createdAt"]),
        "Upvotes": d["upvoteCount"],
        "Comments": d["comments"]["totalCount"],
        "URL": d["url"]
    } for d in filtered],
    use_container_width=True
)

if not filtered:
    st.stop()

choice = st.selectbox(
    "Open discussion",
    [f"#{d['number']} – {d['title']}" for d in filtered]
)

num = int(choice.split("–")[0].replace("#", "").strip())

try:
    d = fetch_discussion_full(owner, repo, num)
except Exception as e:
    st.error(e)
    st.stop()

st.divider()
st.header(f"#{d['number']} – {d['title']}")

st.markdown(f"**Author:** {d['author']['login']}")
st.markdown(f"**Upvotes:** {d['upvoteCount']}")
st.markdown(f"**Comments:** {d['comments']['totalCount']}")
st.markdown(f"[Open on GitHub]({d['url']})")

body = d["body"] or ""
comments = d["comments"]["nodes"]

combined = body + "\n\n" + "\n\n".join(c["body"] for c in comments if c["body"])

st.subheader("Summary")
for s in summarize_local(combined):
    st.markdown(f"- {s}")

st.subheader("Body")
st.markdown(body if body else "_No body_")

st.subheader(f"Comments ({len(comments)})")
for c in comments:
    st.markdown(f"**{c['author']['login']}** — {fmt(c['createdAt'])}")
    st.markdown(c["body"])
    st.markdown("---")

