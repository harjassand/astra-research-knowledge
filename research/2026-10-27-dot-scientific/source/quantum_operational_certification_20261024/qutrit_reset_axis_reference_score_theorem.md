# Axisymmetric unfiltered reference-score receiving

Status: independently PASS; see `qutrit_reset_axis_score_independent_audit.md`. This receives only an infinitesimal exceptional-axis reference filter, not general finite anchored filter order or accepted-only GLS monotonicity.

For d>0 and A=diag(a,b,b)>=0, let X=3d Phi3+I3 tensor A. The homogeneous deficit derivative under the reference filter Z_epsilon=diag(sqrt(1+epsilon),1,1) at epsilon=0 is nonnegative. With positive noise it is strictly positive. The exact source acquisition is `qutrit_reset_anchored_reference_score_interface.md`:

Q1=d integral_0^infinity s/(a+s)^2 g1(d/(a+s),d/(b+s),d/(b+s)) ds.

Homogeneity reduces d to1. For b>=1, the factorization

g1(x,y,y)=2(1-y)(x+3y)/[(x+3)(x+y+2)(x+2y+1)]

makes the integral positive. Suppose 0<=b<1 and theta=1-b. Its unique crossing is s=theta. Write v=b/theta,w=a/theta,z=s/theta, all nonnegative. The pure-seed baseline

q0(z)=4(z-1)/[(z+1)(z+3)(3z+1)]
      =-3/(3z+1)-1/(z+3)+2/(z+1)

has integral0 on(0,infinity), negative below1 and positive above1. Let q(s)=s g1/(a+s)^2. Direct exact cancellation gives

q(s)/(q0(z)/theta)=R(z)=N/(2ABC),

A=v+3w+3z+1,
B=v^2+3vw+4vz+v+wz+2w+z^2+3z,
C=v^2+3vw+4vz+v+2wz+w+2z^2+2z,
N=z(v+1)(z+1)(z+3)(3z+1)(v+3w+4z).

All denominators are positive for z>0. Exact differentiation gives

R'(z)=P(v,w,z)/(2 A^2 B^2 C^2),

where P has177 monomials, every nonzero coefficient a strictly positive integer between3 and65208. The companion script constructs this polynomial from the displayed rational function using exact integer arithmetic, checks every coefficient, reacquires the ratio from the actual source kernel, and checks the baseline integral exactly. Thus R is nondecreasing. It is constant only at v=w=0, where it equals1; with v+w>0 its derivative is strictly positive on z>0 (also checked by the exact coefficient representation).

Consequently [R(z)-R(1)]q0(z)>=0 pointwise and

Q1=integral_0^infinity [R(z)-R(1)]q0(z) dz>=0.

Convergence follows from the original source integral and the baseline integrability; R has a finite limit at infinity. This subtraction is the missing compensation: a single crossing alone would not determine the sign. Endpoint a=0 or b=0 follows either from the same rational formula at positive z or entropy continuity. At a=b=0, Q1=0, consistently with the zero first variation of the maximally entangled pure seed.

No assertion is made here about the repeated-axis coordinate scores for diag(a,b,b), nor about finite reference filters. The general anisotropic ratio remains an open candidate, not a theorem.
