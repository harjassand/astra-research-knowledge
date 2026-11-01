# Ordinary clearance-time baselines: bounded empirical pilot

**Result first.** Ordinary exact-algorithm SSA is already practical at the tested sizes, despite spending almost all its work on population-conserving reactions. At N=10,000 it used **13.45 million reactions and 0.906 seconds per path** on average. Ordinary full mass-action mean field already predicts clearance on approximately the observed time scale, using a stiff solver in about 0.29 seconds for the initial BDF setting. Neither that deterministic point nor the supplied asymptotic point is a stochastic clearance-time distribution. This pilot demonstrates a workload to accelerate, **not a new algorithm or an accuracy/cost victory**.

## 1. Frozen task and different predictive objects

The state is (A,B,C,D,E), initially **(0,N,1,1,0)**. The twelve channels are 0↔A, 2A↔AC, 2A↔AD, 2A↔AE, AE↔CD, CD↔AB. All coefficients are one except CD→AE, which has coefficient two. The stochastic 2A propensity is **A(A−1)** with no factor 1/2. All physical holding time, immigration, death, competing reactions and neutral recrossings are retained.

The target is the **first total population S≤floor(15(N+2)/16)**, namely 95, 939 and 9,376. It is not a threshold on B, or floor(15N/16). Every successful SSA path exits with exactly the target total because only births and deaths change S, by one.

Three objects are compared:

1. **Direct SSA paths:** the standard exact-in-time Gillespie algorithm, implemented in C++ with twelve-channel linear selection. It has no tau-leap or reduction bias in its mathematical idealization; this floating-point, pseudorandom implementation is not a certified random-bit/roundoff sampler. It yields sampled times, exit states, occupations and reaction counts.
2. **Full deterministic mass-action ODE:** the same stoichiometric channels, with each 2A rate **a²**. This is an ordinary deterministic approximation, **not the expectation of the CTMC**, and its event time is not E[tau]. In particular E[A(A−1)] is not E[A]². Using a(a−1) as a continuous propensity would also produce negative rates for 0<a<1; that nonphysical extension was not used.
3. **Supplied asymptotic timing point:** 1.1065805219125796 N^0.2. The constant is an input, not re-proved here. Its finite-N meaning and error are not certified by this experiment.

A deterministic point has no stochastic spread. Treated as a point-mass CDF, its Kolmogorov distance from a continuous hitting-time law is at least 1/2. No apparent agreement of means or medians changes that obstruction.

## 2. Pilot results

Main samples only; the four cost-gating preflight paths are retained separately in the raw files and summary. “SE” is the empirical standard error of the sample mean, not a rigorous finite-N model-error bound. Quantiles are descriptive sample quantiles, not coverage guarantees.

| N | Main paths | SSA mean (SE) | SSA median | SSA sample 10–90% quantiles | Mean-field point | Asymptotic point |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 64 | 2.970 (0.142) | 2.705 | 1.620–4.407 | 2.453 | 2.780 |
| 1,000 | 64 | 4.002 (0.153) | 3.717 | 2.509–5.884 | 3.715 | 4.405 |
| 10,000 | 16 | 6.562 (0.472) | 6.817 | 4.198–8.885 | 6.234 | 6.982 |

**All 148 requested clearance paths completed:** 64+64+16 main paths and two preflight paths at each of N=100 and N=1,000. No production path was horizon-, event-, or wall-censored, failed, omitted, or left unstarted. The conditional N=10,000 stage is explicitly exploratory, admitted by the prespecified N=1,000 cost gate.

Mean-field minus the observed sample mean is −0.517, −0.287 and −0.328, respectively. The asymptotic point minus the observed mean is −0.191, +0.404 and +0.420. These are descriptive sample discrepancies, not measured errors against an exactly known population mean. The sample fractions below the mean-field point are 0.359, 0.500 and 0.375; below the asymptotic point they are 0.531, 0.688 and 0.500. No point is being silently chosen post hoc as a distribution model.

The pilot is small: under the **ideal iid exact-path model**, the per-N 95% DKW empirical-CDF half-widths are 0.170 for 64 paths and 0.340 for 16 paths. They are not simultaneous bands across all N, not numerical implementation certificates, and not approximation-error certificates for either deterministic clock. As an ordinary benchmark, DKW would require 738 iid paths for epsilon=0.05, beta=0.05; this larger experiment was **not** run.

## 3. Where the microscopic work goes

| N | Mean reactions/path | Observed min–max | Population-conserving internal fraction | Mean C++ kernel seconds/path | Mean launch-inclusive seconds/path |
|---:|---:|---:|---:|---:|---:|
| 100 | 2,081 | 615–4,622 | 99.3934% | 0.000142 | 0.0485 |
| 1,000 | 138,916 | 100,204–181,001 | 99.9486% | 0.00891 | 0.0706 |
| 10,000 | 13,452,824 | 12,482,547–14,204,278 | 99.9953% | 0.906 | 0.975 |

The last two sizes exhibit an approximately hundredfold event increase for a tenfold N increase in this pilot. That is an observed workload trend, not a proved complexity law. A competent compiled SSA is important: at N=1,000 one sampled exact path was **much cheaper than this Python/SciPy stiff ODE solve**. At N=10,000 the ordinary ODE is cheaper than one SSA path, but it supplies a different object. Timings must not be advertised as matched-error speedups.

Every raw path includes all twelve reaction counts, integrated occupation ∫A dt, exit state and time. The checks enforce **S=N+2+births−deaths**. Occupation is accumulated over every holding interval with the pre-jump A; ∫A dt is the death compensator and is **not** equated pathwise to the death count. Internal events conserve total population; they are not all dynamically dispensable.

## 4. Ordinary ODE verification and limitations

SciPy 1.17.0 BDF and Radau, analytic Jacobian, event interpolation and dense output were used. Each N received BDF and Radau at rtol=1e−9, atol=1e−11, plus BDF at rtol=1e−11, atol=1e−13. The table uses the tighter BDF point. The maximum discrepancy among all three runs is 1.33e−8, 3.13e−8 and 6.69e−8; Radau versus tighter BDF differs by at most 1.25e−9. This is a numerical consistency check, not a validated error enclosure.

The base BDF costs were 0.258, 0.205 and 0.286 seconds, with 1,680 / 2,653 / 3,310 RHS evaluations and 109 / 170 / 218 LU factorizations. All nine solver trials, cross-checks, startup and dense-domain checks are charged: **4.934 seconds** launch-inclusive. Rejected steps are not separately exposed by `solve_ivp`; their work remains included in reported wall, CPU and solver work counters.

No rate clipping or state projection was used. All accepted-node and 10,001-per-run dense sample species values were nonnegative; Newton internal iterates were not recorded, and sampled nonnegativity is not an all-time validated enclosure. The ODE identity S=N+2+t−∫a dt was checked with maximum residual 4.73e−11. Deterministic symmetry C=D is not imposed on the SSA.

## 5. Budget, validation, failures, and full cost

`PLAN.json` froze the sample counts, seed rule, cost gate and caps before sampling. Each path had a 50-million-event cap, five-second kernel cap checked every 4,096 events, physical horizon 200, and an eight-second outer timeout; each batch had a 100-second launch-inclusive limit. Both N=1,000 preflight paths cleared with at most 141,154 events and 0.00866 kernel seconds, passing the ≤2-million-event / ≤0.5-second gate for 16 N=10,000 paths. All limits and unstarted-path handling remain in the code.

Independent literal reactant/product Python construction checked rates on all 4^5 low-count states plus 200 seeded larger states. Three shared-uniform traces at N=10,100,1,000 checked 5,000 consecutive reaction marks, successor states, elapsed times, occupations and population identities each. All twelve channel marks occurred in the validation. Explicit zero-horizon and one-event-cap cases test honest censor reporting. These are software checks, not a mathematical proof of stochastic correctness.

Two failed setup attempts remain visible and charged:

- `/usr/bin/time` was absent; the first launch failed before compilation or simulation. It was replaced by a standard-library Python resource wrapper, with no installation.
- The first N=10 validation trace reached horizon 200 after 3,430 events, so its demand for 5,000 events failed. The trace was valid and retained under `attempt_001`; only that validation horizon was raised to 100,000,000, with the same 5,000-event and five-second caps. Production horizon 200 and all sample counts were unchanged. Compilation and those 3,430 events are charged again, not discarded.

**Cost reconciliation:** 224,543,093 production/preflight reaction events; 18,431 C++ validation events including the failed trace and cap test; 18,430 additional Python reference-replay reaction updates. Thus **224,561,524 C++ events**, or **224,579,954 total reaction updates including reference work**. Two compilations cost 2.024 seconds in total. All measured child-process wall times, including both attempts, sum to 31.187 seconds; child CPU sums to 26.421 seconds. The successful controller took 31.142 seconds. Charging the entire 14.506-second failed-attempt/debug/relaunch window plus the observed 0.0366-second missing-timer failure gives **45.684 seconds** of execution window, before finalization. Nested clocks are not added twice.

Peak OS child/descendant RSS reported was **90,120 KiB** (compiler); ODE process peak was 68,620 KiB. Per-path launch RSS is retained. These are maximum process-tree reports, not an instrumented simultaneous total-container peak. Exact failed-controller CPU/RSS was not captured; its full elapsed interval is charged and its child measurements are retained. Initial file inspection, report authoring/model deliberation and shell inspection are not benchmark throughput, and no exact all-session CPU figure is claimed. `FINALIZATION_COST.json` separately records final checks/CSV generation. Hardware was the same shared Linux container, reporting Intel Xeon Platinum 8573C; no hardware action or installation occurred. Fixed seeds reproduce trajectories on this arithmetic/toolchain, not portable wall times.

## 6. The capability still to earn

The useful target is **not another cheap deterministic time prediction**: ordinary stiff mean field already provides one and captures much of the finite-N timing scale. Nor is it merely finite-time sampling: competent ordinary SSA already does that.

A proposed accelerated clock/kernel must either supply a quantitatively justified finite-N timing window, or produce a first-passage law **with exit composition and integrated occupation** at the same specified error/confidence contract as its competitors, while reducing total construction, validation and query cost. Boundary startup, changing regimes and continuing immigration/deaths must remain paid. No such finite-N model-error or complexity guarantee is established here.

This is a deliberately modest baseline, not an exhaustive best-method contest. Adaptive critical-reaction/hybrid methods, slow-scale methods and finite killed-chain kernels were not implemented, and remain legitimate stronger competitors. The accepted stability theorem and the asymptotic point do not themselves solve their finite-N constants or certify this pilot. No claims about hardware, new preparation operations, publication, external deployment, or historical novelty are made. No external sources were retrieved; stopped sources remain untouched and Morrey remains paused.
