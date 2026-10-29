# One completed exact critical-point oracle instance, independent of SOS
2026-10-29. Author computation and proof, receiving review pending. This is ONE complete acquired-bank instance, not yet a generic all-input solver or a bit-complexity theorem.

## Input and exact stationary equations
Input is `bank_one_axis.json`, edge0, with29,916 probes. The homogeneous quarticF is reconstructed exactly by the same verified bank formula. On the real unit sphere every global extremum satisfiesgradF=lambda q. BecauseF is homogeneous of degree4, a ray withq0!=0 can be represented byq=(1,x,y,z). Its stationary equations are the three quartics
 P_i=partial_i F(1,x,y,z)−u_i partial_0 F(1,x,y,z)=0, i=1,2,3.
No division by1+x²+y²+z² is used to construct this ideal, avoiding spurious complex isotropic components introduced by multiplying a rational-gradient equation.

`critical_chart_attempt.py` computes an exact rational/primitive-integer Groebner basis in grevlex order, then FGLM converts it to lex order. The output in `critical_chart_result.json` has three shape equations
 A x+P39(z)=0, B y+Q39(z)=0, H40(z)=0,
whereA,B are nonzero constants. The first two polynomials are NOT assumed monic: the evaluation code explicitly divides byA,B. The shape basis is the same ideal as the original stationary equations by the exact Groebner/FGLM operations. This is reproducible symbolic-computation evidence, not a separately exported formal proof-assistant trace.

## No missed real boundary extrema
Forq0=0, `check_missing_chart.py` computes the exact ideal
 {partial_0F(0,x,y,z), partial_xF−lambda x, partial_yF−lambda y,
  partial_zF−lambda z, x²+y²+z²−1}.
Its Groebner basis is[1], recorded in `missing_chart_result.json`. Thus there are no complex solutions of this normalized system, in particular no missed real stationary points withq0=0. This statement does not by itself exclude complex isotropic PROJECTIVE boundary rays; those are irrelevant to this one real-sphere certificate, but matter for any later generic-family argument.

## All real roots and exact value intervals
H40 is squarefree. `isolate_chart_roots.py` isolates ALL its real roots into four disjoint rational intervals. Every real root supplies realx,y by the shape equations, and conversely every real chart stationary point is represented. `certify_critical_values.py` refines those intervals, evaluatesx,y by rational interval Horner arithmetic, and bounds
 F(1,x,y,z)/(1+x²+y²+z²)²
on each full interval box. It divides by4N to report mean estimated loss. The denominator is bounded strictly away fromzero. Taking the smallest of the four lower endpoints is a global sphere lower bound, because every global minimum is one of these stationary rays and the boundary case has been excluded.

For the upper bound, a numerical proposal from those roots is converted to an exact rational unit quaternion; its original quartic is evaluated rationally. Numerical root selection affects only which valid feasible upper bound is used. It does not establish the lower bound or omit any stationary value. Exact ties need not be decided: interval refinement suffices for an additive global certificate.

The resulting `critical_global_certificate.json` has certified global mean-loss gap1.596e−19. It contains rational root/value bounds and the rational physical quaternion. The complete recorded computation cost was about0.45s forgrevlex,50.4s forFGLM,0.48s forboundary exclusion,0.14s forinitial root isolation and6.1s forvalue certification. Shape coefficients reach10,692bits. These figures are one execution, not a uniform latency guarantee.

## Limits and next obligation
This instance assumes neither SOS representability nor a free global optimizer. Nonetheless degenerate/positive-dimensional or non-shape ideals are not handled by this specific script. A complete universal critical-point controller would need an explicit perturbation/coordinate mechanism, certified all-input termination, arbitrary-precision rational candidate construction, timing/privacy control and bit costs. Those are not supplied by the existence of this one shape basis. The already accepted exact grid fallback remains the completed general route.
