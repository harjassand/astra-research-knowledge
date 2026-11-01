# Independent whole review: ordinary canonical-MDP comparator

**Verdict: PASS within the frozen scope. No correction to the frozen sources is required.** This is a separate review of the ordinary comparator/addendum. It neither silently extends the preceding resolvent-control receipt nor accepts the later direct-canonical-stability or discount-scaling construction.

The useful result is that an established hidden-K transformation consumes exactly the same acquired signed coefficients and yields a small ordinary stochastic **computational decision model**. It returns the same nominal policy/value coordinates and the same actual-source regret certificate. This strengthens the ordinary baseline; it is not a predictive quotient of the observed process, a new observation method, or a practical/novelty claim.

## 1. Source binding and complete read

Directory: `resolvent_canonical_comparator_20261031`.

Freeze manifest: `REVIEW_FREEZE_MANIFEST_20261031_2244UTC.json`, 2,165 bytes, SHA-256

`e0147ff0cc6aa2e3ac6600c579dd027f147fcf29f0fd4be06750f57548db1476`.

I read the complete proof/prior, README, current compiler and test source, saved results, and the historical code/diagnostic. The seven manifest files and four pinned dependencies were hash-checked before and after review. Principal bindings:

- `PROOF_AND_PRIOR.md`: `136b9d8161c2cfbfa1e02c3878779f77ab86ce58d5aef7376053af82bcad5df2`.
- `canonical.py`: `d9790facc7aef712b9dab01b42a268f0f48fe85a540a70f0bb5c9286f6a941f7`.
- `check_canonical.py`: `265fab5adfc8ff05745ebc86e165c50a701f8de2f3f6ac10fc381d0b98493660`.
- `canonical_checks.json`: `457e881156113350a6f794c89f66a05b61002f95527eb4dd28c5c8956f9a9da4`.
- `README.md`: `fbc5c67e85c31232b84141fb2de3247888fe468e7e86af6bb103d9be1de80e60`.
- Historical first formulation: `f4a6877b00a95307b99034c372ace44fafb64d6c5b5f2789383e3f266de718c8`.
- Historical backend diagnostic: `1eceb7d106a493ccf3419300a5347c3faa9ac47d08af3c2e56e2d629d8088b35`.

Pinned accepted dependencies are the preceding `control.py` d701d787…, `check_control.py` b9cf83f1…, acquired-margin proof 5e24d900…, and whole receipt 84c5e8be…. Their exact full hashes and byte counts are in this manifest. No source or saved result was edited. Reviewer artifacts are confined to the unique `reviewer_2251/` directory.

## 2. Exact raw common-reset alternative

Under the additional **known-matrix** identity `A_a-A0 = Z D_a W`, with uniform averaging W and D0 zero, define the entrywise minimum Dmin, common background `K=A0+Z Dmin W`, and `R_a=D_a-Dmin`.

For microscopic source row i in block j and destination l in block k, the action-dependent offset is `D_a[j,k]/|block k|`. Therefore minimization over actions commutes with this positive scale and gives exactly `K[i,l]=min_a A_a[i,l]`. This proves K nonnegative and substochastic, R_a nonnegative, `A_a=K+Z R_a W`, and common reset masses `s=-Dmin 1`, `R_a 1=s`, `K1=1-Zs`, with `0<=s<=1`.

For common normalized state rewards `f=(1-gamma)Zg`, it is important to retain the reward earned on **both** reset and nonreset branches. Let `D=diag(1-Zs)` and, first, assume every s_j is positive. With `G_K=(I-gamma K)^(-1)` and `S=diag(s)`, the equations

`v=G_K[ZS u+D f]`,

`u_j=max_a { (1-gamma)g_j + gamma [S^(-1) R_a W v]_j }`

give exactly the original Bellman equation after substitution. The resulting T_a and b_a in the source are consequently correct. In particular,

`Zs <= (I-gamma K)1`

because the difference is `(1-gamma)(1-Zs)>=0`. The positive resolvent implies `G_K Zs<=1`, and hence `T_a1<=gamma 1`. The embedded decision operator is an ordinary discounted nonnegative operator, optionally completed by a cemetery state.

For zero-reset rows, R_a has a zero row for every action, so there is no control effect there. Restrict decision coordinates and S to the positive-reset indices, but keep those zero-reset microscopic states inside G_K and the nonreset reward term. This avoids division by zero and still accounts for their rewards and common continuation. I checked this explicit restriction on an additional exact three-state case. The source's zero-reset qualification is sound; it must not be read as permission to silently delete such rewards.

This route is for common state rewards and exact known raw factorization. The source does **not** claim that arbitrary action-dependent rewards can be deferred until reset epochs, or that D_a can be reconstructed by inverting a possibly singular WH. The already checked weak-closure example genuinely lies outside raw factorization. The conventional known-model reset route nevertheless remains an important equally informed comparator on its actual class.

## 3. Restricted Bernoulli-factory obstruction

For two Bernoulli rows, the exact entrywise-minimum common mass is `1-|p-q|`. An exact reset/noncommon flag would therefore simulate Bernoulli `|p-q|` from independent unknown p- and q-coin samples.

The finite-transcript proof is valid, including adaptive choices of which input coin to query and independent internal randomness. If an output-1 event has positive probability at an interior pair with p different from q, some bounded finite stopping-time portion of that event has positive probability. On this bounded portion, likelihood ratios between that pair and any fixed interior diagonal pair are bounded below by a strictly positive constant, uniformly over the finitely many coin outcomes and choices. The same internal-randomness event then has positive probability on the diagonal, contradicting the required zero output probability there.

This is only an impossibility of an exact unknown maximal-common-part flag on the entire interior parameter domain with almost-surely finite sampling. It does not prohibit approximate common parts, confidence-qualified conservative decompositions, additional known probabilities/couplings, restricted parameter promises, or ordinary approximate reset learners. It is not a new general computation/sample lower bound and does not show that the acquired resolvent route is cheaper.

I freshly read the ordinary sampling formulation in Section 2.2 of [Dughmi et al., Bernoulli Factories and Black-Box Reductions](https://www.cs.cornell.edu/~rdk/papers/stoc17-rad.pdf). That source supplies primary context and attribution to earlier Bernoulli-factory work; the specific two-coin interior-zero argument above is directly verified rather than inferred from a broader theorem not read here.

## 4. Hidden-K premise and the transformation LP

Let `t=gamma/(1-gamma)`, and arrange columns of A by action and block, with column `e_j-t Bhat_a[j,:]^T`. Representative matrices are `M_pi^T`. The previously reviewed acquired margin gives nonsingularity for **every randomized block selector** and a positive solution `(hhat M_pi^(-1))^T` for the same right-hand side. Continuity from the baseline selector keeps representative determinants positive. This is precisely the established hidden-K/positive-basis setting, not an arbitrary generalized P-matrix problem.

The ordinary canonical-form LP seeks X and delta with diagonal entries of each transformed column at most 1, off-diagonal entries nonpositive, and every transformed column sum at least delta in `[0,1]`. The cited hidden-K theorem provides a positive feasible solution after scaling. Its role is existence of an ordinary LP witness, not a supplied spectral/transform oracle.

The bounds used by the implemented translation are earned. Baseline columns of A are the coordinate vectors, so they impose those same conditions on X itself. Each diagonal lies in `[0,1]`; each off-diagonal lies in `[-1,0]`, since its magnitude cannot exceed the diagonal when the column sum is nonnegative. Thus all feasible X entries lie in `[-1,1]`. Replacing X by `U-1` with U nonnegative excludes no feasible witness. The original inequalities still impose the necessary upper bounds; no new guessed bound is being used.

There are `r^2+1` variables and `mr(r+1)+2` displayed inequalities. A **positive feasible** rational candidate is sufficient; maximizing delta may improve the computational discount but optimality is not a correctness premise. The implementation checks every original inequality, positive delta, and nonsingularity. It does not accept a backend's optimization status as evidence.

## 5. One-extra-state stochastic model and exact value correspondence

Put Y=XA. For column (j,a), its sum s satisfies `0<delta<=s<=Y_j<=1`, and off-diagonal entries are nonpositive. Append the cemetery row `delta-s` and the dummy column `delta e_dummy` to form Q. Then all Q columns sum to delta, have nonpositive off-diagonal entries, and have diagonal at most 1.

For `beta=1-delta>0`, `(e_j-Q_column)/beta` is a stochastic probability column. Transposing gives the row convention used by the code. The dummy state is absorbing, with zero reward. If beta is zero, these sign and sum conditions force Q to be the identity: immediate reward maximization is the correct branch. The stored P=I in that branch is harmless because its multiplier is zero.

Give the canonical model the action-dependent table g and zero dummy reward. Its ordinary **unnormalized** discounted value satisfies `v_dummy=0`. Set `w=X^T v_original`. Direct multiplication yields

`Q[:,(j,a)]^T v = w_j-t[Bhat_a w]_j`.

Thus its Bellman inequalities and active action labels agree exactly with the acquired signed inequalities `w_j>=g_a[j]+t[Bhat_a w]_j`. This includes action-dependent rewards, nonsymmetric effects, unequal original blocks, singular WH and actual nonzero closure error. It uses no inverse of WH, no full H, no raw D_a and no new observations.

The canonical value v is not the actual normalized source value. The canonical P is not an observed block transition law, and beta need not equal the source discount gamma. The actual-source policy certificate continues to use the original gamma, acquired eta and reconstructed w:

`2 (rho + gamma eta ||w||_infinity/(1-gamma))`.

At the exact canonical solution rho is zero. No unjustified canonical-to-physical discount rescaling is made. The same prior acquisition event supports these later tasks; compilation introduces no new statistical union.

## 6. Code receiving, solver failures and scope

`compile_model` first binds the trusted received core and checks its acquired all-goal admission. It then treats rational simplex output only as a proposal. The exact original LP inequalities, positive gap, determinant, transformed signs/sums and stochastic rows are checked before PASS.

`plan_model` binds model, goal and core hashes, reconstructs each transformation identity from the actual Bhat, checks stochasticity and the dummy geometry, and performs ordinary exact policy iteration with retained ties. A strict improving change cannot cycle; the finite discounted model has an optimal stationary deterministic policy. Final canonical Bellman equations, zero dummy value, original nominal residual and active-policy identities are checked exactly. Its claimed source-regret bound is computed from the reconstructed w, not trusted from model metadata.

The consumer remains a consumer of an already received core. Digests do not authenticate iid observations or prove the core event when a caller invents both a core and its digest. These are scientific typed Python routines in normal assertions-enabled execution, not a newly claimed hardened verifier under `python -O` or arbitrary backend object attacks. Invalid inputs and failed exact assertions are refusals/errors, not successful certificates.

The historical first free-variable formulation is preserved unchanged. It proposed the zero transform/gap on an instance with a positive witness, and the compiler refused it. The current bounded translation is a reasonable ordinary workaround; it does not prove the backend is universally reliable. Exact checks remain mandatory. Independent tests also injected a zero-gap proposal and an infeasible proposal and verified refusal. A deliberately suboptimal but positive feasible half-scale witness was accepted and produced the correct policy, confirming that optimality is genuinely unnecessary.

## 7. Replays and independent checks

The frozen nonmutating author harness reproduced the saved result exactly after removing timing fields:

- **1,685 checks and 3 refusals**.
- **327 action-reward tasks**, 540 total exact policy-iteration evaluations.
- **Zero source calls**.
- All five existing fixtures remain covered: nonpredictive baseline, strict weak closure, genuinely nonclosed source, singular WH and rank-three refinement.

The existing nonpredictive source with gamma `9/10` yields the checked canonical gap `2539/2989` and discount **450/2989**. This is a property of that computational witness, not a faster physical source or a uniform favorable-gap theorem. The prototype's canonical transitions differ from averaged observed block transitions on every listed fixture.

Additional reviewer work passed **550 exact checks and 13 refusals**, with zero source calls:

- Twelve rational five-state/three-action models, unequal block sizes, and alternating exact/nonexact closure cases.
- Sixty action-dependent reward tables, checked against independent full-state exact policy iteration and actual selected-policy evaluation.
- Twelve exact common-reward raw-reset models, plus one explicit zero-reset-row elimination case.
- Immediate-decision beta-zero behavior, positive nonoptimal transform receiving, backend zero-gap/infeasible proposal refusal, model/core/goal binding and transition/X/gap/reward tampering.

Unique reviewer artifacts:

- `reviewer_2251/extra_checks.py`, 7,340 bytes, SHA-256 `aac1bbfcb9bd1db2cfba8a2d038b1cb7f3a223f944472b457a056361fb65e602`.
- `reviewer_2251/extra_checks.json`, 1,935 bytes, SHA-256 `4e10162a1ef04c43ee175df1bb9377e453c72f75553029cb9dadb81f2db9c77e`.
- `reviewer_2251/author_replay.json`, 12,371 bytes, SHA-256 `026e6a066b4cd167301513144a39cd8e3b672eca3993d833ca49833d7801e70a`.

These are exact algebra/code checks, not new empirical acquisition evidence. No frozen result was rewritten.

## 8. Paid resources and ordinary-method conclusion

Compilation pays a new rational LP, transform verification, coefficient reading, naive `O(mr^3)` matrix arithmetic, storage of X and `O(mr^2)` transition coefficients, and all rational bit lengths. Per-task execution also reconstructs transformation products; it does not silently receive those checks for free. Exact policy iteration pays every actual matrix inversion/evaluation and may be expensive when the canonical gap is small. The reported entry-bit fields do not measure every intermediate pivot/inverse operation or peak memory.

Generic rational LP supplies a polynomial-bit mathematical option. The actual SymPy simplex and policy-iteration implementations are not given a universal polynomial-worst-case claim here. The earlier primary small LP remains an alternative when canonical compilation or iteration is unattractive. Original acquisition, failed attempts, map retention and microscopic sensor/source execution are unchanged and remain paid.

The direct prior match is [Morris, generalized P-property canonical form](https://math.gmu.edu/~wmorris/cubemdpmprev4.pdf), Theorem 2 and Section 3, already read in the preceding review. Its positive-basis criterion, transformation LP and extra-state construction are the ordinary methods explicitly being implemented. This addendum does not turn them into a new planner. Strong retaining ALP/successor-feature/hidden-K methods may adopt the same acquired certificate and thereby obtain the same useful computational model.

**Final acceptance:** the frozen ordinary canonical-MDP construction, exact checked implementation, common-reward known-matrix reset alternative and restricted exact-common-part sampling obstruction are sound as stated. No practical or historical-novelty conclusion follows. The later direct-canonical-stability admission and discount-scaling extension are outside this manifest and remain unreviewed by this receipt.
