#!/usr/bin/env bash
# Build a static site with the Sail essay as the landing page.
# The Sail is the centre; all "further reading" links point back into the repo on GitHub.
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/threehouse-plus-ec/measurement-resolved-complexity}"
BRANCH="${BRANCH:-main}"
OUT=_site
TEMPLATE=docs/site/template.html
CSS=docs/site/style.css

rm -rf "$OUT"
mkdir -p "$OUT"

cp "$CSS" "$OUT/style.css"
cp -R docs/site/assets "$OUT/assets"

# Landing page: the Sail.
pandoc when-does-the-experiment-still-see.md \
  --from=markdown+tex_math_dollars+tex_math_single_backslash \
  --to=html5 \
  --mathjax \
  --standalone \
  --template="$TEMPLATE" \
  --metadata title="When does the experiment still see something happening?" \
  --metadata repo_url="$REPO_URL" \
  --metadata branch="$BRANCH" \
  --metadata is_sail=true \
  --output "$OUT/index.html"

# Secondary page: a short "about this repo" rendered from README, with a link home to the Sail.
pandoc README.md \
  --from=markdown+tex_math_dollars+tex_math_single_backslash \
  --to=html5 \
  --mathjax \
  --standalone \
  --template="$TEMPLATE" \
  --metadata title="measurement-resolved-complexity — repository overview" \
  --metadata repo_url="$REPO_URL" \
  --metadata branch="$BRANCH" \
  --output "$OUT/repo.html"

# Rewrite intra-repo relative links in the rendered HTML so they point at GitHub,
# not at non-existent files on the deployed site. Keep anchors, external URLs, and
# references to the two locally-rendered pages (index.html, repo.html) intact.
python3 docs/site/rewrite_links.py "$OUT/index.html" "$OUT/repo.html" \
  --repo-url "$REPO_URL" --branch "$BRANCH"

echo "Built site in $OUT/:"
ls -la "$OUT"
