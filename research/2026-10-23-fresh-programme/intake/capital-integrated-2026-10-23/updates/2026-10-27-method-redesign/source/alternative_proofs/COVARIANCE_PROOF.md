# A covariance evaluator for square three-input channels

This is an ordinary mathematical construction, using the accepted free formula. It does not claim historical priority. All matrices below may act on arbitrary finite complex Hilbert spaces.

Put B=[[1,0],[0,1],[-1,-1]]. The free form is the positive quadratic form

A_M(Q)=sum_y (M_y B)^T(M_y B) tensor (sum_i M_yi Q_i)^(-1)

on the coordinate vector u=(u_1,u_2), with u_3=-u_1-u_2. For scalar vertices e_i define the rational 2-by-2 matrices A_Mi=A_M(e_i). Their entries are well defined because every channel entry is positive. If M is invertible on zero-sum vectors, all these forms are positive definite.

## 1. Exact inverse identity

For a channel M invertible on the zero-sum subspace, let R_M be the first two rows of MB. It is invertible. Write W_y=sum_i M_yi Q_i, so sum_y W_y=I. In output zero-sum coordinates the form has matrix

D=diag(W_1^(-1),W_2^(-1))+[I;I]W_3^(-1)[I,I].

The Woodbury identity (valid without commuting any W's) gives

D^(-1)=diag(W_1,W_2)-[W_1;W_2][W_1,W_2].

Consequently A_M(Q)^(-1)=(R_M^(-1) tensor I)D^(-1)(R_M^(-T) tensor I).

Define the input covariance block matrix

G(Q)=diag(Q_1,Q_2)-[Q_1;Q_2][Q_1,Q_2].

It is positive semidefinite: map v to (Q_1^(1/2)v,Q_2^(1/2)v,Q_3^(1/2)v), an isometry, and compress the orthogonal projection onto its complement. Equivalently its quadratic form is the operator-valued variance of (t_1,t_2,0).

Since R_M^(-1)[W_1;W_2]=[Q_1;Q_2]+R_M^(-1)M_{first two rows,3} tensor I, expanding the preceding inverse identity shows its quadratic term is exactly -[Q_1;Q_2][Q_1,Q_2], independent of M. The remaining terms are affine in Q. Evaluate that affine part at the three scalar vertices, where G(e_i)=0, to obtain the exact polynomial identity

(**) A_M(Q)^(-1)=G(Q)+sum_i A_Mi^(-1) tensor Q_i.

No Q_i inverse is used; this remains valid at PSD boundaries.

## 2. Exact expansive regime, including singular K

For invertible K,L, inverse-order reversal gives

A_K(Q)<=c A_L(Q) iff c A_K(Q)^(-1)-A_L(Q)^(-1)>=0.

By (**), the matrix on the right is

(c-1)G(Q)+sum_i [c A_Ki^(-1)-A_Li^(-1)] tensor Q_i.             (1)

Thus for c>=1 it is positive at every Q if it is positive at the three scalar vertices. The converse is immediate by evaluating vertices (or their faithful approximations). Equivalently, check the three rational 2-by-2 matrices c A_Li-A_Ki>=0.

Let C_vertex=max_i lambda_max(A_Ki,A_Li). Then

C_vertex <= C_complete <= max(1,C_vertex),

and if C_vertex>=1, C_complete=C_vertex. This certifies arbitrary noncommuting Q and all reference sizes through the supplied free formula.

This conclusion also holds for singular K. Take K_epsilon=(1-epsilon)K+epsilon L. Its determinant on the two-dimensional tangent subspace is a polynomial in epsilon, nonzero at epsilon=1, so there are arbitrarily small positive epsilon for which it is invertible. The three vertex forms and all fixed-Q forms vary continuously because the output inverses have a uniform positive lower bound. Apply the invertible theorem at c_epsilon=max(1,C_vertex(K_epsilon,L)), let epsilon decrease to zero outside the finitely many singular values, and pass to the limit for each fixed Q. The result is exactly the stated universal bound. No numerical inversion of singular K is needed.

## 3. A small global certificate below one

Suppose K is also invertible and 0<=c<1. Set tau=1-c, H_Ki=A_Ki^(-1), H_Li=A_Li^(-1), S_i=c H_Ki-H_Li. Let e_1=(1,0),e_2=(0,1),e_3=(0,0).

A certificate consists of one real vector z=(z_1,z_2) such that the three rational matrices

M_i=S_i-tau(e_i-z)(e_i-z)^T >=0.                            (2)

Indeed, (1) has the exact sum-of-squares decomposition

sum_i M_i tensor Q_i + tau ([Q_1;Q_2]-[z_1 I;z_2 I])([Q_1,Q_2]-[z_1 I,z_2 I]).   (3)

Every term is PSD for every complex POVM Q. The certificate therefore consists of c,z and six diagonal minors plus three determinants, all checkable by rational arithmetic. Feasibility search does not certify itself: the evaluator accepts only candidates passing these exact checks.

## 4. Why this small certificate is complete in the contraction regime

This paragraph is a self-contained semidefinite-duality derivation; evaluator safety does not require assuming its conclusion, because every returned upper bound has (1) or (3).

For any vector t=(t_1,t_2), put x=Q_1t_1+Q_2t_2 and let P project onto span{t_1,t_2}. The form of (1) is a term linear in Q plus tau||x||^2. Compressing Q to that span preserves the linear term and replaces ||x||^2 by ||Px||^2, which cannot increase it. Therefore every violation has dimension at most two.

Normalize ||t_1||^2+||t_2||^2=1. Write Z_i=[<t_a,Q_i t_b>]_(a,b=1,2), T=sum_i Z_i, and w=sum_i Z_i e_i. Then Z_i>=0, tr(T)=1 and ||x||^2>=w^* T^+ w, with equality after compression. Conversely any such Z_i are realized on supp(T) by t_a=T^(1/2)e_a and Q_i=T^(-1/2) Z_i T^(-1/2), with generalized inverses on the support. Thus the exact minimum of the quadratic form (1), over all dimensions and normalized t, is the convex SDP

min sum_i tr[(S_i-tau e_i e_i^T)Z_i]+tau s
subject to Z_i>=0, tr(sum_i Z_i)=1, [[T,w],[w^*,s]]>=0.

Strict feasibility holds by taking Z_i=I/6 and s large. Expressing the Schur-complement term as

w^* T^+ w=sup_z {2 Re(z^*w)-z^*Tz}

and using standard finite-dimensional SDP strong duality yields the dual value

max_z min_i lambda_min[S_i-tau(e_i-z)(e_i-z)^*].

The maximum is attained: the displayed minimum tends to minus infinity as ||z|| tends to infinity. Complex z cannot improve it, because taking real parts and then dropping tau Im(z)Im(z)^T gives the same or larger lower eigenvalue for the real center Re(z). Hence the universal inequality holds exactly iff a real center satisfying (2) exists. This also proves that real dimension at most two suffices for the coefficient when it is below one. The complex domain has not been discarded.

A dual certificate near the optimum supplies a witness constructively. If r_i spans the kernel of M_i, choose nonnegative weights alpha_i solving sum_i alpha_i r_i r_i^T(e_i-z)=0, sum alpha_i||r_i||^2=1. Set Z_i=alpha_i r_i r_i^T, T=sum Z_i and use the preceding realization. Numerical kernel recovery can be ill conditioned at scalar optima; the implementation keeps this as a witness-acquisition heuristic and checks every final rationalized witness directly.

## 5. Lower bounds and closure

A rational scalar vertex and rational coordinate u give an exact rational Rayleigh quotient. Every boundary vertex is approached by Q_i(eta)=(1-eta)delta_ij+eta/3, all strictly positive; every output remains uniformly positive and the quotient is continuous. Therefore the boundary quotient is already a rigorous lower bound for the supremum. The implementation additionally produces faithful rational witnesses when convenient.

For numerical dimension-two witnesses, round Q_1,Q_2 symmetrically, set Q_3=I-Q_1-Q_2, mix a rational amount of I/3 into every Q_i, and check all principal minors exactly. Round u_1,u_2 and set u_3=-u_1-u_2. The exact inverse quadratic evaluations give the recorded rational lower bound. Rounding or optimization is never used as evidence for the upper bound.

These operations solve the supplied four asymmetric development instances through Section 2. Their values exceed one. Section 3 independently certifies the noncommuting quantum-reference control below one. This is a result at this square finite classical-channel interface; it does not assert a comparable identity for rectangular channels, coherent quantum input channels, other metrics, or a practical advantage over an unmeasured comparator.
