## ASTRA — A stronger mechanism: exact broadband scattering from a local lattice

The passive spectral-moment programme has revealed a simpler alternative to high-order dispersion compensation.

A uniform semi-infinite oscillator chain can produce an exactly frequency-independent conditional scattering phase across its entire propagation band, without auxiliary resonators.

Take a chain with on-site energy \\(B\\), nearest-neighbour hopping \\(B/2\\), and a boundary emitter coupled by \\(B/\sqrt2\\). In units \\(B=1\\), its exact endpoint spectral density is

\\[ J(E)=\frac{\sqrt{E(2-E)}}{\pi},\qquad 0\<E<2. \\]

Its real continuum self-energy is

\\[ \boxed{\Sigma(E)=1-E.} \\]

For an emitter energy \\(H=1\\), the Fano reactance cancels identically:

\\[ D(E)=E-H+\Sigma(E)=0. \\]

Consequently,

\\[ \boxed{S\_{\mathrm{selected}}(E)=-1\quad\text{for every }0\<E<2.} \\]

This is not a Taylor-series approximation. It is an exact full-band scattering identity.

The construction has a transparent microscopic interpretation: its boundary coupling is precisely that obtained by folding the even-parity sector of an infinite uniform lattice. Thus the spectral compensation follows from lattice geometry, not finely adjusted high-order side resonances.

The underlying surface Green function is established tight-binding physics.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://cpoli.github.io\&sz=32)

tbkit 0.6.0 documentation

+1

&#x20;The result here is its integration with Astra's conditional-memory and all-particle-capacity framework, not a claim that semicircular spectral densities are new.



A direct real-space reflection calculation independently agrees with the Fano scattering formula to within \\(4.3\times10^{-15}\\).

## 2. An interacting gapless version with rigorous error bounds

The exactly flat chain alone lies at the boundary of its positive-energy stability condition. To obtain a strictly positive margin while retaining genuine access to arbitrarily soft excitations, I constructed a two-chain Hamiltonian:

- A signal chain with on-site energy \\(1.2B\\), hopping \\(0.5B\\), and emitter coupling \\(B/\sqrt2\\).
- A gapless soft-excitation chain with on-site energy \\(B\\), hopping \\(0.5B\\), and emitter coupling \\(0.0015B\\).

The soft chain genuinely interacts with the emitter. No scattering branch is discarded.

With memory-conditioned emitter detuning \\(201B\\) per missing stored excitation, the following analytic bounds hold for all incoming photon energies \\(0.4B\le E\le1.8B\\).

Selected-state error

## <0.548%

Unselected-state error

## <0.996%

Positive Schur margin

## 0.6633 B

The errors bound complete outgoing photon state vectors, including the gapless unwanted-output channel, for arbitrary supported wavepackets and reference-entangled memory inputs.

The same Hamiltonian obeys

\\[ \boxed{\inf\operatorname{spec}H_N=-B\min(N,m)} \\]

for every finite total particle number \\(N\\) and memory capacity \\(m\\). The lower bound follows from one-particle positivity and conserved memory charge; the matching upper bound comes from arbitrarily soft escaping excitations in the coupled gapless channel.

### Robustness to imperfect controls

The conclusion survives, simultaneously, an emitter-energy calibration error of \\(\pm0.0005B\\), a relative error of \\(\pm0.0005\\) in the squared signal-boundary coupling, and a \\(\pm10\\%\\) error in the weak soft-channel coupling amplitude.

Throughout this parameter box, exact rational inequalities establish:

\\[ \boxed{ \epsilon\_{\rm selected}<0.674\\%,\quad \epsilon\_{\rm unselected}<0.996\\%,\quad M\_{\rm Schur}>0.6625B. } \\]

This is a stronger controlled microscopic result than the previous isolated spectral-shape fits, although the oscillator-chain model still lacks a demonstrated electromagnetic implementation.

## 3. A sharper physical principle: broadband matching, stability and loss are different constraints

The calculation establishes two boundaries that earlier spectral-optimization work did not separate.

First, in a gapless scalar continuum with a finite zero-energy self-energy, an exactly flat \\(-1\\) scattering phase all the way to zero photon energy forces the local Schur stability margin to vanish. This follows because the reactance must vanish at zero, giving \\(H=\Sigma(0)\\).

A gapped signal channel avoids that requirement. Coupling it weakly to a separate gapless channel then gives a strictly positive Schur margin, all-particle dissociation thresholds and a quantitatively controlled scattering error in the same Hamiltonian.

Second, the two-chain system has an exact stability boundary:

\\[ \boxed{\zeta^2\_{\mathrm{critical}}=\frac{\sqrt{11}}{10}\approx0.33166248.} \\]

Above this coupling strength, a negative-energy one-particle orbital appears. Unlimited bosonic occupation then destroys the particle-number-independent energy bound.

But the 1% coherent-photon criterion is far more restrictive. At the central frequency, independent-channel leakage requires

\\[ \boxed{\zeta<0.00357185.} \\]

Therefore coherent information preservation, rather than thermodynamic binding stability, is the controlling resource in this construction.

## 4. Spectral classification

I also proved a support-restricted uniqueness result.

Among sufficiently regular positive scalar spectral densities supported on \\([0,2B]\\), with finite inverse-frequency coupling integral, the semicircular density is the unique one that simultaneously permits exact selected-state \\(-1\\) scattering throughout the entire band and uniformly accurate unselected-state \\(+1\\) scattering with finite emitter-only detuning.

This is a consequence of the finite Hilbert transform's one-dimensional nullspace. It is not a uniqueness theorem for arbitrary multiport, active or auxiliary-coupled systems.

## 5. Finite-device evolution

The infinite-chain idealization has a separate, controlled finite-time approximation.

For two chains truncated after site \\(L\\), an initial state supported within site \\(R\\), and evolution time \\(T\\), I obtained

\\[ \boxed{ \\|(U\_\infty(T)-U_L(T))P_R\\| \le T\sum\_{n=L-R}^{\infty}\frac{(1.21T)^n}{n!}. } \\]

In binding-energy time units, \\(T=10\\) and \\(L-R=50\\) give an analytic error bound below \\(5.95\times10^{-10}\\). The bound is uniform over memory capacity and emitter detuning because those controls affect the diagonal energies, not the maximum hopping speed.

A spatially noncompact photon contributes an additional tail error. This is a finite-time locality theorem, not a claim that a finite chain possesses the infinite system's asymptotic scattering matrix.

## Saved derivations and executed checks

Complete 10-section mathematical derivation

Exact lattice Hamiltonians, spectral classification, all-particle proof, coherent scattering bounds, sharp failure thresholds, parameter robustness and finite-time locality.

Independent scattering and Hamiltonian audit · Results

Exact calibration-box certificate · Results

Sharp stability-threshold calculation · Finite-time evolution audit

Scientific assessment: This is a substantive improvement in the model construction: exact broadband conditional scattering follows from nearest-neighbour lattice symmetry, and exact all-particle capacity survives a genuinely interacting gapless environment with rigorously bounded coherent leakage.

The largest remaining resource is the pairwise memory–emitter shift, \\(201B\\) per missing excitation, requiring a total control range scaling as \\(201mB\\). Physical emitter arrays, nonlinear circuit elements, source preparation and independent radiation have not been acquired. The result is established mathematics for a local quantum Hamiltonian, not yet a newly demonstrated physical capability or a foundational change to known physics.