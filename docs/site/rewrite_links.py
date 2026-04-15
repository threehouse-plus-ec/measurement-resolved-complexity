#!/usr/bin/env python3
"""Rewrite relative links in rendered HTML so they point at GitHub.

The site ships two pages (index.html = the Sail, repo.html = README). Every other
intra-repo link (e.g. `stages/stage8_synthesis/writeup.md`, `VOYAGE_PLAN.md`,
`figures/...`) should resolve to the corresponding file on GitHub.
"""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

LOCAL_PAGES = {"index.html", "repo.html", "style.css", "assets/tokens.css"}


def is_external(href: str) -> bool:
    p = urlparse(href)
    return bool(p.scheme) or href.startswith("//") or href.startswith("mailto:")


def rewrite(href: str, repo_url: str, branch: str) -> str:
    if not href or href.startswith("#") or is_external(href):
        return href
    if href.split("#", 1)[0].split("?", 1)[0] in LOCAL_PAGES:
        return href
    path, _, frag = href.partition("#")
    # Pick blob/ for files, tree/ for directories (heuristic: trailing slash or no extension).
    is_dir = path.endswith("/") or ("." not in Path(path).name)
    kind = "tree" if is_dir else "blob"
    clean = path.rstrip("/")
    new = f"{repo_url}/{kind}/{branch}/{clean}"
    if frag:
        new += f"#{frag}"
    return new


HREF_RE = re.compile(r'(href|src)="([^"]+)"')


def process(path: Path, repo_url: str, branch: str) -> None:
    text = path.read_text(encoding="utf-8")
    def sub(m):
        attr, href = m.group(1), m.group(2)
        return f'{attr}="{rewrite(href, repo_url, branch)}"'
    path.write_text(HREF_RE.sub(sub, text), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("--repo-url", required=True)
    ap.add_argument("--branch", default="main")
    args = ap.parse_args()
    for f in args.files:
        process(f, args.repo_url.rstrip("/"), args.branch)
    return 0


if __name__ == "__main__":
    sys.exit(main())
