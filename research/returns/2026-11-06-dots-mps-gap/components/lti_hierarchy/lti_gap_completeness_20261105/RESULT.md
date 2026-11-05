# A constructive spectral-gap completeness proof candidate

## Result

A provisional proof that Rai et al.'s local translation-invariant spectral-gap SDP converges to the actual **periodic finite-size gap limit** for proper injective-MPS parent chains. The comparison is

    gamma_n >= Delta_n - O(sqrt(log n/n)),

for the valid nearest-neighbor levels n ≥ 3, with model-dependent constants. The formal n=2 problem is excluded; an exact AKLT counterexample shows its value 1 exceeds a four-site periodic eigenvalue 1/3. Together with existing large-periodic-system lower-bound validity, it also proves existence of that periodic limit within the stated class.

The nearest-neighbor unrestricted theorem has undergone three independent internal adversarial mathematical audits. The first found a real Gram-matrix transpose error; after its correction, all three independently rederived the full-subspace boundary operation and found no remaining algebraic gap. The second and third auditors did not consult earlier reports for their independent checks. The third required making n>=3 explicit and supplied the exact level-two AKLT counterexample; that correction is now included. This is still a proof candidate, not a machine-checked theorem, peer-reviewed result, or verified novelty claim.

## Complete central construction

1. Take any nearly optimal positive SDP dual marginal.
2. Project out its open-chain ground space. This preserves every local energy and pair-energy moment exactly and reduces its otherwise unbounded trace to O(n).
3. Decode two logarithmic-length end buffers through exact MPS polar isometries, discard their outer virtual factors, and re-encode the retained inner pair as a joined periodic buffer. A full trace-preserving completion handles inputs outside the buffer ground spaces.
4. The ideal tensor contraction closes both core seams exactly. Exponentially small Gram errors, local defect-energy bounds, and the bounded projected trace control the actual boundary cost.
5. Apply the exact finite periodic inequality H^2 >= Delta_n H to the repaired positive operator. No false orthogonality or normalization assumption is used.

The core algebra, complete map, constants, and final limit argument are in PROOF_CANDIDATE.md. The map is implemented and tested in test_repair.py and full_operation.py. An independent implementation is included in the sibling mps_gap_independent_audit_20261105 directory.

## Scope

The interaction must be a proper parent: sufficiently long open-chain kernels equal precisely the MPS boundary spaces. Normal transfer mixing, a faithful fixed point, and a uniform open gap follow under the stated standard parent assumptions. Merely having a unique infinite-chain injective-MPS ground state is not enough for this proof.

The theorem does not cover general frustration-free chains, higher dimensions, or a separate identification with the infinite-volume GNS gap. A finite-range extension is explicitly defined separately. Appendix D's projected-Y variant has a separately checked argument from the first auditor, with a one-level shift for its literal printed indexing, not an assertion of equality of finite-level optima. The second and third auditors did not review that extension or the finite-range note. The reduced formulation remains a corollary of the energy-moment proof, not an independently established practical improvement.

## Prior art and consequence

Rai et al., Quantum 10,2065 (2026), explicitly leave completeness open. Positive detection for proper MPS parents is already known and is not the contribution. Rozman–Molnar–Schuch's 2026 martingale result already converges to the open-chain gap; Rao's 2026 hierarchy is complete for each finite qubit system; Xu et al.'s 2026 hierarchy gives general bulk-GNS upper bounds. Their lower-bound undecidability construction is outside the proper-parent promise used here.

The separate PRIORITY_AUDIT_SUPPLEMENT.md verifies that open and periodic gaps can differ even for entangled proper injective parents. Thus the result is not obtained by silently identifying those gaps. A targeted primary-source screen found no proof of this exact restricted periodic-limit statement. Close scalar quadratic gap-SDP antecedents exist in Cruz et al. (2022), and no claim to invent that principle is justified.

## Empirical checks and practical comparison

The full local-ground-subspace repair tests include AKLT and a generic complex MPS. The corrected ideal seam residual is below 4.7e-15; actual channel isometry error is below 2.2e-14. The generic Gram-limit regression test explicitly distinguishes the correct metric from the initially erroneous transpose. A complete-channel test includes a nonzero reset branch and preserves trace to 2.2e-14 and unchanged-core moments to 1.4e-15.

A reduced energy-moment-only SDP is suggested by the proof. At n=6 AKLT it uses 11 scalar variables including the gap, and reaches about 0.345553 in an exploratory 59.5-second eigenvector-exchange run with 259 MiB peak memory. This is **not a rigorous numerical certificate** and is weaker than Rai's already certified 0.34976 at the same level. No matched-budget speedup over the best implementation was established. Full details and limitations are in reduced_benchmark/RESULTS.md.

Thus the strongest current outcome is a restricted-class foundational convergence proof candidate and working central operation, not a demonstrated practical or universal scientific breakthrough.

## Verification still needed

- External expert proof and novelty review.
- Formal verification or independently validated exact numerical certificates if claiming computational gap values.
- Matched-resource benchmarks against strongest full/projected-Y and symmetry-reduced solvers, across nonprojector and near-critical parents, before claiming a practical gain.

No external publication, outreach, or user-sensitive action was taken.
