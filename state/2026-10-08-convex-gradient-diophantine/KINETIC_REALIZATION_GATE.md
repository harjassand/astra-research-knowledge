# SOS-clock realization gate: a stable kinetic polynomial flow without a weakly reversible realization

**Internal algebraic counterexample, 2026-10-08.** A direct consequence of the classical geometry of source exponents, not a claim of historical originality. Scope: **dynamical equivalence without auxiliary species**, ordinary finite mass-action networks with positive rate constants.

## Exact flow and kinetic realizability

Take

    M(x,y)=(x-y)^2 >=0,
    dx/dt=M(x,y)(1-x),
    dy/dt=M(x,y)(1-y).

These are polynomial ODEs on (0,infty)^2. Both coordinates are monotone toward 1, so every positive orbit remains in a compact positive rectangle and converges to an equilibrium. The potential `V=((x-1)^2+(y-1)^2)/2` is globally 1-strongly convex and satisfies `dV/dt=-M||grad V||²`. The equilibrium set contains the entire positive diagonal x=y, and (1,1) is the unique minimum of V.

Expanded:

    F_x = -x³+2x²y+x²-xy²-2xy+y².
    F_y = -x²y+x²+2xy²-2xy-y³+y².

This flow **does** have an ordinary kinetic mass-action realization: for each positive coefficient `+k x^alpha` in coordinate i, use a reaction `alpha -> alpha+e_i` of rate k; for each negative coefficient `-k x^alpha` use `alpha -> alpha-e_i` of rate k. Every negative monomial in F_i contains its consumed species, so all target complexes are nonnegative. This realizes the polynomial vector field exactly, although the resulting network need not be reversible.

## No weakly reversible dynamically equivalent network (without auxiliaries)

**Lemma (maximal-source direction).** Let a finite polynomial vector field F be realized by a weakly reversible mass-action network. For any linear functional w on the exponent/source space and any monomial support exponent alpha of F whose w-weight is **maximal among all monomials with nonzero vector-field coefficient**, it is impossible that `w dot [x^alpha]F >0`. Here `[x^alpha]F` is the coefficient vector of that monomial.

**Proof.** Consider a weakly reversible component containing the source alpha. Let h be the maximum w-weight of its complexes. If h exceeded the maximum weight H of the nonzero-coefficient support of F, then some source on the h-maximal face must have an outgoing edge to smaller weight (a directed return path from any lower complex to this component ensures such an edge in a strongly connected component). Its net w-drift would be strictly negative, because every outgoing edge from a maximizer has nonpositive w-projection. But F has no monomial coefficient at weight h>H. Contradiction. Thus no component producing the coefficient at alpha can contain a source of weight exceeding H; consequently the w-projection of its contribution at alpha (weight H) is <=0. Contributions from all other components at alpha are also <=0. Hence w dot coefficient <=0. QED.

Apply with w=(1,1). All nonzero coefficient monomials of F have total degree <=3. At alpha=(2,1), total degree 3, the vector-field coefficient is

    [x²y]F = (2,-1),
    w dot [x²y]F = 1 > 0.

This violates the maximal-source condition, proving **there is no finite weakly reversible mass-action realization dynamically equivalent to F on the same species x,y**, even though F is kinetic, SOS-clock, monotone, bounded, and Lyapunov stable.

### Exact audit

SymPy polynomial expansion, total-degree bound, coefficient (2,-1) and negative-monomial consumption condition were replayed independently. This is a finite algebraic check, not a proof assistant or specialist audit.

### Boundary and significance

The failure is stronger than the simpler claim that an arbitrary nonnegative polynomial multiplier need not satisfy kinetic coefficient sign constraints: this example **is kinetic** but admits **no weakly reversible realization** on the original two species.

The lemma is a standard necessary geometric consequence of weak reversibility / endotacticity, not a new literature breakthrough. It does **not** exclude a higher-dimensional **auxiliary-species embedding** with rational-point preservation and a normally attracting invariant fiber. That is the actual missing bridge if one hopes to carry the SOS-clock Hilbert-10 reduction to weakly reversible or reversible CRNs.

Sources: Boros–Craciun–Yu (2020), SIAM J. Appl. Math. 80(4):1936–1946, doi:10.1137/19M1303034; Deshpande–Jin–Kothari (2026), *Realizations Through Weakly Reversible Networks and the Globally Attracting Locus*, doi:10.1137/25M1745027 (necessary endotacticity for weakly reversible realization).
