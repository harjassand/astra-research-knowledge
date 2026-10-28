# Explicit open neighborhood and evaluated conic values

This is an explicit domain for the primitive in `PROOF.md`, with the
same frozen compensated parameters. Its implementation is
`local_evaluator.py`; exact outputs are in `LOCAL_EVALUATION.json`.

## A fixed rational base Gram

At z=0 the polynomial D(A)[0-ell_A(0)] is

    P0=P8_H+[6sigma T H+eT^3]+[3sigma^2 H+2e sigma T^2]
                                                        +e sigma^2 T.

Let GF be the old rational10 Gram for H on quadratic monomials, after
the verified kappa q^2 subtraction. The degree1,2,3,4 Gram blocks are

    G1=e sigma^2 I,
    G2=3sigma^2 GF+2e sigma diag(multinomial(2,alpha)),
    G3=6sigma sum_i J_i GF J_i^T+e diag(multinomial(3,alpha)),
    G4=G35-kappa v(Tq)v(Tq)^T.

Here J_i multiplies each quadratic monomial by A_i. Exact coefficient
reconstruction verifies the full block identity. Separate rational LDL
calculations prove each block strictly above d_j^2 I, where

    d1=1/400, d2=1/50, d3=9/100, d4=3/100.

Thus Gbase>=diag(d_i^2) on the69 monomials. This uses actual strict
Gram inputs, not only positivity of the represented polynomial.

## Uniform coefficient correction on an explicit cube

Put ra=1/4000, rb=1/32000, rs=1/10000. Allow arbitrary anchor coordinates
|a_i|<=ra and query coordinates |B_i|<=rb, |s|<=rs. The anchor here
need not satisfy stationarity. Let d_e(a) be the Y^e coefficient of
D(a+Y), and n_e(a,z) that of N(a+Y,z). For t0=ell_a(z), the change
from the base polynomial coefficient is exactly

    Delta_e=d_e(a)t0-[n_e(a,z)-n_e(0,0)],  2<=|e|<=8.

The script expands these as rational polynomials, cancels their constant
terms exactly, and bounds a polynomial by the sum of the absolute
coefficients times the powers of ra,rb,rs. Since D(a)>=sigma^2,
the same operation bounds |t0| by bound(N(a,z))/sigma^2. Consequently
each |Delta_e| has an explicit rational bound.

To lift a coefficient change, list all pairs of nonconstant monomials
whose exponents sum to e, retain those maximizing d_i d_j, and divide
Delta_e equally among those pairs. Off-diagonal entries receive half
the polynomial coefficient. This defines a fixed rational right inverse.
Summing the resulting scaled absolute matrix rows proves

    ||diag(d)^-1 (Q-Gbase) diag(d)^-1||
       <=rho=69249540579711104218703/155675520000000000000000
       <9/20<1/2.                                         (1)

The operator norm is bounded by that maximum row sum because the
correction is symmetric. Hence Q>(1/2)diag(d_i^2) throughout this
coordinate cube, with no solver or sampling premise.

## Root existence and smoothness on a full five-dimensional box

The coefficient cube above is distinct from the Euclidean ball used
here: concavity is needed ONLY for ||a||<=ra. That ball is contained
in the coefficient cube. On it ||B||<=2rb=ra/4.

Write k=pH/(T+sigma)^2 and R=s+q(a)-cofa:B. Then

    ell_a(z)=-3H(a)-eT(a)+DH(a):B+2e a:B+k(a)R.

For ||a||<=r=ra and ||B||<=b=2rb, let C,P be the coefficient-l1 norms
of H,pH. The rigorous derivative bounds used in the script are

    K0=P r^6/sigma^2,
    K1=6P r^5/sigma^2+4P r^7/sigma^3,
    K2=30P r^4/sigma^2+52P r^6/sigma^3+24P r^8/sigma^4.

They bound |k|,|Dk|,||D2k||. Product differentiation bounds
||D2_A ell+2eI|| by

    L=36C r^2+24C r b+K2(rs+r^2/2+r b)+2K1(r+b)+K0.

Here products such as r b mean multiplication of the Euclidean radii
r and b; the separate coordinate radii were named ra and rb above.
Exact arithmetic proves L<e. Thus D2_A ell<=-eI on the Euclidean ball.
At a=0 its gradient is exactly2eB. On ||a||=ra the radial derivative
is at most2e||B||ra-e ra^2<0. There is a unique stationary maximum in
the ball, with ||a(z)||<=2||B||<=ra/2. The IFT gives a smooth stationary
map throughout the open query box. At that root the linear coefficients
vanish, and(1) gives a global SOS certificate, proving equality to the
finite conic value. Therefore G is C-infinity and has Hessian>=2kappa I on

    |B_i|<1/32000 (i=0,...,3),  |s|<1/10000.                (2)

This is an open five-dimensional neighborhood containing a Euclidean
ball of radius1/32000. It includes a small patch of the minors graph;
the general theorem separately supplies a qualitative neighborhood of
every graph point. It is not a uniform tube about all |A|<=1.

## Actual off-axis evaluations and honest costs

The two rational queries, in row-major B order followed by s, are

    z1=(1/64000,-1/96000,1/160000,1/128000, 1/20000),
    z2=(1/96000, 1/128000,-1/160000,1/64000,-1/20000).

They are inside(2). One floating Newton step at each point supplied a
60-bit rational anchor. Exact correction of every nonconstant polynomial
coefficient gave scaled row norms about.01986 and.02127, respectively.
Square completion in `PROOF.md` gives the two exact rational value
brackets, displayed as

    G(z1) approximately4.527577264887657e-12, width6.24816e-39,
    G(z2) approximately4.527577264790954e-12, width6.25700e-39.

The JSON endpoints, not these rounded decimals, are the certificates.
Newton accuracy is untrusted and the conic value is enclosed without
running a70 SDP. Both coefficient identities and the completion parameters
are reconstructed exactly by the script. No sample is used to infer box
convexity or smoothness.

For the original frozen15-moment representative, PSD covariance implies

    G15(B,s)>=epsilon|B|^2+2epsilon|s-detB|,

because L(T)-T(B)>=2|L(q)-q(B)| and F is SOS. These lower bounds at the
two queries are about1.000000784e-6 and1.000008759e-6, much larger than
the respective new values. The representatives are different off graph;
this separation is not an optimization-accuracy or speed comparison.

A matched actual value control uses its previously proved exact B=0
slice. Rational derivative bisection encloses G15(0,1/10000) at
approximately2.0019412329625e-6. The new value there is exactly
kappa/10^8=5e-16. The latter also follows from root's separately owned
homogeneous normal-strip certificate. The original G15 uses F+epsilon T;
root additionally compares the compensated15 value plus kappa|z|^2.
Those comparators should not be silently conflated.

The final measured module run took about4.40 seconds, excluding Python
startup. It charges about.60s for imports/literal setup, .079s for base
Gram reconstruction and exact LDL, .404s for the coefficient-bound
compiler, and3.03s once for symbolic Newton gradient/Hessian compilation.
The five bounded radius tests are included in the total. After compilation,
each Newton proposal took about.0005s and exact certificate verification
about.12s. The old15 exact scalar comparator took about.0012s for80
rational bisections. Prior R180 and26/35 Gram acquisitions remain charged
upstream inputs, with their costs preserved in those source packages.

The global operation outside the explicit box remains the fixed70-cone
SDP. No general70 solver run, global precision-complexity bound, peak
memory measurement, physical entropy implementation, or generic speed
advantage is acquired. The substantive result is an exact finite convex
primitive with proved smooth strict local geometry and a concretely
verified, numerically accessible full-dimensional evaluation domain.
