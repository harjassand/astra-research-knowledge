# Independent whole review: acquired resolvent action effects and reusable control

**Verdict: PASS within the stated finite, fully observed discounted-MDP observation and task interface.** This is a new source-bound review, not an extension of the earlier contrastive-discovery receipt. I read the complete current mathematical, acquisition, code, execution and comparison bodies, ran all three nonmutating harnesses, and added independent exact checks. No correction to frozen scientific files is required by this review.

The mathematical result earns a small ordinary rational LP from acquired action-effect and objective errors, without assuming an exact predictive quotient, an inverse of `WH`, a contracting reduced iteration, an optimal teacher, or enumeration of all block policies. It does **not** establish economical acquisition, historical novelty, a practical advantage, an implemented polynomial-worst-case LP backend, or physical access to chosen microscopic rows. Actual sampled data in this package still refuses the requested 0.01 regret. Successful huge count arrays are fabricated unit fixtures, not observations.

## 1. Exact source binding

Reviewed directory: `resolvent_control_reuse_20261031`.

Freeze manifest: `REVIEW_FREEZE_MANIFEST_20261031_2229UTC.json`, 4,232 bytes, SHA-256:

`ec2fbfb9fed2f28fc90f45d9abcfda01ea0fd9b71e582389ba4d621cd18e2503`.

All 15 current and two explicitly historical entries matched their manifest byte counts and hashes before and after review. Principal current bindings are:

- `ROBUST_CLOSURE_SUCCESS.md`: `5e24d90019af84770b056fe3c1c9bbebc53ca4f896821c5acff5be7668050593`.
- `PROOF.md`: `bf36ee3aa47c75c93c48bc206cf79ba7a87b2f9a3600234c973fba13c1c67cbd`.
- `control.py`: `d701d787fd2a0ad90c396b9207a49231e6fec8b0bc1848a67f3c5b8d963f3877`.
- `episode_protocol.py`: `5e8979e9c27f8b8d23d09f89e4d8ade583cab6b66a12dedf0e46e062bf1fb33f`.
- `README.md`: `9d80797df65e624e7dfdb743a9ec59ca61c2c9c5369d1b4c95ea1db8c006bdd6`.
- `COSTS_AND_SCOPE.md`: `ffde35e32351472208df5055ddd8bfe57dff25a6d2adb687a4d320fd71523c19`.
- `EXECUTION_SCOPE.md`: `29ba89c592a4735028e34d738657a7008554fe0a217149ae415c0ce46580fe64`.
- `PRIOR_AND_COMPARISON.md`: `2d14149d5b61b79735253925305d92603c83614fbaa10ca84d7925f2b0624e85`.

The manifest also binds all three test sources, saved results and actual compressed microscopic paths. I read the historical alternatives to verify their separation; they are not needed by, and do not override, the primary LP construction. In particular, no topological existence argument is being treated as an efficient nonlinear solver.

Unique reviewer directory: `reviewer_2231/`. No frozen source or saved result was overwritten.

## 2. Actual task and retained interface

The model is a finite stationary stochastic MDP with named microscopic states, a fixed rational discount `0 < gamma < 1`, and finite actions including baseline 0. A call at a chosen state/action returns a fresh next-state label; subsequent baseline calls can start at that observed label. The assumed iid/source/coin protocol is substantive and is not authenticated by a count array or digest.

The starting partition is obtained from explicit native task-feature tuples. It need not predict dynamics. The algorithm may refine it; every later reward is constant on the final acquired blocks. The stronger extension admits separate bounded reward tables for each action. Net rewards/prices must still lie in the declared `[0,1]` scale; arbitrary microscopic or unbounded rewards are not received.

A later task can be selected adaptively after acquisition. For each such task, the theorem is about its fixed discounted reward objective and the resulting stationary block policy, pointwise over starting states, against optimal microscopic/history policies in the fully observed MDP. It is not a guarantee for arbitrary changing rewards inside one execution, a hidden-state sensor, or arbitrary new discounts/actions/partitions.

The retained core contains coefficients, radii and hashes, not the whole state map. Actual deployment separately retains and consults the `n`-label partition map and obtains the current microscopic label. Native feature reading, chosen-row preparation, source calls, map operations, evidence retention and full receiving are not removed by the small downstream LP.

## 3. Geometry and the corrected resolvent identity

Write `a = 1-gamma`, `t = gamma/a`, `H = a (I-gamma A0)^(-1) Z`. Stochasticity makes H row-stochastic. Since Z is an indicator lift of nonempty disjoint blocks, `||Zx||_infinity = ||x||_infinity`. Therefore

`a ||x|| = ||(I-gamma A0) Hx|| <= (1+gamma)||Hx||`.

This proves the lower embedding bound `||Hx|| >= kappa ||x||`, where `kappa = a/(1+gamma)`, without inverting `R = WH`. Unequal blocks cause no change.

For a rowwise randomized block selector pi, use the same convex weights to define the true stochastic A_pi and the acquired Bhat_pi. The full error bound on every action/row implies `||E_pi||_infinity <= eta`, where

`E_pi = (A_pi-A0)H - Z Bhat_pi`.

With `M_pi = I-t Bhat_pi`, the exact identity is

`(I-gamma A_pi)H = a Z M_pi - gamma E_pi`.

The stochastic inverse bound gives `||M_pi x|| >= (kappa-t eta)||x||`. Hence every mixed selector has an inverse with norm at most `1/d`, for `d = kappa-q > 0`, `q = t eta`. This applies to all mixed selectors, not merely deterministic policies or an unknown optimum.

Multiplying the same identity by the true resolvent yields the **minus-sign** formula

`H M_pi^(-1) = a G_pi Z - gamma G_pi E_pi M_pi^(-1)`.

This is the corrected orientation in the frozen source. The reviewer checked it symbolically on 120 nontrivial mixed selectors with three actions, unequal blocks, nonzero closure defect and perturbed acquired coefficients.

## 4. Objective margin, grouped dual and LP root

The analysis law is `mu = (1/r) 1^T W`, uniform over blocks and then uniform within a block; it is not generally uniform over microscopic states. It has full support. Define `h = mu H`.

Because `G_pi >= I` entrywise and `||mu G_pi||_1 = 1/a`, the corrected identity gives

`hhat M_pi^(-1) >= [a/r - (q+delta_h)/d] 1^T`.

The error estimate uses induced infinity norm for the right factors and row L1 norm for the left vector. Thus the computable positive margin `z = a/r-(q+delta_h)/d` is valid for all rowwise mixed selectors. The endpoint estimator constructs hhat as a probability row with entries at least `a/r`; its approximation to the true h is separately paid.

For common block rewards, minimize `hhat w` subject to `w_j >= g_j+t[Bhat_a w]_j`. Feasibility is explicit: `w=1`, since every Bhat_a has zero row sums. The baseline constraints impose `w>=g>=0`. Positive hhat makes objective sublevel sets bounded, so an optimum exists.

For any exact optimal dual, group multipliers as `nu_j = sum_a lambda_ja`. Assign mixed policy weights proportional to these multipliers wherever nu_j is positive, arbitrarily where it is zero. Dual stationarity is `hhat = nu^T M_pi`. The all-selector inverse and objective margin then imply `nu_j >= z > 0` for every j. Complementary slackness supplies an active constraint in every block. Consequently the ordinary LP optimum is precisely the nominal max-affine root, not merely a supersolution.

Differences of maxima are rowwise convex combinations of action-row slopes along the segment between two arguments. The same all-selector bound therefore proves uniqueness and `||w|| <= 1/d`. No assumption that the reduced iteration contracts is needed. The supplied divergent-iteration example remains a genuine warning against that shortcut.

This argument also covers action-dependent bounded rewards: replace g_j by g_a[j] in each constraint. Feasibility `w=1`, nonnegativity from the baseline reward, grouped dual positivity and active-selector norm bounds survive unchanged. The prototype implements this extension directly, rather than pretending a common-reward call already receives it.

## 5. Actual-process regret and all-goal reuse

For a candidate w and nominal policy, the actual Bellman and fixed-policy residuals are bounded by

`a rho + gamma eta ||w||_infinity`.

Both contraction comparisons occur in the original n-state stochastic process. Dividing by a and adding the two comparisons gives pointwise normalized regret

`2 (rho + q ||w||_infinity)`.

For the checked LP root, rho is zero, hence regret is at most `2q/d`. This remains valid for genuinely nonclosed sources on the received error event. The signed matrices Bhat do not need to define a stochastic reduced model. The acquired h-objective margin earns root construction; the posterior residual check itself does not require LP optimality.

The same uniform coefficient event supports arbitrarily many later bounded compatible reward tables and candidates, including data-adaptively chosen ones. No additional statistical goal union is necessary. This is an unconditional high-probability acquisition guarantee under the observation protocol, not a posterior claim that every particular accepted transcript is correct. Numerical execution/checking of each later LP is still charged.

The older bounded robust LP in PROOF sections 4 and 9 is separately coherent: its shift satisfies `c-q M0=q(M0+c)=s`, the shifted exact-class optimum is feasible, and the objective error and block-average residual bounds give the stated fallback estimate. Its exact-class sufficient success statement is not silently promoted to all approximate sources. The current primary acquired-margin theorem supplies that stronger small-error success route.

## 6. Endpoint statistics, truncation and confidence

After one action-a transition, a geometric number T of baseline steps has endpoint block law `A_a H`. Capping T at K couples to the uncapped experiment except on `T>K`, with L1 bias at most `2 gamma^(K+1)`. The actual loop implements `min(T,K)`: it executes no fictitious extra transition at the cap. Expected calls per episode are exactly

`1 + gamma (1-gamma^K)/(1-gamma)`,

and at most `K+1` calls occur. Cap zero is included. Independent exact truncated-kernel calculations checked the displayed bias for eight caps.

For a fixed partition/design and N fresh endpoints per row/action, the subset Hoeffding argument gives the simultaneous row-L1 radius `sqrt(2 L/N)` when `L >= log(2^r n m/delta)`. Complements handle the opposite sign. The integer ceil-log2 bound is conservative, and the dyadic square-root routine rounds outward. Count denominators and the rational truncation tail are explicit.

Subtracting the same empirical baseline row produces effect error at most `2 epsilon`. Averaging and measured within-block defects yield `eta = eta_hat+2 epsilon`; exact closure implies `eta_hat<=4 epsilon`, hence `eta<=6 epsilon`. The estimator

`hhat = a u + gamma u W Phat_0`

is justified by `H = a Z + gamma A0 H`; therefore `delta_h = gamma epsilon`. No independence between Bhat, hhat, the measured defect and the confidence radius is assumed.

The primary sufficient epsilon bound gives `q+delta_h <= kappa a/(4r)`, `d >= kappa/2`, `z >= a/(2r)` and the advertised `2q/d` target. These are sufficient schedules, not necessary sample requirements. Dependence is polynomial in inverse accuracy and inverse discount gap, not merely in the bit length of gamma.

For adaptive refinement, each design and batch size must be fixed before its fresh outcomes, with summable externally budgeted failures. This proof does not supply an optional-stopping confidence sequence. Recorded counts cannot certify that timing or source identity.

## 7. Native-feature refinement and receiving boundary

Exact refinement starts with equality of native feature tuples, recomputes baseline action-effect rows for the current partition, and splits by full effect-row tuples. If a stable target partition refines the native partition, the relation `Z_current=Z_target L` gives `H_current=H_target L` and prevents splitting a target block. Finite strict refinement terminates and yields exact closure. Dense exact inverses in the reference routine are explicitly analysis/fixture operations, not the statistical learner's observation interface.

For noisy proposals, the row-tuple error is at most `2 epsilon`; a same-target pair differs by at most `4 epsilon` and is joined. Separation above `8 epsilon` yields the exact classes. Connected components may otherwise merge through chains, but the posterior defect can then refuse. No good basis, hidden partition, clustering teacher or optimal policy is supplied.

The executed receiver checks the externally supplied native features, source identifier, action/state counts, discount, per-attempt schedules, confidence total and requested tolerance. It receives every supplied count record, computes each next partition, and refuses omitted/replaced intermediate designs and records after a declared successful stop. Its costs include all supplied attempts; it cannot authenticate that the caller disclosed every real-world failed experiment.

The small planner is intentionally a consumer of a **previously received core with an externally retained digest**. A caller manufacturing both a fake core and its digest has not thereby acquired a statistical certificate. This is not an untrusted standalone proof-of-source verifier. Exact fixture cores in tests are plainly labeled analysis data. The source and task hashes are useful receiving bindings, not evidence of physical provenance.

## 8. Code and independent tests

All current scientific code was read in full. The supplied nonmutating replays passed:

- `check_control.run()`: **182 exact checks and 13 refusals**.
- `check_uniform_control.run()`: **208 checks and 5 refusals**.
- `check_episode_protocol.run()`: **4,096 actual software episodes, 38,626 forward calls**, correctly returning UNKNOWN for 0.01 regret.

All saved results reproduced exactly after removing wall-time fields. The actual path archive's canonical digest, per-row/action/episode uniqueness, endpoint counts, path lengths and total call count were independently reconstructed. The replay adds 38,626 executed source calls to the audit bill; it is a same-seed reproduction, not new independent evidence.

Additional reviewer checks:

- **13,163 exact checks and 19 refusals**.
- Twelve rational five-state, three-action models with unequal blocks, actual nonzero closure defects and nonzero acquired coefficient/objective errors.
- 120 mixed-selector inverse, flow-sign and objective-margin checks.
- 48 bounded action-dependent reward tasks, independently evaluated against an exact full-state policy-iteration optimum and actual selected-policy value.
- Degenerate single-state/baseline-only/zero-goal cases, cap-zero and finite-cap laws, fixed-design source/task/confidence substitutions, malformed integer/count/partition inputs, and all 4,096 saved paths.
- These extra algebra tests execute **zero** new source calls.

An important backend diagnostic was retained: in one of the extra full-state comparison LPs, installed SymPy `linprog` returned an infeasible value. The exact Bellman check detected it. I replaced the independent truth comparator by exact policy iteration and retained the failed LP matrices and outputs in the extra-check JSON. This is not a failure of the mathematical theorem or an accepted false policy. It demonstrates why the frozen primary consumer's exact primal feasibility, nonnegative dual, stationarity, objective equality, grouped positivity and zero-residual checks must remain load-bearing. A failed exact check raises an error rather than producing PASS; some backend exceptions instead return UNKNOWN. Neither route earns a policy certificate.

Reviewer files:

- `extra_checks.py`, 7,018 bytes, SHA-256 `5e19691d0dbc01da149c22bf066f1490c28b13d04cd730e33a2a101fa2bffeda`.
- `extra_checks.json`, 3,614 bytes, SHA-256 `4209d7441631597da21c0346a95cb354f4ecce0cfc79658c8da159d5d1955c8f`.
- `author_nonmutating_replay.json`, 11,701 bytes, SHA-256 `5850c06e6cb2c5fada4fdeb50a876d3a871417460cd2189dda3b3f377f3e4fea`.

## 9. Execution and cost qualifications

The single actual batch retained 42,722 microscopic labels, made 38,501 stopping-coin draws, requested 613,934 random bits through 123,398 requests, and examined 96,484 source-sampler CDF entries. The exact rational source is a test fixture; the acquisition function only consumes forward outcomes. Python's seeded PRNG is not ideal-iid or physical-randomness authentication.

The successful synthetic count tests did not execute their implied observations. The first fabricated frontend represents 8 trillion episodes; the two-round refinement fixture represents **8,640,000,000,000,000,000,000,000,000 episodes**. Those numbers are deterministic unit-test metadata, neither an observed success nor a necessary lower bound. The actual modest experiment refuses.

Every acquisition attempt pays all named rows/actions, N endpoint episodes, capped/random stopping, state preparation and labels, count updates, partition refinement and independent receiving. Pairwise refinement can cost `O(m n^2 r)` arithmetic. The retained map and count evidence remain ambient-size objects. Only later small-core planning avoids an n-state scan after that acquisition and receiving.

Ordinary polynomial-bit rational LP theory supplies a mathematical consumer. The prototype uses ordinary SymPy rational simplex; its measured input/output entry lengths are not all internal pivot costs or peak memory, and simplex is not declared polynomial worst case here. Exact checking earns correctness of successful outputs, not an efficient worst-case implementation. Finite execution of a stationary policy additionally pays its J transitions and has normalized tail at most `gamma^J`.

## 10. Strong ordinary comparison and final scope

I freshly opened and read the relevant primary statements in Walter Morris's [generalized P-property paper](https://math.gmu.edu/~wmorris/cubemdpmprev4.pdf), especially Theorem 2(3) and Section 3. The positive common-right-hand-side representative-basis condition matches the abstract LP criterion here after transposition. The present grouped-dual proof makes the match explicit; it is not a new generic solution of P-matrix complementarity. Mixed-selector nonsingularity also places all representative determinants in the same positive orientation by continuity from the baseline.

I also freshly read the [generalized reduced LP primary paper](https://arxiv.org/pdf/1409.3536), whose construction already reduces ALP constraints through positive combinations and analyzes approximation error. With the implicit H basis, exact duplicate-constraint collapse is an ordinary ALP operation. Strong ALP/successor-feature/value-equivalence methods get the same learned certificate, all endpoints and paths, native task labels, failures and retained work. They may use sharper confidence bounds, policy portfolios, on-demand learning or warm starts. No weaker baseline is justified by withholding these ingredients.

The independently checked contribution **to this construction** is the source-derived error and objective margins, the actual forward endpoint/refinement interface, and their complete many-goal LP receiving join. Historical novelty and an economically favorable important workload remain unresolved. Nonpredictive utility is a valid mathematical distinction, not by itself a comparative advantage. Earlier contrastive, tagged/population and history-policy archives are unchanged; none of their statistical events is silently reused here.

**Final acceptance:** the frozen primary proof, finite-observation acquisition/refinement receiver, exact checked small-LP consumers and bounded action-dependent reward extension are sound within the explicit observation, task, cost and confidence scopes above. No frozen correction is requested. No practical, physical, novelty or unexecuted large-acquisition claim is promoted.
