# New calculation and operation contract

Written before the principal's new diagnostic outputs were examined.
Scientific date: 22 October 2026, Australia/Brisbane.

The mathematical contract is SAFE_LOCAL_THEOREM.md. The implementation is
ordinary two-stage delayed acceptance with a fixed first-stage q-MH proposal,
and fixed alpha. This work uses no empirical data, fitted KL estimate,
experimental intervention or laboratory interface. No discovery holdout is
meaningful for exact symbolic identities and specified finite-chain checks.

## Principal finite-chain calculations

Use alpha=1/2 and the inherited positive three-state funnel family with
p=1/50, b=1/2, r=p*2^(-20), s=p*2^(-40),
pi=(p,s,1-p-s), q=(r,b,1-b-r). The target-independent symmetric Q has
A--B probability 4/5 and B--C probability 1/5, with diagonal complements.
Compare ordinary pi-MH(Q), delayed acceptance via MH(Q,q) then W acceptance,
and pure IMH. Calculate exact rational kernels, reversibility, qL/q, actual
deterministic-time laws and expected operation rewards. A finite-horizon
rational check and higher-precision Decimal matrix calculations will be
distinguished. Validate D(pi||q)<=1; if it fails, report that failure rather
than tune the family into the class.

Predetermined horizons: n in {1,2,5,10,25,50,100,250,500,1000}.
Predetermined accuracy thresholds: epsilon in {0.1,0.03,0.01}.
For threshold calculations, deterministic matrix powering may find the first
integer crossing; this is not a literal run of that many sampler transitions.
The ordinary comparator is the strongest simple operation with the same
weight oracle, pure IMH, as well as the ordinary local/global mixture.

Report both global/local proposal counts and expected target evaluations.
Only the current state's target value is cached. A proposal of the current
state reuses that value. Every other proposed target value costs one oracle
evaluation if the relevant acceptance stage reaches it. First-stage q work
and local proposals are counted separately; no claim of a wall-clock exchange
rate is made. A fully disclosed finite target table could instead be sampled
directly, so these examples are theorem diagnostics, not evidence of an
application speedup.

## General-law checks

Check finite-step first-hit decomposition, the no-hit bound and propagated
warm submeasure on positive rational finite chains. Small exact cases check
the coded mechanism; they do not prove the arbitrary-measurable-space theorem.
Any counterexample to an attractive stronger bound is preserved, not hidden.

Decimal calculations use 80 digits and a separate 120-digit consistency run.
Agreement is a numerical precision check, not outward interval certification.
Exact Fraction checks require equality or rational inequalities without a
tolerance. No computation substitutes for the written uniform estimates.

## Scientific and resource acceptance

Accept the new theorem only if the first-hit submeasure, general initial-law
bound, growing-s uniformity and lower inversion survive targeted review.
Finite-time domination is not an acceptance criterion and is not expected
from the theorem. Preserve costs that defeat a practical interpretation.
Record actual script wall/CPU/RSS and elapsed research observations separately;
replay time and file size are not discovery cost.
