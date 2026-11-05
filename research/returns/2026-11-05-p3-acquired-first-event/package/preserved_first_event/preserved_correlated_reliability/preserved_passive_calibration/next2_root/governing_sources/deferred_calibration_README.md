# Output-only Hamiltonian calibration and recovery of the first archived input

The completed construction captures the first arbitrary unknown quantum input and its reference correlations **before the Hamiltonian is known**, then learns that static Hamiltonian from later outputs of the same source and decodes the archive. It supplies a finite output-experiment compiler, rather than assuming exact derivatives or direct source preparation/control/readout. Read the [complete report](package/Astra_Output_Only_Deferred_Calibration.pdf), [editable proof](package/construction/output_only_calibration.tex), [independent construction review](package/proofs/independent_construction_review.txt) and [separate no-burn-in construction](no-burn-in-calibration.md).

| Distinct result | Direct route |
|---|---|
| Local output process experiment, coefficient learning and deferred recovery | This page |
| Arbitrary-start calibration with complete bounded neighborhoods | [No-burn-in companion](no-burn-in-calibration.md) |
| Separate completed classical reliability consequence | [All-deadline relative CDF sensitivity and finite implementation precision](reliability-cdf-sensitivity.md) |
| Original material | [ZIP](original/Astra_Deferred_Calibration_Research_Package.zip), [complete visible return](P3_DEFERRED_CALIBRATION_20261105_RETURN.txt), [provenance and hashes](SOURCES.json) |

This is a conditional polynomial-resource theorem under specified pure coherent access and paid growing finite receiver controls. It is not a competitive device, an optimality/priority result or a proved bounded-hardware implementation of this full deferred operation. The newly supplied P1 bounded-component result remains separately scoped; this source does not automatically claim that additional composition.

## Known interface, unknown Hamiltonian

The labelled `n`-qubit source has a static `H=sum_a theta_a P_a`, a complete known list of distinct nonidentity Pauli candidates of maximum weight `k`, and known `B_H>=sum|theta_a|`. Identity energy is unidentifiable and irrelevant. Taking all weight-at-most-`k` strings permits unknown support with `M=O(n^k)` at fixed `k`. Port labels, axes, phases and rates are already calibrated: actual pure-vacuum nonidentity Weyl outputs generate `r sum_i(E_i-id)` and are coherently/losslessly delivered. The physical photon rate is `3nr/4`, distinct from synthetic reset rate `r`. Unknown gauges, extra missing terms and arbitrary time drift are outside the theorem.

The inherited finite noise-bin collector does not require Hamiltonian coefficients. It exposes an input-independent reset flag, an old-state export `B`, and the physical purifier `A` of the replacement Bell state on source plus `A`. **Actual A access is essential.** These are acquired coherent output registers, not unprovided source SWAP/reset operations. Discarding all A registers at source `I/d` leaves these B exports and flags independent of H; that is not a claim that all classical field observations are useless.

## Local process experiment and raw signed-output identity

Starting at `I/d`, retain the last A on a chosen local set during a front window `w`, discard intermediate output for duration `t`, and retain the first required B exports during a back window `w`. On all required flags this acquires a local Choi process state. Ideal acceptance on `b` sites is `(1-exp(-rw))^(2b)`; a receiver Bell projection adds `4^-b` for a chosen-input query. Failed queries consume their input. Finite Hamiltonian window error and any physical instrument error must be converted to conditional error with a valid acceptance lower bound; there is no repeat-until-success guarantee on one unknown state.

The principal learning experiment keeps failures as outcomes instead. For candidate P, choose site i and a single-site Pauli Q_i anticommuting with P_i, set `R=i P Q_i`, retain front purifiers on `supp(P)` and one back export at i, and measure `R^T_A Q_i,B`. Output `Y` is the signed result on success and zero on failure. For `s=|supp(P)|+1`,

```text
partial_w^s partial_t E[Y](0,0)=2 s! r^s theta_P,
E[Y^2]=(1-exp(-rw))^s.
```

Extra Hamiltonian/reset insertions in the windows add a power of w. The transpose/sign convention and zero outcomes are part of the physical experiment. Fixed-basis purifier measurements can be deferred or made immediately with only the latest local outcome kept; calibration need not store a long entangled probe register.

## Finite learning and two distinct start regimes

Record-machine generators have norm at most `Lambda=2B_H+2nr`; scalar Taylor coefficients have bound `(2Lambda)^a Lambda^b/(a!b!)`. Finite tensor Chebyshev interpolation on a window of size `h=1/(8Lambda)`, explicit tail bounds and ordinary statistical estimates acquire the derivative. A stronger supplied schedule uses actual interpolation-weight norm and factorial remainder `2 exp(3/8)4^(-D-1)/(D+1)!`. At fixed support, precision cost is `eta^-2` up to logarithms with the clock-success/variance factors paid. Every raw attempt, including zero outcomes, counts. No exact derivative or free normalized-postselection oracle is used.

For general fixed-k candidate graphs, paid passive burn-in before each capped trial provides source/reference decoupling `||rho_SR-I/d tensor rho_R||_1<=2sqrt(n log2)exp(-rt/2)`. Choosing `t_burn=(2/r)log(2sqrt(n log2)N/epsilon_mix)` pays whole-protocol error over N trials. The proof uses conditional-relative-entropy contraction, not a source-only relaxation claim.

The distinct [no-burn-in companion](no-burn-in-calibration.md) works from arbitrary correlated starting states by front-resetting each **complete candidate interaction neighborhood** and freshly randomizing interpolation nodes. Efficient bounded neighborhoods are a stronger premise than bounded term weight k; a high-degree graph does not acquire that claim automatically.

## Archive recovery despite correlated later calibration

For known upper interaction bound `beta(H)<=beta0<r`, let `kappa0=r-beta0` and archive the first payload for `T0=kappa0^-1 log(400n/epsilon^2)` using the accepted P1 H-independent collector. Only the later inverse-history decoder needs H. Learn coefficients to `eta<=epsilon/(100 M T0)`. On good estimates, the common-layout receiver decoder obeys full diamond difference at most `2T0 sum|theta_hat-theta|<=2T0 M eta`. The estimate itself need not satisfy the extinction margin.

Calibration need **not** be statistically independent of the archive. For subnormalized archive/reference branches `sigma_z`, good branch decoders within diamond distance e of one fixed true-H decoder contribute at most `e Tr(sigma_z)` and bad branches at most `2 Tr(sigma_z)`. Later operations leave the unconditioned archive marginal unchanged. A uniform bad probability delta therefore adds at most `e+2delta`. This replaces the historical working notes' initial independence requirement; those notes do not override the final report/review.

Only one original arbitrary input is consumed. The archive must survive the entire later calibration and decoding, including propagation, hardware operations, statistical/classical work and storage-error cost `Q_memory T_wall nu_memory` or paid protection. Calibration alone works for every `r>0`; this generic deferred-recovery corollary retains the supplied margin `r>beta0`.

## Real costs, supplied evidence and incomplete routes

Continuous field and finite record-machine comparisons, equal-bin receiver executions, growing finite peak/slew, timing precision, local references, gate/readout/refresh, bank-per-bin fallback or actual recycling throughput, routing and protected storage all remain charged. Unconditional physical errors are allocated over the full capped protocol before any conditional guarantee; rare branch normalization cannot be skipped.

At the supplied `n=2`, `M=15`, `epsilon=0.1` point, a loose sufficient raw-trial schedule is approximately `10^62.54`; a sharper factorial/actual-weight schedule is approximately `10^39.12`, with degree fourteen and timing precision about `9.35e-24` time units. Both precede receiver compilation and are upper bounds, not minimum costs. They do not demonstrate practical capability.

The [ideal-instrument diagnostic](package/construction/output_calibration_diagnostic.json), [finite-derivative diagnostic](package/construction/finite_derivative_diagnostic.json), [evaluated sharper schedule](package/construction/sharper_schedule.json), original programs and [convergence figure](package/construction/finite_derivative_convergence.png) are retained. Accepted counts were generated by binomial sampling from computed probabilities; the physical rejected attempts, noisy fields and protected factories were not run. Taylor/70-digit interpolation calculations separately record analytic truncation and uncertified roundoff; large resource schedules evaluate formulas rather than execute those trials. The substantive [independent review](package/proofs/independent_construction_review.txt) covers the new calibration/composition, finite dyadic sampler, martingale variance, timing/rate errors and reference-uniform recovery at its actual scope. No new Capital execution or audit occurred.

Generic output identification, Choi/process tomography, Hamiltonian derivative learning and known-H recovery have strong prior machinery, credited in the [governing sources](package/GOVERNING_SOURCES.json) and report. No superiority over all same-output alternatives is proved. The [all-strength hidden-noise theorem and effusion companion](../2026-11-05-p3-all-strength-control-speed/README.md) are preserved byte-for-byte under `package/preserved_prior/` with their original conditions. The reliability CDF computation remains [unfinished](package/independent_routes/reliability/UNFINISHED_COMPUTATIONAL_EXTENSION.txt); convex-capacity work is [explicitly incomplete](package/independent_routes/convex_capacity/STATUS.txt). Neither becomes a premise or completed substitute. Generated current retrieval is unchanged; these complete proofs and result pages are public directly on GitHub.
