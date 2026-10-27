## ASTRA — New foundational physics result

The strongest construction is now an exactly protected, interacting two-excitation state embedded in a gapless quantum environment. It improves on the previous SSH resonance by eliminating intrinsic two-photon radiation altogether, while retaining a nonzero coherent interaction.

### 1. A symmetry-resolved spectral principle

In the original SSH model, the two-memory state was metastable: its connected interaction appeared at order \\(g^4\\), while its radiation width appeared at order \\(g^8\\).

I constructed a different Hamiltonian in which a conserved parity separates the two relevant photon bands. The bound pair belongs to the even-parity sector, while the propagating two-photon states at the same energy belong to the odd-parity sector.

The result is

\\[ \boxed{ E\_{\mathrm{pair}}\in\sigma\_{\mathrm{ess}}(H_2), \qquad E\_{\mathrm{pair}}\text{ is isolated within its own parity sector}. } \\]

Thus the pair is an exact bound state in the global continuum, not merely a long-lived resonance.

The coherent connected interaction is

\\[ \boxed{ \chi(g)=-(28\sqrt3-48)g^4+O(g^6) } \\]

with a nonzero coefficient of approximately \\(-0.4974226\\).

This produces a useful distinction: a globally embedded quantum state can support coherent interactions and adiabatic control when it has a spectral gap within an exactly conserved symmetry sector. A global spectral gap is sufficient for ordinary adiabatic protection, but it is not necessary here.

### 2. A genuinely local realization

The construction uses two hard-core memories and a connected ladder of bosonic oscillators. Every bath hopping is nearest-neighbour along a rail or across a rung, and each memory attaches only to the first rung.

All hopping coefficients are real. The infinite bath has two continuous bands,

\\[ [0,2B]\cup[4B,6B], \\]

including modes arbitrarily close to zero energy.

The pair lies near \\(6B\\), inside the global two-photon continuum \\([4B,8B]\\). The model remains nonnegative in every finite excitation sector.

Direct diagonalization of the complete hard-core Fock Hamiltonian independently reproduces the embedded-pair energy, symmetry and spectral weight from the exact Green-function construction.

### 3. The interaction can be reversed without destroying protection

A further result separates two physical requirements that are often conflated: radiation protection and interaction strength.

Let \\(t\\) be the direct memory-to-ladder coupling and \\(s\\) the crossed coupling. For small couplings,

\\[ \boxed{ \chi(t,s)=-8ab\\,ts(t^2+s^2)+O((|t|+|s|)^6) } \\]

where \\(a=4-2\sqrt3\\) and \\(b=4/\sqrt3-2\\).

The sign is controlled by \\(ts\\), while the radiation-protecting parity remains unchanged.

| Cross coupling \\(s\\), with \\(t=0.20B\\) | Exact computed connected shift |
| ------------------------------------------ | ------------------------------ |
| \\(-0.04B\\)                               | \\(+0.000417888B\\)            |
| \\(0\\)                                    | \\(0\\)                        |
| \\(+0.04B\\)                               | \\(-0.000417888B\\)            |

The zero case is especially revealing. With no crossed coupling, an additional spectral-reflection symmetry forces the nonlinear interaction to vanish exactly to every order, even though the embedded pair remains protected.

Therefore, protecting a many-body state from radiation is not enough. The architecture must also break the appropriate spectral-reflection symmetry to generate a useful interaction.

### 4. End-to-end coherent gate

A symmetric coupling ramp can adiabatically load and retrieve the bound eigenstates. Two identical cycles with local memory echo pulses cancel the faster one-particle exchange while retaining the connected pair phase.

In the ideal infinite-ladder model, the sector-specific spectral gaps establish asymptotically arbitrarily accurate coherent controlled-Z operations at fixed sufficiently small nonzero coupling.

An executed finite-chain test at \\(g=0.4B\\), using ten bath sites per rail, gives:

Full code-isometry error

## 0.0664%

Total duration

## 562.8 \\(B^{-1}\\)

This numerical result retains the complete hard-core two-particle Hilbert space. It is not an infinite-volume finite-time fidelity certificate.

### 5. What happens when spectral filtering becomes imperfect?

For a specified additional wrong-band coupling of relative amplitude \\(\delta\\), I derived the leading positive on-shell two-photon spectral coefficient:

\\[ \boxed{c(\delta)=\frac{16}{9\pi^2}\delta^2.} \\]

The corresponding formal small-coupling resonance calculation gives an amplitude linewidth beginning at approximately

\\[ \gamma\sim1.46263\\,\delta^2g^8. \\]

This shows how a radiative channel reopens when the spectral separation is imperfect. It does not establish a general tolerance for arbitrary mirror-symmetry-breaking errors, which remain the main physical vulnerability.

## Saved research

- Complete derivation and theorem
- Exact spectral-resolvent calculation · Results
- Independent connected-ladder Fock audit · Results
- Full coherent gate simulation · Results
- Interaction-sign tunability · Spectral leakage calculation

Scientific significance: This establishes a constructive route from symmetry-filtered one-particle bands to an exact embedded many-particle eigenstate with a tunable, nonzero coherent interaction. The crucial principle is the distinction between a gap in the full spectrum and a gap in the dynamically accessible symmetry sector.

Bound states in continua and photon-mediated interactions have substantial prior art.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

Phys. Rev. A

+2

&#x20;The particular combined construction has not been externally reviewed for correctness or novelty.



The next decisive step is deriving the effect of physically realistic parity-breaking radiation from one microscopic electromagnetic model. The current result is an exact Hamiltonian construction and a numerical gate demonstration—not an experimentally acquired capability or a new fundamental force.