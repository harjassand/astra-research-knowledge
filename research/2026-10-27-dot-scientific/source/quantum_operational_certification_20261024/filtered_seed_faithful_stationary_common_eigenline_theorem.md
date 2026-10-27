# A faithful fixed-reset stationary filtered seed has a common eigenline

26 October2026. Exact source-derived stationary reduction, submitted for audit. No whole-value or anchored-gap conclusion is inferred.

## Statement

Let H be a faithful qutrit matrix and A be a PSD qutrit matrix and consider the actual source

 X(H,A)=|(I tensor sqrt(H))Omega3><...|+I3 tensor A.

If H is stationary for Delta(X(H,A)) under ALL Hermitian variations preserving TrH, with A fixed, then H and A have a common reducing eigenline. Singular A is received in the final section below. For simple A, in its eigenbasis H has at most one nonzero off-diagonal pair.

This is a stationary reduction, not an exact same-data replacement. It is consistent with the Fourier obstruction to a same-data common-eigenline replacement. In particular, any faithful joint normalized minimum in the full H,A family satisfies the hypothesis because the stated H variations preserve the actual source trace.

## Actual derivative invariants

Use the exact source kernel Delta=integral F(K(t))dt, where K=sqrt(H)(A+tI)^(-1)sqrt(H), with invariants T=TrK,E=e2(K),P=detK. Write

 O=1+T+(T^2+E)/4+(TE-P)/8,
 R=1+T/3+E/9+P/27,
 F=2logO-3logR-log(1+T).

The root proof `filtered_seed_trace_invariant_monotonicity.md` establishes F_T>0 on the actual positive spectral domain. Direct differentiation gives

 F_P=-1/(4O)-1/(9R)<0.

In an A eigenbasis, A=diag(a1,a2,a3), define finite real integrals

 alpha=int F_T/det(A+tI) dt >0,
 beta=int t F_T/det(A+tI) dt >0,
 c=int F_E/det(A+tI) dt,
 j=int t F_E/det(A+tI) dt,
 n=int F_P/det(A+tI) dt <0.

Faithfulness bounds all integrands near zero. At infinity F_T=O(1/t), F_E=O(1),F_P=O(1), so these integrals and the differentiated source kernels converge. There is no eigenvalue-order or simultaneous-diagonalization hypothesis on K(t).

## First necessary equation: actual orientation variations

At fixed H spectrum the independent overlap data are m_i=H_ii and ell=Tr(A adjH). Their derivatives are

 d_i=int F_T/(a_i+t) dt, and c.

The d_i themselves may be understood directly through the convergent source derivative; differences certainly converge and obey

 d_j-d_i=-(a_j-a_i)(alpha a_k+beta),

where k is the remaining index. Orientation stationarity therefore gives

 [H,diag(d_i)]+c[adjH,A]=0.

For distinct a_i,a_j this is exactly

 (1) c(adjH)_ij=(alpha a_k+beta)H_ij.

The scalar determinant and Tr(adjH) terms are fixed under orientation, which is why no n or j term occurs here.

## Second necessary equation: actual off-diagonal main variations

Vary H_ij and its conjugate with all diagonal entries fixed. Such variations are two-sided feasible because H>0 and preserve TrH. At the kernel level T does not change, while

 delta E= -2(a_k+t) Re(conj(H_ij)delta H_ij)/det(A+tI),
 delta P= 2 Re(conj((adjH)_ij)delta H_ij)/det(A+tI).

The real and imaginary stationary equations give

 (2) n(adjH)_ij=(c a_k+j)H_ij.

These are variations of the actual source H, not an independent relaxation of T,E,P.

## Simple reset spectrum

If c=0, equation(1) forces every off-diagonal H_ij=0 because alpha a_k+beta>0.

Suppose c is nonzero. If two off-diagonal pairs are nonzero, their complementary eigenvalues a_k,a_l are distinct. Combining(1),(2) on each pair yields

 n(alpha a_k+beta)=c(c a_k+j),
 n(alpha a_l+beta)=c(c a_l+j).

Subtracting forces n alpha=c^2, impossible because n<0 and alpha>0. Hence at most one off-diagonal pair is nonzero, and the remaining coordinate is a common reducing eigenline.

## Repeated reset eigenvalues

If A is scalar, every H eigenline is already common. Otherwise let A=diag(a,a,b), a!=b. Use a unitary within the first two coordinates to diagonalize the corresponding2x2 principal H block, so H12=0. The DIRECT off-diagonal stationarity equation(2) on that zero pair gives

 n(adjH)12=n H13 H32=0.

Since n<0, at least one of H13,H23 vanishes. The corresponding coordinate in the repeated-A plane is then a common reducing eigenline. This proof uses only the finite coefficients c,j,n, not alpha or orientation differentiation. It therefore also handles the rank-one-reset case A=diag(0,0,b) without a divergent coefficient.

## Singular reset receiving

For rank(A)=2, the three eigenvalues of K(t) have orders t^(-1),1,1 with positive finite constants as t tends to zero, because H is faithful. Thus T,E,P are O(t^(-1)), O is of order t^(-2), and R is of order t^(-1). The displayed derivative formulas give F_T,F_E,F_P=O(t). Since det(A+tI) is of order t, all five coefficients alpha,beta,c,j,n and the d_i converge at zero. The same actual derivative equations therefore hold, including simple A with one zero eigenvalue. If its two positive eigenvalues coincide, use the repeated-eigenvalue argument.

For rank(A)=1, write A=diag(0,0,b), b>0. Two K eigenvalues have order t^(-1), and the third has a positive finite limit. Consequently T=O(t^(-1)), E,P=O(t^(-2)), O has order t^(-3), and R has order t^(-2). Hence F_T=O(t), F_E,F_P=O(t^2). The coefficient alpha may diverge and is NOT used. The coefficients beta,c,j,n and d_i remain finite. The direct off-diagonal equation(2) is finite. Diagonalize H on the zero-A plane and use the repeated-eigenvalue proof, which invokes only n H13 H32=0 and no alpha. The cross-pair orientation differences also remain finite, but are unnecessary. If A=0, a common eigenline is automatic.

The actual source spectra have constant nonzero ranks under sufficiently small faithful-H variations at each fixed rank of A. Equivalently, the positive Gram matrices on the relevant fixed success/reset spans have locally fixed support dimension. The above integrable resolvent derivative bounds receive the differentiated entropy identities without inventing a logarithm on a moving zero space. The same bounds hold uniformly in a small compact neighborhood of a fixed faithful H. No derivative in a direction opening reset rank is invoked.

## Exact scope

- The result applies to faithful stationary H at fixed PSD A and fixed main trace, including joint finite-dimensional normalized minima.
- It does not assert that every fixed-A minimum is faithful, or receive singular-H boundary faces without an actual boundary theorem.
- A common eigenline need not satisfy the paid spectator condition h3<=2a3. The superthreshold spectator case remains a separate question.
- The anchored gap contains an additional varying unfiltered-baseline/filter term, so its stationarity is not equation(2); no anchored reduction is claimed.
- No commutation of the remaining2x2 blocks or general value sign follows merely from this common-eigenline reduction.

## Compact negative-value consequence (not an anchored-gap statement)

The already-received `wh3_physical_two_plus_one_block_entropy_theorem.md` pays X(H,A) when H is singular: the pure main then has physical Schmidt rank at most2 and the isotropic physical reset preserves the physical2+1 block form. The companion `schmidt_rank_two_isotropic_reset_value_theorem.md` supplies the explicit lower bound

 Delta(X(H,A)) >= f(A)+3f(A+H/3)-4f(A+H/4) >=0.

Thus, if any negative X(H,A) exists with qutrit A, fix that actual A and TrH. Minimize its continuous value over the compact set of PSD H with this trace. The minimum remains negative, cannot occur at a singular H, and is stationary in all trace-preserving faithful-H directions. The theorem therefore gives a negative source with a common reducing H/A eigenline. This is a finite actual-source counterexample-preserving reduction; it does not invoke arbitrary-reference attainment or infer the sign of the remaining2x2 block-plus-spectator family.

## Transverse second-order exclusion of a middle spectator

Assume simple A, a faithful H stationary as above, and a nonzero active off-diagonal pair. Relabel/gauge so

 H=[[h1,z,0],[z,h2,0],[0,0,h3]], z>0,
 A=diag(a1,a2,a3).

Put da=a1-a3, db=a2-a3, u=h1-h3, v=h2-h3. Off-diagonal stationarity gives j=-a3 c-n h3, while orientation gives c=-[alpha a3+beta]/h3<0. The diagonal variation increasing h3 and decreasing h1 gives the exact additional identity

 alpha da db+c(da v+db u)+n(uv-z^2)=0.             (3)

To verify it directly, subtract the two diagonal kernel derivatives, put them over det(A+tI), and integrate. Before substitutions the result is

 (a1-a3)(alpha a2+beta+h2 c)
 +(h1-h3)(a2 c+j+h2 n)-z^2 n=0.

Inserting the two preceding identities yields(3).

Now open only the transverse main entries H13=t x,H23=t y and their conjugates. The source is two-sided feasible for small real t since H>0, and its trace is unchanged. At t=0 both E and P have zero first derivative, so there is no missing F Hessian term. The exact t^2 coefficient is (x,y)* B (x,y), where

 B=-[[c db+n v,-n z],[-n z,c da+n u]].

Consequently, using(3),

 det B=(c^2-n alpha) da db.

Here c^2-n alpha>0. If a3 lies strictly between a1 and a2, det B<0, so an actual transverse H variation decreases the value to second order. Such a point cannot be a local minimum. Therefore every noncommuting faithful fixed-A local minimum uses an EXTREME reset eigenvalue as its common spectator. This is only a necessary condition; neither extreme-spectator case is excluded.

The formula states the coefficient of t^2; the real Hessian itself has the conventional additional factor2, which does not change inertia. All singular-reset cases with simple spectrum use the already-received rank(A)=2 integrability. No rank-opening reset variation is involved.
