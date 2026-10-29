# Scoped review: controller complexity and real experiments

Date: 2026-10-29. Reviewer: existing Astra P1 / record_geometry role. Internal mathematical review, not external peer review.

## Actual input and outcome

Reviewed actual file: `new_science/continuation6_20261029/CONTROLLER_COMPLEXITY_AND_REAL_EXPERIMENTS.md`.

SHA256: `b349238435d68e9e7731bb9f21753dad1010cb56330abf6203c08f61bcca6efd`.

Unchanged snapshot: `CONTROLLER_COMPLEXITY_REVIEWED_b349238435d6.md` in this directory.

Scope: Sections 3–7, especially the adaptive learning lower bound, KL direction, counts packing, selection, and conditional-record interface. I did not edit the root proof and did not duplicate its construction in a new fixture.

**Outcome:** the intended minimax episode-complexity theorem is mathematically sound. The lower bound is a learning lower bound for arbitrary adaptive calibration within the stated interface, not merely a path-domination or importance-sampling lower bound. I found no error in its packing, probability thresholds, KL direction, or constants. Two theorem-wording qualifications should be made explicit: the accuracy-dependent hard family and the meaning of the episode budget. These do not require changing the construction.

## 1. Required precision of the theorem's quantifiers

The lower proof chooses the terminal reward gap as `Delta = 8 epsilon`. Therefore the clean statement is: for every sufficiently large `n`, every `0 < epsilon <= 1/32`, and every allowed `beta`, there exists the stated hard family, and every uniformly successful procedure with a fixed or hard episode budget `N` obeys (8). Equivalently, fix one class containing all devices indexed by `(b, Delta)` with `0 < Delta <= 1/4`, and take its minimax complexity at accuracy `epsilon`.

The present opening can be read as one finite fixed-gap family working for all arbitrarily small accuracies. That stronger reading is not supplied by the proof. For a known finite family with fixed positive gap, identifying the device and then computing its optimal policy need not cost `epsilon^(-2)` as `epsilon` tends to zero. Moving the accuracy quantifier before the hard-family choice, or explicitly including the gap parameter in the family, resolves this.

Likewise, the displayed sum `sum_b N_b <= N` is pathwise for a fixed or hard episode budget. If a procedure stops after a random number `tau`, the same proof, when the stopped KL chain rule is justified, lower-bounds `E_0 tau` under the null law. It does not by itself lower-bound the expectation under every alternative. Please name the fixed/hard-budget interpretation in the theorem; no optional-stopping extension is needed.

## 2. Upper route, Section 3

The selector is causal at the supplied-context interface. Its gamma product is exactly the product of the chronological selector probabilities. The environment factor cancels even with latent path memory because all controllers use the same initial law and conditional physical kernels. The private-key exclusion is necessary and correctly retained.

The contextual KT ceiling and AM–GM step are correct. The second-moment estimate uses `W_pi^2 R^2 <= C_T W_pi R^2`; hence the variance supplier is linear in `C_T`. This is the appropriate quantity for the subsequent Bernstein statement.

The exact rational selector has the stated implementation limitation: rejection sampling provides an exact distribution with variable bit use/latency. The common physical timing premise prevents this from being silently ignored.

## 3. Finite-bank selection, Section 4

The fixed grid has the claimed cardinality. Rounding the first `A-1` row coordinates down changes the last coordinate by the total deficit, giving row TV at most `(A-1)/L`. Coupling until the first different action proves (5) for an arbitrary common causal plant.

Only a finite-grid uniform concentration event is needed: the selected policy lies on that grid, and the best continuous policy is approximated by one grid point. Equation (6) correctly adds one approximation term, two estimation terms, and the optimization error. It does not assert uniform confidence for all arbitrary continuous policies selected by an unrelated optimizer.

The stated sufficient constants work. If `N >= 32 C_T x/epsilon^2`, then `r_N <= epsilon/4 + epsilon^2/48`; with rounding error at most `epsilon/4`, the total in (6) is at most `3 epsilon/4 + epsilon^2/24 < epsilon` for `epsilon <= 1` and zero optimization error.

The deterministic-policy mixture comparator is valid. It supplies domination `A^S` before the additional half-mixture factor and is independent of horizon on that subclass. Using the marginal mixture law, rather than identifying the private branch key across target and behavior, is consistent with the declared record.

## 4. Packing and useful-policy identification, Section 5

Each tracked mean lies between approximately `n/(4A)` and `n/(2A)`, and the sum of the tracked means in any row is below `n/2`. Thus all designated policies are valid with a positive remaining coordinate. A spacing of `2r+1` makes the integer coordinate boxes disjoint. For fixed `A,S`, interval width is linear in `n`, while `r = ceil(sqrt(d n))`; the number of available centers per coordinate is at least a positive dimension-dependent multiple of `sqrt(n)` for sufficiently large `n`. The number of boxes therefore has the required `n^(d/2)` order.

Under the center policy, each tracked count is a binomial marginal with variance at most `n/4`. Coordinate dependence does not affect the union bound. The radius choice proves box probability at least `3/4` exactly as in (9).

An `epsilon`-optimal returned target policy on device `b` must have box probability at least `3/4 - epsilon/Delta = 5/8`. These identification events are disjoint because the boxes are disjoint and the returned policy defines one probability law. The argument also covers the declared episode-level mixtures of target policies. It would not automatically cover a more powerful deployment controller outside the stated target class, which is appropriately not promised.

## 5. Adaptive KL and its direction

For each fixed candidate `b`, compare the complete algorithm transcript under the null device and under device `b`, including any common-law algorithm randomization. Conditional on the previous transcript, the learner's next decisions have identical kernels under both laws. Intermediate counts and observations are deterministic or have common laws. The only changed kernel is the final Bernoulli readout of an episode whose realized count vector belongs to box `b`.

Consequently, for a fixed/hard budget,

`KL(P_0 || P_b) = E_0[N_b] kl(1/2 || 1/2 + Delta)`

is correct. Within-episode and across-episode adaptivity do not create another information source. Allowing the learner to force count vectors only strengthens the learner and remains covered by this identity.

For `Delta <= 1/4`, the Bernoulli divergence is `-(1/2) log(1-4 Delta^2) <= (8/3) Delta^2`. For at least half the indices, `P_0(E_b) <= 1/2`, while `P_b(E_b) >= 1-beta`. Binary KL is decreasing in its first argument when that argument lies below the second, and increasing in the second argument in this range. Hence data processing gives

`KL(P_0 || P_b) >= kl(1/2 || 1-beta) = (1/2) log(1/[4 beta(1-beta)])`.

This is the correct KL direction for the null-expectation counting argument. Summing the information requirements over the selected indices gives the stated `3K/(32 Delta^2)` constant and therefore `3K/(2048 epsilon^2)` after substitution. The final policy/output rule is part of the algorithm transcript, so post-data selection is already covered by data processing.

## 6. Records, starts and interpretation, Sections 6–7

Conditional confidence is correctly distinguished from posterior confidence at every realized bank. A fixed unknown device parameter is compatible with the proof: the law and independence premises must hold pointwise at that parameter. The hard family has the same initially available information across its alternatives. The lower bound would not apply if an extra old record revealed the hidden device index; no such side channel is supplied by its interface.

Fresh deployment from the warranted conditional initial law is essential. Reusing the last hidden physical state is not licensed by the policy-evaluation theorem. The root text says this explicitly. Similarly, the per-call execution-TV accumulation and the possible `C_T` amplification of a behavior-law TV error are valid for the declared bounded score.

The exponent describes worst-case episode complexity under the supplied start contract. Hidden mixing and state dimension can still govern the *cost of supplying that contract*. The manuscript already charges preparation and waiting; replacing any informal phrase such as total experimental burden by episode count would make this distinction immediate.

## 7. Predecessor status

The upper route is correctly credited to Cover–Ordentlich and Peshkin–Mukherjee. I independently read the Peshkin dissertation qualification: §6.5, printed p. 105, leaves the constructive optimal sampler and explicit class constant open there. This does not turn contextual KT into a new mechanism because the inspected Cover–Ordentlich theorem provides it.

The classical Shtarkov/Ordentlich–Cover optimum concerns domination, so it does not subsume the new proof *as a logical statement* about adaptive noisy-task learning. Its geometric exponent and the standard finite-armed KL technique are prior. I have not established historical priority for their combination in this exact controller class and operating interface.

No new tests were needed to resolve the scoped algebraic and quantifier questions. The acceptance here concerns the intended minimax statement with the two qualifications in §1 made explicit.
