# What the composition removes, and what capability is still missing

29 October 2026. Historical priority is UNKNOWN. Mathematical acceptance,
native implementation, initialization and useful hardware storage remain
distinct claims.

## Primary same-consequence controls

* [Alicki et al., 0811.0033](https://arxiv.org/html/0811.0033), Section II.1,
  already relates a virtual qubit and thermal ancilla to logical
  autocorrelations and average fidelity. Its exponential Dirichlet estimate
  uses the specified reversible generator structure. That principle is prior.
* [Bravyi--Terhal, 0907.2807v2](https://arxiv.org/html/0907.2807), Section 6,
  already supplies a full-qubit criterion for arbitrary stationary Lindblad
  noise, with protected observables/projector commuting with H. It requires
  no detailed balance and can obtain a linear bad-weight bound. Our receiver
  removes that exact commutation by paying a Gibbs twirl error and the full
  GNS generator defect; it is not stronger in the commuting case.
* [Balasubramanian--Davydova--Lin, 2605.10943v1](https://arxiv.org/html/2605.10943v1),
  Sections 3--5, supplies the actual 3D recursive code, decoder and unperturbed
  thermal memory. General existence of that memory is not the new result.
  Here the accepted check-soundness and central-polymer bridge allow the
  actual Gibbs state of weak local noncommuting H perturbations, with the
  same decoder, to enter a qubit-memory receiver.
* [Chen--Kastoryano--Gilyen, 2311.09207v2](https://arxiv.org/html/2311.09207v2)
  supplies the exactly stationary noncommutative Gaussian sampler. Its
  coherent correction and Hamiltonian-dependent filters are preserved. We
  compose this known dynamical class with the static/decoder result; we do
  not invent a Gibbs sampler or infer a microscopic bath from it.
* [Thorngren, 2607.20605v1](https://arxiv.org/html/2607.20605v1) proves classical
  Wegner-gauge memory robust under diagonal perturbations, with a favorable
  temperature wedge. It is stronger than an analyticity statement and must
  be admitted as a memory comparator. It does not by itself protect an
  unknown quantum phase against coherent Hamiltonian perturbations.
* [Sengoku--Cao--Watanabe, 2610.27938v1](https://arxiv.org/html/2610.27938v1)
  treats noncommuting quantum perturbations of classical lattice-gauge
  models, with free-energy analyticity under a beta|g|e^(Cbeta J) condition.
  Its imaginary-time/cluster machinery is relevant prior, not a physical
  logical-coherence recovery theorem for this recursive code. The cited
  companion local-channel work is not silently upgraded to a thermal
  generator/storage theorem.
* [Drechsler--Oreg--Aharonov, 2610.05589v1](https://arxiv.org/html/2610.05589v1)
  supplies strong CSS quantum/classical equivalences for syndrome-based
  generators/channels and Pauli noise, and autonomous/Floquet constructions.
  Its stated scope and Section 1.8 separate general coherent Markovian noise.
  The new composition is not a replacement for those stronger operational
  results within their domain.

The removed restriction is therefore precise: on the supplied recursive
family, weak native noncommuting static perturbations need not preserve an
exact logical/Gibbs product structure, syndrome-diagonal dynamics, or
independent-Pauli jump decomposition. An H-dependent exactly stationary
quasilocal generator remains a load-bearing model input. No world-priority
claim follows from these bounded comparisons.

## The next consequential gate is a fixed-generator theorem

The present logical decoder is fixed, but both the CKG generator and thermal
ancilla are adapted to the actual H0+V. Its quantifiers do not give a
controller which works without learning V or retuning its coherent correction.
This distinction matters more than another finite value or a better constant.

A concrete next target is to choose one qualified local recovery generator
D_k^0 using the nominal H0,k, then prove an all-input bound on

    exp{t[-i[H0,k+V,·]+D_k^0+E_k]}

uniformly for an entire fixed-strength class of UNKNOWN bounded-local
Hamiltonian perturbations V and physically specified local dissipative
imperfections E_k. The same generator and preparation contract must precede
the choice of V. It need not have the perturbed Gibbs state as an exact
fixed point. A meaningful positive theorem needs a mechanism controlling
the decoder-bad probability along this nonstationary evolution, or an
alternative nonequilibrium protected subsystem, over the memory interval.

Merely quoting the static Gibbs bound is insufficient. Likewise the ordinary
diamond-norm Duhamel comparison only gives

    ||exp(tL')-exp(tL)||_diamond <=t||L'-L||_diamond.

With a constant per-site implementation error and O(n) sites, this bound
does not retain an exp(c n^alpha) interval. This is a limitation of that
generic comparison, not a no-go theorem for local fault tolerance or for a
better autonomous mechanism. Active fault-tolerant recovery and the admitted
syndrome-based/Pauli autonomous results must get the same hardware/control
access when comparing consequences.

Thermal initialization is a separate obstruction: exact mathematical
Enc(omega)=omega tensor tau_H does not supply an efficient native method for
preparing tau_H. The composition does not imply rapid cooling, and its long
logical-memory interval actually prevents the full stationary sampler from
being uniformly rapidly mixing over all logical initial states. A useful
physical operation needs a stated initialization strategy and its resources;
that debt is not hidden in the fixed-generator target above.

No new hardware experiment, claimed native robustness wedge, or practical
threshold is proposed on the basis of this theorem alone. The surviving
research question is a quantitative nonequilibrium protected-logical theorem
for one controller, rather than more precision on an H-adapted Gibbs model.
