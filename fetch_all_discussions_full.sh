#!/usr/bin/env bash
set -euo pipefail

OWNER="vchinnap"
REPO="vchinnap-discussions"

OUT_JSONL="all_discussions_full.jsonl"
OUT_MD="all_discussions_full.md"
PER_DIR="discussion_bodies"

mkdir -p "$PER_DIR"
rm -f "$OUT_JSONL" "$OUT_MD"

# 1) Get list of discussion numbers (pagination)
cursor=""
numbers_file="$(mktemp)"
trap 'rm -f "$numbers_file"' EXIT

while :; do
  if [ -z "$cursor" ]; then
    resp=$(gh api graphql --raw-field query='
      query($owner:String!,$name:String!,$after:String){
        repository(owner:$owner,name:$name){
          discussions(first:50, after:$after, orderBy:{field:CREATED_AT, direction:DESC}){
            pageInfo{hasNextPage endCursor}
            nodes{ number }
          }
        }
      }' -F owner="$OWNER" -F name="$REPO")
  else
    resp=$(gh api graphql --raw-field query='
      query($owner:String!,$name:String!,$after:String){
        repository(owner:$owner,name:$name){
          discussions(first:50, after:$after, orderBy:{field:CREATED_AT, direction:DESC}){
            pageInfo{hasNextPage endCursor}
            nodes{ number }
          }
        }
      }' -F owner="$OWNER" -F name="$REPO" -F after="$cursor")
  fi

  echo "$resp" | jq -r '.data.repository.discussions.nodes[].number' >> "$numbers_file"

  hasNext=$(echo "$resp" | jq -r '.data.repository.discussions.pageInfo.hasNextPage')
  cursor=$(echo "$resp" | jq -r '.data.repository.discussions.pageInfo.endCursor')
  [ "$hasNext" != "true" ] && break
done

# 2) Fetch full body + comments for each discussion number
while read -r n; do
  echo "Fetching discussion #$n ..."

  full=$(gh api graphql --raw-field query='
    query($owner:String!,$name:String!,$number:Int!){
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
          comments(first:100){
            totalCount
            nodes{
              author{login}
              createdAt
              body
            }
          }
        }
      }
    }' -F owner="$OWNER" -F name="$REPO" -F number="$n")

  # Save raw JSON line
  echo "$full" | jq -c '.data.repository.discussion' >> "$OUT_JSONL"

  # Save per-discussion readable markdown
  echo "$full" | jq -r '
    .data.repository.discussion as $d |
    "#\($d.number) \($d.title)\n" +
    "- URL: \($d.url)\n" +
    "- Author: \($d.author.login)\n" +
    "- Created: \($d.createdAt)\n" +
    "- Updated: \($d.updatedAt)\n" +
    "- Upvotes: \($d.upvoteCount)\n" +
    "- Comments: \($d.comments.totalCount)\n\n" +
    "## Body\n\n" + ($d.body // "") + "\n\n" +
    "## Comments\n\n" +
    (if ($d.comments.nodes | length) == 0 then
      "_No comments_\n"
    else
      ($d.comments.nodes[] | "- **\(.author.login)** (\(.createdAt)):\n\n  \(.body)\n")
    end) + "\n---\n"
  ' > "${PER_DIR}/discussion_${n}.md"

done < "$numbers_file"

# 3) Combine into one big markdown file
cat "${PER_DIR}"/discussion_*.md > "$OUT_MD"

echo ""
echo "✅ Done!"
echo "Saved:"
echo " - Raw JSONL: $OUT_JSONL"
echo " - Combined Markdown: $OUT_MD"
echo " - Per-discussion files in: $PER_DIR/"

