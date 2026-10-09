# Hidden-equilibrium acquisition audit and variance refinement

Date: 2026-10-10, Australia/Brisbane. Historic objective: **NOT ACHIEVED**.

## Result and status

For the exact continuous-time ten-state target and seven-time witness of Astra
N507–N512, the source's sufficient acquisition budget of about
`1.0624e93` independent stationary windows is unnecessarily large. Conditional
on the source's universal witness inequality and certified target gap, a
distribution-free empirical-Bernstein test has type-I error at most 0.05 against
every stipulated equilibrium null and power at least 0.95 at this target with
**`2e64` independent stationary windows**.

This is a rigorous improvement of a sufficient bound by about 29 orders of
magnitude, obtained by combining an inherited witness with standard statistics
and a new resource audit. It is still physically useless. It is not a lower
bound on all possible tests, and not a new general hidden-dissipation principle.
The finite arithmetic checks passed locally; the complete inherited theorem
has not received external validation or full formal reconstruction here.

The decisive obstacle in the inherited mechanism remains finite-lag acquisition
of sharp positivity facets. Exact matrix exponentials alone do not remove it.

## Source pin, route, and decisive originals

Repository: `https://github.com/harjassand/astra-research-knowledge`, revision
`8aed7fd74eb14622ed5a0a3635a799374296e32a`.

Read `AGENTS.md`, `00_START_HERE.txt`, physics/probability topic routes,
`agent/RESEARCH_WORKFLOW.txt`, and the reviewed wrappers for N507–N512.
All six cards remain `source_derived_unreviewed`; proof availability is not
independent correctness certification.

The historical `updates/BP/package/...` aliases are not Git paths in this
revision. The exact UTF-8 source is in the HTML-unescaped `<pre>` body of:

| Source | Pinned path | Local extraction |
|---|---|---|
| Original seven-time proof | `web/pages/d-73435e0023e887fe.html` | `observable_v1.txt` |
| Linear entropy transfer | `web/pages/d-488df16d802121aa.html` | `observable_v3.txt` |
| Hidden realization/closure | `web/pages/d-de5f6553aedc1dd4.html` | `hidden_v2.txt` |
| Finite-frame follow-up | `web/pages/d-5a6708305d17d906.html` | `hidden_v3.txt` |
| Exact ten-state model | `web/pages/d-f4a7bf9bd106f7d1.html` | `certificate.txt` |
| Exact witness coefficients | `web/pages/d-e1d55dab231fc760.html` | `witness.txt` |

No sparse-checkout state or research history was changed. Decisive proof sections
read: original observable proof §§1–7; particularly §§3–6, where the `h` geometry
defect, residual penalties, target margin, and range normalization arise.

## Acquisition contract

Input to the test: a fixed, predeclared rational witness coefficient file, plus
iid stationary seven-letter windows from the same process at times
`{-t-h,-t,-h,0,h,t,t+h}`, where `t=1/1000`, `h=1/10^12`.
Within-window dependence is unrestricted. The six observable labels are the
only measured variables. Hidden state access is not used to evaluate the test.

The seed model is **supplied for this target-specific power analysis**. The
construction does not learn a suitable witness or an unknown realization from
data. Selecting or optimizing a witness on the test data would require sample
splitting or another complexity correction. Stationarity, independent window
preparation, physical time calibration, all-even parity, and memoryless emission
are substantive requirements. One trajectory does not provide independent
windows automatically; no uniform mixing time has been obtained.

The inherited null is every stationary reversible hidden Markov model with the
stated conditional-feature interpretation and deterministic instantaneous
emissions. It includes unbounded hidden cardinality/rates. The quantitative
entropy interpretation is specifically for finite all-even stationary CTMCs.

## Why exact finite-lag reconstruction is insufficient

Let the marker probabilities at lag `h` be
`a_k(h)+b_k(h)·v_i`, and recover target coordinates by inverting a two-marker
block of the exact `exp(hL)`. This makes the target conditional coordinates
exactly `v_i` and its representation residuals zero. But positivity in a
competing equilibrium model constrains its coordinate only to

`P_h = {x : a_k(h)+b_k(h)·x >= 0 for every marker k}`.

For an irreducible finite CTMC, every entry of `exp(hQ)` is strictly positive
for every `h>0`: uniformize at an escape-rate bound, take a positive directed
path between any two states, and use the positive Poisson mass at that path
length. Therefore every one of the five target vertices lies **strictly inside**
`P_h` at positive lag. Marker positivity at that lag does not expose those
vertices. The target's saturated unit-circle moment does not confine a general
competitor to the five vertices once the admissible polygon expands beyond the
unit disk.

Thus replacing Taylor coefficients with exact exponentials removes a numerical
approximation error, but does not eliminate the finite-lag geometric defect.
A new sharp support/acquisition mechanism or a changed physical protocol is
required. The coordinator's separate discrete-time `P=I+epsilon Q` construction
changes this point because zero transition probabilities can survive one step;
that is a changed target and is not a fixed-lag sample of the original CTMC.

## Complete variance-refinement proof

Use the raw source summand `W` rather than its normalized version. The inherited
premises are

* every equilibrium null satisfies `E W >= 0`;
* the exact target satisfies `E W < -Delta`, with `Delta=10^-6`;
* `|W| <= 6e39`, hence the range is at most `R=1.2e40`.

Write `F,D,G,S_q,p_0,s_2,R_h,R_t` as in source §§3–5. The following facts were
checked from the rational matrices using Python `Fraction`, without floating
rounding (`exact_variance_bound.py`):

1. The target has uniform stationary distribution, nonnegative off-diagonal
   rates, zero row/column sums, and maximum exit rate at most 1.
2. For the local two-label input `(Y_0,Y_h)`, let
   `A={Y_0=0,Y_h in {1,...,5}}`. On `A`, `||F||² <= 100/h²` and `||D||² <= 1`.
   On its complement, `||F||² <= 3` and `||D||² <= h²`.
3. `||K||_F² < 9` and each of the five coefficients of `q` has absolute value
   less than `1/10`.

For any starting hidden state, `Pr(A) <= Pr(at least one jump in h) <= h`.
The stationary adjoint is `Q*=Q^T`, with the same exit rates, so this statement
holds on both sides of the window. Consequently, conditional on the middle
hidden state,

`E ||F^+||², E ||F^-||² <= 3+100/h <= f2 := 103/h`,

`E ||D^+||², E ||D^-||² <= h+h² := d2`.

The bounds are uniform in the initial hidden state, so also apply to the
time-shifted `F`. Since `G=U_t F-KF`,

`E(||G^+||² | X_0), E(||G^-||² | X_0) <= 2 f2+2*9*f2 = 20f2 := g2`.

In a stationary Markov chain the complete past and future are conditionally
independent given `X_0`; they need not have equal conditional laws. Combining
this conditional independence with Cauchy–Schwarz gives

`||s_2||_L2 <= f2`, `||R_h||_L2 <= d2`, `||R_t||_L2 <= g2`.

For example, `(D^-·D^+)² <= ||D^-||² ||D^+||²`, whose conditional expectation is
at most `d2²`. This step does **not** use the false pointwise equality between
target past and future conditional features.

The coefficient bounds yield pointwise

`|S_q| <= (1/10)(1+||F^-||+||F^+||+2||F^-||||F^+||)`.

Hence `||S_q||_L2 <= (1+2 sqrt(f2)+2f2)/10 <= 41/h`, where the last deliberately
loose inequality uses `h<=1`. Also `||p_0||_L2<=1`.

Applying Minkowski to the exact source formula proves

```
||W||_L2 <= B
B = 41/h +72(1+f2)+(45000h+tau)(1+f2)+tau+Lambda*d2+Mu*g2
  < 2.025928e25,
E W² <= B² < 4.105e50.
```

The rational comparison with `4.105e50` is checked exactly. Thus the target
variance is at most `v=4.105e50`.

### Distribution-free test and power budget

For `n>=2` independent observed windows, compute `X_i=W(window_i)`, its sample
mean `bar_X`, and unbiased sample variance `s_n²`. Set

```
r_n = sqrt(2 s_n² log(2/alpha)/n)
      + 7 R log(2/alpha)/(3(n-1)).
```

Reject hidden equilibrium if `bar_X+r_n<0`. This has type-I error at most
`alpha`, by Maurer–Pontil Theorem 4, for every null satisfying `E W>=0`; no null
variance or hidden model is supplied to the test. This is a standard statistical
method, not a new inference principle.

To bound power, apply ordinary Bernstein to the sample mean and Maurer–Pontil
Theorem 10 to the sample standard deviation. With joint probability at least
`1-2 eta`,

```
bar_X - E X <= sqrt(2v log(1/eta)/n)+R log(1/eta)/(3n),
s_n <= sqrt(v)+R sqrt(2 log(1/eta)/(n-1)).
```

At `alpha=.05`, `eta=.025`, `n=2e64`, both logarithms are `log 40<4`.
The sum of the two leading square-root terms is less than `8.105e-7`; all
remaining range-over-sample-size terms sum to less than `1e-22`.
Their total is below `Delta=1e-6`, so the rejection probability at the exact
target is at least `.95`. The finite budget check evaluates approximately
`7.78218e-7`, safely below the target gap.

Primary statistical reference: [Maurer and Pontil, COLT 2009, Theorems 4 and 10](https://www.learningtheory.org/colt2009/papers/012.pdf).

## Executable evidence and accounting

Commands from the task workspace:

```
python3 work/hidden_equilibrium/exact_variance_bound.py
python3 work/hidden_equilibrium/variance_audit.py
```

The first uses only Python's standard library and performs exact coefficient
checks. The second uses NumPy and enumerates all `6^7=279936` words, obtaining:

| Quantity | Value | Status |
|---|---:|---|
| Sum of word probabilities | `0.9999999999999998` | Floating diagnostic |
| Raw coefficient range | `2.6527314487951306e37` | Floating diagnostic |
| Raw second moment | `1.0360062360848566e49` | Floating diagnostic |
| Certified second-moment bound | `<4.105e50` | Analytic + exact coefficient checks |
| Source sufficient Hoeffding windows | `1.0623972828e93` | Inherited range/gap formula |
| New sufficient iid windows | `2e64` | Conditional proof above |
| Required measured letters | `1.4e65` | Seven per window |
| Required time resolution | `1e-12` model-time units | Unchanged |

The numerical enumeration took about 0.28 seconds on this host. NumPy's
`longdouble` is float64 on this machine; this is recorded explicitly. An initial
fraction-to-float conversion overflow is preserved in
`variance_failed_conversion.json`; the corrected conversion scales the fraction
before casting. No tiny target mean is inferred by cancelling enormous floating
word contributions. The target negative mean is retained from the source's
certificate.

The computed numerical variance suggests leading empirical-Bernstein planning
counts around `1e62`, but this is not the certified budget. Model construction,
witness discovery, independent stationary-window preparation, physical sampling
time, precision, and mixing acquisition remain uncharged unknowns beyond the
stated supplied-data interface. A statistic can be evaluated in constant-sized
matrix arithmetic and streamed with an online variance accumulator; fast
evaluation does not fix the acquisition barrier.

## Matched predecessors and limitations

The detailed primary-literature audit is `literature/REPORT.txt`.

* [Skinner–Dunkel, PNAS 2021](https://arxiv.org/html/2011.08765v2) already obtains
  positive hidden-dissipation bounds from entirely time-symmetric observed paths
  using two-jump statistics and a finite reduction of arbitrary hidden
  architectures. The present target's stronger claimed distinction is passing
  the entire reflection-CP hierarchy, not merely having zero observed arrow of
  time. Their method was not implemented on this exact target in this audit.
* [Skinner–Dunkel, PRL 2021](https://arxiv.org/html/2105.08681v3) already studies
  equilibrium exponential-mixture dwell restrictions and moment optimization.
* [Dechant et al., 2023](https://arxiv.org/html/2303.13038) and
  [Dechant's PSD bounds](https://arxiv.org/html/2306.00417) detect dissipation from
  time-symmetric correlation information, with short-time/high-frequency
  acquisition requirements. Source N507's completely monotone visible scalar
  correlations are specifically designed to avoid elementary spectral tests.
* [Aznagulov, 2026 preprint](https://arxiv.org/html/2609.37205v1) develops a
  dependent-trajectory hidden-equilibrium test based on antisymmetric scores.
  Such scores have zero mean for this exactly reversible observed full law.
* [The October 2026 hidden-dissipation-floor candidate](https://github.com/ipitchford/hidden-dissipation-floor)
  at `fd8d198fcfe50179bc7897ae043f3753f3c96821` is a substantial unrefereed
  comparator on alternating-renewal laws. It is not external validation of the
  Astra candidate.

No strongest-baseline empirical comparison on a real acquired system was
performed. Neither priority nor practical novelty is established. Odd hidden
variables, nonstationarity, and history-dependent observation devices can
change the equilibrium interpretation. Finite arithmetic and agreement among
models are not independent mathematical certification.

An independently tasked model critic found no local error after replaying the
36 local rational feature/residual checks, generator and reversed-generator
bounds, conditional independence, shifted-feature bounds, L2 aggregation, and
statistical constants. A separate statistical subcritic also checked the power
calculation. Both retained the inherited mean/range/gap as unreviewed premises;
their agreement does not establish external correctness.

## Most consequential remaining gate

Find and prove an observable equilibrium obstruction with a **non-negligible
statistical margin relative to its actual variance**, accessible at finite
temporal resolution, that retains the target's all-reflection-CP blindness and
can be acquired without supplied hidden coordinates. The finite-h positivity
facet loss explains why exact exponentiation alone does not cross this gate.
The discrete-time structural-zero protocol is a precise cross-branch lead; its
physical interpretation, sample costs, and separation from standard baselines
must be established independently.
