# Compact semialgebraic nil semigroups need not be word nilpotent

9 October 2026. Exact counterexample to a proposed abstract shortcut for nonstationary PPT composition. No priority claim. This is not a quantum channel construction or a counterexample to the PPT-square question.

## Statement

There is a compact convex semialgebraic subset S of R^3, carrying a continuous semialgebraic associative multiplication and a zero element, such that x^2=0 for every x in S, but S^n contains a nonzero element for every positive integer n. A single infinite sequence has all its finite prefix products nonzero.

Thus compactness, finite-dimensional semialgebraicity and a uniform bound on the nil index, even index two, do not by themselves imply a common extinction length for arbitrary varying products.

## Interval labels and associative multiplication

Represent a nonzero element by (a,b,z), where 0<=a<=b<=1 and 0<z<=1. All triples with z=0 represent one zero element. Define

 (a,b,z)*(c,d,w)=(a,d,z w (c-b)) if c>b,
 (a,b,z)*(c,d,w)=0 if c<=b.

For a finite string (a_i,b_i,z_i), its product is zero if any z_i=0 or any a_(i+1)<=b_i. Otherwise it has endpoint labels (a_1,b_n) and amplitude

 (product_i z_i)(product_(i=1)^(n-1) (a_(i+1)-b_i)).

This formula is independent of parenthesization, proving associativity. Multiplication by zero is zero.

Every element squares to zero because its own left endpoint a is at most its right endpoint b.

For an arbitrarily long nonzero product, take a_i=b_i=i/(n+1), z_i=1 for i=1,...,n. Its amplitude is (n+1)^(-(n-1))>0. For one infinite example, take a_i=b_i=1-2^(-i), z_i=1. Each consecutive gap is 2^(-(i+1)), so every finite prefix product is nonzero, although the amplitudes converge to zero.

## Explicit compact finite-dimensional realization

Realize the quotient by the coordinates

 (z,x,y)=(z,z a,z b).

Its image is the compact convex semialgebraic set

 S={(z,x,y): 0<=x<=y<=z<=1}.

The unique element with z=0 is (0,0,0). Given u=(z,x,y) and v=(w,X,Y), set

 tau=max(z X-w y,0).

If tau=0, define u*v=0. If tau>0, define

 u*v=(tau, x tau/z, Y tau/w).

Positive tau forces z,w>0 and x/z<=y/z<X/w<=Y/w. Hence the output belongs to S. Also 0<=tau<=z w<=1. The graph of the operation is semialgebraic: it is specified by polynomial equalities and inequalities after splitting into the cases tau=0 and tau>0.

On tau>0 it is rational and continuous. When tau tends to zero, every output coordinate lies between zero and tau, so the output tends to the zero element. This also covers z or w tending to zero. Thus multiplication is jointly continuous everywhere. The interval-label proof proves its associativity on this realization.

## Boundary for the PPT investigation

The compact CPTP slice of the PPT cone is a composition semigroup, and its EB subset is a closed two-sided ideal. Collapsing that ideal to zero gives a Rees quotient. The uniform-power theorem makes every quotient element nilpotent with a common bound.

The present example shows why no theorem based solely on compactness, continuous semialgebraic multiplication and a uniform nil index can finish the varying-word problem. A stronger argument must exploit the actual bilinear composition of finite-dimensional CP maps, the convex positive decompositions, or full filter invariance before quotienting. The example's multiplication is not asserted to have such a CP or finite-dimensional bilinear lift.

A narrow primary comparison found Magalhaes, On Definably Compact Semigroups in o-Minimal Structures, arXiv:2507.19162v1 (2025), https://arxiv.org/html/2507.19162v1 . Its idempotent and minimal-ideal theorems are compatible with this example: the only idempotent and unique minimal ideal here are zero. Those conclusions do not imply word nilpotence. No broad survey or claim of novelty for this counterexample is made.
