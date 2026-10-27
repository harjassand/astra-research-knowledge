# Independent full-chain receipt: arbitrary qutrit pure main and isotropic physical reset

26 October 2026. Reviewer: audit_source_coupled_entropy. **PASS**.

Governing theorem: `arbitrary_qutrit_filtered_seed_whole_value_theorem.md`.
Final lemma: `clean_core_conditional_curvature_operator_proof.md`.

Received statement: for every psi in C3 tensor C3 and every qutrit A>=0,

Delta(P_psi+I3 tensor A)>=0.

Reference dimension at most three may be padded. This is a whole VALUE theorem for this source class, not the unrestricted WH3 inequality, a noncommuting anchored-filter comparison, or an arbitrary larger-reference reset theorem. No equality classification is received.

## 1. Independent receiving of the final determinant-gradient formula

For the clean spectator, put D(t)=det(A2+tI), N(t)=Tr[H2 adj(A2+tI)], v=det H2, s=N/D, p=v/D, k=h/t. The actual determinant-gradient integrand is

F_p/D=2/[v+(k+2)N+(k+2)^2D]-3/[v+3N+9D].

The first denominator is det[H2+(k+2)(A2+tI)]. Set u=h+2t in its integral; the numerator 2dt is exactly du. In the second integral set u=3t. These give precisely the two determinant integrals defining Ip in the governing lemma, with no missing factor two or three.

Normalized complex-qubit Haar measure satisfies E(<psi,M psi>^-2)=1/det M: in an eigenbasis the squared first coordinate is uniform on [0,1]. Applying this identity separately to the two positive integrals is legitimate by Tonelli. With alpha=<A2>, beta=<H2>, sigma=beta+3alpha, the first substitution x=u-h gives K(beta+h+2alpha,2alpha h); the second integral is 1/sigma. Thus the printed Haar formula for Ip is exact, also when A2 and H2 do not commute.

## 2. Strict lower bound for the Ip zero

The scalar K formula and logarithmic inequality were independently checked and the exact checker replayed. The cleared logarithmic difference has derivative (z-1)^4(z+1)^2/[2z²(z²+z+1)²]>=0. The equal-root limit is 1/(3r). In the present Haar application beta>0 makes c>2sqrt(d), so the K lower bound is strictly greater, not merely nonnegative.

The reciprocal tangent identity is valid for either sign of n=alpha-h-sqrt(2alpha h), since sigma-n=c+sqrt(d)>0. Weighted Cauchy uses exactly the measure sigma^-2 dHaar and gives Z²<=XY. Consequently h<=(2-sqrt3)X/Y implies Ip(h)>0.

Ip is strictly decreasing in h directly from its original t-integrand: only its first positive reciprocal term depends on k=h/t, with strictly increasing denominator. It has positive values at small h. For h>=lambda_max(A2), K(c,d)<1/c<=1/sigma pointwise, so Ip<0. Continuity and strict monotonicity therefore give a unique finite positive zero h_star and h_star>(2-sqrt3)X/Y. No numerical root premise is used.

## 3. Weighted matrix mean and determinant inequality

Set S=A2+H2/3, T=Tr S, V=det S. The matrix M=V E[psi psi*/<S>²] has trace one. Since sigma=3<S>, the factors of nine cancel exactly and X/Y=Tr(A2 M).

Differentiating the divided-log identity E[1/<S>]=integral det(S+uI)^-1 du gives M=V integral adj(S+uI)/det(S+uI)^2 du. All matrices are positive and the integrals converge. The elementary mixed-determinant inequality for positive two-by-two matrices gives

sqrt(det M)>=V integral det(S+uI)^(-3/2)du
             =2sqrt(V)/(T+2sqrt(V)).

This direction follows from homogeneity/superadditivity, or from the explicitly stated double-integral polarization, not from a false entrywise or operator determinant order. The integral formula also holds at scalar S by its continuous limit. The trace-determinant inequality then gives

X/Y>=4sqrt(BV)/(T+2sqrt(V))>=4B/(T+2sqrt(B)), B=det A2.

The last step holds T fixed and uses V>=B and monotonicity in sqrt(V). Comparing the denominators gives X/Y>=4 h_cert with the exact h_cert printed in the source. Thus h_star>4(2-sqrt3)h_cert>h_cert.

## 4. Curvature transport

The exact expansion R(2u,h)-L(u) is

2u²+(C+2h)u+h A-B+hB/(2u).

AM-GM on the two reciprocal-linear terms gives the stated threshold. The rationalized h_cert solves the unsquared equation h A+sqrt(2hB(C+2h))=B; its right-side sign is valid since h_cert A<B. At h>=h_cert the remaining 2u² makes R(2u,h)>L(u) for every u>0. The change t=2u therefore gives Q0(h)<0. Both endpoint integrals converge. This proves Ip=0 implies Q0<0 with a strict margin in the thresholds.

Executed `clean_core_conditional_curvature_operator_check.py`: PASS transport, scalar logarithmic inequality, delta factors, reciprocal tangent, determinant integral and threshold identities. Independently reacquired the determinant-gradient denominator identity and mixed Hessian, not only the helper script's algebra.

## 5. Actual fixed-trace H-only negative curvature

For a genuinely noncommuting pair, diagonalize A2=diag(a,b), a!=b, and gauge H2=[[x,z],[z,y]] with z>0. The actual curve

x_e=x+e/(b-a), y_e=y-e/(b-a),
z_e=sqrt(x_e y_e-v+3e)

is smooth and faithful for sufficiently small positive and negative e. It preserves Tr H2 and gives EXACTLY u_e=u+e and v_e=v-3e. Thus its resolvent invariants change affinely by delta s=e/D, delta p=-3e/D, with spectator fixed. This is a valid source curve at fixed reset and fixed total trace, not a fictitious independent matrix-eigenvalue variation.

Independent differentiation of F in the direction partial_s-3partial_p gives

(s+k+1)^-2-2(s+2)^-2-2(k-1)^2/[p+(k+2)(s+k+2)]².

The reference logarithm's Hessian vanishes because delta p+3delta s=0. Dividing by D² and integrating gives Q<=Q0<0. There is no missing path-acceleration contribution: u and v are affine exactly. At a local minimum their independent first derivatives give Ip=Is=0, and only Ip=0 is needed for the strict curvature theorem. No reset variation or third stationary equation is used.

Differentiation is justified at the clean boundary: A2,H2 are faithful, h>0, and the full source support ranks remain locally constant. The displayed first- and second-derivative integrands are uniformly integrable in a faithful H2 neighborhood. Near zero k~h/t but D stays positive, while the extra negative Hessian term is O(t²); near infinity the Hessian integrand is O(t^-4). Scalar A2 commutes automatically and never needs this noncommuting coordinate chart.

## 6. Complete global reduction ledger

1. Physical covariance puts any psi into the reference-Gram representation with H>=0 without changing the isotropic physical reset. The domain Tr H+3Tr A=1 is compact and the deficit continuous.
2. Singular H is already paid by the full physical 2+1 block theorem. Its newer DPI bound is an alternative representation, not a new dependency or broader scope.
3. Rank A<=1 is literally the whole coherent-star theorem: A=a|e><e| gives physical bath a I3 on one reference line with arbitrary pure main. This is not an analogy between unrelated rank labels.
4. At faithful A, the exact F integral and its received zero-surface gradients imply the scalar-floor negative-value reduction for arbitrary faithful H. The removed interval is strictly negative. Smaller positive normalization then strictly improves a negative value. This excludes a faithful reset at a negative global minimum, not unconditional reset monotonicity.
5. The remaining minimum has H>0 and rank A=2. The received actual H stationarity theorem, including rank-two-reset integrability, supplies a common eigenline. Commuting pairs are paid by the independently prior aligned CQ dilation theorem.
6. The actual transverse Hessian excludes a middle reset spectator. The independently received maximal-spectator exclusion excludes a largest one, including repeated reset spectra. Thus any remaining noncommuting negative minimum has the clean spectator and faithful A2 covered above.
7. The final actual H-only negative curvature contradicts local minimality. Hence no negative normalized source exists. Homogeneity and the zero source receive the unnormalized statement.

These earlier dependencies do not use the new whole theorem. No arbitrary-reference compact attainment, rank-opening derivative at singular reset, universal pinching, or universal fixed-spectrum orientation endpoint claim is inserted. The exact orientation and joint-balancing obstructions remain consistent with this stationary proof.

## Scope retained

The received class is precisely a qutrit pure main plus I3 tensor a reset supported in a common reference space of dimension at most three. It permits arbitrary noncommutation and arbitrary main Schmidt weights and does not require a TP source. It gives nonnegative VALUE for such a filtered seed. It does not supply lambda_min(filter*filter) times the original unfiltered value, arbitrary larger-reference coherent-reset GLS payment, a channel-capacity statement, or the unrestricted WH3 theorem.
