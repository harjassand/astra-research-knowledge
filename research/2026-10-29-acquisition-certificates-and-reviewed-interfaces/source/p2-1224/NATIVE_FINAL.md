**I constructed a stronger principle: accuracy and regularity can come from different processes.** A protected computation can have a regular logical comparison even when sharp readout makes the uncut physical model’s moments diverge. This lets the proof cover coherent returns involving newly written hidden detector records while keeping readout and feedback in their actual chronological order.

The construction, its control/readout interface, and the missing Bell/T amplitude bridge are now saved with separate scoped reviews.

## The new principle

Let \(F\) be the normalized model with its complete records. Construct an auxiliary process \(A\) by inserting smooth contractions before certain record copies. These contractions are mathematical proof devices; no filtering, postselection, reset or record deletion is performed.

The decisive property is that each contraction acts identically on **every admitted finite protected history**. Consequently, both processes share the same finite approximation \(T_k\), with rigorous remainder bounds

\[
\|F-T_k\|\le E_k,\qquad \|A-T_k\|\le E_k.
\]

The auxiliary process has the moments needed for regularity renewal. Its supported logical average can then be normalized on the original input, using \(F\) as the normalized anchor. This produces a regular logical isometry \(V\) satisfying

\[
\boxed{\|F-V\|\le 4E_k.}
\]

The proof never requires the actual postmeasurement state to recover finite moments. Its unbounded insertions act on qualified finite reference histories, followed by a norm-bounded actual suffix.

This is more than agreement of formal Taylor coefficients. A saved continuum counterexample has identical coefficients at every order while the two processes differ at every nonzero exposure. The finite remainder is what makes the comparison legitimate.

The full construction is in POSTRECORD_COMPARISON_DYNAMICS.md[POSTRECORD_COMPARISON_DYNAMICS.md](producer-workspace/POSTRECORD_COMPARISON_DYNAMICS.md).

## What it newly admits

The earlier retiming route required compatibility with every newly written label-bearing register. The new chronological construction admits, for example,

\[
H_1(t)=\kappa(t)\,p_Rq_B\otimes X_E,
\qquad
H_2(t)=\lambda(t)\,q_Rp_B\otimes Z_E,
\]

where \(R\) is the retained pointer, \(B\) the computational mode, and \(E\) a newly written hidden detector copy. The hidden copy changes, and its two coefficient operators do not commute.

The new logical bridge transports those coefficients **forward** through later reference operations, preserving their order. It never pushes them backward through the measurement that created \(E\). The complete finite history retains the intended Bell/T logical factor.

That conclusion has substantive boundaries:

- Every register actually used for later control must satisfy the faithful-selector or explicit transport condition.
- A hidden register cannot silently become a fresh source, detector target or clean control workspace.
- The actual classical-report boundary remains acquired and retained. An additional untouched reporting copy supplies one explicit example.
- Every returned oscillator remains explicit through its last declared unbounded interaction.

Exact checks retain the physical T phases and all incoming Pauli frames across **28 Bell and 112 T complete input columns**. They also reproduce logical failure when the wrong register controls correction.

The amplitude construction is in FORWARD_MEMORY_ROW_LEMMA.md[FORWARD_MEMORY_ROW_LEMMA.md](producer-workspace/FORWARD_MEMORY_ROW_LEMMA.md).

## Controls and readout are included at the correct boundary

A further issue was necessary to resolve: calibration bounds cannot be evaluated on an irregular sharp-record prefix whose required moments may diverge.

The acquired implementation \(W\) is therefore compared directly with the regular auxiliary process. Calibration, initialization and control estimates use its regular prefixes. The comparison retains actual suffixes, complete workspaces, detector purifiers, flags and physical timing.

For a round with \(c_r\) comparison cuts and \(m_r\) acquired guarded meters, the resulting sufficient allowance is

\[
\|W_r-V_r\|
\le
(4+c_r+2m_r)E_{r,k}
+\sum_j\bigl(\epsilon_{\mathrm{alg},j}
+\epsilon_{\mathrm{control},j}\bigr)
+\text{other acquired allowances}.
\]

The meter guard and smooth-cutoff guard require separate support statements. The cutoff must be positive. Each port covers the same physical boundary times and all active systems, including holding during acquisition; late completion needs its actual flag cost or a revised schedule.

These conditions and the calibration bounds are developed in POSTRECORD_ACQUIRED_PORTS.md[POSTRECORD_ACQUIRED_PORTS.md](producer-workspace/POSTRECORD_ACQUIRED_PORTS.md).

## The conventional comparisons changed the construction

The clean parity port now has three distinct comparisons:

| Route | Constructed reach | Remaining cost or distinction |
|---|---|---|
| Coherent majority | Explicit compute/copy/uncompute, with full error \(\sqrt{2p_{\rm bad}}\), including workspace | Coherent processing, initialization, duration and physical faults remain paid |
| Coherent quantum signal processing | Better inverse-gap query scaling under the same known linear signal access | No certified numerical phase schedule or calibrated implementation has been acquired |
| Measured Ramsey tests | Forward-only tests and classical majority; potentially cheaper when the transcript is acceptable | Retains additional information about the fine coordinate and requires its actual measurement/reset interface |

The signal-processing alternative uses established bounded sign-polynomial machinery. Its local construction separately supplies controlled access and the phase-sensitive complete-output bound. Its asymptotic query dependence is \(O(\gamma^{-1}\log(1/\epsilon))\), compared with majority’s \(O(\gamma^{-2}\log(1/\epsilon))\), where \(\gamma\) is the promised signal bias. This does not establish a smaller finite-instance hardware cost. [yuansu.me](https://yuansu.me/publication/qsvt/qsvt.pdf?utm_source=chatgpt.com)

I also preserved the failed three-SUM shortcut: it restores an ancilla’s position but leaves momentum backaction and copies the full analog coordinate. That failure does not exclude more capable encoded-control or measurement-free constructions.

## Scope and saved state

**The completed advance is a proof instrument for protected operations with returning quantum memory.** It removes the requirement that the physical sharp-record trajectory itself remain moment-regular, and it covers a concrete family of newly interacting hidden records that the previous retiming interface excluded.

It does not establish a device threshold or total computing advantage. Fresh-state supply, the calibrated signal primitive, bounded controls, actual reporting, capture, pump discrepancies, reset and whole-lifetime exposure still need their declared physical conditions and error budgets. The comparison remains for a fixed programmed workload.

The domain argument, auxiliary regularity and normalization, logical-row extension, and acquired-port accounting have separate completed reviews. Shared derivations and excluded dependencies are recorded explicitly. Infinite-dimensional claims rest on analytic arguments; the exact finite checks test the algebra.

The usable entry points are README.md[README.md](producer-workspace/README.md), REVIEW_INDEX.md[REVIEW_INDEX.md](producer-workspace/REVIEW_INDEX.md), and REPRODUCE.md[REPRODUCE.md](producer-workspace/REPRODUCE.md). The predecessor proofs, corrections and useful failures remain in place.