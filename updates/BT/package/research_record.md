# Delayed division responses: a falsification-first continuation

**Date:** 10 October 2026  
**Programme:** Astra, natural-science branch  
**Scientific status:** No new natural law, molecular mechanism, or historic foundational discovery is established. The results below are explicit model calculations and synthetic measurement tests. Published observations were inspected, but no raw experimental trajectory was acquired or reanalysed. Historical priority and independent correctness remain unestablished.

## 1. Outcome and research decision

The investigation continued the earlier cell-growth and glass-aging work rather than treating its conditional constructions as discoveries. The most developed candidate was a delayed transfer of division-associated randomness into measured growth. It passes several coarse summaries, including a balanced aggregate across/within-division mean-squared-displacement (MSD) ratio. It does **not** thereby explain the observations.

Three independent consequences were then derived: suppression of short-lag changes across division, long quiet intervals within each cycle, and an upturn in the variance of growth averaged since birth late in the cycle. The first remains distinguishable from continuous fluctuations after the controlled noise/smoothing tests. The last is in qualitative tension with published curves. Consequently this response should remain a diagnostic countermodel, not be promoted to a biological explanation.

The mathematical contribution is narrower than the scientific mission: it specifies why one summary is insufficient and how to test this particular alternative. There is no experimental confirmation of the proposed delay or response shape.

## 2. Scientific opportunities assessed

**Cell-growth fluctuations.** Levien et al. study L1210 mass trajectories and favor continuous growth noise. Their Figure 5B places the aggregate MSD ratio near one-half; Figure 5A also tests how time-averaged growth variability changes with age. These are published results, not findings here. [S1] This branch was developed because its earlier candidate could make additional quantitative predictions for the same observable.

**Glass aging.** Böhmer et al. report apparent reversibility in material time. Crucially, their molecular-dynamics observable is **single-particle** potential energy, and their processing suppresses a fast, non-aging component. [S3] A bulk central-limit argument therefore does not explain that result. The earlier proper-Gaussian optical-intensity symmetry remains conditional and does not supply the microscopic aging clock. No raw glass record was obtained.

**Microdroplet peroxide.** Existing primary experiments propose distinct sources, including surface-hydroxyl recombination and oxygen reduction at solid–water interfaces. [S4,S5] A peroxide signal alone cannot adjudicate these mechanisms. Isotope-resolved oxygen accounting, solid-interface controls, and controlled acoustic/electrical inputs would be required. No independently justified new chemical mechanism was obtained, so this branch was screened rather than developed into another fitted explanation.

## 3. Continuity, provenance and evidence access

Astra was entered through `00_START_HERE.txt` and read at commit:

`83acd76e2f876ea68f8ccdf32c1a844d09294343`

The relevant source is the BO record, especially N494–N499. N496's status JSON explicitly retains `source_derived_unreviewed`; its authored proof text is available, but ingestion did not independently certify it. The earlier original is indexed at `web/pages/d-52c8721524abc085.html`, original SHA-256 `da0cd4b68f1a332b63b3ed6e1c9770825070003e39aeffe05cf3d217f2b61a10`. The flat-variance sine/cosine construction below is inherited from that record, not newly discovered in this session.

OpenAI/math was read at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Its varying verification statuses were preserved. No unverified theorem from that collection is a premise of the calculations below. In particular, an equilibrium diluted-spin-glass free-energy result is not used as an explanation of aging dynamics.

The experimental source repository `elevien/L1210` was read at the **tag** `published`, which resolves to commit `53f2a77798ded3441280e5615c677da4b4c72da3`. The raw file `smr_data/traceupdated.csv` is reported as 12,534,116 bytes with Git blob SHA `ebd5efe490070995dcbd08f6ff8fe8f8c9044ed2`. Its bytes were **not** obtained: large-file connector reads, the publisher supplement, and runtime network routes did not provide a usable trajectory. A partial base64 figure response also did not yield a complete local PDF and was not analyzed. These failures are not negative empirical findings.

The PNAS HTML and displayed Figure 5 image were inspected. No experimental coordinates were digitized, no raw-data likelihood was fitted, and no empirical p-value was computed. A June 2026 preprint specifically addressing growth-noise disentanglement was located; its full argument was not accessible for priority comparison. [S2]

## 4. Explicit model and inherited identities

Let x(t) denote a **centered fluctuation** of the logarithmic mass growth rate. Total growth can include a deterministic baseline. Assume fixed division period T, independent innovations eta_n with mean zero and variance sigma_eta^2, and a deterministic causal response h. No biological noise enters between divisions:

\[
x(t)=\sum_{n\in\mathbb Z}\eta_n h(t-nT).
\]

The inherited response is

\[
h_0(t)=\begin{cases}
0,&t<0,\\
\sin(\pi t/(2\delta)),&0\le t<\delta,\\
1,&\delta\le t<T,\\
\cos(\pi(t-T)/(2\delta)),&T\le t\le T+\delta,\\
0,&t>T+\delta.
\end{cases}
\]

Its value is continuous, although some derivatives are not. For cycle phase theta,

\[
x(nT+\theta)=\eta_{n-1}\cos w(\theta)+\eta_n\sin w(\theta),
\quad w(\theta)=\min\{\pi\theta/(2\delta),\pi/2\}.
\]

Independence and sin²+cos²=1 give constant phase variance sigma_eta². The phase-averaged covariance is

\[
\overline C(s)=\frac{\sigma_\eta^2}{T}\int_0^\infty h_0(u)h_0(u+s)\,du.
\]

Consequently,

\[
\tau_{\rm int}=\frac{(\int h_0)^2}{2\int h_0^2}
=\frac{[T+\delta(4/\pi-1)]^2}{2T}.
\]

The triangular integral giving the first equality is half the integral over the positive quadrant. These are exact identities under the stated assumptions, not universal biological laws.

For continuity with the earlier illustration choose T=10.2 hours and **chosen integral memory** tau_int=5.4 hours, giving delta=1.082249683 hours. The published fitted relaxation time is not thereby measured to equal this integral memory. Across-lineage variation is not a confidence interval for a common parameter.

## 5. New conditional-MSD calculation

For lag s, define W(s) as the expected squared growth-rate change, averaged over starting phases with both measurements in one cell. Define B(s) similarly for phases crossing a division. Below, W and B are divided by sigma_eta².

Write k=pi/(2 delta). For 0<s<delta,

\[
W(s)=\frac{2}{T-s}\left[(\delta-s)(1-\cos ks)+s-\frac{\sin ks}{k}\right],
\qquad
B(s)=2\left[1-\frac{\sin ks}{ks}\right].
\]

For delta<=s<T-delta,

\[
W(s)=\frac{2(\delta-1/k)}{T-s},\qquad
B(s)=2\left[1-\frac{1}{ks}\right].
\]

These follow by expanding x(t+s)-x(t), taking the innovation covariance, and integrating separately over the transition and plateau phases. The short-lag ratio tends to T/(T+3 delta)=0.75855, rather than one-half.

Use an explicitly defined aggregate statistic,

\[
R=\frac{\int_0^{4\mathrm h}B(s)\,ds}
{\int_0^{4\mathrm h}[B(s)+W(s)]\,ds}.
\]

For the unshifted inherited response, R=0.924823934. Thus flat age variance and no instantaneous division jump did not make that particular response resemble a stationary division-independent process under this statistic.

### Delaying the response

Set h_l(t)=h_0(t-l) for l>=0. This is still causal. Translation preserves the phase-average covariance and, by periodicity, exact flat phase variance. But it changes the alignment of growth changes relative to division.

Numerical integration and root finding give l approximately **1.301 hours** for R=0.5. This matches a **theoretical stationary null**, not measured data. A second root near 7.817 hours was found but not developed as the primary candidate. High-resolution quadrature checks the first ratio to approximately 2e-7. Do not interpret the stored many-digit root as biological precision.

The delayed construction replaces the inherited fluctuation only during the interval from l to l+delta after division. Before and after that interval it is constant. A possible verbal interpretation is delayed transmission of a regulatory partitioning perturbation, but no measured biochemical network is shown to implement its specially chosen trigonometric transfer.

## 6. Controlled measurement tests: all synthetic

Each model was simulated for 24 lineages of 10 cycles, using minute-scale observations. The continuous comparator was stationary Ornstein–Uhlenbeck noise with correlation time 5.4 hours and growth-rate SD 0.01/hour. Each division-response amplitude was calibrated to match its fixed-period **full-cycle mean-growth variance** to the OU comparator, not arbitrarily chosen to optimize the MSD result.

Growth was integrated to centered log mass and independent Gaussian measurement noise with SD 0.001 was added. This noise level follows the source simulator's setting, not a fit here. [S6] A lineage-wide linear trend was removed, and a Matérn-3/2 Gaussian-process derivative smoother was fitted and applied. Hyperparameter optimization used every fifth observation among the first 4,000. Predictions were evaluated every half-hour.

This reproduces the `Matern32NoTrendModel` covariance, **not the full experimental Julia pipeline**. Actual experimental timestamps, mitotic mass processing, and the real-data cell-cycle trend kernel were not replayed. Our objective used the correct Gaussian marginal likelihood and a 500-iteration optimization budget. Numerical state-space/dense-Gaussian checks are recorded below.

The finite-sample statistic uses equal lag weights at 0.5,1,...,4 hours and equal start-cell weights. It is distinct from the continuous-lag integral in Section 5. Variable cycle durations were independently gamma-distributed with coefficient of variation 0.2, mean 10.2 hours and an explicit lower cutoff at 2 delta; they were not generated by size-control feedback. The gap condition removes one hour of observations centered on each division but allows the smoother to predict inside gaps.

**Aggregate R, mean ± SD across synthetic lineages:**

| Synthetic observation condition | Continuous OU | Unshifted division response | Delayed division response |
|---|---:|---:|---:|
| Fixed periods, no gaps | 0.481 ± 0.069 | 0.920 ± 0.014 | 0.523 ± 0.032 |
| Variable periods, no gaps | 0.499 ± 0.087 | 0.919 ± 0.018 | 0.475 ± 0.061 |
| Variable periods, one-hour gaps | 0.494 ± 0.090 | 0.926 ± 0.016 | 0.473 ± 0.060 |

The SDs are not experimental uncertainties. Seeds are reused across conditions; these conditions are not independent empirical replications. There are 216 simulated model-condition-lineage runs, not 216 independent experiments on nature.

## 7. Predictions not used to set the delay

### 7.1 Short-lag across-division suppression

For the fixed-period delayed candidate, B(s)=0 exactly when 0<s<l: both observations sample the same inherited plateau even though they straddle division. W(s)>0 because within-cell pairs can cross the delayed transition.

The theoretical lag-specific ratio B/(B+W) is 0 at 0.5 and 1 hour, approximately 0.227 at 2 hours, and 0.648 at 4 hours. It is not a flat one-half curve. See `lag_predictions.csv` and `lag_predictions.png`.

The contrast survives the synthetic forward filter. With variable periods and one-hour gaps, the **one-hour-lag ratio** is:

- OU: **0.469 ± 0.094**;
- delayed response: **0.0657 ± 0.0279**.

This is a model-discrimination feasibility result. It is not a measurement of the corresponding ratio in cells.

### 7.2 Quiet intervals and raw log-mass curvature

A quarter-hour latent increment is identically zero for 86.94% of cycle phases in this construction. To test quiet intervals without relying only on a smoothed derivative, consider centered raw log mass Y and

\[
C_h(t)=Y(t+h)-2Y(t)+Y(t-h).
\]

Inside a plateau, biological C_h is zero because Y is linear there. Pair C_h(t) with C_h(t+epsilon) using **six distinct measured samples**. Independent additive measurement errors then give zero contribution to their covariance. This removes the white-noise bias of squaring a single three-point contrast, not all possible measurement bias.

For stationary OU fluctuations, define the integrated variogram

\[
V_Y(s)=2\sigma_x^2\{\tau|s|-\tau^2[1-e^{-|s|/\tau}]\}.
\]

With weights w=(1,-2,1) and offsets a=(-h,0,h),

\[
\operatorname{Cov}[C_h(t),C_h(t+\epsilon)]
=-\tfrac12\sum_{ij}w_iw_jV_Y(\epsilon+a_j-a_i).
\]

At epsilon=0 this reduces to

\[
2\sigma_x^2\tau^2[2u-3+4e^{-u}-e^{-2u}],\quad u=h/\tau,
\]

with small-h leading term 4 sigma_x² h³/(3 tau). The covariance formula follows from zero-sum contrast weights and the covariance–variogram identity; it is not claimed as a new general statistical principle.

For h=1 hour, epsilon=1 minute and the stated OU parameters, the prediction is **2.15296895e-5** in squared log-mass units. Independent double integration of the OU covariance agrees to 9.5e-20 absolute error. In the fixed-period noisy synthetic lineages, the contrast averaged **2.206e-5** for OU and **3.247e-7** for the delayed candidate, whose plateau expectation is zero.

For real data this must be a **centered conditional covariance**, not an uncorrected product contaminated by a deterministic cell-cycle trend. Estimate the trend on held-out cycles, account for lineage effects and variable cycle durations, and verify measurement-error cross-covariance using appropriate controls. Correlated sensor noise, biological baseline curvature, feedback-dependent division, and selection by future cycle duration can invalidate a naive interpretation. No real-data estimate has been made here.

### 7.3 A late-cycle variance upturn: warning against the candidate

Let bar{x}_t=t^{-1} integral_0^t x(u)du. For t>=l+delta within a fixed-period cycle, write

\[
a=l+2\delta/\pi,\qquad b=l+\delta-2\delta/\pi.
\]

Direct integration of the two innovation coefficients gives

\[
\frac{\operatorname{Var}(\bar x_t)}{\sigma_\eta^2}
=\frac{a^2+(t-b)^2}{t^2}.
\]

This has its minimum at t=(a²+b²)/b approximately **4.032 hours**, then increases. At 10.2 hours it is **1.265 times** its four-hour value. The OU counterpart is **0.735 times** its four-hour value.

Several curves in the published Figure 5A decrease or flatten over the corresponding late-cycle range rather than showing the candidate's upturn. [S1] This visual comparison is a qualitative warning, not a formal statistical rejection: the trajectories, trend corrections and survival/age conditioning were not replayed. Nevertheless, it is a reason **not** to defend the delayed construction merely because it matches the aggregate statistic.

## 8. Verification, implementation audit and limitations

The independent adaptive-quadrature MSD calculation agrees with the unshifted closed form to 2.3e-15. The delayed phase-variance identity is checked on a grid to 1.8e-15. State-space log likelihood agrees with dense Cholesky to 8.3e-12, derivative posterior means to 1.6e-14, and derivative variances to 1.2e-16. These are internal numerical consistency checks, not formal proof or external scientific validation.

Two source-code observations are preserved in `implementation_audit.md`, with narrow consequences. One likelihood coefficient differs from the usual Gaussian expression; an exact scale identity shows why this alone does **not** establish that the inferred posterior mean growth dynamics are wrong. A separate matrix construction reads uninitialized storage. Julia was unavailable, and the full original pipeline was not executed. These observations are not a substitute for experimental evidence about biological noise.

The central biological gaps are stronger than computational correctness: the response shape has not been derived from chemical reactions, the division innovation has no independently measured molecular source, and its independent trajectory predictions have not been tested on raw data. The contemporary literature has not been reviewed sufficiently to claim priority for the mathematical/statistical framework. [S2]

## 9. Falsification conditions and exact scientific status

The delayed candidate should be rejected as an explanation of these cells if a correctly calibrated, held-out analysis shows continuous-noise-like one-hour across-division changes, persistent stochastic curvature throughout the proposed plateau, or late-cycle averaged-growth variance incompatible with the upturn. A model with extra continuous noise or a distribution of delays would be a different hypothesis with additional parameters and would require a new held-out test.

A positive biological claim would require joint evidence: phase-resolved growth predictions, independently measured molecular perturbations and delays, and a perturbation experiment shifting the predicted response time without simply refitting the growth trajectory.

**Established in this session:** conditional formulas, an explicit delayed countermodel, internal computational checks, synthetic discrimination tests, and a qualitative warning from an independent published observable.

**Not established:** the true molecular source of growth variability; an explanation of glass aging; a new chemical mechanism; empirical superiority over existing theories; a new law of nature; a historic foundational breakthrough.

## Reproduction

Use Python with NumPy, SciPy and Numba. The exact installed versions are in `provenance.json`. Matplotlib is needed only for the figure.

```bash
OPENBLAS_NUM_THREADS=1 python analysis.py --replicates 24
python delay_test.py
python diagnostics.py
python plot_predictions.py
```

`analysis.py --checks-only` writes a separate check file without overwriting the full run results. Different numerical-library/platform versions can cause small optimization differences. Every trajectory generated by these scripts is synthetic. No script silently fetches, fabricates, or substitutes an experimental dataset.

## Sources

[S1] Levien et al., *Stochasticity in mammalian cell growth rates drives cell-to-cell variability independently of cell size and divisions*, PNAS 123, e2516372123 (2026), DOI: 10.1073/pnas.2516372123. Article HTML and Figure 5 image inspected; raw trajectories unavailable.

[S2] Holtzman, Sheinman and Amir, *Disentangling mechanisms of single-cell growth rate fluctuations*, bioRxiv (June 2026), DOI: 10.64898/2026.06.07.730294. Metadata/accessible abstract information only; full argument not reviewed.

[S3] Böhmer et al., *Time reversibility during the ageing of materials*, Nature Physics 20, 637–645 (2024), DOI: 10.1038/s41567-023-02366-z; arXiv:2312.02395v2. Methods on single-particle energy and time filtering inspected.

[S4] Chen et al., *Water–solid contact electrification causes hydrogen peroxide production from hydroxyl radical recombination in sprayed microdroplets*, PNAS 119, e2209056119 (2022), DOI: 10.1073/pnas.2209056119. Primary bibliographic/abstract evidence used for screening.

[S5] Eatoo and Mishra, *Disentangling the Roles of Dissolved Oxygen, Common Salts, and pH on Spontaneous Hydrogen Peroxide Production in Water: No O2, No H2O2*, JACS 147, 35392–35400 (2025), DOI: 10.1021/jacs.5c09028; arXiv:2505.21175. Competing primary experimental interpretation, not a universal conclusion adopted here.

[S6] `elevien/L1210`, tag `published`, commit `53f2a77798ded3441280e5615c677da4b4c72da3`: `src/GP.jl`, `src/gp_models/matern32.jl`, `pipeline/gp_pipeline.jl`, `pipeline/run.jl`.
