**WITHDRAWN APPLICATION: no unconditional magnetic-gap theorem has been proved for the actual gauged rotor/cochain family. Only the conditional localization lemma survives after its uniform local Schur–Lipschitz premise is earned.**

# Conditional magnetic localization lemma, and retained electric geometry

2026-11-03. AUDIT CORRECTION: the localization algebra below is valid, but its local Schur comparison has NOT been acquired for the full actually gauged discontinuous rotor/cochain family. Tree gauging after onsiting translates rotor arguments through floor walls, so arbitrarily small residual link shifts can change a coefficient by O(1). Different overlapping stencil trees need not give one common transformed rotor configuration. A finite charge cutoff restores norm differentiability but makes the coefficients operator-valued rotor matrices, so it is not the same classical-phi free family. Therefore this is a CONDITIONAL localization lemma, not a proved magnetic gap theorem for the full actual interface. It does apply to a smooth Wilson-link-only family with a genuinely common fixed/gauge-transformed texture. No later claim should import its sign-function conclusion for the actual gauged parent without paying this input.

The intended lemma would replace the volume-growing spanning-tree threshold for the FREE fast slab only. It does not silently promote that statement to an interacting interface theorem or to a slab with a gapless desired face.

## 1. Inputs already acquired

For every rotor configuration phi, the actual finite-range one-body Wilson-plus-decoration family h0(phi) has spectrum outside(−gamma,gamma), uniformly in volume and normal thickness, when BOTH faces are massed. Keep individual UV normal sites explicit. Let r be hopping/stencil range, and J0 a uniform operator Schur row/column norm bound on hopping matrices. Decoration couplings and conditional boundary masses are included. Their fixed spatial stencils have bounded rotor dependence; no rotor derivatives are needed here.

Gauging a quadratic term by the actual integer-charge local trees leaves it quadratic conditional on phi and gauge links. Let qpath be a bound on the sum of absolute charges and path lengths appearing in any one hopping/mass stencil. All these quantities are finite at the already chosen astronomical UV refinement. The gauge transformation also acts on charged rotor coefficients. A local gauge choice transforms phi to another allowed configuration, for which the same uniform gamma bound holds.

## 2. Local gauges, not a global vector-potential assumption

In a simply connected cubic patch of side ell (plus r-sized buffer), if every plaquette principal angle has magnitude≤epsilon and epsilon ell² is small enough to choose consistent lifts, the usual coordinate axial gauge gives residual link representatives bounded by c_d epsilon ell. Each representative is a sum of at most c_d ell plaquette angles, not the area of an arbitrary global spanning-tree loop. A nearest-neighbor axial construction sets the first-direction links to zero, the second-direction links to zero on a reference first-coordinate plane, etc. Plaquette identities recursively determine the remaining links. Integer charges make different2pi lifts physically identical. Pure gauge fields are removed exactly.

Thus for vectors supported inside the patch,

 ||[h(A,phi)−G_patch h0(phi_patch) G_patch†]v||
 ≤C_mag epsilon ell ||v||,

with C_mag bounded by c_d J0 qpath times fixed stencil geometry. The row/column Schur estimate is why no patch volume appears. The reference rotor configuration phi_patch is the locally transformed phi extended arbitrarily outside the buffered patch; all references have the acquired gamma gap.

The lift restriction can be retained explicitly as epsilon ell²≤c_lift. It does not spoil a volume-independent threshold: choose ell first, proportional to C_loc/gamma, and then require epsilon≤min(gamma/(4C_mag ell),c_lift/ell²). There is no need to optimize ell to quote a clean existence threshold. This covers nonzero constant magnetic fields without requiring globally small A. On large tori all patches are chosen contractible; holonomies outside patches do not enter. Very small tori can be dealt with separately, not by assuming their holonomies vanish.

## 3. Partition-of-unity gap estimate

Choose real diagonal localization functions chi_j with Σ_j chi_j²=1, patch diameter ell, bounded overlap, and discrete gradients≤C/ell. Finite range and a Schur estimate give

 (Σ_j ||[h(A,phi),chi_j]ψ||²)^(1/2)
 ≤(C_loc/ell)||ψ||,

where C_loc≤c_geometry J0 r and is independent of volume and normal thickness. Boundary charts can be reflected/one-sided; their overlap constants remain fixed. Normal direction may be localized as well or left unchanged if the gauge field is the same along it, provided no whole-slab norm is inserted.

For each patch,

 ||h(A,phi)chi_jψ||≥(gamma−C_mag epsilon ell)||chi_jψ||.

Minkowski in the direct sum over j gives

 (Σ_j||h chi_jψ||²)^(1/2)
 ≤||hψ||+(C_loc/ell)||ψ||.

Therefore

 ||h(A,phi)ψ||≥[gamma−C_mag epsilon ell−C_loc/ell]||ψ||.

Choose ell≥4C_loc/gamma and epsilon≤gamma/(4C_mag ell), also respecting the local lift condition. Then the magnetic fast gap is≥gamma/2, UNIFORMLY in volume. If lifts permit the optimizing scale, the error is2sqrt(C_mag C_loc epsilon). This proves the conditional localization lemma ONLY under the unearned local Schur comparison for the actual family. It is not an acquired actual-model magnetic gap.

The same polynomial sign-function construction as in EXPLICIT_JOINT_POLYNOMIAL_LOCALITY.md now applies to h(A,phi) on this curvature domain, with gamma/2 and the same bounded range. It gives exponentially decaying JOINT rotor/link/fermion coefficients for sign h and the fast vacuum energy. If the missing Schur premise is supplied, this would earn weak-curvature Gaussian locality for that fast block. It has NOT been earned for the actual gauged cochain family. It does not establish a global sign on all compact link configurations.

## 4. Berry and Born–Huang terms must remain

Even when a smooth unique fast ground ray Ω(A) and P=|Ω><Ω| are acquired, projection of ordinary electric energy is NOT bare electric energy. In a local phase convention, write a link-space state f(A)Ω(A), and define

 mathcal A_l=−i<Ω,∂_lΩ>,
 Phi_BH=(κ_E/2)Σ_l <∂_lΩ,(1−P)∂_lΩ>.

The exact quadratic form restricted to the ground-ray bundle is

 <fΩ,H fΩ>
 = (κ_E/2)Σ_l ||(−i∂_l+mathcal A_l)f||²
   + <f,[H_B+E0(A)+Phi_BH]f>.

This identity follows by orthogonally decomposing ∂(fΩ). Phi_BH≥0. The connection transforms under ground-ray phase changes and cannot generally be set to zero globally. The off-diagonal electric coupling is proportional to κ_E[2(1−P)∂Ω ∂f+(1−P)∂²Ω f]; this is the source of the finite-time leakage estimate, not an absent term.

For the Gaussian fast block, resolvent/sign differentiation and its joint locality provide locally decaying response kernels under the magnetic gap. For the FULL interacting mirror ground, the corresponding smooth local response and its separation from a desired gapless boundary still must be acquired. The entire gauge effective action also contains the E0(A) vacuum polarization and any induced local counterterms. A proof of small mirror excitation probability alone does not show that these terms reproduce the target chiral gauge response or evade the propagator-zero constraints.

## 5. Consequence gate still open

Conditional on the unearned Schur premise, this note would pay the free-block magnetic gap independently of total volume, and the separate local moment note pays finite-time local curvature under ordinary quantum Wilson links. What does NOT follow merely by combining them is a symmetric interacting mirror gap at nonzero curvature, a local mirror/light factorization, or fixed-coupling thermodynamic decoupling. The reason is concrete: after the actual onsite disentangler, the rotor-reset parent and its electric response require their own gauge-covariant local construction; gauging a non-symmetric Gaussian preparation W is not justified by gauging the already symmetric final Hamiltonian. The desired light face also prevents using the whole-slab sign(h) as a uniformly local unitary.
