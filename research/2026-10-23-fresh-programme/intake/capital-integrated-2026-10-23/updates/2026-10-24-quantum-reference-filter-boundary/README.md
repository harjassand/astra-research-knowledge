# U reference filters and the exact weak-live-table boundary — 24 October 2026

This selected update preserves new source work on two related replacement routes for quantum live tables: common-reference POVMs and smooth local filters, followed by an exact limitation for a weaker success/fine/abort interface. The finite predicate-mass and parity theorems already integrated remain unchanged.

## Conditional filter constructions

A question-independent common reference POVM with Loewner bounds on every full-input coarse effect gives complete local success/fine/failure instruments on one offline resource. It preserves each accepted fine entry and bounds one-sided success masses by the opposite side's domination radius. The radius is a real operator condition: one fresh-input-copy example forces it to grow exponentially even when the desired live law can be made trivial by discarding the irrelevant tag. There is no universal small-radius theorem.

The U0117 revision adds local spectral clipping to sub-POVMs, with a payoff-weighted rejected-mass bound and an explicit loss-aware change from the original accepted event to the clipped event. It also retains the direct joint-abort strategy when its normalized total success mass is close to one. Neither route treats a successful conditioning event as free or replaces full resource and timeout accounting.

A quadratic-gap bound follows only under a uniform payoff-weighted moment premise at the greedy-selected histories of the repeated strategy, with its stated prefactor and source assumptions. That premise is not proved for arbitrary strategies. The table-first commuting extension preserves actual referee KL drift through finite-table approximation; it is not a new density theorem, efficient compiler, or general answer-free repetition result.

## Exact live-table mass obstruction

For complete local binary success/fine/failure POVMs, the source proves the weighted CHSH inequality

`max(G_A, G_B) >= sqrt(2) p (1 - 2 alpha_CHSH)`.

A legal two-round copied-question construction embeds a perfect PR live bit table in a base game of value one. Its original tested-event mass is `p0 = (1 + 1/sqrt(2))/2`, and exact live-table preservation forces `max(G_A, G_B) >= sqrt(2) p0 = (1 + sqrt(2))/2 > 1`, even after the old coarse history is forgotten. The source also records a product-sign extension with a `2^(r/2)` mass ratio and a three-shared-bit classical upper witness for the single PR table; it does not determine the quantum optimum.

This blocks a universal **exact live-table plus both one-sided masses at most one** replacement at that interface. The source game has value one, so a repair that preserves payoff alone may discard the irrelevant PR fine correlations and win perfectly. The obstruction is not a lower bound on actual Jensen gaps, conditional QRE, reconstruction error, or an answer-free repetition theorem. It does not invalidate the earlier predicate-mass theorem or establish a general no-go.

## Evidence status

The selected source proofs and records are preserved byte-for-byte in [the manifest](source_manifest.json). Source reports and the finite replay were read; the replay was not executed here. Independent checking, physical implementation, resource efficiency, historical novelty, and a general repetition rate remain UNKNOWN. The broader U units remain in progress.
