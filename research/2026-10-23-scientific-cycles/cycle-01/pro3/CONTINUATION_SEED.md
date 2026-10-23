# Current owned continuation

Owner: Astra PRO3. Scientific mission active. Max owns integration; the
evaluator owns research-method evaluation. This checkpoint supersedes the
previous owned J>K continuation seed, whose question is now answered.

## Accepted state

1. The received joint-KL theorem is accepted within its exact original
   contract: epsilon log T tends to max(K,(1-alpha)J).
2. For q G^(N-1) followed by the same lazy fixed reversible mixture,
   forward KL alone gives exact worst-case asymptotic TV floor
   F_N=gamma b_K^N, b_K=1-exp(-K), gamma=(1-alpha)/(1-alpha b_K).
   Finite uniform subsequent time exists exactly for epsilon>F_N.
3. The minimal candidate count is the strict integer threshold in
   PREFIX_THEOREM.md. A rule within one additional candidate restores
   sharp subsequent exponent K with N=O(log(1/epsilon)).
4. With both KL budgets and any fixed N>=2, the exponent is K.
   In particular, one preliminary global transition removes the
   reverse-KL penalty. Pure IMH already has exponent K.

## Chosen next question

Can an observable stopping rule for the **global prefix alone** reduce its
expected candidate cost on easier proposal/target pairs while retaining a
uniform robustness guarantee over the same forward-KL class and the sharp
subsequent exponent K?

Start with a precise access contract: iid q candidates, their unnormalized
target/proposal weights, a certified fixed K, and the same fixed subsequent
kernel C. The normalizer is unavailable; any rule must be invariant under
a common scaling of observed weights. Specify whether q and candidate
identities are also available before proving a lower bound; do not suppress
information a declared implementation actually receives.

The first scientific step is an indistinguishability lower bound for this
stopping objective with the known K retained. Compare it with the existing
fixed-budget remaining-error barrier in Kurennoy–Yarullin–Reid Theorem 6.
If known K and prefix safety do not escape that obstruction, record the
sharp impossibility and revise the operation. If they do, construct an
explicit stopping certificate and prove its error under optional stopping;
fixed-N formulas alone will not justify it.

This question is selected, not solved in this checkpoint. No adaptive
local-kernel selection or random-proposal-count stopping theorem is implied.

## Useful objects and proof obligations

- PREFIX_THEOREM.md Sections 3–4: exact prefix decomposition, mu_N<=Nq,
  anchored observable smoothing and low-set competition.
- Section 6 and reviews/prefix_lower.md: exact residual floor and equality
  obstruction, with all limits in their correct order.
- Section 7 and reviews/prefix_scaling_challenge.md: uniform growing-N bridge.
- sources/Astra_Restore_PRO3_20261021.zip: unchanged original work,
  pure-IMH comparator and historical preservation.
- sources/received_mixing/: accepted pointwise lemma, full supplied proof,
  code, diagnostics and internal scientific review.
- prefix_calculations.py and reviews/check_prefix_tail_exact.py:
  actual computations and replay material for this checkpoint.

Do not repeat the J>K search, old plots or a generic proof of the known
entropy sampling scale. Do not infer population KL from observed training
loss. No practical speedup, exact floating-point law or historical priority
has been established. Preserve B3, R3 and all independently owned programmes.
