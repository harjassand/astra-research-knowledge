# ASTRA foundational physics — symmetry-resolved embedded pairs with nonzero coherent interaction

27 October 2026. Independent continuation of the embedded two-photon SSH resonance. Units: \(\hbar=B=1\). This note records exact mathematical statements for an explicit local Hamiltonian, finite-chain executable checks, the original route that fails to give an exact bound state, and a deliberate counterconstruction in which radiation protection **also cancels the interaction**. No external novelty, experimental platform, or practical gate advantage is asserted.

## 1. Choice of mechanism

The preceding SSH gradient-port model had a pair resonance with a nonzero connected shift \(\chi=-g^4/12+o(g^4)\) and an eighth-order radiative linewidth \(\Gamma=(43/(5184\pi))g^8+o(g^8)\). Its two-photon radiation coefficient was a **sum of nonnegative parity-channel spectral convolutions**. Changing emitter spacing did not remove the shell contribution. One option is to prove finite-coupling resonance-error estimates. A higher-upside alternative is to **filter the one-photon bath bands by symmetry**: make each emitter-parity channel see only one side of the one-photon gap. Then the pair remains embedded in the *full* two-photon continuum but is spectrally isolated in its invariant symmetry sector. We construct this alternative.

## 2. One connected, nearest-neighbour, real-hopping ladder

There are two hard-core memory sites \(L,R\) and two semi-infinite oscillator rails \(A_j,B_j\), \(j=0,1,\dots\). Each memory has excitation energy 3. Each rail oscillator has energy 3, neighbouring sites in a rail hop with amplitude \(-1/2\), and corresponding sites across rails have real rung hopping \(+2\). Thus the bath has no direct connection between different distant rail sites other than local leg and rung edges.

Both memories attach only to **the first rung**, by real and nonnegative couplings:

\[
 t=\frac{1+\sqrt2}{2}g,\qquad s=\frac{\sqrt2-1}{2}g.
\]

Memory \(L\) connects to \(A_0\) with \(t\), to \(B_0\) with \(s\); memory \(R\) connects to \(B_0\) with \(t\), to \(A_0\) with \(s\). The Hamiltonian preserves total excitation number. The physical two-memory space excludes \(|LL\rangle\) and \(|RR\rangle\), but contains \(|LR\rangle\); no harmonic approximation is made to the two memories.

The symmetry \(S\) exchanges \(L\leftrightarrow R\) and both bath rails \(A_j\leftrightarrow B_j\). In the symmetric/antisymmetric basis
\(e_\pm=(L\pm R)/\sqrt2\), \(b_{\pm,j}=(A_j\pm B_j)/\sqrt2\), the one-particle problem becomes *exactly* two independent Jacobi problems:

* plus sector: endpoint memory energy 3, a semi-infinite band centered at 5 with hopping \(-1/2\), endpoint coupling \(\sqrt2g\), continuous spectrum \([4,6]\);
* minus sector: memory energy 3, a semi-infinite band centered at 1 with hopping \(-1/2\), endpoint coupling \(g\), continuous spectrum \([0,2]\).

The infinite graph itself is connected, and all couplings are real and local. The separation into bands is a consequence of the rail-exchange symmetry, not a nonlocal spectral projection.

## 3. A symmetry-resolved two-particle spectral gap inside the global continuum

At \(g=0\), the physical even-parity two-particle subspace has exactly one memory–memory state
\(p=|LR\rangle\) at energy 6. Other even configurations belong to lower-lower two-photon energies \([0,4]\), upper-upper energies \([8,12]\), lower-photon-plus-memory energies \([3,5]\), or upper-photon-plus-memory energies \([7,9]\). Thus \(p\) is isolated by a gap of 1 **within the even sector**.

At the same energy, the **odd sector** contains upper-plus-lower photons with continuous energies \([4,8]\), including 6. Therefore the global two-particle system is gapless at the pair energy, while the invariant even sector is gapped. This is a genuine embedded-eigenvalue setting, not a claim that the entire two-particle spectrum is gapped.

For nonzero \(g\), let \(\mu_\pm\) be the *complete* one-body endpoint spectral measures of the two parity channels (in-gap bound atom plus continuum; no pole may be silently deleted). Define

\[
 L_\sigma(z)=\iint\frac{d\mu_\sigma(x)d\mu_\sigma(y)}{x+y-z}.
\]

The exact hard-core pair resolvent, including all bath modes, is

\[
 \boxed{\langle p,(H_{g,2}-z)^{-1}p\rangle
       =\frac{2L_+(z)L_-(z)}{L_+(z)+L_-(z)}.}\tag{1}
\]

It follows from compressing the harmonic two-boson operator away from its two forbidden double-memory occupations and then using parity; it is **not** a projected-pair approximation. In the interval between the two double-bound poles \(2E_+<2E_-\), \(L_++L_-\) increases strictly from \(-\infty\) to \(+\infty\), producing a unique simple root \(E_p(g)\), hence a normalizable hard-core pair eigenvector with nonzero bare-pair overlap.

For **every** \(0<g\le0.4\), the one-body scalar Schur equations give
\(2.8<E_+(g)<3<E_-(g)<3.1\). Therefore
\[
 5.6<2E_+<E_p<2E_-<6.2,
\]
while all **even-sector continua** in this energy range lie below \(E_-+2<5.1\) or above \(E_++4>6.8\). The eigenstate is therefore isolated from the even essential spectrum by at least \(0.5\) in this declared family. Simultaneously \(E_p\in(4,8)\), so odd two-photon scattering states exist at the same energy. The embedded eigenvalue persists for the infinite system because the symmetry forbids coupling to them.

The pair residue in the bare input is exactly
\[
 Z_p=-\frac{2L_+(E_p)L_-(E_p)}{L_+'(E_p)+L_-'(E_p)}>0.
\]
An isolated even eigenprojection and the symmetry-specific spectral gap are sufficient for the adiabatic statement below, even though a *global* spectral gap is absent.

## 4. Nonzero fourth-order interaction and its closed-form coefficient

The endpoint Weyl function for a half-line chain of center \(c\), hopping magnitude \(1/2\), outside its band is
\[
 m_c(z)=2\left[(z-c)-\mathrm{sgn}(z-c)\sqrt{(z-c)^2-1}\right].
\]
At the memory energy 3 set
\(a=4-2\sqrt3\), \(b=4/\sqrt3-2\). Then
\[
 F_+(3)=-2a,\ F_-(3)=a,\qquad F_+'(3)=-2b,\ F_-'(3)=-b.
\]
The exact rank-two formula gives the general leading interaction
\[
 \chi(g):=E_p(g)-E_+(g)-E_-(g)
 =-g^4\Delta F\,\Delta F'+O(g^6),
\quad \Delta F=F_+-F_-,\ \Delta F'=F_+'-F_-'.
\]
Consequently
\[
 \boxed{\chi(g)=-(28\sqrt3-48)g^4+O(g^6)
        =-0.49742261192856\ldots\,g^4+O(g^6).}\tag{2}
\]
This is an interaction of **actual hard-core memories**, not a bare Kerr term inserted into the Hamiltonian. The pair is an *exact* eigenstate, so its intrinsic radiative linewidth is **zero for every nonzero coupling in the stated stable symmetry-protected regime**. This is stronger in a sharply delimited mathematical sense than the preceding SSH model's metastable \(g^8\) width, but uses additional band-filtering controls.

## 5. A decisive counterconstruction: protection alone can remove the interaction

Set the cross-memory couplings \(s=0\), retaining the same local ladder and a direct-to-own-rail coupling \(t=g\). The two parity couplings now have equal magnitude. There is an exact spectral reflection between their one-particle measures:
\[d\mu_+(E)=d\mu_-(6-E).\]
It follows that \(E_++E_-=6\) and \(L_+(z)=-L_-(12-z)\). Therefore the hard-core pair root is **exactly** \(E_p=6\), and
\[
 \boxed{\chi(g)=0\quad\text{to every order, not only }g^4.}\tag{3}
\]
The embedded pair still exists and remains perfectly protected, but cannot generate the desired conditional phase via a connected energy shift. A nonzero cross-endpoint coupling \(s\) breaks this extra **spectral-reflection** relation *without breaking the protecting rail-exchange parity*. This is the mechanism's crucial separation of roles: one symmetry preserves the state, a distinct asymmetry generates the interaction.

## 5A. The interaction is continuously tunable without opening a radiation channel

There is a stronger conclusion than the single calibrated ratio in §2. Let the direct and crossed first-rung memory hoppings be any sufficiently small real numbers \(t,s\), **retaining mirror symmetry**: both memories have the same direct hopping and the same crossed hopping. The parity endpoint couplings are \(c_+=t+s\), \(c_-=t-s\). The bath bands and conserving parity do not change. The leading interaction coefficient is therefore

\[
\boxed{\chi(t,s)=-8(4-2\sqrt3)(4/\sqrt3-2)\,ts(t^2+s^2)
+O((|t|+|s|)^6).}\tag{3a}
\]

This has three distinct regimes. For \(s=0\), the interaction vanishes **exactly to all orders** by the stronger spectral-reflection symmetry (3). For \(ts>0\), it is negative (attractive connected shift); for \(ts<0\), it is positive. **The exact radiation-protecting parity remains conserved in all three cases.** Thus the interaction can be tuned continuously through zero and have its sign reversed without opening the symmetry-forbidden two-photon decay channel. A sign-reversed physical hopping is an additional control resource; none is assumed in the all-positive implementation §2.

An independent endpoint-resolvent computation at \(t=.20\), \(s=-.04,0,+.04\) gives the respective *finite-coupling* connected energies \(+0.0004178879439\), \(0\), and \(-0.0004178879439\). The complete pair energies remain in the global odd two-photon band and retain an even-continuum gap exceeding 0.96 in all three tests. See `astra_local_pair_interaction_tunability.py` and its JSON output. This is a controllable spectral principle, not an experimentally acquired attractive/repulsive gate.

## 6. Complete positivity and all-sector stability

The lower parity bath is gapless at zero, but its endpoint inverse-frequency form is finite: \(\langle0,h_-^{-1}0\rangle=2\). The upper band contributes \(\langle0,h_+^{-1}0\rangle=10-4\sqrt6\). The exact one-body zero-energy Schur matrix, in the two emitter parity sectors, is
\[
 \Gamma_+(0)=3-2g^2(10-4\sqrt6),\qquad
 \Gamma_-(0)=3-2g^2.
\]
For \(g\le0.4\), both are strictly positive (in particular \(\Gamma_-\ge2.68\)). Completing squares gives \(h_1(g)\ge0\). Second quantization preserves nonnegativity, and compressing to hard-core memory occupations preserves it in **each fixed particle sector, for all particle numbers**. This is all-sector *stability*, **not** the earlier negative-energy `-min(N,m)` storage-capacity theorem; the two statements have different energy interfaces.

## 7. Coherent CZ without a global two-particle gap

Use a mirror-symmetric, smooth, calibrated coupling ramp \(g(t)\) from 0 to a chosen \(g_0\le0.4\), hold at \(g_0\), and ramp back to zero. In the plus and minus **one-particle parity sectors**, the discrete emitter-derived eigenstates remain gapped from their respective continua. In the even **two-particle parity sector**, the embedded pair also remains isolated from its allowed continuum, even though odd two-photon states exist at the same total energy. The symmetric ramp commutes with parity throughout.

The standard gapped adiabatic theorem can therefore be applied **within each invariant symmetry sector**. There is no Berry rotation on the real normalized nondegenerate eigenbranches. One on–hold–off cycle produces phases \(\Phi_+,\Phi_-,\Phi_p\) to vanishing isometry error as its ramp is slowed.

At \(g=0\), apply the local memory pulse \(Z_L=e^{i\pi n_L}\), which swaps bare \(|e_+\rangle\) and \(|e_-\rangle\) and multiplies bare \(|LR\rangle\) by \(-1\). Repeat the same on–hold–off cycle, and apply \(Z_L\) again. The one-particle exchange phases now exactly refocus in the adiabatic limit, while the pair retains its nonlinear dynamical phase. Correcting the known single-memory phases gives
\[
 U_{\rm echo}\ \xrightarrow[\text{adiabatic ramps}]{}\
 \mathrm{diag}\left(1,1,1, e^{-2i\int\chi(g(t))dt}\right).
\]
Since \(\chi(g_0)\ne0\) (at least for sufficiently small positive \(g_0\)) the plateau duration can be tuned so that the fourth entry is \(-1\). Thus the model supports an *arbitrarily accurate, finite-duration* coherent CZ with no intrinsic even-sector pair radiation in the ideal symmetry-preserving Hamiltonian. Finite-duration switching errors are controlled by the positive **sector-specific** gaps, not by an assumed global gap. This theorem is qualitative in the adiabatic error constant; it does **not** certify a particular finite-\(g\) experimental fidelity.

The distinction from the earlier SSH CZ matters: the prior gate achieved vanishing error by taking \(g\to0\) despite a nonzero \(g^8\) linewidth. Here a nonzero \(g_0\) can be fixed first; ramp time can then increase while the pair stays an exact eigenstate. The symmetry-protected operation still requires engineered band separation, controllable coupling ramps, local pulses, and absence of parity-breaking environmental noise.

## 8. Executed independent checks and numerical scope

1. `astra_symmetry_filtered_embedded_pair.py`: computes complete one-body spectral measures of the two Jacobi parity channels (all finite-chain eigenstates retained), evaluates their exact two-boson resolvents and solves the hard-core pair eigenvalue. For \(g=.2,.15,.1,.08,.05,.03\), \(\chi/g^4\) approaches \(-0.4974226119\). The bare-pair overlap tends to one. These calculations use 256 bath sites per branch.
2. `astra_local_ladder_embedded_pair_audit.py`: builds the **connected rail ladder and two hard-core memories** directly, not the pre-separated parity model. At \(g=.1,.2,.4\), its finite-Fock pair eigenvalues and overlaps agree with the independent harmonic-mean resolvent to about \(10^{-12}\). The two-particle symmetry commutator is exactly zero for these integer/radical real couplings at floating-point precision.
3. `astra_symmetry_filtered_CZ_protocol.py`: numerically propagates both local one-excitation code columns and the **complete allowed two-particle Fock state** through two actual smooth ramps, static plateau evolution, and two local memory-echo pulses. At \(g=.4\), ramp duration 80, and 10 bath sites per rail, the executed full-code operator error is \(6.6384\times10^{-4}\) for a total time \(562.8\). This is a **finite-chain diagnostic**, not a rigorous continuum-state error certificate. A sweep of four ramp durations finds decreasing error.
4. `astra_band_filter_leakage_coefficient.py`: independently integrates the nonnegative leading on-shell convolution for a declared additional parity-preserving *wrong-band source* with relative amplitude \(\delta\). In this extension
\[
 c(\delta)=\frac{16}{9\pi^2}\delta^2,\qquad
 \chi(g,\delta)=-(3-2\delta^2)ab\,g^4+O(g^6).
\]
If the preceding resonance-convolution regularity assumptions are retained, its formal leading radiative amplitude coefficient is
\[
 \gamma(g,\delta)=\frac{16a^2}{9\pi}(3-2\delta^2)^2\delta^2\,g^8+o(g^8),
\]
so, as \(\delta\to0\), \(\gamma\sim(16a^2/\pi)\delta^2g^8\). The exact coefficient \(16/(9\pi^2)\) comes from a positive endpoint-density integral \(\int_4^6[\rho_+(E)/(E-3)^2]^2dE=16/(27\pi^2)\). The numerical quadrature matches that expression to machine precision. **This is a different perturbation from a mirror-asymmetric fabrication error**. It does not establish a lifetime or operational error for an actual mismatched ladder.
5. The own-rail-only equal-coupling case was independently diagonalized at 6, 10 and 18 sites per rail: the protected hard-core pair energy was 6 to \(2\times10^{-15}\), while the overlap remained nonzero. This checks the all-orders cancellation (3), independently of the perturbation theory.

## 9. A generalized symmetry-resolved sumset principle

Let a one-particle bath split into conserved parity bands with spectral supports \(A_+\) and \(A_-\) separated around a memory frequency \(\varepsilon\). Suppose (i) \(\varepsilon\) lies outside each band; (ii) even-parity two-particle continua \(A_++A_+\), \(A_-+A_-\), and the same-parity bound-plus-bath continua all avoid \(2\varepsilon\); (iii) the **opposite-parity** sum \(A_++A_-\) contains \(2\varepsilon\). Then a symmetry-even hard-core pair at energy \(2\varepsilon\) is isolated **in its symmetry sector** but embedded in the full two-particle spectrum. For sufficiently small bounded parity-preserving coupling, its isolated eigenbranch persists exactly. If the off-diagonal bath response and its derivative satisfy \(\Delta F\Delta F'\ne0\), the pair acquires a nonzero fourth-order connected interaction while remaining bound. This follows by Kato's isolated-eigenvalue perturbation theorem *within the symmetry sector*, plus the rank-two hard-core Schur identity.

A different necessary-and-sufficient criterion governs vanishing **leading-order** radiation in an *open* same-parity sector. Its leading coefficient is a sum of nonnegative convolutions
\[
 c=\frac12\sum_{\sigma=\pm}\int\nu_\sigma(E)\nu_\sigma(2\varepsilon-E)dE\ge0.
\]
Thus \(c=0\) iff the product of the opposite-energy spectral densities vanishes a.e. in **each parity channel**. Cancellation between channels cannot remove a strictly positive term. A *symmetry-sector spectral gap* (as in the ladder) is stronger: it removes the continuum channel over a neighborhood and gives an exact bound state, not merely a vanishing leading linewidth.

## 10. Physical limits and novelty boundary

The ladder is a declared number-conserving oscillator/qubit Hamiltonian, **not** a Maxwell-derived, measured waveguide. It needs both rail parity and a calibrated ratio of cross to direct memory–first-rung couplings. A conventional signal-and-loss environment can break the rail-exchange symmetry and immediately connect the pair to formerly forbidden odd two-photon channels. The wrong-band leakage coefficient in §8 is not a general tolerance against such errors. Time-dependent coupling controls, local echo phases and their finite power/noise costs remain unacquired. The global many-particle Hamiltonian remains semibounded, but the theorem is about two-memory nonlinear control, not an all-sector occupancy capacity law or a new force.

Symmetry-protected bound states in continua, spectral Green functions and photon-mediated effective spin interactions are established research directions. Relevant context includes Schrinski–Brimer–Sørensen (PRA 110, L041701, 2024), Tečer et al. (PRL 132, 163602, 2024), and the 2025 photonic BIC experiment (PRB 111, 075427). Priority of the specific combined theorem has **not** been established.

**Next real physics question:** determine how a *microscopically constrained, symmetry-breaking* radiation bath perturbs this exact embedded pair, ideally deriving an inclusive finite-\(g\) error law with separate energy-calibration, parity-breaking and source-preparation costs. An equally important alternative is realizing the parity-filtered bands in a circuit or Maxwell-compatible ladder rather than assuming their component Hamiltonian.
