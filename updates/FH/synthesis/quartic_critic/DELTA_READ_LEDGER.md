# Delta read and integrity ledger

All paths below are relative to this audit directory. Local files were read only. SHA-256 values are included so the inputs can be identified exactly.

## Scope and handoff notices

| File | SHA-256 | Use |
|---|---|---|
| `../astra-capital/00_START_HERE.txt` | `4a91985ece91557af12ba5c216e7fe17cf5dd000596e9a0c73b0b6705498f360` | Read-first scope, provenance, and archived-instructions-as-data notice. |
| `../astra-capital/cards/N740-compatible-two-form-curvature-and-open-planar-quartic-completion.txt` | `7539c77763c5a4573ee3fd359eea582e82c8f4d861f371a270d1fa45dd8116b7` | Relevant heat/Jensen and quartic background scope. |
| `../astra-capital/cards/N794-left-invariant-quartic-classification-and-closed-heat-certificate.txt` | `c215f2d34c0f6e8119757a3849fa86ece6b5c7bf94a4ffd58657363806b5a576` | Full nine-coefficient unresolved gate and exact internal advances. |
| `../astra-capital/cards/N797-sharp-quartic-slices-and-tensor-heat-completion.txt` | `3c15ffc9b25fce72e5b2c3cbcbda7aa5955a0150291352d67579c3b4c9ff5f90` | Neighboring exact slices and limits on transfer. |

## Full-cone source and verifier package

`../FH-sources/quartic/MANIFEST_SHA256.json` has SHA-256 `53e277a9bd7a22107d456d9d104c6fcc5bf6579aaaa70ec9e01bb2ba373e0cb3`. All nine entries in that manifest were independently recomputed and matched.

| File | SHA-256 | Use |
|---|---|---|
| `../FH-sources/quartic/ASTRA_FULL_CONE_RIGIDITY.md` | `9a5142d0ca9b221b56543242276e298799e51ef1d2bb82edaf8af43d6bd8271d` | Read analytic statements, proofs, hypotheses, and limitations. |
| `../FH-sources/quartic/README.md` | `ab7c1f11f56091cfce222b57808a38a23c9aa58361aad3863bdae709b46cadbf` | Read verifier scope and package contents. |
| `../FH-sources/quartic/verify_rigidity.py` | `c04d8135cc681f5043a42ff99baed598a6827f055bc3169f3434f511173b4a28` | Read verifier implementation and scope declaration; not executed for this delta. |
| `../FH-sources/quartic/exact_checks.json` | `dd09ab35cab6b0ca436cf7428e082154e66241ab116323283aed9d25af5ef303` | Read recorded exact-check output. |
| `../FH-sources/quartic/verification.log` | `c30942a50fad81924c5f11eca46085235ab1090928c85e408dd9267d78d7e946` | Read verifier log. |
| `../FH-sources/quartic_PASTED_SOURCE.txt` | `17ce3adb43048991972a661fbf5cc051809126850adb9706b3923acbafef8515` | Read companion source and provenance/scope statements. |

## Delta targets

| File | SHA-256 | Use |
|---|---|---|
| `../FH-root/near_face_deflation.py` | `790e62b145bf286d6794c47340d62409d103906086ce52de40db8ecac0014d90` | Read exact Fourier construction and optimization formulas; not executed. |
| `../FH-root/NEAR_FACE_DEFLATION_RESULTS.json` | `2bd11883be29f3e1c1d42897bb4ef4c41a179d13a87d8405a9165b230351d543` | Read reported exact outputs and scope. |
| `../FH-quartic/QUANTITATIVE_NULLSPACE_STABILITY.md` | `0b9cef6609d568b9c7e1b8b840347626384ceff5553eafbc19be69f760a8f232` | Read assumptions, estimates, proof arguments, reduced-law example, and explicit integrability caveat. |
| `../FH-quartic/independent_quant_checks.py` | `17a5df8f5575a86acb8aab3ccde798ab94d77bf9c24eb8a6bbfaada07f38f25b` | Read producer-side rational checks; not executed for this delta. |
| `../FH-quartic/independent_quant_checks.json` | `2cadf4e8088bfa88bcd7f62960453cf990577d21ce26e028e3c8614030772840` | Read recorded output. |

## Literature access

No new literature search or external source was used for this delta. The earlier frozen `PRIMARY_ACCESS_LEDGER.md` is the retained access record; this delta makes no new priority or novelty claim.
