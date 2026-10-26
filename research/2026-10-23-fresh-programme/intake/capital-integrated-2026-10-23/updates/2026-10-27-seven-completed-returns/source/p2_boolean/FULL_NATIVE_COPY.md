## ASTRA — New construction: programmable many-body interactions with bounded local controls

The local Jacobi programme now has a more general construction. Instead of connecting the photon emitter directly to every stored excitation, a network of auxiliary two-level systems computes a collective property of the memory and presents it to the emitter as one binary control.

For \\(m\\) memory excitations, this replaces the previous emitter-detuning range proportional to \\(m\\) with a fixed detuning of \\(201B\\), independent of memory capacity.

### 1. An exact two-body construction

For binary occupancies \\(a,b,c\\), define

\\[ p\_{\mathrm{AND}}(a,b,c)=ab-2ac-2bc+3c. \\]

This polynomial contains only one-body and two-body interactions. It is nonnegative and vanishes exactly when \\(c=ab\\).

Connecting \\(m-1\\) such constraints in a balanced binary tree produces a final flag

\\[ r=x_1x_2\cdots x_m. \\]

The emitter now has energy

\\[ H_e=B\left[1.2+201(1-r)\right]n_e. \\]

Only the root flag couples directly to the emitter. The other controls implement the Boolean constraints.

For this exact Hamiltonian family:

- The interaction graph has maximum degree four.
- Every individual coupling coefficient is bounded independently of \\(m\\).
- Incorrect flag configurations cost at least \\(3B\\) in the constraint Hamiltonian.
- The encoded memory states remain exact eigenstates of the control Hamiltonian.

The construction preserves the earlier all-particle spectral theorem,

\\[ \boxed{\inf\operatorname{spec}H_N=-B\min(N,m)} \\]

for every finite \\(N\\), including the genuinely coupled gapless photon continuum.

### 2. The coherent photon operation survives

The same complete two-output Jacobi scattering calculation gives, uniformly over photon energies \\(0.4B\le E\le1.8B\\),

\\[ \boxed{ \epsilon\_{\mathrm{selected}}<0.005478,\qquad \epsilon\_{\mathrm{unselected}}<0.009951. } \\]

After coherently computing the flags, scattering one photon and uncomputing the flags, the resulting operation on the memory approximates

\\[ \boxed{U\_{\mathrm{AND}}=I-2|11\cdots1\rangle\langle11\cdots1|.} \\]

This is a many-qubit conditional phase, assembled from static pairwise interactions and a single-photon scattering operation.

The error bound includes both photon output channels and holds for arbitrary memory superpositions entangled with a reference. It assumes ideal coherent flag preparation and the previously specified lossless microscopic Hamiltonian; those resources have not been experimentally acquired.

## 3. A lower bound explains the resource tradeoff

For the original direct longitudinal coupling, nonnegative one-particle spectra and 1% photon accuracy together require

\\[ \boxed{\Delta\_{\mathrm{total}}\ge199.99794\\,mB.} \\]

The compiled flag construction uses a fixed \\(201B\\) emitter shift instead.

| Memory capacity | Direct minimum detuning | Compiled detuning | Extra flag spins |
| --------------- | ----------------------- | ----------------- | ---------------- |
| 8               | \\(1,600B\\)            | \\(201B\\)        | 7                |
| 32              | \\(6,400B\\)            | \\(201B\\)        | 31               |
| 128             | \\(25,600B\\)           | \\(201B\\)        | 127              |

The theorem is specific to an emitter detuning affine in the original memory occupations. The new architecture escapes it by using additional internal degrees of freedom.

There is a second obstruction: for \\(m\ge3\\), one auxiliary flag with no intermediate registers cannot implement the same uniquely encoded, zero-penalty AND condition using only diagonal two-body terms. The intermediate structure is necessary under that exact encoding contract.

## 4. Extension beyond occupancy detection

I constructed a compiler for arbitrary Boolean predicates using two-body NAND and COPY penalties. In principle, the resulting photon scattering implements

\\[ \boxed{U_f=I-2\sum\_{x:f(x)=1}|x\rangle\langle x|.} \\]

The full-output stationary scattering-error bound remains independent of the register size.

Executed exhaustive checks covered XOR and three-input majority, including every auxiliary-register assignment. Both retained unique zero-energy encodings and maximum interaction-graph degree four.

### Next attack: preparing the flags without a three-body gate

I also constructed a time-dependent two-local Hamiltonian that conditionally flips one flag through a uniformly gapped path, with a proven instantaneous gap of at least \\(B\\).

Numerical Schrödinger evolution confirmed coherent conditional flipping and showed errors reaching approximately \\(1.21\times10^{-4}\\) for one tested pulse duration. The error was not monotone with pulse duration.

A separate exact argument rules out achieving perfect conditional AND with one constant square pulse and equally spaced two-body detunings. Its required integer resonance conditions contradict each other modulo four.

These results identify coherent flag preparation as the next resource bottleneck. An ideal bounded-degree static encoding does not automatically provide a reliable end-to-end operation.

## Saved research

Complete mathematical continuation

All-sector capacity proof, full photon error theorem, two resource obstructions, universal Boolean compilation and conditional flag dynamics.

Executable research and results package

Independent scripts, exhaustive truth-table checks, complete two-channel scattering checks, coherent evolution calculations and JSON results.

Scientific assessment: The new mathematical capability is compiling a collective many-particle predicate into a bounded-strength, two-local, capacity-preserving photon interaction. Its scattering accuracy does not deteriorate with memory capacity, but auxiliary count and coherent preparation resources grow.

Boolean quadratization and ancilla-mediated quantum logic have substantial prior art.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://personal.lse.ac.uk\&sz=32)

personal.lse.ac.uk

+1

&#x20;The specific integration is useful, but historical novelty and a physical advantage remain unestablished.



The strongest remaining challenge is to achieve the same conditional response with substantially smaller emitter detuning and a physically realizable, low-error preparation interface—not to add more formal spectral optimization.