# Coefficientwise Pauli-history compiler and initialization/readout interface
2026-10-29. New composition lemma after the forest-gauge audit; independent exact-version review pending.

## 1. Why Pauli expansion preserves the good-source certificate
In the forest-gauge frame every owner-good projector is

   P_h = I_DATA tensor Q_h,

where Q_h requires the appropriate clock/ownership consistency and workspace zero (and is zero in abort phases). This is true on the ENTIRE augmented Hilbert space, not merely a particular input state. It follows because on a consistent C_t block the mask is all-owned and the gauge is exactly the clean prefix V_t; A/Q gauges are identity. Other frame factors commute with the projector and cancel.

Suppose an actual instrument Kraus operator A preserves an owner-good sector:

   (I−Q_h) A Q_h=0.

Expand A in the linearly independent Pauli basis on its DATA support D_X:

   A=sum_P P_DATA tensor B_P.

The controller projectors do not act on DATA. Consequently

   0=sum_P P_DATA tensor [(I−Q_h) B_P Q_h]

implies (I−Q_h) B_P Q_h=0 for EACH P. The same argument applies to an output-range condition (I−Q_h) A=0, such as a complete terminal/abort regeneration. Thus the support/mark invariants hold coefficientwise, not just after coherent cancellations in the physical channel.

No Pauli twirl or probability interpretation is assigned to the B_P. They are retained-controller/bath operators and may have arbitrary interference and memory.

## 2. Actual record histories become the required serial Pauli histories
Fix only a finite actual kick/reset/monitor record, with a Kraus refinement where needed. In the exact transformed evolution:

* all inter-event no-jump, monitor, commit/ready/cleanup and A/Q refresh operators act only on controller/bath;
* each dressed physical kick is a bounded-support joint DATA/controller operation;
* each marked terminal/abort is a bounded-support joint DATA/controller operation;
* every unmarked terminal is the intended recovery instrument tensor a controller source/reset factor.

Expand only the dressed kicks and marked DATA emissions in DATA Paulis. The preceding coefficientwise lemma guarantees that every unmarked terminal still has a good source in every nonzero expansion term. Hence its exact intended-instrument identity can be used along that term, rather than only after summing all terms.

When the chosen intended recovery is the SSF syndrome-measurement/conditional-Pauli instrument, its Kraus operators have the form

   K_y = F_y Pi_y,

where Pi_y is a projector onto the measured local stabilizer syndrome and F_y is the declared accepted Pauli correction, or identity if no candidate is accepted. Separate classical choice labels may be retained if there are several choices. On a Pauli error E applied to an encoded state, Pi_y selects the syndrome determined by E, independently of the logical state. Thus every nonzero coefficient follows a definite current-syndrome Pauli history in the actual terminal order. Correct corrections obey the declared SSF rule; local Pauli terms from kicks/marked emissions are the bad events.

Arbitrary coherent controller dynamics between these events can change the coefficient operators, but cannot add a DATA Pauli or change a branch's syndrome. Pauli terms can have zero coefficients; this only removes histories. No independent schedule distribution or normalized record-conditioned DATA channel is introduced.

This establishes the semantic serial-history interface needed by a deterministic SSF witness, **provided** the compiled Phi_h actually implements the declared SSF instrument with complete read footprint and acceptance rule. It does not prove the probabilistic fault-mass bounds or the deterministic witness itself.

## 3. A common record envelope, not branch probabilities
The marked emission and good-service record majorants used by the physical-window analysis must dominate ALL these coefficient histories simultaneously. They do: marks depend only on kick support and actual reset records; unmarked sources are good coefficientwise; conservative no-service cells depend only on resets and affecting-kick records. A witness union over fixed spatial/time sets therefore need not union over Pauli labels or assume Pauli expansion coefficients are probabilities.

To derive a logical channel bound, the safe-record event must ensure every compatible Pauli coefficient is corrected by the SAME fixed final recovery. Then each safe Kraus operator restricted to the logical codespace is I_logical tensor a bath/record operator, up to scalar phases absorbed into that operator. This is the correctable-span step; it must be proved from the deterministic witness and common record envelope, not assumed from marginal Pauli tails.

### Input-dependent scheduler records do not invalidate the final norm step
With the fixed initial bath/controller preparation below, the safe decoded CP map is c times the logical identity for a scalar 0≤c≤1, because its Kraus operators are I_logical tensor bath/record operators. This conclusion is algebraic; it does not assume the noisy schedule was independently sampled. Completeness of the full decoded channel makes the complementary bad effect (1−c)I_logical. If the common bad-record CP instrument has the uniform diamond bound delta, then 1−c≤delta and

   ||E_dec−id_logical||diamond≤2 delta.

Thus the comparator's final use of an input-independent exogenous clock schedule can be replaced, for the compiled process, by the exact correctable-span property plus a uniform bad-record effect bound. Neither property follows from marginal liveness alone.

## 4. Explicit clean initialization requirement
A sufficient initialization is:

* DATA in the exact encoded logical input, with arbitrary logical reference;
* every hub at A_0 with workspace zero;
* every resource lock free;
* monitor and retained-bath initial state fixed independently of the logical input (arbitrary mutual bath/controller correlations are allowed if the preceding fixed pure controller conditions remain satisfied).

The forest frame is identity on this initial A_0 sector, every history is good, and every classical analysis mark is zero. This is a memory theorem starting from an encoded state, not an encoding/preparation theorem.

Arbitrary corrupted initial controllers are NOT covered merely because they later regenerate. They can enact DATA damage before regeneration, and F† can turn their initial state into an extensive dressed error. Such an initialization needs an explicit sparse initial-fault/mark hypothesis or a separately proved safe initialization protocol. Full-state liveness does not protect an encoded input from arbitrary initial controller corruption.

## 5. Actual finite-time decoding convention
At any deterministic observation time t, the exact dressed state is obtained by applying F† to the full physical DATA/controller state. The declared final mathematical decoder is

   physical state -> F† -> sectorwise fixed minimum-syndrome Pauli recovery -> logical decoding,

with controller/bath traced only after the desired output instrument is formed. The first step is bounded-depth graph-local with fixed support; the minimum-syndrome decoder is a global ideal readout map and is not claimed efficient, local, autonomous, or already physically implemented.

This convention handles unfinished clean and marked transactions without waiting for a drain. Reading bare DATA at an arbitrary time is a different channel and is not justified by the dressed theorem. If a physical fault-tolerant implementation of this readout is desired, its gates/noise/resources must be separately compiled and charged. No global recovery is inserted between analysis blocks.

The architecture remains a driven system with maintained reset/monitor resources and graph-local bounded qudit dimensions; none of these statements supplies passive equilibrium storage, fixed-dimensional geometric wiring at constant overhead, or an ideal encoded-state preparation process.
