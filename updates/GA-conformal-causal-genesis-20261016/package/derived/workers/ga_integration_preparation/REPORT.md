# GA integration preparation

This is a metadata and append-only route preparation, not an assessment of the conformal or causal mathematics. No scientific card text was authored here, no canonical checkout file was changed, and no archive was preloaded.

## Pinned state and route availability

The inspected repository is `/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016`, branch `codex/conformal-causal-genesis-20261016`. The immutable main base is `f80a8f15137575133ad2c9af975513b32e8fa93e`; after root's source-preservation commit, the expected branch HEAD is `f116469ee41bdc54a155099175b8ce063be98edd`. `origin/main` remains at the immutable base. The working tree was clean.

At that checkout, numeric routes N885, N886, N887, and N888 are absent from `indexes/claims.jsonl`. A read-only patch-text scan of the five currently open PRs (#84, #85, #87, #88, #95) found no occurrence of any of those four route IDs. Recheck route occupancy and PRs immediately before integration, since either can move.

Root subsequently specified a fourth route, `N888-nonlinear-separable-conformal-calibration`. The renderer now accepts a variable-length root-authored card list over the four reserved IDs; it does not generate or assess that card's scientific content.

Current GitHub read receipts (path count is from the paginated PR files API; no full diffs were copied):

| PR | State | Paths | Relevant observation |
|---|---:|---:|---|
| #84 | open, draft, conflicting | 186 | N815–N816; base `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871` |
| #85 | open, draft, conflicting | 152 | N817–N818; base `1c45f77e32d6fbd72483aed5014061c7bda4f372` |
| #87 | open, draft, conflicting | 138 | N822; base `00631610750c708263d5cf6d812ebbb8edc77335` |
| #88 | open, draft, conflicting | 310 | N822–N824; same base as #87, so N822 is present in two competing open PRs |
| #95 | open, draft, mergeable | 594 | Its body retains a chemical-quantitation HOLD and says no new enabling capability was established; it changes worker `CLAIMS*.json` files, not canonical top-level cards |
| #101 | merged | 436 | N877–N879; merged 2026-10-15 |
| #102 | merged | 638 | N880–N884; merged 2026-10-15 and reflected in the pinned main base |

The current base contains N880–N884. Those routes should be referred to by their exact canonical IDs in any material-update notices; their historical card/status bytes should remain unchanged.

## Repository contract and smallest compatible route

Repository instructions read: `AGENTS.md`, `00_START_HERE.txt`, and `state/CONTINUITY.md`. The practical requirements are to preserve source bytes and their provenance, append scoped corrections rather than rewriting prior claims, keep open obligations explicit, and avoid presenting hashes/indexing/replay as scientific validation.

Root's source-preservation commit already places the 57 incoming original files under `updates/GA-conformal-causal-genesis-20261016/package/originals/`, with its manifest and README under the same update. The manifest records the 57 exact inputs, including the byte-identical physical-report pair and the 54-file mathematical packet. Its paths are relative to `package/originals`; source-catalog records and evidence locators need full repository-relative paths. Preserve those source bytes in place. The generator accepts records for only the indexed evidence actually cited by the new cards; it does not copy the package archive again.

The original preservation receipt is `updates/GA-conformal-causal-genesis-20261016/SOURCE_MANIFEST.json` and must stay byte-identical. The renderer's separate selected/indexed-source manifest is named `INDEXED_SOURCE_MANIFEST.v0001.json`. It performs a final create-only collision pass over every staged overlay file, including update-local manifests, before writing the external stage. Historical N880/N884 status rows and sidecars are not edited; any scoped reciprocal material updates belong in newly appended semantic notices.

The existing canonical data shapes are illustrated by current N884 and FZ's `updates/FZ-positive-memory-genesis-20261016/build_integration.py`:

- New card bytes go to `cards/<full-id>.txt` and `frontier/review_cards/<full-id>.txt`; the exact same bytes are hashed into `frontier/cards/<full-id>.json`, `indexes/claims.jsonl`, and `indexes/agent_catalog.json`.
- Claim records are appended to `indexes/claims.jsonl`; source metadata to `indexes/source_metadata.jsonl`; status rows to `frontier/CURRENT_CLAIM_STATUS.jsonl`; open gates to `frontier/OPEN_PROOF_GATES.jsonl`; notices to `agent/SEMANTIC_NOTICES.jsonl`; source/card rows to `web/documents.jsonl`.
- Append array entries, preserving all old values and order, in `indexes/agent_catalog.json` (`claims`), `indexes/agent_graph.json` (`nodes`, `edges`), `web/catalog.json`, and `mechanisms/bridge_candidates.json` (`bridges`, `rejected_transfers`). Add new lookup terms to `indexes/query_aliases.json`.
- Create source/card pages in `web/pages/`, gate sidecars in `frontier/gates/`, and bridge sidecars in `mechanisms/bridges/`. `frontier/build_access.py` regenerates the public access projections, including dossiers/connections and gate/bridge indexes, from those canonical rows.

`frontier/build_access.py` requires identical claim IDs across claims/status/catalog and consistent card hashes. Graph endpoints, gate/notices/bridge card references, and route IDs also need to resolve. FZ's `protected_baseline.py` provides the read-only integrated baseline check for immutable files, byte-prefix registries, append-only array order, aliases, ancestry, current HEAD, and optional live `origin/main`.

## Stage-only renderer

`build_ga_overlay.py` is a small standalone renderer. It has no apply mode and refuses to write inside the repository. It reads root-authored canonical records from an external `claim_config.json` and writes an overlay plus append deltas and a hash plan to a new external output directory. It checks the clean working tree, exact expected HEAD, immutable base ancestry, live remote main, baseline preservation, route availability, source hashes/bytes, inclusive evidence line ranges, source-catalog path/hash/ID matching, card/status hashes, ID collisions, open gates, and scoped bridge evidence before producing the output.

The config contract is:

```json
{
  "schema": "astra.ga-claim-config.v1",
  "intake_id": "GA-conformal-causal-genesis-20261016",
  "pins": {
    "base_revision": "f80a8f15137575133ad2c9af975513b32e8fa93e",
    "expected_branch_head": "f116469ee41bdc54a155099175b8ce063be98edd",
    "expected_remote_main": "f80a8f15137575133ad2c9af975513b32e8fa93e"
  },
  "sources": [{"source_file": "optional absolute or config-relative file", "record": "canonical source metadata object"}],
  "cards": [{"id": "N885-...", "title": "...", "topics": ["..."], "card_text": "exact root-authored card bytes", "status_record": "canonical current-status object"}],
  "gates": ["canonical open gate objects"],
  "notices": ["canonical unreviewed scoped notice objects"],
  "bridges": ["canonical scoped bridge objects"]
}
```

`cards` is deliberately variable-length: IDs must use distinct, currently reserved numeric routes among N885–N888, and the status record must point to the exact card bytes and indexed proof sources. Source records need the existing `source_metadata.jsonl` fields (`source_id`, `path`, `title`, `sha256`, `bytes`, `date_version`, `read_depth`, `reported_verification`, `extraction`, `provenance_role`, `source_handling`). Root supplies all scientific text, status records, gates, notices, and bridges; the renderer does not draft or infer scientific content. Positive bridge states require explicit transfer-proof references; rejected/refuted transfers need their relevant source/counterexample references. Gates remain open, and external correctness, priority, physical capability, formal verification, and empirical confirmation remain `UNKNOWN`.

The renderer stages these deltas only. Root separately handles the checkpoint draft outside the immutable tree, the requested workflow trace, and technology-record update. No checkpoint is published by this generator.

After root reviews and applies the staged records to the checkout, the deterministic access commands are:

```sh
python3 frontier/build_access.py build --base-revision f80a8f15137575133ad2c9af975513b32e8fa93e
python3 frontier/build_access.py check --base-revision f80a8f15137575133ad2c9af975513b32e8fa93e
```

These build/check commands validate projection and metadata consistency within their stated scope; they do not certify the scientific statements. Do not run them against the current checkout before root applies the integration.

## Preparation checks and limits

The renderer passed Python AST parsing and `--help`. Its pin check passed against the current clean branch: base f80a8f…, expected branch HEAD f116469…, and live remote main f80a8f…; the inherited baseline checker found no historical paths changed from the immutable base. Route checks reported all four IDs free. The full renderer was not run because root's `claim_config.json` has not yet been supplied. No `build_access` command or scientific validator was run.
