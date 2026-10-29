# Independent review of completed v2 runs and public large-K routing

2026-10-29. Supersedes only the absence-of-N4096-output statement in REVIEW_v1; v1 remains an immutable review of its own frozen version. Governing file bindings are in `check_exact_v2.json`.

## Accepted

* All 12,288 N4096 learner projections have exactly PSD rational effects summing to I, exact input chains driven solely by the recorded Bell-label/flag-probe outcomes, and rational primal-dual gaps at most `1/4294967296`. Maximum gap is approximately 4.419754e-15. This bank uses the unchanged v1 solver under a resumable v2 driver.
* All 733 shadow updates in the three mixed-role N1024 runs pass identical checks with their correct importance-weighted step and `xi=1/(256*1024^2)`. Maximum gap is approximately 3.341123e-14. These runs use the v2 solver, although their modest label multiplicities follow its ordinary Dykstra proposal route.
* Independent reconstruction of the high-recoverability source isometry, conditional retained-memory updates, evaluation instruments, predictable scores, terminal diagnostics and floating EXP3 weights reproduces average scores within 5.56e-16. All recorded branches have positive probability. This is a separate floating-physics check, not an exact physical certificate. Source is unchanged from the earlier fixture. The new meta record bank is exactly identical to the original float-fixture bank.
* The public v2 solver, unlike v1, genuinely routes the overload test family at K=2^40,2^60,2^120,2^512,2^2048 without converting those multiplicities to floats. Independently checked output gaps are about 5.25e-17 against requested xi=1e-12. A single-block indefinite-center test with K=2^2048 returns the unique feasible effect with exact gap zero.

The source inspection confirms correct role separation: the candidate evaluated on an evaluation call is predictable, while the shadow gradient uses the independently chosen role and no inaccessible conditional source matrices. Those matrices are used to simulate acquisition and score diagnostics, not feed the learner. The learner update coefficient is eta*(r/q)=8 eta. EXP3 uses the evaluation-role probability 3/4 in its importance weight.

## Useful failures / retained limitations

Public v2 fails closed on two simple boundary cases at K=2^2048 and xi=1e-12:

1. Seen center .1 I, default center .8 I: gap about 1.81e-8.
2. Seen center .25 I+.25 X, default center .75 I-.25 X: gap about 1.10e-8, despite the input already being feasible.

These are preserved in `check_public_interface_v1.json`; the author was notified. Boundary-dual candidate quality is the issue, not acceptance of invalid certificates. Thus the five overload examples do not establish general solver reliability, termination or complexity. No tolerance relaxation is accepted. Later repairs need separate immutable version tests.

The N4096 negative fixture still yields learned averages .39705/.38969/.38370 below identity .44759. The mixed-role positive fixture remains a conditional-path simulation, not a confidence-certified advantage, hardware result or independent replication. Exact rational learner updates close an implementation obligation; they do not make floating source acquisition, arbitrary flag dimension, floating meta-selector arithmetic, randomized pruning or physical receiver compilation exact. No broad-noise practical architecture or scientific novelty claim is accepted by this review alone.
