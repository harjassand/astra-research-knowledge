# Exact lower-dimensional reductions at channel boundary strata

9 October 2026. These are exact boundary reductions for the proposed mapping-cone uniformization route. They do not provide a quantitative neighborhood theorem. The CP support splitting and corner-index recursion have overlapping PPT-specific prior in Park, arXiv:2608.13551, Section 3; the filtering argument below states its broader conditional hypothesis explicitly.

Let C be a closed convex CP mapping cone on M_d. Assume every map in C has finite EB index. Assume uniform exponents N_r have already been established for its compressed cones on M_r, r<d. Compression into a fixed r-dimensional subspace defines such a cone; arbitrary CP filters and unitary invariance ensure that the choice of that subspace does not change the available exponent.

## 1. Exact pure-output maps have no input coherence incident to that ray

Suppose a TP map Phi in C sends a pure state |psi><psi| to |phi><phi|. Postcompose by a unitary and choose coordinates so that the resulting map fixes E_00. Kraus operators then have form

 K_i=[[a_i,b_i],[0,C_i]],

where b_i is a row and C_i acts on the orthogonal complement Q. Trace preservation gives sum conjugate(a_i)b_i=0, so

 Phi(|0><v|)=|0><Zv|,  Z=sum conjugate(a_i) C_i.

If Z is nonzero, a block-unitary postcomposition can replace Z by a nonzero positive matrix (use a full unitary polar factor). It therefore has a nonzero eigenvalue lambda and an eigenvector v. For the postcomposed map F,

 F^n(E_00)=E_00,
 F^n(|0><v|)=lambda^n |0><v|.

The Choi partial transpose has a 2-by-2 principal minor with one zero diagonal entry and off-diagonal lambda^n, hence is not positive for any n. Since F remains in C, this contradicts the premise. Therefore Z=0. Undoing coordinates shows that all |psi><v| and |v><psi|, v orthogonal to psi, are annihilated.

Thus

 Phi=R+L,
 R(X)=<psi|X|psi> |phi><phi|,
 L=Phi compose Ad_Q.

R is EB and L is CP. Every word in (R+L)^n containing R is EB. The only remaining term L^n factors through n-1 powers of the compressed CP map Theta=Ad_Q compose Phi compose Ad_Q on M_(d-1). Theta belongs to the compressed cone. Therefore

 n_EB(Phi)<=N_(d-1)+1.                              (1)

This exact argument has no rotating-subspace loss. It does not assert that Phi itself is EB when d>2.

## 2. Proper invariant corners have no persistent cross-corner transport

Suppose P is a nonzero proper invariant projection for an arbitrary CP map Phi in C: Phi(P M_d P) is contained in P M_d P. Put Q=I-P, p=rank P and q=rank Q. Kraus operators have block form

 K_i=[[A_i,B_i],[0,C_i]].

The cross-corner transport is the linear map

 T(X)=sum_i A_i X C_i*  on Hom(QH,PH).

If T is nonzero, there exist unitaries U_P,U_Q such that the operator (U_P tensor conjugate(U_Q))T has nonzero trace. Indeed, products U_P tensor conjugate(U_Q) span the full matrix algebra on Hom(QH,PH), and the trace pairing is nondegenerate. This postfiltered cross operator consequently has a nonzero eigenvalue.

Postcompose Phi by Ad_(U_P direct_sum U_Q). The projection P remains invariant. The cross-corner operator of every nth power is exactly the nth power of the displayed cross operator, so it never vanishes.

An EB map with invariant P must have zero cross-corner transport. To see this, write it as a sum X->Tr(F_j X)R_j with F_j,R_j positive. Invariance implies Tr(F_j P)Tr(R_j Q)=0 termwise. Positivity then forces each term either to have F_j supported on Q or R_j supported on P; either way its cross transport is zero. The postfiltered map would therefore have no EB power, contradicting the premise. Hence T=0.

## 3. CP splitting and the corner index bound

The identity T=0 says that the coefficient vectors of the A_i matrices are orthogonal, in Kraus-index space, to those of the C_i matrices. A unitary change of Kraus coordinates splits the Kraus operators into two groups: the first has C_i=0 and is output-supported on P; the second has A_i=0 and is input-supported on Q. Any remaining operators have both A_i=C_i=0 and may be assigned to either group.

Let the associated CP maps be F and G. Then

 Phi=F+G,  F=Ad_P compose F,  G=G compose Ad_Q,  G compose F=0.

F and G are not claimed to belong to C. The two corner maps

 Phi_P=Ad_P compose Phi compose Ad_P,
 Phi_Q=Ad_Q compose Phi compose Ad_Q

(with their smaller-domain identifications) do belong to the corresponding compressed cones.

Their powers control those of the split maps:

 F^m=Ad_(V_P) compose Phi_P^(m-1) compose Ad_(V_P*) compose F,
 G^m=G compose Ad_(V_Q) compose Phi_Q^(m-1) compose Ad_(V_Q*).

The order in the second identity is important: G is input-supported on Q, not necessarily output-supported there.

Since GF=0,

 Phi^n=sum_(j=0)^n F^(n-j) G^j.

For n=N_p+N_q+1, every term contains an EB power of F or of G. Therefore

 n_EB(Phi)<=N_p+N_q+1.                              (2)

This proves a uniform bound on all exactly reducible maps, conditional on lower-dimensional uniform bounds. It does not extend (2) to approximately invariant corners without a new argument.

## Remaining obstruction

The key open step is a positive, quantitative extension from these exact boundary strata to nearby primitive maps, with finite algebraic vanishing orders charged. Generic small distance to EB is inadequate; a signed approximation is not a CP decomposition, and powers of a changing filtered map are not powers of a fixed map. Higher-dimensional separability cannot be replaced by the PPT criterion used in the qubit theorem.

## Narrow prior interface

Park, *Every PPT channel has finite entanglement breaking index*, arXiv:2608.13551, https://arxiv.org/abs/2608.13551, Section 3, obtains the relevant cross-support vanishing from complete copositivity and gives a CP Schur-complement split plus an index bound through PPT corner maps. Only that interface was inspected here. The paper's overall pointwise theorem and later uniform-index claims are not certified by this comparison. The generic unitary-postfilter contradiction above uses the explicitly assumed pointwise-eventual mapping cone instead of PPT to force vanishing.
