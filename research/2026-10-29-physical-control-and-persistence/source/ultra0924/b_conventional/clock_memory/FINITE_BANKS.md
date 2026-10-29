# A finite bank is not an all-time reservoir; a paid epoch alternative

29 October 2026. Companion to PROOF.md. No reservoir/dynamics fixture is run.
The inequalities below concern correlation-based admission and explicit reset
resources. They are not an impossibility theorem for every finite bath or for
the actual RX/RZ memory lifetime.

## 1. A spacing-free finite-bank obstruction

For a passive M-mode oscillator bank in its own Gaussian thermal state, the
Hermitian end-field correlation is a finite positive Fourier sum

    C(u)=sum_(a=1)^D w_a exp(-i omega_a u),
    w_a>0,  W=sum_a w_a=C(0)>0,  D<=2M.                 (1)

Combine identical signed frequencies first; no minimum separation is assumed.
The signs of the frequencies may differ, but the thermal emission/absorption
weights are nonnegative. For any T>0 the Fejer identity gives

    integral_0^T (1-u/T)|C(u)|^2 du
       =T/2 sum_a w_a^2
        +sum_(a!=b) w_a w_b
          [1-cos((omega_a-omega_b)T)]/[T(omega_a-omega_b)^2]
       >=T/2 sum_a w_a^2.                              (2)

The sum convention includes both ordered off-diagonal terms; this is the
real paired integral of the full Fourier sum. Since |C(u)|<=W and by scalar
Cauchy--Schwarz,

    integral_0^T |C(u)|du >=TW/(2D).                    (3)

In particular the infinite-time absolute-correlation norm diverges for EVERY
nonzero finite passive bank, irrespective of incommensurate frequencies or
small coefficients. This is stronger than merely waiting for a numerical
recurrence and uses no Bohr-resolution input.

For equal slots of duration ell, consider the FIRST slot[0,ell] and all later
slots up to a horizon T. Its row mass in PROOF(3) obeys

    eta_first >=8alpha^2 ell W
             [T/(2D)-ell(1+1/(2D))]_+.                (4)

Indeed for t in[0,ell], (3) on[0,T-t], minus the omitted[0,ell-t] interval
whose integral is at most ell W, gives the bound inside the brackets.
Thus the specific sufficient gate eta<=eta_0 of the local memory receiver
cannot hold at all horizons for a fixed finite bank. It requires at least

    D >=(T-ell)/[2ell+eta_0/(4alpha^2 ell W)]            (5)

whenever the right side is positive. This is a LINEAR horizon cost for that
receiver at fixed ell,alpha,W,eta_0. A divergent upper-bound parameter is
not a lower bound on actual logical error, and no such lower bound is claimed.

For the ACTUAL fixed compact-band measure of the frozen preparation packet,
mu_total>=1/16 from its flat central interval. Every finite own-chain thermal
state therefore has W=C_M(0)>=mu_total>=1/16. Consequently(5) gives the native
receiver resource consequence

    M >=(T-ell)/[4ell+8eta_0/(alpha^2 ell)].             (5a)

This is not evaded by assigning very small weights to increasingly many
finite frequencies while leaving the actual end-field coupling unchanged.
At fixed rates and budget, an exponentially long target horizon needs an
exponentially large unreplenished bank FOR THIS admission receiver. It is
not a universal lower bound against another finite-bath analysis.

The frozen preparation packet's finite-chain estimate was designed for a
specified finite time and does not contradict(3)--(5). Appending that bank
once and reusing it indefinitely is an invalid shortcut. Resetting source
qubits does not replace the bath state; prior PRX Quantum6,010323(2025)
already gives exact control-history examples of this distinction.

## 2. Finite epochs with an explicit local memory gate

Choose an EPOCH length T_e, a multiple of ell. Supply a FRESH independent
M-mode bank for each seed at each epoch. Within its epoch the bank may be
reused for many slots. The Gaussian kernel is then the own-chain C_M(t-s)
inside an epoch and zero across epochs. The exact fresh-slot reference has
the same finite-bank kernel inside each slot. Both are physical Gaussian
processes, so PROOF.md applies directly, without a global state comparison
to an infinite bath.

The finite bank can be acquired with an explicit first-moment gate using
the SAME fixed passive spectral measure of frozen clock_controller. Write

    f_u(z)=[n_b(z)+1]exp(-iuz)+n_b(z)exp(iuz),
    n_b(z)=(exp(bz)-1)^-1.

On the Bernstein ellipse of parameter2 for[1/2,3/2], Re z>=3/8 and
|Im z|<=3/8. At b>=1 both |n_b(z)| and |n_b(z)+1| are <=4, hence
|f_u(z)|<=8exp(3|u|/8). Degree-(2M-1) Chebyshev approximation has error
<=16exp(3|u|/8)2^(-(2M-1)). Jacobi moments at the FIRST site agree through
degree2M-1 (a path leaving the M modes and returning has length at least2M).
Using mu_total<=1 yields

    sup_(|u|<=T_e) |C_infty(u)-C_M(u)|
             <=64exp(3T_e/8)2^(-2M).                  (6)

In particular, for a specified delta in(0,1), the scalar integer choice

    2M>=8+ceil(T_e)+ceil(log2(1/delta))                 (7)

pays(6) by delta. It uses exp(3/8)<2, not a floating quadrature assertion.
The explicit moment-Gram and Gevrey algorithms in the frozen packet pay
actual Jacobi acquisition; no new table or model is executed here.

Within one epoch, the local memory row therefore satisfies

    eta_epoch<=8alpha^2[M1+delta T_e^2],
    M1=integral_R |u C_infty(u)|du<=32 A_B^2.           (8)

For example, choose delta<=zeta/T_e^2 for a specified zeta>0. The row budget
is then 8alpha^2(M1+zeta), independent of total number of epochs and clocks.
For fixed b,alpha,ell,T_e,zeta, the bank length is a CONSTANT in system size
and total elapsed time. All covariance, coefficient and state-precision
algorithms are supplied by the earlier packet. Equation(8) is an exact
Gaussian-process statement before local occupation truncation.

## 3. Renewal, capacity and geometry are real resources

For m seeds and total run time T, the explicit fresh-bank epoch construction
consumes

    m ceil(T/T_e) banks and mM ceil(T/T_e) initial mode vacua,

as well as Gaussian random draws, force pulses and discarded bath outputs.
The frozen packet gives a finite-time model for preparing each Gaussian bank
from local vacua; it does NOT produce an unlimited new-vacuum supply from a
closed finite apparatus. Fixed per-epoch bank size can be time-multiplexed,
but reinitializing unknown spent banks needs an actual entropy-export/reset
operation. That operation is not inferred from its scalar logZ or covariance.

A simple resource lower bound explains the distinction. Suppose a closed
environment of Hilbert dimension D_B repeatedly resets k independent input
qubits initially maximally mixed, such that every output qubit has population
error <=p<1/2 relative to its target pure state. Entropy conservation and
subadditivity imply

    log D_B >=k[log2-h_2(p)]+S(rho_B_initial).           (9)

Here logs are natural, h_2 is binary entropy, and outputs may be mutually
correlated. Each marginal entropy is at most h_2(p); output correlations do
not improve the environment entropy-capacity bound. This statement assumes
the reset task and no external entropy export. It is not a native memory
heat-rate bound or a universal dissipation-in-joules claim. Classical records,
discarded modes and new pure ancillas are external entropy resources and
must be counted if used.

Constant-size bank MODULES can be placed near bounded-density source sites
in3D at constant overhead, after resolving a bounded number of coincident
source sites and rescaling by a fixed module size. This observation concerns
one active finite bank per seed. It does NOT lay out all the fresh future
banks, their delivery/removal streams, pumps or the entropy sink in a fixed
bounded-density3D volume. Conversely, no full3D-grid comb obstruction is
claimed for the sparse recursive source merely from its existing embedding.

There is also a non-Gaussian gate: local finite-level truncation and physical
initialization/calibration errors require a LOCAL multi-time admission bound
for their repeated implementations, not the earlier global preparation error.
Uniform single-epoch process estimates are promising, but a product CPTP-
fault-budget conversion is not silently supplied here. None of these costs
are needed to prove the Gaussian memory bound(6) of PROOF.md; all are needed
before claiming a fixed finite physical controller for long storage.
