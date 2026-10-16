# GB overlay adaptation review

The external builder `build_gb_overlay.py` is adapted from the pinned GA v0002 builder at `work/astra-positive-memory-20261016/updates/GA-conformal-causal-genesis-20261016/build_ga_overlay.v0002.py` (source SHA-256 `88a271cc382296f1b4a325f423f26aa6aaf84f8a6d00e1e9e088d3e6f1974b2c`). The source file was left unchanged.

The intake and owned repository prefix now use `GB-dots-capital-genesis-20261016`. Reserved routes are `N889` through `N893`; card count remains config-driven from one through the five available routes, with distinct IDs required. Source, gate, bridge, and notice identifiers now use `src-GB-`, `G-GB-`, `GB_`, and `SN-GB-`. Intake-specific `astra.ga-*` schemas and user-facing GA labels were changed to GB. Existing Astra registry filenames, including `OPEN_PROOF_GATES.jsonl`, retain their exact names.

The adaptation preserves the inherited behavior: pins remain config-supplied and are checked against the repository's existing protected-baseline guard; source paths, bytes, hashes, IDs, and evidence references are checked; identifier and destination collisions fail closed; overlay targets are create-only; registry outputs are append-only deltas; and output is staged atomically outside the repository with application marked `NOT_PERFORMED`. The builder has no apply mode. No claim config was generated and the builder was not run.

Validation was limited to `--help` and `py_compile`, as requested. These checks validate the CLI surface and Python syntax only.
