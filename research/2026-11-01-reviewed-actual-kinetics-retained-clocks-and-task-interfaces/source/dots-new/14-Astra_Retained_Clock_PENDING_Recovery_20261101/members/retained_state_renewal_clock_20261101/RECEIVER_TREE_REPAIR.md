# Separately frozen malformed-certificate repair

After exact recovery, the independent whole reviewer found that public Python
`verify` applied recursive `proof_record` to an unexpected depth-1100 dict and
raised RecursionError rather than UNKNOWN. No false mathematical certificate
was accepted. The original exact source (SHA 4c4e7d10...2c92a9), all 24 recovery
payloads and the c292c4d2... recovery-v2 descriptor were preserved byte-for-byte
in `pre_tree_guard_snapshot/` before any source edit.

The current receiver adds an iterative proof-tree guard **before** expensive
raw/scalar recomputation. Its public Python certificate contract is now:

- at most depth 64 and 100,000 visited proof nodes;
- string dictionary keys and ordinary JSON scalar leaves;
- no cycle or shared-container graph in proof fields;
- diagnostic `seconds`, `work` and `display` values remain ignored and are
  not traversed, because the recursive proof comparison also omits them.

Malformed shapes fail with UNKNOWN. Valid producer certificates remain in the
admitted class. This is a finite receiving/resource interface, not a security
claim about arbitrary hostile Python objects or code execution. The numerical
formulas, physical model, initial-law target and probability widths are
unchanged. All 2,503 author checks were actually rerun on the repaired source,
plus 18 focused checks including the exact depth boundary, cycle/alias inputs,
early failure before recomputation, ignored diagnostics and a small real replay.

An attempted shell write of the focused test initially used a redundant path
prefix under the already-selected directory. The target was not written by
that command. It was then written using an explicit absolute workspace path
before the scheduled focused test executed; the actual test run passed. This
orchestration correction does not change a scientific source or a test result.

The governing new descriptor is `FROZEN_SHA256_RECOVERY_V3.json`. Whole
executable acceptance is still pending. The historical v1/recovery-v2
descriptors remain historical and must not be confused with this repaired
receiver. The older independent replay and lost independent suite are not
relabeled as a whole audit of this new source.
