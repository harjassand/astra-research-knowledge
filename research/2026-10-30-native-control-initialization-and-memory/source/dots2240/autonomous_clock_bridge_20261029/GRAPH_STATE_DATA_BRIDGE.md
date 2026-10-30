# From healthy controllers to an actual quantum resource state

2026-10-29. Root new construction, pending independent review. This aims at a complete noisy quantum-state factory rather than another controller-only certificate. It is not yet a received factory theorem, and is not an autonomous-memory threshold.

## Actual target and ordinary comparator

For a bounded-degree graph let S_y=X_y product_(z~y) Z_z be its graph-state stabilizers. They commute and have a unique common +1 state. Define P_y±=(I±S_y)/2 and the local recovery map

    Phi_y(rho)=P_y+ rho P_y+ + Z_y P_y- rho P_y- Z_y.

This map clears its own syndrome defect d_y=(I−S_y)/2 and preserves every other syndrome. Ideal dissipative graph-state preparation is established prior machinery, not our invention. The intended missing interface is robustness when those maps are implemented by actual finite-rate, imperfect coherent controllers rather than supplied ideal many-body dissipative jumps.

Implement these rank-two maps using the GUARDED_CHANNEL_CLOCK Hamiltonian and one-body resets. Fix uniform positive constants g_x=g>0 and kappa_x=kappa>0 independent of volume and runtime (or explicitly supply volume-uniform lower and upper bounds). Positivity separately in each finite instance is not enough for size-uniform conclusions. Additional local noise terms are Hermiticity-preserving, adjoint identity-annihilating, and bounded on the actual retained-bath support; Hamiltonian/Lindblad terms and their physical differences satisfy the Hermiticity condition, arbitrary complex decompositions need not. This version still uses bounded-range many-body guards. The two-site lease compiler is a different architecture and is not automatically certified here.

## Whole-space dressing, including controller defects

Choose the excited-sector Stinespring unitary for each map. One explicit two-by-two block completion is

    U_exc,y = [[P_y+, P_y-], [Z_y P_y-, -Z_y P_y+]].

It maps data tensor good excited label1 to K0 data tensor1 + K1 data tensor2. Extend by identity on ready label0 and guard by every overlapping controller being ready. These guarded unitaries commute. Their product U is finite depth and local at bounded graph degree.

The stronger identity is valid on the WHOLE physical Hilbert space:

    U* H U = I_data tensor H_clock,

where the clock Hamiltonian only toggles ready0 and good excited1, with the original occupancy guards. Bad excited labels do not participate. A neighboring dressing is identity whenever a term H_x can act, because that neighbor's own clock is ready; nonneighbor dressings commute by locality. Thus only the dressing at x transforms H_x.

In this frame the bad-controller projectors B_x are clock-only commuting projectors: an isolated excited label2 is bad, and any adjacent occupied clocks are bad. Their full-space no-creation/product decay remains as established earlier.

A transformed reset U* L_xs U is supported on the data boxes and controller neighborhoods near x. If all controller flags in the relevant neighborhood are good, it is the intended K_xs data action and a clock removal. Otherwise it can cause arbitrary data damage, but only in that fixed neighborhood. No claim is made that clearing a clock flag repairs that data damage.

## Combined data/controller flags

An explicit choice is R_y=the radius-two ball about y in the UPDATE-OVERLAP graph (whose edges mean the data boxes overlap). Indeed U* L_xs U can affect data only in the union of boxes z in the closed neighborhood of x: only U_x and its neighbors fail to commute with reset x. This union overlaps the stabilizer box y only if dist_overlap(x,y)<=2. Moreover, on B_x=0 a nonzero reset has x in good excited label1 with every adjacent controller ready; all neighboring dressings are then identity, and the reset is exactly K_xs. Thus only B_x itself is needed to qualify that reset. Radius two includes every potentially damaging reset center. |R_y|<=(D+1)^3 is a safe volume-independent bound. Clock support of the dressed reset may extend to radius two around x, but that does not enlarge its DATA support or the stated qualification.

In the dressed frame define

    A_y = I - (I-d_y) product_(z in R_y)(I-B_z).

All A_y commute: data stabilizers commute, all B are clock-only commuting projectors, and the two families act on different factors. Conjugate them by U for physical observables.

Claim: clean dynamics never creates A_y, so L_clean*(A_y)<=0. H_clock commutes with A_y. A reset far from S_y cannot affect it. A reset near S_y, on the A_y=0 subspace, has every relevant controller good and therefore performs the intended graph-state correction, which cannot create any syndrome. Bad-controller flags are themselves never created. Thus A_y L_xs(I−A_y)=0. The total no-jump loss sum_s L_xs*L_xs=kappa Q_x commutes with A_y, giving the explicit negative Gram decomposition

    L_clean*(A_y) = -sum_(x,s) A_y L_xs* (I−A_y) L_xs A_y <=0.

This argument must be checked with a precise support choice R_y; it is not an assertion that arbitrary recovery channels have monotone data defects.

## Uniform finite-time healing: proposed proof

From any initial state, the probability of any bad controller in R_y after time t1 is at most |R_y| exp(-kappa_min t1). These flags cannot reappear under clean dynamics. Choose t1 so this is <=eta=c²/16, where c is the full-space probability lower bound for at least one recorded reset at y during a subsequent interval t2.

Let P be the joint good-controller projector at t1 and sigma=P rho P. Gentle projection gives ||rho-sigma||_1<=2sqrt(eta). Do NOT treat unmeasured good/bad clock sectors as an automatically classical event. On the subnormalized sigma branch, all relevant flags stay good, and a subsequent y reset is an intended Phi_y that clears d_y. Later clean operations cannot recreate it. The full-space progress bound applies to this branch, so its final bad probability is at most1-c. CPTP contractivity adds at most2sqrt(eta)<=c/2 for the removed coherences. Hence

    exp((t1+t2)L_clean*) A_y <= (1-c/2) A_y.

The final relative-to-A_y order uses the no-creation invariant corner: the evolved observable is supported on A_y, so its uniform norm bound is an order bound inside that corner.

This is a finite-time local healing certificate independent of system size, without assuming a globally mixing quantum data process. It does NOT yet satisfy the small-time delta C0<1 condition used in LOCAL_REPAIR_TO_SPARSE_DEFECTS.md. A justified finite-time-to-local-polynomial construction is still needed; do not skip it.

One proposed route is to split the fixed healing time into short intervals and approximate both the semigroup and its integral by local Taylor polynomials. Choosing Q_j(z)=sum_(k=0)^m_j (delta z)^k/k! and R_j(z)=(Q_j(z)-1)/z preserves the exact telescoping identity L*F=Q_M(L*)...Q_1(L*)A_y−A_y. Every term remains A_y-supported, so truncation bounds are relative. Support/precision may grow badly with the fixed local healing time, but must remain independent of total volume. This step and the support-count constants require review.

## Exact finite regression

check_graph_state_factory.py constructs two graph-state stabilizers XZ and ZX, their actual rank-two recovery maps, and two overlapping three-level controllers (36-dimensional physical model). Exact rational arithmetic verifies: local dressing unitarity and commutation; full-space clock-only Hamiltonian; commuting combined flags; every jump's no-creation property; and the exact negative Gram identity. No floating positivity test is used.

The regression supports the interface, not the general noisy-factory theorem. Even a completed factory theorem would still need resource-state decoding/readout, actual pump/reset energy, and a careful comparison with standard dissipative graph-state preparation. Arbitrary unknown-data quantum memory and universal fault-tolerant computation are separate harder consequences.

## Root correction during derivation

The initial healing sketch used a classical union bound across an unmeasured clock projector. It is replaced above by gentle projection with eta=c²/16. This explicitly charges possible good/bad-sector coherences. No measurement of the flag is added to the physical protocol.

## Proposed noisy-factory consequence after the finite-time repair lemma

The arbitrary-finite-time extension in LOCAL_REPAIR_TO_SPARSE_DEFECTS.md now supplies a finite-support positive F_y with a0 A_y<=F_y<=b0 A_y and L_clean*F_y<=-r F_y, pending independent review. Pack its supports so local perturbation terms touch at most one factor. Normalize Z_y=F_y/b0, K=b0/a0, and let eta_R be the actual total noise norm touching one such support. For arbitrary initial system–bath state, comparison yields

    Tr[product_(y in U) Z_y rho(t)] <=q(t)^|U|,
    q(t)=exp(-rt)+(eta_R/r)(1-exp(-rt))

on every packed set U. Since A_y commute, every set S then obeys

    Tr[product_(y in S) A_y rho(t)] <=p(t)^|S|,
    p(t)=[K q(t)]^(1/P), whenever K q(t)<1,

where P is the fixed packing loss. The actual graph-state syndrome defect d_y in the dressed frame is bounded by A_y. Hence this would be a size- and runtime-uniform sparse DATA-defect guarantee for an autonomously prepared graph-state resource, with finite-rate imperfect controllers and bounded local noise including a retained bath. For any fixed target defect level above the noise floor, preparation time is a local-parameter constant independent of volume. Global state fidelity need not be close to one; a fixed defect density produces an extensive number of errors.

This conclusion concerns a dressed subsystem. Extracting the bare graph state requires the explicit finite-depth U* decoder, or equivalent dressed local measurements. Its control and readout errors are additional local operations to price. It is not a free trusted output port.

The equally informed ordinary comparator can prepare the same graph state using a finite-depth controlled-Z circuit with local resets, or the known ideal dissipative stabilizer maps. Thus neither the resource state nor universality from graph states is new. The possible contribution is the completed noisy-controller implementation contract; historical novelty and a practical advantage still require comparison. A successful proof here is an intermediate architecture result, not the requested civilisation-level endpoint and not permission to stop the harder quantum-memory investigation.
