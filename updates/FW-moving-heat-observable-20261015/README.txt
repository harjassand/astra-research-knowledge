FW moving-heat-observable integration preparation

This packet preserves all supplied source bytes and supplies guarded machinery
for a later root integration. It contains no curated scientific cards, notices,
bridges, gates or technology records. The curation templates deliberately leave
those fields empty. Root must finish the scientific contracts and exact proof,
review and replay selection before the generator can produce a live plan.

The source intake remains pinned to 33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d.
package/SOURCE_MANIFEST.json is its original, byte-identical manifest. The source
wrapper SOURCE_MANIFEST.json pins 58 originals (11,379,563 bytes), including seven
ZIPs, and all 319 safe ZIP members (16,884,400 bytes). Original files live under
package/originals/sources/. Recomputed archive members live separately under
package/extractions/<archive-stem>/. The complete source inventory contains 377
files and 28,263,963 bytes. No supplied file, producer manifest, whitespace, binary
array, image, script or result has been rewritten. Source scripts were not run by
this tooling. The original ZIPs are retained in addition to the extracted members.

One embedded producer digest in the avalanche archive disagrees with its actual
member. The ZIP member and the supplied extraction agree exactly. The discrepancy
is recorded in SOURCE_IDENTITY_COORDINATION.v0001.json; neither the embedded
manifest nor the result was repaired. Four unmanifested Python bytecode caches
appeared in the shared research source directory during concurrent scientific
work. Preservation inventories them as excluded runtime artifacts and does not
copy, remove or treat them as supplied originals. Other unexpected source files
remain a fail-closed condition.

Root subsequently reconciled its privately owned checkout to main
8a1e001ac128468ae8d151c9a859b89ef3b9a664, where PR98 occupies N866. The original
intake pin and preservation draft v0001 remain intact. PREPARATION_STATE.v0002.json
selects the new preservation draft v0002, empty curation template v0002 and freeze
template v0002 against the reconciled base. The draft is outside canonical state;
its previous draft is cited as evidence, not invented canonical checkpoint
parentage. Tentative route labels N867-N871 remain unreserved and require one
fresh collision check before root application. The names src-FW-MHO-*, FW_MHO_*,
SN-FW-MHO-* and G-FW-MHO-* separate this intake from PR98's FW-storage namespace.

Use Python 3.10+ with -B from the repository root. The tools use only the standard
library. Preservation and validation commands are read-only unless an explicit
copy/apply flag is supplied. Copy operations create exact packet bytes only and
refuse collisions. Generator application is the sole live curation operation;
it requires root-final input, explicit root attribution, the exact input hash,
root's application flag, exact HEAD/base agreement and a fresh origin/main check.
This preparation did not invoke generator application, projections, canonical
checkpoint publication, commits, pushes or PR actions.

Read-only checks for the current prepared packet:

  python3 -B updates/FW-moving-heat-observable-20261015/validate_intake.py --repo . --check-remote --check-global
  python3 -B updates/FW-moving-heat-observable-20261015/preserve_sources.py --repo .
  python3 -B updates/FW-moving-heat-observable-20261015/test_tooling.py
  python3 -B updates/FW-moving-heat-observable-20261015/test_boundaries.py

The global checkpoint command is expected to fail with the unchanged inherited
unsupported-schema condition. The FW validator reproduces each of the three
historical failures separately and validates only the new draft's shape and exact
references. A valid draft is not canonical publication. No historical ancestry or
schema is guessed or rewritten to bypass this condition.

For root's later review, fill a NEW versioned research freeze in R and hash-pin it.
Each selected entry needs an exact research-relative path, package/derived/
destination, SHA-256, bytes, provenance_role, payload_kind, selection_reason and
the explicit external-fulltext/full-network declarations in SELECTED_FILE.template.
Only exact selected final files are copied. Earlier selection versions and their
payloads remain intact; new names are required when bytes differ. Acquired full
texts, third-party repository clones, virtual environments and caches remain
outside selected research. Preserve literature URLs, versions, hashes, licenses
and acquisition receipts. User-supplied originals and ZIP member bytes have the
separate complete source inventory described above.

Root-only sequence after claims and review are final:

  1. Refresh/reconcile main and recheck every numeric route and owned namespace.
     Preserve stale draft versions; append a fresh preparation draft if needed.
  2. Run preserve_selected.py with --repo, --selection and a NEW --freeze-name.
     Review its read-only plan. Then --copy additionally requires the exact
     --expect-selection-sha256. This copies packet evidence, not live authority.
  3. Validate --phase preserved --freeze-path <exact-repository-freeze-path>
     --base-revision <actual-current-base>. The selection base must match.
  4. Finish a versioned root curation input. Set schema astra.fw-curation-input.v1,
     curated_by root and curation_status root_final; select exact cards/routes,
     source metadata, inclusive evidence ranges, paired bridges and open gates.
     Keep checkpoint_path null. Point checkpoint_draft_path to the reconciled
     individual draft outside canonical state and selected_freeze to its exact
     repository path and SHA-256. Sources need only include artifacts actually
     used by the final claims; complete source-byte preservation is separate.
     Preserve the reviewed exact input bytes at this packet's CURATION_INPUT.json
     before running integrated validation; the generator reads --input but does
     not invent or normalize a replacement for the approved input bytes.
  5. Run build_integration.py --repo . --input <root-final-input> --dry-run.
     An empty template or an unpreserved derived source fails closed. A DRAFT_
     input may use --draft-plan for a read-only plan after evidence preservation;
     no draft plan can apply. Review all exact output paths and before/after hashes.
  6. Only root may invoke --apply --root-authorized-apply with
     --expect-input-sha256 <reviewed-root-final-input-hash>. The generator never
     performs scientific inference, canonical checkpoint publication, a commit,
     a push or a PR. It keeps every old scientific artifact unchanged, appends
     registry records and fixes new claim status to source_derived_unreviewed.
     External correctness, priority, physical capability, formal verification and
     empirical confirmation remain UNKNOWN; owned gates remain open.
  7. Root then refreshes generated views with frontier/build_access.py build/check
     against the same actual base. This produces the frontier gate sidecars used
     by integrated validation. Run validate_intake.py --phase integrated with
     the base and read-only freshness/global checks. Review Git changes before
     any separately authorized commit or PR. The canonical checkpoint blocker
     stays separately reported, and the individually valid draft stays outside
     state/checkpoints.

The disposable fixture suites check hostile archive paths/types/CRC, byte and
range identity, exact freezes, immutable collisions, concurrent modifications,
ID collisions, root-final guards, stale HEAD/remote refusal, historical registry
preservation, paired bridge evidence and fixed scientific-status boundaries.
Synthetic fixture application occurs only in temporary directories; Git is
mocked there. Actual baseline checks are separately run against the real pinned
checkout. These are software/integrity checks, not mathematical review, external
verification, originality clearance or physical capability evidence.
