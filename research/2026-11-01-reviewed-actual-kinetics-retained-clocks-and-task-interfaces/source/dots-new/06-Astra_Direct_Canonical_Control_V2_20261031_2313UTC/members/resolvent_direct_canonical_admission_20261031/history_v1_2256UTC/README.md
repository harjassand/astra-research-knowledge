# Direct canonical admission — separate unreviewed strengthening

Do not merge this branch into the accepted resolvent-control package or infer
that either earlier receipt covers it. This is a prospective stronger admission
rule, not a reclassification of any historical acquired data.

## Result
Acquire/check an ordinary hidden-K canonical witness X,delta directly from the
received action-effect coefficients. Its signs/column sums yield

    ||w_goal||_infinity <= maxdiag(X)/delta,
    true normalized pointwise policy regret <=
        2 gamma/(1-gamma) * eta * maxdiag(X)/delta.

This is uniform over all later adaptive bounded action-dependent reward tables
constant on the learned blocks. No source hhat/delta_h accuracy, old kappa-q
condition or exact closure promise is required. The ordinary r-variable LP gets
its objective from X: h_c=(X^-1 1)^T. The positive stochastic decision-model
interpretation remains computational, NOT a predictive block law.

Strong ordinary hidden-K, ALP and successor-feature learners receive the same
certificate and obtain the same improvement. Historical novelty of this precise
source-error/admission join has not been established. The canonical LP is an
established ordinary method, not a new generic complementarity solver.

## Evidence and limits
`check_direct.run()` currently gives 557 exact checks and 8 refusals, zero source
calls. It reuses five existing algebra fixtures, compares both ordinary planners,
checks 36 noisy-family witnesses, receives the old actual batch, and tests external
task/model/core bindings. The same conservative valid eta=.001,gamma=.9 bound
refuses the older admission but passes this rule at requested .05 regret with
26901/1269500 (~.02119). This is an algebraic certificate comparison, NOT a newly
acquired empirical success.

The actual saved 4,096-episode/38,626-call batch still returns UNKNOWN at .01.
One explicitly vacuous tolerance20 test exercises successful-stop receiving;
it is NOT a useful empirical planning result. No observations were regenerated.

PROOF.md gives a noisy-family success calculation on the EXISTING four-state
source as task discount tends to1. A healthy acquired canonical gap removes an
unnecessary vanishing source-objective margin: endpoint radius O(epsilon*(1-gamma))
suffices. Expected source-call sufficient scaling becomes (1-gamma)^-3 instead
of the former conservative (1-gamma)^-7, at fixed accuracy/confidence/rank. This
is a comparison of sufficient proofs, not lower bounds or an exclusive algorithmic
advantage. The explicit schedules remain enormous (already >10b episodes at
.9 in the conservative .1-regret calculation), all unexecuted. Do not optimize
those generic constants or call them necessary acquisition prices.

Full source calls, truncated episode/coin/label work, failed attempts, statistical
receiving, exact finite-bit witness construction/checking, retained n-label map
and deployment sensing/execution remain paid. The actual SymPy backend can refuse;
positive candidates are checked exactly, not trusted because of solver status.
Generic rational LP gives the structural polynomial-bit consumer; implemented
simplex / policy iteration is not claimed polynomial worst case. Entry-bit fields
are scoped, not full internal-arithmetic or peak-memory ledgers.

## Receiving interface
`compile_model` binds an already received core containing r,m,gamma,eta,Bhat; no
h fields are needed. Its output may have a valid nominal model but UNKNOWN uniform
source-regret admission. `verify_uniform` binds caller core/model/tolerance and
recomputes every witness/transition identity and claimed uniform bound.
`plan_small_lp` and `plan_model` independently check their exact outputs and
actual per-goal regret bounds. `receive_refinement_attempts` performs the unchanged
full endpoint count receiver for every fixed batch, pays every attempted compile,
and uses the new admission as its stopping test. It starts from caller-supplied
actual native features, not useful partition advice. New partitions require fresh
validation; source iidness/nonanticipation/identity remains an external premise.

## Nonmutating replay
From this directory with Python and installed SymPy:

    PYTHONDONTWRITEBYTECODE=1 python -c 'import check_direct as c; print(c.run())'

About10 seconds on the present environment, including exact powers for cap
159,428; zero source calls, no artifact edits. Script main writes JSON; use run()
for a frozen replay. Dependencies are explicitly pinned in the manifest: the
accepted original source receiver/fixtures and separate canonical comparator
fixtures. No installs, uploads or external actions.
