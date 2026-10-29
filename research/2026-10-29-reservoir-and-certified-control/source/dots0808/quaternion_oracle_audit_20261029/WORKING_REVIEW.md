# Quaternion optimization/controller working review
2026-10-29. Partial findings; not a receipt for the forthcoming complete FTPL algorithm.

## Checked now
The actual bank f(q) is four times cumulative signed star-loss estimator on the unit quaternion sphere. The convention V=wI−i(xX+yY+zZ) gives exactly the author's matrix R(q), not its transpose. Independent physical SU(2) trace calculation at 30 rational quaternions across all six bank/certificates passed exactly. Replayed author verifier in a copied audit tree: all six exact coefficient identities, unit quaternion upper values, and positive rational LDL decompositions passed. Certified mean-objective gaps range from 8.66e-11 to 1.74e-10. Floating optimizer timings are demonstrations, not worst-case running-time guarantees.

A rational positive-definite Gram for f−lambda||q||^4 is an actual global lower certificate. Approximate numerical optimization has no authority until the exact verifier succeeds. Strict positive pivots suffice; inability to certify a semidefinite boundary is not proof of infeasibility. A positive rational safety shift can make a valid lower certificate weaker, not false.

## Exact non-SOS obstruction
Let p=x²y²+y²z²+z²x²+w⁴−4xyzw. AM-GM gives p≥0 and p(1/2,1/2,1/2,1/2)=0. If p were a sum of squares of quadratic forms, zero coefficients of x⁴,y⁴,z⁴ force every quadratic form's x²,y²,z² coefficients to vanish. Then absent x²w²,y²w²,z²w² force every xw,yw,zw coefficient to vanish: there are no remaining x²·w² etc cross terms able to cancel these squared coefficients. The remaining possible monomials xy,xz,yz,w² cannot produce xyzw. This contradicts its coefficient −4. Thus the degree-four SOS fast path is genuinely incomplete. A numerical negative lower bound alone would not prove this impossibility or the optimal relaxation gap.

## General fallback available
For f(q)=sum_e a_e q^e on S³, let A=sum|a_e|. On the unit cube its gradient l1 norm is at most 4A, hence |f(q)−f(r)|≤4A||q−r||infinity≤4A||q−r||2. Hemisphere q0≥0 is covered by one stereographic chart q(u)=((1−||u||²),2u)/(1+||u||²), ||u||≤1. A grid u=k/m with each k∈[−m,m] covers this ball to Euclidean distance sqrt(3)/(2m); the map is globally 2-Lipschitz. Thus every sphere point up to sign has a grid quaternion within sqrt(3)/m, and `min_grid f−4 sqrt(3) A/m` is a global lower bound. The rational looser correction `7A/m` suffices. Choose m to reach a requested positive additive tolerance. All objective evaluations and grid quaternion coordinates are rational. The grid is cubic in m, but may be enormous; this is not a practical runtime claim. A=0 is handled immediately. Degenerate minima require no gap premise.

## Approximate FTPL proof checks to request
For cube perturbation coordinate z uniform on [−R,R], fix the other coordinates and past coefficients. Define concave F(z)=min_x(a·x+z x_i), with all feature coordinates in[−1,1]. An epsilon-argmin x_epsilon satisfies
`(F(z+h)−F(z))/h−epsilon/h <= x_epsilon,i <= (F(z)−F(z−h))/h+epsilon/h`.
The exact expected minimizing coordinate equals the averaged derivative of F (ties occur on a null set or the derivative agrees). Integrated finite differences differ from the derivative average by at most h/R; therefore
`|E x_epsilon,i−E x_exact,i| <= h/R+epsilon/h <= 2 sqrt(epsilon/R)`
using h=sqrt(epsilon R). The bound may be capped at2. For a current coefficient g independent of the fresh perturb given actual past, the bias is at most `2||g||1 sqrt(epsilon/R)`, not automatically O(epsilon).

A finite uniform midpoint grid with 2^b points per coordinate couples to continuous uniform perturb within R/2^b per coordinate. A grid epsilon-argmin is an `(epsilon+2dR/2^b)`-argmin for the coupled continuous perturb. This is a proof coupling, not a physical continuous-random oracle.

Remaining obligations before acceptance: full adaptive-history potential telescope and constants, fresh per-round perturb rather than reused hidden randomness, actual product-probe record independence of the current chosen frame, exact finite coin/arithmetic contract, fallback integration with certified tolerance, source-clock/key privacy (padding optimizer latency to an honest deterministic bound), quantum-control synthesis/precision costs, and strongest existing finite learner comparator. No FTPL acceptance yet.
