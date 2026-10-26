# Exact comparison certificates

All arithmetic below is rational. Each comparison polynomial has no root in (0,1) by its saved Sturm sequence and is positive at 1/2. Its denominator is positive in that interval. The analytic binary lifting theorem supplies the dimension-uniform quantum guarantee.

| Comparison | Exact certified bound | Interior roots |
|---|---:|---:|
| biased_reset_vs_identity | 137/500 | 0 |
| biased_reset_vs_BSC | 3/4 | 0 |
| asymmetric_3output_vs_BEC | 2/5 | 0 |
| BSC_vs_asymmetric_3output | 63/25 | 0 |

The sharp biased-reset value is separately derived analytically as `(19-sqrt(105))/32`; 137/500 is a rational upper certificate, not a claim of sharpness.

Full channel matrices, polynomial coefficients and Sturm sequences are in `exact_certificate_results.json`.

Run: `/usr/local/bin/python3 exact_certificates.py`
