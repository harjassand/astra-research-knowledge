# Independent whole review: direct acquired canonical admission

**Verdict: PASS for corrected v2, with one genuine auxiliary v1 error withdrawn and preserved.** The main feasible-witness theorem, all-goal source-regret bound, acquired objective, noisy-family sufficient schedule and checked consumers are sound within the declared observation/task interface. No acceptance is given to the withdrawn claim that maximizing the Morris gap necessarily minimizes the new value-bound constant.

This is a separate review, not an automatic extension of either earlier resolvent receipt. It includes the complete new proof, implementation, full-trace receiver, tests, actual-data refusal, calculated schedules and the v2 correction. No practical acquisition win, historical novelty, necessary sample bound, or reliable fast simplex implementation is established.

## 1. Binding and review history

Directory: `resolvent_direct_canonical_admission_20261031`.

Original manifest: `REVIEW_FREEZE_MANIFEST_20261031_2256UTC.json`, 2,534 bytes, SHA-256

`63d44ffa744d70683f6ab67b7115e2dabfdae08213f2ee341515fa15fdf5422c`.

Original proof: `fb8537291dfa6016aef01387a659f3e0ad098d48e1cbe52e58c70d95b9a3f689`.

I read and checked this freeze, found the optimization-equivalence defect described below, and sent an exact actual-source counterexample before any acceptance. The author preserved all v1 files and the manifest under `history_v1_2256UTC/`, removed only the false auxiliary claim from the proof, and added an explicit correction and exact executable counterexample.

**Accepted v2 manifest:** `REVIEW_FREEZE_MANIFEST_V2_20261031_2308UTC.json`, 4,097 bytes, SHA-256

`7322c35f33e85d00cd616eed91b1097f56cea7c5da3995b45af3a1f48242d6c6`.

Principal current bindings:

- `PROOF.md`: `c74a86d0de64d29acfc106082497c6ab60dc1a77f43628de22a9b12f1283162a`.
- `direct.py`: `8b57cfec3a16b764fd287c153bdb32272f8998e9ea3b0ebaba62de73067978b9` — unchanged from v1.
- `check_direct.py`: `d806151765be20587db68538b6a0239a696322ec8e4ff95e18bf7c78ad4e04d9` — unchanged.
- `direct_checks.json`: `e0aa4115fa9cab1269eeb94b455a86f010829eb493eaac692fb2288694208299` — unchanged.
- `README.md`: `15c44f8d7ec7d1bba77e524764a64e05d97812ce4d1b829bfda9c78eafb83ea8`.
- `GAP_OBJECTIVE_CORRECTION.md`: `ecca26cb9e114aff15aee83fc4242f0ed4037d3ff5b35764571e7e54be01005f`.
- `check_gap_objective_counterexample.py`: `7010f40cafc5d0c6438ae43fd11ceccb5037748a4006fbaa6ac85f9d22e69d09`.
- `gap_objective_counterexample.json`: `090bb6aed7ae949800e25e472fb48eae7edbde826dec001aacaf8f38a7c0e341`.

The v2 manifest binds fourteen current/history files and eight exact dependencies. All were checked. The prior accepted source receiver, actual saved observations, canonical comparator and their scientific boundaries remain unchanged. Reviewer files are in the unique `reviewer_2305/` directory; no author source was edited by this reviewer.

## 2. What is newly received

The unchanged source interface supplies an already received simultaneous error event

`||(A_a-A0)H-Z Bhat_a||_(infinity -> infinity) <= eta`,

where `H=(1-gamma)(I-gamma A0)^(-1)Z`, the baseline effect is zero, and each Bhat row sums to zero. The true source remains a finite, fully observed stationary discounted MDP with chosen-row forward access and fresh fixed-design endpoint experiments. Native-feature partition discovery/refinement, full data receiving and all failed attempts remain paid.

The direct consumer genuinely does not need source hhat or delta_h accuracy. `effect_coefficients` reads only r, m, gamma, eta and Bhat. The full older endpoint receiver still computes its other fields; this does not mean those fields are assumed or secretly used by the new admission. Independent tests with unusable extra h fields confirmed they are ignored.

The nominal geometry is acquired by an actual ordinary rational LP over the retained coefficients, then checked by exact inequalities. A positive canonical transform is not supplied as an unexamined favorable condition. The implementation may fail or refuse to find a witness; no claim of completeness of the installed simplex backend follows from the mathematical existence of a polynomial-bit LP algorithm.

## 3. Canonical signs imply invertibility and the uniform value bound

Set `t=gamma/(1-gamma)` and put the action/block column `e_j-t Bhat_a[j,:]^T` into A. For a received witness X and delta, every column of Y=XA has nonpositive off-diagonal entries and satisfies

`0 < delta <= column_sum(Y) <= diagonal(Y) <= 1`.

Baseline columns of A are coordinate vectors. Consequently X itself has these signs and strictly positive column sums. Its transpose is a strictly row-diagonally-dominant Z-matrix with positive diagonal. Writing `X^T=D(I-P)` with P nonnegative and row sums below one proves invertibility and a nonnegative inverse by a convergent Neumann series. In particular every diagonal of X is strictly positive and at most one. This argument is independent of a source-derived lower singular bound for H.

The previously reviewed exact augmentation yields a stochastic computational MDP with discount `beta=1-delta` and zero-valued cemetery state. For every later bounded action-reward table, its unnormalized optimal value satisfies `0<=v<=1/delta`. The transformed nominal solution is `w=X^T v_original`.

The key improvement is valid and uses two distinct positivity statements. The original baseline Bellman constraint implies `w_j>=g_0[j]>=0`; this is not inferred merely from X. On the other hand, nonpositive off-diagonal entries of X and nonnegative v imply

`w_j <= X_jj v_j <= X_jj/delta`.

Therefore the explicitly computed `C_X=max_j X_jj/delta` controls the sup norm of the unique nominal root for **every** allowed reward table. It is not an arbitrary operator-norm bound on X, and it does not assume that Bhat defines source block dynamics.

The original-process residual theorem then gives

`regret <= 2 t eta ||w||_infinity <= 2 t eta C_X`.

The canonical witness may depend on all acquired data. No extra statistical union is needed, because the already received event controls every action-effect row uniformly and the witness inequalities are deterministic consequences. This supports adaptively chosen later bounded compatible tasks on the same acquisition event, not posterior certainty for a particular transcript or a new within-execution changing-reward objective.

## 4. Acquired objective and the ordinary small LP

The new objective has the correct orientation:

`h_c=(X^(-1)1)^T = 1^T X^(-T)`.

It is strictly positive, since X has a nonnegative inverse with positive diagonal. For any rowwise randomized selector, put `M_pi=I-t Bhat_pi` and `Y_pi=X M_pi^T`. Convex selection preserves the checked signs and positive column-sum margin. Thus Y_pi is also a strictly column-diagonally-dominant Z-matrix with nonnegative inverse, and

`h_c M_pi^(-1) = 1^T (Y_pi^T)^(-1) > 0`.

This is the required **row** identity; replacing X inverse/transposes in a different order would not be justified. It was checked independently on 56 nonsymmetric mixed selectors.

Minimizing `h_c w` subject to `w_j>=g_a[j]+t[Bhat_a w]_j` is an ordinary r-variable LP. The all-ones vector is feasible by row-zero sums. Baseline constraints impose w nonnegative, and positive h_c gives bounded objective sublevels and attainment. Grouping an optimal nonnegative dual by state gives `h_c=nu^T M_pi`; the identity above forces every grouped weight strictly positive. Complementary slackness then forces an active action in each block and hence the nominal Bellman root. Equivalently the stochastic canonical model supplies the same unique root.

The implementation checks exact primal feasibility, dual signs, stationarity and objective equality, then recomputes the original nominal residual and value bound. The nonnegativity convention in its primal simplex call is valid because the explicit baseline constraints already imply it. The auxiliary source objective h has no role in this argument.

Generic rational LP provides the mathematical polynomial-bit consumer. Neither this particular simplex backend nor the canonical policy-iteration backend is given a universal polynomial-worst-case runtime guarantee. The exact computed objective may have substantial bit length; X inversion and all arithmetic must be paid.

## 5. The real v1 defect and its correction

The original proof asserted that maximizing delta in the canonical LP also minimizes `maxdiag(X)/delta`. This was false. The LP bounds the diagonals of **all** transformed action matrices, not just X. Homogeneous scaling alone does not identify these optimization objectives.

An exact counterexample uses baseline M0=I and

`M1=[[3/4,1/4,0],[-1/2,3/2,0],[0,0,1]]`.

At delta=3/5, both

`X_bad=[[4/5,0,0],[-1/5,3/5,0],[0,0,1]]`

and the same matrix with its last diagonal changed to 4/5 satisfy every canonical inequality. Their constants are respectively **5/3** and **4/3**.

Both witnesses maximize delta. Indeed the baseline second column gives `delta<=X22`; the action's first-column off-diagonal sign gives `X21<=-X22/3`; and its second diagonal bound gives `1>=-X21/2+3X22/2>=(5/3)X22`. Hence delta cannot exceed 3/5.

This is realized by an actual source, not merely an impossible nominal table. With gamma=9/10, singleton blocks and

`A0=[[1/2,1/2,0],[1/4,3/4,0],[0,0,1]]`,

`A1=[[103/144,41/144,0],[49/72,23/72,0],[0,0,1]]`,

the exact baseline H gives `I-t(A1-A0)H=M1`. Taking the valid conservative eta=1/1000 and requested error 27/1000 makes the worse witness refuse (bound 3/100) and the better witness pass (bound 3/125), despite their equal optimal gap. The exact proof and executable checks preserve this distinction.

Corrected v2 explicitly withdraws the optimization claim and states that a feasible witness can be worse than another available witness. The main code and successful scientific certificates never used optimality of C_X, so they remain valid. The original proof and all original freeze bytes are preserved; the defect is not erased or reclassified as merely stylistic.

## 6. Noisy fixed-source family and discount scaling

The source matrices stay fixed at `.9 S+.1 J` and `.9 S+.1 P`; only the task discount gamma varies in `[.9,1)`. The exact formula

`t B1 = p [[1,-1],[-1,1]]`,

`p=gamma/[20(1-(81/100)gamma^2)]`

has `450/3439<=p<5/19`. This is consistent with the earlier gamma=.9 fixture and was checked by exact rational resolvents on the stated grid.

On the endpoint event of total row L1 radius e and exact closure, the estimated block effect differs from the true one by at most 2e, and eta is at most 6e. Thus the two acquired scaled coefficients p1,q differ from p by at most 2te. If `2te<=1/50`, both are in `[0,3/10]`.

The displayed observed-coefficient witness

`X=[[1,-q/(1-q)],[-p1/(1-p1),1]]`

is correctly oriented. Multiplication by the action matrix transpose kills both off-diagonal entries. The resulting diagonals are `1-p1/(1-q)` and `1-q/(1-p1)`, each in `[4/7,1]`; baseline column sums are also at least 4/7. Consequently delta=4/7 and C_X=7/4 are valid. The source error bound becomes `2t(6e)(7/4)=21te`.

For `0<epsilon_req<=21/100`, the choice `e<=epsilon_req/(21t)` also ensures the required coefficient range. This is a genuine stronger **sufficient** family calculation, using an explicit rational witness computable from observed coefficients. The production compiler still uses its ordinary LP and can refuse; the formula is not an unimplemented probability/conditioning oracle, but neither is an automatic fallback implementation silently inferred from its test.

The full endpoint schedule is sufficient: `N>=32 L/e^2` makes the exact square-root term at most e/4, upward dyadic rounding with step at most e/4 makes it at most e/2, and the chosen cap contributes at most another e/2. N, cap and rounding bits must be fixed before the fresh batch. Confidence, all rows/actions and all refinement attempts are still charged.

At fixed requested accuracy, rank and confidence, e is proportional to `1-gamma`, so N is O((1-gamma)^-2) and the expected number of source calls is O((1-gamma)^-3). The older source-margin sufficient schedule used e of order `(1-gamma)^3` and hence an O((1-gamma)^-7) sufficient expected-call bound. The capped new bill adds the stated logarithmic factor. These comparisons are of sufficient proofs, not lower bounds, not total bit-operation bounds, and not an exclusive improvement unavailable to ordinary methods receiving the same moments.

## 7. Receiving and execution scopes

`compile_model` can produce a valid nominal canonical model while its uniform source-regret admission is UNKNOWN. These are intentionally different statuses. `verify_uniform` independently checks caller-bound core/model/tolerance, dimensions, all signs and sums, stochastic kernels, transformation identities and the recomputed actual uniform bound. The scalar `direct_admission` helper is not a standalone witness verifier.

Per-goal planners recompute actual w and the posterior source error. A particular goal can pass even if a stronger uniform-all-goal request is unavailable. The full-trace receiver uses the unchanged fresh-endpoint count receiver for every supplied attempt, proposes the same native-feature refinement only after failure, and rejects supplied later records after a declared successful stopping point. It pays all supplied batches and compile attempts, but cannot authenticate omitted real experiments, iidness, nonanticipation, physical source identity or a caller-invented trusted core.

All claims use the declared finite fully observed MDP, fixed discount/actions and bounded rewards constant on the final partition. Deployment still needs the microscopic label and retained n-state map. No new reward language, hidden-state sensor or physical preparation capability is earned.

Normal assertions-enabled execution is part of the research prototype scope. Invalid checks may raise errors or return UNKNOWN; neither is a successful certificate. Exact feasibility and residual checks remain necessary in light of the already preserved SymPy backend defects.

## 8. Executed checks and a retained backend limitation

The unchanged main author harness was rerun nonmutating: **557 exact checks and 8 refusals**, zero source calls. Its saved results reproduced apart from timing. The new correction harness independently reproduced **33 exact checks** and its saved counterexample JSON exactly.

The requested algebra comparison is correct: at gamma=.9 and valid eta=.001, the older acquired source-objective margin refuses .05 regret, while the direct witness gives **26901/1269500**, approximately .02119. This is a comparison of valid bounds, not a new empirical acquisition success.

The actual saved 4,096-episode batch remains **UNKNOWN at .01**. Its displayed direct bound is larger than one and not useful. The tolerance-20 success is explicitly vacuous and only exercises stopping/receiving. No sampled data were regenerated or retrospectively promoted.

Independent extra checks completed **310 exact checks and 10 refusals**, zero source calls. They include:

- The actual-source optimization counterexample, including different PASS/UNKNOWN outcomes at the same optimal delta.
- Eight randomized three-action/unequal-block test models attempted; seven compiled successfully.
- 56 mixed-selector h_c identities and positivity checks.
- 35 bounded action-reward tasks comparing the canonical and small-LP consumers and checking their values against C_X.
- Omitted or unusable source-objective fields, malformed core/model entries, false claimed bounds and external tolerance substitution.

One randomized compile did not finish promptly under the installed simplex implementation. The initial unrestricted reviewer run was interrupted; its test source is preserved. A separate replay imposed a five-second **per-LP test budget** by raising TimeoutError around the backend call. That compile then returned `UNKNOWN_CANONICAL_BACKEND`, as the production exception handling specifies. It was not counted as a successful model or its five tasks as completed. The other seven models and 35 tasks passed. This is an actual backend/resource limitation, not a counterexample to the mathematical LP theorem, and not a guarantee that the production interface already has a built-in timeout.

Reviewer artifacts in `reviewer_2305/`:

- `extra_checks.py`: `b7c3e1179e0e589c0437d7511d73f411b9a9ee58b8c12d0f804948b6566546ed`.
- `extra_checks.json`: `44cae18f62c62af325e3bb2560a0fa6c3c0ece96a7b24156da099d3d7598f57a`.
- `extra_checks_unbounded_first_attempt.py`: `af3d145321365967f54ab34113968f8b322596423f14e5beebe9b313acda813b`.
- `author_replay_original.json`: `e69996bc5bb866ceb56d527d4fa05fb4ee56149e71c12de38d605630d3ea4767`.
- `correction_replay.json`: `090bb6aed7ae949800e25e472fb48eae7edbde826dec001aacaf8f38a7c0e341`.
- `PROOF_original_fb853729.md`: exact original proof bytes, independently preserved.

## 9. Cost and comparison conclusion

The calculated .1-regret family schedules start at **10,973,491,200 episodes** for gamma=.9 and reach **13,544,810,631,475,200 episodes** at gamma=.9999. Their capped source-call bills are respectively 932,746,752,000 and 2,159,435,614,165,459,660,800. All are unexecuted sufficient schedules, not necessary acquisition prices or measured results. Exact powers, integer/rational work, endpoint labels, random coins, receiving, failed batches, partition maps and execution costs are additional real obligations.

The new bound can be substantially better than the earlier conservative admission, but it remains ordinary hidden-K geometry coupled to the accepted source-residual transport. [Morris's canonical-form/hidden-K primary construction](https://math.gmu.edu/~wmorris/cubemdpmprev4.pdf), already directly read in the preceding reviews, supplies the established algebraic planner. Strong ALP, successor-feature and other ordinary methods may use the same acquired witness and receive the same improvement. This review does not establish historical novelty of the precise join or an economical important workload.

**Final acceptance:** corrected v2's direct feasible-witness admission, uniform C_X bound, acquired h_c small-LP consumer, all-goal/source-error receiving and noisy-family sufficient discount scaling are sound within the scopes above. The v1 optimizer claim is rejected and visibly withdrawn. The finite backend timeout and huge unexecuted schedules remain limitations rather than being hidden by a mathematical PASS.
