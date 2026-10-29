# Independent scientific review: pruning-to-local-control receiver bridge

**Disposition: ACCEPTED, scoped to the recorded ideal circuit-model instances and conditional mathematics below.** Date: 2026-10-29 UTC. This review is separate from all predecessor projection/meta reviews. It is not a hardware, source-acquisition, or online-trajectory certificate.

## Frozen evidence and independent procedure

`results.json` binds the 15 frozen review inputs to their actual SHA-256 hashes and byte counts and records the manifest hash, supplemental projection-arithmetic dependency hash, and six retained-memory bank/record hashes. `review.py` and `review.log` document an independent rational replay. The review did not run the original output-writing test/compilation tails and did not modify frozen inputs. It reused the inspected Gaussian-rational value type and matrix multiplication, and the inspected pruning/Gray-expansion definitions, rather than presenting itself as a wholly separate arithmetic implementation. The checker independently implements local gate action, exact residual accumulation, and integer-square-root upper bounds. The implementation and analytic argument were both reviewed.

Checks passed:

- All 15 manifest hashes and sizes match, including the three governing scope documents.
- Each terminal bank supplies nine exactly positive rational effects summing to identity. All 32 pruning leaves per seed have four surviving effects, positive weights, exact completeness, positive branch probabilities summing to one, and exact effectwise weighted mean equal to the original nine columns. Seeded sample outputs reproduce saved labels/effects.
- The unseen-label rank map is a bijection onto the complement for every proper observed subset of alphabets of size 1 through 10. Its general argument is monotone rank insertion: incrementing past each excluded sorted label yields the selected complement rank, without enumerating the alphabet. Preconditions are distinct valid known labels and a correctly matched compressed effect list.
- Each saved rational phase and SU(2) gate is exactly unitary. For all six full/thin instances, explicit Gray-path controlled gates yield exactly the direct rational two-level circuit. Full-circuit controlled-primitive records agree with their expansion.
- Exact physical effects are reconstructed from the two occupied input columns, paired by ancilla outcome, and their four Frobenius-error upper bounds are recomputed.
- Every saved local single-qubit gate is exactly unitary. Saved gate lists are segmented into their addressed primitive blocks and each exact rational 8-by-8 product is compared against its intended controlled gate. Recomputed residual upper bounds reproduce every saved aggregate and total bound. This validates the finite records even if the floating eigendecomposition, square-root proposal, Euler-angle selection, or QR proposal were imperfect.

## Mathematical checks and assumptions

Fixed positive original columns have positive trace. Therefore a nonzero real dependence has both signs; both endpoint weights are nonnegative and each kills an active effect. The specified coin probability preserves conditional mean weights. Iterated expectation gives effectwise identity. Moving the default aggregate to a uniformly selected unseen label restores its aggregate divided by the number of unseen labels in mean.

For a denominator d, b=(d-1).bit_length(), each uniform b-bit attempt rejects with probability (2^b-d)/2^b < 1/2 (zero for powers of two). With 128 independent attempts, failure is at most 2^-128. A cap fallback still selects a feasible branch. The general unconditional union bound uses **max(0,m-4) + one_default_draw** for m active starting columns, not a realized random number of draws. For these nine-positive-column instances every leaf uses five prunings and one default draw, so the bound is exactly the stated conservative 6*2^-128. A random realized count is not a substitute for this deterministic upper bound on other inputs.

All mathematical mean/coupling claims require fresh fair private bits independent of returned quantum systems and retained source memory conditional on the controller’s past. This is a trusted private-randomness interface in the theorem/circuit model; a secret deterministic seed does not establish it. Python `random.Random` seeds provide reproducible sample paths only; these tests do not certify physical entropy or cryptographic unpredictability. Repeated use must satisfy the corresponding conditional independence requirements.

For Hermitian effect difference H_a, the partial-evaluation map T_H(X)=Tr_flag[(H_a tensor I)X] has diamond norm ||H_a||op: its adjoint Y -> H_a tensor Y has completely bounded operator norm ||H_a||op. Summing over outcome blocks, with label-dependent Pauli conjugations, gives half-diamond <= (1/2) sum_a ||H_a||op <= (1/2) sum_a ||H_a||F. This holds for arbitrary correlated data, retained environment, and reference. The **postmeasurement flag is discarded**; effects alone do not identify its retained postmeasurement state. The **private pruning branch is discarded**; retaining it jointly does not preserve the same instrument. The ordinary correction/output label may be retained.

Gray-path swaps conjugate the terminal adjacent operation onto the desired pair, with explicit orientation and negative controls. A CC-U uses the controlled V, CNOT, controlled V-adjoint, CNOT, controlled V construction, V^2=U; standard controlled-unitary A-X-B-X-C factors apply next. Numerical factor proposals are not acceptance evidence: the rational local products and exact residuals are.

For exact unitary factors, operator norm telescoping bounds product error by the sum of primitive operator residuals, themselves bounded by Frobenius residuals. Moreover half-diamond(Ad_U,Ad_V) <= ||U-V||op. Preparation/postprocessing are contractive. Consequently the local residual sum is added with coefficient one, not two, to the effect-based half-diamond bound. The documented constants are correct.

## Accepted numerical results

| Seed | Thin CNOT | Thin single-qubit | Thin half-diamond bound (approx.) |
|---|---:|---:|---:|
| 7301 | 248 | 646 | 3.9146903536572205e-13 |
| 7302 | 248 | 646 | 4.2760148138054041e-13 |
| 7303 | 248 | 646 | 4.0488847680088931e-13 |

Each thin instance has 15 two-level/phase gates and 31 controlled primitives. The common **4.277e-13** bound is rounded upward. Full-unitary instances have 544 CNOTs and 1,384 single-qubit gates, with independently reproduced bounds 7.6815574524144855e-13, 8.6305600838230428e-13, and 8.5980493697706348e-13. Exact rational totals, not printed decimal approximations, govern.

## Exclusions and conditional physical use

The accepted outputs are finite classical descriptions of three learned pruned POVMs and their exact rational-unitary circuit approximations. No new source calls, hardware runs, exact source physics, full online physical trajectory, beneficial recovery performance, practical advantage, optimal circuit cost, or generic all-input synthesis/runtime theorem is certified. Historical acquisition remains floating-point. Correct implementation additionally requires named accessible flag control, two trusted zero ancillas, and actual composable gate, preparation, readout, storage and selected-Pauli error bounds under the relevant history/memory conditions. Scalar average infidelities are not interchangeable with those bounds. Approximation across online rounds requires its own cumulative analysis. This review does not change the predecessor poor-recovery result.
