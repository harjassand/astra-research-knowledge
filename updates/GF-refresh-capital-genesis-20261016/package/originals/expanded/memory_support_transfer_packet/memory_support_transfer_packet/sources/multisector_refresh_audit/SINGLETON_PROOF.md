# Exact one-node K-bad-sector endpoint bound

Date: 2026-10-16. Mathematical audit; not a device qualification or priority claim.

## Frozen source prerequisites

- imperfect_refresh_product/PROOF.md SHA256: 85cd5d2ec30f51de87c292092f047eb240dc596c8a0e5b15cfac1f84db6c7262
- /workspace/shared/measurement_randomizer_bridge/PARTIAL_DEPHASING_BOUNDARY_THEOREM.md SHA256: 5ffa0063d83ac1917f1286f8463182a94343274eb2d75b24368c3c49a7fc6240

## Contract and theorem

Orthogonal projectors P_0,...,P_K resolve identity, K>=1. P_0 is good and P_bad=sum_{j>=1}P_j. Begin in the good sector. There are two gaps with good/bad-odd interaction norm-action budgets a,b, arbitrary good/bad-preserving baseline, and one specified intervening full joint channel

T(rho)=eta rho+(1-eta)sum_{j=0}^K P_j rho P_j, 0<=eta<=1.

All persistent bath/reference factors are part of this specified contract. The discarded node environment is inaccessible. Let p=sin^2(min(a,pi/2)), q=sin^2(min(b,pi/2)), Q=p+q-pq, lambda=eta+(1-eta)/K. The sharp endpoint bad probability, over sufficiently rich finite sector dimensions, is

F_K=Q+max_{0<=c<=1}[-lambda p q c^2+2 eta sqrt(pq(1-p)(1-q))c].

For 0<p,q<1, c*=min(1,eta sqrt((1-p)(1-q)/(pq))/lambda). Thus F_K=Q+(eta^2/lambda)(1-p)(1-q) if eta^2(1-p)(1-q)<=lambda^2pq; otherwise F_K=p+q-(1+lambda)pq+2eta sqrt(pq(1-p)(1-q)). Endpoint values are F_K(0,q)=q, F_K(p,0)=p, and F_K=1 if either argument is 1.

## Upper proof

Purify good/bad-preserving gap operations, retaining their environments as references. Immediately before the node the pure state is sqrt(1-w)u+sqrt(w)v, with u good, v bad, both normalized, and 0<=w<=p by the one-gap sine theorem. Write v_j=P_jv. For every x,

sum_j |<x,v_j>|^2 >= |sum_j<x,v_j>|^2/K,

so sum_j|v_j><v_j| >= |v><v|/K. The node good block remains (1-w)|u><u|, its cross block is multiplied by eta, and its bad block dominates w lambda |v><v|.

Purify the second gap into an isometry U and put A=P_good Uu, B=P_good Uv, r=||A||^2, t=||B||^2. The one-gap bound in both entering parities gives r>=1-q and 0<=t<=q. Positivity and Cauchy-Schwarz lower-bound final good probability by

h=(1-w)r+w lambda t-2eta sqrt(w(1-w)rt).

For fixed r the minimizing t is min(q,eta^2(1-w)r/(w lambda^2)). On its uncapped branch minimized h=(1-eta^2/lambda)(1-w)r. On its capped branch the derivative in r is (1-w)-eta sqrt(w(1-w)q/r). At the transition it is (1-w)(1-eta^2/lambda)>=0, and it increases thereafter. Here lambda>=eta>=eta^2. Hence r=1-q minimizes. Substituting t=q c^2 gives the asserted F_K(w,q).

Increasing q enlarges the relaxed rectangle, so F_K(w,q) is nondecreasing in q. The explicit formula is symmetric in w,q, hence also nondecreasing in w. Therefore w<=p gives F_K(w,q)<=F_K(p,q). Degenerate endpoints follow directly or by continuity.

## Equality witness

Take one good basis state u, one bad basis state e_j in each P_j, and an extra bad state z orthogonal to every e_j, placed in any existing bad sector. Set v=sum_j e_j/sqrt(K), and w_vec=c v+sqrt(1-c^2)z. Drive only |u><v|+|v><u| to angle arcsin(sqrt(p)) in the first gap, then apply the specified node, then drive only |u><w_vec|+|w_vec><u| to angle arcsin(sqrt(q)). Baseline is zero. Both generators are Hermitian good/bad-odd of norm one. The bad node state is p[eta|v><v|+(1-eta)sum_j|e_j><e_j|/K]. Its expectation in w_vec is p lambda c^2. Direct evaluation yields Q-p lambda q c^2+2eta sqrt(pq(1-p)(1-q))c, attaining the upper bound.

This construction needs K+2 total dimensions generically. Fixed smaller sector dimensions retain the upper bound but need not attain it. When c=1 no extra sink is necessary.

## Consequences and boundaries

K=1 recovers the binary result. With a=b=pi/6 and eta=1/2, F_K=19/32-1/(32K): K=2 gives 37/64, strictly above binary 9/16. Thus binary sharp constants cannot be silently transferred to a full finer pinch.

As K tends to infinity lambda tends to eta. For eta>0, pulling eta outside the maximization shows the limit is (1-eta)Q+eta sin^2(min(a+b,pi/2)). Eta=0 follows separately. Thus the retained-pinch mixture bound is a sharp supremum over unbounded finite sector counts.

The singleton proof allows baselines preserving only good versus total bad. Such baselines need not commute with the fine pinch; do not move them through that node unchanged. This document proves no coordinate product theorem, syndrome-history support theorem, or hardware implementation claim.
