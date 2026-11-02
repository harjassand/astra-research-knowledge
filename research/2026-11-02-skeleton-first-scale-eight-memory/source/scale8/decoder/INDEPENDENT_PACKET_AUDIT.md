# Independent review of hardened theorem and packet extension

Reviewed 2026-11-02 after the original independent audit.

## Verdict

The hardened numbered hypotheses address the precision issues raised in `INDEPENDENT_AUDIT.md`. I found no additional fatal issue in the main abstract theorem or in the packet theorem **when its whole-state component contraction is assumed directly**.

There is one missing hypothesis in the packet extension's proposed *per-atom verification shortcut*, as read at the start of this review. This does not refute the conditional theorem. It matters if one tries to discharge its contraction premise using atomic columns without establishing map additivity.

## Per-atom shortcut needs additive maps

Section 3 says that the two-sheet inequality follows from per-atom inequalities and subadditivity for atomic packet norms. In addition, the sheet maps must respect the operation used to combine atoms. For binary syndrome linear maps this means fixed F2-linear maps, and the atomic norm should be defined as the minimum number of atoms in an XOR representation.

Counterexample to the shortcut without additivity: take a two-coordinate input block and the singleton atomic norm, hence ordinary Hamming charge. Define both sheet maps by

    p_A(00)=p_B(00)=00,
    p_A(10)=p_B(10)=00,
    p_A(01)=p_B(01)=00,
    p_A(11)=p_B(11)=11.

These maps are deterministic, bounded-local, and zero-preserving. Every singleton atom satisfies the proposed two-sheet inequality, since its two images both have charge zero. However, for input 11 the sum of the two sheet output charges is 4, whereas the input charge is 2. Minimum-sheet output charge is 2, not at most 1.

This counterexample violates directly assumed component contraction, so it is **not** a counterexample to the main theorem. It only disproves the claimed shortcut under the previously stated general map assumptions. Repair: explicitly require fixed additive sheet maps and an atomic norm for the same operation, or verify every complete admissible block/component state directly. The issue was reported promptly to the author and root.

For fixed linear maps the intended proof is valid: choose a minimum XOR atom representation x = XOR_j a_j. Linearity and subadditivity give Q(p_A x)+Q(p_B x) <= sum_j [Q(p_A a_j)+Q(p_B a_j)] <= number of atoms = Q(x). If a map is chosen adaptively, its fixed linear branch must satisfy the relevant column inequalities; one cannot silently linearize a nonlinear branch-selection function.

## Whole-block ownership and ancestor recurrence are sound

The key improvement is selecting complete actual block states. If upper block B is selected, its unique lower owner contributes precisely its full actual state. Thus its charge is literally one nonnegative summand in the selected owners' whole-output charge, irrespective of the values of g on strict bitwise subsets. Consequently

    Q_(i+1) <= sum_selected_owners Q(O(C)) <= Q_i/2.

No monotonicity under bit deletion or nonlinear subadditivity across overlapping contributors is being used. Input block closure makes the last input sum additive. Output ownership over all possible branches avoids assigning inconsistent portions of one nonlinear block charge to multiple components.

The fixed preimage-block connections can support this ownership assertion provided their stated ambient-degree, connected-shape, and causal premises are actually verified. Their existence is not automatic from the charge table. The text correctly leaves these as geometric obligations.

## Gibbs payment and entropy are sound

For selected base blocks, the inequality g_B(x)<=c|x| gives Q_0 <= 2c M + O(k), where M counts distinct original occupied coordinates in their union. Complete blocks can contain additional zero coordinates without probabilistic payment because block size is bounded and their geometry is charged to positive block charge. Only the initially flipped coordinates can change occupancy between the two runs; enlarging the root to their bounded blocks costs a constant.

Shape size is O(Q_0), hence O(M+k). Whole-block states and atom decompositions have only bounded finite-state labeling entropy per block. Fixed ambient bounded degree and a fixed fault root therefore give exponential witness entropy with no volume or free depth factor. A fixed original occupied leaf set is paid for by q^M. The direction of the q-exponent comparison in Section 5 is correct.

## Cutoff, extinction, and exponents are sound

A surviving discrepancy gives a nonzero upper block in one run, of charge at least one. Downward closure forces charge at least 2^h at the base, and the upper bound by c times Hamming mass yields the claimed distinct-leaf lower bound. If the inputs become identical, common higher corrections cancel; selected charge bounds changed lower correction supports and gives the same S_h(K) distance estimate. The exponents are consequently unchanged, up to constants.

## Minor textual correction

In the hardened Hamming theorem, the displayed inequality was reversed to upper mass <= half lower mass, but the following sentence still says forward additions “only increase the left side.” It should instead explain that lower-layer additions increase available input mass and upper-layer additions force their own downward ancestry. This is a wording inconsistency, not a new mathematical failure.

## Scope

The review does not establish actual blue/red map inequalities, recursive block sizes, preimage geometry, admissibility, or lift identities for ell8. Those obligations remain conditional exactly as stated in the extension.

## Final correction verification — 2026-11-02

**Reviewed and signed by task `producer-workspace/audit_component_contour_proof`.**

I re-read the corrected packet extension and the corrected selected-mass paragraph of the theorem and independently computed these SHA-256 hashes:

- `PACKET_CHARGE_EXTENSION.md`: `e862fcad8e25bc456311931982f01a3dc94c94b8697534a66665905240613d93`
- `THEOREM.md`: `44a585dcae19eb2d4582104e8674939c495680073a4f5e385d7da396b46f126e`

Both match the versions submitted for final verification. Packet section 3 now explicitly requires fixed F2-linear maps, defines the atomic norm using XOR decomposition, gives the correct subadditivity argument, and separates the nonlinear minimum-sheet selection from the two fixed linear maps. Nonadditive maps require direct whole-state verification. This repairs the per-atom shortcut gap identified above. The retained counterexample and pre-correction snapshot clearly mark the audit boundary rather than presenting the old shortcut as valid. The theorem's lower-layer/upper-layer wording has also been corrected.

**Final verdict on these versions:** the identified shortcut defect is repaired. No remaining fatal defect was found in the conditional abstract theorem or complete-block charge extension under their explicit hypotheses. This sign-off is not verification of the concrete ell8 maps, recursive geometry, cochain identities, or full-family lifetime.
