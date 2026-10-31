# Independent audit of the implemented quadratic scalar learner

31 October 2026. Reviewed quadratic_scalar_baseline.py, the called source and shot-schedule code, the rational norm/contraction helpers, and both saved H=8 and H=64 results. No acquisition experiment was repeated. The only executed check reconstructed the existing physical bills from saved raw batch records.

## Verdict

No model-soundness error was found in either recorded successful run. The implementation follows the rational-whitener/Schur theorem, including the true-subspace gauge, the two leakage directions supplied by actual self-adjointness, stored contraction/seed errors, and binary64 execution allowance.

The substantive presentation qualification is that the confidence ledger proves joint soundness with possible rejection, not automatically conditional accuracy given a successful return. A bit-length metadata label was also corrected in coordination with the spectral-baseline agent; numerical results were not changed.

## 1. Pool and successor indexing

The pool starts with the actual landmarks in their existing order and appends each distinct one-step successor. The empty seed remains the first landmark. Therefore the seed coordinate is consistently e_0.

For primitive a, the code uses

    Khat_a = sym(Gram[W, W+a]),
    Dhat_a = Gram[W+a, W+a].

The successor map w -> wa is injective on distinct literal words, so both selections have operator norm one. The acquired full-pool operator-norm Gram error eta therefore also bounds the G, K, and D submatrix errors. Symmetrization preserves the error bound because the true K is symmetric under the supplied self-adjointness premise.

D_a is the Gram of the actual successor vectors. Thus D_a=V*T_a*T_aV, which equals V*T_a^2V here. The interpretation as both forward and reverse leakage is justified by actual self-adjoint primitives, not by the numerical symmetry imposed on the fitted matrices.

## 2. Rational whitening and seed

The floating upper Cholesky factor U is only a proposal. Its entries are converted exactly to dyadic rationals, and R=U^(-1) is computed in rational arithmetic. The code then independently certifies

    nu >= ||R*Ghat R-I||,
    z = eta ||R||^2,
    t=nu+z <= 1/2.

The checked norms include the exact rational matrix being bounded; the floating SVD only proposes a factorization whose reconstruction and orthogonality errors are subsequently bounded in exact arithmetic. Inaccurate numerical decompositions can make a certificate conservative or fail, but cannot make it falsely small if the helper's exact inequalities are respected.

The actual metric E=R*GR is positive definite on the Gram event, so Q=V R E^(-1/2) is an isometry onto the true landmark span. No numerical access to Q or E is used by the learner.

The first column of U is exactly R^(-1)e_0, so the seed0 construction is correct. Treating this vector as a one-row matrix is legitimate: its operator norm is its Euclidean norm. The stored seed's norm and its distance from seed0 are checked, and the bound 2(t+d_b) correctly covers both the seed and the same endpoint readout.

## 3. Schur and stored-operation certificates

For each action the code forms, in rational arithmetic,

    B0=R*Ghat R,
    Atilde=R*Khat R,
    C=B0^(-1) Atilde,
    Rhat=R*Dhat R-Atilde C.

The code checks Rhat is exactly symmetric. Since B0 is positive definite, the empirical residual identity used in the proof applies. It uses ||Rhat|| as an upper bound on lambda_max(Rhat), which is conservative but sound and automatically nonnegative.

The squared leakage bound

    [||Rhat|| + z(1+||C||)^2]/(1-t)

is therefore valid. Exact norm certificates are also applied to the stored contraction and to its difference from Atilde. Thus 3t+d_a is a valid operator error in the actual isometric gauge. The stored matrix is checked to remain exactly symmetric in its dyadic representation; exact symmetry is helpful but the subsequent rollout proof only needs its certified contraction norm.

The final expression

    binom(H,2) e_max^2 + H max_a(3t+d_a) + 2(t+d_b)

matches the theorem. The acceptance decision compares exact rational quantities to an exact rational task tolerance, before converting anything to display floats.

## 4. Adaptive confidence and rejection

Stage s uses the exact rational allowance delta/[s(s+1)]. Its pool and requested precision are fixed before the fresh reports are acquired. The full-pool confidence event simultaneously controls every subsequent G/K/D selection, candidate independence test, whitening proposal, fitted matrix, and task decision made from that stage. No extra per-candidate or per-fit union bound is required.

The updated shot schedule is conservative in integer/rational arithmetic. It uses 3N > N ln(9), an integer upper bound on ln(2/delta_s), and an exact ceiling. It also reserves N times the known per-report coin-mean rounding bias before allocating the statistical eta. This resolves the earlier floating-log/ceiling qualification in the direct diagnostic.

The good event across all stages has probability at least 1-delta. On that event, any returned model is sound. The precise consequence is

    Pr(successful return AND violated certificate) <= delta.

Because the implementation can reject at a numerical, stage, landmark, or physical-preparation cap, this is not by itself the conditional statement Pr(violated certificate | success)<=delta. That stronger statement needs a yield bound or a conditional error adjustment. No such adjustment is needed if the result is described as the joint soundness guarantee above.

Each saved run has a delta=0.01 ledger. A simultaneous guarantee for both separately run outputs should either union their budgets or explicitly use a common nested acquisition record. The H64 final model by itself covers every word of length at most 64, so its own 0.01 ledger suffices for use of that model alone.

## 5. Adaptive landmark discovery

Floating factor coordinates are used only to propose which actual successor to consider. A new landmark is appended only after exact positive-definiteness certification of Ghat_[W+j]-eta I. On the joint Gram event this proves physical independence from the current landmarks. Numerical factor rank or a least-squares residual is never trusted as a physical independence fact.

The discovery factor's own rank certificate is not required by this selection step, because the decisive appended-landmark test is independent and exact. A poor proposal can delay discovery or cause failure under the finite cap; it cannot invalidate an accepted scalar certificate.

The final model can be accepted before acquiring all true reachable directions. That is legitimate because the measured task-specific leakage certificate, rather than a rank-completeness assertion, is what licenses the return.

## 6. Physical accounting reconstructed from saved batches

Every fresh unordered-pair batch is present in the saved raw ledger. Recomputing the counters from n, u, and v in each batch exactly reproduced both final bills:

| Run | Preparations | Primitive controls | Endpoint readings | Scalar jobs | Maximum return depth |
| --- | ---: | ---: | ---: | ---: | ---: |
| H=8 | 1,689,301,760,258 | 6,081,268,320,879 | 3,378,603,520,516 | 258 | 6 |
| H=64 | 7,076,851,016,432,793 | 25,476,663,441,142,005 | 14,153,702,032,865,586 | 423 | 6 |

Every stage's planned preparation count equals its actual count in the saved runs. All landmark-addition and unsuccessful precision stages are included. The preparation cap is checked before requesting the next stage, so a rejected planned stage is not silently counted as executed or omitted after execution.

The H8 and H64 run_case calls initialize new source objects and acquire from scratch. They are separate acquisition demonstrations, not an implemented incremental H8-to-H64 update. A sequential lifetime containing both executed acquisitions must include both bills; a proposed nested reuse path needs explicit implementation and accounting.

The implementation performs aggregate binomial simulation, using exact rational physical moments internally and an explicitly bounded binary-coin rounding bias. It does not physically execute trillions of laboratory episodes. The recorded CPU seconds measure the simulation and local matrix work; they must not be presented as the execution time of the billed physical work.

The learner receives exact empirical batch means, not population means or hidden vectors. Population truth is used only inside the source simulator and in the explicitly post-acquisition audits. The code checks that those audits did not change the physical-query ledger.

## 7. Saved task certificates

The H8 run accepts after six stages with three landmarks and a pool of ten words. Its bound is approximately 0.2457599255, decomposed as:

- Quadratic leakage: 0.1997971963.
- Estimated operators: 0.0424652143.
- Initial/readout coordinates: 0.0034975148.
- Binary64 evaluation: about 4.95e-15.

The H64 run accepts after nine stages with the same landmark descriptors. Its bound is approximately 0.2305919145, decomposed as:

- Quadratic leakage: 0.2252468191.
- Estimated operators: 0.0052904045.
- Initial/readout coordinates: 0.0000546909.
- Binary64 evaluation: about 3.73e-14.

Both meet their requested additive tolerance 0.5. The finite held-out audits checked 844 words each. The statement about all 5,150,525,730,438,768,726,986,773,633,921 words of lengths zero through 64 comes from the mathematical uniform certificate, not from enumerating or testing those words. Evaluating future supplied words still has its ordinary matrix arithmetic cost; no planner or whole-table computation is supplied for free.

## 8. Finite precision and metadata correction

The execution error bound assumes ordinary binary64 arithmetic with the stated underflow allowance. Stored contractions and the seed have norms at most one, so the dimension-three, horizon-64 computations cannot overflow. The state-rounding and final dot-product contributions are accounted for by the called bound.

The original field largest_checked_rational_bit_length scanned entries of selected matrices, not every exact-arithmetic intermediate or the final error-bound fraction. In coordination with the spectral-baseline agent, it was renamed to largest_selected_matrix_entry_bit_length, and final_error_bound_bit_length was added separately. Numerical experimental results were unchanged and no acquisition was rerun for this metadata correction.

The exact bound fraction can have much larger numerator/denominator lengths than a matrix entry, particularly because the binary64 propagation allowance is represented as exact rational powers. Neither statistic is a count of all integer operations or a global peak-memory certificate. The proof's rational arithmetic costs and the measured local CPU time remain separate from the physical bill.

## Scope retained

This audit supports the specified stationary, norm-bounded, self-adjoint scalar-return experiment and the same seed endpoint readout. It does not establish a full visible-record model, arbitrary new readouts, unknown nonreversible controls, source stability from data, universal success under the finite caps, physical apparatus performance, or optimal acquisition complexity.

## Dated addendum — 31 October 2026: explicit warm continuation now audited

The separate-run caveat above remains correct for the original quadratic_scalar_baseline_results.json records. A new, separately saved operation in quadratic_scalar_warm_results.json and quadratic_scalar_warm_model.json now implements H8-to-H64 continuation on the same source. It retains the actual landmarks and exact Gram data, first rechecks the H64 bound without new samples (about 14.7286, correctly rejected), and then acquires only stages 7 through 9 under the continued original confidence ledger. The final bound is about 0.230592. The initial-plus-marginal physical bill equals the recorded lifetime bill exactly. No new word types or unordered Gram-pair types are introduced; all finer-precision cohorts are fully charged. This resolves the earlier operational gap for the new warm artifact without rewriting the status of the original independent runs. Details and the saved-record audit are in quadratic_task_final_review.md. No experiment was rerun for this audit.
