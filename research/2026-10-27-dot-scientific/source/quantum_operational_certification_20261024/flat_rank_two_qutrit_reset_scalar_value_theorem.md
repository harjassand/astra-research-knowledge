# Flat-rank-two qutrit reset: whole scalar value certificate

## Statement

The actual channel E(rho)=p rho+q Tr(rho)P2/2, where P2 is any rank-two projection on the qutrit output, has positive WH3 deficit whenever p,q>0. At p q=0 its deficit is zero.

The proof is a one-variable derivative theorem: elementary endpoint estimates plus an exact all-interval rational certificate on a compact middle interval. It does not infer positivity from finitely sampled values.

## 1. Exact scalar value and derivative

Use unnormalized main coefficient a>0 and reset eigenweights b=(0,b,b), b>0. Matched covariance removes the choice of P2. With f(x)=x logx and f2(T,P) the sum of f of the eigenvalues with traceT and determinantP, the exact deficit is

 D=f2(b+3a,ab)-f(b)-2f(b+a)+6f(b+a/3)
    +3f(a/3)-4f2(b+a,ab/2).

Homogeneity gives D=b d(x), x=a/b, where

 d(x)=f2(1+3x,x)-2f(1+x)+6f(1+x/3)
      +3f(x/3)-4f2(1+x,x/2), d(0)=0.                   (1)

Put

 U=sqrt(9x^2+2x+1), V=sqrt(x^2+1),
 c_s=(1+9x)/U, c_o=4x/V,
 L_s=(1+3x+U)/2, L_o=(1+x+V)/2.

Differentiating the actual two eigenvalue pairs gives exactly

 d'(x)=[(1-c_s+c_o)/2]logx+log(4/27)
       +2log((x+3)/(x+1))+c_s logL_s-c_o logL_o
       -(c_o/2)log2.                                  (2)

All assertions below concern this exact derivative.

## 2. Elementary small-x receiver

Assume0<x<=1/20. Since

 U<=1+x+4x^2,
 (1+9x)>=(1+4x)(1+x+4x^2),

we have c_s>=1+4x>=1+c_o. Thus the logx term in(2) is nonnegative. Also L_s>=1, while L_o<=1+x and c_o<=4x. Therefore

 c_s logL_s>=0,
 c_o logL_o<=4x^2,
 (c_o/2)log2<=2x,
 log(4/27)+2log((x+3)/(x+1))
  =log(4/3)+2log(1+x/3)-2log(1+x)>=1/4-2x.

Here log(4/3)>=1/4, log2<=1 and log(1+x)<=x are elementary. Consequently

 d'(x)>=1/4-4x-4x^2>=1/25>0.                            (3)

The squared inequality for U holds by expansion, and the second displayed comparison reduces to4x-8x^2-16x^3>=0 on the indicated interval.

## 3. Elementary large-x receiver

For x>=10 set y=1/x<=1/10. Define

 c_s=(9+y)/sqrt(9+2y+y^2), c_o=4/sqrt(1+y^2),
 ell_s=(3+y+sqrt(9+2y+y^2))/2,
 ell_o=(1+y+sqrt(1+y^2))/2.

Rearranging(2) without approximation gives

 d'(x)=[(1+c_s-c_o)/2]log(1/y)
 +(c_s-3)log3-[(c_o-4)/2]log2
 +2log((1+3y)/(1+y))+c_s log(ell_s/3)-c_o log ell_o.     (4)

The first term is nonnegative: for y<=1,

 3-c_s=8y^2/[sqrt(9+2y+y^2)(3sqrt(9+2y+y^2)+9+y)]
       <=4y^2/27,
 4-c_o=4y^2/[sqrt(1+y^2)(sqrt(1+y^2)+1)]>=y^2.

The third and fifth terms in(4) are nonnegative. Using log3<=2,

 (c_s-3)log3>=-8y^2/27,
 c_o log ell_o<=4(y/2+y^2/4)=2y+y^2,
 2log((1+3y)/(1+y))>=4y/(1+3y)>=4y-12y^2.

Thus

 d'(x)>=2y-(13+8/27)y^2>0 for0<y<=1/10.                (5)

These bounds do not claim that the homogeneous value tends to zero as a increases at fixed b. That is a different path from the common-noise limit in the preceding boundary theorem.

## 4. Exact middle-interval certificate

flat_rank_two_reset_scalar_interval_certificate.py proves(2)>0 on the ENTIRE interval[1/20,10] by228 adjoining adaptive rational intervals. Coverage and adjacency are checked exactly. For every such interval, natural interval evaluation of(2) produces a strictly positive lower endpoint.

The arithmetic uses Python integers, not floating point:

* Every interval endpoint is a multiple of2^(-80), with every arithmetic operation rounded outward by integer floor/ceiling.
* Square roots use integer isqrt with outward endpoints.
* Logarithms reduce to arguments in[1,2] by powers of two, then use logt=2sum_(j>=0) z^(2j+1)/(2j+1), z=(t-1)/(t+1).
* After60 terms, the positive remaining tail is bounded by2 z^121/[121(1-z^2)], evaluated outward. The same construction certifies log2.

The minimum reported interval lower bound was

 508237401513783999573/302231454903657293676544>0.

The script and JSON record precision, coverage and interval count. No sampled sign is a premise, and no non-rigorous numerical root is used.

## 5. Receiving the whole scalar value

Equations(3),(5) and the compact interval certificate prove d'(x)>0 for every x>0. Entropy continuity gives d(0)=0, so d(x)>0 for x>0. Homogeneity then proves D>0 for a,b>0. The a=0 and b=0 endpoints are reset and identity, both exact equality.
