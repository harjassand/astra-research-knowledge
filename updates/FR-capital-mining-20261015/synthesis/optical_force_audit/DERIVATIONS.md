# Electrodynamic and structural derivations

15 October 2026. Independent internal audit, not external validation. Historical originality UNKNOWN. These are conditional results with explicitly specified optical and structural models. No laboratory response, hot material parameters, useful transformation, or industrial advantage was acquired.

## 1. What the source pressure actually assumes

Let true inversion-related variants have bulk response `chi_s^(2)=s chi_0^(2)`, `s=±1`, in the same laboratory axes. This relation must be checked for the actual APB; the name “antiphase domain” alone does not establish it. The linear responses can agree while the third-rank response changes sign. Let a scalar contraction of that tensor be real, local, instantaneous and weak enough for perturbation theory. At a prescribed electric field the nonlinear contribution to the effective material potential is

\[
f_s(E)=-\epsilon_0s\chi_{\rm eff}^{(2)}E^3/3.
\]

This is a fixed-field effective potential, not the complete stored electromagnetic/material energy of a driven dispersive system. With peak fields `E1,E2`,

\[
E(t)=E_1\cos\omega t+E_2\cos(2\omega t+\phi),\qquad
\overline{E^3}=\tfrac34E_1^2E_2\cos\phi,
\]

so

\[
f_s=-s h\cos\phi,\quad h=\epsilon_0\chi_{\rm eff}^{(2)}E_1^2E_2/4,
\quad p_0=2h.
\]

Positive pressure is defined to expand `s=+1`. The source's prefactor is consistent with these assumptions; this audit does **not** identify an algebraic error in it. An absorption/injection coefficient alone does not supply this conservative potential. Nor does an arbitrarily chosen real room-temperature SHG coefficient certify a hot, carrier-loaded, moving-wall force.

For dispersive transparent normal modes the safe reduced model is a calibrated Hermitian interaction

\[
H_{\rm int}=\hbar[g(X)b^\dagger a^2+g(X)^*b(a^\dagger)^2],\qquad
F_X=-2\hbar\operatorname{Re}[g'(X)\beta^*\alpha^2].
\]

The modes must be normalized by their full dispersive field-plus-material energy, with their actual hot optical boundary conditions. The force is a partial derivative at fixed canonical optical state; it is not the total derivative of the energy after replacing the amplitudes by arbitrary steady-state functions of `X`. Driving, damping and changes of the optical state must then be evolved separately. If linear mode frequencies also depend on wall position, the ordinary term `-hbar sum_j omega_j'(X) Nj` and any dissipative-coordinate forces must be included; equality of the ideal bulk variants' linear response does not remove an APB's own localized response. Quesada–Sipe's nonlinear quantization analysis is a relevant warning about canonical variables, not a proof that this fixed-field source formula is wrong. [Primary paper](https://opg.optica.org/ol/abstract.cfm?uri=ol-42-17-3443).

## 2. Exact wall-overlap pressure and thickness cancellation

Assume prescribed, undepleted forward fields. Absorb the real tensor contraction and amplitude product into `h(r)≥0`; write the relative phase as `Phi+q·r`, with `q=2k_omega-k_2omega` (changing this convention only reverses phase signs). The interaction is

\[
U[s]=-\int s(\mathbf r)h(\mathbf r)
       \cos(\Phi+\mathbf q\!\cdot\!\mathbf r)\,dV.
\]

For a wall whose positive-variant side expands with normal displacement `delta X`, its virtual-work pressure is

\[
p(\mathbf r)=2h(\mathbf r)\cos(\Phi+\mathbf q\!\cdot\!\mathbf r).
\]

The generalized force on **rigid translation of the entire wall** is the surface integral of this pressure. For a rectangular uniform wall of tangent lengths `L1,L2` and normal position `X`,

\[
\frac{F_X}{A}=p_0\prod_{j=1}^2
\operatorname{sinc}(q_{tj}L_j/2)
\cos(\Phi+q_nX+\mathbf q_t\!\cdot\!\mathbf r_c),
\quad \operatorname{sinc}x=\sin x/x.
\]

**Consequences.** A tangent direction spanning an integer beat length `2pi/|q_t|` has exactly zero net force in this uniform lossless model, for every externally set phase. An infinite flat wall has zero mean pressure if there is any nonzero tangent mismatch. A finite thin wall can survive this restriction. Net-force cancellation does not imply every patch of a flexible wall is stationary: opposite local pressures can bow it or write different polarities at different depths.

In a film, if the wall spans `0<z<d`, the two internal intensity attenuation coefficients are `alpha1,alpha2`, and no reflections or depletion occur, the normalized overlap is

\[
W(d)=\frac1d\int_0^d e^{-az+iq_zz}dz
=\frac{1-e^{-(a-iq_z)d}}{d(a-iq_z)},\qquad
a=\alpha_1+\alpha_2/2,
\]

\[
\bar p=p_0\operatorname{Re}[e^{i\Phi}W(d)],\qquad
|\bar p|\le p_0|W(d)|\le p_0\frac{1-e^{-ad}}{ad}\le p_0.
\]

At `a=0`, `W=exp(i q_z d/2) sinc(q_z d/2)`. At nonzero attenuation the exact sinc zeros generally lift; that does not restore a uniformly driven thick volume. Standing waves, multiple reflections, changing tensor projections and pump depletion require their measured complex overlap instead of this forward-wave formula.

Using **only** Skauli et al.'s original 22 °C dispersion fit, the fundamental/SH pair 2.3/1.15 µm has `Lc=pi/|q|≈5.01 µm`, while 4.6/2.3 µm has `Lc≈40.97 µm`. The corresponding uniform 400 nm overlap magnitudes are 0.99738 and 0.99996. Therefore this propagation theorem is **not** a demonstrated cancellation of the proposed 400 nm film. The fit's temperature measurements extend only to 95 °C; no 650 °C refractive index is extrapolated here. [Original author-uploaded paper, Eq.13/Table II](https://www.researchgate.net/publication/241151797_Improved_dispersion_relations_for_GaAs_and_applications_to_nonlinear_optics).

For common external propagation directions on a planar film, tangential wavevector conservation can make the in-plane components of `q` zero even when the internal normal components differ. A lateral wall can then see position-independent average pressure while the phase varies through its thickness. The theorem must be applied using the wall orientation, not simply the optical path length.

## 3. Fixed-phase drift obstruction and a conditional moving-phase alternative

If mismatch projects onto the direction of wall motion, `q_n!=0`, and the tangent overlap remains fixed, write

\[
p(X)=P\cos(q_nX+\Phi),\qquad
U(X)/A=-P\sin(q_nX+\Phi)/q_n.
\]

Then

\[
\int_X^{X+2\pi/|q_n|}p(x)dx=0.
\]

A static optical phase thus creates a periodic potential, not an indefinitely directed bulk pressure. Under deterministic isothermal gradient motion `Xdot=M p(X)`, with positive mobility and no other force, the wall approaches a stable zero of the force rather than traversing repeated cells. Thermal detailed balance in this static periodic potential likewise gives no stationary directed current. Depletion, spatial temperature variation, nonthermal carriers, radiation recoil or moving phases can escape this narrow result and must be accounted for as different driven mechanisms.

A useful mechanism mutation is to translate the phase pattern: `Phi(t)=-q_n v t`. With `eta=q_n(X-vt)`,

\[
\dot\eta=q_n[MP\cos\eta-v].
\]

For positive `q_n`, a stable locked solution exists if `|v|<MP`; choose the root with `sin eta>0`. It advances a **freely moving** wall at the programmed speed. The input sources supply power `F v` and all loss. The experiment would compare positive/negative phase-ramp velocity and zero-ramp controls, with independently measured optical overlap and temperature/carriers. This is a conditional optical conveyor interpretation; moving optical potentials are established physics and historical originality of this APB application is UNKNOWN. It removes the static-phase travel restriction, not pinning, absorption, tensor zeros, duty-cycle limits or retention obligations. It is unnecessary when `q_n=0` and a uniform pressure is already available.

For an ideal thick one-dimensional system with `f=-h s(z) cos(qz)`, minimizing local optical energy instead favors `s(z)=sign cos(qz)`. Over an integer number of periods this pattern gains `2h/pi` energy per volume but introduces `|q|/pi` walls per length. With constant wall energy `gamma`, it beats a uniform variant only when

\[
p_0=2h>\gamma |q|.
\]

Hence domain inversion used to quasi-phase-match the optical coupling is not an independent free resource while those same domains are being removed. A static mismatched field can favor a periodic polarity pattern rather than a uniform selected bulk polarity. This comparison assumes sharp freely creatable walls, fixed field and isotropic wall energy; it is not a hot-GaAs nucleation prediction.

## 4. SHG backaction, no-seed symmetry and energy balance

For the closed resonant three-wave interaction,

\[
\dot\alpha=-i2g^*\alpha^*\beta,\qquad
\dot\beta=-ig\alpha^2.
\]

Set `Z=g beta* alpha^2`. Direct calculation yields

\[
\dot N_a=-4\operatorname{Im}Z,\qquad
\dot N_b=2\operatorname{Im}Z,\qquad
\frac d{dt}(N_a+2N_b)=0.
\]

Conservative force samples a real quadrature; frequency conversion samples an imaginary quadrature. Zero **instantaneous** conversion is therefore compatible with nonzero force. It does not provide sustained uncharged work: amplitudes/phases or coupling energy change, and a driven steady state must supply mechanical work and dissipation. For a stationary apparatus a complete energy boundary is

\[
\frac d{dt}(U_{\rm optical+material}+E_{\rm mechanical})
=P_{\rm drive}-P_{\rm outgoing}-P_{\rm absorbed}.
\]

For a closed cycle returning both mechanics and all optical/material states, net delivered work is bounded by supplied work minus losses. There is no new energy source.

For a cavity with an undepleted fundamental and **no independent SH seed**,

\[
\beta=-ig\alpha^2/(K-i\Delta_2),\qquad K=\kappa_2/2.
\]

For real `g,g'`,

\[
F_X^{\rm self}=-\frac{\hbar|\alpha|^4\Delta_2}
{K^2+\Delta_2^2}\,\partial_X|g|^2.
\]

This force is zero on SH resonance in this real-overlap limit and is invariant under global inversion `g,g' -> -g,-g'`. More generally the full unseeded equations are covariant under `g -> -g, beta -> -beta`, leaving the force unchanged even with pump depletion. Complex overlaps can carry recoil forces, but the same global parity remains. A target crystal's **own** generated harmonic cannot by itself supply an independently chosen polarity reference. A separately phase-locked injected SH field can do so; its cross term is odd under seed phase reversal while the self-generated contribution is even. This is a design restriction, not a falsifier of the source, which explicitly supplies both colors.

## 5. Same-temperature spectral compatibility

Panish–Casey's published absorption measurements cover GaAs from 300 to 973 K and give

\[
E_g(T)=1.522-5.8\times10^{-4}T^2/(T+300)\quad{\rm eV}.
\]

At `T=923.15 K` (650 °C), `Eg≈1.11790 eV`. This is within their measured range, though it is an old bulk fit rather than a calibrated capped-film gap. The publisher-deposited abstract was fetched through Crossref; the full paper could not be fetched. [Primary DOI](https://doi.org/10.1063/1.1657024).

Let `epsilon=hc/lambda_omega`. For a two-color actuator the relevant electronic thresholds include:

| Channel | Minimum final photon energy | To be below the direct-gap threshold at 650 °C |
|---|---:|---:|
| SH linear absorption; fundamental 2PA | `2 epsilon` | `lambda_omega > 2.218 µm` |
| Mixed-color 2PA; fundamental 3PA | `3 epsilon` | `lambda_omega > 3.327 µm` |
| SH 2PA | `4 epsilon` | `lambda_omega > 4.436 µm` |
| SH 3PA | `6 epsilon` | `lambda_omega > 6.655 µm` |

These are **kinematic channel screens**, not absorption coefficients, selection-rule proofs or measured hot attenuation. Being below threshold does not remove defect, free-carrier, phonon-assisted or higher-order absorption. Being above it does not give a rate without matrix elements and material populations.

The room-temperature 1.8/0.9 µm cavity precedent's SH crosses this fitted gap around 151.6 °C, so its cold “below-gap SH” premise cannot be used at 650 °C. For 2.3/1.15 µm, the SH is only about 39.8 meV below the fitted hot gap, while mixed-color 2PA and SH 2PA remain energetically open. Considering only the fundamental's room-temperature 3PA coefficient leaves those lower-order two-beam channels unqualified. Experimental nondegenerate 2PA in GaAs is established independently; its hot coefficients are not imported from a different diode or quantum well. [Cold cavity paper](https://doi.org/10.1021/ph500054u), [primary GaAs nondegenerate 2PA experiment](https://photonics.umd.edu/pubs/ja-30/).

## 6. Root topology, capillarity and why surface disappearance can mislead

Suppose a film-spanning wall has fixed substrate root `X(0)=0`, free top at `z=d`, isotropic positive wall tension `gamma`, uniform pressure `p`, and no interface registry change. Its energy per transverse length is

\[
\mathcal E[X]=\gamma\int_0^d\sqrt{1+X'(z)^2}\,dz
-p\int_0^d X(z)\,dz.
\]

The Euler–Lagrange equation and natural free-top condition give

\[
\frac{X'}{\sqrt{1+X'^2}}=\frac p\gamma(d-z),\quad X'(d)=0.
\]

For `r=|p|d/gamma<1`,

\[
X(d)=\frac\gamma p[1-\sqrt{1-(pd/\gamma)^2}]
=\frac{pd^2/\gamma}{1+\sqrt{1-r^2}}
\simeq\frac{pd^2}{2\gamma}.
\]

The last rationalized form is numerically stable. The root remains present regardless of apparent surface progress. At `|p|d/gamma>=1` this graph-equilibrium solution fails; that failure alone neither proves depinning nor authorizes an interface reconstruction. A rooted APB cannot be erased through the whole film while its root boundary condition is held fixed. Contact-line motion, root release or an annihilation path is an additional structural process.

Rubel–Baranovskii's relaxed static DFT result `gamma_{110}=28 meV/Å²≈0.44861 J/m²` supplies a **normalization**, not a measured 650 °C wall tension/stiffness. With it, source pressure 442.7 Pa in a 400 nm film gives only 0.07895 nm of free-top bow; the source's largest example 11.95 kPa gives 2.132 nm. An anisotropic wall uses its orientation stiffness, which must be measured in the operating regime. [Primary paper, Table 1](https://www.mdpi.com/1422-0067/10/12/5104).

For a cylindrical selected-polarity island spanning a film, curvature competes as

\[
\mathcal E(R)=2\pi R d\gamma-\pi R^2d p,\qquad
\dot R=M(p-\gamma/R).
\]

Phase reversal cannot reverse the direction of radius drift if `|p|<gamma/R`; both phases still shrink the island. The same static DFT normalization and middle source pressure give `Rc=gamma/p≈1.013 mm`, far above a micrometer island. This is not an acquired hot critical radius; the exact same-regime falsifier is the **measured** inequality `p_max R < gamma_hot` in this model. A flat unrooted wall avoids this capillary threshold but still needs acquired mobility/pinning and retained exit behavior.

## 7. Coupled loss, carriers, timing and a constrained beam ratio

At a fixed measured state, the phase-even channel contributions can be organized as

\[
q_{\rm even}=a_1 I_1+a_2 I_2+b_{11}I_1^2+b_{12}I_1I_2+b_{22}I_2^2
+\sum c_{ijk}I_1^iI_2^j+q_{\rm FCA}.
\]

The full loss can additionally contain coherent interference terms such as `q_Phi=2 Re[D E2* E1²]`, plus propagation-mediated changes of absorption. Those signed terms must be combined with their underlying pathways so the total passive absorption remains nonnegative; they must not be assigned independent favorable values. Coefficients depend on temperature, carrier populations, optical polarization, spectrum, defect state and the boundary. Carrier generation must be computed channel by channel using the corresponding absorbed photon energy, rather than equating a carrier percentage with a lattice-heat percentage. Temperature, carriers, detuning, optical overlap and wall kinetics must all evolve together.

Even in a linear-loss-only comparison at a fixed state, equal beams are not generally optimal. Since `p=A I1 sqrt(I2)`, maximizing pressure for prescribed `a1 I1+a2 I2=Q` gives

\[
a_1 I_1=2a_2 I_2,\qquad I_2/I_1=a_1/(2a_2).
\]

The optimal split depends on measured losses; it does not allow assigning each beam a favorable coefficient. Nonlinear or mixed absorption changes the optimum and the carrier/thermal state changes with the split.

For time-varying illumination in the simplest overdamped wall law,

\[
\Delta X=\int M[T(t),n(t),X(t),\ldots],p(t)\,dt.
\]

Only constant mobility and temperature permit replacing this by `M D p_peak t`. The source's 100 fs/1 MHz duty penalty is correct in that specified linear regime. Pulsed thermal activation can alter the weighting but must be measured in the same specimen.

If phase jitter is independent and Gaussian with variance `sigma_Phi²`, the mean conservative drive is reduced by `exp(-sigma_Phi²/2)`. Group-velocity walkoff changes the pulse product itself: for field-amplitude Gaussian widths `tau1,tau2`, the normalized time overlap at differential delay `delta` is `exp[-delta²/(tau1²+2 tau2²)]`. Optical phase lock, pulse overlap and hot phase matching are separate obligations.

All calculations in `calculate.py` verify these explicit identities/normalizations only. They do not close N821's physical acquisition gates.
