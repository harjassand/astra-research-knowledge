# Fresh whole-proof, constructor, and receiver audit: multipartite seed

31 October 2026. Ordinary mathematical CTMC research only.

## Verdict

**SCOPED MATHEMATICAL PASS.** The current complete-multipartite theorem, trusted
exact-rational constructor, and separately implemented receiver are accepted within
their stated family and compact representation. No substantive proof or code repair
was needed. This is a fresh review of the new proof, not an inherited acceptance of
the preceding biclique construction, and not proof-assistant formalization.

The conclusion is nonexplosion, full-orthant irreducibility, positive recurrence,
and all finite exponential stationary total-count moments for arbitrary strictly
positive real rates in this raw family. Numerical construction and receiving use
exact positive rational rates and rational t>1.

The polynomial-bit claim is accepted **only for explicit binary-rational input,
compact rational constants and a symbolic base/integer-exponent certificate**, and
for exact rational pointwise evaluation after cancelling t^N. Expanded exponential
moment bounds, W itself at huge binary-encoded N, and state-space enumeration are
not covered. Constants are very conservative, not practical mixing estimates.

No external source retrieval occurred. The preceding source-access failure remains
quarantined and is not retroactively cleared or used as a significance premise.
Nothing here establishes historical novelty, exhaustive prior-art coverage,
general weak reversibility, or arbitrary conservative one-port stability.

## Frozen sources and independence

The current author manifest binds 13 files and has SHA256
`aa232d64c068a0de1ffb8a5e41af5f5728a241945b4edb5e4c74d02dd82e3e85`.
The separate 26-file audit manifest has SHA256
`0d69b6f2fc9d62335a933ef47b61878809c932b9642b407e768a17c3b0a8a385`.
Every listed byte count and SHA256 was verified before replay. Principal bindings:

- Current proof: `4d96e067d5127034d2d27f99c44b62656cccdc689438f8ba1e13b99ef798e702`.
- Constructor: `329b43c01ee7a3940b8f76d90db21fd6818bcd4144d74bd88f1d8eb0ab045b0f`.
- First independent whole receipt: `0492b85660c4b066e5e1c0bbea57dc30d8e090055d5572486b19adcbcae4a557`.
- Separate receiver: `bddfaac10543e547bf91bf29e4a65291e2d62bd1f6347e99fabb4b910458fec0`.

The current proof, README, constructor, all execution drivers, separate receiver,
both mechanism notes, first independent receipt and manifests were read in full.
The historical proof was compared with the current proof: the difference is the
recorded structural-scope correction about reacquiring partitions after edge
removal, not a changed mathematical inequality or numerical formula.

This audit's fresh raw fixtures, coordinates, propensities, state transitions,
scaled generator, channel table, and graph-recognition criterion do not use the
constructor's fixture/state/drift helpers. Candidate code supplies certificates;
the separately authored receiver additionally re-receives them. That receiver
imports no candidate code and uses its own complement-graph traversal and scalar
construction. The author's same-implementation receivers remain self-checks, not
independent validators.

All new audit material is in this uniquely created directory. Frozen candidate
bytes and the preceding accepted archive were not modified.

## Independent ordinary proof reconstruction

### 1. Acquired graph, raw architecture and positivity

Exact input checks identify the sole nonconservative pair 0↔A. Every nonnull
internal channel is binary and joins an A-free square-free hub to either 2A or
A+X, with its reverse present. Every hub has its own amplification pair; every
satellite has an arm. Duplicate channels are summed and validated null rows
removed. These conditions allow sparse arm incidence and arbitrary positive rates.

The complement components are discovered on **all satellites**, then checked for
within-part nonedges and all cross-part edges. Thus no grouping is supplied and
no isolated passenger is omitted. Nonadjacency must be an equivalence relation.
The resulting graph is complete multipartite with at least two nonempty parts.
A missing edge relative to a previously imagined partition is not a rejection
criterion: triangle-minus-edge is a valid K1,2 with newly acquired parts. The
historical wording correction is appropriate and the current implementation
already behaved correctly.

For part totals Z_j, N=A+ΣZ_j, M=max Z_j, R=N−M, and
P=(1+eta)R−eta A=R+eta(R−A), one has R≤P≤(1+eta)R. Every internal destination
contains A or a cross-part hub, so it has R≥1. At R=0, A=0 and all satellites
occupy a single part, so all internal sources vanish. Core birth/death changes
R and P by exactly +1/−1. No numerical conservation of R or P is asserted.

### 2. Global finite-jump bounds and every switching boundary

Every internal jump changes each part total by at most one, giving |ΔR|≤1.
Direct reaction-form enumeration sharpens the naive triangle bound to
|ΔP|≤1+2eta: for 2A→hub, ΔR is −1 or 0 and ΔA=−2; for a forward arm,
ΔR is −1, 0 or +1 and ΔA=−1; reverse forms give the opposite possibilities.
Since 0<eta≤1/16 and both active endpoints have P,P'≥1, P/P'≤3 and
|1/P'−1/P|≤6/P². This is valid through arbitrary max switches and ties.
All internal propensities sum to at most S N², proving the global inverse bound.

For 1≤R<N/2, integrality gives M≥R+1 and the dominant part I is unique.
It remains a maximizer after **every enabled** jump, not just after infinitesimal
or generic moves. Details that matter:

- Forward 2A jumps have A≥2 and cannot lower the old dominant total; other totals
  increase by at most one from at most R−A.
- If a forward arm consumes from I and its hub avoids I, the old total becomes
  M−1, while each other total is at most R−A+1≤R≤M−1. Equality is allowed.
  All other forward-arm cases have at least as much margin.
- On a reverse cross-hub arm, an outside-I particle is consumed before an outside
  return can be added. Therefore the entire new outside population is at most
  R−A≤R≤M−1; it cannot overtake the possibly reduced old dominant total.
  Returning into I restores that total. Reverse amplification is simpler.
- A reverse hub entirely outside I cannot lower I, while its outside consumption
  again supplies the necessary margin.

Thus the strict-cone table uses the old I exactly, even when the destination ties.
All 12 directional/incidence subcases were independently exercised. In particular:
2A→hub has ΔP=−1+eta when touching I and 2eta otherwise. Forward arms have
ΔP=eta, 1+2eta, −1, eta for (X in I, hub touches I), (X in I, hub avoids I),
(X outside I, hub touches I), (X outside I, hub avoids I), respectively.
Reverse subcases have the negative of these values. Outside the strict cone,
including R=N/2, the proof uses only the global finite-jump estimate.

### 3. Fast boundary inverse drift with adverse reverse arms retained

Every dominant-part forward arm increases P by at least eta. Its inverse drift is
at most −eta/(3P²), and the aggregate rate is at least k_- A M, without requiring
any particular destination hub. A cross-hub amplification increases P by 1−eta,
contributing at most −3b_h/(8P²).

The potentially adverse cross-hub arms return into I and lower P by eta. Their
inverse increment is at most 2eta/P². Since eta=b_-/(16s_+), their full source-wise
rate sum is paid by at most b_h/(8P²) of amplification. At least b_h/(4P²) negative
inverse drift remains. These order-NR reverse costs are not discarded.

Complete multipartiteness gives exactly Σ_cross-hub x_u x_v=M U, U=R−A.
Combining capture and amplification leaves −c0 M R/P²≤−gamma M/P.
Every remaining potentially positive inverse channel has a source made only of
A and outside-I particles, hence propensity at most its constant times R².
The global jump bound pays these channels by 6S, giving inequality (3).
No stationary-fiber, success-coin, protected clock or mixing premise enters.

### 4. The interior correction has the necessary opposite sign

The exact A-generator is

    L_int A = −2a A(A−1) − A Σ_X k_X x_X + Σ_h(s_h+b_h)x_u x_v.

The reverse coefficient is s_h+b_h because amplification creates two A's, not
one. Hence L_int A≥b0 Q−F0 A N and

    L_int[−epsilon A/(N+1)]
      ≤ epsilon F0 A − epsilon b0 Q/(N+1).

The negative phase term rewards activation; its adverse capture contribution is
paid by actual physical A-death. The proof does not transplant the sign or clock
argument from the earlier biclique correction.

### 5. Physical time, near-one t, and last-seed loss

On R≥1 use the exact core decomposition with λ(t−1)h and −D A h, where
D=mu(1−1/t). Birth decreases both 1/P and −epsilon A/(N+1), so its difference
term is nonpositive. On regular death states R≥2, P≥2 and A≤P give inverse
cost at most mu. The phase difference has positive cost at most epsilon mu,
using [A/(N+1)−(A−1)/N]≤1/N and A≤N.

The only death-enabled inverse singularity is R=A=P=1. Its destination is evaluated
using h0=4t directly, charging at most 4mu for the whole positive death difference.
No last-copy death channel is deleted or replaced by a constant protected clock.

Since active h≥1−epsilon≥1/2 and epsilon F0≤D/4, the combined baseline death
and adverse phase-capture terms leave −D A/4. Keeping D, rather than replacing it
prematurely by mu, is essential as t approaches 1. The enlarged bounded allowance
B=2λ(t−1)+5mu covers all remaining core costs. This proves master inequality (6).
At R=0 only immigration acts and the displayed formula (7) is exact.

### 6. One finite geometric cover and exact finite exception

The acquired delta is positive and at most 1/4. If R≤delta N and R≥1, then
M/P≥1/[2(1+eta)delta], so the boundary estimate pays B+6S with at least unit
slack. If R>delta N, then P>delta N and the inverse term is at most 6S/delta².

In that complement, either A≥delta N/2 and death pays at least D delta N/8,
or A<delta N/2, M≥(N−A)/q≥N/(2q), and U=R−A>delta N/2. The exact cross-hub
identity gives Q≥M U≥delta N²/(4q). Since N²/(N+1)≥N/2 for N≥1, the phase term
pays at least epsilon b0 delta N/(8q). Thus the stated kappa and N_* yield
scaled drift at most −1 throughout the active region outside the finite head.

Crucially, active h≤2, not just the global H=4t. Therefore ζ=min(1,λ)/2 converts
this to LW≤−ζW. The inactive-face estimate handles the larger h0 separately.
All cone, tie, A=0, A=1 and count-cutoff joins are included.

For N<N_*, the raw internal rate sum S N_*², core rate bounds and global h≤H
bound both destination values and ζW. The factored coefficient in (12) safely
covers every head state without enumeration. The number of such states is exactly
binomial(N_*+n−1,n); storing that expression is not a state search.

### 7. Nonexplosion, communicating class, and invariant moments

Internal moves conserve N; constant-rate immigration and count-decreasing death
give N(s)≤N(0)+Poisson(λs). Up to any finite horizon, a trajectory remains in a
finite count sublevel with bounded total jump rate, excluding explosion.
For each satellite, an acquired arm and its hub amplification provide the fully
reversible singleton path 0→A→2A→H→A+X→X. Nonnegative translations preserve
enabling, so these paths construct or remove every count vector. This proves
full-orthant irreducibility without an assumed stationary fiber.

Localized integrating-factor Dynkin gives the asserted semigroup bound; Fatou and
nonexplosion remove stopping. Equivalently, finite-time integrability follows
from h≤4t and the Poisson bound, even after multiplication by the polynomial total
propensity. Normlikeness makes occupation averages tight, yielding an invariant
probability and positive recurrence; irreducibility gives uniqueness. Fatou on
those averages gives π(W)≤C_F/ζ without assuming W is already in the invariant
generator domain. Because h≥1/2, π(t^N)≤2C_F/ζ, with the factor 2 correctly present
in the receipt. The construction works for every fixed finite t>1 and positive
real rate vector; the all-exponential conclusion is not a finite-test inference.

## Compact polynomial-bit claim and receiving contract

Let input size mean the total explicit binary lengths of all complexes, indices,
and rational numerators/denominators. Raw normalization sums at most the supplied
number of rational rates: numerator and denominator bit growth is polynomial in
that total length. The graph, coordinate and incidence scans are polynomial in
the explicit representation. Afterward the scalar formulas have fixed arithmetic
depth, using sums/products, divisions by proved positive values, minima and one
ceiling. Their exact numerator/denominator sizes, N_*'s binary length, and the
compact receipt are consequently polynomial-size; standard exact rational
arithmetic computes them in polynomial bit complexity.

This is conditional on explicit binary rationals, not a claim about arbitrarily
succinct expressions denoting huge rationals. The named 14 formula blocks are not
14 machine operations. Qualitative admission still performs raw rational summaries;
its zero Foster-block count does not mean zero arithmetic. There is no hidden loop
of length controlled by a rate ratio, t−1, N_*, or a count-space head.

The certificate stores coefficient, base t, and integer exponent N_*+1 separately.
Expanding t^(N_*+1) is generally enormous. At a binary-encoded state, exact
LW/t^N uses only t^(ΔN), where validated channels have ΔN∈{−1,0,1}, and computes
rational h, inverse/phase increments and binary mass-action polynomials. Its bit
complexity is polynomial in the explicit network, certificate and state lengths.
No evaluation of t^N is hidden in that statement.

Raw rates and t accept only exact int/Fraction types; bool, float, string and
subclass substitutes are rejected. Malformed domains raise; validly typed outside
families return stability UNKNOWN. Duplicate splitting and null insertion preserve
normalized mathematics but correctly change input-work counters. The separate
receiver reconstructs all receipt fields, including work and factored constants;
the author self-receivers are not misrepresented as independent. The documented
process-wide decimal-conversion guard change is trusted research behavior, not a
hostile-input admission policy or a wall-time/memory cap.

## Negative controls, mechanism need, and comparative scope

The sparse perturbed triangle is not complex balanced. Its internal complex graph
is a tree, so complex balance forces zero net flow across each bridge. Unit
amplification pairs imply bc=bd=cd=a² and therefore b=c=d=a>0; the perturbed leaf
requires ab=2bc, a contradiction. The all-unit control is already detailed balanced
and has the ordinary product-Poisson solution.

For at least three equally occupied parts and A=0, a reverse hub leaves at least
one untouched maximal part. M cannot decrease; A strictly increases, so P strictly
decreases on every enabled reverse. Therefore every inverse-profile increment is
positive. For fixed t>1, geometric immigration also becomes positive along the
ray. This proves failure of radial-only t^N(1+1/P), not failure of every alternative
Lyapunov method. The negative phase term earns order-N drift there; eight fresh
exact controls confirmed positive radial-only versus negative full drift.

For a free passenger omitted from hub parts, pure-passenger states have R=N and
P=(1+eta)N despite no enabled internal source. The exact extended-template drift
in the separate note tends to λ(t−1)>0 for every fixed finite correction coefficient.
Four fresh exact controls, including t very close to 1 and eta=0, corroborate it.
This is an ansatz failure, not instability: the earlier biclique/free-passenger
construction can succeed, and unit-rate controls are product-form stable.

The two sufficient families do not contain one another: this one allows complete
multipartite triangles/cliques but excludes disconnected hub components and free
passengers. The earlier matching-removal drop-two counterexamples remain valid. Even in the
two-part overlap, 1+1/P is not a profile of R alone: P depends on A, so there is
no conflict with the earlier profile-only no-go.
Neither family nor graph property classifies stable networks. The exhaustive graph
controls below use all-unit reversible raw networks, so their nonempty rejected
examples are also detailed-balanced controls, not counterexamples to recurrence.

## Optional graph/clock addendum

The separately frozen `FAST_ACTIVITY_GRAPH_BOUNDARY.md` is also mathematically
accepted as a **separate scope lemma**, not as a stronger stability theorem.
Its exact binding and replay are recorded separately in this audit.

For a nonempty finite graph on all satellite vertices, nonadjacency is transitive
iff no induced edge-plus-isolate exists, which is equivalent to complete
multipartiteness. On an active integer capacity vector, multipartiteness gives
Q≥M(S−M)≥S−1, since M and S−M are positive integers. This implies uniformly
linear Q at large S. Conversely an induced edge uv plus a vertex w adjacent to
neither endpoint gives x_u=x_v=1, x_w=N and Q=1, S=N+2. It defeats every uniform
positive linear activity bound. The nonempty-edge assumption prevents a vacuous
empty-graph counterexample, and inclusion of all vertices prevents omission of
isolated passengers.

At latent A=0 states the raw architecture has internal exit rate Σ_h s_h x_u x_v.
Multipartiteness therefore supplies at least s_min(N−1) at every active latent
state, and every departure creates A. Outside that class, the explicit witness has
only hub uv active, constant internal rate s_uv, no death, and immigration rate λ.
The exact exponential race gives λ/(λ+s_uv)>0 for immigration before any internal
jump, hence a nonvanishing lower bound for first-core up. The converse is correctly
not claimed: a linear next-internal rate alone does not prove an O(1/N) first-core
up probability, recurrence, or all moments. Additional internal channel types lie
outside this clock statement.

## Actual executions and costs

`EXACT_REPLAYS.json` records actual subprocess times, source/output hashes, exit
codes, output sizes and zero stderr for five byte-identical published outputs:
constructor demo, author exercise, independent mechanism checks, separate receiver
exercise and extreme-wire controls. All author and first independent totals were
reproduced, including mu=10^-5000, t−1=10^-200, t=10^100 and a reverse rate 10^1500.
These are finite corroborations, not a complexity proof. The separate optional
graph addendum also replayed byte-identically: 1,094 nonempty graphs, 11,824 active
integer-capacity checks, 1,024 forbidden witnesses and 3,072 large-bulk witness checks.

Fresh controls in `INDEPENDENT_ADVERSARIAL_RESULTS.json`:

- Six independently built sparse/full random-rational geometries, including
  nonsingleton three-part graphs, a five-part clique, and permuted open coordinates.
- 3,278 exact state checks and 30,986 enabled internal jumps; 1,740 strict-boundary
  states, all 12 boundary channel subcases, 270 destination ties, 3,778 max-index
  switches, 197 last-seed deaths, 681 cone states and 872 outside-Foster states.
- 3,136 direct master checks; 15 targeted independent qualitative/numerical
  re-receivings, plus every exhaustive graph receipt and six normalization receipts.
- All 1,098 simple graphs on two through five satellites: exactly 70 admissions,
  matching an independent transitive-nonadjacency characterization. Four empty
  graphs and 1,024 nonempty nonmultipartite graphs are outside the recognizer.
- 74 invalid-domain refusal calls across both implementations (37 paired cases),
  seven additional structurally invalid families, and six duplicate/null controls.
- Three joint extreme-rate/t cases with 18 exact states: tiny immigration/death
  combined with t−1=10^-250; t=10^120 combined with huge reverse and small death;
  and amplification rates 10^-500. The largest new receipt is 43,522 bytes with
  21,094-bit retained scalars. No rate-dependent iteration or power expansion.
- Eight radial-only obstruction comparisons and four free-passenger positive-drift
  controls. Infinite-ray claims rest on the proofs above, not these finite values.

The main cutoff remains 600861655025994950. Its factored power and finite exception
are not expanded or enumerated. All runs used assertions-enabled Python and
PYTHONDONTWRITEBYTECODE=1. The final fresh suite took about 2.7 seconds on this
execution environment; timing is recorded evidence, not an asymptotic or service
performance promise. No fresh harness or implementation failure occurred in this
audit. The earlier independent receiver's disclosed development-label correction
and the author's historical scope wording are retained as provenance, not silently
rewritten or confused with current frozen output.

## Reproduction and closed scope

Set AUDIT_OUTPUT_DIR to a fresh writable absolute directory before running the final
entry points, so frozen evidence is not overwritten. Use ordinary Python, not -O:

    AUDIT_OUTPUT_DIR=/absolute/fresh/output PYTHONDONTWRITEBYTECODE=1 python replay_package.py
    AUDIT_OUTPUT_DIR=/absolute/fresh/output PYTHONDONTWRITEBYTECODE=1 python independent_adversarial_checks.py
    AUDIT_OUTPUT_DIR=/absolute/fresh/output PYTHONDONTWRITEBYTECODE=1 python replay_optional_boundary.py

The optional addendum's three exact sources are retained under optional_boundary_source/.
Drivers support the original sibling layout and byte-identical staging
under the candidate's fresh-whole-audit subdirectory. Elapsed timings may vary;
source bindings, exact replay bytes and mathematical totals must not.

The requested proof, receiver, boundary, cost and adversarial audit is complete.
There is no outstanding mathematical/code blocker and no pending external action.
Acceptance is limited to the exact source boundary and qualifications above.
