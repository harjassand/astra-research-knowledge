# Internal audit of the explicit rational feasible cell

27 October 2026. Decision: **PASS as an explicit finite positive feasible cell with strict all-band gain**, without a claim that this rational cell is the exact global optimizer.

The source scripts were copied unchanged into `rational_audit/` and executed only there, preserving their local import. Every assertion passed. Preserved hashes:

* rational_cell.py: e05d4621ec6c3e65ef2a535ba4e6ba4646be959314fc0a675d22ee9401b322af
* certify.py: b40b5ec048c673d7fb60bdb1c4b50695d9104c1e28e01f0ce71290bc2ff20dca
* generated RATIONAL_CELL.md: 4c6059fd201ae1545f7ab936983a48d321cbda066a1fb022fee5b4345014bb01

The inspected parent RATIONAL_CELL.md agrees with this generated output.

## Independent characteristic-polynomial reconstruction

For masses (1,m1,m2) and star springs (k1,k2), the mass-normalized internal matrix has diagonal entries k1+k2,k1/m1,k2/m2 and off-diagonal backbone entries -k1/sqrt(m1),-k2/sqrt(m2). Its translation eigenvalue is exactly zero. Writing

B2=(k1+k2)m1m2+k1m2+k2m1,

its positive alpha roots have sum B2/(m1m2). The sum of its principal order-two minors is

k1k2(1/m1+1/m2+1/(m1m2))=2k1k2/(m1m2),

because m1+m2=1. This is exactly the quadratic used in the script.

Adding the intercell pi-point shift 4 to the backbone diagonal adds four to the trace, adds 4(k1/m1+k2/m2) to the principal-minor sum, and gives determinant 4k1k2/(m1m2). Therefore the beta characteristic cubic is exactly the displayed coefficient list.

The exact rational sign changes on disjoint intervals (1,3), (41,44), (70,80) imply at least one real root in each interval. A cubic has total degree three, so these exhaust every eigenvalue and each is simple. The bisection preserves its bracketing root even if an exact midpoint root occurs. The interval quadratic formulas and the asserted strict alpha/beta ordering then prove complete strict positive interlacing. Thus all three occupied bands, including the highest optical band, are included in the objective.

## Exact resources and objective

All stated masses and springs are positive rational decimals; m1+m2=1 exactly. Static star force balance gives the original CM compliance

C=m1²/k1+m2²/k2,

with no normalization ambiguity because the side total mass is one. Exact Fraction comparisons prove C<1/20 and k1+k2=20.0199<20.02. The enclosing margins are approximately 1.0000035374e-8 for compliance and exactly 1e-4 for spring sum.

The copied standard-library interval certificate gives

J in [1.142045204145875753226610,
      1.142045204145875753226611],

J_pendant-J in [0.000000183396196008489989,
                 0.000000183396196008489990].

The comparator is the strongest legal one-pendant under the same caps, k=20, as already audited. The full Bose-tail bounds and exact root isolation make this strict gain independent of transcendental root tuning or omitted bands.

This removes the need to use rounded representatives of the exactly binding joint optimum for a feasible example. It supplies one explicit rational design with strict budget margins. It does not quantify fabrication tolerances, connector mass, robustness, individual displacement/strain or material/device performance, and it is not asserted to attain the exact joint optimum from JOINT_PROOF.md. This is exposed internal mathematical verification, not historical novelty or external acceptance.
