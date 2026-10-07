# W07 — Web/raw access and agent navigation audit

## Finding

The static edition has a workable raw-text fallback, but live publication currently appears behind the local build, and GitHub Pages did not open in the constrained web reader used for this check. Raw GitHub is the most reliable entry and retrieval route: requests for the root `llms.txt`, `01_CORE.txt`, a card, a hash-addressed HTML evidence page, `web/catalog.json`, and `web/llms-full.txt` all returned. GitHub repository HTML opened, but its UI response is noisy and its README advertises an older edition. The Pages root returned an access error in this reader; that is a reader limitation, not evidence the site is down for ordinary browsers.

## Route checks

Checked 8 October 2026 using the web reader:

- `raw.githubusercontent.com/.../main/llms.txt`: readable, 16 lines, with relative repository/raw/Pages bases and an instruction to load only relevant cards/proofs.
- `raw.../01_CORE.txt`: readable, 27 lines.
- `raw.../cards/N27-h5-nonsofic-refinement.txt`: readable, exact named card and evidence source IDs.
- `raw.../web/pages/d-e81c58360bb05ca9.html`: readable, full HTML-wrapped source with a link to exact original bytes under `web/assets/`.
- `raw.../web/catalog.json`: readable but one-line JSON; reader expanded it to 1,078 display lines. It is a large machine index, not a good first prompt.
- `raw.../web/llms-full.txt`: readable but large (3,327 displayed lines); use only after selecting a relevant record.
- `github.com/...`: repository page opened; the README visible there reports 178 cards / 10,328 source pages and J/K-era navigation.
- `harjassand.github.io/.../`: inaccessible through this web-reader tool.

## Publication drift / gating issue

The local target `outputs/ASTRA_GITHUB_WEB` is materially newer than the content exposed on the current `main` raw URLs. Local `indexes/BUILD.json` says 186 claim cards, 10,298 scientific source pages, and updates through Z; local `llms.txt` lists W–Z evidence and local `web/llms.txt` is 217 lines. The remote root `llms.txt` is only 16 lines and describes the earlier J/K state; remote `web/llms.txt` is 88 lines and README says 178 cards / 10,328 pages. The remote still resolves some later-looking records (including N27 and a Z hash-page route), so this is likely a mixed/partial publication or stale top-level entry rather than a cleanly synchronized snapshot. Do not tell agents that the complete local W–Z edition is remotely available until a revision/content comparison confirms it.

The local package exposes no obvious `MANIFEST`, `sitemap`, or `robots.txt` under this static export. The local catalog is a single 624-KiB JSON line; `llms-full.txt` is about 508 KiB. The cited `d-<hash>` identifiers are stable content-addressed source handles, while card IDs such as `N27-h5-nonsofic-refinement` are semantic/canonical handles. Keep both in citations: card ID for discovery, `d-...` for exact source/evidence. A source path alone can move as packaging changes.

## Small web bootstrap and retrieval protocol

1. Pin a small root `llms.txt` to the deployed revision and put the revision/commit SHA, build timestamp, card count, source-page count, and a brief freshness warning on the first screen. Link only `00_START_HERE.txt`, `01_CORE.txt`, a compact topic/card router, the source-library directory index, and a package status/manifest page.
2. Expose a compact line-oriented manifest (JSONL/TSV) with `record_id`, title, status, topics, source IDs, relative raw URL, byte count, SHA-256, and optional evidence/package membership. Paginate it by topic/update family. Do not send the one-line 624-KiB catalog or all 10k pages at startup.
3. Preserve two-stage selection: agent reads root/core (roughly 6k estimated tokens), searches a small card/topic shard, then requests one or a few exact card/source URLs. Retrieve further proof/dependency files only when a card names them. The 508-KiB `llms-full.txt` is a fallback search index, not context to load wholesale.
4. Use canonical card IDs for claim references and content hashes (`d-...`) for exact source versions. Include source-file SHA-256 in the manifest and repeat it in each evidence page footer or adjacent metadata. Add a generated publication manifest with hashes for the bootstrap, catalogs, pages, and assets, so web freshness and integrity can be checked without cloning the repository.
5. In any constrained browser, construct direct `raw.githubusercontent.com/<owner>/<repo>/<commit>/<path>` URLs for small text files. Prefer a pinned commit URL over `main` for a reproducible audit. If raw fetch fails, use GitHub's `/blob/<commit>/<path>` page or a narrow raw download through an allowed client. Treat Pages availability as optional. For huge package archives, avoid browser ingestion: follow the relevant source manifest and fetch only named components, or use a deliberate archive download if the task actually needs the full package.
6. Have the bootstrap say explicitly that web access is a static edition and that local SQLite/Python retrieval, cold binaries, and excluded originals are unavailable remotely. It should also distinguish source-reported checks from replayed checks and never imply publication validates the science.

## Decision

Raw access is usable for targeted retrieval and source-level evidence; Pages is not a dependable route for this reader. Current local-to-remote drift is the main agent-navigation risk. First establish that the intended newer export is the deployed commit and refresh root `llms.txt`, README counts, and card/source manifests together. Then use a small topic-sharded index plus exact hash-addressed evidence links; no full-corpus crawl is needed.
