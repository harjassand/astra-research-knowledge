# A covariance certificate for the three-input, three-output evaluator

This is an independently inspectable construction using the accepted free
representation in `FINITE_REFERENCE_PROOF.md`. It makes no historical priority
claim. All positivity statements below include complex Hermitian effects and
arbitrary finite dimension. The executable certificate verifier uses exact
rational arithmetic; the SDP solver only discovers a candidate.

## 1. Closure and notation

Let B have rows (1,0), (0,1), (-1,-1). Write the free vector as
u=(u1,u2,-u1-u2), and let A_K(Q) be its two-by-two operator form matrix, so
F_K=u_free* A_K(Q) u_free. Because all channel entries are positive,
min_i K_yi I <= W_y <= max_i K_yi I even on the closed POVM domain.
For L of full input rank, A_L(Q) has a uniform positive lower bound: it
dominates B^T L^T diag(1/max_i L_yi) L B tensor I, which is positive definite.
Consequently all free quotients extend continuously to the closed POVM
domain after normalizing the two free vectors to unit squared norm.
Every boundary witness is approximated by (1-epsilon)Qi+epsilon I/3.
Thus closure does not change the supremum or any bound below.

Initially assume K also has full input rank. Put V_K(Q)=A_K(Q)^-1.
For c>0, the desired inequality A_K<=c A_L is equivalent by inverse
order to c V_K-V_L>=0. The c=0 case is exactly the constant K channel.

## 2. A channel-independent Jensen gap

Let R_K be the first two rows of K B; its determinant is nonzero. Let
w=(W_1,W_2)^T. The third output vector is minus the first two, and
W_1+W_2+W_3=I. Woodbury elimination, valid without commutativity, gives

    V_K(Q) = R_K^-1 [diag(W_1,W_2)-w w*] R_K^-T.             (1)

For example, the inverse of the bracket is the block matrix with diagonal
W_1^-1,W_2^-1 plus the all-ones block tensor W_3^-1; multiplying the two
matrices verifies (1) directly. Constant two-by-two matrices commute only
with the operator tensor factor, which is the only commutation used.

Let e1=(1,0)^T, e2=(0,1)^T, e3=0, q=(Q1,Q2)^T, and let V_Ki be
V_K evaluated at scalar vertex Qi=1, Qj=0 for j!=i. Then

    V_K(Q) = sum_i V_Ki tensor Qi + Gamma(Q),
    Gamma(Q)=diag(Q1,Q2)-q q*.                            (2)

To check this identity, let k_i be the first two entries of channel column
i. We have k_i=R_K e_i+k_3. In the difference between the expression in
(1) and its affine vertex interpolation, the constant k_3 and both cross
terms cancel using sum Qi=I. The remaining expression is precisely Gamma.
This proves that the same Gamma occurs for every full-rank channel.

Gamma is PSD. More generally the three-by-three block matrix

    C(Q) = diag(Q1,Q2,Q3)-[Qi Qj]_{i,j=1}^3               (3)

is PSD: put r=[sqrt(Q1),sqrt(Q2),sqrt(Q3)], so rr*=I. Then C is
diag(sqrt(Qi)) (I-r*r) diag(sqrt(Qi)); the middle factor is an orthogonal
projection. Gamma is the principal two-by-two block of C.

## 3. The explicit upper certificate

For a rational c>=0, define the rational symmetric matrices

    Pi=c V_Ki-V_Li,      i=1,2,3.

Set E=[I2;I2;I2], s=(1,0,0,1,0,0)^T, S=ss^T, and

    T = [ I2   0
           0  I2
         -I2 -I2 ].

The columns of T span ker(E*). A certificate consists of a symmetric
rational six-by-six matrix A satisfying

    A >= 0,
    Aii = Pi  for its three diagonal two-by-two blocks,
    T^T [A+(c-1) S] T >= 0.                              (4)

Every condition in (4) is checked exactly by rational LDL elimination.
There is no numerical tolerance in the final acceptance decision.

To prove sufficiency, choose any complex vectors z1,z2 in the effect
space and let V have those two columns. Define Xi=V*Qi V and the block
matrix Y with Yij=V*Qi Qj V. Let D=diag(X1,X2,X3), H=D-Y. Then

    Y>=0, H>=0, HE=0.

The first inequality is the Gram positivity of Qi V; the second follows
from (3); the equality uses sum Qi=I. From (2),

 z* (c V_K(Q)-V_L(Q)) z
     = sum_i Tr(Pi Xi)+(c-1) s* H s
     = Tr(A Y)+Tr([A+(c-1)S] H) >=0.                    (5)

Indeed H is supported in ker(E*) and hence has the form T J T* with
J>=0; its second trace is nonnegative by (4). The vector z was arbitrary,
so (5) proves the operator inequality, then the free quotient inequality,
and finally the conditional-Umegaki inequality via the accepted free
representation. Complex entries cause no exception to the trace argument.

When c>=1, one may simply use A=diag(P1,P2,P3), provided Pi>=0.
Therefore if the maximum of the three scalar vertex coefficients is at
least one, it is exactly the global coefficient. A rational c>=1 only
requires checking c A_L(ei)-A_K(ei)>=0 at the three vertices. These are
two-by-two rational PSD checks. They imply Pi>=0 by inverse order.

This last sufficient condition also covers singular K. Approximate K by
K_epsilon=(1-epsilon)K+epsilon L. Apart from finitely many epsilon values,
K_epsilon is invertible; its determinant polynomial is nonzero at 1.
The three vertex coefficients converge continuously. For every delta>0,
the preceding full-rank result applies with c+delta for sufficiently small
epsilon. The output inverse forms converge uniformly because entries of
K remain strictly positive. Passing epsilon to zero and then delta to zero
proves the claimed bound for singular K as well.

## 4. The SDP is exact for full-rank K, not just a sufficient hierarchy

For completeness, the moment conditions above are also sufficient for
degree-two realizability. Suppose Xi are two-by-two PSD, D=diag(Xi), and
0<=Y<=D with (D-Y)E=0. Factor D=A0* A0, where A0 is block diagonal and
surjective onto H=direct_sum_i ran(Xi). Set V=A0 E. There exists a
positive contraction R on H with A0* R A0=Y, obtained by the pseudoinverse
of D^(1/2). The row-sum equality gives

    A0*(I-R)V = (D-Y)E=0.

Since A0 is surjective, its adjoint is injective, so RV=V. Dilate R to
the projection

    P = [ R                  sqrt(R(I-R))
          sqrt(R(I-R))       I-R              ]

on H direct_sum H. It fixes (V,0). Let Ei be the coordinate projections
on the first H summand, extended in any partition of the second summand.
Define Qi=P Ei P restricted to ran(P), and use vectors (V,0). Then
sum Qi=I, V*Qi V=Xi, and V*QiQj V=Yij. This verifies all moments exactly.
No commuting replacement or assumed optimizer is used. Real moment data
produce real effects; real parts of complex feasible moments are real
feasible moments with the same objective.

It follows that the coefficient is exactly the finite SDP-fractional
optimum max beta/alpha, where

    alpha=sum_i Tr(V_Ki Xi)+s*(D-Y)s,
    beta =sum_i Tr(V_Li Xi)+s*(D-Y)s,
    0<=Y<=D,  (D-Y)E=0, Tr(sum Xi)=1.                  (6)

Both alpha and beta are uniformly positive on this compact feasible set.
Homogeneity allows imposing alpha=1 instead. Ordinary SDP duality yields
(4). One can also see dual exactness directly: parameterize H=T J T*;
the feasible set has a strictly feasible point Xi=a I2 and J=b I4 for
sufficiently small positive b/a, and normalize alpha to one. A dual optimum
exists by this strict feasibility, while full-rank vertex matrices bound
the objective. Thus (4), optimized over c, has no gap from the global free
coefficient. This construction supplies a general, fixed-size certificate
mechanism for the square three-output full-rank case, rather than a claim
that a global optimizer is available.

## 5. Implemented scope and remaining numerical work

`covariance_certificate.py` implements the expansive vertex shortcut and
the fixed-size SDP with rational reconstruction, exact checking, and no
hardcoded instance bounds. Every supplied development case has passed.
For singular nonconstant K it currently uses the always-valid expansive
bound (which can be loose when the true coefficient is below one); the
exact inverse SDP implementation requires nonsingular K. The general
evaluator still returns a rigorous upper bound in that case. Tightening
that exceptional branch is a separate implementation issue, not a missing
proof of any reported bound.

The accepted active/vacuum lift supplies equal-marginal Umegaki witnesses
from any free lower witness. The certificate by itself is an upper bound;
it does not turn a numerical search value into a certified lower witness.
