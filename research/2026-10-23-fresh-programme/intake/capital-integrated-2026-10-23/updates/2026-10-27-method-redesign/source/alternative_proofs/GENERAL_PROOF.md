# A fixed-size exact SDP for every allowed K

This strengthens `PROOF.md` by removing the assumption that K is invertible.
Only the required full input rank of L is used. The supplied finite free
representation and its accepted compression/witness lift are the interface.
This is a new construction within this experiment, with no historical-priority
claim. The code and all executed data are ordinary local files.

Use B and V_L(Q)=A_L(Q)^-1 as in `PROOF.md`. Put M=K B (a three-by-two
real rational matrix), D_K(Q)=diag(W_1^K,W_2^K,W_3^K), and V_Li=V_L(e_i).
The original quadratic form is

    A_K(Q)=M^T D_K(Q)^-1 M.

For any c>=0 the required free comparison is equivalent to

    P_c(Q):=c D_K(Q)-M V_L(Q) M^T >=0.                  (1)

For c>0 this is the equivalence between T*T<=cI and TT*<=cI, with
T=D_K^-1/2 M A_L^-1/2. Congruence yields (1). For c=0 it holds exactly
when M=0, namely when K is constant on its input columns. This handles
rank-one nonconstant and all other singular K without a limiting inversion.

The covariance identity proved in `PROOF.md` gives

    V_L(Q)=sum_i V_Li tensor Qi+Gamma(Q),
    Gamma=diag(Q1,Q2)-[Q1;Q2][Q1,Q2].                  (2)

Set C_i=M V_Li M^T, D_i=diag(K[:,i]), and P_i(c)=c D_i-C_i.
Define E=[I3;I3;I3], and let the rational vector s in R9 have successive
blocks M[:,0], M[:,1], 0_3. Let

    T=[ I3   0
         0  I3
       -I3 -I3 ],       S=ss^T.

A rational, independently checkable upper certificate is a symmetric
nine-by-nine matrix A with

    A>=0,    A_ii=P_i(c),    T^T(A-S)T>=0.             (3)

Here diagonal blocks have size three. All conditions are affine in c,A.
The first and last conditions are exact rational PSD tests of sizes nine
and six, respectively. No effect dimension, vector, or numerical residual
is part of the final certificate verifier.

To prove sufficiency, fix arbitrary complex test vectors z1,z2,z3 and put
V=[z1,z2,z3]. Set Xi=V*Qi V, Yij=V*QiQj V, D=diag(Xi), H=D-Y.
As proved in `PROOF.md`, Y>=0, H>=0, HE=0. The covariance term obeys

    z* M Gamma(Q) M^T z=s*H s.

Indeed the first part is sum_{i=1,2}<sum_a M_ai z_a,Qi sum_b M_bi z_b>,
and the subtracted norm is ||sum_{i=1,2}Qi sum_a M_ai z_a||^2, exactly
the two parts of s*(D-Y)s. Thus

    z*P_c(Q)z
      =sum_i Tr(P_i(c) Xi)-Tr(S H)
      =Tr(A Y)+Tr((A-S)H)>=0.                         (4)

The last inequality follows from (3) and support(H) subset ker(E*).
This proves (1), the all-dimension free comparison, and the all-reference
conditional-Umegaki comparison via the accepted theorem.

The certificate is also complete. The degree-two realization proof in
`PROOF.md`, section 4, works verbatim with Xi of size three (replace the
two test columns by three). Thus its moment cone is exactly

    D=diag(Xi),  Y>=0, H=D-Y>=0, HE=0.

Real parts preserve feasibility and the objective, so a real SDP suffices
despite allowing complex physical witnesses. The exact coefficient equals

    max beta/alpha,
    alpha=sum_i Tr(D_i Xi),
    beta =sum_i Tr(C_i Xi)+Tr(S H),                    (5)

over this cone except its zero element. The denominator is uniformly
positive after trace normalization because every K entry is strictly
positive. The normalized cone is compact: Xi>=0 have bounded total trace,
and 0<=H<=D. Set alpha=1 by homogeneity. Parameterizing H=T J T^T,
the resulting finite primal SDP has strict feasibility: take Xi=a I3 and
J=b I6 with sufficiently small positive b/a, then rescale to alpha=1.
Its objective is finite and attained. The dual is exactly minimization of
c under (3), and strict feasibility gives dual attainment and no gap.
This proves exactness of this fixed-size SDP for the entire stated input
class, not just a sufficient relaxation or a favorable test family.

`general_certificate.py` implements (3), rational reconstruction, and
exact checking. `primal_witness.py:general_moment_witness` implements (5),
the explicit moment realization, accepted compression to active dimension
at most three, and exact rational free-witness evaluation. Numerical
moments are not trusted: reconstructed rational Qi must be positive
definite, sum to identity exactly, vectors sum to zero exactly, and the
reported ratio is computed by exact rational matrix inversion.

The solver can fail at unfavorable numerical conditioning. The implemented
upper fallback is the rigorous expansive vertex certificate from `PROOF.md`;
it preserves validity, although it can lose tightness. This finite numerical
limitation does not alter the exact SDP theorem or any verified certificate.
There is no assumption of a supplied optimizer, optimal witness, or favorable
conditioning in the mathematical reduction.
