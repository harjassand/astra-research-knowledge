# Exact logarithmic-corner reduction for Schmidt-rank-two source topfaces

2026-10-25. A proved analytic reduction, not yet a proof of all four corner inequalities.

Use the exact physical source reduction in source_topface_symmetry_reduction.md. Write u=(sqrt(p),sqrt(q)), p+q=1, 0<p,q<1, P=uu*, and X=P+t(I-P), 0<=t<=1. Define d1=p+tq, d2=q+tp and a=(1-t)sqrt(pq). The complete feasible marginal rectangle is

b_j in [d_j/3,(d_j+2)/3].

For C=(X+3diag(b1,b2))/4 set

j(p,t,b1,b2)=p log b1+q log b2-2<u,log C u>.

## Theorem: separate concavity in logarithmic marginal variables

For each fixed p,t and fixed other marginal entry, j is concave as a function of log b_j. Consequently

min_{physical b1,b2} j
 = min_{e1,e2 in {0,1}} j(p,t,(d1+2e1)/3,(d2+2e2)/3).

This is equality for the true source rectangle, not an independent-moment relaxation. It reduces the entire aligned Schmidt-rank-two topface question, in every reference dimension, to four explicit two-parameter functions. By swapping p and q there are only three types of corner.

### Proof by an exact two-dimensional Schur integral

Fix the varied diagonal coordinate j, denote the other coordinate i, and write

C(y)=[[c+y,h],[h,d]]

in order (j,i), where y=3b_j/4>0, c=X_jj/4, h=X_ij/4>=0, and d=(X_ii+3b_i)/4. The test vector in this order is (v,w)=(u_j,u_i), both nonnegative. Crucially,

vd-hw=(t+3b_i)v/4>=0.                              (1)

Let F(x)=<u,log C(exp x)u>. For s>=0 define

z(s)=s+c-h^2/(s+d),
W(s)=(v-hw/(s+d))^2.

C(0) is positive definite when t>0 (and also for t=0 if p,q>0 and b_i>0), so z(s)>0. The resolvent's j component acting on u is (v-hw/(s+d))/(z(s)+y). Differentiating the logarithm's resolvent formula twice with respect to x=log y gives

F''(x)=y integral_0^infinity W(s)(z(s)-y)/(z(s)+y)^3 ds.

As z'=1+h^2/(s+d)^2, integration by parts yields

F''(x)=y [W(0)/z'(0)] z(0)/(z(0)+y)^2
       +y integral_0^infinity (W/z')'(s) z(s)/(z(s)+y)^2 ds.

The boundary at infinity vanishes. Putting r=s+d,

W/z'=(vr-hw)^2/(r^2+h^2),
(W/z')'=2h(vr-hw)(wr+hv)/(r^2+h^2)^2>=0,

where the sign follows from (1) and r>=d. Thus F''>=0. Scaling y=3b_j/4 shifts the logarithmic parameter by a constant and does not affect convexity. The weighted logarithm p log b1+q log b2 is affine in each logarithmic parameter, proving the claimed separate concavity of j. Apply the endpoint minimum property first in one coordinate, then the other.

## Automatically safe corner and subregion

If both b1,b2>=1/9, then for every b in [1/9,1], 4sqrt(b)-3b>=1. Therefore

X<=I<=4sqrt(B)-3B, C<=sqrt(B),

and operator monotonicity gives j>=0. In particular the (1,1) corner is safe. Since b1+b2>=1/3, any remaining obstruction has exactly one marginal entry below 1/9.

## Remaining two corner types

The (0,0) corner has B=diag(d1,d2)/3 and C=(X+diag(d1,d2))/4. The mixed (0,1) corner has B=diag(d1,d2+2)/3 and

C=[[d1/2,a/4],[a/4,(d2+1)/2]].

The other mixed corner follows by p<->q. A numerical diagnostic suggests the (0,0) value increases with t, while the (0,1) value decreases with t; neither derivative sign is asserted as a theorem here. The mixed endpoint t=1 is exactly p log(4/3)>=0. Closing those derivative signs or finding a different bound would finish the aligned Schmidt-rank-two top-log principle. All unrestricted WH3 claims remain open.
