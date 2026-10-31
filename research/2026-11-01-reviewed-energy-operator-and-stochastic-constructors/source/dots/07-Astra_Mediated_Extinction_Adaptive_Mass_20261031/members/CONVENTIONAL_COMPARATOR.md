# Ordinary unbounded service-radial comparator

This independently derived comparator concerns the exact abstract count family
`0 <-> A`, `A+B_j <-> 2B_j`, plus channels preserving A and total count. It is
not a counterexample to the bounded finite-capped-table obstruction, and no
historical novelty is asserted. It prevents interpreting that restricted
obstruction as excluding every layer or radial correction.

Let t>1 be rational, D=d(1-1/t), a=A, B=sum B_j and m>=1. Write alpha=max alpha_j
and beta=min beta_j. Put

    L=2 alpha+beta/2,
    0<c<=min(1,D beta/(2m L^2)),
    g(0)=2t, g(1)=1, g(a+1)/g(a)=a/(a+c) for a>=1,
    U=t^(a+B) g(a).

All of these values are acquired directly from the raw positive rates. Neutral
channels preserve U identically.

For a>=2 the immigration quotient is at most lambda(t-1). The death quotient
is `-D a+(dc/t)*a/(a-1)<=-D a+2dc/t`. The forward-star contribution is at most
`2c alpha B`; the reverse contribution is at most

    -c beta B^2/[m(a+c)] + c beta B/(a+c)
       <= -c beta B^2/(2ma)+c beta B/2.

By the elementary completed-square inequality,

    c L B <= c beta B^2/(4ma)+c m L^2 a/beta.

The choice of c therefore yields

    LU/U <= lambda(t-1)+2dc/t - D a/2 - c beta B^2/(4ma).

Splitting a>=N/2 from B>N/2 shows a negative linear total-count tail, with for
example coefficient min(D/4,c beta/(8m)).

At a=0, immigration has ratio t*g(1)/g(0)=1/2, and reverse stars have ratio
1/(2t)<1, giving `LU/U<=-lambda/2` for every satellite population.

At a=1, the exact death contribution is d and the other terms give

    LU/U <= lambda(t-1)+d
       +[(2t-1)alpha+c beta/(1+c)] B
       -c beta B^2/[m(1+c)].

The leading quadratic coefficient is strictly negative. A finite integer
threshold is acquired by direct polynomial evaluation or a completed-square
bound. Thus this layer has only a finite exception set. Combining the three
regions gives a geometric Foster inequality with an explicitly acquired finite
exception set and constant.

Since c<=1, g(a)>=1/a for a>=1, while g(0)=2t. Therefore U is normlike and
controls exponential count moments below log t. Repeating for arbitrary rational
t>1 gives all finite exponential moments by the same justified stopped-semigroup
and stationary-truncation argument as the main construction. Nonexplosion also
has the ordinary immigration-Poisson bound because only immigration increases
N.

The main proposed normalized-composition function
`t^N[1-epsilon A/(N+1)]` is cleaner: its correction is uniformly bounded and it
yields one global analytic inequality, without the separate a=1 polynomial
exception calculation above. Both are legitimate count-adaptive corrections.
The no-go argument for a finite capped table times asymptotically flat g(N)
excludes neither this unbounded g(A) construction nor all conceivable Lyapunov
methods.
