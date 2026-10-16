# Independent audit: crossing shared-bath echo obstruction

Date: 2026-10-15.

## Verdict

PASS as an obstruction to directly transferring the atomic theorem's small conditional completion-mark bound to overlapping held-frame pulses using only separate pulse action bounds or isolated-pulse echo errors. The first rare completion label is causally available as an actual syndrome measurement; the example is not an artifact of conditioning on a future-only Fourier label. It is not a no-go theorem for fault tolerance, subset-moment bounds, or other instruments/certificates.

Independent exact reconstruction is in ../checks/exact/check_crossing_independent.py. Both that script and the constructor's ../checks/exact/check_crossing_echo.py were run successfully. No floating-point eigenvalue or approximate probability is used.

## 1. Algebra independently reconstructed

Use memory qubits A,C and one bath qubit B. Set H=X_A X_B and K=X_C Z_B; they anticommute and square to identity. Independent private Z_A,Z_C frames supply signs x,y in {+1,-1}. The chronological subpulses are

exp(-i x a H), exp(-i y b K), exp(+i x a H), exp(+i y b K).

Thus A's interval starts first and completes third, while C's starts second and completes fourth. Each isolated two-subpulse echo is exactly identity. The final unitary is

W_xy=exp(+i y b K) exp(+i x a H) exp(-i y b K) exp(-i x a H).

Write c_a=cos(a), s_a=sin(a), c_b=cos(b), s_b=sin(b). Its four sign-character operators are

W_00=(1-2 s_a² s_b²) I,
W_10=-2 i c_a s_a s_b² H,
W_01=+2 i s_a² c_b s_b K,
W_11=+2 c_a s_a c_b s_b H K.

Averaging independent signs gives the complete Kraus channel sum_chi Ad_(W_chi). Each W_chi† W_chi is a scalar times identity, so the following probabilities hold for arbitrary input states:

p_10=4 c_a² s_a² s_b⁴,
p_01=4 s_a⁴ c_b² s_b²,
p_11=4 c_a² s_a² c_b² s_b²,
p_00=(1-2 s_a² s_b²)².

They sum to one. Therefore

Pr(A_bad)=4 c_a² s_a² s_b²,
Pr(C_bad | A_bad)=c_b²,

whenever the denominator is positive. The corresponding reverse conditional is c_a², though chronological completion order is A then C.

## 2. Why the first label is causal

Immediately after A's last subpulse, before C's final subpulse, the signed interaction-picture unitary is

V_xy=exp(+i x a H) exp(-i y b K) exp(-i x a H).

Its A-sign character-1 part is y sin(2a) sin(b) H K. Thus the completed A character already has a causal CP-instrument realization before the remaining C operation, because no future interaction uses A's frame.

More concretely, start memory A,C in |00> and allow an arbitrary bath input, including a reference entangled with B. Measure Z_A at A's completion and Z_C at C's completion. The character-1 part flips A, whereas the character-0 part leaves A at zero. Consequently the genuine Z_A outcome 1 selects exactly the first rare character. That branch also places C in state 1. The last weak C subpulse leaves C in state 1 with probability cos²(b).

The independent checker uses the actual physical frame gates at their starts and undos, rather than assuming the interaction-picture formula. For every fixed frame pair, the measurement instrument's bath-input effects are exactly p_ac I_B. This proves that both probabilities and the conditional ratio are valid for every initial bath state, not just a chosen pure bath vector.

The remaining C gate commutes with Z_A. On the encoded input domain, averaging the discarded A frame already eliminates coherence between its two syndrome outcomes, so making this syndrome record explicit does not introduce a new hidden interference-based probability. No controller learns either private frame value. These syndrome records are distinct from the discarded frame registers.

This causal observation closes the most important loophole in using a final multi-frame Fourier decomposition as a counterexample: a generic end-only label need not correspond to any available earlier record, but this example does.

## 3. Exact weak-pulse comparison

Choose a=b=2 arctan(1/10), so cos(a)=cos(b)=99/101 and sin(a)=sin(b)=20/101. The exact conditional is

Pr(C_bad | A_bad)=9801/10201.

Because arctan(1/10)<1/10, the integrated action of either two-part pulse is 2b<2/5, and its square is less than 4/25. The displayed conditional is strictly larger than 4/25. It also exceeds the two-half operator-distance triangle bound squared, 16/101, since each half rotation has squared distance 4/101 from identity. Thus neither of these natural separate weak-pulse bounds is a valid uniform conditional completion-mark bound.

The marginal A event is rare: at these rational parameters its probability is 6272640000/1061520150601. Conditioning on it selects a rare component created while C's pulse is already in progress. The subsequent C completion is therefore not a fresh weak operation relative to C's original syndrome. An isolated-echo channel equal to identity cannot repair that causal conditioning issue.

## 4. Relation to the atomic theorem

The atomic theorem assumes an entire bounded-patch post-error instrument, following its correction, with a pointwise small bad-effect bound on every current conditional state. In this crossing example a previous completion measurement occurs inside another pulse's interval. The long pulse's earlier action has already occurred when that conditioning is performed. Its two halves cannot be substituted by a single fresh atomic post-error at its completion while keeping the same records and support assumptions.

The example therefore invalidates an attempted derivation of the required conditional-effect premise from individual integrated strengths, disjoint memory supports, a shared bath, ideal held private frames, and small isolated echo channels alone. It does not contradict the atomic theorem or the ideal syndrome-sandwich theorem when their complete instruments really are atomic and satisfy their stated conditional hypotheses.

It also does not establish that every possible instrument ordering, grouping of overlapping pulses, or enlarged spacetime-patch certificate must fail. Grouping both intervals or proving a different fault-path/subset-moment estimate remains logically possible.

## 5. What is not proved

The joint bad probability is

p_11=4 c_a² s_a² c_b² s_b²=O(a² b²).

In particular p_11<=4 a² b², while the product of the two squared integrated-action budgets is 16 a² b². Thus this example is consistent with an ordinary small joint-subset bound and does not prove a large fault cluster or memory failure. Near-one conditional probability after an unusually rare record is a different statement.

No hardware claim, general continuous-Hamiltonian noise theorem, or no-go result for fault tolerance is made. The subpulses can be modeled as separate bounded-duration Hamiltonian segments, but ideal frame operations and any diagnostic syndrome measurements remain ideal in this construction. Appending untouched logical qubits supplies a nontrivial logical code without changing the calculation.

The earlier nested example has the same conditional-interface issue but allows an idle-tail rescheduling simplification. The crossing echo removes that particular simplification: both intervals have a nontrivial final interaction, and their endpoints genuinely cross.
