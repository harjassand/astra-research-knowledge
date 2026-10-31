# Full-manifold pair response: closure, motion, and what detuning buys

Root-working complementary construction. This file preserves a microscopic finite-matrix calculation and several exact operator statements. It does not qualify a molecular device, a warm three-dimensional gas, or a spin-transparent cooling interface. All optical rates remain within their declared rotating-wave, weak-drive and finite-domain regimes.

The useful question is stronger than scalar single-atom polarizability: can a physical pair interaction act identically on every vector of a surviving nuclear-spin triplet, including its correlations with motion and retained apparatus, while a singlet-consuming branch remains strong?

The answer from the following model is that ordinary hyperfine closure alone does not provide that capability. It removes several low-order terms but leaves a definite pair tensor and, when the pair moves, a term linear in hyperfine coupling. A separate completeness cancellation also weakens the useful free-to-bound Raman amplitude. These are mechanism-specific obstructions, not universal impossibility theorems.

## 1. Established machinery and the comparison being made

Reiter and Sørensen's [effective-operator formalism](https://arxiv.org/abs/1112.2806) supplies the standard weak-drive elimination: an effective Hamiltonian and one effective jump for each physical output process. It is essential to retain the jumps individually; a scalar sum of their effects does not prove a spin-transparent instrument.

[Cavity-controlled ultracold chemistry](https://arxiv.org/abs/1803.10004) supplies a real theoretical cavity association/dissipation construction. Its selected-level model has an initial atom-pair state, an excited molecular state and a desired ground molecular state; the proposal explicitly assumes tight confinement and neglects external motion. Its cavity cooperativity is reduced by the molecular Franck–Condon factor, and its analysis includes the speed/efficiency tradeoff. It does not establish nuclear-spin opacity over a warm orbital domain.

Ground-electronic molecular association is established in [Sr2 STIRAP experiments](https://arxiv.org/abs/1205.4505), and Yb2 ground-state levels are characterized by [two-color spectroscopy](https://arxiv.org/abs/0708.0752). These results justify investigating a real final molecular state rather than inventing an output sink. They do not transfer a cold prepared motional state or a selected intermediate resonance into an arbitrary-orbital guarantee.

Interference among intermediate levels is established optical-control machinery, including the analysis of Raman gates in [Ozeri et al.](https://arxiv.org/abs/quant-ph/0611048). At extremely large detuning, photon-frequency dependence and counterrotating terms require care; [Moore et al.](https://arxiv.org/abs/2211.00744) show why a fixed-linewidth extrapolation can give false fundamental scattering floors. The laws below are finite-domain statements, not extrapolations to zero optical frequency or unlimited laser power.

## 2. What must factorize

Write an excited-manifold non-Hermitian generator as

\[
H_{\rm NH}=H_e-\frac i2\sum_\alpha C_\alpha^\dagger C_\alpha,
\]

where all quantities in this file are in angular-frequency units unless otherwise stated. A pump V_+ and physical decay outputs C_alpha produce

\[
H_{\rm eff}=-\frac12 V_-\left(H_{\rm NH}^{-1}
+H_{\rm NH}^{-1\dagger}\right)V_+,
\qquad
L_{\alpha,\rm eff}=C_\alpha H_{\rm NH}^{-1}V_+.
\]

The survivor requirement is a factorization on the protected triplet for every physical fine history. Neither a scalar H_eff alone nor a scalar total rate sum_alpha L_alpha†L_alpha is enough.

The executable includes an exact minimal example with a complete J=1,I=1/2 excited manifold. Ideal linearly polarized illumination gives a scalar total scattering effect to floating-point error below 4×10⁻²⁰. Nevertheless, conditioning on a photon while discarding its polarization changes the purity of a maximally entangled spin/reference input from one to approximately 0.92393. The fine Raman channels retain spin information. This verifies the distinction at the physical resolvent level rather than with an abstract POVM counterexample.

## 3. Complete Franck–Condon closure cancels the leading association amplitude

Consider ground relative-motion Hamiltonian H_g, an entrance state |a> and a desired bound state |f>, with <f|a>=0. In a Condon approximation the electronic dipole is independent of the relative coordinate, and the pump/Stokes spatial phases can be taken equal in the relative electric-dipole limit. For a complete excited vibrational basis {|m>}, the Raman amplitude includes

\[
\mathcal A_{fa}(\Delta)
=\sum_m\frac{\langle f|m\rangle\langle m|a\rangle}
{\Delta-E_m}
=\langle f|(\Delta-H_e)^{-1}|a\rangle.
\]

Completeness gives

\[
\sum_m\langle f|m\rangle\langle m|a\rangle=0.
\tag{1}
\]

Thus the leading 1/Delta term is absent. If H_e=H_g+V on a bounded admitted domain, then

\[
\mathcal A_{fa}(\Delta)
=\frac{\langle f|V|a\rangle}{\Delta^2}
+O(\Delta^{-3}).
\tag{2}
\]

For ||H_e||≤M<|Delta|, an explicit remainder after the displayed leading term is

\[
\left|\mathcal A_{fa}-\frac{\langle f|V|a\rangle}{\Delta^2}\right|
\le\frac{M^2}{|\Delta|^2(|\Delta|-M)}.
\tag{3}
\]

A less global exact identity is useful when V is only controlled on the states in question. If H_g|a>=E_a|a>, H_g|f>=E_f|f>, z=Delta+i gamma/2 and R=(z+E_a-H_e)^-1, then

\[
\langle f|R|a\rangle
=\frac{\langle f|V|a\rangle}
{z(z+E_a-E_f)}
+\frac{\langle f|V R V|a\rangle}
{z(z+E_a-E_f)}.
\tag{4}
\]

When the full resolvent norm is bounded by 1/d, the remainder is at most

\[
\frac{\|Vf\|\,\|Va\|}{|z|\,|z+E_a-E_f|\,d}.
\]

This connects to the earlier local-orbit approach: source/interaction norms on the actually accessed states can suffice, without bounding an unrelated entire reservoir Hamiltonian. It does not produce those norms for a singular contact potential by assumption.

The finite executable sums a complete six-state manifold. Its leading Franck–Condon sum is zero to 3×10⁻¹⁶; Delta² A_fa converges to the calculated matrix element V_fa=0.7. Keeping one of those same intermediate levels instead produces an apparent nonzero Delta^-1 term. This is a concrete failed truncation, not a small numerical adjustment.

### Full-manifold dark-state obstruction

Under the same constant-dipole completeness hypotheses, the excited-manifold images of |a> and |f> are orthogonal. The matrix with those two columns has two nonzero singular values. Hence no nontrivial superposition of |a> and |f> is dark to the entire manifold. Projecting onto a single excited level makes the matrix rank one and creates the familiar Lambda dark state.

This does not invalidate selected-level STIRAP. It identifies its required spectral isolation. With several warm entrance states and one final molecular state, a single instantaneous Raman row also has a kernel. Cooling, transport, resolved output modes or an observability argument must remove those orbital dark states; a scalar spin response does not do so by itself.

## 4. A complete 24-state electronic/nuclear pair model

Take two ground J=0 atoms with nuclear spins I_1=I_2=1/2. The one-electronic-excitation manifold consists of:

- the excited atom label, dimension two;
- its full J=1 Cartesian manifold, dimension three;
- both nuclear spins, dimension four.

The resulting excited space has dimension 24. This retains all electronic magnetic and nuclear components of the declared atomic manifold; it does not pretend to be the complete chemical molecular spectrum.

Let the Cartesian generators satisfy (J_a)_{bc}=−i epsilon_{abc}. Define

\[
F=\begin{pmatrix}
\mathbf J\cdot\mathbf I_1&0\\
0&\mathbf J\cdot\mathbf I_2
\end{pmatrix},\qquad
W(\mathbf n)=\begin{pmatrix}0&T(\mathbf n)\\T(\mathbf n)&0\end{pmatrix}
\otimes I_{\rm nuclear},
\]

\[
T(\mathbf n)=J_d(I-3\mathbf n\mathbf n^T).
\]

W is the standard near-field resonant electric-dipole exchange tensor in the one-excitation sector. Take real linear pump polarization epsilon and the normalized symmetric electronic drive

\[
D=\frac1{\sqrt2}\binom{\epsilon}{\epsilon}\otimes I_{\rm nuclear},
\qquad D^\dagger D=I.
\]

The optical response is

\[
\mathcal R(\Delta)=D^\dagger(\Delta-H)^{-1}D,
\quad H=W+AF
\]

for a stationary pair, or H=K+W+AF when orbital motion K is retained. A physical pump factor Omega²/4 multiplies the response in the light shift. The sign depends on the detuning convention and is irrelevant to the scalar/non-scalar conclusions.

For a ground operator X define its triplet non-scalar part by

\[
\mathcal N_t(X)=P_tXP_t-
\frac{I_t}{3}\otimes\operatorname{Tr}_t(P_tXP_t).
\]

Orbital/source operators are retained by this subtraction. It removes only an action common to all three triplet directions.

## 5. A stationary pair already has a definite fourth-order response defect

Choose n=z and epsilon=x. Expand

\[
\mathcal R(\Delta)=\sum_{j=0}^\infty
\frac{D^\dagger H^jD}{\Delta^{j+1}}.
\]

The triplet non-scalar parts vanish for j=0,1,2. At j=3, the term proportional to A² J_d is

\[
D^\dagger(WF^2+FWF+F^2W)D
=J_d\left[I-2I_{1y}I_{2y}+I_{1z}I_{2z}\right].
\tag{5}
\]

Its triplet non-scalar norm is 5|J_d|/6. Therefore

\[
\|\mathcal N_t(\mathcal R)\|
=\frac{5A^2|J_d|}{6|\Delta|^4}+O(|\Delta|^{-5}).
\tag{6}
\]

The useful physical interpretation is two hyperfine insertions and one interatomic exchange. Ground J=0 eliminates the direct first-order nuclear dependence; it does not eliminate this pair interaction. The term is not merely a singlet/triplet energy difference: it splits triplet directions.

For A=0.2,J_d=1 the executable finds the coefficient 0.0333333 and checks the Delta^-4 convergence using the inverse of the full 24×24 matrix.

### Why a coarse detuning interval cannot make this exactly scalar

Each finite-dimensional response matrix element is analytic away from its poles. If the triplet non-scalar response vanished on a real open interval not containing a pole, analytic continuation would make its Laurent coefficients vanish. Equation (5) contradicts that condition. Thus this primitive does not become exactly triplet-scalar over any open detuning interval. Isolated cancellations, additional controls and finite-accuracy regimes remain possible.

## 6. Motion introduces a term linear in hyperfine coupling

The static first-order cancellation cannot simply be applied to a moving pair. Let W depend on the orbital configuration and let K couple different configurations. Assume for this derivation that F is independent of the configuration, so [K,F]=0, and that D has a fixed real polarization. Define

\[
B=D^\dagger W F D.
\]

For the stated real dipole tensor, B is anti-Hermitian. The single-hyperfine part of the cubic response coefficient includes the six permutations of K,W,F. Using D†FD=0 and D†FW D=−B gives exactly

\[
\sum_{\text{one }K,W,F}D^\dagger(\cdots)D
=[B,K].
\tag{7}
\]

The commutator is Hermitian. It produces

\[
\mathcal R_{\rm motion,spin}(\Delta)
=\frac{A[B,K]}{\Delta^4}+O(\Delta^{-5}).
\tag{8}
\]

In a continuum model this is the expected nuclear-spin/orbital-motion coupling generated by spatially varying electronic response. Its finite-dimensional version is enough to refute a general frozen-pair inference.

### Exact two-configuration witness

Take configurations n=z and n=x, real polarization epsilon=(x+z)/sqrt(2), and orbital coupling K=k sigma_x. Direct calculation gives

\[
B=\frac{3iJ_d}{4}\,\sigma_z\otimes I_{{\rm tot},y},
\qquad
[B,K]= -\frac{3J_dk}{2}\,
\sigma_y\otimes I_{{\rm tot},y}.
\tag{9}
\]

It vanishes on the nuclear singlet but acts nontrivially on the triplet and entangles it with orbital motion. For k=0.3,J_d=1 the coefficient norm is 0.45. The 48-state executable verifies the cubic coefficient identity to 8×10⁻¹⁶ and the corresponding Delta^-4 response scaling.

This is precisely a failure that can preserve a parity label while damaging the quantum information that should survive inside its sector.

### Coarse bounds and domain limitations

On a genuinely admitted finite domain, ||W||≤W_max and ||K||≤E_max give

\[
\|A[B,K]\|\le2|A|W_{\max}E_{\max},
\]

using ||F||=||D||=1. The two-hyperfine/one-exchange cubic terms are bounded by 3A² W_max. A bounded full H with norm M admits an explicit Neumann remainder after the cubic moment of at most

\[
\frac{2M^4}{|\Delta|^4(|\Delta|-M)}
\]

after triplet scalar subtraction. These are sufficient mathematical bounds, not fitted residuals.

The physical dipole tensor behaves as r^-3 before molecular corrections. A low kinetic-energy promise alone does not bound it at contact or justify a finite orbital projection. Actual molecular response requires a qualified spectral/resolvent domain or controlled local moments such as those in (4), including tails into omitted channels. Neither a cold 3D cloud nor low transverse occupation automatically constrains the interatomic direction at short range to one axis.

## 7. A possible leading-order repair has a sharp geometry limitation

Let M be a real symmetric polarization covariance, representing positive sums of independent linear-polarization intensities in the coherent light shift. For the two-hyperfine/one-exchange contribution, its nuclear-spin tensor is, up to a spin-scalar part,

\[
N(M,T)=-\operatorname{Tr}(M)T+MT+TM
\]

when Tr(T)=0. More completely it includes −Tr(MT)I, which is isotropic in nuclear-spin indices and therefore harmless within a triplet.

For a fixed axis n=z, the leading anisotropy vanishes when

\[
M\propto\operatorname{diag}(1,1,4).
\tag{10}
\]

This is a real leading-order cancellation, stronger than simply making the light unpolarized. It is not a complete optical instrument: higher response moments and distinct spontaneous-emission channels remain.

The same fixed polarization mixture cannot cancel the term for two orthogonal interatomic axes. For n=z, off-diagonal isotropy conditions force M_xy=M_xz=M_yz=0, while diagonal conditions require M_x=M_y and M_z=4M_x. For n=x they require M_y=M_z and M_x=4M_y. Together these imply M=0. Thus no nonzero fixed covariance can make this leading pair tensor scalar over a domain containing both axes.

The code verifies the fixed-axis cancellation and the full-rank two-axis constraint. A true narrow-axis molecular geometry could exploit (10), but supplying that geometry at the contact radius is an independent confinement problem. It cannot be inferred from warm motion in a one-dimensional effective trap. This is a possible material/geometric repair to investigate, not a supplied device interface.

## 8. Useful association and error are co-suppressed in a fixed-cavity closure limit

Let B_fa=<f|V|a> be the spatially varying matrix element that survives the closure cancellation, g a fixed vacuum Stokes coupling, Omega_p the pump Rabi scale and kappa the cavity photon-population decay rate. In a weak, off-resonant, bad-cavity model,

\[
G_{fa}\simeq\frac{\Omega_p g B_{fa}}{2\Delta^2},\qquad
\Gamma_{\rm assoc}\simeq\frac{4|G_{fa}|^2}{\kappa}
=\frac{\Omega_p^2g^2|B_{fa}|^2}{\kappa\Delta^4}.
\tag{11}
\]

Nuclear Raman scattering has the form

\[
R_R=C_R\frac{\Gamma_A\Omega_p^2 A^2}{\Delta^4},
\]

with C_R supplied by the actual angular matrix. The pair anisotropic light-shift scale is Omega_p² A² J_d/(4Delta⁴), with the warm commutator correction in (8) as an additional term. Therefore in this model

\[
\frac{R_R}{\Gamma_{\rm assoc}}
\simeq C_R\frac{\Gamma_A\kappa A^2}{g^2|B_{fa}|^2},
\qquad
\frac{\delta H_{\rm pair}/\hbar}{\Gamma_{\rm assoc}}
\sim\frac{\kappa A^2J_d}{4g^2|B_{fa}|^2}.
\tag{12}
\]

The detuning cancels. Meanwhile leading scalar Rayleigh scattering is proportional to Omega_p²/Delta², so its number per successful association grows as Delta². It may be spin-transparent, but its momentum/entropy cost is real.

This is why a complete-manifold calculation must compare useful and damaging responses together. It is not a universal cavity limit: another final-state matrix element, non-Condon dipoles, spatially structured fields, additional control couplings or a different domain can change the scaling.

### Warm bandwidth competes with cavity enhancement

With the population-decay convention above, the cavity rate has the Lorentzian factor

\[
\frac{1}{1+(2\delta/\kappa)^2}.
\]

Maintaining at least a fraction eta of the resonant rate over |delta|≤W requires

\[
\kappa\ge2W\sqrt{\frac{\eta}{1-\eta}}.
\tag{13}
\]

At fixed g, increasing kappa reduces the enhancement in (11). A frequency sweep, several modes, or sideband-resolved output can alter the tradeoff, but supplies extra time, controls or mode resources. The literature cavity paper uses a field-amplitude decay convention; its kappa is half the population decay used here. Their factors must not be mixed.

## 9. Ground-molecule parity is a useful alternative, with remaining costs

A target ground-electronic homonuclear molecular state with even rotational parity gives a genuine selection principle. Two electric-dipole interactions preserve the relevant ground spatial parity in the relative long-wavelength limit. For identical I=1/2 fermions in the same ground electronic state, nuclear singlet and triplet occupy even and odd relative spatial parity respectively. A selected even ground molecular output can therefore be a singlet-consuming channel without using excited hyperfine splitting as the discriminator.

This is stronger than asking a nearby lossy excited line to distinguish nuclear spin. It still does not make the virtual triplet response scalar, and the final branch must be physically removed or flagged. Relative optical gradients, finite photon momentum, other multipoles and a non-spin-scalar trap require their actual bounds. A molecule's localized final wavefunction can supply finite relative-coordinate moments for such bounds; the warm input alone cannot.

A classical two-photon scheme can evade the fixed-vacuum-coupling scaling in (12) by increasing both classical Rabi amplitudes with detuning. In the closure model, Omega_p and Omega_s proportional to Delta can retain a finite useful coupling while some spin errors fall as Delta^-2. This costs optical power proportional to Delta² in each beam, leaves finite scalar scattering, and still needs a dissipative molecular outlet and a way to empty warm orbital dark states. It is a possible change of apparatus, not a free detuning cure.

## 10. Source-unit correction retained

The primary Yb spectroscopy source [arXiv:0708.0752](https://arxiv.org/abs/0708.0752) reports the 171Yb ground-state scattering length as −0.15(19) nm. The previously used optical-Feshbach paper's prose is retrieved as −0.15 a0. These units are inconsistent; the spectroscopy value must govern unless a separately justified conversion or revised measurement is supplied.

This does not change the earlier calculated imaginary scattering length or PA loss rate. At the illustrative 100 kHz harmonic point, the central value can produce a real singlet contact shift on the order of −3.1×10³ s⁻¹. It is a singlet scalar/resonance issue in direct absorption, but it cannot be omitted from a reused charge-star detuning box. The quoted uncertainty is also substantive.

## 11. Consequence

The completed calculation identifies a specific reason to avoid treating single-atom scalar response as a warm pair interface. The first nontrivial pair moment contains both an anisotropic nuclear tensor and a motion-dependent spin term. The same completeness operation that suppresses spin sensitivity can suppress the useful association amplitude. Neither a four-line sum nor a scalar rate effect repairs these facts.

The most constructive molecular alternatives are final-state parity selection, a physically constrained molecular axis with correctly balanced polarizations, or an actual multichannel Raman source whose two classical controls and output sink are counted together. None has yet supplied a complete state-uniform source/instrument cycle. Moving the main capability to an already supplied longitudinal QND interface is therefore a justified architectural choice, while these pair results remain useful mechanism-specific theory.

`pair_response_checks.py` and `pair_response_results.json` preserve the complete finite matrices, closure sum, dark-state rank, fixed-pair tensor, warm commutator identity, polarization geometry limitation, scalar-effect failure and relative cavity scalings. Numerical checks are ordinary floating-point checks; the identities and bounds above state their mathematical content and physical limits.
