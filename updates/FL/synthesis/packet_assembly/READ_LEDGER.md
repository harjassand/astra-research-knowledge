# Read ledger — FL packet assembly

Research date: 2026-10-14. Scope: cold reconstruction and strengthening of the global Fourier-packet assembly argument. All owned material is in `work/FL-packet-assembly/`. No capital, source, or other FL worker file was modified. No other FL worker output was read.

## Contract and pinned capital

| Input | SHA-256 / version | Read scope and use |
|---|---|---|
| `work/FL_WORKER_CONTRACT.txt` | `acbe78c446d847d6936a1ab7fff32419e30399e206d32bf9d64af54bf039409a` | Read in full. Followed the owned-directory, copy-before-execution, capital/source immutability and evidence-scope requirements. |
| `work/FL_PIN.json` | `7ceea5724f1be63666f121f0ebd8adddf0ceb06b37766feff37d94175303c27d` | Read in full. It distinguishes main `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871` from the cumulative PR83 checkout `3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d`; its separate published Ultra pin is `00d1c9769bc26829fef2653dbcc10ed1dc8a927c`. |
| `work/astra-capital/00_START_HERE.txt` | `4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360` | Read in full before targeted retrieval. |
| `work/astra-capital/AGENTS.md` | `581cdda103fed0c87acdb0ee527bd5ba174f55b1baa0cbfe60b177d52027ee7d` | Read in full. |
| `work/astra-capital` checkout | HEAD `3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d`; branch `research/capital-synthesis-active-certificates-20261014`; initially clean | Read-only status check. This working checkout is the cumulative PR83 head, distinct from the main pin in `FL_PIN.json`. |
| `work/astra-capital/frontier/dossiers/N809.txt` | `d712726215c275e0d2df7c0807cf7d8b6b11d42728d99c0d992211132aee91a8` | Read lines 1–45. The exact scope remains simple-transverse near-line stability; general large-transverse fields are excluded and the global left-SO(2) completion gate is open. |
| `work/astra-capital/updates/FK/synthesis/quartic_global/REPORT.md` | `29a3890d04a90300277b4abbdb15a696e51f5a35eec5667dd01b82be1411911f` | Read all 109 lines. Used its finite PSD moment-completion obligation and exact statement that the arbitrary compatible-profile decomposition is still missing. |

## Supplied global packet and original verification

| Input | SHA-256 / size | Read scope and use |
|---|---|---|
| `work/FL-sources/INTAKE_MANIFEST.json` | `e66de8b042a3e445ec7aa35aaed63bf32440344c527ba897494034099707b9ab` | Read in full to confirm the source copy and chronological intake. |
| `work/FL-sources/global/MANIFEST.json` | `89fb357bf39ed398dcdf88a3c87384867dbc99ba184c27b867fa20066cd18cad` | Read in full for source byte counts and hashes. |
| `work/FL-sources/global/GLOBAL_COMPATIBILITY.md` | 32,255 bytes; `bddd6149e1523a8e73fdd26a3d8820dadc3ebad023eb319878ff77ca64f32eee` | Cold-read Sections 5–6, lines 234–331, including moment assembly, range/minimizer formula, Fourier resonance criterion, dilation, component reduction and the determinant-square obstruction. Copied byte-identically to `GLOBAL_COMPATIBILITY_SOURCE.md`. |
| `work/FL-sources/global/verify_global_compatibility.py` | 12,325 bytes; `00eb94a94ae587a4ab09640bbfa94dba189657dc9c3b0bad4e0317692ac0d5fb` | Read in full. Decisive code: quartic moment/affine minimum lines 124–137; Fourier packet gluing lines 182–195; exact resonant obstruction lines 197–207. Copied byte-identically before execution. |
| `work/FL-sources/global/global_verification.json` | 3,862 bytes; `04991a22e98bc05534cf7c495aa3c9fdf84fdd32fa87e10daf63a0c7183b614f` | Read in full; copied to `original_global_verification.json`. It records nine exact finite-check groups and explicitly limits their scope. |
| `work/FL-sources/global/verification.log` | 922 bytes; `1d4c0548bf5c2ebc4921ff5cdb9c395585b31bb5808d344c434a269b48e1a052` | Read in full; copied to `original_verification.log`. |
| `work/FL-sources/global/environment.json` | Source-declared Python 3.13.5, SymPy 1.14.0, NumPy 2.3.5, Torch 2.10.0+cpu | Read in full. The replay below instead used the already installed scientific venv available in this workspace; no package was installed. |

The source package's exact verification was replayed only from the owned copy:

```text
work/FE-hidden-gate/venv/bin/python work/FL-packet-assembly/verify_global_compatibility.py
```

The runtime was Python 3.14.3 and SymPy 1.14.0. All nine groups passed. The generated `global_verification.json` is byte-identical to the copied source JSON, with the same SHA-256 above. The run log is retained as `rerun_verification.log`. This is a source replay and finite algebraic evidence, not analytic proof certification.

## Independent exact work

| Owned artifact | Method and scope |
|---|---|
| `independent_packet_checks.py` | Authored from scratch using only Python standard-library `Fraction` arithmetic and sparse Laurent coefficient convolution. It does not import the supplied verifier. |
| `independent_packet_checks.json` | Reproducible exact outputs for the resonant moment-factorization example, degree-six dependence witness, positive `|A|^4` optimized composition, fixed-integrand coefficient relaxation, affine-optimized determinant-square obstruction, and growing connected resonance examples. |
| `independent_packet_checks_run.log` | Captured stdout of the independent exact checker; all exact assertions completed and JSON was written. |
| `REPORT.md` | Self-contained reconstruction, generalized coefficient-match theorem, pseudoinverse/nullspace conditions, exact examples and limits. |

Command:

```text
work/FE-hidden-gate/venv/bin/python work/FL-packet-assembly/independent_packet_checks.py > work/FL-packet-assembly/independent_packet_checks_run.log
```

The checker uses no third-party runtime even though it was launched from the existing venv. Exact finite checks do not establish global quasiconvexity, external correctness, or priority. No external literature comparison was needed for these algebraic claims, and no novelty claim is made.

## Access and exclusions

No access failures occurred. No exploratory carrier search was rerun. No capital file, source file, other worker directory or external application was modified. No messages were sent. Original inputs remain unchanged.
