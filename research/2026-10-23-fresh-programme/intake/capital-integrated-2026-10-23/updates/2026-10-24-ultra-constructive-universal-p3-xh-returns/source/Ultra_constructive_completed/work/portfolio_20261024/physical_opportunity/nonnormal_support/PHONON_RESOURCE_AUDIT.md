# Physical resource audit: local-resonance phonon filter

## Scope

The candidate is a passive, periodic mechanical/phononic link between two cryogenic stages. A positive-mass side resonator is coupled to each backbone cell; the intended operation is to reshape *ballistic phonon transmission* near a chosen operating temperature while holding cell mass and static longitudinal stiffness fixed. This is a stronger physical direction than the original fracture reserve because the model has a sharp same-resource comparator and an experimentally falsifiable spectral signature. It is still a model proposal, not a measured thermal-conductivity result or a claim of novelty.

The proposed application is deliberately narrow: a thermal link in a cryogenic package, where one can measure coherent/ballistic transmission. It does not establish reduced bulk thermal diffusivity, electronic/thermoelectric performance, or room-temperature insulation.

## What the ideal cell charges

Take a cell of period \(a\), backbone mass \(m_b>0\), resonator mass \(m_r>0\), intercell spring \(K>0\), and internal spring \(k>0\). Let \(M=m_b+m_r\), so both moving masses are charged to the cell mass. With \(s(q)=4K\sin^2(qa/2)\), the generalized eigenproblem is

\[
\begin{pmatrix}s+k&-k\\-k&k\end{pmatrix}u
=\lambda\begin{pmatrix}m_b&0\\0&m_r\end{pmatrix}u,
\qquad
 m_bm_r\lambda^2-[m_r s+kM]\lambda+sk=0.
\]

At \(q=0\), the two squared frequencies are \(0\) and
\[
\omega_0^2=k\left(\frac1{m_b}+\frac1{m_r}\right)=\frac{kM}{m_bm_r}.
\]
At long wavelength, the resonator follows the backbone and the acoustic branch is
\[
\omega_-(q)=a\sqrt{K/M}\,|q|+o(|q|).
\]
Thus adding a resonator does not buy a lower long-wave sound speed if the comparator has the same total cell mass and \(K\); it redistributes the spectrum above the acoustic limit.

The rigidly bound comparator has \(\omega_R(q)=2\sqrt{K/M}|\sin(qa/2)|\), hence cutoff \(2\sqrt{K/M}\). The natural-resonance ratio is
\[
\frac{\omega_0}{2\sqrt{K/M}}=\frac12\sqrt{\frac{k/K}{\alpha(1-\alpha)}},
\quad \alpha=m_b/M\in(0,1).
\]
This ratio stays finite for positive masses and finite \(k\). The \(m_b\to0\) limit sends \(\omega_0\) to infinity and is singular; it is excluded. The physically meaningful design variables include both \(\alpha\) and \(k/K\), with an explicit positive lower bound on \(m_b\) and a finite internal-stiffness budget. A massless spring is an idealization too: a real spring, attachment, frame, and proof mass all contribute mass and parasitic modes and must be included in \(M\).

For the supplied fixture \(m_b=m_r=K=1, k=4\) (consistent units), the bands are exactly
\[
[0,\sqrt{6-\sqrt{20}}]=[0,1.2361\ldots],\qquad
[\sqrt8,\sqrt{6+\sqrt{20}}]=[2.8284\ldots,3.2361\ldots].
\]
The equal-mass rigid comparator has band \([0,\sqrt2]=[0,1.4142\ldots]\). The resonator narrows the acoustic band but adds an optical band; total width is \(1.6437\ldots\), larger than the comparator's \(1.4142\ldots\). It therefore does not reduce the classical ballistic mode-count integral. Its possible benefit is finite-temperature reweighting, where the added high-frequency branch is less occupied.

## Resource interpretation in a real solid

For a uniform 1-D rod of length \(a\), area \(A\), density \(\rho\), and Young modulus \(E\), the ideal intercell spring corresponds to \(K=EA/a\) and cell mass \(M=\rho Aa\). Holding \(a,M,K\) fixes line mass \(M/a\), axial rigidity \(EA\), and long-wave speed \(a\sqrt{K/M}=\sqrt{E/\rho}\). It does **not** fix the internal resonator's material, internal spring mass, allowable stress, loss tangent, or volume. A fair specimen comparator should therefore match (i) total mass per period including resonator supports and housing, (ii) static end-to-end axial stiffness, (iii) span and boundary contacts, and (iv) operating temperature. The resonator design must separately report its internal stiffness and strain/stress budget; otherwise taking \(k/K\) arbitrarily large just hides a material-resource cost.

A real spring with length \(\ell\), area \(A_s\), density \(\rho_s\), and modulus \(E_s\) has the elementary scaling \(k\simeq E_sA_s/\ell\), \(m_s\simeq\rho_sA_s\ell\), so \(k/m_s\simeq(E_s/\rho_s)/\ell^2\). Raising a resonance by increasing stiffness cannot be treated as free: it changes the spring geometry/material, its mass, and the required force/stress. The lumped model is useful only if these added degrees of freedom remain well above the modeled bands and their loss is measured.

## Thermal operation and decisive bound

In an ideal ballistic link, the finite-temperature conductance is
\[
G(T)=\frac1{2\pi}\int_0^\infty \hbar\omega\,\mathcal T(\omega)\,\partial_T n_B(\omega,T)\,d\omega,
\]
where \(\mathcal T\) is the number of propagating branches. At low temperature, a single gapless acoustic channel approaches the universal quantum conductance, so the resonator does not improve the asymptotic \(T\to0\) limit when the comparator has the same acoustic channel. At high temperature the weighting tends to a constant, and total passband width is the relevant resource; the candidate's bandwidth lower bound then rules out a classical ballistic win. A useful operating window, if one exists, is intermediate: the acoustic cutoff must overlap the Bose thermal window while the optical branch is substantially above it.

This points to a specific operation: a finite-length, suspended, periodic phononic bridge whose local resonator is tuned for the temperature range of a cryogenic interconnect. The meaningful output is measured \(G(T)\) or frequency-resolved transmission, against a rigidly bound same-mass/same-static-stiffness bridge. It is not the existence of a Bloch gap by itself.

## Hard falsifier and unresolved gates

The decisive experiment is a matched pair of bridges with the same total mass per period, axial stiffness, span, contacts, and envelope; one has its internal proof masses elastically bound to the backbone, the other has the finite-\(m_b\), finite-\(m_r\), finite-\(k\) resonator arrangement. Measure transmission and heat flow over the designed temperature interval, including support/contact losses. The proposed thermal-filter operation fails if the resonator does not lower delivered \(G(T)\) in the target interval after these losses and resource matching, or if its apparent benefit disappears when spring/support mass is included.

The exact lattice theorem and finite-temperature optimizer are separate mathematical questions. Even a correct optimizer establishes neither a manufacturable continuum realization nor a reduction in diffusive \(\kappa\). At room temperature the characteristic thermal frequency \(k_BT/h\) is about 6.25 THz; a kHz or MHz macroscopic acoustic resonator is not automatically a room-temperature thermal-phonon filter. Any claimed application must show that its measured bands and transport regime overlap the actual thermal spectrum.
