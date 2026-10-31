# A stronger mediated-network obstruction: (A,total) is insufficient for geometric Foster drift

Consider the abstract count network

    0 <-> A;
    A+B <-> B+C;
    A+C <-> 2B;
    B+C <-> 2C,

with all rates positive. Write lambda,d for immigration/death and alpha2 for
A+C->2B. Let N=A+B+C. This statement is independent of complex balance.

**Proposition.** No positive normlike function of the form V(x)=F(A,N) can
satisfy `LV<=-epsilon V+C` at all states for constants epsilon>0 and finite C.
This excludes arbitrary positive F, not only exponentials, capped corrections,
or separable radial factors. It does not exclude nongeometric additive Foster
criteria or functions resolving B and C individually.

**Proof.** Replacing epsilon by min(epsilon,lambda/2) and C by max(C,0) only
weakens the supposed inequality. Thus assume 0<epsilon<=lambda/2 and C>=0.
Put

    u_n=F(0,n), w_n=F(1,n), r=1-epsilon/lambda in [1/2,1).

At the pure-C state (0,0,n), the only enabled internal transition is
2C->B+C, which preserves both A and N. Hence the exact generator is

    LV(0,0,n)=lambda [w_(n+1)-u_n].

The supposed Foster inequality therefore gives

    w_(n+1)<=r u_n+C/lambda.                              (1)

At (1,0,n-1), n>=2, the only internal transition changing A is
A+C->2B, with intensity alpha2(n-1) and next value u_n. The reverse 2C->B+C
again preserves A,N. Using positivity to discard the nonnegative arrival-value
and death-value terms from the core yields

    LV(1,0,n-1)>=alpha2(n-1)u_n
                  -[alpha2(n-1)+lambda+d]w_n.

Combining with the supposed upper bound -epsilon*w_n+C gives

    u_n <= [1+q/(n-1)] w_n + C/[alpha2(n-1)],
    q=(lambda+d-epsilon)/alpha2>0.                       (2)

Substitute (1), indexed by n-1, into (2). For sufficiently large n,
`r[1+q/(n-1)] <= rho=(1+r)/2 <1`. The remaining additive term is uniformly
bounded, for example by

    M=(1+q)C/lambda+C/alpha2.

Thus `u_n<=rho*u_(n-1)+M` for all sufficiently large n. Iteration bounds u_n
uniformly. But normlikeness along (0,0,n) requires u_n->infinity. Contradiction.

This ordinary proof is stronger than the separable `t^N H(A) phi(N)` obstruction
and explains why the weighted mediator correction is structurally useful: it
resolves B versus C even at equal A and N. A corrector depending only on the
regenerating species and total count cannot provide a global geometric Foster
bound for this triangle.

All statements are purely mathematical. No historical novelty or general
weak-reversibility conclusion is asserted.
