# Aggregate-resource whole audit

**Scoped PASS**, separate from the frozen pending author package. See
`WHOLE_PROOF_CODE_AUDIT.md` for the complete proof/code review and precise scope.
No frozen input was edited, no new external source was retrieved, and no numerical
expansion of the actual mass/global head was performed.

Main independent canonical receipt: 1,351,671 bytes, SHA256
`3be6e9012fb166f56a1e9ea085c809a657b477f08c80da9792bdd9473c54bc85`.
Main K: 29,729,394,962,313,506,647, retained as a factored closed head.

- `INPUT_BINDING.json`: all 89 files in the supplied binding union, including 82
  author-manifest entries.
- `independent_aggregate_receiver.py`: no author imports; new raw deletion,
  aggregate constants, full receipt receiving, executable arithmetic AST,
  pointwise combined h/generator, bounded-power and nested-head decisions.
- `retained_independent/`: three unchanged earlier independent primitive files;
  their reuse is explicit capital, not inheritance of the new theorem.
- `MAIN_NESTED_AST.json`: exact executable main expression, not expanded powers.
- `INDEPENDENT_RESULTS.json`, `GRAPH_DOMAIN_RESULTS.json`,
  `NESTED_FRACTIONAL_RESULTS.json`, `COMPARATOR_RESULTS.json`: exact check results.
- `author_replay/AUTHOR_REPLAY.json`, `supplement.stdout`: byte-identical author
  output replays.
- `STAGED_REPLAY.json`: relocated source-bound independent replay evidence.
- `FINAL_AUDIT_MANIFEST.json`: final audit artifact hashes and verdict boundary.

Assertions-enabled Python is required (not `-O`). From this audit directory:

```
PYTHONDONTWRITEBYTECODE=1 python exercise_independent.py
PYTHONDONTWRITEBYTECODE=1 python graph_domain_controls.py
PYTHONDONTWRITEBYTECODE=1 python nested_fractional_controls.py
PYTHONDONTWRITEBYTECODE=1 python comparator_controls.py
PYTHONDONTWRITEBYTECODE=1 python reproduce_staged.py
```

The first four scripts write their named results into their own audit directory,
never the source. `AGGREGATE_SOURCE_DIR` may name a verified relocated source.
`reproduce_staged.py` stages the complete bound input union plus the necessary
independent files under a fresh `/tmp` directory and compares the three main
independent result files and AST byte-for-byte. Its source recheck is mandatory.

Synthetic small heads/cutoffs validate component lemmas only. Actual-K local tail
checks do not claim to instantiate the unexpanded global cone. Budget refusals
retain qualitative/symbolic information; they do not establish instability.
No general WR, practical-tail, source-process-clearance, historical-novelty,
macroscopic recovery-time or operational-chemistry claim is part of this verdict.
