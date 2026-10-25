# A finite active aperture preserves the canonical memory and its static port dipole

26 October 2026. New root construction, independent whole review pending.
This closes a model-level aperture issue in CANONICAL_MEMORY_SYMMETRY.md,
not its unproved detuned cold dynamics or actual material implementation.
It uses elementary Gibbs variation and the existing exact sector algebra;
no priority claim is made.

## 1. Replace the whole-line interaction by an actual compact profile

Keep the complete Gaussian mechanical host H_G, with actual terminal bare
inertia B_0, port Y, port spring kY^2/2, and fixed identical Rubin leads.
Use finite far-pinned regulators first. Let

    r(s)=1-10s^3+15s^4-6s^5,  0<=s<=1,
    chi(u)=1 for |u|<=1,
           r(|u|-1) for 1<|u|<2,
           0 for |u|>=2,
    w_L(Y)=Y chi(Y/L).

This is an odd C^2 profile, equals Y on the core, vanishes outside
[-2L,2L], and satisfies

    |w_L(Y)|<=|Y|,  ||w_L||<=2L,
    ||w_L'||<=19/4,
    |w_L'-1|<=(23/4) 1_{|Y|>L}.                       (1)

Indeed 0<=r<=1 and max|r'|=15/8. The stated derivative constants are
conservative. All spatial derivatives and the interaction norm are finite
at a fixed L. The literal model is now

    H_eta,L=H_G+E_R(N-1/2-eta)^2-lambda w_L(Y) Q,
    Q=2cos(phi),  ||Q||=2.                            (2)

Its active extent is 4L, interaction norm at most4lambda L, and actual
mechanical force at most19lambda/2. These are resources, not a free field
generator. There is no limit L->infinity in the construction below.

The original J=e^{i phi}R_phi still commutes with H_0,L. Mechanical
inversion times pi rotor translation still commutes with H_eta,L and
anticommutes with J, because w_L is odd. Thus the exact paired sectors,
ND normal ladder and off-sector detuning operation survive unchanged.

## 2. Uniform port second moment, without linear-force identities

The earlier matrix momentum-domination theorem assumes LINEAR coordinate
coupling and is not inherited by (2). Instead derive its actual port
bound directly. Write H_G(s)=H_G-(k-s)Y^2/2 and let V_G(s,T) be its full
Gaussian variance. For s>=k/4, all spring forms remain positive.

Work in either exact J sector at eta=0. Write Z(s) for its full partition
function with H_G(s). The Gaussian Gibbs state times the free ND ground
state is a variational state. Its interaction mean is zero: the Gaussian
law is centered and w_L is odd. Hence

    Z(k)>=Z_G(k) exp(-beta E_R/4).                    (3)

The scalar square bound, using |w_L|<=|Y|, gives

    H_L(k/2)>=H_G(k/4)+E_R(-partial_xi^2)_ND
                                      -8lambda^2/k. (4)

Eigenvalue monotonicity of the finite-regulator trace therefore implies

    Z(k/2)<=exp(8beta lambda^2/k) Z_G(k/4)
                          exp(-beta E_R/4) A(beta E_R),
    A(t)=sum_{j>=0}exp[-t j(j+1)]
        <=1+exp(-2t)/(1-exp(-4t)).                    (5)

Convexity of log Z(s), with derivative -beta<Y^2>_s/2, yields

    (beta k/4)<Y^2>_k<=log Z(k/2)-log Z(k).

Gaussian spring differentiation and variance monotonicity give

    log[Z_G(k/4)/Z_G(k)]
        <=(3beta k/8)V_G(k/4,T).

Consequently, for every L,

    <Y^2>_sector <=32lambda^2/k^2 +(3/2)V_G(k/4,T)
                         +4 log A(beta E_R)/(beta k). (6)

For T<=T_0 use

    V_G(k/4,T)<=4k_B T_0/k+hbar/sqrt(B_0 k),
    M_2=32lambda^2/k^2
        +(3/2)[4k_B T_0/k+hbar/sqrt(B_0 k)]
        +(4k_B T_0/k)log A(E_R/(k_B T_0)).             (7)

All regulator constants are uniform; bounded truncation/Fatou transfers
the second-moment upper bound to any stated local sector KMS limit. The
full symmetric mixture obeys the same bound. No moment is transferred
using trace distance. This is a port bound; it is not an assertion that
the infinite reservoir's total energy is finite.

## 3. Full-ladder sector dipole survives at a fixed finite aperture

The bounded-penalty argument of CANONICAL_MEMORY_SYMMETRY Section5 applies
literally, because its only interaction lower bound used |Y Q|<=2|Y|.
Here |w_L Q|<=2|Y|, and the same variational state still has zero mean
interaction. Put

    C_0=4lambda^2/k,
    K_*=C_0+(k/4)V_G(k/2,T_0),
    t=beta E_R.

For the free ND excited-state projector Pi_ex, that proof gives

    <Pi_ex>_+ <=K_*/E_R
         +(1/t)log[1+exp(-t)/(1-exp(-3t))].             (8)

Choosing fixed E_R>=128K_* and E_R/(k_B T_0)>=10 ensures
<Pi_ex>_+<1/64. The reduced normal state's trace distance to its free
ground state is at most sqrt(<Pi_ex>_+). Since Q is bounded and its free
ground mean is1,

    <Q>_+>=1-4sqrt(<Pi_ex>_+)>1/2.                    (9)

This uses trace distance only for the bounded Q observable. The actual
force is w_L'(Y)Q, and its missing tail is controlled instead by (6):

    |<w_L'(Y)Q>_+-<Q>_+|
         <=(23/2) Pr_+(|Y|>L)
         <=23M_2/(2L^2).                              (10)

Choose ONCE a finite L with L^2>46M_2. Then (9)--(10) give
<w_L'Q>_+>1/4. The exact Gaussian mechanical equilibrium equation,
including all lead coordinates, is

    <Y>_+=lambda C_reg <w_L'Q>_+,
    C_reg=v^T K_reg^{-1}v.

For the stated local infinite-lead limit C_reg->1/k, hence

    <Y>_+>lambda/(4k),   <Y>_-<-lambda/(4k).           (11)

The unrestricted sector mixture is unbiased but retains its nonzero
conserved-J correlation and the corresponding static spectral memory.
This is a fixed finite-aperture, full-normal-ladder conclusion. It does
not assert a retarded susceptibility or a heat deficit.

## 4. Rotor energy and limits of the result

The rotor kinetic bound in CANONICAL_MEMORY_SYMMETRY(8) survives for all
|eta|<=1/4. Its lower square bound uses only |w_L|<=|Y|, and its charge
trial has Q mean zero. Thus the complete minimally coupled charge kinetic
energy remains uniformly bounded at fixed parameters, not merely the
population outside a chosen doublet. The constants need no temperature-
dependent gain, barrier, pitch, aperture or E_R.

Nonlinear w_L removes the exact linear-force Matsubara completion, so the
old matrix mechanical momentum domination and its total spring/kinetic
EXCESS bounds require a separate argument; they are NOT claimed here.
Detuned cold intersector dynamics, inclusive current completeness, finite
Gibbs/NESS preparation, actual finite-extent field construction, material
energy/mass, offset precision and symmetry-defect tolerances remain open.
The construction shows that the static canonical memory/dipole does not
depend on an infinite active field extent. It does not acquire a device.
