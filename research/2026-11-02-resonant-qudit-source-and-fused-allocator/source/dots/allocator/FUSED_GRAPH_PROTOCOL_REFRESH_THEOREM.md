# Fused physical allocator: explicit generator and uniform refresh theorem

2026-11-01, independent constructor reconciliation. This file supersedes the separate-controller stopping-time argument, without modifying the frozen independent derivation. Root supplied the native completion theorem and fused-state simplification. This proof uses the ideal specified GKSL generator; arbitrary coherent physical imperfections are to be added as local generator perturbations by the parent's positive-corrector compiler, not assumed classical fault sets.

## 1. Hilbert space and all physical transitions

Let the conflict graph have maximum degree D. An edge must connect every pair whose simultaneous partial native operations can spoil either report. Local edge order is arbitrary; no global ordering or coloring is needed. Each edge uv has a physical qutrit with states 0,u,v.

At check v of weight w, ONE apparatus qudit has:
* CLEAN_j,c, j=0,...,D, c=±1: 2(D+1) states;
* WAIT,c: 2 states;
* COLLECT_j,c, j=0,...,D: 2(D+1) states;
* native g_j,b,c and e_j,b,c, j=1,...,w, b=0,1: 8w states;
* native f,b,c: 4 states.
Total dimension exactly 8w+4D+10. Lower-degree vertices pad the scan with onsite steps. Active quantum and classical controller phases cannot coexist: they are orthogonal subspaces, not separate tensor registers. Cache Z has eigenvalue c in every state.

For j<D and the next incident edge vu, at rate g:
* CLEAN_j,c ⊗ |v> -> CLEAN_{j+1},c ⊗ |0>;
* CLEAN_j,c ⊗ |a> -> CLEAN_{j+1},c ⊗ |a>, a=0,u;
* COLLECT_j,c ⊗ |a> -> COLLECT_{j+1},c ⊗ |v>, a=0,v;
* COLLECT_j,c ⊗ |u> -> CLEAN_0,c ⊗ |u>.
Each is a rank-one two-apparatus GKSL jump; channels distinguish source phases/cache values. The free-or-already-self collection branch also makes arbitrary initial lock states legal. CLEAN_D,c -> WAIT,c is onsite at rate g. WAIT,c -> COLLECT_0,c is onsite at rate νg. COLLECT_D,c -> g_1,σ_X,c uses the native finite-purity preparation, total rate g, probabilities 1-p and p. All these preserve c.

The native two-body apparatus-data Hamiltonians and coherent-preserving onsite stage decays are unchanged. Replace final native readout by
 L_read,s,c = sqrt(γ) |CLEAN_0,s><f,s_X,c|.
It simultaneously completes readout, writes physical cache s, and starts cleanup. There is no separate DONE state, no free instantaneous reset, and no partial-probe reset or pause. No lock wait occurs during a native quantum job. All intended rates are fixed multiples of g; ν does not tend to zero to obtain accuracy.

Classical phase/lock/cache-diagonal observable blocks are invariant under these source transitions; native g/e coherences remain fully quantum. The separate rank-one source-phase jumps prevent arbitrary initial off-block coherence from affecting these block observables. Native completion applies to arbitrary within-stage coherence and environment entanglement.

Resource charge: O(D) finite apparatus levels plus D/2 edge qutrits per check, pairwise dissipative apparatus-edge transitions, native two-body data couplings, finite-purity phase reference/preparation, coherent b-indistinguishable decay channels, readout/cache entropy disposal, and every local level/lock/cache/reservoir error. These edge transitions are two-site CLASSICAL GKSL primitives, not onsite reservoirs. No laboratory realization is implied by writing the generator.

## 2. Native premise and notation

Use parent's proven conditional active-cycle bound, including final readout:
 E[e^{θ τ_A} | arbitrary past and active state] <= M_A(θ),
 S_A(t)=min(1,M_A(θ)e^{-θt}), τbar_A=integral S_A(t)dt.
It is uniform in graph size and arbitrary neighboring quantum dynamics with bounded incident commutator. Choose θ also below g and νg. This is a conditional future bound, not independence of native completion clocks.

## 3. Correct local regeneration stopping time

R_v is the first completion of an ENTIRE scan CLEAN_0 -> ... -> CLEAN_D -> WAIT. If initially CLEAN_j with j>0, finishing that partial scan does NOT count: the process must first reach CLEAN_0 and then execute the whole scan. Fusion ensures no native probe is active during this scan.

From any initial phase, reaching R_v takes at most 3(D+1) rate-g classical steps, one rate-νg WAIT delay, and one native active cycle, in conditional stochastic domination. This allows an initial partial cleanup, a full collection/preparation or abort, and a subsequent complete cleanup. Hence
 M_R(θ) = [g/(g-θ)]^{3(D+1)} [νg/(νg-θ)] M_A(θ)
 bounds E[e^{θ R_v}], and S_R(t)=min(1,M_R e^{-θt}) bounds P(R_v>t). Loose overcounting is intentional. Busy collection immediately aborts; cleanup never waits for another owner. Neither outside locks nor graph size enter this bound.

After R_v every new launch by v has genuinely acquired every incident lock. While v is native-active, these locks remain v: another endpoint only acquires 0 or its own value, and only releases its own value. Thus even a distant or neighboring unrepaired controller cannot STEAL v's occupied lock. Before its own R_u a neighbor can nevertheless launch without having collected that edge. Therefore target v is guaranteed collision-free for each cycle launched after max_{u in N[v]} R_u. No global n-vertex flush is needed.

A cycle launched earlier may remain contaminated despite valid lock ownership. For deterministic B, put t0=B/2. With m=|N[v]|<=D+1,
 S_burn(B) = min(1, m S_R(B/2) + S_A(B/2))
 bounds the event that some local R_u>t0 OR the target cycle active at t0 remains incomplete at B. On the complementary event, every target cycle still active at B or launched later is a freshly prepared isolated cycle. Target cache can still be stale; this statement concerns current/future reports. Neighbor cycles may be corrupted by unrepaired vertices outside N[v], but cannot overlap v while correctly owning/releasing their mutual edge. That is why the proof is pointwise local.

## 4. Explicit non-dilute fresh-service word

After the local regeneration event, let an arbitrary observation interval start. Suppress all dominating WAIT-attempt Poisson clocks in N[v] for L time. Each initially collecting/active/releasing vertex finishes its existing attempt/job, releases owned locks, and reaches WAIT. No new attempt starts. A conditional drain moment bound is
 M_Q(θ)=[g/(g-θ)]^{2D+2} M_A(θ).
Choose L so m M_Q e^{-θL}<=1/2. Conditional on suppressing the dominating clocks, the drain succeeds with probability >=1/2: use the modified generator with those attempt channels removed, whose native completion bound remains valid. This is not illicit conditioning of the completion theorem on an arbitrary future measurement record.

Next choose an attempt window h=1/(νg). Require exactly one target dominating attempt event in this h window and no other dominating attempts in N[v] throughout the full interval. After this target event, permit W time for collection/preparation/native completion. A fresh completion moment bound is
 M_F(θ)=[g/(g-θ)]^{D+1} M_A(θ).
Choose W so M_F e^{-θW}<=1/2. Put Δ=L+h+W. A post-interval-start target attempt completes a report with conditional probability at least
 q=(νg h/4) exp[-m νg Δ] > 0.
The bound is uniform over all valid initial controller phases, cache values, and quantum states. Its constants depend only on D,w and fixed local rate ratios. This is a conservative service certificate, not a practical numerical throughput estimate; q may be very pessimistic. It does NOT require lowering ν as p or physical perturbations decrease.

On k consecutive intervals, conditional failure probabilities give
 P(no completed cycle from a post-B target attempt by B+kΔ | burn success) <=(1-q)^k.
A completed fresh cycle need not be the last write; subsequent isolated cycles are also correct if their preparation marks are good.

## 5. Uniform cache mismatch operator bound

Let e_v=(1-Z_cache,v S_tilde,v)/2. Dressed stabilizer sectors are invariant under every ideal source/controller term; all controller phases have trivial prefix dressing. Let T=B+kΔ. Attach a latent independent preparation-error mark of probability p to every target WAIT attempt, reveal it only if that attempt reaches preparation. This is exactly the native preparation mixture because the mark cannot affect preceding collection/abort dynamics. Its use is for a union bound, not an assumption of reliable physical classical records.

If burn succeeds, a post-B attempt completes, and no post-B target attempt has a bad mark, then the final cache at T is correct. Any pre-B pending report necessarily occurs before the completed post-B cycle and is overwritten. The expected number of marked post-B attempts is at most p νg(T-B), because the dominating attempt clock has rate νg. Therefore for EVERY initial global state,
 e^{T L_ideal*} e_v <= [S_burn(B)+(1-q)^k+p νg(T-B)] I.
For grid times, (1-q)^k=exp[-c(T-B)] with c=-log(1-q)/Δ. For arbitrary T use k=floor((T-B)/Δ), or retain the harmless exponential prefactor. No last-report independence is asserted.

Choose fixed B and k large enough to make the first two terms less than a desired constant admission budget, then choose fixed preparation impurity p below the remaining budget/[νg kΔ]. Constants are independent of memory size. This establishes arbitrarily small fixed admitted error by apparatus quality, without rate dilution or dimension growth. It does not promise arbitrarily vanishing error at fixed p.

## 6. Bad-report readiness, separately from cached error

Define
 d_v=Π_final,v (1-X_probe,v Sbar_v)/2,
where Sbar_v is the appropriate dressed target label with the target's final-phase dressing trivial. It is a positive projector indicating that an imminent native readout would report the wrong protected sign. In final phase it commutes with cache mismatch e_v. The write hazard is γΠ_final, but only γd_v is bad-report hazard. A high service rate must NOT be paid as if every cache write were an error.

After the burn event, current target native jobs are isolated fresh cycles. A correctly prepared cycle has exactly zero d_v, including its final-state quantum coherences, by the native parity instrument. A bad-prepared current job must originate at an actual bad preparation jump. Such jumps have intensity at most pg. Conditional on any such jump at time s, its active survival to t is at most S_A(t-s), uniformly for both preparation signs and any state. Counting all bad preparations, even ones that later abort their contribution by completion, gives
 P(current job originated from bad preparation at t) <= pg integral_0^t S_A(t-s) ds <= pg τbar_A.
This uses conditional survival bounds and compensators, not a stationary or independent-clocks approximation. Initial arbitrary active states are covered by burn failure, not assigned a favorable preparation distribution. Consequently the all-state operator bound is
 e^{t L_ideal*} d_v <= [S_burn(t)+pg τbar_A] I.
Thus after choosing a fixed burn target ε_d, q_d<=ε_d+pgτbar_A. Unlike cache e_v, readiness d_v needs no rare fresh-service word. As t increases, limsup all-state readiness is at most pgτbar_A=O(p), with fixed microscopic ratios. A sharper constant may follow from the isolated timing law, but is unnecessary and not claimed.

This bound furnishes the root's separate positive corrector H_d and permits cancellation of good-write variation: for G=e(1-d)Π_final and Bflip=(1-e)d, L_source*e=γ(Bflip-G). Only the residual bad-report readiness cost needs admission. Physical controller faults remain separately priced local generator perturbations of the correctors; no classical local-stochastic reduction is assumed here.

## 7. What is and is not established

Established under the explicit native completion premise: a finite physical bounded-degree allocator, local self-stabilization from every apparatus/lock state, no partial-job reset, no infinite lock wait, positive graph-size-independent useful service at fixed ν, uniform all-state cache refresh and bad-report readiness bounds, and explicit noise/resource accounting interfaces.

Not established here: a tight general-graph throughput constant, a physical reservoir-engineering implementation, or the full protected-memory lifetime theorem. The exact two-probe benchmark supplied by root (η=.001 token error .000659917 and rate .0668601 versus augmented random r=.1 error .0639995 and rate .0603015) materially supports the mechanism but is not a general-graph numerical certificate. Same-hardware timed extraction must receive these same locks, qudit levels, phase references, baths and noise charges; autonomy alone does not establish superiority over that comparator.

### Technical clarification: graphical attempt clocks and coherence
The dominating Poisson-clock representation is used on the invariant phase/lock/cache-block-diagonal observable algebra. For these observables, one may dephase the initial phase/lock labels without changing expectations, and ordinary classical phase transition uniformization is exact. It is not a claim that the full off-diagonal GKSL attempt channel equals an arbitrarily chosen projective Poisson channel; those can have different off-diagonal dephasing rates. Native within-stage quantum coherences are retained and covered by M_A. Thus the quiet-clock good word and latent preparation marks establish all-state operator inequalities through block closure, without physically inserting a free dephasing step.

## 8. Verified revision: non-exponential-degree service certificate

Revision 2026-11-01 18:24 UTC. Root proposed the parameter choice below; constructor independently verified it. Sections 1–7 and their conservative parameter choice are preserved. The pre-revision file is `FUSED_GRAPH_PROTOCOL_REFRESH_THEOREM.pre_polynomial_service_20261101T1823.md`, SHA-256 `65010d08ec93b9af62ab6ec748ce581830f795d86a3d5cf694d4fb83c9609de6`. This section supplies the preferred service constants, replacing only Section 4's optional choices of h,L,W and the unnecessary common θ restriction.

Choose θ0>0 below g and within the native M_A moment domain, INDEPENDENT of the attempt rate. Define
 M_Q0=[g/(g-θ0)]^(2D+2) M_A(θ0),
 M_F0=[g/(g-θ0)]^(D+1) M_A(θ0),
 m=D+1,
 F=max{log(2m M_Q0)/θ0, log(2 M_F0)/θ0}.
(The first term dominates with these uniform bounds, but retaining both is harmless.) Set ONCE, as a function only of hardware degree and native response constants,
 λ=νg=1/(6mF), L=F, h=F, W=F, Δ=3F.
No target error tolerance, preparation impurity, or physical perturbation parameter occurs in this choice.

The no-attempt drain over F succeeds with probability >=1/2 because m M_Q0 exp(-θ0F)<=1/2. After the target's unique attempt in the middle F window, it has at least the final F window left for collection/preparation/readout; this succeeds with conditional probability >=1/2 because M_F0 exp(-θ0F)<=1/2. Exactly one target dominating event in the middle window and no other dominating events in the entire closed neighborhood over 3F has probability
 λF exp(-3mλF) = exp(-1/2)/(6m).
Therefore the same good-word argument gives EXACT conservative constants
 q=exp(-1/2)/(24m),
 service rate lower bound q/Δ=exp(-1/2)/(72mF),
 c=-log(1-q)/(3F) >= exp(-1/2)/(72mF).
Use q and Δ in Section 5's cache-refresh inequality unchanged. Because each successful disjoint word contains a completed report, q/Δ is a lower bound on long-time mean completed-report service, not merely an inverse waiting-time notation.

Regeneration DOES include a WAIT delay, unlike drain/fresh service. Consequently use a SEPARATE exponent
 θ_R=min{θ0,λ/2},
 M_R(θ_R)=[g/(g-θ_R)]^(3(D+1)) [λ/(λ-θ_R)] M_A(θ_R),
 S_R(t)=min{1,M_R(θ_R)exp(-θ_Rt)}.
Use the original native S_A (it may use θ0) in S_burn(B)=min{1,m S_R(B/2)+S_A(B/2)}. No circular requirement θ0<λ is introduced. The readiness estimate still uses pg τbar_A and is unchanged.

Polynomial-degree interpretation: F=(1/θ0) max{log(2m)+(2D+2)log[g/(g-θ0)]+log M_A(θ0), log2+(D+1)log[g/(g-θ0)]+log M_A(θ0)}. Thus if θ0^-1 and log M_A(θ0) are polynomial in bounded native length/incident degree at fixed rate ratios, so are F and inverse certified service 72mF exp(1/2). For the supplied native observability bound, take θ0<=min{g/2,γ/2,-log(1-p_stage)/(2T_stage)}. Then the geometric-stage moment factor is at most 1+1/sqrt(1-p_stage), final readout factor is at most 2, and log M_A(θ0)<=w log[1+1/sqrt(1-p_stage)]+log2. The supplied inverse stage-completion probability/time scales are polynomial in the incident bound B/g, so this choice yields polynomial degree/length cost, not exp(D).

This is NOT accuracy dilution: λ is fixed by local hardware once, remains positive and independent of p/desired admission accuracy, and service stays fixed as those error parameters are reduced. It is legitimate degree/response-time matching. The earlier h=1/λ certificate suppressed D neighbors for an unnecessarily long target mean-attempt time and lost an exp(D) factor; that loss was an artifact of the proof's parameter choice, not an intrinsic feature of the allocator.
