# W19 — portable, machine-first repository interface

## Recommendation

Add a tiny, versioned JSON bootstrap and task-bundle manifest over the current text files. Make UTF-8 text the payload and JSON the control plane. A client should be able to start with one file, select named cards and source records, read inclusive one-based line ranges, and verify each fetched file from SHA-256 references. Keep paths relative and deterministic so the same manifest works in a checkout and on GitHub Pages. No step should depend on `tools/knowledge.py`, SQLite, a private Astra decoder, or a model-specific tokenizer.

This is a protocol proposal, not a claim that the current exports already implement it. The local edition has Python/SQLite, a 3.9-GB evidence store, exact-byte `indexes/files.jsonl`, and CLI/API retrieval. `ASTRA_GITHUB_WEB` is a 710-MB static export: it has cards, source text/pages, `web/documents.jsonl`, and static `web/catalog.json`, but no Python/SQLite/API runtime, cold evidence mirror, or current full-file hash inventory. Existing card and source indexes are useful routes, but the public document records do not expose SHA-256. Card HTML pages are rendered text without stable per-line anchors. The new interface should close those portability gaps explicitly.

## Bootstrap and bundle manifest

Publish `protocol/v1/bootstrap.json` in both editions. It should contain only protocol version, relative paths, repository identity/revision, and hashes/sizes for the small catalog shards. The bootstrap must not embed the 186-card corpus or claim the static export contains all source originals. Let it point to a task-bundle manifest chosen by the user or client. The bundle names the requested materials and their status; the client fetches only those paths.

Minimal illustrative bundle (the hash values below are placeholders, never valid evidence):

```json
{
  "protocol": "astra.bundle/1",
  "repository": "astra-research-knowledge",
  "revision": "<git-commit-or-snapshot-id>",
  "bundle_id": "repetition-interface-review",
  "selectors": {
    "cards": ["L02-commuting-repetition"],
    "sources": ["d-2815b2aba17e044e"],
    "ranges": [{"id": "d-2815b2aba17e044e", "start": 1, "end": 80}]
  },
  "items": [
    {
      "id": "L02-commuting-repetition",
      "kind": "card",
      "path": "cards/L02-commuting-repetition.txt",
      "sha256": "<64-lowercase-hex-of-exact-file-bytes>",
      "bytes": 1234,
      "encoding": "utf-8",
      "line_count": 12,
      "status": "source_derived_unreviewed"
    },
    {
      "id": "d-2815b2aba17e044e",
      "kind": "source",
      "path": "web/pages/d-2815b2aba17e044e.html",
      "text_path": "web/text/d-2815b2aba17e044e.txt",
      "sha256": "<64-lowercase-hex-of-exact-text-file-bytes>",
      "bytes": 4567,
      "encoding": "utf-8",
      "line_count": 92,
      "availability": "supplied"
    }
  ],
  "limits": {
    "meter": "utf8_bytes",
    "max_bytes": 24000,
    "scientific_validation": false
  }
}
```

In production, avoid duplicating `selectors` and `items` when a compact selector can be resolved against the bootstrap catalog. `items` here shows the resolved form a client can retain as a self-contained handoff. Define source `text_path` as canonical UTF-8 text even when the navigable page is HTML. If a source is missing, summarized, or intentionally excluded, list an explicit `availability` value (`supplied`, `summary_only`, `absent`, `excluded`) and do not invent a path. For this example, the card has a stable human ID and an associated source ID present in the current `web/documents.jsonl`; the card itself identifies the claim as unreviewed and says the source proof is needed.

## Selectors, ranges, and hash references

- Select cards by their existing IDs (`L02-commuting-repetition`); select sources by existing document IDs (`d-…`). Permit topic selectors only as discovery hints. Resolve them to explicit IDs before a bundle is handed to another agent, because topic membership alone is not a reproducible task definition.
- A range is `{id, start, end}` with 1-based inclusive line numbers over the canonical text file. Return the actual `start`, `end`, `total_lines`, and `next_line`; do not silently truncate. A range request past EOF clips at `total_lines`. Keep an exact file SHA-256 and byte length with every resolved item. A whole-file hash authenticates the retrieved file; line boundaries are then interpreted against those bytes after UTF-8 decoding and LF line splitting. Do not hash a re-rendered HTML page as if it were the source text.
- Give every catalog shard and text payload a SHA-256 of its exact served bytes. Pin the repository revision/snapshot in each bundle so a valid hash cannot accidentally point at a different edition. Full archived originals retain their own content SHA-256, which can be cross-referenced to the existing content-addressed `evidence/objects/<first-two>/<rest>` layout locally. Do not treat current short `d-` IDs as full-file hashes: they are identifiers, while `indexes/files.jsonl` has the actual full hashes.
- A response or handoff should report hash state as `verified`, `unverified`, or `unavailable`, plus verifier/method when known. A client without SHA-256 support can still read the named text and report unverified. Hash match establishes byte identity only, never proof correctness, completeness, or novelty.
- Keep token budgets advisory and byte-based in the portable layer. Local retrieval may report `o200k_base_estimate`; the current tool already falls back to a UTF-8-byte upper bound. Never promise equal token accounting across local and web agents.

## Format tradeoffs under the actual clients

| Format | Local checkout / CLI and API | Static web and constrained agent tools | Protocol role |
|---|---|---|---|
| Markdown or plain text | Easy to inspect, edit, and cite; current `00_START_HERE.txt`, topic routers, cards, and `web/*-sources.txt` already work. Parsing is fragile when delimiters, tables, or prose change; hashes and ranges need extra conventions. | Best fallback for browser open/read tools and prompt ingestion; links are navigable. Current pages are HTML and large `llms-full.txt` is a bulk file, so blind loading is costly and line selectors are unavailable. | Human-readable payload and optional quick-start. Keep one item per file; do not make Markdown the only machine contract. |
| TSV | Trivial streaming/parsing in shell/Python and compact for flat catalogs. Escaping tabs, embedded newlines, Unicode, optional fields, and nested source dependencies invites incompatible parsers. Poor at expressing missingness/provenance cleanly. | Often renders as opaque text, with no native schema validation; large tables are easy to overfetch. | Optional generated index for simple IDs/path/topic routing only; never authoritative for bundle structure. |
| JSON | Native in Python and the local API; deterministic field names, arrays, nested availability, range requests, and hashes. Verbose and one malformed/truncated file can break parsing; huge monolithic JSON is a bad browser fetch. | Browser tools can read small JSON manifests and issue ordinary static-path fetches, but some agents only have page-open/text tools and cannot run arbitrary JS or WebCrypto. Use small shards and allow unverified reading. | Canonical control plane: bootstrap, catalog shards, and task bundle. Keep payload text separate and hash it. |

The local API currently supports `/api/search`, `/api/packet`, and `/api/read` (with `id`, `start`, `end`); the CLI supports equivalent search/packet/read commands. Those are conveniences, not required protocol capabilities. A static client can follow JSON paths and open text directly. A browser/agent with only link navigation can still follow Markdown `path` fields; clients able to fetch raw responses can enforce byte and hash checks. This avoids making browser JavaScript, Python installation, or a custom parser a prerequisite.

## Small shards, not a single giant catalog

Use a bootstrap under a few KB that lists catalog shard paths, byte sizes, hashes, and schema version. Shard first by kind (`cards`, `sources`, `bundles`) and then by stable leading ID or topic, with a bounded target such as 100–300 KB. Current `web/documents.jsonl` and `indexes/claims.jsonl` are useful generation inputs; current `web/llms.txt`, topic routers, `web/library.txt`, and `web/*-sources.txt` remain human-readable fallback routes. `web/llms-full.txt` (about 138k estimated tokens) and `exports/ALL_RESULT_CARDS.txt` should remain opt-in bulk payloads, not bootstrap defaults.

Each card catalog record should carry `id`, title, status, topics, relative card path, exact-byte hash/size, and `source_ids`. Each source record should carry `id`, relative text/page paths when present, role, cycle, extraction/availability, source hash/size when payload is supplied, and any known source-to-card relation. Represent `summary_only` and `absent` explicitly: the static export notes that J/K, N/O/Q/U summaries have linked full packets absent, while L/M/P/R/S/T/V/W/X/Y/Z have varying supplied full evidence. Do not treat “source metadata” or an HTML link as the source text.

## Migration plan

1. Specify `astra.bundle/1`, UTF-8/LF line semantics, exact-byte hashing, missing-source states, and the narrow bootstrap schema. Freeze this schema independently of search ranking and tokenizer behavior.
2. Add a deterministic exporter that emits the bootstrap and card/source shards from the existing indexes for both local and static editions. Include SHA-256 and byte counts for every emitted JSON/text file. Preserve status labels and source-availability boundaries from the current routes.
3. Add canonical `web/text/<source-id>.txt` for supplied static source text (or declare a source unavailable). Keep HTML pages as navigation views, not canonical range-addressed protocol payloads. Ensure paths stay relative and work under both a checkout root and GitHub Pages base URL.
4. Add a thin resolver to local CLI/API for selectors and ranges, but keep direct path + range retrieval as the baseline. Return resolved bundle JSON so local and web agents exchange the same portable artifact.
5. Validate with a few representative bundles: one small card only, one card plus decisive source ranges, one missing/summary-only source. Check exact byte hashes and range boundaries in Python, then open the same paths through the static site. These checks establish packaging parity, not mathematical correctness.

The key migration constraint is evidence preservation: resolution may narrow what an agent reads, but cannot change a card’s claim status or erase supplied/acquired inputs, quantifiers, dependencies, cost fields, controls, failures, or the distinction between exact source bytes and extracted text. The representation contract at `mechanisms/REPRESENTATION_CONTRACT.json` is compatible with this protocol’s role: serialize scoped claims and known gaps without claiming that ingestion or a hash match certifies them.
