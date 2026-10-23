# Rejected shortcuts, changed contracts, and remaining boundary

This preservation note records the explicit rejected or insufficient arguments in `FEEDBACK_AND_STOPPING.tex` and the focused reviews. It is not a new audit or a claim that each shortcut was separately tested computationally. The authoritative current mathematical statements are the proof source and its incorporated corrections. Historical review files remain unchanged, including conclusions later strengthened by this continuation.

## 1. Three different operations

| Operation | Fixed objects and counted resource | Established conclusion | Remaining limit |
| --- | --- | --- | --- |
| Fixed-horizon classical feedback | Original U, one fixed normal bath, n counted forward qutrit calls; all transcript branches | Capacity is 3/2. Diagonal initializers have the displayed exponential strong converse; every fixed normal initializer has the strong-converse limit | No common exponential rate for arbitrary coherent tails; no exact finite-block optimum |
| Receiver-controlled stopping | Same U and fixed bath; all actual calls counted in a random N; almost-sure termination on every logical input; deterministic decoded channel | Minimum mean cost is `(2f/3) log2 K + o(log K)` at target entanglement fidelity f, and `2(1-epsilon)/3 log2 K + o(log K)` at half-diamond error epsilon. Both maximally-mixed and worst-input means have these coefficients | Expected cost is a different contract. Its strong converse fails, although reliable capacity remains 3/2 |
| Coherent stationary family | One fixed `V_s = cos(s) U + i sin(s) I` across all calls; return to the fixed-horizon contract; same stationary `eta tensor tau_pi` | A strict capacity deficit persists for the stated small-angle interval. Unassisted and backward-classical capacities both tend to 3/2 at s=0 | Capacities at individual nonzero s, and equality between feedback and unassisted capacities there, are open |

No operation supplies bath access, bath replacement, preshared entanglement, a backward quantum wire, or a free forward timing channel. The bath initializer is fixed across horizons. The stopping contract expressly excludes Alice-controlled silence or termination carrying uncharged information.

## 2. Fixed-horizon feedback: the correct invariant and branch weights

- **One encoder for every transcript is unjustified.** The accepted lemma uses a different frozen `E_t` for each complete classical transcript. The identity `Lambda_t = D_t o N_n o E_t` concerns the full unnormalized branch, not Alice's normalized conditioned state in isolation.
- **Normalizing branches destroys the accounting.** Remote steering is compatible with commutation of fixed unnormalized operators on disjoint systems. Physical trace preservation is used only after summing all branches. No successful branch receives extra weight or free calls.
- **Individual operator rank is not Kraus count.** The relevant invariant is the full block Choi Schmidt number, or the minimum maximal individual Kraus-operator rank. It is neither one-use rank nor the number of Kraus operators. General channels can exhibit feedback gains without contradicting this bound.
- **Continuous CP densities need not be trace-nonincreasing.** The incorporated contract requires normal instruments and measurable controls, for example standard Borel outcomes. Integrated normalization suffices. A literal uncountable collection of copied orthogonal pointer states is unnecessary; the common transcript measure and direct-integral Kraus representation are the precise formulation.
- **Arbitrary finite-rank cutoff projections are insufficient.** The coherent initializer argument uses finite vertex-coordinate sets. Only that support makes each truncated Kraus matrix a sum of finitely many vertex-conditioned matrices. Fix this cutoff before taking the long-horizon limit, then enlarge it.

Sources: the unchanged supplied feedback trial, `FEEDBACK_AND_LOTTERY_REVIEW.md`, and the corrected feedback section of the proof.

## 3. Stopping: expected cost cannot be substituted into a fixed-length exponent

The bound `F_e <= E[min(1,M_N/K)]` does not permit replacement of N by its mean inside the exponential. Convexity goes in the wrong direction. The valid converse first isolates the bounded event “stopped by L and passed the entanglement test.” Its complement is charged through `E N >= (L+1) Pr(N>L)`.

Trace-distance proximity of initial bath states does not control an unbounded expected stopping time. The coherent-state proof compares only that bounded event; it keeps the long-event probability under the actual bath. It does not require termination or finite mean under the auxiliary coordinate-truncated state.

Mathematical padding of an already stopped branch to L calls preserves its stored decoded marginal through nonselective operations on other systems. It need not preserve the bath and is not a charge to the actual protocol. It is solely a finite-horizon realization of a selected subchannel.

The matching lottery counts both branches. Bob samples a Bernoulli(p) coin and sends one backward classical bit; the run branch uses an exact Dyck block, while the zero-call branch outputs `I_K/K`. Its decoded channel is `p id + (1-p) D_K`, not a postselected identity. A generic fixed-output replacer gives the same entanglement fidelity, but choosing the maximally mixed output is what supplies the particularly clean exact uniform diamond-error identity used in the final theorem.

The factor `1/(1-epsilon)` in the fixed-error expected-use rate is not an increase in reliable capacity. A two-point duration distribution already defeats the fixed-horizon strong converse under mean cost; genuinely unbounded support is unnecessary. The result is a leading asymptotic frontier, not an exact finite-K optimization. The classical lottery and expected-length phenomenon have primary predecessors; no general historical novelty is claimed.

Sources: the stopped-event and frontier proofs, `STOPPING_CONVERSE_REVIEW.md`, `FEEDBACK_AND_LOTTERY_REVIEW.md`, and `STOPPING_LITERATURE.md`.

## 4. Coherent perturbations: retain interference and the persistent bath

Replacing `V_s` by a stochastic mixture of U and I changes the process. The upper proof keeps a coherent sum over move/stay histories within each actual classical transcript. It uses common transcript, local Kraus and bath indices. Rank subadditivity applies to that sum; the norm remainder is bounded by a sum of **absolute amplitudes**, not squared probabilities. The truncated map is CP but generally not trace preserving, so its trace bound and normalization error are retained explicitly.

An ordinary block-channel diamond comparison cannot simply be declared an adaptive-strategy comparison. The proof constructs common-index isometries for the complete strategy and expands those directly. Likewise, a bound proportional to total horizon times `||V_s-U||` alone does not prove a positive asymptotic coding rate.

For the lower limit, the perturbation estimate is used on one **fixed inner block**. The ideal Dyck block equals an external isometry tensor `I_E` on the whole bath Hilbert space. Mere return of one density marginal would not prevent an earlier bath disturbance from propagating into later packets. This stronger operator identity is why good blocks leave every packet outside the selected bad-block set untouched, even with coherent correlations.

The outer code corrects the entire span of sparse Pauli errors, including environment-valued coherent combinations. Its auxiliary uniform Pauli channel is a device for obtaining Knill–Laflamme conditions, not an IID model of the physical reservoir. No reset, fresh bath or independence between inner blocks is introduced. The low-history environment amplitude need not be normalized; the accepted polar-isometry argument supplies the uniform normalization and full-diamond bound.

The lower-stability statement applies to sufficiently small fixed unitary perturbations on the same port/bath space. The **upper** argument remains specific to the coherent U/I family. Their combination proves endpoint continuity for that family; it is not generic upper continuity for infinite-memory channels. Applying a memoryless-channel continuity theorem to independently reinitialized tree blocks would change the resource model.

Sources: the coherent-family section, `COHERENT_HISTORY_REVIEW.md`, `HISTORY_EXPONENT_REVIEW.md`, `LOWER_STABILITY_REVIEW.md`, and `COHERENT_STABILITY_LITERATURE.md`. The earlier history review established only the upper side; its missing lower side is now supplied by the later inner/outer construction.

## 5. Return, errors, and implementation limits

- **Terminal versus all-use return:** The original exact Dyck code and the stopping lottery return the bath and an inert purification at their block/termination boundary. The bath can change during a block. The actual perturbed inner/outer code promises approximate logical transmission, not terminal bath or purification return. Its recovered environment is allowed to change.
- **Full versus half norm:** `D(rho,sigma) = ||rho-sigma||_1/2`; full trace error is twice D. `epsilon_diamond = ||Lambda-id||_diamond/2`; full diamond error is twice this allowance. In the lower-stability construction, full diamond error is at most `4 T_N`, hence half-diamond error at most `2 T_N`. The equality `epsilon_diamond = 1-F_e` is proved for the specific depolarizing lottery and is not asserted for arbitrary channels.
- **Communication versus recurrence:** Communication error is different from bath-return error. A fixed nonzero bath-return allowance is not recurrence. None of the new operations changes that original distinction.
- **Existence versus efficiency:** The Dyck subspace and inherited Knill–Laflamme/Tverberg argument specify mathematical codes. No efficient compiled encoder/decoder, useful universal blocklength, optimized local-memory cost, energy budget or material implementation has been established. All decoder syndrome registers are external and counted in the model; they are not hidden internal bath supplies.

## 6. Current question and preservation

The fixed-horizon feedback and expected-cost operations are closed under their stated assumptions. Endpoint stability is now established. The continuing question is the capacity at a **fixed nonzero** parameter in the coherent family: can one attain a reliable rate above 3/2 for some fixed `0 < sin(s) <= 1/512`, or can a converse exclude such an increase on a nonzero interval? A plateau, an increase, and a decrease are not distinguished by the present bounds. The device parameter must remain fixed throughout each capacity code sequence.

A continuation must exploit the coherent dynamics and persistent bath. It cannot assume the original Dyck code remains noiseless away from s=0 or restart the answered feedback search. The completed R1 archive, original recurrence proofs, source provenance, and separately owned programmes remain preserved. This note adds no research, replay, outreach, or new allocation.
