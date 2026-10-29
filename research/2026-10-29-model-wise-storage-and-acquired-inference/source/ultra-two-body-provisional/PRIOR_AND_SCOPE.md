# Strong ordinary comparison and surviving boundary

The full proof and actual construction are in `PROOF.md` and
`CLOCK_HAMILTONIAN.json`. This note is a scope comparison, not priority
clearance. No theorem is inferred merely from a paper's title or abstract.

* [Bravyi--DiVincenzo--Loss--Terhal0803.2686v1](https://arxiv.org/html/0803.2686v1),
  Theorem1, already obtains O(N)-qubit two-body simulators with strength
  independent of N at fixed precision. The guaranteed error there is an
  extensive ground-energy error. It does not directly supply the weighted
  local-norm ground-phase identity needed here.
* [Bravyi--DiVincenzo--Loss1105.0675v1](https://arxiv.org/html/1105.0675v1),
  Section4, supplies the ordinary local SW and linked-cluster toolbox.
  Finite-order locality does not remove the excited-ancilla conditioned
  terms or isolate the entire vacuum band at constant penalty.
* [König0901.1333v2](https://arxiv.org/html/0901.1333v2) supplies the ordered-
  product clock mechanism. Its several-clock extension explicitly leaves
  a size-independent convergence criterion open. The Pauli simplification
  used here is stronger than treating general noncommuting link operators:
  mixed words can only create scalar signs and whole-check products.
* [Ocko--Yoshida1107.2697v1](https://arxiv.org/html/1107.2697v1) already obtains
  exactly solvable, uniformly gapped two-body toric/quantum-double models
  locally connected to their targets. It also charges composite particle
  dimensions. Thus neither first two-body topological order nor first
  exact logical degeneracy nor first local phase transfer is claimed here.
* [Brell--Bartlett--Doherty1407.4829v2](https://arxiv.org/html/1407.4829v2),
  Theorems6--8 and SectionV, proves effective-parent phase results with
  isometric/quasi-injective PEPS and topological-order hypotheses. Its base
  model is two-body on code gadgets, not automatically on the individual
  virtual particles (SectionVI.1). We have not supplied those PEPS/LTQO
  hypotheses for the RX/RZ family, and do not use this theorem as a free
  family-admission or full-simulator stability premise.
* [Harley et al.2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11297168/)
  shows important scalability barriers for stronger analogue-simulation
  encodings. Our path transports the ground phase, not the whole extensive
  code spectrum as one isolated low-energy band. No claimed violation of
  their energy-scaling theorem is involved.
* [BDL0707.1894v1](https://arxiv.org/html/0707.1894v1) gives the controlling
  product-ground-state KT, spectral-gap and linked-cluster priors. The
  proof here explicitly extends the elementary coefficient estimates to
  finite-body, bounded-dimension, inhomogeneous clock interactions and a
  commutative coefficient algebra. It does not silently import a two-qubit
  theorem for a many-body clock model. Yarotsky's
  [math-ph/0412040v1](https://arxiv.org/html/math-ph/0412040v1) states a
  translation-invariant lattice setting; that restriction is not silently
  removed either.

The positive general construction is a fixed-resource Pauli-clock uniform-
gap and local gapped-path theorem. Its historical novelty is UNKNOWN. The
native compiler consumes the retained code description, rather than a
fresh manufactured small-matrix fixture. The code does not certify the
general theorem by its one execution; the operator and KT proofs do that.

The originally requested FULL small-error identity remains NOT_ACQUIRED.
For the symmetry-preserving dressing supplied by this clock/SW route, the
ancillary-trace obstruction in Section8 rules out an arbitrarily small
weighted error. The required replacement is a real relative-defect/local-
parent stability theorem, or a different all-sector simulator/dressing.
No claim is made that such a theorem is impossible. A quasi-local ground-
phase unitary alone does not control the support-volume norm of arbitrary
physical perturbations. Two-body qubit locality remains another unpaid gate.

Actual construction costs: one deterministic compiler pass took0.1532s after
imports, with no trajectory, matrix diagonalization or new replacement step.
It emitted11424 hopping terms for1336 data qubits and1428 eight-level clocks.
Uniform-family strengths require a9554-bit penalty numerator, constant in N
but physically prohibitive. All proof, source-reading and existing code-
family/geometric acquisition costs are additional. No practical gain,
initialization, noisy calibration or thermal lifetime is claimed.
