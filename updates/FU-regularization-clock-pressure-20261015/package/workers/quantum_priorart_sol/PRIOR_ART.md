# Targeted quantum prior-art audit

Audit date: 2026-10-15. Scope: the exact state-independent scalar-convolution contract
\[
\widehat M(t)=\widehat\nu(t)\exp(i\,t\cdot\sigma),\quad t\in\mathbb R^3,
\]
with \(M\) a normalized qubit POVM and \(\nu\) one classical probability law. The same law supplies the projected additive noise in every direction. Coordinate compatibility, arbitrary classical postprocessing, spherical convolution, and state-specific positive representations are different contracts.

**Finding:** no inspected primary result supplies a stronger variance lower bound for this exact class, or the explicit Dickman scalar regularizer. This is a bounded search finding, not historical priority clearance. The vector-output/all-direction measurement problem, covariant POVM architecture, Weyl characteristic function, and ordinary added-noise lower bound already have substantial primary antecedents. In particular, the all-direction requirement itself should not be described as absent from earlier joint-measurement work.

Ordinary Husimi smoothing is already an exact positive scalar convolution for the special canonical position/momentum pair, and therefore for its quadrature marginals. The bounded-tuple universality and specified tail/moment guarantees are the remaining distinguishing requirements; the scalar-convolution idea itself is not new.

The root-supplied candidate \(\operatorname{tr}\Sigma\ge 6+16/\pi^3\) is not independently certified in this literature audit. Its proof and sharpness need their own audit. This worker found no exact prior statement containing that constant or a stronger bound under the same scalar contract.

## Closest primary results, with proof locations

| Source | Original proof inspected | Exact overlap and boundary |
|---|---|---|
| [Husimi, 1940](https://www.jstage.jst.go.jp/article/ppmsj1919/22/4/22_4_264/_article), *Some Formal Properties of the Density Matrix*, [DOI](https://doi.org/10.11429/ppmsj1919.22.4_264) | Original PDF printed pp.277–279 (PDF pp.14–16), Sec.5, Eqs.(5.1),(5.5),(5.6), visually inspected | Positive wave-packet expectations and the Gaussian/Fourier smoothing relation are explicit. In modern Fourier form this is state-independent scalar Gaussian convolution for canonical position and momentum, already yielding noisy quadrature marginals. It is a special unbounded canonical pair, and does not establish arbitrary bounded-tuple universality. The modern exact Gaussian identity is also derived in the 2025 primary preprint, Eqs.(1a)–(1b). |
| [Dammeier, Schwonnek, Werner, 2015](https://arxiv.org/abs/1505.00049), *Uncertainty relations for angular momentum*, NJP 17, 093046, [DOI](https://doi.org/10.1088/1367-2630/17/9/093046) | PDF pp.20–24: all projected directions, calibration/Wasserstein errors, Lemma 9, covariance averaging in Lemma 10; pp.24–27: Eqs.(109)–(118), Theorem 12 | This is the closest measurement-theoretic antecedent. A single \(\mathbb R^3\)-valued output is projected in every direction. Its covariant classification allows arbitrary radius and spin seed. The marginal kernel \(P(m,dx)\) in Eq.(111) depends on the ideal eigenvalue \(m\); a common translated scalar kernel is not imposed. Consequently its sharp error theorem optimizes a larger class, and does not establish the exact-convolution variance optimum. |
| [Schwonnek, Werner, 2018/2020](https://arxiv.org/abs/1802.08342), *The Wigner distribution of n arbitrary observables*, JMP 61, 082103, [DOI](https://doi.org/10.1063/1.5140632) | PDF pp.2–5: definition, moment and support arguments, positivity result; p.14, Eqs.(51)–(55), Pauli triple | The all-linear-marginal distribution and its Fourier transform are established prior mathematics. Their Pauli calculation gives \(\widehat W_I(t)=2\cos|t|\) and the shell-derivative distribution. Gaussian smoothing is used to define/visualize distributions; it is not a theorem of positive scalar smoothing for every state. The paper does not give the Dickman law or an exact-class variance lower bound. |
| [Barchielli, Gregoratti, 2019/2020](https://arxiv.org/abs/1912.09758), *Entropic measurement uncertainty relations for all the infinite components of a spin vector* | PDF pp.3–8: sphere POVMs, Eqs.(10)–(26), Theorem 1; pp.9–10: noise distinctions; pp.15–17: spin-half optimum | Explicitly distinguishes all directions from two/three coordinates. It obtains compatible discrete spin reports by directional projection and discretization of a sphere outcome, with classical transition probabilities. The optimized loss is relative entropy, and noise includes outcome mixing. This does not impose additive convolution of one \(\mathbb R^3\) scalar law. |
| [Appleby, 1999/2000](https://arxiv.org/abs/quant-ph/9911021), *Optimal Measurements of Spin Direction* | PDF pp.8–11, especially Sec.5 and Eq.(36) | Characterizes optimal spin-direction measurements under its retrodictive/predictive fidelity criteria. The isotropic retrodictively optimal POVM is the spin-coherent one, and its first moment supplies the familiar rescaling by \(s+1\). This is an antecedent of the direction measurement in the pasted construction, not of the exact radial scalar factor. |
| [D'Ariano, Macchiavello, Sacchi, 2000/2001](https://arxiv.org/abs/quant-ph/0007062), *Joint measurements via quantum cloning* | PDF p.3, Eqs.(13)–(17), coherent POVM comparison | Computes unbiased reports from a spin-coherent POVM and their second moments, and contrasts them with cloned-coordinate measurements. For \(j=1/2\), rescaling to Pauli units gives the familiar report \(3n\) and per-coordinate second moment 3. This confirms that the pasted construction's comparison baseline is established. That baseline does not satisfy the exact all-linear scalar contract; see the direct calculation below. |
| [Sabbagh, Movilla Miangolarra, Georgiou, 2025](https://arxiv.org/abs/2505.00245), *On a time-resolved interpretation of the Husimi function* | All 4 PDF pages; general Eqs.(2a),(2b), Pauli Eqs.(5),(6) and p.3 kernel | Gives positive representations for arbitrary tuples through a Gaussian-semigroup kernel. General normalization is state-dependent. Crucially, the Pauli-triple normalization is state-independent, so normalization alone does not distinguish that case. The Pauli kernel is not translation convolution; the independent first-moment calculation below excludes its raw finite-time output from the requested class. |
| [Sabbagh et al., 2024/2025](https://arxiv.org/abs/2409.19206), *Particle approximations of Wigner distributions for n arbitrary observables*, [published DOI](https://doi.org/10.1103/PhysRevResearch.7.013102) | Definitions, signed-measure approximation propositions, and Pauli examples in downloaded 19-page preprint | Constructs signed discrete approximations with exact principal-axis marginals, converging to the all-linear Wigner distribution. Schwartz smoothing with compactly supported smooth Fourier transform improves convergence. Neither the approximants nor smoothing are proved positive scalar regularizers of the exact class. |
| [Massar, 2007](https://arxiv.org/abs/quant-ph/0703036), *Uncertainty Relations for Positive Operator Valued Measures* | PDF pp.2–4, uncertainty operator and Eqs.(9)–(12) | Useful for avoiding a false variance comparison. Its qubit example calls a four-outcome POVM “unbiased” in the weak maximally-mixed-state sense; its first moments are contracted Pauli operators. The numerical lower bound 1 in that paper is not the added-noise covariance bound for reports with first moments exactly \(\sigma_j\). |
| [Ghai, Sharma, Ghosh, 2023](https://arxiv.org/abs/2306.07917), *Negativity of Wigner distribution function as a measure of incompatibility* | PDF pp.1–3: definitions and noise setup, Gaussian visualization regularization | Adds identity noise to the operators/eigenprojectors themselves and studies negativity of their resulting Wigner distributions. This changes the operator tuple; it does not establish positive convolution of the fixed sharp tuple by one state-independent scalar law. |

The downloaded PDFs, extraction hashes, and inspected pages are recorded in SOURCE_RECEIPTS.json. Primary full-text proofs, rather than review claims, support the principal scope distinctions above. Mathematical formulas below are independent calculations from the stated models, not claims quoted from those papers.

## Direct distinctions

**1. General covariance is substantially weaker than the exact scalar multiplier.**

After centering the noise and Haar averaging an admissible exact measurement over rotations, the covariance trace is unchanged and its noise is radial. The usual covariant qubit form is
\[
M(dr,dn)=\frac{I+a(r)n\cdot\sigma}{4\pi}\,d\Omega(n)\,P(dr),
\qquad |a(r)|\le1.
\]
Its Fourier transform has two radial coefficients:
\[
\widehat M(ku)=A(k)I+iB(k)u\cdot\sigma,
\]
\[
A(k)=\mathbb E\,\mathrm{sinc}(kR),\qquad
B(k)=\mathbb E\,a(R)\frac{\sin(kR)-kR\cos(kR)}{(kR)^2}.
\]
The exact contract requires a single classical characteristic function \(\phi\) such that
\[
A(k)=\phi(k)\cos k,\qquad B(k)=\phi(k)\sin k.
\]
Neither rotational covariance nor a general noise kernel \(P(m,dx)\) forces this relation. Even imposing it algebraically would still require \(\phi\) to be a classical characteristic function on \(\mathbb R^3\).

DSW's Eq.(110) covers this general radius/seed architecture. The Dickman construction uses the extremal seed \(a(r)=1\) and a special independent radius. The architecture and quantum information channel are therefore established; the exact choice of radius/noise factor is the potential new ingredient.

**2. The familiar report \(3n\) fails the exact contract.**

For the ordinary covariant qubit measurement \(N(dn)=(I+n\cdot\sigma)d\Omega/(4\pi)\), reporting \(X=3n\) has first moments \(\sigma_j\) and second moments \(3I\). However
\[
\frac12\operatorname{tr}\widehat M(ku)=\mathrm{sinc}(3k).
\]
An exact scalar convolution requires this scalar part to vanish at \(k=\pi/2\), since \(\cos(\pi/2)=0\). In fact
\[
\mathrm{sinc}(3\pi/2)=-\frac{2}{3\pi}\ne0.
\]
Thus optimality of this usual unbiased report in a weaker measurement problem does not settle the exact-convolution problem.

**3. The newer Pauli Husimi representation is excluded directly, despite scalar normalization.**

The 2025 preprint's Pauli model is
\[
M_\tau(x)=Z_\tau^{-1}e^{-\tau|x|^2}
  \exp(2\tau x\cdot\sigma),
\qquad
Z_\tau=(\pi/\tau)^{3/2}(1+2\tau)e^\tau.
\]
The omitted common scalar \(e^{-3\tau}\) cancels between numerator and denominator. Put
\[
Z(\tau,c)=\int_{\mathbb R^3}e^{-\tau|x|^2}\cosh(c|x|)\,dx
=(\pi/\tau)^{3/2}e^{c^2/(4\tau)}
 \left(1+\frac{c^2}{2\tau}\right).
\]
Rotation invariance and differentiation in \(c\) give
\[
\int x_jM_\tau(x)\,dx
=\frac{\partial_c Z(\tau,c)}{3Z(\tau,c)}\bigg|_{c=2\tau}\sigma_j
=\frac{3+2\tau}{3(1+2\tau)}\sigma_j.
\]
For every \(\tau>0\), this coefficient is strictly below 1. Any scalar convolution with finite first moment instead gives \(\sigma_j+\mu_jI\). The two cannot agree for any scalar noise mean. The limit is the unit-sphere direction measurement, with first moment \(\sigma_j/3\).

This excludes the model as published. Rescaling a report to repair its first moment is insufficient to establish the full Fourier contract.

**4. Ordinary second moments give the established bound 6, and equality cannot satisfy the exact contract.**

For a centered qubit POVM, write
\[
M(dx)=(I+b(x)\cdot\sigma)\lambda(dx),
\quad |b(x)|\le1,\quad \lambda(\mathbb R^3)=1.
\]
The exact first moments imply \(\int x_jb_k\,d\lambda=\delta_{jk}\), hence \(\int x\cdot b\,d\lambda=3\). Cauchy–Schwarz yields \(\int|x|^2d\lambda\ge9\). The exact second moments give
\[
\int|x|^2d\lambda=3+\operatorname{tr}\Sigma,
\]
so \(\operatorname{tr}\Sigma\ge6\). Equality forces \(|b|=1\) and \(x=3b\) almost surely. Haar averaging then gives the radius-3 coherent measurement of item 2, which violates the scalar zero. This shows nonattainment of 6 in the exact class; it does not alone produce a uniform numerical gap above 6.

The root's proposed gap must therefore be assessed as an additional restriction beyond these old first/second-moment methods, not as a new general joint-measurement uncertainty principle.

## Unresolved historical gates

- Anderson, *The Weyl functional calculus* (1969), [DOI](https://doi.org/10.1016/0022-1236(69)90013-5), and *On the Weyl functional calculus* (1970), [DOI](https://doi.org/10.1016/0022-1236(70)90050-9): primary publisher metadata obtained; full PDFs returned 403. The latter abstract concerns connected support and impossibility of an unsmoothed measure in finite dimension. Its full contents were not cleared.
- Cohen and Scully, *Joint Wigner distribution for spin-1/2 particles* (1986), [DOI](https://doi.org/10.1007/BF01882690): publisher abstract and bibliographic details obtained, full text subscription-only in this run.
- Chandler et al., *Quasi-probability distribution for spin-1/2 particles* (1992), [DOI](https://doi.org/10.1007/BF01889685): publisher abstract and references obtained; full text subscription-only. Operator-ordering variants cannot be excluded from full-text priority by the abstract alone.
- Martens and de Muynck, *Towards a new uncertainty principle: quantum measurement noise* (1991), [DOI](https://doi.org/10.1016/0375-9601(91)91015-6): primary abstract contrasts additive object-dependent and object-independent nonadditive noise. A located full-PDF index link failed (404 by curl, 403 through web). It is a relevant unresolved historical lead, not a theorem applied here.
- Busch, *Unsharp reality and joint measurements for spin observables* (1986), [DOI](https://doi.org/10.1103/PhysRevD.33.2253): primary abstract obtained, PDF access unavailable. Modern full proofs above establish the relevant covariant/coordinate distinctions without relying on an unread old proof.

No result from the failed full-text gates is represented as fully inspected. No journal or author was contacted. No Git/GitHub actions, other-worker inspection, or delegation were performed.
