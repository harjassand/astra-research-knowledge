# Small-write-set native compiler for classical clock repair

Status: new exact algebraic construction; not yet independently reviewed and not a full clock-repair theorem. It addresses a specific circularity of the generic full-footprint compiler: a faulty repair hub need not corrupt every clock that it only reads.

## 1. Channel and physical registers

Let R be a fixed bounded read footprint of classical clock registers C_i, and W⊆R a designated write set. Quantum DATA is untouched outside W. The desired attempted channel first pinches C_R in its declared clock basis, then evaluates a finite classical table, writes clocks only in W, and optionally erases or operates on DATA only in W. On classical inputs this is the intended classical repair. The pinching is part of the actual finite channel, not an idealized continuous dephasing assumption.

Use the accepted ownership acquisition of the FULL footprint R. An acquired read is therefore a serializable snapshot, not an early unprotected guard. Unlike the generic swap-everything synthesis, use the following exact payload.

For each i∈R\W, coherently copy its clock into a fresh hub register r_i by

    U_i = Σ_a |a><a|_(C_i) ⊗ X^a_(r_i).               (1.1)

No quantum DATA or other source register is moved. This is one hub/resource two-site unitary. A controlled Hermitian logarithm implements it with bounded Hamiltonian norm (≤π after fixing duration), independently of the clock alphabet size. All subsequent computation on these copied values is hub-local. Use ordinary hub/resource gates only at W to implement the output. Resolved terminal reset/discard of the copied labels realizes the required pinching. Include the copies in the exact inverse-prefix rollback before any abort discard.

The finite hub dimension grows as a fixed function of |R| and q. It is constant in total computation size once the architecture is chosen; no claim of practical small dimension is made. All physical dissipative resources are the actual onsite resolved resets of the accepted compiler.

## 2. Exact conservation on read-only clocks

For every i∈R\W and basis projector P_(i,a), EVERY nominal payload, inverse-prefix, failed-test, ownership, monitor and reset coefficient of this repair owner commutes with P_(i,a). Clock-independent resource tags do not change this. In particular,

    [H_h,P_(i,a)]=0, [J_(h,s),P_(i,a)]=0,
    L_h^*(P_(i,a))=0.                              (2.1)

This is full-Hilbert algebra, not a clean-prefix expectation. A malformed owner mask can suppress read gates or truncate/abort a prefix, but cannot turn a read-only controlled unitary into a clock-label write.

If an arbitrary fault operator/map acts on the hub or its private workspace, all subsequent nominal h-prefix evolution and every actual retirement instrument remain block diagonal in every read-only clock label. A hub fault may change the conditional channel on W, the hub/bath correlations, and phase/coherence blocks of the read clocks; it cannot transfer population between any of their clock labels. The claim is NOT that the resulting joint map is identity on arbitrary coherent read inputs.

## 3. Classical semantic boundary, including coherent faults

The linearized clean attempted channel explicitly pinches its read clocks before evaluating/writing the classical table. Thus the accepted virtual clock algebra is the diagonal algebra, while the quantum DATA/bath/reference state is arbitrary within each classical block.

A fault supported away from a read-only clock cannot create off-diagonal blocks in that clock from a block-diagonal joint state, because every relevant coefficient is block diagonal in its label. If a prior fault already created coherence at a clock site, that site remains charged to that prior fault. Copying or diagonal conditioning on it does not create clock-label coherence at other initially diagonal read registers. Any next clean attempted channel pinches the read registers as part of its actual terminal channel.

Consequently a dirty retirement of h can be assigned arbitrary **classical clock writes only on W**, plus arbitrary quantum DATA action only on its declared DATA-write footprint, when comparing the classical-clock/quantum-DATA process at clean transaction boundaries. Read-only conditional bath correlations are retained, not replaced by a fresh bath. Actual faults directly touching a read resource remain charged at that physical resource.

This is a semantic support statement. Operator-norm/cavity locality still uses the FULL physical read footprint R; it is not permissible to replace that norm support by W. Nor may one use the support statement before a valid linearization/cut has been supplied.

## 4. What this changes, and what it does not

The generic compiler's hub-swap construction allowed a single hub corruption to change every read clock. Construction (1.1) avoids that unnecessary amplification. A large finite inspection neighborhood can therefore coexist with a small actual write set and a bounded semantic clock-root footprint.

It does not yet solve how a locally inconsistent clock configuration can be healed by a sequence of small-write operations, without uncontrolled retiming, stalls, or corrupted command provenance. A multisite repair that actually writes an entire large neighborhood still has that large write footprint. Splitting such a repair into many small writes needs its own safe handshake/validation proof; a large untrusted shared plan is not supplied for free.
