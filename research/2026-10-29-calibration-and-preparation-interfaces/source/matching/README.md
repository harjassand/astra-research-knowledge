# Astra research delta: random-matching survival and guarded storage

29 October 2026, 04:15 UTC. Local review candidate. This package follows the 02:09 UTC package (SHA256 aa1df0f2581c7343f0234f6ca415a5bacdc82be1ccb6ccba1a3a3b17cc52cd67), delivered as three parts. It does not assert Capital integration, publication, hardware performance or historical novelty.

## What changed

The new random-matching test prepares singlets on a uniformly random perfect matching and passes only when all the same pairs return singlet. For any current CPTP channel and any K-dimensional subcode of the n-qubit singlet space of dimension d, its failure probability bounds reset-completed logical entanglement infidelity with coefficient (d/K)(n+2)/(n-1). The coefficient remains bounded when K is the largest power of two below d. This removes the linear-in-n sensitivity cost of the earlier single-edge witness by changing the physical test, not by contradicting its lower bound.

The proof derives the exact matching-projector frame spectrum from Collins–Matsumoto's established pair-partition Gram spectrum. A partial-SWAP unitary exactly saturates the full-space coefficient. The physical test uses pair preparation/readout without a full logical encoder on test rounds. It still pays random routing and trusted control/readout. A nearest-neighbour line has an expected quadratic gate lower bound for exact preparation; the accompanying routing construction and lower bound prevent a misleading free-routing advantage claim.

A separate conditional bridge inserts this witness into the already established sequential hazard guard. This is an accepted-subnormalized correctness statement, with actual private pads and outer correction, not a posterior normalized guarantee. Positive throughput requires a good source and explicit code/control resources. It does not establish positive capacity for arbitrary unknown noise.

## Reviews and governing versions

- matching_architecture_audit_20261029/REVIEW_RECEIPT_v2.json accepts the exact v1 spectral/CPTP proof, routing note and corrected conditional-rate note at their stated scope. It supersedes the v1 receipt's wording/hash context, not the theorem. The proof's original author-pending header is preserved; the version-bound receipt governs its reviewed status.
- matching_survival_20261029/EXACT_PARTIAL_SWAP_SHARPNESS_v2.md strengthens v1's asymptotic sharpness argument. SUPPLEMENT_REVIEW_RECEIPT_v3.json separately accepts this exact author file and its finite-angle saturation calculation.
- matching_survival_20261029/COMPARATOR_AND_RESOURCE_SCOPE_v3.md governs resource and conventional-comparator qualifications and is separately accepted by SUPPLEMENT_REVIEW_RECEIPT_v3.json. These later supplements preserve the original v1 proof bytes.
- comparator_v9_review_20261029/RECEIPT_v9.json accepts the earlier six-state comparison after a full rerun and independent Kraus-map dynamic program.
- The new matching comparison is separately accepted at finite simulated scope by matching_architecture_audit_20261029/COMPARATOR_REVIEW_RECEIPT.json, following an independent common-cap rerun and CP-map checks. Its original pending headers remain preserved; the later exact-byte receipt governs the accepted versions.

## Strong alternative and useful failure

Constant-gap channel verification is established. Two logical mutually unbiased bases already provide coefficient 2 and do not need full-Clifford sampling; they do require the physical logical encoder/decoder. Full two-design tests have coefficient (K+1)/K. The prospective matching benefit is the pair-only test interface, not a new generic no-tomography verification principle. Historical priority remains unresolved.

In the new common-cap simulation, all methods use the same learned frame, final retained bath, 155 service calls, cap 1400 and accepted soundness target 1/128. Matching yields acceptance about 0.775859 and 410.348 expected source calls; six-state testing yields 0.929018 and 373.489. The stronger conventional test still wins this instance. Matching reduces calls relative to weighted testing but loses acceptance. These are floating source-generator simulations conditional on one million-call training history, not measurements or a training-average guarantee. Gate durations, calibration errors and endpoint storage are not included in the scalar-call comparison.

## Reproduction and dependencies

Python programs require NumPy and SciPy where imported. Set OPENBLAS_NUM_THREADS=1 for stable inexpensive finite checks. Run each matching directory's check program from a writable copy; some regenerate JSON outputs. Run comparator_v9_review_20261029/matching_comparison.py and matching_comparison_commoncap.py using the supplied reviewed_fixture_arrays.npz cache. Run independent_review.py to regenerate the cache and full earlier source-generator learning fixture, which is substantially more expensive. No physical bath-state access is supplied to the learner by this evaluator cache.

A minimal unchanged source subset is included under comparator_v9_review_20261029/source/ so its replay imports resolve without the unrelated 29 MB copied source tree. PACKAGE_FILES.json hashes every included file and identifies unchanged dependencies by their prior package path. General guard and outer-code proofs remain governed by the earlier 00:11/02:09 packages; this delta does not silently replace them.

Original scientific sources and receipt versions are preserved. No personal records, account information or conversation dumps are included. Research continues beyond this snapshot.
