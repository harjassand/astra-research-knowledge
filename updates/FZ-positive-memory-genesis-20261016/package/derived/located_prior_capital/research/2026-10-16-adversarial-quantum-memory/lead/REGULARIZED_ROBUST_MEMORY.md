# A regularized autonomous memory robust to local generator errors

Principal reconstruction of the new construction, 16 October 2026. Status:
conditional theorem under the independently reconstructed envelope, LSS and HT
premises; its additional steps survived the separate direct quantum audit in
trajectory/CPTP_REGULARIZATION_AUDIT.md. This generator differs from
the original sweep on syndrome coherences. External correctness and historical
priority are unestablished.

## Exact construction and statement

For each primal or dual vertex v, write Pi_O for its seven active-pattern
projectors and Q_O for the specified one/two-face sweep Pauli. Set

    Pi_inactive = I - sum_O Pi_O,
    C_v(rho) = sum_O Q_O Pi_O rho Pi_O Q_O^dagger
               + Pi_inactive rho Pi_inactive.

This is CPTP, because the Kraus adjoint products sum to I. Every Kraus operator
is supported in the same 24-qubit star. The generator kappa*(C_v-Id) equals
the original sum of seven correction dissipators plus D[sqrt(kappa)*Pi_inactive].
The extra term vanishes on every definite-syndrome Pauli density operator.
The code-initial Pauli law is therefore unchanged, while cross-syndrome
coherences are treated differently. Full individual inactive-pattern projectors
may alternatively be used, with the same definite-syndrome law.

Fix, independently of L, a translation-covariant finite patch family A_(x,a),
with a finite number of patch types per fine cell x. Its fixed radius includes
all perturbation supports under consideration. Let d_a be the Hilbert space
dimension of that patch, and let D_(x,a) be complete depolarization of the patch,
with the identity on its complement. Choose positive fixed proposal rates nu_a.
The regularized baseline is

    G_0 = kappa sum_v (C_v-Id)
          + sum_(x,a) nu_a (D_(x,a)-Id).

For sufficiently small total per-cell proposal rate sum_a nu_a relative to
kappa, the construction below protects all six logical qubits. Add ANY local
linear generator perturbations E_(x,a), supported on A_(x,a), that are Hermiticity
preserving and trace annihilating, with

    ||E_(x,a)||_diamond <= nu_a/d_a^2.

They need not be Pauli, syndrome diagonal, reversible, or translation invariant.
Local Hamiltonian commutators and differences of local Lindblad correction
terms satisfy the algebraic type assumptions. Their norms must obey the
displayed fixed local bound. Multiple terms may be grouped on one patch and
charged by their norm sum. No bound independent of volume is assumed for
the norm of the TOTAL perturbation.

Then G=G_0+sum E_(x,a) is itself a Lindblad generator and, for a compatible
family L=bM, constants A,c>0 independent of L,T give

    || Dec_L exp(T G) Enc_L - Id ||_diamond
       <= min(2, A L^4 (1+kappa*T) exp(-c*L))

for all T>=0. Initialization and final recovery have the original ideal scope.
The fixed support and perturbation radius can make all constants exceptionally
poor. The claim is a qualitative local robustness neighborhood of THIS
regularized generator, not of the unmodified original generator.

## 1 Absorbing perturbations by an interior channel

Use the normalized maximally entangled vector Omega_d. For a local map E set
J(E)=(E tensor Id)(|Omega_d><Omega_d|). Hermiticity preservation makes J(E)
Hermitian. Complete depolarization has J(D)=I_(d^2)/d^2, while

    ||J(E)||_operator <= ||J(E)||_1 <= ||E||_diamond.

Thus the map Psi=D+E/nu has positive Choi matrix whenever
||E||_diamond<=nu/d^2. Trace annihilation of E makes Psi trace preserving.
For completeness, diagonalize that positive Choi matrix into rank-one vectors
and reshape each vector, multiplied by sqrt(d), into a Kraus matrix. Inverting
the matrix-unit Choi correspondence recovers Psi as their Kraus sum; the
trace-preserving partial-trace condition gives sum K_j^dagger K_j=I. Thus Psi
is CPTP, and the following is an exact identity of maps on ALL local inputs,
including references:

    nu*(D-Id)+E = nu*(Psi-Id).

Consequently

    G = kappa sum_v (C_v-Id) + sum_(x,a) nu_a*(Psi_(x,a)-Id).

Every term is a CPTP proposal generator. A channel Psi with Kraus B_j gives
nu*(Psi-Id)=sum_j D[sqrt(nu)*B_j], since sum B_j^dagger B_j=I. Independent
state-independent Poisson times at these rates give the exact evolution,
including its no-jump part. No approximation by a twirled noise model is used.

The interior-channel argument is elementary Choi theory, not an invention of
complete positivity or a historical novelty claim. The scientific question is
its use with an independently stable local autonomous corrector.

## 2 Good clock and location schedules correct every local channel

Condition on the finite sequence of ideal correction proposal locations and
fault proposal locations through T. This conditioning does not expose Kraus
measurement outcomes, and the conditioned physical map remains CPTP: it is
the ordered composition of the assigned local channels. The schedule law is
independent of the logical/reference input.

Construct one envelope, starting healthy, using the old-state sweep map at
every ideal correction clock. At every fault proposal, infect the complete
fixed box containing both sector boundary supports of EVERY Pauli on its
patch. This envelope and its coarse flags depend on proposal locations alone.

Fix a schedule whose envelope never has a macroscopic syndrome component under
the original whole-slab criterion. Expand every Kraus operator of every local
fault channel in its finite local Pauli basis. For a fixed full Kraus record,
including the C_v records and final recovery syndrome, this gives a finite
linear combination of Pauli histories. At an ideal correction Kraus, a
definite Pauli error makes its syndrome projector either zero or scalar one.
Every nonzero summand follows the actual classical sweep rule, with a bounded
local Pauli at each fault proposal. Scalar phases and cancellations are retained.

The SAME proposal envelope dominates all these histories simultaneously.
The fixed decoder and accumulated-homology lemma consequently make every
surviving Pauli summand act as scalar*Id on the entire logical space.
The complete recovered Kraus operator for this record is therefore c_j*Id.
Trace preservation gives sum_j |c_j|^2=1. The conditioned recovered channel
is exactly Id for arbitrary logical/reference inputs.

This is a Kraus-span argument, not an absolute sum of exponentially many
Pauli coefficients. It avoids an exp(constant*L^4*T) normalization loss.
It also does not suppose that correcting selected basis states preserves
logical coherence: each recovered Kraus is scalar on the whole code.

## 3 Probability and topology are still uniform

Fault proposals occur at independent fixed rates, with bounded patch diameter
and bounded number of types per cell. The envelope therefore has homogeneous
bounded-box births; inhomogeneous actual channels do not change that law.
Enlarge the primitive birth guard by the fixed box radius. Its birth-bad
probability is bounded by total proposal rate times slab duration times the
enlarged fixed guard volume. Slow and fast clock flags are unchanged.

The dependence radius remains fixed before b grows. Choose the HT tolerance,
then LSS tolerance, then fixed b, and finally the total small proposal rate.
The uniform forcing, native coarse eroder, stopped finite-torus replay and
whole-slab cover give

    P(bad clock/location schedule through T)
       <= C L^4 (1+kappa*T) exp(-c*L).

A bounded patch Pauli is a bounded 2-chain in each CSS sector. Replacing the
unit event cube by its fixed-width patch makes the decoder transition box
side 2r+O(q), still below rho=L/8 for r=L/32 and sufficiently large L.
Thus the good-schedule statement controls the ENTIRE accumulated error chain
for every Pauli summand, including vanished syndromes and cross-sector errors.

Averaging conditioned schedules gives (1-p_bad)*Id+p_bad*B for a CPTP map B.
The diamond distance is at most 2p_bad, with no logical-dimension factor.
Absorb fixed constants into A,c. The robustness bound follows.

## Why the modification matters

The original correction dissipator is not generally kappa*(C_v-Id) on
cross-syndrome coherences; the explicit inactive jump completes it. A generic
Hamiltonian generator cannot itself be treated as rare positive Pauli faults.
The deliberately included depolarization floor supplies a full-rank Choi
matrix which absorbs that generator perturbation exactly. Removing either
modification loses this particular proof.

The floor is an additional implemented local dissipator, not a free proof
variable. Its rate, patch support and number of Kraus jumps must be charged.
There are still 6L^4 data qubits, fixed cell dimension 64, fixed local support
and rates, and no physical global clock or stored classical controller. The
patch floor may have much larger support and many more jump terms than the
original 24-qubit correction. No device, useful threshold, leakage model,
or noisy preparation/readout theorem is obtained here.

Primary mathematical antecedents: Choi, Completely positive linear maps on
complex matrices (1975), DOI 10.1016/0024-3795(75)90075-0; Knill and Laflamme,
A Theory of Quantum Error-Correcting Codes, arXiv:quant-ph/9604034. The
Pauli-span argument above is written explicitly rather than inferred from a
finite test or a source's abstract. The original memory imports and exact
forcing proof remain pinned in PRINCIPAL_RECONSTRUCTION.md and the audit files.
