# Exact binary single-port counterexample to a uniform mixing premise

This is an author-derived discriminator, not a claimed new recurrence result or historical priority. The ordinary detailed-balance construction solves its stationary law before any new method is applied. The established paper Anderson, Cappelletti, Fan and Kim, *A new path method for exponential ergodicity of Markov processes on Z^d, with applications to stochastic reaction networks*, arXiv:2309.06970v2 / SIAM JADS 2025, already gives a detailed-balanced reaction network without exponential ergodicity. The family below keeps the additional conservative-core and sole-port restrictions of the present question and uses binary reactions.

## The family and its exact invariant law

Fix an integer m>=2. There is exactly one enzyme, in phases C_0,...,C_m. Take all rate constants equal to one, actual falling-factorial propensities, and

    B+C_j <-> C_(j+1), j=0,...,m-1,
    A+C_0 <-> B+C_0,
    0 <-> A.

Every source and target has at most two molecules. The internal network is reversible. Before the sole reservoir is added it conserves the positive weight

    W=A+B+sum_j (j+1) C_j.

The closed class with sum_j C_j=1 consists of states (a,b,j), a,b>=0, 0<=j<=m. It is irreducible: unbind to j=0, convert B to A, remove A, and reverse those paths. Nonexplosion follows from W(t)<=W(0)+Poisson(t); on every bounded-weight sublevel there are finitely many states and bounded rates.

The exact probability

    pi(a,b,j)=exp(-2)/[(m+1) a! b!]

satisfies detailed balance on every edge. For binding, pi(a,b,j)b=pi(a,b-1,j+1). For conversion at j=0, pi(a,b,0)a=pi(a-1,b+1,0)(b+1). For the reservoir, pi(a,b,j)=pi(a+1,b,j)(a+1). Summation gives one. Thus A and B are independent Poisson(1) and the phase is uniform. In particular EVERY exponential moment of ordinary molecule count, weighted mass, or inventory B+j is finite. No numerical simulation is needed for these facts.

## Conductance tending to zero

Use the physical substrate inventory I=B+j and the cut

    S_n={(a,b,j):b+j>=n}, n>m.

All binding/unbinding moves preserve I; reservoir moves change only A. A conversion can cross the lower boundary only when j=0 and b=n, using B+C_0 -> A+C_0 at rate n. Consequently the exact stationary outflow is

    Q(S_n,S_n^c)= n exp(-1)/[(m+1)n!].

On the other hand, the states with j=m,b=n-m all belong to S_n, regardless of A, so

    pi(S_n)>=exp(-1)/[(m+1)(n-m)!].

The conductance is therefore bounded by

    Q(S_n,S_n^c)/pi(S_n)
       <= n(n-m)!/n!
        = n/[n(n-1)...(n-m+1)] ->0, m>=2.                  (1)

For the reversible generator, the Dirichlet form of 1_(S_n) is exactly Q(S_n,S_n^c), and its variance is pi(S_n)(1-pi(S_n)). Since pi(S_n)->0, its Rayleigh quotient tends to zero by (1). Hence the L2(pi) spectral gap is exactly ZERO.

If one defines the generator initially on finitely supported functions, the cut indicators can be approximated in the form norm by finite truncations. The explicit factorial stationary law has finite polynomial-rate moments, so the omitted edge energies tend to zero. Thus the same zero-gap conclusion holds for that standard closure, rather than relying on an inadmissible test function.

## Scope of the obstruction

Stationary exponential tails do not give a uniform physical-time spectral gap. A universal higher-rank construction cannot import such a gap from detailed balance, weak reversibility, binary order, conservativity of the core, a single reservoir, or finite exponential tails: all of those properties hold here.

The proof does NOT establish instability, failure of positive recurrence, or impossibility of a compatible actual-time return construction. It does not by itself address every possible notion of nonuniform exponential convergence. It prevents the specific L2-gap premise from being supplied for free.

`catalytic_bottleneck.py` checks exact detailed-balance edges and selected rational bounds. The general cut and Rayleigh argument above establish the infinite-family claim; the finite checks are supplementary.
