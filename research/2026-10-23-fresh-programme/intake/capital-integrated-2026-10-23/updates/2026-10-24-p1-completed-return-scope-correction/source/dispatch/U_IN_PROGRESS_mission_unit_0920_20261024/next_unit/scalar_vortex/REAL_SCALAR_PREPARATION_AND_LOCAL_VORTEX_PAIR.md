# Real scalar preparation and a finite observation of a vortex pair

24 October 2026. Owned internal model construction. Exact algebra, the work/readout ledger, finite-aperture compatibility, and primary ancestry have bounded independent support checks; the complete preparation proof awaits consequential root read. No experimental acquisition, novelty, efficiency, strong-interaction result, or vortex lifetime is claimed.

## 1. Selected operation and strong ancestry

The operation is to start with an ordinary vortex-free harmonic ground state, use only a real scalar density potential with finite spatial aperture and smooth finite-time controls, return that potential to its initial form, and acquire two opposite local phase windings in a predeclared finite readout window. The controls conserve field norm and do not insert an imposed vortex phase or a complex additive source. This addresses acquisition rather than inferring reachability from the existence or stability of a vortex state.

I compared this with another wave-isolation/transfer-bound route and selected scalar preparation because it supplies a different concrete controlled field operation. I do not select a material or a device implementation.

The broad physical operation is already established. Klein, Jaksch, Zhang and Bao (PRA 76, 043602, 2007) analytically describe harmonic vortex-pair birth/annihilation and simulate weakly interacting Gross--Pitaevskii dynamics, starting with vortex-bearing profiles and discussing phase-imprint/stirring preparation. Tamura, Chen and Hung (PRX 13, 031029, 2023) experimentally produce vortex--antivortex structures after lowering a circular box wall, without imposing a vortex phase. Thus neither pair generation nor density/trap-quench generation is a new capability claim here. The derivation below pins one real-potential ground-state preparation, paid finite-control completion, and local topological readout at its exact model scope.

## 2. Field, inputs, controls and readout in one setting

Use dimensionless harmonic units on R^2 and norm-one fields:

\[
H_0=\frac12(-\Delta+x^2+y^2),\qquad
i\partial_t\psi=[H_0+U(t,x,y)+g|\psi|^2]\psi,
\quad g\ge0,\quad \|\psi\|_2=1.
\tag{1}
\]

The interaction g is fixed during the protocol. U is real, smooth, of finite duration, and supported in a fixed finite disk. The confining harmonic background is an explicit supplied resource, not a compactly supported trap. There is no dissipative or complex source term.

At g=0 the input is the ordinary Gaussian ground state G0=pi^(-1/2)exp(-r^2/2). For small fixed g>0 the input is the ordinary positive radial harmonic GP ground state Phi_g, or a sufficiently accurate prepared approximation. This stock, its cold/phase-coherent preparation, and the harmonic confinement are inputs, not obtained from vacuum by the protocol. The engineered target state below is not assumed available as stock.

The observation is local: two disjoint compact disks inside a finite window K, with nonzero contour density and opposite phase winding. We do not infer a stable hydrodynamic vortex from an isolated zero in an arbitrarily dilute tail, nor assert the absence of zeros outside K.

## 3. An exact positive prototype and its harmonic zeros

Fix real parameters

\[
b>0,\qquad a>b^2/4,\qquad
P(x,y)=r^2+a+b x>0,
\quad Z=(a+1)^2+1+b^2/2,
\tag{2}
\]

and define

\[
\phi_I=cP e^{-r^2/2},\qquad c=(\pi Z)^{-1/2}.
\tag{3}
\]

This state is strictly real and positive everywhere, with no initial phase winding. Direct differentiation gives

\[
H_0(Pe^{-r^2/2})
=e^{-r^2/2}(3r^2+a+2bx-2).
\]

Consequently phiI is the positive eigenfunction, eigenvalue 3, of the real potential

\[
V_{\rm pre}=\frac{r^2}{2}+W_1,
\qquad W_1=\frac{2(a+1)+b x}{P}.
\tag{4}
\]

Its positivity and the ground-state transform make it the simple ground state. W1 is smooth and bounded, generically O(1/r) rather than compactly supported. Merely identifying this ground state is not yet a preparation protocol; Section 4 supplies one without using it as an initial-state oracle.

Under H0 its exact linear evolution is

\[
\psi_I(t)=ce^{-r^2/2-it}
\left[(a+1)+bxe^{-it}+(r^2-1)e^{-2it}\right].
\tag{5}
\]

For sin t nonzero, its zeros obey

\[
x_v=-\frac{2(a+1)}b\cos t,\qquad
x_v^2+y_v^2=a+2.
\tag{6}
\]

They exist when

\[
|\cos t|\le\frac{b\sqrt{a+2}}{2(a+1)}<1.
\tag{7}
\]

At t*=pi/2 there are exactly two simple zeros

\[
p_\pm=(0,\ \pm\sqrt{a+2}).
\tag{8}
\]

After an irrelevant global phase, the local polynomial is a+2-r^2-i b x. Its real-to-imaginary spatial Jacobian determinant is -2by, nonzero at both points and of opposite sign. The local windings are therefore plus and minus one (upper negative for b>0). The complete field is smooth throughout the birth event; a phase/velocity description becomes singular at a zero, not the underlying wavefunction or its scalar drive.

No singular force, nonconserved norm, or nonzero net angular momentum was introduced. The pattern is interference of finitely many harmonic eigenmodes; this does not by itself establish a persistent nonlinear vortex quasiparticle.

## 4. Finite real-potential preparation from ordinary stock

### 4.1 A positive ground path and its literal endpoint issue

For s in [0,1], define

\[
P_s=(1-s)+sP>0,\qquad
\phi_s=c_sP_s e^{-r^2/2},\qquad
W_s=\frac{2+2sa+s b x}{P_s}.
\tag{9}
\]

Then H_s=H0+Ws has simple positive ground phi_s at eigenvalue 3. At s=0 it is H0+2 and phi_0=G0; at s=1 it is (4). The fixed constant 2 is an energy origin. Subtracting it throughout leaves the same states and gaps and makes the initial Hamiltonian H0 and the ideal ground eigenvalue 1.

The family Ws is uniformly bounded, with uniformly bounded spatial derivatives of each fixed order. Complete the denominator as

\[
P_s=s[(x+b/2)^2+y^2]+(1-s)+s(a-b^2/4),
\tag{10}
\]

which is uniformly positive. At s=0 the ideal family is NOT continuous in the L-infinity multiplier norm: for every positive s, Ws tends to zero far away, whereas W0=2. We do not apply an operator-norm-smooth adiabatic theorem to this uncut endpoint.

The ideal H_s is nevertheless norm-resolvent continuous. Ws is strongly continuous as a bounded multiplication family. Multiplying this strong convergence by the compact harmonic resolvent gives norm convergence; the resolvent identity transfers it to H_s. Its simple ground is always 3, its spectrum is discrete, and the next eigenvalue depends continuously on s. Hence on the compact parameter interval it has a uniform positive gap delta.

### 4.2 A compact aperture removes the control discontinuity

Let chi_R be a fixed smooth radial cutoff, one for r<=R and zero for r>=2R, and use the actual preparation Hamiltonian

\[
\widehat H_s^R=H_0+\chi_R(W_s-2).
\tag{11}
\]

It starts at H0 exactly. Every control beyond the supplied harmonic trap is real and compactly supported. For each finite R, all s derivatives are bounded smooth multipliers, and the common operator domain is D(H0). The ideal comparison is H_s-2, not H_s: this is the same fixed energy-origin normalization at every s.

The cutoff family converges to H_s-2 uniformly in s in norm resolvent. One explicit tail bound is

\[
\|\mathbf1_{r>R}(H_s+i)^{-1}\|\le C/R,
\tag{12}
\]

uniform in s. It follows from the uniform boundedness of Ws and the quadratic form control of r(H_s+i)^(-1). The resolvent identity and the uniform bound on Ws-2 then prove the claim; shifting the resolvent point by a fixed real constant is immaterial. Harmonic confinement excludes an extra low-energy branch at infinity. For all sufficiently large finite R, the truncated family therefore has a simple uniformly gapped ground phi_s^R, with endpoint phi_1^R converging to phiI in L2.

The convergence holds in each fixed harmonic graph norm D(H0^k). Uniform bounded spatial derivatives of the potentials, the confining elliptic equation, and bounded low eigenvalues give uniform higher graph bounds for the ground states; interpolation upgrades L2 convergence. This is a model spectral estimate, not an assertion of experimental spatial resolution.

### 4.3 Actual finite-time norm-conserving acquisition

Choose a fixed smooth increasing schedule s=chi(t/T), flat at the endpoints. For finite R this is a common-domain smooth gapped family, so its linear evolution from G0 prepares phi_1^R with error O_R,k(T^(-1)) in any selected fixed D(H0^k), up to a global phase. A direct way to see the hypotheses is to use the reduced inverse

\[
\mathcal R_s^R=(\widehat H_s^R-\lambda_s^R)^{-1}
 (1-|\phi_s^R\rangle\langle\phi_s^R|).
\]

The real normalized ground has zero Berry connection. The ansatz

\[
e^{-i\int\lambda_{s(t)}^Rdt}
\left[\phi_{s(t)}^R+i\dot s\,\mathcal R_{s(t)}^R
\partial_s\phi_{s(t)}^R\right]
\tag{13}
\]

has residual O_R,k(T^(-2)) in the same graph norm. Endpoint flatness removes its initial and final correction. The exact propagator is uniformly bounded in these graph norms over the slow ramp: for a positive shift A_s=H_s^R+c, differentiation of ||A_s^k psi||^2 contains only dot s times bounded relative graph operators, and integral |dot s|dt=1. Duhamel integration gives O(T^(-1)). No target ground state is supplied for free and no observed wavefunction is used as a feedback oracle; (11) is precomputed from a,b,R and the supplied model.

After preparation, remove the compact control with a smooth real ramp of duration tau>0, returning exactly to H0. For fixed finite R and a bounded initial graph norm, its endpoint differs from an instantaneous release by O_R,k(tau), by Duhamel and the bounded compact potential. Equivalently it is O(tau) close to the prepared state after accounting for the short free evolution. The release has finite amplitude and finite time derivatives for every finite chosen tau. No zero-duration bandwidth assumption is required.

Thus, at g=0, choose R large, T finite and large, and tau finite and small to make the actual post-release state arbitrarily close to phiI in a chosen high graph norm, up to phase. All additional controls have returned to zero. The field has not returned to its initial state.

## 5. Fixed weak nonlinearity: a finite horizon, not a lifetime

For defocusing g>=0 the harmonic GP ground Phi_g exists, is positive and radial, and tends to G0 in each fixed graph norm as g tends to zero. Locally this follows from the implicit function theorem at the simple harmonic ground, with the phase and norm fixed; the harmonic gap inverts the real normalized linearized equation. The ordinary input may also carry a specified sufficiently small preparation error.

Run the SAME explicit finite protocol (11) and smooth release at fixed g, starting from Phi_g. There is no physical g ramp, compensating target density, complex control source, or nonlinear adiabatic theorem in this construction. This continuation can be estimated directly. Take X=D(H0^2), whose norm controls H4(R2) and hence C1 on compact sets. The cubic map |psi|^2 psi is locally Lipschitz X to X, by Sobolev multiplication and the harmonic weighted graph estimates. Over the fixed finite horizon H=T+tau+t* plus an observation margin, the supplied smooth-potential linear propagator is bounded on X by a finite constant C_H. A Duhamel bootstrap around its bounded linear solution gives

\[
\sup_{0\le t\le H}\|\psi_g(t)-\psi_0(t)\|_X
\le C_H\left[\|\Phi_g-G_0\|_X+\sigma
 +gH(2M)^3\right],
\tag{14a}
\]

for sufficiently small g and stock error sigma, where M bounds the linear X solution plus its fixed bootstrap margin; the constants absorb the local cubic estimate. The same bootstrap bounds the actual nonlinear solution, so the nonlinearity is not evaluated on an imposed frozen prototype. For fixed R,T,tau the right side tends to zero with g and stock error. Its constant may be very large and depend on the entire preparation duration; no useful numerical interaction range is inferred.

The order is literal: choose a compact readout tolerance, then finite R,T,tau for the linear preparation, and only then a sufficiently small positive g. In two dimensions take a graph regularity embedding into C1 on the readout window. The actual field at t* after release is then C1-close to (5). There are unique simple zeros near p_plus and p_minus with the same windings: choose disjoint small disks, use nonzero boundary values/degree for existence, and closeness of the spatial Jacobian to its invertible prototype for local uniqueness. Away from those disks the prototype is bounded away from zero on a prescribed compact window, so no further zeros occur in that window.

The same argument holds on a sufficiently short fixed observation interval around t*, away from the prototype birth/death times. It is not an asymptotic-in-g retention time, an orbital stability theorem, an adiabatic nonlinear branch capture result, or a claim of strong-interaction vortex dynamics. Possible distant low-density zeros are not controlled by this local statement.

An unused but exact algebraic fact is that Vpre-g|phiI|^2 has phiI as its nonlinear positive norm-one ground. The ground-state transform gives

\[
E_g[V_{\rm pre}-g\rho_I;\psi]
-E_g[V_{\rm pre}-g\rho_I;\phi_I]
=\frac12\int\rho_I\left|\nabla\frac\psi{\phi_I}\right|^2
 +\frac g2\int(|\psi|^2-\rho_I)^2.
\tag{14}
\]

This identity checks nonlinear compatibility but is NOT used to replace the actual preparation above by an assumed target ground state.

## 6. Norm, work, angular momentum, and readout cost

The GP norm is exactly conserved. The external real potential does work according to

\[
\frac d{dt}E_g[U(t);\psi(t)]
=\int |\psi|^2\partial_tU\,dxdy.
\tag{15}
\]

Because initial and final U are both zero and g is fixed, the complete actual control work is

\[
\boxed{\quad W=E_g[H_0;\psi_{\rm final}]
-E_g[H_0;\Phi_g]\ge0.\quad}
\tag{16}
\]

The inequality uses the initial ground property. It is the complete returned-potential ledger; it does not identify electrical wall power or controller loss. A nonideal initial stock adds its excitation inventory and must be charged separately.

For the exact linear prototype,

\[
\langle H_0\rangle_I
=\frac{(a+1)^2+b^2+3}{Z},\qquad
\langle H_0\rangle_I-1=\frac{b^2/2+2}{Z}>0.
\tag{17}
\]

In the untruncated infinitely slow preparation comparison (H_s-2), the eigenvalue is constant 1, so signed adiabatic preparation work is zero; release to H0 supplies the positive excitation energy (17). The alternative one-step notation Vpre with eigenvalue 3 gives preparation cost 2 and a negative release contribution, but the same complete work (17). Those stage ledgers cannot be mixed. Finite aperture, finite ramp speed and finite g have the actual work (16), not a free ideal-stage credit.

The input is radial and all preparation/release potentials are even under y reflection. GP preserves this reflection, which reverses the angular momentum operator Lz. Hence total Lz is zero throughout the exact protocol; after release the radial trap separately conserves it. Opposite local phase windings do not require nonzero total Lz.

The observation must resolve density and phase around nonzero-density contours, not simply locate two numerical zeros. On an annulus with phase winding q, density bounded below on each radius by rho_min(r), the phase part of kinetic energy obeys

\[
\frac12\int_{r_1}^{r_2}\int_0^{2\pi}
\rho\,\frac{|\partial_\theta\vartheta|^2}{r^2}
r\,d\theta dr
\ge\pi q^2\int_{r_1}^{r_2}\frac{\rho_{\min}(r)}rdr.
\tag{18}
\]

It follows by Cauchy--Schwarz and integral dtheta vartheta=2pi q. This distinguishes a local phase winding with a density margin from a nearly empty tail singularity. It does not establish a healing-length core profile or persistent energetic superfluid vortex.

For example, the formal work (17) can tend to zero when a tends to infinity at fixed b, but the pair radius is sqrt(a+2) and its prototype field/density margins contain the Gaussian tail at that radius. They then vanish as well. Such a limit does not acquire a fixed-density readout at vanishing cost; all existence tolerances here are for fixed a,b and fixed positive compact-contour margins.

Only the potential controls return. The field stores the excitation (16). Resetting it, the external controller, any heat bath used for stock preparation, and the detector is a separate full-cycle operation. Reversible work recovery or dissipative cooling must be counted; no energy source or cheap return follows from pair acquisition.

## 7. Exact scope and physical interface

This is a constructive finite-control existence result in the stated smooth norm-conserving field model, with an ordinary input and a compact local readout. It uses no invented material response coefficient. The scalar control profile, its aperture, duration and accuracy are explicit model resources. It does not measure or manufacture those controls.

For a condensate interpretation, quasi-two-dimensional confinement, low-temperature mean-field validity, known effective g, atom number, available trap depth/resolution/slew, stock purity, and the density/phase detector are physical premises. None is acquired here. In particular the order of limits may demand a very weak interaction after a long preparation; no actual experimental parameter window, comparison with the PRX experiment, energy advantage, error rate or lifetime is established.

The linear prototype also has an optical harmonic-propagation interpretation, which is already noted in the 2007 primary. That analogy is not used to silently change hardware, inputs, controls or the physical meaning of the work ledger in this model.

## Primary capital and bounded internal checks

- Klein, Jaksch, Zhang and Bao, Physical Review A 76 (2007), 043602, DOI https://doi.org/10.1103/PhysRevA.76.043602; primary full text https://arxiv.org/html/0709.2132. Exact harmonic pair creation and weak-GP dynamics are conventional ancestry; initial vortex-profile and preparation distinctions are preserved.
- Tamura, Chen and Hung, Physical Review X 13 (2023), 031029, DOI https://doi.org/10.1103/PhysRevX.13.031029. The source comparison `luna_random_lag_sources/PRIMARY_COMPARISON.md` records the actual box-wall-quench experiment, its density readout and its distinct geometry; it blocks a broad new scalar-quench vortex-generation claim.
- Internal checks: `luna_resolvent_algebra/VORTEX_ALGEBRA_AUDIT.md`, `luna_single_port/FIXED_G_CYCLIC_CONTROL_LEDGER.md`, and `luna_boxcar/SCALAR_TRAP_RELEASE_GATE.md`. The fixed-g ledger supersedes the earlier variable-g stage ledger for this operation. These are bounded supporting checks, not external certification or a substitute for the complete preparation proof.
