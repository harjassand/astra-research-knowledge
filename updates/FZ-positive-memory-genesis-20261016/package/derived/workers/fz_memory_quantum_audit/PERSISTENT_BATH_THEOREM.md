# Universal Pauli schedules correct local interactions with a persistent bath

Independent consequence reconstructed on 16 October 2026. This is a
self-contained finite-dimensional operator proof conditional on a universal
Pauli-history certificate. It is not a new proof of the classical sweep tail,
a claim of historical novelty, or a theorem for unrestricted continuous baths.

## Statement and exact hypotheses

Let M be a finite qubit memory, L a logical Hilbert space, V:L -> M an encoding
isometry, and Dec:M -> L a fixed CPTP recovery with Kraus operators D_s.
Fix a finite proposal schedule h. It specifies the ordered locations of ideal
correction proposals and fault proposals, and the memory patch A_i of each
fault proposal. The schedule does not specify quantum Kraus outcomes.

Each ideal correction proposal has Kraus operators Q_j Pi_j, with the
following properties on every encoded Pauli orbit E V:

* Pi_j is a stabilizer-syndrome projector or a sum of such projectors;
* Pi_j E V is either zero or E V;
* every surviving Q_j is precisely the legal deterministic Pauli correction
  selected by that syndrome; an inactive Kraus may have Q_j=I;
* the correction channel is CPTP on the full memory Hilbert space.

The completed sweep channels in the producer packet satisfy these properties.
The seven original active Lindblad jumps, without completion, are not being
identified with such a channel on arbitrary syndrome coherences.

Call h universally correctable if, for EVERY choice of one Pauli P_i supported
on A_i at EVERY fault proposal, every surviving ideal-correction Kraus record
obeys

    D_s E_final V = c_(s,history) I_L.                         (B1)

Here E_final is the entire accumulated Pauli history, including all surviving
ideal corrections and their phases. A final syndrome projector may kill a
history, in which case c=0. The same Dec and its same Kraus representation are
used for every choice. In the sweep application, the location-only support
envelope and accumulated-homology induction are sufficient for (B1).

Let B be an arbitrary finite-dimensional persistent bath. At each fault
proposal allow an arbitrary CPTP channel on A_i tensor B, extended by identity
on all other memory qubits. The same B can be reused at every proposal and at
arbitrarily distant memory locations. Between proposals, arbitrary bath-only
CPTP evolution is also allowed. The fault actions may depend causally on the
past classical proposal schedule and on any record stored in B. Quantum
measurements with feedforward are included when their records are retained in
B or averaged as part of the full CPTP action. No operation acts on a designated
untouched reference R.

**Theorem.** If h is universally correctable, the recovered joint channel is
exactly

    Gamma_h = Id_L tensor Lambda_(B,h)                         (B2)

for a CPTP bath channel Lambda_(B,h). This equality is an equality of linear
maps on ALL operators on L tensor B. It holds for initially correlated or
entangled L,B inputs, and after tensoring with identity on an arbitrary R.
No product-state assumption is required for (B2).

## Proof with operator-valued Pauli coefficients

Choose Kraus representations for all channels in the fixed proposal circuit.
For a fault Kraus operator F_(i,j) acting on A_i tensor B, the Pauli operators
on A_i are a basis of its full operator space. Thus, exactly,

    F_(i,j) = sum_(P on A_i) P tensor B_(i,j,P),               (B3)
    B_(i,j,P) = (1/d_i) Tr_(A_i)[(P^dagger tensor I)F_(i,j)],

where d_i is the patch Hilbert dimension. The coefficients are bath operators,
not scalar probabilities. In particular, coefficients at different times need
not commute. A bath-only Kraus operator simply contributes another bath factor.

Fix a full Kraus record alpha of the proposal circuit and final decoder.
The recovered Kraus operator from L tensor B to L tensor B is

    A_(h,alpha)
      = (D_s tensor I_B) W_N ... W_1 (V tensor I_B).           (B4)

Expand only the fault factors in (B4) by (B3). Keep bath factors in their exact
chronological multiplication order. In each summand, the memory starts as V
and then follows a definite Pauli orbit. At an ideal correction, its syndrome
projector either kills that summand or acts as one on its whole logical space.
Therefore each surviving summand is a legal Pauli history on h. By (B1), its
decoded memory factor is a scalar times I_L. Consequently

    A_(h,alpha) = I_L tensor B_(h,alpha),                     (B5)

where B_(h,alpha) is the actual ordered sum of the bath-operator products,
including all Pauli phases and cancellations. There is no absolute summation
of coefficients and no interpretation of (B3) as a positive Pauli mixture.

The encoded proposal circuit followed by the full decoder is CPTP on L tensor
B. Its Kraus operators obey

    sum_alpha A_(h,alpha)^dagger A_(h,alpha) = I_L tensor I_B.

Substitute (B5):

    sum_alpha B_(h,alpha)^dagger B_(h,alpha) = I_B.            (B6)

These are the Kraus completeness equations of a CPTP bath channel. Equations
(B5)-(B6) prove (B2), including on all cross terms of any joint logical-bath
input. They also prove the result after adjoining an arbitrary untouched R.

The bath dimension does not enter this argument or its probability constants.
The elementary statement is proved for every finite bath dimension, with no
uniform dimension bound. Infinite-dimensional baths would require separate
domain and convergence bookkeeping and are not asserted here.

## Why the same envelope bounds every coherent branch

The input-independent support claim can be formulated without pretending that
a coherent state has one classical syndrome history. Let eta(h_prefix) be the
envelope obtained from the proposal locations, infecting at a fault proposal
the union of syndrome vertices of ALL Paulis on its memory patch. At ideal
correction proposals use the prescribed old-input monotone sweep update.

Assume the one-event support-domination lemma for every even syndrome cycle.
Induction then puts every Pauli summand of every prefix of (B4) inside this
same eta. Define

    P_eta = sum_(s: syndrome support(s) subset eta) P_s.

For every Kraus prefix W and every bath input,

    (P_eta tensor I_B) W (V tensor I_B) = W (V tensor I_B).   (B7)

Thus all resulting quantum states are supported on the direct sum of the
allowed syndrome spaces. They may contain coherences between those spaces.
Equation (B7) is the precise state-independent quantum support statement; it
does not assert a positive Pauli CTMC for coherent faults. The usual quantum
fault has no unique realized Pauli branch.

The full accumulated-homology argument is still needed for (B1). A small
current syndrome is insufficient: a completed logical membrane can have zero
syndrome. The common decoder, local transition-box identity, and induction
from initial identity are what exclude such accumulated logical errors on a
good proposal schedule.

## Averaging schedules and initial bath correlations

Now sample h from the fresh independent Poisson proposal law used by the
classical envelope theorem. This law is independent of the initial joint
L,B,R input and of all quantum outcomes. Let Good_T be ONE location-only event
on which every h is universally correctable, and let

    p_bad(T) = P(h not in Good_T).

The fault channel at a mark may be any causal function of the prior classical
schedule. This changes the conditional circuit, but it does not change the
Poisson location law or the envelope. Its quantum action may have arbitrary
temporal and spatial correlations mediated by the persistent B. Freshness is
required for proposal locations, not for the bath's quantum state or its action.

On a good h, taking the bath partial trace in (B2) gives

    Tr_B Gamma_h = Tr_B,

as maps L tensor B -> L. On a bad h, both Tr_B Gamma_h and Tr_B are CPTP.
Therefore the averaged joint channel Gamma_T satisfies

    || Tr_B Gamma_T - Tr_B ||_diamond <= 2 p_bad(T).          (B8)

The norm in (B8) has joint input L tensor B. Equivalently, for every initially
correlated density operator rho_LBR,

    || Tr_B[(Gamma_T tensor Id_R)(rho_LBR)] - rho_LR ||_1
         <= 2 p_bad(T).                                      (B9)

This is the correct statement when the initial bath is correlated with the
logical input. One must not silently invent a state-independent channel from
L alone by assigning a different correlated bath state to each logical input.

If a fixed initial bath state sigma_B is independent of L,R, then preparation
rho_LR -> rho_LR tensor sigma_B is CPTP, and (B8) yields the conventional
logical-channel statement

    || Lambda_(L,T,sigma_B) - Id_L ||_diamond <= 2 p_bad(T).   (B10)

If the supplied classical support theorem gives

    p_bad(T) <= C L^4 (1+kappa T) exp(-c L),

the same estimate, capped at 2, follows in (B8)-(B10), uniformly over all the
fault channels and all finite bath dimensions allowed above. The classical
probability estimate has not been independently established in this file.

## Exact boundary of the extension

This is a sparse scheduled interaction theorem. It includes quantum memory
of earlier faults, a common bath interacting with many memory patches, initial
logical-bath entanglement, and outcome-dependent actions implemented as a full
CPTP map with a bath record. The patch diameter, type count and charged total
proposal rate remain fixed as in the envelope theorem.

It does not supply a theorem for unrestricted continuous memory-bath coupling,
state-dependent proposal locations, hidden extra interactions on unscheduled
memory qubits, missing ideal correction proposals, leakage, or any fault which
touches R. Changing the location law to a process with correlated increments
can destroy the fresh-slab probability proof. A uniform rate upper bound alone
has not been used as a substitute for that proof here.

For a fixed h the factorization proof would even hold for prechosen
future-dependent action assignments. The operational stochastic theorem uses
causal assignments so that a physical process is specified. Neither version
allows quantum outcomes to alter the charged location schedule.

Individual terminal errors being invertible with error-dependent recoveries
is insufficient. For example, on an unencoded qubit, I and Z each have an
inverse chosen after learning the error; that fact does not make their coherent
span correctable by one fixed decoder. Here (B1) supplies a common decoder
for the same compositional Pauli-history span. It entails the cross-error
Knill-Laflamme identities directly: if A_p are its physical history operators,
then inserting the decoder completeness relation gives

    V^dagger A_p^dagger A_q V
      = sum_s (D_s A_p V)^dagger(D_s A_q V)
      = [sum_s conjugate(c_(s,p)) c_(s,q)] I_L.              (B11)

The relation between a correctable operator span and arbitrary environment
coefficients is established quantum error-correction mathematics. The direct
proof above is the basis for this consequence, and no historical originality
is inferred. For primary background, see
[Knill and Laflamme, Theorem 3.2](https://arxiv.org/html/quant-ph/9604034v1).

## Finite diagnostic and unresolved obligations

The independent script `check_quantum_audit_exact.py` constructs a [[5,1,3]]
code and its full fixed CPTP decoder, applies two rational coherent joint
interactions to the same memory qubit and persistent bath qubit, and inserts a
selective completed syndrome correction between them. All 32 recovered Kraus
records are checked exactly to equal I_logical tensor B_record; the B_record
adjoint products sum to I_bath. This corroborates that one finite circuit,
including noncommuting bath coefficients. It is not a universal proof or a
check of the 4D stochastic lifetime.

Still required for a full memory theorem are the classical universal schedule
tail, whole-slab control at every event, fixed decoder topology, and the exact
ideal initialization/correction/readout assumptions. Historical priority,
external validation, bath acquisition, reservoir engineering, energy/reset
costs, physical placement and practical performance remain UNKNOWN.
