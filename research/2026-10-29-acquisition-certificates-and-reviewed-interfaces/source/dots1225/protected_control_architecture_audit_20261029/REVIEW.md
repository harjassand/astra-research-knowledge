# Independent receiving review: protected-control architecture

2026-10-29. **ACCEPT at the stated obstruction and conditional ideal-control scope**, subject to the unbounded-operator qualification below. No acquired microscopic control, device performance, novelty, or advantage over conventional DFS/geometric-phase control is accepted.

## Load-bearing conclusions

1. **Endpoint-to-generator obstruction is exact.** H0=pi Z1 has exp(−iH0)=−I, so its endpoint channel is identity in every frame. On pair12, H0+theta S12 has opposite-spin restriction pi Z+theta X. At theta=pi sqrt(5)/2 its norm is3pi/2, and its exponential maps the singlet to i(2/3)t0−i(sqrt(5)/3)s. The t0⊗s34 term is total spin1, orthogonal to both code singlets. Leakage is exactly4/9; an encoded-input leakage measurement gives half-diamond error at least4/9 against exchange-only target. This does not violate an endpoint symmetry promise. It refutes promotion of that promise to simultaneous continuous protection without further acquisition/assumptions.

2. **Conditional continuous protection is correct.** In the stipulated instantaneous collective frame, J_a P=0 and exchanges preserve P. The protected restriction of the joint Hamiltonian is Hc|P⊗I+I⊗HM. Its propagator factorizes even for noncommuting time-dependent bath coefficients and initially correlated logical/memory/reference states. This follows from invariant-sector restriction, not from commutation of arbitrary bath operators. The finite-memory theorem is standard. Logical S12=−Z, S23=(Z+sqrt(3)X)/2 and the simultaneous exchange X pulse were checked independently.

3. **Interfaces are not supplied by algebra.** Twisted exchange requires calibrated relative-frame interactions; learned endpoint frame coefficients do not acquire those interactions. The preparation/reset statements explicitly require singlet sources or measurement/feed-forward. Pair singlet measurement is logical Z, whereas code occupancy does not resolve the logical bit. Known-state preparation is not unknown-input loading. Calibration errors inside P can be logical errors invisible to membership tests.

4. **Independent-block distinction is essential.** Genuine at-most-three-spin cross terms cannot be invariant under both independent block SU(2) actions: a singleton spin in one block has no nonscalar invariant. This is the stated instantaneous commutant/support restriction, not a general no-go for mediated, effective or finite-noise gates. S12^A S12^B does implement protected ZZ. Actual boundary exchange in the independent test leaks product-code probability0.0697956 at angle0.31; global singlet preservation does not suffice for independent block baths. Standard exchange-only DFS universality under broader/global collectivity does not discharge this interface.

5. **Bus operator identity is correct.** F is bounded and commutes with the oscillator. H=omega(a+F/omega)†(a+F/omega)−F²/omega is a direct sum of displaced harmonic oscillators. At2pi/omega, its propagator is exp(i2pi F²/omega²)⊗I. The cross term is exp(i4pi gA gB SA SB/omega²); gA=gB=omega/4 gives logical ZZ anglepi/4. This is an operator identity, hence remains true on all initial logical/bus/reference correlations, not just a thermal product state. The ideal forced oscillator is self-adjoint by displacement conjugation.

   **Domain qualification:** extending this to arbitrary oscillator-valued collective bath coefficients requires a well-defined self-adjoint evolution whose domain reduces the protected sector. Arbitrary unspecified unbounded operators do not automatically define a Hamiltonian sum. The claimed arbitrary-state ideal bus identity needs no such additional bath terms. Bath-only evolution must exclude uncontrolled mediator interactions as the author states. With a valid block-reducing joint evolution, collective terms vanish on the protected block and the stated extension is correct.

6. **Robustness and error budgets are properly conditional.** The Duhamel bound min(1,integral||DeltaH||) is valid for bounded perturbations relative to the same collective bath. It does not certify unknown residuals or oscillator timing errors in ordinary operator norm. The exact relative-frame exchange difference is2sin(phi/2), checked algebraically and numerically. The thermal product coherence formula is correct. Nonzero residual displacement has no arbitrary-energy uniform small-error guarantee: a quadrature-squeezed state can have displacement overlap exp(−|delta|² e^(2r)/2)→0 as r→infinity. Such states have unbounded growing mean energy. This is a genuine missing energy/control contract, not evidence that a physical finite-energy device necessarily fails.

## Executed independent checks

Author scripts were copied to `replay/`; originals were not executed in place or altered. Both replay outputs agree numerically. The author's control script comment says two segments, but its actual bath example is one segment; the theorem does not rely on this comment. Our independently implemented program tests three distinct time segments with a three-dimensional noncommuting bath.

`INDEPENDENT_CHECKS.json` records:
- exact symbolic two-spin counterexample identity;
- three-segment full encoded operator factorization residual2.19e−15;
- actual eight-spin logical ZZ residual1.12e−15;
- cross-block exchange product-code leakage0.0697956;
- oscillator cutoff60, all input levels0–5: full-loop operator residual5.89e−15;
- logical/oscillator/reference-correlated vector residual3.52e−15;
- thermal coherence formula difference8.22e−15 at mean occupation0.8 and duration2pi+0.13.

The oscillator cutoff results are finite numerical diagnostics only. The displacement proof, not truncation, establishes the infinite-mode identity. Independent code uses explicit permutation matrices rather than the author's Pauli-sum swap implementation.

## Primary-source comparison

Primary manuscripts were read directly. [Kempe–Bacon–Lidar–Whaley](https://arxiv.org/html/quant-ph/0004064), especially sectionIV and strong-collective control/preparation sections, establishes the conventional DFS/exchange framework and distinguishes endpoint preservation from protection throughout switching. [Harvey et al.](https://arxiv.org/html/1801.04858), sectionII and AppendixB, supplies the longitudinal geometric-phase-gate antecedent and explicitly retains then approximates away a number-dependent coupling. [Ruskov–Tahan](https://arxiv.org/html/2010.01233) discusses encoded-spin longitudinal gates with resonator and charge-noise costs. [Sala–Danon](https://arxiv.org/html/1702.01650v2) supplies a four-dot singlet-only proposal with microscopic orbital, initialization and readout assumptions. None acquires the current unknown-frame pair-exchange oscillator interface. The same supplied controls benefit an equally informed conventional architecture; no special Astra performance advantage follows.

## Acceptance boundary

Accepted: exact endpoint/control counterexample; conditional exchange and bus constructions; scoped low-support obstruction; quantitative conditional perturbation bound; explicit missing physical interfaces and energy-sensitive nonclosure. Not accepted: experimentally calibrated controls, protection under arbitrary unknown noncollective noise, automatic extension of endpoint learning to generators, a fault-tolerance threshold, hardware advantage, universal unknown-input loading, or uniform bus robustness without energy/state bounds.
