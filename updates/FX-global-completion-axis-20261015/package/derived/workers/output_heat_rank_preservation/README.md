# Output-matrix heat rank-preservation audit

The root's extension is confirmed: for every real constant spatial-symmetric output-matrix generator satisfying coercive strong parabolicity, one common compact datum u0=(f,f²), f=x+xy near zero, has det Du0=0 everywhere and initial determinant velocity 4 C^{11}_{22}>0 at zero. Its determinant-square energy therefore increases at small positive times.

The audit also proves:

- Every nonzero homogeneous constant second-order operator has a compact compatible map with strictly negative integrated determinant-square dissipation, even without parabolicity. Hence no universally integral-null correction can make this same dissipation pointwise nonnegative.
- The zero operator is the only homogeneous constant second-order planar operator universally tangent to every rank-one gradient.
- C1 autonomous state/gradient-dependent nondivergence principal flows with a strongly parabolic coefficient at zero fail the same universal monotonicity, conditional on classical solution existence and the stated differentiation.
- The constant-coefficient determinant-square obstruction extends to every square dimension n>=2.

Read [ANALYTIC_PROOF.md](ANALYTIC_PROOF.md) for the proofs, conventions, and exclusions; [CLAIMS.json](CLAIMS.json) for machine-readable scope; [SOURCE_REVIEW.md](SOURCE_REVIEW.md) for provenance and the limited primary-source review.

Run from this directory:

```sh
python3 verify_output_heat.py
```

The verifier uses SymPy 1.14.0 and writes [VERIFICATION.json](VERIFICATION.json). It reconstructs local polynomial identities, the generalized dissipation divergence identity, the full-rank coefficient classification, the adaptive first-jet formula, and finite-dimensional consistency checks. It does not integrate a noncompact polynomial or replace the analytic cutoff/semigroup arguments with samples. Exact symbolic verification is not proof-assistant formalization or independent external review.

The density (det A)² is still polyconvex and quasiconvex. None of these obstructions is a Morrey counterexample. Historical novelty remains unresolved. This worker writes only in its own directory; source packages, the integration checkout, and GitHub are not edited.
