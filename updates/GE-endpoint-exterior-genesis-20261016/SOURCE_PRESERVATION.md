# External-only preservation stage

Created: 2026-10-16. This stage preserves the two original endpoint/exterior ZIP packets, all 75 exact expanded member payloads, the source manifest, and a selected local convergence-campaign record. It is a byte-preservation package only; hashes, copied files, and inventory agreement do not establish a mathematical or physical claim.

## Package paths

- `package/originals/` contains both original ZIP files and the byte-identical `SOURCE_MANIFEST.json`.
- `package/originals/expanded/pair/` contains all members from `Astra_pair_certified_endpoint_sampler_2026-10-16.zip`, retaining each member's exact internal path.
- `package/originals/expanded/interchange_path_exterior/` contains all members from `interchange_path_exterior_packet.zip`, retaining each member's exact internal path.
- `package/prior_convergence/` contains selected C artifacts at their exact C-relative paths. It includes all 103 non-source campaign files, the source audit and receipts, and the seven cited first-party Astra Capital snapshot files.
- `package/prior_convergence/MANIFEST.json` is the exact C manifest; it lists all 147 source entries, including both included and excluded C source files.

The package includes 112 of the 147 C manifest entries and excludes 35. Excluded material consists of third-party paper/reference bodies, extracted or rendered paper text, figure PDFs, upstream paper source bundles, and API XML containing third-party bibliographic/abstract text. Their paths, byte counts, and SHA-256 values remain listed in `SOURCE_PRESERVATION_MAP.json`; the paper contents themselves are not republished here. The supplied campaign date is 2026-10-16. C has no supplied commit revision; its separate capital dependency pin is recorded in the map.

`PRESERVATION_RECEIPT.json` contains the per-file SHA-256 and byte counts, the ZIP CRC/member checks, and the deterministic aggregate payload hash. No files in W or the frozen source inputs were modified.
