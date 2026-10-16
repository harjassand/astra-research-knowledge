# Sources, verification, and scope

## Primary causal theorem

Gutoski and Watrous, *Toward a General Theory of Quantum Games* (2007), Theorem 9, printed page 13, proof on page 14, author-hosted PDF:
https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf

This is the positive domination theorem for arbitrary finite-round strategies. Its explicit tensor implementation and the unchanged-action Hamiltonian embedding are included in the sibling causal_refresh_product/PROOF.md, which is unchanged from the delivered ideal packet.

The one-gap sine lemma and its Redheffer primary reference are reproduced in that prerequisite. The present exact two-gap scalar minimization and three-level construction are proved directly, without invoking a new external theorem.

## Inherited capital

The included measurement_randomizer_bridge/PARTIAL_DEPHASING_BOUNDARY_THEOREM.md and PARTIAL_DEPHASING_INDEPENDENT_AUDIT.md were authored on 2026-10-15. They already contain the identity/full-pinch mixture, independently averaged parent products, joint-channel/fresh-reservoir requirements, and quadratic merged-block certificate. They have a wider stabilizer-group support/reservation purpose; their separate hypotheses must not be silently replaced by this single-parity endpoint statement.

The new exact two-gap formula is distinguished from that inherited mixture calculation. Neither the mixture interpretation nor weak-measurement dephasing is claimed as new.

## Internal mathematical checks

The construction and upper bound were independently checked by the parent and a separate internal mathematical reviewer. Two derivations agree: the concise Cauchy–Schwarz r,t relaxation in the proof, and a compression of the second-gap endpoint effect to the two entering parity vectors with both effect-positivity constraints. These are internal checks, not external validation or peer review.

check_two_gap.py is newly authored deterministic code. It performs twelve fixed three-level calculations, including zero/saturated actions, zero/full/partial dephasing, both scalar branches, and an exact rational obstruction. It does not optimize or import acquired project code. Maximum witness/formula residual is below 7e-16; the 9/16 versus 7/16 obstruction is checked with exact rational arithmetic.

Replay: python imperfect_refresh_product/check_two_gap.py from the extracted root.

## Boundaries

Specified D_eta acts on the complete modeled joint state and as identity on persistent bath/reference factors. Noise environments are fresh and inaccessible. Generic measurement infidelity, reduced-channel calibration, correlated reservoirs, state-selected schedules, finite-width physical realization, and quantum-erasure access are not covered. No exact optimum for three or more partial-dephasing nodes is claimed.
