# Conditional thermality tests for anomalous electronic noise

**Investigation date:** 9 October 2026  
**Status:** Conditional analytical derivations and synthetic numerical checks. **No new natural law, microscopic mechanism established in a material, or historic foundational scientific discovery has been established.** Historical priority of the exact formulations below is unverified. There is no independent expert review or formal proof certificate.

## 1. Scientific question and outcome

The selected question was whether strongly suppressed electrical noise in anomalous metals requires a different microscopic description of charge transport, or can arise from local thermal transport and electrical/thermal feedback. The investigation considered cosmic expansion, bacterial intergenerational memory, glass transport, and anomalous electronic noise before concentrating on the last. These were preliminary screens, not four completed research programmes.

The original observations are those reported by Chen et al. for YbRh2Si2 [S1] and Szurek et al. for beta-Ta [S3]. They are not measurements performed in this investigation. A published challenge to the interpretation of the YbRh2Si2 measurements considers cooling, spreading/contact resistance, and measurement response [S2]. Existing microscopic theories also include coupled electron–boson transport and fractionalization [S7,S8]. None of these interpretations is declared established or disproved here.

The mechanism examined most closely was additional heat transport, possibly through electrically neutral modes sharing a local temperature with the charged sector. Rather than assign a free cooling curve to every noise trace, the analysis derived constraints that this mechanism must satisfy. A separate analysis allowed general reciprocal heat leakage and electrothermal feedback near zero bias.

The strongest completed work consists of: (A) an exact frozen-temperature noise–resistance identity and sharp bounds; (B) a weak-bias relation between noise, dc resistance and complex impedance in a specified electrothermal Langevin model; and (C) an exact bias–bath-temperature constraint for a single-temperature, energy-conserving local transport model. These are tests of assumptions, not discoveries of what a particular material actually does. Explicit counterexamples prevent applying the tests beyond their assumptions.

## 2. Notation, physical conventions, and known starting points

Use one-sided classical voltage-noise spectral density, so an equilibrium resistor has S_V = 4 k_B T R. Assume electrical quasistatic response and frequencies small compared with k_B T/h. This convention and the dissipation-weighted local-temperature expression are established noise-thermometry results [S4,S5], not new discoveries.

At nonzero bias distinguish:

- R = V/I, the secant resistance, equal to the electrical resistance when the mean temperature profile is frozen;
- r_d = dV/dI, the quasistatic differential resistance;
- Z(omega), the small-signal impedance including temperature response.

These generally differ. If only r_d(I) is measured and V(0)=0, then R(I) = I^(-1) integral_0^I r_d(i) di. Replacing R with r_d without justification invalidates several formulas below.

The noise temperature N or T_N is S_V/(4 k_B R). Out of equilibrium it is an effective electrical observable, not necessarily a physical temperature of every part of a conductor. All local-noise calculations below assume independent Johnson sources, a local Ohmic law, and no thermoelectric cross terms. They do not establish the validity of those assumptions in a strange metal.

The term **frozen temperature** means that temperature fluctuations cannot appreciably respond in the electrical-noise band. It does not mean the mean temperature profile is uniform. Such a frequency window need not exist in every device.

## 3. Result A: frozen-temperature identity and sharp bounds

### 3.1 Assumptions and statement

Consider a bounded, connected two-terminal domain with appropriate regularity for the weak elliptic problems below. Fix a symmetric uniformly positive geometric tensor M(x). The local electrical conductivity is

\[
\sigma(x,T)=\frac{M(x)}{a+bT},\qquad b>0,
\]

with a+bT positive throughout the admitted temperature range. The continuum proof also has an exact finite-graph version with edge resistances r_e = g_e(a+bT_e), g_e>0. Insulate the other boundaries. There is no Hall term, field-dependent intrinsic resistivity, or nonlocal electrical response. Noise is evaluated at the frozen mean temperature profile.

Let u be the characteristic potential, equal to zero and one on the terminals, satisfying

\[
\nabla\cdot\left[\frac{M\nabla u}{a+bT}\right]=0.
\]

Define

\[
G=\int_\Omega\frac{\nabla u^TM\nabla u}{a+bT}\,dx,
\qquad R=G^{-1},
\qquad T_N=G^{-1}\int_\Omega T\frac{\nabla u^TM\nabla u}{a+bT}\,dx.
\]

Let u_* minimize the geometric Dirichlet energy K(v)=integral grad(v)^T M grad(v) with the same terminal values, and write K_*=K(u_*). At uniform temperature t,

\[
R_{\rm eq}(t)=\frac{a+bt}{K_*}.
\]

At bath temperature T_0 set R_0=R_eq(T_0), R'_0=b/K_*, and

\[
T_R=T_0+\frac{R-R_0}{R'_0}.
\]

**Exact identity:**

\[
\boxed{T_N=T_R+\frac{R}{b}\mathcal E},\qquad
\mathcal E=\int_\Omega\nabla(u-u_*)^TM\nabla(u-u_*)\,dx\ge0.
\tag{A1}
\]

Consequently T_N >= T_R. If T_- <= T(x) <= T_+, the stronger sharp interval is

\[
\boxed{
T_R\le T_N\le T_R+
\frac{b(T_R-T_-)(T_+-T_R)}{a+bT_R}.
}
\tag{A2}
\]

Sharpness is over the allowed class of geometries and temperature profiles; it does not assert that both endpoints are attainable in every fixed geometry.

### 3.2 Proof of the identity

Multiply the definition of T_N by bG and use bT=(a+bT)-a:

\[
bG T_N=K(u)-aG.
\]

The weak Euler equation for u_* gives orthogonality of grad(u_*) and grad(u-u_*) in the M inner product. Thus

\[
K(u)=K_*+\mathcal E.
\]

The definition of T_R implies a+bT_R=RK_*. Dividing the previous identity by bG proves (A1). All these steps are algebraic/variational within the stated model.

Equality does not require uniform temperature: parallel hot and cold branches can have the same characteristic potential as the geometric minimizer. The excess in (A1) measures a change of electrical potential profile, not temperature variance by itself.

### 3.3 Proof of the upper bound

Write r=a+bT, r_-=a+bT_-, r_+=a+bT_+, and j=M grad(u)/r. Its terminal flux is G. Then

\[
K(u)=\int r^2 j^TM^{-1}j,\qquad G=\int r j^TM^{-1}j.
\]

Since (r-r_-)(r_+-r)>=0,

\[
K(u)\le(r_-+r_+)G-r_-r_+\int j^TM^{-1}j.
\]

The geometric Thomson principle, at terminal flux G, gives integral j^T M^(-1)j >= G^2/K_*. This principle follows directly by writing j as the minimizing divergence-free flux plus a zero-terminal-flux perturbation; the cross term vanishes by integration by parts. Therefore

\[
K(u)\le(r_-+r_+)G-r_-r_+G^2/K_*.
\]

Substitution into bGT_N=K(u)-aG gives (A2). A two-temperature series conductor saturates the upper endpoint. Parallel branches saturate the lower endpoint. The positivity of r_- r_+ is used in the inequality.

If T_R>T_- and the measured noise is known to be in the frozen regime, (A2) also implies

\[
T_{\max}\ge T_R+\frac{R}{R'_0}\frac{T_N-T_R}{T_R-T_-}.
\tag{A3}
\]

No hotspot temperature is inferred from experimental data in this investigation.

### 3.4 Observable form and failure controls

The lower bound is equivalently

\[
S_V\ge4k_BR\left[T_0+\frac{R-R_0}{R'_0}\right],
\]

or, subtracting the measured zero-bias equilibrium value,

\[
\Delta S_V\ge4k_B\left[T_0(R-R_0)+\frac{R(R-R_0)}{R'_0}\right].
\tag{A4}
\]

The local common-affine-material hypothesis is essential. A linear terminal R_eq(T) alone does not establish it.

**Counterexample: different-material contact.** A cold, temperature-independent 10-ohm contact is in series with a wire having R_wire(t)=t ohms/K. At bath temperature 1 K and wire temperature 10 K, R_eq(t)=10+t, R_0=11, and R=20 ohms. Terminal calibration gives T_R=10 K, but the actual frozen noise temperature is (10*1+10*10)/20=5.5 K. The contact violates the local common-material assumption.

**Counterexample: convex material law.** Two equal-geometric-factor parallel branches with rho(t)=t^2 at temperatures 1 and 10 have T_N=1.08910891 and T_R=1.40719509. An arbitrary increasing resistivity law cannot replace the affine assumption in (A1).

For a common affine law with b<0, the identity still holds but the sign of the correction reverses. In particular, the positive-slope lower bound is not directly applicable to beta-Ta, whose measured resistivity has a weak negative temperature coefficient [S3].

A finite-bias electrothermal counterexample, below, also shows why the frozen-frequency restriction cannot be dropped.

## 4. Result B: weak-bias electrothermal noise–impedance relation

### 4.1 Precisely specified model

Use a finite connected resistor network at a uniform bath temperature T. Thermal nodes coincide with electrically dissipating elements. Let A be a real symmetric positive-definite thermal conductance matrix and C a real symmetric positive-definite heat-capacity matrix. They may include internal thermal links and leakage to the bath. Use a current bias I and neglect thermoelectric effects and intrinsic field dependence of resistance.

At the reference temperature all elements have the same fractional resistance slope

\[
c=\frac{r'_e(T)}{r_e(T)}=\frac{R'_0}{R_0}>0.
\]

Only this common first derivative is needed at the order considered; a globally affine material law is not required. Electrical and thermal noises are independent at equilibrium, with one-sided covariances

\[
C_e=4k_BT\,\operatorname{diag}(r_e),\qquad C_Q=4k_BT^2A.
\]

The result is at leading order in the standard linearized Gaussian Langevin approximation. It does not include nonlinear fluctuation-loop corrections to equilibrium transport or an arbitrary microscopic quantum bath.

Let j_e be the current in edge e under unit terminal current and let q_e=r_e j_e^2. Define

\[
H(\omega)=q^T(A+i\omega C)^{-1}q,\qquad H_0=H(0)>0.
\]

Then, for a smooth stable branch near I=0,

\[
R(I)=R_0+cH_0I^2+O(I^4),
\]

\[
Z(I,\omega)=R(I)+2cI^2H(\omega)+O(I^4).
\tag{B1}
\]

Put Delta S_V=S_V(I,omega)-4k_BTR_0. The eliminated relation is

\[
\boxed{
\frac{\Delta S_V}{4k_B}
=\left(T+\frac1c\right)(R-R_0)
+\left(T+\frac{cT^2}{2}\right)(\operatorname{Re}Z-R)
+O(I^4).
}
\tag{B2}
\]

All observables in this equation must refer to the same device, bath temperature, bias, and electrical frequency window. Uncertainty in c is important, especially near c=0. A dividing-by-c formulation should not be used when the slope is indistinguishable from zero.

### 4.2 Derivation

The mean temperature rise is I^2 A^(-1)q+O(I^4). The resistance sensitivity is dR/dT_e=cq_e by the electrical energy variational principle. This proves the dc expansion in (B1). Modulating the terminal current produces a leading heat-source modulation 2Iq delta I; thermal response then proves the impedance expansion.

For completeness, current redistribution does not destroy the equilibrium Johnson–Joule cross correlation used next. Let D be an edge-by-node incidence matrix with one grounded node, g_e=1/r_e, and L=D^T diag(g)D. The response of edge current to additive edge voltage noise is

\[
M=\operatorname{diag}(g)DL^{-1}D^T\operatorname{diag}(g)-\operatorname{diag}(g).
\]

It is symmetric and M diag(r)j=0. The bare terminal voltage noise is e_out=j^T e. To leading order in I the random electrical power delivered to the thermal subsystem is

\[
\delta p=[2\operatorname{diag}(rIj)M+\operatorname{diag}(Ij)]e.
\]

Using C_e=4k_BT diag(r) and the displayed annihilation identity yields

\[
\operatorname{Cov}(e_{\rm out},\delta p)=4k_BT Iq.
\]

There are three contributions at order I^2. In units of 4k_B they are:

\[
I^2H_0(1+cT)
\quad\hbox{(mean heating and resistance change)},
\]

\[
2TcI^2\operatorname{Re}H
\quad\hbox{(Johnson–Joule cross term)},
\]

\[
T^2c^2I^2\operatorname{Re}H
\quad\hbox{(thermal fluctuations transduced to voltage)}.
\]

For the last contribution use

\[
(A+i\omega C)^{-1}A(A-i\omega C)^{-1}
=\operatorname{Re}(A+i\omega C)^{-1}.
\]

Adding the contributions and eliminating H_0 and Re H using (B1) proves (B2).

Diagonalizing C^(-1/2) A C^(-1/2) shows that Re H is a positive sum of lambda/(lambda^2+omega^2). Thus

\[
0\le\Phi(\omega):=\operatorname{Re}H/H_0\le1.
\]

Writing R_2=cH_0, the same prediction is

\[
S_V=4k_BTR_0+4k_BR_2I^2
\left[\frac1c+T+(2T+cT^2)\Phi(\omega)\right]+O(I^4).
\tag{B3}
\]

At frozen high frequency Phi tends to zero; at quasistatic frequency it tends to one. General electrothermal feedback and bolometer-noise physics are established subjects [S6]. No claim is made to have discovered feedback.

### 4.3 Ordinary finite-bias counterexample to an unrestricted lower bound

Take two parallel branches of the same affine material a=b=1. A cold branch is clamped to temperature 1 and has resistance 2. A hot branch has geometric factor 18/101, temperature 100, resistance 18, and resistance derivative beta=18/101. Apply terminal voltage V=1, so the hot current is i_h=1/18.

Choose a linear heat link to the bath with conductance

\[
G_{\rm th}=i_h^2 r_h/(100-1)=1/1782.
\]

Specify its one-sided heat-noise density as 2k_B G_th(T_h^2+T_b^2). This is a stated classical Langevin countermodel, not an empirically validated description of YbRh2Si2.

The hot branch's local loop parameter is ell=i_h^2 beta/G_th=99/101. At fixed voltage its electrical-noise amplitude is attenuated by 1/(1+ell), and its differential admittance is g_h(1-ell)/(1+ell). Combining the branches and converting to ideal-current-bias voltage noise gives

\[
R=1.8,\quad Z(0)=1.9977802442,
\]

\[
T_N^{\rm frozen}=T_R=10.9,
\qquad \frac{S_V(0)}{4k_BR}=5.7746587526.
\]

The full zero-frequency noise is only 0.5297852 times the frozen-profile noise, including the stated heat-link fluctuations. Hence a universal assertion that positive-temperature-coefficient electrothermal feedback can only increase the measured terminal noise is false. This does not contradict (B2), which is a weak-bias expansion about a uniform-temperature state, or (A1), which assumes frozen temperature fluctuations.

## 5. Result C: the bias–bath-temperature constraint

### 5.1 The physical mechanism class

Suppose electrical and heat transport share a single local temperature t(x). Extra neutral heat carriers may be included if they equilibrate locally with the charged sector and their total heat conductivity obeys the proportionality stated below. Assume local Ohm/Fourier laws, no thermoelectric terms, no bulk energy loss, and contacts at a common bath temperature T with potentials zero and V. All other boundaries are insulating for both currents.

Let sigma(x,t) be symmetric and uniformly positive at the solution, with no explicit electric-field dependence. Assume

\[
\hat\kappa(x,t)=w(t)\sigma(x,t),\qquad w(t)>0.
\tag{C0}
\]

The function w is a property of local temperature alone, not a separately adjusted function of applied bias or bath temperature. It need not equal L_0 t. For isotropic material this is w(t)=kappa(t)rho(t). Thus arbitrary temperature-dependent deviations from the Wiedemann–Franz ratio are allowed, but arbitrary tensor misalignment and different temperatures of neutral and charged modes are not.

This form slightly strengthens the separable tensor setting used in the numerical checks: for the noise identity no factorization sigma=M/rho is required. The proof below directly establishes that extension. The additional conductance formula in Section 5.5 does require separability.

Noise is again calculated from local Johnson sources with the mean temperature profile frozen. Define N(V,T)=S_V/(4k_B R) and

\[
W(t)=\int^t w(s)ds,\qquad \Theta=W^{-1}.
\]

Assume the attained range is in the range of W and the steady solution exists. No theorem here asserts existence at arbitrarily high voltage when W has a finite upper limit.

### 5.2 Heat-potential identity and exact noise integral

The steady equations are

\[
\nabla\cdot(\sigma\nabla\varphi)=0,
\qquad
\nabla\cdot(\hat\kappa\nabla t)+\nabla\varphi^T\sigma\nabla\varphi=0.
\]

Since sigma grad(W(t))=kappa_hat grad(t), these imply that

\[
F(x)=W(t(x))+\varphi(x)^2/2-V\varphi(x)/2
\]

is sigma-harmonic. It equals W(T) at both contacts and has zero flux at the other boundaries. Test its weak equation with F-W(T); positivity of sigma gives F=W(T). Hence

\[
\boxed{W(t(x))=W(T)+\tfrac12\varphi(x)[V-\varphi(x)].}
\tag{C1}
\]

For any continuous f, the divergence theorem applied to a primitive of f gives

\[
\int_\Omega f(\varphi)\nabla\varphi^T\sigma\nabla\varphi\,dx
=I\int_0^V f(v)dv.
\]

Using the local dissipation-weighted temperature formula yields

\[
\boxed{N(V,T)=\int_0^1\Theta\left[W(T)+\frac{V^2}{2}s(1-s)\right]ds.}
\tag{C2}
\]

The heat-potential and characteristic-potential methods, including geometry cancellation in the Wiedemann–Franz case, have clear antecedents [S4,S5]. They must not be represented as originating in this investigation. Equations (C1)–(C2) are derived here for the stated arbitrary w class; priority of that generality and of the following eliminated formulations has not been established.

### 5.3 Eliminate the unknown thermal transport function

Define the observable weak-bias curvature

\[
\alpha(T)=\lim_{V\to0}\frac{N(V,T)-T}{V^2}=\frac{1}{12w(T)}.
\tag{C3}
\]

The entire bias–temperature surface obeys

\[
\boxed{V\partial_VN+N-T=3\alpha(T)V^2\partial_TN.}
\tag{C4}
\]

Here partial_T is a derivative with respect to bath temperature at fixed physical voltage and for the same material law. It is not a derivative along a temperature-dependent experimental bias window.

**Proof.** Let y=V^2/8 and z=2s-1. By symmetry,

\[
N=\int_0^1\Theta(W(T)+y(1-z^2))dz.
\]

Integrating the derivative of z Theta(W(T)+y(1-z^2)) gives

\[
N-T=2y\int_0^1z^2\Theta'\,dz.
\]

Also 2y partial_y N=2y integral(1-z^2)Theta' dz and partial_T N=w(T) integral Theta' dz. Add the first two equations and use 2y=V^2/4 and (C3). This proves (C4).

If N has an even Taylor expansion to the required order,

\[
N=T+\sum_{n\ge1}c_n(T)V^{2n},
\]

comparison of coefficients gives

\[
c_0=T,\quad c_1=\alpha,\qquad
\boxed{c_{n+1}=\frac{3\alpha}{2n+3}\frac{dc_n}{dT}.}
\tag{C5}
\]

In particular,

\[
c_2=\frac35\alpha\alpha',\qquad
c_3=\frac9{35}\alpha[(\alpha')^2+\alpha\alpha''].
\]

Equivalently these are -w'/(240w^3) and (3w'^2-ww'')/(6720w^5). Smoothness supplies the corresponding finite-order identities; convergence of an infinite Taylor series is not assumed from smoothness alone.

This predicts higher-order voltage response from the measured low-bias curvature versus bath temperature. It is not a different free fit to each trace.

### 5.4 Quantitative consequences for attempted noise-suppression mechanisms

If alpha(T) is proportional to T^(-2) on a temperature interval, then w(T) is proportional to T^2 on that interval. If that same material law persists to all temperatures attained under high bias, (C2) predicts N proportional to |V|^(2/3) once the bath contribution is negligible. It cannot simultaneously give an exactly linear asymptote in |V|. The continuation qualification matters: a low-temperature law alone does not establish a high-bias asymptote.

More generally w(t)=C t^m, m>-1, gives a high-bias temperature exponent 2/(m+1) while that law holds. For a constant Lorenz ratio, w=L t, the integral recovers the established hot-electron result, including F=sqrt(3)/4 when L=L_0 [S5]. Enlarging a constant L can reduce the high-bias noise but preserves the corresponding single-temperature scaling; it is not an arbitrary explanation of temperature-dependent noise curves.

An exact noise surface of the form N(V,T)-T=C f(V/T), with nonzero temperature-independent C and a nontrivial smooth f having nonzero quadratic term, is incompatible with (C4) over an open interval of T. To see this, write f(x)=f_2 x^2+..., so alpha=Cf_2/T^2. At fixed x=V/T, (C4) becomes

\[
x f'(x)+f(x)=3f_2x^2\left[1-\frac{C}{T}x f'(x)\right].
\]

The left side is independent of T, whereas the right side has unavoidable 1/T dependence for nontrivial f. Fixed unit-conversion constants between voltage and temperature can be absorbed into x and do not alter the contradiction.

The reported beta-Ta fits, approximately inverse-temperature Fano factor and nearly constant broadening factor, motivate this comparison [S3]. They do not establish the exact surface assumed in this corollary. In particular, an approximate coth fit must not be promoted to an exact physical noise law and differentiated to manufacture a violation; even conventional hot-electron noise need not have that exact interpolation. No exclusion of a physical heat-transport mechanism in beta-Ta is claimed here.

### 5.5 An additional conductance prediction in the separable subclass

If sigma(x,t)=M(x)/rho(t), let K_* be the geometric conductance for M. From (C1), t depends on phi. Define psi(phi)=integral_0^phi dv/rho(t(v)). Then div(M grad psi)=0, and hence

\[
G(V,T)=K_*\int_0^1\frac{ds}{\rho\{\Theta[W(T)+V^2s(1-s)/2]\}}.
\tag{C6}
\]

Thus the same w inferred from weak noise curvature, together with independently established rho, predicts both nonlinear conductance and the noise surface. The conductance formula is not claimed for a nonseparable sigma tensor.

## 6. Actual computations performed

All calculations below used synthetic systems, not experimental measurements. They test implementation consistency and attempted falsifications, not historical novelty or physical realization. Floating-point agreement is not a formal verification of an analytic theorem.

`check_theorems.py`, seed 20261009:

- 1,500 connected random resistor networks tested (A1) and (A2). Maximum scaled identity error was 1.0430062526338902e-13. The most negative lower-bound margin was -3.55e-15, at roundoff scale; the minimum upper-bound margin was positive. Separate exact-sharpness examples checked series and parallel saturation.
- Convex-material, different-material-contact, and finite-bias electrothermal counterexamples were evaluated explicitly.
- Twenty random electrical/thermal networks at three frequencies each tested (B2) against an independently assembled finite-bias Langevin covariance calculation. The maximum relative quadratic-noise-coefficient error at I=0.002 in the code's dimensionless units was 1.50979422677144e-05. Halving current reduced the coefficient error by a median factor 4.0000775, consistent with an omitted O(I^4) noise term.

`check_heat_potential.py`:

- Twenty-four nonlinear one-dimensional boundary-value problems independently solved local charge and heat equations with rho(t)=2+0.7t and kappa(t)=(1+t)^p/rho(t), across four p values, two bath temperatures and three biases.
- Maximum disagreement between spatially integrated noise and (C2) was 4.3841152930212957e-11 in dimensionless temperature units.
- The maximum scaled finite-difference residual of (C4) was 2.270794010699853e-09.
- Symbolic checks verified the fourth- and sixth-order coefficient identities.

The C computations test a one-dimensional separable subset, not arbitrary tensor geometries numerically; the latter are covered by the stated analytical proof. No quantum many-body simulation was run.

## 7. Empirical evidence and its limits

### Evidence read

The original YbRh2Si2 paper and supplementary material were read, including images of the principal noise/resistance plots [S1]. The beta-Ta primary manuscript was read [S3]. The YbRh2Si2 interpretation was checked against the primary competing analysis [S2]. Current microscopic alternatives and established noise-thermometry work were also consulted [S4–S8].

The original authors' claims about cooling and their controls, and the challengers' alternative assumptions about geometry and measurement, remain source claims. This investigation does not independently settle their disagreement.

### Raw-data access

The public Zenodo record for YbRh2Si2 was accessible [S9]. It lists All_data_YRS.zip, 18.1 GB, MD5 1a1e84ea5938e16ff07d956eddb8db4e. The archive bytes were not acquired in the computational environment. Some member names were visible through the archive preview, but no raw traces were obtained. The beta-Ta manuscript states that data are available from its authors upon reasonable request; no such data were obtained.

Consequently no independent experimental reduction, fit, covariance estimate, likelihood ratio, p-value, derivative estimate, or experimental residual of (B2)/(C4) was computed. Visual inspection of figures is not substituted for raw measurements. No numerical experimental hotspot bound is reported.

### What is and is not established

The evidence supports investigating anomalous noise. It does not establish that either material violates the derived assumptions/tests. A failed local-thermal test, were one demonstrated with controls, would identify failure of a stated transport class, not by itself establish a unique new microscopic mechanism or the presence/absence of quasiparticles. Conversely, passing a thermal test would not establish quasiparticles: a nonquasiparticle fluid might satisfy the same local constitutive assumptions.

The requested discovery remains unestablished specifically because no discriminating physical residual, independently supported causal mechanism, or validated new quantitative explanation has been obtained—not because the scientific question is longstanding.

## 8. Repository capital and provenance

**Astra pin:** a09fe480a5b51aee15af1a963c5d3c1437c0eeb2. The first read was `00_START_HERE.txt`. Navigation and source-status notices were retained. In particular, the actual N475 cosmology proof was read through `web/pages/d-f57478bb6e4f43d0.html`, after the original archive paths were not directly available at the repository contents endpoint. Its relevant method is elimination of an unknown physical function using sharp integral envelopes, with sufficiency/closure and observational limitations kept separate. Its status is source-derived/unreviewed and explicitly not a foundational discovery. No DESI fit in that document was performed anew here. N454's review card was inspected but is not a premise of these results.

**OpenAI math pin:** fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb. The manuscript map and a selected electrical-energy proof section were read: `preprints/A-Linear-Clock-for-Random-Walk-on-Tree-Weighted-Planar-Maps-October-5-2026/build/sections/04-energy.tex`. The returned section was truncated; no complete audit of that manuscript was performed. The inspected ideas were variational energy comparison, quadratic structure, and geometric control. No random-map result, repository-wide certification, or unreviewed upstream theorem is used as a physical premise. All elementary identities needed above are derived explicitly.

These source revisions are preserved in `sources.json`. Reading or indexing an upstream claim does not promote its correctness or scientific status.

## References and source keys

[S1] L. Chen et al. *Shot noise in a strange metal*. Science 382, 907–911 (2023), doi:10.1126/science.abq6100; arXiv:2206.00673, including supplementary material.

[S2] B. A. Polyak, V. S. Khrapai and E. S. Tikhonov. *What can we learn from nonequilibrium response of a strange metal?* arXiv:2402.09946 (2024); JETP Letters publication linked by the primary record.

[S3] M. Szurek et al. *Anomalous shot noise in a bad metal beta-tantalum*. arXiv:2410.18349v2, submitted 21 February 2025. The generated HTML dateline is not treated as the manuscript submission/publication date.

[S4] C. Pozderac and B. Skinner. *Relation between Johnson noise and heating power in a two-terminal conductor*. Physical Review B 104, L161403 (2021); arXiv:2104.05714v2, especially Appendix A.

[S5] E. V. Sukhorukov and D. Loss. *Noise in multiterminal diffusive conductors: Universality, nonlocality, and exchange effects*. Physical Review B 59, 13054 (1999); arXiv:cond-mat/9809239. The full proof was not independently audited here; the antecedent hot-electron result was also read in [S4].

[S6] K. D. Irwin. *Thermodynamics of nonlinear bolometers near equilibrium*. Nuclear Instruments and Methods in Physics Research A 559, 718–720 (2006). Primary NIST publication page consulted; not a full independent audit of bolometer theory.

[S7] Y. Wang et al. *Shot noise in coupled electron-boson systems*. arXiv:2404.14515v2. Different thermalization/drag regimes are distinguished in that work; it is not represented as excluding every neutral heat-carrier mechanism.

[S8] A. S. Patri et al. *The Sound of Electrons Shattering: Current Noise Composition Laws for Electron Fractionalization*. arXiv:2509.25322v2. Existing microscopic alternative, not a result invented here.

[S9] L. Chen, D. Lowder and D. Natelson. *Data and code for: Shot noise noise in a strange metal*. Zenodo, doi:10.5281/zenodo.7800018. Metadata/preview accessed; archive not downloaded.
