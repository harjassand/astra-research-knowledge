# Q54 stage 1 — a sharp hidden-transition obstruction

**Result:** a completed mathematical counterconstruction and executable comparison. The attempted new-regime learning bridge is defeated in the specified observation model. A qualifying new scientific capability, substantial novel general principle, and civilisation-changing advance are **not established**. The exact specialization's scientific priority is unestablished; the general ill-conditioning of analytic continuation is established prior work.

## Initial question and actual claim

Can a discovery system acquire a constitutive law from safe measurements and reliably certify its use in a new operating regime, if the unknown law is real analytic, passive, uniformly stable and has known lower and upper stiffness bounds?

The actual claim proved here is narrower and negative: those properties alone do not supply such an operation. There is an explicit class of passive analytic springs for which every adaptive finite-budget safe force-query procedure is dominated by an ordinary endpoint repeated-measurement experiment. The exact optimum still needs exponentially many readings to discriminate a macroscopic target-force difference. A sharp safe-to-target modulus remains discontinuous even when the entire safe response curve is available with arbitrarily small positive error.

This is an information obstruction, with arbitrary computation and exact knowledge of both candidate laws granted to the learner. It is not a computational lower bound, a claim about every possible physical sensor, or a manufactured material.

## Construction

Fix `0<a<b`, `0<m<L`, `A=L-m`, `a<c<b`, and `delta>0`. With `sp(z)=log(1+exp(z))`, define

```
f0(x) = m*x
h(x)  = A*delta*[sp((x-c)/delta)-sp(-c/delta)]
f1(x) = m*x+h(x)
```

Both vanish at zero, are real analytic on the full real axis, and have derivative in `[m,L]`. Their storage potentials are strongly convex and nonnegative. The corresponding overdamped driven spring is uniformly contractive. Thus the counterconstruction preserves passivity and a fixed stability margin rather than hiding an instability.

The greatest force difference on the allowed interval `[0,a]` is exactly `epsilon=h(a)`, with

`epsilon <= A*delta*exp(-(c-a)/delta)`.

At the task point `b`, the force difference tends to `A*(b-c)>0` as `delta` shrinks. Taking `c=a+sqrt(delta*(b-a))` instead yields a target difference approaching the full `(L-m)*(b-a)` while the safe signature vanishes. Real analyticity supplies exact uniqueness but no common complex analyticity width.

The full self-contained derivation is in [GOVERNING_PROOF.md](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage1/GOVERNING_PROOF.md). It includes a sharp limiting extrapolation modulus, a fixed-finite-derivative extension, and a strongly convex passive-network sensitivity bound.

## Strong ordinary incumbent and executed comparison

Each allowed reading is `Y=f(x)+N(0,sigma^2)`, with independent noise and `x∈[0,a]`. The budget counts scalar readings; arbitrary retained history, randomization and adaptive choices are allowed. Both candidates and their exact parameters are supplied to every method.

For this two-law problem, repeatedly reading at `a` is **exactly optimal for every decision problem**: an explicit hypothesis-independent Gaussian transformation converts each endpoint reading into the reading requested by any adaptive safe policy. This constructive experiment comparison is stronger than choosing a weak fit as the incumbent. The ordinary Gaussian likelihood test has exact minimax error

`p*(n)=Phi(-sqrt(n)*h(a)/(2*sigma))`.

Therefore the exact symbolic 5% error threshold is

`n >= 4*sigma^2*[Phi^-1(0.95)]^2 / h(a)^2`, rounded upward.

For `m=1, L=5, a=0.5, b=1, c=0.65, delta=0.01, sigma=0.001`:

- The task force difference is `1.4`.
- The largest safe force difference is `1.22360909485e-8`.
- The optimal error after `1,000,000` readings is `0.4975592682`.
- The 5% error threshold is approximately `7.22818e10` readings. Large count columns are floating evaluations of the exact formula, not unit-resolved arbitrary-precision integer certificates.

A proposed stiffness bridge based on paired finite differences uses two force readings per pair. The noise amplification cancels the apparent derivative gain. For `delta=0.025` and the same total of 200 force readings:

| Method | Error probability |
|---|---:|
| Endpoint likelihood test, exact adaptive optimum | 0.04000968 |
| Two-point design, retaining both raw records and optimal likelihood | 0.10580490 |
| Paired finite differences alone | 0.22461396 |

Monte Carlo diagnostics use 40,000 independent repetitions under each hypothesis at 160 readings. The endpoint errors are `0.05770` and `0.05940`, versus the exact `0.0587023`, within sampling error. Uniform and a history-dependent safe policy are included as diagnostics; they are not used as the decisive incumbent. Eighteen anchored parallel/chain equilibrium cases satisfy the derived passive-network sensitivity bound. These are simulations of stated equations, not source measurements or hardware results.

The numerical script runs successfully with Python warnings treated as errors. It uses stable `logaddexp` evaluation and computes the small law difference directly, avoiding subtraction of nearly equal full forces. The first development run exposed spurious host BLAS warnings on small finite matrix products; replacing those products by explicit NumPy tensor sums produced a clean warning-as-error run. The mathematical proof does not depend on those finite checks.

## Consequence and precise unresolved operation

For the class of real-analytic laws with `f(0)=0` and `m<=f'<=L`, define `omega(epsilon)` as the largest target-force difference between laws that differ by at most `epsilon` throughout `[0,a]`. The proof gives

```
omega(0) = 0
lim_(epsilon↓0) omega(epsilon) = (L-m)*(b-a).
```

The corresponding minimax absolute extrapolation error with an entire uniformly noisy safe curve has limiting value `(L-m)*(b-a)/2`. Every fixed pair is learnable with enough readings; there is no uniformly consistent finite-resource extrapolator over the whole class. These are carefully different quantifiers.

The missing bridge is an actual compatible operation that exposes the transition with quantified resources: permission and capability to interrogate the target regime, a separately supported sensor with suitable coupling/noise, or a justified quantitative prior such as a common complex domain/norm or a transition-width lower bound. A guessed source family, a learned coordinate map, additional history processing, or a derivative oracle assumed into existence would not provide it. Passive rearrangement can change sensing gain and conditioning; the explicit network inequality charges those quantities and does not declare all networks inferior to a scalar sensor.

The three preliminary representations and the abandoned analytic-continuation, finite-difference and passive-network bridges are preserved in [RESEARCH_NOTES.md](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage1/RESEARCH_NOTES.md). No positive physical bridge was supplied; the consequential acquisition target remains unmet.

## Primary evidence and originality boundary

SINDy demonstrates sparse equation recovery in suitable variables and a chosen candidate library; it is a pre-existing operation. [Brunton, Proctor and Kutz, 2016](https://doi.org/10.1073/pnas.1517384113).

Analytic nonlinear identification with known features has established non-asymptotic guarantees depending on excitation quantities; it does not claim one universal favorable constant for all narrow analytic transitions. [Musavi et al., NeurIPS 2024](https://proceedings.neurips.cc/paper_files/paper/2024/file/9b3c956210432122aa5385c355fc7c6e-Paper-Conference.pdf).

Analytic-continuation ill-posedness and the role of quantitative complex-domain bounds predate this trial. [Trefethen, 2020](https://doi.org/10.1007/s10543-020-00802-7), [author's paper](https://people.maths.ox.ac.uk/trefethen/trefethen_ac.pdf). SafeOpt also uses explicit regularity hypotheses. [Sui et al., 2015](https://proceedings.mlr.press/v37/sui15.html). The experiment-comparison framework is classical. [Blackwell, 1951, primary archive](https://digicoll.lib.berkeley.edu/record/112749).

These antecedents prevent relabelling this negative as invention merely because it has a new explicit fixture. The exact passive/adaptive specialization has been derived and checked here, but a failed targeted search does not establish its novelty.

## Files and reproduction

Run from any directory:

```
/usr/local/bin/python3 -W error /Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage1/construct.py
/usr/local/bin/python3 -W error /Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage1/plot.py
```

- `construct.py`: law construction, exact resource/risk formulas, matched comparison, adaptive transcript diagnostics, simulation-kernel check, and passive-network checks.
- `rate_sweep.csv`, `sharp_modulus.csv`, `matched_comparison.csv`, `adaptive_simulation.csv`, `blackwell_kernel_check.csv`, `passive_networks.csv`: complete generated numerical tables.
- `numerical_summary.json`: selected numerical values and model-only provenance.
- `construction.png`, `construction.pdf`, `plot.py`: standalone scientific figure and its generating source.
- `SOURCES.md`: exact primary links, relevance and limits.

![Mathematical construction and exact acquisition cost](/Users/harjas/Documents/ChatGPT/coordination/work/astra-method-experiment-20261026/trials/Q54/stage1/construction.png)
