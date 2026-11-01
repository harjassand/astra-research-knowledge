# Dominating-cover stability with an acquired polynomial inventory circuit

**Frozen author candidate; independent whole review pending.** Local mathematics
only. General weak reversibility and arbitrary one-port conservative stability
remain unresolved here. Historical novelty is not established.

This is the current preferred receiving interface for the mathematical theorem in
`frozen_cover_source/COVER_SEED_THEOREM.md`. Its eleven original bound files and
manifest are copied byte-identically; the source proof's exponential cover
implementation remains a valid but now avoidable comparator, not the preferred cost.

`CIRCUIT_ACQUISITION_THEOREM.md` proves a self-contained ordinary graph improvement:
for each satellite v, its anti-neighborhood is a disjoint union of bicliques and
isolates. These decompositions acquire an exact maximum-weight independent-set
max-plus circuit, so `tau=sum(counts)-MWIS(counts)` is computable without enumerating
covers. Every P4/triangle-forbidden-pattern condition, zero-weight tie, and
all-satellite scope remains explicit. The compiler also earns actual optimal
minimal covers and identifies bad active hubs without an optimization oracle.

## Mathematical result (unchanged)

The raw architecture is one reversible port `0 <-> A`, binary square-free satellite
hubs, reversible `2A` amplification at every hub, and reversible `A+X` arms covering
every satellite. Its graph excludes induced triangle+isolate and P4+isolate. The
ordinary proof constructs

    W=t^N [g_R + q A/((N+1)(R+1)^2) - epsilon A/(N+1)],
    R=A+tau.

For all positive rates it proves nonexplosion, full-orthant irreducibility, positive
recurrence and every finite exponential stationary total-count moment. It joins
slow boundary seed amplification with fast overlapping hub activity. Accepted
biclique and multipartite families are contained, while P4 and C5 extend the
geometry. The condition is sharp for the particular heavy-bulk rate absorption,
not for stability; unit-rate rejected graphs still have ordinary product form.

## Interfaces and honest costs

- `qualitative(raw)` returns an acquired graph/circuit receipt and the qualitative
  conclusion, without materializing the requested-t profile.
- `numerical(raw,t,max_profile_steps=...)` constructs the same exact profile and
  constants as the frozen theorem, with a circuit replacing its cover list.
- `UNKNOWN_NUMERICAL_BUDGET` retains qualitative acceptance. Unsupported graph or
  raw structure is stability UNKNOWN. Invalid domains raise.
- Graph acquisition is polynomial: the direct forbidden-pattern test is O(m^5),
  anti-neighborhood decomposition O(m^3), retained circuit O(m^2), weighted
  evaluation O(m^2) arithmetic operations with polynomial binary bit cost.
- Complete numerical acquisition is NOT claimed polynomial. Its `K-1+J-1` profile
  loops and rational bit growth remain paid. The budget caps only loop count,
  not memory, arithmetic bit work or wall time. Foster powers stay factored.
- Same-code `receive_*` are author self-checks, not independent receivers. Trusted
  helper inputs and process-level Python decimal-guard behavior remain explicit.
- Scaled pointwise LW/t^N is exact rational work in the explicit certificate and
  binary count input. Expanding W, the moment bound or the finite head is excluded.

For the non-complex-balanced P4 fixture at t=2, K=580, J=18609, profile loops19,187,
N*=401236632145171579, maximum retained scalar6,610 bits. Graph cover masks: ZERO.
The numerical Foster/profile constants are exactly identical to the frozen version;
the improvement removes acquisition work, not statistical or drift assumptions.

## Exact executions

    PYTHONDONTWRITEBYTECODE=1 python cover_circuit.py
    PYTHONDONTWRITEBYTECODE=1 python exercise_circuit.py

Use normal Python with assertions, never `-O`. Outputs bind actual execution.
All 1,094 nonempty graphs through five satellites are classified; every admitted
case (775 graphs) is compared with exhaustive covers as a TEST COMPARATOR, not
production machinery. Results:177,021 exact capacity/circuit and minimal-cover
witness checks,400,828 active-edge queries,775 large-binary evaluations,
246 exact W/drift comparisons with the frozen constructor, and8 semantic mutations.
The exhaustive production helpers are replaced with throwing functions during the
test, and circuit numerical acquisition still succeeds. Thus no silent cover or
old-constructor fallback supplies the claimed result.

The frozen source also retains its 5,202-state/30,429-jump/90,130-profile-check
suite, coordinate/domain/mutation/budget controls, ordinary product-form wins,
sharp forbidden-pattern witnesses, and proof of every physical-time Foster join.
Finite checks corroborate proofs; none is a simulated stability inference.

No external source was retrieved. The prior disclosed alternate-source access
failure remains quarantined and is not retroactively cleared. The parent's newly
denied graph-paper URL was not read or retried. No publication, upload, outreach,
process design or laboratory action is part of this package.
