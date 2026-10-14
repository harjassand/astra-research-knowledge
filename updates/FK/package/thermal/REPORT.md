# Finite thermal anchors do not preserve bulk quantum response

**Astra Scientific Capability Genesis — research record, 14 October 2026**

**Disposition: rejected computational mechanism; scoped mathematical obstruction and reproducible diagnostics.** No new efficient many-body response algorithm, scientific-computation speedup, independent proof validation, or historical priority has been established.

## 1. Scientific selection and novelty screen

The initial scientific objective was an enabling computation for consequential technology, not a predetermined equation. Four tasks were compared:

| Task | Strong existing operation examined | Selection decision |
|---|---|---|
| Chemical reaction/redox energy differences | Correlated-sampling auxiliary-field quantum Monte Carlo directly exploits cancellation in differences, rather than computing unrelated total energies [P1]. | A difference-only proposal is not new. No justified improvement over its acquisition and bias costs was identified here. |
| Turbulent heat loss in stellarator design | A 2026 study uses surrogates trained on over 200,000 nonlinear adiabatic-electron gyrokinetic simulations [P2]. | Fast evaluation is already possible within that learned domain; free training data or guaranteed extrapolation cannot be assumed. |
| Combinatorial genetic intervention effects | Compressed Perturb-seq pools interventions/readouts and recovers effects using sparse regulatory structure [P3]. | Compression alone is not new; this investigation did not establish sparsity-independent leverage. |
| Low-frequency thermal quantum response | Spectral-functional certificates [P4], direct-frequency diagrammatics [P5], correction-vector methods [P6], and a direct imaginary-frequency stochastic prescription [P7,P8]. | Investigate whether a genuinely temperature-correct information-acquisition operation can bypass noisy analytic continuation. |

These are targeted competitors, not an exhaustive ranking across all problem regimes. The selected task concerns response functions relevant to interacting materials; the tests below do not solve conductivity in a realistic material.

The closest direct-sampling predecessor is Pawlowski and Rothkopf [P7,P8]. It introduces an extended imaginary-time/frequency field and a separate compact thermal field, with the latter inserted at one site during evaluation of the interaction drift. The paper explicitly records a puzzling zero-frequency discrepancy. Its published equations motivated the precisely defined sampler below. This record does **not** replay the authors' code or establish the status of every conceivable implementation of their contour prescription.

The proposed extension considered here is sparse thermal anchoring: retain a small collection of thermal source slices while enlarging the auxiliary domain. The result is that, under the conditions proved below, this cannot retain an order-one thermal correction in the normalized local response.

## 2. Input/output and cost contract

Input: an explicit local quantum Hamiltonian H; inverse temperature beta; an observable A; an imaginary frequency eta > 0; target absolute error epsilon and failure probability delta. No exact eigensystem, analytic continuation oracle, known spectral density, or pretrained predictor is input.

Output: an estimate or certified interval for the regular thermal susceptibility chi_beta,A(i eta), with all model, discretization, sampling, and inference errors accounted for.

For a finite-dimensional system, order the energies E_n and put p_n=exp(-beta E_n)/Z. For a Hermitian A, define the positive transition measure

\[
 d\mu_{\beta,A}(\Delta)=\sum_{E_m>E_n}(p_n-p_m)|A_{nm}|^2
      \delta_{E_m-E_n}(d\Delta).
\]

Then

\[
 \chi_{\beta,A}(i\eta)=\int_0^\infty
       \frac{2\Delta}{\Delta^2+\eta^2}\,d\mu_{\beta,A}(\Delta).
\]

The same formula applies to the oscillator when the trace and sums converge. This is an observable-specific answer, not the full spectral function. It is not automatically a DC conductivity: conserved, diamagnetic, elastic, and order-of-limits issues must be treated separately. In the even oscillator with A=q, parity removes diagonal matrix elements, so the zero-frequency Euclidean integral equals the regular susceptibility used in the checks.

A legitimate algorithm must charge Hamiltonian acquisition when it is not supplied, equilibrium preparation, all auxiliary variables, training/preprocessing, mixing, precision, verification, and the dependence on eta. In the theorem the Hamiltonian is explicit. Supplying it is not the same as supplying its response measure.

## 3. Nonperturbative finite-anchor theorem

### 3.1 Model and assumptions

Let the lattice be a product of a temporal cycle with N sites and a finite periodic spatial lattice Lambda. Its spatial size is unrestricted. Work at fixed discretization, and let

\[
 K=\alpha I+\kappa_\tau L_\tau+\kappa_x L_x,\qquad
 \alpha>0,\quad\kappa_\tau,\kappa_x\geq0,
\]

where the L are nonnegative graph Laplacians. Thus K is symmetric, K 1=alpha 1, and its off-diagonal entries are nonpositive. In physical path-integral units alpha includes the temporal lattice spacing; it is not silently held fixed in a continuum limit.

Choose r fixed temporal slices, each containing all spatial sites, and let P be their diagonal indicator. Put g=lambda/6 >= 0. All vector powers below are componentwise.

The reference, unanchored Langevin process is

\[
 dX^0_s=-[KX^0_s+g(X^0_s)^3]ds+\sqrt2\,dW_s.
\]

Its stationary density is

\[
 \pi_N^0(dx)\propto
 \exp\{-\tfrac12x^TKx-\tfrac g4\sum_i x_i^4\}\,dx.
\]

The finite-anchor process is

\[
 dX_s=-[KX_s+g(I-P)X_s^3+gP Y_s^3]ds+\sqrt2\,dW_s.
\]

Y is a stationary external thermal source at the anchor sites. Assume its coordinate sixth moments are uniformly bounded. Use a stationary coupling with X^0 driven by the same W. Define

\[
 B=\sup_{j\in\operatorname{supp}P}
       \|g(Y_j^3-(X_j^0)^3)\|_{L^2}<\infty.
\]

B is assumed uniform in N and spatial volume. It need not be assumed by fiat for the concrete compact, strongly convex quartic thermal source: Section 3.4 supplies a dimension-independent bound. Source and target need not be independent for this theorem. A stationary joint construction exists for the usual stationary compact Langevin source by the dissipativity and contraction of the driven target. The statement does not include moving/random anchors, critical alpha -> 0, nonconvex interactions, or arbitrary Fourier-space preconditioners.

For a fixed spatial site x and any real omega, define

\[
 F_{x,N}(\omega)=N^{-1/2}\sum_{t=0}^{N-1}e^{-i\omega t}X_{t,x},
 \qquad F^0_{x,N}(\omega)=N^{-1/2}\sum_t e^{-i\omega t}X^0_{t,x}.
\]

### 3.2 Statement

For every g >= 0,

\[
 \|F_{x,N}-F^0_{x,N}\|_2\leq
 D_N:=\frac{rB}{\alpha\sqrt N},
\]

and

\[
 \left|\mathbb E|F_{x,N}|^2-\mathbb E|F^0_{x,N}|^2\right|
 \leq\frac{2D_N}{\sqrt\alpha}+D_N^2.
\]

The constants are independent of the spatial volume, the chosen x, and omega. This is a local-in-space temporal-response theorem, not a volume-uniform assertion for every spatially coherent extensive observable.

Consequently, at fixed alpha, r, and B, the anchor-induced correction vanishes as N increases. If the unanchored long-time path integral has a zero-temperature limit, the finite-anchor output has that same limit rather than an independently prescribed finite temperature. For fixed finite spatial volume, the transfer-matrix interpretation gives this vacuum limit. The theorem itself is a comparison of the two samplers and does not assume existence of every joint thermodynamic/continuum limit.

### 3.3 Proof

Let Z=X-X^0. At a nonanchor coordinate,

\[
 X_i^3-(X_i^0)^3=
 [X_i^2+X_iX_i^0+(X_i^0)^2]Z_i.
\]

The coefficient is nonnegative. Hence

\[
 dZ_s=-(K+D_s)Z_s\,ds+f_s\,ds,
\]

where D_s is a nonnegative diagonal matrix supported off the anchors and

\[
 f_s=-gP(Y_s^3-(X_s^0)^3).
\]

Because -K has nonnegative off-diagonal entries, its heat semigroup is entrywise nonnegative. Adding the nonnegative killing D_s gives an evolution kernel U(s,u) satisfying the componentwise comparison

\[
 0\leq U(s,u)\leq e^{-K(s-u)},\quad s\geq u.
\]

This follows from the comparison principle for cooperative linear systems, or equivalently by a product approximation using positive semigroups and diagonal contractions. Variation of constants in the stationary pullback construction therefore gives

\[
 |Z_i(s)|\leq\sum_j\int_0^\infty(e^{-Kv})_{ij}|f_j(s-v)|\,dv.
\]

Minkowski's integral inequality and stationarity imply

\[
 \|Z_i\|_2\leq B\sum_{j\in\operatorname{supp}P}(K^{-1})_{ij}.
\]

Now fix one anchor time s and the target spatial site x. For the product periodic Laplacian,

\[
 \sum_{t\in\mathbb Z_N}\sum_{y\in\Lambda}
 (K^{-1})_{(t,x),(s,y)}=1/\alpha.
\]

To verify it directly, factor e^{-Ku}=e^{-alpha u}e^{-kappa_tau L_tau u}e^{-kappa_x L_x u}. The temporal column sum and spatial row sum of the respective heat kernels are each one. Integrate e^{-alpha u} over u >= 0. This derivation does not assume statistical independence among spatial sites.

Taking the temporal Fourier sum and using the triangle inequality yields

\[
 \|F-F^0\|_2\leq N^{-1/2}\sum_t\|Z_{t,x}\|_2
 \leq rB/(\alpha\sqrt N).
\]

Finally the reference potential has Hessian K+3g diag(x_i^2) >= K. The Brascamp-Lieb covariance inequality [P9] gives Var(v^T X^0) <= v^T K^{-1}v for real v. Apply it separately to real and imaginary parts of the Fourier vector; their squared norms sum to one. The even reference density has mean zero, so

\[
 \mathbb E|F^0|^2\leq1/\alpha.
\]

Expanding |F^0+(F-F^0)|^2 and applying Cauchy-Schwarz proves the second bound. No weak-coupling approximation was used.

### 3.4 Moment acquisition is not a hidden oracle

For the reference strongly convex density, and for a compact thermal source with quadratic Hessian at least alpha_Y I, apply Brascamp-Lieb also after tilting one coordinate by exp(t x_i). The second derivative of the coordinate log moment generating function is at most 1/alpha, or 1/alpha_Y. Symmetry supplies zero first derivative at zero. Thus each coordinate is sub-Gaussian, with

\[
 \Pr(|X_i^0|>u)\leq2e^{-\alpha u^2/2},\qquad
 \mathbb E|X_i^0|^6\leq96\alpha^{-3}.
\]

The corresponding source bound uses alpha_Y. Therefore

\[
 B\leq g\sqrt{96}\,(\alpha_Y^{-3/2}+\alpha^{-3/2}),
\]

uniformly in both lattice sizes. These conservative constants are not claims of sharpness. A source without this convexity or a moment bound requires separate analysis.

### 3.5 Necessary scaling, not a sufficient repair

For an order-one thermal correction to survive within this class at fixed alpha, rB cannot be o(sqrt(N)). This is only a necessary condition. It does not prove that r proportional to sqrt(N) works; it does not require a positive density of anchors; and increasing their strength or number does not establish correct thermal dynamics. Dense anchoring, nonlocal drift changes, or other mechanisms must be checked afresh.

## 4. Exact first-order failure

### 4.1 The finite-dimensional anchored update

For this calculation take the thermal source noise independent of W. At lambda=0, X and Y are independent centered Gaussians. Let C=K^{-1}, c=C_ii, and Q=I-P. Differentiating the stationary covariance identity from the right at lambda=0 gives

\[
 KC_1+C_1K=-\frac c2(QC+CQ).
\]

Wick's identity E[X_i^3 X_j]=3c C_ij gives the right side; the source term E[Y_i^3 X_j] vanishes by independence and centering. A lambda-dependent source distribution has no first-order effect through an already lambda-multiplied independent forcing term.

For a normalized plane wave with K-eigenvalue kappa_q and anchor fraction f=r/N,

\[
 (C_1)_{qq}=-\frac{(1-f)c}{2\kappa_q^2}.
\]

In particular the intended thermal beta does not occur in this derivative. The finite-matrix test independently solves the Lyapunov equation and compares every Fourier diagonal and the Green-function sum identity.

### 4.2 Coupled quantum oscillator lattice

Consider

\[
 H=\frac12\sum_x p_x^2+\frac{m^2}2\sum_x q_x^2
 +\frac\kappa2\sum_{\langle x,y\rangle}(q_x-q_y)^2
 +\frac\lambda{24}\sum_x q_x^4.
\]

On a periodic d-dimensional lattice, write

\[
 \Omega(k)^2=m^2+4\kappa\sum_{j=1}^d\sin^2(k_j/2),
\]

\[
 c_\beta=\frac1{|\Lambda|}\sum_k\frac{\coth(\beta\Omega(k)/2)}{2\Omega(k)},
 \qquad
 c_\infty=\frac1{|\Lambda|}\sum_k\frac1{2\Omega(k)}.
\]

The exact first right derivative of the physical susceptibility is

\[
 \left.\partial_\lambda\chi_\beta(i\eta,k)\right|_{0^+}
 =-\frac{c_\beta}{2[\eta^2+\Omega(k)^2]^2}.
\]

One derivation uses the single quartic insertion in the connected two-point function. Selecting the two external contractions has 12 choices; division by 24 gives the factor 1/2. The remaining equal-site contraction is c_beta. Fourier transforming the two external propagators gives the squared denominator. This is the exact derivative, not an assertion that a truncated perturbation series solves the strongly interacting system. The finite-temperature factor can alternatively be checked by differentiating oscillator spectral sums, as done in the executable diagnostics.

In the long auxiliary-time limit, the fixed-anchor update instead has c_infinity. The discrepancy c_beta-c_infinity is strictly positive at finite beta and does not vanish by increasing spatial volume. At d=3, m=kappa=1, beta=0.5, the 64^3 lattice gives

- c_beta = 0.38155297425909;
- c_infinity = 0.20086316591098;
- 47.3564145841% of the physical first-order coefficient is missing.

The script checks sizes 8^3, 16^3, 32^3, and 64^3 at three temperatures. This is a spatially coupled, many-coordinate failure test, not an interacting finite-lambda simulation with 262,144 solved quantum degrees of freedom.

## 5. Nonperturbative oscillator witness and independent discretization

For H=p^2/2+q^2/2+q^4, A=q, the numerical continuum-basis results are:

| beta | Thermal chi(0) | Vacuum chi(0) | Relative vacuum bias |
|---:|---:|---:|---:|
| 1 | 0.238307681303 | 0.265526770038 | 11.421826% |
| 0.5 | 0.195522099539 | 0.265526770038 | 35.803968% |
| 0.25 | 0.149606974797 | 0.265526770038 | 77.482882% |

The mismatch also occurs inside the targeted sub-Matsubara interval, not only at the already accessible zero-frequency endpoint. At beta=1 and eta=0.5 (below 2*pi/beta), the thermal value is 0.224368377213 and the vacuum value is 0.248901387900, a relative difference of 10.934255%.

These are **our deterministic spectral calculations**, not measured output from a finite-anchor stochastic simulation. The theorem explains which reference limit the specified anchored process approaches. The small system is a counterexample to correctness, not evidence of a high-dimensional speedup.

The harmonic-basis calculation uses dimensions 64, 96, 144, and 192. Before forming q^4, q is padded by four levels so that the retained matrix is the proper Galerkin block, not the fourth power of a truncated q. All four beta cases at dimensions 144 and 192 agree numerically well below 10^-9. The f-sum 2 sum_(n<m) (p_n-p_m)(E_m-E_n)|q_nm|^2 is checked against 1.

An independent coordinate-grid transfer-matrix calculation uses

\[
 T_a(x,y)=\frac1{\sqrt{2\pi a}}
 \exp\{-\frac{(x-y)^2}{2a}-\frac a2[V(x)+V(y)]\}.
\]

After Nyström quadrature, its eigenvalues and q matrix elements give the exact spectral expression for the chosen discrete-time transfer matrix. At zero Matsubara frequency the pair kernel is a coth(a Delta/2), not the continuum kernel 2/Delta. This distinction is retained. With a=1/16 the values are approximately

- thermal beta=1: 0.238644147276;
- vacuum: 0.265953477483.

The grid is refined from 401 to 801 points on [-6,6], and a is separately reduced through 1/128 to approach the continuum-basis value. Cutoffs, endpoint truncation, high-level truncation, and floating-point arithmetic are **not interval-certified**. These checks provide independent numerical consistency, not a proof of rigorous error bars.

At the parameters shared with [P7], the direction and rough size of the vacuum/thermal separation are consistent with the reported zero-frequency discrepancy. That is an inference, not a reproduction of their code, raw data, Fourier normalization, or every discretization detail. In particular a correctly located lowest spectral pole would not by itself certify the finite-temperature weights: the Hamiltonian's transition energies are fixed while their thermal weights vary.

## 6. Failed repairs and the genuinely missing information

### 6.1 Independent additive noise is insufficient

A process X=X_vac+Y with independent stationary real Y has covariance C_X=C_vac+C_Y. Its spectral measure can only add a nonnegative contribution. But the exact weak-quartic derivative above makes chi_beta(i eta)-chi_infinity(i eta) negative at sufficiently small positive lambda and finite beta. Therefore this additive-independent repair cannot reproduce the response family. Correlated fields or changes to the drift are not excluded.

There is a separate elementary thermal-field obstruction, included in the code but not to be confused with response covariance. On its physical Euclidean strip, the free oscillator satisfies

\[
 C_\beta(t)-C_\infty(t)=\frac{n_B(\Omega)}\Omega\cosh(\Omega|t|),
 \quad 0\leq |t|\leq\beta.
\]

The 2x2 covariance-difference matrix for 0 and t>0 has negative eigenvalue n_B/Omega [1-cosh(Omega t)]. It cannot be the covariance of an independent stationary positive thermal correction. The free oscillator's **response** is temperature-independent; this second calculation concerns thermal Euclidean state correlations, not that response.

### 6.2 The required object is a response measure, not a state marginal

The desired susceptibility already has a positive spectral representation. There is no claim here that a positive representation cannot exist. The difficulty is acquiring it from H and beta without solving the original response problem.

For example, whenever the sum rule is finite,

\[
 M_1=\langle[A,[H,A]]\rangle_\beta=2\int\Delta\,d\mu_{\beta,A}(\Delta).
\]

For M_1>0 define the probability measure

\[
 d\nu_{\beta,A}(\Delta)=\frac{2\Delta}{M_1}d\mu_{\beta,A}(\Delta).
\]

Then exactly

\[
 \chi_{\beta,A}(i\eta)=M_1\mathbb E_\nu\left[(\Delta^2+\eta^2)^{-1}\right].
\]

This identity does not require the complete spectrum as an output. But presenting nu as an available sampler would simply hide the dominant task. A new useful operation must produce temperature-correct transition information, or an equivalent bounded response estimator, with its state-preparation, resolution, normalization and mixing costs paid.

If exact iid nu samples and M_1 were supplied, Hoeffding's inequality would estimate R_eta=eta^2 chi/M_1 in [0,1] to additive error epsilon_R using O(epsilon_R^-2 log(1/delta)) samples. For absolute susceptibility error epsilon_chi this becomes O(M_1^2 eta^-4 epsilon_chi^-2 log(1/delta)); this is a simple conditional upper bound, not an optimal lower bound or an achieved algorithm. Energy-gap inaccuracies must also be charged. No such efficient sampler is constructed here.

A direct physical response intervention could in principle measure the relevant Laplace transform, but controlled thermal preparation and real-time duration would then be the resource. Rephrasing standard linear response as a new oracle would not establish novelty. Direct diagrammatic response [P5] already provides an alternative within regimes where its convergence and cancellation costs are controlled.

## 7. Cost and competitor verdict

A local explicit-discretization update on N auxiliary time slices and M spatial sites costs O(NM) arithmetic per sweep; a time-Fourier implementation additionally uses transforms, normally O(MN log N) for the temporal transforms. These are per-step operation counts, not end-to-end complexity bounds. Thermal-source updates, stability restrictions, equilibration, effective sample count, precision, and verification remain additional costs.

Even granting exact equilibrium samples for the thermal source, the finite-anchor limit retains the wrong response. Thus eliminating statistical error cannot meet an accuracy requirement smaller than the nonzero limiting bias. This rejects an asymptotically consistent algorithm in this class; it does not forbid accidentally accurate finite-N outputs for a particular temperature or observable.

A scalar-only formulation is not itself an advance over [P4], which already bounds spectral functionals from the same Euclidean information. Direct-frequency computation is not itself an advance over [P5] or [P6]. No equal-input/equal-accuracy wall-clock superiority comparison was performed, because the selected mechanism fails its correctness gate. The subsecond deterministic diagnostic runtime recorded in this environment is not a scientific-computation speedup benchmark.

## 8. Status ledger and boundaries

| Item | Status |
|---|---|
| Finite-anchor bound | Complete analytic argument above, using established covariance and comparison inequalities; no independent referee/formal proof review |
| Finite-N Lyapunov and Green-function identities | Derived exactly; finite floating-point matrix checks passed |
| Physical first quartic derivative | Derived; independently checked numerically for the oscillator |
| 3D many-site coefficient mismatch | Deterministic evaluation of the exact derivative coefficient; not a full nonlinear quantum simulation |
| Strongly anharmonic oscillator values | Two numerical representations and refinement checks; not interval-certified |
| Diagnosis of the cited paper's discrepancy | Mathematically motivated inference for its stated local replacement mechanism; authors' implementation and raw data not replayed |
| Efficient thermal transition sampler | Not constructed |
| Historical novelty | Unresolved; the broad principle that massive positive bulk fields lose finite boundary influence is established mathematical territory |
| New scientific computational power | Not established; do not archive this as a positive invention |

This run's usable contribution is the explicit failure mechanism, a spatial-volume-uniform nonlinear bound for the specified update, and an executable falsification suite. It is a negative result about an acquisition architecture, not a universal impossibility theorem for thermal response or a claim that the research task is unattainable.

Astra research capital was consulted only for orientation and a targeted term search at Git revision ace0cfc4437fe91c20ccd24d69e0ee4bb335e871. No repository theorem is a premise of the argument. The repository has not been modified.

## Primary-source ledger

[P1] J. Shee et al. Chemical Transformations Approaching Chemical Accuracy via Correlated Sampling in Auxiliary-Field Quantum Monte Carlo. arXiv:1703.01545v2.

[P2] R. Michael Churchill et al. AI-Accelerated Gyrokinetic Predictions of Turbulent Transport for Stellarator Design Optimization and Experimental Planning. arXiv:2609.28730v1, 2026. Preprint claims, not independently benchmarked here.

[P3] D. Yao et al. Scalable genetic screening for regulatory circuits using compressed Perturb-seq. Nature Biotechnology 42, 1282–1295 (2024); online 2023. DOI:10.1038/s41587-023-01964-9.

[P4] S. Mutzel and A. Tilloy. Certified spectral functions from lattice Monte Carlo data. arXiv:2606.09791v1, 2026. Preprint read for the output-specific certified comparator; its implementation was not run here.

[P5] I. S. Tupitsyn, A. M. Tsvelik, R. M. Konik, N. V. Prokof'ev. Real-frequency response functions at finite temperature. arXiv:2102.11418v2, 2021.

[P6] E. Jeckelmann. Dynamical density-matrix renormalization-group method. Physical Review B 66, 045114 (2002); arXiv:cond-mat/0203500.

[P7] J. M. Pawlowski and A. Rothkopf. Thermal dynamics on the lattice with exponentially improved accuracy. Physics Letters B 778, 221–226 (2018). DOI:10.1016/j.physletb.2018.01.037. Final published PDF, including displayed equations and figures, inspected.

[P8] J. M. Pawlowski and A. Rothkopf. Improved real-time dynamics from imaginary frequency lattice simulations. arXiv:1710.02672v1, 2017. Supplementary explanation of the local interaction-drift replacement inspected.

[P9] H. J. Brascamp and E. H. Lieb. On extensions of the Brunn-Minkowski and Prékopa-Leindler theorems, including inequalities for log concave functions, and with an application to the diffusion equation. Journal of Functional Analysis 22(4), 366–389 (1976). DOI:10.1016/0022-1236(76)90004-5. Covariance inequality is imported, not newly proved here.
