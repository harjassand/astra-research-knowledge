# Independent receiving: local calibration errors inside a correctable interleaved patch

28 October2026. Reviewer `producer-workspace/review_effect_only_acquisition`. PASS at the corrected receipt-bound source. This is distinct from the generic additive-inverse bridge; its stronger locality and factorization assumptions matter.

## Arbitrary single-patch CPTP correction

Routing one carrier from EACH of w standard five-qubit codes into each known patch gives w product syndrome spaces. A patch Pauli is a tensor product of one permitted I/X/Y/Z error in each component code. Different such Pauli products have distinct product syndromes, so the product Knill--Laflamme matrix is identity. Therefore the product decoder exactly corrects the LINEAR SPAN of all patch Paulis, hence every patch CPTP channel, including coherent entangling Kraus operators across that patch's carriers. This is a joint2^w-dimensional logical identity on entangled inputs, not a list of independent marginal fidelity claims.

The actual frozen residual channel satisfies q_a<=p_a+delta_a by the complete triangle inequality. Since both native channel and actual receiver factor across the five patches, the residual product expansion is legitimate. Exact correction kills all single-patch terms, yielding the same half product expression with q_a. Thus delta_a=O(p), rather than O(p^2), suffices for O(p^2) logical error. This relaxes the conditional inverse-accuracy budget; it is not a new error-correcting code or a claim that global inverse error is already quadratic.

The physical layout must really isolate the patches. Overlapping inverse circuits, shared noisy ancillas/control faults, or an actual correlated native channel cannot be replaced by products of marginal channels. Nonlocal encoder/routing/storage/syndrome errors remain whole-system debits unless separately constructed to have the correctable structure. At fixed patch width there are5w physical carriers per full native block; parallel calibration block counts and per-site final-fit counts must not be mistaken for total carrier passages. All preparations, readouts, finite local synthesis and code routing remain paid.

## Future noise and record-retaining version

The calibration family is needed to acquire the fixed frame. Subsequent weak patch channels can be non-Pauli and need not preserve the calibration contrasts, provided they have the same fixed mixer and actual declared product/norm bounds. Those future promises are not learned from finite training. On each good calibration record the receiver is fixed and the bound is deterministic; records need not be retired for this version. Taking a common confidence event and charging beta once is valid. Initial source independence and the stated conditional product law are substantive. Full retained bath/syndrome behavior and arbitrary repeated-cycle feedback are not covered.

## Faster onsite record-retired specialization

The separately received polar inverse theorem bounds a ONE-USE genuinely averaged local inverse by1620/(a_i^3 N_i). I checked its receipt/source binding. Independent fresh final programs across sites and independent service permit tensoring those averaged channels even on an entangled encoded payload. The code then absorbs their O(p) local errors and yields O(p^2) logical error with O(a_i^-3/p) final probes per site. The large constant, pilots, randomness caps, finite controls and beta=O(p^2) remain real costs.

The source initially risked identifying the polar learner's target with an arbitrary original V_i. The author clarified that V_i here is the canonical polar orientation of the CALIBRATION channel, or the calibration residual must separately be SPD. Future N_i and p_i are defined AFTER that same canonical inverse. The statement does not invert an arbitrary hidden allocation of local rotations.

A common private fitting coin can create an all-sites XXXXX logical error of probability h while each averaged marginal has error h. Thus genuine program independence is necessary for this particular averaging/product proof. Conditioning on pilots is allowed only with fresh independently acquired final programs and the declared conditional factorization. Physical retirement is required; records cannot merely be hidden from a chosen mathematical norm while future devices can access them. Reuse of the same random programs over many cycles needs its own analysis.

## Independent checks and fair baseline

In `five_qubit_patch_bridge_independent_check_20261028.py` I directly encode TWO logical qubits into TEN carriers, apply a general entangling two-qubit CPTP map to each of the five possible patches, and propagate all three native Kraus operators through all256 product syndrome outcomes. Each full joint logical Choi matrix equals identity-channel Choi to numerical precision. This goes beyond checking coefficient normalization or Pauli marginals. The shared-program logical-error counterexample is also verified. The author's exact rational pattern enumeration and floating Kraus fixture were replayed separately with identical outputs.

These are exact code identities and floating channel fixtures, not acquired confidence data or hardware. Standard QEC/interleaving with the SAME learned frame is the equally informed conventional architecture and has identical performance. Primary foundations are the five-qubit code and Knill--Laflamme recovery papers. Knill--Laflamme--Viola's general-noise work (https://arxiv.org/html/quant-ph/9908066v1) further prevents interpreting this source's product premise as a universal necessity for all QEC. No new code, historical novelty, fault-tolerance threshold or practical advantage is received.
