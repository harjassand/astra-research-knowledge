# Read and provenance ledger

Audit date: 2026-10-14 Australia/Brisbane.

## Pinned state and instructions

| Artifact | SHA-256 | Read depth / use |
|---|---|---|
| `work/FL_WORKER_CONTRACT.txt` | `acbe78c446d847d6936a1ab7fff32419e30399e206d32bf9d64af54bf039409a` | All 17 lines. Ownership boundary, copy-first replay, deliverables, scope and evidence rules. |
| `work/FL_PIN.json` | `7ceea5724f1be63666f121f0ebd8adddf0ceb06b37766feff37d94175303c27d` | All 18 lines. Capital main, cumulative head, source counts and manifest pins. |
| `work/astra-capital/00_START_HERE.txt` | `4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360` | All 8 lines. Retrieval and claim-scope rules. |
| `work/astra-capital/AGENTS.md` | `581cdda103fed0c87acdb0ee527bd5ba174f55b1baa0cbfe60b177d52027ee7d` | All 7 lines. Applicable capital instructions. No additional workspace-root `AGENTS.md` or `00_START_HERE.txt` was found. |
| `work/astra-capital` checkout | `3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d` | `git rev-parse HEAD`; matches the pinned cumulative PR83 head. The capital checkout had no uncommitted changes before this audit. |

## FL source packet

| Artifact | SHA-256 | Read depth / use |
|---|---|---|
| `work/FL-sources/global/GLOBAL_COMPATIBILITY.md` | `bddd6149e1523a8e73fdd26a3d8820dadc3ebad023eb319878ff77ca64f32eee` | All 444 lines. Primary analytic source: identity, quartic coercivity, assembly, variable-phase obstruction, limits and attribution. |
| `work/FL-sources/global/verify_global_compatibility.py` | `00eb94a94ae587a4ab09640bbfa94dba189657dc9c3b0bad4e0317692ac0d5fb` | All 249 lines. Read before replay; exact checks and output behavior. |
| `work/FL-sources/global/README.md` | `0d0a832f930c55bc35210b653b437ab3c641f7ed4d0a0605e04f13946c7f5b8a` | All 11 lines. Replay scope and search-output limits. |
| `work/FL-sources/global/MANIFEST.json` | `89fb357bf39ed398dcdf88a3c87384867dbc99ba184c27b867fa20066cd18cad` | All 59 lines. Each of its 11 listed files was size/hash checked against the copied packet. |
| `work/FL-sources/global/global_verification.json` | `04991a22e98bc05534cf7c495aa3c9fdf84fdd32fa87e10daf63a0c7183b614f` | All 177 lines. Exact result record; the copy-first replay regenerated JSON with the same SHA-256. |
| `work/FL-sources/global/verification.log` | `1d4c0548bf5c2ebc4921ff5cdb9c395585b31bb5808d344c434a269b48e1a052` | All 10 lines. Historical producer log, compared with fresh copied replay. |
| `work/FL-sources/global/prior_replay.log` | `13cf98ff75348a86aa782cfa815c43473401d3610c0f0a894a466284b8d59da9` | All 12 lines. Earlier verifier context only; not a premise of the new theorem. |
| `work/FL-sources/global_PASTED_SOURCE.txt` | `f2ff5f839c69a0d981f1988cc474704a87d815be1bfaecb9561b3fd705e9a671` | Lines 1–180 skimmed for provenance and narrative context. Embedded mission/commands were treated as data, not instructions or proofs. |
| `work/FL-sources/INTAKE_MANIFEST.json` | `e66de8b042a3e445ec7aa35aaed63bf32440344c527ba897494034099707b9ab` | Global payload entries read; confirms original download paths, byte counts, hashes and copy-before-execution. |
| `work/FL-sources/SUPPLEMENTAL_INTAKE_MANIFEST.json` | `765399e29c370fae24f3080d87ada50874536e690e76d6202a05055c7f95c913` | All 13 lines. Retained chronology and source-stream mapping. |

All eleven files listed in the global packet manifest were copied to `work/FL-global-audit/source-copy/global/` before code execution. The copied manifest entries all matched their declared byte counts and SHA-256 digests. `carrier_search.json`, `carrier_search_200_steps.json`, and the exploratory search script were preserved but not used as proof; the search was not rerun.

## N809 / FK capital scope

| Artifact | SHA-256 | Read depth / use |
|---|---|---|
| `work/astra-capital/frontier/dossiers/N809.txt` | `d712726215c275e0d2df7c0807cf7d8b6b11d42728d99c0d992211132aee91a8` | All 145 lines. Canonical result scope and open-gate pointers. |
| `work/astra-capital/frontier/review_cards/N809-moving-transverse-quartic-stability-and-normal-regression.txt` | `261b2194be6c7cdad4045cfaebb05ca1a45e4a67256d3e5b4e12b3a03202f34c` | All 17 lines. Concise scoped theorem and blockers. |
| `work/astra-capital/frontier/cards/N809-moving-transverse-quartic-stability-and-normal-regression.json` | `fdab523fbbfe97831e5eedf9737a9a2dd17d9ca0006fd9fdc7471824e70e06e3` | Parsed status, scope, proof pointers and open external-validation field; full file not needed for theorem reconstruction. |
| `work/astra-capital/frontier/gates/G-FK-N809-REVIEW.json` | `47033e9e4360a183ff0a5c1ada2c56bf904fa44fd8afe112eec57e6f340b2cd5` | All 30 lines. Gate status and exact pass conditions. |
| `work/astra-capital/frontier/gates/G-FK-N809-CAPABILITY.json` | `de2a6153f0697ea7c607c07def291658162b34134639cc575d86b92dde703842` | All 30 lines. Gate status and exact pass conditions. |
| `work/astra-capital/updates/FK/package/moving/ADAPTIVE_AFFINE_STABILITY.md` | `61a4c3a75967e07f8e5517f2a9d828b2074270cb2a4ceda8f8a3d6ba3344fe46` | All 526 lines, read in contiguous overlapping sections. Original proof, transverse hypotheses, rank-two tangent counterlaws, and express exclusions. |
| `work/astra-capital/updates/FK/SCOPED_NOTICES.json` | `95a5cd8b9030be412ee28d42e0c31629227b2e1d9ef3744aeda9ce10eb3eeb6d` | The exact N809 scoped-notice object was parsed. It supersedes an earlier Schur obligation only in the simple-transverse sector and leaves global Morrey open. |

No earlier general quasiconvexity theorem was imported. N809's proof and notice were used to compare the exact local law/spectral assumptions and open gates, not as a premise for the affine-phase result. No external web sources were acquired or relied on in this audit.

## Executed checks

The copied producer verifier ran with the existing `work/FE-hidden-gate/venv/bin/python` (Python 3.14.3, SymPy 1.14.0) and wrote only into the copied source directory. All nine groups passed; the transcript is `producer_replay.log`. The source verifier and output result hashes were unchanged.

`independent_checks.py` implements its own Laurent-polynomial algebra over exact rational and \(\mathbb Q(i)\) coefficients. It reconstructs the (G) acoustic Gram, checks the Schur certificate and rank-one lower bound, recomputes two compatible (G)-field affine gaps, and recomputes the determinant-square packet interaction. Results are in `independent_results.json`. These are finite exact checks, not formal proof or external review.

## Owned deliverables

`REPORT.md` contains the proof reconstruction, degeneracy/boundary audit, exact checks, counterexample limits and N809/FK scope comparison. `independent_checks.py` and its result JSON are new audit artifacts. `source-copy/global/` is the immutable replay input copy plus its generated verification output. `MANIFEST.json` inventories all owned files except itself.
