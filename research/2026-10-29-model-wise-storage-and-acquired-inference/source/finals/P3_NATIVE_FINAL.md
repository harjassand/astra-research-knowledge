**I committed to acquiring the observable law needed for inference, with reconstruction of original inputs kept as a separate operation.** The completed pipeline now handles temporal conditioning and exact short samples over enormous horizons, within a precise raw-circuit admission.

I also developed the alternative based on graph representations of functional dependencies. Its obstruction is decisive for choosing a general direction: that representation can require exponential width even for linear bijections that ordinary Gaussian inversion handles cheaply. I retained the construction and its failure, then pursued stochastic inference more deeply.

## Completed construction

The input is a literal transition circuit \(T(x,u)\), a requested observation circuit \(O(x)\), and a declared state/noise split with fresh independent original noise at each step. The compiler acquires and verifies an identity of the form

\[
O(T(x,u))=q(u+a(x))+c,
\]

including the quadratic form \(q\), the state-dependent shift \(a\), and their governing identities. These are recovered from the gates; they are not supplied as a decoder.

The current admission is **scalar quadratic noise with constant polar form and a nonuniform base law**, with all intermediate representation costs charged. The identity makes the requested future observations iid even while the hidden evolution remains nonlinear.

This escapes a substantive restriction of the earlier affine-uniform representation. For example, the acquired channel can have original-fiber sizes \(10\) and \(6\). Such a biased bit cannot be an affine readout of any uniform affine law.

I then completed the temporal-event operation. Given an explicit deterministic automaton describing the requested event, set

\[
M_{ij}=\sum_{b:\delta(i,b)=j}N_b,
\qquad
Z_H=e_{q_0}^{T}M^H\mathbf 1_F,
\]

where \(N_b\) is the acquired number of original noise words producing observation \(b\). **\(Z_H\) counts original noise tapes**, including their unequal observation-word multiplicities.

The operations remain distinct:

| Operation | Completed guarantee |
|---|---|
| Count | An exact positive arithmetic expression; expanded integer output pays its actual bit cost. |
| Selected future observations | Their exact joint conditional marginal, in expected polynomial time in the acquired representation, automaton, query size, and \(\log H\). |
| Original-history witness and uniform sample | Actual original noise words, reconstructed causally from a known initial state or an evaluated raw initializer; every emitted step is paid. |
| Posterior original initialization seed | For this future-only evidence, exact uniform sampling of the original seed without evaluating the initializer. |
| Full regular-event rank/unrank | Not implemented; the stronger local and prescribed-word indexing results retain their separate scope. |

### Removing the enormous-integer obstacle

The new arithmetic component makes exact random choices directly from nonnegative addition/multiplication DAGs. It uses certified dyadic bounds and refines one retained stream of fair bits until the choice is determined. It never substitutes a fixed-precision approximate decision.

The proof and independent implementation review establish **expected polynomial bit work**, even when the represented counts have exponentially many digits. Worst-case random streams can require arbitrarily long refinement. The review also preserved two useful failures: insufficient precision under shared squaring, and the bias caused by discarding precision-capped attempts and restarting.

## Evidence at the actual output scope

A constructed nonlinear source with acquired counts \((2,6)\) was conditioned on **no consecutive ones** over

\[
H=2^{80}+19
\]

steps. This event is exponentially rare, while its original count has at least \(H+1\) binary digits.

The implementation drew exact conditional observations at four selected positions using **2,142 allocated arithmetic nodes**. During that control, actual transition execution, hidden-state shifts, initializer execution, and expanded-count evaluation were disabled by guards. The largest stored interval significand had 102 bits; larger temporary arithmetic remains explicitly charged.

A separate internal review used a different raw source, different bias \((6,2)\), and a different temporal event. It reconstructed all **1,760 accepted original tapes** in its finite control, checked the exact probability composition, and exercised guarded short queries at \(2^{65}+23\). The raw channel, arithmetic engine, and temporal wrapper now have separate reviews tied to their exact versions.

## A sharper obstruction to broader acquisition

The complementary quadratic attack found that **constant full polar rank and inexpensive coordinates still do not make the global law easy to acquire**.

The saved construction puts an arbitrary CNF truth function \(F(x)\) into a quadratic completion phase, producing

\[
\#\{(u,v):G(x,z,u,v)=0\}
=
2^{2m-1}+(-1)^{zF(x)}2^{m-1}.
\]

Thus the law is independent of hidden state exactly when \(F\) is unsatisfiable—even though the raw source has sparse cubic gates, unit pivots, and constant full polar rank. A separate family has raw representation widths \(O(k)\) but completion-phase width \(2^k\) in the original order.

I independently checked the governing argument. Its determinant/path-sum ancestry is established mathematics; the result here isolates the precise obstruction in the acquired noise-law task. **A compact coordinate circuit does not certify the signed conditional populations.** :chatgpt-content-reference{index="0"}

## What remains distinctive

The equally informed ordinary weighted-automaton method remains strong. It was faster on all three finite matched tasks—original count plus three exact uniform original tapes—with the same acquisition charged to both routes. It can also use certified arithmetic to match the long-horizon operation.

Coupling-based independence proofs and certified random generation have primary antecedents. I am not claiming a new general principle merely from combining those ideas. The completed asset is the explicit **raw acquisition → checked law → temporal count representation → exact conditional output → original reconstruction** chain, together with a sharper account of where acquisition becomes hard. :chatgpt-content-reference{index="1"}

The substantial barrier removed is compulsory trajectory expansion and enormous integer materialization for short conditional predictions after genuine law acquisition. Unrestricted law discovery and arbitrary circuit counting remain unresolved.

The proofs, executable controls, corrections, and reviews are saved in place:

- :chatgpt-content-reference{index="3"}[ACQUIRED_LONG_HORIZON_REGULAR_INFERENCE.tex](producer-workspace/ACQUIRED_LONG_HORIZON_REGULAR_INFERENCE.tex)
- :chatgpt-content-reference{index="4"}[acquired_regular_channel_inference.py](producer-workspace/acquired_regular_channel_inference.py) and :chatgpt-content-reference{index="5"}[positive_count_circuit_sampling.py](producer-workspace/positive_count_circuit_sampling.py)
- :chatgpt-content-reference{index="6"}[CONSTANT_RANK_QUADRATIC_PHASE_REFINEMENT.tex](producer-workspace/CONSTANT_RANK_QUADRATIC_PHASE_REFINEMENT.tex)

Earlier constructions and versioned failures remain intact. No upload, export, repackaging, or archive retry was performed.