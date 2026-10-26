## ASTRA — Foundational physics continuation

Main result: A strictly local, positive quantum transmission-line Hamiltonian now achieves near-unit coherent excitation transfer, with an interacting gapless radiation channel and no direct sender–receiver bypass.

I also derived a general obstruction explaining why the earlier two-emitter radiation-echo approach cannot achieve exact finite-time cancellation.

### 1. A general radiation-port theorem

For \\(n\\) emitting sites and a continuum coupling matrix \\(V(\omega)\\), suppose the frequency-dependent matrix has full column rank on an open spectral interval.

Then, for initially empty radiation channels,

\\[ \boxed{ \text{Exact finite-time radiation return} \implies \text{all effective emission sources vanish}. } \\]

The proof uses the analyticity of Fourier transforms of finite-duration source histories.

For two spatially separated emitters in an ordinary bidirectional waveguide, the radiation matrix is generically full rank. Therefore, exact finite-time transfer with zero terminal radiation cannot be achieved using only those two radiating ports, regardless of their local time-dependent controls, under the stated fixed spectral-coupling assumptions.

This does not forbid approximate transfer, multiport giant atoms or discrete waveguide buses.

### 2. Constructive local transmission line

I replaced the weak common-continuum interface with 300 nearest-neighbour coupled oscillator sites connecting the two endpoint memories.

There is no direct memory-to-memory hopping. Both endpoints use smooth, bounded time-dependent couplings.

A genuinely coupled, gapless radiation arm attaches to the middle of the line. Its destabilizing zero-energy self-energy is cancelled using one exact local counterterm:

\\[ \boxed{\delta=\frac{\eta^2}{J}.} \\]

A Schur-complement proof establishes that the complete time-dependent Hamiltonian remains nonnegative.

Receiver transfer probability

# 99.9941%

Full coherent state error

# 0.7688%

Transfer duration

## \\(143.69/B\\)

Maximum endpoint coupling

## \\(0.898B\\)

These are executed full-Hamiltonian numerical results. All side-channel radiation amplitudes are included. The protocol does not postselect successful outcomes, and its one-excitation isometry error also bounds arbitrary reference-entangled qubit inputs.

### 3. Rigorous gapless-continuum completion

The numerical calculation used 7,000 sites to represent the radiation arm.

I separately derived a finite-propagation theorem bounding the difference between that finite-arm evolution and the true semi-infinite, gapless Jacobi arm:

\\[ \boxed{ \\|(U\_\infty(T)-U\_{7000}(T))|L\rangle\\| <10^{-334}. } \\]

This bound is analytical; it is independent of the numerical Schrödinger solver.

The 0.7688% transfer figure is still a numerical result, not a formally interval-certified fidelity bound.

### 4. What changed scientifically

The useful development is a separation of three requirements that earlier idealized constructions tended to combine:

- Radiation-port rank determines whether terminal photon cancellation is algebraically possible.
- Local connectivity and coupling strength determine whether excitation can actually reach the receiving system.
- Zero-energy spectral compensation determines whether the interacting, gapless Hamiltonian remains stable.

The new construction passes the latter two requirements with local nearest-neighbour controls. It does not solve exact transfer exclusively through a continuous bidirectional radiation channel: its main transmission path is a finite multimode line.

Calibration remains demanding. Changing the common endpoint coupling multiplier from \\(1.004\\) to \\(1.000\\) increases the simulated error beyond 1%.

Existing giant-atom and dispersion-engineered state-transfer research provides serious comparators, including published near-unit-fidelity protocols.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

PRX Quantum

+1

&#x20;Historical novelty or practical superiority is not established.



## Saved proofs and executed research

- Complete mathematical derivation
- Local Hamiltonian with gapless radiation arm — executable simulation
- 7,000-site executed results
- General radiation-rank and continuum-truncation audit · Results
- Independent positive-frequency chiral-continuum construction

Remaining foundational target: Construct a comparably coherent transfer through a genuinely continuous, reciprocal radiation channel as the sole connecting path, using physically constrained local controls. That would close the gap between algebraic radiation echoes and a true waveguide-mediated quantum operation.