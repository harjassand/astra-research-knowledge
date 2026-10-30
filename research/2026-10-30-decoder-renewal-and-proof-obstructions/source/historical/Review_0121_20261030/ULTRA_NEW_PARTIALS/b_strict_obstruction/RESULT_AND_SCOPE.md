# Strict/open obstruction acquired

There exists epsilon0>0 such that every quartic

    F_epsilon(A)=|A|⁴+12(det A)²
                 +4det A(a²+c²−b²−d²)+epsilon |A|⁴,
    0<epsilon<epsilon0,

is positive off zero, satisfies

    F_epsilon''(A)[R,R]>=4epsilon |A|²|R|² for rank-one R,

and CANNOT be a finite sum of a polyconvex quartic polynomial and
quartic heat-certificate parts with origin-C² correction coefficients.
Different summands may use different constant mean-converging flows.
A full35-dimensional open strict-ROC neighborhood is excluded as well.

The trace-free governing extension is stronger: it even grants each
heat summand any NONZERO real constant operator, provided the summand
is itself ROC. It does not claim unstable flows prove QC.

The proof uses a closed OUTER class and compact ROC bases. It does not
assume that the actual union over flows is closed/convex. The endpoint
extremality and non-PC proof is a preserved frozen input; no old files
were changed. Every polynomial primitive of arbitrary degree is included
by the origin Taylor lemma.

The neighborhood radius / an explicit admissible epsilon / a strict
separating functional remain UNEVALUATED. The theorem is a qualitative
strict/open mathematical obstruction, not an executed numerical certificate
for a named epsilon. The exact newly acquired universal constants are
||F||∞<=6ell(F) and ||Omega_coeff||∞<2^21||F||∞ at normalized L.

Full angular/rational corrections (Omega merely C¹ at zero), arbitrary
nonpolynomial integrand summands, nonlinear operations and independent
QC mechanisms remain outside this result. No non-QC example, Morrey
resolution, physical gate or historical-priority claim follows.

Governing proof: `PROOF.md` with `TRACE_FREE_EXTENSION.md`.
Universal exact arithmetic: `acquire_coercivity.py` / `COERCIVITY.json`.
Provenance, ordinary methods and actual costs: `COST_AND_PRIOR.md`.
