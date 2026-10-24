# Inclusive heat loss from three equilibrium imaginary-time correlations

25 October 2026. Owned continuation of INCLUSIVE_NOISE_TRANSPORT.md. The
purpose is to replace an unnecessarily strong microscopic target--uniform
real-frequency convergence of a retuned double-well susceptibility--by a
finite equilibrium correlation certificate. This theorem is conditional only
on that note's explicit equilibrium scattering contract, not on a TLS
approximation. No measurement or efficient Gibbs sampler is assumed.

## Scaled positive measure

Put theta=k_B T/hbar and let

    C_theta(s)=<Y(-i s/theta)Y(0)>_T-<Y>_T^2,  0<=s<=1.

The Lehmann representation, with any static covariance included as an atom
at zero, defines a positive measure rho_theta on z=omega/theta such that

    C_theta(s) = int K_s(z) d rho_theta(z),
    K_s(z)=cosh[(1/2-s)z]/cosh(z/2),
    rho_theta([0,infinity))=Var_T(Y).                         (1)

For positive omega its unscaled measure is
(hbar/pi)coth(omega/(2theta))chi_Y''(omega)d omega. The static atom contributes
equally to all C_theta(s). Thus it cancels in every combination below.

The auxiliary inclusive deficit with the even phase set to one is exactly

    delta_0 = (3Z/(2pi hbar)) int w(z) d rho_theta(z),
    w(z)=z^3/(2sinh z).                                      (2)

The actual finite-common-mass deficit delta obeys
|delta-delta_0|<=c_M M theta/Z, c_M=9zeta(3)/pi^2. This error is uniform in
the nonlinear potential and in the retuned family.

## A finite certificate, without analytic continuation

Define the actual full-system equilibrium quantity

    H_theta=C_theta(1/4)-(2/3)C_theta(1/2)-(1/3)C_theta(1/8).

Then

    delta >= [Z/(24pi hbar)] H_theta - c_M M theta/Z.         (3)

Proof: set h=K_(1/4)-(2/3)K_(1/2)-(1/3)K_(1/8). I prove the GLOBAL
pointwise inequality w(z)>=h(z)/36, not a frequency-grid approximation.
For x=z/8 and c=cosh x,

    h(z)=[(c-1)(-4c^2+2c+5)]/[3cosh(4x)].

Its positive region has c<(1+sqrt(21))/4<7/5. But
cosh(7/8)>1+(7/8)^2/2+(7/8)^4/24>7/5, so h<=0 for z>=7.
For 0<=z<=7,

    h(z) <= [cosh(z/4)-1]/cosh(z/2) <= z^2/32,
    w(z) >= z^2/(2cosh z) >= z^2/(2cosh 7) > z^2/1152.

Here sinh z<=z cosh z, cosh t-1<=t^2 cosh t/2, and cosh 7<576 (direct
Taylor bound) suffice. Thus w>=h/36 wherever h>0; it is automatic elsewhere.
Integrating against the positive rho in (1), then using (2) and the exact
finite-M error, proves (3).

If estimated correlations have certified absolute errors e_(1/4), e_(1/2),
e_(1/8), replace H_theta by

    H_hat-e_(1/4)-(2/3)e_(1/2)-(1/3)e_(1/8)

in (3). Only three imaginary-time observables are required. They may be
bounded in an equilibrium path-integral calculation or by some separately
specified acquisition method. Their computational/mixing and precision
costs are not supplied for free. Imaginary-time values are not being
misidentified as three ordinary laboratory-time measurements.

The numerical constant is deliberately conservative. Optimizing it is not
needed for the consequence: any strictly positive limit of H_theta gives a
strictly positive cold heat-deficit fraction at fixed M,Z. The criterion
applies to the FULL canonical coordinate, including high intrawell states.

## Qualitative effective-theory transfer theorem

There is also a complete convergence statement. Suppose Var_T(Y)<=V_max
uniformly along a cold sequence and, for every s in a dense subset of (0,1),
C_theta(s) tends to int K_s d rho_* for a specified finite positive measure
rho_*. Then

    delta -> (3Z/(2pi hbar)) int w(z)d rho_*(z),              (4)

provided M theta/Z->0. A fixed finite high-frequency variance need not vanish:
it can escape to z=infinity and does not contribute to the thermal heat
functional. No claim that it costs no physical range is made.

Proof: bounded positive measures are vaguely precompact on [0,infinity).
Each K_s for 0<s<1 is continuous and vanishes at infinity, as does w. Any
vague subsequential limit therefore reproduces the assumed correlations.
These correlations uniquely determine the finite part of the measure. To
see uniqueness, let sigma be the difference of two such finite measures.
Place half of d sigma(z)/cosh(z/2) at each of +z and -z. Its bilateral
Laplace transform is int cosh(xz)/cosh(z/2)d sigma(z), which vanishes for
|x|<1/2. It is analytic in that strip, and hence its Fourier transform is
zero by analytic uniqueness. The signed measure is zero, and the strictly
positive weighting then implies sigma=0. Continuity in s extends the dense
set premise to the open interval. All subsequential limits agree, so the
w integral converges. Equation (2) and the uniform mass error give (4).

This is a transfer theorem, not an efficient analytic-continuation algorithm.
It explains exactly what an imaginary-time low-energy construction must
prove to determine inclusive heat. For a nonzero lower bound, the finite
certificate (3) is substantially weaker than even the full premise of (4).

## Exact conventional impurity benchmark

For the unbiased Toulouse spin-boson SCALING MODEL, alpha=1/2,
Y=d sigma_z and Zd^2=pi hbar/2. Refermionization gives a half-filled
noninteracting resonant level with

    A(epsilon)=Gamma/[pi(epsilon^2+Gamma^2)],
    chi_Y''(omega)=4pi d^2 int A(epsilon)A(epsilon+hbar omega)
                         [f(epsilon)-f(epsilon+hbar omega)]d epsilon.

Wick's theorem proves this bubble and Var(Y)=d^2; no bare isolated TLS line
is used. At Gamma/(hbar theta)=gamma>0 fixed, direct rescaling gives

    delta_0 = (6alpha gamma^2/pi^2) I(gamma),
    I(gamma)=int_0^infinity dz z G(z) int_R du
       [f(u)-f(u+z)]/[(u^2+gamma^2)((u+z)^2+gamma^2)],
    G(z)=[z/(2sinh(z/2))]^2.

The integral is finite and positive. For gamma=1 there is even a simple
analytic lower bound. Restrict to 1<=z<=2, -1<=u<=0. The Fermi difference is
at least (e-1)/(2(e+1))>2/9; the denominator is <=10. On this interval zG(z)
increases and G(1)>5/6 (cosh 1<8/5). Thus I(1)>1/54, and at alpha=1/2,

    delta_0 > 1/(18pi^2) > 1/180.                            (5)

This proves a nonzero cold fraction in that exact scaling model, rather
than inferring it from a plotted susceptibility. The finite-M correction
is already controlled uniformly. It does NOT identify a finite-mass
continuous double-well coordinate with the scaling model.

For reference, the same model's imaginary-time correlations follow directly
from Wick contraction:

    C_theta(s)/d^2=4 F_gamma(s)^2,
    F_gamma(s)=int_0^infinity [gamma/(pi(u^2+gamma^2))]K_s(u)du.

At gamma=1 a finite quadrature diagnostic gives

    C(1/4)/d^2 = .58724546328529903898,
    C(1/2)/d^2 = .52277657994577533389,
    C(1/8)/d^2 = .69474021760935105121,
    H/d^2      = .00714767078499829810 >0.

These displayed decimals are a DIAGNOSTIC, not an outward certificate. The
strict positivity of the deficit is already proved independently by (5).
A full microscopic approximation which bounds these three correlations
within less than their positive H margin would instead use (3) directly,
without requiring a real-frequency response convergence theorem.

## Source and realization scope

The TLS-to-resonant-level mapping is conventional (Guinea, Hakim & Muramatsu,
Phys. Rev. B 32, 4410, DOI10.1103/PhysRevB.32.4410); the free-fermion bubble
and Wick correlations above are independently derived. Dorsey, Fisher &
Wartak, Phys. Rev. A 33, 1117, DOI10.1103/PhysRevA.33.1117, supplies a
controlled low-energy double-well truncation under a scale hierarchy, not
an exact finite-parameter projection. Its indexed primary equations were
read; an accessible full PDF was not acquired. No claim of novelty for
Toulouse physics or of a physical double-well attainer is made here.

The new load-bearing microscopic target is precise: retain a full bounded
continuous coordinate and actual lead ultraviolet modes, retune its actual
low scale, and bound H_theta from below. Uniform pointwise susceptibility
approximation and a free inverse analytic continuation are unnecessary.
