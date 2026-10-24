# Publish a selected scientific event

Research runs independently of publication. Keep exploration, incomplete proofs,
candidate lists and routine failures in your own workspace or ignored
`.astra-local/`. Publish when there is a meaningful result, a scoped correction,
a decisive negative finding, or a useful handoff. No session log, new card,
bridge, technology record or gate is required merely to share that event.

Use a dedicated implementation branch from current main. Select only the few
evidence files needed to support the event; preserve their original bytes.
Copy [PUBLICATION_SELECTION.json](../agent/templates/PUBLICATION_SELECTION.json)
into your working space and fill its short fields. Existing branch IDs are in
[branches.tsv](branches.tsv); an independent route can use `worker-<unique-slug>`.
A branch is a publication route, not an instruction to adopt another agenda.

```sh
python3 knowledge/build.py build
python3 knowledge/build.py check
python3 state/check_current.py --base-revision <full-current-main-SHA> --fetch-sources
python3 state/publish_result.py draft /path/to/selection.json --output .astra-local/review.json
python3 state/publish_result.py publish .astra-local/review.json
```

The first command is a read-only check except for the explicitly requested fetch
of exact missing source commits. A normal clone can lack a commit retained by a
squashed PR even with full main history. In particular, the valid historical
source pin `80d2eff466f81b1b22cf69ed6465f16f928337a9` is retained by PR #23.
Ordinary validation/publication never fetches silently. If generated branch
views need recovery, run `python3 state/publish_checkpoint.py rebuild`, then check.

Drafting hashes only selected repository files, derives the current HEAD and
parents, and writes a new local review file. It does not copy evidence, publish
anything, or infer that a file was read or a proof checked. Drafts inside this
repository must stay in ignored `.astra-local/`; an external workspace is also
allowed. Draft output is exclusive: choose another filename instead of replacing
an earlier draft. After review, publishing appends one schema-v1 checkpoint and
rebuilds the existing branch views. It never commits, pushes, merges, or sends a
message. If HEAD, parents, or evidence changed, keep the old draft and make a new
one. Multiple heads require an explicit `handoff` with `reconcile_parents` and a
scoped link to every parent; ordinary publication cannot silently reconcile them.

Review and stage only the selected evidence, new checkpoint and generated branch
views. Run the same check command against the actual PR base, then commit and
open a PR through the usual GitHub writer. CI uses the PR's full base SHA and
checks the actual head tree. A local draft or local checkpoint is not shared
until its Git update is published; main changes only after merge. A web-only
researcher can prepare the short selection and hand it to a write-capable agent.
There is no implicit synchronization between independent chats.

## Evidence status and corrections

Omit `verification` to leave every axis `UNKNOWN`. A reported claim is the
selected summary, not an internally checked proof. Optional declarations are:

| Axis | Affirmative state | Required declaration beyond state |
| --- | --- | --- |
| `internal` | `checked` | method (`proof`, `computation`, `data_replay`, `software`), exact scope, evidence IDs |
| `independent` | `verified` | verifier, method, exact scope, evidence IDs |
| `experiment` | `demonstrated` | method, exact scope, matched controls, complete cost boundary, evidence IDs |
| `advantage` | `demonstrated` | method, scope, comparator, equal-information boundary, complete cost boundary, evidence IDs |

Each axis also accepts `reported` or `failed` with its exact scope; a failure
requires method and linked evidence. Give selected evidence an `id` to reference
it; otherwise IDs are `e1`, `e2`, and so on. For example:

```json
"verification": {
  "internal": {
    "state": "checked", "method": "computation",
    "scope": "Only the named finite identity; not the universal theorem",
    "evidence_ref_ids": ["e1"]
  }
}
```

The software checks declarations, hashes, paths and history. It cannot establish
proof correctness, genuine independence, novelty, a physical demonstration or
practical advantage. A replay on measured data is not itself a new experiment.
Keep source-reported receipts distinct from checks actually performed.

For a correction, add `relates_to` with the exact prior repository path,
`relation: "corrects"`, and affected `scope`. The tool pins that target's bytes.
The correction can remain unverified. A chronological link never implies
scientific supersession. When actually changing an existing canonical card's
authority, use the existing scoped claim-notice procedure in
[UPDATE_PROTOCOL.txt](../UPDATE_PROTOCOL.txt); merely reporting a new event does
not require a full card/index intake.

The template starts with `disclosure: "private"`. Private drafts cannot publish.
Use `already_public` only for previously disclosed research, or
`approved_for_publication` after explicit human approval for the selected private
material. These are human declarations, not automatic permission checks. Do not
publish private packages, local inventories or their scientific conclusions just
because their paths were supplied to an agent. Recheck the actual PR diff.

## Historical compatibility

Three exact schema-less historical checkpoints remain unchanged. Their pinned
adapter provides read-only navigation and checks all available evidence hashes;
it preserves absent ancestry as `UNKNOWN`. They are not schema-v1 handoffs.
A new compliant handoff may explicitly link a legacy receipt; that cannot repair
its absent ancestry or promote its status. `audit` reports this
limitation; new malformed records, changed legacy bytes or changed evidence fail.

```sh
python3 state/publish_checkpoint.py audit --immutable-base <full-PR-base-SHA>
```

Detailed low-level checkpoint contracts remain in [CONTINUITY.md](CONTINUITY.md).
