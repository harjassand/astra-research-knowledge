# Independent policy-specific tail and unchanged-law transfer — PASS

2026-10-26. Replayed `receive_stationary_tail_lyapunov.py` and `receive_stationary_tail_same_law_transfer.py`; all mathematical output matched the frozen receipts and original timing-bearing bytes were restored. No sparse solve or optimizer replay. Extra independent checks are `independent_stationary_tail_checks.py`.

## Exact policy and transition semantics

The vector is hash-bound to `three_axis_control_actual_paid_policy.json`, exactly component0 of the audited40-bit16 mixture and inherited through the accepted80-bit17 mixture. The transfer checks this identity and the latter's exact(1−alpha) reweighting, rather than merely identifying a similarly named controller.

Independently rechecked all3844 helper states are strictly inside the correlation body. Every one of3338 directed ordinary transitions belongs to a positive-probability binary split with exact barycenter and q-null difference. At each state the three nonnegative axis-stop counts plus all ordinary action counts sum exactly to the policy denominator2^40. The stop terms terminate by the previously received complete axis chord laws and do NOT contribute to the ordinary substochastic matrix P. Both ordinary children do contribute with their exact conditional probabilities. No positive branch is discarded.

The saved rational vector obeys1<=v<=958733/65536<15, root v=3233431/262144<13. Every row satisfies Pv<=(15/16)v, with positive minimum slack89843/1048576. These are exact rational inequalities, not a spectral-radius estimate from a numerical solve; unreachable states are covered too.

## Tail coupling and counter convention

Positivity gives P^n1(root)<=P^nv(root)<13(15/16)^n. P^n1 is the probability of performing n ordinary transitions before selecting a stopping macro. This implies almost-sure absorption and the required tail bound for the existing policy.

Couple the original and truncated policies through all identical ordinary decisions until forced completion. On the tail event, both terminal outcomes lie in[-1,1]^3, whose diameter is<4; arbitrary continuation/forced full-chord couplings therefore cost at most4 times that probability. No RMS substitution, terminal-density assumption, or special chord orientation is needed. Using N−1 ordinary transitions is conservative for either relevant before/after counter convention.

Exact integer-power comparisons receive52(15/16)^(N−1)<=2^-b for:

- N21504,b1024: SAME current finite instance;
- N19968,b1024: SAME earlier finite instance;
- N1024,b80: a DISTINCT optional shorter instance, not adopted.

The root categorical draw is outside the inherited branch's ordinary-transition counter. Its probability multiplies the conditional tail; it does not change the cutoff rule.

## Scalar actual-source consequences

The old raw source upper, exact root probabilities,21504 cutoff, coupling and separate AC(10^-24) kernel remain unchanged. Replace only the loose conditional1/4096 estimate by2^-1024, weighted by the exact baseline probability. Received SAME-law finite+AC upper bounds become:

-16-law: .06755186814622662;
-17-law: **.06718566499649657 < .0672**.

Thus this new gain is precision-only, not another control/root/cutoff change. The raw17 upper remains .06718566499159759. Atomic and AC law interpretations remain separate, and AC is paid once.

The already received raw actual-law decrease against the SAME rational finite source was .0003954267442488992. Paying both new tails and both AC transfers now leaves a strictly positive finite+AC decrease .0003954267344509399. The prior negative bound using coarse tails remains a correct historical failed estimate. Neither result orders the exact true cosine-source distances; their improved certified uppers are separate statements.

No source membership, global optimum, new selected affinity law, or shorter-law adoption follows. All upstream source receipts remain unchanged.
