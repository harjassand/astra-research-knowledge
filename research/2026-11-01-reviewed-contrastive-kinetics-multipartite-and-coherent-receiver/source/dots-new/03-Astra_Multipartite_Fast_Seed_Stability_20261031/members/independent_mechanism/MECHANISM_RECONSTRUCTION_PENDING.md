# Complete-multipartite latent inventory: independent pending mechanism check

31 October 2026. No web or external retrieval is used. This is a new ordinary mathematical investigation, not an amendment to any accepted file and not a whole-source acceptance receipt.

## Useful result

The proposed overlapping-hub mechanism survives the boundary/tie/rate challenge. The old dominant part remains a maximizer after every enabled jump whenever R<N/2, even if the destination develops a tie. The adversarial order-NR reverse-arm terms can be paid source-by-source by amplification. All other adverse inverse terms are O(R²), so become bounded after inverse normalization. An angular A/N correction then pays the interior. A free passenger is an exact negative control for this particular candidate, so the all-satellites-in-the-hub-graph condition is substantive.

## Geometry

Let the complete multipartite hub graph have parts indexed by i, with count totals z_i. Put N=A+Σz_i, M=max z_i, R=N−M, and P=(1+η)R−ηA=A+(1+η)(R−A), with 0<η<=1/16. Thus R<=P<=(1+η)R. Each internal destination has A>0 or a cross-part hub; consequently it cannot have R=0. At R=0 all internal source propensities vanish. Immigration/death changes P by exactly +1/-1.

Every internal jump has |Delta P|<=1+2η<2, including ties in the maximum. For enabled jumps from R>=1, P,P'>=1; hence P/P'<=3 and

    |1/P'−1/P| <= 6/P².

### Exact strict-boundary table

If R<N/2, M>R and the dominant part d is unique. It remains a maximizer after each enabled jump. In the potentially delicate capture A+X_d→hub off d, M falls by one but each other part increases by at most one; A>=1 gives old other total<=R−1, so no other part exceeds M−1. In a cross-hub reverse arm returning X to another part, one other-part particle is removed before one is added; every new other-part total remains<=R−A<=M−1. The remaining channels are immediate. Destination equality is allowed.

The following table is therefore exact, not a differentiable approximation to max:

| Channel | Incidence | Delta P |
|---|---|---:|
| 2A→hub | hub touches d | -1+η |
| 2A→hub | hub avoids d | 2η |
| hub→2A | hub touches d | 1-η |
| hub→2A | hub avoids d | -2η |
| A+X→hub | X in d, hub touches d | η |
| A+X→hub | X in d, hub avoids d | 1+2η |
| A+X→hub | X outside d, hub touches d | -1 |
| A+X→hub | X outside d, hub avoids d | η |
| hub→A+X | reverse of the preceding arm | negative of its Delta P |

## Rate reconstruction and boundary inverse inequality

Let a be the sum of 2A→hub constants, k_X each satellite's total forward arm constant, k_- and k_+ their extrema, b_h each hub→2A constant, b_- their minimum, s_h the total reverse rate constant from a hub including b_h, and S the sum of all internal rate constants. All are acquired finite raw sums. Put s_+=max s_h and

    η=b_-/(16s_+),
    c0=min(η k_-/3,b_-/4),      gamma=c0/(1+η).

Every dominant-part capture increases P by at least η, at total rate at least k_- A M. Its negative inverse drift is at least η k_- A M/(3P²).

For a cross hub, amplification increases P by1−η and supplies inverse drift at most −(1−η)b_h/(2P²). The only adverse order-MR reverse arm returns X to d and decreases P byη. Its positive inverse magnitude is at most2η/P² times its rate. Since η s_+<=b_-/16, their source-wise total leaves at least b_h/(4P²) negative amplification drift. Complete multipartiteness gives total cross-hub source product M(R−A).

Every other adverse inverse channel has a source propensity bounded by its constant times R²: 2A sources, A times a non-dominant satellite, or an entirely non-dominant hub. Their combined inverse drift is at most6S. Thus

    L_int(1/P) <= -c0 M R/P²+6S
                 <= -gamma (N−R)/P+6S,       R<N/2.

Globally, the absolute-jump bound and source orders give

    L_int(1/P) <= 6S N²/P².

## Angular and physical core joins

Write Q=Σ_(i<j) z_i z_j, F0=2a+k_+, b0=min_h(s_h+b_h), and D=mu(1−1/t). Exact raw A drift gives

    L_int A >= b0 Q−F0 A N.

For epsilon=min(1/2,D/(4F0)), define h=1+1/P−epsilon A/(N+1) at R>=1, and h0=4t at R=0. Then1/2<=h<=2 on the active region and the global upper bound is H=4t. The boundary value is not obtained by differentiating 1/P through zero.

Immigration's angular contribution is nonpositive. For death, its positive angular contribution is bounded by epsilon D A plus epsilon mu; retaining D here is essential when t is near1. The inverse/core contribution is at most -D A plus a finite constant: at P>1, a death-enabled state has P>=2; at P=1 necessarily A=R=1, and the h0 destination is evaluated directly. These estimates give the safe bound

    t^(-N)LW <= B+L_int(1/P)−D A/4−epsilon b0 Q/(N+1),
    B=2lambda(t−1)+5mu.

At R=0, the exact immigration drift is at most -lambda h0/2. No death clock, stationary fiber law, ODE or first-activation estimate is supplied.

## Closing the two regions constructively

Choose

    delta=min(1/4,gamma/[2(1+η)(B+6S+1)]).

For1<=R<=delta N, the boundary inverse term pays B+6S with at least unit margin. If R>delta N, its positive part is bounded by6S/delta². Either A>=delta N/2, yielding negative death drift at least D delta N/8, or A<delta N/2. In the latter case Q>=delta N²/(4q), where q is the number of parts: M>= (N−A)/q>N/(2q), and Q>=M(R−A). Consequently the angular drift pays at least epsilon b0 delta N/(8q) for N>=1.

Thus kappa=delta/8 min(D,epsilon b0/q)>0 and

    N*=ceil[(B+6S/delta²+1)/kappa]

give scaled drift<=-1 on active states with N>=N*. Since active h<=2, zeta=min(1,lambda)/2 converts this to geometric drift; H=4t is only needed on the inactive face and for the finite exception. The count-conserving internal dynamics and Poisson immigration give ordinary nonexplosion. The reversible singleton paths supplied by the arm/amplification architecture give irreducibility. The usual stopped Foster argument then supplies recurrence and moments. These joins remain pending a frozen full-source/receiver audit, not a claim of new-to-literature results.

## Essential negative control

If a free passenger B is appended but is not included in any hub part, at pure-B states R=N and P=(1+η)N. Only immigration is enabled, and the candidate h tends to1 before and after that jump. Hence scaled LW tends to lambda(t−1)>0. The candidate therefore fails there, despite reversibility of an arm A+B↔hub. This excludes a tempting silent extension, not network stability or alternative inventories.

At triangle capacities(1,1,2), maximum-matching inventory can lose two on a hub removal; that example lies at R=N/2 and is deliberately handled by the interior angular term here. There is no conflict with the previously accepted sharp matching-inventory graph lemma.
