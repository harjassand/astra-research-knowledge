# LTI gap hierarchy: constructive completeness proof candidate

This package addresses an explicitly unresolved question in Rai et al., *A Hierarchy of Spectral Gap Certificates for Frustration-Free Spin Systems*, Quantum 10, 2065 (2026), https://arxiv.org/html/2411.03680v3 : does its lower-bound hierarchy converge to the true periodic bulk gap?

## Result and scope

The proposed theorem is exact convergence for nearest-neighbor **proper injective-MPS parent** chains, using hierarchy levels **n ≥ 3**. Level n=2 is excluded: it omits a potentially negative overlapping anticommutator and is not generally a valid lower bound. An exact AKLT counterexample is included. “Proper” means that sufficiently long open-chain ground spaces are precisely the MPS boundary spaces. It includes the standard AKLT parent. It does not establish the claim for every frustration-free chain, for higher-dimensional systems, or for every interaction having a unique injective-MPS infinite ground state.

The central operation is an explicit completely positive trace-preserving boundary repair. It decodes two end buffers with their MPS polar isometries, discards their outer virtual factors, and re-encodes the retained inner factors as a joined periodic buffer. After removing the dual marginal's energy-invisible ground-state mass, this converts any low hierarchy objective into a physical periodic excitation quotient with vanishing error. The claimed comparison is O(sqrt(log n/n)), with model-dependent constants.

**Status:** provisional proof candidate, not externally peer reviewed, machine checked, or established as novel. Numerical tests support specific operator identities; they do not prove the asymptotic theorem or practical superiority.

Review scope is deliberately separate:

- **Nearest-neighbor unrestricted Eq. (17) theorem:** three independent internal adversarial audits. The second and third auditors did not consult earlier reports for their independent checks. See INDEPENDENT_REVIEW.md, ../lti_gap_adversarial_second_20261105/INDEPENDENT_AUDIT.md, and ../lti_gap_fresh_resource_audit_20261105/INDEPENDENT_AUDIT.md.
- **Projected-Y extension:** separately checked by the first auditor only. The second and third did not review it. PROJECTED_VARIANT_EXTENSION.md handles Appendix D's literal one-level indexing shift, whose valid nearest-neighbor levels start at n ≥ 4; no equality of finite-level optima is asserted.
- **Reduced energy-moment formulation:** a corollary of the moment argument, with exploratory numerical tests, not a separately demonstrated practical improvement.
- **Finite-range note:** outside the second and third audits' established scope.
- **Priority supplement:** independent literature and assumptions checks, not another proof review or a novelty guarantee.

Throughout, the thermodynamic gap means the limit of finite periodic gaps. No separate GNS-gap identification is established.

## Reproduce

Extract **all four sibling folders** from compact_reproduction.zip. From the extraction root, verify every payload hash without changing files:

    python lti_gap_completeness_20261105/verify_bundle.py

Run the eight core and independent test scripts from that clean extraction:

    python lti_gap_completeness_20261105/verify_bundle.py --run-tests

Add --include-benchmarks to rerun the two exploratory solver scripts as well. Clarabel 0.11.1 must be importable for that optional comparison. Tests overwrite generated result JSONs with new timing/resource measurements, so later manifest verification should use a fresh extraction.

Requires Python, NumPy, and SciPy; the fresh audit’s exact symbolic counterexample also requires SymPy (tested with 1.14.0). No new packages were needed for the core proof tests. The optional reduced-SDP benchmark separately installs Clarabel 0.11.1 from PyPI, a 1.2 MB wheel, into a temporary directory.

    OPENBLAS_NUM_THREADS=1 python test_repair.py
    OPENBLAS_NUM_THREADS=1 python check_moments.py
    OPENBLAS_NUM_THREADS=1 python full_operation.py

`test_repair.py` constructs the full Stinespring operator on the entire product of the two local ground spaces, rather than sampling input states. It tests AKLT and a seeded generic complex MPS with a non-scalar transfer fixed point, at buffer lengths 2, 3, and 4. `mps_inputs.npz` stores the actual tensors.

`check_moments.py` independently reshuffles the transfer matrix to check the block Gram limit, verifies local translation invariance of the ground marginal, and checks the exact moment-preserving projection after adding ground-state mass of 100000.

## Accepted numerical results

- AKLT compressed boundary-square operator norms at buffers 2/3/4: 0.0168778, 0.00216766, 0.000222719.
- Generic complex MPS: 0.137898, 0.0315586, 0.0137522.
- Stinespring isometry error: at most 2.2e-14.
- Corrected ideal stitching seam residual: at most 4.7e-15.
- Generic transfer Gram error against the correct limit at length 100: 4.1e-14.
- With 100000 units of added ground mass, the generic marginal's trace falls from 100001.79 to 1.698 under projection; local energy moments change by less than 7e-11 in floating point. The projected marginal is no longer LTI, as expected and allowed in the proof.

The complete CPTP operation, including its nonzero complement/reset branch, is also implemented in full_operation.py. On a six-site AKLT LTI witness it preserves trace to 2.2e-14, middle energy moments to 1.4e-15, and annihilates joined-buffer terms to 1.9e-15. Its resulting excitation quotient is 1.01079 versus the finite gap 0.347866: this small-buffer construction is deliberately loose and is not a competitive variational upper bound.

## Correction made during independent review

The first numerical comparison used I tensor sigma-transpose as the limiting Gram matrix. Under the code's explicit vectorization, the correct limit is I tensor sigma. The wrong choice stayed 0.270613 away at length 100 for the complex test. It was corrected, and an independent transfer-limit check was added. The actual polar-isometry repair never used this limiting metric, so its boundary-square results were unchanged. The ideal seam cancellation alone could not detect the wrong metric because it cancels algebraically for any positive right factor. The proof now derives its Gram convention explicitly.

## Minimum-level correction from the third audit

The original asymptotic argument used n=3 as the minimal nearest-neighbor construction but did not consistently state that domain beside every hierarchy definition. The third audit required making **n ≥ 3** explicit. At n=2 the formal AKLT objective gives gamma_2=1, while an exact four-site periodic eigenvector has energy 1/3. Two independent exact-arithmetic reconstructions are included. The corrected lower-bound and monotonicity claims start at n=3; the asymptotic proof is unchanged. The natural range-k version requires n ≥ 2k−1. Appendix D’s literal one-level-shifted nearest-neighbor indexing requires n ≥ 4.

## Resources and limitations

The accepted six-case repair run took 2.63 seconds in aggregate and peaked at 409016 KiB resident memory (about 399 MiB). An earlier diagnostic run before the metric correction took about 2.66 seconds. The complete-channel run took another 1.37 seconds and peaked at 146964 KiB. Three additional primary-source HTML files totaling 4,157,415 bytes were acquired in parallel in 9.89 seconds. Source acquisition and all drafting, search, and review time are additional. The dense test works in physical Hilbert spaces up to 3^10; it is not a large-scale experiment.

A separate exploratory reduced-SDP benchmark was run at n=3 through6, with selected independent solver comparison. Its n=6 value about0.345553 is not rigorously certified and is weaker than Rai’s existing certified0.34976. No new best numerical AKLT bound or faster practical solver is claimed. See reduced_benchmark/RESULTS.md. Rai's level-n SDP still contains a d^n-dimensional positive-semidefinite matrix, requiring exponential resources in n. Even an explicit convergence estimate of this form can demand prohibitive levels for tight precision. Existing martingale and finite-size criteria remain stronger choices for many practical computations.

## Files

- PROOF_CANDIDATE.md: full argument, finite-range extension with separate scope, prior art, and disproof checklist.
- test_repair.py / repair_results.json: central boundary operation and results.
- check_moments.py / moment_checks.json: independent algebra checks and correction regression test.
- mps_inputs.npz: tested tensors.
- full_operation.py / full_operation_results.json: complete channel, including reset branch, applied to an explicit feasible dual witness.
- LITERATURE_AUDIT.md: exact source definitions, prior completeness distinctions, and assumptions.
- INDEPENDENT_REVIEW.md: first independent internal adversarial review, including its separately checked projected-Y extension.
- ../lti_gap_adversarial_second_20261105/: second independent internal audit and separate executable tests; its established scope is the nearest-neighbor unrestricted theorem.
- ../lti_gap_fresh_resource_audit_20261105/: fresh third audit, whole-code tests, and exact symbolic n=2 counterexample.
- check_minimum_level.py / minimum_level_regression.json: independently reconstructed exact integer/Fraction regression for the excluded n=2 level.
- PRIORITY_AUDIT_SUPPLEMENT.md: independent priority and assumptions audit, not another proof review.
- verify_bundle.py: standalone manifest verification and optional functional tests.
- STANDALONE_TEST_RESULTS.json: clean-extraction test results, with tested source/input hashes.
- PROJECTED_VARIANT_EXTENSION.md: separately checked projected-Y extension.
- REDUCED_HIERARCHY.md / REDUCED_HIERARCHY_PRIOR_ART.md: exact small-coefficient formulation and close antecedents.
- reduced_benchmark/: exploratory solver code, all results and limitations.
- RESULT.md: concise scientific outcome and remaining verification.
- resource_accounting.json: measured computational resources.
- rai.html / rai.txt: acquired primary source and local text extraction; omitted from the compact reproduction archive.

## Relevant comparisons

- Rai et al., https://doi.org/10.22331/q-2026-04-13-2065 : the hierarchy being analyzed, already encompassing Knabe-type bounds.
- Rozman, Molnar, Schuch, https://arxiv.org/abs/2607.19078 : strong 2026 MPS martingale bounds; positive gap detection is already established for proper parents and is not the new claim.
- Xu et al., https://arxiv.org/html/2606.03836v5 : convergent bulk-gap upper bounds and general lower-bound uncomputability; the latter does not directly apply to the promised proper-parent class.
- Rao, https://arxiv.org/html/2510.08427v2 : finite-system SDP convergence, distinct from thermodynamic completeness of Rai's hierarchy.

The targeted literature screen found no prior proof of this exact restricted completeness statement. PRIORITY_AUDIT_SUPPLEMENT.md independently checks source locations and shows why known convergence to the open-chain gap does not imply this periodic-gap result, even within the proper-parent class. It also reviews the adjacent October 2026 Scheer–Khalaf work. This is not an exhaustive novelty determination.
