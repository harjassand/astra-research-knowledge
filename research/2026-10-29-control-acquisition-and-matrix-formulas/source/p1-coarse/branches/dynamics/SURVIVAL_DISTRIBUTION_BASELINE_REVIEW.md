# Review of the standard survival-distribution baseline

## Verdict

`core/survival_distribution_baseline.py` is sound for the complete survival curve of one repeatedly applied operation, from an identically prepared source with independent trials and an exact, nonintrusive absorbing-event report. Its uniform certificate requires neither a hidden-rank bound nor eventual absorption. A positive probability of never being absorbed is covered by the censored mass.

The method is the standard Dvoretzky–Kiefer–Wolfowitz–Massart empirical-distribution band, with a conservative treatment of the censored tail. It is a strong existing baseline for this single-curve question, not a new predictive-state construction. A hidden-rank closure certificate is unnecessary here.

## Fixed censor cap and the all-length proof

Let T be the absorption time, taking values in the positive integers together with infinity. Define survival by S(h)=Pr(T>h), so a death at step t contributes to survival through step t−1 and not at step t. Fix a deterministic censor cap C before acquiring the data. The observed variable is

\[
Y=\min(T,C+1),
\]

where Y=C+1 denotes every trajectory still alive after step C, including T=infinity. This is an ordinary finite-valued random variable. Its independent samples therefore satisfy the usual two-sided DKW–Massart inequality

\[
\Pr\!\left(\sup_y|\widehat F_Y(y)-F_Y(y)|>\epsilon\right)
\le 2e^{-2n\epsilon^2}.
\]

For every integer 0≤h≤C, Pr(Y>h)=S(h). The estimator used in the code is the empirical fraction of recorded Y values greater than h on this range, so its error is at most epsilon on the single DKW event, simultaneously for every such h.

For h>C, the estimator is zero. If m observations were censored, monotonicity gives

\[
0\le S(h)\le S(C)
\le \widehat S(C)+\epsilon
=m/n+\epsilon.
\]

Hence the implemented estimator obeys

\[
\sup_{h\ge0}|\widehat S(h)-S(h)|\le\epsilon+m/n
\]

with the same failure probability. There is no extra union bound over repetition lengths and no extra tail event. The cap is fixed; stopping each path at actual absorption merely avoids executing an already absorbed state. If every acquired path dies before C, stopping the overall software loop then is also harmless. The censor rule is unchanged.

This proof handles never-absorbed mass directly. On the good event, that mass is at most m/n+epsilon. It is not assumed to be zero. When m is large the certificate becomes loose, which correctly exposes an unresolved tail; the software does not silently infer eventual absorption.

Reference: P. Massart, “The Tight Constant in the Dvoretzky–Kiefer–Wolfowitz Inequality,” *The Annals of Probability* 18(3), 1269–1283 (1990), [DOI 10.1214/aop/1176990746](https://doi.org/10.1214/aop/1176990746). The two-sided theorem applies to arbitrary distribution functions, including the discrete censored variable above.

## Source simulation and receipt replay

The private fixture chooses one of two absorption probabilities, 1/32768 or 1/32, with equal probability independently for each preparation. A living trajectory then uses exact integer draws with its selected probability at each step. The hidden mixture component is not supplied to inference. Its private survival formula is

\[
S(h)=\tfrac12(1-1/32768)^h+\tfrac12(1-1/32)^h.
\]

This formula is used only for a floating diagnostic. The certificate is distribution-free and does not depend on the mixture formula, its two-component rank or its rates. Vectorized simulation does not omit physical costs: the active count is charged on every clock step, which equals the sum of each observed lifetime capped at C.

An independent saved-count replay verified all 4,000 recorded lifetimes, equality with the raw receipt, the censor count, last observation time and exact resource sum. It generated no trajectories.

| Quantity | Verified value |
|---|---:|
| Independent preparations/trials | 4,000 |
| Fixed censor cap | 1,000,000 |
| Censored observations | 0 |
| Last observed absorption time | 234,748 |
| Primitive applications | 62,181,306 |
| Coarse observations | 62,181,306 |
| Uniform survival error bound | 1/32 |

The exact DKW exponent is 2n epsilon²=125/16. An independently recomputed rational partial sum for exp(125/16) verifies 2 exp(−125/16)<0.001 without trusting floating exponentiation. The code's approximately 0.0168562 private maximum-error diagnostic is not used as evidence for the statistical certificate.

## Actual scope

The guarantee is simultaneous over all repetition lengths of **this one operation** and this total-survival readout. It supports later length selection from the same curve without an additional confidence penalty. It does not supply predictions for unexecuted switching programs, different preparations or arbitrary receivers. Monotonicity of survival is the reason an observed tail-mass bound controls every later length; a general signed or oscillatory port-response curve cannot be handled by this argument.

Independent identically distributed preparations and a truthful absorption report are experimental premises. The earlier conditional live/dead sensor-error theorem does not automatically turn this standard iid DKW application into a dependent-noise DKW theorem. The present executable and reviewed certificate use the exact-report fixture.

The baseline genuinely pays for long survival observations: 62,181,306 native steps and reports are recorded despite only 4,000 preparations. Its measurement count does not replace those execution costs. Within its single-curve scope it already removes the need to identify or close the hidden dynamics.

Reviewed result SHA256:

`8384026644fadab025d1cea1c645e41d1f4699f8e175907f430edeaa9eddfd8e`

Reviewed code SHA256:

`84eef943443e654c397ad6d025733aa9060a97d5de92274e49f85e2eba6b5b72`

The independent checker is `replay_survival_distribution_review.py`; its saved output is `SURVIVAL_DISTRIBUTION_REVIEW_RESULTS.json`.
