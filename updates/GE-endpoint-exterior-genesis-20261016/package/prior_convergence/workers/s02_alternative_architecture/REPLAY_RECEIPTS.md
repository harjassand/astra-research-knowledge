# Recombination replay receipts

16 October 2026. Run from `/Users/harjas/Documents/ChatGPT/ultra`. These commands read only the worker scripts and the s01 geometry helper; they do not validate a physical quantum device, recursive threshold theorem, or arbitrary lattice size.

```sh
python3 research/2026-10-16-convergence-genesis-v1/workers/s02_alternative_architecture/check_bank_parity_decoder.py --all-modulo
```

Observed output:

```text
PASS clean states 120 two-site cases 282240 invalid 276480 wrong_or_ambiguous 0 valid_undetected 0
```

This enumerates all modulo-8 clean counter states reachable from zero on a 4x4 torus, then every arbitrary replacement of two counters on one tile. It assumes their outer-bank parities remain pristine. It checks uniqueness of the original four-counter repair when the focal tile is invalid, and absence of a globally valid same-parity counterfeit when it is not. The size-independent isolated-tile argument is in `RECOMBINATION_TEST.md`; the finite run is a falsification check, not that proof.

```sh
python3 research/2026-10-16-convergence-genesis-v1/workers/s02_alternative_architecture/check_emergency_traps.py --known-trap
```

Observed output:

```text
KNOWN_TRAP_REPRODUCED invalid_tiles [(0, (0, 1, 4, 5)), (1, (1, 2, 13, 14))]
```

The hard-coded flat-state injection has `(c_0,g_0)=(1,1)` and `(c_2,g_2)=(7,1)`. The checker verifies that none of the listed `R_v`, `R_P`, `A_P`, or `F_v` repair guards is enabled. The text proof in `RECOMBINATION_TEST.md` identifies the two mutually blocking tile constraints.

```sh
python3 -m py_compile research/2026-10-16-convergence-genesis-v1/workers/s02_alternative_architecture/check_bank_parity_decoder.py research/2026-10-16-convergence-genesis-v1/workers/s02_alternative_architecture/check_emergency_traps.py
```

Observed exit code: 0.
