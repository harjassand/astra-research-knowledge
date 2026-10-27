# Actual-channel Jensen variance payment for the maximal anchor

2026-10-25. Root construction. A general finite-dimensional unital-CP resolvent identity; not a proof of the WH3 target and no novelty claim for the underlying Jensen machinery. It records a source-compatible payment omitted by the abstract index-nine effect relaxation.

Let N be a unital CP map, 0<=Z<=I, C=N(Z), and define V=N(Z^2)-C^2>=0. Then, on supported vectors where the logarithmic expressions are finite,

log C-N(log Z) >= integral_0^infinity (C+sI)^(-1) V (C+sI)^(-1) ds/(1+s).     (1)

The operator integral may be read first with positive spectral floors and then through the exact resolvent representation; kernels require supported quadratic-form limits, not assigning a finite logarithm to zero.

## Derivation

Choose a Stinespring isometry W with N(X)=W* pi(X) W and decompose pi(Z) on ran W and its orthogonal complement:

pi(Z) = [[C, X], [X*, D]], 0<=pi(Z)<=I.

Then XX*=N(Z^2)-C^2=V and 0<=D<=I. At s>0,

N((Z+sI)^(-1))=(C+sI-X(D+sI)^(-1)X*)^(-1).

For H=C+sI and T=X(D+sI)^(-1)X*, the positive block Schur complement gives

(H-T)^(-1)-H^(-1) >= H^(-1) T H^(-1)
 >= (1+s)^(-1) H^(-1) V H^(-1).

The first inequality follows from (I-H^(-1/2)TH^(-1/2))^(-1)>=I+H^(-1/2)TH^(-1/2); the second uses (D+sI)^(-1)>=(1+s)^(-1)I. Integrating the logarithm resolvent difference proves (1). No commutativity of C and V is used. All terms at s>0 are actual channel terms.

## WH3 receiving interface

For an actual effect A with A psi=psi, set Z=N(A), B=E(A), C=N^2(A)=(A+3B)/4. Self-adjointness of N gives the exact equality

g(A,P)=<psi,(log B-2log C)psi> +2<psi,(log C-N(log Z))psi>.

Thus a sufficient, still unproved, actual-source certificate is

<psi,(log B-2log C)psi>
+2 integral_0^infinity ||V^(1/2)(C+sI)^(-1)psi||^2 ds/(1+s) >=0.

The abstract first term can be negative under both index-nine effect inequalities. That does not falsify the actual anchor: the omitted nonnegative second term is physically fixed by the same A and N, not freely adjustable. Conversely this variance lower bound may be too weak; no assertion that it always pays the negative first term is made.

Support issue for WH3: NP<=NA and P<=A imply finite original anchor. C>=A/4 supports psi, so <psi,log C psi> is finite. The weighted N(log Z) is finite from NP<=Z. Hence both sides of the exact scalar decomposition are well-defined, and the nonnegative resolvent integral has a finite quadratic-form limit in psi.

## Explicit finite spectral evaluation, without quadrature

If C has positive eigenvalues c_i and V is expressed in that eigenbasis, the variance payment matrix has entries h(c_i,c_j)V_ij, where

f(c)=log(c)/(c-1), f(1)=1,
h(c,d)=(f(c)-f(d))/(d-c) for c!=d,
h(c,c)=(log(c)-1+1/c)/(c-1)^2, h(1,1)=1/2.

These formulas follow by partial fractions of the defining integral; h is positive semidefinite as a Gram kernel of s->(c+s)^(-1) in measure ds/(1+s). Thus the map V->h(C,C) Schur V is positive, and no entrywise sign test is used. For singular C use positive-floor limits in supported quadratic forms, as above. This supplies an executable exact-log finite-dimensional payment for discriminating whether the variance lower bound itself suffices.
