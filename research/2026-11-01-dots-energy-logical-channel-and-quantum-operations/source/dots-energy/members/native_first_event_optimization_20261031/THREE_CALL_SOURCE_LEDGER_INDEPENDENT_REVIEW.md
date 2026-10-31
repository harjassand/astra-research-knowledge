# Independent three-call source and ledger binding

31 October 2026. PASS for the strengthened scalar acceptance bound, the three-call source preparation, and reproduction of the separately labeled numerical ledger. No whole Gaussian-kernel integration or practical advantage is admitted.

## Exact versions

I read the full diff from the preserved five-call source, SHA `c58d3e1e99128ddc3de8c3442d0d6e8666be3a491f86333a259fa356df524061`, to current `CONSTANT_AMPLIFIED_BRIDGE_PREPARATION.md`, SHA `c09eba3ff6c759cba06ffb81d143ae4cb3f7350c920366ae094f4d9377b2283b`. The original is preserved exactly as `CONSTANT_AMPLIFIED_BRIDGE_FIVE_CALL_DRAFT_c58d3e1e.md`. The prior complete source review remains `HIERARCHICAL_AMPLIFIED_BRIDGE_INDEPENDENT_REVIEW.md`, SHA `32fac2f17d0fa60a16642eb1447aa14f07bfa2d5b1743284dacae96f778bf9a2`.

The current ledger code was read in full: `amplified_source_ledger.py`, SHA `01fe68ba4f2c32b9560c611b3020355af437ea77a230db816f645b96310c54e5`. Its JSON has SHA `c15eb1aa564aaac2d79552c3271daef36362b1de69c36977f3c418ad38cc95d5`. All 30 rows were regenerated in memory and matched exactly without overwriting the saved data.

## Mean acceptance and exact degree change

On the lower triangular arm set z=x/x0. Its proposal density is 2z. Since a*x0 <= v*x0 <=1 and z-1<=0, exp(a*x0*(z-1)) >= exp(z-1). The function (1-exp(-y))/y decreases for y>=0, so its value at v*x0*z is at least its value at z. Thus the lower-arm mean is at least

 2 integral_0^1 exp(z-1)(1-exp(-z)) dz = 2-4/e > 1/2.

On the upper arm v*x>=1, and acceptance is at least 1-exp(-1), which is larger. Mixing the arms preserves the lower bound. This is a uniform analytic mean bound, not a typical-value or numerical inference; the pointwise 1/5 bound used for the separate stability coupling remains valid.

Attenuation by sin(pi/6)/sqrt(P) is a contraction, ideally at most 1/sqrt(2). One ordinary Grover iterate gives sin(3*pi/6)=1, hence three calls to the attenuated proposal or its inverse. The old coherent-time-register, fixed phase, selected-word-mean and finite-grid error arguments remain valid with constant degree reduced from five to three. Clipping the numerical P representative into [2/5,1] also leaves a safe contraction and is charged to the scalar error budget. No measurement of the parameter register, unknown-probability estimation or retry has been introduced.

## Ledger and independent rerun

The ledger instantiates the unchanged displayed delta_s, h, h_prop, strip width and finite-uniform budgets of the current source. In these fixtures tau_max<1, so its use of one for max(1,tau_max) is correct. The inherited sharp S, d_A and K are unchanged. The conditional-proposal-unitary call proxy, including path preparation and unpreparation, is exactly 6 S d_A K.

The reproduced inner-uniform budgets range from 209 to 294 bits. The reproduced whole conditional-proposal-unitary proxies range from 18,629,688 to 435,157,470. These counts concern whole proposal-unitary invocations, not elementary arithmetic or quantum gates. Scalar P computation, logs/square roots, rotations, Poisson scans, actual source kernels, operator encodings and consumer costs remain separately paid. No inner operation count or physical error certification is inferred merely from the numerical bit columns.

I also read and reran `check_three_call_source.py` in memory with its output writer intercepted. All 12 cases passed the vector-rotation and finite-grid checks. Its smallest computed analytic acceptance was approximately 0.5284822353145986, agreeing with the limiting 2-4/e bound. The script's built-in acceptance assertion is only the older 1/5 bound; I separately checked all its cases against 2-4/e with numerical tolerance. This is a diagnostic, not the proof or a synthesized gate backend.

## Scope

The earlier five-call source and receipt are historical valid results, not silently relabeled. This note binds the actual three-call change and its current ledger only. The stable hierarchical source assumptions, selected-mean versus vector-error distinction, full finite synthesis budgets and private outer-clock interface remain binding. The count/window/word caps and the sharp padded-kernel stage ledger are not changed. No quantitative runtime crossover, novelty or practical implementation follows from the lower proposal-call proxy.
