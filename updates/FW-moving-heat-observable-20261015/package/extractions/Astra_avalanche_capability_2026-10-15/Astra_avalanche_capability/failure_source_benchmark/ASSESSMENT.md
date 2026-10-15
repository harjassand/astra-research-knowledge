# A source-grounded avalanche benchmark and exact clock correction

15 October 2026. This is computational verification of a published theoretical model, not validation against physical creep measurements. No rare-event certificate for this new target is claimed.

## Primary sources and what they establish

1. Hiemer, Moretti, Zapperi and Zaiser, *Fiber bundle model of thermally activated creep failure*, https://arxiv.org/abs/2508.13367; full HTML https://arxiv.org/html/2508.13367v1. The model has fixed total force F, equal load sharing, fixed fiber strengths h_i, and dimensionless thermal rates exp((F/k-h_i)/T) while k fibers survive. Mechanically overloaded fibers fail immediately, including during initial loading. The public author's code uses h_i > F/k for survival, so equality breaks. The paper supplies theoretical phase-type distributions and stochastic simulations, not a measured material calibration. Its HTML Eq.4 has the opposite stress sign to Eq.3/10 and the author's code; Eq.6 as printed is a survival function rather than a normalized exponential density. We use Eq.3, Eq.10 and the code's consistent sign. Temperature is appropriately scaled; time has the model's implicit unit attempt frequency. No conversion to kelvin or seconds was supplied or inferred.

2. Author repository: https://github.com/ComplexityBiosystems/fiber-bundle. Acquired read-only source files are in `upstream/`, with original LICENSE; SHA256 hashes in `results.json`. `fig2.py:test_cond_heterog_lifetime` specifies an exact numerical fixture: five sorted uniform strengths from legacy NumPy seed 0, f0=.125, T=.05. The author's implementation recomputes all rates and uses a categorical thermal failure followed by mechanical closure; its separate phase-type solver enumerates states. These are the appropriate small-system reference methods. `run.py` supplies the parameter grid f0=.125,.15,.175 and T=.05,.1,.15. The n=10 setting f0=.175,T=.15 is also used for the paper's conditional CDF figure; its exact plotted threshold realization was not recovered.

3. Zenodo https://doi.org/10.5281/zenodo.16413747. Acquired API metadata identifies one file, `fiber-bundles.h5`, 42,004,816,615 bytes, MD5 992aa5ab1c26396b7a3b80f148a80fcd. The file contains simulation trajectories, not physical tests. It was not downloaded. We do not claim reproduction of the deposited trajectories or the figure's exact realization.

4. Mattsson and Uesaka, *Characterisation of time-dependent, statistical failure of cellulose fibre networks*, https://doi.org/10.1007/s10570-018-1776-5. This experimental work measures compression creep lifetime and constant-loading-rate strength distributions of containerboard. It reports fitted load sensitivity rho roughly 20–60 and lifetime Weibull beta approximately .4 to above 1, with censoring and batch/position variability limiting direct comparisons. These are specimen/network parameters, not an identified set of elementary fiber rates. It cannot calibrate our microscopic equal-load-sharing model by direct substitution. It does show why rho=2 and memoryless beta=1 cannot be presented as generally measured material values. No raw numerical replicate dataset was acquired in this search; plots and fitted ranges are insufficient for a new mechanistic validation.

5. Engelbrecht-Wiggans and Phoenix, *A stochastic model based on fiber breakage and matrix creep for the stress-rupture failure of unidirectional continuous fiber composites*, https://doi.org/10.1007/s10704-019-00359-9. Public PDF acquired from https://d-nb.info/1198373822/34 as `matrix_creep.pdf`. Its carbon/epoxy mechanism uses essentially time-independent brittle fibers with random strength flaws; matrix shear creep changes the spatial stress-transfer length after breaks. It explicitly distinguishes this from lifetime laws driven by degrading fibers, especially after proof loading. Thus a common count-only hazard multiplier is not a justified replacement. For material validation, this history-dependent shear-transfer mechanism is a stronger physical competitor than generic thermal equal sharing. Its illustrative model comparisons are not a new validation dataset for our computation.

6. Phoenix, Schwartz and Robinson, *Statistics for the strength and lifetime in creep-rupture of model carbon/epoxy composites* (1988), https://doi.org/10.1016/0266-3538(88)90001-2. The original abstract identifies ambient-condition experiments on seven Hercules IM-6 fibers in Dow DER 331 epoxy/No.26 hardener, approximately hexagonally arranged, with a model using strength disorder, stress redistribution and matrix creep. This is a promising genuinely coupled physical validation target, but its full experimental data and calibrated numerical law were not acquired. The abstract alone does not support claiming a successful fit or test.

## Exact extension derived here

Fix strengths h, total force F>=0 and T>0. Let lambda_i=exp(-h_i/T), and draw independent internal clocks E_i~Exp(lambda_i). Rates and mechanical thresholds are tied to the same h_i; do not choose them independently. Define u by du/dt=exp(F/(kT)) whenever the stable population is k>0.

Algorithm:

1. Start at u=t=0 with all fibers. Repeatedly remove every h_i<=F/k, updating k, until stable or empty. If empty return lifetime zero.
2. Among surviving fibers find i with least E_i. Advance physical time by (E_i-u) exp(-F/(kT)) and set u=E_i.
3. Delete i; perform the same zero-time mechanical closure. Stop if empty; otherwise repeat.

Why this is exact: conditional on survival to internal time u, residual independent exponential clocks have rates lambda_i. Their minimum produces the correct total internal rate and winner probability. Multiplying the time rate by exp(F/(kT)) gives the original physical rates. Mechanical deletion censors the unused clocks without consuming time. The next closure and waiting law therefore agree inductively. Thermal ties have probability zero; implementation uses deterministic stable ordering. Mechanical equality is handled exactly as in the reference model.

Sort E and h separately, keep a Boolean alive array, and scan each ordering monotonically. Each fiber is visited only a bounded number of times. Complexity is O(n log n) time and O(n) storage, with no heap required. This is an exact simulator in real arithmetic; it is not by itself a rare-event estimator, an arithmetic certificate, or a demonstrated priority claim over all prior methods.

## Static representation derived and independently checked here

For k=1,...,n let A_k={i:h_i>F/k}. Define C_k as the kth-largest E among A_k, or zero if |A_k|<k. Set T_k=max_{l>=k} C_l and psi(k)=exp(-F/(kT)), with psi(0)=0. Then

    tau(E) = sum_{k=1}^n [psi(k)-psi(k-1)] T_k.

Proof: at internal time u, a population k is feasible iff at least k fibers have both h_i>F/k and E_i>u. Let K be the largest feasible integer, or zero. If more than K eligible fibers remained, then K+1 would be feasible because A_K is a subset of A_(K+1), contradicting maximality. K is therefore a fixed point of mechanical closure. Starting with all fibers and repeatedly removing failed/overloaded ones selects the largest such fixed point. Eligibility only decreases as u advances and as population shrinks, so no mechanically deleted fiber could become eligible later. Thus K is exactly the event algorithm's survivor count. Now K>=k iff u<T_k, up to measure-zero clock boundaries. Integrating psi(K(u)) and expanding psi(K) as its positive increments proves the identity.

Each order statistic is coordinatewise monotone and 1-Lipschitz in sup norm; maximum preserves both properties. Consequently tau is monotone and Lipschitz with constant sum_k Delta psi(k)=psi(n)<=1. Initial failure can make all T_k zero, so the representation includes an atom at zero. Fixed-strength arithmetic coupling is promising: if all clock approximations differ by at most epsilon, lifetime error is at most psi(n)epsilon. This alone gives no uniform probability-of-misclassification bound near a requested deadline. Strength rounding also changes the discrete sets A_k and requires a separate margin/interval treatment; the clock-only Lipschitz statement does not cover it.

The old convex survival-profile importance bound cannot simply transfer. Mechanical closure removes fibers before their thermal clocks fire, producing a smaller lifetime and a larger early-failure event. A cap proved only for the original complete thermal-failure event need not hold on this enlargement. A new proposal/cap or new event-specific certificate is required.

## Independent numerical results

All saved result files come from our independently written routines using already installed NumPy/SciPy. `verify_avalanche_clock.py` implements the O(n log n) clock algorithm, an independent O(n^2) residual-clock algorithm, an independent direct Gillespie sampler, and a reachable-subset generator. The exact public five-fiber fixture is preserved without fitting favorable strengths.

- Reachable generator: 28 states including absorption.
- 50,000 clock paths: maximum error at the nine saved CDF grid points .00091277; the 99% DKW bound is .00727895. This is a stochastic diagnostic, not proof of exactness.
- Clock/Gillespie means 2054.81 and 2061.12; independent two-sample KS statistic .01018, p=.35124.
- 1,080 paired residual-clock/event-loop tests: identical event identities and survivor counts, maximum relative lifetime discrepancy 1.34e-15.
- Static formula: 6,300 cases, maximum relative discrepancy 1.10e-15, including zero load, immediate global collapse, equality thresholds and heterogeneous strengths. Numerical monotonicity/Lipschitz checks include rounding slack; the proof above supplies the exact claim.
- A single 100,000-fiber path at f0=.15,T=.1 took .130 seconds, with 55,411 thermal events. This is a diagnostic single-path timing, not an optimized matched-runtime benchmark or rare-event performance comparison.
- `grid_results.json` records coupled comparisons with and without avalanche closure on the full published parameter grid, avoiding arbitrary independent rates or selected favorable strengths. Random fixtures are independently generated; they are not the deposited dataset.

The strongest competitor depends on the task. At n=5 use the reachable-state phase-type solution, including stable matrix exponential evaluation instead of cancellation-prone partial fractions. For ordinary large-system sampling use an optimized direct kinetic Monte Carlo implementation, including cached rate data/Fenwick selection; a comparison only to the author's vectorized O(n^2) routine would overstate novelty. For extremely rare tails, this work currently has no new certified efficient estimator.

## Execution provenance and scope

An initial local test imported and executed the inspected author's phase-type and trajectory functions during preliminary verification. That run completed computation but failed during checksum aggregation because `__pycache__` is a directory, so no result JSON was emitted. The corrected final script has no upstream imports; final saved results were regenerated independently. This earlier execution must not be described as having never happened. The two imported files were inspected in full: module-level operations are NumPy/SciPy/itertools imports and function definitions; no file/network/subprocess calls occur. The executed trajectory resets global NumPy RNG; Python created bytecode cache. No unexpected external operations are evident from source inspection. We have not installed packages, modified canonical project code, published, contacted authors, or downloaded the 42 GB dataset.

## Decision

The acquired source gives a real, independently specified computational challenge and a substantive missing operation: instantaneous avalanche closure, with thermal rates tied to strengths. The corrected common-clock algorithm and static order-statistic representation solve that operation exactly under the source model. Physical validation is still open, and the existing 400-fiber rare-event certificate cannot be advertised as solving this different avalanche target. The next computational gate is a source-model rare-event bound plus a matched competitor; the next physical gate is actual calibrated coupled microcomposite data, including matrix/load-history effects.

## Classical radial conditioning transferred to the avalanche model

A further exact extension follows from positive homogeneity of the static representation. For fixed h,F,T, write X_i=lambda_i E_i, R=sum_i X_i and V=X/R. Then X_i are iid Exp(1), R~Gamma(n,1), and V~Dirichlet(1,...,1) independently. Since tau(E)=R tau(V/lambda),

    P(tau<=d) = E_V[ GammaCDF(n, d/tau(V/lambda)) ].

Set the conditional value to one when tau(V/lambda)=0. This retains all initial and subsequent avalanche closures. It is classical Gamma/Dirichlet Rao–Blackwellization, not a new general identity. The substantive transfer is that the genuinely avalanche-aware lifetime remains homogeneous, enabling the earlier radial operation without replacing the physical source's transition law.

`check_radial.py` applies this to fixed uniform strengths generated by NumPy RandomState(0), published f0=.175 and T=.15. Independent pilot paths choose the empirical 1% lifetime quantile as a deadline; production uses a different seed. These are transparent numerical fixtures, not the exact strengths in the deposited figure or measured samples.

- n=100: deadline 1.8604127565, 50,000 production paths. Plain estimate .010000 (SE .000445); radial estimate .00989868 (SE .000287). Empirical variance reduction 2.40x. Single timing comparison suggests 2.26x matched-cost efficiency.
- n=1000: deadline 3.1613068399, 10,000 paths. Plain estimate .01210 (SE .001093); radial estimate .0111302 (SE .000649). Empirical variance reduction 2.84x. Timing noise made the measured radial loop slightly faster than plain, yielding an unreliable apparent 3.14x matched-cost gain; the variance reduction is the cleaner evidence.
- Explicit independent homogeneity checks agree to 1.4e-15 relative error or better.

The radial estimator adds only a scalar sum and incomplete-gamma evaluation to the same exact path kernel, and its theoretical variance cannot exceed plain Monte Carlo. These modest gains are useful evidence of correct transfer; they do not demonstrate efficient computation of 1e-50 tails, bounded relative error as the deadline vanishes, or certified gamma arithmetic.

For finite precision, let a=tau(V/lambda)>0. Differentiation gives |d GammaCDF(n,d/a)/d log a| = y^n exp(-y)/Gamma(n), y=d/a, bounded by n^n exp(-n)/Gamma(n). Thus a positive certified enclosure [a_lo,a_hi] gives the monotone enclosure [GammaCDF(n,d/a_hi),GammaCDF(n,d/a_lo)] and a logarithmic-width bound. Combining this with the lifetime Lipschitz bound is a route to a certificate, but it still needs certified rate/exponential/gamma evaluations, strength-margin decisions, and the distributional approximation budget. None is established by the present floating-point experiments.
