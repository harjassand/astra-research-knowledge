# Matched prior-art and finite-budget QEC comparison

## Verdict

The witness calculation has a meaningful **finite-confidence specification advantage** over the inspected MCMC/splitting methods: its retained trials are independent Bernoulli observations with an exact proposal normalizer and an explicit omitted-witness bound, so it does not need an MCMC mixing assumption. The public mcmc4qec implementation expressly does not guarantee finite-time mixing or nominal interval coverage.

The present comparison does **not** establish a speedup over the upstream software, an optimal tuned splitting implementation, or every established importance sampler. Upstream source was inspected read-only, not imported or executed. The numerical runs below independently implement the published kernel/BAR equations on exactly the candidate's public graph and decoder. Their fixed budgets did not establish convergence or match the candidate's precision. Their times are therefore not measured times to the candidate's accuracy.

## Acquired comparator and scope

- Haruna and Murakami, *Fast and accurate rare-event simulation by Markov chain Monte Carlo for general quantum codes*, arXiv:2610.35498v1, https://arxiv.org/html/2610.35498v1 . Its direct benchmarks concern conditional **mean fault weight**, not finite-confidence logical failure probabilities. Section VI.2 extrapolates logical-error estimation costs under stated assumptions and charges the full ladder. It explicitly says faster mean-weight estimation does not itself imply faster logical-error estimation.
- Official code: https://github.com/junichiharuna/mcmc4qec . Read-only files pinned to tag v0.1.0.dev6, commit f6726d0628c84ed7ec837bfa6ac4907981671cfd. See UPSTREAM_PROVENANCE.json and upstream_readonly/.
- The source supplies square-root locally balanced single-bit proposals, a weight-preserving exchange of two occupied and two empty locations, and BAR ratio estimation. The paper's default mixture is70% locally balanced and30% exchange. Its surface-code comparisons also require ordinary single-bit MH and pure locally balanced proposals: cluster moves can add overhead where trapping is absent.
- The package's default BAR interval is a95% circular-block-bootstrap/delta-style interval. Its source and release notes warn that mixing bias is not included, healthy diagnostics do not guarantee coverage, and published tile-study95% intervals covered only151–176 of192 runs. Those tile results are not evidence of failure on the present surface code; they are explicit limits on a general coverage claim.
- The paper already places rare-event splitting in the established Bravyi–Vargo2013 lineage and notes circuit-level simulations below10^-20. Merely reaching an extremely small modeled probability is not a new capability by itself.

## Matching contract

All numerical comparisons here use the same current Model construction as canonical_qec_witness_20261105: unrotated planar distance13,313 data qubits,156 ideal X checks, independent Z flips of probability0.001, integer unit matching weights, the same PyMatching2.4.0 object construction, edge insertion order, and deterministic tie behavior. This is a specified code-capacity model, not measured hardware noise. No reserved or held-out decoder files were read.

The independent implementation uses an incremental syndrome, exact logical-failure predicate, and a correction-parity cache keyed by syndrome bytes. The cache is shared across chains within a rung and reset for the next rung. It is an optimization of the mathematical comparator, not a claim to reproduce upstream timing. Float probabilities and seeded NumPy random streams are used, as is conventional for the comparator; the numerical MCMC intervals are not outward arithmetic certificates.

The common ladder has23 rungs from0.15 to0.001, selected before the chain runs from code size and noise only. Its50,000-trial independent anchor returned20,315 failures, estimate0.4063, and cost2.9491s. Each cold-start kernel used8 independent chains per rung,8,000 retained steps after1,000 burn-in steps. Starts alternate full straight logical strings and known minimal failing prefixes on different rows. A predeclared stronger follow-up used16 pure-Zanella chains, exact rejection-sampled failure-conditioned starts at the top rate, and terminal-state warm starts down the ladder, with the same retained length and burn-in. No candidate-generated conditional samples were supplied to the baselines.

Independent checks exhaustively cover all8,192 distance-3 patterns, prove the MH detailed-balance identities by rational arithmetic over55,552 directed failing-neighbor checks, check2,000 incremental syndrome/failure updates, and verify BAR against exact enumerated conditional distributions. The distance-3 one-bit failure graph is connected. These checks validate the implemented operation but do not certify distance-13 mixing.

## Recorded finite-budget results

All intervals in the following MCMC rows are **nominal99.9% Student-t/delta diagnostic intervals**, not guaranteed-coverage intervals. Full-chain ladder totals retain the covariance from using each rung in both adjacent BAR ratios. The anchor variance is also charged.

| Method | Logical-failure point estimate | Diagnostic interval | Total seconds including anchor | MH proposals | Actual decoder calls |
|---|---:|---:|---:|---:|---:|
| Uniform one-bit MH |4.3795e-15|[9.7709e-16,1.9630e-14]|17.83|1,656,000|158,302|
| Pure Zanella |4.5938e-16|[2.0932e-16,1.0081e-15]|63.34|1,656,000|1,234,802|
|70/30 Zanella/exchange |5.3136e-16|[2.1316e-16,1.3245e-15]|124.35|1,656,000|1,376,215|
| Warm-start pure Zanella |3.2778e-16|[2.2447e-16,4.7864e-16]|140.81|3,312,000|2,469,614|

For orientation, the frozen candidate d13 result used10,000 independent idealized witness trials,2,752 accepted trials, and an exact99.9% interval [3.6126087840e-16,4.0213154904e-16]. Its recorded time was12.5000s, including10.5571s for exact confidence inversion and1.9281s sampling. This is the recorded original result, not a rerun against subsequent candidate optimizations.

The cached pure-Zanella comparator was faster than the default mixture in this screen. The warm-start follow-up narrowed its interval and overlaps the candidate interval, but did not match its precision. The ordinary one-bit result is inconsistent with the candidate interval at this budget; its poor convergence diagnostics prevent interpreting this as an intrinsic failure of the established method.

All four MCMC runs have unresolved convergence diagnostics. Using a conservative per-rung screen that requires the retained length to exceed50 times the **largest estimated chain weight autocorrelation time**, the numbers of failing rungs are23,16,20,18 out of23. This is our conservative diagnostic, not a verbatim reproduction of the paper's full convergence protocol. Conventional maximum between/within-chain Rhat values are about1.099,1.112,1.069,1.174, respectively. Neither these statistics nor their improvement can certify mixing. The nominal intervals consequently must not be relabeled as matched finite-confidence results.

## What can and cannot be concluded

**Supported:** on this exact specified instance, the candidate has already delivered a finite-confidence probability bracket with an explicit truncation error; the tested established-kernel implementations have not supplied the same confidence/precision specification. The comparison does not rely on direct Monte Carlo at the tiny target rate as a straw-man competitor. It includes locally balanced, exchange, ordinary MH, caching, a charged anchor, the complete BAR ladder, and a stronger warm-start check.

**Not supported:** an upstream mcmc4qec runtime benchmark; a measured time-to-equal-accuracy speedup; optimal splitting tuning; proof that MCMC cannot meet the target; a general quantum-code or circuit-level capability; or a novelty claim against all canonical-witness/union-estimation/importance-sampling literature. Fixed-budget runtimes cannot be extrapolated as if every chain had mixed. The candidate also depends on its geometric failure cover and on its decoder-optimality assumptions, unlike a general black-box failure sampler.

The remaining novelty question is whether this particular efficiently normalized geometric cover and canonical correction on surface-code failures goes beyond established certified union/importance-sampling constructions. That question is separate from the MCMC gap and was not resolved by these runs.

## Artifacts

- PRECOMMIT.md and WARM_START_PRECOMMIT.md: frozen numerical plans.
- independent_mcmc_initial.py: exact initial-screen implementation; independent_mcmc.py adds optional supplied/terminal states for the warm follow-up.
- check_kernel.py, kernel_checks.json: independent mathematical/circuit checks.
- Four *_result.json and *_traces.npz files: complete run outputs and retained weight traces.
- comparison_summary.json: diagnostics and resource ledger.
- candidate_d13_at_comparison.json: frozen candidate reference.
- ENVIRONMENT.json and model_descriptor.json: environment and exact graph/failure contract.
- upstream_readonly/: selected inspected public source/documents as inert text, with the MIT license. They were not executed.
