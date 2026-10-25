# Bounded motion does not bound the compact lock's physical kinetic cost

25 October 2026. This is an additional consequence of the COMPLETE live-lead
Gibbs comparison, not an effective-band moment calculation. It explains
which real resource replaces hidden linear excursion when an amplifier
uses a winding compact coordinate. The state can have bounded port
displacement and fixed physical masses, yet its actual bare translational
and rotational momentum fluctuations diverge. No heating rate, assembly
work or material implementation follows merely from this kinetic statement.

The proposed momentum limit was formed after the equilibrium/dynamical
construction. Root independently suggested the simpler W_0 comparison
below; I reconstructed it before using it. It avoids trying to treat a
noncommuting momentum correction as an operator-Lipschitz perturbation.

## 1. Physical versus helical momentum

Keep the COMPACT fixed-I, fixed-B_0 family of
LIVE_CONTACT_EQUILIBRIUM.md, with g tending to infinity,

    B=B_0+Ig^2, R=B/B_0, a=gI/B, beta=sB,
    k=kappa/B, b=(1/4+epsilon)log R, epsilon>0.

The stronger b=R(log R)^2 dynamical family also satisfies every limit
used here. The actual local mechanical kinetic energy is

    T_bare=p_Y^2/(2B_0)+L_phi^2/(2I).

After psi=phi-gY the helical canonical momentum is

    P=p_Y+gL_phi, L_phi=hbar N, N=-i partial_psi.       (1)

Thus P is NOT the physical relative bare momentum. Equating their Gibbs
variances would miss the main kinetic cost.

## 2. A full-state product comparison for bounded measurements

Let rho_G be the complete loaded Gaussian reference, including all its
lead and possible bound modes. The governing comparison uses

    W Phi=Phi exp[i(aP/hbar)chi_b]psi_b,
    psi_b=exp(bcos psi)/sqrt[2pi I_0(2b)].

Define the simpler isometry W_0 Phi=Phi psi_b in the SAME helical
representation. The elementary pointwise phase bound gives

    ||(W-W_0)rho_G^(1/2)||_HS^2
       <= (a^2/hbar^2)<P^2>_G v_chi =:eta_0^2,       (2)
    v_chi<=C_chi/b, <P^2>_G=O(1+log R).

Hence eta_0 tends to zero. Purify rho_G once and use the two isometries
on that purification: trace distance in the half-norm convention is at
most the Hilbert-space vector distance. Together with the accepted Gibbs
relative-entropy comparison this yields, at finite regulator and then on
the local thermodynamic limit,

    (1/2)||rho_full-rho_G tensor |psi_b><psi_b|||_1
                   <=sqrt(epsilon_G/2)+eta_0 ->0.      (3)

For infinite leads (3) means the same bound on local bounded measurement
statistics, not a formal global trace-class density matrix. It applies
also to B-dependent bounded functions of the local momenta. It does NOT
by itself transfer any unbounded second moment.

The phase in W is essential to the energy and dynamical intertwining
despite (2): small state norm does not bound the error of an unbounded
generator. Dropping that phase inside the Hamiltonian is not justified.

## 3. Exact normal characteristic function and the joint limit

The exact characteristic function of N in psi_b is

    <exp(it N/sqrt b)>
       = I_0[2b cos(t/(2sqrt b))]/I_0(2b)
       -> exp(-t^2/4).                                (4)

The identity is just the periodic overlap of psi_b with its translated
copy. Its limit follows from the elementary Laplace asymptotic
I_0(x)~exp(x)/sqrt(2pi x). For this application that asymptotic can be
proved directly by setting u=sqrt(b)psi in the defining integral; the
global bound cos psi<=1-2psi^2/pi^2 supplies an integrable Gaussian
majorant. Also 2b[cos(t/(2sqrt b))-1]->-t^2/4.

Under the product state in (3), P and N commute and are independent.
The P marginal is centered Gaussian. Define the ACTUAL physical scaled
momenta

    X_B=p_Y/(g hbar sqrt b), Z_B=L_phi/(hbar sqrt b).

By (1), their joint characteristic function is exactly

    exp[-t^2<P^2>_G/(2g^2 hbar^2 b)]
       * I_0[2b cos((u-t)/(2sqrt b))]/I_0(2b)
                       ->exp[-(u-t)^2/4].             (5)

P and L_phi also commute in the actual model, so this is an ordinary
joint spectral measurement. Equation(3) transfers (5), a bounded
observable at every B, to the TRUE full Gibbs state. Consequently

    (X_B,Z_B) converges in distribution to (-G,G),
                 G a real centered normal variable of variance1/2. (6)

This is a degenerate joint limit. Large opposite bare momenta cancel in
the helical quantity P; the growing effective inertia is not an increase
in the actual translating mass.

## 4. Genuine bare kinetic lower bounds, with all modes retained

Apply (6) first to min(x^2,K) and then let K increase. Positivity gives
the valid lower semicontinuity statements

    liminf <p_Y^2>_full/(g^2 hbar^2 b)>=1/2,
    liminf <L_phi^2>_full/(hbar^2 b)>=1/2.             (7)

There is NO assertion of second-moment convergence. A vanishing trace
distance could hide additional kinetic energy in rare high-momentum
components, which can only increase these lower bounds. Time-reversal
symmetry makes the momentum means zero whenever their moments exist.
All finite-volume states have these moments; a divergent local moment
in a limit is allowed as +infinity and does not evade (7).

Since E_R=hbar^2 B/(2B_0 I) and g^2 I/B tends to1,

    liminf <T_bare>_full/(E_R b)>=1/2.                (8)

At the optimal-order equilibrium lock b~log R, the translational kinetic
cost alone is Omega(R log R). The physical relative RMS velocity obeys

    sqrt(<dot Y^2>) >= (1-o(1))g hbar sqrt(b/2)/B_0,
    dot Y=p_Y/B_0,                                   (9)

so it grows at least as sqrt(R log R). The rotor angular RMS velocity
grows at least as sqrt(log R) at fixed I. For the stronger sufficient
dynamical choice b=R(log R)^2, these lower orders become R^2 log^2 R
for bare translational energy, R log R for relative RMS velocity and
sqrt(R)log R for angular RMS velocity.

These are quantum equilibrium fluctuations, not a claim of dissipated
heat per operation. The bounded Cartesian orbit of a rotor does not
bound its winding momentum. A fixed apparatus with a genuine local
kinetic/momentum, elastic-bandwidth or rigidity ceiling cannot support
this unbounded family. Assigning a particular ceiling to a real material
still requires that material's actual dynamics. No universal work cost
is inferred without specifying the initial state, force generator and
assembly/control energy reference.

## 5. The canonical oscillator strength is not missing

The full continuous-coordinate Hamiltonian, with the actual lead contact,
satisfies exactly on its natural core

    [Y,[H_full,Y]]=hbar^2/B_0.

Thus its positive-frequency Kubo first moment is the actual bare-mass
sum rule

    int_0^infinity omega chi_Y''(omega)domega=pi/(2B_0). (10)

For any fixed scaled thermal window 0<=Bomega<=z_*, the positive Lehmann
measure and the uniform full port-variance bound instead give

    int_0^(z_*/B) omega chi_Y''(omega)domega
             <=pi z_* Var(Y)/(hbar B)->0.             (11)

The canonical sum-rule weight must remain outside every fixed scaled
thermal window. The large low-frequency inertance therefore coexists
with the fixed bare mass by redistributing response strength to other
frequencies. Equations(7)--(9) expose the associated physical kinetic
resource in this actual all-mode construction. They do not locate every
piece of the residual spectrum or replace the inclusive-current contract.

The new conclusion is a resource boundary for the literal compact lock:
bounded port range and bounded physical mass do not make inertial
amplification free. Here the escape from growing linear excursion pays
growing locking, recoil and actual kinetic fluctuations. Finite material
geometry and preparation remain to be acquired; the broader fixed-control
or all-passive-implementation problem is not settled by this family.
