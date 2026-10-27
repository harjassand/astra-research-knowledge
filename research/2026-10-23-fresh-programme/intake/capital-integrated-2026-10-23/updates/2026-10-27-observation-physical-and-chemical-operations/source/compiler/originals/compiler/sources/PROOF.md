Completion version: the frozen source remains byte-for-byte in selected/PROOF_ORIGINAL.md. This version makes the Schur argument, M_K definition and dual sign convention explicit after the two independent audits. No mathematical identity, scientific implementation or accepted certificate changed.

# A three-LMI global evaluator for positive 3 by 3 classical channels

26 October 2026. This is a self-contained construction using the accepted free representation, ordinary Schur complements, matrix covariance, and SDP duality. No historical priority claim is made. Numerical optimization proposes certificates; rational verification establishes each reported bound.

Let K,L be strictly positive column-stochastic 3 by 3 matrices and L invertible on the zero-sum subspace. They need not have equal output distributions and K need not be invertible. Set

- B = [[1,0],[0,1],[-1,-1]], P = [[1,0,0],[0,1,0]].
- R = P L^{-1}; r_y is its y-th column.
- M_i = sum_y L[y,i] r_y r_y^T.
- e_1=(1,0)^T, e_2=(0,1)^T, e_3=0.
- H_i^L = M_i - e_i e_i^T.
- D = P K B, x_i=P K[:,i].
- T_i=diag(x_i)-x_i x_i^T and S_i=D H_i^L D^T.

All of these are real rational matrices. The T_i are positive definite. The H_i^L are positive definite, and the S_i are positive semidefinite. Let

    r = max_i lambda_max(S_i,T_i).

This r is exactly the maximum of F_K/F_L over the three scalar deterministic input effects Q_j=delta_ij. Thus it is a lower bound using the closure of the free domain.

## The executable certificates

For c>=1, the following three 2 by 2 rational tests suffice and are necessary:

    c T_i - S_i >= 0, i=1,2,3.                         (A)

If r>=1, the desired all-quantum-reference coefficient is therefore exactly r.

For 0<=c<1, put t=1-c. A global upper certificate consists of z in R^2 for which

    B_i(c,z) = c T_i-S_i-t(z-x_i)(z-x_i)^T >=0         (B)

for i=1,2,3. Only the three 2 by 2 principal-minor tests must be rationally verified. These certificates are also complete: if the all-reference inequality holds at such a c, some real z exists.

For numerical proposal, set a=t z. Then (B) is equivalent to three 3 by 3 LMIs,

    [[c diag(x_i)-S_i-x_i x_i^T+a x_i^T+x_i a^T, a],
     [a^T,                                               1-c]] >=0.   (C)

Minimizing c in 0<=c<=1 over these three LMIs is a small convex SDP. At c=1 one uses a=0 and (A). An ordinary numerical SDP/SLSQP proposal is not itself trusted: the code rounds z to a rational vector, raises c slightly, and checks (B) exactly. If that check fails, it retains a proved broader bound.

## Why this certifies arbitrary complex, noncommuting effects

For any Q_i>=0 with sum Q_i=I, write q=(Q_1,Q_2)^T, W_y^A=sum_i A[y,i]Q_i and w_A=(W_1^A,W_2^A)^T. On the zero-sum tangent coordinates, define

    J_A = B^T A^T diag((W_y^A)^{-1}) A B.

This is the operator whose quadratic form is F_A. Since L is injective on zero-sum inputs and its output weights are positive, J_L is positive definite uniformly on the compact effect domain.

For positive W_1,W_2,W_3 summing to identity, direct block multiplication gives

    [[W_1^{-1}+W_3^{-1}, W_3^{-1}],
     [W_3^{-1}, W_2^{-1}+W_3^{-1}]]^{-1}
       = diag(W_1,W_2)-(W_1,W_2)^T(W_1,W_2).           (1)

No two W's are assumed to commute. Applying (1) to L and changing its zero-sum coordinates gives

    H_L := J_L^{-1} = sum_i M_i tensor Q_i - q q^*.    (2)

One can check (2) without any inverse of K: R L=P, R maps the output covariance diag(W)-WW^* to the input covariance, and constant shifts of a row of R cancel from that covariance. Equivalently, let D_L=P L B and b=P L[:,3]. Then R=D_L^{-1}(P-b 1^T), and substituting this identity into the right side of (2) gives D_L^{-1}[diag(W_1^L,W_2^L)-w_L w_L^*]D_L^{-T} exactly.

Let M_K=B^T diag((W_y^K)^(-1)) B be the positive output-coordinate K pencil before the inversion in (1). Thus J_K=D^T M_K D. Small scalar matrices act as their tensor product with the reference identity. Put Z=M_K^(1/2) D J_L^(-1/2). Then J_L^(-1/2) J_K J_L^(-1/2)=Z^*Z and ZZ^*=M_K^(1/2) D H_L D^T M_K^(1/2). The norms of Z and Z^* coincide, so for c>=0,

    J_K <= c J_L
      iff Z^*Z <= c I
      iff ZZ^* <= c I
      iff D H_L D^T <= c M_K^{-1}.                  (3)

This argument holds even when D is singular and at c=0. It uses no inverse of K. It is the precise Schur-complement contraction test, rather than a generic claim about singular values of CA and AC.

Let X=sum_i x_i tensor Q_i, a two-block operator column. Its matrix covariance

    V(Q)=sum_i x_i x_i^T tensor Q_i - X X^*

is positive semidefinite: it equals

    sum_i (x_i tensor I-X) Q_i (x_i^T tensor I-X^*).

Using x_i=D e_i+x_3, expand (2) and (3). The exact resulting polynomial is

    c M_K^{-1}-D H_L D^T
      = sum_i (c T_i-S_i) tensor Q_i + (c-1)V(Q).    (4)

For c>=1, (A) makes every term on the right positive. Necessity follows by taking Q_i=I, Q_j=0 for j!=i. This proves the claimed r>=1 endpoint, including singular K.

For c<1, expand the covariance in (4) and complete the square around any scalar vector z:

    c M_K^{-1}-D H_L D^T
      = t (X-z tensor I)(X-z tensor I)^*
          + sum_i B_i(c,z) tensor Q_i.              (5)

Equation (5) proves sufficiency of the rational certificate (B) in every complex reference dimension. It does not impose commutation or replace the quantum problem by a scalar calculation.

## Completeness of the subunit SDP and a two-dimensional witness

Fix 0<=c<1 and let A_i=c T_i-S_i-t x_i x_i^T. To minimize the Rayleigh quotient of the left side of (5), take an arbitrary two-component vector w=(w_1,w_2) with sum ||w_a||^2=1. Let U have columns w_a, G=U^*U, and E_i=U^*Q_i U. Then E_i>=0, sum_i E_i=G and Tr G=1. Put d=sum_i E_i x_i. Projection onto the span of the columns of U gives

    ||X^*w||^2 >= d^* G^+ d.

Equality is attained on a Hilbert space of dimension rank G<=2 by U=G^{1/2} and Q_i=G^{-1/2} E_i G^{-1/2}, with inverses restricted to the support. Consequently the exact universal minimum is the small convex optimization

    min sum_i Tr(A_i E_i)+t s,
    E_i>=0, sum_i Tr(E_i)=1,
    [[G,d],[d^*,s]]>=0,
    G=sum_i E_i, d=sum_i E_i x_i.                   (6)

The objective and constraints are conjugation invariant. Averaging a complex feasible tuple with its conjugate gives a real feasible tuple with the same objective. Thus real symmetric E_i suffice. Taking E_i=I/6 and s strictly large gives Slater feasibility. The objective is bounded below because the E_i are compact and s>=0. Standard finite-dimensional SDP duality applies with dual attainment.

The dual of (6) is

    max mu subject to B_i(c,z)>=mu I for i=1,2,3.     (7)

For completeness, let the PSD multiplier of the 3 by 3 block in (6) be Y=[[Z,b],[b^T,t]]. The remaining dual constraints are A_i-mu I-Z-(b x_i^T+x_i b^T)>=0. The strongest choice is Z=bb^T/t by the Schur complement, since a larger Z only weakens those constraints. Writing b=-t z gives exactly B_i(c,z)>=mu I and hence (7). This fixes the off-diagonal sign convention explicitly. Hence universal positivity is equivalent to existence of z with all B_i>=0. This proves necessity of (B) and the exactness of the three-LMI formulation. It also shows that real effects of active dimension at most two suffice for a subunit extremal witness. A rank-deficient optimum is handled by closure; no assumption of a faithful optimizer is made.

This is an exact reduction, not an assertion that the numerical optimizer has found a global solution. Every executed upper bound comes with the explicit rational SOS (5), and every executed lower bound is independently rationally evaluated.

## Rational lower witnesses and closure

The saved witness uses rational PSD matrices E_i with G=sum E_i>0 and rational vectors h_i with sum h_i=0. It denotes

    Q_i=G^{-1/2} E_i G^{-1/2}, u_i=G^{-1/2}h_i.

Although the square root need not be rational, its quotient is exactly rational:

    F_A = sum_y h_y^T E_y^{-1} h_y,
    E_y=sum_i A[y,i]E_i, h_y=sum_i A[y,i]h_i.       (8)

The verifier checks positivity of E_i and G and evaluates (8) exactly. The implementation normally makes every E_i strictly positive by a small rational regularizer. Scalar vertex witnesses use E_i=1 for one i and zero otherwise. They lie in the allowed closure. Replacing them by (1-epsilon)E_i+epsilon I/3 gives faithful effects, and all W_y remain bounded below by min_i A[y,i]I. Therefore F_A and the quotient are continuous, and the boundary witness gives a valid supremum lower bound. L's full zero-sum rank prevents a zero denominator.

The accepted finite free representation then identifies these bounds with the conditional-Umegaki comparison coefficient with arbitrary finite quantum side information. Its active/vacuum construction converts any faithful free witness into equal-marginal quantum states when needed; this evaluator does not claim practical physical state preparation.

## Scope and antecedents

N965/N970's equality and binary claims are accepted priors. The finite-reference formula and its supplied refinement are used at their stated scope. This derivation supplies an efficient global certificate at the frozen 3 by 3 interface. Its operations are conventional matrix inverses, covariance factorizations, the Schur complement, and small SDP duality. No outside literature search has established historical originality. It makes no claim about generic coherent quantum-input channels, physical measurements, or the larger scientific mission.
