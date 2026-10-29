# Independent review of LOCAL_FLOW_INITIALIZATION.md

2026-10-29. Reviewed the root working derivation in `producer-workspace/LOCAL_FLOW_INITIALIZATION.md`. This is a mathematical audit, not a certified implementation receipt.

The unchanged-curve initialization, local analytic Taylor quadrature, inexact contraction, and binary time-scaling argument are sound in structure. I found two precision guards omitted from the statement; both can be repaired with polynomially many extra input-dependent bits.

## 1. Inexact iterates must remain in the analytic domain

The stated zeta<=2^(-p-3) alone does not ensure this: r can be exponentially small independently of a modest requested p. Define

    zeta <= min(r/8, desired_angle_error/4).

For every ||h||<=r, the exact map satisfies

    ||Phi(h)||<=||Phi(0)||+(1/4)||h||<=3r/8.

The inexact map then has norm <=r/2. Thus, starting at zero, every approximate iterate remains within the domain on which the contraction and quadrature estimates were proved. No circular invocation of the estimates outside their domain is needed. The error is <=4^-l ||h*||+(4/3)zeta. Choose l so the first term is <=desired_angle_error/2 and zeta so the second is <=desired_angle_error/2.

An explicit iteration count is

    l=max(0,ceil(log_4(2r/desired_angle_error))).

The fixed point satisfies ||h*||<=r/6, so using r here is conservative. If the desired tolerance exceeds r, output zero already meets it. Enforcing the new zeta cap costs O(log(1/r)) extra precision, polynomial in the spectral input size.

## 2. Convert coordinate error into direct Abel error

A p-bit angle error is not automatically a p-bit Abel error. On the complex collar use, for example,

    J_forward = g max(1,(2M)^(g-1)) (2/Delta)^g.

This bounds the operator norm of the Abel differential by column estimates. Set

    desired_angle_error <= delta/(2 J_forward)

and give final point encoding the remaining half of the direct budget. Thus working precision includes log J_forward in addition to m+log(1/epsilon)+log kappa_dec. Its logarithm is polynomial in the original input; the claimed polynomial-bit regime is unchanged, but the term must not be silently omitted from an exact accuracy theorem.

## 3. Taylor recurrence precision

The statement that coefficient recurrence costs polynomial precision is consistent, but a certified implementation should use the scaled variable s=rho*z (or any certified dyadic radius <=rho). Unscaled q-th coefficients can have size rho^-q; their bit size is O(q log(1/rho)), still polynomial but not constant. In scaled coordinates the Cauchy bound is U_J, geometric truncation applies directly, and the integrand uses sin(theta0+rho*z), evaluated from cos(theta0),sin(theta0). This avoids a need to recover an angle branch with arccos near endpoints. The initial circle coordinates can be obtained from the signed divisor using the endpoint-safe W expression.

No period lattice is needed: all these are local Abel lifts on the fixed curve. The m doublings amplify direct errors by 2 per call, so the binary budget is legitimate once the arithmetic interface itself has been certified. It does not justify treating a numerically good output as an arithmetic admission certificate.

## Outcome

No counterexample found to the repaired initialization argument. The all-input relative arithmetic implementation and full precision/representation composition remain unaccepted here. The two repairs above are mathematical safeguards, not new integrability identities or a speedup over equally informed classical methods.
