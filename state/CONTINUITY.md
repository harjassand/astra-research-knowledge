# Shared research continuity

Fetch `state/branches.tsv`, then only the relevant `state/branches/<branch>.txt`. Open its checkpoint JSON for the exact contract, source hashes, failures and next decisive step. `UNPUBLISHED` means no shared checkpoint was recorded; older histories do not establish current branch activity. The registry starts honestly empty. A published checkpoint is an agent handoff, not a scientific status authority. Read the relevant current claim notice before reusing its mathematics.

Built-in IDs: `theoretical-pro`, `natural-sciences-pro`, `ultra`, `primitive-genesis`. Additional independent instances use `worker-<unique-slug>` and describe their purpose. Branch identity does not dictate a common trajectory. Permanent proofs, originals and historical research records remain unchanged. Working notes stay in the agent's workspace; completed shared handoffs are new immutable files under `state/checkpoints/<branch>/<checkpoint_id>.json`.

Use `agent/templates/BRANCH_CHECKPOINT.json` as the shared extension of the existing SESSION/BRIDGE workflow. Populate observed facts only; null means unknown/unstudied, and an empty list does not certify an exhaustive search. Record the current objective, strongest obstacle, scoped failures, new mechanisms, exact references, substantive result and next decisive step. Keep work progress (`read`, `reconstructed`, `reviewed`) separate from each result's scientific status. Publishing never promotes a claim. A result summary or failed attempt needs linked evidence.

An evidence reference has `id`, repository-relative `path`, full `sha256`, optional one-based inclusive `lines`, optional full `source_revision`, and a scoped `status` such as `source-reported internally derived; external correctness UNKNOWN`. A failed attempt has `attempt`, narrow `failure_scope`, and `evidence_ref_ids`. A cross-branch update has `checkpoint_path` and a note describing its relevance; observing it does not make its conclusion applicable.

## Publication and concurrent work

Web-only agents can read the static registry/views and prepare a complete checkpoint with explicit expected parent IDs and the retrieved full revision. Publication requires an actual GitHub update by a write-capable connector, GitHub edit/PR, or an explicit handoff to a local coding agent. The repository does not synchronize independent conversations automatically. A web-only draft without checked hashes stays a draft. Refresh remote main and the branch view before publishing; preserve a stale draft as a separate file and reconcile its scope explicitly.

Local agents use a dedicated Git branch from current main, include every referenced new artifact, and run:

```text
python3 state/publish_checkpoint.py publish /path/to/completed-record.json --base-revision <checked-out-HEAD> --expected-parent <current-checkpoint-ID>
```

For the first checkpoint use `--expected-parent NONE`. `base_revision` inside the record must equal the full checked-out HEAD. `parent_checkpoint_ids` must equal the expected current head set. Use a unique lowercase slug for `checkpoint_id` (for example `2026-10-10-session-<unique-suffix>`). The publisher validates references, hashes and line ranges, rejects stale HEAD or parent sets, exclusively creates the record and regenerates compact views. Publication locking uses the Unix Python standard library and a transient lock in `.git`; static retrieval needs no process or Python.

Commit the new checkpoint/artifacts and generated views together; open a PR. Recheck against remote main before integration. The local HEAD check cannot by itself prove remote main has stayed unchanged. Never force-push shared state or replace an old checkpoint. If independently published commits create multiple heads, regeneration retains them as `CONFLICT`, with no timestamp winner. Read their scopes and publish an explicit reconciliation whose `parent_checkpoint_ids` lists all heads; repeat `--expected-parent` for each. A merged handoff does not upgrade either scientific claim.

Before a new publication on a clean, privately owned implementation branch, run `git fetch origin main`, `git rebase origin/main`, then `git rev-parse HEAD`; retrieve the regenerated branch heads and fill a fresh draft against that revision. Keep unfinished drafts outside the immutable checkpoint tree. If a checkpoint was already published, retain its bytes through the rebase and append a new handoff or reconciliation; do not rewrite its recorded base to appear current. Shared branches use a normal merge instead of history rewriting. After concurrent integration, regenerate views and inspect every conflicting head before publishing a reconciliation.

```text
python3 state/publish_checkpoint.py rebuild
python3 state/publish_checkpoint.py validate
python3 state/publish_checkpoint.py validate --immutable-base <full-PR-base-commit>
python3 state/publish_checkpoint.py self-test
```

`rebuild` is deterministic from checkpoint bytes. `validate` checks all checkpoint evidence, ancestry and generated views; if an original referenced artifact changes, retain the old bytes and publish a new record rather than repairing an old checkpoint. Default validation rejects uncommitted edits/deletions of tracked checkpoints; `--immutable-base` also detects committed alterations of records present at a named PR baseline. Without that baseline, validation cannot establish historical append-only compliance from current HEAD alone. The small software fixtures test stale publication, hashes, append-only preservation, fork retention, interrupted writes and reproducibility; they do not evaluate discovery. Publication exposes a complete flushed record atomically without replacing an old path. A crash before that point may leave an ignored temporary file; after it, rebuild the views from the retained complete record. Inspect changes since a saved revision using GitHub Compare (`compare/<saved>...<current>`) or `git diff --name-only <saved> <current> -- state/checkpoints frontier/cards`; open relevant changed records only.

## Primitive Genesis

The branch supports both obstruction-driven work and independent conceptual invention. Optional obstruction routes are existing `frontier/OPEN_PROOF_GATES.jsonl`, scoped blocker records, reviewed result connections and `mechanisms/TRANSFER_MAP.txt`; use targeted routes when available. No candidate must start from an existing card, gate or disciplinary taxonomy.

Copy `agent/templates/PRIMITIVE_CANDIDATE.json` into a new versioned research artifact. It extends `mechanisms/REPRESENTATION_CONTRACT.json` with a definition, operations, consistency obligations, substantive consequences, theorem candidates, counterexamples and prior-art status. Preserve conventional notation and local symbol meanings. Publish its path/hash in a branch checkpoint. Keep consequences and exact unresolved obligations central: naming an object is not establishing a foundational discovery. The repository validates publication integrity, not mathematical consistency or originality.
