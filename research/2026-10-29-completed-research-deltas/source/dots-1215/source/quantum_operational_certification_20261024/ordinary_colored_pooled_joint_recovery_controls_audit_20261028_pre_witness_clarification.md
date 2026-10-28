# Independent physical/control review: colored and pooled joint recovery

28 October 2026. **PASS under the imported exact-local-algebra, reset-source and paid-control contracts.** This is a proof review with zero new source calls or simulations. Earlier received sources, receivers, receipts and pilots are unchanged. The colored receiver is a new learned policy, not an equal-channel compilation of a previously index-ordered learned receiver.

## 1. Exact packing, observable coloring and the actual block supports

If s independent logical qubit algebras have their true X/Z generators supported inside L physical qubits, they generate a faithful representation of M_(2^s) inside M_(2^L). Its irreducible dimension is 2^s, so s<=L. This uses the exact common compatible operator algebra on the physical register, not the occupied gauge rank or a factorization of the state. Arbitrarily correlated or rank-deficient gauges do not change the dimension argument.

On the coarse good event each known envelope W_i contains both true and learned supports. All envelopes of width at most W covering one site lie within an interval of at most 2W-1 sites. Packing therefore bounds their number by min(q,2W-1). Left-endpoint sweep coloring attains this interval graph overlap bound; arbitrary-order greedy coloring would not suffice for the claimed guaranteed cap. The observed color-count guard is consequently never triggered on the coarse good event. Its replacement fallback is a real CPTP policy on exceptional records, not acceptance/postselection or a test certifying the source model.

Every exact-reference SWAP block has net support W_i plus its distinct output ancilla A_i. Restored routing is essential: a physical route may cross other patches and output qubits, but the route-execute-unroute macro must leave all other labeled registers unchanged. Then each ancilla is a private leaf, acted on only by its own net block. This prevents ancilla wires from creating unaccounted long-distance causal paths. Within one color the blocks have disjoint net supports and commute, although their physical routing can be serialized and their learned generators need not obey any mutual Pauli relations.

The color count is abstract block depth, not hardware depth. Approximate routing faults are covered by the whole-process implementation allowance; the proof does not assert that such physical faults have the same local cone as the ideal restored macro.

## 2. Causal-cone bound with arbitrary initial correlations

Use the directed envelope graph with edges only from earlier to later colors. In one backward layer a physical span can grow by at most W-1 at each end. Same-color disjoint intervals cannot form a propagation chain within that layer. Starting from output i's own block, every ancestor envelope is contained in a span of width at most

    W+2(C_max-1)(W-1).

All those block indices have their true independent logical algebras inside that span, so packing and the trivial q bound give the stated K. The forward-span argument is identical and bounds the number of output cones containing any one block by K. The proof applies to actual graph ancestors/descendants; it must not add arbitrary gap-filled-interval members that have no graph path.

For the local Bell projector on R_i,A_i, backwards Heisenberg propagation touches only its envelope cone. Every outside-cone net block can be deleted for every input state, irrespective of entanglement with the source gauge or other references. Delete outside blocks separately in the actual and ideal circuits and compare the resulting two restricted circuits from the **same initial purified state**. This is not an unjustified removal of summands from a full-state error expansion with an uncontrolled prefix.

Keep the full Bell reference R, gauge purifier E and receiver mixed-ancilla purifiers S. Every subset of ideal elementary gates leaves rho_PA=rho tensor I_A/2^q invariant. The restricted ideal circuit still gives perfect Bell success on R_i,A_i by the same causal deletion from the complete ideal receiver. Its gate-error norms are therefore exactly the previously received delta_Zj/2, delta_Xj/2, delta_Zj/2, even though supports overlap across colors.

With e_j=delta_Zj+delta_Xj/2, the restricted hybrid gives

    p_i <= 3|Anc(i)| sum_(j in Anc(i)) e_j.

The actual final Bell projectors on distinct R_i,A_i commute, and I-product_i Phi_i<=sum_i(I-Phi_i). These p_i are marginals of one real joint output, not separately fitted receiver fidelities. Summing and using both the backward and forward K bounds gives

    ell0_joint <= 3K^2 sum_j e_j.

The earlier complete hybrid remains valid in the new color order and gives 3q sum e_j. Taking A=min(q,K^2) is therefore valid and never worsens that earlier bound. With delta_Xj,delta_Zj<=25eta and eta=epsilon/(16384qA), the uniform source regret is at most 450epsilon/16384<epsilon/20, assuming the separately imported global dominance condition. No gauge independence or learned-generator compatibility was used.

## 3. Exact-fill paired source calls really produce the required banks

Fix one envelope color, one local candidate-interval color and one axis. All active physical patch registers are disjoint. Each pair consists of **two actual reset source calls**, on independent uniform anchors, with logical sign vectors s and -s. There is no source inversion or counterfactual output.

For logical i's plus bank, the chosen call has other logical signs u_k=s_i s_k. Conditional on i's own sign, these remain independent uniform signs. The minus bank uses their negatives. For either bank separately, averaging all other labels therefore gives exactly the source with logical i in its specified eigenstate and every other logical input maximally mixed. Fresh pairs are independent, so each selected single bank has marginal r_(i,j,+)^{tensor N_B} or r_(i,j,-)^{tensor N_B}. Independent anchors ensure the required anchor mixture in each bank.

Different logical learners may select different members of a pair. They nevertheless receive distinct physical subregisters because their active patches are disjoint. A single register is never assigned to two estimators. Multiple same-logical candidate patches in one local color are likewise disjoint and may share the same input sign/routing label without sharing a quantum register.

The plus and minus banks are generally correlated with each other; learners' banks can also be correlated or entangled. A useful counterexample is the two-logical identity source when a learner's patch contains the other logical input as spectator: the two selected spectator X signs are perfectly anticorrelated. Each bank has a maximally mixed spectator, whereas their joint X correlation is -1 rather than zero. Conditioning on an opposite-bank measurement could reveal that spectator state. The manuscript correctly does not assert a conditional iid guarantee after such conditioning.

Each individual state-estimation instrument is thus fixed on its own selected bank, using only its own routing labels and internal outcomes. No cross-sign, cross-learner or shared-anchor-dependent adaptive measurement is permitted before all state estimates are frozen. The other instruments are TP on disjoint registers and preserve each bank's marginal when their outputs are not conditioned upon. A union bound over these individual estimator bad events needs no joint independence. Subsequent classical ERM may combine all four frozen estimates because its Bures transfer bound is pointwise.

The firewall is an algorithmic measurement/dataflow contract, not cryptographic hiding: the input controller knows the full sign vector. The resulting confidence statement is a joint bad-event probability, not a posterior guarantee conditioned on every final transcript. Exact paired fill requires no extra fill probability, rejection or optional stopping. The earlier oversized-pool idea would instead have required a separately charged fill event and could not simply condition every estimator on global fill success.

## 4. Fine-bank source, input and memory ledger

There are at most 4qR_max state estimates. Assigning beta_F/(4qR_max) to each gives precisely the logarithm in the displayed N_B cap. There are two axes, at most C_max envelope colors and c1 local candidate colors. Each nonempty axis pool uses exactly 2N_B raw source calls and gives both sign banks. Hence

    N_fine <= 4 C_max c1 N_B.

This does not reduce the number of receiver state-estimation circuits, which remains at most 4qR_max. One axis pool uses qN_B fresh sign bits plus the complement rule, two q-logical input blocks per pair, independent anchor choices, and 2nN_B physical output-qubit exposures. The full 2nN_B-qubit pool can be stored and routed according to the known classical labels, plus the paid Bures purification/Schur and compilation workspace. These are actual quantum copy banks and cross-copy controls, not free coefficient or independent-sample oracles.

Local color indices may be assigned separately inside each disjoint envelope; matching global physical start residues across different envelopes is unnecessary. Empty pools can be omitted within the predetermined cap. Reordering memory by sign is a known physical permutation of separately labeled registers and must be compiled/routed, not declared costless.

## 5. Pooled comparisons use a different, iid experiment

Comparison pools correctly do **not** reuse the antithetic two-call schedule. Every raw call instead chooses fresh independent own axis/sign labels for every logical input, including inactive inputs. Conditional on the complete previous-batch history, each active pair and its two spectral controls are fixed. Averaging the other current labels leaves exactly the desired mixed-other-input source for that learner. Its actual local spectrum outcome has the received mean, second moment and finite backward-observable slack.

Only one current comparison per logical index is run in a slot, on its actual candidate-union support inside its envelope. Different active envelopes are disjoint. Local TP measurement instruments preserve each comparison marginal on the same actual output. Current cross-learner outcomes are not used to change a running batch; candidates advance through their own fixed balanced-bracket postorder only at batch boundaries.

Consequently each individual comparison's N_pair samples have the required conditional iid law. Cross-learner outcomes and winners can be correlated without invalidating the conditional concentration or union bound. There are at most q(R_max-1) comparison events, giving the stated logarithm with beta_T, but only C_max(R_max-1) pooled batches. Thus

    N_tournament <= C_max(R_max-1)N_pair.

The number of local spectrum-measurement executions can still be q(R_max-1)N_pair; source sharing does not refund receiver controls. Independent decoder-error counts, independently resampled marginals, overlapping comparisons for one learner, or unproved paired-score concentration would not implement this protocol.

## 6. Complete cap, new policy freeze and honest scaling

The coarse phase remains label-specific: it cannot reuse one unknown overlapping physical patch for all logical conditional tomography tasks. Its 2qM state estimates and 2qcN0 calls have the correct beta_L union-bound logarithm. On their good event the observable coloring guard passes. Coarse, fine, tournament and encoder budgets sum to the declared statistical allowance; no hidden fill budget is needed.

The complete raw block-call cap is

    2qcN0 + 4C_max c1N_B + C_max(R_max-1)N_pair + N_count + 1.

R_max=1 skips all comparison logarithms and calls. The last call is a real q-logical payload. Every failure history returns a physical channel within this cap, without postselection or omitted calls. Implementation precision includes all inputs, collective bank controls, exact-feasible SDP arithmetic, finite sign/spectrum controls, routing, private randomness and payload operations.

The newly color-ordered joint receiver must be frozen before fresh global encoder learning/qualification. Learned blocks across colors generally do not commute, so this is not an equivalent compiler of the old index-ordered channel. The manuscript correctly reuses no earlier encoder decision or holdout. The imported global Clifford input/all-zero readout law applies to this actual new joint channel; product-only global validation is still a weaker unsupported access model.

For fixed w, C_max,c1,R_max and A are bounded independently of q. The fine and comparison block-call rates are therefore linear in q at fixed accuracy, with the displayed width and confidence factors. Total logical input traffic is qN_total and physical output exposure is nN_total, so neither total qubit traffic nor receiver work is claimed linear in q. Quantum storage, coarse O(qn) local estimator invocations, extensive local POVMs and global input/output Clifford controls remain paid. The payload still uses q distinct mixed ancillas, 3q controlled reflections, 4q Hadamards and restored routing per joint invocation, and has abstract rather than physical color depth.

## 7. Linear-error boundary and final verdict

The gauge-bit example is physically correct. When the spectator bit is zero, the learned reflection pair gives an ideal SWAP. When it is one, the middle controlled -X adds a control phase, and the full three-gate block equals (Z_logical tensor Z_ancilla)SWAP. With a maximally mixed initial ancilla, the retained output therefore receives a Z error. Independent spectator bits of probability p yield joint Bell loss 1-(1-p)^q, while delta_X=4p and delta_Z=0. It is a valid zero-source algebraic example showing the natural linear accumulation for small errors, not an acquired-data claim.

The global operator-dominance assumption, known physical output coordinates, exact compatible local algebra, reset source and global Clifford control remain substantive. They are not learned or verified by a successful color cap. The optional private-key Pauli twirl and the untwirled dimension-dependent diamond boundary remain unchanged. An equally informed conventional learner receives the same coloring, pooled banks, ERM, physical comparisons and receiver order.

All requested physical law, control, confidence, memory and source-count checks pass. This review generated no simulations or source calls and changed no received source or frozen pilot. The companion controls receipt binds the final manuscript and this independent derivation.
