# Acquiring normalized regenerative mass across accelerated last-copy loss

## Result and the obstruction actually crossed

Consider the three-species weakly reversible network

    0 <-> A,
    A+B <-> B+C,
    A+C <-> 2B,
    B+C <-> 2C.                                           (1)

At A=1,B=0,C=n, the reaction A+C->2B erases the last A at rate proportional to n. At A=B=0,C=n, the only internal move creates B, not A. Thus the relevant restoration is mediated: C first creates B, which helps restore the dissipative coordinate A.

Neither a fixed-rate token certifying A-occupancy nor an arbitrary one-coordinate correction t^N H(A) can solve this obstruction. First activation of A itself is easy—immigration has constant positive rate. The missing operation is controlling composition and dissipation after activation, amid accelerated last-copy loss.

The construction acquires a weighted mass P=A+v_B B+v_C C, then uses the globally defined rational correction

    W(x)=t^N [1-epsilon P(x)/(N+1)].                       (2)

The weights are found from the raw generator by a finite exact coefficient LP, not supplied as a useful premise. A quadratic boundary-production inequality converts fast conservative restoration into negative order-N drift. No stationary fiber law, return-clock oracle, asymptotic averaging theorem, or assumed favorable decomposition is used.

**Main soundness theorem.** Every positive certificate returned by the raw-list algorithm below yields exact rational constants C0,kappa>0 such that

    LW/W <= C0-kappa N                                    (3)

at every integer state. Consequently every reachable class is nonexplosive and positive recurrent, and its invariant law has all finite exponential total-count moments. The same acquired weight vector can be used for every requested rational t>1.

**Acquisition scope.** The unbudgeted finite basis enumeration decides positivity of the stated linear-composition cone. It is not complete for stable networks. For the particular mediated family (1), an explicit positive cone witness proves that acquisition succeeds for every choice of positive rational rates. A declared finite basis budget may return UNKNOWN.

Read the separate exact independent-review binding. No historical novelty, general weak-reversibility solution, operational chemistry, or efficient universal algorithm is claimed. Earlier accepted packages are unchanged.

## 1. Raw list and coefficient extraction

The input is a finite positive-rational-rate mass-action list on n=m+1 species with m>=1 (equivalently n>=2). The receiver asserts n>=2; the separate n=1 immigration-death case is outside this certificate implementation. The finder enumerates the distinguished species A. For that candidate it requires:

- All non-conservative reactions are exactly 0->A and A->0, with aggregate positive rates lambda,d.
- Every other non-null reaction preserves total count N.
- The full reaction graph is weakly reversible.

No roles are supplied. The other species are B_1,...,B_m. A general conservative internal channel is allowed in the raw list; the certificate constraints below decide which ones the weight can handle.

For a tentative weight vector v with v_A=1 and 0<=v_j<=1, define P(x)=v dot x. For every unary or binary source complex u, acquire the aggregate weighted drift coefficient

    c_u(v)=sum_(r with source u) kappa_r v dot (u'_r-u).   (4)

Thus the corresponding contribution to L_internal P is c_u(v)(x)_u. Reactions of higher order are handled only if the acquired v makes their individual weighted increments zero.

## 2. A finite exact cone, not a supplied mass oracle

The LP variables are v_1,...,v_m and beta. Fix v_A=1 and impose

    0<=v_j<=1,     0<=beta<=M,
    c_(2B_j)(v)>=beta                    for every j,
    c_(B_j+B_k)(v)>=0                    for every j<k,    (5)
    v dot (u'-u)=0                      for each internal
                                            source of order>2.

Absent source coefficients are zero. One explicit finite upper bound is
M=max(1,2 sum_(binary internal channels)kappa_r). It does not exclude a positive feasible point: with 0<=v<=1, the weighted increment of a binary reaction is at most2. The all-ones v and beta=0 are always feasible because every internal reaction conserves total count.

The prototype converts (5), including paired inequalities for equalities, into rational affine inequalities. With dimension m+1, it enumerates every subset of that many constraint rows, solves the corresponding exact rational system, skips singular bases, and checks every remaining inequality and beta>0. It returns the first exact positive feasible vertex.

This unbudgeted procedure is complete for positivity of (5). The feasible polytope is compact and nonempty. If it contains a point with beta>0, the maximum of beta is positive and attained at an extreme point. At an extreme point the active constraint normals span the full ambient space, even if the polytope has lower dimension; otherwise a small two-sided displacement would preserve all constraints and contradict extremality. Thus some enumerated nonsingular active basis gives a positive feasible vertex. Conversely every accepted point is explicitly verified.

The implementation charges singular and nonsingular attempted bases, total candidate bases, constraint count, dimensions and maximum solved fraction size. Budget exhaustion is UNKNOWN. Full exhaustion proves only that this specified algebraic cone has no positive beta, not that the network is unstable. There is no floating LP proposer or hidden weight oracle here.

## 3. The acquired regenerative production inequality

For a verified v,beta, set

    K1=max(0,max_(unary sources u)[-c_u(v)]),
    K2=max(0,max_(binary sources u containing A)[-c_u(v)]).

These are finite raw coefficient computations. Write a=x_A, b=sum_j x_(B_j), so N=a+b. Every positive boundary mixed coefficient can be discarded from a lower bound. The pure boundary sources give at least beta sum_j(b_j)_2. Unary negative contributions are at least -K1 N. Negative binary sources containing A give at least

    -K2[(a)_2+a b] >= -K2 a N.

All higher-order weighted increments vanish individually by (5). Therefore

    L_internal P >= beta sum_j b_j(b_j-1)-K2 a N-K1 N.    (6)

This is the structural principle: production of dissipative weighted mass is quadratically coercive on the boundary A=0, while adverse production away from that boundary is controlled by the available A mass. It is acquired from finite reaction coefficients, not from an assumed stationary distribution.

Also a<=P<=N, a consequence of the verified weight bounds.

## 4. Constructing a global normalized-composition function

For any rational t>1 define

    D=d(1-1/t)>0,
    epsilon=min(1/2,D/(4K2)) if K2>0, else epsilon=1/2,
    h(x)=1-epsilon P(x)/(N+1),
    W(x)=t^N h(x).

Then 1-epsilon<=h<=1, so W is positive and normlike and is uniformly comparable to t^N. The correction is bounded; its variation with composition is small but not confined to finitely many service-count layers.

### Immigration and death

An A immigration increases both P and N by1. Since P<=N,

    (P+1)/(N+2)-P/(N+1)=(N+1-P)/[(N+1)(N+2)]>=0.

Thus h after immigration is at most h before it, and immigration contributes at most lambda(t-1) to LW/W.

For a>=1, an A death changes P to P-1 and N to N-1. The h increment is

    epsilon (N+1-P)/[N(N+1)].

Its total quotient contribution is at most

    -D a + d epsilon/[t(1-epsilon)],                     (7)

because a(N+1-P)<=N(N+1). There is no death term at N=0.

### Internal reactions

Internal reactions conserve N. Since h is affine in P at fixed N, their exact contribution is

    -epsilon L_internal P/[(N+1)h].                      (8)

Using (6), h>=1-epsilon, h<=1, and sum b_j^2>=b^2/m gives

    internal quotient
       <= epsilon K2 a/(1-epsilon)
          +epsilon(K1+beta)/(1-epsilon)
          -epsilon beta b^2/[m(N+1)].                    (9)

To verify the last two terms carefully, sum_j(b_j)_2=sum_j b_j^2-b. The negative squared term is bounded using h<=1, and the positive linear remainder using b/(N+1)<=1 and h>=1-epsilon. No invalid real-valued replacement of falling factorials is made.

The choice of epsilon guarantees epsilon K2/(1-epsilon)<=D/2. Hence, with

    C0=lambda(t-1)+d epsilon/[t(1-epsilon)]
                     +epsilon(K1+beta)/(1-epsilon),

we have

    LW/W<=C0-(D/2)a-epsilon beta b^2/[m(N+1)].             (10)

For N>=1, either a>=N/2, giving dissipation at least D N/4, or b>N/2, giving b^2/(N+1)>=N/8. Therefore (3) holds with

    kappa=min(D/4,epsilon beta/(8m))>0.                   (11)

At N=0 the actual immigration quotient is at most lambda(t-1)<=C0, so (3) also holds there. This is one global inequality, not a patch assembled from unverified boundary limits.

## 5. Explicit Foster bound and all-exponent scope

Choose zeta=kappa and

    R=max(1,ceil((C0+zeta)/kappa)),
    C_F=(C0+zeta)t^R.                                    (12)

For N>=R, (3) gives LW<=-zeta W. For N<R, W<=t^R, so LW+zeta W<=C_F. Thus

    LW<=-zeta W+C_F                                      (13)

globally. The constant can be expanded when its declared bit budget permits, or stored as an exact rational-power expression with its exponent and conservative unreduced bit bounds. No enumeration of all finite exception states is necessary.

Nonexplosion already has a simpler conventional proof in this raw class: only constant-rate immigration increases N; internal reactions conserve it and A death decreases it. Thus N(t) is bounded above by its initial value plus the immigration Poisson count. On each finite-time realization the chain stays in a finite count set with bounded rates. The normlike Foster proof independently gives the same conclusion; neither is presented as a new nonexplosion principle.

Weak reversibility gives feasible return paths for every enabled jump, so communicating classes are closed. The Foster bound gives classwise positive recurrence. Global irreducibility is not assumed.

To justify stationary moments without circular integrability, stopped exponential Dynkin gives P_tW<=aW+b with a<1. Invariance and concavity of min(W,n), followed by Fatou with the difference bounded below by -b, give pi(W)<=C_F/zeta. Since W>=(1-epsilon)t^N, the invariant t^N moment is finite. For every requested exponent theta, choose rational t>exp(theta) and repeat the explicit scalar construction using the same acquired v,beta. This proves all finite exponential moments for each classwise invariant law; it does not claim uniform constants or computational cost across t.

## 6. The mediated family always has an acquired positive cone

Write the positive rates of (1) as:

    A+B -> B+C : alpha1;   reverse : beta1,
    A+C -> 2B  : alpha2;   reverse : beta2,
    B+C -> 2C  : alpha3;   reverse : beta3.

For proof of universal acquisition within this family, take

    eta=min(1/4,beta1/(2alpha3)),
    v=(1,eta,0).

The boundary coefficients are

    c_(2B)=beta2(1-2eta)>0,
    c_(2C)=beta3 eta>0,
    c_(B+C)=beta1-alpha3 eta>=beta1/2>0.                 (14)

Thus a positive beta exists for every choice of positive rational rates. The actual program does not receive this witness: it finds a positive vertex by the raw coefficient enumeration. Equation (14) proves that the unbudgeted search terminates positively for this family, not merely for the executed parameter choice.

For the executed instance all rates are1 except B+C->2C, whose rate is2. The raw scan acquires A after one candidate. Exact enumeration returns

    v=(1,1/3,0), beta=1/3,
    epsilon=1/8 at t=2,
    C0=47/42, kappa=1/384, R=431.

The search pays62 exact bases,41 nonsingular, with a3-variable/9-constraint LP and at most4-bit solved fractions. There are5,456 original exact generator-quotient checks and25 additional targeted states, including counts up to10^50. The implicit finite exception set contains13,436,856 possible count states, but none are silently enumerated: (12) bounds it analytically.

This network is not complex balanced. Core balance gives a=1. Balance at the leaf complex A+B gives c=a=1. Balance at2C gives c=2b, hence b=1/2. The separate linkage A+C<->2B would then require ac=b^2, a contradiction. It is also not strongly endotactic: in the all-ones direction every maximal quadratic complex has only total-conserving outgoing reactions, so none descends.

## 7. What the new joint coordinate resolves

### Fixed-rate A-occupancy tokens

At (1,0,n), the A+C->2B jump erases A at rate alpha2 n. Any coupled token whose occupied-A state certifies actual A>=1 must leave that state on every such jump. Its exit rate must therefore be at least alpha2 n for every n. No finite population-independent exit rate can do so. This excludes that fixed-rate occupancy-token comparison, not every possible adaptive or joint abstraction.

First A activation is not the hard quantity: direct immigration alone gives mean at most1/lambda. The failure concerns retention/clearance after activation.

### Any one-coordinate multiplicative correction fails here

Let

    U(a,b,c)=t^(a+b+c) H(a) phi(a+b+c),

where t>1, H(a)>0 is arbitrary, phi(N)>0, and phi(N+1)/phi(N)->1. This includes an arbitrary unbounded H(A) and the usual asymptotically flat polynomial radial factors.

Along (0,0,n), every enabled internal reaction leaves A and N unchanged. The generator quotient tends to lambda[t H(1)/H(0)-1]. Any eventual negative Foster drift requires H(0)>=t H(1); if that inequality fails the quotient is bounded positively away from zero.

Along (1,0,n), A+C->2B contributes

    alpha2 n[H(0)/H(1)-1] >= alpha2 n(t-1)>0.

Every other enabled internal reaction leaves A and N unchanged, while immigration/death quotients stay bounded because phi's adjacent ratios tend to1. Thus LU/U tends to positive infinity on this ray. No finite-C geometric Foster inequality, nor an eventual constant negative drift, can hold for this U. This is a precise ansatz obstruction, not a claim that all conventional Lyapunov methods fail.

Plain normalized P=A also fails: at (0,0,n), the internal generator of A is zero and its immigration quotient tends to lambda(t-1)>0. In contrast, the acquired P=A+eta B decreases the Lyapunov function as 2C creates the mediator B. Its order1/N composition gradient turns a quadratic creation rate into order-N dissipation while avoiding the order-N last-copy penalty of a fixed jump in H(A).

### Strong ordinary comparators are retained

For the easier direct-return star family0<->A, A+B_j<->2B_j, an ordinary unbounded service-radial g(A) correction also works by Young's inequality. Normalized composition is not uniquely necessary there. The mediated network above was selected precisely because that whole one-coordinate multiplicative class fails, not merely because an old parser did not recognize it.

## 8. Same-input compiler comparisons and honest limits

The unchanged prior unified pivot/terminal-gap compiler returns UNKNOWN on the mediated example after3,188 exact terminal-cone basis candidates. Its uniform all-ones obstruction on the quadratic linkage classes is explicit in `baseline_results.json`. The preserved protected-family and partial-row coverage recognizers also reject the same raw list. Those outcomes are restrictions of the respective sufficient architectures, not instability evidence.

The present cone test is likewise restricted. A stable complex-balanced network can fail it when a pure satellite quadratic source is absent, even if indirect unary mixing restores that species. Full cone exhaustion is not a general recurrence decision. Higher-order channels are accepted only when the acquired weight makes them individually neutral. No claim covers arbitrary mass-conserving nonlinear interactions or general weak reversibility.

The finite coefficient LP, quadratic inequalities, normalized-composition correction and Foster machinery are conventional mathematical ingredients. Their exact raw-list acquisition and the mediated-boundary proof are the constructed result. No exhaustive historical priority search has been completed. All work is mathematical and non-operational.
