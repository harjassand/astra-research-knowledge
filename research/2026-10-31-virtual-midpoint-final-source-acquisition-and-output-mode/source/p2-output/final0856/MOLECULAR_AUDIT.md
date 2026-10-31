# Molecular pair absorption: protected final channel, complete virtual manifold

Root-working complementary audit, 31 October 2026. This preserves a concrete
microscopic calculation, two useful structural statements and the failed
shortcuts. It is not a qualified Yb device, a new experimental result, or an
all-orbital loss guarantee. The stronger moving-pair and fixed-cavity analysis
is preserved separately in [the pair-response derivation](../pair_response/DERIVATION.md).

## 1. The useful capability and its complete instrument

The intended capability is a reusable singlet/triplet measurement of two
identical spin-1/2 carriers. A conclusive singlet branch may consume the pair
and reload a genuine fresh singlet; every surviving triplet history must
preserve all three triplet amplitudes and their external correlations. A
correct population label or scalar total scattering effect does not establish
that property. In the ideal factorized setting, consumption and renewal have
fine operators

\[
K_h=|\mathrm{vac}\rangle\langle s|\otimes F_h,\qquad
R_k=|s\rangle\langle\mathrm{vac}|\otimes G_k,
\]

and therefore \(R_kK_h=P_s\otimes G_kF_h\). The original carriers need not
survive the rank-one outcome. The triplet cannot be replaced this way.

Here the physical question is whether real optical association and molecular
removal supply those operators, with spin-transparent no-loss histories,
over the same admitted orbital/source domain used by cooling and return.
The arbitrary retained source is distinct from laser coherence, initially
empty output radiation, cold particle reservoirs and a molecular disposal
channel. Those latter resources must actually be supplied.

## 2. A real final-state selection principle

Take identical fermionic atoms with ground electronic angular momentum J=0
and nuclear spin I=1/2. In that electronic manifold, antisymmetry decomposes
the two-body Hilbert space as

\[
(V_0\otimes\mathcal H_{\rm even})\oplus
(V_1\otimes\mathcal H_{\rm odd}).
\]

The spin singlet has even relative spatial parity; the spin triplet has odd
relative parity. Consider a chosen ground-electronic homonuclear
\(X\,{}^1\Sigma_g^+\) molecule with rotational N=0. Its nuclear state is the
unique I=0 singlet. In the relative electric-dipole approximation, a two-E1
Raman transition preserves the relevant ground-state spatial parity. If the
intermediate Hamiltonian preserves that parity, arbitrary hyperfine mixing
inside that Hamiltonian does not change the selection rule. Thus the
amplitude from an incoming triplet to this chosen molecule vanishes.

This is a statement about a selected final channel. It does not require
excited hyperfine splitting to distinguish the incoming spin. It also does
not establish a quiet surviving triplet. In particular:

- Odd-rotation, I=1 ground molecules are physical channels. Two-E1 association
  can connect an odd entrance wave to them. A generic device that removes
  every molecule therefore need not be a singlet-only sink. Their transition
  amplitudes need real spectral detuning, resolved controls, or state-selective
  removal. The relevant gaps and time are not supplied by the parity label.
- Unobserved virtual light shifts and spontaneous Raman photons can disturb
  the triplet even if no triplet reaches the chosen target molecule.
- Relative optical gradients, finite photon momentum, higher multipoles and
  parity-breaking external potentials require their own matrix-element and
  exposure bounds. A long-wavelength statement is not an arbitrary spatial
  domain guarantee.
- Coherent association is reversible. A molecule must actually leave, be
  transferred into an outgoing spin-zero mode, or be irreversibly flagged.
  Reverse association, recapture and product branching belong in the cycle.
- A single target state does not remove every warm even orbital dark state.
  Cooling or another supplied observability/progress mechanism is still
  necessary. Fine spin opacity and orbital progress are separate conditions.

Ground-electronic Yb2 association is a credible spectral starting point:
[Kitagawa et al., PRA 77, 012719 (2008)](https://doi.org/10.1103/PhysRevA.77.012719)
measured bound levels through two-color spectroscopy across Yb isotopes.
That spectroscopy does not provide a warm state-uniform Raman-transfer rate
or the final molecular outlet. Its 171Yb scattering length is
\(-0.15(19)\,\mathrm{nm}\), not \(-0.15a_0\); see the
[NIST primary publication record](https://www.nist.gov/publications/two-color-photoassociation-spectroscopy-ytterbium-atoms-and-precise-determinations-s).

## 3. Complete Franck–Condon closure changes the useful rate

Let \(|i\rangle\) and \(|f\rangle\) be orthogonal entrance and bound
eigenstates of the same ground relative Hamiltonian \(H_g\). In a Condon
approximation, the electronic dipole is independent of relative coordinate.
Take matched relative optical phases and retain a complete excited
vibrational manifold with Hamiltonian \(H_e=H_g+W\). The two-photon spatial
matrix is

\[
\mathcal A_{fi}(z)=\langle f|(z-H_e)^{-1}|i\rangle.
\]

On a bounded admitted domain with \(|z|>\|H_e\|\),

\[
\begin{aligned}
\mathcal A_{fi}(z)
&=\frac{\langle f|i\rangle}{z}
+\frac{\langle f|H_e|i\rangle}{z^2}+O(|z|^{-3})\\
&=\frac{\langle f|W|i\rangle}{z^2}+O(|z|^{-3}).
\end{aligned}
\tag{1}
\]

The nominal inverse-detuning term vanishes by completeness. Writing
\(h=\|H_e\|\), a direct bound is

\[
\left|\mathcal A_{fi}(z)-\frac{W_{fi}}{z^2}\right|
\le\frac{h^2}{|z|^2(|z|-h)}.
\tag{2}
\]

For unbounded continua, the exact resolvent identity and local matrix-element
bounds in the companion derivation are the proper replacement. Merely
truncating a singular molecular potential does not earn (2).

Equation (1) has explicit exceptions. Non-Condon dipole variation, unequal
relative optical phases or different electronic ground potentials can give
a nonzero leading matrix element of the product of the dipoles. Those are
physical changes to calculate. The invalid step is to retain an isolated
line's \(1/\Delta\) Raman rate while simultaneously invoking cancellation
over the whole manifold for spin protection.

### A full-manifold dark-state rank obstruction

For a complete orthonormal excited basis \(\{|e_n\rangle\}\), define

\[
u_n=\langle e_n|i\rangle,\qquad v_n=\langle e_n|f\rangle.
\]

Completeness gives \(u^\dagger v=0\) and \(\|u\|=\|v\|=1\). With nonzero
pump and Stokes amplitudes, the instantaneous coupling columns
\([\Omega_pu,\Omega_sv]\) have rank two. Hence no nonzero vector supported
only on \(\{|i\rangle,|f\rangle\}\) is dark to the entire excited manifold.
Projecting onto one intermediate level makes the matrix rank one and
produces the usual Lambda dark state. Selected-line STIRAP remains valid
when its spectral isolation and omitted-channel effects are actually
controlled; exact full-manifold darkness does not follow.

This is consistent with established multilevel interference work, for
example [PRL 122, 253201 (2019)](https://doi.org/10.1103/PhysRevLett.122.253201).
It is a mechanism-specific linear-algebra statement, not a general
impossibility of adiabatic molecular association.

## 4. Retaining both nuclear spins cancels a spurious leading tensor

The useful atomic-limit model retains one electronic excitation, its full
J=1 Cartesian manifold and both I=1/2 nuclei. The excited dimension is
\(2\times3\times4=24\). It is complete for those atomic degrees of freedom;
it is not the complete electronic chemical spectrum.

Let \((J_a)_{bc}=-i\epsilon_{abc}\), and define

\[
F=\sum_{a=1}^2 |a\rangle\langle a|\otimes
\mathbf J\cdot\mathbf I_a,\qquad H=H_0+AF.
\]

Assume the spin-independent \(H_0\) is diagonal in Cartesian electronic
polarization, although it may transfer excitation between atoms and have
operator-valued orbital/source entries. Let a real pi drive prepare

\[
B=\frac{|1,z\rangle+|2,z\rangle}{\sqrt2}\otimes I_4.
\]

The response is \(\mathcal R(z)=B^\dagger(z-H)^{-1}B\). Its first three
compressed moments are scalar on the full nuclear space:

\[
B^\dagger H^nB=I_4\otimes C_n,\qquad n=0,1,2.
\tag{3}
\]

Here each \(C_n\) may act on orbitals/source. The proof does not require
different entries of \(H_0\) to commute. At n=1,
\(\langle z|J_j|z\rangle=0\). Cross terms at n=2 also vanish because one
hyperfine insertion changes the Cartesian polarization and \(H_0\) does
not change it back. Finally,

\[
\langle z|(\mathbf J\cdot\mathbf I_a)^2|z\rangle
=I_{ax}^2+I_{ay}^2=I_4/2.
\]

The last equality uses the actual spin-1/2 of each nucleus. It is lost by
projecting intermediate nuclear states prematurely onto a collective I=1.

### Leading fixed-axis pair tensor

Take real excitation-transfer coefficients \(V_x,V_y,V_z\), so
\(H_0=\tau_x\otimes\operatorname{diag}(V_x,V_y,V_z)\otimes I_4\).
At the cubic moment, the nuclear-nonscalar part comes from \(AFH_0AF\):

\[
\mathcal N_t(B^\dagger H^3B)
=\mathcal N_t\!\left[\frac{A^2}{4}
(V_y\sigma_{1x}\sigma_{2x}+V_x\sigma_{1y}\sigma_{2y})\right],
\tag{4}
\]

where \(\mathcal N_t\) restricts to the triplet and subtracts its scalar
trace part. The other cubic terms are nuclear scalars for this geometry.
Consequently, elastic triplet anisotropy starts at \(\Delta^{-4}\).
For \(V_x=V_y=V_\perp\), its T0 energy differs from T+ and T- by
\(A^2V_\perp/(2\Delta^4)\), before the common optical intensity factor.

A sufficient finite-domain bound following directly from (3) is

\[
\|\mathcal N_t(\mathcal R(z))\|
\le\frac{2\|B\|^2\|H\|^3}{|z|^3(|z|-\|H\|)}.
\tag{5}
\]

The bound controls nuclear nonscalarity, not total scalar response. It is
deliberately conservative. Arbitrary retained-source bandwidth is not
eliminated by this stationary resolvent expression. Common source evolution
must be treated in the actual interaction picture or by a valid local-orbit
argument. The companion derivation shows a moving-pair term linear in A,
\(A[B_1,K]/\Delta^4\), when the pair orientation changes. It therefore
cannot be omitted from a warm three-dimensional claim.

### Why the tempting I=1 projection gives the wrong order

Project the electronic label to \(|+\rangle=(|1\rangle+|2\rangle)/\sqrt2\)
and nuclear states to their triplet before taking the resolvent. Then

\[
PFP=\tfrac12\mathbf J\cdot\mathbf I_{\rm tot}.
\]

The resulting second moment is
\(A^2[2I-I_{{\rm tot},z}^2]/4\), which is not triplet scalar. The toy
therefore predicts a \(\Delta^{-3}\) defect. The omitted electronic
\(|-\rangle\), nuclear-singlet virtual channel contributes at exactly the
same order and restores (3). Algebraically,

\[
PF^2P=(PFP)^2+PF(I-P)FP.
\]

Discarding the second term is an unavailable physical projection. This
correction is significant even when the input and returned ground pair are
both in the triplet.

## 5. Fine optical outputs remain necessary

The usual weak-drive effective-operator formula gives a physical jump for
each output mode, \(L_\alpha=C_\alpha H_{\rm NH}^{-1}V_+\), with
\(H_{\rm NH}=H_e-i\sum_\alpha C_\alpha^\dagger C_\alpha/2\).
This established machinery is described by
[Reiter and Sørensen, PRA 85, 032111 (2012)](https://arxiv.org/abs/1112.2806).
A scalar elastic response or scalar \(\sum L_\alpha^\dagger L_\alpha\)
does not make the individual \(L_\alpha\) scalar.

In the atomic pi-drive model, spin-changing spontaneous amplitudes begin
at \(\Omega A/\Delta^2\), giving rates of order
\(\Gamma\Omega^2A^2/\Delta^4\). Scalar Rayleigh amplitudes begin at
\(\Omega/\Delta\). Scalar photon recoil can preserve nuclear information
while changing the orbital energy: it enters the actual cooling, escape,
holding and repeated-use budget. The distinction between Rayleigh and Raman
errors is established, for example in
[Ozeri et al., PRA 75, 042329 (2007)](https://doi.org/10.1103/PhysRevA.75.042329).
The finite-domain scalings here should not be extrapolated beyond the
optical rotating-wave and spectral model. The corrected large-detuning
analysis in [Moore et al., PRA 107, 032413 (2023)](https://arxiv.org/abs/2211.00744)
is a warning against using fixed-linewidth extrapolation as a fundamental
optical no-go.

## 6. The useful action determines whether detuning helps

Let \(W_{fi}\ne0\) be the actual matrix element in (1). For two comparable
classical beams with amplitudes of order \(\Omega\), a coherent association
Hamiltonian has strength of order
\(g_{fi}\sim\Omega^2W_{fi}/\Delta^2\). Its fixed-angle time is
\(T\sim\Delta^2/(\Omega^2|W_{fi}|)\). Under the fixed-axis hypotheses,
the action-scaled errors then have the schematic forms

\[
\epsilon_{\rm tensor}\sim\frac{A^2 V}{|W_{fi}|\Delta^2},\qquad
\epsilon_{\rm Raman}\sim\frac{\Gamma A^2}{|W_{fi}|\Delta^2},\qquad
N_{\rm Rayleigh}\sim\frac{\Gamma}{|W_{fi}|}.
\tag{6}
\]

The numerical factors depend on the physical beams, channel matrices and
pulse shape. The useful conclusion is the shared scaling, not a numerical
Yb prediction. At fixed optical power, holding error grows as
\(r_h\Delta^2/(\Omega^2|W_{fi}|)\). Thus increasing detuning indefinitely
does not produce arbitrarily accurate finite-time operation with fixed
holding noise. Raising both amplitudes proportionally to detuning can keep
the coherent association time finite, but requires power proportional to
\(\Delta^2\), a controlled weak-drive ratio, finite spectral validity and
the same real output/return apparatus.

A fixed vacuum Stokes coupling is different. In a bad-cavity association
model with fixed g and population linewidth kappa,

\[
\Gamma_{\rm assoc}\sim
\frac{\Omega_p^2g^2|W_{fi}|^2}{\kappa\Delta^4}.
\]

The Raman rate and fixed-axis tensor scale are then co-suppressed with the
useful rate, so their ratios to progress do not improve with detuning.
Scalar Rayleigh photons per accepted association grow as \(\Delta^2\).
Warm entrance detuning bandwidth also demands a sufficiently broad cavity,
which reduces enhancement at fixed g. The companion derivation supplies
the complete coefficients and bandwidth inequality. A classical coherent
Raman scaling must not be substituted into that different apparatus.

## 7. A natural metastable sink has an actual odd-wave cost

Keeping qubits in the J=0 metastable clock manifold would avoid a repeated
spin-dependent clock transfer and could use natural e-e inelastic loss.
However, [Ludlow et al., PRA 84, 052724 (2011)](https://doi.org/10.1103/PhysRevA.84.052724)
measured substantial loss for fully nuclear-spin-polarized 171Yb at about
10 microkelvin: the reported coefficient was approximately
\(5\times10^{-11}\,\mathrm{cm^3/s}\), with large absolute density
uncertainty, and polarized/unpolarized rates agreed within about ten
percent. Odd partial waves therefore cannot be called a quiet branch in
that actual regime. The primary author PDF is
[available from NIST](https://tf.nist.gov/general/pdf/2589.pdf).

A contact-model scaling can guide a different confinement question without
erasing this evidence. Define complex s-wave length
\(a_s=\alpha_s-i b_s\) and p-wave volume
\(v_p=\alpha_p-i b_p\), both with positive imaginary-loss parameters.
For relative mass mu and harmonic length a, first-order pseudopotential
conventions \(g_s=2\pi\hbar^2 a_s/\mu\) and
\(g_p=6\pi\hbar^2 v_p/\mu\) give

\[
\Gamma_s=\frac{4\hbar b_s}{\sqrt\pi\mu a^3},\qquad
\Gamma_p=\frac{24\hbar b_p}{\sqrt\pi\mu a^5},\qquad
\frac{\Gamma_p}{\Gamma_s}=\frac{6b_p}{b_s a^2}.
\tag{7}
\]

In a separable anisotropic harmonic domain with a longitudinal odd mode,
the ratio uses the longitudinal \(a_x^2\); transverse confinement enhances
both rates through \(1/(a_y a_z)\). This suggests a possible geometry
tradeoff, not an earned small error. Actual complex scattering, confinement
corrections, interactions during warm cooling and the full retained orbital
domain still need qualification. Cooling to the lowest allowed odd mode
does not remove its zero-point gradient at contact.

## 8. What the executable establishes

`molecular_response_check.py` runs without molecular data. Its results are
preserved in `molecular_response_results.json`.

- A complete two-state radial model has zero leading Franck–Condon sum and
  \(\Delta^2\mathcal A_{fi}\to0.7\). Both exact coupling singular values
  are nonzero (0.8 and 0.6). A selected-level dark vector remains coupled
  to the rest of the complete manifold.
- The full 24-state model has scalar nuclear moments n=0,1,2. Its cubic
  triplet tensor agrees with (4) to floating-point precision. At
  \(A=1,(V_x,V_y,V_z)=(0.3,0.3,-0.6)\), the triplet-nonscalar cubic norm is
  0.1, and \(\Delta^4\|\mathcal N_t(\mathcal R)\|\) approaches 0.1.
- The physically incomplete collective-I=1 projection produces a false
  inverse-cubic leading response with coefficient 1/6. This check displays
  the missing virtual channel explicitly.

These checks support exact finite-model identities. They neither certify
rounding enclosures nor prove that a real molecular spectrum fits a bounded
matrix truncation. The result worth retaining is that final-channel parity,
complete-manifold closure and complete fine-output opacity are different
requirements; a useful molecular cycle must satisfy them together. The
construction has not yet supplied that complete cycle, which justifies
moving the main capability to a more directly available longitudinal
measurement stack while retaining these corrections.
