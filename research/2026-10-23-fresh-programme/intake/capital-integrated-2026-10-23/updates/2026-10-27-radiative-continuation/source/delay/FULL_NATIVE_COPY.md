## ASTRA — New result: time-delayed darkness

The strongest result is a new distinction in the continuum-radiation problem: a photon can leave a set of emitters temporarily and return completely to vacuum at a designated final time without the emitters ever possessing a common instantaneous dark state.

This does not contradict the previous radiative-rank theorem. That theorem assumes frequency-separable emitter–radiation coupling. Spatially separated emitters instead introduce frequency-dependent propagation phases.

### 1. Why three emitters are fundamentally different from two

Consider emitters at positions \\(-\tau,0,+\tau\\), coupled to the left- and right-moving modes of a one-dimensional waveguide. Their source amplitudes are \\(q_1(t),q_2(t),q_3(t)\\).

Choose

\\[ \boxed{ q_1(t)=q_3(t)=f(t),\qquad q_2(t)=-f(t-\tau)-f(t+\tau). } \\]

If \\(f\\) has support strictly inside \\([\tau,T-\tau]\\), the complete radiation amplitudes in both propagation directions cancel exactly at time \\(T\\).

The result follows from Fourier translation identities, without using a Markov approximation.

Three precise conclusions follow:

- Two separated emitters cannot produce a nonzero, finite-duration source history with exactly zero final radiation under the same bidirectional coupling assumptions.
- Three equally spaced emitters can, even though the intersection of their instantaneous radiative kernels is trivial.
- A nonzero cancellation history requires \\(T>2\tau\\). Propagation delay therefore imposes a minimum duration.

The relevant mathematical object is no longer the nullspace of one coupling matrix. It is the space of time-shifted source histories satisfying the complete continuum cancellation equations.

This suggests a more general theory of spatiotemporal radiative protection.

### 2. A positive Hamiltonian realizes the construction

I also constructed a complete number-conserving Hamiltonian with two storage states, three emitters and a genuinely gapless two-direction continuum.

The internal controls are obtained by inverse engineering the desired state trajectory. A conservative analytic estimate gives a positive instantaneous Schur margin exceeding \\(12B\\).

The independent numerical integration gives:

| Quantity                                   | Executed result          |
| ------------------------------------------ | ------------------------ |
| Minimum sampled Schur eigenvalue           | \\(14.525B\\)            |
| Maximum transient radiation amplitude norm | \\(7.49\times10^{-4}\\)  |
| Final radiation amplitude norm             | \\(1.29\times10^{-12}\\) |
| Complete state-transfer error              | \\(1.37\times10^{-8}\\)  |

The exact zero final radiation and positivity follow from the mathematical construction; the small nonzero numerical residuals arise from integration accuracy.

Important limitation: The inverse-engineered internal Hamiltonian uses dense, complex, time-dependent couplings, including a direct storage-to-storage interaction. This proves compatibility with positive quantum dynamics, not implementability using the original restricted two-edge interface.

## 3. Stronger result: real controls, no bypass, and an on-band continuum

I extended the construction to eliminate its two most important idealizations:

- The internal Hamiltonian now uses only real, symmetric, two-mode hopping interactions, with no direct connection between the two storage states.
- The excitation's carrier frequency is \\(2\pi B\\), inside the radiation continuum \\(0<\omega<12B\\), rather than outside its spectral band.

The system contains two storage modes, three radiating emitters and two continuum propagation directions.

For the explicit control protocol, I proved a time-uniform internal Schur bound:

\\[ \boxed{H\_{\mathrm{Schur}}(t)\succeq1.125B\\,I.} \\]

The full Hamiltonian remains nonnegative, with a genuinely gapless radiation spectrum.

An independent propagation calculation gives:

Complete state-transfer error

## \\(2.85\times10^{-11}\\)

Final radiation amplitude

## \\(8.96\times10^{-14}\\)

Maximum sampled hopping

## \\(1.0023B\\)

Transfer duration

## \\(12/B\\)

The exact terminal-radiation cancellation is analytical. The residual errors above come from a finite-frequency quadrature and numerical time propagation.

### 4. Calibration is the remaining bottleneck

A new perturbation calculation retains every radiation output and leaves the designed controls unchanged.

| Perturbation                                   | Complete state error |
| ---------------------------------------------- | -------------------- |
| Symmetric outer-emitter position shift of 0.01 | 0.0139%              |
| Central-emitter position shift of 0.01         | 0.0770%              |
| 1% increase in radiation coupling              | 0.00033%             |
| Central-emitter energy offset of \\(0.01B\\)   | 1.022%               |

A separate Duhamel estimate bounds the full state error caused by emitter-position changes:

\\[ \boxed{\epsilon\_{\rm position}\le1.46043\\|\delta x\\|\_2} \\]

with positions measured in the model's propagation-time units.

The significant vulnerability is now coherent onsite-energy calibration, not geometric radiation leakage, for the chosen parameter regime.

## Research preserved

Complete mathematical proof and limitations

Two-emitter obstruction, three-emitter construction, exact real controls, uniform positivity, calibration bounds and alternative mechanisms.

Full-Hamiltonian implementation · Executed results

Uniform positivity certificate · Certificate data

Calibration simulation · Results

Scientific conclusion: The new explanatory result is that frequency-dependent propagation enables spatiotemporal radiation cancellation where ordinary frequency-independent dark-subspace arguments fail. The mathematics also produces an exact, positive, finite-time implementation without a direct storage bypass.

Related giant-atom and decoherence-free waveguide mechanisms are established physics.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

Phys. Rev. Research

+1

&#x20;Historical novelty remains unresolved.



The strongest remaining attack is to replace the five-mode network's precomputed time-dependent hopping controls with a more restricted microscopic control interface. Until that is achieved, this is a constructive quantum-dynamics theorem, not an experimentally demonstrated new capability.