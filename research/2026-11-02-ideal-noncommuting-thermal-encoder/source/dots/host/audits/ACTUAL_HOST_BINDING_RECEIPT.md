# Independent actual hierarchical-host binding receipt

2026-11-01. **PASS for the actual main RX/RZ family and the analytical supergraph gap interface.** This closes the host/TQO-II premise of `SUPERGRAPH_PROOF_GATE_RECEIPT.md`; filtered-parent norm estimates and an operational preparation theorem remain separate.

## Frozen inputs

- Host v1: `producer-workspace/actual_hierarchical_host_filling.md`, SHA256 `4628c91a701b43e43738926d0e435a19791960c953321ebabb85a465a9ce65a6`.
- Accepted host v2: sibling `actual_hierarchical_host_filling_v2.md`, SHA256 `3ac1009ce21d0c9d7c4eba1266d46821858c8e10f5a0e036b2f8cb062e50af14`.
- Previously independently audited two-sheet contraction: `producer-workspace/two_sheet_contraction_addendum.md`, SHA256 `7a18df5e5c6eeaaee63aff2455256ad3b7048fb75ded030dbac2093c36593f29`.
- Previously audited actual full-cohomology filling: sibling `polynomial_filling_theorem_candidate.md`, SHA256 `e653d035699ed69febcb61eacdf23efba93e912b4187e4ce00c175e9863fc186`.

Personally checked the v1→v2 diff. It explicitly adds paired graph completion, its degree accounting and provenance; ancestry and filling arguments are unchanged. In fact v1's simultaneous projections already imply the two required connectivity properties, but v2 is the clearer interface.

## 1. The host and matching are genuine bounded-size combinatorics

The parent of a fine basis cell is its unique old direct-sum gadget label in the actual source cochain replacement, not a nearest spatial point. These labels include all degrees/check-relation cells. Each old label has at least two fine children, including endpoint gadgets; all gadget dimensions are bounded by a fixed function of the fixed ell and source degree bounds. Fine cells are not identified merely because embedding coordinates coincide.

The stated B and Delta_H bounds are conservative: Tanner incidence contributes at most 7, same-type overlap/co-occurrence neighbors at most 42, ancestry contributes one parent plus B children, and the optional physical graph contributes D_R. Nonempty checks bound each level's number of Tanner vertices by 8n_i. The actual Q-block growth n_(i+1)≥(ell+1)n_i≥4n_i makes the sum of all levels O(n_L), as stated.

For completeness, the internal-node matching proof is valid without a hidden Hall assumption. In a subtree with every internal node having at least two children, leaves minus internal nodes is at least one. Process children first. Each child subtree returns at least one unused descendant leaf; an internal node therefore receives at least two unused leaves and consumes one. Different subtrees have disjoint leaves. Every internal vertex gets a distinct descendant leaf. Mapping each top leaf to itself gives fibers of size at most two. Projecting host edges cannot increase a path length, and projected degree is at most twice the original maximum degree. The assignment may be geometrically long-range, which is permitted only because it defines an analytical graph, not an operation.

## 2. Anchored logarithmic filling, including the complementary sector

For RX X cocycles, each fixed-sheet readout has a carrier either in its own Q block or on a radial path in an incident X gadget. These have old-label distance at most one. The anchored primitive vanishes on an untouched X gadget. Choosing the globally smaller sheet does not change this support-adaptation property; it is an existence choice, not a local decoder algorithm.

The complementary RX Z map is the transpose of the actual Q-block inclusion, hence disjoint-block parity and nonincreasing. Its local reconstruction uses the full cohomology contraction, including extra degree-two relation spaces. This is essential: it is not legitimate to discard those spaces or substitute an unknown-error cleaning operation. The audited HPL maps have at most two g factors, and each g changes old gadget label along one old Tanner edge; h and the local inclusion/projection preserve the label. A full monomial can therefore be connected by a path consisting of child→old label, at most two old-label edges, and old label→child. Its carrier displacement is at most four host edges. Transposition preserves this support relation. RZ supplies the dual statements.

Every two alternating coarse steps reduce the chosen sector's stabilizer weight by at least one half while preserving stabilizer class. Thus after O(log(1+m)) steps the residual vanishes, or the finite seed is reached and filled. Every nonzero coarse coordinate has a nonzero-input ancestor. Every correction is attached to a touched gadget. Lifting an individual selected coarse generator through another level again costs only a bounded number of host edges. Composing downward ancestry and upward generator lifting therefore produces a path from EACH selected top check to SOME original occupied qubit of length c0+c1 log(1+m). This is anchoring to the original support union, not merely a diameter bound or a claim about filling cardinality. Disconnected original supports are allowed. A fixed seed diameter is absorbed in c0. Mixed X/Z stabilizers can be split and filled sectorwise, each with weight at most m.

No code-distance cutoff is used for a globally known stabilizer. Distance enters only when converting a sufficiently small centralizer into a stabilizer and in the separate spectral theorem's TQO-I cutoff.

## 3. Real-vertex quotient and norm-compatible graphs

The incident-pair projection fixes each real top check in the check image. Its fiber has size at most 2(1+wc): a check leaf and at most wc adjacent qubit leaves, each with at most one additional matched ancestor. Thus the check graph has uniformly bounded degree. Lift all selected fixed-range physical qubit edges to incident-check pairs, paying wc wq D_R, and then complete the qubit graph along the check edges as in v2.

For every qubit edge the incident-check union is connected in the check graph. For every check edge the union of its actual supports is connected in the qubit graph. Consequently connected covers satisfy exactly

    |ext(M)|≤wq|M|, with ext(M) check-connected;
    |supp(S)|≤wc|S|, with supp(S) qubit-connected.

These are the two properties required by the independently checked proof extension. Graph growth must use kappa≥log(max(Dc,Dq)+1); original LDPC incidence constants are not silently replaced or counted as physical interactions.

## 4. Actual TQO-II and gap-interface conclusion

For any nonempty actual check set S and any stabilizer p supported in supp(S), m≤wc|S|. The anchored host filling followed by the check projection places each filling check within c0+c1 log(1+wc|S|)+1 of S. The final +1 is justified: an original support qubit is mapped to its selected incident check, which overlaps whichever member of S contains that qubit. Since log(1+wc s)≤s log(1+wc) for integers s≥1, a uniform ell_* gives the required linear-in-|S| radius. This holds even for disconnected S and therefore for all sets connected in the enlarged graph.

The previously established power-law distance supplies d*=min(d/wc,d_tilde)≥c log n for d_tilde=Theta(d), after the usual finite-size choice of constants. Host projection does not change the stabilizer group, distance, projectors, check weights, or energy spectrum. No fictitious check, zero-energy generator or ancillary Hilbert space is added.

Combining this binding with the supergraph proof-gate receipt therefore earns the actual unperturbed-family hypotheses for the extended gap-stability argument. It gives uniform gap stability for sufficiently small perturbations in that analytical graph's intensive locality norm. Fixed-range bounded-density physical terms are included after the described physical-edge lift. General filtered or slowly decaying terms still need their own norm proof. Neither a physically local shortcut unitary nor a quantum Gibbs-preparation algorithm follows from this binding alone.

## 5. Independent finite fixture

Read and reran `actual_host_quotient_test.py`, suppressing only its final JSON overwrite. It constructs actual seed→RX3→RZ3 incidence, with n=5,60,1336, not a fabricated second-level Euclidean embedding. Observed:

- host: 2,895 vertices, maximum degree 85;
- children per internal node: 2 through 66;
- leaf quotient maximum fiber: 2;
- final actual check vertices: 1,428, degree at most 58;
- final actual qubit vertices: 1,336, completed degree at most 273;
- check/qubit projection fibers: at most 5/6;
- every host edge check-nonexpanding; real endpoints fixed;
- both edgewise support-connectivity properties pass;
- projected qubit edges retained by completion.

No physical-nearness edges were fabricated in this fixture. These checks corroborate the quotient construction, not the all-level filling proof or a filtered-parent gap computation.
