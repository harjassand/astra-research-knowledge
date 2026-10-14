# Independent audit: hidden dissipation from three passive observations

**Date:** 15 October 2026. **Status:** mathematical derivation independently checked below; no laboratory observation, peer review, or exhaustive novelty assessment. This follow-up audits the root's geometric-mean argument and records the earlier, weaker reversibilization check. It does not identify the exact all-architecture optimum or an attaining model.

## Result and quantifiers

Let \(Q\) be **any finite irreducible stationary CTMC generator** in row convention, with stationary law \(\pi\), all microscopic variables even under ordinary time reversal, and a deterministic observation \(Y=h(X)\). Let \(B\) be one observed label, \(p=\Pr(Y_0=B)>0\), and for a fixed \(t>0\) define

\[
 a=a_t=\Pr(Y_t=B\mid Y_0=B)=\Pr(Y_{-t}=B\mid Y_0=B),\quad
 b=b_t=\Pr(Y_{-t}=B,Y_t=B\mid Y_0=B),\quad
 D=p(a^2-b).
\]

If \(0<a<1\) and \(D>0\), then every exact realization with finite entropy-production rate \(\sigma(Q)\) obeys \(D<a(1-a)\) and

\[
 \boxed{\displaystyle \sigma(Q)\ \geq\ -\frac1t\log\left(1-\frac{D}{a(1-a)}\right).}\tag{1}
\]

The centering \(a\) in (1) is convenient but not optimal. Put \(w_{00}=1-2a+b\), \(w_{01}=a-b=w_{10}\), and \(w_{11}=b\). If these cells are positive and \(b<a^2\), then \(w_{01}>\sqrt{w_{00}w_{11}}\), and a stronger certificate is

\[
 \boxed{\displaystyle
 \sigma(Q)\geq-\frac1t\log(1-C_t),\qquad
 C_t=2p\bigl(w_{01}-\sqrt{w_{00}w_{11}}\bigr)>0.}\tag{1*}
\]

Boundary cells are treated by a one-sided limit. The claim is **uniform in hidden dimension and hidden rates**, and needs only the observed three-time law. It does not require an alternating-renewal target. If \(\sigma(Q)=+\infty\), the lower bounds are vacuous. Any finite-cost exact realization forces \(C_t<1\).

For the target \(P_q\) observed from the three-state ring of the primary sources, \(q\in(0,1)\), \(p=2/3\), \(s=1+q\), and the result implies

\[
 \boxed{\displaystyle V_\infty(P_q)\geq\frac23(1-\sqrt q)^2}.\tag{2}
\]

In particular, \(V_\infty(P_{1/20})\geq(21-4\sqrt5)/30\approx0.4018576030>2/5\), since \(9>4\sqrt5\). These are target inverse-time units with \(k_B=1\). This improves the **previously released candidate lower certificate** \(V_\infty(P_{1/20})>0.017568198744\), but is well below the ring realization's cost \((19/20)\log20\approx2.84595\). Neither number locates the optimum or settles attainment.

## Proof audit: the geometric path measure

Write \(Q^*=D_\pi^{-1}Q^{\mathsf T}D_\pi\) for the stationary reverse and consider the microscopic path laws \(P=P_Q^{[-t,t]}\) and \(P^*=P_{Q^*}^{[-t,t]}\). Both start with \(\pi\) at the left endpoint. Stationarity gives \(Q^*_{ii}=Q_{ii}\). If a positive edge has no reverse, \(\sigma(Q)=+\infty\); the rest of this proof assumes finite cost, so the path laws have mutual support.

For any common dominating path measure, define \(\mu=(P+P^*)/2\) and the **subprobability** \(\nu\) with density \(\sqrt{dP\,dP^*}\). Arithmetic-geometric mean gives \(\mu-\nu\geq0\) as a measure, with total mass \(1-A\), where \(A=\int\sqrt{dP\,dP^*}\) is the path Hellinger affinity. This is an inequality between path measures; \(\mu\) is not the path law of the additive reversibilization.

The product-of-jump-rates path density shows that \(\nu\) has initial law \(\pi\) and a killed generator \(G\) with

\[
 G_{ij}=\sqrt{Q_{ij}Q^*_{ij}}\quad(i\ne j),\qquad G_{ii}=Q_{ii}.
\]

The holding-time factors combine without an extra potential because \(Q_{ii}=Q^*_{ii}\). Its row sums are nonpositive by arithmetic-geometric mean. Moreover \(\pi_iG_{ij}=\sqrt{\pi_i\pi_jQ_{ij}Q_{ji}}=\pi_jG_{ji}\), so \(G\) is self-adjoint in \(L^2(\pi)\). Killing, rather than normalizing, is essential: normalization would generally destroy this simple path formula.

Fix \(f=1_B-a\mathbf1\) and the symmetric path score

\[
 W=1_B(X_0)f(X_{-t})f(X_t).
\]

Reversal swaps the endpoints and leaves \(W\) unchanged, hence \(E_\mu W=E_PW=-D\). For the geometric submeasure, the killed Markov composition and self-adjointness give the exact nonnegative square

\[
 E_\nu W
 =\sum_i\pi_i1_B(i)\,[e^{tG}f(i)]^2\geq0.\tag{3}
\]

Because the three factors are binary-centered, \(W\geq-a(1-a)\) pathwise. Therefore

\[
 -D=E_\nu W+E_{\mu-\nu}W\geq-a(1-a)(1-A),
 \qquad D\leq a(1-a)(1-A).\tag{4}
\]

The full-path relative entropy is \(D_{\mathrm{KL}}(P\Vert P^*)=2t\sigma(Q)\): stationarity removes boundary entropy and the same holding rates cancel in the likelihood ratio. Jensen applied to \(A=E_P\exp[-\tfrac12\log(dP/dP^*)]\) yields \(A\geq\exp[-t\sigma(Q)]\). Combining with (4) yields \(D\leq a(1-a)(1-e^{-t\sigma})\), and rearranging proves (1). **The direction of both inequalities is as needed**: replacing \(A\) by its lower bound makes the allowed deficit larger, not smaller.

The same proof works with **any** score center \(r\in(0,1)\): put \(f_r=1_B-r\mathbf1\), \(W_r=1_B(X_0)f_r(X_{-t})f_r(X_t)\), and \(D_r=-E_QW_r=p[\delta-(a-r)^2]\), where \(\delta=a^2-b\). If \(D_r>0\), then \(\sigma\geq-t^{-1}\log[1-D_r/\{r(1-r)\}]\). To optimize this ratio, set \(z=r/(1-r)>0\). A direct expansion of the four conditional endpoint cells gives

\[
 \frac{D_r}{r(1-r)}
 =p\left[2w_{01}-w_{00}z-\frac{w_{11}}z\right]
 \leq 2p\left(w_{01}-\sqrt{w_{00}w_{11}}\right)=C_t.
\]

Equality holds at \(z=\sqrt{w_{11}/w_{00}}\), equivalently \(r=\sqrt{w_{11}}/(\sqrt{w_{11}}+\sqrt{w_{00}})\). This proves (1*); \(w_{01}^2-w_{00}w_{11}=a^2-b>0\) proves its positivity. The optimized inequality is a new derivation in this audit, not an optimum over all possible observable scores.

The proof requires the usual finite-state, stationary, noninvasive deterministic observation model. It does not apply as written to odd-parity microscopic reversal, time-dependent generators, causal measurements that alter \(Q\), or arbitrary temporally correlated observation noise.

## Exact ring calculation and independent checks

For

\[
 Q_q=\begin{pmatrix}-s&1&q\\q&-s&1\\1&q&-s\end{pmatrix},\quad
 \pi=(1/3,1/3,1/3),\quad h(0)=A,\ h(1)=h(2)=B,
\]

put \(\gamma=3s/2\) and \(\omega=\sqrt3(1-q)/2\). Conditional on \(X_0=1\) or \(2\), the future \(B\)-success probabilities are

\[
 u(t)=\frac23+e^{-\gamma t}\left(\frac{\cos(\omega t)}3+\frac{\sin(\omega t)}{\sqrt3}\right),\qquad
 v(t)=\frac23+e^{-\gamma t}\left(\frac{\cos(\omega t)}3-\frac{\sin(\omega t)}{\sqrt3}\right).
\]

The past probabilities swap \(u,v\). Consequently \(a=(u+v)/2=2/3+e^{-\gamma t}\cos(\omega t)/3\), \(b=uv\), and

\[
 a^2-b=\frac13e^{-3st}\sin^2(\omega t)>0
 \quad\text{for }\sin(\omega t)\ne0.\tag{5}
\]

As \(t\downarrow0\), \(a=1-st/2+O(t^2)\), \(w_{01}=st/2+O(t^2)\), \(w_{00}=qt^2+O(t^3)\), and \(w_{11}=1+O(t)\). Hence \(C_t/t\to p(s-2\sqrt q)=\frac23(1-\sqrt q)^2\), proving (2). The unoptimized right side of (1) tends to \((1-q)^2/[3(1+q)]\), equal to \(361/1260\) at \(q=1/20\). For **each** finite exact realization the finite-\(t\) inequality holds for every sufficiently small \(t\); taking this target-law limit before the infimum over hidden realizations creates no hidden uniform-rate assumption.

At \(q=1/20,t=3/10\), an independent 60-digit matrix-exponential check gave \(a=0.8681827585774305281\ldots\), \(E_QW=-D=-0.00515576738019247919\ldots\), \(E_\nu W=0.00234432217129927112\ldots\), \(A=0.6965108954780772159\ldots\), and \(a(1-a)(1-A)=0.0347317350885180571\ldots\). Formula (1) gives \(0.15365980295790974\ldots\); optimizing the center via (1*) gives \(0.17033643656648687\ldots\). These numerics check the signs and factors; the exact small-time constant follows from the algebra above, not from floating point. The scripts high_precision_geometric_check.py and audit_calculations.py in this worker directory reproduce the checks; neither certifies a global optimum.

## Independently checked jitter and stochastic-readout extension

The square argument survives **independent identically distributed** left and right sampling gaps \(T_-,T_+\sim\rho\), independent of the CTMC, with finite common mean \(m>0\). It also survives a fixed, passive, memoryless binary readout: at each sampled time, conditional on microscopic state \(i\), independently draw \(Z\in\{0,1\}\) with \(\Pr(Z=1\mid X=i)=b_i\in[0,1]\). Choose any score center \(r\in(0,1)\), for example the common conditional endpoint marginal \(\Pr(Z_{T_+}=1\mid Z_0=1)=\Pr(Z_{-T_-}=1\mid Z_0=1)\), whose equality follows from stationarity when the same channel is used at all three times, and let

\[
 W=Z_0(Z_{-T_-}-r)(Z_{T_+}-r),\qquad D=-E_Q W>0.
\]

The common gap distribution and endpoint channel make the joint observation protocol invariant under time reversal. Attach its common clock and sensor kernel to \(P\) and \(P^*\); their geometric mean retains that kernel. With \(f=b-r\mathbf1\), integrating the iid gaps in the killed path law gives

\[
 E_\nu W=\sum_i\pi_i b_i\left[ E_{T\sim\rho}(e^{TG}f)(i)\right]^2\geq0.\tag{6}
\]

Because \(W\geq-r(1-r)\), (4) holds with \(a\) replaced by \(r\). Conditional path affinity over a total length \(T_-+T_+\) is at least \(e^{-\sigma(T_-+T_+)/2}\); averaging and Jensen give \(A\geq e^{-m\sigma}\). Hence

\[
 \boxed{\displaystyle \sigma(Q)\geq-\frac1m\log\left(1-\frac{D}{r(1-r)}\right).}\tag{7}
\]

The center channel may be a different fixed Bernoulli kernel \(c_i\); then the factor \(b_i\) outside the square in (6) becomes \(c_i\). Keep \(r\) as any chosen scalar and compute \(D=-E_QW\) directly: with distinct center and endpoint kernels, the two conditional endpoint marginals need not coincide under a nonreversible chain. Equal *endpoint* kernels and identically distributed independent gaps remain the relevant conditions. A common passive sensor at three times is the most direct physical interpretation. Unequal or correlated gaps, state-dependent clock selection, temporally correlated readout errors, and measurement disturbance need separate analysis; (6) must not be silently applied to them. Random jitter needs its actual distribution or a justified uncertainty set; the theorem is not an empirical calibration of clocks or sensors.

If the conditional endpoint cells given \(Z_0=1\) are now \(w_{uv}\), possibly with \(w_{01}\ne w_{10}\), the same one-dimensional optimization gives the observable coefficient \(C=p_0[(w_{01}+w_{10})-2\sqrt{w_{00}w_{11}}]\). If \(C>0\), (7) holds with its logarithm argument \(1-C\). This formula does not assume equal conditional endpoint marginals; it only uses the reversal-symmetric score and protocol.

An independently executed floating fixture for \(P_{1/20}\), with iid gaps taking \(0.2\) or \(0.4\) with equal probability (\(m=0.3\)), illustrates the scope. Ideal three-time readout gives \(r=0.870657154122\ldots\), \(D=0.004726050508\ldots\), and bound \(0.142910468104\ldots\). With independent symmetric \(10\%\) errors at **all three** times, \(D=-0.004846820337\ldots\), so this score gives no positive certificate even though the theorem remains true. If only the endpoints have that error and the center is ideal, \(D=0.003024672325\ldots\) and the bound is \(0.062796021825\ldots\). These are model calculations, not measured sensor performance.

## Earlier additive-reversibilization certificate: valid but superseded here

The 3 October candidate release already proves the path comparison for \(R=(Q+Q^*)/2\): \(D_{\rm KL}(P_Q^{[0,T]}\Vert P_R^{[0,T]})\leq T\sigma(Q)/4\). The killed \(R_B\) is self-adjoint and negative, so its no-exit \(B\)-persistence \(H_R(t)\) is completely monotone. If the target's third finite difference \(d_h=H(3h)-3H(2h)+3H(h)-H(0)>0\), the nested event score takes values \(-1,0,2\), with range width 3; Pinsker on \(T=3h\) then gives the valid but weak certificate \(\sigma\geq8d_h^2/(27h)\). For \(q=1/20\), \(H'''(0)=2387/8000>0\), so positive \(d_h\) exists for small \(h\). A floating grid of \(h=0.001,\ldots,10\) gave a best displayed value \(1.0197\times10^{-5}\) at \(h=0.419\), **not** a certified optimum. Squaring a negative \(d_h\) would be invalid. This route is substantially weaker than both (2) and the candidate release's fixed-window certificate.

For a more operational comparison, the candidate release's fixed-window result requires continuous no-exit observation on both sides. The new bound (1) uses only three passive snapshots, though a near-zero-time implementation would demand increasing temporal resolution and statistical precision. Its negative score is \(O(t^2)\) while \(1-a=O(t)\); a distribution-free Hoeffding calculation for independent bounded triplet scores and a \(t^2\) absolute margin scales as \(t^{-4}\) replicates. Target-specific variance and structured estimation may improve that scaling, and repeated samples from one trajectory require dependence/mixing analysis. Infinite precision at arbitrarily small \(t\) is a property of the **exact target law**, not an experimentally established affordance. At any fixed \(t>0\), (1) remains a finite-window certificate with a finite, weaker constant.

## Prior art and status

The original [thermodynamic-realizability preprint](https://arxiv.org/html/2609.14623) conjectures zero all-dimension cost in §6 and calculates a positive dwell-density slope in §8.8. A later, unreviewed [Evidence Press release](https://www.evidencepress.org/releases/hidden-dissipation-floor/) and its [full source](https://github.com/ipitchford/hidden-dissipation-floor/blob/main/PAPER.tex) already refute zero cost under the finite stationary even-variable assumptions, supply the additive-reversibilization path inequality and a stronger qualitative zero-cost classification, and explicitly leave the positive optimum and attainment open. The geometric-mean proof above is an independently audited improvement to the *numerical lower certificate and sampling access*, not a first refutation of the conjecture. A targeted reading of that release found no Hellinger/geometric-mean path construction, but wider prior art for this exact bound is **UNKNOWN**. Geometric rate symmetrizations are themselves established; see [Choi and Wolfer, Systematic Approaches to Generate Reversiblizations of Markov Chains](https://arxiv.org/abs/2303.03650). Their conservative reversiblizations should not be conflated with the killed geometric path measure used here. General thermodynamic inference from coarse observations predates both works; see, for example, the primary [Nature Communications study on broken detailed balance without observable currents](https://www.nature.com/articles/s41467-019-11051-w).

The decisive remaining tests are (i) independent specialist proof review of the geometric-submeasure identification and the small-time quantifier; (ii) a systematic primary-literature search for equivalent Hellinger/path-affinity lower bounds; and (iii) a finite-rate, sampled-readout study with calibrated jitter/noise and valid confidence intervals, comparing (7) against matched existing estimators. None has been completed here.
