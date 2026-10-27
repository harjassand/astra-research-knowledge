# Selected-source admission repair

Base: `54b1e0d80cf653a82db573a984020865f2ba7794` (PR242).
This is a source-navigation repair, not a new scientific acceptance decision.

The existing `research/2026-10-27-dot-scientific/SOURCE_INDEX.json`
(`859124526a0ac3671e641463d89355b6ae3363e8e00ef2ab6557d1fefd824001`)
declares 644 already-public originals in `astra.scientific-source-selection.v1`.
The former adapter discovered only `INDEX.json` and two other schemas. The
repair follows each declared `repository_path`, byte count and SHA256, never
its private `original_path`. Missing or malformed support fails ingestion.

All 644 declarations now enter the evidence view. The generated coverage gives
160 exact (public path, hash) originals with existing record citation context
and 484 without. Context routes cover N1093–N1117 and 58 existing units; these
83 IDs are routes, not 83 new discoveries. The study's older 470-hash absence
count used a different denominator and repository pin. Neither count means a
number of missing theorems. Semantic reconciliation remains required.

All 1,921 canonical scientific record objects equal the base records exactly.
No scientific original, review, unit, correction or acceptance is modified.
Original/read-path aliases retain existing correction context, explicitly
without widening a supporting citation range or inheriting acceptance.

## Verification and retained limitations

- `python3 knowledge/build.py build`, then `check`: passed; deterministic views.
- 45 existing agent/core/P3 regression tests: passed.
- Nine admission checks, including a new actual-corpus declaration/bytes test:
  passed (eight fixtures plus one corpus check; overlap with the 45 above).
- Exposed navigation probes, not held-out evaluation: “negative spectral trace
  mass bounded Hessian paid closure” returns the actual
  `FINITE_NEGATIVE_MASS_TO_PAID_DISTANCE.md` at lines 1–63; inspected its
  `dist_W1(mu,C) <= 3 delta + 3 K_delta N` receiving bound and the explicit
  absence of a useful power law or evaluated threshold. “guarded posterior
  control conditional law boundary” returns `GUARDED_POSTERIOR_CONTROL.md`
  lines 1–15 with four existing notices, and its independent audit with the
  exact continuous-controller scope. Source bytes/ranges were read through
  `Library.source`, not inferred from filenames or matching hashes.

The admission repair does not resolve the scientific reconciliation backlog.
The negative-mass original still carries its historical pending-audit label;
its separately searchable later audit is not silently merged into a new
acceptance decision. Evidence search can return duplicate original/read-path
aliases, and coarse lexical ranking remains a limitation. This focused change
makes the declared originals and existing correction routes available to
subsequent semantic curation and compact agent retrieval.

Internal implementation review: inspected schema dispatch, failure paths,
source-version context propagation and actual returned passages; no source
or canonical-record mutation. Regression coverage targets silent omission,
private-origin fallback, byte drift and correction loss across aliases. Full
publication integrity is required on the PR's actual reviewed head.
