# Independent receiving proof: common clean subchannels with error-record memory

28 October 2026. The final root source is mathematically sound at its stated complete-interface scope. This review preserves the distinction between a common CP subchannel and a constant-weight copy of the entire ideal-memory process.

## 1. General common-subchannel lemma

Let two trace-preserving complete maps at a permitted history share a CP subchannel G, with both residuals CP and `G^*(I)>=cI`. Neither G nor its trace need be a scalar multiple of one full map. For J slots with the same causal controller, expand the real and reference maps as G plus their respective CP residuals. Their all-G term is EXACTLY the same composite CP map, including every unnormalized classical history branch. Every other term is CP.

Backwards propagation through positive adjoints proves the all-G trace effect lower bound c^J I: each G adjoint multiplies an existing scalar lower bound by at least c, and every interleaved TP controller has a unital positive adjoint. History-controlled maps are handled on their explicit classical record blocks; the bound is uniform on each. This does not assume equal memory occupation in branches that have already differed, independent faults, or observed classical trajectories in place of a quantum process.

Since both total processes are TP, their residuals have the SAME trace effect `I−G_all^*(I)<= (1−c^J)I`. For a CP map its diamond norm is the operator norm of this effect. The triangle inequality therefore gives half-diamond distance at most 1−c^J. Fixed per-slot bounds give the product of c_j, and finite stopping uses common identity padding. The statement is uniform over the allowed common controller, so it also bounds the corresponding operational tester advantage. It is not a theorem about two different controllers or an unbounded service horizon.

For the root Pauli-memory form, choose G=id tensor F_0 and c=1−eta. Both residuals are explicit sums of CP branches, and the bad-effect assumption is exactly the required uniform trace-effect bound. This proves the main result without deriving the generally false inequality F_0>=_CP(1−eta)T.

## 2. Stronger CP-mixture failure and sharpness

The retained-error-tag example gives a literal normalized-Choi witness −p(1−p) for `R−(1−p)R_id`, equal to −3/16 at p=1/4. The source therefore correctly excludes the inference that the real process is a constant mixture containing `(1−eta)^J Phi_id`. The common all-clean map can have state-dependent mass and a different continuing-memory map from any constant multiple of Phi_id. There is no physical clean flag and no normalized postselection.

For independent recorded errors on distinct Bell probes, each nonzero error string is orthogonal to its reference Bell state in that SAME recorded block. The half-distance is the sum of those weights, `1−(1−p)^J`, so the envelope can be sharp. The author's finite scalar fixtures verify this example only; they are not presented as a generic-controller execution.

The independent check adds a genuine coherent-feedback test: two source slots, a non-Clifford rational rotation and CNOT from an earlier logical output into the later input, noncommuting/state-dependent retained-memory updates, and a second source chosen from the first retained native error record. Both complete processes contain the exact same all-clean Kraus map on all 64 joint input matrix units. Its effect is `I_logical tensor diag(1,(144/169)^2)`, manifestly not a constant trace multiple. The residual effects agree exactly and are bounded by `1−(144/169)^2`. An actual logical Bell input with memory |1> attains that bound. This directly checks the new feedback/memory mechanism rather than reusing the scalar independent-error example.

## 3. Learned extraction and arbitrary known decoders

The received private-frame extraction theorem supplies a COMPLETE Pauli/gauge instrument with positive gauge effects T_gamma summing to identity and T_0>=(1−b)I. In its identity-labelled learned branch retain just native alpha=0 and decoder gamma=0. Its adjoint effect is at least

    G_0^*(T_0 tensor I_M')
      >=(1−b)G_0^*(I_G tensor I_M')
      >=(1−b)(1−r)I_M.

All discarded terms are CP; no cancellation or native-map CP domination is used. Summing the gauge effects shows the learned branch family has the SAME total memory map T. The stated eta=b+r−br follows. The full output-memory tensor factor in the adjoint is explicit in the final source.

The more general known-code paragraph is also valid and avoids an important false shortcut. An arbitrary CPTP decoder need NOT turn bad physical Paulis into logical Pauli channels. Instead exact correction of Good gives a CP subchannel `id tensor T_good` of the native decoded channel. Learned physical-inverse CP domination gives the common subchannel

    G=(1−b) id tensor T_good

of the learned decoded map. It is also a subchannel of the reference id tensor T, since its residual there is `id tensor (bT_good+T_bad)`. The uniform bad EFFECT gives `G^*(I)>=(1−b)(1−r)I`. The general lemma above then applies without any logical-Pauli assumption, extra logical twirl or constant ideal-memory component.

The independent known-decoder fixture makes this distinction concrete: a supplied two-wire encoder and syndrome-dependent CPTP decoder correct II exactly, but IX induces `Ad_((3I−4iZ)/5)`. Its Bell matrix has a nonzero off-diagonal element 12i/25, so it is not a Pauli mixture. Explicit positive common-subchannel residuals still hold, and the tagged Bell half-distance is 1/5 below its bad-effect bound 1/4. No unsupported Pauli representation was inserted.

## 4. Conditional local faults, not marginal frequencies

At sequential physical fault locations, a uniform conditional fault EFFECT bound p_max I applies to every state reaching the location, including states conditioned on previous fault records. Selecting two specified fault branches and propagating backwards through intervening complete TP maps bounds their joint effect by p_max² I. Summing the three pair events upper-bounds the majority-failure effect for three bit-flip locations by 3p_max² I. Fault records may remain in outgoing memory and error events may be dependent.

The independent check uses eight full three-location fault branches with history-dependent rational memory rotations and state-dependent fault probabilities. All fault tags are retained. It verifies completeness, all three specified-pair effect inequalities, and the union effect bound as exact positive 2-by-2 matrices. This is NOT a claim that a one-site marginal error rate, finite calibration frequency or unrestricted correlated fault model supplies the conditional bound. Acquisition of a useful inverse or native tail remains a separate hypothesis.

## 5. Records, implementations and evidence ledger

Native records can be included only through the complete instruments explicitly represented in the theorem. This is not a waiver of the learned extraction theorem's private-frame retirement or discarded gauge/decoder-record requirements. A record port cannot be added by looking only at its outcome probabilities. Generic finite control errors are handled by the stated whole-service norm debit; they do not automatically preserve the exact Pauli/gauge representation or its common-subchannel premise.

Calibration and acceptance are shared, unknown payloads arrive only after acceptance, and bad-certificate/calibration/whole-service debits are paid once. Conditional acceptance retains its denominator. The enlarged-input complete map statement allows correlated inputs, while a payload-only channel requires the stated conditional product source state. Neither this reduction nor the sequential-fault example establishes a physical threshold or an unknown-noise acquisition theorem.

The main independent check verifies 131,072 complete real/reference residual matrix entries, 192 complete learned gauge/memory entries, the retained-tag negative Choi witness, and all eight dependent three-location branches. The additional arbitrary-decoder check verifies 32 exact decoder entries and the non-Pauli Bell coherence/trace-distance calculation. The initial complex-trace and factored-polynomial structural equality assertions were preserved before replacement by canonical expanded zero differences; no source formula changed. Both corrected checks pass exactly, with zero source calls and RNG draws. No acquisition or hardware execution is claimed. The source's Astra attribution is not a new external refetch or historical-priority assessment by this reviewer.
