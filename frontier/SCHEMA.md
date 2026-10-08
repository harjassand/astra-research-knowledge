# Frontier schema v1

`CURRENT_CLAIM_STATUS.jsonl` has exactly one record per existing card. It is a view of the evidence, not a replacement theorem ledger. Retrieve individual records or the per-card sidecars; do not preload this file.

- `card_id`, `card_path`, `card_sha256`: immutable card identity and exact byte hash.
- `claim_status`: verbatim existing `indexes/claims.jsonl` status. A new timestamp or a later claim never promotes it.
- `reported_status`: verbatim card status line. This keeps source-reported internal checks distinct from checks executed at ingestion or during another research run.
- `proof_availability`: separate evidence inventory. Its classification is one of the values below; it never asserts proof validity.
- `validation`: reports the limits of this restructure. It does not erase source-scoped formal declarations, finite checks or internal proof receipts; reopen the cited source for their exact scope.
- `supersedes`, `invalidates`, `depends_on`, `requires_external_validation`: arrays of objects with `target`, `scope`, `relation_status`, and `evidence`. Targets can be full card IDs or explicitly named external/interface nodes. Existing declared dependencies are retained, not independently validated.
- `material_updates`: reciprocal notices on affected older cards, plus explicit source-backed state corrections. Read these before historical blocker metadata. This is a curated subset; an empty array does not establish that no later correction exists.
- `contrasting_blockers`: preserved scoped obstruction routes. A blocker’s historical wording is not automatically current, and must not override a newer explicit correction notice.
- `relation_coverage`: acknowledges that exhaustive theorem-dependency reconstruction has not occurred.

Availability classifications:

| Value | Meaning |
|---|---|
| `summary_only_at_original_cited_version` | The card explicitly states its linked full proof/packet was absent. Its cited summary is available. This does not assert that no related proof exists elsewhere. |
| `proof_text_located_not_completeness_audited` | The named technical proof passage is present in indexed source text. Completeness, every subclaim and imported premise, correctness, and priority have not been audited by this restructure. |
| `provisional_manuscript_available` | The original provisional manuscript is available, separately from its reported validity and later correction notices. |
| `cited_source_inventory_available_proof_scope_unclassified` | Cited source texts are available; per-subclaim proof completeness has not been classified. This must not be displayed as either “full proof verified” or “proof absent.” |

Every evidence pointer contains repository-relative `path`, `sha256`, inclusive `lines`, `range_scope` and `read_path`. For indexed sources it also contains `source_id`, and when available, the exact original byte hash/object path. `sha256` denotes indexed UTF-8 text when `hash_kind=indexed_utf8_text`; PDF discovery text is distinct from its original PDF bytes. Whole-source inventory ranges explicitly disclose that finer claim-to-proof mapping remains unclassified.

Relations are scoped. `target_component` identifies a local part of a card or branch, and `whole_claim_invalidated=false` forbids propagating the notice as a whole-theorem refutation. In particular, the N65 point/label correction concerns AE cycle7 actual-origin blocks and dependent audits, not a refutation of N65. The N47/N129 notice concerns the conjunction of torsion-free hyperbolicity and group-ring direct-finiteness failure, not separate nonsofic constructions. State-reported primary-literature reconstructions are not newly externally verified by this metadata build.

`OPEN_PROOF_GATES.jsonl` contains nine selected open decisions with `gate_id`, `priority_order`, `card_ids`, exact question/pass condition, priority rationale, and immutable evidence. The order prioritizes documented evidence/control failures and explicit restart obligations; it is not a predicted ranking of scientific impact. `completion_evidence=[]` means the restructure did not close the gate. Closing a gate requires scope-specific new evidence and retaining its prior record.

Regenerate this layer with `python3 frontier/build_frontier.py` from the full local knowledge snapshot (requires its SQLite database and exact source objects). The static GitHub edition uses `python3 frontier/retrieve.py` for lookup; it cannot rebuild source inventories without the full snapshot. The builder opens SQLite read-only and writes only frontier files; explicit curation is in the builder. `BUILD_VALIDATION.json` pins its inputs and card snapshot. This command generates navigation metadata and does not replay scientific scripts, run Lean, prove general theorems, establish historical priority, or authorize archived restart instructions.
