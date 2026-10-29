# Result: polynomial ideal nominal initialization

The nominal syndrome-only initialization gap is closed for the accepted
recursive RX/RZ family at one sufficiently low fixed inverse temperature.
The all-level proof is in PROOF.md and STRONG_ORDINARY.md.

The source-specific construction is a local binary decoder-history model.
It enforces redundant syndrome relations, has a unique history per admissible
top syndrome, and bounds history support by four times top energy. Its
connected accepted supports are computably enumerable positive polymers.
Established polymer samplers then give:

* bounded work polynomial in n and 1/epsilon (finite-list implementation);
* work polynomial in n and log(1/epsilon) in EXPECTATION (exact rational
  rooted implementation), including exponential logical accuracy.

The latter does not assert bounded worst-case or high-probability polynomial
work in log(1/epsilon). No runtime-conditioned restart is used.

The nominal corrected encoder changes by diamond norm at most 2epsilon.
Its actual memory decoder is unchanged: the all-level auxiliary histories
are sampling coordinates, not new recovery actions. Ideal Clifford encoding
and classical correction costs remain polynomial additional inputs; noisy
physical preparation has not been established.

The literal n=1336 source consumer checks admission and component identities;
both ordinary engines were executed at the same target temperature. The
ordinary all-zero approximation already has TV upper about 4.23e-54 and wins
the requested .01 finite case. This is a constructive asymptotic admission,
not a practical speed or hardware result. PRIOR_AND_COST.md preserves the
strong same-information methods and all recorded execution costs.

Root whole-read/analytically accepted the history/admissibility proof and
literal predicates, independently consumed local predicates at n60/1336,
and whole-read/accepted the rooted expected-work proof. This substantive
review is distinct from the seeded producer executions. It does not imply
that every newly written sampler line received an independent software
implementation or a physical qualification. World priority is UNKNOWN.
