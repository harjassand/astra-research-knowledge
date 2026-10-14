# FL ancestry audit read ledger

All listed files were read from the frozen FL intake or pinned capital checkout. Hashes below are SHA-256 of the bytes read. Intake paths and source hashes were checked against the two FL manifests. The source and capital trees were not edited.

| Path | Bytes | SHA-256 | Read scope / use |
|---|---:|---|---|
| `work/FL_WORKER_CONTRACT.txt` | 3,118 | `acbe78c446d847d6936a1ab7fff32419e30399e206d32bf9d64af54bf039409a` | Entire contract; own-directory, source-preservation, proof/checker, ledger and manifest requirements. |
| `work/FL_PIN.json` | 795 | `7ceea5724f1be63666f121f0ebd8adddf0ceb06b37766feff37d94175303c27d` | Entire pin; actual capital checkout is the cumulative PR83 head `3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d`; main pin is `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871`. |
| `work/astra-capital/00_START_HERE.txt` | 1,879 | `4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360` | Entire capital start; route/dossier instructions and evidence-scope rules. |
| `work/astra-capital/AGENTS.md` | 1,077 | `581cdda103fed0c87acdb0ee527bd5ba174f55b1baa0cbfe60b177d52027ee7d` | Entire applicable capital instructions. |
| `work/FL-sources/INTAKE_MANIFEST.json` | 5,486 | `e66de8b042a3e445ec7aa35aaed63bf32440344c527ba897494034099707b9ab` | Entire manifest; establishes first intake includes temporal note and no ancestry script. |
| `work/FL-sources/SUPPLEMENTAL_INTAKE_MANIFEST.json` | 886 | `765399e29c370fae24f3080d87ada50874536e690e76d6202a05055c7f95c913` | Entire supplemental manifest; establishes later ancestry pasted report and no attached script. |
| `work/FL-sources/temporal/astra_temporal_ancestry_note.md` | 19,468 | `06b02159b294c894984b1985a866c75f159e8b9beff29dabeca927b0a6ca86b7` | Entire 240-line note, including all assumptions, formulas, simulation claims, costs, references and status. |
| `work/FL-sources/ancestry_PASTED_SOURCE.txt` | 24,782 | `0e77a93477641f41f98b357c0bc81eb914e03babaf7aa2bae8d91030b7698b5a` | Entire 328-line report; claim context, same theorem and synthetic-script discussion. |

The live `work/astra-capital` Git HEAD was read-only verified as `3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d`, matching the `checkout` and `cumulative_pr83_head` fields. The current dossier/concept search found no direct isotope-ancestry theorem to import. No capital theorem or external literature claim is used as a proof premise here. The source note's reference list was read as supplied provenance only; no independent prior-art review was undertaken in this lane.

No ancestry producer `.py` file appears in the frozen FL source inventory. The only `.py` files under `work/FL-sources` are the two unrelated global-compatibility scripts. Both scripts in this audit are new reconstructions. The independent finite/numeric checks were run with system Python 3.14 standard library; the fresh shared-code Monte Carlo was run using `work/FE-hidden-gate/venv/bin/python` with NumPy 2.5.3. Neither command executes source-provided code.
