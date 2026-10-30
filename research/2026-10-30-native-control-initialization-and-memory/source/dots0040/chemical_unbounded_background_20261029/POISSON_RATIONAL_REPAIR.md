# An exact global dual repair with two unbounded populations

29 October 2026. Exploratory derived proof; not externally reviewed or novelty-cleared. This is a mechanism test, not general recurrence. The general two-species recurrence theorem has already been publicly claimed by other authors.

## Network

Use the weakly reversible triangle and a separate reversible linkage:

    2A --100--> A+2B --1--> 2A+B --1--> 2A,
    0 <--1 / 1--> A.

Both coordinates are unbounded. The triangle has complex-balanced concentration (100,100). The linear linkage requires A=1, so their union is not complex balanced. No product-Poisson stationary law is assumed.

## 1. Every product-geometric dual fails

Suppose mu(A,B)=exp(-u A-v B), u,v>0, up to a constant. Along B=A^2 as A tends to infinity, the source A+2B dominates and the leading adjoint defect has coefficient exp(u-v)-1. Therefore an eventual nonpositive defect requires u<=v.

But along B=2 and A tending to infinity, the coefficient of A^2 in L*mu/mu is

    100[exp(-u+2v)-1]+3 exp(-v)-2.

For u<=v this is at least 100(exp(v)-1)+3 exp(-v)-2. The latter equals1 at v=0 and has derivative 100 exp(v)-3 exp(-v)>0 for v>=0. It is strictly positive. Thus no positive product-geometric envelope works, regardless of how its two constant tilts are tuned. The linear linkage contributes only lower-order A terms to this obstruction.

## 2. Replace the representation, not the tilt constants

Let pi be the product of Poisson(100) laws and put

    d=1/1000,
    h(a)=1+1/(a+d),
    mu(a,b)=pi(a,b) h(a).

This is positive, summable, and has all exponential moments. Also sum mu q is finite because every rate is polynomial and 1<=h<=1001.

The triangle alone has invariant pi. Reversing its stationary fluxes shows that its adjoint action on pi h, divided by pi, is exactly

    R(a,b)=a b(b-1)[h(a+1)-h(a)]
          +a(a-1)b[h(a-1)-h(a)].

The final term is absent at a=0,1. The linear linkage contributes

    T(a)=(a/100)h(a-1) 1_(a>=1)+100h(a+1)-(1+a)h(a).

Hence L*mu/pi=R+T, an exact identity at every nonnegative integer state.

For a>=1 define

    alpha=a/[(a+d)(a+d+1)],
    beta=a(a-1)/[(a+d-1)(a+d)]  (zero when a=1).

Then

    R=-alpha b^2+(alpha+beta)b.

The correction has supplied a negative quadratic term in the genuinely unbounded background coordinate. No finite phase approximation occurs.

## 3. All-size sign bound including the boundary

For a>=2, beta<=1, alpha<=1/a, and 1/alpha<=a+4. Thus, maximizing the concave quadratic over real b,

    R <= (alpha+beta)^2/(4alpha)
      <= a/4+13/8.

For a>=100, write

    T=(99-99a/100)h(a)
      +(a/100)[h(a-1)-h(a)]
      +100[h(a+1)-h(a)].

The last term is negative, the middle term is <=1/100, and the first coefficient is nonpositive. Consequently

    R+T <= 99-99a/100+a/4+13/8+1/100
         =100.635-0.74a < -1   for a>=138.

For 2<=a<=137, the rough bounds T<149, alpha>=1/141 and alpha+beta<=3/2 give

    R+T <= -b^2/141+3b/2+149 < -1  for b>=400.

For a=1, alpha>1/6, beta=0 and T<160, so R+T<=160-b(b-1)/6<-1 for b>=400. At a=0, the triangle contribution vanishes and

    T(0)=100*(2001/1001)-1001=-801901/1001<0

for every b, including arbitrarily large b.

Therefore L*mu<0 outside the finite rectangle {1,...,137} x {0,...,399}. The exact finite-dual-measure excursion argument from the reviewed strip theorem now applies without any finite-background premise: nu=mu q is finite and nu P<=nu outside that rectangle. Every communication class is closed by weak reversibility; finite expected embedded excursions imply nonexplosion and positive recurrence. Regenerative occupation is dominated by a class-dependent multiple of mu, so this example has all exponential moments.

## What changed and what remains open

The reference was an explicit infinite-dimensional Poisson law, not a stationary law of the full process. A bounded rational correction repaired its adjoint defect globally, including the A=0 face. No mixing gap, approximation, finite cutoff, deterministic barrier or boundary-gluing estimate was imported.

The special complex-balanced core supplied a usable reference measure. A general weakly reversible network need not have a compatible dominant complex-balanced core; finding a reference and corrective hierarchy for all boundary strata remains unproved. This is not permission to assume that premise in a general recurrence theorem.
