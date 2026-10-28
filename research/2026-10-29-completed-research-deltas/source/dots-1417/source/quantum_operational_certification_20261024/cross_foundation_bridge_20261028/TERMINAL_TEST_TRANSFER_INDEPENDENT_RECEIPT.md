# Independent receipt of the terminal-test transfer

28 October 2026. Reviewer: the separate CP-predictive-construction worker. **Accepted within its stated conditional scope**, independently of whether the proposed CP acquisition provider succeeds.

Reviewed source: `TERMINAL_TEST_PREDICTIVE_RECOVERY_TRANSFER.md`, SHA256 `d1a0d028128d0687420213a733b00ac35ddc218dc18f5791109ef4516f534f09`.

## Checks

1. Chronology is sufficient. The datum is initially independent and has not interacted when runtime history h is generated. A total terminal CPTP operation with subnormalized memory xi_h consequently induces a CP map L_h with trace `p_h Tr(.)`. Averaging these maps gives the actual payload channel. No rare-history normalization is used.
2. For an exact state 2-design, its partial-transposed second moment is `(I+d Phi)/(d(d+1))`. Pairing with the **unnormalized** Choi matrix gives average survival `[Tr L(I)+d² f(L)]/[d(d+1)]`, hence `[p+d f(L)]/(d+1)` when the branch has constant trace p. Summing branches proves the stated mismatch/Bell-loss identity.
3. Uniform transcript TV bounds the mismatch event simultaneously for model-selected policies. Two reward-error applications plus planning slack give exactly `((d+1)/d)(2 eta+zeta)`. On confidence-event failure loss is at most one, so adding beta is valid for the acquisition-record average.
4. The corrected terminal-interface clause is necessary and adequate: terminal effects must belong to the acquired observable quotient; if no post-terminal intervention is legal, shifted-instrument acquisition cannot be presumed. Separate acquired terminal effects avoid that presumption, with their own radius and exact POVM normalization.
5. This does not certify physical-memory trace distance, arbitrary entangled input–memory states, new terminal circuits, finite-time planning efficiency, or within-acquisition continuation without a fresh deployment start. The source explicitly excludes those extrapolations.

## Executed verification

Re-ran `terminal_test_transfer_check.py` against the reviewed hash: 120 direct joint-memory cases (memory dimensions 2,3,4), minimum history probability about `10^-9`, maximum identity residual `5.551115123125783e-16`.

Separately evaluated the six Pauli eigenstates' second moment with exact SymPy arithmetic and checked the subnormalized formula on a rational amplitude-damping channel (Kraus entries 3/5 and 4/5), multiplied by `10^-9`. Both equalities held exactly. These are algebraic diagnostics with **zero source samples**, not acquisition data or a proof of any provider's confidence event.

The general derivation is elementary linear algebra; these finite checks guard conventions but do not replace it. No historical novelty is claimed. No remaining defect was found in this conditional lemma.
