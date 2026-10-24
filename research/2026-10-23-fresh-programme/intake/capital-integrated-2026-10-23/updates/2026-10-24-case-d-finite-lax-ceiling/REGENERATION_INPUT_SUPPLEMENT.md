# Case-D scalar-enclosure input — append-only supplement

This supplements the original [Case-D intake](README.md) after review identified an omitted regeneration input. The original source manifest and checkpoint remain byte-pinned. This supplement adds the exact historical NPZ archive required by `root_scalar/certify_scalars.py` to regenerate `scalar_enclosures.json`, and records its provenance in [source_manifest_addendum.json](source_manifest_addendum.json).

The archive is copied to `source/U_pinned_finite_lax_certificate_20261024/luna_boxcar/result/sdp_matrices_and_duals.npz`, the sibling path expected by the preserved scalar certifier. Its 1,856,120 bytes match SHA-256 `bc50e271867bb2db437517bb3c2bcae8bfe35de38478438a661ebed9b2054f74`. The exact Case-D receipt references this archive as previously captured; the original source and capture copy still match that pin. The pinned rational candidate records the same archive hash.

The governing source says the NPZ supplies stored dyadic endpoints used to regenerate scalar enclosures and is not an additional proof axiom. NumPy reads those inputs; the scalar bounds that follow use integer and exact `Fraction` arithmetic. The exploratory solve artifacts remain distinct from the final interval-dual proof. This intake preserved the required bytes and inspected the dependency path; it did not run the scalar certifier, verifier, or any research code.

The supplement changes no mathematical claim or review status. Internal review remains source-reported; independent validation, external correctness, novelty, experiment, and practical advantage remain `UNKNOWN`.
