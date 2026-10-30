# The acquired rank is the sharp exponent of the abstract robust interface

30 October 2026. New abstract candidate, not a stronger chemical theorem. Fix the finite baseline/excess graphs and rate contract of ROBUST_FORCING_CONVERSE. Assume the rank finder succeeds and at least one type differs from a. Write r* for its output and L=max r*>=1. Define

    F(t)=inf_{initial type i, admissible freely chosen excess rates} P_i(X_t=a).

Then there are positive finite constants c,C such that for 0<t<=1,

    c t^L <= F(t) <= C t^L.                                  (S)

In particular the acquired rank is not merely one available exponent: it is sharp for this graph-only, arbitrary-rate robust terminal-forcing interface. This does NOT assert optimal exponents for a fixed raw network or across different pool partitions.

## 1. The finder returns the least valid rank

The completeness induction already proves more: for any valid integer rank r with target rank0, every node with r(i)<=k has been processed by round k. Hence r*(i)<=r(i) for every node. Since r* itself is valid, it is the componentwise least valid rank and minimizes the maximum rank. No numerical rate optimization is involved here.

The root progress-clock proof gives the lower half of (S), for example

    F(t)>=exp(-(Qmax+qmin)t)(qmin t)^L/L!,

where qmin is realized by selected strict-lower baseline edges and Qmax bounds total baseline rate.

## 2. Intermediate pruning records supply within-rank reset paths

Fix a type i with r*(i)=k>=2. Call it dangerous if it has a baseline edge into S_(k-2)={j:r*(j)<=k-2}, i.e. a jump that skips at least one rank.

Look at the algorithm's earlier round k-1, whose processed set is S_(k-2). This i was initially eligible in that round but was pruned, since it did not join rank k-1. Its recorded removal edge points to an already pruned node or an initially ineligible node. Following those recorded edges ends at a node with NO baseline edge into S_(k-2), and never visits a surviving rank-(k-1) node or an earlier processed node.

Every node along this path has rank at least k, because it lies outside S_(k-1). Every allowed excess edge is nonincreasing for the final valid rank, so starting at rank k forces the ENTIRE path to stay at rank k. Thus each dangerous type has a chosen within-rank excess path to a safe type whose baseline moves never decrease rank by more than one.

At each rank use the corresponding earlier-round parent records. Define d(i) as the length of its chosen path; safe types, a and rank1 types have d=0. Parent paths are acyclic by pruning order and have length at most n=|I|. Each selected excess move decreases d by exactly one and leaves r* unchanged. At a parent with the same rank, the same earlier-round record is used, so the distance assignment is consistent.

## 3. A finite-rate policy suppresses all baseline rank skips

Assign rate K to each selected parent edge and zero to other extras. This is a finite, time-homogeneous, nonexplosive control. Let D be the dangerous types. Globally,

    L d <= -K 1_D + n Qmax,

because a baseline jump changes d by at most n. Dynkin gives

    E integral_0^t 1_D ds <= n(1+Qmax t)/K.

A baseline rank-skip can occur only from D, with hazard at most Qmax. Thus

    P(at least one baseline rank-skip by t)
        <= n Qmax(1+Qmax t)/K.                              (E)

Chosen extras preserve rank exactly. On the complement of (E), each baseline jump decreases rank by at most one; upward baseline moves only delay arrival. Starting from any type with rank L, reaching a therefore requires at least L BASELINE jumps. Baseline uniformization supplies a rate-Qmax Poisson clock, independently of the excess implementation, and actual baseline jumps are a subset of its rings. Consequently

    P_i(X_t=a) <= P(Pois(Qmax t)>=L)
                   + n Qmax(1+Qmax t)/K.

Taking the infimum over the admissible finite-K policies and then K to infinity yields

    F(t) <= P(Pois(Qmax t)>=L) <= (Qmax t)^L/L!,

where the final inequality is the factorial-moment bound. This proves the upper half of (S). No infinite-rate process is invoked, and large expected hitting time alone is not used as a probability argument.

## 4. A nontrivial three-level witness

Use baseline edges 1->0, 2->0, 3->1, 4->0, 5->3, all at unit rates, with target0 and excess edges2->3 and4->5. The acquired ranks are0;1;2,2;3,3. Types2 and4 have direct target jumps, but arbitrarily fast allowed extras route them to3 and5 within their own rank before those shortcuts occur. Starting at rank3, the robust small-time exponent is3, not the ordinary shortest baseline distance1 from type4. This illustrates why the adversarial progress rank, rather than a fixed shortest path, is the relevant acquired quantity.

## Scope

The allowed control class may turn extras off and scale selected ones arbitrarily. Actual chemical remainder rates are fixed functions of population, so they need not realize the worst-case policy. The theorem sharpens the ABSTRACT interface and its rejection/success interpretation. It supplies neither a necessary chemical recurrence condition nor an optimal Lyapunov exponent for a concrete raw network. Face pool-neutrality and every global compiler guard remain separate.
