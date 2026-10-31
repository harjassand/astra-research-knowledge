# Separate post-freeze comparator: all open-loop words versus feedback

The accepted feedback checkpoint is unchanged. This independent comparator
consumes its received model certificate; it is NOT a standalone verifier of
that certificate or its external iid/fresh-probe premises.

## Deterministic exhaustive upper bound

Each retained action is B_a=M_a/D, with M_a a nonnegative integer matrix and
each row sum D=240000000. Let S=2^p and initialize y_0=S*b for the indicator
reward. For each word, use integer updates

    y_(t+1)=floor(M_a y_t/D), componentwise.

Because B_a is stochastic, induction gives 0<=y_t<=S and

    0 <= B_(a_t)...B_(a_1)b − y_t/S <= (t/S)*1.

All uint64 accumulations are safe: each row dot product is nonnegative and
at most D*S<2^64. No wrapping occurs, including within the accumulation.
Each concatenation expands both actions for every current prefix; splitting
at depth4 only batches the same complete binary tree and does not prune.
Thus all 2^24 words are represented exactly once. Taking the maximal grid
output gives a one-sided interval of width 24/2^32 for the true optimum of
this retained open-loop model. The maximizing word is also replayed with
unbounded Python integers and exact SymPy rationals.

The source fixture initial coarse law is one block point mass; the program
explicitly checks that interface. Arbitrary initial laws, action alphabets
and longer horizons are not silently supported. Smaller length0–8 calls are
backend tests only; no same-horizon feedback gap is reported for those calls.
The arrays compute backwards value products. Physical action order is the
reverse of the reported multiplication word, explicitly retained in output.

## One confidence event, not two independently reused budgets

The accepted polynomial feedback operator event covers all sequences of
acquired-block Markov policies. A global open-loop action at each time is a
member of that class (the same action in every block). Therefore the SAME
error E=0.014402306334221847 bounds both the learned feedback policy and
every open-loop word. If U is the deterministic coarse open-loop upper bound,

    true_feedback − max_word true_openloop
      >= coarse_feedback − U − 2E.

No old per-action norm event is needed. The old open-word error appears only
as diagnostic metadata, not in this inequality. No additional statistical
union, posterior-on-PASS assertion or physical sensor is inferred. This gap
compares expected terminal rewards under two different action-information
interfaces: feedback requires the microscopic label/map lookup supplied by
the explicit-state simulator. It is not a claim that open-loop computation
has been unfairly denied data; an open-loop policy by definition cannot use
realized intermediate state labels. Ordinary coarse-MDP methods using the
same acquired certificate obtain the same feedback capability.

## Executed result and costs

All 16,777,216 length24 words were checked. Retained-model open-loop optimum
is at most 0.3773533191997558. The acquired feedback policy value is
0.6244843518542954. Hence the displayed exact-rational bound gives true gap
at least 0.21832641998609595 on the same accepted good event.

This explicit exhaustive comparator pays 536,870,880 uint64 scalar products,
not a claimed efficient general open-loop planner. Peak bulk-array bound is
reported separately from small arrays/metadata/Python objects and implementation
internal scratch. The multiply temporary is divided in place, assigned to the
new frontier and explicitly deleted; the bulk count includes old frontier,
new frontier and that one temporary. A prior two-temporary expression and its
understated memory record are preserved as obsolete history. Additional
checks enumerate every word through length8 with exact rational operations
and reject an unsafe uint64 precision: 557 checks. No new source observations
are used; all original acquisition and sensing/lookup costs still apply.

This establishes a concrete task/interface distinction, not historical
novelty, practical end-to-end learning advantage, or superiority over all
same-information retained planning methods. It is not part of the earlier
feedback ZIP/source freeze; only a separate bound receipt can cover it.

## Nonmutating entry points

`exhaustive_openloop.run()` and `check_exhaustive.run()` return records without
writing files. Main scripts write their separate local result files only.
The former takes about one second on this workspace; not a timing guarantee.
