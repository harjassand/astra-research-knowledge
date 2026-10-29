# A physical data-noise input for asynchronous coherence suppression

29 October2026. Root construction; whole independent challenge pending.
This is a corollary of PROOF.md for a concrete continuum-noise model.
It is not a logical-memory lifetime theorem.

## Model

Use the source checks, finite-rate independent Poisson check dephasers,
and nominal Pauli-times-check recovery operations of PROOF.md Section5.
The source has distance d_code. Each data-noise seed has source support
X_j, |X_j|<=q, touches<=b checks; a check meets<=K seed supports. All these
constants count actual supplied operations/supports, not just their names.

The nominal clock/bath environment can have arbitrary strength and memory
provided its joint source action is sum_s Pi_s tensor H_s(t), identity on
the logical algebra. Initial source encoding is syndrome diagonal with
logical-input-independent weights, and the environment is independent of
the logical input. Add independent centered Gaussian DATA-noise baths,
factorized initially from source/nominal environment, with couplings

    alpha sum_j A_j(t) tensor B_j(t), ||A_j(t)||<=1.

Precisely, H_tot=H_good tensor I_noise + I_good tensor sum_j H_Bj
+ alpha sum_j A_j tensor B_j. H_good acts TRIVIALLY on these data baths;
their H_Bj are the specified source-independent free Gaussian Hamiltonians.
A_j acts only on source/clock/nominal-environment factors. Arbitrary separate
CLOCK baths may be part of H_good, not hidden additional couplings to the
same Gaussian data fields.

A_j is Hermitian with the stated FIXED source support (clock/environment
coefficients are permitted if bounded). Its source label may change the
syndrome. Baths j satisfy Wick and stationary correlations with

    M0=sup_j integral_R |C_j(u)|du < infinity.

Well-defined joint dynamics and the finite-horizon Wick/resummation
premises are as in the accepted Gaussian packet. This is not a bounded
operator-norm assumption on the oscillator field B_j.

## Crucial reference change: switch off the whole marked slot

For finite horizon T use slots v=(j,k) of duration tau, shortening the
final slot if needed. Phi[K] is the PHYSICAL comparison experiment which
couples bath j only in slots (j,k) in K. The SAME free bath can be reused
across all its active slots. There is no fresh bath per slot and no claim
that a system reset resets a bath. Equivalently the effective free covariance
is C_j(t-s) times the two active coupling masks; this is a physical switched
coupling, not an arbitrary covariance-deletion ansatz.

Define F_M by finite Mobius inversion of these Phi[K]. Then F_empty has
NO data-noise couplings at all, and F_M contains only data-noise insertion
labels from slots in M. All nominal clock-only cooling remains exact.
The supported-label premise of PROOF.md Section5 is therefore paid: zero
data-noise reference dynamics preserves relative Pauli labels, while each
marked slot supplies only Paulis on its X_j. This differs essentially
from keeping exact data-bath dynamics inside every unmarked fresh slot.

For an inclusive marked set R, compare every Phi[V minus U], U subset R,
to the same physical reference Phi[V minus R]. The differing covariance
pairs all touch R. They include pairs with BOTH endpoints in ONE marked
slot; their omission would be an invalid shortcut. Resum all reference
pairs into exact reference joint propagators and use finite difference
cancellation. Every surviving selected-pair family covers R, so it has
at least ceil(|R|/2) pairs. Define the overpaid slot-pair row

    eta = 8alpha^2 sup_v sum_w integral_(I_v)x(I_w) |C_j(t-s)|,

where only slots of the same seed j contribute, and w=v IS included.
The stationary L1 bound gives

    eta <=8alpha^2 tau M0.

The accepted Gaussian coverage argument, including complete strategy
norm for arbitrary common nominal interventions and inert references,
then gives the CONSISTENT local condition

    ||sum_(M superset R) F_M|| <= epsilon^|R|,
    epsilon=sqrt(2e eta), eta<=1/2.                      (1)

It is uniform over all fixed exogenous read/nominal schedules. Born
outcomes are never normalized under conditioning. Thus averaging the
independent Poisson read flags is legitimate. For a last partial block,
extend ONLY the exogenous Poisson read process to its full endpoint when
defining the auxiliary graph flag. Those extra times cannot lie strictly
between two actual fault slots, since that block is the last one. Endpoint
flags are ignored by the graph, so no artificial cut between actual
insertions is introduced. The physical process and receiver still stop
at T; no additional physical evolution is being equated with them.

## Actual acquired conclusion

Let theta=1/(64bK), d=ceil(d_code/q), and N the TOTAL number of seed/time
slots. If Gamma tau>=log2 and 2epsilon<=theta, the final actual logical
CPTP channel Lambda satisfies

    ||Lambda - T_L(Lambda)||_diamond
       <=min{2, 2[exp(4Ntheta(2epsilon/theta)^d)-1]}.     (2)

T_L is the mathematical logical-Pauli twirl. Its output is an actual
Pauli channel, so this supplies proximity to SOME positive logical Pauli
law from a signed non-Markovian data-noise expansion. No positive fault
slot indicators or fresh data baths were assumed.

For the fixed compact-band spectrum, the accepted temperature-uniform
M0<=16A0^2, A0=4C_B, C_B=22806356488960, permits the simple overpay

    epsilon=28alpha A0 sqrt(tau).

Indeed 2e eta<=768alpha^2 tau A0^2<28^2alpha^2 tau A0^2.
This sufficient coupling is constant in volume and elapsed time, though
its displayed constants are physically poor. At fixed admitted rates,
the bound has a prefactor N linear in the finite horizon and a distance
exponent. It suppresses residual LOGICAL COHERENCE over such a horizon.

It does NOT bound the nonidentity Pauli weight. Even exactly Pauli noise
can destroy the memory, and the resulting Pauli law can depend on full
past/future environment/read histories. The native noisy classical
decoder must still prove an offline pathwise persistence estimate; a
causal-only Markov threshold or static Gibbs Peierls weight is insufficient.

Ideal nominal Pauli/check operations and read dephasers are model inputs.
Their microscopic realization/calibration and a local multi-time budget
for implementation errors are separate. A closed finite bank cannot be
given the all-time M0 premise: its finite positive Fourier sum has divergent
absolute correlation norm, as the accepted FINITE_BANKS proof establishes.
Fresh epochs can supply a different kernel, but renewal/entropy export
then remains a physical resource. No repeated faulty-recovery, thermal
rate, bounded-density3D or useful-device conclusion follows from(2).

Established inputs: Liu--Lu arXiv2408.04009v3 Lemma1 resummation,
Ng--Preskill arXiv0810.4953 Gaussian fault bounds, ordinary stabilizer
decoherence/correctability, and the accepted c_poisson_syndrome_history
supported-label algebra. Generic coherent FT and static qLDPC thresholds
are established; Han et al. arXiv2609.20537v1 is a close controlling prior.
The claimed mathematical work here is the explicit full-slot-toggle
admission to this asynchronous receiver at the displayed assumptions.
Historical priority UNKNOWN; independent review pending.
