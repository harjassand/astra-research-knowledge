# Positive finite-depth multiplicative activity weight
2026-10-30. Conditional exact lemma. This packages the collision hierarchy without a global linear-credit norm loss. It does not yet combine the useful DATA-recovery CP credit with these factors.

## 1. Inputs and output
Assume all hypotheses of `COLLISION_HIERARCHY.md`. Let U be any finite anchor set and E_U any bounded-degree collection of selected activity pairs whose endpoints are in U. The supports of the X_h and Y_e have fixed radius and incidence. These constants do not depend on U.

Choose B>0, then A sufficiently large compared with B and the local constants. Choose delta>0 sufficiently small, then epsilon>0 sufficiently small; all choices are fixed independently of U and total volume. Define positive invertible local gates

   Q_e=exp(delta B Y_e),
   Q_h=exp(delta A epsilon^2 X_h).

Color the enlarged gate-support overlap graph and order the gates in a fixed bounded number of color layers. Let Y_U be their ordered product and

   G_U=Y_U^dagger Y_U.

Every gate commutes all P_h. Therefore G_U commutes all P_h. There are constants a,b,c,C>0 independent of U and volume such that

 (L0*+epsilon V*)G_U
 <= [-a delta A epsilon^2 sum_(h in U)P_h
     -b delta B sum_(e={h,j} in E_U)P_hP_j
     +C delta A epsilon^4 |U| I] G_U.                     (1)

Harmless changes in a,b,C cover selected edge sets with a uniformly bounded multiplicity and duplicated local gates. One must include all selected pair endpoints as singleton anchors.

The comparison is exponential in the anchor count, not polynomially amplified:

   I <= G_U <= exp[c delta (B |E_U|+A epsilon^2 |U|)] I.

The lower bound follows from the product of the gates' minimum singular values, each at least one; it does not assert that noncommuting positive factors have a positive product.

## 2. Exact nonunital local conjugation
Define a congruence map C_U(O)=Y_U^dagger O Y_U. Its inverse is another positive completely positive congruence. Both are usually NONUNITAL. Set

   L_eff,U*=C_U^{-1} (L0*+epsilon V*) C_U.

This is an exact similarity, not an effective generator approximation in time. Equation (1) is equivalent to an upper bound on L_eff,U*(I), because every activity projection commutes Y_U.

A gate with support disjoint from a local generator term commutes through that term and cancels with its inverse. Bounded depth therefore enlarges a local term's support by only a fixed radius. Each transformed local term has uniformly bounded local norm. There is no extensive-generator norm or dependence on the number of animals.

## 3. Fast Taylor remainder has the needed corners
For Hermitian X write M_X(O)=XO+OX. Congruence by exp(delta X) is exp(delta M_X). At first order,

   [L0*,M_X] I=2 L0*X.

Hence first order supplies

   -2 delta A epsilon^2 sum P_h -2 delta B sum P_hP_j.

The crucial remainder statement is stronger than a generic O(delta^2)|U| estimate:

   R_fast(I) <= C delta^2 [B^2 sum_e P_e
                          +AB epsilon^2 sum_e P_e
                          +A^2 epsilon^4 sum_h P_h].     (2)

Constants absorb bounded incidences and higher orders for delta B and delta A epsilon^2 in fixed bounded intervals.

To justify the corner claim, every gate X is positive and supported in its flag corner P_X, and commutes every activity projection. The no-creation/block-preservation hypotheses imply L0*(O) is supported in the same corner whenever O is. Products of two such gate operators are supported in the intersection of their corners. Thus every nested commutator contribution on I that contains a pair gate remains in that pair corner; a contribution containing only singleton gates and at least two gates carries at least epsilon^4. Locality bounds the connected nested-commutator coefficients with fixed incidence, not |U|^2.

Equation (2) is absorbed by choosing delta small for pair terms and epsilon small for singleton terms. This is the point at which a generic scalar remainder estimate would fail.

## 4. Weak part: exact flag-block hierarchy
Because all gates commute every P_j, conjugation cannot change which activity projections an initiation H_h toggles. After cancellation of disjoint gates, its contribution remains local with the same block pattern.

* Blocks preserving a selected pair are O(delta B epsilon) on that pair and are absorbed for small epsilon.
* A pair-creation/annihilation block is O(delta B epsilon) between P_hP_j and (1-P_h)P_j (or the symmetric block). Young with a fixed fraction of delta B P_hP_j leaves O(delta B epsilon^2)P_j.
* On a sector where no selected pair can occur, all pair gates are identity. Only singleton gates change the weak initiation. Their active/idle block is O(delta A epsilon^3). Young with delta A epsilon^2 P_h leaves O(delta A epsilon^4)I.
* Singleton-gate terms involving other initiations remain in the singleton corner and are O(delta A epsilon^3), hence absorbable.

Choose A after B to absorb the bounded sum of pair-to-single remainders. All normalization factors from the local gate inverses are bounded uniformly. This proves (1) after distributing fixed fractions of the negative budgets.

Notice the order: constant pair credit, epsilon^2 singleton credit, epsilon^4 idle source. A constant singleton credit would give an epsilon^2 idle source and would lose the intended separation from useful recovery.

## 5. Local-noise sensitivity: do not use a unital lemma
For an animal A, choose U(A) with |U(A)|<=C_A |A| and bounded-radius incidence. Suppose f_A>0 has the usual uniform local-orbit ratios. Define

   F_A=Y_(U(A))^dagger f_A Y_(U(A)).

This is positive even if f_A and the gates do not commute. For a local perturbation N_e*, conjugating through Y gives an enlarged local map, but it generally DOES NOT annihilate I. The unital CP-dressing noise lemma cannot simply be quoted.

Instead bound it directly in the f_A-relative norm. For a Hamiltonian term, put H_tilde=Y H_e Y^{-1}; then

 C_U^{-1}(i[H_e,C_U(f_A)])
    = i(H_tilde^dagger f_A-f_A H_tilde).

H_tilde has bounded enlarged support and norm. The local-orbit ratio bounds both f_A^{-1/2}H_tilde^dagger f_A^{1/2} and its partner by fixed constants. For a jump J_e the transformed gain uses J_tilde=Y J_e Y^{-1}, whereas the transformed loss uses Y J_e^dagger J_e Y^{-1}, NOT J_tilde^dagger J_tilde. Both are still bounded local operators; bound gain and loss separately. The same argument works with an untouched common bath because all Y gates act on the system only.

Only O(|A|) perturbation supports meet f_A or the selected gate circuit. Thus

   N*F_A <= C_noise eta |A| F_A

for a local perturbation budget eta, with fixed constants. This is the desired O(|A|), not O(|A|^2), sensitivity. It is a direct nonunital relative-norm estimate.

## 6. What this does NOT yet prove
Equation (1) is a controller activity inequality. It is not automatically a DATA-weighted inequality for sum_A F_A. In particular, individual animal factors need not decrease under each intended correction even when their summed potential V decreases. One may NOT multiply (1) by arbitrary f_A and drop all reset-data cross terms.

On a genuinely tensor-separated controller/data model with Phi_h*f_A<=f_A separately, such multiplication is valid. That extra monotonicity is not assumed for the actual weighted SSF animals. The intended application must combine local animal surgery, the isolated useful-service credit, and the activity charge. This combined local drift is still open. Full-Hilbert dirty-mask extension is also separate.
