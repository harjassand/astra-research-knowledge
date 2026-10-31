# Independent main-agent review and closed-class strengthening of the aggregate no-go

## Binding and verdict

Accepted the independently authored proposition in `MEDIATED_AGGREGATE_NO_GO.md`, SHA256

    f53a4d50e83a4b645f5cde8304fece51d092a53ccdbcaf4294fa94326f9b9aa6

The original author file is preserved at `stochastic_last_copy_independent_20261031/MEDIATED_AGGREGATE_NO_GO.md`; the copy in this package is byte-identical. This review independently reconstructs the proof and supplies its positive-satellite closed-class scope. It is an internal mathematical review, not external refereeing or priority clearance.

## Independent reconstruction

Assume V=F(A,N)>0 is normlike and LV<=-epsilon V+C. Reducing epsilon to at most lambda/2 and increasing C to max(C,0) preserves this upper bound. Set u_n=F(0,n), w_n=F(1,n), r=1-epsilon/lambda in[1/2,1).

At pure C state(0,0,n), all internal jumps preserve A,N. Hence

    lambda(w_(n+1)-u_n)<=-epsilon*u_n+C,
    w_(n+1)<=r*u_n+C/lambda.

At(1,0,n-1), the only internal A-changing channel is A+C->2B, with rate alpha2(n-1). The other enabled internal channel2C->B+C is invisible to F. Immigration and death have nonnegative destination values. Discarding those destination terms gives the lower bound

    LV >= alpha2(n-1)u_n-[alpha2(n-1)+lambda+d]w_n.

Combining with the assumed upper bound yields

    u_n <= (1+q/(n-1))w_n+C/[alpha2(n-1)],
    q=(lambda+d-epsilon)/alpha2>0.

Substitution gives a scalar contraction u_n<=rho*u_(n-1)+M for every sufficiently large n, with rho=(1+r)/2<1 and finite M=(1+q)C/lambda+C/alpha2. Iterating bounds u_n. Normlikeness on the pure-C ray requires u_n->infinity, a contradiction.

Every sign and index was checked. Positivity, not integrability or regularity of F, justifies dropping the two core destination terms. The generator has finitely many finite-rate outgoing channels at each fixed state, so the argument requires no prior stationary distribution. The proof excludes global geometric Foster drift (and its outside-finite-set equivalent), not all additive, sampled-time, excursion, or path-based recurrence criteria.

## The contradiction occurs inside one positive-satellite closed class

It is not an artifact of combining a zero-satellite class with a different class. Write C^n for count state(0,0,n). All arrows below are enabled transitions with positive probability; their reverses are also available.

A path connects C to3C:

    C -> A+C -> 2B -> A+2B -> 2B+C -> B+2C -> 3C.

A path connects2C to3C:

    2C -> A+2C -> A+B+C -> B+2C -> 3C.

For every n>=2, a path connects C^n to C^(n+1):

    C^n -> A+C^n -> A+B+C^(n-1) -> B+C^n -> C^(n+1).

The second arrow uses2C->B+C, the third A+B->B+C, and the fourth B+C->2C. Thus every pure-C state with n>=1 belongs to the same communicating class Gamma containing C. Reversibility makes Gamma closed. For n>=2, immigration from C^(n-1) reaches(1,0,n-1), and its further immigration/death destinations also lie in Gamma.

Therefore every state and destination used in the contraction proof for sufficiently large n lies in this **one** closed communicating class. The proposition remains true for a positive normlike F(A,N) defined only on Gamma and a Foster inequality required only there. No classification of every other positive-satellite state is needed.

The A-only states B=C=0 form a separate closed immigration/death class. Their existence neither helps nor harms this no-go. The constructive weighted-mass theorem remains classwise and covers both.

## What information is necessary, and what is not claimed

The result says that a geometric one-step Foster function must distinguish some states with the same A and N but different mediator composition. It does not say that full-state coordinates are mandatory: the acquired aggregate P=A+eta B together with N suffices for the constructive proof. Thus two poorly chosen aggregate coordinates fail while two differently chosen coordinates succeed.

No impossibility of all finite abstractions, all recurrence proofs, or all unbounded corrections is inferred. No general weak-reversibility theorem or historical novelty is claimed.
