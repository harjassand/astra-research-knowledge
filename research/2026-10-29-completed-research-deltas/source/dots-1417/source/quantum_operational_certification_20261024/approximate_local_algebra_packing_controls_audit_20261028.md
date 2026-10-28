# Independent audit: approximate local algebra packing and physical causal controls

28 October 2026. **PASS for the lemmas and control contract stated here.** This is a separate proof review, not a replacement of any received manuscript, a full audit of a forthcoming approximate-local acquisition theorem, or an acquired-data experiment. No source calls, source actor, private source files, or new random sampling were used. The exact-support received sources remain unchanged.

## 1. Contract and the distinction that matters

There are integers `1 <= q <= n` and `1 <= w <= n`. A common unknown unitary identifies q exact logical qubits and a gauge. Write

`E0(omega) = U[omega tensor Gbar]U†`,

`rho = E0(I/2^q)`, and `B_(j,i) = U(sigma_(j,i) tensor I)U†`.

The exact logical Pauli factors are mutually compatible and commute with rho. They are **not** assumed to be locally supported. For each i there are two Hermitian unitary proxy reflections `V_Xi,V_Zi`, both supported in one unknown interval `I_i` of width at most w, such that

`delta_(j,i) = Tr rho (B_(j,i) - V_(j,i))^2 <= tau^2`.

The proxy pair need not anticommute. The proof uses their existence, not a supplied proxy matrix or a free learning oracle. The small-error regime used below is `0 <= tau <= kappa/8`, `0 < kappa <= 1`. More generally the Bell-packing proof needs `eta0 = 11 tau^2/4 <= 3/4` and `h2(eta0) + eta0 log2 3 <= 1/2`.

Known expanded envelopes are a separate acquisition output. This audit assumes, on its explicitly paid good event, that each known envelope contains its witness proxy interval and all actual learned controls for that label. This review does **not** establish that the old exact-local coarse locator retains its guarantees under approximation. That extension requires its own approximate contrast/error ledger.

## 2. Literal two-reflection extraction, with globally supported exact generators

Fix one logical label and let `P=(I+B_Z)/2`, `Q=I-P`, `P'=(I+V_Z)/2`, and `Q'=I-P'`. Define the two isometries into a new qubit plus the full physical residual register:

`V0 = [P ; B_X Q]`,  `V' = [P' ; V_X Q']`.

Both are exact isometries: the two output-qubit components are orthogonal and `V_X†V_X=B_X†B_X=I`. Anticommutation is not needed for the proxy isometry. The exact ideal isometry decodes the specified logical qubit perfectly; it is only a proof device and is not implemented or assumed local.

For any purification with physical marginal rho,

`||(V' - V0)|psi>||^2`

`= Tr rho (P'-P)^2 + Tr rho [V_X Q' - B_X Q]†[V_X Q' - B_X Q]`

`<= delta_Z/4 + 2 Tr rho Q(V_X-B_X)^2 Q + delta_Z/2`

`<= 2 delta_X + 3 delta_Z/4`.

The last inequality follows from `[rho,Q]=0` and positivity: `Q rho Q <= rho`. This is the only support-sensitive-looking step, and it uses commutation, **not** locality of B_Z. Since the ideal output has a Bell factor on the chosen input reference and extracted qubit, projecting onto its orthogonal complement proves

`ell0(V') <= 2 delta_X + 3 delta_Z/4 <= eta0 := 11 tau^2/4`.

If the proxy pair lies in J, the proxy decoder is a CPTP map of J alone: its isometry factors as the local isometry tensor the identity outside J, after which all residual registers can be traced. The same full virtual Choi state can be used to evaluate every such local decoder **separately**. No simultaneous application, cloning, commuting decoder assumption, or operational source reference is introduced.

## 3. Bell-reference packing proof

Take any s logical labels whose proxy pairs lie in an L-qubit interval J. In the full virtual Choi state the selected reference marginal is exactly `I_(R_S)/2^s`, hence its qubit factors are mutually independent. Let A_i be the qubit produced by the separate local decoder for i.

Writing `ell_i <= eta0`, pinching the `R_i A_i` state into its Bell direction and three-dimensional orthogonal complement cannot decrease entropy. Maximizing within the orthogonal complement gives the quantum Fano bound

`S(R_i A_i) <= h2(ell_i) + ell_i log2 3 <= f`,

where `f = h2(eta0) + eta0 log2 3`. The final inequality uses monotonicity on `[0,3/4]`. Since `S(R_i)=1`, Araki–Lieb implies `S(A_i) >= 1-S(R_i A_i)`. Data processing then gives

`I(R_i:J) >= I(R_i:A_i) >= 2-2f`.

The product reference marginal and strong subadditivity imply

`sum_i I(R_i:J) <= I(R_S:J)`.

For clarity, chain rule writes the right side as `sum_i I(R_i:J | R_<i)`. Each summand is at least `I(R_i:J)`, because `I(R_i:R_<i)=0` and conditional mutual information is nonnegative. Finally `I(R_S:J) <= 2S(J) <= 2L`. Thus

`s <= floor[L/(1-f)] <= 2L` whenever `f <= 1/2`.

The stated coarse regime makes this automatic: `tau <= 1/8` gives `eta0 <= 11/256 < 1/16`. A fully analytic bound is

`f(eta0) < f(1/16) < 1/4 + 15/128 + 1/8 = 63/128 < 1/2`,

using `(16/15)^8 < 2` and `log2 3 < 2`. No numerically evaluated entropy threshold is needed by the theorem. Zero error uses the continuous convention `h2(0)=0` and recovers the sharper `s<=L`.

## 4. Independent cross-check: a stronger one-axis random-access packing bound

This alternative is proof-only and does not enlarge the learner's measurement access. Prepare uniform independent classical X-basis bits on the selected s logical factors, with other logical inputs maximally mixed and gauge Gbar. If V_Xi is measured on J, its prediction error for bit i is

`p_i = (1-Tr rho B_Xi V_Xi)/2 = delta_Xi/4 <= tau^2/4`.

The trace is real because `[rho,B_Xi]=0`; the identity follows by expanding the weighted squared difference of reflections. Binary Fano plus data processing gives `I(C_i:J) >= 1-h2(tau^2/4)`. Independence of the input bits and SSA give `sum_i I(C_i:J) <= I(C_S:J)`, while the cq Holevo bound gives `I(C_S:J)<=S(J)<=L`. Therefore

`s <= floor[L/(1-h2(tau^2/4))]`.

This is stronger than the conservative Bell-reference estimate in the stipulated regime and independently confirms the safe `s<=2L` packing used below. It requires neither simultaneous decoding nor an actual sampled ensemble in the learner.

## 5. Integer-safe geometry and observable coloring guard

Let `W=min(n,3w-2)`. On the acquisition good event, each known envelope has width at most W and contains its proxy interval. All envelopes covering a site lie in an interval of width at most `min(n,2W-1)`. Their proxies all lie there, so the preceding packing bound limits overlap to `2(2W-1)`.

Use a left-endpoint sweep/optimal interval coloring. A sufficient integer cap is

`C = min(q,4W-2)`.

If the observed coloring exceeds C, deploy the prescribed physical replacement receiver and predetermined encoder, count all executed calls, and charge the exceptional history. Passing this guard is not a family-membership or approximate-locality certificate.

Define a directed edge j to k when its color is earlier and their envelopes intersect. Within a color the envelopes are disjoint. Each graph-ancestor or graph-descendant step enlarges the physical span by at most W-1 per endpoint. Thus put

`S = W + 2(C-1)(W-1)`, `K=min(q,2S)`, `A=min(q,K^2)`.

Every ancestor cone spans at most S sites and contains at most K block labels, by proxy packing. The same forward argument shows that each block occurs in at most K output cones. Clipping S by n could improve constants but is unnecessary. All these expressions are valid integers for `w=1`, `q=1`, and boundary-clipped envelopes. Sharper floor bounds from Sections 3 or 4 are optional; the conservative factors of two are sound.

## 6. Required repair to the causal comparison proof

**The exact-support proof cannot be copied verbatim.** Exact B_i need not be supported in the known envelopes. Therefore outside-cone ideal gates must not be deleted by claiming local Heisenberg cancellation for those gates.

The correct argument is:

1. Consider the actual color-ordered receiver with restored/tracked routing and one distinct private ancilla per block. Its exact-reference net block support is its known physical envelope plus its own ancilla.
2. For output i, delete outside-ancestor-cone gates from the ACTUAL Heisenberg evolution of `Phi_(R_i,A_i)`. This is an exact support cancellation for every input state, with no independence of gauges or output states.
3. From the SAME full initial purification, compare this restricted actual circuit with the exact ideal SWAP subcircuit on the SAME block indices. This is a newly chosen proof comparison, not a locality deletion of the full ideal circuit.
4. The subset includes i. Complete ideal SWAP blocks of distinct exact logical factors commute, and each acts on its own distinct receiver ancilla. Therefore the ideal subset still produces a perfect `R_i A_i` Bell factor, even though its physical generators may be nonlocal.
5. Every elementary ideal prefix in the subset leaves `rho tensor I_A/2^q` invariant. Retain the full logical reference, gauge purifier and mixed-ancilla purifiers throughout.

For actual learned reflections with errors `delta_Xj,delta_Zj` against the global exact B, the same three elementary gate errors are `delta_Zj/2, delta_Xj/2, delta_Zj/2`. Set `e_j=delta_Zj+delta_Xj/2`. Unitary actual suffixes and Cauchy–Schwarz give

`p_i <= 3|Anc(i)| sum_(j in Anc(i)) e_j`.

The Bell projectors commute, so their union bound and the two cone-cardinality bounds give

`ell0_joint <= 3K^2 sum_j e_j`.

The unrestricted full-state hybrid still gives `ell0_joint<=3q sum_j e_j`, hence

`ell0_joint <= 3A sum_j e_j`, with `A=min(q,K^2)`.

This conclusion requires the actual learned-reflection error ledger, not merely the existence of the proxy witnesses. Acquiring that ledger from approximate-local data and absorbing its irreducible tau floor are separate parts of the forthcoming theorem.

## 7. Physical controls, conditioning, and retained boundaries

- The ideal globally supported controls in the proof are never implemented or supplied to the learner. Actual extraction is still three finite controlled local reflections per logical label, four ancilla Hadamards, and q paid maximally mixed receiver ancillas. Preparation coins are ignored/discarded, not conditioned upon in the invariant-marginal proof.
- Restored/tracked routing around each block is essential. The received end-block construction costs at most `2(n+q)` routing SWAPs per block and preserves the net envelopeproducer-workspace/private-ancilla support. Physical routing depth need not equal C. Finite gate approximations and routing faults remain in the whole-process operational discrepancy.
- Source resets and marginal linearity, not exact spatial support of B_i, prove the paired-pool laws. Thus the exact-fill two-real-call sign pairing, disjoint physical patch reuse, own-sign-bank estimator firewall, and prohibition on conditional joint-bank independence remain unchanged. The comparison pools must remain fresh iid calls with own-current-label averaging; antithetic state-bank calls are not silently reused for iid comparison tails.
- Packing is a deterministic property of the fixed virtual source and its proxy witnesses. Applying it pathwise to acquired envelopes on the acquisition good event does not replace rho by a posterior/conditioned payload state. Independent reset calls remain governed by the same source after the calibration history.
- Global identity dominance, if invoked, still supplies the separate uniform noisy-source oracle transfer; it is not a consequence of approximate local packing. Global Clifford input/readout, fresh qualification of the newly frozen receiver, whole-process confidence, block-call versus input/output-qubit traffic, and the untwirled diamond limitation remain as in the received sources.
- This audit does not certify the approximate coarse locator, new ERM approximation terms, tournament budget, total source cap, or final excess-risk constants before those are explicitly supplied and reviewed. The strongest equally informed conventional learner can use the same mechanisms.

## 8. Independent deterministic check and provenance

`approximate_local_algebra_packing_controls_check_20261028.py` performs no sampling. Its exact rational example uses

`U=(1599/1601)I - i(80/1601)Z tensor Z`, with maximally mixed physical marginal.

Each single-site X/Z proxy is an exact local reflection pair, while its corresponding true X generator is genuinely nonlocal. For both labels the exact values are

`delta_X=25600/2563201`, `delta_Z=0`,

`proxy Bell loss=6400/2563201`,

`weighted isometry distance squared=12800/2563201`.

The check verifies exact isometricity and the ideal Pauli pullbacks, as well as the extraction inequality. It also exhaustively checks 8,934 small interval families (`n<=6`, width<=3, `q<=4`) satisfying the safe packing consequence, including repeated envelopes and boundary cases. Sweep coloring and ancestor/descendant span/cardinality bounds pass. These finite cases support, but do not replace, the analytic proof.

The first local check invocation stopped on SymPy's unsimplified syntactic matrix equality `U.H*U == I`; applying exact symbolic simplification resolved that check-harness issue. No mathematical parameter, assertion tolerance, source draw, or learned decision was changed. The final check is exact rational algebra plus deterministic geometry; entropy decimals are diagnostic only, with the analytic guard proved above.

Received source hashes are recorded in the check output and receipt. No received file was modified.
