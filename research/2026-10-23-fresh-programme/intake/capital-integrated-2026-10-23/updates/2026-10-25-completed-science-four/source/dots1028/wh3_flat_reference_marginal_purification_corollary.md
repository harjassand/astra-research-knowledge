# Full WH3 absolute entropy target for every flat reference marginal

2026-10-25. Analytic corollary and independent audit. **PASS.** Every state rho_AR with rho_R=P_R/r, a normalized projection on its reference support, satisfies

D(rho_AR || I_3/3 tensor rho_R)
 >=2D((W3 tensor id_R)(rho_AR) || I_3/3 tensor rho_R).

The global spectrum of rho_AR is unrestricted. The reference support rank r and global rank are arbitrary finite values. This follows from the all-projector input theorem and the already established WH3 purification duality, not from an assumption that a flat marginal makes the joint state flat or classical.

## Exact purification transfer

Purify rho_AR to a pure state psi_ARE, and write rho_AE=Tr_R psi. The nonzero spectra of rho_AE and rho_R agree. Since rho_R has r equal nonzero eigenvalues 1/r, there is an orthogonal projection Pi_AE of rank r such that

rho_AE=Pi_AE/r.

The complementary state is therefore in the complete normalized-projector class, regardless of its reference E marginal or ambient zero eigenspace. The proved theorem `wh3_all_projector_inputs_entropy_theorem.md`, independently audited in `wh3_all_projection_inputs_independent_audit.md`, gives Delta_N(rho_AE)>=0.

To verify that this is the desired target, apply the antisymmetric WH3 Stinespring isometry from A to B,C. Both reduced channels A->B and A->C equal W3 up to a fixed unitary basis convention. The resulting Omega_BCRE is pure. Consequently

S((N_R rho_AR))=S(BR)=S(CE)=S(BE)=S((N_E rho_AE)).

Also S(rho_AR)=S(rho_E) and S(rho_AE)=S(rho_R). Thus the absolute entropy deficits satisfy exactly

Delta_N(rho_AR)
=2S(BR)-S(rho_AR)-S(rho_R)-log3
=2S(BE)-S(rho_AE)-S(rho_E)-log3
=Delta_N(rho_AE).

This is the same duality reconstructed in Section 3 of `wh3_rank_two_qubit_reference_mi_theorem.md`. No measurement, reference discarding inequality, or convexity of Delta_N is used. The claimed result follows immediately.

## Scope boundaries

The conclusion is the full absolute entropy target on the flat-reference-marginal class, including arbitrary global spectra and quantum correlations. It does not by itself prove the stronger mutual-information contraction I(B:R)<=I(A:R)/2, because the all-projector theorem used here proves the absolute target rather than that stronger comparison.

A reference marginal with two DISTINCT positive eigenvalues is not automatically covered by the affine-projector theorem on the complement. Its complementary joint state has those positive eigenvalues plus any ambient zero eigenvalues; if the zero eigenspace is nonproduct, this generally has three spectral levels and is not an affine-projector input. The flat case is safe because equal positive eigenvalues plus zeros are exactly a normalized projector at every ambient dimension.

The exact duality can transfer any other independently established spectral class whenever the complementary state actually meets that class's full ambient/support hypotheses. No unsupported extension to arbitrary reference spectra is inferred here. This corollary is specific to WH3's self-complementary dilation and is not claimed for general Werner-Holevo dimension or every isotropic-adjoint-square channel.
