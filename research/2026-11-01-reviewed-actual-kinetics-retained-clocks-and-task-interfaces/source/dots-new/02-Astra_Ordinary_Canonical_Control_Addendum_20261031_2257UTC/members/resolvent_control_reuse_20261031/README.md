# Reusable control without predictive aggregation — new review candidate

The central new result is `ROBUST_CLOSURE_SUCCESS.md`: a finite-observation
certificate of approximate baseline action-effect closure earns an ordinary
small rational LP for EVERY later bounded block-compatible reward/cost table,
without an exact closure promise or a Markov predictive quotient. It derives
both coefficient stability and the positive LP-objective margin from actual
stochastic-source structure. The resulting policy is near-optimal pointwise
against microscopic/history control in the stated fully observed discounted
MDP. This is NOT hidden-state inference or a physical sensing/preparation claim.

`PROOF.md` supplies task/interface, exact-class motivation, general posterior
receiving, truncated geometric endpoint acquisition, confidence, partition
refinement from native reward labels, finite-bit/cost scopes and limitations.
Its original robust LP success theorem is conditional on exact closure; the
primary strengthening removes that premise under its acquired scalar margin.
`COSTS_AND_SCOPE.md`, `EXECUTION_SCOPE.md` and `PRIOR_AND_COMPARISON.md` are part
of the scientific scope, not optional caveats.

## What is and is not earned

- No useful partition is passed to the acquisition trace: start from actual
  native reward labels, then receive every effect-based refinement and failure.
- No inverse of R=WH, reduced fixed-point contraction, optimal teacher or generic
  nonlinear root oracle is assumed. The consumer is an explicit r-variable LP.
- One complete confidence event supports arbitrarily many adaptive future goals.
  All named-row sampling, source calls, finite episode caps, failed attempts,
  data receiving, map storage and actual deployment sensing/execution are paid.
- Core later planning avoids ambient n only AFTER acquisition/full receiving.
  The small core holds a map hash; the actual n-state map is separately retained.
- SF, ALP/constraint aggregation, value equivalence, Bellman-rank and hidden-K
  complementarity are strong ordinary priors. In particular the abstract positive
  objective-row LP criterion is an established hidden-K result. No historical
  novelty or exclusive advantage over ordinary methods using this certificate.
- No consequential empirical advantage or economical large-scale workload is
  demonstrated. The theoretical schedules can be prohibitive near gamma=1.

## Executable evidence (nonmutating commands)

Run from this directory with Python, NumPy/SymPy already available:

    PYTHONDONTWRITEBYTECODE=1 python -c 'import check_control as c; print(c.run())'
    PYTHONDONTWRITEBYTECODE=1 python -c 'import check_uniform_control as c; print(c.run())'

Currently 182 exact checks + 13 refusals, then 208 additional checks + 5 refusals.
The second harness includes unequal blocks, nonsymmetric and randomized
selectors, wrong-objective and divergent-iteration failures, action-dependent
rewards, and a truly nonclosed source with positive actual policy regret
3/59996 <= certified posterior 1/3750. These are algebra/receiving checks, not
performance benchmarks. Large successful count arrays, including the two-round
refinement trace, are FABRICATED deterministic UNIT TESTS, never observations.

    PYTHONDONTWRITEBYTECODE=1 python -c 'import check_episode_protocol as c; print(c.run())'

This reruns 4,096 actual software-source episodes / 38,626 forward calls on the
OLD four-state nonpredictive counterexample. It correctly returns UNKNOWN at
0.01 regret. All actual microscopic paths are saved in
`episode_micro_paths.json.gz`; their canonical hash is in the result. Replays
cost additional source calls and do not supply independent new evidence.
The theorem's iid/provenance premises are external; the test uses a seeded PRNG.

The primary LP backend is ordinary SymPy rational simplex, with separately
checked exact primal/dual equations and grouped dual weights. Its wall work and
input/output entry bits are reported; no polynomial worst-case simplex or full
internal-pivot bit ledger is claimed. Standard rational LP theory supplies the
polynomial consumer in the mathematical construction.

## Current versus historical

Current: PROOF.md, ROBUST_CLOSURE_SUCCESS.md, control.py and the three harnesses,
saved results/path evidence, the cost/execution/prior files, this README.
`FIRST_CONSTRUCTION_UNREVIEWED.md` is the initial stronger raw-factorization
foothold. `HISTORICAL_TOPOLOGICAL_FALLBACK_DRAFT.md` is an exploratory alternative
existence/fallback argument, not needed for the primary ordinary LP consumer.
Neither historical file overrides current receiving or reward scopes.
All earlier accepted packages remain unchanged. Local only; no uploads.
