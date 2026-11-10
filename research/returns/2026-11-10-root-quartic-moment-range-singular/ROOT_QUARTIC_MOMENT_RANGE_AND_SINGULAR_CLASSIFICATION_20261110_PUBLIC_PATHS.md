The affine-mean range condition and singular fields for the original quartic

Fix k>1/3 and the original density J_k from the supplied quartic research packet. Let G=Dphi be a real mean-zero periodic compatible L4 gradient, and set c=integral J_k(G), b=integral DJ_k(G), H=integral D2J_k(G), with matrices identified with R4. Assume the accepted rank-one convexity and all-background small-original-gradient quasiconvexity. No full arbitrary-amplitude conclusion is assumed.

1. H is positive semidefinite for a specific reason. The symmetric four-linear polarization of the homogeneous quartic gives
  Z:H Z=integral D2J_k(G)[Z,Z]=integral D2J_k(Z)[G,G].
The last integrand is a CONSTANT quadratic form in G. On each Fourier gradient mode it is nonnegative by the Legendre-Hadamard condition at Z. Summing Fourier modes proves the assertion. Rank-one convexity of a variable Hessian alone would not have justified an arbitrary average-Hessian claim without this quartic polarization identity.

2. The range condition is already automatic. Take Z in ker H. Each Fourier contribution to the last nonnegative sum is zero. Periodic finite Fejer approximations G_N preserve those modewise acoustic nullspaces, are compatible and smooth, and converge strongly in L4 to G. For any fixed N, accepted local quasiconvexity at background Z applies to t G_N for both signs of sufficiently small t. The exact quartic identity is
  integral J_k(Z+tG_N)-J_k(Z)
   =(t^2/2) Z:H_(G_N) Z+t^3 b_(G_N):Z+t^4 c_(G_N)
   =t^3 b_(G_N):Z+t^4 c_(G_N).
Both signs force b_(G_N):Z=0. Cubic growth and strong L4 convergence imply b_(G_N)->b, hence b:Z=0. Since H is symmetric finite-dimensional, b belongs to range H. This argument is a deduction from accepted local stability, not a fresh proof requirement for that result.

Consequently the unrestricted full question reduces to the SINGLE sharp inequality
  b^T H^dagger b<=2c
for all compatible G. No separate range failure can yield a valid counterexample under these premises. The constant 2 is not improved or established by this deduction.

3. For this family, the newly supplied complete acoustic zero classification sharpens the singular case. The packet's family_geometry.txt states that every nonzero background/nonzero rank-one zero pair is one of
  (F,E)=(t Q, a Qe1 tensor e2),
  (F,E)=(t Q B_k, a Qe1 tensor e1),
where Q is in SO2, t,a are nonzero, and B_k=[[0,k],[1,0]]. Use this exact table as a supplied premise.

If G is nonzero and H is singular, choose nonzero Z in ker H. Every nonzero real and imaginary Fourier amplitude must form one of these zero pairs with the SAME Z. In the first orbit all its frequencies are parallel to e2 and all output amplitudes are parallel to the same Qe1; in the second they are parallel to e1 with the same output direction. The two orbits cannot coexist for the same Z, since their backgrounds have opposite determinant signs. Hence, up to a constant left rotation and amplitude,
  G=(Qe1 tensor e_i) g(x_i),  i=1 or 2,
with real mean-zero scalar g. Conversely any such nonzero G has a one-dimensional H kernel, by the same zero table and integral g^2>0, so rank H=3.

Every one of these singular cases satisfies the FULL all-mean inequality already: for every A, the scalar function r->J_k(A+(Qe1 tensor e_i)r) is convex by rank-one convexity, and ordinary scalar Jensen applies to g. The zero field is trivial. Thus a strict negative witness, if any, can always be sought among fields with H POSITIVE DEFINITE. This statement gives no uniform lower eigenvalue bound near the one-direction shear set, and no finite counterexample search bound.

4. Constructive boundary opened and limit retained. For nonsingular H, the exact minimizing mean is -H^-1 b and the exact minimized gap is c-b^T H^-1 b/2. The single inequality above is still an unrestricted gradient moment problem. Approaching a one-direction shear can make H ill-conditioned; positivity at each singular field alone is not a quantitative neighbourhood estimate or the full theorem. The packet's arbitrary-convex-g scalar projection inequality and unmatched infinite-scale projection blocks are genuinely different compatible constructions from the excluded constant heat generators and finite locally polyconvex block sums. No representation, touching minorant, quantitative cubic bound or full J_k result is supplied here.
