# Independent review: corrected scalar complementarity study

Reviewer: `/root/cycle11_quantum`. Date: 2026-10-23.

**Verdict: PASS within the declared proof-budget/family-exclusion scope, after three repairs.** I read the initial and corrected code, plan and saved results against the owner proofs independently inspected in `quantum_review.md`. No owner suite or new scalar calculation was rerun by this reviewer. The root reran only its new corrected scalar calculation. This is not a new invention test, an external mathematical certification or a universal complementarity theorem.

## Final source binding

| File | Bytes | SHA256 |
|---|---:|---|
| `meta_study/complementarity.py` | 5,618 | `88b74310ea39e283c6a3f96dea81b3874b34221a06db5e556e9763f196d89f03` |
| `meta_study/ANALYSIS_PLAN.txt` | 3,321 | `7aa702bf867b5c7a68b8a082e1e0975079ea6989dbc959c1dd207d276fba76a3` |
| `meta_study/COMPLEMENTARITY_RESULT.json` | 7,777 | `d7ced9d2f597274d78b2636f61c2172f08e12e7647427f96d4a35871061886d9` |

The initial versions and correction explanation remain under `meta_study/failed_initial/`. Initial detailed review is preserved separately as `reviews/meta_complementarity_review.md`; it records the defects before correction and is not a competing final verdict.

## Mathematical checks

- The `ln2` interval follows from `2 atanh(1/3)`. For `N` retained terms the positive tail is at most `9/[4(2N+1)3^(2N+1)]`, exactly as implemented.
- The three closed central-binomial sums follow by telescoping from `a_n/a_(n-1)=(2n-1)/(2n)`. The parity split correctly recovers both the original variance `v_k` and the exact charge moment `c_k`. The direct-sum comparison covers 79 cases, `k=2,...,80`; it validates this new arithmetic, not the entire owner theorem.
- The square-root bounds have the correct directions and are checked by exact rational squaring. The raw-square coefficient is correctly `s=(ln2/8)b`, matching the owner's polynomial square factor.
- Every selected `k` lies in the owner's proved window at `r=1/256`, `b=r/k`.
- The structured slack uses lower affine inward margin minus upper correction and upper retained target. This is a valid sufficient comparison.
- The raw charge lower divides a lower positive numerator by an upper positive denominator. Subtracting the upper offdiagonal correction therefore gives a valid lower bound on complete bulk drift, conditional on the owner's all-length identities.

## Repairs completed

1. The initial generic-exhaustion calculation subtracted two upper enclosures. The corrected source uses a **lower generic allowance minus an upper affine margin**, and asserts positivity. Thus it now certifies the intended direction for the exact allowance.
2. Fields named lower/upper now use directed decimal rounding (`ROUND_FLOOR`/`ROUND_CEILING`). The exact internal rational comparisons and displayed inequality directions agree.
3. The plan and output explicitly state that this is **not a factorial intervention holding the complete input fixed**. Both families use the same polynomial square factor, but the delivered pattern-normalized density additionally contains a charge-only tilt `T` absent from the source's raw-square family. No normalization-only causal claim is made.

No remaining concrete mathematical or interpretation defect was found within this review's scope.

## Result accepted within scope

At all seven selected `k`, the structured sufficient correction budget preserves a positive certified inward margin, whereas the supplied generic allowance exceeds that same affine proof budget. At `k=131072`, the raw-square family's actual bulk drift is bounded below by

`3.27039186474546957999791783456e-7 > 0`.

This is a finite witness excluding the stated raw family from the strict inward-drift route at that parameter. Negative lower bounds at the six smaller selected values are explicitly inconclusive. They do not establish inward drift.

The saved corrected run reports approximately 1.08 s CPU/wall and 12,288 KiB process high-water on Linux. Those are costs of this scalar arithmetic only. Scientific design, model inference, total review and integration costs remain unknown.

## Strong conventional controls and final interpretation

The generic inequality is one deliberately coarse sufficient estimate, not the strongest possible conventional analysis. Alternative state-specific trace bounds, other positive families and other drift proofs remain available. The existing cubic and clipping constructions already yield useful rates under the same channel contract and beat the new conservative bound at several finite parameters. Thus the study does not show that both specific innovations were universally necessary for progress.

Likewise, Ultra's ordinary periodic receiver already produces useful actual coherent information; its finite-size performance challenges any claim that only the newer logarithmic construction can give useful output. Raw single-copy coherent information being negative is not zero distillable entanglement, and an `r eta` error upper bound becoming useless is not proof of protocol failure.

The accepted inference is **quantified complementarity within the delivered sufficient argument, plus one actual family-level exclusion**. It supplies evidence about why this construction succeeds. It does not establish a general discovery policy, agent-strategy superiority, research amplification or recursive scientific intelligence.
