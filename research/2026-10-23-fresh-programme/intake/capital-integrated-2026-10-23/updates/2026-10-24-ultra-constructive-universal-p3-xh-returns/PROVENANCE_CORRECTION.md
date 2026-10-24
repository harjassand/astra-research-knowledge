# Provenance correction — 24 October 2026

The N936 capacity-boundary update in `frontier/CURRENT_CLAIM_STATUS.jsonl` now cites its selected XH1 completion report, source ID `src-xh1-partner-operation-2131`, at `source/XH1_completed_partner_operation/XH1_physical_partner_operation_completed_2131_20261024.json` (SHA-256 `7e3aeb46f94ba8d88ea44a8ec3d1816f3822792d560e50509e06fe3a4128f885`). This replaces an incorrect evidence pointer into XH2 receipt rows.

The correction changes provenance only. N936 remains `source_derived_unreviewed`; it does not promote the reported mechanism, physical capability, correctness, novelty, or practical advantage. The previous v3 access snapshot and its checkpoint evidence remain unchanged. The current access projection, retrieval command, and publication check use v4.
