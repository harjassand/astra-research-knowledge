# The exact vacuum-frame unitary is an implemented primitive

29 October 2026. This is a deterministic circuit specification at finite
precision. No quantum circuit is executed. It closes an input-access gate
in ALL_COLD.md, rather than supplying an independently presumed ground
state or normal form.

## 1. Known path, known constant gap, and a fixed scalar filter

The native input supplies H(v)=N+vV_s for 0<=v<=lambda and the previously
proved uniform ground gap at least1/2 on this path for every known s.
Each H(v) is an explicit list of O(n) bounded-rank terms. The list for
V_s is explicit as well and has sum of operator norms E_V=O(n).

Use an ordinary exact ground spectral-flow filter with Fourier values
equal to the appropriate signed i/omega for |omega|>=1/2 and smoothed
near0. Its sign is chosen consistently with ground transport. A concrete
construction is a fixed real even Gevrey cutoff c(omega), equal1 near0
and0 before |omega| reaches1/2, followed by the frequency multiplier
i[1-c(omega)]/omega. The associated real odd time kernel w(u) is bounded,
has a possible one-sided jump at0, and decays stretched exponentially.
For u>0 it can be evaluated as a tail integral of the compact-frequency
inverse transform of c. Hence w, its one-sided derivative, and every
absolute time moment have explicit finite bounds from the same smooth
step derivative recurrence as the frozen scalar compiler.

The exact Hermitian ground-flow generator is

    A(v)=integral_R w(u) exp(iuH(v)) V_s exp(-iuH(v))du.   (F1)

It transports the isolated ground projection. It acts on the WHOLE clock
Hilbert space and is not an adiabatic state-preparation oracle. Other
syndrome sectors play no role because s is a known classical input here.
No excited-band separation is required.

## 2. Explicit finite operator-norm approximation

Suppose the final full-unitary tolerance is delta_U. Pick a generator
quadrature tolerance delta_A<=delta_U/[32(1+lambda)]. With fixed filter
constants C_r, choose a time cutoff

    T >= 1+32 C_2 E_V/delta_A.

The norm of the discarded tail is <=delta_A/16 by the elementary second
absolute-moment bound. Integrate positive and negative times in paired
form, or split the one-sided jump at0; no quadrature crosses an unresolved
kernel discontinuity. On each side the integrand derivative has a bound
polynomial in E_V, E_H=sup_v sum_X||H_X(v)||=O(n), and the known bounds
on w,w'. A rectangle mesh at most delta_A divided by16T times that
derivative bound has finite polynomial length. Compute every coefficient
to error <=delta_A/[32T E_V] by fixed compact-frequency scalar quadrature
and its tail bound. Hamiltonian-simulation errors get the remaining
delta_A margin. This constructs Ahat(v) within delta_A in operator norm.
Hermitize to retain a genuine Hamiltonian generator.

The normalization of its LCU block encoding is at most

    E_V [integral |w(u)|du+1]=O(n),                      (F2)

with coefficient-table construction charged at its actual polynomial
length. V_s is a supplied finite local sum, so its block encoding is
ordinary LCU of fixed-dimensional local matrices, or local contractions.
Every conjugation in (F1) uses native H(v) simulation. No spectral values
or many-body ground amplitudes are requested.

For path discretization, Duhamel bounds

    ||A(v)-A(v')|| <=2|v-v'| E_V^2
                            integral |u w(u)|du.         (F3)

Thus a path mesh with spacing delta_U divided by a fixed multiple of
(1+lambda)E_V^2 times the first filter moment gives O(delta_U) unitary
error in the time-ordered product. Each piece is the evolution of the
known Hermitian block encoding Ahat(v). Ordinary block-encoded Hamiltonian
simulation implements it. Allocate the per-piece unitary precision by
the total number of pieces. All resulting gate counts and classical
coefficient calculations are polynomial in n,delta_U^-1 for the fixed
native path/filter. Reversing these gates implements W rather than W^*.

The native exact ground flow in ALL_COLD.md is precisely this W (up to
orientation). Thus its use to make the ground state a vacuum, to dress
seeds, inside Hbar real-time evolution, and to return the final state is
paid uniformly. An O(log n)-time abstract spectral flow is NOT asserted.

## 3. Composition with finite Gibbs filtering and reset channels

The exact sampler is specified in the vacuum frame; its implementation
calls exp(iuK)=W exp(iuH_s) W^* up to the irrelevant scalar phase.
The global scalar phase cancels in every Heisenberg conjugation. Its
Gevrey jump and compact coherent filters are exactly the frozen
IMPLEMENTATION.md filters, so the coefficient recurrence, grid and error
allocation remain valid after replacing its update time by ALL_COLD Eq(21).

The previously explicit schedule has a polynomial number of calls to W,
W^* and controlled native evolutions. Demand delta_U less than epsilon
divided by128 times that number and the largest associated LCU
normalization. This is polynomial precision, not a thermal condition
number. Inverting W at the final output receives its own epsilon/64
operator-norm budget. The known physical prefix unitary, when required,
is a further fixed-depth local circuit and is also retained.

The parent similarity and the bootstrap spectral flow used to PROVE its
gap in ALL_COLD Section6 are NEVER simulated. They introduce no additional
preparation input or oracle. Only the native uniformly gapped path above
is simulated by this primitive. The resulting full circuit has polynomial
work in n,t,epsilon^-1. The deliberately loose time-grid exponent becomes
O(t^39) when the new update time O(nt) is substituted, suppressing other
polynomial factors. This is far from a practical hardware estimate.

It prepares only known-s conditional clocks. A full Gibbs initializer must
separately obtain the correct syndrome marginal, including its excited-clock
trace. No bath/calibration, physical quantum controller, or actually executed
state preparation is acquired by this mathematical circuit description.
