# Prior and resource boundary

29 October 2026. New analytical work only; no Hamiltonian fixture, dynamics,
finite code level, clock spectrum or previous compiler is rerun.

The strongest ordinary route is not a global-operator-norm gadget theorem.
It is exact quasi-adiabatic spectral flow, positive local Hamiltonian
comparison, and the frustration-free BHM stability strategy. All three are
retained. A given gapped path alone still fails to establish arbitrary
perturbation stability, as the ordinary pinned-Ising counterexample shows.

The first interface missing from that route was an actual positive local
normal form for the frustrated clock endpoint. `PROOF.md` Sections 2--6
construct it. A blockwise common filter uses the already acquired gap
inside every syndrome. The CP martingale pays physical supports and local
vacuum annihilation without an exponential normal-order expansion. Large
excited-clock terms remain explicitly allocated to the clock penalty.

The second missing interface was the actual source's polynomial filling
bound rather than a stronger spatial Local-TQO assertion. Sections 7--8
replace that use in the BHM proof by an explicit polynomial-radius
localization and a convergent relative-form sum. This does not infer strict
spatial TQO-2. The argument is restricted to finite-dimensional spatial
growth and finite-range physical perturbations, or specified rapidly
spatially decaying perturbations. It is not the nonspatial k-local theorem
of Yin--Lucas.

Primary tools read for this construction:

* [Bachmann--Michalakis--Nachtergaele--Sims 1102.0842v2](https://arxiv.org/html/1102.0842v2),
  exact filter and uniform spatial quasi-locality. The usual projection
  theorem assumes an isolated global band; the proof here instead verifies
  its matrix-element identity separately in every conserved-symbol block.
* [Nachtergaele--Sims--Young 1810.02428](https://arxiv.org/html/1810.02428),
  interaction transformations, weighted integrals, composition and difference
  estimates for quasi-local maps. Their spatial decay estimates are used as
  such, not relabeled support-volume decay.
* [Michalakis--Pytel 1109.1588v2](https://arxiv.org/html/1109.1588v2),
  filtered globally block-diagonal Hamiltonians, relative form bounds and
  the gap bootstrap. Its displayed stronger Local-TQO condition is not
  asserted for the source family; Section 7 supplies the needed replacement.
* [Nachtergaele--Sims--Young 2010.15337v3](https://arxiv.org/html/2010.15337v3),
  the general frustration-free BHM framework and explicit separation of
  local gaps, indistinguishability and positivity.
* [Yin--Lucas 2411.01002v2](https://arxiv.org/html/2411.01002v2),
  governing source of the accepted code-stability theorem and its actual
  check-soundness hypotheses. Its weighted support-volume perturbation
  norm is not acquired by a spatial spectral-flow argument.

Ring gadgets, weak-product expansions, and special exactly topological
two-body constructions remain credited in frozen `two_body_phase/`.
The present composition is not a novelty or priority clearance.

The new result is parameter-qualified. The old literal `lambda_*` was
selected to pay the syndrome-energy remainder; it was not selected using
the new martingale constant. The new sufficient choice is

    0<lambda<=min(lambda_*,rho/2,1/(2 Cmart)),
    Delta=1/(4lambda^L).

`Cmart` is a convergent sum of ordinary fixed filter/LR majorants and fixed
geometric constants. The proof establishes that it is finite and uniform
in N. No numerical `Cmart`, physical perturbation threshold, or new literal
clock parameter is evaluated. The penalty is constant in N but can be even
larger than the already prohibitive frozen compiler example. Neither the
two-body-qubit conversion nor hardware preparation/calibration is supplied.

The mathematical receipt is a theorem-level construction and its quantified
remaining numerical parameter boundary. No finite simulation can replace
that proof. No finite-temperature lifetime or open-system claim is made.
