# Uniform stochastic interior entrance and clearing from factorial boundary drift
Status: V2 corrected scope; personal derivation under review. No rapid mixing or deterministic permanence theorem is assumed. This concerns the killed homogeneous conservative fast subsystem, not the full coupled process.

## Contract
There are k>=2 composition species, total N. A finite strongly connected graph of degree-m composition complexes, m>=2, contains every pure complex mX_i. Fixed positive fast constants are arbitrary. Let L_N be its actual mass-action generator on the finite N-shell. Killing has rate c(A)_m for one distinguished species A. A common resource factor (B)_q may multiply BOTH fast reactions and killing; restore it at the end.

## Uniform negative fractional-factorial drift near every simplex face
For sufficiently small fixed 0<alpha<1, set V_N(x)=product_i(x_i!)^alpha. The uniform homogeneous boundary-limit lemma gives

    (L_N V_N)/(N^m V_N) -> E_alpha(t),  t=x/N,

uniformly over ALL integer compositions, including disabled source counts. On any proper simplex face, complexes involving a missing species have zero monomial weight. The remaining source subgraph is killed on exit from that face; strong connectivity gives a path to killing from every remaining complex. The finite killed-graph fractional-power lemma therefore makes E_alpha strictly negative on each face after choosing one alpha for the finitely many faces. Pure complexes guarantee total source monomial weight at least k^(-m), so this is a uniform absolute negative margin, not a vanishing normalization.

Continuity and compactness give epsilon,c>0 such that for all sufficiently large N,

    L_N V_N/V_N <= -c N^m  whenever min_i x_i<=epsilon N.    (1)

The alpha and constants can be chosen uniformly over a fixed positive compact box of coefficients.

## Concavity converts the factorial certificate to an O(N) entropy range
For every positive V and jump generator,

    L log V <= (LV)/V,

because log u<=u-1 termwise. Define the nonnegative shell entropy potential

    U_N(x)=log V_N(x)-alpha log(N!)+alpha N log k.

The multinomial inequality N!/product x_i!<=k^N gives

    0<=U_N(x)<=alpha N log k.

The subtracted terms are constant on the conservative shell. Consequently (1) yields L_N U_N<=-cN^m outside the fixed interior set K_N={min_i x_i>epsilon N}. Stopped Dynkin on the FINITE shell gives

    sup_x E_x tau_(K_N) <= C N^(1-m).                     (2)

This earns fast stochastic interior entrance. It says nothing about mixing between interior metastable states or the stationary distribution.

## A bounded killed supersolution gives the same clearing scale
Let W_N=1+U_N/N, so 1<=W_N<=1+alpha log k. In the boundary region, (L_N-c(A)_m)W_N<=-c N^(m-1) by (1).

Globally, bounded reaction jumps and factorial increments imply |L_N log V_N|<=C N^m log(N+1). Thus L_N W_N<=C N^(m-1)log(N+1). In the interior, A>=epsilon N and the killing rate is at least c' N^m. Since W_N>=1, for sufficiently large N its killing term dominates this upper bound. Therefore everywhere on the shell,

    (L_N-c(A)_m)W_N <= -c'' N^(m-1).

Finite-state killed Dynkin gives

    sup_x E_x tau_clear <= C N^(1-m).                     (3)

For the finitely many smaller ACTIVE STATES (those enabling a fast source), complex-path access gives finite killing times and constants can be enlarged over those states/components. A shell containing some active states may also contain an inactive closed class: for 2A<->2C at N=2, (1,1) is inactive and never clears. Such states are excluded. For B>=q, restoring the exact positive shared resource factor gives

    E tau_clear <= C N^(1-m)/(B)_q

for all sufficiently large N, uniformly in composition. If B<q, the factor is zero and no finite clearing-time claim follows. The common supersolution also gives this bound under coefficients varying in a fixed positive compact box, by stopped Dynkin, without a stationary-average assumption.

## Scope and potential use
For m=3, this is a generic O(N^-2)/(B)_q bound in arbitrary composition dimension. The earlier special-chain N^-9/4 bound is sharper but structurally narrower. The present result may support a physical repair of low-A boundary phases before using the N-directed residual; it does not itself prove that repair or close the higher-dimensional entropy-interface mismatch.
