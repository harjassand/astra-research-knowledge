# Independent review: interaction-assisted boundary diagnostic

29 October 2026. Reviewer read and replayed `exact_counterexamples.py` and
`finite_boundary_tests.py`, then wrote independent symbolic tests in
`independent_review_checks.py`. This review concerns the specific generators,
observations and claims below, not apparatus validation or novelty clearance.

## Verdict

**PASS after one implementation repair, with essential scope qualifications.**
The saved pair is genuinely separated by classical exclusion. The finite-source
protocol removes the instantaneous pair-preparation idealization. The local
six-rate rank calculation is exact. More importantly, the degree-one hidden
module gives an exact all-control exclusion no-go; a distinct contact quotient
gives an exact two-particle no-go even with separately controlled/labeled boundary
sources and separately recorded contact reactions.

No scalable reconstruction, global uniqueness, reliable finite-sample estimator,
or physical bulk calibration follows. Nothing in these checks supports treating
an arbitrary latent CTMC coordinate as a physical exclusion site.

## 1. Replay results and repair

Initial independent execution of `exact_counterexamples.py` failed at the
contact diagonal modification: SymPy's `kronecker_product` returned an immutable
matrix. This happened *after* the exclusion quotient check, but *before* the
contact verification. The producer was notified and wrapped the product in
`s.Matrix(...)`. No mathematical generator was changed. The repaired producer
script replayed successfully; output is `review_counterexample_replay.json`.

`finite_boundary_tests.py` replayed without modifications. Exact output saved in
`review_finite_replay.json` verifies:

* Vacuum + finite two-particle source, `r=1/10` versus equilibrium: derivatives
  through order six agree; the seventh difference is exactly **−9/25**.
* From the idealized pair `{0,1}`, `r=1/5` versus `r=4/5`: first difference at
  derivative five, **−69/5**.
* The same pair of rates with finite source: first difference at derivative eight,
  **−171/5**.
* At positive interior rate vector `(1,2,1,3,2,3)`, the cap-two boundary-occupancy
  moments of orders **4,5,6,7,8,9** have six-by-six parameter-Jacobian determinant
  **65586**, exactly.
* The cap-one diagnostic found rank four through order 24. A finite truncation
  alone is not a proof that every later moment has rank four; the single-particle
  similarity obstruction is the relevant structural reason for nonidentifiability.

Independent symbolic `r` calculations verify that the `{0,1}` pair's derivative
differences for `r` versus `1−r` are zero at orders 0–4 and exactly
**23(2r−1)** at order five. Rates must remain in the admissible positive interval;
not every formal `r` has physical meaning.

## 2. The finite boundary source is implementable without bulk counting

The cap-two generator adds a particle at site 0 with rate one when site 0 is empty
and fewer than two have been supplied. In the diagnostic, extraction is off and
particle number is conserved after injection. Hence the condition `len(z)<2`
can be implemented by a **known boundary source inventory of two particles**:
it tracks its own successful emissions, not hidden occupancy. A sequential
emitter with the stipulated exponential waiting law and local occupancy blocking
implements the modeled transitions.

This interpretation must be explicit. An unlimited reservoir that somehow reads
the instantaneous total hidden occupancy and stops at two would be a hidden
sensor. That is not needed here. The source must have its release law, local
blocking and particle conservation independently qualified. The forward model
assumes known vacuum, ideal counting, no unobserved loss and exact CTMC dynamics.
Repeated runs can in principle reset by counting extraction of the known injected
inventory at the boundary, but neither reset-time bounds nor detector errors are
acquired by these calculations. Empty initialization is not established from a
finite period of observed silence.

The reported finite-time values are forward-model probabilities, not experimental
measurements or acquired moments. The Jacobian was computed using known symbolic
rates by the researcher, not supplied to a blind receiver.

## 3. Exclusion quotient proves more than equal moments

For the five-site counterexample, write the module as `M={2,3,4}`. Site 0 is a
physical degree-one gateway, linked only to connector 1. Connector-to-module and
module-to-connector rates are uniformly one. The projection is

    eta -> (eta_0, eta_1, k),   k = sum_{i in M} eta_i.

Every internal module jump preserves this projection. When connector 1 is empty,
exactly `k` particles can hop into it at rate one each. When it is occupied,
exactly `3−k` available module sites can receive that particle. Gateway motion
and reservoir injection/extraction depend only on `eta_0,eta_1`. Thus the
projected generator is independent of every internal module rate, not merely
of the two cycle parameters tested in code. This reasoning works at all particle
numbers and also with a boundary source/sink.

The symbolic identity `L P = P Lbar` is strong lumpability, where `P` is the
partition indicator matrix. It implies `exp(t L)P=P exp(t Lbar)`. Gateway
occupancy is constant on partition cells. The resulting quotient therefore
determines the **whole continuous boundary record**, not just one-time means.
The same identity holds for every boundary control value. Piecewise controls,
limits to admissible nonexplosive waveforms, and nonanticipating feedback based
on visible history consequently have the same laws in the two models. Initial
laws must have the same projected distribution; vacuum preparation has this
property. This is an exact obstruction, not a sampling limitation.

## 4. Contact quotient and independent boundary controls

The producer's two labeled walkers have independent kinetic generators and a
uniform same-site annihilation at rate `kappa`. Classify pair states by:

* both positions in `{0,1}` (retaining both labels);
* one position in `{0,1}`, the other somewhere in `M`;
* both positions in `M`, retaining only oriented separation `d=(j−i) mod 3`;
* annihilated.

With both walkers in the module, `d` increases at rate `u+v` and decreases at
rate `u+v`: a clockwise move of one walker is a counterclockwise relative move
of the other. Uniform connector entrances/exits have quotient rates independent
of absolute module positions. Contact depends only on `d=0`, or on the retained
outside pair coordinates. Consequently the entire quotient depends on `u+v`,
not `u−v`.

The independent reviewer first checked this with **separate `A1,B1,A2,B2` gateway
controls**, rather than the producer script's common `A,B`. Then a stronger
36-state model was constructed: each labeled particle may be absent or at one
of the five sites; absent particles are injected at 0 at separately controlled
rates `alpha1,alpha2`, particles at 0 can be removed at `beta1,beta2`, and a
reaction removes both particles. An 18-state quotient passed exact identities
**separately for the kinetic/source generator and the marked reaction generator**.
Thus even reaction event times may be granted to the observer without exposing
`u−v`; no direct interior reaction detector is required for the negative result.
Sequential finite-rate preparation, removal and reinjection at the boundary
respect this quotient. Results: `independent_review_results.txt`. The stronger standalone replay is
`audit_contact_source.py` with `audit_contact_source_results.json`, including
exact quotient matrices and separate injection, removal, gateway-jump and
reaction-mark intertwining checks.

Because the labeled gateway observations and event marks factor through the
partition, equality extends to full records and admissible adaptive boundary
policies, by the same controlled-lumpability argument. The extended model closes
the producer comment's unsupported leap from a fixed pair start to general
boundary injection/removal.

**Important exclusions:** the two particles must experience the same internal
`u,v`. Independently slowing, reversing, pausing or otherwise modulating one
particle's *bulk* dynamics is a different acquisition operation; it can expose
common drift through relative motion. Site-specific reactions or interventions
inside the module are likewise not covered. The contact counterexample does not
prove a no-go for every conceivable interaction law, all higher particle numbers,
or the combined hard-core-plus-contact operation. It proves failure of the
specified two-particle uniform-contact acquisition.

## 5. Hidden entropy production is unbounded despite fixed activity

At baseline `A=B=1`, the five-site single-particle process is balanced and has
uniform stationary mass `1/5`, independently of `u,v`. The three oriented module
edges each contribute `(u−v) log(u/v)/5`; gateway and connector edges have zero
stationary current. Hence

    sigma = (3/5)(u−v) log(u/v).

Along `u=2−epsilon, v=epsilon`, equilibrium occurs at `epsilon=1` and sigma
diverges as `epsilon` tends to zero. All **baseline individual off-diagonal
rates** are bounded by two. The JSON `rate_bound:2` should not be read as bounding
arbitrary applied boundary-control amplitudes or total exit rates. Uniform
stationary masses do not vanish. The contact quotient is fixed along this path;
the exclusion quotient is independent of `u,v` even without fixing their sum.
This is entropy of the underlying single-particle CTMC, not a thermodynamic
accounting of the added source, detector or contact reaction apparatus.

## 6. Classical exclusion is not a free-fermion exterior power

For an occupied pair `{i,j}`, classical exclusion retains only jumps into empty
sites and renormalizes the diagonal to minus the allowed outgoing rate. Its
diagonal is

    L_ex({i,j},{i,j}) = Q_ii + Q_jj + Q_ij + Q_ji.

The exterior-power lift has diagonal `Q_ii+Q_jj` and permutation signs on hopping
matrix elements. It is generally not a Markov generator. For the saved
four-state equilibrium example, the diagonal corrections in pair order
`01,02,03,12,13,23` are **2,0,0,2,4,6**. The reviewer also checked the hop
`{1,2}->{2,3}`: the exterior entry is `−Q_13`, while the exclusion entry is
`+Q_13`. Therefore exterior-functor covariance under a general similarity does
not establish covariance of this classical exclusion generator. Pauli exclusion
as a slogan is insufficient to identify these models. Likewise, the cited
quantum-boson contact results are comparators, not direct proofs for this CTMC.

## 7. Exact local rank is not global or scalable recovery

The nonzero determinant proves that the selected finite moment map is locally
invertible at the tested positive point. Because its entries are polynomials in
the six rates, a nonzero determinant at one point implies generic full local
rank off the corresponding algebraic zero set, **within this fixed four-site,
known-topology, known-boundary-rate model**. This does not imply global
injectivity, known hidden order, control of discrete permutations or other remote
solutions, stable derivative estimation, or a dimension-uniform acquisition
budget. High-order derivatives are not free boundary data. The exact source
probability difference is small in the displayed finite-time tests.

## Review scope and remaining blockers

The requested finite algebra and the specified all-control counterexamples are
verified. The initial code bug is repaired. The full-record claim is supported
by exact quotient identities, including independent boundary controls and
reaction marks in reviewer-added code. No hidden projector is required by the
mathematical exclusion/site-contact models, provided actual physical sites and
the stated bulk law exist. Whether a particular specimen realizes those sites,
unchanged hopping under loading, uniform contact and reliable boundary counting
remains unverified. That physical qualification is a real blocker to claiming an
acquired scientific capability, not an algebraic issue repaired by more fitting.
