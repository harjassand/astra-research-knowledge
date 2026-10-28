# Scalar-reaction audit of one continuous intervention

The supplied physical class supports a global regret certificate from **n+1 scalar reports at one proposed action and its separate forward steps**. No microscopic matrix, hidden dimension, affine actuation model, or coordinatewise monotonicity is needed. In the specified synthetic check the conservative source formula certifies

\[
\sup_{u\ge0,\,\sum u_i\le1/5}[G(u)-G(x)]
\le \boxed{0.144409859210197}.
\]

A further local curvature derivation below handles the general question's omission of a supplied bound on \(\|e\|\) and gives the tighter bound **0.142506013134265** from the same three scalar intervals. All arithmetic underlying these rounded-up bounds is exact rational arithmetic. These are synthetic certificates conditional on the stated physical assumptions; no physical apparatus was acquired or measured.

## Governing public science actually read

Repository revision was confirmed with `git rev-parse HEAD` as `6360a39d9488a041f259181e38c37e638b83c609`. All source links below are pinned to it.

1. **Matrix-concave scalar audit**, `research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/shape/ASTRA_PRO3_MATRIX_CONCAVE_CLASS_AUDIT.md`: [observation contract, shape/curvature proof, and corrected acquisition/certificate, lines 13–78](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/shape/ASTRA_PRO3_MATRIX_CONCAVE_CLASS_AUDIT.md#L13-L78); [hidden gates and the precise excitation limitation, lines 110–145](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/shape/ASTRA_PRO3_MATRIX_CONCAVE_CLASS_AUDIT.md#L110-L145).
2. **All-actions simplex tangent lemma**, `.../source/sharp/ASTRA_PRO3_TASK_SHARP_CONTINUOUS_CERTIFICATION.md`: [tangent inequality, lines 119–131](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/sharp/ASTRA_PRO3_TASK_SHARP_CONTINUOUS_CERTIFICATION.md#L119-L131) and [simplex certificate, lines 190–200](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/sharp/ASTRA_PRO3_TASK_SHARP_CONTINUOUS_CERTIFICATION.md#L190-L200). Its preceding matrix-learning acquisition assumes affine rank-one actuation and is not reused for this question. The tangent lemma only needs concavity and sound gradient intervals.
3. **Completed scoped internal review**, `.../source/curator/RESPONSE_PHYSICAL_REVIEW.txt`: [lines 31–62](https://github.com/harjassand/astra-research-knowledge/blob/6360a39d9488a041f259181e38c37e638b83c609/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-response-and-physical-interfaces/source/curator/RESPONSE_PHYSICAL_REVIEW.txt#L31-L62). This reconstructs the tangent and scalar-audit mathematics and explicitly corrects the monotonicity issue. Its accepted mathematics does not turn missing source-specific matrices, traces, or numerical archives into acquired evidence. Those numerical claims are unnecessary here.

The shape proof's displayed Theorem 2 lower endpoint at lines 64–65 contains a misleading maximum with \(-c_i\). Its proof at line 75 explicitly says to omit that maximum without a monotonicity premise; the review independently makes the same correction. This report uses the corrected raw lower endpoint throughout.

## Derivation and the actual acquisition

Write \(D=\{u\ge0:\mathbf1^Tu\le\delta\}\), and distinguish the fixed physical port vector \(e\) from control coordinate vectors \(E_i\). The supplied physical argument must apply over all of \(D\): real symmetric uniformly SPD \(Q\), joint Loewner concavity, C2 regularity, and the stated derivative caps. The calibrated readout, reproducible dose command, fixed source, reset, and deterministic error envelope must remain valid. The proof only uses the uniform matrix bounds on feasible points/segments; a C2 neighborhood permits the usual derivatives.

**Shape transfer, reused and rederived.** For \(0\le t\le1\), inverse antitonicity followed by operator convexity gives

\[
Q(tu+(1-t)v)^{-1}
\preceq[tQ(u)+(1-t)Q(v)]^{-1}
\preceq tQ(u)^{-1}+(1-t)Q(v)^{-1}.
\]

Thus \(Z=e^TQ^{-1}e\) is convex, so \(G=Z(0)-Z-c^Tu\) is concave over the full simplex. For \(p=Q^{-1}e\), direct differentiation gives

\[
Z_i=-p^TQ_i p,\qquad
Z_{ii}=2p^TQ_iQ^{-1}Q_i p-p^TQ_{ii}p\ge0.
\]

Here symmetry makes the first term nonnegative, and joint matrix concavity gives \(Q_{ii}\preceq0\). If a bound \(\|e\|\le E\) is supplied, the source theorem gives

\[
0\le Z_{ii}\le M_i,
\qquad M_i=E^2(2L_i^2/m^3+B_i/m^2).
\tag{1}
\]

**Required observations.** Choose positive steps \(h_i\) with \(x+h_iE_i\in D\), equivalently \(\sum_jx_j+h_i\le\delta\) for every \(i\). Query the resettable source once at \(x\) and separately at every \(x+h_iE_i\). This consumes n+1 scalar values; reuse a previously paid value only when its dose, source/reset/calibration contract and error envelope still match. Charge every missing preparation, reset, calibration, proposal/screening and refinement experiment. The steps are separate experiments, so their doses are not added within one preparation.

Let \(r_0,r_i\) denote these report centers. First check \(r_k-\epsilon>3/2\) for every report. Then form, with sound arithmetic,

\[
[a_k,b_k]=\left[\frac1{r_k+\epsilon-3/2},
                         \frac1{r_k-\epsilon-3/2}\right].
\tag{2}
\]

If this positivity check fails, this reciprocal operation cannot supply a finite upper interval: return UNKNOWN or acquire stronger information. Deterministic, correlated errors are allowed; repetition alone does not shrink the stated envelope.

**Additional derivation for the stated input contract.** The general question does not explicitly give \(E\), and an unknown dimension does not supply it. This need not block the audit. From \(Q\succeq mI\),

\[
\|p\|^2=e^TQ^{-2}e\le Z/m,\qquad
Z_{ii}\le(2L_i^2/m^2+B_i/m)Z.
\]

Convexity of \(Z\) on the queried segment bounds its value by the maximum of its endpoint values. Consequently the **acquired**, price-independent bound

\[
\widehat M_i=(2L_i^2/m^2+B_i/m)\max(b_0,b_i)
\tag{3}
\]

is valid on \([x,x+h_iE_i]\). This uses only the physical bounds and reports already obtained in (2), without knowing \(\|e\|\) or the dimension. This local substitution is a deduction in this report, rather than a claim that the governing source printed it. The source's global shape theorem and the rest of its proof remain unchanged. If both bounds are available, their minimum is also sound on this segment.

**Acquire simultaneous gradient intervals.** Use any sound segment curvature cap \(K_i\), such as (1) or (3). Integration of \(-K_i\le G_{ii}\le0\) gives

\[
\frac{G(x+h_iE_i)-G(x)}{h_i}
\le G_i(x)
\le\frac{G(x+h_iE_i)-G(x)}{h_i}+\frac{K_i h_i}{2}.
\]

Combining the reciprocal intervals with the known price yields

\[
\ell_i=\frac{a_0-b_i}{h_i}-c_i,\qquad
H_i=\frac{b_0-a_i}{h_i}-c_i+\frac{K_i h_i}{2},
\quad \ell_i\le G_i(x)\le H_i.
\tag{4}
\]

The shared baseline error does not undermine simultaneous deterministic containment. There is **no clipping at \(-c_i\)**. For example, \(Q(u)=2-u,e=1,c=0\) is uniformly SPD on this domain and affine/Loewner-concave, yet \(G'(u)=-(2-u)^{-2}<0\); clipping to zero would be false.

**Certify the whole simplex.** Concavity gives \(G(y)-G(x)\le\nabla G(x)^T(y-x)\). A linear function on \(D\) maximizes at \(0\) or \(\delta E_j\). Negative coefficients require lower gradient endpoints, while nonnegative coefficients require upper endpoints. Therefore

\[
\boxed{C(x,c)=\max\left\{-\sum_i x_i\ell_i,
\ \max_j\left[(\delta-x_j)H_j-\sum_{i\ne j}x_i\ell_i\right]\right\}}
\tag{5}
\]

bounds the regret against **every continuous feasible action**. This works irrespective of the proposal method and needs no acquired optimum. It can be loose; certification of a requested tolerance requires that the computed C meet that tolerance. Neither \(R(0)\) nor \(Z(0)\) is needed for this regret audit, since the common offset cancels in objective differences.

## Executed n=2 synthetic check

For this section only,

\[
Z(u)=\frac{1+u_1}{1+2u_1}+\frac{1+u_2}{2(1+2u_2)}.
\]

The diagonal entries of Q are at least 1 and 2. Their coordinate derivatives have norms \((1+u_1)^{-2}\le1\) and \(2(1+u_2)^{-2}\le2\), and their second derivative norms are at most 2 and 4. Their second derivatives are negative, with no cross terms; hence Q is jointly Loewner-concave. The supplied m=1, L=(1,2), B=(2,4) are valid over the dose simplex. The stencil sums are 0.04 at x and 0.05 at either forward point, so all doses are feasible.

Exact native values were used as centers, but each still received the full \(10^{-8}\) error envelope. The table displays outward-rounded Z intervals:

| Dose point | Exact report center r | Sound Z interval (outward, 12 decimal places) |
|---|---:|---:|
| (1/50,1/50) | 667/306 | [1.471153824510, 1.471153867797] |
| (3/100,1/50) | 35201/16118 | [1.462082707215, 1.462082749970] |
| (1/50,3/100) | 8819/4042 | [1.466618265863, 1.466618308883] |

All lower reaction endpoints exceed 3/2. With \(\|e\|^2=2\), equation (1) gives K=(8,24). Equations (4)–(5), using the exact underlying fractions, give:

| Coordinate | Gradient interval (outward, 12 decimal places) |
|---|---:|
| 1 | [0.807107454188, 0.847116058148] |
| 2 | [0.403551562821, 0.523560193348] |

The vertex upper bounds at \(0,\delta E_1,\delta E_2\) are approximately \(-0.0242131803402031,\ 0.1444098592101961,\ 0.0780986857186873\). Rounding the maximum upward yields the first boxed bound, 0.144409859210197.

For the norm-free local alternative (3), the exact caps are

\[
\widehat M_1=61200000000/10399999847\approx5.88461547118713,
\quad
\widehat M_2=183600000000/10399999847\approx17.6538464135614.
\]

The same lower gradient endpoints and the respective upper endpoints 0.836539135504 and 0.491829425415 (rounded upward) give **C ≤ 0.142506013134265**. This alternative consumes the same three reports.

**Verifier-only numerical check.** The explicit synthetic formulas give the true gradient
\((2787/3380,2787/6760)\approx(0.8245562130177515,0.4122781065088757)\), inside both acquired boxes. Its exact tangent gap is \(47379/338000\approx0.1401745562130178\), below both certificates. Both reward derivatives stay positive on the simplex, so the true optimum uses total dose 1/5. Exact rational bisection of the strictly decreasing full-dose derivative brackets its first coordinate near 0.1883883578467490; a concavity tangent at the lower bracket endpoint certifies the actual regret in

\[
[0.097241384458499,\ 0.097241384458500].
\]

This optimum/gradient computation checks the transparent fixture; it is not input to the report-only learner operation and is not a physical acquisition. The proof supplies uniform soundness over the class; this finite calculation supplies one check of its execution.

Executed artifacts: [check.py](producer-workspace/check.py) and [results.json](producer-workspace/results.json). Running the script completed successfully, including exact interval, gradient-containment, and regret-order assertions. It uses Python's standard-library Fraction arithmetic and writes only into this output folder.

## Reuse when prices change

Retain the dose-tagged raw intervals and their source/reset/calibration/error contract, and retain the independent physical class warrant. At the **same x**, price changes to c' leave the Z intervals and both types of curvature caps unchanged. Shift each gradient endpoint by the known amount:

\[
\ell_i'=\ell_i+c_i-c_i',\qquad H_i'=H_i+c_i-c_i',
\]

then recompute (5), with **zero new scalar reports**. Equivalently retain intervals for the benefit gradient \(-Z_i\) and subtract each task's prices. The bound may become weak after repricing. A newly proposed x' generally needs its own valid stencil; matching cached points can be reused and only missing points queried. The three observations do not identify the whole physical response function or guarantee certificates at arbitrary new actions after the source expires. No 510-reading model-learning prerequisite is involved in this operation. Acquisition, reset, proposal, failed/refinement work and arithmetic remain real costs; no practical advantage or historical novelty is inferred.

## What finite passive observations do not establish

Finite scalar observations do not, without an independently justified structural restriction or source-wide physical argument, establish global joint Loewner concavity, uniform derivative bounds, the calibration/reset law, or an affine rank-one microscopic class. Agreement with a fitted model on observed points is not that warrant. In particular, the governing source's C2 monotone PSD gate \(50(u_j-0.1)_+^3\) is exactly invisible to every observation with \(u_j\le0.1\), while becoming active later and violating Loewner concavity. Its first two derivative magnitudes can remain within the stated kind of caps through the source's orthogonal-block construction. Thus passivity, monotonicity and smooth magnitude bounds do not imply the missing concavity premise.

The source also proves an excitation-counting limit for its **specified finite known** 124-gate family: with total dose 0.2 a query activates at most one coordinate strictly above 0.1. This is not a universal lower bound for arbitrary causal learning, nor a randomized expected-regret theorem. Its missing original numerical traces and witness values are not used here. More generally, finite passive scalar samples alone cannot rule out permitted changes in unobserved regions or reconstruct an unknown-dimensional microscopic source. The real physical class warrant remains an obligation supplied by the question, not a conclusion of this synthetic check.

## Navigation, access, and prior exposure

I read TASK_C.txt and the public 00_START_HERE.txt, then used ordinary file-name navigation and rg over original cards, raw knowledge/units and the lemma atlas for `Loewner`, `scalar reaction`, `dual.?hessian` and `dose simplex`. A broad file listing was noisy/truncated; the targeted search located original cards N1090/N1089 and raw units U1090-scalar-curvature-audit, U1090-monotonicity-guard, U1089-simplex-tangent-regret and U1090-unexcited-threshold-family. I read those files and followed their source paths to the proof and review ranges above. A combined source display was truncated; I reread the decisive simplex range separately. There was no substantive source access failure. The attractive N1089 matrix-learning acquisition was insufficient for the nonlinear general class; only its independently applicable tangent lemma was reused. The printed lower-endpoint shortcut was corrected by reading the governing proof and review.

I did not call the excluded retrieval/search projections, inspect Git history, read memory registries, other chats, experiment protocols/expected scopes, other experimental workers' outputs, or prior study reports. No external browsing was needed. All writes were confined to this output folder.

Actual prior exposure: the preloaded product context included a general Astra memory summary, including the words `dual-Hessian` and `harmonic spring` and generic evidence-scope guidance. It supplied no task-C formula, governing card ID, proof path, or numerical answer. I disclose that context rather than claim total absence of Astra exposure; it was not used as scientific evidence. The matching source IDs, correction, derivations and numerical bounds were obtained during this run.

Outcome: the requested operation was located, read, correctly reused with its monotonicity correction, extended explicitly to the omitted port-norm input, and executed on the specified fixture. The mathematical certificate and its price reuse are established at the stated conditional scope. Actual apparatus acquisition and an independent physical class warrant remain unperformed.
