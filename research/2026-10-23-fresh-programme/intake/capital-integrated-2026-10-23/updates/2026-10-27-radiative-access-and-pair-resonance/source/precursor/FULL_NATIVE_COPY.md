## ASTRA — Foundational physics continuation

New result: The reciprocal, gapless SSH waveguide supports a controlled two-qubit entangling operation even though its two-excitation memory state lies inside the two-photon continuum.

The central insight is that being embedded in a continuum does not automatically mean an excitation decays on the timescale of the desired operation. Here, the leading emission pathways cancel algebraically.

### 1. Exact dressed-pair cancellation

Consider two hard-core quantum memories \\(L,R\\), with excitation energy near \\(3B\\), coupled to the same infinite SSH bath. Its one-particle spectrum is

\\[ [0,2B]\cup[4B,6B]. \\]

Thus the memory energy \\(3B\\) lies in a gap, but the energy \\(6B\\) of two excited memories lies inside the two-photon continuum.

Let \\(h\\) be the bath Hamiltonian, \\(v_L,v_R\\) its local coupling profiles, and define, in units \\(B=1\\),

\\[ r_j=(h-3)^{-1}v_j. \\]

I constructed a normalized-up-to-dressing two-excitation state

\\[ |\Psi_g\rangle= |LR\rangle -g\left(|R;r_L\rangle+|L;r_R\rangle\right) +g^2a^\dagger(r_L)a^\dagger(r_R)|0\rangle. \\]

For adjacent gradient ports, direct operator algebra gives the exact identity

\\[ \boxed{ \\|(H_g-6)|\Psi_g\rangle\\| =\frac{g^3}{4\sqrt6}. } \\]

There is no second-order residual, even though freely propagating two-photon states exist at the same total energy.

This is stronger than a perturbative cancellation of an individual scattering amplitude: it holds for the complete infinite-volume Hamiltonian, including every bath mode and both photonic bands.

I independently assembled the hard-core two-particle Hamiltonian on a finite SSH ring and verified the corresponding exact residual identity to approximately \\(10^{-15}\\).

## 2. An entangling-gate theorem despite the open two-photon channel

The same Hamiltonian has two isolated one-particle bound levels near energy \\(3B\\). Their splitting is

\\[ E\_+-E\_-=\frac{g^2B}{4}+O(g^4B). \\]

After the exact exchange time

\\[ T_g=\frac{\pi}{E\_+-E\_-}, \\]

the one-excitation states approximately exchange places, while the two-excitation state remains approximately unchanged.

Combining the exact two-excitation residual with bounds on the one-particle spectral projectors, I obtain, for \\(0\<g\le1/20\\),

\\[ \boxed{ \\|U\_{\mathrm{physical}}(T_g)P\_{\mathrm{code}} -U\_{\mathrm{iSWAP}}P\_{\mathrm{code}}\\| \le5g. } \\]

Here \\(U\_{\mathrm{physical}}\\) includes the entire infinite waveguide, and the comparison includes known local memory-phase corrections. The computational input space consists of the four bare memory states with the bath initially in vacuum.

This is a complete coherent-isometry bound, including arbitrary states entangled with an untouched reference. No photon-survival postselection is used.

For illustration, choosing \\(g=0.002\\) gives a rigorous state-vector error bound of 1% or less in the ideal lossless model. The price is a long interaction time, approximately \\(3.14\times10^6/B\\).

The target iSWAP operation entangles the input \\(|+\rangle|+\rangle\\) maximally. Thus the bound provides a mathematically controlled entangling operation through a reciprocal, genuinely gapless continuum, without direct memory-to-memory hopping.

The result is a model capability, not an experimental gate or a claim of historical novelty. The small-coupling time cost leaves it vulnerable to independent memory dephasing.

## 3. Generalization: emergent spin dynamics without a many-particle gap

The two-memory cancellation is part of a broader result.

For any fixed finite collection of hard-core emitters with identical excitation energy \\(\varepsilon\\) lying in a gap of the one-particle bath, define the dressed excitation operators

\\[ B_i^\dagger=\sigma_i^+-g\\,a^\dagger(r_i), \qquad r_i=(h-\varepsilon)^{-1}v_i. \\]

Products of these operators generate approximate multiparticle states, even when their total energies overlap propagating multiphoton states.

With individually calibrated detunings, their dynamics are governed, to leading nontrivial order, by

\\[ \boxed{ H\_{\mathrm{eff}} =\varepsilon\sum_i n_i -g^2\sum\_{i\ne j} \beta\_{ji}\sigma_j^+\sigma_i^-, \qquad \beta\_{ji}=\langle v_j,r_i\rangle. } \\]

I derived an exact intertwining identity between this effective hard-core spin Hamiltonian and the complete bosonic Hamiltonian. Its residual begins at order \\(g^3\\), not \\(g^2\\).

For each fixed number of emitters \\(m\\), it implies

\\[ \boxed{ \\|U\_{\mathrm{full}}(t)P- P e^{-iH\_{\mathrm{eff}}t}\\| =O_m(g) \quad\text{when } |t|=O(g^{-2}). } \\]

There is no assumed many-particle spectral gap in this theorem. Every continuum excitation is retained.

I independently tested the identity for all eight computational states of a three-emitter system, using the complete hard-core Fock Hamiltonian through three excitations. The largest algebraic residual discrepancy was below \\(4\times10^{-15}\\), and the calculated residual scales cubically with coupling.

This gives a generative framework for effective quantum spin interactions inside globally gapless environments. Its scope is finite emitter collections and finite operational times; it does not establish permanent many-particle bound states or a useful thermodynamic limit.

## 4. The first genuinely unprotected interaction appears at fourth order

A further dressing calculation gives a sharper picture of the boundary between coherent control and irreversible radiation.

For the adjacent-memory construction, the two-particle quasimode acquires the perturbative energy correction

\\[ E\_{\mathrm{pair}}=6-\frac{g^4}{24}, \\]

and its residual can be reduced to

\\[ \boxed{ \\|(H_g-E\_{\mathrm{pair}})\Psi_g^{(3)}\\| <0.105g^4,\qquad 0\<g\le0.05. } \\]

For an already prepared normalized dressed input, this yields a coherent evolution-error bound of approximately \\(1.64g^2\\) over the single-excitation exchange timescale. Preparation of that input remains an unacquired resource.

There is a connected effective interaction of order \\(g^4\\): comparing the pair's perturbative energy with the sum of the two one-particle energies gives \\(-g^4/12\\).

However, the next correction encounters a real continuum obstruction. The remaining two-photon source has exact spectral density

\\[ \boxed{ \rho(6)=\frac{43}{162\pi^2} \approx0.0268939>0. } \\]

For every finite separation between the two gradient ports, an associated on-shell density remains strictly positive. Consequently, the ordinary Hilbert-space perturbation series cannot simply continue to a normalizable fourth-order bound-state correction.

This establishes a useful distinction:

- Proved: finite-time coherent protection and an effective many-body interaction.
- Not proved: a permanent embedded two-particle bound state, an exact long-time controlled-phase gate, or a radiative linewidth scaling law.

A formal golden-rule calculation suggests that the first decay width may arise at order \\(g^8\\), while the connected energy shift appears at order \\(g^4\\). If that separation survives a rigorous resonance analysis, it could permit a substantial conditional phase before appreciable radiation. That is now the most consequential unresolved attack.

## Research preserved

Complete mathematical proof

Exact spin–bath intertwining theorem, full-code error bound, entangling-gate proof, fourth-order source analysis and limitations.

Reproducible research package

13 files: mathematical derivation, five executed scripts, numerical results, arithmetic certificate and original gradient-transfer source.

The numerical audits establish:

- Exact dressed-pair residual identity reproduced to approximately \\(10^{-15}\\).
- Three-emitter full-code identity reproduced to approximately \\(4\times10^{-15}\\), including a random complex Hermitian bath.
- Fourth-order residual identity reproduced to approximately \\(9\times10^{-16}\\).
- Independent continuum quadrature agrees with the analytically derived nonzero two-photon spectral density.

Existing waveguide-QED research already studies metastable hard-core many-body states and multiexcitation bound states.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

Phys. Rev. A

+1

&#x20;The specific theorem derived here has not received independent external mathematical review or a historical priority determination.



Scientific assessment: This continuation advances beyond single-particle transfer. It establishes a finite-time mechanism by which a globally gapless bosonic environment generates coherent, interacting many-qubit dynamics without requiring a many-particle spectral gap.

The central open problem is now sharply defined: determine whether the fourth-order connected interaction can be exploited over a \\(g^{-4}\\) timescale while controlling the genuinely open two-photon radiation channel. That requires an interacting limiting-absorption or resonance theorem, not another finite-volume fidelity scan.