# Independent audit of the modified CPTP proposal and depolarizing-floor construction

Date: 16 October 2026. This is a third, separate audit requested by the root
investigator. It uses no other worker's conclusion as a premise. The original
trajectory verdict is in `REPORT.md`; the narrower structured-Pauli extension
is in `STRUCTURED_FAULT_EXTENSION.md`.

## Verdict

**The proposed construction's additional operator steps are valid.** I
independently reconstructed the exact CPTP correction proposal map, its
constant-rate no-jump representation, universal good-history Kraus-span
recovery, the normalized Choi norm bound, and the local depolarizing-floor
absorption of small trace-annihilating Hermiticity-preserving perturbations.
No counterexample was found under the precise conditions below.

The result is conditional on the same base classical block/cluster/finite-torus
argument as the original memory candidate. It supplies a robustness argument
for a **deliberately modified and regularized generator**. It does not establish
robustness of the unmodified original sweep generator. The two differ on
coherences between syndrome sectors, despite having the same original Pauli
trajectory law.

The indispensable quantifier is that a *single location-and-clock-only good
event* certifies correctness for **every** sequence of Pauli actions on the
fault patches. A small failure probability separately for each chosen Pauli
error sequence would not by itself support the coherent extension. Here the
universal event follows from an envelope which births the union of all
possible local Pauli syndrome supports at every fault proposal.

## 1. Full correction-channel identity, including no-jump terms

At one ideal sweep vertex, let `Pi_O` be the seven orthogonal active local
syndrome-pattern projectors and `Q_O` its one/two-face correction Pauli. Set

    A_v=sum_O Pi_O,        Pi_0=I-A_v,
    C_v(rho)=sum_O Q_O Pi_O rho Pi_O Q_O^dagger + Pi_0 rho Pi_0.             (C1)

Both `A_v` and `Pi_0` are projectors. The Kraus operators in (C1) obey

    sum_O (Q_O Pi_O)^dagger(Q_O Pi_O)+Pi_0^dagger Pi_0
        =sum_O Pi_O+Pi_0=I.                                              (C2)

Thus `C_v` is CPTP on the entire physical Hilbert space, not only on states
with definite syndrome. Its support is the same at-most-24-qubit star as
the original correction. No commutation of `Q_O` with `Pi_O` is needed.

Since the Kraus rate operator is identity,

    kappa(C_v-Id)
       =kappa sum_O D[Q_O Pi_O]+kappa D[Pi_0].                            (C3)

This is an exact equality of superoperators on all operators. The original
vertex term is only the first sum. The difference is syndrome dephasing:
`D[Pi_0]=D[A_v]`. It is zero on every definite-syndrome density operator.
Consequently the modified generator has the same independent-attempt
classical Pauli law from a code-space input under Pauli faults.

It is *not* equal to the original generator on arbitrary syndrome coherences.
For coherence between one active and one inactive syndrome, the original
vertex term damps at rate `kappa/2`, while the modified term damps at
`kappa`. This explicit difference prevents treating the modification as
an already established property of the original dynamics.

For any CPTP channel `Phi` with Kraus operators `B_j`,

    gamma(Phi-Id)=sum_j D[sqrt(gamma) B_j],
    sum_j gamma B_j^dagger B_j=gamma I.                                  (C4)

Its no-jump propagator is `exp(-gamma t/2) I`; it has an exact independent
rate-`gamma` Poisson channel-proposal representation. Applying `Phi` at
those proposal times reproduces `exp[t gamma(Phi-Id)]`.

More generally, for finitely many correction and fault streams on a finite
torus, let their CPTP maps be `Phi_i` and rates `gamma_i`. Independent
Poisson proposals, applying maps in chronological order, have generator
`sum_i gamma_i(Phi_i-Id)`: in time `dt`, zero proposals have probability
`1-sum_i gamma_i dt+O(dt^2)`, one proposal of type `i` has probability
`gamma_i dt+O(dt^2)`, and two or more have probability `O(dt^2)`.
This calculation proves the exact finite-dimensional master equation.

The full effective no-jump rate operator is

    [2 kappa L^4 + sum_fault_patches gamma_x] I.                          (C5)

It remains scalar for states with coherent superpositions of syndromes and
for arbitrary reference entanglement. This is the clean quantum
uniformization furnished by the modification.

## 2. Arbitrary local CPTP faults at fresh Poisson locations

Consider

    L_mod=sum_(primal/dual v) kappa(C_v-Id)
          +sum_x gamma_x(Phi_x-Id),                                     (C6)

where each `Phi_x` is an arbitrary CPTP map on a bounded qubit patch,
tensored with identity on the rest of the memory. Fault proposal streams
are fresh independent Poisson streams. The patch range and the sum of
proposal rates per fine owner cell are bounded independently of `L`.
All environments are represented by these memoryless local channels.

Fix one complete proposal history `omega` up to storage time `T`: all
correction/fault locations, types and times, but **no Kraus outcomes**.
Almost surely it is finite. The conditional physical map is a finite
composition of CPTP maps. Encoding followed by that composition and the
fixed decoder is therefore CPTP for each `omega`.

For the envelope in each sector, at each fault proposal set occupied every
vertex that could belong to the syndrome boundary of *any* Pauli string on
the fault patch. A fixed-radius ball containing the patch boundary supports
is a sufficient overcount. Correction proposals use the same ideal
old-state sweep envelope map.

The deterministic support inclusion and block flags in the narrower
extension now give a universal statement:

    For a fixed omega in Good_T, every sequence of local fault Paulis
    on its patches, interleaved with its ideal correction attempts,
    has trivial decoded residual homology at time T.                    (C7)

Why the quantifier is valid: the envelope and primitive good flags depend
only on `omega` and the patch balls. The birth map dominates every allowed
Pauli on that patch at once. The correction domination is pathwise for
every current cycle. Induction therefore uses the same envelope for all
sequences; it does not average over a chosen Pauli distribution.

The base guard argument, if correct, bounds the probability of this one
universal bad event by

    P(omega not in Good_T)
        <= C L^4(1+kappa T) exp(-cL)                                    (C8)

when the total patch-proposal rate budget is sufficiently small relative
to `kappa`. Enlarged fixed balls and guards change constants. There is
no Kraus-rank or Pauli-coefficient factor in the proposal rate in (C8).

## 3. Kraus-span recovery on a fixed good proposal history

The following is the central independent reconstruction.

Choose Kraus operators `B_(x,j)` for each fault channel. Since each is
supported on a bounded qubit patch, it has a finite Pauli expansion

    B_(x,j)=sum_(P on patch) b_(x,j,P) P.                                (C9)

Choose also a Kraus index for each correction proposal in (C1), and a final
decoder syndrome index `s`. The resulting decoded logical Kraus operator
is a product of the fault/correction Kraus operators with the encoding
isometry `V` on its right and

    K_s=V^dagger R_s P_s                                                (C10)

on its left. Expand only the fault factors using (C9).

In a fixed Pauli summand, starting from `V`, each intermediate state has a
definite syndrome. A correction factor `Q_O Pi_O` either vanishes or acts
as `Q_O`; the inactive factor `Pi_0` either vanishes or acts as identity.
The selection is independent of the logical input. Every surviving summand
is therefore precisely a valid deterministic sweep trajectory for that
sequence of local fault Paulis at the proposal times. Products of Paulis
carry only scalar phases beyond their binary labels.

If `omega` is good, (C7) states that its final decoded residual is a
stabilizer for *all* surviving Pauli summands. The final syndrome projector
in (C10) either kills a summand or selects its syndrome. Therefore each
summand of the recovered Kraus operator equals a scalar times the full
six-qubit logical identity:

    K_s [one surviving Pauli-history summand] V = c I_logical.           (C11)

Summing the complex coefficients in (C9) preserves this conclusion. Every
recovered Kraus operator for this fixed good `omega` is of the form

    L_(omega,alpha)=c_(omega,alpha) I_logical.                            (C12)

The entire conditional map for `omega` is CPTP, so Kraus completeness forces

    sum_alpha |c_(omega,alpha)|^2=1,
    Lambda_omega=Id.                                                    (C13)

This proves exact correction of coherent rotations, amplitude damping,
local measurements and all other CPTP qubit faults supported on the
certified patches. It also proves preservation of arbitrary reference
entanglement, since (C12) is an operator identity on the whole logical
space and tensors with identity on the reference.

There is no absolute summation of Pauli expansion coefficients, no
interpretation of complex coefficients as probabilities, and no
approximation of a coherent error by a Pauli twirl. Interference remains
inside the scalar coefficients in (C12); trace preservation normalizes
their squared moduli. The potentially enormous expansion is a proof device,
not an implemented computation.

Two essential restrictions:

1. Conditioning here is on the external *proposal* history. Conditioning on
   Kraus outcomes would generally produce trace-decreasing maps and would
   invalidate the trace-preservation inference in (C13).
2. The final decoder must be the same for all Pauli choices and histories.
   A separate recovery chosen after inspecting each Pauli term would not
   prove (C11) for the fixed decoder. The canonical component-filling
   decoder and its eventwise homology invariance provide the common choice.

Averaging (C13) over the independent classical proposal law gives

    Lambda_T=P(Good_T) Id+P(Bad_T) B_T,                                  (C14)

where `B_T` is CPTP if its coefficient is nonzero. Hence

    ||Lambda_T-Id||_diamond <= 2 P(Bad_T).                               (C15)

Unlike the earlier exact Pauli-channel case, the bad component here need
not be a Pauli channel, so equality with `2P(Bad_T)` is not asserted.

This is the error-correcting linear-span principle in an explicitly
history-dependent setting. The standard background is the original
[Knill–Laflamme paper](https://arxiv.org/html/quant-ph/9604034v1);
equations (C9)–(C13) are the full proof needed here.

## 4. Depolarizing floor and Choi normalization

Fix a bounded patch of Hilbert dimension `d` and its completely depolarizing
channel `D(A)=Tr(A) I/d`. Let `E` be a linear Hermiticity-preserving,
trace-annihilating map on that patch:

    E(A^dagger)=E(A)^dagger,        Tr E(A)=0 for every A.                 (C16)

Use the **normalized** Choi matrix

    J(F)=(F tensor id_d)(|Omega_d><Omega_d|),
    |Omega_d>=d^(-1/2) sum_i |i,i>.                                     (C17)

Directly,

    J(D)=I_(d^2)/d^2,
    J(E)=J(E)^dagger,
    Tr_output J(E)=0.                                                   (C18)

The diamond norm definition gives

    ||J(E)||_infinity <= ||J(E)||_1 <= ||E||_diamond,                     (C19)

because the input Choi state has trace norm one. There is no additional
factor of `d` in (C19) with convention (C17).

Assume

    ||E||_diamond <= nu/d^2.                                           (C20)

Then the map

    Psi=D+E/nu                                                         (C21)

has

    J(Psi) >= [1/d^2-||E||_diamond/nu] I >=0,
    Tr_output J(Psi)=I/d.                                              (C22)

These conditions imply that `Psi` is CPTP. To reconstruct rather than
merely name the implication: diagonalize the positive Choi matrix as
`sum_j |v_j><v_j|`, reshape `sqrt(d) v_j` into Kraus matrices `B_j`, and
compare matrix units in (C17). This gives `Psi(A)=sum_j B_j A B_j^dagger`.
The partial trace condition gives `sum_j B_j^dagger B_j=I`.

Consequently the exact generator identity is

    nu(D-Id)+E = nu(Psi-Id).                                            (C23)

The right side is a fresh rate-`nu` local CPTP proposal stream of the type
in (C6). The smallness condition is sufficient and need not be sharp.

For comparison with common conventions, the unnormalized Choi matrix
is `d J`; its depolarizing floor is `I/d` and its perturbation norm is
bounded by `d ||E||_diamond`. The same final condition (C20) results.
Mixing the two conventions would produce a wrong dimension factor.

The standard definitions and complete-positivity/trace-preservation
characterizations were checked in the author's
[Watrous chapter 2](https://cs.uwaterloo.ca/~watrous/TQI/TQI.2.pdf),
Theorems 2.22 and 2.26, and the norm definition in
[chapter 3](https://cs.uwaterloo.ca/~watrous/TQI/TQI.3.pdf), Definition
3.43. The latter uses the unnormalized book Choi convention in other
formulas; this report explicitly uses (C17).

## 5. The resulting regularized generator and local robustness budget

Fix a list of bounded patches, with bounded multiplicity per fine cell,
and deliberately choose low floor rates `nu_x`. Define the nominal model

    L_reg=sum_v kappa(C_v-Id)+sum_x nu_x(D_x-Id).                         (C24)

For arbitrary time-independent, strictly local maps
`E_x=E_x^local tensor id_outside` satisfying (C16) and

    ||E_x^local||_diamond <= nu_x/d_x^2,                                 (C25)

one has

    L_reg+sum_x E_x
        =sum_v kappa(C_v-Id)+sum_x nu_x(Psi_x-Id),                        (C26)

with each `Psi_x` CPTP on its patch. Thus the arbitrary local perturbations
are absorbed into the same low-rate patch proposal budget. The overall
generator remains a legitimate GKSL generator even when a particular
trace-annihilating Hermiticity-preserving `E_x` is not one by itself.

Let at most `m` such patches be owned by each fine cell and let
`d_x<=d_max`, both fixed independently of `L`. With uniform floor rate
`nu`, the guard birth budget is at most `m nu`. If the base proposal
threshold is `epsilon_ell kappa`, choose

    m nu <= epsilon_ell kappa,
    ||E_x||_diamond <= nu/d_max^2.                                      (C27)

This is a strictly positive, size-independent local perturbation radius.
It can be extremely small because `d_max=2^(number of patch qubits)`.
The probability estimate depends on proposal rate and patch range, not
on the number or sizes of coefficients in a Kraus/Pauli expansion.

Examples of perturbations included:

* For `E_x=-i[H_x,.]`, `||E_x||_diamond<=2||H_x||_infinity`; thus
  `2||H_x||_infinity<=nu_x/d_x^2` is a sufficient Hamiltonian condition.
  Subtracting a scalar from `H_x` can improve this bound.
* For a local dissipator, `||D[L_x]||_diamond<=2||L_x||_infinity^2`.
  The first completely positive term contributes at most `||L_x||^2`
  and its two anticommutator terms together contribute at most the same.
  A sum/difference of local GKSL terms can be grouped into (C16) and
  bounded by the triangle inequality.

This is not the global Duhamel estimate `T||sum E_x||_diamond`. The floor
conversion obtains a genuinely local fresh-proposal representation and
then uses the universal spatial/time event certificate. That is why the
argument can retain an exponentially long lifetime at a fixed sufficiently
small *per-patch* perturbation strength, subject to the base tail theorem.

If the base classical proof is correct, the mathematical consequence for
`L_reg+sum E_x` is the same form

    ||Dec_L exp[T(L_reg+sum_x E_x)] Enc_L-Id||_diamond
       <= min(2,A L^4(1+kappa T)exp(-cL)),                               (C28)

for `L=bM` and sufficiently large `M`, uniformly over the local perturbations
in (C25)–(C27), with exact initialization and ideal readout.

## 6. What changes, what remains open, and potential failure modes

The nominal model in (C24) has two deliberate additions relative to the
original sweep theorem:

1. one inactive-syndrome dephasing jump `sqrt(kappa) Pi_0` at every primal
   and dual correction vertex;
2. low-rate complete depolarization on each prescribed perturbation patch.

The first changes seven to eight ideal correction Kraus/jump terms per
vertex and sector, or `16L^4` listed ideal jump terms. Its support remains
at most 24 qubits. The floor channel, or its absorbed `Psi_x`, has local
Kraus rank at most `d_x^2`, a fixed constant for each bounded patch. Storage
still uses `6L^4` data qubits; no global schedule or classical memory layer
is added. These are algebraic model resources, not fabricated channels.

The original unmodified generator has state-dependent no-jump evolution on
syndrome superpositions. It cannot simply inherit (C5) or the conditional
CPTP proposal-history proof. The extra dephasing in (C3) is essential to
the particular proof given here. This does not prove that original-generator
robustness is false; it leaves that separate problem open.

The following would invalidate the proof as stated:

* a good event based on the *realized* syndrome or a selected Pauli fault,
  without a universal location-only certificate;
* conditioning on Kraus outcomes while claiming the conditional map is TP;
* a final recovery selected separately for different Pauli terms;
* a fault patch range or patch multiplicity growing with `L` without a new
  scaling analysis;
* noise with memory or adversarial proposal correlations which destroys the
  fresh block increments used in (C8);
* leakage outside the fixed qubit Hilbert space, or perturbations that act
  on the external reference;
* perturbation pieces which are not individually trace annihilating and
  Hermiticity preserving, unless they can first be regrouped into bounded
  local pieces with those properties;
* dropping the dimension-dependent Choi margin or using an averaged
  state-dependent rate in place of a uniform local bound.

The remaining mathematical dependencies are the original uniform block
forcing, correct infinite-volume cluster comparison, stopped finite-torus
replay and whole-slab control, now with fixed enlarged patch guards. The
universal envelope argument and all the additional quantum/floor steps
are supplied above. Historical novelty, external formal certification,
physical 3D realization, preparation, conditioned-channel fabrication,
reservoir/reset/energy/calibration costs, and noisy readout remain unacquired.

## 7. Exact checks and reproduction

Run:

    python3 research/2026-10-16-adversarial-quantum-memory/trajectory/check_cptp_regularization_exact.py

The saved `CPTP_REGULARIZATION_CHECKS.json` records:

* the full correction-proposal superoperator identity on all 16 matrix
  units of a two-qubit example with two active orthogonal patterns and
  one inactive aggregate; the differing active/inactive coherence rates
  are checked explicitly;
* a full `[[5,1,3]]` code isometry and CPTP syndrome decoder, correcting
  all 16 single-Pauli error syndromes;
* exact scalar-identity recovery Kraus operators for a coherent unitary
  `(3I+4iX)/5`, amplitude damping with `K_0=diag(1,3/5)` and
  `K_1=4|0><1|/5`, and their two-fault composition on one correctable patch;
  the scalar squared moduli sum to one in each case;
* a qubit Choi-floor example at the proposed bound:
  `nu=1`, `H=X/8`, `||-i[H,.]||_diamond=1/4=nu/d^2`.
  The normalized `J(Psi)` spectrum is `1/8,1/4,1/4,3/8`, with output
  partial trace `I/2`. The diamond norm here is exact: the upper bound
  `2||H||=1/4` is attained on `|0><0|`, whose commutator has trace norm
  `1/4`;
* a countermodel to discarding the margin: at `H=X/2`, the normalized
  Choi spectrum is `-1/4,1/4,1/4,3/4`, so `D-i[H,.]` is not CP.

All matrix arithmetic uses Gaussian integer pairs and cleared denominators.
No floating-point tolerance, stochastic simulation, absolute coefficient
estimate or empirical lifetime inference is involved. These are finite
checks of the stated examples; the general proof is (C1)–(C28).
