# A signed core predictor can certify a quantum service without fitting the environment

28 October 2026. **Root construction, independent receiving pending.** Alternative to the physical-realization/CP-suffix route. This first version uses a certified FULL memory core, not a noisy rank-truncation inference. It does not require a CP model of hidden memory or a semialgebraic hidden-model search. Its intermediate predictions may be nonpositive. The final accessible service and decoder are made physical separately.

## 1. Physical and acquisition contract

Use the stationary finite-memory quantum input/output port of IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md, with supplied memory dimension upper bound d, independent paid whole-process starts, actual ordinary informationally complete (IC) input preparations rho_(a,u) and output effects E_(a,v), and classically selected native actions a. A native instrument maps M A_a to M B_a, with classical outcome o. Known caller-local CP operations may retain quantum registers, entangle/recycle inputs and use classical feedback. No coherent superposition of distinct native action labels is inferred. Current and future source calls use the SAME stationary instrument. The hidden memory is never directly measured or controlled.

Let r=d^2. Select r subnormalized physical branch-prefix states tau_j and r physical future effects F_i (0<=F_i<=I), including empty prefix j=1 and empty future i=1. Prefixes and future tests are actual ordinary IC words, not conditional-state oracles. The raw tables are

    H_ij=Tr(F_i tau_j),
    H_z,ij=Tr[F_i Phi_z(tau_j)],
    z=(a,u,o,v),
    Phi_z(sigma)=Tr_B[(I tensor E_(a,v)) V_(a,o)(sigma tensor rho_(a,u))].

The first trace row is m_j=H_(1,j), and tau_1=rho_initial, m_1=1. Every prefix mass is <=1. Assume simultaneous entrywise confidence bands |H-Hhat|<=D_H and |H_z-Hhat_z|<=D_z, acquired by ordinary raw joint-event counts including all failed prefixes. All empirical trace-row entries lie in [0,1], with Hhat_(1,1)=1 fixed exactly.

The algorithm accepts a core only if Hhat is invertible and the rational interval-inverse test below passes. On the confidence event this makes H truly invertible. Since actual memory dimension is at most d and the core has rank d^2, its tau_j span the entire Hermitian memory space. A lower-rank source can legitimately fail this full-core test forever. No smaller noisy minor is promoted to a complete core in this theorem.

A finite exhaustive search can use all prefix/future IC words of length <=d^2-1. The span-stabilization argument gives a full core whenever the actual memory process is fully reachable and observable in this interface. Shifted words have length <=2d^2-1. The word pool can be exponentially large in d^2. Nonsingularity, physical promise and conditioning remain real restrictions, even though a numerical core bound is acquired rather than supplied.

## 2. Completely bounded coordinate maps

For a memory operator, including one correlated with an arbitrary caller register R, define

    Pi_j(X_MR)=sum_i (H^-1)_(j,i) Tr_M[(F_i tensor I_R)X],
    Lambda(x_1,...,x_r)=sum_j tau_j tensor x_j.

On r-tuples of Hermitian caller operators use ||x||_Sigma=sum_j||x_j||_1, uniformly over all reference dimensions. The maps Tr_M[(F_i tensor I) .] are CP contractions in trace norm on Hermitian operators: sandwich with sqrt(F_i) before the partial trace. Since Tr tau_j<=1,

    ||Lambda||_(Sigma->1),cb <=1,
    ||Pi||_(1->Sigma),cb <=K,
    K=max(1,sum_(j,i)|(H^-1)_(j,i)|).                 (1)

The bound is valid for arbitrary Hermitian X, not only positive occupied states. Moreover Pi Lambda=id and Lambda Pi=id on the full memory operator space. The second equality is where the FULL core is used; it must not be asserted from an arbitrary lower-rank minor.

For ANY complete physical source/controller segment P, its exact predictive-coordinate representation is Pi P Lambda. Hence

    ||T_segment||_(Sigma->Sigma),cb <=K              (2)

independently of segment length, even when memory is correlated with quantum feedback registers. The complete physical segment is CPTP, and its trace norm on Hermitian inputs contracts; no positivity of the tuple Lambda(x) is assumed. A zero-length coordinate identity has norm one<=K. Controller-only operations act identically on each coordinate and have norm at most one. This uniform segment bound is the stability property that naive multiplication of one-step matrix norms discards.

## 3. Complete one-step quantum transfer from the ordinary IC alphabet

Let D_(a,u) be the Hermitian input dual basis, so X_A=sum_u rho_(a,u)Tr(D_(a,u)X). Let B_(a,v) be Hermitian output dual matrices for an independent IC subset of the actual output effects, so Y_B=sum_v B_(a,v)Tr(E_(a,v)Y). All dual matrices are known from the actual preparations/readouts; their conditioning is paid.

Set C_z=H^-1 H_z. For a tuple whose components x_j act on the current accessible input A and the remaining caller register R, the native quantum transfer is explicitly

    y_(i,o)=sum_(j,u,v) C_(a,u,o,v)[i,j]
          B_(a,v) tensor Tr_A[(D_(a,u) tensor I_R)x_j]. (3)

Native o is retained as a classical block. This is a linear identity on full operators and their reference extensions, obtained by IC expansion of input and output matrix entries. It does not promote a classical-only measurement alphabet to coherent access: both actual IC preparation and IC output readout are essential.

Estimate C by Chat_z=Hhat^-1 Hhat_z. Let U=Hhat^-1 and A=|U|D_H. Require ||A||_infinity<1 and compute

    M=(I-A)^-1 |U|,
    E_z=M[D_z+D_H |Chat_z|].                          (4)

A Neumann-series comparison gives |H^-1|<=M and |C_z-Chat_z|<=E_z on the common confidence event. Take the known rational bound K=max(1,sum M_ji) in all subsequent formulas.

The partial functional defined by D has completely bounded trace norm ||D||op; tensoring B multiplies it by ||B||1. Thus the induced one-step complete coordinate error is at most

    delta=max_a max_j sum_(o,u,v,i)
          ||D_(a,u)||op ||B_(a,v)||1 E_(a,u,o,v)[i,j]. (5)

Certified rational upper bounds for the known dual norms suffice. Classical adaptive choice of a costs a maximum, not a sum over possible schedules: the controller first produces a classical action register, whose block trace norm is the sum of its branches. Native outcome records, entangled inputs and coherent output recycling are retained by (3). No tensor-power-in-horizon IC condition number appears.

## 4. Discrete perturbation expansion instead of physical intermediate predictions

Fix ANY allowed physical caller/controller with at most H native calls. It may be selected using the entire calibration record. Keep every branch unnormalized: never feed normalized negative predictions into a nonlinear decision rule. A classical policy is a known record-controlled CP operation, even when selected offline from the counts.

Replace each exact transfer T_t by its signed estimate That_t=T_t+E_t, where ||E_t||<=delta. Expanding the product by the positions of the m perturbations, each term has m perturbations and at most m+1 exact contiguous segments. By (2),

    ||That_H ... That_1-T_H ... T_1||_Sigma,cb
       <=sum_(m=1)^H choose(H,m) K^(m+1)delta^m
       =K[(1+K delta)^H-1].                          (6)

All interleaved physical controls are included in the contiguous segments; this proof does not commute errors through quantum feedback. It is a uniform bound for every such controller. The looser estimate <=H K^2 delta exp(HKdelta) is sometimes convenient, but the exact rational power in (6) is directly certifiable.

The initial tuple is e_1 tensor the caller input state, with norm one, because the first core prefix is empty. There is no additional unknown initial-state factor. At the final end apply the empirical trace row mhat=Hhat_(1,:), rather than secretly setting every prefix mass to one. Its coordinate functional has norm at most one since 0<=mhat_j<=1. Let delta_m=max_j D_H,(1,j). The true final coordinate tuple has norm <=K. Therefore the signed predicted accessible map Nhat for the chosen complete service obeys

    half ||Nhat-N_true||_diamond <= eta_core,
    eta_core=(K/2){delta_m+[(1+Kdelta)^H-1]}.          (7)

This is a Hermiticity-preserving-map bound, with all accessible classical records included. Nhat need NOT be CP or TP, so eta_core must NOT be clipped at one before physical projection. The raw trace-row debit is essential, as in the already received raw-joint-core example. Initially the payload/reference is product with source memory; alternatively use the enlarged input domain explicitly.

## 5. Physical service projection and full-CPTP recovery

For a fixed service with finite accessible output Y and payload dimension p, compute its signed Choi matrix Jhat by the transfer representation (3). This uses the actual known controller circuit; there is no hidden-memory physical realization or generic semialgebraic search. A forward-only prefix and exactly one payload USE with a small output is a particularly direct instance. General controllers may have exponentially large record/memory representations; those costs are not suppressed.

Project Nhat to a physical channel Ntilde by minimizing half diamond distance over J>=0, Tr_Y J=I_p. A certified optimization slack xi means

    half ||Ntilde-Nhat||_diamond
       <= inf_(N CPTP) half ||N-Nhat||_diamond +xi.

The actual N_true is feasible, so on the confidence event

    half ||Ntilde-N_true||_diamond <=2 eta_core+xi.    (8)

This projects only an ACCESSIBLE service channel, not a hidden source state or process realization. Then choose a physical decoder Rhat with certified slack zeta for Ntilde over ALL CPTP maps Y->L. Triangle inequality and contractivity give

    e_true(Rhat) <= inf_(R CPTP)e_true(R)
                          +4 eta_core+2xi+zeta,       (9)
    e_true(R)=half ||R N_true-id_L||_diamond.

Both optimizations are explicit finite diamond-norm SDPs on known accessible Choi matrices, not a supplied decoder menu. The Hermitian diamond dual uses Z>=J_Delta, Z>=-J_Delta and Tr_output Z<=tI; minimizing t/2 gives the objective. Unlike hidden physical realization, these are convex SDPs. No new norm-SDP identity is claimed.

An actual implementation must use a certified finite SDP procedure and a finite decoder synthesis interface, not trust an approximate optimizer's nominal Choi matrix. One standard route is weak rational optimization with an explicitly strictly feasible depolarizing Choi center and an oversized positive Z,t epigraph center. Their dimensions, norms and interior radii are known from Jhat, so the optimization and separation costs are charged. If an approximate output C has eigenvalues >=-a and ||Tr_out C-I||op<=a, shift C1=C+aI and set P=Tr_out C1. For sufficiently small declared a, P is positive with a known gap, and

    C2=(P^-1/2 tensor I) C1 (P^-1/2 tensor I)

is EXACTLY positive and TP. Known finite matrix arithmetic controls its trace-norm/diamond displacement by a dimension-dependent constant times a. Allocate this displacement inside xi or zeta, extract Kraus operators from C2, and compile the resulting Stinespring isometry to a separately paid complete-norm tolerance. This paragraph is an implementation obligation with an explicit repair mechanism, not a claim that a production optimizer/compiler was executed. A complete polynomial bit-complexity bound for a chosen solver and gate set is still to be instantiated in a successor; it is not inferred merely from convexity.

## 6. Finite acquisition, abstention and actual record accounting

A caller funds a finite joint-event count cap, or a declared finite series of stages with a summable confidence allocation. At each stage, acquire the finite raw IC word pool, search the finite full-core minors, and compute (4)-(7). Declare ACCEPT only when the inverse test passes and eta_core is below the chosen target; otherwise return UNKNOWN/ABSTAIN within the cap. On the simultaneous confidence event, every accepted core and controller selected from it is sound. Failure to pass is not a claim that no recovery exists.

For a fixed actual full core, confidence widths tend to zero, K stays bounded, and delta and delta_m tend to zero. Hence any fixed finite H,target eventually passes with enough independent starts. Near-singular cores can demand arbitrarily many calls. Every raw event pays its whole start and every attempted prefix, including failure branches; maximum core/shift episode depth is2d^2-1. Input/output dual conditioning, finite matrix inversion, H-step signed arithmetic, final accessible Choi dimension, SDP/synthesis precision, memory, routing, resets and native calls all remain in the cost bill. This is not a dimension-free or automatically efficient source learner.

A calibrated record-law discrepancy and an actual end-to-end deployed-channel implementation allowance must be distinguished. Statistical confidence bounds (7)-(9) concern record-conditioned nominal selected maps on the good event. After averaging, the bad-event probability costs at most beta because the final projected service/decoder is physical on every record (including declared fallback). A single end-to-end diamond debit transfers the ACTUAL RECORD-AVERAGED deployed channel guarantee, not automatically the expectation of record-conditioned diamond distances. Capped optimizer UNKNOWN histories require their own abort/fallback accounting; they are not hidden inside the sampling failure beta.

## Scope and next obligation

The checked target here is a full-core, complete-controller perturbation mechanism and service-only physical projection. No lower-rank extension, physically realizable hidden simulator, infinite-horizon guarantee, environment tomography, practical advantage or novelty is inferred. Its intended benefit is to replace exponentially unstable signed prediction and hidden-model feasibility search by a paid stable finite-service calculation. The physical CP-suffix residual route remains distinct and may give sharper constants when a physical candidate is actually available. The load-bearing coordinate/product norm proofs, empirical error certificate, physical projection and numerical realization require independent receiving. Efficient finite SDP/compiler accounting remains explicitly unfinished.
