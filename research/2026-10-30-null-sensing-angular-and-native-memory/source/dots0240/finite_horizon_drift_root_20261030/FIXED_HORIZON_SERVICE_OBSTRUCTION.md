# Fixed-horizon CP averaging fails the uniform service requirement
2026-10-30 01:16 UTC. Root derivation; independent review requested.

The exact connected-commutator noise-transfer lemma remains valid. Its proposed finite-window service premise is NOT automatically available and, in the following elementary finite-rate controller, is false even with integrated W. This rejects plain time averaging as the native compiler bridge.

## 1. Independent two-stage controllers
At each of m sites, a rate-one classical chain goes ready -> primed -> corrected. Start all sites ready. A data defect is present in both ready and primed states and absent in corrected. The clean generator is strictly local, finite-dimensional, and removes defects without creating them. The probability that the defect remains at time t is

    s(t)=exp(-t)(1+t).

For theta in (0,1), a single occupancy factor is 1 before correction and theta afterward. Its expected value is

    g(t)=theta+(1-theta)s(t)=1-(1-theta)t^2/2+O(t^3).

For the full interval animal of size m, its expected weight is exp(am) g(t)^m. No quantum interference or shared environment is needed for the obstruction.

## 2. Actual full-animal potential on a path
Use ALL nonempty connected intervals of the m-site path:

    V=sum_A exp(a|A|) theta^(holes(A)),
    W=sum_A |A| exp(a|A|) theta^(holes(A)),   a>0.

Thus

    E V(t)=sum_(ell=1)^m (m-ell+1) exp(a ell) g(t)^ell,
    E W(t)=sum_(ell=1)^m ell(m-ell+1) exp(a ell) g(t)^ell.

Every clean correction makes both V and W decrease pointwise. Initial V grows exponentially in m, and W(0)/V(0) grows linearly in m. Therefore V(0)-E V(T)<=V(0) immediately rules out a uniform positive alpha in

    V-exp(TL)V >= alpha W - b m I.

The additive linear term does not repair this: b m/V(0) tends to zero.

## 3. Integrated W also fails
For 0<=t<=m^(-1/2), use 1-s(t)<=t^2/2 (integrate u exp(-u)<=u). Hence g(t)>=1-(1-theta)/(2m), and g(t)^ell is bounded below by a positive constant for every ell<=m.

The contribution to V(0) of intervals with ell>=m/2 tends to one: the omitted part is at most a polynomial in m times exp(am/2), whereas V(0)>=exp(am). Consequently for sufficiently large m and t<=m^(-1/2),

    E W(t) >= c m V(0).

For ANY fixed T>0, once m>=T^(-2),

    integral_0^T E W(t) dt >= c sqrt(m) V(0).

But the total V decrement is at most V(0). Thus no volume-independent alpha>0,b<infinity can satisfy

    V-exp(TL)V >= alpha integral_0^T exp(tL)W dt - b m I.

This is a concrete bounded-rate two-stage startup obstruction. A controller with p sequential startup stages analogously gives t^p startup and integrated W scaling m^(1-1/p) V(0).

## 4. What it changes
An exact positive time average F_T=integral exp(tL)V dt has derivative exp(TL)V-V, but its noise sensitivity is governed by the much larger integrated W. Small fixed T does not solve the asymptotic mismatch. Thus even the proposed integrated-W repair is insufficient.

The phase-dependent multiplicative CP credit of the reviewed simple compiler avoids this particular reasoning: it changes each animal's controller weighting locally rather than averaging a common startup time across arbitrarily many sites. A native controller proof must construct an analogous local service weight (or a different mechanism). It cannot be obtained from the reset tail and raw monotonicity alone by fixed-horizon averaging.

Scope: exact counterexample to these generic service inequalities, not an impossibility theorem for autonomous quantum memory or for all adaptive/state-dependent smoothing. The example is not itself an FGL code. Large admissible error clusters in a code would require separate geometry/basin embedding to transfer this exact counterexample to that family. As an abstract implication from locality, monotonicity and finite reset service, the proposed argument is disproved.
