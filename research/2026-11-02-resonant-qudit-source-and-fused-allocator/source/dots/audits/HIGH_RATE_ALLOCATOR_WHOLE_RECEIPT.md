# Independent whole-join receipt: fused allocator and high-rate protected memory

2026-11-01. **Qualified mathematical PASS for the frozen finite-dimensional GKSL construction.** This closes the requested formal audit, not the practical consequence gate.

Reviewed bytes:
- `HIGH_RATE_ALLOCATOR_MEMORY_JOIN.md`: SHA256 `f769b7163ab54386c6c4313d6ea3feefc19dcec70466630932b00805fdbe24ab`.
- `producer-workspace/FUSED_GRAPH_PROTOCOL_REFRESH_THEOREM.md`: `cd7285cf05b92a6b41d5e408c9c254cc9b8d7526b68d2b46e5e780975105825d`.
- `producer-workspace/FAULT_RECOVERY_RECEIPT.md`: `028ea8223c09d9247337eba65d100d9d62bee4964f1203aa78375427e6613b7a`.

Prior independently received imports: uniform quantum-stage completion, finite-patch positive-corrector theorem, Tanner witness/flag component, noncommuting exponential lift, and killed-subchannel comparison. No pending alternative mechanism is imported.

## 1. All-state fused regeneration

The physical dimension count is 2(D+1)+2+2(D+1)+8w+4=8w+4D+10, plus one edge qutrit per conflict edge. Distinct classical/native phases are orthogonal subspaces of ONE apparatus. Thus a partial probe cannot coexist with an independent cleanup controller or finish out of order with another job at the same vertex.

The local legitimacy invariant in the structural receipt is correct. A full cleanup removes every lock owned by the vertex. Subsequently a collected prefix is owned by it and the unprocessed suffix is not. Neighbors cannot change an edge owned by this vertex: they acquire only free/self and release only self. These statements remain true even for illegitimate neighboring phases. Cleanup and collection have total rate g for every edge value; contention aborts rather than waits.

Starting at arbitrary CLEAN_j, WAIT, COLLECT_j or native phase, at most 3(D+1) rate-g steps, one rate-nu*g delay and one residual native cycle suffice to complete a full CLEAN_0 scan. Conditional moment multiplication gives the stated M_R. An initially partial cleanup does not count as full regeneration. All-state quantum interpretation is valid on the invariant phase/lock/cache-block observable algebra; within-live-stage coherences remain included in the quantum completion premise.

Once all R_u in N[v] have occurred, newly launched target cycles are isolated, but an already active target may have been contaminated. The burn construction correctly handles this: union-bound R_u>B/2, then charge survival until B of the target job active at B/2. A target still collecting at B/2 launches only after all neighborhood legitimacy has been established. A neighbor's corrupted probe from more distant conflicts cannot overlap the legitimate target while holding their common edge correctly. Thus m S_R(B/2)+S_A(B/2) is a valid local burn bound, not a global graph cleanup claim.

## 2. Quiet service word, marks and readiness

Suppressing independent dominating WAIT-attempt streams can be implemented in the analysis by removing those channels from the generator on the invariant block algebra. Its no-attempt event has state-independent Poisson probability. The native bound remains valid for that modified generator, with the same conservative incident norm bound. This avoids applying an unconditional completion estimate after arbitrary future quantum-record postselection.

During the drain, collecting jobs either abort or finish; active jobs complete; all then clean and reach WAIT. Neighbors outside N[v] cannot block cleanup. Once the entire closed neighborhood is at WAIT, every target-incident edge is free, because its two endpoints have released their own holdings. The target's unique subsequent attempt therefore acquires every edge and completes under the native bound while neighboring attempts are suppressed. Multiplying the two conditional >=1/2 success bounds is justified; independence of drain/completion times is not assumed.

For theta0 independent of lambda=nu*g, choose F using M_Q0 and M_F0, then lambda=1/(6mF). Exactly one target event in the middle F window and no other neighborhood event in the 3F word has probability lambda F exp(-3m lambda F). Therefore q=exp(-1/2)/(24m) is safe, with q/(3F)=exp(-1/2)/(72mF). Regeneration separately uses theta_R=min(theta0,lambda/2). There is no circular requirement theta0<lambda.

The polynomial-degree assertion follows with its stated hardware assumptions: at theta0 T_stage<=-log(1-p_stage)/2, the geometric stage moment is at most 1+1/sqrt(1-p_stage). Hence log M_A grows at most linearly in w times the bounded log factor, plus the final response factor. The supplied p_stage and T_stage make inverse moment radius polynomial in the incident strength bound. This is degree/response matching, not accuracy dilution; it is not a tight throughput theorem.

A latent bad-preparation mark can be attached to every target dominating WAIT attempt because it has no effect until preparation, whose mixture has state-independent weights. Aborted/null attempts only overcount marks. A job initiated before B cannot finish after an already completed post-B target job because jobs are fused and sequential. Therefore after one completed post-B job, all later potentially bad reports are covered by post-B marks. The union bound p lambda(T-B) is valid without last-report independence.

For readiness, after burn a correctly prepared active job has zero wrong-report projector in its final phase. A bad-prepared current job must descend from an actual bad preparation jump of intensity <=pg. Integrating its uniform conditional active survival gives pg integral S_A<=pg tau_A. This argument counts bad births unconditionally and does not condition their survival on future burn success. Initial arbitrary probes are covered by burn failure. Thus both claimed service bounds are full-state operator inequalities.

## 3. Exact good-write cancellation

On final phase F, put e=(1-c Sbar)/2 and d=F(1-X Sbar)/2. These commute; target final dressing is trivial. Define G=Fe-ed and Bflip=(1-e)d. Both are positive orthogonal projectors and

 chi=G+Bflip=F(1-cX)/2,
 Bflip-G=d-Fe.

All source terms except final cache write preserve e. The readout instrument gives L_src e=gamma(d-Fe). Boolean consistency changes only when the cache actually flips, so its increase is bounded by epsilon B_s gamma chi, including arbitrary probe coherences. Consequently

 L_src[epsilon E_B+epsilon sum_s B_s e_s]
 <=2epsilon sum_s B_s gamma Bflip_s
 <=2epsilon sum_s B_s gamma d_s.

This is an operator identity/inequality, not a stochastic approximation. The added positive epsilon B_s e_s price is necessary and is present in the root's V and height K. Its source drift cancels good-write exposure. The factor2 multiplying H_d and the corresponding source floor is correct.

## 4. Corrector interface and full drift

The allocator/source Hamiltonians and each lock/cleanup/preparation/decay/readout jump preserve the dressed data stabilizers termwise. Classical phases have identity prefix, preparation enters prefix I, and final readout exits a full-check prefix that commutes with each protected label. Lock qutrits are extra apparatus, not hidden stable records.

The source correctors depend only on data, source apparatus and locks. They are identity on physical witness/flag/Boolean wires, and are block diagonal in every cache. Thus ideal Boolean input-read/repair jumps and flag actuation annihilate H_e,H_d and e exactly. These claims do not say flag actuation preserves every old syndrome label: flag moves change the witness component, and their protected action instead uses the prior bounded-Pauli component argument.

Actual finite-patch generator inequalities supply -e and -d plus their floors, including both locality errors. The existing flag/verifier estimates then give the claimed -cW-aE_B-a sum e+b_src n. No all-write activity floor is needed. K correctly includes epsilon E_B, alpha H_e, epsilon B_s e_s, and twice epsilon B_s gamma H_d.

Choosing the two source floors as stated gives b_src/c<=beta/32. Actual continuing noise contributes uV/c<=beta/32, and positive height aK<=beta/32. The mean floor is thus <=3beta/32. A quadratic exponential allowance beta/8 gives total <=7beta/32. With split theta=beta/2, the moment prefactor is <=1+16/9<3. Initial encoded W=0 states satisfy the moment condition even with coherent correlated apparatus; arbitrary unencoded hot attachment is not allowed.

## 5. Protected storage and cost scope

The finite-depth prefix and flag frames still have bounded expanded support at fixed w,D and apparatus dimension. Include every actual expanded H,J and FULL J†J in the admitted old-system Pauli alphabet, with arbitrary apparatus coefficients. The prior distance/radius proof then supplies logical flatness and actual two-step W-shell bandwidth for sufficiently large n. Correctors commute the full component labels; scalar W conservation alone is not substituted.

The noncommuting local exponential theorem and killed CP-subchannel comparison therefore apply with actual enlarged constants. Counting all ideal/noise terms that cross the cut yields the stated

 2sqrt(3)n(2h_all+3Gamma_all) T_storage exp(k b_W) exp(-k beta n/4).

Fixed rate selection is independent of source accuracy, but the preparation quality must improve to reduce the service floor. Finite patch size, corrector norms/incidence, local dimension, edge reservoir rates and full hardware count remain charged. Actual perturbation norms are evaluated after these are fixed; this is a parameter-admission condition, not postselection of favorable noisy trajectories. It does not preserve tolerance to a fixed nonzero error rate as actuator rate is slowed.

The source now uses two-body data Hamiltonians, onsite native baths, and two-site CLASSICAL apparatus/edge GKSL lock operations. The Boolean verifier still uses three-site jumps. Neither full two-body hardware nor atomic reservoir engineering has been earned. Ideal encoding and terminal decoder remain the admitted endpoints. Same-resource timed control retains access to all locks, levels, reservoirs and phase references. No uniform-network numerical throughput or practical superiority follows from a two-cell example.

## 6. Checks performed and stopping boundary

Reran `allocator_audit/check_fused_allocator.py`: all-state SCC/invariant checks pass for isolated, edge, path3, triangle and star4, up to58,320 states and233,280 transitions. ACTIVE completion remains an enabled STRUCTURAL edge, not a rate model. Separately checked all16 exact rational sign cases for F,c,X,Sbar of the good-write identity, flip projector and factor2 bound; all pass. These checks support but do not replace the ordinary proofs above.

No counterexample or remaining formal gap was found in the frozen join under its explicit premises. This receipt closes the requested mathematical review. The next gate is consequential physical scale/geometry/comparator evidence, not further automatic constant optimization.
