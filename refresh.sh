#!/bin/bash
# Re-center the contribution-graph art.
#
# The GitHub graph is a sliding 53-week window, so the art drifts left and
# erodes as weeks pass. This regenerates the whole history against today's
# window and force-pushes it.
#
# Usage: ./refresh.sh [text] [commits-per-pixel]
set -euo pipefail

TEXT="${1:-HELLO WORLD !}"
PER_PIXEL="${2:-10}"
REMOTE="${REMOTE:-FareisGit/contribution-graph}"
NAME="${NAME:-FH}"
EMAIL="${EMAIL:-136382351+FareisGit@users.noreply.github.com}"

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

python3 -I gen_art.py "$TEXT" "$PER_PIXEL" > plan.txt
./build_art_repo.sh "$HERE/art" "$HERE/plan.txt" "$NAME" "$EMAIL"

git -C art log --pretty=format:'%ad' --date=short | sort -u > actual_days.txt
python3 -I verify.py actual_days.txt

read -r -p "Force-push this history to $REMOTE? [y/N] " ok
[ "$ok" = "y" ] || { echo "aborted"; exit 1; }

git -C art remote add origin "https://github.com/$REMOTE.git" 2>/dev/null || \
  git -C art remote set-url origin "https://github.com/$REMOTE.git"
git -C art push --force -u origin main
echo "done -- the graph may take a few minutes to update."
