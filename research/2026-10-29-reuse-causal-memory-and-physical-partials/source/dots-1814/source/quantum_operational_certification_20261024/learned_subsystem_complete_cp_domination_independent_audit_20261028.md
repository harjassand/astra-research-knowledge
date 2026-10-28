# Independent receiving: complete-memory CP domination and adaptive service

28 October 2026. Reviewer `producer-workspace/review_repeated_service_factorization`.

**PASS at the stated discarded-gauge, retired-private-key interface.** Governing source `learned_subsystem_complete_cp_domination_20261028.md`, SHA-256 `5890ae9c708c08aa4dd9909d1e6154fd8bbf64973f51395c5bf31552d3eebf6d`.

This receives a stronger composition than isolated-output noise factorization: the learned complete map CP-dominates a scalar multiple of the particular true-extraction map. It therefore gives an all-clean-process decomposition under common adaptive controllers, without commuting output errors through feedback. Independent exact checks include coherent retained memory, legitimate feedback, non-diagonal gauge effects, native Pauli noise that violates identity dominance, and a retired-key-access failure that persists even after the key is subsequently discarded.

## 1. Requested correction, now resolved

The initial coefficient formula used `(P_gamma^dagger tensor I) A_l` as a partial-trace shorthand even though `A_l:L tensor G -> L` is rectangular. That is not literally a well-typed matrix product. The root replaced it by the explicit indexed contraction

`<v_lgamma|g> = D^-1 sum_ab (P_gamma^dagger)_ab (A_l)_(b,a g)`.

This is the trace of `P_gamma^dagger` times the g-th D-by-D logical block. It has the correct factor D^-1 and leaves a row on G. The original is preserved as `_pre_block_contraction_clarification.md`; no other source change was requested. The first exact check passed on the prior bytes. Its result JSON is preserved separately, and the same mathematics was rerun and hash-bound to the corrected source. This reviewer did not modify any author or accepted source.

## 2. Effects, Bell normalization and the complete contraction

Let `A_l=sum_gamma P_gamma tensor <v_lgamma|` be Kraus operators for `Dhat Ad_U`. Pauli Hilbert–Schmidt orthogonality gives

`D^-1 Tr_L(sum_l A_l^dagger A_l)=sum_l,gamma |v_lgamma><v_lgamma|=I_G`.

Thus the positive `T_gamma` form a POVM on the emitted gauge. For a normalized maximally entangled logical input, contraction of its two logical legs gives `Tr(P_gamma)/D`, which is one at gamma=0 and zero otherwise. Consequently

`F_e(Dhat Ad_U(. tensor sigma))=Tr(T_0 sigma)`.

The hypothesis for **every** normalized gauge state is therefore equivalent to `T_0 >= c I_G`, with c=1-b. This is not justified by a successful test on the occupied gauge state alone. Although the Bell pair in this derivation is product with the gauge, the resulting operator inequality is the mechanism that later handles arbitrary logical-memory entanglement.

For any positive T, the map

`C_T(X)=Tr_G[(sqrt(T) tensor I) X (sqrt(T) tensor I)]`

is CP, also after arbitrary reference extension. Partial-trace cyclicity on G gives `C_T(X)=Tr_G[(T tensor I)X]` on every operator X, not only product states. Hence C_T is linear in T, and

`C_T0-c Tr_G=C_(T0-cI)`

is CP. T may be non-diagonal and may fail to commute with the gauge marginal or with gauge-memory correlations. The exact check deliberately uses such a non-diagonal T0.

This step requires that emitted G and decoder ancillary/measurement records are genuinely outside every later source/controller/tester port. If an ignored gauge register can later return to the source, it is future-accessible memory, not a discarded gauge. The effect then does not specify the continuing instrument, and this proof cannot be reused without a stronger instrument certificate.

## 3. Complete-memory Pauli identity and CP order

For each native Pauli alpha, the framed Kraus expression contains

`Q^dagger P_gamma P_alpha Q tensor <v_lgamma|`.

Averaging fresh Q removes cross terms between different gamma by orthogonality of the Pauli conjugation characters. The character of alpha is common to those terms and disappears from the CP expression. Therefore the resulting **complete** map is

`sum_(alpha,gamma) Ad_(P_gamma P_alpha) tensor (C_Tgamma G_alpha)`.

This is an equality on the full logical/source-memory input operator space. It is not obtained from Bell probabilities or from a fitted classical noise trajectory. Any gauge-memory-reference correlation emitted by G_alpha remains inside the positive contraction C_Tgamma.

Keeping gamma=0 and using the preceding CP order proves

`E_framed-c E_exact >=_CP 0`,

where `E_exact=sum_alpha Ad_Palpha tensor (Tr_G G_alpha)`. Both complete maps are TP, since the native Pauli operators are unitary, `sum_alpha Tr_G G_alpha` is TP, and the actual receiver/framing is CPTP. Thus the positive difference has trace effect `b I_LM`, and division by b produces a genuine CPTP residual for b>0. For b=0, a CP zero-trace difference is zero; for b=1 the residual is just E_framed.

The clean label here is a **decoder-extraction** label gamma, not the native noise label alpha. Native Pauli errors can be large, correlated and non-identity-dominant. Neither global CP identity dominance nor positive service-time X/Z contrasts enters this proof. The benchmark is the particular true-extraction process, not an optimal or noiseless channel.

The residual is a proof device. The learner neither computes its unknown source-dependent Kraus operators nor receives a clean flag. No physical implementation of the virtual mixture is required by the actual protocol.

## 4. Adaptive process semantics and the correct reference trajectory

Fix a finite T and a single declared causal source law on **all** admissible histories. At each slot the selected nominal receiver/source block must obey the same uniform b certificate and the same complete port conditions. A classical-history-controlled block inherits CP domination blockwise. Coherent controllers between slots are ordinary CPTP supermaps and need not be diagonal or commute with any logical error.

Expanding the composition of `c E_exact+b F` produces a branch with coefficient c^T in which every slot uses E_exact. That branch is exactly the true-extraction process with the same initial source memory, calibration record and controller law. In other branches, controller outcomes and source memory trajectories may differ arbitrarily. They are not forcibly identified with the ideal trajectory. This is precisely why the new argument works where same-occupation comparisons or isolated-output commutation would not.

A useful formal construction chooses all T virtual clean/residual coins before the process, independently of every input. Each fixed choice defines a deterministic causal CPTP strategy because the local exact and residual maps are CPTP on every allowed history. Conditioning this finite mixture on at least one residual choice leaves a convex mixture of deterministic strategies. Thus

`E_learned,process=c^T E_exact,process+(1-c^T)F_process`

is a strategy-level statement, not merely a residual final map invented after selecting one tester. Every permitted common tester then has output-state half trace distance, or event-probability difference, at most `1-c^T<=Tb`. Deterministic per-slot uniform bounds b_t similarly give the product `product_t(1-b_t)`. This formula does not silently extend to history-dependent random b_t without an additional uniform bound/accounting argument.

Allowed controllers may process, measure, feed back, swap or reuse prior logical outputs and their own ancillas. They must not receive retired frame keys or discarded gauge/decoder records, and must preserve the declared source class. The strategy supremum is over that allowed interface, not over testers furnished extra leaked ports.

For an induced channel on arbitrary payload inputs alone, initial full payload/reference independence from source memory, conditional on calibration, is needed. The source states this. The complete linear identities remain valid on the larger input including source memory and hence also for arbitrary initial correlations there; such correlated preparations do not in general define a payload-only channel. The calibration good-event averaging remains unconditional, with no postselection on a particular accepted or exposed history.

## 5. Independent exact adaptive and CP checks

`learned_subsystem_complete_cp_domination_independent_check_20261028.py` is independent of the author's fixtures. It uses rational/Gaussian-rational arithmetic and exact symbolic square roots, with no floating tolerance or random data.

The receiver is a gauge-basis rotation followed by one of two logical rotations and a gauge trace. Direct rectangular Kraus expansion gives

`T0 = [[75664,10752],[10752,81936]] / 105625`.

Its certified c is 16/25, b=9/25, and `T0-cI` has eigenvalues 896/4225 and zero. The off-diagonal entries ensure the contraction test is not merely a classical diagonal-gauge example. The check recovers every Pauli effect from the actual Kraus matrices, verifies positivity/normalization and checks the contraction on every source-memory matrix unit.

Two different time-dependent weak source instruments have noncommuting rational memory Kraus operators, retain off-diagonal information and do not reset memory. Their native Pauli probabilities are `(1/5,3/5,1/5,0)`, so identity dominance explicitly fails. For each slot the exact 16-by-16 Choi difference `J_framed-c J_exact` equals a displayed sum of nonnegative Kraus outer products. Its trace effect is exactly bI. This directly verifies complete CP order, not just positivity on a sample of states.

The two-slot process then interleaves a legitimate external-controller CNOT from completed output1 into future input2. The controller never accesses source memory or frame keys. All 16 fresh-frame histories are enumerated, and the complete 64-by-64 Pauli-transfer map on two logical registers plus retained source memory is checked on all 64 input operators. The positive nonclean part equals

`c E2 C R1 + c R2 C E1 + R2 C R1`,

where `R_t=E_framed,t-c E_exact,t` is CP with trace effect bI. Its trace effect is `(1-c^2)I`. The all-clean coefficient is exactly 256/625 and the process-distance bound is 369/625. Tracing final source memory preserves the equality. All initial correlations and external-reference extensions follow from equality of the complete linear maps.

## 6. Exact failure checks for leaked keys and retained gauge

The key restriction is stronger than merely discarding a key at the final reporting time. Take one logical rotation `W=(12/13)I-i(5/13)X`, whose uniform extraction b is 25/169. With properly private retired Pauli frames, the channel is the Pauli mixture with half-diamond error b.

If a later controller obtains Q, it can apply `Q` to the recovered logical output and `Q*` to its Bell reference. On every branch this maps the framed state back to the same coherent W-Bell state; the exact-extraction Bell state stays unchanged. The controller may then discard Q. The final half trace distance is **5/13**, strictly larger than **25/169**. Thus future key access invalidates the claimed bound even when the final tested registers contain no key.

The key-flagged normalized Choi comparison also has an explicit negative witness: a unit vector orthogonal to the actual W-Bell vector gives expectation `-900/28561` in one key block of `J_learned-(1-b)J_exact`. Hence the failure is of CP domination itself, not just a loose estimate.

For the discarded-gauge boundary, a receiver that performs logical identity but flips an emitted gauge qubit has virtual logical Bell fidelity one for every gauge state: T0=I and b=0. If the gauge is retained and compared with a benchmark that preserves it, input gauge |0> produces orthogonal |1> versus |0> outputs. The effect certificate controls the traced gauge contraction, not that retained instrument. Both boundary checks are exact.

## 7. Acquired certificate, implementation budgets and resource meaning

The approximate on-site acquisition source is bound to SHA-256 `8ed5031f786c6eac4a3a5c10e02d2cb149f70343bc1a519ee1ce8a4d3eea54d5` with its independent statistics and memory receipts. I imported only its good-record **all-gauge extraction** bound and finite call cap, not its one-service oracle interpretation or lower-bound theorem. Its full-reference stabilizer argument gives the required uniform virtual loss, including arbitrary gauge purifiers. A persistent fixed-axis tube supports the same certificate for later allowed U_t/history changes. Actual later membership in that tube is a physical premise, not inferred from the fit.

At epsilon_train=epsilon/T, the approximate certificate obeys

`Tb <=9 T q tau^2+2epsilon/9`.

Adding one bad-calibration event, `beta<=epsilon/8`, and `nu_cal+nu_svc<=epsilon/4` gives the coefficient `2/9+1/8+1/4=43/72<1`. This proves the stated `min(1,9Tq tau^2+epsilon)`. The exact source's sharper certificate instead gives `21epsilon/32`. Forty-eight exact scalar cases supplement these direct inequalities.

Calibration-record TV transfers the probability of a **record-defined uniform extraction event**. Every good physical record then supplies the same all-gauge bound even at memory altered by imperfect calibration. The benchmark service starts from that actual conditional post-calibration memory. It does not replace the acquisition trajectory by a counterfactual oracle trajectory.

The whole-T service implementation debit must compare complete processes from that same starting state and include the actual declared feedback/controller, local controls, holding, routing, resets and key retirement. A complete-register per-slot local-control discrepancy summing to nu_svc suffices by hybrid; a reduced payload-only test at fresh/product memory does not. If an implemented controller differs from the benchmark controller, that discrepancy must be included rather than called a common-controller comparison for free.

The actual implementation uses the received finite ordinary calibration and classical fits, followed by T native payload calls, q known inverse one-qubit controls and 2q fresh frame bits per slot. It does not implement the residual map, learn the environment or herald clean uses. Quantum storage, feedback processing and privacy/retirement are paid supplied interfaces. Unlike the isolated-output theorem, this result permits output reuse, but it does not make arbitrary coherent feedback or quantum memory inexpensive or available on unvalidated hardware.

The floor grows as Tq tau^2. No local-stochastic distribution across sites, threshold, general code performance, collective decoder optimum or small native source error is implied.

## 8. Relation to the supplied Astra comparison

Read the root's comparison companion and the exact selected N1004 governing/review passages retained in `astra_task_effects_cp_comparison_20261028.json`. They already contain full Pauli-twirl identities, positive task effects, bad-effect/fault envelopes with retained memory, and a same-total-environment-channel comparison. These are not newly received inventions here. Their fixed-product and backward-isolation conclusions have their stated output/future-wire restrictions.

The specifically checked addition is the discarded-gauge contraction's CP lower bound by the **particular true-extraction complete map**, followed by its all-clean adaptive-process mixture. This is not a claim that no prior complete channel comparison can compose adaptively, nor a generic promotion of an effect bound into control of an arbitrary retained instrument. I bind the companion and supplied exact passages as an interface comparison, not as a new imported theorem or a historical-priority determination. The parent retrieved their current corpus context; this review did not independently refetch the entire current capsule or claim a literature search.

## Receiving conclusion

No unresolved mathematical issue remains within the corrected source's declared interface. The strongest exclusions are essential: persistent all-gauge certification, a causal source law specified on all compared histories, genuinely discarded emitted gauge/decoder records, and **no later controller/source access to retired frame keys**. Actual physical validation of these ports and of the whole-process control budget remains an external implementation obligation. Source calls, acquired outcomes, random draws, production gate synthesis and hardware executions in this review were all zero.
