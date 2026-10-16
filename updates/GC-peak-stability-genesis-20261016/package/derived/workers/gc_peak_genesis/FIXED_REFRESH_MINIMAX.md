# Exact singleton minimax for fixed refresh slots

Author: gc_peak_genesis. Date: 2026-10-16. Status: internally derived theorem and independent audit of the root-supplied fixed-slot receiving lead. External correctness and historical priority UNKNOWN.

## 1. The operation and precise interface

Let 0=t₀<t₁<⋯<t_m=T, m=N+1. There are N prescribed internal refresh slots, so there are m weak-evolution gaps. On each gap the virtual seed parity evolves under

    H(t)=H₀(t)+V(t), [H₀(t),Z]=0, {V(t),Z}=0,
    ||V(t)||≤j(t), a_k=∫_(t_(k−1))^(t_k) j(t)dt.

At each internal node apply the exact nonselective pinch D_Z=(Id+Ad Z)/2. The entering sector is specified; the final wrong-sector Born effect is the observable of interest. The Hilbert space and bath may be finite and arbitrary; a reference can be tensored throughout. No bath reset is used.

In the qualified private-sign interface, this is a mathematical representation of a known random DD operation. Take an independent uniform initial bit f and independent fair toggle bits b₁,…,b_N at the fixed slots, ξ(t)=(−1)^(b₁+⋯+b_k) after slot k, and

    H_(f,b)(t)=H_base(t)+(−1)^f ξ(t) A(t).

H_base and A are independent of the selected seed and **all** selected toggle paths. The ordinary input, all other randomness and controls meet the source's additive common-dilation requirements. The final frame is inverted or read out covariantly. A virtual seed q with Hamiltonian H_base+X_q⊗A and copied Z_q jumps yields the initial-bit Walsh coefficient at each final Z_q label, up to an irrelevant output-label phase. Averaging each fair toggle is exactly D_Zq at its fixed slot.

Thus this theorem is an endpoint theorem for actual ideal pinches and a singleton odd-Walsh **effect** theorem for a qualified private-sign implementation. A Fourier label is not automatically a physical spatial fault. The primitive protocol is established random DD, not newly invented here; primary precedents are recorded in PRIMARY_PRIOR.md.

## 2. One-gap sharp subspace-angle lemma

For a gap of envelope action b, any entering state in one Z sector has mismatch probability at most

    s(b)=sin²(min(b,π/2)).                           (1)

To prove it, transform away H₀. This preserves sector projectors and the norm bound. Purify an arbitrary entering state. Write q(t)=||P_opposite ψ(t)|| and p(t)=q(t)². The odd interaction gives

    |p'(t)|≤2j(t)√(p(t)(1−p(t))).

Starting at p=0, integration of the subspace angle gives arcsin√p(t)≤∫j until π/2. A limiting argument handles endpoints or zeros. This proves (1), uniformly on the whole entering sector and with arbitrary bath/reference state. Equivalently, the compressed gap survival effect is at least cos²(min(b,π/2)) times the entering-sector projector.

## 3. Exact fixed-schedule worst case

Keep the internal sector outcomes in isolated mathematical records. For the record event that every gap retains the entering label, the uniform one-gap lemma successively lower-bounds each conditional survival factor. No independence of bath or outcomes is needed. Its probability is at least

    ∏_(k=1)^m cos²(min(a_k,π/2)).

A final wrong-sector outcome requires some gap mismatch. Therefore the actual endpoint effect is bounded by

    Q(a₁,…,a_m) I,
    Q=1−∏_(k=1)^m cos²(min(a_k,π/2)).               (2)

The bound is **attained** by a finite bath, so it is the exact minimax value for the fixed schedule over the arbitrary-finite-bath uncertainty class. The upper holds for every finite bath size; if an application separately fixes a smaller bath dimension, the attainment statement needs the dimension specified below and is not automatic.

Use one physical memory qubit M with Z_M and bath basis |u>,|d₁>,…,|d_m>. Set H₀=0 and, on gap k,

    V_k(t)=j(t) X_M⊗(|d_k><u|+|u><d_k|),

until its integrated action reaches π/2, then set V_k=0. Its norm is at most j(t), it is Hermitian and odd under Z_M, and it is selected-randomness independent. Start in |0_M,u>.

If no mismatch has occurred, gap k rotates |0,u> toward |1,d_k> by angle min(a_k,π/2). Previously created |1,d_l> with l<k are dark under every later V_k. An internal pinch removes only the newly created entering/wrong-sector coherence. Induction gives survival mass ∏cos²(min(a_k,π/2)); every complementary branch has memory parity 1 at the terminal time. This proves equality in (2). The bath dimension is m+1=N+2, finite for each finite slot count. The construction is available on any larger bath by embedding; exact saturation is not asserted for a separately fixed smaller bath.

For the private-sign version multiply each V_k by (−1)^f ξ. On each gap this changes the transition's phase, not its probability; previous d_l branches remain dark. Every final wrong-memory branch has an odd number of selected-sign insertions. Its initial-seed Walsh label is therefore odd. On the input |0,u>, the averaged singleton odd-Walsh effect and the actual final memory-parity error both equal Q. This supplies an operational lower witness within the qualified sign interface; it does not identify arbitrary receiving Walsh labels with faults.

## 4. Globally optimal slots for a known nonuniform envelope

Let a=∫₀ᵀj(t)dt and m=N+1. Over all prescribed slot placements, the exact robust minimum is

    Q_N*=1−cos^(2m)(min(a/m,π/2)).                   (3)

If a<mπ/2 and any gap has a_k≥π/2 then Q=1, which cannot beat equal actions. Otherwise log cos x is strictly concave on [0,π/2), so

    ∑ log cos a_k ≤ m log cos(a/m).

This proves (3), attained by equal **action** gaps a_k=a/m. The cumulative action is continuous, so quantile slots exist for every integrable j; plateaus can be resolved by choosing any corresponding times. If a≥mπ/2, every partition has a saturated gap and the robust minimum is one. If a=0 every schedule is perfect and uniqueness is irrelevant.

For constant j=J this means equal time gaps. Its expansion is

    Q_N*=a²/m −a⁴/(2m²)+a⁴/(6m³)+O(a⁶)

for fixed m. In particular Q_N*≤a²/m. The old deterministic certificate is the exact leading minimax coefficient, but the finite-action worst case is (3), not a²/m.

Knowing only total action, without a pointwise envelope or profile, does not justify equal-action placement. An unknown interaction can concentrate its action inside one gap; PEAK_AND_POISSON_MINIMAX.md gives the exact obstruction.

## 5. Joint subsets: established upper, separate lower

For several selected private seeds with independent fair toggles at their own fixed slots, the source's fixed-cut deletion-null proof gives

    F_S≤∏_(i∈S) min(1,∑_k a_(i,k)²) I.             (4)

One may reproduce it by fixing all node times, adding the retained virtual-seed parity records, deleting one selected interaction restriction on each chosen witness gap, applying the mixed Duhamel estimate, then unioning one gap per parent. Clock averaging is unnecessary. Adjacent-gap records commute. Shared noncommuting bath terms stay in chronological order. No independence of actual errors is asserted.

Independent tensor copies of the sink construction give the **actual** selected joint lower witness ∏Q(a_(i,1),…,a_(i,m_i)). Thus for fixed counts and independently selectable slots,

    ∏Q_(N_i)*
      ≤ inf_slots sup_allowed_H Pr(all selected endpoint flips)
      ≤ ∏min(1,a_i²/(N_i+1)).                      (5)

The analogous statement holds for all-selected odd-Walsh effects in the qualified sign interface. Equation (5) gives the exact leading subset minimax constant as every action tends to zero. The singleton product ∏Q is **not** asserted as a universal finite-action shared-bath upper bound; no proof of that stronger statement is supplied.

For a total integer slot budget NΣ=∑N_i, the product certificate in its uncapped regime is minimized by assigning counts that differ by at most one: write NΣ=qr+s, 0≤s<r. Then r−s parents receive q slots and s receive q+1, with product certificate

    (∏a_i²)/[(q+1)^(r−s)(q+2)^s].                 (6)

This follows by balancing the positive integers N_i+1 to maximize their product. It is specific to an all-selected product objective. The exact finite-action singleton minimax allocation need not be balanced when actions differ. Minimum slot separation, serial gate occupancy, and positive-duration pulse constraints are additional constraints not optimized by (6).

## 6. Equal-resource comparisons

There are three different counts:

1. N fixed **refresh opportunities**, each applying Z with probability 1/2: maximum N and mean N/2 interior actual involution flips.
2. Telegraph Z kicks of intensity γ: mean n=∫γ physical flips, with an unbounded Poisson count.
3. Latent complete pinches for that same telegraph average: mean Λ=2n. These are mathematical labels, not physical pulses.

Initial private frame preparation, terminal inverse, selected-coordinate support, controller bit generation/privacy, and all ramps/resets must be charged separately to both implementations. A count comparison omitting these is only an interior ideal-operation comparison.

At matched interior mean physical flips n with N=2n an integer, the fixed-slot certificate is a²/(2n+1). The globally optimal unconstrained Poisson certificate is 2a²/(2n+2)=a²/(n+1). A latent peak cap can only increase the Poisson optimum. Thus the fixed-slot improvement is an already known random-DD timing advantage, expressed here through the sharp joint-effect interface; it is not a new physical operation.

The new minimax bounds make that comparison operational inside the exact ideal model. For a≤π/4 and integer N=2n≥1,

    Q_N*≤a²/(N+1)
      <κ(a)·2a²/(N+2)
      ≤W_Poisson*,                               (7)

where W_Poisson* is the exact-model worst-case endpoint error optimized over any admissible Poisson rate profile with latent budget Λ=N. The strict middle inequality follows because κ(a)≥8/π²>3/4≥(N+2)/(2(N+1)). The right side is the physical witness lower bound from PEAK_AND_POISSON_MINIMAX.md. Hence fixed private fair-refresh slots beat every Poisson intensity schedule in exact-model robust endpoint error throughout this stated action range at matched mean interior flips, subject to the same qualified ideal sign-control interface. Both protocols also need a common feasible physical implementation before this becomes a device comparison.

If instead exact full syndrome pinches are the acquired primitive, use N deterministic actual pinches versus mean Λ=N Poisson actual pinches. The same equations hold at matched mean **measurement** count; this is a different resource comparison from physical telegraph flips.

Public deterministic DD pulses are a weaker comparator under the source's full uncertainty class. Given a known toggling frame U_c(t) preserving the measured parity, an allowed adversary can choose V(t)=j(t)U_c(t)XU_c(t)†. In the toggling frame it is always j(t)X. The final flip probability is sin²a for a≤π/2, independent of pulse count. The subspace-angle bound supplies the matching upper, so the worst case is exactly sin²(min(a,π/2)). This is an envelope-only, arbitrary-time-dependence minimax statement. If the actual Hamiltonian is known to be a constant commuting interaction, spin echo cancels it exactly and is the relevant better informed incumbent.

## Limits

No finite-width implementation follows from fair bits or final compensation. The additive sign-independent Hamiltonian, pointwise ideal-action covariance, complete support/completion imports, full reservation time, private controller isolation, and noise during ramps remain explicit receiving gates. No hardware bandwidth, energy, threshold, or external originality claim is made.
