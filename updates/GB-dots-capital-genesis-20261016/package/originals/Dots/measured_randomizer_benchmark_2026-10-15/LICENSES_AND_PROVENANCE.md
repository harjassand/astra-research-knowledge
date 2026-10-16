# Source attribution, licenses and retained material

## Ware RGST
Matthew Ware et al., *Experimental Pauli-frame randomization on a superconducting qubit*, Physical Review A 103, 042604 (2021), https://doi.org/10.1103/PhysRevA.103.042604 ; primary dataset https://zenodo.org/records/4609459 . Source/data repository snapshot: https://github.com/matthewware/RGST-analysis/tree/9afedca174dbcb14d52c245cf7504a834816fc39 . Retained rgst/ source and data carry Apache 2.0 in rgst/LICENCE. The original count files, notebook and selected scripts are unchanged; source is not executed by replay.

## QGL compiler
BBN-Q/QGL.jl snapshot https://github.com/BBN-Q/QGL.jl/tree/70e66d76f2e5f518ff2d8b78bc93b65779182c9f . Apache 2.0 notice retained as qgl_source/LICENSE. Source files are unchanged; diatomic_angles.csv is a disclosed literal table extraction with the source factor 0.5 applied. This snapshot is not identified as the actual acquisition revision.

## EDD
Nicholas Ezzell et al., *Dynamical decoupling for superconducting qubits: a performance survey*, https://arxiv.org/abs/2207.03670 . Source snapshot https://github.com/naezzell/edd/tree/fc72448880fa6132ffd09a9f15297306c9cd791e . Apache 2.0 notice retained as source/edd_LICENSE. Only one bounded Armonk acquisition condition and relevant source are included. Original archive URL, selected member names and complete acquired archive hash are recorded in edd_subset/extraction_manifest.json and provenance.json; the unused archive is omitted.

## pyGSTi
Pinned v0.9.3 convention and germ-length source is retained as text in source/pygsti_v093_*.txt. It carries the upstream Sandia copyright/GPLv3-or-later notice in source/pygsti_v093_license.txt; the full GPL text is source/GPL-3.0-or-later.txt. These unchanged source snapshots are separate reading material, not linked into or executed by the own-code replay. Preserve their notices and applicable license when redistributing. The older version is deliberately used to verify the author's pinned interface, not recommended as a current software installation.

## Added artifacts
validate_counts.py, independent_audit.py and replay.py are newly authored standard-library parsing/arithmetic/replay code. Reports, CSVs, selection declarations and audits are original evaluation artifacts or expressly identified derivations. They do not imply endorsement by the data authors. Upstream files remain unchanged; no full source-paper PDF/HTML/text is redistributed. Paper-reported implementation details are summarized with citations, not copied as a paper attachment.

provenance.json records original URLs, commit/tag pins, byte sizes, SHA256 and extraction status for 61 source/acquisition artifacts. INDEPENDENT_AUDIT.md records verification. MANIFEST_SHA256.json covers the complete portable payload; its hashes are integrity records, not external signatures or independent authentication of experimental provenance.
