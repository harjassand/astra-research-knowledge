# Finite-anchor thermal theorem: independent audit

**Disposition.** The finite-dimensional comparison theorem in the supplied thermal report is valid under its stated assumptions. Its proof is nonperturbative and uniform in spatial volume. The principal qualifications are that the theorem is a fixed-discretization statement, its Fourier statistic is a raw second moment unless centeredness is imposed, and the displayed first-order covariance identity needs the source to be independent of the target at zero coupling. A standard fixed-physical-temperature continuum scaling admits a useful conditional extension when the quartic coupling carries its physical factor of lattice spacing and coordinate moments stay uniformly bounded. The report does not prove that extension without those additional hypotheses.

This is an audit of a particular local-source Langevin drift. It is not a review or refutation of the full Pawlowski–Rothkopf contour algorithm, its finite-resolution data, or its spectral reconstruction.

## 1. Exact scope audited

For a finite product graph with temporal cycle \(\mathbb Z_N\) and finite periodic spatial graph \(\Lambda\), let

\[
K=\alpha I+\kappa_\tau L_\tau+\kappa_xL_x,
\qquad \alpha>0,\quad \kappa_\tau,\kappa_x\geq0,
\]

where the graph Laplacians act as a Kronecker sum. Let \(P\) select \(r\) fixed temporal slices, each with all spatial sites, and put \(Q=I-P\), \(g\geq0\). The target and reference are

\[
dX_s=-[KX_s+gQX_s^{\circ3}+gP Y_s^{\circ3}]\,ds+\sqrt2\,dW_s,
\qquad
dX_s^0=-[KX_s^0+g(X_s^0)^{\circ3}]\,ds+\sqrt2\,dW_s.
\]

Powers are coordinatewise. For each finite \(N,\Lambda\), assume a jointly stationary, adapted coupling \((X,X^0,Y,W)\) exists, the two target fields use the same Brownian motion, and

\[
B=\sup_{j\in\operatorname{supp}P}
\|g(Y_j^3-(X_j^0)^3)\|_2<\infty.
\]

For volume-uniform conclusions, \(B\) must be uniform in \(N\) and \(|\Lambda|\). The source may be correlated with \(X^0\); no source-target independence is used in this theorem. Define \(F_{x,N}(\omega)=N^{-1/2}\sum_t e^{-i\omega t}X_{t,x}\).

The assumptions that matter are the positive mass \(\alpha\), the M-matrix sign pattern of \(K\), fixed anchors, a nonnegative onsite quartic coefficient, the product temporal/spatial kernel, the shared noise for \(X,X^0\), and the finite stationary forcing bound \(B\). There is no claim here for \(\alpha=0\), nonconvex interactions, moving anchors, arbitrary preconditioning/noise covariance, or an unproved source process without a stationary adapted coupling.

## 2. Proof reconstruction

Set \(Z=X-X^0\). At an unanchored coordinate,

\[
X_i^3-(X_i^0)^3=(X_i^2+X_iX_i^0+(X_i^0)^2)Z_i,
\]

and the coefficient is nonnegative because it equals \((X_i+X_i^0/2)^2+3(X_i^0)^2/4\). Thus

\[
dZ_s=-(K+D_s)Z_s\,ds+f_s\,ds,
\]

where \(D_s\) is diagonal, nonnegative and zero on anchors, and \(f_s=-gP(Y_s^{\circ3}-(X_s^0)^{\circ3})\). Since \(-K-D_s\) is Metzler, its propagator \(U(s,u)\) is entrywise nonnegative. The free propagator \(V(s,u)=e^{-K(s-u)}\) is also entrywise nonnegative. Variation of constants gives

\[
V(s,u)-U(s,u)=\int_u^s V(s-v)D_vU(v,u)\,dv\geq0
\]

entrywise. This proves the cooperative comparison \(0\leq U(s,u)\leq e^{-K(s-u)}\), including time-dependent random killing. Also \(\|U(s,u)\|_{2\to2}\leq e^{-\alpha(s-u)}\), since \(K\geq\alpha I\) and \(D_s\geq0\).

Under the assumed stationary finite-moment coupling, the pullback term \(U(s,s-T)Z_{s-T}\) vanishes in \(L^2\) as \(T\to\infty\). Therefore

\[
Z_i(s)=\int_{-\infty}^s\sum_j U_{ij}(s,u)f_j(u)\,du,
\qquad
|Z_i(s)|\leq\sum_{j\in\operatorname{supp}P}\int_0^\infty
(e^{-Kv})_{ij}|f_j(s-v)|\,dv.
\]

Minkowski and stationarity yield

\[
\|Z_i\|_2\leq B\sum_{j\in\operatorname{supp}P}(K^{-1})_{ij}.
\]

For fixed anchor slice \(s\) and output site \(x\), product factorization and mass preservation give

\[
\sum_{t\in\mathbb Z_N}\sum_{y\in\Lambda}
(e^{-Kv})_{(t,x),(s,y)}=e^{-\alpha v}.
\]

Integrating over \(v\geq0\) gives \(\sum_{t,y}(K^{-1})_{(t,x),(s,y)}=1/\alpha\). Summing over the \(r\) anchors then gives

\[
\sum_t\|Z_{t,x}\|_2\leq rB/\alpha,
\qquad
\|F_{x,N}(\omega)-F^0_{x,N}(\omega)\|_2
\leq D_N:=\frac{rB}{\alpha\sqrt N}.
\]

This Green sum is independent of spatial volume. It depends on the product heat-kernel structure and the fact that each anchor slice is summed over its spatial coordinates; it is not a generic identity for arbitrary space-time couplings.

The reference density is proportional to \(e^{-V(x)}\), with \(\nabla^2V(x)=K+3g\operatorname{diag}(x_i^2)\geq K\). The Brascamp–Lieb covariance inequality gives \(\operatorname{Cov}(X^0)\preceq K^{-1}\). Since the reference is centered and a normalized complex Fourier vector has squared norm one,

\[
\mathbb E|F^0_{x,N}(\omega)|^2\leq1/\alpha.
\]

Cauchy–Schwarz now proves the report's raw-second-moment bound

\[
\left|\mathbb E|F|^2-\mathbb E|F^0|^2\right|
\leq 2D_N/\sqrt\alpha+D_N^2.
\]

No decorrelation or mixing estimate is needed. At fixed \(\alpha,r,B\), the amplitude difference is \(O(N^{-1/2})\), and the raw second-moment difference is \(O(N^{-1/2})\). If the target is a connected covariance and the source need not be centered, then \(|\mathbb EF|\leq D_N\) and the corresponding bound is

\[
|\operatorname{Var}_{\mathbb C}(F)-\operatorname{Var}_{\mathbb C}(F^0)|
\leq2D_N/\sqrt\alpha+2D_N^2.
\]

Thus the main result survives for connected covariance, but the report should call its displayed quantity a second moment unless it states centeredness or applies this extra estimate. To identify either statistic with a physical susceptibility also requires the exact lattice-to-response normalization and estimator map; the comparison theorem alone does not supply that map.

## 3. Moment acquisition and a qualification

For the centered reference, tilt the density by \(e^{t x_i}\). The tilted potential has the same Hessian lower bound. Brascamp–Lieb gives \(\frac{d^2}{dt^2}\log\mathbb E e^{tX_i^0}\leq (K^{-1})_{ii}\leq1/\alpha\). Since the reference is even, the first derivative at zero is zero. Hence

\[
\Pr(|X_i^0|>u)\leq2e^{-\alpha u^2/2},\qquad
\mathbb E|X_i^0|^6\leq96\alpha^{-3}.
\]

The same argument gives the source bound if its law is even and its potential has Hessian at least \(\alpha_Y I\), yielding

\[
B\leq g\sqrt{96}(\alpha_Y^{-3/2}+\alpha^{-3/2}).
\]

The symmetry/centering clause is needed. A Hessian lower bound by itself only controls fluctuations around the mean. For example, \(Y\sim N(h,\alpha_Y^{-1})\) has Hessian \(\alpha_Y\) for every \(h\), but its sixth absolute moment is unbounded as \(|h|\to\infty\). So the report's concrete even quartic source is covered; the general source-moment acquisition claim should explicitly require symmetry or a uniform mean bound. The theorem's primary assumption that \(B\) is finite remains sufficient even for asymmetric sources.

A sharper coordinate version replaces \(1/\alpha\) by \((K^{-1})_{ii}\) in the tilted Brascamp–Lieb step. That distinction matters when \(\alpha\) shrinks with the time spacing.

## 4. Source correlation and the exact first-order identity

At \(g=\lambda/6=0\), write \(C=K^{-1}\), \(Q=I-P\), and assume the source is independent of the target Brownian noise. If the source and target are independent centered Gaussians at zero coupling, stationarity of \(XX^T\) and Wick's identity \(\mathbb E[X_i^3X_j]=3C_{ii}C_{ij}\) give

\[
KC_1+C_1K=-\frac{c}{2}(QC+CQ),
\qquad c=C_{ii}
\]

in the homogeneous product case. For a normalized Fourier mode with eigenvalue \(\kappa_q\), and anchor fraction \(f=r/N\), this gives

\[
(C_1)_{qq}=-\frac{(1-f)c}{2\kappa_q^2}.
\]

This formula is correctly scoped in the source report: independence is stated for this calculation, not for the nonperturbative theorem.

If the source is correlated with \(X\) at \(\lambda=0\), the source term does not vanish. In general set \(R=\mathbb E[P Y^{\circ3}X^T]\); the right side gains \(-(R+R^T)/6\). In a scalar example with target and source both stationary OU variables of variance \(1/k\), correlation \(\rho\), and target drift \(-kX-(\lambda/6)Y^3\), Wick gives

\[
\left.\frac{d}{d\lambda}\operatorname{Var}(X)\right|_{0}
=-\frac{\rho}{2k^3}.
\]

The source and target marginals are unchanged as \(\rho\) varies: at \(\rho=0\) the derivative is zero; at \(\rho=1\) it equals the vacuum quartic derivative. Exact rational cases at \(k=3/2\) in [exact_finite_audit.json](exact_finite_audit.json) give \(0,-2/27,-4/27\) for \(\rho=0,1/2,1\). Thus source correlation is decisive for the perturbative identity, but it does not break the main bound so long as the stated \(B\) and stationary coupling hold.

The physical quantum oscillator calculation is a separate derivative. For \(H=p^2/2+\Omega^2q^2/2+\lambda q^4/4!\), the free thermal Euclidean covariance at coincidence is

\[
c_\beta=\frac1\beta\sum_{n\in\mathbb Z}\frac1{(2\pi n/\beta)^2+\Omega^2}
=\frac{1}{2\Omega}\coth(\beta\Omega/2).
\]

One quartic insertion in the connected two-point function has 12 contractions joining the two external fields to the vertex; dividing by \(4!=24\) leaves the tadpole coefficient \(1/2\). Fourier transformation therefore gives

\[
\left.\partial_\lambda\chi_{\beta,q}(i\eta)\right|_{0^+}
=-\frac{c_\beta}{2(\eta^2+\Omega^2)^2}.
\]

For a spatial oscillator lattice the same insertion gives \(c_\beta=|\Lambda|^{-1}\sum_k\coth(\beta\Omega(k)/2)/(2\Omega(k))\). At every finite \(\beta\), this exceeds the vacuum value \(c_\infty\) termwise when the modes are massive. The independent-source anchored update instead has \(c_\infty\) in the long auxiliary-time limit because \(f=r/N\to0\). This is an exact first-order mismatch for the declared update, not a finite-coupling solver test. The finite 3D sums and oscillator basis calculations in the supplied package are floating-point diagnostics; their cutoffs are not interval-certified.

## 5. Continuum scaling: what follows and what does not

The theorem itself fixes \(\alpha>0\). For a family \(\alpha_N\), its amplitude bound only vanishes if

\[
\frac{r_NB_N}{\alpha_N\sqrt N}\longrightarrow0.
\]

So the fixed-\(\alpha\) conclusion cannot be carried over merely by letting the time step shrink. An exact finite-cycle example shows the issue. Let \(a=\beta/N\), \(K_N=am^2I+a^{-1}L_{\mathbb Z_N}\), one anchor at \(t=0\), and a stationary OU source with mean one and variance one, independent of the target noise. Its third moment is four. At zero coupling the derivative of the target mean is \(-4K_N^{-1}e_0\), so

\[
\left.\frac{d}{dg}\mathbb E F_{0,N}(0)\right|_{g=0}
=-\frac{4}{am^2\sqrt N}
=-\frac{4\sqrt N}{\beta m^2}.
\]

This Gaussian source is stationary, has finite sixth moment, and is strongly convex but asymmetric. It demonstrates that a moment-only theorem does not give a uniform continuum estimate if the quartic coefficient is held fixed while \(\alpha_N\sim a\). It is a derivative counterexample to that unqualified extension, not a counterexample to the fixed-\(\alpha\) theorem.

There is also a conditional continuum corollary for the conventional massive Euclidean discretization at fixed physical \(\beta\), fixed spatial lattice, \(a=\beta/N\), and

\[
K_N=am^2 I+a^{-1}L_{\mathbb Z_N}+aK_x,
\qquad g_N=a\lambda/6.
\]

For the temporal cycle, the diagonal Green value obeys, uniformly in \(N\),

\[
(K_N^{-1})_{ii}\leq \frac1{\beta m^2}
+2\sum_{\ell\geq1}\frac1{\beta m^2+16\ell^2/\beta}<\infty,
\]

because \(\sin(\pi\ell/N)\geq2\ell/N\) for \(\ell\leq N/2\). Nonnegative spatial Laplacian eigenvalues only improve this bound. Tilted Brascamp–Lieb then gives uniform coordinate sixth moments for centered source and reference laws with analogous positive mass. Thus \(B_N=O(a)\), \(D_N=O(N^{-1/2})\), and the raw \(\mathbb E|F|^2\) discrepancy bound is \(O(1)\). The physical discrete susceptibility uses the factor \(a\) multiplying the Fourier covariance; under that normalization the discrepancy is \(O(a)=O(N^{-1})\). This extension is proved only for the specified massive time-continuum scaling and moment assumptions. It does not cover simultaneous spatial continuum/renormalization, massless limits, different source scaling, or a response estimator with a different normalization.

The exact finite values and both scaling branches are retained in [exact_finite_audit.json](exact_finite_audit.json). This conditional refinement is a new deduction from the source theorem, not a claim in the supplied report.

## 6. Finite-volume and thermodynamic limits

At fixed \(\alpha,r,B\), the estimate is uniform in \(|\Lambda|\) and the output site. Hence any joint sequence of finite spatial volumes and temporal lengths inherits the same bound as \(N\to\infty\), provided the same \(B\) applies. If both thermodynamic observables converge, their limiting difference is bounded by the same estimate; if they do not converge, the theorem supplies no limit-existence result and does not establish that thermodynamic and long-time limits commute. Likewise, a transfer-matrix vacuum interpretation at fixed spatial volume is a separate existence fact; the comparison theorem transfers an existing reference limit to the anchored statistic.

The continuum example above changes \(\alpha\) and the normalization, so it is not covered by that fixed-parameter uniformity. A strictly positive mass and a volume-uniform source moment bound are enough for the fixed-lattice thermodynamic comparison, but massless/critical cases require new estimates.

## 7. External-source edge cases

- Temporal dependence, non-ergodicity and long memory do not by themselves violate the comparison: the proof uses stationarity and pointwise \(L^2\) forcing bounds, not mixing or independence.
- Correlation between \(Y\) and \(X^0\) is permitted in the nonperturbative theorem. It changes the value of \(B\), but not the argument.
- An asymmetric or non-centered source can create a nonzero Fourier mean. The raw-second-moment statement still holds; physical connected susceptibility requires the connected-covariance correction above.
- A source with bounded marginal sixth moments but no joint stationary adapted coupling is not enough to justify the pullback SDE proof. The existence/adaptedness assumption should be explicit for general external processes. For the ordinary finite-dimensional strongly dissipative Langevin source, a stationary coupling is plausible from contraction and a Lyapunov bound, but it should not be generalized to arbitrary non-Markov or anticipative sources without proof.
- A source Hessian bound alone does not bound its absolute moments if its mean is unconstrained; the stated theorem directly assumes the needed uniform forcing moment.

## 8. Independent checks and their limits

I copy-first inspected and replayed the supplied [checks.py](source/thermal/checks.py) into [replay](replay/). All assertions passed. The oscillator values reproduce the source table to displayed precision; the finite-matrix residual, mode identity and Green identity were at floating-point roundoff. These are producer checks reproduced in a local environment, not independent mathematical proof or interval validation.

I then implemented [exact_finite_audit.py](exact_finite_audit.py) independently with exact rational/algebraic arithmetic. For a \(4\times3\) product cycle with rational \(\alpha,\kappa_\tau,\kappa_x\), it checks all 12 fixed-slice Green sums, exact inverse positivity, the exact Lyapunov equation, and all 12 Fourier diagonal formulas. The zero-frequency linear resolvent forcing example attains the amplitude bound exactly. The scalar correlated-source derivatives and the continuum source derivatives are also exact. The continuum moment bound is analytic; its displayed finite Green values are exact rational matrix inversions. These checks support the reconstruction and the correlation/continuum qualifications; none substitutes for the proof above or validates an algorithm implementation.

## 9. Source-paper boundary

The 2018 paper's displayed prescription has a mixed noncompact-imaginary-time/imaginary-frequency representation, a separately sampled compact Euclidean field, a thermal value inserted when evaluating the local interaction drift at the selected time, and a finite-DFT artifact that the authors say vanishes as the frequency-grid length grows. That is the specific local replacement motivating this model. The paper also includes its finite discretization, noise conventions, contour argument, and spectral inversion. This audit proves an asymptotic failure statement only for the stated positive local-drift model with the hypotheses above. It does not replay the authors' code, reproduce their figures, certify their finite-\(N_\omega\) data, or rule out other contour, normalization, control-variate or correlated-source implementations.

## 10. Status

| Claim | Audit status |
|---|---|
| Cooperative-killing comparison and pullback bound | Proof closes, conditional on the stationary adapted coupling and finite moments. |
| Product-graph Green sum and spatial-volume independence | Exact under the stated Kronecker-sum kernel and full spatial anchor slices. |
| Local Fourier amplitude and raw second-moment bounds | Valid as stated; connected covariance gets the displayed extra \(D_N^2\) term if source is non-centered. |
| Source moment acquisition | Valid for centered/even uniformly convex source; Hessian lower bound alone needs a mean bound. |
| Independent-source Lyapunov derivative | Valid under zero-coupling independence; correlated-source exact cases refute any broader formula. |
| Physical oscillator and lattice first derivative | Duhamel/tadpole derivation closes; spatial sums are coefficient checks, not finite-coupling simulations. |
| Continuum conclusion | Not automatic when \(\alpha\) varies. A massive fixed-physical-\(\beta\), \(g=a\lambda/6\) corollary follows with uniform coordinate moments and the correct factor \(a\); massless/spatial renormalized cases remain open. |
| Cited paper's full method | Not audited or refuted. The proven scope is the declared finite-anchor local drift. |
| Novelty, speedup, device impact, external validation | UNKNOWN / not established. |
