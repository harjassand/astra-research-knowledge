# Local conditioning of the universal optimum

This supplements FAMILY_THEOREM_v3.md without changing any prior proof bytes. Root suggested the curvature identity; the owner independently reconstructed it and instantiated it with exact rational intervals.

Let r_* be the universal one-resonator optimum and p(r)<r<s(r) its endpoint curve. Hold the stationary multipliers lambda,mu FIXED while differentiating; their moment combination lambda L+mu T is constant on the curve.

Write R(w)=g_theta(w)+lambda/w+2mu w=F(w)/w. Then
j'(r)=sum_(w=p,r,s) epsilon_w R(w) w'(r),
epsilon=(+1,-1,+1).

At the optimum every endpoint has R(w)=0. Differentiating once more eliminates every R(w)w'' term:
j''(r_*)=sum_w epsilon_w R'(w)[w'(r_*)]^2
=sum_w epsilon_w F'(w)[w'(r_*)]^2/w >0.

The strict sign follows from F'(p)>0,F'(r)<0,F'(s)>0; the middle endpoint has derivative1. Every displayed term is positive. The unique stationary root is therefore simple, so local interval-Newton or inverse-function conditioning is legitimate.

This is a LOCAL statement. No uniform curvature or condition-number lower bound is asserted near zero side mass, temperature limits, vanishing gap or extreme stiffness ratios.

## One certified attainable object

certify_design_example.py uses exact Fraction interval arithmetic,160-bit rational square-root bounds and positive100-term exponential Taylor sums with a geometric remainder. It proves, for K=1,M=2,m0=1,theta=1/2:

r_* is in[2.336273985489,2.336273985490],
k_* is in[2.7290880676363280,2.7290880676386644],
j''(r_*) is in[0.04863839147019,0.04863839147314].

The exact derivative interval at the lower endpoint is negative and at the upper endpoint positive. The certificate also encloses the physical two-band endpoints, multipliers and all three dual-slope signs. All asserted signs are rational interval assertions; rounded decimal outputs are directed outward.

The code's finite part tolerances are a numerical instantiation of the universal proof, not a parameter sweep or a proof by grid. Output is certified_design_example.json.

