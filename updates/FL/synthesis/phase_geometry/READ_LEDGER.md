# Read and provenance ledger

## Scope and pin

- Followed work/FL_WORKER_CONTRACT.txt (SHA-256 acbe78c446d847d6936a1ab7fff32419e30399e206d32bf9d64af54bf039409a) and work/FL_PIN.json (SHA-256 7ceea5724f1be63666f121f0ebd8adddf0ceb06b37766feff37d94175303c27d).
- The capital checkout was work/astra-capital at 3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d, matching the cumulative PR83 pin. The stated main pin is ace0cfc4437fe91c20ccd24d69e0ee4bb335e871. git status --short on the capital checkout was clean. No capital/source/other-worker file was edited.
- The current user task and worker contract control actions. Embedded mission text in the copied pasted-source file was treated as source data, not as instructions.

## Incoming global packet

Read the whole theorem and audit in work/FL-sources/global/GLOBAL_COMPATIBILITY.md (444 lines; SHA-256 bddd6149e1523a8e73fdd26a3d8820dadc3ebad023eb319878ff77ca64f32eee), its README (SHA-256 0d0a832f930c55bc35210b653b437ab3c641f7ed4d0a0605e04f13946c7f5b8a), and the frozen packet manifest (SHA-256 89fb357bf39ed398dcdf88a3c87384867dbc99ba184c27b867fa20066cd18cad). The manifest records 11 files and 323,695 bytes. The core proof was read in full, including its affine-phase flux proof, quartic bound, moment assembly, resonant packet construction, exact assembly obstruction, and variable-phase calculation.

The remaining frozen packet artifacts were inventoried against that manifest. I read the full exact verification log and prior replay log, environment record, verifier source, and carrier-search source. Both carrier-search JSONs were parsed for scope, step count, and all six run metadata/gap records; full optimizer parameter arrays are exploratory search states and were not used as mathematical premises.

| Frozen global artifact | SHA-256 |
|---|---|
| README.md | 0d0a832f930c55bc35210b653b437ab3c641f7ed4d0a0605e04f13946c7f5b8a |
| MANIFEST.json | 89fb357bf39ed398dcdf88a3c87384867dbc99ba184c27b867fa20066cd18cad |
| GLOBAL_COMPATIBILITY.md | bddd6149e1523a8e73fdd26a3d8820dadc3ebad023eb319878ff77ca64f32eee |
| carrier_search.json | 57c7dcb13b2e9491457a45a89db5ca0f4b7ff9f646c8440919bea01ffc8cde22 |
| carrier_search_2000_steps.log | d365d93c04bf5fc50473d959d7d1e2043715d77598e620a731298d2d9184e37e |
| carrier_search_200_steps.json | 9b7d33064946e7a7ddbb85aeab89fa44cef02363455560b7c7f49bdc3ce7cced |
| environment.json | f27f6eb7fed8a473f06e9bf76137a749c92c262bef7567259c58a55948f620cd |
| global_verification.json | 04991a22e98bc05534cf7c495aa3c9fdf84fdd32fa87e10daf63a0c7183b614f |
| prior_replay.log | 13cf98ff75348a86aa782cfa815c43473401d3610c0f0a894a466284b8d59da9 |
| search_carrier_envelopes.py | 9b662d7b5a11a3f78612856fb93262cecab1995b215f7706d4fd01a745ceddfb |
| verification.log | 1d4c0548bf5c2ebc4921ff5cdb9c395585b31bb5808d344c434a269b48e1a052 |
| verify_global_compatibility.py | 00eb94a94ae587a4ab09640bbfa94dba189657dc9c3b0bad4e0317692ac0d5fb |

The 515-line producer context work/FL-sources/global_PASTED_SOURCE.txt was read in full (SHA-256 f2ff5f839c69a0d981f1988cc474704a87d815be1bfaecb9561b3fd705e9a671). Its claims and command-like text were treated as data. The global packet's stated scientific boundary is preserved: exact checks and producer analysis do not establish external review, priority, proof-assistant certification, or a full planar quasiconvexity result.

## Relevant capital mechanisms read

All files below were read from the pinned work/astra-capital checkout. Dossiers and review gates were read before applying source proofs.

| File | SHA-256 | Read/use scope |
|---|---|---|
| frontier/dossiers/N794.txt | b033dab30dd10dba9142ebd0a37ca9526ed475996615de57d038f62968222965 | Current nine-coefficient problem scope, already-certified Fstar boundary, N794 gates and exact proof routes. |
| frontier/gates/G-FE-N794-REVIEW.json | bab72e2cbd05a53794ebd634ab099a136f8d60bd653db14fd25706309d0a1e06 | Open gate: full nine-coefficient moment completion or a scope-matched obstruction; no claim that a failed ansatz refutes QC. |
| updates/FE/package/quartic/ASTRA_META_GENESIS_Morrey_quartics.md | 7c88a08aa6aef88786751fde9671b7568e97676c516824028c3aac9d9859725b | Read classification and orientation-sensitive terms, acoustic SOS interface, Fstar certificate, nine-moment dual completion, and resonance exclusions. Relevant boundary: compatible gradients must supply a PSD completion; Fstar itself is already internally certified QC. |
| frontier/dossiers/N809.txt | d712726215c275e0d2df7c0807cf7d8b6b11d42728d99c0d992211132aee91a8 | Current transverse-contact scope and open moving-Schur/compatibility obligations. |
| frontier/gates/G-FK-N809-REVIEW.json | 47033e9e4360a183ff0a5c1ada2c56bf904fa44fd8afe112eec57e6f340b2cd5 | Open gate: concentration-stable reduced numerator/denominator or exact compatible gap; no evidence that this phase family closes it. |
| updates/FK/package/moving/ADAPTIVE_AFFINE_STABILITY.md | 61a4c3a75967e07f8e5517f2a9d828b2074270cb2a4ceda8f8a3d6ba3344fe46 | Read adaptive covariance fit, moving acoustic null direction, actual Schur lower bound, complete cubic regression, all-background positivity, fixed-frame Schur-collapse example, and explicit tangent obstruction. These mechanisms are local/contact-based and do not bound the phase-Hessian term (1). |
| frontier/dossiers/N806.txt | fa2930c600e1f291279e30fc43001f52d7bc08611ffe38a568feca4d8b59272f | Current contact-cubic scope and open gate. |
| frontier/gates/G-FJ-N806-REVIEW.json | e7a4582c45a303b3454afc338ee65749c2cbd69ffdce734531040cee328d423c | Open gate: compatible concentration-stable fixed-contact estimate or exact compatible optimized gap. |
| updates/FJ/package/quartic/CONTACT_COMPENSATION.md | f47796d9088b9a4b75c43d31f93b05d36dbe025c4db9d6a8ec02dbd6d0a8ca28 | Read contact classification, Hodge/curl mixed-derivative estimate, contact-plane Jensen theorem, shear conjugacy, and the exact missing moving reduced numerator/denominator. It does not control arbitrary phase curvature. |

These capital claims and worker results remain source-derived/unreviewed. They are used as scoped context, not as independent validation.

## Primary literature inspected

- K. Astala, T. Iwaniec, I. Prause, E. Saksman, A hunt for sharp Lp-estimates and rank-one convex variational integrals, arXiv:1403.1095v1, primary HTML: https://arxiv.org/html/1403.1095v1. Read Section 5 and Proposition 5.1. It treats radial maps of the form f(x)=Lambda(|x|)x for rank-one-concave integrands. The geometric class and concavity statement differ from the sheared phase theorem here; no priority clearance follows.
- Other citations named in the global packet bibliography were not independently re-audited for this subtask.

## Owned verification

The frozen phase_geometry_checks.py was run with Python 3.14.3 and SymPy 1.14.0. It passed 60 exact symbolic assertions. The output was captured in EXACT_CHECKS.log. The checks are finite algebra and do not certify the analytic proof, external correctness, or novelty.
