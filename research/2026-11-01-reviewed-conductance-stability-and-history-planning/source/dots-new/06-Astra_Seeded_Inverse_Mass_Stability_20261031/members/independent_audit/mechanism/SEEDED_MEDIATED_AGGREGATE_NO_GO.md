# Aggregate no-go for the common-A lift of mediated restoration

Consider positive rates on

    0 <-> A,
    2A+B <-> A+B+C,
    2A+C <-> A+2B,
    A+B+C <-> A+2C.

Write lambda,mu for immigration/death and alpha2 for `2A+C->A+2B`. All other rates are positive but do not enter the obstruction inequalities.

**Proposition.** On the positive-satellite communicating class Gamma described below, no positive normlike function `V(x)=F(A,N)` can satisfy a one-step geometric Foster inequality `LV<=-epsilon V+C` with epsilon>0 and finite C. F may be arbitrary and nonseparable. This excludes neither joint mediator-dependent functions nor additive, sampled-time, excursion or path criteria.

## 1. Three-layer scalar contradiction

Assume such an inequality holds. Increasing C to at least zero and reducing epsilon preserves it. Choose epsilon small enough that

    0<epsilon<=lambda^2/[4(lambda+mu)].

Define

    u_n=F(0,n),  v_n=F(1,n),  w_n=F(2,n),
    r=1-epsilon/lambda,
    s=(lambda+mu-epsilon-mu/r)/lambda.

Then r>=3/4 and

    s=r-mu epsilon/(lambda^2 r),
    0<s<r<1.

For positivity, `mu epsilon/(lambda^2 r)<=mu/[3(lambda+mu)]<1/3`, so s>5/12 suffices.

At `(0,0,n-1)`, every internal channel is disabled. The Foster inequality gives

    lambda(v_n-u_(n-1))<=-epsilon u_(n-1)+C,
    u_(n-1)>=(v_n-C/lambda)/r.                           (1)

At `(1,0,n-1)`, any enabled internal channel preserves both A and N and is invisible to F. Immigration and death give exactly

    lambda w_(n+1)+mu u_(n-1)
       -(lambda+mu)v_n<=-epsilon v_n+C.

Using the lower bound (1),

    w_(n+1)<=s v_n+B,
    B=(C/lambda)[1+mu/(lambda r)].                       (2)

At `(2,0,n-2)`, for n>=3, the only internal channel changing A is `2A+C->A+2B`, at rate `2 alpha2(n-2)`. Its destination has A one and the same total n, hence value v_n. Other internal transitions are invisible to F. Dropping the nonnegative immigration/death destination values gives

    LV>=2 alpha2(n-2)v_n
           -[2 alpha2(n-2)+lambda+2mu]w_n.

Combining with the upper Foster bound yields

    v_n<=[1+q/(n-2)]w_n+C/[2 alpha2(n-2)],
    q=(lambda+2mu-epsilon)/(2 alpha2)>0.                 (3)

Substituting (2), with its index shifted by one, gives

    v_n<=s[1+q/(n-2)]v_(n-1)
           +B[1+q/(n-2)]+C/[2 alpha2(n-2)].              (4)

For all sufficiently large n the first coefficient is at most `rho=(1+s)/2<1`. The additive part is at most `M=B(1+q)+C/(2 alpha2)`. Iterating `v_n<=rho v_(n-1)+M` bounds the whole tail of v_n. Normlikeness on the distinct states `(1,0,n-1)` requires v_n to diverge to infinity. Contradiction.

The proof is pointwise generator algebra. It assumes neither stationary integrability nor regularity, asymptotic shape or separability of F.

## 2. Every comparison lies in one closed class

The common-A internal network is the ordinary mediated network after setting `r=A-1` on A>=1, with its generator multiplied by the actual A. Therefore enabled mediated paths can be lifted by adding one A to every state. Explicitly, all arrows below and their reverses are enabled:

    A+C -> 2A+C -> A+2B -> 2A+2B
        -> A+2B+C -> A+B+2C -> A+3C;

    A+2C -> 2A+2C -> 2A+B+C -> A+B+2C -> A+3C.

For every k>=2,

    A+C^k -> 2A+C^k -> 2A+B+C^(k-1)
          -> A+B+C^k -> A+C^(k+1).

Thus every `A+C^k`, k>=1, belongs to the same class. Core immigration/death attach `C^k`, `2A+C^k`, and `3A+C^k` to it. All states and destinations used in (1)--(3), for sufficiently large n, consequently belong to this one class Gamma. Reversible raw pairs make Gamma closed.

The A-only class is separate and is not used in the contradiction. No classification of every other positive-satellite state is needed.

## 3. Meaning of the obstruction

The seeded direct-return star family has an ordinary service-only correction `h(A)=1+c/A` on A>=1, with a patched A-zero value. That does not contradict this proposition: there the A-one pure-satellite state has a fast reverse channel that creates A. In the mediated lift, A-one pure C only creates a mediator while preserving A; A-two then has accelerated last-copy-to-first-layer loss. Eliminating these three layers forces the contraction above.

This shows that `(A,N)` omits consequential mediator information for one-step geometric Foster control on the harder lifted network. It is not an impossibility result for all recurrence methods, all finite abstractions, or suitable alternative aggregate coordinates.
