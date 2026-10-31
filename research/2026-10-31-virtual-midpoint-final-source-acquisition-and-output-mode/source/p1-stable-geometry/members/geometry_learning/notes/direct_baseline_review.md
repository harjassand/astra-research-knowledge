# Bounded independent review of the direct successor-pool baseline

31 October 2026. Read direct_baseline.py, its recorded results, the called source/acquisition routines in compact_geometry.py, and the rational certification helpers in spectral_baseline.py. No new source experiments or parameter scouting were performed.

## Verdict

The direct baseline's central certificate is valid. I found no error that invalidates either recorded successful run. The code acquires its own landmarks and its own Gram data; the teacher report is read only after direct acquisition, for comparison. All failed task-certificate stages in the recorded runs remain in the physical bill.

The method is a bounded, possibly unsuccessful learner, not a universal polynomial-time identification guarantee. Its largest practical obligation is the attained frame floor, which is measured and paid rather than supplied.

## 1. Operator certificate: accepted

Let Z be the deduplicated pool of actual landmark words W and their one-step successors. The factor-square-root proof supplies the full operator coupling

    ||V_Z-QX_Z||op <= alpha,

not merely a maximum-column error. This stronger statement is essential here.

For each fixed operation a, the selections W and W+a both have column-selection matrices of norm one. Literal landmark words are distinct, and w -> wa is injective. Therefore the selected operator errors are each at most alpha. With E_a=A_a X_W-X_(W+a),

    (T_a Q-QA_a) X_W
       = T_a(QX_W-V_W) + (V_(W+a)-QX_(W+a)) - Q E_a.

This has norm at most 2alpha+r_a. The computed full-row-rank frame X_W has a certified smallest singular value at least sigma. Right multiplication by X_W's mathematical right inverse proves

    ||T_a Q-QA_a||op <= (2alpha+r_a)/sigma.

No inverse is executed by this proof step, and sigma is obtained from the acquired numerical frame. It is still a real conditioning cost, not a floor-free direct theorem.

The contraction A*=Q*T_aQ has operator residual at most 2alpha, proving feasibility of the fitting target. The code does not trust floating optimality: it accepts only after exact-rational contraction and actual operator-residual upper checks.

## 2. Scalar task bound: accepted

For seed x_0, S=||x_0||, and kappa=max_a(2alpha+r_a)/sigma, source/model telescoping gives

    ||T_w f-QA_w x_0|| <= alpha+|w| kappa S.

The seed readout differs from its coordinate counterpart by at most alpha, and the computed trajectory has norm at most S. Hence

    |<f,T_w f>-<x_0,A_w x_0>|
       <= alpha(1+S)+|w| kappa S.

This matches the code. The statement concerns the seed linear readout and actual control words. No full temporal-record, new-readout, or feedback conclusion follows automatically.

## 3. Selection and confidence: accepted

Each stage fixes its pool before drawing the new Gram batches. The stage budget delta/[s(s+1)] sums to at most delta, including stages that add a landmark and stages that merely refine eta. A union bound over stages therefore covers the adaptively selected final model and stopping time. The positive-definiteness tests, factor-rank check, frame check, fitted matrices, and final error decision are deterministic functions of that stage's data, so they do not require additional per-test confidence allocations.

The physical-independence test Ghat_WW-eta I positive definite is valid on the operator-error event. It proves actual independence of selected hidden word vectors, so additions cannot exceed true reachable rank on the good event. The factor-rank congruence W_num*(Ghat-eta I)W_num is also a valid exact check even though its numerical eigenvectors are not exactly orthogonal. Positive definiteness itself implies the required column independence.

The pool coupling is checked using exact rational measured means and the exact rational Gram matrix of the stored floating factor. The SVD is only a proposal for a rigorous norm upper bound: orthogonality and reconstruction defects are subsequently measured in exact arithmetic. The frame floor is independently checked by exact LDL positivity of X_W X_W* minus a proposed positive scalar. These are appropriate certificates.

## 4. Source accounting: accepted at the declared simulated-law scope

acquire_geometry purchases every unordered pool pair afresh at each stage. sample_mean increments actual episode, transition, reading, and scalar-job counters. Refinement and landmark-addition stages are included. The source's exact rational physical moment is used internally only to simulate the distribution of the aggregate binomial count; it is not supplied to the learner. The exact recorded mean is an empirical count divided by the paid sample count.

The known binary-coin rounding bias is reserved in the Gram accuracy budget. The mathematical probability statement concerns the specified independent binomial/report model; the NumPy PRNG and its huge-count numerical sampler are not separately formally verified physical instruments. The results already mark that no physical episodes were executed.

The reported CPU seconds are local simulation/linear-algebra time, not the runtime of the billed physical experiments. Keep that distinction explicit when reporting the very large savings ratios.

## 5. Recorded results and fair interpretation

For mixed_controls, the direct learner acquired three actual landmarks in a pool of ten words, then accepted at stage seven with a certificate about 0.376687 at the requested horizon eight and tolerance 0.5. Its bill includes approximately 1.924e13 preparations and 6.926e13 primitive controls. The 313 scalar jobs equal the sum over all seven stages, including the four unsuccessful task-certificate stages.

For weak_reachable_directions, the direct learner retained one landmark, accepted at stage three with certificate about 0.452019, and paid approximately 7.218e9 preparations and 1.083e10 controls. All three fresh ten-pair stages are charged. It is allowed to omit weak directions because the task certificate passes; true full rank was not assumed to be one.

Both comparisons use the same requested horizon, epsilon, confidence target, and source interface. The teacher and direct routes do not have identical attained certificate tightness: teacher certificates are about 0.273684 and 0.160002, versus direct certificates 0.376687 and 0.452019. Thus the ratios are fair comparisons of the named procedures meeting the same requested task, but not equal-attained-error comparisons or proofs of algorithmic optimality. The source bills remain enormous despite the relative improvement.

## 6. Small implementation qualifications

- If the computed positive frame floor is smaller than the resolution of sqrt_lower, that helper can return sigma=0. Check sigma>0 before dividing, and treat failure as an explicit bounded precision failure. This does not affect the recorded runs, whose floors are about 0.297 and 0.995.
- NumPy LinAlgError is not among the explicitly caught failure classes. A numerical nonconvergence can therefore abort rather than produce the promised structured failure. Add that exception if the code is presented as returning a failure object on every numerical-cap failure.
- The formal shot formula uses real logarithms and an exact ceiling, whereas the diagnostic uses ordinary binary64 math.log and math.ceil. This is a small implementation qualification for a fully outward-rounded end-to-end probability certificate. It does not affect the mathematical stage-selection proof; reserve a modest shot-count margin or validate the final allocation with interval arithmetic if claiming exact finite-machine confidence constants.
- The comparison's "complete_physical_bill" is complete for its explicitly enumerated preparations, primitive controls, and endpoint readings. Model fitting, exact certificates, simulator overhead, and future prediction arithmetic need their separate runtime/bit ledger; they are not represented by the physical counts alone.

The attained final residual checks make floating optimizer inaccuracies harmless to soundness. A capped or inaccurate optimizer can cause failure or extra cost, but cannot produce an accepted false bound while the rational checks and Gram event hold.
