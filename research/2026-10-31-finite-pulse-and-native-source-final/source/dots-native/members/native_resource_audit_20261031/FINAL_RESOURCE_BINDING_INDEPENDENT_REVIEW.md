# Final resource-report binding: independent review addendum

31 October 2026. PASS as a conservative resource/comparator diagnostic, not a final gate count or certified elimination theorem. This addendum preserves and supersedes only the resource-version discussion in the earlier energy/activity receipt; it does not change that mathematical receipt or any frozen theorem.

## Exact current sources

The entire report `RESOURCE_AND_COMPARATOR_AUDIT.md` was read: SHA-256 `a160cd14a0c7dbb5feb20bd9478d5af6e5be149e220a3dfc8d1641cbc887aa6e`.

Current live code and data were read and hashed:

- `resource_ledger.py`: `b6b3100e07008cec6f3416cf8806474ddc98c4020fc073dac5e72131a761e8fd`.
- `resource_ledger.json`: `1dfdaf137731a1c5db8e2917f5da4be8129a04ee7cfcfac62303a2b2f4b721d9`.
- `small_cq_dense_check.py`: `280265a767d42f672b6ad5a83c9914877fced844c50afa3e0d695cb48f763c9f`.
- `small_cq_dense_check.json`: `bb10a018882a5cbdc6d843a671ce2f1c9ecf1ecd6714d9a0d3c40c6d2179a8cc`.

The immediately preceding ledger versions are separately preserved as `resource_ledger_frozen_dd41d63c.py`, SHA `dd41d63c76fc6ec42b179223ba16105ff2eb3f385331b52868a6575807ca211e`, and `resource_ledger_frozen_25eeb1c4.json`, SHA `25eeb1c44060249114da1d5b65ee2ab055ab974f99a8cf825ef686985e2abf43`. The live code differs from that preserved code only by adding explicit precision-scope metadata. This is not a claim that the still earlier 100-times-operation-proxy source bytes were preserved: the earlier independent receipt records what was actually inspected then, and remains unchanged.

## Corrected precision interpretation

All 30 live ledger rows were regenerated in memory and matched exactly. The renamed field `kernel_precision_bits_lower_bound` ranges from 291 to 339 bits. It uses beta/[10^4(Kcap+1)], justified only as a lower floor under the stated padded interval layout and its uniform worst-case subdivision rule. It is not a universal algorithmic precision lower bound, a final per-gate tolerance, or an enumeration of all inner operations.

The report now explicitly says that real LCHS/SVA, arithmetic and synthesis counts require tighter budgets. This addresses the earlier caveat rather than pretending the multiplier 100 supplied those counts. The original count/window/virtual caps and padded-slot figures are unchanged, including 3,123,922,221 slots for n=4, epsilon=.01 at the high-rate threshold. Their match to frozen f503c800 formulas remains as checked in `ENERGY_ACTIVITY_AND_RESOURCE_INDEPENDENT_REVIEW.md`, SHA `4bb1b450ae3ba82b527655eabbbc97c5bc3034b92f173a70e35d10d9b5a68a48`.

## Dense ordinary comparator: construction and rerun

I read the complete dense-check source and reran it in memory, intercepting its output writer so the saved data were not overwritten. The reported finite-versus-white trace norms reproduced exactly in this run; the independent eigenvector-reconstruction disagreement differed only in negligible final floating-point digits. No bitwise equality claim is made for every floating-point diagnostic field.

The classical generator uses column orientation Q[y,x] and exact intended heat-bath rates computed in double precision. The Poisson equation uses -Q^T + 1*pi^T, which imposes the centered solution for the backward generator. Its correlation pi^T diag(z) w is 1.0011911848070056. Column-major system vectorization gives the commutator I tensor H - H^T tensor I. Thus both the 64-dimensional CQ generator and the 4-dimensional effective system generator are assembled consistently with the report's stated model and initial state.

The regenerated system trace-norm discrepancies are approximately 1.6704e-6, 5.1102e-7 and 1.8063e-8 at lambda = 305954, 10^6 and 10^8. The retained-CQ discrepancies are approximately 9.7907e-4, 5.4156e-4 and 5.4156e-5. At the last rate the expm/eigendecomposition vector disagreement is approximately 1.1180e-7 and the trace defect approximately 1.8063e-8. The report correctly treats the final system discrepancy as unresolved numerical floor, not measured asymptotic physical error. Eigenvector comparison, positivity and trace checks are diagnostics, not rigorous error certification; they can share numerical limitations.

These observations apply to one stationary-CQ input and the displayed localized single-qubit coupling. They do not establish arbitrary-input diamond error, errors under all instruments, or an asymptotic elimination theorem. A small dense calculation being plainly feasible here is nevertheless a legitimate ordinary negative comparator for the huge conservative padded construction.

## Comparison and final status

The report correctly keeps three unlike quantities separate: padded kernel slots, generic acquired-stack normalized action, and expected classical ticks/flips. Generic action 1 + sqrt(lambda) + 2n*lambda follows from the stated physical encodings; it is not itself a gate count. Classical path tick counts concern the CQ task, not arbitrary coherent source inputs. Neither numerical column comparisons nor the small dense example establish a quantitative crossover against the best ordinary algorithm.

The corrected report openly retains the cost failure: billions of conservative padded slots precede nontrivial kernel/arithmetic costs, and no practical advantage or final executable quantum resource estimate is earned. The separately accepted energy-form count refinement cannot retroactively change this ledger without a new full resource substitution. No scientific correction is needed to the current report within these boundaries.
