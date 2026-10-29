# A complete rational search for coercive smooth heat-form certificates

30 October 2026. Root construction following A's successful rational-angular
certificate. This is a proposed general theorem, pending independent challenge.
It credits ordinary polynomial approximation and matrix Reznick machinery.
Completeness is for the stated COERCIVE HEAT-FORM witness class, not for
quasiconvexity or rank-one convexity themselves. No polynomial runtime or
unconditional termination on an arbitrary quasiconvex energy is claimed.

Let F be a rational homogeneous quartic on2-by-2 matrices and D_nu its
compatible-jet dissipation from HEAT_BRIDGE.md, with a real skew-flow parameter
nu. Suppose there exists a one-form alpha, smooth off0 and homogeneous of
degree3, C2 at0, and an eta>0 with

    D_nu F(A,h)+(dalpha)_A(B1,B2)>=eta |A|²|h|²         (1)

for EVERY A,h. The flow parameter need not initially be rational. The claim
is that some finite pair k,N>=0 admits a rational nu, rational homogeneous
one-form numerator P of degree2k+3, and rational PD Gram Q such that

    T^N {T^(k+1) D_nu F +[T dP-k dT wedge P](B1,B2)}
          =z^T Q z,                                   (2)

where T=|A|² and z lists degree d=k+2+N monomials in A times each h_j.
The rational form P/T^k therefore proves full strong quasiconvexity through
the already reconstructed Stokes/skew-heat receiver. Its origin regularity
is still C2: its coefficient functions have degree3, independently of k.

## 1. Density at the operation that matters

Since the quartic dissipation is even in A, replace alpha by its odd part
[alpha(A)-alpha(-A)]/2; its exterior derivative averages the old corrections
at A and -A, preserving(1). Approximate each odd coefficient of alpha onS3
in C1 by a rational odd polynomial p. One elementary density route extends
it smoothly to an annulus, multiplies by a radial cutoff supported away from
the origin and periodically inside a cube, uses Fejer approximation of it
and its first derivatives, then approximates the finite trigonometric sum
by Taylor polynomials in C1. Rational coefficient approximation and odd
symmetrization retain arbitrary desired accuracy. Thus the density claim
does not demand an oracle for a best approximant.

Choose a common odd degree D=2k+3 above every degree present, increasing it
to at least3. Homogenize

    P(A)=sum_beta p_beta A^beta T^((D-|beta|)/2).

OnS3, P/T^k agrees with p and its tangential derivative. Its radial
derivative is3p, while alpha's is3alpha. Tangential C1 approximation plus
value approximation therefore controls the FULL first derivative onS3.
Uniformly small error controls the exterior-form evaluation on B1,B2,
since |B1||B2|<=(|B1|²+|B2|²)/2<=|h|². Positive homogeneity extends this
error as a constant times T|h|². Approximate nu rationally too; the fixed
quartic's bounded Hessian onS3 controls that additional error. Choose both
errors so the corrected dissipation remains>=eta/2 T|h|².

No effective degree bound is inferred merely from existence of alpha.
Given derivative/modulus and margin bounds, the approximation argument can
be made effective; acquiring those bounds is a separate stronger contract.

## 2. The numerator has an ordinary matrix positivity certificate

For the rational P,nu just obtained, write

    T^(k+1)D_nu F+[T dP-k dT wedge P](B1,B2)=h^T M(A)h.

M is a rational symmetric polynomial matrix, homogeneous degree2k+4 and
positive definite for every A!=0. In fact M>=eta/2 T^(k+2) I6. Choose a
positive rational epsilon<eta/2. The matrix M-epsilon T^(k+2)I remains
strictly positive away from0.

Apply Zheng--Fantuzzi2007.11410v2, Theorem2.3, with the COMPLETE sparsity
graph (one clique). The theorem, read at its actual statement, supplies an
integer N for which T^N[M-epsilon T^(k+2)I] is an SOS matrix. Hence T^N M
has an SOS Gram PLUS epsilon T^(k+2+N)I. The latter has a strictly positive
DIAGONAL Gram in the full homogeneous monomial-times-h basis. The resulting
Gram is therefore PD, not only a boundary real SOS representation.

https://arxiv.org/html/2007.11410v2

The identity constraints have rational coefficients. A nonempty affine
rational solution space has a rational particular point and rational basis;
its rational points are dense in its real points. The PD Gram can therefore
be approximated WITHIN that identity space by a rational PD Gram. This
pays the exact rational certificate in(2), rather than assuming arbitrary
rounding preserves an SOS identity. The matrix theorem is the ordinary
constructive predecessor; a generic scalar SOS assertion was insufficient.

## 3. What the search and its converse actually establish

For fixed k,N, equation(2) is affine in P,nu,Q. One may search bounded
coefficient boxes by ordinary SDP and qualify exact identities and PSD
afterward. A completely exact semidecision procedure dovetails rational
coefficient/Gram candidates of growing degree/bit size, checking(2) and
Q>0 with exact arithmetic. Existence above guarantees eventual acceptance
under premise(1). This existence guarantee is not a practical runtime bound
for that enumeration or for a particular floating SDP implementation.

Conversely any accepted finite certificate implies a coercive correction.
If Q>=rho I and C_d is the maximum multinomial coefficient in T^d, then
sum_(|beta|=d)A^(2beta)>=T^d/C_d. Dividing(2) by T^(N+k+1) gives

    D_nu F+d(P/T^k)>=rho/C_d T|h|².

The origin is filled by continuity. HEAT_BRIDGE.md supplies the full-domain
Jensen consequence. Thus every finite success is sound and every smooth
strict witness of the specified type has a finite rational success.

A's literal original quartic is a paid nontrivial member k=1,N=0, not a
numerical demonstration of the general completeness theorem. Closed-form
existence without strict margin, all QC functions, all ROC quartics, generic
nonhomogeneous energies and finite-level failure are OUTSIDE the converse
termination guarantee. Failure at a finite level proves none of their
negations. The proposed scientific gain is a repeatable search over a much
larger proof-operation class, not a universal solution of Morrey's problem.
