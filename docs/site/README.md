# docs/site/

**Endorsement Marker:** T(h)reehouse +EC voyage, Infrastructure layer. Local candidate framework under T(h)reehouse +EC stewardship. No external endorsement implied.

**Licence:** MIT (Infrastructure / code and tooling, per CD §0.3). Design-token asset under [`assets/`](assets/) is also MIT and is a Model-B copy from `threehouse-plus-ec/cd-rules` (see [`assets/SOURCE.md`](assets/SOURCE.md) for provenance and drift-detection instructions).

Static-site build for the public-facing page. The **Sail essay** (`when-does-the-experiment-still-see.md` at the repo root) is the landing page; a secondary page renders the repository `README.md`. All other in-essay links are rewritten at build time to point at GitHub.

## Files

- `build.sh` — pandoc invocation: Markdown → HTML5 with MathJax, using the template and stylesheet here, then runs the link rewriter. Copies `assets/` into the build output.
- `template.html` — pandoc HTML5 template with site header, nav, and footer.
- `style.css` — site-specific styling. Imports the canonical T(h)reehouse +EC tokens from `assets/tokens.css` (per CD §0.11, tokens are not redefined locally).
- `rewrite_links.py` — rewrites intra-repo relative links in the rendered HTML to `https://<repo>/blob|tree/<branch>/...`. Local assets (`index.html`, `repo.html`, `style.css`, `assets/tokens.css`) are preserved.
- `assets/tokens.css` — Model-B copy of `cd-rules/tokens.css`.
- `assets/SOURCE.md` — provenance record (source repo, commit, SHA-256) per CD §0.10.

## Local build

```bash
bash docs/site/build.sh
# open _site/index.html
```

Requires `pandoc` (≥ 3.0) and `python3`. Override the repo URL / branch with environment variables if needed:

```bash
REPO_URL=https://github.com/you/fork BRANCH=draft bash docs/site/build.sh
```

## Deployment

Automated via [`.github/workflows/pages.yml`](../../.github/workflows/pages.yml) on pushes to `main`. **One-time setup:** enable GitHub Pages under *Settings → Pages* with **Source: GitHub Actions**. After that, every push that touches the Sail, `README.md`, or `docs/site/**` will rebuild and redeploy.

## Asset-drift hygiene (CD §0.10)

When `cd-rules` publishes a new tag, refresh `assets/tokens.css` within one release cycle and update `assets/SOURCE.md` with the new commit, copy date, and SHA-256. Drift check: `shasum -a 256 docs/site/assets/tokens.css`.
