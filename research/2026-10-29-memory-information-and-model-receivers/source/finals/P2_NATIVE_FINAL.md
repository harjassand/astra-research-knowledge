**I completed a construction that protects causal quantum memory through source redundancy while preserving a strict information-processing advantage.** It also identifies two resources that peak memory size misses: the number of time boundaries across which coherence must survive, and the source errors that an unfinished interaction can spread.

The proofs, executable constructions, useful failures and six scoped independent internal reviews are preserved in :chatgpt-content-reference{index="2"}[README.md](producer-workspace/README.md).

### 1. A protected operation that classical records cannot replace

For the specified source–field erasure operation, I constructed a receiver and source code that:

- Encode **six logical qubits in ten source qubits**.
- Retain **one controlled receiver qubit** across each of five arrival gaps.
- Correct **one arbitrary completed coherent storage fault**, including the admitted persistent-bath correlations.
- Preserve the logical state together with the **actual receiver and correction records**.

A receiver that is classical at all five gaps can preserve at most five logical qubits exactly. For a six-qubit logical input, its half-diamond error is at least **1/2**, even when granted arbitrary source encoding, unlimited classical records and arbitrary final decoding. The quantum construction has zero logical error under its exact one-location fault contract. :chatgpt-content-reference{index="3"}[CODED_CAUSAL_ERASURE.md](producer-workspace/CODED_CAUSAL_ERASURE.md)

This comparison retains the essential interface restrictions. The field carries no supplied preparation label or purification; additional source–field contacts and protected quantum bypasses are unavailable. Avoiding an optional contact, or supplying a known Bell field, can make the task easier. Returning quantum baths count as additional physical memory.

### 2. The stronger result tolerates weak noise at every interval

I continued beyond the sparse-fault construction. Let the source code correct errors arising from \(t\) completed exposure locations, and let each interval’s admitted noise remainder satisfy an all-input operator-norm bound \(\|F_j\|\le\eta\). The completed operation obeys

\[
\frac12\left\|\Phi-\operatorname{id}_{L}\otimes\mathcal R_{\mathrm{mix}}\right\|_\diamond
\le
\min\!\left(1,\sum_{m=2t+1}^{2L}\binom{2L}{m}\eta^m\right).
\]

Here \(\mathcal R_{\mathrm{mix}}\) is an explicitly normalized CPTP instrument retaining the actual classical records. Its law is code dependent; it does not inherit the previous receiver’s record distribution.

The decisive step is **actual syndrome measurement**. Different syndromes remove cross terms; equal syndromes at sufficiently low combined fault degree force the same correctable source character. This works with noncommuting persistent-bath coefficients and correlated logical, bath and reference inputs. It also extends to overlapping exposure spaces whose errors touch many source qubits.

An independent negative control found the sharp interface distinction: keeping the syndrome coherent permits a lower-order logical cross term. Converting it into the actual classical record removes that term.

Combining this theorem with a code-existence construction gives a family with \(k\ge5L/4\): under the conservative sufficient allowance \(\eta\le1/128\), the quantum operation’s error bound tends exponentially to zero, while the classical comparator’s error tends to one. **This is a conditional operation separation.** Extensive-error decoding may be expensive, and source preparation, storage, syndrome extraction and controls still need their own protection. :chatgpt-content-reference{index="4"}[CHANNEL_ORDER_AND_ROBUST_CAPACITY.md](producer-workspace/CHANNEL_ORDER_AND_ROBUST_CAPACITY.md)

Distance-order suppression of coherent errors has established QEC ancestry. The addition here is the causal exposure construction, normalized complete-record comparison and coded receiver separation. Current qLDPC results provide a strong conventional comparator under their own locality and ideal-syndrome assumptions. :chatgpt-content-reference{index="0"}

### 3. The principle also changes a useful gate schedule

I constructed two implementations of logical CZ with the **same bus and the same 28 core contacts**. Closing each local interaction loop makes an admitted coherent fault correctable. The dense schedule admits a bus fault that becomes an undetected logical phase error, with error one on a specified input.

The full ideal preparation-and-correction implementation costs **316 controlled bus contacts and 198 Hadamards**, ending at recovered encoded outputs. Those costs are explicit. Seven direct transversal CZ gates remain the stronger alternative when those direct couplings are available. :chatgpt-content-reference{index="5"}[CLOSED_LOOP_LOGICAL_CZ.md](producer-workspace/CLOSED_LOOP_LOGICAL_CZ.md)

### Evidence and significance

All six components have completed internal reviews with distinct executable challenges. The final channel theorem was checked using a different code and noncommuting bath, including **5,632 exact low-degree record/logical/bath matrix-unit blocks**. Integrity checks passed for the new evidence and **299 unchanged predecessor files**. Commands and evidence scopes are in :chatgpt-content-reference{index="6"}[REPRODUCE.md](producer-workspace/REPRODUCE.md).

The completed construction makes it possible to design protection around **what each causal interaction exposes**, then deliberately choose where coherence must remain and where a measured record improves correction. That is a usable theoretical instrument for architecture design. Efficient, noisy source-control and record-conversion interfaces remain the consequential implementation frontier; no device error rate or total workload advantage has been inferred from these bounds.