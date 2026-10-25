# Equilibrium comparison of the complete helical contact and live harmonic leads

25 October 2026. Owned continuation of the compact amplifier. This is a
new load-bearing representation: after the helical change and Fourier
transformation of all mechanical coordinates, the normal coupling is an
abelian magnetic connection. Diamagnetism and an explicit isometry then
compare the COMPLETE coupled Gibbs state to a loaded Gaussian reference.
The result includes all lead and rotor modes. No low-band Gibbs ansatz,
instantaneous thermal preparation or heat-current inference is made.

The actual hardware/material limitations remain exactly those of the
preceding compact-lock construction. Finite volume is an infrared
regulator, not a physical equilibration clock.

## 1. Literal contact and Gaussian reference

The actual local kinetic energy is the same counted pair of terminal
translating groups plus the balanced rotor. In common/relative coordinates
it is P_U^2/(2M_tot)+p_Y^2/(2B_0)+L_phi^2/(2I), B_0=M_tot/4. The potential
is V_b(phi-gY)+kY^2/2 plus the two actual terminal-to-Rubin-lead springs.
All lead atoms and springs are retained, with fixed Z,m_L,k_L,Omega.

Set B=B_0+Ig^2, R=B/B_0, a=gI/B and E_R=hbar^2 B/(2B_0 I). In the helical
representation its relative kinetic term is P^2/(2B)+h_b(q(P)),
q(P)=aP/hbar. The exact normal zero-flux state is psi_b and its energy E_R b.

The comparison H_G is the ACTUAL loaded harmonic two-port obtained by
replacing that relative kinetic term by P^2/(2B), dropping only the normal
rotor Hilbert space. It keeps the common mass, spring k, both full chains,
their reactive endpoint terms and contact coupling. It is an auxiliary
Gaussian reference, not another uncounted physical mass.

First use finite chains with weak far-end pinning so that all Gibbs traces
exist. Then take their standard local thermodynamic limit on relative
observables. The constants below depend on the actual loaded reference,
not an unexamined infinite density-matrix trace.

## 2. Exact upper partition bound by full phase-space diamagnetism

Fourier transform Y,U and every lead coordinate to their momenta, but
retain the normal angle psi. The full Hamiltonian is a magnetic
Schrodinger operator of the form

    -hbar^2/2 nabla_p^T K_springs nabla_p
       +P^2/(2B)+P_U^2/(2M_tot)+sum_j p_j^2/(2m_L)
       +E_R(-i partial_psi-q(P))^2+V_b(psi).           (1)

The positive pinning makes the constant spring-diffusion matrix positive.
Without pinning it is obtained by the same form limit. The sole vector
potential is in the psi direction, with value q(P). The scalar potential
is unchanged when that connection is removed. Its zero-connection
operator is EXACTLY H_G+h_b(0).

Magnetic heat-kernel diamagnetism therefore gives the all-mode trace bound

    Z_full(beta)<=Z_G(beta) exp(-beta E_R b) Z_n'(beta),             (2)
    Z_n'(beta)=Tr exp[-beta(h_b(0)-E_R b)].

One can see the required positivity directly from the Trotter/Brownian
loop formula in the momentum/angle variables: the vector potential adds
a unit-modulus phase to every path. Removing that phase leaves the
positive scalar heat kernel. This argument uses the COMPLETE connection,
not a factorwise trace inequality that assumes the lead variables commute
with the junction. Finite Fourier/volume form approximations justify the
unbounded-operator passage. There is no intrinsic band-count substitution.

The previous normal heat-trace proof supplies

    Z_n'(beta)<=1+3 exp[b-2(beta E_R-1)/pi^2]
                                             for beta E_R>=1.      (3)

## 3. An explicit globally defined comparison isometry

Put rho_b=psi_b^2 and

    A_b(psi)=exp(-2b cos psi)/I_0(2b),
    chi_b'=1-A_b, chi_b(0)=0.

A_b is even and int_0^pi A_b=pi. Thus chi_b is a smooth periodic odd
function, chi_b(+-pi)=0. On[0,pi], A_b increases, so chi_b is concave,
0<=chi_b(psi)<=psi. Consequently |chi_b|<=|psi| on[-pi,pi]. Its normal
mean is zero.

For b>=1, cos psi<=1-2psi^2/pi^2 and the earlier positive normalization
bound yield

    v_chi:=<chi_b^2>_(rho_b)<=C_chi/b,
    C_chi=e pi^(7/2)/32.                              (4)

Indeed bound the numerator by the whole-line Gaussian second moment and
use int exp(2bcos)>=2exp(2b-1)/sqrt b. This is a shrinking physical
coordinate correction, not the coarse gap-based O(b) metric bound.

Define an isometry from the WHOLE Gaussian support-plus-leads Hilbert space:

    (W Phi)(P,other;psi)=Phi(P,other)
                              exp[iq(P)chi_b(psi)]psi_b(psi).      (5)

It is defined for every P, so no momentum-tail projection is needed.
It preserves the nonzero spectrum and entropy of any Gaussian density
operator. The phase-corrector identity gives exactly

    W^dagger H_full W
       =H_G+E_Rb+zeta P^2/(2B)+(K_YY/2)Q_chi,
    zeta=(R-1)f_b, f_b=I_0(2b)^-2,
    Q_chi=a^2 v_chi, K_YY=k+k_L/2.                   (6)

Here K_YY is the coefficient of Y^2 in the ACTUAL full spring form:
the two terminal-lead springs add k_L/2. Cross terms with other coordinates
have no correction because <chi_b>=0. This exact identity follows either
by differentiating(5) or by conditional unitary translation:
W^dagger Y W=Y, W^dagger Y^2 W=Y^2+Q_chi. The normal phase energy is
E_R f_b q(P)^2 for every momentum.

## 4. Matched lower free energy and a full-state comparison

Let rho_G be the true Gibbs state of H_G. Use W rho_G W^dagger as a trial
state in the Gibbs variational principle; it has exactly entropy S(rho_G).
Define

    dE=zeta<P^2>_G/(2B)+(K_YY/2)Q_chi.

Then

    Z_full>=exp[-beta(E_Rb+dE)] Z_G.                 (7)

Combining with(2) also gives the exact finite-regulator relative entropy

    D(W rho_G W^dagger ||rho_full)
          <=epsilon_G:=beta dE+log Z_n'(beta).         (8)

Thus any common bounded final measurement differs between these two
states in total variation by at most sqrt(epsilon_G/2). This is an
equilibrium state comparison, not a comparison of their Hamiltonian
dynamics. In the infinite-lead limit use bounded relative local observables
and the finite-volume inequalities, not a formal global density matrix.

## 5. The actual finite-band reference has only logarithmic momentum cost

Take k=kappa/B and beta=s B with fixed positive s,kappa. In the infinite
Rubin reference the exact Euclidean odd susceptibility is

    c_G(nu)=[k+Bnu^2+s_E(nu)/2]^-1,
    0<=s_E(nu)<=min(Znu,k_L).

The full Gaussian normal-mode/Matsubara formula, including bound modes, is

    <P^2>_G=(B/beta){1+2 sum_(n>=1)
             [k+s_E(nu_n)/2]/[k+Bnu_n^2+s_E(nu_n)/2]},
    nu_n=2pi n/(beta hbar)=d n/B, d=2pi/(s hbar).      (9)

It follows directly from the finite-system normal-mode coth identity
before passing to the chain limit; it is not a propagating-only integral.
Use

    ratio_n<=kappa/(d^2 n^2)
                   +min[Z/(2d n), k_L B/(2d^2 n^2)].

Splitting at N=ceil(Bk_L/(Zd)) gives

    <P^2>_G <=(1/s){1+kappa pi^2/(3d^2)
                                       +(Z/d)(H_N+1)}
             =O(1+log R).                             (10)

At any fixed B the finite-chain expressions converge to(9), by the
explicit Euclidean lead recursion and the summable high-n bound. The
thermodynamic limit is taken before the gain limit; no finite clock is
deduced from it.

Now use the COMPACT fixed-I, increasing-g family, b=(1/4+epsilon)log R.
Then beta E_R is order R^2, zeta log R->0 and
beta Q_chi=O(1/b). Equations(3),(8),(10) prove

    epsilon_G ->0.                                   (11)

In particular the nonlinear contact's full equilibrium state approaches
the explicitly dressed loaded Gaussian reference on bounded relative
observables. Its normal fast ground energy and huge locking resources
have not been omitted. This conclusion is not asserted for the different
large-I/fixed-g route: its Q_chi has a different scaling.

## 6. Full loaded port variance, without a trace-distance moment fallacy

The Gaussian position variance has the elementary uniform bound

    V_G(k)<=1/(s kappa)+pi^2/(3s d^2),                 (12)

from its positive Matsubara sum and c_G(nu)<=1/(Bnu^2) for n>=1.
To obtain a TRUE upper bound for the nonlinear state's unbounded Y^2,
use partition functions at k and k'=(1-r)k,0<r<1. Convexity in k gives

    V_full(k)<=[2/(beta r k)]
                         log[Z_full(k')/Z_full(k)].

Apply(2) at k' and(7) at k. Gaussian variance decreases with its positive
spring constant, so integrating its free-energy derivative yields

    V_full(k)<=V_G(k')+2epsilon_G(k)/(beta r k).        (13)

For example r=1/2 and beta k=s kappa fixed give a uniform full loaded
variance cap using(11)-(12). It is not inferred from a small population
outside a band or a small trace distance.

More precisely the Gaussian Matsubara variance converges as B->infinity,
by its summable1/n^2 domination. Letting r down to0 AFTER that limit gives
a limsup bounded by the limiting V_G(k). For the reverse bound, (8)
compares bounded truncated position squares. The trial Y distribution is
the Gaussian reference convolved with the bounded independent shift
-a chi_b; its variance is V_G+Q_chi and its distribution converges to the
same Gaussian limit. Fatou/truncation then gives the matching liminf.
Therefore V_full has that same finite limiting variance. This also
establishes uniform integrability of Y^2 in this equilibrium family, a
fact not supplied by trace distance alone.

## 7. Exact scope of the closure

This closes LIVE-LEAD EQUILIBRIUM port range for a complete continuous
canonical compact-rotor model, at the paid optimal-order locking scale.
It retains the literal spring, all normal and lead modes, finite lead
band and actual total translating mass. Finite material rigidity/pitch/
barrier capacities remain unacquired implementation data.

Neither (8) nor free-energy closeness identifies the real-time evolution
of the two different Hamiltonians. A thermal transmission deficit still
needs an actual dynamical/intertwining or equilibrium spectral argument
and the inclusive-current/scattering contract. The prepared packet
operation and this equilibrium theorem do not themselves supply finite
Gibbs/NESS preparation. No practical or novelty claim is inferred.
