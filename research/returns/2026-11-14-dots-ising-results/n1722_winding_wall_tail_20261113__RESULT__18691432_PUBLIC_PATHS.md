# Global high-winding-perimeter tail, with a direct Gibbs baseline

This is a standard full-contour exponential-moment bound applied to the actual torus. It is NOT a new current-method gain and uses no capacity estimate. Its purpose is to remove a genuinely broad winding class from the unresolved occupation problem and prevent baseline-dominated higher-homology claims.

Let P_w(x) be the TOTAL PHYSICAL perimeter of all noncontractible cycles in the actual fixed-triangulation domain-wall set. Work at theta>=4, phi=theta/R, L=8R, n=L², integer R>=80. Let B={M>=0}; outside B, Nplus<n/2. The actual core contains allminus, hence ZA>=w_minus. Also0<=v<=1.

## Full wall-set bound
Each domain-wall set determines the spin configuration up to global sign. All walls, including contractible holes, are retained. Using the proved physical-walk count100n3^s, let q=3exp(-2theta). Every wall has physical length at least4; every noncontractible wall has length at leastL.

For lambda>0 with qe^lambda<1, drop all loop incompatibility constraints in positive sums to obtain
 sum_(x outsideB,P_w>=5L) w(x)/w_minus
 <=2 exp(phi n-5lambda L)
      *exp[100n q^4/(1-q)
             +100n(qe^lambda)^L/(1-qe^lambda)].

The field inequality w(x)/w_minus=exp(-2theta P_total+2phi Nplus)<=exp(-2theta P_total+phi n) is pointwise. The first pressure term overcounts all unmarked contractible walls; the second overcounts all marked winding walls. Including some winding activities in both upper counts only enlarges the result. No outer-contour-only encoding or absent background entropy is used.

Choose qe^lambda=9/10, so lambda=2theta-log(10/3). Exact log(10/3)<5/4 implies
 phi n-5lambda L <=(50-16theta)R<=-14R.
At theta4, q<1/900 and100q^4/(1-q)<1/6553710000. Therefore

 Z_(outsideB,P_w>=5L)/ZA
 <=2 exp[-14R+n/6553710000+1000n(9/10)^L].       (1)

The same is an upper on the actual occupation numerator divided byZA, becausev<=1. The native clock and source do not enter or change in this direct bound.

## Exact finite certificates
check.py/json verifies the two pressure terms are each<1 atR80,200,1000,10000. Thus mass AND occupation are bounded by
R80: exp(-1117) ZA.
R200: exp(-2797) ZA.
R1000: exp(-13997) ZA.
R10000: exp(-139997) ZA.
In fact the same exp(-14R+3) bound holds for every integer80<=R<=10000: the bulk pressure increases withR and is<1 at10000, while R²(9/10)^(8R) decreases forR>=80, as the exact successive ratio is at most(81/80)²(9/10)^8<1. Both checks are in the script. The explicit formula(1) displays the cost beyond that range; no unrestricted thermodynamic-limit claim is made.

## Structural consequence for the remaining winding class
Resolved domain-wall cycles are disjoint embedded curves on the torus. All noncontractible cycles therefore have parallel primitive homology(a,b), up to orientation. Their number is even, since the total wall set is a boundary mod2 and a primitive homology is nonzero mod2. Each has physical perimeter at least(|a|+|b|)L.

Consequently P_w<5L leaves only:
- two or four axis-homology cycles (|a|+|b|=1); or
- two diagonal-homology cycles (|a|+|b|=2).
Higher primitive homologies, six-or-more winding cycles, and sufficiently rough winding wall collections already lie in the direct-mass tail. This is a classification of ACTUAL domain walls, not of an arbitrary plus seed contained in a source state.

Important distinction: a configuration may contain a high-slope plus winding seed but have no winding domain walls at all (for example, a plus sea around contractible minus regions). Thus equation(1) does not automatically dominate every higher-slope SEED theorem. Seed homology and actual wall homology must not be conflated.

## Remaining gap
The remaining two/four low-homology interfaces can still be rough, lack a full straight plus line, and carry nonrare Gibbs mass. The no-winding-wall sector can also contain high-mass states. This reduction does not prove current coverage or total exit/residence closure. It narrows the unresolved geometric alternatives without presenting a simple Gibbs tail as a new linear-current breakthrough.
