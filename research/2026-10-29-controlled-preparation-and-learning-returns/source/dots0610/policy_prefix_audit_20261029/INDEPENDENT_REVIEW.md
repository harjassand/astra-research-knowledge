# Independent review: tolerant policies and calibration-prefix tradeoffs

2026-10-29 04:58 UTC. Verdict: **accepted as conditional source-model computations and exact policy/cap algebra at the stated scope**. No new hardware, acquired optimal-control, unrestricted unknown-noise or global-optimality result is accepted. Files are hash-bound separately. The reviewer did not author the policy or prefix construction.

## 1. Embedded CP chain is chronologically correct

For private service probability s>0 and trace-nonincreasing test-pass CP map Tpass, G=sum_k[(1-s)Tpass]^k converges in completely bounded trace norm, since its kth term norm is at most (1-s)^k. Thus the inverse representation is legitimate and CP. The chronological event maps are S=s Svc G and F=(1-s)Tfail G, where the rightmost G contains all passed tests BEFORE the next service or failed test. The expected number of native calls to that event is trace G applied to the entering unnormalized bath state, including the terminal event call.

For a service epoch, r allowed failed tests precede the service, so its map is S F^r, not F^r S. The lower triangular failure-count transfer uses this correct order. Its cost row sums trace G F^r over all allowed failures, including the last epoch that terminates in abort. Augmenting with a cost accumulator and raising to J gives acceptance and expected calls with no bath reset or independent-event approximation.

An independently written native-call recursion, retaining service count, failure count and the full bath density matrix, was compared with the compressed evaluator in eight noncommuting CP fixtures. The unresolved survival tail after 600 calls was negligible and both acceptance and cost agreed below 1e-11. All 716 actual expanded-grid rows were subsequently replayed through that validated evaluator and reproduced exactly in this runtime.

## 2. Exact soundness parameters, not a numerical rare-tail certificate

For R equal to bad-service/test-failure hazard ratio, the negative-binomial bound is the probability that at most b test failures occur among t+b+1 relevant events. The displayed rational binomial sum is correct. Every one of the 716 rows was independently checked with Fraction arithmetic: stored tail, target <=1/128, minimality of t, service-probability relation, outer-code dimensions and exact integer cap. This verifies new parameter choices, not a fresh proof of inherited guard or arbitrary-error outer correction theorems.

Four winners are indeed maxima of the reported finite admissible grid, and all lie at its largest length B=2047. Therefore neither a global optimum nor an asymptotic optimum is established. Exact source matrices were used to evaluate/select these policies; the deployed counter/coin controller itself is simple, but no method for learning the optimal policy from unknown-noise observations is supplied.

## 3. Finite caps

Before absorption, surviving beyond r calls implies fewer than J service coins. With r s>=2J, the binomial Chernoff estimate exp(-r s/8) is valid. N=ceil((2J+256)/s) satisfies the condition. Summing that bound from r=N onward gives the stated expected-call truncation bound. Aborting at the cap cannot increase accepted bad mass. The positive exp(-700) floor conservatively overestimates still-smaller analytic cap corrections.

Important numerical scope: serialized fields named finite_guard_payload_per_call_lower/upper are floating evaluations of analytic formulas, NOT outward-rounded interval-certified numerical endpoints. Floating probability errors are much larger than some cap corrections. The manuscripts disclose this; do not later quote their last digits as rigorous finite-rate bounds. The all-input accepted-operation error bound instead comes from exact parameter arithmetic and the governing theorem.

## 4. Prefix acquisition and retained bath

The learner uses only each prefix's counters divided by that prefix length, followed by the same singular-vector rounding. Exact rotations and conditional bath states appear only in source/evaluation diagnostics, not as learner inputs. The wrapper adds copy snapshots without additional random calls or changes to source/measurement chronology. The original training-script hash matches the receipt. Final million-call counters and bath match the earlier retained bank exactly. This review did NOT rerun the million-call acquisition; it checked its source/provenance and rebuilt every prefix CP map from the frozen bank. All rebuilt arrays matched exactly and all 30 branch Choi matrices were positive within numerical tolerance.

For b=0, the accepted map S^J, terminal map S^J+F sum_(j=0)^(J-1)S^j, and call row trace G sum S^j have the correct order. A separate backward recursion End_J=F+End_(J-1)S and cost_J=trace G+cost_(J-1)S reproduced all ten prefix/method terminal maps. End is TP. Applying End to the actual prior attempt's bath, rather than repeatedly using the training-end bath, is the correct unconditional retained-memory evolution under the stated fixed policy and source.

This independently reproduces the 2,032-attempt crossover and the one/1,000/10,000-attempt rates. The result is a ratio of expected accepted payload to expected native calls, conditional on one sampled training history and an explicit post-training switch to U0. It is not a training-average guarantee, an inferred future-noise law, or an expectation of the realized rate ratio. Repeated attempts also must not be interpreted as safely retrying the SAME unknown quantum payload after rejection: the accepted-operation theorem does not promise safe data recovery on abort. Fresh attempts/resources and retained bath propagation are the evaluated interface.

The one-million small-policy uncapped acceptance 0.929018292 differs slightly from the old cap-500 value about 0.929007225 because the stopping/cap model changed, not because the learned map or bath was silently changed.

## 5. Workload dependence is essential, not optional

The two selected large-block policies are frozen from the million-call benchmark and applied unchanged to earlier prefix maps. Replaying them gives six-state acceptance 2.13458645e-6 at 100k calibration calls and 0.98812804 at 1m; matching gives 6.09814e-17 and 0.95455824. Thus the 100k prefix's calibration-inclusive advantage for the small 35-qubit task cannot be transferred to 22,517 services. It is correct to retain both findings rather than declare one universally best training duration. Very small numeric zeros remain potential underflow, not impossibility proofs.

## 6. Resource accounting and comparators

Training is charged once as m full-array calls, then actual guard calls are accumulated. Dividing by four gives physical input-qubit exposures for this n=4 fixture. This is not a gate-time, memory-error, energy, net capacity or complete hardware utility measure. The conventional six-state operation remains strongest in the reported native-call grid.

The simplified inner-control break-even 0.0737843698 reproduces from matching/six-state throughput ratio rho and matching service fraction s: matching test relative cost must satisfy s+(1-s)c<rho. It excludes source duration, outer operations, storage, routing and acceptance-dependent payload preparation. It establishes no measured advantage. The dense outer-transform budget is explicitly a sufficient construction upper bound, not a lower bound or an executed large compilation; subsequent structured-compiler work must be reviewed separately and may supersede that cost.

For repeated attempts with finite caps, the stated A exp(-Ns/8) path-coupling and A² exp(-Ns/8) accepted-count differences are valid conservative bounds. The uncapped total expected-call denominator still needs separate truncation/coupling accounting for a rigorous finite repeated-rate statement, as the prefix manuscript expressly notes. No such missing denominator estimate is silently accepted here.

## Accepted evidence and remaining obligations

Accepted: exact policy algebra; CP event summation; finite-cap inequalities; finite-grid numerical rankings; source-known prefix/bath computations; workload and calibration-cost qualifications. Remaining: confidence-certified learned policy selection, training-history averages, interval-certified yield numbers if required, complete large-code implementation and calibrated physical resource advantage. No historical novelty claim is assessed.

Reproduction files: independent_checks.py/.json; map_and_provenance_checks.json; full_grid_replay.json; author_map_replay contains a copied map builder and frozen input bank. Original scientific sources were not overwritten.
