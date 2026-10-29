# Interaction-assisted boundary discovery: primary-source comparison

29 October 2026. Focused literature check; not an exhaustive novelty clearance. No
claim that any cited theorem directly proves the present CTMC counterexamples.

## Result first

**Interactions as extra inverse information are an established mechanism.** The
most direct quantum-walk predecessor already uses a spatially uniform on-site
contact interaction, not a programmable hidden-state projector, and observes a
fourth-order distinction in one example. Nonlinear inverse-boundary problems
have a mature, stronger version of the same acquisition idea: interacting waves
produce information inaccessible to first-order response. Therefore a new CTMC
pair separation is a useful physical-access diagnostic but not, by itself, a new
flagship discovery principle.

The present parent's stronger constructions have a clean role in this context:
* Exclusion can break the saved single-particle similarity family.
* Nevertheless a degree-one port feeding a uniformly attached hidden module
  remains exactly lumpable at every occupancy, independently of internal rates.
* Uniform two-replica contact on a circulating module can measure relative motion
  while being blind to common circulation, hence cannot universally bound hidden
  entropy production.
These are direct operational no-gos in the proposed acquisition model, not
conclusions imported from graph-isomorphism papers. They defeat a universal
boundary-only reconstruction promise despite authentic bulk interactions.

## 1. Closest interaction mechanism: Gamble et al. (2010)

**Source:** John King Gamble, Mark Friesen, Dong Zhou, Robert Joynt and S. N.
Coppersmith, *Two-particle quantum walks applied to the graph isomorphism problem*,
Physical Review A **81**, 052313 (2010),
[primary paper](https://arxiv.org/pdf/1002.3003),
[journal record](https://doi.org/10.1103/PhysRevA.81.052313).

Read: model and Green-function setup; Sections V–VII, especially Eq. (32) and
Fig. 3 / Eqs. (33)–(37), PDF pp. 9–10. Their Hamiltonian contains a hopping term
and uniform double-occupancy penalty `U R`, with `R = sum_i |ii><ii|`.
Noninteracting two-particle walks fail on certain strongly regular graph pairs;
interacting bosons distinguish every tabulated pair they tested. One diagnostic
first differs at fourth order in time; some larger cases require sixth order.

**Comparison:** local contact is already an accepted physical-coordinate
reference that need not address each hidden vertex. But their data comprise
Green functions across the two-particle basis, assembled into graph invariants,
not a single controlled boundary detector. They test graph distinction with
known graph inputs, not blind parameter acquisition or noisy boundary inversion.
A fourth-order gap in the CTMC task is not an independent new mechanism.

## 2. Fixed-particle universality fails: Smith (2010)

**Source:** Jamie Smith, *k-Boson Quantum Walks Do Not Distinguish Arbitrary
Graphs*, [primary preprint](https://arxiv.org/pdf/1004.0206), 1 April 2010.

Read: full five-page paper, especially Sections V–VI, Lemmas 4–5 and Theorems
2–3. The model includes uniform interaction penalties determined by occupancy
patterns. Cellular-algebra k-equivalence preserves the required kinetic and
interaction operators. Nonisomorphic k-equivalent graphs therefore have equal
Green-function multisets for the interacting k-boson walk; such graph pairs
exist for every fixed k.

**Comparison:** this blocks the inference “two-particle examples separate, so a
fixed number of interacting particles must reconstruct every graph.” It is not
automatically a proof about labeled boundary ports, arbitrary boundary controls,
CTMC exclusion, contact-killing trajectories, or sample complexity. Extending the
algebra to marked ports and the exact controlled generator family would require
proof. The parent's explicit Markov lumping counterexample is more directly
applicable and needs no such transfer.

## 3. Nonlinear Calderón: actual stronger acquisition theory

**Source:** Matti Lassas, Tony Liimatainen, Yi-Hsuan Lin and Mikko Salo, *Inverse
problems for elliptic equations with power type nonlinearities*, Journal de
Mathématiques Pures et Appliquées **145**, 44–82 (2021),
[author-hosted primary PDF](https://users.jyu.fi/~salomi/pub/Calderon_elliptic_nonlinear_V16.pdf),
[arXiv record](https://arxiv.org/abs/1903.12562).

Read: introduction, Theorems 1.1–1.3, higher-order linearization identity and
method (PDF pp. 1–7). For a semilinear elliptic model, mixed derivatives of the
nonlinear Dirichlet-to-Neumann map yield integrals of products of internal
solutions against unknown coefficients. Their completeness arguments give
uniqueness in regimes where corresponding linear problems were unresolved.
One theorem simultaneously recovers a two-dimensional manifold, conformal
geometry and coefficient up to the stated gauge.

**Comparison:** the bulk local nonlinearity is intrinsic to the PDE, not an
interior sensing oracle. However they require a rich boundary function-to-flux
map, regularity/geometry assumptions and arbitrary sufficiently small boundary
sources. One physical scalar port does not supply that map. Differentiating
finite noisy data and synthesizing spatially diverse fields incur costs not
removed by the uniqueness theorem. Any claimed finite-network breakthrough must
compare its reachable product algebra and stability against this incumbent.

## 4. Nonlinear wave interaction creates interior information without sensing it

**Source:** Yaroslav Kurylev, Matti Lassas and Gunther Uhlmann, *Inverse problems
for Lorentzian manifolds and non-linear hyperbolic equations*,
[primary PDF, arXiv v4](https://discovery.ucl.ac.uk/id/eprint/1462501/1/1405.3386v4.pdf),
[arXiv record](https://arxiv.org/abs/1405.3386).

Read: introduction / active-measurement setup and method overview; not a full
audit of all microlocal proofs. Sources and observations are restricted to an
open neighborhood of an observer's path. Interactions among distorted wave
packets produce new singularities that allow recovery of topology,
differentiable structure and conformal metric in an appropriate causal region.

**Comparison:** this is a direct predecessor to “use natural interaction as an
internal marker while retaining external access.” It does not assume known
interior projectors. Its source family, hyperbolic propagation, smooth
spacetime and causal accessibility are substantial structure, and the accessible
open region is not a single scalar gateway. The relevant unmet burden here is
not to reannounce interaction-generated information but to acquire enough of it
with a genuinely smaller interface and controlled statistical cost.

## 5. Indirect Hamiltonian identification: topology matters

**Source:** Daniel Burgarth and Koji Maruyama, *Indirect Hamiltonian
Identification through a small gateway*, New Journal of Physics **11**, 103019
(2009), [primary PDF](https://arxiv.org/pdf/0903.0612),
[journal record](https://doi.org/10.1088/1367-2630/11/10/103019).

Read: full five-page preprint, especially setup, infection criterion, tomography
and efficiency. A known spin graph with specified Heisenberg-type interaction
and known anisotropy is reconstructible from an infecting accessible set. The
proof propagates known spectral information along uniquely exposed neighbors;
local tomography supplies the spectral data. Efficiency requires negligible
localization, and near-degeneracies can impair resolution.

**Comparison:** boundary-only learning is not new, nor are structural access
criteria. The saved graph's single gateway infects its neighbor but then meets
multiple hidden neighbors, so this sufficient condition stops. Assuming an
infecting topology or controllability certificate would be a genuine restriction,
not an information acquisition obtained automatically from exclusion. Conversely,
the work does not establish that every noninfecting model is unidentifiable.

## 6. General similarity-equivalence framework

**Source:** Daniel Burgarth and Kazuya Yuasa, *Identifiability of Open Quantum
Systems*, [primary PDF](https://arxiv.org/pdf/1401.5240) (2014).

Read: introduction and framework statement. Under an appropriate rank condition,
input-output experiments identify Markovian models up to similarity. Additional
known preparations, observables or dynamics determine what remains ambiguous;
similarity need not collapse to unitary equivalence in the general setting.

**Comparison:** adding a known physical interaction should be analyzed as reducing
the joint input-output equivalence class. Showing that the obvious tensor-lift
of a one-particle gauge fails is not sufficient: one must rule out other
similarities, smaller accessible quotients or lumpings. The degree-one uniform
module counterexample is exactly why a residual-equivalence test is essential.

## 7. Classical random-walk boundary inverse problems

**Source:** Victor de la Peña, Henryk Gzyl and Patrick McDonald, *Inverse problems
for random walks on trees: network tomography*, Statistics & Probability
Letters **78**, 3176–3183 (2008),
[primary preprint](https://arxiv.org/pdf/math/0610821).

Read: abstract, introduction and Theorem 1.1. On a known finite rooted tree,
augmenting leaves with suitable chains and observing joint first-hitting time and
place at two boundary layers allows recovery of transition probabilities.

**Comparison:** single-particle stochastic boundary reconstruction already works
with sufficient geometric access. It pays for distinct boundary destinations
and an augmented known tree; it is not one-port universal recovery. An interaction
proposal must be compared with this honest alternative: whether the same hardware
budget is better spent on more boundary channels, rather than assuming they are
forbidden while declaring the interaction capability free.

## 8. Current discrete partial-observation gauge result

**Source:** Giovanni Covi and Matti Lassas, *An inverse problem for fractional
random walks on finite graphs*,
[primary v2, 10 April 2026](https://arxiv.org/html/2408.05072v2),
[DOI](https://doi.org/10.1088/1361-6420/ae5c2f).

Read: introduction, Theorem 1.3 and Section 4. In the stated full-cross-block-rank
regime, boundary blocks of the first three powers characterize the transition
matrix up to hidden-block similarity; higher powers add no information. Their
current abstract carefully separates this gauge reconstruction from recovering
geometry once the transition matrix is known. The v1 indexed abstract uses a
stronger-sounding reconstruction phrasing; use v2 for claims.

**Comparison:** this supports treating hidden similarity as a real inverse-problem
object rather than a numerical fitting pathology. Their cross-block rank premise
requires enough observed vertices and does not cover a large hidden module behind
one degree-one port. Their fractional graph model also differs from local CTMC
exclusion. No interaction result is claimed in this source.

## 9. Exclusion-process inverse fitting is not boundary acquisition

**Source:** Luca Ciandrini, Richmond L. Crisostomo and Juraj Szavits-Nossan,
*TASEPy: a Python-based package to iteratively solve the inhomogeneous exclusion
process*, SciPost Physics Codebases **22** (2023),
[primary preprint v3](https://arxiv.org/pdf/2308.00847),
[software repository](https://github.com/ExclusionProcess-tools/TASEPy).

Read: model, power-series overview and Section 5.2. This supplies an exclusion
forward solver and conventional constrained fitting of spatial hopping-to-input
rate ratios from the full local stationary density profile on a known chain.
Dimensionless densities alone do not identify the absolute time scale.

**Comparison:** it is a competent numerical incumbent if those interior profiles
are supplied, but not a solution to the requested boundary-only acquisition.
It also illustrates why fitting a nonlinear exclusion forward model does not,
by itself, establish structural identifiability or new information access.

## Physical capability ledger and decision standard

These are deductions for the present task, not claims borrowed from a source:

1. If hidden CTMC labels are actual one-occupancy sites and particles can traverse
   the same specimen, hard-core blocking is a plausible fixed bulk law independent
   of our knowing site labels. No hidden-basis projector need be delivered to the
   receiver.
2. If hidden labels are metastable conformations, unspecified mesostates, or an
   algebraic realization, “exclude matching hidden states” is not a free natural
   interaction. A mechanism that recognizes equal hidden labels may already be
   the missing coordinate capability. Reject that implementation until acquired.
3. Uniform contact on actual co-located particles similarly supplies a physical
   equality relation, not programmable site addressing. Its spatial uniformity,
   effect on hopping, reaction products, rate calibration and detectability still
   need independent qualification. A formula containing a diagonal coincidence
   operator is not experimental qualification.
4. Classical hard-core particles, noninteracting fermions and interacting bosons
   are not interchangeable models. The stochastic exclusion diagonal compensates
   for blocked jumps; quantum hopping amplitudes and interference differ.
5. Full two-particle transition matrices, arbitrary interior initial pairs, known
   contact projectors in a reconstructed hidden basis, or a rich boundary DN map
   must not quietly enter the receiver. They would change the acquisition problem.
6. The right target is a class-specific reconstruction theorem with verified
   boundary preparation/observation, residual-equivalence characterization and
   conditioning/sample bounds. A finite separation example plus generic Jacobian
   rank does not supply that theorem.

**Literature-search limitation:** this focused pass found the comparators above,
but no primary result directly matching arbitrary weighted local CTMCs learned
from a single boundary via two-particle exclusion/contact. That absence is not a
novelty claim. The parent's exact universal counterexamples already justify
rejecting the broad flagship, independently of whether a class-specific niche is
unpublished.
