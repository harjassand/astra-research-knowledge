# ASTRA full-cone quartic rigidity

## Read first

`ASTRA_FULL_CONE_RIGIDITY.md` contains the analytic statements, proofs, limits, and attribution.

The full nine-coefficient rank-one-convexity => quasiconvexity implication is **not** proved. The results are a general one-quadric nullspace-closure theorem, a full-cone exceptional-class classification, and a genuine Jensen theorem on all singular averaged-Hessian faces. Exact singular faces are handled; near-singular limits and the positive-definite sector remain unresolved.

## Exact verification

Requirements: Python 3 and SymPy.

```bash
python verify_rigidity.py
```

This reconstructs twelve groups of exact checks from definitions written in the script. It needs no optimizer, numerical matrices, internet connection, pickle, or previous artifact. It writes `exact_checks.json`. `verification.log` records the current successful execution.

The verifier does not formally establish the measure-theoretic or Fourier arguments. Those are proved in the note. Historical novelty and external mathematical validation are not established.

## Contents

- `ASTRA_FULL_CONE_RIGIDITY.md`: complete current analytic note.
- `verify_rigidity.py`: standalone exact checker.
- `exact_checks.json`, `verification.log`: exact check results.
- `prior_sharp_verifier_replay.log`: successful replay of the preceding sharp-scalar verifier; continuity evidence, not a premise of the new proofs.
- `exploratory_evidence/`: one floating-point Fourier-search output and the retained numeric candidate/field parameters. These are not exact certificates and are not inputs to the new verifier. The complete exploratory heat/SDP scratchpad is not required or represented as formally verified by this package.
- `MANIFEST_SHA256.json`: integrity hashes, not proof validation.

No source manuscripts or fonts are redistributed. No repository write was performed.
