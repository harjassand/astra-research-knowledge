# A finite interacting thermal reserve that remains fresh while waiting

Constructive source challenge, 7 November 2026. The principal proposed independent
two-spin reserves to avoid assuming that delivered thermal tokens were noiseless
during an exponentially long idle. This note verifies the proposal and strengthens
it to a genuine Gibbs state of the interacting waiting Hamiltonian.

For a target energy gap Delta>0, let two source spins have

    H_pair=Delta*(n_1+n_2)+h*(sigma_+ tensor sigma_-+
                              sigma_- tensor sigma_+),
    0<|h|<Delta.

The energies/eigenstates are 0 on |00>, 2Delta on |11>, and Delta±h on the two
single-excitation Bell states. For any fixed beta>0 take the actual Gibbs state

    omega_pair=exp(-beta H_pair)/Z,
    Z=1+2 exp(-beta Delta)cosh(beta h)+exp(-2beta Delta).

Every pair is stationary under its **nonzero** waiting interaction for every
delivery time. A bank with Hamiltonian sum_j H_pair,j has product Gibbs state
tensor_j omega_pair,j. Therefore distinct unused pairs remain independent of one
another and of the incoming payload/old memory bath, provided there is no other
coupling before delivery.

There is an exact positive decomposition

    omega_pair=(1-p_bad)|00><00|+p_bad omega_bad,
    p_bad=[2 exp(-beta Delta)cosh(beta h)+exp(-2beta Delta)]/Z
         <=3 exp[-beta*(Delta-|h|)].

The fresh-block bad flags are genuinely independent. They retain *all* token--
partner correlations inside omega_bad. This is better than asserting only a
thermal marginal. A preparation difference from the ground-pair reference has
diamond norm at most 2*p_bad and constant two-spin support, and can be inserted
directly in the full-swap round expansion. Choosing fixed h with |h|<=Delta/2 and
fixed sufficiently large beta*Delta makes this a small fixed local budget.

The delivered token marginal has excitation probability

    q_token=[exp(-2beta Delta)+exp(-beta Delta)cosh(beta h)]/Z.

It is not generally the uncoupled Gibbs state with gap Delta. That equality is
unnecessary for the direct cooling theorem, which only needs the small positive
fresh-block fault weight above. If an exact detailed-balance sampler were desired,
the difference would matter and could not be omitted.

To deliver, ramp h(t) to zero. All Hamiltonians Delta*N+h(t)V commute, so the
state remains exactly omega_pair during an arbitrary-duration ideal ramp. The
token and partner may remain correlated; keep the partner in the actual output
environment or exclude it permanently from future accesses. The decoupling work
for this equilibrium state is

    W_decouple=-h Tr(V omega_pair)
       =2h exp(-beta Delta)sinh(beta h)/Z>=0.

All routing, finite ramp duration, switching/control error, token temperature and
source spacing are paid. The bound is a **reserve/fuel** construction; it does not
recycle a spin or prove an indefinitely reusable refrigerator. K rounds use O(nK)
source spins and O(nK) delivery operations. For exponential K the entire finite
reserve is exponential in n, just as its total consumption time is exponential.
Peak O(n) active source space requires a replenished flow and charges that flow.

The initially proposed product tau_Delta tensor tau_Delta is also stationary,
because it is a function of N=n1+n2 and [N,V]=0. It is a valid explicitly prepared
state, but is not the interacting Gibbs state exp(-beta H_pair)/Z at h!=0. The
genuine Gibbs version above avoids that terminology issue.

**Load-bearing noise boundary.** Future source pairs must remain private until
delivery. The arbitrary old retained bath B in the memory theorem must not have
unbudgeted access to unused reserve pairs. Otherwise long waiting can correlate
the future tokens, and correct marginal temperatures do not prevent a common
logical fault. Additional nonequilibrium, cross-pair, calibration or bank noise
needs a delivered-block bound or an explicit fresh reset before delivery. A
private waiting channel that exactly fixes omega_pair can be allowed, but its
fixed-point property and independence have to be proved for the actual model.

This establishes a finite, interacting, genuinely thermal, stationary source at
its exact Hamiltonian/initial-state/isolation premises. It is not a robustness
theorem for every perturbation of an unmonitored thermal bank, a practical
refrigerator, or a favorable resource comparison.
