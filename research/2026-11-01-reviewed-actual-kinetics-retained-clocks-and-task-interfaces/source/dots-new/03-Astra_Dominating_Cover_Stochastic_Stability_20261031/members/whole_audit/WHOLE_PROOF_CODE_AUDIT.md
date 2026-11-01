# Fresh whole-proof and independent-receiver audit: cover seed and preferred circuit

31 October 2026. Pure mathematical CTMC work, local files only.

## Verdict and exact scope

**SCOPED MATHEMATICAL PASS** for both separately frozen boundaries:

1. The eleven-file dominating-cover seed theorem and explicit-cover constructor.
2. The eighteen-file preferred circuit package, which preserves those original
   sources byte-identically and replaces only inventory acquisition/evaluation.

No substantive mathematical or implementation repair was needed. This is ordinary
proof/code review with independently written exact receivers, not proof-assistant
formalization. Neither preceding acceptance receipt was used as a substitute for
reviewing this new theorem or compiler.

The theorem establishes nonexplosion, full-orthant irreducibility, positive
recurrence and all finite exponential stationary total-count moments for arbitrary
strictly positive real rates in the specified binary hub/arm architecture whose
satellite graph has no induced triangle-plus-isolate or P4-plus-isolate.
Executable construction/receiving uses exact rational rates and rational t>1.

The preferred circuit acquires and evaluates the exact weighted-cover inventory in
polynomial graph/bit complexity. **The complete numerical profile, compensation
scan, rational certificate, N_* or expanded moment bound is NOT thereby proved
polynomial-size or polynomial-time in binary rate input.** The old explicit
constructor retains its exponential cover-mask cost. Budget refusals preserve
qualitative certification and do not assert instability.

No external retrieval occurred in this audit. The prior disclosed alternate-source
failure remains quarantined, not cleared or used as a significance premise. The
newly denied Citeseer source was not retried, mirrored or treated as verified; the
circuit proof is self-contained. No historical novelty, exhaustive prior-art,
general weak-reversibility or arbitrary conservative one-port conclusion follows.
All prior artifacts and both frozen source boundaries remain unchanged.

## Source binding and independently written code

Base author manifest, 11 files:
`1f9303143b0bae61b7066c2f3d8e8fbac564b76339fa91315ad291a3f85ff8a8`.

- Base proof: `e57b1150da2f65cd4ad4aa0cfc3fed1bc83e030d60f5165019a9a0d0dcc728dd`.
- Base constructor: `d91fdac93ceb6ebf6e21de8d028a4222135a3092897bb7bcda342e2b47609a63`.

Preferred circuit manifest, 18 files:
`64be3db4d97541eef968548572887f3f518c3e3343377a05c07e693ab26cb60d`.

- Circuit proof: `ee82fce51c6f6fe8dcbca83f8a5b58559dd9f688a2dca0ce437d0e2cf4456f0b`.
- Circuit constructor: `3c88da3dc4357cacef4eb4c0694edc9c5e557224b6661bd27b1468cb7bbefcb9`.

Every bound byte count and hash was verified. `SOURCE_BINDING.json` and
`CIRCUIT_SOURCE_BINDING.json` retain complete bindings. The preferred package's
`frozen_cover_source/` files match the original eleven sources and manifest.
Both complete proofs, all constructors and test drivers, READMEs, scope notes,
and actual outputs were read or replay-bound, not merely spot-tested.

This audit adds two independently written semantic receivers:

- `independent_cover_receiver.py` imports no candidate code. It independently
  parses/normalizes the raw network and graph, reconstructs all numerical fields,
  and generates minimal covers as complements of maximal independent sets.
  Its qualitative path never enumerates covers.
- `independent_circuit_receiver.py` imports only this audit's independently written
  parser/encoding helpers. It has its own breadth-first anti-neighborhood compiler,
  weighted evaluation, maximal witness construction, enabled-edge queries and full
  numerical reconstruction. It calls neither explicit-cover numerical constructor
  nor cover enumeration. All such entry points were disabled by throwing test
  sentinels during production tests.

The candidate's same-implementation receivers remain correctly labeled as author
self-checks, not independent validators. Generic parser scaffolding is standard
local reuse; no earlier stability theorem is assumed by either new receiver.

## Whole base theorem reconstruction

### 1. Structural recognition and the graph equivalence

The raw parser validates exact integer nonnegative complexes of fixed dimension,
strictly positive exact rates, the sole nonconservative pair 0↔A, and reversible
binary hub/active edges. Every square-free A-free hub has its own 2A amplification
pair, and every satellite has an arm. Duplicate directed channels are summed;
validated null channels are removed. Isolated hub-graph vertices remain included
as satellites and may have arms. This is not a supplied grouping or cover oracle.

For an inclusion-minimal cover C, each vertex of C has a neighbor outside C;
otherwise it could be removed. If an edge uv inside C fails to dominate some w
outside C, choose outside neighbors b of u and c of v. The outside set is
independent. A common neighbor, or a cross adjacency, gives an induced triangle
with w isolated. With neither, b-u-v-c is an induced P4, again with w isolated.
Conversely, extend the isolate together with the triangle's third vertex, or the
P4's endpoints, to a maximal independent set. Its complementary minimal cover
contains the offending edge. This proves the exact forbidden-pattern equivalence.

The degree tests used in code are sufficient: a four-vertex induced graph of
degrees (0,2,2,2) is triangle-plus-isolate; a five-vertex graph of degrees
(0,1,1,2,2) and three edges is P4-plus-isolate. The test is polynomial over the
explicit graph and does not enumerate covers. The class contains disjoint
bicliques with free vertices, complete multipartite graphs, P4 and C5; this is a
sufficient geometry, not a classification of stable networks.

### 2. Weighted-cover inventory, all ties, and bad edges

Because weights are nonnegative, a minimum-weight cover can be reduced to an
inclusion-minimal structural cover without changing its optimum cost. Let tau be
that minimum and R=A+tau. Every cover contains one or two endpoints of a hub.
Thus hub insertion/removal changes tau by one or two, while deleting one satellite
changes it by zero or one. Comparing each cover's net cost for an arm directly
gives forward ΔR∈{−1,0,1}; reverse arms have the same range. Amplification has
ΔR∈{−1,0} forward and {0,1} reverse. Core jumps change R by exactly ±1.

R=0 iff A=0 and the positive satellite support is independent. All internal sources
then vanish. Every internal destination contains A or a positive hub, so R≥1 is
internally invariant. This does not claim that R is numerically conserved.

On an enabled hub, removal lowers tau by two iff an old optimal cover contains
both endpoints. If a destination-optimal cover achieves a two-unit drop, its old
cost must equal tau and both endpoints must belong to it. Conversely such an old
cover attains the drop. Reducing an optimal nonminimal cover cannot remove a
positive-weight endpoint without lowering its cost below tau, so an optimal
minimal witness exists. Consequently good H→2A raises R by one and bad H→2A
leaves R fixed, exactly as claimed.

A reverse arm can decrease R only if tau drops by two; its destination-optimal
cover must have been optimal before the jump, contain both positive hub endpoints,
and omit the returned satellite. Thus the edge is bad. This argument retains all
optimal covers and all switches; a single arbitrarily selected cover would not
suffice. Inactive zero-product edges are irrelevant to the generator comparisons.

### 3. Heavy-bulk rate absorption and its sharp limited boundary

A heavy vertex has x_v>R≥tau, so it belongs to no optimal cover. Every edge
incident to a heavy vertex is therefore good. Fix a positive-product bad edge uv
and an optimal minimal cover witnessing both endpoints. By the graph condition,
each heavy w is adjacent to u or v. Selecting one such edge for each w produces
distinct good edges and gives

    Q_g ≥ H_B min(x_u,x_v),
    x_u x_v ≤ R min(x_u,x_v).

The endpoints are not heavy because they lie in an optimal cover. Summing this
bound over bad edges yields Q_b H_B≤|E| R Q_g. Zero-product edges cause no issue.
All nonheavy satellites and A contribute at most nR, giving H_B≥N−nR.
Hence in R≤delta N with delta≤1/(2n), H_B≥N/2 and
Q_b≤2|E| delta Q_g. No averaging, independent-event or stationary-fiber assertion
is hidden in this deterministic rate comparison.

The stated sharpness witnesses survive embedding in a larger graph: add all
zero-weight outside vertices to covers of the induced obstruction, then reduce
redundant vertices. Positive-weight minimizers cannot disappear. Triangle-plus-
isolate has (tau,Q_b,Q_g)=(2,3,0), and P4-plus-isolate has (2,1,2), with arbitrarily
large isolate count. Neither permits Q_b≤C(R/N)Q_g with fixed C. This is sharpness
of this particular small-cone absorption property only, never instability.

A heavy-consuming arm cannot decrease R. Covers omitting its consumed X gain at
least one unit; covers including X already cost at least tau+1 and have nonnegative
net change. Thus the new minimum is at least tau+1. Such capture has rate at least
k_- A H_B and reduces f=A/(R+1)^2 by at least 1/(R+1)^2.

One nonblocking editorial typo was found: the last sentence of Section 2 says the
adverse forward rate is “bounded below” in Section 3. The displayed and proved
bound there is an upper bound, K_f A R. No inequality or code is affected, and
frozen bytes were not changed.

### 4. The global quadratic packing bound

For any nonempty graph, greedily remove enabled edge pairs in batches equal to the
smaller residual endpoint count. At least one vertex saturates on each batch and
never becomes positive again, so the process terminates. Saturated vertices cover
the original graph; otherwise an edge with two positive residual endpoints would
remain. Their original weight is at most the total removed population 2K, so
tau≤2K. For each used edge, its original product dominates k_e². Cauchy gives

    Q ≥ Σ_e k_e² ≥ K²/|E| ≥ tau²/(4|E|).

Zero-count vertices may be included among saturated vertices at no cost. This
bound does not require the special graph condition and is not a matching oracle.

### 5. Profile acquisition and acyclic compatibility

R-decreasing forward arms can consume only nonheavy satellites, each of count at
most R. With at most m types and 2A capture included, their total rate is at most
K_f A R and hence K_f R². Other forward moves do not increase a decreasing profile.
All raw rate summaries are positive finite sums/minima with the stated conventions.

The backward denominators are positive because epsilon0<lambda+beta. The recurrence
multiplier exceeds one and joins exactly to g_K=1+c/K. On the tail, c/r≤1/2 and
r/(r+1)≥1/2 prove (5); the finite head gives equality. The lower slope bound d_* is
valid because tail (r+1)²d_r=c(r+1)/r≥c. G_* includes every finite ratio through
r=K; beyond that the exact tail ratio is (r+1)/(r−1)≤3. Thus adverse reverse moves
are paid at their actual profile slope, not at an assumed universal slope ratio.

D>0. The epsilon choice gives epsilon≤1/4,
epsilon(F+D)≤D/4, and epsilon mu≤epsilon0/4. J≥K+1 puts both neighbors in the
tail for r≥J and gives E_r≤−D/2, so E_r+epsilon(F+D)≤−D/4. The finite q scan
covers every remaining r<J, including last-seed extinction and d_0.

The dependency order is genuinely acyclic: raw quantities → profile and slopes →
epsilon/J/q → delta and N_*. Delta may be tiny and N_* huge, but no quantity is
required to be chosen smaller/larger than a function of itself. All constructions
exist mathematically for each fixed finite t>1 and positive real rate vector;
exact execution is restricted to rationals.

### 6. Both phase signs and actual physical core costs

For every enabled internal jump, |ΔA|≤2 and |ΔR|≤1, and direct subtraction gives
|Δf|≤11/(R+1)². The decrement estimate uses destination denominator R² and
2/R²+R[1/R²−1/(R+1)²]≤11/(R+1)². The bound also covers core death to R=0.
Heavy capture supplies the exact negative term; nondecreasing-R forward arms have
nonpositive f drift. The remaining forward and all reverse source rates yield (13).
Good amplification and adverse bad reverse arms give (14); neutral amplification
is dropped, not incorrectly credited as negative drift.

The positive phase's physical core generator changes both N and R denominators.
Its birth bound is the displayed q lambda[11t+(t−1)/4]/(N+1). Multiplying the death
increment by the actual rate mu A gives at most 11q mu/(4N) for its difference
term, hence 11q mu/[2(N+1)], and at most q mu/[4(N+1)] for the positive denominator
term. Their sum is below 6q mu/(N+1), so C_core's enlarged 12mu allowance is safe.
A=1 extinction is fully charged, not protected or deleted.

The negative phase uses the exact A-generator, with reverse coefficient s_H+b_H
because amplification creates two A's. Its internal contribution is bounded by
epsilon F A−epsilon b0 Q/(N+1). Immigration's scaled contribution is nonpositive.
For death, writing the scaled change as its ordinary ratio difference plus the
(1−1/t) term gives at most epsilon mu+epsilon D A. Keeping D rather than replacing
it by mu is essential near t=1. Together these prove (17), uniformly for every
fixed positive parameter choice.

### 7. Boundary cone: both adverse terms are separately paid

In N≥N_* and 1≤R≤delta N, delta≤1/(2|E|) gives Q_b≤Q_g, and the
b_-/(8|E|s_+G_*) condition pays bad reverse profile drift by one quarter of
b_-Q_g d_R. The threshold 88q s_+/(b_-d_*) pays the entire positive reverse-phase
cost by another quarter. The remaining half satisfies

    (b_-/2)Q_g d_R ≥ (b_-/4)Q d_R ≥ beta(R−A)²d_R.

Adding the exact base core drift, profile inequality, both phases and
R²−(R−A)²≤2RA yields master bound (18). H_B≥N/2 implies H_B/(N+1)≥1/4.
The acquired q pays A[E_R+epsilon(F+D)] in the finite head; its tail is already
negative. Each constant error is at most epsilon0/4. Thus scaled drift is at most
−epsilon0 g_R/2, and h≤g_R+1/4≤2g_R gives LW≤−epsilon0 W/4.

This is the substantive P4 join: small-R adverse cover-loss events need not vanish,
but their rate is dominated by good hubs with all slope/rate losses explicitly
charged. Slow positive-inventory clocks also remain possible and are paid by the
finite profile; no uniformly fast latent-clock claim is imported.

### 8. Interior, R=0 and the finite head

N≥K/delta and R>delta N imply R>K, so all neighboring profile terms are in the
tail. Internal profile increments are at most 2c/R²; the positive phase contributes
at most 11S/delta² internally and C_core through the core because q/(N+1)≤1.
Base immigration is at most 3L/2 and base death at most −DA+mu/2. Equation (17)
and epsilon(F+D)≤D/4 leave the enlarged interior bound (19).

If A≥R/2, physical death pays at least D delta N/4. Otherwise tau>delta N/2,
and the packing bound pays at least epsilon b0 delta² N/(32|E|). Kappa and N_*
therefore give scaled drift ≤−1. Active interior h≤3/2+1/4<2, so LW≤−W/2.
At R=0, internal sources/death vanish; the separately displayed immigration
formula, including both phase corrections, gives LW≤−lambda W/4. These regions
join at ζ=min(epsilon0,lambda)/4 with no uncovered state, tie or cutoff boundary.

Globally h≥3/4 and h≤H. In the finite exception, each internal propensity is at
most its rate constant times N_*², each core rate is bounded as stated, and each
destination has bounded h and count at most N_*+1. The factored C_F covers both
positive drift and ζW. The head has binomial(N_*+n−1,n) states; none are enumerated.

### 9. Nonexplosion, irreducibility and stationary moments

N(s)≤N(0)+Poisson(lambda s). Finite-horizon paths remain in finite count sublevels
with bounded jump rates, proving nonexplosion. Every satellite has a reversible
singleton path 0→A→2A→H→A+X→X, using an acquired arm. Nonnegative translations
preserve enabling, so concatenation creates/removes every vector and proves
full-orthant irreducibility, including free passengers.

Localized integrating-factor Dynkin and Fatou give the semigroup bound. Finite-
horizon integrability is also directly available from W≤Ht^N and the Poisson
bound, including polynomial total propensities. Normlikeness makes occupation
averages tight; the usual countable-state argument yields an invariant probability,
positive recurrence and uniqueness. Fatou on averages gives π(W)≤C_F/ζ without
assuming prior invariant-generator domain membership. The reported
π(t^N)≤2C_F/ζ is conservative but valid from h≥3/4. Repeating the mathematical
construction for each finite t>1 proves all exponential moments; tests at finitely
many t values are not that proof.

## Preferred circuit: additional whole review, not automatic inheritance

### 10. Anti-neighborhood decomposition and exact weighted inventory

For every anchor v, its anti-neighborhood U_v has no triangle or induced P4:
otherwise v supplies the forbidden isolate. A connected triangle-free/P4-free
nontrivial component is complete bipartite. A shortest odd cycle would be
chordless and of length at least five, supplying a P4, so the component is
bipartite. A missing cross-shore edge then has a shortest odd path of length at
least three, again supplying a P4. Singleton components are isolates. This is
an elementary proof and uses no inaccessible external graph-algorithm source.

An independent set containing v lies entirely in {v}∪U_v. On each biclique it
chooses one shore, and nonnegative weights allow all isolates and all vertices
of the chosen shore to be included. Taking the maximum over anchors yields exact
maximum independent-set weight, including all-zero weights because a nonempty
optimum can still be chosen. Complementation therefore gives exactly the same
minimum weighted-cover value tau as the base theorem, not a relaxation.

Choose an attaining anchor/shore set and greedily extend it to a maximal
independent set. Any addable vertex must have zero weight or optimality would
be contradicted. Its complementary cover is structural, inclusion-minimal, and
optimal. Both candidate and independent implementations explicitly handle these
zero-weight ties rather than returning an unjustified nonminimal cover.

### 11. Enabled-edge query and all optimal-cover ties

For an enabled edge ij, both endpoint weights are strictly positive. Zeroing them
can only lower the maximum independent-set objective. Equality with the original
optimum is equivalent to an original optimum avoiding both endpoints: remove
zeroed endpoints from a maximizing independent set without changing its modified
weight. Conversely an original optimum avoiding them retains its value.

Extend the avoiding optimum to maximality under the original weights. Neither
positive endpoint can be added, since it would increase the original optimum;
only zero-weight vertices can be added. The complementary minimal optimal cover
therefore contains both endpoints. This proves the query in both directions.
The positivity/enabling qualification is essential; inactive edges do not enter
Q_b or generator drift, and the implementation skips them. Querying a single
chosen cover instead would be incorrect at ties; the objective comparison properly
quantifies over all optimal covers.

### 12. Circuit cost, implementation and boundaries

There are m anchor records and O(m²) retained vertex occurrences. Anti-neighborhood
BFS and complete cross-pair verification use O(m³) graph work after the raw
O(m^5) forbidden-pattern test. Weighted evaluation costs O(m²) integer additions
and comparisons, with bit length bounded by weight-input bits plus O(log m).
Witness construction and all enabled-edge queries are also polynomial; the latter
uses O(|E|) evaluations of the same acquired circuit. No weighted optimization
oracle or cover collection is supplied.

The candidate compiler imports the frozen parser/scalar/profile helpers but calls
neither its cover enumeration nor its numerical constructor. Our separate receiver
uses its own parser and BFS circuit and independently reconstructs all scalar and
wire fields. The two constructions agree on the complete profile, constants,
Foster bound and moment bound: only inventory representation and its charged work
change. Scaled LW/t^N needs only t^(ΔN), ΔN∈{−1,0,1}, the circuit and exact rational
head/tail arithmetic. It is polynomial in the already materialized certificate
and binary state size; computing actual t^N need not be.

This graph improvement does not shorten K−1 backward steps or J−1 compensation
checks, control rational bit growth, make N_* small, or establish polynomial
complete numerical acquisition. The base constructor still enumerates 2^m masks;
the preferred production paths enumerate zero. Both budget meanings and distinct
receipt families are preserved rather than silently conflated.

## Exact execution, adversarial coverage and honest costs

All six published outputs replayed byte-identically with zero stderr: base demo,
base exercise, graph controls, author receiving controls, preferred demo and
preferred circuit exercise. `EXACT_REPLAYS.json` and `CIRCUIT_EXACT_REPLAYS.json`
record actual exit codes, timings, byte counts and hashes. The base exercise took
about 33.2 seconds and its receiving controls about 10.9 seconds on this environment;
these are measurements, not service or asymptotic guarantees.

Fresh base-receiver controls (`INDEPENDENT_RESULTS.json`):

- Six separately built P4/full-incidence, C5, house, star/free-passenger,
  three-disjoint-edges/free-passenger and permuted-P4 raw cases with unequal rates.
- 4,165 state checks, 33,325 internal jumps, 12,138 optimal-cover-set switches,
  1,891 optimal-cover ties, 98 adverse reverse-arm decrements and 362 last-seed deaths.
- 23,970 exact profile/phase points; 1,324 heavy-bulk comparisons; 840 outside-Foster
  checks, including 540 boundary and 210 interior states. R=0 is checked separately.
- All 1,094 nonempty graphs through five satellites compared against direct
  minimal-cover domination: 775 admitted. Another 13,128 random-weight packing
  checks and 6,558 heavy-bulk comparisons supplement the ordinary combinatorial proof.
- Twelve raw qualitative/numerical receipts, six duplicate/null normalizations,
  43 semantic mutations, 76 domain refusal calls and six exact-budget/extreme-budget
  controls. Throwing sentinels confirm qualitative and preflight refusals never
  enumerate covers in either implementation.
- mu=10^-5000, t−1=10^-200 and t=10^100 budget refusals retain qualitative success;
  they are not falsely advertised as cheap successful profile constructions.

Fresh preferred-circuit controls (`INDEPENDENT_CIRCUIT_RESULTS.json`):

- All 775 admitted small graphs, 177,021 weighted inventories/minimal witnesses,
  400,828 enabled-edge queries and 775 large-binary weight vectors agree with exact
  exhaustive comparators used **only in the small-graph test harness**.
- 252 scaled-generator equality checks; 120 qualitative coordinate permutations
  and four full numerical permutations. Twenty circuit/scalar/metadata/UNKNOWN
  corruptions are rejected, along with 40 invalid-domain calls and five explicit
  structural UNKNOWN controls.
- Both authors' and this audit's exhaustive numerical/cover helpers were patched
  to throw during production tests. A 24-satellite disjoint-edge network still
  constructed and independently received a full numerical certificate in 101
  profile steps, with 11,251 wire bytes and 188-bit retained scalars. Its circuit
  charged 24 anchors, 576 anti-neighborhood tests, 11,616 component-neighbor tests
  and 264 biclique-pair checks. The old constructor correctly refused its default
  16,777,216-mask requirement. No cover list was materialized by the preferred paths.

Finite controls corroborate the proofs, not establish unbounded-state results by
enumeration. All state checks cancel t^N. No Foster power or exceptional-state set
was expanded. The main original P4 receipt still has K=580, J=18609, 19,187 charged
profile/compensation steps, three covers from 16 masks, 6,610-bit retained scalars,
and N_*=401236632145171579. The preferred circuit preserves its numerical constants.
These are proof witnesses, not practical mixing bounds.

Budgets cap only named loop counts, not all arithmetic. Additional slope/minimum
scans, raw normalization, cover-edge tests, exact comparisons, rational bit growth,
memory and wall time still cost work. The modules deliberately disable CPython's
process-wide decimal conversion guard; this is documented trusted research use,
not a hostile-input service cap. Exact raw rates/t are required; trusted state
helpers are not advertised as adversarial API validators.

## Scope comparisons and final status

The non-complex-balanced diagnostic P4 has an internal complex tree; complex
balance would force edge-by-edge balance. Unit amplification and three unit arms
force b=c=d=e=a, contradicting the perturbed AE leaf ae=2cd. Its slow latent ray
has R=1,Q=1 with diverging total count, while another small-R ray has a bad middle
hub paid by order-M good endpoint activity. Both phenomena are real and retained.

At all unit rates, ordinary detailed balance/product Poisson solves even excluded
hub graphs. The triangle-plus-isolate and P4-plus-isolate controls therefore show
failure of the specific near-cone comparison, not failure of recurrence or all
moments. The prior biclique and multipartite methods retain their exact scopes;
this graph class is a proved larger sufficient join, not general weak reversibility.
No exhaustive exclusion of stronger ordinary literature is asserted.

The whole mathematical/code/receiving audit is complete for both bound sources.
The only noted defect is the nonblocking “bounded below” wording typo. No current
source or receiver repair was required; no unresolved mathematical blocker remains.
The independent implementations are included as additional auditable artifacts.

The final six Python sources were also replayed from a fresh preferred-package
layout with default source-path resolution and a separate output directory. All
four entry points exited zero, all published outputs remained byte-identical, and
both independent suites reproduced their full semantic totals. Actual timings and
temporary paths are retained in STAGED_REPRODUCTION.json; frozen evidence was not
overwritten.

For reproducibility, set AUDIT_OUTPUT_DIR to a fresh writable absolute directory,
use assertions-enabled Python with PYTHONDONTWRITEBYTECODE=1, and run:

    python replay_author.py
    python exercise_independent.py
    python replay_circuit.py
    python exercise_independent_circuit.py

The source directories can be set explicitly with COVER_SOURCE_DIR and
CIRCUIT_SOURCE_DIR. Drivers also support this audit staged beneath the preferred
package, with its byte-identical frozen_cover_source/ directory. Do not overwrite
frozen evidence by replaying without a fresh output directory. Timings may differ;
source bindings, published replay bytes and mathematical totals must not.
