# Independent check of the exact same-apparatus certificate

Scope: the finite cold-input qubit logical channel at lambda=10^6,T=1 in SAME_APPARATUS_CERTIFIED_OPERATING_WINDOW.md, SHA256 5c10048289a2e1eba41b07ced02388c990c96182fe6173719160c186f335268f. This check was performed separately from the certificate's author. It does not establish hardware implementation, unknown-model calibration, arbitrary-source-input accuracy or a general threshold.

Read the full proof and both actual scripts. The source-first/column-major orientation matches the frozen qutrit fixture. The mixed-output source jump is not replaced by split jumps. Source jump norms give dissipative diamond bound 8 lambda, and ||K||=1 gives the stated conservative generator bound 8,002,002. The target bound6 is sufficient. Exact denominator12 encodes both generators, including the target quarter entries.

Checked the Taylor/Horner construction and numerical enclosure: scaled action<=1/4, remainder2/4^49; entrywise Gaussian-integer rounding at128 bits contributes at most2d^3 2^-128 in diamond norm; x=e+r gives x_next<=(1+x)^2-1. The verified N x<=1/2 justifies final error<=2N x. This compares to exact CPTP exponentials without assuming that the rounded matrices are themselves CP.

Checked exact system-Z conjugacy, cold preparation/source partial trace and even-parity averaging. For the paired difference, unnormalized Choi reshuffling preserves Frobenius norm and ||Delta||diamond<=||J||1<=2||J||F gives a valid complete qubit-channel upper bound. For the unpaired lower, |1><1| and norm-one Pauli Y give a valid explicit channel witness. Physical and target exponential errors are added in both directions.

Executed test_same_apparatus_certificate.py without modifying frozen artifacts: all36 direct-generator column checks, exact parity/K norm identities, and independent160-bit/degree52 replay passed. Additionally independently reconstructed the witness and both upper/lower rationals from the saved dyadic matrices, recomputed the Choi Frobenius square, and verified the matrix-artifact hash. All match exactly.

Conclusion: PASS for the stated finite numerical operating-window separation. The unpaired error exceeds2.266611872732366e-4; the paired complete error is below9.88465317203069e-7, rigorously separating target1e-4. The operation producing the improvement is precisely ordinary private system-Z twirling. A freely chosen direct GAD implementation remains a stronger ordinary task baseline; no advantage over twirling or GAD is inferred.
