# Ordinary canonical decision-model comparator — separate post-freeze addendum

This is NOT included in the accepted resolvent-control ZIP or its whole receipt.
It implements the strongest ordinary structural comparator requested at that
boundary, using precisely the same already received signed moments/certificate.

## Result
Morris's ordinary hidden-K canonical-form LP compiles the r-dimensional signed
Bellman constraints into an (r+1)-state stochastic discounted decision model.
Ordinary exact policy iteration then returns the same nominal solution and the
same source-regret certificate as the primary small LP. No new source calls,
raw reset factorization, R inverse, full H, or predictive block model is needed.
This strengthens the conventional method, not a claim of an exclusive win.

The exact 327 action-reward tests reuse five existing algebra fixtures. All pass:
1,685 checks and 3 receiving refusals; 540 total policy-iteration evaluations.
The strict weak-closure, singular-R and genuinely nonclosed cases are included.
On the old nonpredictive fixture, the compiled discount is 450/2989, unlike the
original 9/10; its transitions differ from even averaged observed block dynamics.
The small exact fixture is not a new workload, acquisition experiment or practical
performance claim. All current tests execute zero forward source calls.

PROOF_AND_PRIOR.md also constructs the conventional known-model common-reset
alternative, including a common-reward embedded decision model. Its exact raw
factorization is stronger than resolvent action-effect closure. A scoped familiar
Bernoulli-factory argument shows why independent row samplers do not automatically
provide an exact maximal-common-component reset flag. Approximate ordinary reset
learners, extra couplings/probabilities and stronger domain promises are NOT ruled
out and must receive the same metadata.

## Receiving and cost scope
`compile_model` binds the already trusted received core and its acquired all-goal
admission, and checks a proposed transform by exact rational inequalities and
nonsingularity. `plan_model` binds the core/model/reward hashes, reconstructs the
transformation identity, executes ordinary stochastic policy iteration, and checks
exact Bellman equations and original nominal residual. It does not authenticate
the upstream data event or replace the full source receiver. No new observation
interface, microscopic control/sensor upgrade or broader reward scope is added.

Compile: r²+1-variable, mr(r+1)+2-constraint ordinary rational LP; matrix arithmetic
and O(mr²) retained coefficients plus X, all coefficient bits, are paid. Per goal:
read the mr rewards, transform verification, actual exact policy-iteration
inversions/evaluations and policy output. `max_transform_entry_bits` and
`max_evaluated_value_entry_bits` measure the indicated entries only, not all LP or
matrix-inversion intermediate arithmetic or peak memory. Actual exact arithmetic
runs are timed; no constant-bit accounting or polynomial worst-case claim for
SymPy simplex / this policy-iteration implementation is made. Generic rational
LP remains the polynomial-bit fallback. A small canonical gap may make iteration
expensive. No favorable gap is assumed by the source-acquisition theorem.

An initial SymPy free-variable call incorrectly proposed the zero transform as
optimal on a positive-witness instance. The result was refused. Its original
code and observed diagnostic are preserved under history/. The current ordinary
translation X=U−1 uses implied [-1,1] bounds and independently verifies every
accepted result. This is a backend failure, not a failure of the hidden-K theorem.
Every development/replay compile is real work; none is statistical acquisition.

## Reproduce nonmutating
From this directory, with Python and installed SymPy:

    PYTHONDONTWRITEBYTECODE=1 python -c 'import check_canonical as c; print(c.run())'

This writes no files and performs zero source calls. The script main writes its
result JSON, so use run() for frozen replay. Dependencies are the accepted sibling
`resolvent_control_reuse_20261031/control.py` and `check_control.py`; their exact
hashes and the underlying whole receipt are pinned by this addendum's manifest.
No installs, external operations, publication or upload. No historical novelty
claim: Morris/Klaus/ALP/successor-feature priors are explicitly credited.
