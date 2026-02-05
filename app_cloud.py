import streamlit as st
import requests

st.set_page_config(page_title="GitHub Discussions Viewer", layout="wide")

st.title("📘 GitHub Discussions Web UI (Cloud)")

# --- Secrets ---
TOKEN = st.secrets.get("GITHUB_TOKEN")
OWNER = "vchinnap"
REPO = "vchinnap-discussions"

if not TOKEN:
    st.error("Missing GITHUB_TOKEN in Streamlit secrets")
    st.stop()

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json"
}

QUERY = """
query($owner:String!, $name:String!, $after:String) {
  repository(owner:$owner, name:$name) {
    discussions(first:50, after:$after, orderBy:{field:CREATED_AT, direction:DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number
        title
        url
        createdAt
        author { login }
        upvoteCount
        comments { totalCount }
        body
      }
    }
  }
}
"""

def fetch_discussions():
    discussions = []
    cursor = None

    while True:
        variables = {"owner": OWNER, "name": REPO, "after": cursor}
        r = requests.post(
            "https://api.github.com/graphql",
            json={"query": QUERY, "variables": variables},
            headers=HEADERS
        )
        data = r.json()

        nodes = data["data"]["repository"]["discussions"]["nodes"]
        discussions.extend(nodes)

        page = data["data"]["repository"]["discussions"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        cursor = page["endCursor"]

    return discussions


with st.spinner("Fetching discussions..."):
    discussions = fetch_discussions()

# --- Filters ---
title_filter = st.text_input("Filter by title")
author_filter = st.text_input("Filter by author")

for d in discussions:
    if title_filter and title_filter.lower() not in d["title"].lower():
        continue
    if author_filter and (not d["author"] or author_filter.lower() not in d["author"]["login"].lower()):
        continue

    st.markdown(f"## {d['title']}")
    st.markdown(f"**Author:** {d['author']['login'] if d['author'] else 'Unknown'}")
    st.markdown(f"**Created:** {d['createdAt']}")
    st.markdown(f"**Upvotes:** {d['upvoteCount']} | **Comments:** {d['comments']['totalCount']}")
    st.markdown(d["body"])
    st.markdown(f"[Open on GitHub]({d['url']})")
    st.divider()

