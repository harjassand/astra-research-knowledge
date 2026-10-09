# Primitive Genesis continuation — positive composition

**Date:** 10 October 2026 (Australia/Brisbane)

The principal result is a sharp composition bound for every finite-state positive lift of a spectrally gapped rotation action. It closes the specified five-gate qubit state-counting obligation and transfers to an exact memory–numerical-range theorem for positive interpolation. An independently explored Gaussian-likelihood characterization of convex order is also preserved, together with the limitations that prevent calling it a new efficient capability.

## Read first

`MAIN_THEOREMS.md` contains the full statements, definitions, proofs, hypotheses, counterexamples, source dependency, and explicit rational compiler.

`CONVEX_ORDER_PROBES.md` contains the complete order-characterization proof and scalar-profile counterexample.

`HANDOFF.md`, `CLAIMS.json`, and `SOURCES.json` preserve the decision boundary, dependencies, historical/verification status, and exact source revisions.

## Main conclusions

For a fixed finite rotation averaging law with an absolute L2 gap on the sphere, arbitrary m-state positive lifts obey

    (1 - 8/m)^T <= F_m(T) <= 2 exp(-c T/m)     (lower bound: m >= 16),
    1 - rho_m = Theta(1/m).

For the requested alphabet I, Rx(+/-theta), Rz(+/-theta), cos(theta)=3/5 and sin(theta)=4/5, the gap is supplied by the established Bourgain–Gamburd theorem. In the precise time/deadline-dependent-readout model,

    m_*(T; epsilon) = Theta(T), uniformly for 0 <= epsilon <= 1/72.

The upper construction is exact at delta=1/3. The lower bound uses only six preparations and one terminal observable. These are state counts, not total software workspace, time, or probability-description costs.

For exact unbiased positive interpolation on time-dependent grids,

    max final grid radius / max initial grid radius >= (1/2) exp(c T/m),

and an exp(C T/m) construction matches the exponent. No quantum hypothesis is required for this numerical-analysis statement.

## Verification

Run with Python 3 and the supplied requirements:

```bash
python verify.py
python -O verify.py
python verify_rational_mesh.py
python -O verify_rational_mesh.py
```

The scripts use explicit checks that remain active under Python optimization. The two programs contain **162 distinct check groups in total**: 123 in verify.py and 39 in verify_rational_mesh.py. These include 936 exact finite-word/preparation comparisons and 30 exact rational barycentric certificates, plus numerical identities, quadrature convergence checks, counterexamples, and finite harmonic diagnostics. The exact word enumeration uses a coarse grid and delta=1/81; it checks the compensation identity, not the entire delta=1/3 asymptotic theorem. The rational mesh certificates use delta=1/3 at T=3. Finite harmonic degrees 1–24 do not certify the all-mode gap.

Normal and optimized receipts are preserved separately. The default receipt files are overwritten by rerunning their corresponding programs. Counts are not doubled for the optimized reruns, and the historical checks inside the earlier packet are not counted as new checks.

NumPy/SciPy numerics propose supports in the rational mesh checker; SymPy exact arithmetic verifies every accepted support and weight. A failed exact check raises an exception. Results in other numerical environments may select different supports, but no floating-point candidate is accepted without its exact certificate.

## Status and provenance

All new derivations and diagnostics are from this one assistant research session. There has been no independent referee, external agent audit, Lean proof, empirical validation, or priority certification. A historic 9–10/10 breakthrough is **not established**. The argument imports an established external spectral-gap theorem and does not claim to have independently proved that theorem.

The original packet is preserved unchanged at `prior/primitive_genesis_retention.zip`; its SHA-256 is in SOURCES.json. No files in either GitHub repository were written.

The final unresolved research gate is stated precisely in MAIN_THEOREMS.md section 13 and HANDOFF.md. It is an unproved converse, not a claim that a celebrated open problem has been resolved.
