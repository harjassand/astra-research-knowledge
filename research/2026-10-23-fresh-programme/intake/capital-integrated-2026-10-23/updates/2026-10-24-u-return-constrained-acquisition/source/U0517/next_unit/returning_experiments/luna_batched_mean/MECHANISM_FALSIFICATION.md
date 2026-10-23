# Bounded symbolic check of acquired-return licensing

**Scope:** exact hand audit of the two-action family supplied in the coordinating message; no implementation, source query, benchmark, or novelty claim.

Let \(\theta,\phi\in\{0,1\}\). The immutable candidate world is \((M_\theta,H_\phi)\), with states \(H_\phi,S_\phi,T_\phi,D\), binary actions \(a,b\), and binary outputs. Rules are:

- At \(H_\phi\): \(a\) outputs 1 and moves to \(S_\phi\); \(b\) outputs \(\phi\) and moves to \(T_\phi\).
- At \(S_\phi\): \(a\) outputs \(\theta\) and moves to \(H_\phi\); \(b\) outputs 1 and moves to \(D\).
- At \(T_\phi\): \(a\) outputs 0 and moves to \(H_\phi\) iff \(\theta=0\), otherwise to \(D\); \(b\) outputs 0 and moves to \(H_\phi\) iff \(\theta=1\), otherwise to \(D\).
- \(D\) loops on both actions with output 0.

## Exact return and information checks

1. Starting at \(H_\phi\), `aa` yields outputs \((1,\theta)\) and ends exactly at \(H_\phi\) for each \((\theta,\phi)\). It is a returning discriminator for \(\theta\), leaving both \(\phi\) values in the version set.
2. From any \(H_\phi\), `b` outputs \(\phi\) and reaches \(T_\phi\). Once \(\theta\) is known, append `a` when \(\theta=0\) and `b` when \(\theta=1\). The appended action returns to \(H_\phi\) for every remaining candidate. Its output is 0, while the earlier `b` output reveals \(\phi\). This is a returning discriminator for \(\phi\) in the post-`aa` version set.
3. Before learning \(\theta\), a returning experiment whose first action is `b` is impossible: at the reached \(T_\phi\), `a` returns only in the \(\theta=0\) candidates and `b` returns only in the \(\theta=1\) candidates. Both choices emit 0, so no observation branch can avoid the nonreturning \(D\) candidate. Since \(D\not\sim H_\phi\) (`a` emits 0 at \(D\) and 1 at \(H_\phi\)), no continuation can repair that branch.
4. This is not a claim that the later test cannot be executed immediately in the *original* state: the composite contingent policy can start with `aa`, observe \(\theta\), then run `b` plus the appropriate return action. Precisely, the newly licensed operation is the standalone `b`-test from the anchor under the narrowed version set. A belief-space planner on the original version set can already synthesize the composite policy.

No `reset` action or observed state-ID channel is present. Binary outputs are not unique state labels: output 1 occurs at both \(H\) under `a` and \(S\) under `b`; output 0 occurs at multiple states. The first word's output is an ordinary consequence of the declared machine class, not a teacher-supplied counterexample. Nevertheless, this is an engineered finite automata example whose mechanism is standard conditional/safe belief-space planning. It supports the access-preservation distinction but no algorithmic novelty or comparative advantage. The complete candidate class is the planner's shared prior; the class itself supplies substantial structure.

## Relation to the frozen planner reduction

The sequence `aa` strictly refines the version set and returns; its observed second output determines which return continuation makes the `b`-test safe. This is a concrete witness to the conditional experiment interface. It also confirms the earlier reduction: an ordinary finite-belief contingent planner can plan `aa` then the branch-specific `b` return, while after `aa` it can plan the now-safe `b` discriminator. Calling the latter a newly licensed test describes the updated feasible action tree, not a new planning primitive.
