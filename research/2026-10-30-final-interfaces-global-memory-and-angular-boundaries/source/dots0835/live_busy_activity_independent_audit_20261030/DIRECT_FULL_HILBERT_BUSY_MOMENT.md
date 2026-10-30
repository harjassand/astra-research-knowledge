# Direct full-Hilbert activity moment on the accepted native apparatus
2026-10-30. Independent constructive review by `challenge_live_busy_energy`.

## Verdict
**PASS as a new mathematical corollary of the accepted full-Hilbert BUSY activity machinery, on the SAME unified native physical generator.** This earns an exponentially small fixed-positive BUSY-density tail uniformly at each elapsed time, for sufficiently small fixed physical first-drive/noise parameters and all-ready initialization. It uses neither a DATA-energy theorem nor dirty-controller normalization.

This is the corrected governing derivation. The earlier root `ACTIVITY_ONLY_GLOBAL_MOMENT.md` proposed a history-weighted, guarded, dirty-normalized observable. That route is unnecessary for the stated BUSY-tail goal and is NOT silently promoted to an independently audited theorem here. All accepted retirement/readout constructions remain unchanged.

## 1. Exact inherited inputs and same hardware
Read together:
- `weak_initiation_compiler_20261030/ONSITE_ABORT_BUSY_WITNESS.md`;
- `weak_initiation_compiler_20261030/COLLISION_HIERARCHY.md`;
- `weak_initiation_compiler_20261030/MULTIPLICATIVE_ACTIVITY_WEIGHT.md`;
- `weak_activity_independent_audit_20261030/INDEPENDENT_REVIEW.md`, especially sections 1–7;
- `weak_initiation_compiler_20261030/UNIFIED_GENERATOR_INTERFACE.md`, especially sections 1, 2 and 8;
- `native_continuous_bridge_20261030/NATIVE_CONTINUOUS_BRIDGE_MANUSCRIPT_V1.md`, sections 1 and 5, and its governing `WHOLE_REVIEW_INDEX.md`.

Hashes are recorded separately. The original weak-activity receipt was not by itself a receipt for a differently retuned native apparatus. The unified interface supplies the actual identification: the global BUSY fast generator L0 sets ONLY the first acquisition amplitude epsilon to zero, keeps later acquisition at the already chosen fixed positive zeta, keeps EVERY new complete Ai-to-Q0 abort, fast cleanup, the actual payload, and the FULL actual finite monitor generator. The witnesses below are recomputed from THIS L0. Its accepted ready-return path needs no acquisition edge; the fixed later zeta is therefore compatible with the full-Hilbert return proof. The actual native generator is exactly

    L_native = L0 + epsilon V,

where V consists of the actual first-edge Hamiltonian terms. No simulated/effective physical generator is introduced.

The inherited full-Hilbert finite-support witnesses are the ORIGINAL X_h, before history pinching, DATA conditional expectation, or history guards. For fixed x_-,x_+>0,

    x_- P_h <= X_h <= x_+ P_h,
    L0* X_h <= -P_h,
    [X_h,P_j]=0 for EVERY j.

P_h is the actual BUSY projector, the complement of (A0, workspace zero, no own o/z resource tags), with monitors unrestricted. All P_h commute. The original X_h may depend on DATA on malformed histories. That is harmless here: there is NO DATA potential to commute through it. Pinching/conditional expectation was needed for the DATA-weighted synthesis, not for a separate activity observable.

The accepted full-Hilbert block-algebra proof is load-bearing: every fast Hamiltonian preserves P masks, and the complete separately resolved resets preserve their adjoint block algebra. It is stronger than a classical or expectation-only no-creation statement. The fast-return argument includes arbitrary DATA, workspace, monitor, exterior, bath/reference input; the local polynomial construction preserves the flag corner and controls derivative error without applying an extensive generator to a norm remainder.

## 2. Full catalog, with the pair term retained
Let H be ALL native owners, including boundary owners, and E all pairs in the chosen fixed bounded-degree activity/read-write overlap graph. Every pair endpoint is included in H. Let |H|<=nu_H N; incidence and support/color depth are fixed. Orient each pair e={h,j} once and use X_e=P_j X_h. The inherited inequalities imply

    x_- P_hP_j <= X_e <= x_+ P_hP_j.

Choose the fixed coefficients B>0 and then A sufficiently large as in the reviewed multiplicative theorem. For a sufficiently small fixed proof parameter delta>0, form, in the inherited global bounded-depth color order,

    Q_h=exp(delta A epsilon^2 X_h),
    Q_e=exp(delta B X_e),
    Y=ordered product of ALL Q_h and Q_e,
    G=Y†Y.

These are mathematical gates only. They add no hardware operation. There is NO history guard, NO history exponential, NO T_B, and NO useful T_t.

Set

    M1=sum_h P_h,      M2=sum_{e={h,j}} P_hP_j.

Every factor and G commute every P_h. On one joint P-mask, every singleton gate has minimum/maximum singular value bounded respectively by exp(delta A epsilon^2 x_- p_h) and exp(delta A epsilon^2 x_+ p_h), and every pair gate has the analogous pair bounds. Minimum singular values multiply, as do upper norm bounds, without requiring the gates to commute internally. Therefore, sector by sector,

    2 x_- delta(A epsilon^2 M1+B M2)
      <= log G
      <= 2 x_+ delta(A epsilon^2 M1+B M2).             (2.1)

In particular,

    G >= exp(k delta A epsilon^2 M1),  k=2 x_->0.     (2.2)

This proves the lower barrier directly on the full physical Hilbert space. It does not infer positivity of Y or replace a noncommuting product by the exponential of its sum. Equivalently first prove scalar bounds on G inside each joint mask, then use operator monotonicity of log there.

The M2 term MUST remain in the upper bound used for coercivity. Bounding it by degree times M1 prematurely would lose the matching epsilon^2 singleton scale. Full singleton coverage is explicit; there are no omitted boundary anchors.

## 3. Exact native drift and entropy coercivity
The accepted full-Hilbert multiplicative activity theorem, applied to this full anchor/pair catalog, gives positive constants a,b,C independent of N, elapsed time, and sufficiently small epsilon,delta:

    L_native* G <=
      [-a delta A epsilon^2 M1-b delta B M2
       +C delta A epsilon^4 |H| I] G.                (3.1)

This is the actual physical generator acting directly on G. It is not inferred from a DATA-weighted inequality, a clean-only restriction, or a nonpositive inverse. In particular there are NO dirty activation terms to bound and NO generic O(delta^2)N or O(delta)N source.

The absence of those generic sources is inherited from the reviewed corner-sensitive calculation: a fast Taylor word containing a pair gate stays in a pair corner, while a word with only at least two singleton gates carries epsilon^4 and a singleton corner. Weak pair creation is charged to pair service and then singleton service; only own singleton ready/busy creation leaves the O(delta A epsilon^4) idle source. Full-Hilbert DATA dependence of X_h does not affect these flag-block statements.

By (2.1), choose, for example,

    lambda=min(a,b)/(2 x_+)>0.

All coefficients in (2.1) and (3.1) commute G. Consequently

    L_native* G <= -lambda G log G +rho_native N G,
    rho_native=C nu_H delta A epsilon^4.             (3.2)

Lambda is independent of epsilon and delta in their allowed small ranges. Neither the DATA basin nor canonical DATA error weight occurs in this calculation.

## 4. Actual bounded-body common-bath noise
Use the same physical bounded-body incident-cb-norm noise convention as the accepted memory theorem. The finite-depth physical-to-forest conjugation enlarges each noise support by only fixed bounded cones. Arbitrary retained bath coefficients remain untouched. Assume the actual normal joint CPTP evolution exists; bath-only generators commute the system observable and contribute zero.

For a local HP perturbation N_Z*, define C_Y(O)=Y† OY. Exact finite-depth cancellation gives a bounded local map

    Ntilde_Z*=C_Y^{-1} N_Z* C_Y,
    ||Ntilde_Z*||_cb <= K ||N_Z*||_cb,

where K depends only on the fixed bounded-body size, local dimensions, gate cones, and local inverse norms. It is uniform in N and in the allowed small epsilon,delta range. This congruence is NONUNITAL; do not apply an identity-annihilation lemma to its transformed map. Instead, directly at I,

    Ntilde_Z*(I)<=K ||N_Z*||_cb I.

Congruencing back and summing the actual incident norm budget gives

    N_u* G <= C_noise eta N G.                       (4.1)

This is the accepted nonunital local-noise argument with raw factor I; no syndrome-orbit ratios are needed. It is representation-free under the cb-norm convention, includes common-bath/reference extensions, and does not sum a chosen representation's jump norms. A support may be a union of boundedly many distant cones; bounded-body size and incident norm budget, not a complete partner graph, bound the sum.

With rho=rho_native+C_noise eta, (3.2) and (4.1) give the full physical joint inequality

    (L_native*+N_u*)G <= -lambda G logG+rho N G.      (4.2)

## 5. Scalar moment and direct BUSY-density tail
For the FULL normalized physical joint state rho_u (not a killed or renormalized process), set x(u)=Tr(rho_u G). The observable acts as identity on bath/reference. Scalar spectral Jensen for z log z gives

    Tr(rho_u G logG)>=x(u)log x(u).

Thus

    d log x(u)/du <= -lambda log x(u)+rho N,

and

    log x(u) <= e^{-lambda u}log x(0)
                 +(rho/lambda)(1-e^{-lambda u})N.   (5.1)

All-ready initialization gives G=I on its entire input subspace, hence x(0)=1. This holds for arbitrary DATA and arbitrary reference/bath entanglement consistent with that ready support; encoded DATA is only needed for the separate logical-memory statement. The result is uniform at every elapsed time u>=0:

    log x(u)<=(rho/lambda)N.

From (2.2), for fixed beta>0,

    Pr_rho_u(M1>=beta N)
       <= exp{-[k delta A epsilon^2 beta-rho/lambda]N}. (5.2)

No no-jump survival factor or useful-credit identity-branch loss appears. This is a pointwise-in-time uniform bound, NOT a claim that no high-BUSY excursion ever occurs over an infinite time interval.

## 6. One compatible apparatus and proof-parameter order
Keep the native physical fast rates, new abort channels, fresh dirty coefficients, and chosen fixed positive zeta. Build the actual full-Hilbert X_h at that zeta. Choose the activity-only A,B and a fixed sufficiently small delta according to the reviewed theorem. They may differ from the mathematical coefficients and delta_mem=d_mem epsilon^2 used by the separate DATA-memory proof; no physical rate differs.

For a desired fixed beta, choose the ONE physical epsilon small enough for both the accepted memory theorem and

    C nu_H epsilon^2 <= lambda k beta/4.             (6.1)

Choose the allowed physical noise threshold to satisfy BOTH the accepted memory threshold and

    C_noise eta <= lambda k delta A epsilon^2 beta/4. (6.2)

All requirements are upper bounds on the same epsilon/noise scale after fixed zeta, so a common strictly positive choice exists. No independent hidden hardware retuning is performed. For an already numerically fixed apparatus, its epsilon and actual noise budget must satisfy these additional inequalities before this particular beta is certified; a merely qualitative earlier receipt is not numerical verification.

Equations (6.1)–(6.2) imply, for every u>=0,

    Pr(M1>=beta N)<=exp[-(k/2)delta A epsilon^2 beta N]. (6.3)

Unlike the superseded guarded route, delta need not scale as epsilon^2. The source-to-BUSY-barrier ratio is O(epsilon^2)+O(eta/(delta A epsilon^2)). The memory theorem's still smaller permissible eta can be intersected with this threshold. All constants are fixed independently of N and runtime, although potentially extremely poor.

## 7. Consequences and retained boundaries
This result supplies a physical BUSY-count tail on the SAME running memory and does not require controlled retirement, DATA-basin conditioning, or an ideal frame inverse to establish that tail. It does NOT say all controllers are idle: at fixed weak drive an extensive but small BUSY population is allowed.

The direct bare-DATA decoder conclusion additionally needs the separately verified forest-prefix support bound: on M1<=beta N, the active physical forest prefix acts only on at most r_R beta N DATA sites. It also needs the accepted canonical DATA-radius tail/common-span recovery theorem and a common positive good branch. The canonical basin/count projectors and BUSY projectors commute in forest coordinates, so there is no need for the two PROOF OBSERVABLES themselves to commute. This corollary does not by itself construct a physical quantum output coupling, a noisy gate, or an active-controller handoff. Destructive readout or a shutoff ramp still needs its own already stated interface conditions.

The use of full-Hilbert X_h, the full-catalog masks, the exact native drift, and the relative noise estimate are mathematical deductions from the frozen accepted inputs, not a numerical device simulation. Accepted retirement/readout sources remain valid fallbacks and are not edited.

## 8. Independent check of the original dirty-credit mask question
Although not needed above, the proposed no-jump concern has a stronger exact resolution for the actual T_B. Ready_h is always history-good, so B_h<=P_h. Since S_h-I is supported in B_h, S_h commutes P_h. For j!=h, the monitored owner algebra is nontrivial only within h's o/z block and scalar on all other labels; it commutes j's own-tag predicates and does not touch j's private variables. Hence [S_h,P_j]=0 for every j.

The weighted erasure Kraus E_h,a sqrt(I-S_h) has source in B_h, hence in BUSY_h, and target Q0,W0, which remains BUSY_h (Ready requires A0). It preserves all other BUSY_j. The no-jump and erasure Kraus therefore commute every P_j. Since T_B is unital, every P_j and the entire joint BUSY algebra are in its multiplicative domain and are fixed EXACTLY. Thus any valid history-weighted lower bound could be pulled through T_B with no survival loss. This confirms the mask assertion but does not replace the direct construction above with an unreviewed dirty drift.
