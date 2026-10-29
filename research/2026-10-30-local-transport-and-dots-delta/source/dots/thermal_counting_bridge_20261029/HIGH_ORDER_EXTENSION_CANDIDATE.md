# Separate candidate extension: fixed even order and stagewise rounding

Date: 2026-10-29. Author: `challenge_thermal_counting_consequence`.

**Status: independently unaudited candidate; NOT part of COUNTING_INDEPENDENT_RECEIPT.json.** The fixed-second-order certificate remains unchanged. This note records a possible next strengthening and its exact obligations. No historical novelty is claimed.

## A. General real palindromic product formulas

Fix an even integer p. Let `P_p(t)` be any finite real-coefficient palindromic splitting formula in the colored layer Hamiltonians, with order p:

`P_p(t)=exp(-tH)+O(t^{p+1})` as a Taylor identity for each finite system.

Usual recursive Suzuki formulas supply such words for every even p; their negative coefficients do not obstruct the following algebra. Every factor `exp(-a t H_j)` is positive definite for real a,t. Splitting the central exponential in half makes the whole palindromic word exactly `Q_p(t)^dagger Q_p(t)`, where Q_p has finite layer depth L depending on p,k,Delta but not n. Write its layer coefficients as `a_1,...,a_L`, set `S=sum |a_l|`, `a_*=max |a_l|`, `K_L=sum_{s=1}^L k^s`, and `A=2 a_* J K_L`. Trivial zero-Hamiltonian cases may be removed.

Let `R(t)=Q_p(t) exp(tH/2)` and `G=R'R^{-1}`. Product differentiation expresses G entirely as sums of finite-prefix conjugates of local terms:

`G = -sum_l a_l Ad_{prefix>l}(H_{j_l}) + (1/2)Ad_{Q_p}(H)`.

The active-cone argument in the saved second-order proof applies with signed coefficients, using absolute values in the norm bound. Consequently

`||[t^j]G(t)|| <= m J (S+1/2) A^j/j! <= n C A^j/j!`,

where `C=Delta J(S+1/2)`.

The order-p identity implies

`R(t)^dagger R(t)=exp(tH/2) P_p(t) exp(tH/2)=I+O(t^{p+1})`.

But exactly

`Herm G(t)=(1/2)R(t)^{-dagger} [d/dt(R(t)^dagger R(t))] R(t)^{-1}`.

Thus every coefficient of `Herm G` below degree p is zero. This step uses only a Taylor identity at each finite n; no uniform estimate on the full-H exponentials or inverse R is used. Uniformity comes from the separate finite-cone coefficient majorant. For t>=0,

`||Herm G(t)|| <= n C sum_{j>=p}(At)^j/j! <= n C exp(At)(At)^p/p!`.

Singular-value Gronwall followed by the operator-monotone logarithm, exactly as in the saved proof, yields

`||log P_p(delta)+delta H|| <= 2n C exp(A delta) A^p delta^{p+1}/(p+1)!`.

For `r>=A beta`, the resulting free-energy-density error is at most

`2 C e A^p beta^p/((p+1)!r^p)`.

The potentially delicate step is the order-condition-to-Hermitian-generator cancellation; the displayed exact identity is intended to settle it rather than assuming that arbitrary error generators share the formula's order.

## B. Stagewise local rounding without a shared nearby Hamiltonian

Different Suzuki coefficients need different rounded local gates; they cannot in general all be interpreted as exponentials of one common perturbed h_e. Instead compare positive palindromes directly.

In the half-word Q, replace every local positive exact factor `A_g` by a rational Hermitian `G_g` with `||G_g-A_g||<=eta`. Reuse its identical Hermitian partner in the reverse half so the rounded full word is `P_1=Q_1^dagger Q_1`. Repeat this same rounded word r times. Put `A_g(s)=(1-s)A_g+sG_g` and let Q_s be the corresponding half-word product, for `0<=s<=1`.

Assume `|a_l| delta J<=1/2` and `eta<=1/10`. Then `lambda_min(A_g(s))>1/2`, `||A_g(s)||<2`, and every gate condition number is less than 4. The derivative `Q_s'Q_s^{-1}` is a sum of prefix conjugates of `D_g A_g(s)^{-1}`, where `D_g=G_g-A_g` and `||D_g A_g(s)^{-1}||<=2eta`. The half word has at most mL gates. Each local generator's finite-prefix cone retains at most K_L gates, so

`||Q_s'Q_s^{-1}|| <= 2m L 4^{K_L} eta <= n C_round eta`,

where `C_round=2 Delta L 4^{K_L}`.

For `R_s=Q_s Q_0^{-1}`, its relative generator is exactly `Q_s'Q_s^{-1}`. Gronwall over s in [0,1] and congruence therefore give

`exp(-2n C_round eta) P_0 <= P_1 <= exp(2n C_round eta) P_0`.

Monotone log, not a power-in-Loewner argument, gives

`||log P_1-log P_0||<=2n C_round eta`.

The r-step free-energy-density change is at most `2 C_round eta/delta`. Taking `eta<=delta epsilon/(8 C_round)` allocates epsilon/4 to rounding. The interpolated gates remain supported on their original k sites; no statement about locality of their logarithms is needed.

The condition `r>=A beta` already ensures `|a_l|delta J<=1/2` since K_L>=1. The harmless eta<=1/10 cap can be imposed explicitly.

## C. Conditional scaling if A and B pass independent audit

Choose `beta=4/epsilon` and `r=Theta_p(beta epsilon^{-1/p})`, large enough for A and the desired epsilon/4 physical error. Then

`r=Theta_p(epsilon^{-(1+1/p)})`, `delta=Theta_p(epsilon^{1/p})`, and `eta=Theta_p(epsilon^{1+1/p})`.

Local dimension remains fixed. Algebraic real Suzuki coefficients are fixed computable numbers; certified rational enclosures plus rational Taylor approximation give dyadic local gates with `B=O_p(log(2/epsilon))` bits. The existing unique-extension width-3 compiler then uses

`N=O_p(n epsilon^{-(1+1/p)} log(2/epsilon))`.

Under the imported sparse #3SAT bound, `epsilon_n=Theta((log n)^{-a})` gives volume-subexponential time whenever

`a < p/(2(p+1))`.

For every fixed a<1/2 one may choose a sufficiently large fixed even p. This does not establish the endpoint a=1/2, a usable practical constant, or inverse-polynomial total-energy precision. It also does not supersede the need for an independent audit of this note. Standard splitting-theory provenance should be cited and no invention claim attached to the high-order machinery.
