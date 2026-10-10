# Uniform eventual entanglement breaking in semialgebraic CP mapping cones

9 October 2026. Complete proof candidate. One focused independent adversarial check of the entire proof found no mathematical gap under the stated hypotheses; see WHOLE_CLAIM_REVIEW.md. This is internal checking, not external certification. No priority or historical claim is made. The mechanism is a positive rank-one truncation of Kraus words, followed by squaring the resulting EB approximation to generate its own separable margin.

## Theorem

Let C be a closed convex semialgebraic cone of CP maps M_d(C)->M_d(C), invariant under arbitrary CP pre- and postcomposition. Suppose every map in C has a finite EB power. Then there exists a common integer N=N(C,d) such that Phi^N is EB for every Phi in C.

The premise includes non-TP filtered maps. The exponent is cone-dependent. No explicit dimension-only numerical bound is asserted. The proof does not apply after dropping semialgebraicity, as the preserved counterexample shows.

Throughout, J(Phi)=sum Phi(E_ij) tensor E_ij is unnormalized, tr J(Phi)=d for TP maps, and D_I(X)=tr(X)I has J(D_I)=I tensor I. The EB order E>=_EB F means E-F is EB.

## 1. A Kraus lift near an EB channel

For a CPTP map Psi, let

 g(Psi)=dist_F(J(Psi), {J(E): E is CPTP and EB}).

This is a continuous semialgebraic function: the comparison set is compact and semialgebraic, by the finite separable-product decomposition bound. Choose a nearest EB channel E_0. Its Choi matrix J_0 has a rank-one Kraus decomposition with at most r=d^4 columns; pad with zero columns. Write the matrix of vectorized Kraus columns as W_0, so W_0 W_0*=J_0.

There exists a d^2-by-r coisometry U, UU*=I, with W_0=sqrt(J_0)U. Indeed the polar partial coisometry can be extended on ker J_0 because r>=d^2. Set

 W=sqrt(J(Psi))U.

Its columns give Kraus matrices K_1,...,K_r for Psi. The square-root inequality for positive matrices gives

 ||W-W_0||_F^2=||sqrt(J(Psi))-sqrt(J_0)||_F^2
               <=||J(Psi)-J_0||_1 <=d g(Psi).           (1)

Every original Kraus matrix K_i^0 has rank at most one, so wedge^2 K_i^0=0. Using the tensor-product telescoping bound and Cauchy-Schwarz,

 b:=sum_i ||wedge^2 K_i||_op
 <=sum_i (||K_i||_F+||K_i^0||_F)||K_i-K_i^0||_F
 <=2sqrt(d)||W-W_0||_F
 <=2d sqrt(g(Psi)).                                    (2)

Here sum_i||K_i||_F^2=sum_i||K_i^0||_F^2=d. This is a finite constructive-existence bound; no optimized convex roof is required.

## 2. Rank-one truncation of all Kraus words

For any matrix A, let L be its top-singular-value rank-one truncation. If s_1>=s_2 are the first singular values, then

 || |vec A><vec A|-|vec L><vec L| ||_F
       <=c_d s_1s_2=c_d||wedge^2 A||_op,
 c_d=sqrt(d^2-1).                                     (3)

Proof: with A=L+R and orthogonal vectorizations, the square of the left side is 2s_1^2||R||_F^2+||R||_F^4. Since ||R||_F^2<=(d-1)s_2^2 and s_2<=s_1, this is at most (d^2-1)s_1^2s_2^2.

The nth power Psi^n has Kraus words A_w=K_(i_n)...K_(i_1). Replace each word by its rank-one truncation L_w and let E_n be the resulting CP map. It is EB. Exterior-square submultiplicativity and the triangle inequality give

 delta_n:=||J(Psi^n-E_n)||_F
 <=c_d sum_w ||wedge^2 A_w||_op
 <=c_d (sum_i ||wedge^2 K_i||_op)^n
 <=c_d b^n.                                           (4)

The number of words may be exponential. This is an existence proof, not an efficient algorithm for writing E_n explicitly.

## 3. The EB approximation manufactures a separable margin after one square

Let T be CPTP, E EB, delta=||J(T-E)||_F, and suppose

 T(rho)>=f I for every density matrix rho, f>0.

For delta<=f/2, contraction of the Choi matrix against rho^T gives E(rho)>=(f-delta)I>=fI/2. Also

 ||E*(I)-I||_op<=sqrt(d)delta,

so delta<=1/(2sqrt(d)) gives E*(I)>=I/2. In a Holevo decomposition E(X)=sum_a tr(F_aX)sigma_a with sigma_a density matrices,

 E^2(X)=sum_a tr(F_aX)E(sigma_a)
       >=_EB (f/2)tr[E*(I)X]I
       >=_EB (f/4)D_I.                               (5)

The inequalities are in EB order: their differences have positive measure-and-prepare decompositions.

The HS-induced operator norm of a CPTP map is at most sqrt(d), by trace-norm contraction on Hermitian matrices; the same bound extends to the complexified space. Hence

 ||J(T^2-E^2)||_F
 <=(||T||_(2->2)+||E||_(2->2))delta
 <=(2sqrt(d)+delta)delta.                              (6)

The elementary separable ball ||Z||_F<=1/d^2 around I tensor I absorbs (6) into (5). Since f<=1/d, the single sufficient condition

 delta<=f/kappa_d, kappa_d=4d^2(2sqrt(d)+1)             (7)

implies all the preceding smallness conditions and proves T^2 EB.

This step is indispensable. Small distance to EB alone is insufficient; the actual EB approximation E gains its own positive product margin from the output positivity of T, and that margin is linear in f rather than quadratic.

## 4. Compressed cones and the exact invariant-corner lemma

Fix an isometry V:C^r->C^d and define C_r by requiring Ad_V theta Ad_(V*) in C. This is a closed convex semialgebraic CP mapping cone on M_r. It equals the compression image Ad_(V*) C Ad_V because C is filter invariant. Pointwise eventual EB passes to C_r. Unitary closure identifies the induced cones for different choices of rank-r subspace.

If P is a proper nonzero invariant projection for Phi in C, write Kraus operators as [[A_i,B_i],[0,C_i]]. Then

 T(X)=sum_i A_i X C_i* =0.                             (8)

If not, block-unitary postcomposition can make the trace of its induced cross operator nonzero: products U_P tensor conjugate(U_Q) span the full matrix algebra on Hom(QH,PH). The resulting cross operator has a nonzero eigenvalue, and all its powers remain nonzero. Every EB map with invariant P has zero cross transfer, as is immediate termwise from its positive Holevo decomposition. This would produce a cone member with no EB power, contradicting the premise.

The vanishing in (8) makes the Kraus-index coefficient spaces of A_i and C_i orthogonal. A unitary Kraus-coordinate rotation therefore splits

 Phi=F+G,
 F output-supported on P, G input-supported on Q, GF=0.

The split maps need not belong to C, but the corner maps Phi_P,Phi_Q do belong to the induced cones. Their powers imply that F^(N_p+1),G^(N_q+1) are EB whenever the corresponding corner powers are EB. Since

 Phi^n=sum_(j=0)^n F^(n-j)G^j,

one obtains

 n_EB(Phi)<=N_p+N_q+1.                                (9)

For completeness, with V_P,V_Q the corner isometries, the factor identities are

 F^m=Ad_(V_P) Phi_P^(m-1) Ad_(V_P*) F,
 G^m=G Ad_(V_Q) Phi_Q^(m-1) Ad_(V_Q*).

They follow from F being output-supported on P and G being input-supported on Q. At n=N_p+N_q+1, either n-j>=N_p+1 or j>=N_q+1, making every summand EB. Invariance alone also proves the Holevo assertion above: tr(F_a P)tr(sigma_a Q)=0 termwise, so each positive summand either has input effect supported on Q or output supported on P.

## 5. Induction gives a common exponent on every nonprimitive TP stratum

The theorem is trivial for d=1. Assume it for all smaller induced cones, and put N_*=max_(r<d) N(C_r,r).

Every reducible TP member of C has an EB power of exponent at most 2N_*+1 by (9).

If Phi is irreducible but nonprimitive, finite-dimensional quantum Perron theory gives a period h with 2<=h<=d and orthogonal cyclic projections P_1,...,P_h. Each has dimension below d. More explicitly, apply the cyclic theorem to the irreducible unital adjoint: Phi*(P_j)=P_(j-1), with indices modulo h. For x in P_(j-1)H,

 sum_i ||(I-P_j)K_i x||^2
 = <x, Phi*(I-P_j)x> = 0.

Thus every Kraus operator sends P_(j-1)H into P_jH, and every h-letter Kraus word is block diagonal. For Psi=Phi^h, an input P_i X P_j can therefore output only in P_i M_d P_j. It remains in C, and (8) applied to the invariant P_i annihilates this entire cross-input image when i!=j. Consequently Phi^h is genuinely the direct sum of its compressed maps, each with EB exponent at most N_*. Therefore n_EB(Phi)<=h N_*<=d N_*.

Thus every nonprimitive TP map in C satisfies

 Phi^N0 is EB, N0=max(2N_*+1,d N_*).                   (10)

This is a uniform boundary theorem, obtained by induction; pointwise membership alone would not justify it.

## 6. Semialgebraicity closes the primitive neighborhoods

Let K=C intersect {TP maps}. This is compact and semialgebraic. Choose q=d^4. The quantum Wielandt theorem gives eventual full Kraus rank by this exponent for every primitive CPTP map. Thus

 f(Phi)=lambda_min J(Phi^q)

is continuous, semialgebraic and nonnegative on K, and f(Phi)=0 exactly on its nonprimitive members. By (10),

 f(Phi)=0 implies g(Phi^N0)=0.

The compact semialgebraic Lojasiewicz inequality gives A,alpha>0 with

 2d sqrt(g(Phi^N0))<=A f(Phi)^alpha                    (11)

for all Phi in K. Choose an integer n with N0 n>=q and alpha n>1. Apply Sections 1-2 to Psi=Phi^N0. The resulting EB approximation to T=Phi^(N0 n) has

 delta<=c_d A^n f(Phi)^(alpha n).                      (12)

For f(Phi)>0, Choi domination J(Phi^q)>=f(Phi)I tensor I implies Phi^q(rho)>=f(Phi)I for every density rho. Since N0 n>=q, the final q steps give the same output margin for T. Equations (7) and (12) show that T^2 is EB whenever 0<f(Phi)<=epsilon for a sufficiently small common epsilon>0. The f=0 case already follows from (10).

It remains to cover f(Phi)>=epsilon. On this compact primitive set, the blocks Psi=Phi^q satisfy

 epsilon D_I<=_CP Psi<=_CP d D_I.

The elementary faithful-word bound proved in Appendix B supplies a common m>=2 with Psi^m EB; explicitly it suffices that

 (1-epsilon/d)^m d^6<=epsilon^2.

Taking the maximum of the two exponents 2N0 n and qm works on all of K, because every later power after an EB power remains EB.

## 7. Extend the common TP exponent to the entire cone

A nonzero CP mapping cone contains D_I: sandwich any nonzero member between suitable positive measurement/preparation maps. The zero cone is trivial. Given arbitrary Phi in C, let Phi_epsilon=Phi+epsilon D_I. Its Choi matrix is positive definite. The map X->Phi_epsilon*(X)/tr(Phi_epsilon*(X)) is continuous on the compact convex density-matrix set and takes values in strictly positive matrices. Brouwer's fixed-point theorem gives a strictly positive Y_epsilon with Phi_epsilon*(Y_epsilon)=r_epsilon Y_epsilon and r_epsilon>0. Identifying r_epsilon with the spectral radius is not needed. The similarity

 Theta_epsilon=r_epsilon^(-1) Ad_(Y_epsilon^(1/2))
                         Phi_epsilon Ad_(Y_epsilon^(-1/2))

is TP and remains in C. If N is the common exponent from Section 6, Theta_epsilon^N is EB. The filters telescope through powers, so Phi_epsilon^N is EB too. Let epsilon decrease to zero and use the closedness of the EB cone. Then Phi^N is EB, with the same N for every member of C. QED.

## Dependencies, reproducibility and limits

- Quantum Wielandt: Sanz, Perez-Garcia, Wolf and Cirac, arXiv:0909.5347v2, Theorem 1 and Proposition 3 (with eventual full-span persistence as stated in the definition of i(A)). The full-Kraus-span exponent i(A), not only minimum-output positivity, is used in Section 6. Its bound is <=(d^2-r+1)d^2<=d^4, where r is Kraus rank. Primary source: https://arxiv.org/pdf/0909.5347 .
- Cyclic decomposition: Carbone and Jencova, arXiv:1905.00857, Definition 1, Proposition 5 and Corollary 2, pp. 9-10, applied to the unital adjoint. Primary source: https://arxiv.org/pdf/1905.00857 .
- Conic Caratheodory, the Powers-Stormer positive square-root trace inequality, Brouwer's fixed-point theorem and the compact semialgebraic Lojasiewicz inequality are used explicitly.
- Appendix B gives the complete faithful-word positive expansion used here; it does not require an external lemma.
- One focused independent check of the whole proof is recorded in WHOLE_CLAIM_REVIEW.md. Bounded numerical checks test the Kraus lift, word estimates and margin inequalities; they do not establish a universally quantified theorem.
- All exponents and constants may depend on the semialgebraic cone. The proof does not yield N=2, a universal polynomial in d, or a computationally efficient Kraus-word expansion.
- PPT application requires the pointwise premise. A separate established-input closure is recorded in PPT_POINTWISE_DEPENDENCY_CLOSURE.md; it is not silently assumed from a unital-only theorem.


## Corollary for all PPT maps in fixed dimension

For each positive integer d there exists a finite integer N(d) such that every CP and completely copositive map Phi:M_d->M_d satisfies Phi^N(d) in EB. The statement includes non-TP maps.

The PPT cone is closed, convex and semialgebraic: J(Phi)>=0 and J(Phi)^Gamma>=0 are finite polynomial matrix inequalities in the real and imaginary entries. It is invariant under arbitrary CP filters. Its pointwise eventual-EB premise follows from Hanson, Rouze and Stilck Franca (2020), Theorem 3.14, plus the following dimension induction (the same general pointwise conclusion is Park (2026), Theorem 1.1, and is credited as prior):

If the spectral radius is zero, Cayley-Hamilton gives Phi^(d^2)=0. If Phi is irreducible, positive-map Perron theory gives positive-definite left and right eigenmatrices and the published faithful theorem applies. Otherwise choose a proper invariant P. For p in PH,q in QH, q tensor conjugate(p) has zero quadratic form against J(Phi)^Gamma>=0, hence lies in its kernel. Matrix entries of this kernel identity force sum A_i X C_i*=0. Section 4 gives a CP split with GF=0, while the two smaller compressed maps remain PPT. Induction and the bound N_P+N_Q+1 finish the pointwise argument. No family-uniform exponent is assumed at this stage.

Applying the main theorem now supplies N(d). The proof does not give N(d)=2, an exponent independent of d, or a useful numerical estimate. It addresses equal-map iteration; it does not assert that every arbitrary nonstationary word of length N(d) in PPT maps is EB.

## Appendix A Elementary separable ball

Choose a real HS-orthonormal Hermitian basis H_1,...,H_(d^2) of M_d. Each satisfies ||H_a||_op<=1. Expand a Hermitian Z=sum z_ab H_a tensor H_b. The real coefficients obey sum|z_ab|<=d^2||Z||_F. Moreover

 I tensor I + H_a tensor H_b
 =[(I+H_a) tensor (I+H_b)+(I-H_a) tensor (I-H_b)]/2,

and the minus sign follows by replacing H_b by -H_b. These are sums of positive product operators. When sum|z_ab|<=1, I tensor I+Z is a convex combination of these separable operators and I tensor I. This proves the radius 1/d^2 used in Section 3.

## Appendix B Faithful-word bound

Suppose alpha D_I<=_CP Psi<=_CP beta D_I with 0<alpha<=beta. Put R=Psi-alpha D_I and z=1-alpha/beta, so 0<=_CP R<=_CP z Psi. For n>=2, arbitrary CP C_1,...,C_(n-1), let

 T_n=Psi C_(n-1) Psi ... C_1 Psi,
 R_n=R C_(n-1) R ... C_1 R.

Replacing factors in CP order gives R_n<=_CP z^n T_n. Expanding Psi=R+alpha D_I at every location, F_n=T_n-R_n is EB. Write T_n=Psi L Psi and w=tr L(I). Then T_n<=_CP beta^2 w D_I. The whole collection of expansion terms with alpha D_I at the leftmost position is alpha D_I L Psi. Its difference from alpha^2 w D_I is alpha D_I L R, which is EB. The remaining terms in F_n are EB as well. Hence F_n>=_EB alpha^2 w D_I.

Meanwhile ||J(R_n)||_F<=tr J(R_n)<=z^n beta^2 w d^2. Appendix A absorbs this remainder into the positive product term whenever

 z^n beta^2 d^4<=alpha^2.

If w=0 the word is zero. If alpha=beta every word is already EB. For Section 6, take alpha=epsilon,beta=d, all C_i=id, giving its displayed d^6 condition.
