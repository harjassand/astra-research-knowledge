# Dirty-erasure credit gives a raw local similarity inequality
2026-10-30. New strengthening candidate for full-Hilbert surgery. It does not claim the inverse is CP globally.

## 1. The triangular local CP map is exactly invertible
For owner h let B=B_h, G=I-B, S=G+S_B B with 0<s_min I<=S_B<=I, and Psi the private reset to Q0,W0, which always lands in G. The correctly ordered Heisenberg credit is

    T_h(O)=sqrt(S) O sqrt(S)
             +sqrt(I-S) Psi^*(O) sqrt(I-S).

Its GG block is O_GG, its GB/BG blocks are scaled by the invertible sqrt(S_B), and its BB block is sqrt(S_B)O_BB sqrt(S_B) plus a known linear pullback of O_GG. Therefore T_h is an invertible bounded local linear map. Its inverse is HP and unital, but need not be positive.

Let Z_h={O : P_(Q0,W0) O P_(Q0,W0)=0}. Since Psi resets only the private hub, this condition is exactly Psi^*(O)=0. The coefficient sqrt(S) is identity on the whole G sector and preserves B, hence Z_h is invariant under congruence by sqrt(S) and its inverse. On this invariant subspace,

    T_h(O)=sqrt(S) O sqrt(S),
    T_h^{-1}(O)=S^{-1/2} O S^{-1/2}.                 (1)

The inverse is consequently positive ON Z_h whenever its argument is positive and belongs there. No extension of this claim to all observables is made.

## 2. The actual own drift lies in this subspace
Let O_h=L_h^* T_h(V), using exactly the owner decomposition from the dirty-credit proof (and, if adopted, the monitored owner-block cleanup decomposition). The good Q0,W0 compression of O_h is zero:
- on that source all h flags are clear and the credit is identity;
- h's cleanup/verification/monitor actions preserve DATA and every flag;
- there is no Q0 terminal or acquisition source;
- any h reset enabled there is DATA/flag identity on this source.

Offdiagonal matrix elements elsewhere do not affect Psi^*(O_h); it pulls back only this Q0,W0 diagonal compression. Thus O_h belongs to Z_h.

The proved dirty-credit estimate is

    O_h <= -gamma B_h Delta_h -R_h^good,
    Delta_h=V(B_h=1)-V(B_h=0),

where R_h^good is the actual nonnegative good terminal DATA decrement (and optional nonnegative good commit terms). Both displayed negative targets lie in Z_h. Apply the positive congruence (1), not an unjustified globally positive inverse. Since Delta_h commutes S_B and S_B<=I,

    T_h^{-1} L_h^*T_h(V)
      <= -gamma B_h Delta_h -R_h^good.              (2)

The good term is unchanged because S=I on G. Terms retained as extra negative bad-source intensity charge remain negative under the same congruence.

## 3. Exact many-owner local similarity
The dirty credits commute with one another and every exterior nominal term. Therefore for T_B=product_h T_h,

    Lhat=T_B^{-1} L_native^* T_B
          =sum_h T_h^{-1} L_h^* T_h

plus any commuting resource-only terms. Lhat is a sum of bounded-support HP, identity-annihilating maps with bounded incidence. It is not asserted to be a Lindblad generator. Summing (2) gives the RAW inequality

    Lhat(V)<=-gamma sum_h B_h Delta_h -sum_h R_h^good. (3)

On the all-good invariant range, T_B is identity and the restriction of Lhat is exactly the actual clean native generator. Thus the dirty normalization does not change the clean acquisition calculation.

## 4. Consequence for a later local-surgery proof
Suppose a further near-identity bounded-depth local DATA-credit/activity construction has parameters b,delta and is proved on buffered all-good sectors. Work first with the exact local operator Lhat and raw V. Equation (3) supplies immediate dirty weight, rather than a merely dressed bad term.

Pinching the activity witnesses in the actual commuting B masks preserves positivity, support up to a fixed enlargement, activity corners and the all-good restriction. It need not preserve the dirty activity inequality; (3) is available to pay those local errors. At b=delta=0 the raw source calculations have zero clean/dirty cross block. Perturbative cross blocks are therefore O(b+delta); weighted Young absorption against (3) costs O((b+delta)^2) clean animal weight. Dirty diagonal terms of size O(b+delta) are paid by the same local token completion. These statements require the actual linked-support/animal-local circuit audit; they are not a blanket assertion that arbitrary nonlocal reweightings are safe.

After a complete inequality is proved for Lhat and the new positive observable F_new, applying the positive T_B yields the corresponding inequality for the actual L_native and T_B(F_new). This is the legitimate role of the exact similarity. No positivity of T_B^{-1}, no effective Lindblad model and no finite-time simulation error is invoked.
