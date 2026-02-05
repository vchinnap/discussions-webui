#!/usr/bin/env bash
set -euo pipefail

OWNER="vchinnap"
REPO="vchinnap-discussions"
QUERY_FILE="query.graphql"
OUT_LINES="discussions.jsonl"

rm -f "$OUT_LINES"
cursor=""

QUERY_CONTENT="$(cat "$QUERY_FILE")"

while :; do
  if [ -z "$cursor" ]; then
    resp=$(gh api graphql \
      --raw-field query="$QUERY_CONTENT" \
      -F owner="$OWNER" \
      -F name="$REPO")
  else
    resp=$(gh api graphql \
      --raw-field query="$QUERY_CONTENT" \
      -F owner="$OWNER" \
      -F name="$REPO" \
      -F after="$cursor")
  fi

  echo "$resp" | jq -c '.data.repository.discussions.nodes[]' >> "$OUT_LINES"

  hasNext=$(echo "$resp" | jq -r '.data.repository.discussions.pageInfo.hasNextPage')
  cursor=$(echo "$resp" | jq -r '.data.repository.discussions.pageInfo.endCursor')

  [ "$hasNext" != "true" ] && break
done

jq -r '. | "- [#\(.number) \(.title)](\(.url)) — \(.author.login) — comments: \(.comments.totalCount) — upvotes: \(.upvoteCount)"' "$OUT_LINES"

