# Fresh matched subregion baseline precommit

Frozen before production, 2026-11-05 UTC. Goal: complete the conventional splitting ladder on the existing distance-21 target, not certify MCMC mixing or claim equal-confidence time.

- Same target graph and dyadic edge probabilities as qec_fault_tuple_20261105/d21, fixed integer 4/5 MWPM, edge insertion order and PyMatching 2.4.0. Single logical parity output replaces the correction-edge output; 4,000 random pattern checks agree.
- Use published Mullan–Weippert–Brown independent heat-bath subregion update with region rate 1/ceil(d/2), a tuning heuristic only. No imported/executed upstream rare-event source. New implementation batches independent chains, uses sparse envelope Bernoulli sampling, packed syndromes, and parity-only decoding.
- 20,000 fixed independent anchor shots at common-log-odds tilt log(8), then separately rejection sample 16 independent failing starts. 31-rung ladder, decrement .8/sqrt(sum(q(1-q))), identical to the earlier comparator. Terminal states warm-start lower rungs.
- 16 independent chains per rung, 1,000 burn-in plus 2,000 retained proposals; log every completed rung and save all weight traces. Production stops after complete ladder or cooperative 1,200-second cap at rung end. A partial run produces no target estimate.
- Bennett ratios pooled across chains; uncertainty diagnostic from complete per-chain ladder log ratios plus anchor variance. Report nominal 99.9% Student-t/delta intervals, Rhat and IAT; all exclude possible mixing bias and are not familywise confidence certificates. Keep covariance from repeated rung use.
- Source/header/optimization validation cost, setup/anchor, all rungs, analysis, peak RSS and separately prior development will be disclosed. Exact arithmetic auditing is not attributed to this floating baseline.
- Independent component checks: rational tiny-kernel/BAR proofs already recorded in qec_fault_tuple_comparison_20261105; fresh packed incremental-syndrome checks, sparse Bernoulli full-small-space distribution check, and parity-output matching comparison.
- Do not use candidate-generated failures or target probability intervals to initialize or tune.
