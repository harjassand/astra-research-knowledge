# Exact real structure of the actual Wilson/SU(2) family

Root construction, 2026-11-03. This reduces one phase question; it does not establish cancellation of determinant-line holonomy or a quantum interface gap.

For the code gamma matrices
Gamma=(X tensor X, X tensor Y, X tensor Z, Y tensor I, Z tensor I),
let S=I tensor (iY) on its four spin/normal orbitals, and J=i tau_y on the two flavor copies. Both are real and square to -I.

They obey S Gamma_mu* S†=-Gamma_mu for mu=1,...,4, and S Gamma_5* S†=Gamma_5. Therefore the real-space Wilson hopping -Gamma5/2-i Gamma_mu/2 is fixed by S followed by complex conjugation. The onsite Wilson term is fixed too; real ± antiperiodic seam factors do not alter this.

Every SU(2) matrix satisfies J U* J†=U. Consequently the combined antiunitary

  T = diag(J tensor S, J tensor S) K

on the doubled +/-h model (with site identity factors understood) fixes the COMPLETE Hamiltonian for every arbitrary spatial SU(2) texture U(x). It is independent of the rotor values, and T²=+I because the two pseudoreal factors each square to -I.

A nondegenerate gapped Slater ground line therefore has a real structure. In a smooth parameter patch one can choose a normalized T-real ground vector; its Berry connection vanishes, since normalization makes its real inner product with its derivative zero. The determinant-line transition functions are then signs. Thus the free ground family has no continuous U(1) Berry curvature in each smooth chamber: remaining holonomy is Z2, not an arbitrary complex phase.

This statement does not assert triviality of that real line bundle. In particular a real Berry phase -1 around a loop remains possible. Cross-chamber charged transfer operators have to be constructed, and the Majorana decoration's phase/sign conventions must be joined explicitly. Matching self-linking charges alone does not prove cancellation of this real holonomy. An arbitrary complex kernel is not made adequate merely by knowing the Hamiltonian has a real structure.

The antiunitary can be checked on local matrix blocks, so there is no finite-volume or UV approximation here. Numerical algebra on all four hopping directions and100 random SU(2) matrices gave zero residual at floating precision; results are in root_real_structure_check.json.
