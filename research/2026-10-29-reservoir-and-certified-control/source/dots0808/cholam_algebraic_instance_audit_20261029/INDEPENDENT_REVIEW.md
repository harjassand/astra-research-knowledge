# Independent review: perturbed Choi–Lam algebraic certificate
2026-10-29. One executed exact instance, separate from generic expected-bit theorems.

## Decision
Accepted: the stored rational lower/upper pair globally certifies the original sphere objective to gap1.2935983156279698e-5, below the requested1e-4. Original lower is approximately−1.293598313633626e-5 and feasible upper approximately1.994343804046699e-14. The independent known minimum0 lies inside this interval. This demonstrates a different exact mechanism on the deliberately non-SOS example; it does not establish generic runtime, hardware feasibility or an unknown-noise protection advantage.

## Independent complete algebraic replay
I rebuilt the perturbed quartic from exact input coefficients, independently computed a grevlex Gröbner basis using Buchberger (author used f5b), counted40 standard quotient monomials, and converted it by FGLM. The three resulting monic shape equations exactly equal the stored author basis. Their leading monomials are x,y,z^40. The univariate factor is squarefree.

A fresh exact complete real-root isolation with `fast=True` found28 real roots. Every one of the28 stored final intervals is disjoint, ordered and sign-changing. Together with the complete count28, this proves exactly one real root per interval and none omitted; cached root-count assertions were not trusted. Independent projective boundary calculations in all three q0=0 charts return the unit ideal, excluding all boundary stationary rays. The full algebraic replay completed in about307.6 seconds in this shared environment; that is one observed run, not a general complexity bound.

## Exact value and perturbation checks
All35 original, perturbation and perturbed coefficients were checked for exact equality. The exact perturbation l1 budget is1.1875e-5, below epsilon/4. This implies a uniform objective change bound on the unit sphere; it is not a probabilistic assumption.

At each stationary chart root, Euler's identity gives the normalized perturbed objective as partial_0F(1,x,y,z)/(4(1+x²+y²+z²)). My independent Fraction arithmetic evaluates the shape-coordinate intervals and this expression, reproducing all28 stored rational value bounds exactly. Denominators are bounded away from zero. Taking the minimum lower endpoint and subtracting the exact perturbation budget reproduces the original global lower bound.

The final returned quaternion is exactly rational with squared norm1. Independent evaluation of the ORIGINAL quartic reproduces its exact feasible upper bound and the stated final gap. The numerical/arbitrary-precision proposal procedure need not establish globality: feasibility and exact evaluation suffice for the upper bound. The known AM-GM minimum0 was used only as an external sanity check, not as a shortcut in the replayed lower bound.

## Timing, cache and scientific scope
The supplied fast certificate combines cached initial root intervals with exact fast refinement. The original default isolation/refinement runs had substantial option-dependent delays. The additive execution-cost clarification correctly says the redundant slow run was stopped and that fast initial isolation is exact, not floating approximation. No unexecuted optimized end-to-end runtime is inferred by combining best timings from separate runs.

This one perturbation uses its own seeded129-point coefficient choices; it is not the16384-point law in the separately reviewed generic-template theorem. It therefore proves neither that theorem's sampling probability by experiment nor a general fixed-z shape success rate. The generic theorem now has its own separate receiving status; the older working document's generic-status wording does not govern that other result.

No instance receipt here accepts the separate Macaulay constructor, actual scalar-resultant diagnostic, lambda-primitive implementation, online FTPL performance, or a source-clock privacy mechanism. Root/candidate caches, previous timed-out partial runs and the later generic mathematical theorem remain distinct evidence.

## Evidence
`check_shape_roots.py`, `shape_roots.log`, `shape_roots_checks.json`: full independent exact ideal/root/boundary replay.
`check_values.py`, `value_checks.log`, `value_checks.json`: exact all-value, perturbation and feasible-candidate replay.
The receiving receipt binds the frozen instance plus the additive execution-cost clarification, without modifying author files.
