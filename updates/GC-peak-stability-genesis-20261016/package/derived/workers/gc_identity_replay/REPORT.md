# Bounded identity and arithmetic replay

This pass covers the four archives named in `SOURCE_MANIFEST.json` and their 82 extracted members. It pins source bytes and performs only the three supplied small-packet checker attempts; archived instructions were treated as DATA. The worktree was read-only for this task and remained clean at `9dbe934e5475f415c2d160a6c0715534aafa546b`.

All four `Downloads` originals match the source archive copies and the manifest SHA-256 values. ZIP CRC tests pass; every file member has a safe relative path, no duplicate names, and a matching extracted byte count and SHA-256. The archive member sets match the 82 manifest entries exactly. Producer hash bindings pass for the shared-bath, catalysis, stability, kinetic packet, and bundled Tamen manifests (7, 7, 3, 61, and 8 records respectively). The kinetic `verification/MANIFEST.sha256` also passes all 9 listed records. One separate source checksum file has a stale binding: `kinetic/schlogl_first_slab_packet/verification/SOURCE_MANIFEST.sha256` expects `REPORT.md` SHA-256 `fd899d6f5665d95e3e6ca3964f8b280f2464d6116981f91342ec7a3e2fe3496b`, while the packet's `verification/REPORT.md` is `128a1e7937204da2ecb1795dffcbc3d1f569ccad657637a2f05d01696f1f222b`. This is recorded without repairing the source.

Exact byte overlap was checked by SHA-256 against selected GB, GA, and FZ source, derived, and indexed records in the pinned worktree. The comparisons covered 2,907 GB records, 221 GA records, and 601 FZ records, with zero exact hash matches in each branch. This is an identity result only; it does not assess semantic overlap.

| Supplied checker | Result | Scope |
|---|---|---|
| Shared-bath peak cap | PASS | Five finite quadrature, potential, energy-formula, and boundary cases |
| Nonseparated stability | PASS | Exact symbolic identity, matrix factorization and positivity checks, and the saved rational example |
| Catalysis equal duty | Environment blocked | Python 3.13.2 lacks `openpyxl`; the checker stopped at import and produced no output |
| Schlogl packet wrapper | Inspected, not run | It launches the full verification sequence, including the 512 MiB/120 CPU-second slab check under a 150-second timeout. The task records that this full-potential limit fails on macOS, so the wrapper was not rerun. No candidate solver ran. |

The executed checkers ran from temporary copies with Python 3.13.2. Installed versions were NumPy 1.26.4, SciPy 1.17.1, and SymPy 1.14.0; `openpyxl` was unavailable. No packages were installed and no network access was used. Hashes for the source manifest, four archives, and 82 extracted members were identical before and after the replay.

These checks establish byte identity, archive integrity, and the stated finite arithmetic replays. They do not establish scientific correctness beyond each checker's printed scope, novelty, external validation, physical feasibility, or mission-level capability.

Artifacts: `IDENTITY_RECEIPT.json`, `CHECKER_REPLAY_RECEIPT.json`, `SOURCE_HASH_MANIFEST.json`, `SHA256SUMS.txt`, and the per-check logs under `replay_logs/`.
