# Stage 2 result: the no-go survives sequential stopping; the positive operation is conventional

**No new physical capability or verified novel scientific advance was established.** The stress work extends the original obstruction to unbounded adaptive stopping and constructs a useful, rigorously valid upper certificate for equilibrium stiffness. The positive construction is an application of established confidence-sequence methods, and ordinary late-window methods outperform its simplest version on the withheld comparison.

## Strongest attack on the first construction

The proposed escape was to keep experimenting until each particular material reveals itself. The stage 1 finite-horizon lower bound alone did not settle this possibility. Stage 2 proves the following full-domain statement: if a bounded causal procedure declares a permanent spring at a finite, possibly unbounded random stopping time, and its false-solid probability is at most alpha for **every** positive Maxwell rate, its probability of declaring solidity under the actual permanent spring is also at most alpha.

The proof applies finite-record total-variation convergence to the event “declare solidity by T,” then increases T to infinity. It includes arbitrary bounded feedback and random stopping; it is not inferred from a collection of slow examples. Thus a procedure cannot both terminate reliably on the permanent spring and uniformly distinguish it from arbitrarily slow fluid alternatives with error below one half. The missing exclusion of slow modes persists.

The original noise and observation scope matters. This is not an impossibility across all possible material observables, nonlinear activation, or model-dependent fluctuation detectors. No such additional compatible physical operation was supplied.

## Stronger positive construction completed

For a conventional step and the full nonnegative spectral class, the stress is always at least U times the equilibrium modulus g. This one-sided physical inequality supports a nonnegative Gaussian betting supermartingale. Mixing its nonnegative betting parameter against a half-normal density gives an explicit closed-form process. Inverting it yields an upper confidence sequence with

\[
P(\forall t:\ g\le\overline g_t)\ge0.95.
\]

It requires no slow-rate floor, component count or fitted spectrum. With enough time it converges from above to the true g on the coverage event. Whenever g is below an engineering tolerance gamma>0, it eventually certifies g<gamma. The stopping time is finite pointwise and can be arbitrarily large across materials. The operation supplies an upper bound, not a positive lower rigidity certificate, and does not confirm exact g=0 at finite time.

The complete supermartingale, half-normal integration, optional-stopping validity, inversion and consistency proofs are in `PROOF.md`. The engine is established [time-uniform confidence-sequence machinery](https://doi.org/10.1214/20-AOS1991); no invention claim is made for it.

## Ordinary methods and genuinely withheld test

Before generating new cases, `DESIGN.md` froze the generator seed, observation grid, noise, error level and evaluation. The inference methods never receive the generated spectrum or equilibrium value. All three methods use the **same single strain step, integrated stress increments, observation timestamps and noise calibration**:

* A cumulative half-normal mixture confidence sequence, the initial positive candidate.
* A conventional restart version that may discard early transient data, with a valid simultaneous error allocation.
* A conventional method that can select any recorded late window, using Gaussian correction valid simultaneously over all 2,080 windows of the prescribed grid.

The last method is valid on the declared observation grid. The mixture methods additionally have continuous-time validity. No global optimality of any one-sided procedure is claimed, and no stronger conventional estimator is alleged to fail. Existing sequential methods already supply the positive operation.

The held-out evaluation contains **32 cases**: 24 previously unseen random discrete spectra, four continuous gamma spectra with exact analytic response integrals, three adversarial slow modes and one permanent spring. There are **2,000 synthetic paths per case**, or **64,000 total paths**, at 64 readouts spanning 0.001 to 1,000,000 normalized time units. No parameter was retuned after observing outcomes.

The largest observed simultaneous miscoverage across the 32 cases was 1.85% for the cumulative candidate, 0.05% for the restart method and 0.45% for the ordinary window method. These are finite Monte Carlo diagnostics, not proofs or calibrated estimates of the worst case over materials. Exact binomial confidence intervals are recorded in the comparison file; zero observed failures are not treated as zero failure probability. Domain-wide validity follows from the independent proofs.

The ordinary all-window method gave a lower median final upper bound in **30 of 32 cases**; the remaining extreme cases tied at an uninformative bound of one. Across this finite case collection, the average of the per-case median final bound excesses was **0.136889** for the cumulative candidate, **0.104698** for restart inference and **0.104665** for the ordinary window method. These aggregates describe this case collection, not a material population or universal performance rate.

For withheld case 01, with true g=0.1, the cumulative candidate first certified g<0.2 at median time **268.270**; both stronger ordinary procedures did so at **138.950**. The final median bounds were approximately **0.103951**, **0.100404** and **0.100367**, respectively. This is a conventional-method success, not a new-method advantage.

For the broad continuous-spectrum case `continuous_gamma_0`, no method certified g<0.2 before the maximum horizon. The candidate's median final bound was **0.489196**, and the ordinary window bound was **0.409949**, although the true equilibrium modulus is zero. For the rate-1e-10 mode, all three median bounds remained **1**, with **no completed tolerance certificate**. These failures are retained explicitly; noncompletion was not replaced with a favorable runtime.

## Established consequence and precise remaining obstacle

The full-domain sequential argument strengthens the first-stage failure boundary. The positive result shows why that boundary does not forbid useful tolerance-based, one-sided engineering inference: finite noisy records may establish that eventual stiffness is small enough, even while they cannot prove permanent nonzero rigidity or exact infinite-time flow uniformly over arbitrarily slow modes.

The required new operation for the original universal exact target remains an independently justified exclusion of slower alternatives, or a compatible independent observable that bypasses the mechanical contrast obstruction. Neither stage constructs it. The statistics used for the attainable upper certificates are established, and the conventional comparison supplies no evidence of a new general advantage.

Run `/usr/local/bin/python3 -W error stress_test.py` in stage 2 to regenerate the complete withheld comparison, quantitative sequential witnesses, example trajectories and standalone figure. `SOURCES.md` records new primary-source links and retrieval limits. All scientific assertions in the executable passed with warnings promoted to errors. `STAGE1_SHA256.txt` and the executed end-of-run check confirm that all 11 preserved first-stage files remain unchanged. Hash equality confirms preservation only, not scientific validity.
