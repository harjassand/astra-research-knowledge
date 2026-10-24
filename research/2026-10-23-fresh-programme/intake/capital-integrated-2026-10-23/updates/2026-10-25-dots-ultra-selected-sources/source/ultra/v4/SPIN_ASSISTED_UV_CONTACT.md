# A canonical massive port with an explicit internal spin

25 October 2026. Owned next construction. The pure continuous-double-well
projection problem remains open. This construction changes the actual
operation: an explicit internal spin controls the two structural sectors,
while the mechanical port remains a full, untruncated canonical oscillator.
It is a conventional spin--oscillator/reaction-coordinate Hamiltonian, not
a claim to discover that coupling. The point is to expose exactly which
resource removes the harmonic motion law, without assigning a spin-only
Hilbert space the canonical port's mass or commutator sum rule.

## 1. Full mechanical Hamiltonian and actual new resource

Keep the equal endpoint masses M/2, identical ideal leads Z, actual port
planes, U and Y of INCLUSIVE_NOISE_TRANSPORT.md. Add ONE genuine spin-1/2
degree of freedom and use the translation-invariant odd Hamiltonian

    H_odd = P_Y^2/(2B) + (k_0/2)(Y-d sigma_z)^2
                         -(hbar Delta_0/2)sigma_x + H_leads+coupling,
    B=M/4, eta=Z/2, k_0>0, d>0.                             (1)

The square includes the constant k_0 d^2/2; the force coupling is
-lambda Y sigma_z with lambda=k_0 d. A literal internal spin is an additional
physical resource, rather than the projection of Y onto a doublet. Its host
mass is part of M. A spin-dependent equal/opposite force dipole and a
transverse spin splitting must actually be supplied. No material realization
of that conjunction has been acquired. A passive Hamiltonian model need not
include a hidden spin relaxation bath; adding one would change the two-port
problem and invalidate a two-port-only current assertion.

For every finite Delta_0 the Hamiltonian is bounded below: the mechanical
square is nonnegative and the spin term is bounded. At Delta_0=0, sigma_z
is EXACTLY conserved by the full system and all lead modes. Consequently no
elimination of high mechanical modes can create a spin flip independent of
Delta_0. This is an explicit selection rule. A bare spatial double well did
not supply such a finite-dimensional conserved sector before a projection.

The common U sector is unchanged. The odd input/output boundary derivation
and KMS current proof require only a separated interacting odd subsystem;
they therefore apply to (1), with the full response of the canonical Y.

## 2. Exact Gaussian elimination and total quantum range

For the spin held absent, the FULL lead-dressed oscillator susceptibility is

    chi_0(i nu)=1/[k_0+B nu^2+eta |nu|],
    chi_0^R(omega)=1/[k_0-B omega^2-i eta omega].             (2)

The mechanical Hilbert space is infinite dimensional and is not truncated.
Let C_A,n be the imaginary-time Fourier transform of the connected
correlation of A over 0<=tau<beta hbar, nu_n=2pi n/(beta hbar). Gaussian
integration, with an arbitrary source for Y, is exact and gives

    C_Y,n = hbar chi_0(i nu_n)
               +lambda^2 chi_0(i nu_n)^2 C_sigma_z,n.        (3)

This uses the FULL interacting spin correlation. No weak spin coupling,
Born, Markov, rotating-wave or two-state mechanical approximation is used.
The connected Matsubara coefficients C_sigma_z,n are nonnegative by their
Lehmann representation. Since k_0 chi_0(i nu)<=1,

    Var_T(Y) <= V_0(T)+d^2 Var_T(sigma_z) <= V_0(T)+d^2,     (4)
    V_0(T)=k_B T sum_n chi_0(i nu_n).

The bare mass B>0 makes V_0 finite including zero point motion. For T<=T_0,
V_0(T)<=V_0(T_0), so this is a UNIFORM total-motion cap for the entire
family Delta_0(T), independent of how small its actual transition scale is.
It counts every high oscillator and lead frequency. The full canonical
f-sum remains int omega chi_Y'' d omega=pi/(2B), because only P_Y^2 depends
on its momentum. It has not been replaced by a finite-spin f-sum.

An explicit fixed-resource choice is critical damping:

    a=Z/M, k_0=Z^2/(4M)=B a^2, eta=2Ba.

Then chi_0(i nu)=1/[B(nu+a)^2] for nu>=0 and

    V_0(0)=4hbar/(pi Z),
    V_0(T)-V_0(0)<=hbar theta/k_0.

At d^2=pi hbar/(2Z), the exact full-coordinate bound is therefore

    Var_T(Y) <= (pi/2+4/pi)hbar/Z+hbar theta/k_0.             (5)

Neither increasing participating mechanical inertia nor an uncounted
displacement amplification appears in (4)--(5). The new bounded quantum
sector is paid explicitly in (1).

## 3. Exact bath seen by the spin, including ultraviolet completion

Diagonalize the oscillator plus odd lead, not the interacting spin. If
Y=sum_j q_j(b_j+b_j^dagger), then
chi_0''=(pi/hbar)sum_j q_j^2 delta(omega-omega_j). The standard spin-boson
coupling (sigma_z/2)sum_j l_j(b_j+b_j^dagger) has l_j=-2lambda q_j. Hence
the EXACT spectral density is

    J_SB(omega)=pi sum_j l_j^2 delta(omega-omega_j)
               =4hbar lambda^2 chi_0''(omega)
               =4hbar k_0^2 d^2 eta omega /
                    [(k_0-Bomega^2)^2+eta^2omega^2].          (6)

At small omega it is 2pi alpha hbar^2 omega with

    alpha=2eta d^2/(pi hbar)=Zd^2/(pi hbar).                 (7)

At high omega it falls as omega^-3. Thus the spin's cutoff is supplied by
the actual finite-mass mechanical oscillator, not a discarded high-frequency
spin-only spectrum. In the critical-damping choice,

    J_SB=2pi alpha hbar^2 omega/[1+(omega/a)^2]^2.            (8)

The reaction-coordinate mapping is exact; its use is conventional. For
example Thorwart, Paladino & Grifoni, arXiv:cond-mat/0310140v1, Sec.2,
Eqs.(1)--(5), explicitly relates a two-state system plus a damped oscillator
to this class of structured spectral densities. I read those primary
equations. Their QUAPI initial preparations and weak-residual-damping
numerics are not being imported as equilibrium or Toulouse proofs here.

Primary: https://arxiv.org/html/cond-mat/0310140v1

## 4. Exact transfer from a spin scaling correlation to the actual port

Equation (3) also avoids an uncontrolled real-frequency approximation. Put
A_n=k_0 chi_0(i nu_n). These are the Fourier coefficients of a nonnegative
normalized kernel on the imaginary-time circle. Positivity follows, for
example, from

    k_0/(k_0+Bnu^2+eta|nu|)
     =int_0^infinity k_0 exp(-k_0 t)
                    exp[-t(Bnu^2+eta|nu|)]dt:

the last factor is the characteristic function of a Brownian plus Cauchy
increment. The periodized kernel is a probability distribution. A_n^2 is
its twofold convolution. On the SCALED circle s=theta tau, for every fixed
integer n, A_n->1 as theta->0. The kernels therefore tend weakly to a delta
at s=0.

Suppose the actual spin correlations, after a retuning of Delta_0, obey

    C_sigma_z,theta(s)->C_*(s),  0<s<1,                     (9)

where C_* is continuous there. Bounded spin variance gives uniform local
equicontinuity of these correlations: use their positive Lehmann measures
and the bounded derivative of K_s(z) on every compact subinterval of (0,1).
Thus convolution with the preceding approximate identity preserves (9).
The free oscillator correlation tends to zero at any fixed 0<s<1: apply
dominated convergence to its fixed spectral function, bounded by its finite
variance at T_0. Consequently the ACTUAL full coordinate obeys

    C_Y,theta(s)->d^2 C_*(s),  0<s<1.                       (10)

Combined with (4) and EUCLIDEAN_HEAT_CERTIFICATE.md, this transfers either
the full limiting heat functional or the three-correlation lower bound to
the massive physical port. This part is exact. No high oscillator states
were projected out. The only remaining effective-theory input in an
application is the actual spin scaling premise (9).

## 5. Toulouse operation: exact model versus scaling input

Take d^2=pi hbar/(2Z), giving alpha=1/2. In the conventional Ohmic scaling
limit, the spin is the noninteracting resonant level with width Gamma.
Retuning Gamma/(hbar theta)=1 gives the benchmark correlation in
EUCLIDEAN_HEAT_CERTIFICATE.md and a strictly positive limiting inclusive
deficit; Var_T(Y) is bounded by (5). This would be a complete asymptotic
counterfamily to extending the positive-HARMONIC logarithmic range theorem
to the explicit spin-assisted Hamiltonians (1).

The structured density (8) is NOT identically the ideal wide-band Toulouse
Hamiltonian at finite parameters. A low-frequency coefficient alpha=1/2
alone is not a proof of (9). A rigorous transfer still requires the
conventional scaling/irrelevance statement for this fixed cutoff shape,
or a direct certified lower bound on the three actual spin correlations.
No such finite-parameter certification has been produced in this note.
The exact UV embedding and exact range bound remove the continuous-coordinate
TRUNCATION issue; they do not silently solve this remaining scaling issue.

The bare scale can be specified without a mysterious cutoff. In the
polaron representation at zero temperature, the spin-flip vertex has

    Q(tau)=2alpha int_0^infinity [1-exp(-omega tau)]
                       d omega/[omega(1+(omega/a)^2)^2].

For alpha=1/2,

    Q(tau)=log(a tau)+gamma_E-1/2+o(1),
    omega_*=a exp(gamma_E-1/2).

The constant follows from
int_0^infinity [(1+x^2)^-2-1_(x<1)]dx/x=-1/2. Matching the long-time
vertex 1/(omega_* tau) to the normalized chiral fermion gives the usual
Toulouse leading width Gamma/hbar=pi Delta_0^2/(4omega_*). Thus the
candidate retuning is Delta_0~2sqrt(omega_* theta/pi), with actual width
retuning or a quantified error still required at finite cutoff. At
Delta_0=0 sector conservation is exact, so no Delta_0-independent transition
error is permitted. This is the useful structural difference from a naive
absolute-error projection of a spatial double well.

## 6. Physical and conventional boundary

The operation pays a bounded internal spin, spin-dependent force lambda,
fixed k_0, fixed M and Z, and an increasingly small transverse splitting.
Unbiased symmetry is explicit: Y->-Y with sigma_z->-sigma_z. A residual
longitudinal bias is not harmless when the target scale tends to zero.
No active bias-cancellation precision, hidden spin bath, free spectroscopy,
free equilibration or finite-time tunnelling access is assumed. The actual
thermal relaxation time of the target scaling state is of order 1/theta;
the stationary limit in the current theorem must precede the cold limit.

The strongest conventional explanation is precisely a spin-boson impurity
embedded through a damped oscillator, with the inclusive series-response
kernel already present in Josephson heat theory. There is no claimed device
advantage or new generic spin-boson mechanism. The scientific gain is an
explicit all-mode canonical-coordinate embedding, its exact total-variance
resource law, and a finite equilibrium observable criterion for deciding
whether its actual low-energy operation realizes a cold heat deficit.
