# Prior art, completed reviews and resource costs

The [final source literature audit](package/LITERATURE_PRIORITY_AUDIT.md) supersedes preliminary novelty comments in earlier logs. It credits the 19-qubit construction to Aydin, Alekseyev and Barg, Quantum 8, 1321 (2024), Section 7, with the example and computer-assisted existence statement already in the 2023 preprint. Its shorter-code assertion is discussed in the source as restricted to that construction's real/parity form. It is neither omitted nor promoted to an unrestricted complex, even-length no-go theorem.

Okada's December 2023 dissertation, posted in 2025, Table 3.1 already yields the applicable lower bound of 18: the reported code-dimension bound is 1 at n=17 and about 2.019 at n=18. The new exact LP certificates make the old bracket replayable; they are not a new lower bound. Bumgardner's earlier SU(2) MacWilliams framework, intrinsic-distance correspondence, general SDP hierarchies, PPT relaxations and rigorous rational certification are credited in the supplied audit. The proposed contribution is the evaluated unrestricted n=18 exclusion and consequent minimum 19 within this code family.

The source's targeted search through 5 November 2026 found no earlier unrestricted exclusion at 18. That bounded negative search does not establish global priority. Capital has preserved the supplied source links and assessment without conducting another literature search. The same-class equivalence with correction of four deletions/erasures is prior work; it is not a new two-deletion result or an unrestricted deletion-code optimum.

| Supplied completed work | Coverage and limitations |
|---|---|
| [Independent residual audit](package/audit_residual/AUDIT.md) | Analytic necessary conditions, corrected equality orientation and exact interval residual contradiction; lower-length and known positive-control checks |
| [Second adversarial review](package/audit_second/INDEPENDENT_REVIEW.md) | Separate derivation, arbitrary complex product-basis convention checks, actual-spin exact recoupling tests, fresh corrected-witness replay and lower-length reconstruction |
| [Earlier independent checks](package/audit_independent/AUDIT.md), [residual review](package/audit_independent/RESIDUAL_CERTIFICATE_REVIEW.md) | Prior checks preserved in their chronological scope |
| [Positive-19 review](package/symmetric19_audit/INDEPENDENT_REVIEW.md), [positive-control guide](package/audit_positive19/README.md) | Independent reconstruction of the already published construction and lifted-map sanity checks |

The two final adversarial reviews report no substantive gap and a passing rigorous contradiction certificate at their stated scope. This is computer-assisted mathematical evidence with analytic representation identities and exact arithmetic inputs, without a formal proof-assistant verification or external peer-review claim. The visible response's request for external expert review is an assessment of discovery status, not a new Capital permission requirement.

The source construction used Python 3.12, SymPy, NumPy/SciPy, CVXPY and Clarabel, with a roughly 542 MB isolated environment and one OpenBLAS thread. Reported compilation, solves, failed export attempts, interval replays, positive-control reconstruction and literature checks are separate costs. Runtime logs do not give full end-to-end CPU accounting. An approximately eight-second successful replay is not the total discovery cost, and no speed or compute-efficiency advantage is claimed. The last constructor completed optimization and wrote raw duals before interruption during redundant floating diagnostics; the certificate does not depend on completing those diagnostics.

The supplied [replay program](package/REPLAY.py) and [requirements](package/requirements.txt) are archived without execution. Some source scripts regenerate timing-bearing receipts, so their regenerated hashes may differ; the frozen witness and verifier identify the checked mathematical input. Capital checked the current package manifest for transport only, preserved all numerical artifacts as opaque bytes, and performed no new scientific audit or replay. No hardware memory lifetime, fault-tolerant overhead, implementation cost or broader quantum-code optimum follows.

The actual human prompt supplied quantum-error-correction context after a broader invention-lab request. Dots selected this smaller complete mathematical problem. This result does not establish an efficacy comparison for a coordination policy, completion of the separate harder comparison, or repaired compute-limit enforcement. The earlier diagnostic fix supplies no such operational evidence.

[Certificate guide](certificate-model-and-proof.md) · [Return overview](README.md)
