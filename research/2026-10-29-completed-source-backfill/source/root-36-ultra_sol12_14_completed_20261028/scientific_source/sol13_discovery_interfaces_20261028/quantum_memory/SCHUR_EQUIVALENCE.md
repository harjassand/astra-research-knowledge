# Exact matrix-weight and complete Schur-coherence formulations

Use the nine Hesse unit vectors s_i and S_i=|s_i><s_i|. Let A_i>=0
on finite L, C=sum A_i, M=sum S_i tensor A_i, and Tr C=1. Choose
rectangular factors A_i=V_i V_i* with a common column space E. Put
V=[V_1 ... V_9]. The Gram state rho=V*V on I9 tensor E has blocks
rho_ij=V_i*V_j. Define G_ij=<s_i|s_j> and Gamma(rho)=G o rho.
The exact nonzero-spectrum identities are
`rho <-> C=VV*`,
`(diag_I tensor id_E)rho <-> direct_sum_i A_i`, and
`(Gamma tensor id_E)rho <-> M`.
For the last use W=[|s_1>tensor V_1 ... |s_9>tensor V_9]: W*W has
blocks G_ij V_i*V_j and WW*=M. Thus the target is exactly
`2S(Gamma rho)>=S(rho)+S(diag rho)`, or complete coherence contraction
`D(Gamma rho||diag rho)<=D(rho||diag rho)/2`.

Conversely factor any finite rho as V*V and use its nine block columns
V_i. The resulting PSD A_i=V_i V_i* recover exactly those entropies.
No scalar-to-complete transfer or unrestricted-W3 equivalence is used.
Factorization and matrix reading are actual finite-input operations.
In the purification convention |Psi>=sum_i |i>|psi_i>_LE, rho_IE is the
global transpose of this Gram state and the Schur coefficient is instead
<s_j|s_i>. These conventions are equivalent by GLOBAL transpose of the
label-plus-E matrix, preserving positivity/entropy. A label-only partial
transpose is not assumed positive.

The completely solvable controls with A_i=S_i/9 have
C=I3/3, M=P_sym/6 and target log(4/3). For A_i=S_i^T/9, M=(I+P_Omega)/12,
with eigenvalues1/3,1/12(x8), giving target(8/3)log2-log3. Orthogonal
memory weights A_i=p_i|i><i| give exact equality: the memory knows the
label and both conditional entropies vanish. These are analytic controls,
not a justification for monotonicity under losing arbitrary memory.
