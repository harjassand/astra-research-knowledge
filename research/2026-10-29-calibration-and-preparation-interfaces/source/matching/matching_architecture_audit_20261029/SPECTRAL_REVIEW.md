# Independent spectral and CPTP review
2026-10-29. Accepted at stated scope, with provenance hashes in REVIEW_RECEIPT.json. Author file: PROOF_MATCHING_SURVIVAL_v1.md. Review completed before any subsequent author revision.

I independently opened the primary source https://arxiv.org/html/0903.5143 and read its Gram definition, equation3.6, Lemma4.3 and equation4.6. Together they yield the Gram eigenvalues as the zonal product, including singular cases with more than four rows. This is an established representation-theory input, not a new Astra spectral identity.

I checked the singlet loop contraction normalization: each overlap squared is 4^(loops-m), and dividing frame columns by sqrt(L) makes the nonzero frame spectrum the O(4) matching Gram spectrum divided by 4^m L. The permutation-invariant first moment is P/d on the irreducible spin-zero module. The top product gives exactly 1/d.

The partition ordering proof is complete: remove a bottom-row corner while at least two boxes remain below row one and append to row one. Row lengths remain ordered; removed factors are positive for rows<=4; the added factor strictly exceeds the removed factor. The terminal nontrivial partition is (m-1,1), whose eigenvalue ratio is 3/(n+2). Zero eigenvalues and complex/non-Hermitian directions cause no gap. The top is simple and scalar. The second eigenspace contains a nonzero Hermitian element because the frame preserves adjoints. The small-unitary perturbation establishes sharpness without requiring the transposition identification used in diagnostics.

The source's proof of arbitrary-CPTP leakage and arbitrary-subcode transfer agrees with the independent derivation in BRIDGE_AND_SCOPE.md. Reset completion contributes nonnegative fidelity. Full-space coefficient (n+2)/(n-1) and general-subcode coefficient d/K times that value are valid. Only the full-space coefficient is proved optimal. n>=4 avoids the trivial one-dimensional n=2 case.

No historical-priority clearance, physical implementation result, scalable encoder-acquisition theorem, or practical superiority is established. Same-channel and private-setting conditions remain essential. I executed a separate 40-instance complex-CPTP diagnostic and a disclosed-setting attack, recorded in check.py/check.json. These checks do not replace the all-n proof.
