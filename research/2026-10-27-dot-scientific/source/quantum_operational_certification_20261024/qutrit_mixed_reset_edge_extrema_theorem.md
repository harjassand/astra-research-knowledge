# Exact rank-two reset edge: minima are pure or flat-rank-two

## Theorem and scope

For the actual qutrit channel E(rho)=p rho+q Tr(rho)tau, restrict tau to rank at most two and fix p,q. The WH3 deficit on this spectral edge is minimized either at a pure reset or at the maximally mixed reset on a two-dimensional subspace.

Thus, combined with qutrit_mixed_reset_white_shift_boundary_theorem.md, the entire arbitrary mixed-qutrit-reset value problem reduces to the scalar flat-rank-two reset family (the pure reset family is already paid). No flat-rank-two positivity proof is asserted in this note. The theorem does NOT say that the edge function is globally concave or that the physical twirl is monotone.

## 1. Actual determinant reduction

Write unnormalized a=p/3>0 and b=(0,u,v), u,v>=0. Set e=u+v and r=uv, so0<=r<=e^2/4. The value is symmetric in u,v and hence a function D(a,e,r).

Using the exact physical spectra in qutrit_mixed_reset_simplex_main_monotonicity_interface.md, source, output and reference determinants factor so that the r-dependent entropy integral is

 D_r=integral_0^infinity K(s;e,r) ds,
 K=2/(r+B)+2/(r+C)-1/(r+A)-3/(r+R),                    (1)

where

 A=[s^3+(e+3a)s^2+2ae s]/(s+a),
 R=(s+a/3)^2+e(s+a/3),
 C=s^2+(e+a)s+ae/2,
 B=C*s(s+a)/(s+a/2)^2.                                 (2)

The determinant factors omitted in(1) are independent of r, so differentiating removes them exactly. Positive r gives faithful nontrivial blocks; fixed zero spectator eigenvalues had already canceled. Derivatives and integrals are absolutely convergent.

Scale a to6 in the remaining proof. This loses no parameter range.

## 2. A source-compatible single-crossing integrand

The numerator of K after clearing positive denominators is a degree-seven polynomial in s with leading coefficient-90 and constant coefficient

 324r(e^2+2e+2r)>0.

Set e=u+v,r=uv. The exact coefficient-chain certificate proves that the polynomial's coefficients have at most one sign variation, descending from negative to positive. Consequently K has exactly one positive root s_*, counted with multiplicity, and

 K>0 for0<s<s_*, K<0 for s>s_*.

The certificate uses only nonnegative rational polynomial multipliers, exactly as in the preceding white-shift theorem. Its explicit multiplier coefficients are in qutrit_mixed_reset_edge_extrema_certificate.json; the replay verifies every monomial coefficient algebraically.

## 3. A decreasing multiplier pays curvature at every stationary point

Define, at a=6,

 k(s)=5/2+s/[30(s+180+e)],
 w(s)=k(s)/(r+R(s)).                                    (3)

The exact rational/Sturm certificate proves pointwise

 partial_r K+w(s)K<=0.                                 (4)

It does not infer this from sampling. After clearing the manifestly positive denominator and substituting e=u+v,r=uv, the NEGATIVE of the numerator is a polynomial in u,v with61 coefficients that are polynomials in s.33 of them have nonnegative coefficients directly. For each of the remaining28, remove its zero power of s; its leading and constant coefficients are positive and its exact Sturm count of roots on(0,infinity) is zero. Hence every coefficient polynomial is nonnegative for s>=0. The replay uses exact rationals and Sturm root counts, with no numerical roots or optimizer.

The multiplier is strictly decreasing on the physical parameter range. Indeed

 k'/k <=1/[75(s+180+e)],
 R'/(r+R)>=2/(s+2+e/2),

where the second inequality follows from r<=e^2/4. The first upper bound is strictly smaller than the second lower bound, proving w'<0.

Suppose D_r=integral K=0 at an interior r. By the unique crossing and strict decrease of w,

 integral wK=integral [w(s)-w(s_*)]K(s)ds>0.

Integrating(4) therefore gives

 D_rr<=-integral wK<0.                                  (5)

Every interior stationary point in r is a strict maximum, never a minimum. Since the entropy value is continuous on the compact interval0<=r<=e^2/4, its global minimum occurs at an endpoint. These endpoints are pure reset(r=0) and flat rank-two reset(r=e^2/4), proving the theorem.

## 4. Exact remaining scalar family

For b=(0,b,b), spectral diagonalization reduces the value to

 D=f2(b+3a,ab)-f(b)-2f(b+a)+6f(b+a/3)
   +3f(a/3)-4f2(b+a,ab/2),                              (6)

where f(x)=x logx and f2(T,P) is the trace of f of the two eigenvalues with traceT and determinantP. The source3x3 block splits into spectator b and a2x2 block of trace b+3a and determinant ab; the output pair on the two noisy references has eigenvalues b,b+a, and the other two pair blocks each have trace b+a and determinant ab/2. Formula(6) is the remaining scalar receiver, not yet its sign proof.

## Reproduction and limitations

qutrit_mixed_reset_edge_extrema_certificate.py and its JSON replay the exact sign-variation implications and all28 Sturm checks in ordinary SymPy. The certificate establishes only the stated edge-extrema reduction. It does not establish generic noise concavity, pointwise positivity of D_r, or the unrestricted WH3 entropy target.
