# Explicit matrix bridge (separate, exploratory)

Primary reference checked: official Macaulay2 Resultants documentation for `macaulayFormula`, https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Resultants/html/_macaulay__Formula.html, and its Resultants.m2 implementation. The documented determinant quotient is the classical Macaulay formula, not a new resultant identity.

macaulay_template.py independently constructs rows indexed by monomials of total degree rho=sum d_i−n+1. Assign each monomial to the first distinguished power q_i^{d_i} dividing it and multiply H_i by the remaining monomial. The extraneous principal minor retains monomials divisible by at least TWO distinguished powers. Four cubics give rho9, full dimension220, minor112, quotient degree108.

Executed tests: four diagonal cubics give product(a_i)^27 exactly; four linear forms give the ordinary4×4 determinant; two homogeneous quadratics agree with the univariate Sylvester resultant. Generic specialized denominator zero is explicitly rejected. This small/structured evidence is not a generic oracle validation.

An auxiliary symbolic shift H_i -> H_i+t q_i^3 adds tI to BOTH matrices, so both determinants are monic in t. Thus the denominator is not the zero polynomial for any specialized H. Exact polynomial quotient, followed by t=0, avoids a specialized0/0. This shift/quotient path and universal-coefficient derivatives are not yet implemented.

check_actual_macaulay_value.py separately attempts a scalar resultant of one actual bank's unscaled gradient at lambda0, with a180s cap. Only an actual_macaulay_value.json emitted after the final exact division is a completed result. This is not a whole resultant polynomial or optimizer.

Post08:11 correction: the exploratory matrix constructor originally rejected zero forms even when a homogeneous degree was explicitly supplied. It now admits them by ignoring zero terms in homogeneity/matrix-fill checks, requires explicit positive degrees when a zero form is present, and returns scalar resultant0 for a validated zero-form input. New executable zero-form/missing-degree tests pass alongside all prior structured checks. This changes only an unfrozen generic-input edge, not the nonzero supplied bank/factorable diagnostics or any accepted theorem/certificate.
