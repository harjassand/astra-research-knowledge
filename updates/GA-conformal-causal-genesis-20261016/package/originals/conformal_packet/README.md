# Cubic compatibility at the positive conformal contact

The sharp positive-coupling quasiconvexity problem remains unresolved in this packet. No compatible negative Jensen field is supplied.

Start with **RESEARCH_REPORT.md**. Its main result is an exact selection rule for which homogeneous cubics admit bounded compensation under the rank-varying conformal operator. It also gives a nonlocal cubic resolvent, a quantitative estimate, a concentration limitation, and exact failures of stronger proposed bounds.

## Replay

Python 3.10+ and SymPy are sufficient for the standalone checks:

```sh
python verify_compatibility.py
```

The script reconstructs all algebra from the displayed quartic and reads only `EXACT_RESONANCE_FIXTURE.json`. It uses explicit runtime checks, not assertions. All 21 groups pass. The receipt does **not** machine-verify interpolation, Hodge decomposition, density, or the complete all-gradient analytic theorems.

`inputs/` preserves the two immutable incoming ZIPs; their replay logs and hashes are in `evidence/` and `INPUT_AUDIT.json`. `exploration/` preserves local searches and failed representations. Those are not a portable or certified optimization service and are not needed for verification. `SOURCES.json` distinguishes actual reading scope from historical-priority clearance. `RESEARCH_STATE.json` identifies the exact missing sharp inequality.

Neither publication, exact algebra, nor same-model reconstruction establishes independent external review or historical novelty.
