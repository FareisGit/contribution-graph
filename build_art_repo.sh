#!/bin/bash
# Build a git repo whose commit dates draw pixel art on the GitHub
# contribution graph. Uses commit-tree so we never touch the index.
#
# Usage: ./build_art_repo.sh <repo-dir> <plan-file> <name> <email>
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"

REPO="$1"
PLAN="$2"
NAME="$3"
EMAIL="$4"

rm -rf "$REPO"
mkdir -p "$REPO"
cd "$REPO"
git init -q -b main
git config user.name  "$NAME"
git config user.email "$EMAIL"

cp "$SRC/gen_art.py" "$SRC/verify.py" "$SRC/build_art_repo.sh" \
   "$SRC/refresh.sh" "$SRC/messages.txt" .
cp "$SRC/art_readme.md" README.md

git add -A
TREE=$(git write-tree)

PARENT=""
COUNT=0
while IFS=$'\t' read -r STAMP MSG; do
  [ -z "${STAMP:-}" ] && continue
  export GIT_AUTHOR_NAME="$NAME"    GIT_AUTHOR_EMAIL="$EMAIL"
  export GIT_COMMITTER_NAME="$NAME" GIT_COMMITTER_EMAIL="$EMAIL"
  export GIT_AUTHOR_DATE="$STAMP"   GIT_COMMITTER_DATE="$STAMP"
  if [ -z "$PARENT" ]; then
    PARENT=$(git commit-tree "$TREE" -m "$MSG")
  else
    PARENT=$(git commit-tree "$TREE" -p "$PARENT" -m "$MSG")
  fi
  COUNT=$((COUNT + 1))
done < "$PLAN"

git update-ref refs/heads/main "$PARENT"
git reset -q --hard main
echo "built $COUNT commits in $REPO"
