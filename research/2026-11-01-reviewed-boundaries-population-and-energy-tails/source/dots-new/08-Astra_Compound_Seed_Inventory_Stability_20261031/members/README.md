# Acquired compound-seed stability beyond a common-species factor

Ordinary mathematical CTMC research; **independent whole-source acceptance governs
this candidate package**. Earlier accepted packages are unchanged. No operational
chemistry, uploads, broad one-port theorem, general weak-reversibility solution, or
priority claim is made.

## Result

Only `0 <-> A` changes total count. Binary internal complexes are either `2A`, an
arm `A+X`, or an A-free hub `X+Y`. Every hub has a reversible edge to `2A`; arbitrary
reversible arm/hub edges cover every satellite. The A-free hub graph must be a union
of complete bipartite components. A finite raw graph calculation acquires

    R = A + sum_components min(total left-shore count, total right-shore count).

This inventory's positivity cannot be erased by an internal jump. It is not a
conserved count. The theorem constructs, for every fixed t>1,

    W = t^N [g_R + q A/((N+1)(R+1)^2)].

The decreasing g is acquired by a finite rational backward recurrence joined to the
certified tail `1+c/R`. The vanishing-amplitude active-phase correction earns
order-one drift through fast A+bulk capture. Its adverse reverse reactions and all
physical immigration/death costs are explicitly bounded. The conclusion is full
orthant irreducibility, positive recurrence, and every finite exponential stationary
total-count moment for arbitrary positive rates in this family.

There is no stationary-fiber law, independent success-coin premise, supplied good
pivot, grouping oracle, ODE trajectory, or simulation. A finite raw qualitative
certificate is distinct from constructing numerical Foster constants.

## Why this is a substantive boundary

The four-species fixture is

```
0 <-> A
A+B <-> C+D
2A  <-> C+D
A+C <-> C+D
A+D <-> C+D
```

with every rate one except `C+D -> A+C` at two. It is not complex balanced. There
is no common species in all internal complexes, and pure B/C/D leading faces are
inactive. At a single latent CD pair with B arbitrarily large, the next-core
immigration probability stays bounded away from zero: the prior common-seed
O(1/N) clock proof cannot transfer. Every positive normlike physical geometric
Foster function depending only on (A,N) fails. For sufficiently large requested t,
even the natural profile-only `t^N g_R` fails. The active/latent composition term
is therefore genuinely used, not merely a smaller constant.

These are representation obstructions, not instability or novelty claims. At the
all-unit-rate point the ordinary product-Poisson construction already solves the
model. Strong sampled-time, tier, queueing, piecewise/Foster and later literature
get the same raw network. The primary-source note gives bounded, actually inspected
hypothesis comparisons and explicit access limitations, not an exhaustive prior-art
exclusion.

The graph boundary is also exact: maximum integer capacitated matching loses at
most one upon EVERY enabled hub removal iff all nontrivial components are complete
bipartite. An induced P4 or triangle supplies an exact drop-two witness otherwise.
That classifies this inventory's universal removal property, **not stability**, all
inventories, or all correction methods. Missing cross edges and odd cycles remain
UNKNOWN, not counterexamples to weak-reversibility recurrence.

## Interfaces and honest costs

`compound_seed.py` is a trusted exact rational research constructor. It accepts
only int/Fraction rates (no bool/float/string) through the raw interface. Null
channels are discarded and duplicate channels combined. Its semantic receivers
recompute with the SAME implementation and are not independent validators.
An independently written receiver and full proof receipt must be bound separately.
It is not advertised as a hostile-input network service.

```
from fractions import Fraction
from compound_seed import fixture, qualitative, numerical
raw = fixture()
qualitative(raw)                # finite raw graph/inventory acquisition only
numerical(raw, Fraction(2))     # finite profile/head scalar construction
```

Qualitative success certifies recurrence and all finite exponential moments without
materializing g, q, a count-space head, or a Foster power. Failed family recognition
means stability UNKNOWN. Invalid numerical domains raise explicit exceptions.
Numerical budget exhaustion returns NUMERICAL_UNKNOWN while retaining the successful
qualitative certificate. The optional `max_profile_steps` caps ONLY the total count
of backward-recurrence and finite-head scan iterations; it does not cap input size,
rational bit growth, total arithmetic, memory, or wall time. The trusted module
explicitly disables CPython's decimal integer conversion guard for its interpreter
process on import. That permits exact receipt serialization, not secure-service
resource admission.

For the main t=2 case the actual construction performs 27 backward recurrence steps
and 503 finite-head checks, retaining 29 profile values. It earns N*=948431 and a
Foster constant containing `2^948432`; the count-space exception has
`binomial(948434,4)` states. Neither that power nor that state set is expanded or
enumerated. The huge numerical bound is not claimed sharp or computationally useful
as a mixing estimate. Direct product form, when available, remains much cheaper.

Executed author controls: seven rate/t/geometry cases, 2,128 exact state checks,
18,852 local assertions, 912 outside-head Foster checks (including counts10^30),
159 semantic leaf corruptions rejected, 24 coordinate permutations, 10 invalid-domain
controls, and five UNKNOWN controls. Shared K2,2 hubs, two components, no free
passenger, t close to1, larger t, and unequal core rates are included. Finite controls
supplement the ordinary proof; they do not prove its tail or universal rate statement.
Extreme death rates and huge t exercise numerical UNKNOWN with qualitative success.
No physical simulation or stationary-fiber approximation is used.

## Files

* `COMPOUND_SEED_THEOREM.md`: full proof, all constants, raw scope, physical core
  costs, irreducibility, Foster receiver, template obstruction and missing-edge warning.
* `compound_seed.py`: raw graph acquisition, qualitative and quantitative construction,
  semantic re-receiving, and exact finite-state generator helpers.
* `exercise_compound.py`, `exercise_results.json`, `main_demo.json`: executed controls.
* `comparators/PRIMARY_SCOPE_AND_COMPOUND_INVENTORY.md`: primary literature hierarchy,
  full F(A,N) no-go and conventional-method/access boundaries.
* `comparators/MATCHING_LIPSCHITZ_BOUNDARY_PENDING.md`: complete exact graph theorem;
  its pending filename is a provenance label, not a stability claim.
* Other comparator geometry/graph scripts and JSON: separate exact mechanism tests.
* `AUTHOR_MANIFEST.json`: frozen author and comparator source hashes. Independent
  receipt/manifest, when present, governs additional audit scope.

Use normal Python with assertions enabled, not `python -O`. All files are local;
no remote publication, push, outreach, or upload is authorized or performed.
