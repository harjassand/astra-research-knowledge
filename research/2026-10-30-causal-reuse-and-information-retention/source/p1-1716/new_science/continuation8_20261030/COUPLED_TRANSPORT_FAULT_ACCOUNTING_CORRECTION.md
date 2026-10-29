# Complete fault accounting for the coupled-current gate

30 October 2026. Root addendum prompted by the actual receiving review.
The reviewed coupled-transport proof and its snapshot remain unchanged.

Its equation (9), |J_1-J_2|<=1+2N_wrong+N_extra_bit, applies to wrong-sign
selected events that still perform their atomic bit flip, and to isolated extra
bit flips. It is not a bound for missed selected-event bit updates. The review's
counterexample is two correct-sign channel-1 events with a stuck bit: the
current difference becomes two while both of those original counts are zero.
The adjacent original caveat mentioned missed actuation but did not include
its count in the displayed formula. The following is the explicit complete
accounting to use when such failures are allowed.

For each actual event e define, with g(u)=-u/2,

    r_e=d_1(e)-d_2(e)-[g(u_after)-g(u_before)].

Telescoping on every actual path gives

    J_1-J_2=g(u_t)-g(u_0)+sum_e r_e,
    |J_1-J_2|<=1+sum_e |r_e|.                             (1)

For selected events with unit signed current and a bit that either flips or
stays unchanged, classify the faults as follows. A wrong-sign selected event
with a successful bit flip has |r_e|=2. A selected event whose flip is missed
has |r_e|=1, regardless of its gate sign. An isolated bit flip has |r_e|=1.
Correct selected events and ordinary unselected events have r_e=0. Therefore

    |J_1-J_2|<=1+2N_wrong_and_flipped+N_missed+N_extra_bit. (2)

The classes in (2) are disjoint. Other kinds of event, multiple simultaneous
increments, unmodeled moving apparatus, or incorrect observations must use
their actual mismatch in (1); their costs are not presumed covered by (2).
Neither equation supplies a sensor, a confidence interval or an error rate.

This correction does not alter the perfect-gate path identity, force and stall
theorems, productive cycle, or executed population results. It makes the
finite-error interface explicit and preserves the useful stuck-bit failure.
