# A normalization bound and a genuine remaining interpolation obstruction
2026-10-29. Root working derivation, independent review pending. This is NOT a Jacobian-arithmetic algorithm or a Toda fast-forwarding theorem.

Let F be a monic squarefree real polynomial of degree2g+2, with all roots E_l in[-M,M], M>=1, pairwise separation>=Delta>0. Let a,b have degrees<=2g,g-1 and normalize max coefficient modulus across(a,b) to1. Suppose
 Q=a^2-F b^2=c product_{i=1}^{4g}(x-r_i)
with every |r_i|<=M. In the proposed relative-doubling Riemann–Roch section f=a+yb, these roots are the abscissas of2D+conjugate(D0)+conjugate(E), including multiplicities. This supposes the actual output is in the physical compact real component; it is not a way to infer that fact for arbitrary input sections.

Then |c| has an explicit exp(-poly(g,logM,log1/Delta)) lower bound.

At each branch root E_l, |a(E_l)|^2=|Q(E_l)|<=|c|(2M)^(4g). Interpolate a at any2g+1 branch roots. Every Lagrange coefficient is bounded by((1+M)/Delta)^(2g), so
 ||coeff a||_infinity <= C_A sqrt(|c|),
 C_A=(2g+1)((1+M)/Delta)^(2g)(2M)^(2g).
Also ||coeff Q||_infinity<=|c|(1+M)^(4g). Hence coefficients of a^2-Q have modulus at most |c|C_U, where
 C_U=(2g+1) C_A^2+(1+M)^(4g).

Because F is monic and ||coeff F||_1<=(1+M)^(2g+2)=F_1, elementary long division bounds
 ||coeff(b^2)||_infinity <=|c| C_U (4g+1)(1+F_1)^(2g-1)=|c|C_B.
For b of degree<=g-1, Cauchy's coefficient bound on the unit circle gives
 ||coeff b||_infinity^2 <= max_|z|=1 |b(z)|^2
 =max_|z|=1 |b(z)^2| <=(2g-1)||coeff(b^2)||_infinity.
Thus
 |c| >= 1/max(C_A^2,(2g-1)C_B).
Since c=a_(2g)^2-b_(g-1)^2 and each leading coefficient has modulus<=1, the two leading pole factors a_(2g)+/-b_(g-1) also have modulus>=|c|/2. No assumed pole denominator is needed for these actual compact-output sections. g=0 is trivial and handled separately.

## What this does not prove
This bounds normalization and final polynomial division, NOT the smallest nonzero singular value of the interpolation constraint matrix used to acquire f. Naive rows can become arbitrarily ill-conditioned at perfectly regular physical configurations.

For g=1 take F=(x^2-4)(x^2-1), initial D0=(0,2), and current D_e=(e,-sqrt(F(e))) with e near0. A section f=a0+a1 x+a2 x^2+b y has constraints
 f(D_e)=0, (d/dx)f(D_e)=0, f(conjugate D0)=0.
With b=1, a0=2 and
 a2=(2+y(e)-e y'(e))/e^2,
 a1=-2e a2-y'(e),
the coefficients tend to(2,0,-5/4,1), whose norm leading coefficient is9/16 before max-normalization. The kernel is well-behaved. But the first and third raw evaluation rows coincide at e=0 and their difference after subtracting e times the derivative row is O(e^2). A raw least-squares/pivot condition bound therefore fails.

Replace the third row by the Hermite divided difference of the analytic section along a local curve parameter; at collision it is the second derivative/2. Evaluate that divided difference using analytic series or rationalized algebraic formulas, not cancellation of nearly equal floating values. This removes this LOCAL degeneracy. Across all g gaps, global uniform nonzero-singular-value bounds remain an open obligation. Compactness alone may give constants with unacceptable genus dependence; no polynomial bit-cost conclusion is drawn here.
