# Actual sector-changing response of the complete canonical contact

26 October 2026. This follows CANONICAL_MEMORY_SYMMETRY.md into eta!=0.
It gives two exact all-normal-mode representations, the actual positive
bath-dressed transition spectrum, and a finite-duration response bound
for a real detuning pulse. No ground-doublet Hamiltonian, instantaneous
equilibrium replacement or thermal-current inference is used.

The finite-clock result is a response of a specified prepared sector,
with explicit moment/source premises. It is not a sufficient cold-heat
or KMS/NESS preparation theorem. The precise remaining infrared object
is identified in Section5.

## 1. Exact charge-ladder representation

Use D=N-1/2, Q=2cos phi and the fixed Hamiltonian

    H_eta=H_G+E_R(D-eta)^2-lambda YQ.

For j=0,1,..., put

    |j,+>=(|-j>+|j+1>)/sqrt2,
    |j,->=(|-j>-|j+1>)/sqrt2.

Here J is sigma_z. On the normal half-line let d_j=j+1/2,
P_0=|0><0|, and T the adjacency with matrix elements1 between j,j+1.
Direct charge algebra gives EXACTLY

    D=-sigma_x tensor d,
    Q=I tensor T+sigma_z tensor P_0,
    H_eta=H_G+E_R d^2-lambda Y(T+sigma_z P_0)
                      +2E_R eta sigma_x d+E_R eta^2. (1)

The normal adjacency is common to both sectors; only its boundary
projector carries the explicit sector force. Every normal level remains,
and the actual transverse vertex is d, not a bounded Pauli coefficient.
This is an exact Hilbert-space identification, not a two-state reduction.

Multiplying the minus-sector basis at normal j by (-1)^j gives the
equivalent folded representation

    Q=sigma_z tensor (T+P_0),
    D=-sigma_x tensor A, A_j=(-1)^j(j+1/2),
    C=sigma_x tensor P_m.                            (2)

P_m is the full Gaussian mechanical inversion. In the unrephased basis
C=sigma_x tensor[(-1)^j P_m]. The two formulas must not be mixed.

This is conventional parity/Fulton--Gouterman structure, extended here
with the literal normal ladder and actual leads. Moroz,
arXiv:1601.06721v2, Theorem1 and Eqs(2)--(8), gives the primary
operator-valued parity diagonalisation; I read those equations directly:
https://arxiv.org/html/1601.06721 . Its existence of a parity reduction
does not identify the spectrum or imply a Gaussian bath for the reduced
operator.

## 2. The actual bath-dressed one-sector transition spectrum

At eta=0, D anticommutes with J and commutes with C. On the J=+ sector
define

    B=(D C)|_(J=+).

B is self-adjoint because D and C commute; B^2=D^2. In (2),

    H_+=H_G+E_R d^2-lambda Y(T+P_0),
    B=-A P_m.                                       (3)

This reduced Hamiltonian is generally NON-Gaussian. Its global mechanical
parity in B is a mathematical representation, not an acquired parity
measurement on an infinite reservoir.

In a finite canonical regulator, take rho_+ proportional to exp(-beta H_+).
The local two-insertion correlation of D in that sector is exactly the
autocorrelation of B under H_+. Let mu_B be its positive bilateral
Lehmann measure in frequency units. It satisfies ordinary KMS balance and

    M_0=int mu_B=<D^2>_+>=1/4,
    M_2=int omega^2 mu_B
       =lambda^2/hbar^2 <Y^2(Q')^2>_+
       <=4lambda^2/hbar^2 <Y^2>_+, Q'=-2sin phi.       (4)

Indeed [H_0,D]=-i lambda Y Q', [H_0,C]=0, and C is unitary.
Thus no physical mode is missing from this measure. The preceding full
rotor kinetic and bounded-force estimates bound M_0 and M_2 uniformly
for T<=T_0 and fixed resources. Positive measures therefore have tight
local lead-limit subsequences; KMS balance and the stated moment bounds
pass to those limits. One need not postulate an infinite product-parity
operator to define the local D correlation in that passage.

For an initial eta=0 thermal plus sector, a small constant detuning gives
the EXACT leading transition coefficient at fixed T and fixed t:

    P_(+ to -)(t;eta)
      =(4E_R^2 eta^2/hbar^2) I_t+o(eta^2),
    I_t=int [4sin^2(omega t/2)/omega^2] mu_B(domega).   (5)

The value at omega=0 is t^2. This follows from state-induced first-order
Duhamel; D has finite thermal second moment. Strong resolvent continuity
and dominated Hilbert--Schmidt integration justify that first derivative.
It is not a termwise expansion with an assumed bounded D norm.

The global inequality 4sin^2(omega t/2)/omega^2
>=t^2-omega^2t^4/12 yields

    I_t>=t^2/4-lambda^2<Y^2>_+ t^4/(3hbar^2).         (6)

So the full bath-dressed response is nonzero on a definite short time
window, with no doublet approximation. Equation(5) alone has no uniform
joint eta,T remainder and is NOT used as such. The next section supplies
a genuine finite-eta, finite-pulse bound instead.

## 3. Finite detuning pulse: no unbounded-control norm shortcut

Let rho be ANY joint initial state supported in J=+, not necessarily a
product, Gaussian, thermal or normal-ground state. For its eta=0 reference
evolution over0<=s<=t assume the actually declared moment bounds

    ||Y exp(-isH_0/hbar)rho^(1/2)||_HS<=Y_*,
    Tr[rho exp(isH_0/hbar)D^2 exp(-isH_0/hbar)]<=K_*.   (7)

The canonical thermal sector provides such constants by the preceding
all-mode theorems. A different real preparation/history must supply its
own bound; it is not declared thermal by this proposition.

Take a nonnegative predeclared eta(s), with

    a(s)=(2E_R/hbar)int_0^s eta(u)du, A=a(t).

Drop only the scalar global phase from E_R eta(s)^2. Compare the actual
unitary U_eta(t) with the EXPLICIT reference

    R(t)=exp[ia(t)D]exp(-itH_0/hbar).

Its generator differs from the actual one only by

    -lambda Y[Q(phi+a(s))-Q(phi)].

Since ||Q(phi+a)-Q(phi)||<=2|a| and Y commutes with the rotor rotation,
state-induced Duhamel gives

    ||(U_eta(t)-R(t))rho^(1/2)||_HS
       <=(2lambda Y_*/hbar)int_0^t |a(s)|ds
       <=(2lambda tY_*/hbar) A.                      (8)

This is a complete nonlinear-host bound with real finite eta. It does
not assume conditional Gaussian noise or integrate an unbounded control
using an invented operator norm.

Because J D J=-D and the reference evolution preserves J,

    ||Pi_- R(t)rho^(1/2)||_HS^2
       =<sin^2(A D)>_(reference final state).

Markov applied to the actual D^2 moment in (7) puts probability at least
1/2 in |D|<=sqrt(2K_*). Also |D|>=1/2 as an operator. Therefore, if

    A sqrt(2K_*)<=1,
    t<=hbar/(16lambda Y_*),                           (9)

then sin x>=5x/6 on0<=x<=1 gives reference transition amplitude at least
A/4. Equation(8) costs at most A/8. The Hilbert--Schmidt triangle inequality
and a separate direct Duhamel upper bound thus prove

    A^2/64 <= P_(+ to -)(t) <=K_* A^2.                (10)

All higher charge states and all lead modes are included. With a
triangular pulse of peak eta_pk and duration t, A=E_R eta_pk t/hbar;
its peak and slew are eta_pk and2eta_pk/t. Conditions(9) leave a nonempty
finite pulse family at fixed apparatus caps for sufficiently small peak.
Its small response still has to be detected by an ACTUAL sector-sensitive
instrument; no measurement of J or free independent copies are supplied.

## 4. Moment and work resources of this finite operation

For the specified finite-band Gaussian support, the no-bound-pole free
retarded kernel has a finite L1 norm Lambda_chi. For two evolutions with
the SAME initial joint state and differing only in eta controls, exact
linear mechanics gives

    Y_eta(s)-Y_0(s)=lambda int_0^s chi_0^R(s-u)
                                         [Q_eta(u)-Q_0(u)]du.

Since ||Q||=2, its operator norm is at most4lambda Lambda_chi. Thus the
actual-pulse moment obeys ||Y_eta(s)||_2<=Y_op:=Y_*+4lambda Lambda_chi.
The exact equation dot D=lambda Y Q'/hbar then gives

    ||D_eta(s)||_2<=sqrt(K_0)+(2lambda/hbar)Y_op s,
    K_0=Tr rho D^2.

The same equation with the reference Y bound supplies, for example,
K_*=[sqrt(K_0)+(2lambda/hbar)Y_*t]^2 in (7). These estimates apply to
unconditional joint states; no per-outcome Gaussian premise is inserted.

For a differentiable actual offset waveform, system work from the source
is bounded by

    |W_system|<=2E_R TV(eta)
            [sqrt(K_0)+(2lambda/hbar)Y_op t+eta_max].  (11)

This follows from partial_t H=-2E_R dot eta(D-eta). It is a finite
state-induced work bound, not the construction energy of the offset-field
generator, its calibration confidence or detector/reset cost. If the
actual finite generator cannot meet the specified peak/slew/precision,
the operation remains unavailable rather than silently idealised.

## 5. The cold transport gate is now a precise actual spectrum

Equation(5) is the actual canonical-memory analogue of a dressed tunnelling
vertex. It is NOT the free-Gaussian Weyl vertex of the earlier literal
spin model. In particular (1) retains normal adjacency T, the boundary
projector P_0 and the unbounded d in the flip. A finite normal population
bound does not control a vanishing low-frequency vertex RELATIVELY.

Persistent cold heat still requires the actual eta-dependent Q/Y
susceptibility, or a controlled low-frequency/all-order expansion built
from (3). The mass and second moment in (4), and the positive finite-time
response in (10), do not determine mu_B near frequency theta. An atom,
a broad continuum and ultraviolet weight can obey the same moment bounds
while giving different scaled-time responses. Equilibrium degeneracy and
static dipoles cannot decide that question.

The strongest conventional explanation remains a charge-qubit/impurity
boundary-condition-changing operator, with known spin-boson/Rabi and
Fulton--Gouterman ancestry. What is new in this continuation is the exact
all-normal-mode target and finite control operation in this literal model;
historical priority is not cleared. The already accepted spin cold theorem
is neither assumed nor inferred for (1).

## 6. Finite full-rotor pulse discriminator

check_canonical_sector_response.py verifies the unrephased ladder formulas
with integer matrices before doing a separate floating pulse diagnostic.
The latter keeps ten host oscillator levels and eight rotor charge states,
E_R=8,lambda=.4,beta=2, and the actual eta=0 thermal plus sector. A
triangular eta pulse of peak .02 and duration .05 has A=.008 and meets
the moment/time conditions(9) with the directly calculated moments.

The complete retained transition measure has mass .2509223202 and second
moment .2598486735, matching the actual commutator expression within3e-16
and below its .5329224406 upper bound. Full time-ordered pulse evolution
gives transition probability1.60572193e-5 within the analytic interval
[1e-6,1.60590285e-5]. The full spectral quadratic prediction is
1.60573077e-5. Purified state error .000101231 is below the finite-pulse
bound .000146004; doubling the temporal mesh changes that state by
1.02e-9. These are finite-cutoff/floating diagnostics of normalization,
phase and pulse factors. No infinite-bath, cold or physical-instrument
certification follows from the matrices.
