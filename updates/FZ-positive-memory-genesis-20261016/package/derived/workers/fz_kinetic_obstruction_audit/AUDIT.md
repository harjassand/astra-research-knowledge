# Independent kinetic packet audit

**Disposition:** retain the reconstructed proposal-family obstructions and reproduction evidence with their exact scope. No foundational invention, efficient new physical capability, benchmark superiority, or certified eight-site probability follows. The work/second-moment inequality has direct exact prior art. The eventual-time moment and work bounds do not transfer unchanged to the implemented deadline-1 splitting experiment.

Audit date: 2026-10-16. Original packet: `/Users/harjas/Downloads/astra_kinetic_investigation`. Repository context verified at `3dde9ce74d829a93388e64032d27351b36dd2221`. This worker writes only inside `research/2026-10-16-positive-memory-genesis-v1/workers/fz_kinetic_obstruction_audit`; it made no source-packet or repository changes and ran no SSA, splitting or FSP simulation.

## Analytic findings

| Claim | Independent disposition |
|---|---|
| CT two-state finiteness iff δ²<κ/[4(1+κ)] | Reconstructed from the path-density second-moment operator and exact determinant/trace. Equality diverges. |
| Clock-marginalized two-state repair | Correct, with exact threshold δ²<(1+κ)²/[(1+κ)²+1], tending to 1/2. It is a special deterministic-internal-routing case. |
| Clock-marginalized triangle threshold | Correct: δ²<κ(κ+2)²/(κ³+4κ²+7κ+4). Exact positive-vector witness replays. |
| General irreducible-routing obstruction | Correct under a row containing two supported destinations with unequal approximation multipliers. Branching or nonconstant approximation alone is insufficient. |
| Local critical stationary-variance coefficient | Correct for fixed S,f: ρ=1-κ+δ²∑π_i Var_{S(i,·)} f+stated local remainder. Periodicity is allowed; no size/gap-uniform remainder follows. |
| Positive absorption at every transient state saves the estimator | False as a general objection: the source examples already have positive success and failure hazards at every state. A uniform escape lower bound is an additional condition. |
| Deterministic/periodic routing exceptions | Explicitly reconstructed. A branching period-two chain with error constant on destination classes has K^0=S and no strict-row instability. Periodic chains with within-row variation still satisfy the theorem. |
| Work/second-moment inequality and sharp optimizer | Mathematically correct; exact prior art is now located in a primary source. It concerns explicit full-path production and normalized second moment. |
| Infinite variance or unavoidable 1/κ work at the actual deadline 1 | Does not follow. Deadline-truncated likelihood moments are finite under the finite-network bounded-rate assumptions. The implemented splitting estimate is itself bounded in [0,1]. Deadline-conditioned work can remain bounded as κ↓0. |

Full reconstructed arguments are in `RECONSTRUCTED_PROOFS.md`. Their finite-horizon replacements, including exact integrated-clock growth, are in `FINITE_HORIZON.md`.

At the packet's illustrative κ=10^{-6}, δ=.01, T=1, the CT Perron growth factor is only about 1.00039912. Exact truncated second moment divided by p_T² is approximately 1,004,410.31 or 995,763.66, depending on the initial state. Even an exact *eventual* committor has normalized deadline second moment 1,000,000.50 because success before the short deadline remains rare. Relative to that baseline, the approximate CT moments are about 1.00441 and .99576. These small-network evaluations do not evaluate the spatial benchmark.

For a fixed finite network the honest positive-growth law is Θ(e^{αT}) as T→∞, with α the second-moment spectral abscissa; at the critical point it is Θ(T). For a routing proposal that exactly integrates the original constant-rate clocks, the sharp order is Θ(T^{-1/2} exp[2q(√ρ-1)T]) when its embedded second-moment Perron root ρ>1. A separate fixed-deadline counterfamily can be obtained by scaling internal rate λ→∞; the corresponding positive exponential rates are proved in `FINITE_HORIZON.md`. None of these establishes the efficiency of an algorithm on the eight-site model.

## Splitting unbiasedness and boundedness

The code's fixed interfaces are nested sets max(n)≤47,45,…,15 in the main saved repetitions. On the augmented state z=(configuration,elapsed time), let H_l be the substochastic kernel for first hitting the next interface before deadline T. Strong Markov continuation from each saved configuration/time makes these the correct physical kernels. Returning immediately when a particle already lies inside the next interface is also correct.

Let γhat_{l-1} be the previous empirical measure multiplied by all preceding survival fractions. Conditional on its particles, independent ideal propagation makes the empirical successful unnormalized measure have conditional mean γhat_{l-1}H_l. If n_l>0, uniform whole-particle resampling from survivors preserves that measure in conditional expectation after multiplication by n_l/N. If n_l=0, the weighted measure and final product are zero. Induction gives E γhat_m(1)=P(τ_B≤T). This proves ideal product-estimator unbiasedness without assuming identical stage success probabilities or independent descendants.

Elapsed times are retained in `x=x[keep]`, `t=t[keep]`. Resetting time would target a different event, but this code does not do that. Whole states are resampled, preserving spatial correlations. The estimator is a product of fractions in [0,1], so its variance is finite and at most 1/4. Shared ancestry and heterogeneous particle success probabilities mean within-stage binomial errors do not provide the final uncertainty law. Independent full repetitions provide descriptive dispersion, not a rigorous tail certificate.

This splitting estimator is not the long-path importance-sampling likelihood estimator used in the obstruction theorem. Neither its empirical dispersion nor its event count can be identified with that theorem's spectral instability or pathwise work lower bound.

The actual reaction model has an unbounded count space and unbounded rates, so a finite-state bounded-rate theorem does not apply to it merely because T is finite. For the ideal process, nonexplosion can be justified separately: diffusion conserves total count, births grow quadratically and deaths cubically with a negative leading drift. A coercive total-count Lyapunov function has generator bounded above, and higher polynomial moments give finite expected reaction work on compact time intervals. This is analytic process control, not an interval validation of the floating implementation. Bounded splitting output already suffices for its moment bound once execution terminates.

## FSP bracket and sampler diagnostic

`fsp_reference.py` builds a column generator on two-site states in [0,cap]² outside B, one absorbing B state, and one absorbing overflow state. Every original transition crossing the cap goes to overflow, with its original rate retained in the diagonal loss. Initial state is (50,50). For cap=120 this gives (121²-16²)+2=14,387 states, matching the saved record. The supplied trace argument is the trace of A*T and is correctly scaled.

Couple the original and FSP paths up to the first box exit. FSP B mass counts exactly hits before overflow; any additional original hit by T must occur on a path that already overflowed by T. Thus the exact-arithmetic inequality is

\[
\text{hit mass}\le P(\tau_B\le T)\le\text{hit mass}+\text{overflow mass}.
\]

The displayed numbers use floating sparse `expm_multiply`, with no outward-rounded or residual-based error enclosure. Their mass-sum defect is a useful diagnostic but is not an error bound on either coordinate. The cap-120 width of about 2.57×10^{-9} is a numerical bracket width, not a rigorous certificate of that width. The packet correctly discloses this. No FSP calculation was rerun in this audit, including the failed cap-100 T=1 attempt.

The two-site T=.2 direct-SSA/binomial and splitting comparisons are implementation diagnostics under ideal Bernoulli/randomness assumptions; they do not validate the eight-site rare tail. A Clopper–Pearson interval for simulated hits does not also cover floating arithmetic error or governing-model error. Optional capped SSA in `kinetics.py` suppresses births/diffusion at the boundary, whereas FSP kills overflowing paths; these are different operations and must not be substituted without a separate comparison.

## Model match, randomness and timing

The executed contract is an unbounded-count 2×4 open lattice, starting at all 50, with first target entry by T=1. The neural article's §I.1 supports counts 0,…,M-1 and its Table 1 uses M=85. Therefore maximum supported count is 84, while saved SSA repetitions reached 109. The article tracks a time-evolving joint distribution. Endpoint occupancy and absorbing first passage differ because the original process can leave B after first entry. Boundary dynamics also need matching, not merely equal nominal M. The published GPU training time is consequently not a matched baseline. The packet already says so; [the primary article confirms these distinctions](https://arxiv.org/html/2512.10309v1).

The mechanistic decimal rates are supplied, rather than acquired/calibrated for a particular physical device. No rate-uncertainty contract, control interface, or measured physical response is demonstrated. A pinned upstream system-file blob does not pin a training environment, and no neural execution is claimed here.

`run_replicates.py` fixes master seeds 8017+1009j for j=0,…,11. Each splitting run creates a NumPy generator, derives one integer Numba seed per stage, and uses its generator for survivor resampling. The saved master seed, particle count, levels and deadline support reproduction under a compatible implementation/runtime. Individual derived stage seeds are not explicitly saved. Distinct master seeds do not establish mathematical independence, PRNG ideality, or a historical preregistration chronology; the source's claim that seeds were set before validation is a producer claim, not independently timestamped evidence in this audit. No result-based seed change was found in the supplied script.

`run_replicates.py` times each call to `splitting`; it excludes imports and JSON output. It has no explicit warmup, so a first Numba compilation/cache load reached inside a timed call can be included. The separate CLI entry point in `kinetics.py` does perform and separately report warmup, but that branch is not called by `run_replicates.py`. Per-stage timers end before survivor resampling; total per-repetition timers include that resampling, including unnecessary final-stage resampling. Saved wall sums are scoped execution measurements, not total research costs, CPU time, peak memory, or acquisition-inclusive superiority. The recorded failed 40-second FSP attempt remains additional work outside the reported replicate sum.

Saved event counts count actual state-changing jumps. They exclude rate-construction work for a holding time that crosses the deadline and do not measure every machine operation. The rates use floating arithmetic and PRNG draws; the exact SSA algorithm's unbiasedness is not a proof of bit-level unbiasedness or interval correctness of this implementation. No new simulation was needed to identify these scopes.

## Evidence and remaining status

- `source_snapshot_before.json` and `source_snapshot_after.json` record every original packet file hash and manifest comparison.
- All 30 entries in the original manifest match original bytes; the additional ordinary file is `MANIFEST.json` itself.
- `replay/verify_algebra.py` is a byte-identical disposable copy. Its 17 source checks passed. `audit_checks.py` independently passed 13 exact checks on fixed matrices, plus numerical evaluations of proved deadline formulas.
- `replay_receipt.json` records hard 45-second limits, paths, exit codes, script hashes and wall times. No run approached its limit. Preserved `*.attempt1`, `*.attempt2`, `*.attempt3` receipts retain audit-harness normalization failures; they were SymPy expression-comparison issues, repaired without source-packet changes. The original script passed on every attempt.
- `metadata_audit.json` checks the saved 12-repetition metadata and exact source-output fields without running the stochastic kernel.
- `PRIOR_ART.md` gives primary-source dispositions. The work inequality/optimizer is direct prior art; historical priority of the exact thresholds and branching/local coefficient is UNKNOWN.

The finite checks support specified identities and witnesses. They are not proofs of all general theorems, formal compiler certificates, independent benchmark reruns, or evidence of model acquisition, scalable excursion contraction, empirical scientific novelty, or a completed enabling capability.
