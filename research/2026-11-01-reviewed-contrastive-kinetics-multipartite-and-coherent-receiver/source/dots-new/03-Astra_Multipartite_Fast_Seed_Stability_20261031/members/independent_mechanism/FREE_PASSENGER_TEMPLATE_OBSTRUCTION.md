# Excluded free-passenger class: exact template obstruction

Pure mathematical negative control. No external source is retrieved and no accepted file is changed. This is not an instability claim.

Take the reversible four-species network

    0 <-> A;
    2A <-> C+D;
    A+B <-> C+D;
    A+C <-> C+D;
    A+D <-> C+D,

with arbitrary positive rates and immigration rate lambda. Its hub graph has one C--D edge and an isolated free passenger B. This network is admitted by the earlier biclique/free-passenger theorem; at all-unit rates it also has the ordinary detailed-balanced point(1,1,1,1). Thus positive recurrence is not in doubt from this negative control.

Try extending the present multipartite candidate without adding B to any hub part. Let the parts be {C},{D}, M=max(C,D), R=N−M, and P=(1+eta)R−eta A, with fixed eta>=0. For any fixed t>1, c>=0 and finite epsilon, use

    V=t^N[1+c/P−epsilon A/(N+1)]       when R>=1,

with any separate value on R=0. Assume the bracket is positive where needed. The proposed candidate has c=1 and small positive epsilon.

At x_n=(A,B,C,D)=(0,n,0,0), all internal channels and death are disabled; only immigration acts. Here N=R=n and P=(1+eta)n. At its birth destination, N'=n+1, A'=1, R'=n+1 and P'=P+1. Therefore the exact generator is

    t^(-n) LV(x_n)
      = lambda[(t−1)+c(t/(P+1)−1/P)−t epsilon/(n+2)].

As n→infinity this tends to lambda(t−1)>0, while t^(-n)V(x_n)→1. Hence this candidate cannot obey a physical one-step negative geometric Foster inequality outside a finite set. Its R=0 definition is irrelevant because all these states have R=n>0.

This proves that the no-free-passenger hypothesis is essential for this particular deficit/activation ansatz: otherwise R can be called large while all hub sources remain disabled. It does not exclude an alternative inventory, the previously accepted positive active-phase corrector, a sampled-time proof, or a product-form solution. The complete multipartite theorem must not silently absorb this excluded class.

`multipartite_mechanism_checks.py` includes an exact rational finite control at n=10^50, t=2, eta=1/16, epsilon=1/4,c=1, for which the scaled immigration drift is greater than9/10. The asymptotic proof above, not that finite test, establishes the obstruction.
