## ASTRA — A stronger photon-transfer mechanism

The previous Jacobi capture architecture had an almost optimal radiation-exposure cost for a photon captured directly onto a lossy emitter. I have constructed a different local Hamiltonian that avoids that constraint.

Instead, the photon is captured into a buffer mode, transferred through a lossy intermediate emitter into protected storage, given its conditional phase, and returned.

### 1. Exact finite-time transfer with arbitrarily small intermediate occupation

Let \\(a\\) be the buffer, \\(e\\) the radiatively exposed emitter, and \\(b\\) the storage mode. Use the two-edge Hamiltonian

\\[ H(t)=\mu I+g(t)(|a\rangle\langle e|+\mathrm{h.c.}) +J(t)(|e\rangle\langle b|+\mathrm{h.c.}). \\]

There is no direct buffer-to-storage interaction.

I constructed an exact transfer \\(|a\rangle\to|b\rangle\\) with maximum combined hopping strength \\(\Omega\\), taking

\\[ T=\frac{\pi}{2\Omega\tan\phi}+\frac{2\phi}{\Omega}. \\]

Its integrated intermediate-emitter occupation is exactly

\\[ \boxed{ A_e=\frac{\pi\sin\phi\cos\phi/2+\phi-\sin(2\phi)/2}{\Omega}. } \\]

As \\(\phi\to0\\),

\\[ \boxed{A_eT\longrightarrow\frac{\pi^2}{4\Omega^2}.} \\]

Therefore intermediate-emitter exposure can approach zero by allowing longer transfer time, while maintaining a finite maximum coupling strength.

A matching geometric lower bound shows that if the intermediate occupation never exceeds \\(\epsilon\\),

\\[ \boxed{ A_eT\ge\frac{\pi^2(1-\epsilon)}{4\Omega^2}. } \\]

The construction asymptotically attains this bound in the low-occupation regime.

This does not contradict the earlier single-port exposure theorem: the state being captured is now the buffer, not the lossy intermediate emitter.

### 2. Smooth controls and an end-to-end coherent operation

I independently integrated the Schrödinger equation for the transfer and its reverse, then included the matched Jacobi photon source, conditional storage phase, and release.

Previous lossy-emitter exposure

## 2.459 \\(B^{-1}\\)

New transfer-pair exposure

## 0.0701 \\(B^{-1}\\)

The second figure uses smooth hopping controls that vanish at both endpoints, with maximum coupling \\(10B\\). It reduces intermediate-emitter occupation-time by approximately 97.2%.

The ideal full photon operation implements the correct conditional sign with numerical error around \\(2\times10^{-13}\\). Unlike the faster piecewise protocol, the smooth transfer does not require abrupt changes between different hopping configurations.

For the effective Markov loss model at emitter rate \\(2\times10^{-5}B\\), with buffer and storage rates \\(10^{-6}B\\), the calculated complete photon/environment state-vector error is approximately 0.322%. If the buffer has the same high loss rate as the emitter, it rises to approximately 0.935%.

Both include emitted photons, rather than conditioning on successful survival. The improvement depends strongly on access to a comparatively low-loss buffer.

### 3. A microscopic radiation test

I replaced the intermediate emitter's Markov loss term with a permanently coupled, positive-energy Jacobi radiation bath extending down to zero frequency.

For a radiation band covering \\(0\\) to \\(22B\\), and coupling chosen to give a mid-band decay scale \\(2\times10^{-5}B\\), the full closed-Hamiltonian simulation gives approximately 0.117% state-vector deviation from the ideal radiation-free photon operation.

Every radiation mode is retained in the output. This is a numerical finite-time result for that specified spectral bath, not a universal decay estimate. It is separate from the buffer and storage losses above.

### 4. The return operation no longer needs sign-reversed hopping controls

A further construction removes a demanding control assumption from the transfer.

Define a local phase flip on the intermediate emitter:

\\[ Z_e=I-2|e\rangle\langle e|. \\]

Because it reverses both emitter hopping terms, the exact inverse of a transfer \\(F\\) can be implemented as

\\[ \boxed{F^\dagger=Z_eR\_{\mathrm{time}}Z_e,} \\]

where \\(R\_{\mathrm{time}}\\) plays the original hopping profiles in reverse chronological order without reversing their physical signs.

This permits a coherent return using the same hopping controls and two local phase operations. Independent propagator checks verified the identity to approximately \\(4\times10^{-13}\\), including 1% repeatable hopping-calibration errors.

There is a decisive limitation: an uncontrolled emitter-energy offset is not reversed by \\(Z_e\\). The identity is exact for the controllable three-mode Hamiltonian, not for its permanently coupled radiation environment.

### 5. A genuine two-level emitter also works

The intermediate mode need not be an ideal harmonic oscillator.

Replacing it with a two-level emitter restricts the quadratic bosonic Hamiltonian to occupations \\(n_e\le1\\). Since compression of a positive operator remains positive, the construction preserves the all-particle spectral lower bound in every finite excitation sector.

Independent Fock-space tests through four particles agreed with that argument. Multiphoton dynamics become nonlinear, but the one-photon transfer is unchanged.

This makes the proposed mechanism more compatible with ordinary saturable quantum emitters, although no physical apparatus has been acquired.

## Preserved research

The exact derivations, eight executed scripts, numerical results and essential earlier source checks are saved.

Complete mathematical derivation

Exposure-time theorem, exact and smooth transfer protocols, full radiation model, pulse echo and all-sector positivity.

Reproducible research package — 22 files

Proofs, executed Python scripts, JSON results and the necessary earlier capture and flag calculations.

Scientific conclusion: The strongest advance is a near-sharp, geometric time–exposure principle accompanied by a positive local Hamiltonian that approaches its lower bound. It explains how topology changes can reduce radiative occupation by orders of magnitude without discarding leakage branches.

Three-level transfer and shortcuts to adiabaticity have substantial prior art, including experimental implementations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

Phys. Rev. A

+2

&#x20;Historical novelty remains unestablished.



The remaining physical bottleneck is obtaining a low-loss guided buffer, independently tunable local couplings, and a strong conditional storage interaction from one microscopic platform. The current results are mathematical constructions and executed model tests, not a demonstrated device or a new fundamental law.