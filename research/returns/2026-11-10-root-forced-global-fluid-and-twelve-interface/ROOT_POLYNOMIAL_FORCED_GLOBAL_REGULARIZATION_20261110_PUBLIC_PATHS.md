Polynomial common forcing that gives global strong continuation

Premise. The completed enlarged-family compiler supplies one common rational additive force for all mean-zero divergence-free H1 inputs of norm<=M, with polynomial numerical physical resources. For its active interval [0,d] it constructs a strong solution for EACH admitted L-infinity_t L2_x disturbance, identifies ALL Leray-Hopf realizations with it, returns the carrier to zero, and gives
  ||U(d)||2<=e/2, ||U(d)||H1<=4M.
The compiler's tolerance is positive and reciprocal-polynomial, its active duration is <=tau/2, and its force is zero afterwards. The fixed spatial family and precomputation are retained. This uses the actual blockwise estimate of completed657D79, not the earlier exponential-strain transfer.

Claim. One can choose a smaller internal target and disturbance tolerance, still with polynomial numerical resources, so that the SAME common force yields a unique global strong solution from every admitted H1 initial velocity and every admitted disturbance on [0,infinity). All Leray-Hopf realizations agree with it. The force ends before tau/2, and the velocity is small at tau and remains in a small-L2/bounded-H1 invariant region afterwards. This is a FORCED regularization/control theorem; no unforced arbitrary-data global regularity is inferred.

Elementary post-control estimates. For mean-zero u on the unit torus let
 y=||u||2^2, z=||grad u||2^2, r=||Delta u||2^2.
Every nonzero Laplace eigenvalue is >1, so z>=y, r>=z and z^2<=yr. The Fourier Agmon inequality ||u||infinity<=16||u||H1^(1/2)||u||H2^(1/2), together with mean-zero equivalence ||u||H1<=sqrt(2z), ||u||H2<=2sqrt(r), gives
 |<B(u,u),Delta u>|<=64 z^(3/4)r^(3/4).
Young's inequality and |<h,Delta u>|<=eta sqrt(r) therefore imply, with the deliberately loose explicit C_H=2^80,
 z'+nu r<=C_H nu^-3 z^3+4nu^-1 eta^2.
The ordinary energy inequality similarly gives
 y'+nu z<=nu^-1 eta^2.
These estimates require only the actual L2 disturbance bound, not its derivatives.

Set C=2^50 and define
 Y=nu^4/(C^2 M^2), Z=16M^2, eta_g=nu^3/(8CM).
As long as y<=Y and z<=Z, use z^3<=yzr and
 C_H nu^-3 yz <=16 C_H nu/C^2 <nu/2
to obtain
 z'+(nu/2)r<=4nu^-1 eta_g^2.
At the boundary y=Y the energy estimate gives y'<=-nu Y+eta_g^2/nu<0. At z=Z the last displayed inequality, r>=z and eta_g^2=nu^2 Y/64 give z'<=-nu Z/2+nu Y/16<0. Thus the rectangle 0<=y<=Y,0<=z<=Z is forward invariant. This argument concerns actual physical norms and uses no changing-coordinate metric in the post-control interval.

Choose the compiler's internal target
 e_int=min(epsilon, nu^2/(CM)).
Run the completed polynomial compiler with that target and the original M,nu,tau. Reduce its output tolerance further to eta=min(eta_compiler,eta_g). Reducing the disturbance allowance preserves every active-interval conclusion. At the end of control,
 y(d)<=e_int^2/4<=Y/4, z(d)<=16M^2=Z.
The invariant region and standard H1 continuation therefore extend the strong solution for every finite time. Weak-strong uniqueness applies on each finite interval, so every corresponding Leray-Hopf realization equals it globally. The H1 bound may remain of order M; only the L2 bound is claimed small. If desired, replace e_int by min(epsilon,nu^2/(CM),epsilon/2) to retain additional endpoint slack.

All-time disturbance quantifier. The output force is prescribed only over its finite active interval and is then zero. The new statement quantifies over arbitrary future measurable mean-zero divergence-free h with sup_(t>=0)||h(t)||2<=eta. It does not assume a future force profile, a stationary disturbance or feedback. If the intended model specifies h only until tau, extend by any admitted future disturbance; the bound is uniform over that extension.

Resources. Since e_int^-1<=epsilon^-1+CM nu^-2, the new numerical size is bounded by a fixed polynomial in the old R=2+M+nu^-1+tau^-1+epsilon^-1. Its binary description has O(L) bits plus fixed constants. The completed compiler's polynomial bounds remain polynomial after this substitution; eta_g^-1=8CM nu^-3 is also polynomial. No new spatial family, physical phase, infinite-time actuation, solution oracle or computational search is added. The strong-solution proof may contain large finite uniqueness constants; zero initial discrepancy makes them irrelevant to the quantitative tolerance.

Scope and limit. The construction supplies common forced global regularization, with finite-time polynomial actuation and subsequent small-forcing strong continuation. It does not prove the unforced Navier-Stokes Millennium statement, regularity under arbitrary large future forcing, a practical-sized fixed precomputation, or a twelve-fundamental-actuator realization. The last physical actuator question still requires its own nonlinear common-input implementation.
