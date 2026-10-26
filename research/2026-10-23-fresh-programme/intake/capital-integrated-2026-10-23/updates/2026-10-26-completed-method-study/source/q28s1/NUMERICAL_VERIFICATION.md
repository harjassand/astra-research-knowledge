# Numerical verification

All checks passed. These finite diagnostics supplement the analytic proof; they do not prove its quantifiers.

| Comparison | Ordinary numerical optimum | Largest finite-state ratio | Largest local tangent ratio |
|---|---:|---:|---:|
| biased_reset_vs_identity | 0.273532788564 | 0.272537219872 | 0.27297242592 |
| BSC_vs_identity | 0.4356 | 0.434764237191 | 0.435349184488 |
| BEC_vs_identity | 0.72 | 0.72 | 0.720000000029 |
| asymmetric_3output_vs_identity | 0.282511057225 | 0.281996747487 | 0.28250280748 |
| biased_reset_vs_BSC | 0.740390921956 | 0.723063606643 | 0.739821331285 |
| asymmetric_3output_vs_BEC | 0.392376468369 | 0.39198832094 | 0.391985249407 |
| BSC_vs_asymmetric_3output | 2.516520821 | 2.10335735124 | 2.50191946559 |

Biased reset exact coefficient: 0.273532788563763; false index transplant: 0.375.
Scalar optimizing input: t=0.40586884574495.
Reference dimensions: 1, 2, 3, 5, 8. Both equal and unequal marginals were tested.
Each comparison used 400 finite pairs and 24 full tangent-space Hessian optimizations.
The Hessian ratios use the numerically positive comparison subspace; eigenvalues at most max(1e-9, 1e-10 times the largest eigenvalue) are omitted as numerical null directions.
The scalar search uses a 2,001-point grid and refines each grid maximum. Its general-channel optima are numerical estimates; exact rational upper bounds are supplied separately.
All comparison constants came from competent ordinary scalar optimization over the same channels.
The ternary negative control recovers an existing quantum-reference separation, preventing an invalid extension beyond binary input.

Run: `/usr/local/bin/python3 verify_binary_channels.py`
