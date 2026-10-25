# A paid canonical route from compact amplification to live-contact response

25 October 2026. This continues LIVE_CONTACT_EQUILIBRIUM.md. The new step
is an EXACT intertwining defect on an explicit phase-corrected isometry.
A stronger, explicitly paid locking scale makes its full equilibrium
real-time port correlations converge on the thermal clock. No dynamics
is inferred from free-energy closeness alone.

This is a complete canonical-model construction. Assigning its diverging
barrier, force, pitch and normal bandwidth to an actual material remains
unacquired. The heat statement at the end uses the already governing
inclusive KMS/scattering current contract; that existence/preparation
contract is not proved by these estimates.

## 1. Exact defect, including the physical lead contact

Use H_full,H_G,W, a=gI/B, q(P)=aP/hbar from the equilibrium construction.
Let psi_b be the zero-flux normal state and define

    A_b=exp(-2b cos psi)/I_0(2b), chi_b'=1-A_b,
    v_chi=<chi_b^2><=C_chi/b, |chi_b|<=pi.

The normal identity is

    {N,A_b}psi_b=0.                                  (1)

Indeed A_b psi_b^2 is constant. Conjugating by exp[iq(P)chi_b] changes
N-q into N-qA_b and Y into Y-a chi_b. Let F_G=partial_Y V_springs be the
actual loaded Gaussian reference's local relative force gradient and
K_YY=k+k_L/2. Direct calculation gives the FULL defect

    (H_full W-W(H_G+E_R b))Phi
      =U{ c_R P^2 Phi (A_b^2 psi_b)
          -a F_G Phi (chi_b psi_b)
          +(a^2 K_YY/2)Phi(chi_b^2 psi_b)},            (2)
    c_R=E_R a^2/hbar^2=(R-1)/(2B)<=1/(2B_0).

U is the conditional phase unitary. Equation(2) has not discarded any
normal or lead mode, and has no hidden term linear in P. That exact
cancellation is why a generic gap-only estimate is unnecessarily weak.

The positive Bessel formula gives

    ||A_b^2 psi_b||^2=I_0(6b)/I_0(2b)^5
       <=pi^5 e^5 b^(5/2)exp(-4b), b>=1.             (3)

Also ||chi_b psi_b||<=sqrt(C_chi/b) and
||chi_b^2 psi_b||<=pi sqrt(C_chi/b).

## 2. The Gaussian local force has a uniform actual bound

This does not assume an absolute-position Gibbs variance for an infinite
chain. For any positive spring bond f=e_i-e_j of stiffness k_L, static
resistance is at most1/k_L. At finite volume its total Gibbs bond variance
obeys the normal-mode estimate

    Var(f^T q)<=C_f/beta+(hbar/2)sqrt(C_f D_f),
    C_f=f^T K^-1f<=1/k_L, D_f=f^T M_G^-1f.

It follows from coth x<=1+1/x and Cauchy-Schwarz over the COMPLETE normal
modes. The Gaussian reference's added relative inertance is a positive
kinetic form, so M_G^-1<=M_physical^-1. Terminal and lead physical masses
are fixed and positive; D_f is therefore uniformly bounded. This proves
the needed local bond bound even when common absolute position is infrared
singular.

Since

    ||F_G||_(2,rhoG)<=k sqrt(V_G)
                +(k_L/2)[sqrt(V_bond,L)+sqrt(V_bond,R)],

there is a finite C_F independent of large B and lead volume. The preceding
Matsubara argument gives <P^2>_G=O(1+log R). Gaussianity gives
||P^2 rho_G^(1/2)||_HS=sqrt3<P^2>_G.

Thus (2) proves

    d_B:=||(H_full W-W(H_G+E_Rb))rho_G^(1/2)||_HS
       <=C_1(1+log R)b^(5/4)exp(-2b)
           +C_2/sqrt(Bb)+C_3/(B sqrt b).              (4)

Constants depend on fixed physical data, not a free force oracle.

## 3. A sufficient stronger lock and actual dynamics on time O(B)

For definiteness take

    b=R(log R)^2, R->infinity, beta=sB, k=kappa/B.     (5)

Then b grows faster than R but slower than R^2. The equilibrium relative-
entropy error of the preceding theorem still tends to zero: beta E_R is
order R^2, the normal entropy bound is exponentially small, zeta log R
vanishes, and beta Q_chi=O(1/b).

Stationarity of rho_G and state-induced Duhamel give, for finite regulators,

    ||[exp(-itH_full/hbar)W
          -W exp(-it(H_G+E_Rb)/hbar)]rho_G^(1/2)||_HS
                                <=|t|d_B/hbar.        (6)

Equations(4)-(5) make the right side vanish uniformly on every fixed
scaled interval |t|<=t_0 B. This is a real-time statement and does not
follow from the equilibrium trace distance by itself.

For correlations with a bounded inserted Weyl operator O_u=exp(iuY), the
same Duhamel argument is valid. In the Gaussian reference, O_u(-t) is a
Weyl operator of a linear coordinate. Its commutators with P and F_G are
c-numbers, bounded by2|u|sqrt(Var(P)V_G) and
2|u|sqrt(Var(F_G)V_G). Consequently its insertion changes the momentum
HS bound only by a fixed-u factor times1+log R, and the force bound only
by a fixed-u constant. Thus (4)-(6) remain valid on
O_u rho_G^(1/2), uniformly in the scaled time interval.

Finally

    ||(O_u W-W O_u)rho_G^(1/2)||_HS
                              <=|u|a sqrt(v_chi)->0.  (7)

Here Y and the normal chi_b commute after the explicit phase unitary, so
this is not an unjustified operator-Lipschitz substitution. Combining the
initial Gibbs state comparison with(6)-(7) proves convergence of bounded
coordinate-Weyl equilibrium two-time correlations to those of H_G.

## 4. Unbounded Y correlations and the full thermal spectral measure

The equilibrium source separately proved that full loaded Var(Y) converges
to the Gaussian reference limit, using partition functions at nearby k,
and that the Y distribution converges. These two facts imply uniform
integrability of Y^2. Equilibrium stationarity makes the associated
truncation error uniform at every time: Cauchy-Schwarz bounds a two-time
error by the fixed equal-time L2 tail.

For example use the bounded difference quotient
(exp(iuY)-1)/(iu), then send u to0 after the gain limit. This proves
convergence of the COMPLETE unbounded-Y equilibrium correlations on every
fixed scaled real time. It does not infer moments from a small leakage
probability.

The positive bilateral Lehmann measure has total mass Var(Y). Its scaled
characteristic function is precisely that equilibrium correlation. The
Gaussian limit is continuous at zero and the total masses converge, so
the continuity theorem for positive finite measures gives weak convergence
of the scaled FULL Lehmann measure. No inversion of noisy finite-window
data or free real-time measurement is being performed.

## 5. The loaded Gaussian limit is explicit and has a nonzero deficit

With z=Bomega, the Gaussian relative susceptibility has the limit

    chi_G(omega)/B ->[kappa-z^2-i Zz/2]^-1.            (8)

The fixed finite-band Rubin reactive correction is O(1/B) in this scaled
denominator. For sufficiently large B there is no odd above-band bound
pole: above Omega the real lead kernel decreases from2k_L to k_L,
while -Bomega^2 already dominates k+s_R/2. The scaled position spectral
tail is uniformly O(1/z^3), since the real denominator is bounded below
by z^2/4 beyond a fixed z. The small-z thermal singularity cancels the
linear dissipative numerator. These bounds justify full Gaussian spectral
convergence, not just a pointwise low-frequency approximation.

The common channel retains its fixed complete mass and tends to its
transparent phase on omega=O(1/B). Under the governing inclusive-current
contract, the resulting thermal deficit limit is

    D=(3s hbar/pi^2)int_0^infinity G(s hbar z)
               (Zz/2)^2/[(kappa-z^2)^2+(Zz/2)^2]dz,
    G(x)=[x/(2sinh(x/2))]^2.                           (9)

It is strictly positive and less than1. For hbar=s=Z=kappa=1, restrict
z to[1/2,1]: the reflection fraction is at least1/10 and G(z)>25/36.
Hence

    D>5/(48pi^2)>0.                                   (10)

The associated full port-variance limit is the finite Gaussian Matsubara
sum; in these units it is at most13/12. The total translating mass and
rotor radius can stay fixed, but the locking resources in(5) do not.

## 6. Why the same heat functional applies only at its real contract

For a time-independent parity-separated junction with identical leads,
equilibrium KMS input/output completeness and no unassigned persistent
bound-state memory, the already derived inclusive-current relation uses
the FULL odd susceptibility, including inelastic processes. In the
common-channel-unity limit its normalized deficit is

    delta_1=Z/(2J_Q) int_0^infinity omega G(omega/theta)
                                            chi_Y''(omega)domega,
    J_Q=pi^2 theta/3.

For the positive unsymmetrized Lehmann measure nu, KMS gives
chi''(omega)domega=(pi/hbar)(1-exp(-beta hbar omega))nu(domega).
At beta=sB, its scaled test kernel is

    (3sZ/(2pi))1_(z>=0) z G(s hbar z)
                                      [1-exp(-s hbar z)].

It is bounded, continuous at zero and vanishes at infinity. The weak
spectral convergence above therefore gives(9). The actual Rubin factor
sqrt(1-omega^2/Omega^2) converges on the thermal window, with a vanishing
weighted tail, and the fixed-common-mass phase correction vanishes as
well. This is not an elastic-unitarity shortcut for a nonlinear scatterer.

The stated KMS/scattering existence assumptions remain actual premises.
These proofs do not establish asymptotic completeness or a finite Gibbs/
NESS preparation time for the material. Without that current contract,
the unconditional conclusions here are the coupled canonical Gibbs and
equilibrium spectral/dynamical limits; the heat-current statement is its
explicit conditional corollary.

## 7. Cost and what the canonical construction does not acquire

For fixed I,B_0 and growing compact gain, E_R is order R and(5) pays

    U_bar=O(R^3 log^4 R), normal reference energy=O(R^2 log^2 R),
    peak lock force=O(R^(7/2)log^4 R),
    lock curvature=O(R^4 log^4 R), pitch=O(R^-1/2).

This is a sufficient, deliberately nonoptimal dynamical construction.
The earlier E_R log^2 R barrier law is the sharp ORDER for low-band
inertial amplification; it is not proved sufficient for this live thermal
dynamical limit by the rough norm estimate(4). No optimal heat/material
resource tradeoff is asserted.

Every fixed member is a finite smooth positive canonical lock, with the
spring and all lead modes retained. A real rotor/contact has finite elastic
bandwidth, loss, minimum feature size and force capacities. Assigning this
growing family to that apparatus remains unacquired. Preparing the actual
Gibbs/NESS state in finite time and measuring heat are separate operations.
The construction closes a model-level nonlinear-mechanical comparator to
the positive scalar harmonic frontier, not a practical thermal device.
