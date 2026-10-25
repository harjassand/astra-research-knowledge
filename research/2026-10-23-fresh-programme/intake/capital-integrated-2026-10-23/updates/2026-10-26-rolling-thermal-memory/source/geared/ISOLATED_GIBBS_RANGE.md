# Full isolated Gibbs motion of the compact amplifier

25 October 2026. Owned thermal extension of the compact canonical mechanism.
The root independently supplied the isolated spring-ground variational
bound in ROOT_ISOLATED_SPRING_GROUND_VARIANCE.md. I reconstruct its trial
below and extend it to the TRUE finite-temperature Gibbs state using an
all-normal-mode heat-trace estimate. This is not an effective-mass Gibbs
ansatz, a small-leakage moment estimate or a live-lead result.

All initial material/registry/rigid-body limitations remain those of
COMPACT_INERTIAL_AMPLIFIER.md. The finite response preparation is a DIFFERENT
prepared ensemble; it is not silently identified with this Gibbs state.

## 1. Literal full Hamiltonian and its positive energy shift

Add a positive ordinary pair spring to the complete isolated primitive:

    H_k=p_Y^2/(2B_0)+L_phi^2/(2I)+V_b(phi-gY)+(k/2)Y^2,
    k=kappa/B, kappa>0,
    B=B_0+Ig^2, E_R=hbar^2 B/(2B_0 I).

Y is noncompact, phi is compact, and EVERY normal rotor band is retained.
The spring confines the relative coordinate; the common free translation
is removed. The resulting relative Hamiltonian has compact resolvent and
a trace-class Gibbs exponential for every beta>0.

In the helical representation P is conjugate to Y, and the free relative
Hamiltonian is multiplication by P^2/(2B)+h_b(q(P)). Diamagnetism gives
h_b(q)>=E_R b at EVERY q as an operator lower bound. Consequently

    A:=H_k-E_R b>=P^2/(2B)+(k/2)Y^2>=0.               (1)

In particular the true full Gibbs second moment satisfies
k<Y^2>_beta/2<=<A>_beta. This is an ENERGY bound, not a band-population
argument. The exact symmetry(Y,phi)->(-Y,-phi) makes the Gibbs mean Y zero.

## 2. The ground trial has uniformly bounded shifted energy times B

Choose the normalized cosine momentum packet F on |P|<=P_* from the
preparation operation, and use the actual ground vector psi_b,q(P) at each
momentum. On its certified flux window the derivative bound gives

    Q_b=4pi^4(gI/B)^2(b+q_*^2),
    hbar^2 int |F|^2||partial_P psi_b,q||^2<=Q_b.

The real Fourier gauge has zero Berry connection, so the spring's trial
second moment is the sum of that term and hbar^2 int|F'|^2. The global
band bracket gives the variational upper bound

    E_g-E_R b<=C_b/B,                                 (2)
    C_b=1/2{(1+zeta)P_*^2(1/3-2/pi^2)
                    +kappa[hbar^2 pi^2/(4P_*^2)+Q_b]},
    zeta=(B/B_0-1)f_b.

This is the root's complete ground-state trial, independently reconstructed.
For fixed B_0,I,P_*, b=(1/4+epsilon)log(B/B_0), C_b remains bounded because
zeta->0 and Q_b->0. No high normal band has been removed from the actual
operator. The trial need only be an allowed variational state.

Define Z'(beta)=Tr exp(-beta A). Equation(2) immediately gives

    Z'(beta)>=exp(-beta C_b/B).                        (3)

## 3. All normal bands have a controlled shifted heat trace

Put Z_n'(u,q)=Tr_(S^1) exp[-u(h_b(q)-E_R b)]. The magnetic heat-kernel
diamagnetic inequality gives

    Z_n'(u,q)<=Z_n'(u,0) for every real q.             (4)

For this scalar circle operator it follows directly from the Brownian-
loop representation: each winding sector has a nonnegative real-potential
weight, while the constant flux contributes a unit-modulus phase. Taking
the absolute value bounds its trace by the zero-flux trace. This controls
ALL q, not just the small window used by the ground trial.

At zero flux the exact normal gap is at least G_n=2E_R/pi^2. Also
h_b(0)>=E_R N^2 because V_b>=0. Minmax (not a false operator-monotonicity
claim for the exponential) then gives

    Tr exp[-(h_b(0)-E_Rb)/E_R]
                         <=e^b sum_(n in Z)exp(-n^2)<3e^b.

For u E_R>=1, separate the ground eigenvalue0 and apply the gap to every
excited eigenvalue. This yields the explicit all-mode bound

    Z_n'(u,0)<=1+3 exp[b-2(u E_R-1)/pi^2].             (5)

Thus the enormous normal ground-energy reference has been subtracted
EXACTLY, with no spurious normal-mode degeneracy or free high-frequency
entropy. Every actual compact-rotor excitation remains in(5).

## 4. A finite partition bound for the full nonseparable spring problem

Use Golden-Thompson for the semibounded form sum

    A=(k/2)Y^2+{P^2/(2B)+h_b(q(P))-E_Rb}.

Both braces and the spring term are positive forms. The relative P heat
kernel of exp[-u kY^2/2] has constant diagonal
(2pi u k hbar^2)^-1/2. The other exponential is multiplication in P.
Equation(4) therefore proves

    Z'(u)<=sqrt(B/k)/(u hbar) Z_n'(u,0).               (6)

This is the usual trace Golden-Thompson inequality, extended by positive
form approximation; its right side is finite by the explicitly computed
heat-kernel integral. It is not an assumption that P commutes with Y or
that the spring preserves a normal band.

If

    beta E_R>=2+pi^2(b+log3),                          (7)

then (5) at u=beta/2 is at most2. With k=kappa/B, (6) becomes

    Z'(beta/2)<=4B/(beta hbar sqrt(kappa)).             (8)

## 5. True finite-temperature position motion is uniformly bounded

Convexity of log Z' and A>=0 imply

    <A>_beta<= (2/beta)log[Z'(beta/2)/Z'(beta)].

Combine(3),(8), then use(1). Write the dimensionless slow-temperature
ratio tau=beta hbar sqrt(kappa)/B. A convenient positive bound is

    Var_beta(Y)=<Y^2>_beta
       <=4C_b/kappa
          +[4hbar/(tau sqrt(kappa))]log_+(4/tau).       (9)

For EVERY fixed tau in(0,infinity), the compact fixed-I, large-g family
satisfies(7) eventually: beta is order B, E_R is order B, while b is only
logarithmic. Since C_b is bounded, (9) proves a UNIFORM full Gibbs port-
variance cap at temperatures theta=sqrt(kappa)/(tau B).

All nonseparable spring/rotor states, normal bands, thermal excitations
and zero-point contributions are included. The inference uses neither
an isolated two-state truncation nor a tiny leakage estimate. It is
stronger than the earlier isolated ground-motion conclusion and remains
weaker than a live-contact covariance/heat theorem.

## 6. One exact finite resource point, with the very large costs visible

Take hbar=B_0=I=kappa=P_*=tau=1, g=1000,b=6. Then B=1,000,001,
E_R=500,000.5, beta=B, k=1/B and theta=1/B. The exact positive Bessel
enclosure from check_compact_amplifier.py verifies zeta<1/100. Using only
pi^2<10 and the earlier flux-window condition gives C_b<3/2. Criterion(7)
is certified by beta E_R>82, using log3<2. Finally log4<3/2, so(9) gives

    TRUE full isolated Gibbs Var(Y)<12.               (10)

The associated normal-band response has B_eff/B>99/100, but its barrier
upper bound is24,000,024 and its normal ground energy is3,000,003 in these
same units. They are actual model resources, not erased constants when
describing assembly/preparation. A finite point in this Hamiltonian is
not a claim that available material produces that helical registry.

The rational check_isolated_gibbs_range.py verifies these conservative
finite constants. It does not simulate a live heat experiment or supply
the actual Gibbs state. The proof of(9), not a finite truncation or a
temperature sweep, establishes the all-mode thermal statement.

## 7. Remaining physical conjunction

The finite response operation prepares a controlled packet; this note
characterizes a true Gibbs ensemble of the spring-confined isolated
device. Preparing that ensemble in finite time is another operation.
Coupling the live leads adds their full self-energy, reservoir noise and
normal-band dressing. Neither the Gibbs bound nor the packet response
proves the desired contact heat deficit or bounded loaded Y variance.

Real spring mass/modes, rotor elastic bandwidth, finite pitch/barrier and
force capacities, initial information/work and readout remain charged.
This is a positive finite canonical construction with a proved isolated
thermal range, at a visible large-resource cost; it is not a manufactured
passive thermal device or practical advantage claim.
