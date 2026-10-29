# Polynomial weak-bath preparation: exact source composition

29 October 2026. Working continuation, NOT accepted or frozen. This section
composes an EXISTING microscopic Gaussian-bath theorem with the new product-
phase gap. It does not invent Gaussian coarse graining. Finite reservoir,
physical layout, bath initial-state preparation and calibration are separate
gates; no hardware or quantum state is run.

Notation: H is the conditional gauged clock Hamiltonian; lambda is its fixed
data coupling. b is dimensionless inverse temperature, u is dissipative
rescaled time, and alpha is the microscopic system/bath coupling. Physical
time is u/alpha^2. The bath may weaken polynomially with n; the data penalty
and lambda are NOT increased with volume.

## 1. An explicit, Hamiltonian-independent reservoir spectrum

For each of the m=n(L-1) bare conditional-frame onsite seeds A_j, choose an
independent zero-mean thermal Gaussian bath with

    C_hat(-omega)=h_b(omega)^2.

Thus C_hat(omega)>=0 and C_hat(-omega)=exp(-b omega)C_hat(omega) for omega>0.
This is an honest thermal spectral KMS relation. A bosonic realization is
the positive-frequency band[1/2,3/2], with coupling density proportional to

    J_b(nu)=(1-exp(-b nu)) fminus(-nu)^2.

The emission weight is fminus(-nu)^2 and the absorption weight is its
exp(-b nu) partner. The spectrum depends on b and the fixed band, NOT on
the many-body eigenvectors or Bohr gaps of H. Its finite realization and
calibration are not assumed here.

Use the frozen filter compiler's integer C_* and

    A=C_*(1+ceil(b))^4 >=1.

The same fourth-derivative bounds applied to the square-root spectrum give
g0=integral|g(u)|<=4A, g1=integral|u g(u)|<=4A, and
g2=integral u^2|g(u)|<=4A. Convolution then gives the following simultaneous
global bounds for the source's independent-bath constants:

    Gamma0<=Gamma<=Gbar=16m A^2,
    Gamma0 tau0<=Gamma tau<=Mbar=32m A^2,
    K0<=K<=Kbar=64m A^2,
    Gamma0>=m, Gamma>=m, tau0,tau<=taubar=32A^2.           (1)

The lower bounds follow from C_hat(1)=1 and g_hat(1)=1 on the fixed plateau,
and Fourier L1 dominance. These constants grow polynomially, not
exponentially, in n and b. They are acquired from known scalar functions,
not an observed unknown microscopic generator.

## 2. Governing EXISTING primary theorem and its exact hypotheses

Use Scandi--Alhambra, arXiv2505.20064 / PRX16,011040(2026), corrected
renormalized version, Theorems11,13,15,17,18. The primary model assumes

    H_total=H+alpha sum_j A_j tensor B_j+H_B,

initial product rho_S tensor gamma_B, a thermal Gaussian bath satisfying
Wick, zero bath means, and finite moments(1). Bath B_j may be unbounded.
The A_j have norm1. The source explicitly requires an infinite reservoir
for finite infinite-time correlation norms. This theorem is NOT directly
a theorem for finite oscillator banks.

At its observation time

    T=sqrt(2+3Gamma0 tau0)/(2alpha Gamma0),                (2)

its exact-KMS effective generator has Gaussian-twirled rates relative to

    H*=H+alpha^2 H_LS^CG/2.

From the source's time-domain Lamb-shift formula,

    ||H_LS^CG||<=Gamma0, ||H*-H||<=alpha^2 Gbar/2.         (3)

No external Hamiltonian counterterm needs to be implemented: H* is the
effective renormalization of the autonomous microscopic model. Its
difference from the desired bare Gibbs target is explicitly charged.

The observation window(2) is a PROOF parameter; it is not a controller
knob or a scalar optimization oracle. Let R=2+3Mbar. Then

    1/(2alpha Gbar)<=T<=R/alpha.                         (4)

These elementary bounds suffice below, so no exact absolute-correlation
integrals need be experimentally measured to set a time window.

## 3. Uniform effective gap after renormalization

The bare-local-seed/positive-average proof in BARE_SEEDS_AND_AVERAGING.md
gives the all-cold parent gap g=1/16 for H. Write C=4A, so its common
Fourier L1/first-moment bounds C0,C1 are <=C. Equation(5) there and(3),(4)
give, for alpha<=1,

    ||P_T(H*)-P_T(H)||<=alpha Kgap,
    Kgap=m C^2 Gbar(8+2b+8R).                            (5)

Choose alpha<=g/(4Kgap). Ordinary Weyl/minmax then gives the exact effective
parent gap>=g/2=1/32. We do NOT require the increasingly spread Lamb term
to pass a uniform local weak-coupling norm; the global correction is small
because bath alpha is deliberately inverse-polynomial in volume.

The physical coherent drift -i[H*,rho]/alpha^2 is anti-Hermitian in the same
weighted similarity. It fixes its Gibbs state and cannot spoil the real-
part L2 contraction. If E=sum_X||H_X|| and alpha^2Gbar/2<=1, choose

    U=32[ceil(b(E+1))+Ln+ceil(log2(16/epsilon))].          (6)

Then the effective state is within epsilon/8 of sigma_H* from ANY clock
initial state. This is O(n(1+b)+log(1/epsilon)), not logarithmic mixing.

## 4. A literal polynomial microscopic error receiver

The following overpayments use the exact displayed source inequalities,
not its informal big-O abstract. Assume alpha<=1/(2b Gbar); then T>=b and
exp[b^2/(16T^2)]<=2. Using log(1+x)<=sqrt(x), the source's Theorem11
error at rescaled time U is at most alpha K11, where

    K11=2R+2Gbar U(2R+3Mbar)
                    +2Gbar(1+Mbar)(1+Gbar U).            (7)

Its Theorem13 renormalization-picture change is bounded by alpha K13:

    K13=Gbar U[4Gbar R+2Mbar+2Gbar^2 R^2
                     +4Gbar^2 Mbar R+Gbar Kbar].         (8)

This follows by inserting T<=R/alpha in each term of its Eq(105), and
overpaying all higher alpha powers by alpha. Its Theorem17 detailed-balance
correction is bounded by alpha K17:

    K17=Gbar^2 U(8taubar+2b+8Kbar).                      (9)

Here 1/T<=2alpha Gbar, the inverse-square term uses alpha<=1, and the
Gaussian exponent uses T>=b. Finally Theorem18 gives bare-state Gibbs bias
<=alpha^2 b Gamma0<=alpha b Gbar. Set

    Ktot=K11+K13+K17+b Gbar.

The explicit rational choice

    alpha<=min{1,1/(2b Gbar),g/(4Kgap),
                         epsilon/[16(1+Ktot)]}           (10)

pays all microscopic/effective/bare-Gibbs errors by epsilon/16, in addition
to the effective mixing error. Physical time U/alpha^2 is a polynomial
in n,b,1/epsilon, with large constants. No smallest Bohr spacing enters
the receiver. Every parameter is a scalar function of supplied n,b,
epsilon, native norm E and the explicit fixed filter.

These bounds are a continuum-Gaussian-bath composition. A finite-time
reservoir replacement error, imperfect bath initialization, coupling and
Hamiltonian calibration, and physical switching must each receive their
own tolerance. They are NOT contained in(10).

## 5. Remaining physical resources are not silently acquired

On the ungauged code endpoint, preserving the supplied corrected syndrome
requires the constant-support prefix pullback U_prefix^* A_j U_prefix.
It is a finite-range, generally constant-BODY system-bath coupling. This
does not establish an onsite or fully two-body preparation apparatus.

Independent finite chains attached to every source cell give a bounded-
degree graph-local reservoir. Their uniform bounded-density embedding in
physical3D is a separate question; adding a bath direction to an arbitrary
3D source cannot be declared a free physical layout. Bath vacuum/thermal
preparation, finite-precision Gaussian drives, energy/occupation budgets and
finite microscopic coefficients are also separate acquisition costs.

Nothing here is a physical experiment or a hardware-feasibility result.
The meaningful new link, subject to whole review, is that the accepted
product-phase gap can close the THERMALIZATION-TIME input of the strong
ordinary Scandi--Alhambra microscopic mechanism with inverse-polynomial
bath coupling, while leaving its actual reservoir resources visible.
