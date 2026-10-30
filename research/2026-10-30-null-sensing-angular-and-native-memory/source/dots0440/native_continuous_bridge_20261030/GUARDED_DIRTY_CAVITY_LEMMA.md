# Buffered guarded activity weights: exact dirty cavity and inverse repair
2026-10-30. Revised governing lemma after independent objections. This proves activity-only dirty surgery and specifies a concrete first-order useful-credit interface. It is not itself the whole native theorem.

## 1. Input, actual term accounting and guard
Work with the exact local HP/unital operator Lhat=T_B^{-1}L_native^*T_B from `DIRTY_CREDIT_RAW_SIMILARITY.md`. Retain the actual own source-block proof, not only a summed raw inequality. Every owner operation preserves every other B_j exactly; its Hamiltonians preserve B_h and its only B_h-changing gains clear B_h.

Keep free-resource monitor terms explicitly as resource-only terms: they commute all dirty credits and annihilate raw f_A, but may act on activity weights. They are NOT dropped below.

Take the controller-only, B-pinched positive activity factors from `CONTROLLER_ONLY_ACTIVITY_EXTENSION.md`. For an original active factor X_g let K_g be its support BEFORE history guards. Guard it by every B_h whose own generator/credit support meets K_g. Also, for each free-resource term meeting K_g, include every owner B_h in that term's fixed buffered patch. Set

    P_g^good=product_{h in N(g)}(I-B_h),
    X_g^guard=P_g^good X_g.

The factors commute, so positivity, activity corners and controller-only character remain. Use exp(delta X_g^guard) in the fixed globally ordered animal circuit Y_A. Added B guards commute all activity/dirty coefficients and Hamiltonians; an owner reset changes only its own B_h. Consequently guard incidence is determined by the ORIGINAL active supports and one fixed term buffer, not an iterative support closure. All supports, coloring depth and incidences remain constants.

## 2. Cavity and mixed-cavity comparison
For fixed h remove every gate whose guard contains h, obtaining Y_A^h and G_A^h=Y_A^{h dagger}Y_A^h. A bounded number of gates is removed. Every retained active factor commutes every h Kraus/Hamiltonian, the private erasure and survival coefficient, and therefore the entire local map Lhat_h. The added guards also commute these objects. On B_h=1, all removed gates are identity, hence

    Y_A B_h=Y_A^h B_h.

All activity factors commute f_A globally. Fixed-depth cancellation gives relative comparison under a bounded local completion B=A union D:

    e^{-Cdelta}G_A^h<=G_B^h<=e^{Cdelta}G_A^h.

More generally, if g lies in h's fixed buffer, G_A^h and G_B^g differ by the bounded completion gates plus two bounded removed-owner gate sets. Thus

    e^{-Cdelta}G_A^h<=G_B^g<=e^{Cdelta}G_A^h.           (2.1)

This mixed-cavity comparison is required to charge a buffered dirty error to a different owner g.

## 3. Exact baseline with operator-weighted token envelopes
Define

    V_cav,h=sum_A f_A G_A^h,
    Delta_cav,h=sum_A [f_A^(B_h=1)-f_A^(B_h=0)] G_A^h.

Only h's unary tokens are replaced in the raw f_A; the controller weights are NOT counterfactually reevaluated. Strong erasure commutation gives exactly Psi_h^*(f_A G_A^h)=f_A^(B_h=0)G_A^h.

Cavity weights commute every h payload/reset coefficient and every h-affected local predicate. Replace each scalar animal by its scalar times G_A^h in the raw spectral-envelope proof. Source/target envelopes remain Loewner inequalities. The completion proof uses the comparison above instead of simultaneous diagonalization of the different G_A. Its surplus changes only from q_R to q_R exp(Cdelta). Choose q_R with strict margin and delta small.

The exact killed-resolvent and inverse-congruence argument then gives the bad charge -gamma B_h Delta_cav,h. On good h sources, deterministic-syndrome per-move completion with the same operator weights gives a nonnegative recovery decrement R_good,cav,h. Other flags are commuting spectators, so this holds even when another owner is dirty. The complete terminal clean/dirty cross block is zero because the CAVITY CONTROLLER factor commutes the Stinespring unitary and the clean image has deterministic syndrome. Therefore the global baseline is

    Lhat_h(V_cav,h)<=-gamma B_h Delta_cav,h-R_good,cav,h,
    R_good,cav,h>=0,                                  (3.1)

and it is block diagonal in ALL B masks. Its good Q0,W0 target compression vanishes. This is the earned zero-order reweighted inequality, not multiplication of an unweighted global drift.

## 4. Compact activation remainder includes BOTH forward and inverse effects
For each A write Y_A=Z_A Y_A^h with the correctly ordered finite-circuit quotient. It has bounded local support near h, ||Z_A-I||<=Cdelta, and commutes f_A. Put Q_A=Z_A^dagger Z_A-I. Then

    F_A-F_A,cav=Y_A^{h dagger} f_A Q_A Y_A^h,
    ||Q_A||<=Cdelta.

Since Y_A^h strongly commutes every Kraus/coefficient of T_h, T_h^{-1}, and L_h,

    Lhat_h(F_A-F_A,cav)
      =Y_A^{h dagger} Lhat_h(f_A Q_A)Y_A^h             (4.1)

EXACTLY. Lhat_h is a bounded local HP map. Split f_A into unaffected factors and the bounded number of factors in this local patch. Their local orbit ratio is bounded. Hence

    +/- Lhat_h(f_A Q_A)<=Cdelta f_A,

and summing only the animals affected by the removed gates gives a local relative O(delta) remainder.

This calculation uses the COMPLETE inverse

    T_h^{-1}(O)=S_h^{-1/2}[O-C_h Psi_h^*(O) C_h]S_h^{-1/2},
    C_h=sqrt(I-S_h).

It automatically includes both previously missing effects:
- forward credit activation C_h Psi_h^*(F_G-F_cav,h) C_h on a bad source;
- inverse target subtraction -S_h^{-1/2}C_h Psi_h^*(O)C_hS_h^{-1/2} when the weighted O has nonzero good-Q0 compression.

Neither is assumed zero or assigned a sign. Their full local norm is in (4.1). The positive-congruence inverse formula is used ONLY for the zero-target cavity baseline (3.1).

## 5. Buffered dirty block and cross block
For each linked local term choose P_X=product_{g in X}(I-B_g), Q_X=I-P_X with a fixed buffer X containing its primitive, credit and guard supports. Because (3.1) is globally B-block diagonal, its P_X/Q_X cross block is zero.

The activation remainder E has +/-E<=Cdelta sum_local f_A G_A^h. Its WHOLE Q_X block is bounded by Cdelta Q_X times these weights; this includes B_h=0 but another B_g=1 and coherences inside Q_X. Use

    Q_X<=sum_{g in X}B_g

and complete each local animal by a fixed patch and g's token bundle. Mixed-cavity comparison (2.1) pays it from B_g Delta_cav,g. Bounded buffer incidence means the summed dirty error is at most Cdelta sum_g B_g Delta_cav,g, with no extra |A|.

Only P_X/Q_X cross blocks need Young. Allocate a fixed part of gamma sum_g B_g Delta_cav,g to their dirty side; the clean side costs

    Cdelta^2 W_G,  W_G=sum_A |A| f_A G_A.

The single |A| counts local linked supports meeting A. It is not a double pair sum. Keep the ACTUAL clean P_X block for the separate clean activity/service proof; do not bound it by O(delta)W_G.

## 6. Free-resource monitors
For a resource-only free monitor term, enlarge the buffer to all owners specified in section 1. On Q_X every activity factor that could fail to commute with that term is off; the term preserves every B, so there is no healing-target activation. The cavity product commutes it and raw f_A is monitor-independent, giving zero dirty-source/cross contribution. On P_X retain its actual action in the clean activity generator. Equivalently it may be assigned to one neighboring owner once, with that expanded support included in the cavity definition. It must not be dropped solely because its raw-V drift vanishes.

## 7. Concrete useful-credit first-order interface (conditional on clean review)
Use exactly the analytic virtual-ready-reset primitive and history-good guard of `weak_initiation_compiler_20261030/ANALYTIC_GUARDED_USEFUL_CREDIT.md`, with its earned general isolated normalizer. Guard each primitive on all B owners in the fixed local interaction buffer. It preserves every B mask, is raw-syndrome-diagonal on diagonal inputs, is unital CP, and has a uniformly bounded local Z_h=Q_h-Id. Its interpolated circuit T_t is uniformly linearly invertible for t<1/4. Thus

    T_t^{-1} Lhat T_t=Lhat+t sum_h[Lhat,Z_h]+R_t,
    ||R_t||_local<=C t^2,

with fixed supports/incidence and constants uniform as epsilon->0.

On buffered all-good blocks this is the actual clean commutator calculation, since the dirty similarity is identity there. On Q_X and P_X/Q_X, treat t[Lhat,Z_h] as the SPECIFIED bounded local HP perturbation. After activity conjugation its relative local norm is O(t), so the same buffered token completion pays O(t) dirty diagonals and Young costs O(t^2) clean weight. Together with activity activation the cost is O((t+delta)^2)W_G. Generic R_t costs O(t^2)W_G directly; mixed local useful/activity conjugation costs O(t delta)W_G.

This section is a conditional composition interface requiring the cited concrete primitive and the separately reviewed clean linked commutator estimate. It is not a theorem for arbitrary near-identity CP maps. The activity-only cavity/dirty argument in sections 1-6 is independent of that clean useful-service review.
