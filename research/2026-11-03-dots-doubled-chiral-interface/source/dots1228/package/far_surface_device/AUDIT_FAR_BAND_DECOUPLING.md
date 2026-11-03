# Independent audit: explicit far-band finite-time decoupling

2026-11-03. Audited `FAR_BAND_REALTIME_DECOUPLING.md` at the constructor's request; result reported to root.

## Verdict

The foundational lemma is correct for the stated finite slab with bounded even near-strip interactions. It supplies a state-independent finite-time operation on an explicit target CAR band without a rest-state oracle. It does not prove a rest-sector gap or that all remaining low-energy modes are absent.

Corrections/clarifications:
- The old particle/hole-plus-flavor matrix has 16 physical complex orbitals per normal site and r=8m target modes. The CANONICAL-PARENT device additionally doubles that same-chirality fast system, so its full target has r=16m and 32 free orbitals per site. All general formulas in r remain valid; the extra copy must be charged.
- d_X should count physical coordinate orbitals in the local term support. The optional m/N improvement is not generally valid if d_X instead denotes a small number of arbitrarily delocalized linear-combination modes.
- If b_*=0, the target is exactly confined to the far layer and all displayed leakage vanishes for L>R+1; use that case directly instead of log(b_*).
- To promise total continuum error epsilon, split the lattice-decoupling and dispersion budgets. Giving each epsilon only proves total error at most 2 epsilon.

## 1. Geometric CAR modes and free residual

The supplied normalized geometric profiles and distinct Fourier waves define exactly orthonormal one-particle modes. They need not be eigenvectors. On each complete far-chirality internal multiplet, compression of the tangential kinetic matrix is exactly the stated Weyl lattice dispersion. The normal-chain trial residual has magnitude Z_k b(k)^L/a<=b_*^L/a, is at the opposite end, and has opposite normal chirality, so it is orthogonal to the entire target F.

Orthogonality of momenta/internal multiplets makes the leakage norm a maximum, not a sum over modes. The offdiagonal free error has rank at most 2r and trace norm at most 2r b_*^L/a. Its second quantization on the FULL Fock space has norm no greater than that trace norm. In fact its balanced singular-pair structure allows a slightly sharper bound, but the given constant is conservative. No single-particle estimate has been illicitly transferred without an occupation/rank factor.

## 2. Removing the target band from arbitrary bounded local interactions

For a physical support inclusion J, QJ(J dagger QJ)^(-1/2) is an isometry if ||P_F J||<1. Its principal angles to J have sine equal to the singular values of P_F J. The canonical direct rotation has nontrivial rank <=2d_X and eigenangles bounded by arcsin(alpha_X).

Its canonical number-conserving Fock lift has vacuum phase one. Bounding sums of occupied one-body eigenangles gives

  ||Gamma(U_X)-I||<=2d_X arcsin(alpha_X)<=4d_X alpha_X

for alpha_X<=1/2. Therefore the stated conjugation error <=8d_X ||K_X||alpha_X holds even when K_X has arbitrary bounded rotor-operator coefficients.

The transformed term is in the CAR algebra of Q modes and the original rotor factors. Because K_X and Gamma(U_X) are even, this transformed term commutes with EVERY target CAR operator, including odd annihilators. An ordinary ungraded tensor-factor argument without this parity statement would be insufficient; the note handles it correctly.

For a physical coordinate orbital in the strip, its diagonal target-projector entry is <=(m/N)b_*^(2D), D=L-1-R. Summing these entries over the physical support gives the displayed alpha_X bound. Complete internal multiplets do not add an extra factor here: the diagonal entry of their internal projector is at most one. Their multiplicity is already included in r and in the physical support count d_X.

The separate U_X need not be mutually compatible or spatially local. This is harmless because the comparison Hamiltonian is the sum of the separately conjugated Q-only terms, not an asserted single conjugation of the actual device. No local implementation of H_rest is being promised by this lemma.

## 3. Full-norm and observable bounds

The triangle inequality gives exactly the advertised delta_L with C_int=8 sum_X d_X^(3/2)||K_X||. Terms with no fermion factor incur no removal error. The full-volume factor in C_int is essential and is explicitly paid.

On the graded Fock factorization, the even H_rest acts trivially on the target factor. Duhamel's formula for bounded finite-volume self-adjoint Hamiltonians gives operator error <=2|t|delta_L||O|| for every target observable, irrespective of the initial state or its entanglement with the rest. Infinite-dimensional rotor factors cause no issue because all finite-volume terms remain bounded.

With the stated anti-linear annihilator convention,

  c(f,t)=c(exp(it h_F)f),
  {c(f,t),c(g) dagger}=<exp(it h_F)f,g> I.

These signs are correct for the inner product linear in the second argument. Taking the anticommutator of the operator approximation adds a factor 2||g||, giving the stated 4|t|delta_L||f||||g||. The conventional retarded prefactor -i theta(t) does not change that norm bound. This proves a physical even response, despite using odd CAR fields in the intermediate estimate.

The continuum dispersion error adds |t|a^2 Lambda^3||f||||g||. A strictly local single-layer probe has additional target-complement weight; the note correctly does not claim its response is exhausted by this band.

## 4. Thickness, spectra, and remaining gate

The stated logarithmic thickness ensures alpha_X<=1/2 and delta_L<=delta_target because b_*^L<=b_*^D. All factors r, local term counts, interaction strengths, and the inherited strip radius remain in the ledger. The bound is not a practical-resource claim.

For bounded self-adjoint operators, full spectra are within delta_L in Hausdorff distance. Because the F Fock factor is finite dimensional, the decoupled spectrum is the union of copies of the unknown rest spectrum shifted by target free Fock energies. No discreteness or Gibbs trace is implied for the infinite rotor factor.

A subsequent uniform rest-gap theorem must impose that B contains every far mode below a fixed physical cutoff. For an arbitrary narrow B, omitted low-momentum far modes remain in Q. Moreover the sharp Fourier projector P_F is tangentially nonlocal, so a canonical parent built on compressed Q modes is not automatically a local physical model. It may be used as an analytic benchmark, but its relation to the actual near-strip terms needs a separate quantitative bound. Neither issue damages the finite-time decoupling lemma audited here.
