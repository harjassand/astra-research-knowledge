# ASTRA: positive-definite compatibility barrier

Research date: 14 October 2026.

Read `ASTRA_POSITIVE_DEFINITE_BARRIER.md` for the theorem statements, analytic proofs, exact counterexamples to proposed continuity transfers, and unresolved questions.

## Main status

The full nine-coefficient rank-one-convexity-to-quasiconvexity implication is not proved. No compatible negative quasiconvexity gap is supplied. The explicit compatible sequence disproves continuity of the optimized cubic loss near a nonzero singular Hessian; its actual variational gap is positive.

The full-cone two-contact classification, acoustic covariance estimate, and contact-shear theorem are internally proved and exactly checked where finite algebra is involved. Historical priority, external mathematical review, and proof-assistant formalization remain unestablished.

## Exact verification

Run from this directory:

```bash
python verify_positive_definite.py
```

This requires Python 3 and SymPy. The script writes `positive_definite_verification.json` beside itself. It reconstructs all constants internally and does not load the supplied JSON, numerical optimization output, or previous research artifacts. The analytic arguments are in the Markdown note; the finite checks do not replace them.

The supplied `verification.log` records twelve passing groups. `prior_replay.log` records the replay of the previous rigidity verifier, which is not needed to run the present standalone verifier.

## Exploratory evidence

`exploration/` preserves selected numerical search and exact auxiliary computations. These files are not premises of the main verifier. The Fourier search additionally requires NumPy and PyTorch; it used six seeds, cutoff three, a 13-by-13 grid, and 800 steps. No negative gap was found. Its values are local-search observations, not lower bounds. Some auxiliary scripts may expect their named JSON output to be beside the script.

No third-party manuscripts, model weights, fonts, or private credentials are included. No repository publication was performed.

`MANIFEST.json` records SHA-256 hashes of the included payload files; it does not certify mathematical correctness.
