# Read and replay ledger

## Pin and authority

- Workspace source pin: `work/FO_PIN.json` records checkout/main revision
  `1c45f77e32d6fbd72483aed5014061c7bda4f372`, branch
  `research/profile-circulation-causal-operations-20261015`, and merged PR 83.
  That file was read in full. The workspace root has no accessible `.git`
  metadata (`git rev-parse HEAD` returned “not a git repository”), so a live
  VCS HEAD could not be independently confirmed; the pin is source-provided.
- The worker contract was read in full. All new writes are confined to this
  assigned `storage_critique/` directory. No other FO worker output was
  consulted, no source-directory script was executed, and no nested agent or
  external service was used.
- No external literature was acquired or relied on. The analytic claims below
  are reconstructed from the local statement plus the pinned N794/N812 source
  proofs; external correctness and priority remain UNKNOWN.

## Sources read

Hashes below are SHA-256 of the current local bytes at audit time. “Read” is the
depth used for this critique, not a claim that every proof in a larger source
was reviewed.

| Source | SHA-256 | Read depth and use |
|---|---|---|
| `work/FO_WORKER_CONTRACT.txt` | `9b2e4424660e44b95a6d8d8c72f8dae8d34c674c3a107ebc932648878b210ee7` | Full, 13 lines. Owned-output, evidence, source-proof, and freeze requirements. |
| `work/FO_PIN.json` | `3e33623d46231fbf7479574f73a63f7fd9c8e0ca8d9999efb9c18d8bce30ec56` | Full, 29 lines. Source revision and namespace pin. |
| `work/FO-root/CONTINUUM_STORAGE_DRAFT.md` | `f9fe6c072576ce6235fbc9121c3d3d90caf51a1b99d95b4646e17c78a852bb4d` | Full, 59 lines. Independently rebuilt the real-amplitude Fourier averages, two Gram identity, matrix minors, affine transfer, and frequency scaling. |
| `work/FO-root/CONTINUUM_STORAGE_THEOREM.md` | `cb222cae25212a833308ba25bfec95aa1148b06582557c188b8ed40729ddd88a` | Full, 158 lines. Cold-audited the complex-amplitude phase gauge, 12+9 Gram identity, regularity, all-background step, and theorem boundaries. |
| `work/FO-root/CONTINUUM_STORAGE_CERTIFICATE.json` | `cb238e8d41f583c88dfed851f0e948d40034a33afd0b8e2c9a97283a2b2f1315` | Full, 334 lines. Used the listed rational matrices only as candidate certificate data; recomputed the polynomials and all leading minors in the owned checker. |
| `work/FO-root/discovery/EXACT_STORAGE_CERTIFICATE.json` | `acfad54aac4cf884e318daea42e39927838877e23d82ab81606ba6c6c5e8ffc9` | Full, 117 lines. Original real-amplitude exact identity and 6+4 matrices. |
| `work/FO-root/verify_continuum_storage.py` | `8e1f7474b240d17a3cf1828f624fdce760b1361b7f70e95fa2797969b6158f85` | Read, 111 lines; not executed. The independent replay is `verify_storage_critique.py`. |
| `work/FM-sources/resonant/PROFILE_CIRCULATION.md` | `881b80eac0bcfd04113dcba7226b9faee324dda66d44ffee5ae3ea097b072622` | Relevant sections read: lines 52–80 and 125–166. This states the signed polynomial circulation identity and the six degree-two area moments; used to distinguish universal cancellation from the fixed-integrand positive storage theorem. |
| `work/astra-capital/frontier/dossiers/N794.txt` | `bdd17cc2ca4802a5e935fe5aeddd53a1b23bfcb56d45b04a3f113cba5db00a63` | Relevant status and gates read, lines 1–30. N794 remains source-derived/unreviewed; external review and broader acoustic-cone completion remain open. |
| `work/astra-capital/updates/FE/package/quartic/ASTRA_META_GENESIS_Morrey_quartics.md` | `7c88a08aa6aef88786751fde9671b7568e97676c516824028c3aac9d9859725b` | Relevant acoustic criterion read, lines 230–270. The binary-biquadratic Gram criterion and its proof justify checking rank-one Hessian positivity with an exact acoustic completion. |
| `work/astra-capital/frontier/gates/G-FE-N794-REVIEW.json` | `bab72e2cbd05a53794ebd634ab099a136f8d60bd653db14fd25706309d0a1e06` | Full, 30 lines. Gate is OPEN; required external review and broader cone completion are not supplied by this fixed-G theorem. |
| `work/astra-capital/frontier/dossiers/N812.txt` | `523627d823b1c93be90a6197e8d8e07d2a78360e11de81c0309170794721d2a4` | Relevant status and gates read, lines 1–20. N812 leaves arbitrary compatible-moment completion outside certified families open. |
| `work/astra-capital/updates/FL/package/global/GLOBAL_COMPATIBILITY.md` | `bddd6149e1523a8e73fdd26a3d8820dadc3ebad023eb319878ff77ca64f32eee` | Relevant proof sections read: lines 27–106, 107–204, 205–233. Read the general modulation proof, invariant-quartic coercivity and G acoustic certificate, and the separate complex one-coordinate-envelope scope. |
| `work/astra-capital/updates/FL/package/global/verify_global_compatibility.py` | `00eb94a94ae587a4ab09640bbfa94dba189657dc9c3b0bad4e0317692ac0d5fb` | Read, lines 1–95. Its rational skew completion was treated as an acoustic-Gram candidate; my own checker differentiates G and verifies the polynomial identity, minors, and Schur complement. The source script was not run. |
| `work/astra-capital/updates/FL/synthesis/global_audit/independent_checks.py` | `0b8c4d517cf3ac52330c16810af395ef340c064f71da7b798f7a4ee89711a848` | Read, lines 120–180, to confirm the separate source reconstruction scope. Not run or imported. |
| `work/astra-capital/frontier/gates/G-FL-N812-REVIEW.json` | `cb9c7ab478b4b3e45835ebac769feeac8254fb05c967e96bded541987f2c47e2` | Full, 30 lines. Gate is OPEN; full compatible-moment construction/separation and independent review remain required. |

## Replay

Command, from the workspace root:

```text
/Users/harjas/Documents/Codex/2026-10-14/astra-research-capital-integration-synthesis-breakthrough/work/FE-hidden-gate/venv/bin/python work/FO-curvature-classification/storage_critique/verify_storage_critique.py
```

Environment: Python 3.14.3, SymPy 1.14.0. Exit status: 0. The checker passes
17 exact groups, including independently computed real and complex Laurent
averages, both storage identities, every supplied Gram leading minor, the
rank-one acoustic Gram identity and Schur complement, quartic Hessian
reciprocity, half-turn expansion, radial phase-chain rule, frequency scaling,
and an exact unit-square loop with all six nonzero moments. The complete exact
output is saved in `EXACT_CHECKS.json`; the command transcript is
`EXACT_REPLAY.log`.

The script uses only local SymPy arithmetic. It does not call an optimizer or
root/worker verifier. The report supplies the analytic W1,4, Parseval, phase
gauge, and coboundary arguments not mechanically certified by coefficient
checks.

## Cost and validation limits

All mathematical inputs were already present in the workspace. Acquisition,
calibration, physical preparation, noise, and paid-service costs are zero for
this local replay; inference-token and aggregate financial costs were not
measured. Exact arithmetic verifies the listed identities and matrix
certificates only. It is not formal proof-assistant verification, external
mathematical review, historical-priority review, or evidence of physical
capability.
