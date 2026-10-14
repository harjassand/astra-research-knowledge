# Read and provenance ledger: curved N794 completion

## Scope and isolation

This is a new synthesis packet under `work/FL-global-moments/curved_completion/`.
The frozen parent packet files (`REPORT.md`, `READ_LEDGER.md`, its verifier,
results, and manifest) were not edited. No root, phase-worker, source, or
capital file was modified. The read-only capital checkout was at
`3c9c5564fc7f51cdbaa0a5a5b5b54ee9382dcd8d`, matching the pin; its
`git status --short` was empty after this work.

## Contract, pin, and capital status inputs

These were read as recorded in the preceding global-moments packet ledger,
and their current hashes were rechecked for this synthesis.

| Input | Read/use scope | SHA-256 |
|---|---|---|
| `work/FL_WORKER_CONTRACT.txt` | All 17 lines; isolated work, proof artifact, provenance, and claim-scope requirements. | `acbe78c446d847d6936a1ab7fff32419e30399e206d32bf9d64af54bf039409a` |
| `work/FL_PIN.json` | All 18 lines; pinned capital/main/cumulative revisions and source manifests. | `7ceea5724f1be63666f121f0ebd8adddf0ceb06b37766feff37d94175303c27d` |
| `work/astra-capital/00_START_HERE.txt` | All 8 lines; capital route retrieval and proof-scope rules. | `4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360` |
| `work/astra-capital/frontier/dossiers/N794.txt` | All 108 lines; nine-coefficient completion problem and open global compatibility gate. | `b033dab30dd10dba9142ebd0a37ca9526ed475996615de57d038f62968222965` |
| `work/astra-capital/frontier/gates/G-FE-N794-REVIEW.json` | Open nine-moment PSD-completion or scope-matched obstruction gate. | `bab72e2cbd05a53794ebd634ab099a136f8d60bd653db14fd25706309d0a1e06` |
| `work/astra-capital/updates/FE/SCOPED_NOTICES.json` | N794/Fstar scope and source-status notices. | `9f6381c84e72a6db67f26affa61d31b9361701dfd1177c2ac8e2f31eb52a3fb3` |
| `work/astra-capital/frontier/dossiers/N809.txt` | All 145 lines; full35 simple rank-three transverse local all-background scope and open tangent/global gates. | `d712726215c275e0d2df7c0807cf7d8b6b11d42728d99c0d992211132aee91a8` |
| `work/astra-capital/frontier/gates/G-FK-N809-REVIEW.json` | Open concentration-stable transverse estimate or exact compatible-gap gate. | `47033e9e4360a183ff0a5c1ada2c56bf904fa44fd8afe112eec57e6f340b2cd5` |
| `work/astra-capital/updates/FK/SCOPED_NOTICES.json` | Full35 transverse result scope, tangent/rank-two/global limits, source-status notices. | `95a5cd8b9030be412ee28d42e0c31629227b2e1d9ef3744aeda9ce10eb3eeb6d` |
| `work/astra-capital/frontier/dossiers/N806.txt` | All 130 lines; fixed-contact cubic-compensation scope and open gate. | `fa2930c600e1f291279e30fc43001f52d7bc08611ffe38a568feca4d8b59272f` |
| `work/astra-capital/frontier/gates/G-FJ-N806-REVIEW.json` | Open compatible concentration-stable fixed-contact estimate or exact gap gate. | `e7a4582c45a303b3454afc338ee65749c2cbd69ffdce734531040cee328d423c` |
| `work/astra-capital/updates/FJ/SCOPED_NOTICES.json` | Fixed-contact compensation scope and retained moving-background limits. | `78b9508a299bb165ba27dbcf913779cc04980b7af109e2015fe46b69c7dd96a6` |
| `work/astra-capital/updates/FE/package/quartic/ASTRA_META_GENESIS_Morrey_quartics.md` | N794 invariant basis, acoustic Gram/dual interface, Fstar and general completion boundary (read in the preceding ledger). | `7c88a08aa6aef88786751fde9671b7568e97676c516824028c3aac9d9859725b` |

The preceding `work/FL-global-moments/READ_LEDGER.md` records the broader
source intake, source manifests, pinned capital history, and exact prior
checks. The capital claims remain source-derived and externally unreviewed.

## The two worker results joined

| Input | Read/use scope | SHA-256 |
|---|---|---|
| `work/FL-phase-geometry/REPORT.md` | Full phase-flux derivation, signed curvature defect, sheared all-background theorem and hypotheses (9), exact profile and limitations. | `9c6149286ff3de35619c7b6efb84786481f3b9e64e212a418c0c369d5b32b67b` |
| `work/FL-phase-geometry/phase_geometry_checks.py` | Exact identity and curvature checks; used as source evidence, not as an external verifier. | `95472e8324d83ac5e6c6c5a06cdb9f97539a707c12c8aaec350e4249648e54ca` |
| `work/FL-phase-geometry/READ_LEDGER.md` | Original phase worker provenance and read inventory. | `83600e784057cc229642d0e0ed49a0f027cae63e73ab9082975269a6ffa904a1` |
| `work/FL-global-moments/REPORT.md` | N794 basis, explicit acoustic atom map, global modulation completion, and exact profile boundary. | `633f4e1fb206b786082f2da9812e63ac7117c653f1fd2d4993631ca8fe22b38f` |
| `work/FL-global-moments/verify_global_moment_bridge.py` | N794 acoustic matrices and exact nine-pairing implementation. | `09f65ad03a58c708cb8ba497b7f9c169ea11072365249b1adfa490135c5896bd` |
| `work/FL-global-moments/READ_LEDGER.md` | Original global worker source ledger. | `547da017ce70bc43b3db0e3837f8a35d11ca5c290fcecd7f56f3955f0a1d084b` |

The phase worker is a same-team internal derivation, not independent external
verification. Its hypotheses and status were preserved. The N794 8×8 basis
and acoustic-Gram pairing were taken from the global-moments packet and its
exact implementation.

## Owned derivation and check

The report derives (Y_0) from the phase flux identity after applying the
two weighted curvature cancellations to each of the three orientation-odd
coefficients. It derives (Y_H(B)) from the real Fourier expansion of a
compatible periodic gradient, with the factor (1/4) coming from normalized
cosine/sine means (1/2) and the Taylor coefficient (1/2). It then pairs
both matrices in the same N794 basis and records a half-turn profile
obstruction to direct pointwise generation of the connected triad.

`verify_curved_completion.py` was run with Python 3.14.3 and SymPy 1.14.0.
All 14 exact assertions passed. The checks include an explicit rational
curved-profile (Y_0), all nine N794 pairings, both weighted cancellations,
the exact Fourier-Hessian pairings at a rational background, the half-turn
Taylor identity, skew-block constraints, and the connected-triad anti-period
obstruction. `verification_results.json` records the exact output. These are
finite symbolic checks; the analytic proofs are the displayed derivations,
not a proof-assistant or external audit.

No external source, web search, oracle, optimizer, paid service, or environment
installation was used. No external verification, priority review, or general
Morrey conclusion is claimed.
