# Compact law audit

## Verdict

PASS for the current 128-component rational-mixture artifact. This is an exact certificate check and mathematical review of its rounding and mixture conversion, not a certification of NumPy random draws or an implementation of the general native-generator theorem.

Checked `heterogeneous/compact_law.json` SHA256:

`2b2a3aeecf9f8ffbdb8f9751431ecfd034e8da98a241b633cd6cc82cdc95d484`

Run the portable check with `python audit_compact_law.py`, or pass the heterogeneous artifact directory as its first argument. It writes no production files.

## Scope and checks

The exact rational input rates are `(10n+i)/(10n*5^i)`, with n=128, and each local spectral law puts probability 1/2 at zero and at its positive rate. Initial rate rounding and partial-sum rounding are both covered by `(1+2^-12)^129`. The compiler constructs the intended rational family directly; the separate floating formulas must not be treated as identical exact inputs.

- Regenerated the 5,561-bin histogram using the production function definitions and compared every integer key/count and grid parameter. This checks reproducibility; it is not an independently implemented dynamic program. The rounding invariant was reviewed separately.
- Independently reimplemented the certificate arithmetic and checked all 304 retained root brackets. Every interval lies strictly within its claimed interlacing interval, all indices are distinct, and exact fixed-point signs bracket a root.
- Independently recomputed every residue lower/upper numerator and checked them against the artifact.
- Checked exact atom, probability sum, residual reassignment, midpoint physical rate units, and exact relative-bound fraction against the compact law.

The secular sign expression is `F(r)/q = 1 - r sum c_k/(k-r)`. At `r=a/D`, Python floor division encloses each signed term; negative denominators do not invalidate the bound. The reciprocal mixture-weight denominator term is `a D c_k k/(kD-a)^2`. Using lower endpoint numerator and maximum endpoint squared distance gives a lower bound, with the opposite choices giving an upper bound. No bracket contains a pole. The reciprocal floor/ceiling steps correctly enclose mixture mass. Exact signs, rather than floating proposals, establish the accepted roots. Missing floating proposals are covered by residual mass.

## Verified result

- Retained mass lies in `[0.99999951486269, 0.9999995148723965]` (displayed decimals are summaries of exact integer bounds).
- The exact stored residual evaluates to `4.85137309949773e-7`.
- The exact stored total relative bound evaluates to `0.03199136189858363`.
- Exact zero atom is `2^-128`.
- Physical rate units are `(a+b)/(2 D 2^307)`.

The residual is assigned to the first positive component. Hence the exact atom is preserved, and a categorical coupling can agree outside probability at most the certified residual. On agreement, the rate interval and rounding invariant give the displayed multiplicative clock bound.

The artifact therefore defines a reusable certified positive exponential-mixture approximation to this exact rational family. An actual certified finite-random-bit exponential sampler is not implemented. The benchmark uses floating NumPy exponentials and does not explicitly sample the tiny zero atom; it must remain labeled an uncertified floating benchmark. Arbitrary rational-generator spectral acquisition is also not implemented by this pipeline; its general polynomial-complexity statement remains a mathematical proof candidate.

## Reproduction versus independent mathematical checking

This audit's integer checker took approximately 5.47 seconds in its run. Separately, the parent replayed all four production scripts in a clean directory and obtained exactly equal compact-law JSON, observing approximately 0.116 seconds for DP, 0.354 seconds for floating proposals, and 5.212 seconds for certification. Those replay timings are reproducibility observations, not additional independent mathematical evidence.
