# Post-isolation adversarial review of the root joint-ancestry operation

**Status and provenance.** This is a post-freeze review, performed after the isolated FL-ancestry audit was frozen. It is not independent invention, external validation, physical calibration, novelty review, or a replay of a producer script. The only FL construction inspected for this follow-up was `work/FL-root/JOINT_ANCESTRY_OPERATION.md`; root is separately implementing its own exact checks. The original frozen audit was not edited.

## Result

I found no algebraic counterexample to the three-state four-point identity, the stated 32-atom P/R separation against the all-telegraph and single-rectangle interfaces, or the chronological-cuts lemma **when its stated fixed-pattern and uniform-mixing hypotheses apply**. The cut constants follow as written.

I did find a material assumption that should be stated directly in the product-statistics clause (target lines 126–140): observation time must be independent of the ancestry-pattern draw, or the full per-product sampling law must explicitly be a product of the uniform observation-time law and a fixed, code-independent history law. Merely specifying the two marginal laws separately does not justify the fixed-mixture Jensen step. If “stationary ancestry law” is intended to include this time-independence, this is a wording repair, not a failure of the conditional theorem. Without it, the variance claim has a concrete counterexample below.

## Checks that survived

For the finite-state code, exact rational arithmetic verified row sums, stationarity, detailed balance, both eigenrelations, (E_pi f^2=1/2), (E_pi h^2=1/4), and (fh=f/2) at three rational parameter pairs, including the boundary (y=2x). The transition kernel in target line 117 is the reversible spectral expansion with the correct coefficients (2) and (4). Direct finite-state path enumeration then matched the four-point formula for 30 gap/tie configurations within (2\times10^{-13}). The displayed conditioning proof itself is exact: condition (f_4) across (d_3); replace (f_3^2) by (1/2+h_3); condition (h_3) across (d_2); use (f h=f/2); and finish with the (f)-eigenmode across (d_1). Coincident times use the identity kernel.

For the P/R witness, exact `Fraction` checks enumerated 16 atoms per model (32 model-atoms in total), all 14 distinct labelled coordinate marginals of orders one through three, the full (L)-law, and the span law. The exact transform difference at (u=1/4,v=1/2) is (9/8192), hence the corrected-mean difference is (9/32768). I also enumerated all 32 six-node binary masks with at most two transitions (the possible sampled membership masks of a single rectangular pulse on these age nodes) and checked equality of the complete five-bin count law at purities (1/100) and (99/100). The algebraic parity/marginal argument in target lines 58–83 supplies the general-τ and arbitrary-pulse-placement step; this finite checker is a spot-check, not a substitute for that argument. Nothing here establishes equality for shaped or multipulse codes, nor superiority against them.

The chronological-cuts constants are consistent. At each reset, a continuation in ([-1,1]) changes by at most (2d(g)) under the half-ℓ1 TV convention. Resetting all cross-color transitions costs at most (2\sum_{e\in E_\times}d(g_e)). Factoring the reset moment into monochromatic blocks and resetting the inter-block transitions in the two one-color products costs at most another (2\sum_{e\in E_\times}d(g_e)). To see the one-use charging, each nonfinal monochromatic block has one outgoing cross edge; the gap to the next event of that same color spans that edge and is at least its gap, so monotonicity of (d) pays for the reset with that edge. Distinct nonfinal blocks use distinct outgoing edges. Every cross edge is one of at most (n^2) cross-list pairs, so

\[
 |\operatorname{Cov}(U_A(0),U_A(s))|
 \le 4\sum_{i,j=1}^n d(|s+a_j-a_i|).
\]

For each fixed (h), monotonicity gives \(\int_0^\infty d(|s-h|)\,ds\le2K_{\rm code}\). Thus the absolute covariance integral is at most (8n^2K_{\rm code}). Stationarity gives

\[
 \operatorname{Var}\left(T^{-1}\int_0^T U_A(t)dt\right)
 \le {2\over T}\int_0^\infty |\operatorname{Cov}(U_A(0),U_A(s))|ds
 \le {16n^2K_{\rm code}\over T}.
\]

The three-state row-TV envelope is also valid: from the spectral kernel and triangle inequality,
\(TV(P_t(i,\cdot),\pi)\le e^{-xt}/2+e^{-yt}/2\), so the displayed (K_{\rm code}\le1/(2x)+1/(2y)) follows. For (n=4), the phase-code term is (256K_{\rm code}/T\le128(1/x+1/y)/T). For a symmetric-contrast count statistic the separate sampling term is (a^{-8}/N), as stated. The independent-campaign decoder inequality has coefficients (16) and (1); it requires independent campaigns (or an explicit covariance term).

The checker exercised the intermediate pointwise cut inequality on 414 finite-state cases with repeated offsets/ties, (n=1,2,3,4), and six shifts. All passed; the least observed right-side slack was about (0.1783875). These floating-point cases are diagnostic only; the argument above is the proof of the uniform constants.

### Independent reconstruction of the P/R parity transform

Set (C=0) temporarily and let (d\in\{0,\tau\}). From the four ages,
\[
 L=\tau(2+X_2-X_1+X_4-X_3),\qquad
 G=\tau(1+X_3-X_2)+d.
\]
Writing (u=e^{-x\tau},v=e^{-y\tau}), the monomial for (e^{-xL-yG}) has prefactor (u^2v e^{-yd}) and bit weights
\[
 (q_1,q_2,q_3,q_4)=(u^{-1},u/v,v/u,u).
\]
For uniform even versus odd parity on four bits, the difference of expectations of \(\prod_iq_i^{X_i}\) is \(\frac18\prod_i(1-q_i)\). Multiplication by the prefactor cancels the denominators and gives
\[
 M_E(d)-M_O(d)=e^{-yd}(1-u)^2(u-v)^2/8.
\]
The P-minus-R mixture difference is one half of the (d=0) parity difference minus its (d=\tau) translate, giving the target's \((1-v)(1-u)^2(u-v)^2/16\). For (Q(x)), deleting the middle-gap factor makes the even/odd difference independent of (d), so P and R cancel for every (x). Span depends only on (X_1,X_4,d), whose parity-class marginal is common. Each pulse boundary can straddle at most one of the adjacent bit-toggle intervals; the two boundaries therefore make the count depend on at most two bits. At shared interval endpoints, one step convention makes at most one adjacent bit switch, so ties do not invalidate the at-most-two-bit conclusion.

## Product-time independence counterexample to the literal weaker reading

Fix the three-state code at (x=2,y=1), and use the valid symmetric contrast (a=1/2,b=0). Its stated mixing envelope has (K=1/(2x)+1/(2y)=3/4). Let (P>0) be fixed and let the product observation time (T_i) be uniform on ([0,T]), where (T=mP). Couple the four ancestry ages within each product by

\[
 A_{i1}=A_{i2}=A_{i3}=A_{i4}=T_i\bmod P.
\]

Across products these histories are iid, code-independent, and have the same marginal law: all four ages equal a uniform random variable on ([0,P)), for every integer (m). Observation times are iid uniform as required. But time and history are dependent within a product, and every entry time is the grid time (T_i-A_{ij}=kP). The corrected per-product conditional mean is therefore
\(Z(kP)^4=Z(kP)^2=1/2+h(Z(kP))\).

The code variance of the conditional sample mean, after infinitely many products, is exactly

\[
 \operatorname{Var}\!\left({1\over m}\sum_{k=0}^{m-1}Z(kP)^4\right)
 ={1\over4m^2}\left[m+2\sum_{r=1}^{m-1}(m-r)e^{-yPr}\right].
\]

Since (T=mP),

\[
 \lim_{m\to\infty} T\,\operatorname{Var}\!\left({1\over m}\sum_{k=0}^{m-1}Z(kP)^4\right)
 ={P\over4}\,{1+e^{-yP}\over1-e^{-yP}}
 ={P\over4}\coth(yP/2).
\]

With (y=1) and (P=1000), this limit is essentially (250), while the target section-5 code term is (16n^2K=256(3/4)=192) after multiplying by (T). There is also a finite strict instance: take (m=2), (T=2000), (N=10000), and (a=1/2,b=0), so (R_W^2=256). The code term plus the claimed sampling term is exactly
\[
 192/2000+256/10000=76/625=0.1216.
\]
But the variance of the code-conditional mean is exactly \((1+e^{-1000})/8>1/8=0.125\), before adding any nonnegative conditional sampling variance. Thus the displayed section-5 inequality fails under this marginal-only interpretation.

This example deliberately violates **time-independent history sampling**: conditional on (T_i=t), its age is (t\bmod P), not a draw from the fixed uniform history law. It does not refute the fixed-pattern lemma or the variance result under independent time/history sampling. It shows why section 5 should say that independence explicitly (or define the full sampling law conditionally on observation time). A stationary code by itself does not repair this coupling.

## Suggested one-sentence repair

Replace the opening of target section 5 with an explicit full-record condition, for example:

> Conditional on the complete stationary code, product records are iid; for each product its observation time (T_i\sim\mathrm{Unif}[0,T]) is independent of its ancestry pattern (H_i), the (H_i) are iid from one fixed code-independent stationary law, and carbon labels are conditionally independent given ((T_i,H_i,Z)).

If the real experiment uses time-dependent survival, age censoring, catalyst drift, or selection of observation times based on product histories, the fixed-mixture Jensen reduction does not apply as written and a separate joint-sampling bound must be acquired.

## Scope limits

This review did not inspect any other FL worker output or a producer/checker script for the optimized waveform competitor mentioned at target line 83. The 32-mask verification above concerns only the claimed single-rectangle interface. Physical isotope neutrality, waveform calibration, preparation/wash-in, count-response conditioning, acquisition cost, and comparison to optimized multipulse or shaped competitors remain empirical or separate-review gates, consistently with the target's own status language.
