# Ordinary goal-specific comparator — separate frozen review boundary

**Useful result:** the original goal is certified at regret <=0.056432233
against all microscopic/history policies, with 812,951,680 prospective source
calls, versus the earlier block-history regret 0.056505304 and 3,298,951,680
sufficient calls. Both failed prefixes, all row acquisition and 18 million
actually simulated evaluation transitions are paid. This defeats a necessity
claim for the earlier ledger; it does not invalidate its wider uniform
operator/compatible-goal certificate. No new major capability is claimed.

Start with `PROOF.md`. The interval-MDP candidate itself gives only .069282921;
the ordinary maximum goal-entry hazard bound plus fresh policy evaluation gives
the final result. The goal is fixed, not selected adaptively for free. The
chosen controller remains block-Markov; stronger microscopic policies occur
only in the comparator upper bound. Physical sensing and iid provenance are
not established.

## Nonmutating reproduction

From this directory, with the existing Python/numpy/sympy environment:

```
python -c 'import check_comparator as c; print(c.run())'
python -c 'import check_source_transport as c; print(c.run())'
python -c 'import goal_hazard as g; print(g.run())'
```

The first command reproduces candidate acquisition and all 18 million forward
transitions, checks saved values/policies/costs exactly excluding timing, then
runs explicitly cached receiving-negative probes. It does not modify files.
Directly executing a script's `__main__` writes its own result file, so use the
commands above to preserve frozen originals. No software installation required.

## Observed checks and storage

- 17,026 exact checks + 16 negative receiving checks.
- 8,192 source argument laws compared in exact rationals (16,384 assertions).
- Maximum observed transport L1 error 1.903e-16; paid reserve 1e-9.
- 4,608 interval Bellman products over three attempts, plus sorting and all
  count/radius arithmetic; maximum serialized rational component 2,052 bits.
- Reused full compressed transcript 4,167,029 bytes (conservatively retained,
  although outgoing entries are unused), interval result 375,558 bytes,
  hazard result 9,540 bytes, endpoint bits 93,750 bytes.
- Simulator private O(n*degree) state, learner block map, public task, table,
  source/count files and verification work are additional, not a tiny complete
  retained machine. Original acquisition is never refunded.

`COMPARATOR_FREEZE_MANIFEST.json` binds current files and exact dependencies.
Old untransported-envelope bytes and the NumPy-integer alias failure in the
source audit are retained under clearly historical directories. They are not
passing current certificates. Old accepted archives are unchanged.

Whole independent review is requested separately; a new receipt, if issued,
binds this freeze rather than retroactively extending old receipts. This is a
local scientific checkpoint only, with no upload/publication.
