# Independent whole review: factorized many-mode telegraph compiler
31 October 2026. Mathematical-existence review, not an implementation or novelty certificate.

## 1. Verdict and exact source binding
PASS at the stated constructive mathematical-existence scope, with the resource and process conventions below. This is a separate review of the variable-number-of-modes extension; it is not an automatic promotion of the earlier fixed-two-mode receipt.

The following workspace sources were read in the review:
- FACTORIZED_MANY_MODE_EXTENSION_CANDIDATE.md, 6,912 bytes, SHA-256 1028d4495ebf641b01904fe5543271f47bfa78babf19e6a409b67b081f4d7535.
- FINITE_BIT_MANY_MODE_COMPLETION.md, final 21,468 bytes, SHA-256 9fc4e346cb798677e138a61f6dc17ad1f91a6d0c51c7a98043cf15f4e95a401f.

Both are in producer-workspace/. The original 20,556-byte completion was read in full. The subsequently added binary controlled-H0-duration paragraph and final consumer-resource paragraph were separately read; the final hash above was checked against the actual file. The final consumer convention correctly distinguishes simulator overhead from the implementation complexity of arbitrary external instruments. Earlier candidate hashes are superseded for this receipt, not silently relabeled.

Inherited, separately read and reviewed foundations are:
- EXACT_DAMPED_ANCILLA_AND_COUNT_BOUND.md, SHA-256 95217edc38bebdcd9e4d43d12b23b3fcbdfaaa99da6962d73793f37da22fd293.
- METZLER_BRIDGE_FIRST_EVENT_COMPILER_CANDIDATE.md, SHA-256 bdcbc4fecac480e5b4ef56a8d927d1f1ad6d07d1403c463c075ce245c37e4b68.
- FINITE_BIT_FIRST_EVENT_COMPLETION.md, SHA-256 794534e9852ac931dfbbe0b2c19a75159e50f80eaf53f472b5cb2850993294b0.

The earlier fixed-two-mode whole receipt is TWO_MODE_WHOLE_REVIEW.md, SHA-256 693ba0ac8c969770224c57c8655331d13eb492d4e273b314f1a71b115532a917. Candidate headers remain unchanged; this review is a separate document.

## 2. Accepted theorem domain
The number r of independent stationary symmetric telegraph modes is a finite input parameter. The Hamiltonian is H0 plus the sum of sqrt(gamma_i lambda_i) xi_i(t) A_i, with bounded Hermitian, possibly noncommuting A_i. Precision-capable controlled operator encodings, their norm bounds, and finite parameter descriptions are supplied and paid for. Zero couplings and zero rates receive their explicit branches.

The process guarantee concerns arbitrary system instruments at p prescribed times, including adaptive instrument choices, retained ancillas, outcomes, and reference systems. The private damping ancillas, path seeds, jump records, and timestamps remain inaccessible and are retained rather than reset. The guarantee is uniform unconditional output trace-norm accuracy. Arbitrary adaptive intervention times and normalized rare postselection are not included.

The resource bound is polynomial simulator overhead in r, 1 + alpha_H0 T + Gamma T + p, encoded input and register lengths, log(2 + sum_i lambda_i T), and log(1/epsilon), together with the supplied operator-encoding costs. Gamma = sum_i gamma_i a_i^2. The implementation costs of consumer instruments are external or must be added explicitly. Merely counting p slots does not bound an arbitrary instrument's circuit complexity.

## 3. Exact positive representation and actual jump cap
The ground-state damped-qubit dilation remains exact for arbitrary r and noncommuting A_i. For x_S = Tr_E(X_S rho), partial-trace cyclicity gives the closed hierarchy
x_S' = L0 x_S - 2 sum_{i in S} lambda_i x_S + sum_i sqrt(gamma_i lambda_i) L_i x_{S symmetric-difference {i}}.
This matches the classical telegraph moment hierarchy with the same initial data. A system instrument acts on every component by the same CP map, so equality persists through the prescribed interventions. No Gaussian correlation replacement or Born approximation is used.

For the actual Lindblad jump count, the tensor test V = product_i(I + 2(e^theta-1) P_i) and the completed-square tilted-adjoint inequality give
E exp(theta N_T) <= exp(Gamma T (e^theta-1)).
The initial ground ancillas make the prefactor one. System controls preserve V. This is an MGF/Chernoff statement, not an assertion of a pathwise Poisson thinning or pointwise bounded actual intensity. It justifies the global actual-event cap even when a retained ancilla is excited.

## 4. Factorized operator-valued block encoding
The extension avoids enumerating 4^r endpoint pairs. The positive Metzler majorant is E(t) = tensor_i exp(M_i t). Each factor has a bounded row sum
c_i <= exp(Gamma_i t/2) (1 + sqrt(Gamma_i t/2)).
On windows t <= 1/(4 r Gamma), their product is below two. The resulting number of windows is polynomial in r Gamma T and p.

Right column and left row preparations use amplitudes sqrt(E_ji/R), with R = 2, and disjoint padding-failure sectors. They copy only computational-basis endpoint labels. Both sides attach exactly the same conditional bridge seed and transcript for each endpoint pair. SELECT preserves endpoint, seed, and failure labels while applying the chronological operator word. Hence the good overlap is E_ji/R times the conditional bridge mean, exactly the intended K(t)/R block. The padding flags are load-bearing: unrelated failure amplitudes must not overlap.

For a jump in mode k, the local positive factor is
2 sqrt(lambda_k) |0><1| exp(M_k t).
Its output bit is zero, while the bridge's pre-jump endpoint is one. The completion uses this distinction on both preparation sides. Row and column sums are separately bounded by the stated envelope; symmetry is not assumed for this rank-one factor. Tensor-factor preparation and color selection use polynomially many local operations, not an implicit exponential endpoint table.

## 5. Error control without exponential endpoint enumeration
Two different error estimates are correctly separated. Absolute local preparation errors telescope through the r factor preparations. Small branch probabilities can be dropped at an absolute mass budget; otherwise divisions occur only above an explicitly retained threshold. Square-root amplitudes are controlled by their Hölder bound, not an unjustified Lipschitz bound at zero.

Conditional bridge errors are relative to their positive matrix coefficient. If each block error is bounded by eta E_ji/R, applying the nonnegative matrix to the vector of input-block norms gives a full operator-norm bound at most eta ||E/R||_2 <= eta. The analogous row/column sum bound applies to jump majorants. This weighted Schur argument prevents an exponential accumulation over endpoint strings. It is not incorrectly applied to arbitrary absolute preparation errors.

## 6. Conditional bridge acquisition and finite precision
The Doob chain has upward rate s_i = g_i^2/(sqrt(lambda_i^2+g_i^2)+lambda_i) and downward rate sqrt(lambda_i^2+g_i^2)+lambda_i. The rationalized formula avoids subtractive cancellation. Explicit two-state transition probabilities and first-event survival give the bridge law.

The sampler uses one raw uniform for the full event CDF, with the no-event atom treated separately. It does not divide by a possibly tiny conditional event probability. Exact zero coupling is a deterministic branch; impossible endpoints have zero amplitude and do not invoke an invalid conditioner.

The total virtual count cap includes r possible initial downward events. Endpoint conditioning costs the logarithm of the product of endpoint probabilities, a sum of logarithms, rather than rejection with inverse-probability expected cost. Global near-endpoint and near-coincidence exclusions are priced before recursive conditioning. On the retained geometry, remaining durations and transition denominators have fixed lower bounds. This closes the ordering seam for noncommuting operator words.

Recursive remaining-duration perturbations are controlled by the explicit kernel total-variation estimate with the no-event flag separated from its numeric timestamp. Uniform quantization and certified CDF bisection use probability budgets; no inverse-CDF Lipschitz assumption is needed. Potential midpoint comparisons can be union-bounded at a precision cost logarithmic in their number without enumerating the whole bisection tree. Sorting, coherent samplers, and padded event slots are polynomially charged. Numerically tiny lower bounds enter bit precision, not rate-sized loops.

## 7. Complete first-event isometry and outer timestamp quadrature
The actual Kraus family is K(tau) together with J_i K(t) sqrt(dt), and completeness holds for every input on the retained system and damping ancillas. Amplification is applied to this complete instrument, not to the no-jump contraction alone.

The time-envelope construction gives a common-uniform representation. In du coordinates, the amplified event amplitude is J_i K(t(u))/sqrt(q_i(t(u))); there is no additional sqrt(I_i) factor. The outer time/color record is retained, whereas inner bridge seeds are uncomputed to form the conditional operator mean.

When Gamma_i = 0, the exponential damping factor is canceled analytically in the normalized jump amplitude before numerical evaluation. Otherwise the positive envelope floor is controlled by the encoded input scale. This prevents a spurious exponentially small denominator from forcing rate-sized precision.

The finite grid and continuous timestamp laws are not compared in total variation. The proof uses a common-uniform L2 isometry comparison, then a separate bound for the effect of changing the private remaining duration. Uniform tails and short windows are charged explicitly. This is sufficient because the consumer does not observe the private timestamp.

## 8. Polynomial robust amplification
The normalizer is a power of two A of order sqrt(r+1), not a hidden r-independent constant. Attenuating by c = A sin(pi/(4A+2)) and taking m = A ordinary oblivious Grover steps exactly amplifies the ideal isometry amplitude.

The perturbation proof uses the actual block polynomial. For self-adjoint contractions X,Y, the Chebyshev recurrence yields
||T_d(X)-T_d(Y)|| <= d^2 ||X-Y||, d = 2A+1.
This controls singular vectors as well as singular values. Consequently the good-block error is O(d^2 beta) and leakage is O(d sqrt(beta)), with O(A) base calls. The explicit per-call precision budget is more than sufficient and polynomial in log(1/epsilon), log r, and the other encoded parameters. A scalar singular-value derivative alone would not have established this conclusion; the supplied noncommutative polynomial telescoping does.

## 9. Global clock, controls, and circuit costs
The count-augmented exact process, frozen at the actual jump cap, has a generator-norm bound independent of the number of count states. This supplies the private remaining-window Lipschitz comparison. Prescribed later controls are contractive. The backward hybrid therefore prices local isometry error, timestamp displacement, short-window omission, and actual count-tail failure without assuming that the approximate process has the same jump-count law.

Physical damping ancillas survive between calls. The proof never restarts them in their ground state. Window and count caps, sorting, color selection, encoding calls, and arithmetic registers are included. A color-selected operator is not a free oracle when only individual encodings are supplied.

The final binary controlled-H0-duration paragraph is valid: binary fractional duration bits control fixed-time evolutions, with per-piece synthesis errors allocated across the bits. This avoids a table with 2^B durations. The conservative cost charges every virtual slot at an enclosing duration bound; the pathwise sum of durations is not used to claim an unproved optimized coherent H0 cost. The resulting overhead is still polynomial.

The final resource paragraph is binding: arbitrary consumer operations at the p control slots are external, or their real implementation costs are added. Uniformity of the process-error guarantee does not grant free implementation of those operations.

## 10. Boundaries of the acceptance
This is a constructive theoretical existence result, not an executed compiler, tested numerical package, practical-speed claim, optimal-complexity result, or novelty finding. It does not acquire the supplied operator encodings. It does not permit access to private noise/ancilla/timestamp registers, unlimited reuse of a bounded-query source, normalized rare postselection, arbitrary adaptive control times, or general colored/nontelegraph noise.

No numerical test is used as a substitute for the operator, sampler, or error proofs. Existing restricted-access source boundaries remain in force. Comparator work is separate from mathematical validity. Within the stated assumptions, I found no remaining load-bearing gap in the factorized many-mode construction and its final finite-bit completion.
