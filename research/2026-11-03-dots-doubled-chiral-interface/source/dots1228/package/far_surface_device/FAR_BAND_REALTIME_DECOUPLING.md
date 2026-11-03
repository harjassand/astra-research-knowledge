# Finite slab with exposed far Weyl band: full-norm decoupling and state-independent response

Status: constructive proof, sent for independent audit. This is a finite-time operation, not a global gap assertion after deleting the remote mass.

## Acquired input and actual device

Take the constructed strict-range near-interface Hamiltonian. Its additional bounded even interactions K_X (including rotor-dependent near mass, scalar counterterm and dressed rotor reset) are supported in the strip0<=w<=R. All rotor factors are retained, possibly infinite dimensional. Outside this strip the original free Wilson quadratic Hamiltonian is literal. Remove the far mass, its far decoration and far-interface rotor terms. The resulting actual device is

 H=dGamma(h_W)+sum_X K_X,

with N tangential lattice sites, normal thickness L>R+1, physical spacing a and original m=-1 Wilson root. Scalar constants are immaterial. This formula assumes the input near-interface interactions have truly fixed strip support; no long-range tail is silently discarded here.

Choose a target tangential momentum set B contained in |k|<=kappa, where k=ap is dimensionless and b_*=max_B sum_i(1-cos k_i)<1. For a simple low ball, b_*<=kappa²/2. Include complete internal flavor multiplets, so its one-particle projector commutes with the onsite symmetry representation. Let m=#B and r=dim F be the number of target fermionic modes, including all internal multiplicities (r=8m for the original16-orbital particle/hole-flavor Wilson matrix; the actually constructed canonical-parent device has TWO same-chirality fast copies and32 free orbitals per site, so r=16m when exposing all its species). The extra canonical copy is physical; no copy-removal or original-four-species claim is made.

## Exact target CAR subspace and free leakage

For each target k, choose the pure FAR normal-chirality geometric profile

 f_k(w)=Z_k b(k)^(L-1-w),
 Z_k=(sum_{j=0}^{L-1}b(k)^(2j))^-1/2<=1.

Together with normalized tangential Fourier waves and the far-chirality spin/flavor vectors, these form an EXACT orthonormal one-particle subspace F. They are not supplied eigenvectors: the formula is explicit. Write P_F for its projector and Q=1-P_F.

Compression of the free Wilson matrix is exactly the far Weyl lattice dispersion h_F, with the appropriate physical species signs, +/-sigma.sin(k)/a. The normal-chain residual is confined to the opposite end and satisfies

 ||Q h_W P_F||<=b_*^L/a.

The residual is orthogonal to F because its normal chirality is opposite. Thus h_W differs from h_F direct-summed with Qh_WQ only by a rank-at-most2r offdiagonal matrix. On the FULL fermionic Fock space, retaining all particle numbers,

 ||dGamma(h_W)-dGamma(h_F)-dGamma(Qh_WQ)||<=2r b_*^L/a.

This conservative trace-norm bound explicitly charges all r potentially occupied target modes. It is not a single-particle error incorrectly reused for a many-body state.

## Local fermionic algebra removal lemma

Let a bounded even term K_X involve d_X physical coordinate fermionic orbitals (not an arbitrary delocalized mode basis) and arbitrary bounded operators on its local rotor factors. Let S_X be its one-particle orbital support and alpha_X=||P_F P_SX||. If alpha_X<=1/2, there exists a one-particle unitary U_X mapping S_X into Q, with nontrivial rank at most2d_X and principal angles at most arcsin alpha_X. Its exact number-conserving second quantization obeys

 ||Gamma(U_X)-I||<=2d_X arcsin(alpha_X)<=4d_X alpha_X.

Consequently

 K'_X=Gamma(U_X)K_X Gamma(U_X)^*,
 ||K'_X-K_X||<=8d_X||K_X|| alpha_X.

K'_X belongs entirely to the Q-mode algebra and the original rotor factors. Because it is even, it commutes with every target CAR operator. This is an analytical comparison Hamiltonian; K'_X need not be spatially local and is not substituted into the actual device.

Construction: if J is the inclusion of S_X, the map QJ(J^*QJ)^-1/2 is an isometry into Q. Its direct rotation with J has the stated principal-angle bound. The second-quantized generator has eigenvalue absolute sum at most2d_X arcsin alpha_X. No normalized rotor trace or finite rotor dimension is used.

At every strip orbital w<=R, the squared projection onto F is at most(m/N)b_*^(2(L-1-R)), by explicit Fourier normalization and Z_k<=1. Hence

 alpha_X<=sqrt(d_X m/N)b_*^D<=sqrt(d_X)b_*^D,
 D=L-1-R.

Terms with no fermionic factors already commute with F and incur zero error.

## Full operator-norm approximation

Define the comparison operator H_dec=dGamma(h_F)+H_rest, where

 H_rest=dGamma(Qh_WQ)+sum_X K'_X

acts only on Q modes and the FULL rotor system. No eigenstate, spectral gap, response function, inverse or simulation of H_rest is supplied or assumed. With the standard graded Fock factorization, H_rest is even and acts trivially on the F factor.

Then

 ||H-H_dec||<=delta_L,
 delta_L=2r b_*^L/a+C_int b_*^D,
 C_int=8 sum_X d_X^(3/2)||K_X||.

A sharper factor sqrt(m/N) may multiply C_int but is not needed. If the fixed strip interaction density satisfies sum_X d_X^(3/2)||K_X||<=J_strip N, then C_int<=8J_strip N. Thus the full-volume operator-norm charge is explicit. Infinite-dimensional rotor factors cause no difficulty: every finite-volume term is bounded, so both total finite-volume operators are bounded self-adjoint.

## Actual finite-time operation

For every bounded observable O supported in the target CAR algebra,

 ||e^(itH)Oe^(-itH)-e^(it dGamma(h_F))Oe^(-it dGamma(h_F))||
 <=2|t| delta_L ||O||.

This holds for ANY initial state, including correlated interacting equilibrium states. It does not require preparing a factorized Gibbs state or computing an interface response.

In particular the target single-particle RETARDED anticommutator becomes state-independent, up to a controlled error. With c(f)=sum_j conjugate(f_j)c_j and standard inner product linear in its second slot,

 c(f,t)_free=c(e^(it h_F)f),
 {c(f,t)_free,c(g)^*}=<e^(it h_F)f,g>I.

For the actual interacting device,

 ||{c(f,t),c(g)^*}-<e^(it h_F)f,g>I||
 <=4|t|delta_L ||f||||g||.

Thus measuring or predicting the band-limited far-surface retarded propagation is earned without any rest-state oracle. These are explicit geometric-profile wavepackets; a strictly single-layer/local probe has additional non-target-band spectral weight and is NOT claimed to obey this estimate unchanged.

The one-particle continuum Weyl comparison adds only the charged dispersion error: ||h_F-h_cont||<=a²Lambda³ for physical |p|<=Lambda=kappa/a. The scalar anticommutator then has additional error <=|t|a²Lambda³||f||||g||. This is a kinematic finite-window comparison, not a gauged continuum construction.

## Spectral statement and its limitation

Since ||H-H_dec||<=delta_L, their full spectra have Hausdorff distance at mostdelta_L. The comparison spectrum is the sum of the actual unknown rest spectrum and the finite free target-Fock spectrum. If rotor factors are finite, ordered finite-dimensional eigenvalues also differ by at mostdelta_L with multiplicity. For infinite rotor factors, no discrete-eigenvalue or Gibbs-trace assertion is made.

This result does NOT prove that H_rest is gapped or that the only low-energy excitations of the entire finite device are the desired Weyl modes. Its guaranteed operation is the above state-independent real-time response of the explicitly exposed band. It deliberately avoids inferring a global device gap after deleting the remote mass.

## Paid thickness and resources

For target response tolerance epsilon through |t|<=T, set delta_target=epsilon/(8 max(T,1)). It suffices that

 D >= ceil(max{log(2sqrt(d_max)), log[(C_int+2r/a)/delta_target]}/|log b_*|),
 L=R+1+max(1,D).

This ensures every alpha_X<=1/2 and delta_L<=delta_target. Thus L grows as R+O(log[N(T+1)/(a epsilon)]/|log b_*|) for fixed local strip resources and target window. All high Wilson modes and all many-body occupations remain present; no Fock truncation occurs. Spatial resources are N L sites with the original fixed fermion orbital count plus the original near-strip rotor degrees of freedom. The continuum-dispersion condition T a²Lambda³<=epsilon/2 must be charged separately if continuum rather than lattice Weyl propagation is requested.

The massive-interface construction's enormous UV constants and strip radius R remain unchanged and explicitly inherited. This logarithmic remote-face separation is not a claim of practical end-to-end simulation efficiency or finite-dimensional rotor implementation.

Audit closure: independent auditor passed the canonical CAR, free residual, full-Fock rank bound, local direct rotation, graded even commutation, Duhamel and anticommutator conventions. If b_*=0, the selected modes live exactly on the far layer and decouple exactly when L>R+1; the logarithmic thickness formula is unnecessary. The chosen delta budget uses at most epsilon/2 for the lattice response, leaving epsilon/2 for the optional continuum dispersion comparison.
