# Exact large-filter obstruction to reference-axis convexity

Status: source-derived asymptotic obstruction. This does NOT refute anchored value order or the accepted-only GLS comparison.

Fix d>0 and A=diag(a,b,c)>0. Let X=3d Phi3+I3 tensor A and Z_r=diag(sqrt(r),1,1), r>=1. Write D(r) for the homogeneous deficit of (I3 tensor Z_r)X(I3 tensor Z_r). Then

D(r)=r C(a,d)+L(a,d) log r+O(1),

L(a,d)=2d^2 a/[(a+d)(2a+d)]>0,
C(a,d)=f(a+d)+f(3a+d)-4f(a+d/2)-(3a+d)log3.

Consequently D is NOT convex on[1,infinity). This conclusion needs no differentiation of the remainder: any convex function with f(r)/r tending C has f(r)-Cr nonincreasing, whereas the displayed remainder grows to positive infinity.

## Exact source acquisition of the logarithmic coefficient

Partition the reference into its filtered coordinate and its two unfiltered coordinates. Each relevant positive entropy matrix has the form

M_r=[[r H,sqrt(r) K],[sqrt(r) K*,J]], H>0.

Its high spectral block is rH+O(1), with total O(1) eigenvalue shift Tr(K*H^-1 K); its low block tends J-K*H^-1 K. Standard finite-dimensional Schur block diagonalization, or expansion in r^-1/2, gives

Tr f(M_r)=r log r TrH+r Tr f(H)
          +log r Tr(K*H^-1 K)+O(1).

For the actual input, H=aI3+dP0 and KK*=2d^2 P0. Thus its logarithmic coefficient is2d^2/(a+d).

For the WH output, H=aI3+(d/2)(I3-P0) and KK*=(d^2/4)(I3-P0). Its coefficient is d^2/(2a+d). The reference marginal is diagonal, so has no off-diagonal coupling shift and no O(log r) correction. The trace-log3 term is affine in r. The total rlog r terms cancel exactly by the homogeneous deficit's masses. Hence the stated L is input minus twice output.

All matrices are strictly positive for a,b,c>0; the block expansion and bounded low entropy terms are therefore directly justified. No singular limit is needed for the obstruction. For example d=a=b=c=1 gives L=1/3>0.

This explains why even a received positive derivative at the unfiltered seed cannot be integrated by invoking reference-filter convexity. It leaves monotone increase, finite anchored lower bounds, and the actual coherent-reset value problem open.
