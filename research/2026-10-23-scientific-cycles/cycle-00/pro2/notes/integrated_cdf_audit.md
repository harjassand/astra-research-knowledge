# Independent integrated CDF audit

Agent: `residual_challenge`  
Date: 2026-10-21  
Scope: the mathematical and directed-arithmetic integration in `src/run_experiment.py`, the saved-word coupling contract, and the fixed-envelope stopping proof in `src/diagnose_error.py`. No existing program code was changed by this audit. No new eigensolve, matrix-vector product, or probe draw was performed.

**Result: PASS for the implemented fixed-input calculation, with the reporting qualifications below.** One receiving-identity gap was found, reported, and corrected by the parent before final replay.

## 1. The object actually enclosed

For the exact fixed target `A`, let `F(t)=rank(1[A<=t])/n`. Write the stored probe columns as `gtilde_l`, their normalized versions as `u_l`, and

\[
\alpha_\ell=\frac{\|\widetilde g_\ell\|^2}{\sum_j\|\widetilde g_j\|^2}.
\]

The exact residual checker provides, for each probe and depth, a self-adjoint `B_l`, a unit first polar-basis vector `q_l`, an operator allowance `e_l`, and an effect/probe allowance `a_l`. The Jacobi checker provides conservative CMS bounds `L_l <= F_(B_l,q_l) <= U_l`.

For every positive common margin `eta`, the separately proved projection lemma and probe correction give

\[
L_\ell(t-\eta)-a_\ell-e_\ell/\eta
\le F_{A,u_\ell}(t)
\le U_\ell(t+\eta)+a_\ell+e_\ell/\eta.
\]

Thus, with `Htilde=sum_l alpha_l F_(A,u_l)`, define

\[
\bar L=\sum_\ell\alpha_\ell L_\ell,\quad
\bar U=\sum_\ell\alpha_\ell U_\ell,\quad
\bar a=\sum_\ell\alpha_\ell a_\ell,\quad
\bar e=\sum_\ell\alpha_\ell e_\ell.
\]

Then `barL(t-eta)-bara-bare/eta <= Htilde(t) <= barU(t+eta)+bara+bare/eta`. The weighting of the operator and starting-vector allowances in `Envelope` is correct. The original-input allowance `tau` is already in each `e_l`; averaging contributes it once because the weights sum to one.

The aggregate Gaussian coupling slack `rho` and sampling radius `epsilon` then yield, on the sampling event,

\[
\begin{split}
L(t)&=\max\left\{0,\max_{\eta\in\mathcal E}
  [\bar L(t-\eta)-\bar a-\bar e/\eta-\rho-\epsilon]\right\},\\
U(t)&=\min\left\{1,\min_{\eta\in\mathcal E}
  [\bar U(t+\eta)+\bar a+\bar e/\eta+\rho+\epsilon]\right\}.
\end{split}
\]

These are exactly the implemented formulas, with 15 fixed positive margins. All margins and both depths refer to the same original fixed operator and the same fixed set of eight probes. Intersecting these deterministic enclosures, selecting a margin or depth after viewing them, and evaluating any data-selected thresholds therefore require no additional concentration union bound.

The same argument with weights `1/s` and the mean of the per-column coupling slacks gives the classical spherical-probe band. Its different sampling event must be accounted for separately when combining the two estimators.

## 2. CMS step construction and endpoint directions

For each Jacobi certificate, the code uses

\[
L_\ell(t)=\sum_{j=1}^{k-1}w_{\ell j}^{\rm lo}
  1\{\theta_{\ell,j+1}^{\rm hi}\le t\},
\]

\[
U_\ell(t)=w_{\ell1}^{\rm hi}
  +\sum_{j=2}^{k}w_{\ell j}^{\rm hi}
  1\{\theta_{\ell,j-1}^{\rm lo}\le t\}.
\]

`step_data` implements precisely these conservative lag/lead CMS bounds. Delaying lower jumps to node upper endpoints lowers the lower envelope. Advancing upper jumps to node lower endpoints raises the upper envelope. Including equality in the upper step can add an unnecessary weight at a node; it preserves validity. `bisect_right` correctly implements the inclusive event convention.

The Decimal weight endpoints are converted directly from their decimal strings to `Fraction`. This conversion is exact; subsequent weighting, event accumulation, endpoint comparisons, intersections, and width calculations are rational. An upper envelope can temporarily exceed one, which is harmless before the final upper clipping. No signed-weight argument is being used: all supplied probe weights and spectral weights are nonnegative.

## 3. All-threshold width computation

For a fixed margin, lower steps occur at `node_upper + eta`; upper steps occur at `node_lower - eta`. Taking the union over all supplied margins gives every possible change point of the intersected band. The maxima/minima do not introduce new change points between these locations because every constituent bound is constant there.

The support radius is `R=M+tau`, which bounds the norm of the exact target. Therefore `F(t)=0` for `t<-R` and `F(t)=1` for `t>=R`. The implemented distinction at the negative endpoint is necessary: an atom at `-R` is allowed. Both support endpoints are included in the breakpoint list.

The final band is right-continuous and constant on each interval starting at a listed breakpoint. Evaluating all breakpoints plus one point below the smallest therefore captures the **exact global maximum width of the implemented rational band**, including unbounded tails. This is stronger than checking a threshold grid. It is not a bound on the optimal moment-based confidence interval or on the optimal choice of a different algorithm.

## 4. Concentration-radius directedness

Here `n=1074`, `s=8`, and `delta=1/100`. The two exact logarithm arguments are `200` and `214800`, and the denominators are respectively `8590` and `8608`:

\[
\epsilon_{\rm weighted}=\sqrt{\log(200)/8590},\qquad
\epsilon_{\rm sphere}=\sqrt{\log(214800)/8608}.
\]

Both arguments are exactly represented by the 90-digit Decimal context. `Decimal.ln` is used according to its correctly-rounded, nearest-even contract. Adding a full last-place unit to the rounded logarithm gives an upper bound, because its rounding error is at most half a last-place unit. The addition is exact at this precision, including a possible decimal carry. Conversion of that result to `Fraction` is exact. The subsequent integer-square-root enclosure and final upward dyadic rounding preserve the upper direction.

For these admitted constants, this chain is sound. The function is not a general logarithm-enclosure API: the check that the argument denominator equals one alone would not ensure exact Decimal conversion for an arbitrary integer with more than 90 significant digits. No such input occurs in this experiment. The validity of the even-Gaussian concentration theorem is used only at the fixed even sample count `s=8`.

## 5. Exact probability event for saved uniform words

Let `N=2^64`. For each Box--Muller pair, let `J,H` be independent uniform integers in `{0,...,N-1}`. Introduce independent auxiliary continuous uniforms `Z,W` in `(0,1)` and set

\[
U=(J+Z)/N,\qquad V=(H+W)/N.
\]

Unconditionally, `U,V` are independent Uniform(0,1). Ideal Box--Muller applied to each pair gives mutually independent standard Gaussian entries. The row-major placement into the block does not compromise independence of the ideal probe columns. The auxiliary offsets are a mathematical coupling device; they need not be generated or stored.

On the event `C0` that every radial word `J` is nonzero, the integer interval module bounds every ideal point in every saved cell. Its global and per-column Euclidean error bounds imply, uniformly for all spectral projectors,

\[
\sup_t|H_G(t)-H_{\widetilde G}(t)|\le\rho,
\]

and the corresponding per-column bounds for the separately normalized probe estimator. The global error accounts for changes of both the directions and the norm-squared weights. It would be incorrect to retain ideal Gaussian weights while using only stored direction errors; the present implementation does not do that.

There are `4296` radial words, so

\[
\Pr(C0^c)\le p_0=4296/2^{64}.
\]

Let `Cw` be the ideal aggregate-normalized, all-threshold concentration event, and `Cs` the ideal equal-weight spherical event. Their individual probabilities are at least `0.99`; no independence between them is assumed. Hence

\[
\Pr(C0\cap Cw)\ge0.99-p_0,\qquad
\Pr(C0\cap Cw\cap Cs)\ge0.98-p_0.
\]

On the relevant event, every successfully checked deterministic band is valid simultaneously at every threshold and both saved depths. The candidate and classical bands must not be intersected or selected between while retaining a blanket joint 99% claim. Splitting the failure budget would give a 99% joint guarantee, but changes the radii and must be declared.

There is also a useful precise algorithm interpretation: under the iid-word model and without redrawing or selecting among repeated runs, the unconditional probability of **issuing an incorrect candidate band** is at most `delta`. A bit string that produces an incorrect issued band would fail the ideal concentration event for every auxiliary offset in its cells, because the coupling is deterministic for all of them. The same statement separately holds for the classical band; the probability of issuing at least one incorrect band is at most `2delta`. Exceptional cells cause no output, rather than an incorrectly certified numerical result. If no-output is counted as failure of the complete useful-result contract, its probability must be included separately.

The recorded `p0` is specifically the excluded radial-cell probability. It is not, by itself, a proved bound on every possible abort, such as a rejected numerical witness or a zero stored probe column. The observed run accepted all its deterministic checks; that observation does not establish a general abort-probability theorem.

All these are repeated-draw guarantees under the stated iid uniform-word hypothesis. They are **not** posterior probability statements conditional on the particular archived bit string, and replay does not establish physical entropy or independence of `os.urandom`. The generator preserves the initial words and refuses an automatic redraw; the deterministic fixture mode explicitly carries no statistical coverage claim.

## 6. Receiving identity gap and correction

At first inspection, root replay called `verify_probe_block(WIT)` without its supported expected dimensions. A separately valid block with more than eight columns could then supply a full-block coupling slack while the CDF calculation used only an eight-column prefix. A full-block normalized slack need not bound that prefix.

The parent corrected this. The inspected final version binds expected `n` and `s` in Gaussian replay, checks the saved shape and denominator, requires `gcert` dimensions to match analysis, requires exactly eight per-column slacks, and requires exactly eight Krylov certificates for each depth. These checks address the specific gap. No code was edited by this audit agent.

## 7. Dense comparator counts

Given the independently verified sorted eigenvalue intervals `[d_i-e,d_i+e]`,

\[
L_D(t)=n^{-1}\#\{i:d_i+e\le t\},\qquad
U_D(t)=n^{-1}\#\{i:d_i-e\le t\}
\]

are correct for the inclusive CDF. The ambiguity contributed by eigenvalue `i` is the indicator of the half-open interval `[d_i-e,d_i+e)`. Thus the code's `+1` event at the lower endpoint and `-1` event at the upper endpoint are correct, including coincident events, repeated eigenvalues, and radius zero. Summing all simultaneous changes before evaluating the count avoids inventing a positive-width endpoint ambiguity.

The independent small arithmetic audit used a different equivalent formulation: at an interval start `t=d_i-e`, active centers satisfy `d_i-2e < d_j <= d_i`. A sliding window over the sorted exact centers, removing every left center with `d_i-d_j >= 2e`, gives the global maximum overlap. It reproduced **nine ambiguous eigenvalues**, hence maximum dense CDF width `9/1074`. Direct exact endpoint counts at `t=1/10000` reproduced **604/1074 on both sides**.

## 8. Fixed-envelope floor: complete local stopping proof

The saved threshold is

\[
x=12983/536870912.
\]

For every saved probe at each tested depth, exact root enclosures establish

\[
\theta_{\ell1}^{\rm hi}<x<\theta_{\ell2}^{\rm lo}.
\]

The threshold is inside `[-R,R)`, so no support override collapses the CDF interval there. For **every positive margin**,

\[
L_\ell(x-\eta)=0,\qquad
U_\ell(x+\eta)\ge w_{\ell1}^{\rm hi}+w_{\ell2}^{\rm hi}
\ge w_{\ell1}^{\rm lo}+w_{\ell2}^{\rm lo}.
\]

Consequently all implemented lower bounds at `x` are zero after clipping, regardless of nonnegative transfer, start, coupling, or sampling allowances. Every upper bound is at least

\[
c=\sum_\ell\alpha_\ell
  (w_{\ell1}^{\rm lo}+w_{\ell2}^{\rm lo}).
\]

Because `0<=c<=1`, clipping upper bounds at one does not invalidate the lower bound `U(x)>=c`. Neither intersecting any collection of positive common margins nor taking their continuum infimum can lower the width below `c`. The same argument even permits a different positive margin for each probe.

The exact rational floors are saved in the receipt. Safe decimal lower displays, rounded **down**, are:

| Depth | Certified fixed-envelope width floor |
|---|---:|
| 32 | 0.662533215753441563 |
| 64 | 0.594136495994455906 |

At depth 64, the recorded candidate median width is approximately `0.6196777123794612`. Even setting every numerical and statistical allowance to zero cannot reduce the fixed envelope family below its displayed floor. The exact recorded floor is approximately `0.594136495994456`; this nearest-rounded decimal must not be misrepresented as an outward lower endpoint.

This closes attempts to rescue the **same saved Jacobi matrices, saved weighting, and lag/lead CMS family** by choosing better positive transfer margins or reducing only their allowances. It does not establish an optimal truncated-moment ambiguity, a lower bound for every spectral algorithm, or a universal SLQ impossibility. Adding independent information, changing the approximation objects, or solving a sharper moment problem lies outside this floor. No such new calculation was initiated here.

## 9. Interpretation and accounting limits

- `deterministic_probe` sets both sampling and Gaussian-coupling slack to zero. It encloses the **stored norm-weighted probe CDF**, not the unweighted target spectral CDF. Its width is useful for decomposing the error mechanism, but cannot be presented as a certified target error.
- The reported `statistical_increment` in `diagnose_error.py` includes the Gaussian coupling slack as well as sampling. It is an observed difference between the two computed bands. The `numerical_transfer_increment` includes the chosen positive shifts and transfer/start allowances relative to the unshifted CMS enclosure.
- A smaller displayed candidate radius than the cited spherical bound concerns the changed aggregate-normalized estimator and that displayed guarantee. It does not prove universally smaller estimator variance or superiority to every established spectral method.
- Display thresholds were selected using the dense diagnostic solve. Selection is statistically valid because the band is simultaneous. The dense work still belongs in actual end-to-end experiment costs; separately attributed candidate costs can be reported with that distinction stated.
- Per-stage `peak_rss_bytes` comes from process high-water RSS. After an earlier large allocation, a later stage can inherit the same peak without itself allocating that memory. These are not isolated incremental stage-memory measurements.
- The observed cost and width comparison rejects the claimed advantage of this particular implementation on this input. It does not prove a general computational lower bound.

## 10. Observed audit resources and replay boundary

`results/integrated_cdf_audit_receipt.json` records the small independent exact arithmetic check. It binds hashes of the inspected source files; checks all first-node gaps, stored weight identities, the interior support condition, the exact floor and zero-error upper sums; checks the dense threshold count; and verifies the global dense ambiguity through the independent sliding-window formulation.

Observed audit body costs, including NumPy import, were wall `0.07545072900029481` seconds, CPU `0.6148932349999999` seconds, and peak process RSS `25,911,296` bytes on the Linux runtime. New probes, matrix-vector products, and eigensolves were all zero. Agent reasoning, source reading, and note preparation are outside those script-body measurements.

This audit relies on the already independently replayed root/residual/Jacobi certificates for their respective exact-input guarantees. It does not claim to have rerun their full verification or the experiment. Their proofs and full replay programs remain separate archived dependencies.
