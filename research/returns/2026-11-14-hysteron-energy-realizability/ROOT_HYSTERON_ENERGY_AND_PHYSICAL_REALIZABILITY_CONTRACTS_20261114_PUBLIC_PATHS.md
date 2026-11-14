ROOT: ENERGY, DIRECTED THRESHOLDS, AND REALIZABLE MATERIAL HISTORIES
14 November 2026 Brisbane. Bounded original derivations, not a new physical law.

1. Actual primary constructions and source boundaries

Paulsen, Mechanical hysterons with tunable interactions of general sign (2026),
https://pmc.ncbi.nlm.nih.gov/articles/PMC13070039/
DOI 10.1038/s41467-026-70913-2. Actual main Introduction/Results/Discussion/Methods
through lines 214 read, including Eqs.1-7. The constructed platform uses pivoted
rigid bars, hard angular stops, linear driving/coupling springs, bearings and a
shared translating rod. The source actually realizes latching, counting and a
four-hysteron period-two response. Its last construction was tuned iteratively;
its Discussion leaves general realizability and larger-system design open.
The small-angle mapping and arbitrary-angle mapping have different assumptions.
This is an existing physical construction, not a new ROOT invention, automatic
learning law, durable miniature material, full-cost advantage or useful factory.
SI, movies, source data, code and cited originals were not followed or executed.
No failure occurred for this source in this review.

Teunisse--van Hecke, Transition Graphs of Interacting Hysterons: Structure,
Design, Organization and Statistics, exact https://arxiv.org/html/2404.11344v2 .
Actual abstract metadata verified v2/26 November 2025 before this versioned open.
Displayed artifact header agrees. Actual introductory/model passages through
approximately line146 and actual lines214-279 read; intervening passages and later
design proofs/statistics remain unread. The actual read scope includes n*2^n
relevant switching fields, Theorem1.1's scaffold/avalanche restriction, ill-defined
constant-drive cycles and races, and initial/final design inequalities. The
source already treats transition-graph synthesis as an inverse problem and
explicitly identifies the missing energy/dynamics of unconstrained thresholds.
It does not supply cheap growing-family physical synthesis. No PDF, other version,
code or cited original was followed. No failure occurred for this identity here.

Shohat--van Hecke, Geometric Control and Memory in Networks of Hysteretic Elements
(2025), exact https://slam-leiden.nl/Publications/2025/HeckePRL/PhysRevLett.134.188201.pdf .
Initial actual main pp0-1/lines0-164 read: bilinear elements, slow overdamped drive,
freezing the discrete state before solving force balance, geometric mapping and
its stated limits. FIRST governing followup at line155 returned400 Timeout.
SAME identity/DOI10.1103/PhysRevLett.134.188201 is HELD against further navigation,
retry, other author/publisher/arXiv/provider/version/title/PDF/SI/image/export
recovery. Later formulas, detailed examples and conclusions are not premises.
Failure is an access observation, not negative scientific evidence.

2. A restricted mapping retains an integrability constraint

Write the ACTUALLY READ Paulsen small-angle Eq.6 form as
  J_ij = g_ij k_ij C d_j / k_i,
where d_i=theta_i^+-theta_i^->0, C=ell^2/L is common, and the assumed equal-pair
coupling has k_ij=k_ji and g_ij=g_ji. Setting w_i=k_i*d_i gives
  w_i J_ij = g_ij k_ij C d_i d_j = w_j J_ji.
Thus unequal J_ij and J_ji need not signal an active or energetically inconsistent
physical interaction. They can arise from the unequal normalization of state
spans and drive sensitivities. Positive diagonal rescaling makes THIS matrix
symmetric. An overall dimensional constant can rescale w; no source-measured
energy or installed work map is thereby acquired.

For any supplied real zero-diagonal matrix J, positive w satisfying w_i J_ij=
w_j J_ji exist exactly when (i) support is symmetric, (ii) each nonzero paired
entry has the same sign, and (iii) the products along every graph cycle agree
with the reverse products. Necessity follows by multiplying the weight ratios.
For sufficiency, assign one root weight per connected component and propagate
the positive ratios along a spanning tree. Cycle consistency makes every
non-tree edge agree. A sparse graph traversal uses O(n+m) ratio/comparison
operations after its entries are supplied; rational bit lengths must be paid.
The present dense executable scans all n^2 entries, so it claims no sparse-input
implementation speedup or acquisition of inaccessible physical coefficients.

This constraint belongs to the stated mapping. Finite-angle, state-dependent,
nonpairwise or hidden-coordinate mechanisms can escape it. It is neither a
refutation of the actual experimental paper nor a universal passive-material
realizability theorem.

3. An exactly quantified mismatch

INTRODUCED three-bit matrix:
  J = [[0,1,1],[1,0,1],[2,1,0]].
Its directed triangle product ratio is2, excluding positive symmetrizing weights.
If every nonzero entry may change independently within relative error epsilon,
balancing that triangle requires
  2*((1-epsilon)/(1+epsilon))^3 <= 1,
so epsilon >= (2^(1/3)-1)/(2^(1/3)+1) = .11501333195111578.
This lower bound is attained by reducing each forward entry and increasing each
reverse entry by epsilon. In symmetric logarithmic entry error the minimum
radius is log(2)/6, with multiplicative factor1.122462048309373. These are exact
statements about this supplied matrix and error metric, not measured fabrication
error or evidence that no physical system can realize its input/output law.
Its40 introduced initial-state/drive relaxations exhibit no cycle; failure of
this particular energy representation does not by itself demonstrate failure
even of the abstract update dynamics.

4. A complete conditional dissipative update contract

INTRODUCED bits s_i in{-1,+1}, fixed drive H, offsets b_i, half-spans h_i>0,
and local fields L_i=H-b_i+sum_j J_ij*s_j. A bit flips only when
  s_i*L_i < -h_i.
Assume positive w and symmetric K_ij=w_i J_ij. Define
  E(s,H)=-sum_i w_i(H-b_i)s_i-sum_(i<j) K_ij s_i s_j.
For a single allowed flip,
  E(s^flip_i,H)-E(s,H)=2*w_i*s_i*L_i < -2*w_i*h_i.
Every asynchronous avalanche therefore terminates; its outcome need not be
independent of arbitration when several bits are unstable. A nonenumerative
energy-range upper bound is
  B(H)=2*sum_i w_i*abs(H-b_i)+2*sum_(i<j) abs(K_ij).
The number of flips is at most B(H)/(2*min_i(w_i*h_i)); the strict inequality
gives the corresponding integer refinement. For bounded degree, bounded weights,
fields and couplings, and positive uniform w_i*h_i, this is O(n) flips at ONE
fixed drive. It does not bound the length of a useful externally driven program,
physical settling time, preparation cost, or the lifetime of a physical memory.

The same nominal energy decreases if the switching local field has unknown
additive errors |e_i|<=epsilon_i<h_i: each flip decreases E by more than
2*w_i*(h_i-epsilon_i). Bounded row-sum errors in J and offsets can be included
in this epsilon budget. This is a sufficient bounded-error statement; thermal
activation with unbounded tails and arbitrary spontaneous flips are outside it.

For changes of H at fixed s, the formal model work is
  dW=-sum_i w_i*s_i*dH.
Adding that work to the energy released by flips closes the model's energy
ledger. It gives no measured mechanical joules, attainable pulse shape, useful
output or whole-device efficiency.

5. Why arbitrary directed threshold tables are not free physical machinery

INTRODUCED two-bit J=[[0,2],[-2,0]], b=0, h=1, H=0 gives the unique-unstable-bit
loop -- -> -+ -> ++ -> +- -> --. There is no tie-breaking ambiguity. A strictly
energy-decreasing autonomous realization with this as its COMPLETE fixed-drive
state cannot repeat that cycle. Active input or additional changing physical
state would have to be accounted for. This is an explicit example of the loop
problem already treated in the actual transition-graph primary source, not a
new general impossibility or evidence against all directed material behavior.

6. Executed bounded checks and remaining operation

ROOT_HYSTERON_ENERGY_AND_TRANSITION_REALIZABILITY_SCREEN_20261114.py and its JSON
are ROOT-owned standard-library artifacts. All numerical coefficients, drives,
spans and arbitration are INTRODUCED. Exact Fraction arithmetic verifies one
three-bit geometric-form matrix, both mismatch examples, and EVERY initial
configuration at five drives for n=4,6,8 bounded-degree energy families:1680
initial-state/drive cases, no repeated state, zero exact flip-identity error.
The maximum trajectory lengths are4,6,8 respectively. Four-step drive histories
return to their initial configurations and close formal work=dissipation at
73.6,115.2,150.4 normalized model units. These are finite diagnostics alongside
the conditional proofs; no physical operations, noise tests or production life
are represented.

A completely unconstrained n-bit threshold table already requires n*2^n relevant
entries:10240 for n10,20971520 for n20,43980465111040 for n40. Recasting that whole
table as a new language supplies neither a compact physical law nor a scalable
design method. The open operation is acquiring and composing physically
realizable laws while controlling representation size, uncertainty, dynamics
and useful consequences. Neither arbitrary tables nor this restricted quadratic
energy model close it. No general inverse construction, learning mechanism or
qualified material is supplied.
