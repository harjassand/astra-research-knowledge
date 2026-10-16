# GC overlay renderer review

`build_gc_overlay.py` is a staging-only adaptation of the pinned GB renderer at `updates/GB-dots-capital-genesis-20261016/package/derived/root/build_gb_overlay.py`. It targets intake `GC-peak-stability-genesis-20261016`, requires root-configured cards to use one through four distinct routes in `N894`–`N897`, and validates the `src-GC-`, `G-GC-`, `SN-GC-`, and `GC_` namespaces.

The adaptation retains the source renderer's no-apply interface, out-of-repository config/output requirements, SHA-256 and byte-count checks, revision and clean-tree pins, protected-baseline check, create-only target checks, identifier/path collision checks, and append-only registry deltas. It stages only to a new external output directory and labels generated claim status `source_derived_unreviewed`; external validation fields must remain `UNKNOWN`.

Review boundary: no claim config was consumed and no staging run was performed. No source, registry, or receipt in the pinned Astra worktree was edited. The renderer checks artifact integrity and staging constraints; it makes no scientific assessment.

Validation requested for this adaptation: `--help` and Python compilation only. The pinned worktree observed for this review was `9dbe934e5475f415c2d160a6c0715534aafa546b`.
