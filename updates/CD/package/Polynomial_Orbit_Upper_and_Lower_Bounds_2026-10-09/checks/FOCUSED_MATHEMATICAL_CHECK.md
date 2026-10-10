# Focused mathematical check

Completed 2026-10-09. One independent internal read checked the candidate; no counterexample or proof gap was found. No external peer review, formal proof-assistant verification, or priority certification is claimed.

The check covered:

- Positive time jumps are powers of the same map, and survival is certified throughout each jump. Therefore a component cycle is genuinely safe for the unique original orbit.
- An escaping point reaches a bad component in at most m-1 good jumps, giving access-or-exit time mT.
- On a new component A, the initial bad-domain jump plus at most m-1 good jumps gives q<=mT; the old bad-component exit allowance yields (m+1)T.
- The new closed return domain A intersect Q^(-1)(E) is exact. Outside it, the image lies outside the old bad domain, so the old exit certificate applies.
- Every bad restriction is a proper closed subset of its irreducible component. This lowers the maximum dimension even for a non-equidimensional variety.
- Total geometric degree includes every component. In each generic cut, retained target components contribute delta_retained and the others contribute at most E delta_remaining; the sum is at most E times the old total.
- Projective projection and separation give set-theoretic defining equations of degree at most the total geometric degree Delta.
- At most n restrictions suffice, and sum Delta_i T_i=T_n-1. Testing t=0,...,T_n-1 has the correct endpoint.
- The field argument does not use characteristic zero. The rational-input computational corollary uses exact rational arithmetic and has primitive-recursive bit cost.

The small exact computations in boundary_verification.json separately exercise singular observational-algebra identities, dimension-collapsing maps, reducible guards, and binary-counter lower examples. They are sanity checks, not proofs of the theorem.

Open: novelty and comparison with possible unstated corollaries of prior work; external/formal validation; an elementary bound uniform in dimension.
