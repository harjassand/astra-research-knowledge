# Scope of mathematical and computational checks

## Upper-bound candidate

FOCUSED_MATHEMATICAL_CHECK.md preserves the completed focused internal mathematical check of the coherent-return upper proof. Its scope is the upper-bound proof only. It is not an external review or a formal proof-assistant verification.

verify_boundaries.py and boundary_verification.json preserve the original exact finite sanity checks. Their saved output was reproduced without alteration when the original package was prepared; REPRODUCTION_RECORD.json records that reproduction.

## Cyclotomic lower construction

The complete lower construction has exact algebraic tests and direct internal mathematical reading of its induction and endpoint. This is not external validation or priority certification. The earlier focused upper-proof check does not extend to this later construction.

verify_nested_clock.py uses exact rational arithmetic in Q(zeta_256) to test two nested clocks through time 6144. It checks every output against the claimed full pulse sequences. The saved result is nested_clock_checks.json. The proof for arbitrary nesting depth is the separate symbolic induction.

## Rational quadratic illustration

verify_quadratic_carry.py checks the illustrative fixed-degree rational binary counter for m=1,...,16. Its saved result is quadratic_carry_checks.json. The accompanying elementary proof is an illustration, not an independently novel complexity claim.

## General limits

No finite computation establishes a theorem for all dimensions. No external peer review, proof-assistant formalization, exhaustive literature clearance, or priority certification is claimed for either candidate. The two proofs have different arithmetic scopes, made explicit in the README and lower-construction paper.
