# Continuous constrained sampler: finite-bit implementation

Start with **IMPLEMENTATION.md** for results, scope, deterministic arithmetic guarantees and reproduction commands. **FINITE_PROBABILITY_CONTRACT.md** gives the probability allocation and transport argument.

- Input: RAW_INPUT.npz, exact common-denominator rational matrices.
- Main driver: finite_bit_sampler.py. Defaults to OS-backed random bits; use --seed 17391 for pseudorandom replay.
- Saved runs: FINITE_BIT_DRAW.json, FINITE_BIT_SYSTEM_DRAW.json, FINITE_BIT_TIGHT_DRAW.json; accompanying *_SUMMARY.json files are concise.
- Replay and branch checks: verify_finite_bit_sampler.py, FINITE_BIT_VERIFICATION.json.
- Exact normal generation: certified_normal.py.
- Global per-run contract checks: check_global_contract.py and GLOBAL_CONTRACT_CHECKS.json. Exact finite-series guard inequalities: GENERATOR_MAJORANTS.json.
- Global parameter selection: probability_budget.py; tests in test_probability_budget.py.
- Earlier lower-precision local draw: certified_draw.py and CERTIFIED_DRAW.json. This local-only artifact does not meet the global budget; it remains separately labelled.
- File integrity: SHA256SUMS.

The included dense 128-by-128, two-constraint input certifies r=62>=36 natively. All saved accepted outputs have exactly zero homogeneous constraint residual in the high-precision driver. The W1 statement remains conditional on the stated mathematical proof contract and independent-bit model, not on the observed samples or formal verification. There is no performance or broad practical-validation claim.
