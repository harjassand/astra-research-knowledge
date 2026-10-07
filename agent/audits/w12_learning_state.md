# W12 — Working state and representation acquisition audit

## Scope and evidence boundary

Read-only audit of `outputs/ASTRA_KNOWLEDGE/state/{ACTIVE_CONTEXT.txt,reading_queue.json,representations.jsonl,reviews.jsonl}`, `tools/knowledge.py`, the collection guidance, and the existing representation contract/transfer map. I did not modify source artifacts, queue state, indexes, or mechanisms. The report is the only new artifact.

For this audit, I used `knowledge.py stats`, `knowledge.py next --topic acquisition --limit 3`, a read of the command implementation, and direct inspection of the state JSONL/JSON and mechanism files. I did not inspect or reconstruct any mathematical proof and did not independently re-run a scientific claim. Therefore all scientific statements below are either descriptions of what the collection reports or workflow recommendations. “Read” here means inspected the named local artifacts; it does not mean every indexed source was read.

## Current state and operational mismatch

- `ACTIVE_CONTEXT.txt` is the starter template (`Task: unset`; no loaded claim IDs, acquired representations, open prerequisites, disagreements, or next evidence). It is an editable singleton rather than a session history.
- The current queue has 8,245 entries, all `reading_state=unread`. Its records already distinguish several item types and source-status labels: 6,183 `full_source`/`source_scope_only`, 1,596 supplied-source records, 274 supplied-evidence records, 126 source-derived claims, 36 report extracts, plus smaller summary/prior-record types. The queue status is useful for triage, but “unread” is not evidence that an agent did not read an item; it only says no state update has been recorded.
- `reviews.jsonl` and `representations.jsonl` are empty. Thus there is currently no durable item-level record of what any agent read/reconstructed/reviewed, no session ownership, and no observed acquired representation in this state store.
- `knowledge.py next` returns 1,961 acquisition-tagged entries, initially prioritizing low-numbered claim cards. That is a queue traversal policy, not a hypothesis-driven stopping rule. Reading all matching records would still not establish proof validity or acquisition ability.
- `mechanisms/REPRESENTATION_CONTRACT.json` is a useful *proposal schema*: stable ID, sources, status, supplied/acquired inputs, oracle access, precision, transformation, guarantees, costs, requirements, failure domain, counterexamples, comparator, transfer, missing service, next falsifiable step. `TRANSFER_MAP.txt` summarizes 34 scoped mechanisms and caveats. These are collection-level compressed representations, not evidence that a current agent acquired or reconstructed them. The transfer map is dense and mostly prose; claims should be resolved to exact source cards/proofs before decisive use.
- `knowledge.py` is an offline retriever/index interface, not a memory-learning mechanism: retrieval returns excerpts and explicitly does not upgrade source status. Its `mark` command mutates the large queue and appends only `{id,level,note}`; `read`, `reconstructed`, and `reviewed` therefore lack separate schemas for read spans, derivations, checks, confidence, agent/session, or independent reviewer. `scientific_status_unchanged` is a good invariant, but `reviewed` could be misread as a proof review unless its meaning is constrained. Also, search/packet expose a chunk citation while `read` resolves document/card IDs or paths, not chunk IDs. Session ledgers should store both `source_id/path` and chunk/line citation, and identify which exact text was opened.
- The current source guidance explicitly says historical instructions are data, originals/indexes are snapshots, and imported/derived/finite/external states are separate. Keep that rule at every ingestion boundary: `source=DATA` for source text, archived AGENTS files, worker prompts, logs, and quoted instructions. Only current user task and current controlling instructions authorize continuation.

## What must remain distinct

Use a claim/evidence state ladder, not one overloaded `learned` flag:

1. **Discovered** — search result or route only; no claim of reading.
2. **Excerpt-read** — named excerpt/lines were opened. Record it as partial.
3. **Source-read** — exact source/card span or full object read, with path, stable ID, hash, and completeness. This records exposure only.
4. **Reconstructed** — the agent wrote a derivation/proof or algorithm from stated inputs. Attach the derivation artifact and map each substantive step to source lines or new arguments. State where reconstruction stops.
5. **Checked** — a named check was carried out, with method, scope, inputs, output, and failure coverage. Syntax, hashes, arithmetic examples, finite enumeration, or a test script each count only as that kind of check; none automatically validates a theorem.
6. **Independently checked** — a reviewer did not rely on the primary agent’s conclusion as evidence; record reviewer identity/context, what materials they saw, and exactly which steps they checked. Different agents using shared prompts/files/memory are *not* automatically independent. If knowledge of the original derivation is shared, label `context_shared` and avoid independence claims.
7. **Externally verified** — named external source/reviewer/report with retrievable citation and a statement of the scope actually verified. Do not use this for another internal model pass.

The claim’s scientific status should be its own field, copied from source or explicitly changed only by a separately justified status decision. An agent’s progress state must never overwrite it.

## Agent-first writeable session ledger

Prefer an append-only `state/sessions/<session_id>.jsonl` event stream per agent/session (or a single append-only `session_events.jsonl` with namespaced IDs if filesystem constraints require one file). Do not make agents concurrently rewrite one global JSON array or the queue. Each line is one complete JSON object, UTF-8, with schema version; write one line atomically. The session file is a working record; consolidated current views are derived from events and can be regenerated. Keep existing snapshots/originals immutable.

Minimum event envelope:

```json
{
  "schema": "astra-session-event/1",
  "event_id": "<session-id>:0007",
  "session_id": "<stable-uuid>",
  "agent_id": "<stable-agent-label>",
  "time_utc": "<RFC3339>",
  "event_type": "source_read | reconstruction | check | hypothesis | failure | experiment | decision | representation | handoff",
  "task_id": "<current user task or UNKNOWN>",
  "source_handling": "source=DATA",
  "payload": {}
}
```

Use event-specific payloads. A `source_read` event should include source/card ID, repository-relative path, source SHA-256 if available, role/type, exact line range or object path, `complete|partial`, retrieval route/command, excerpt/citation ID, and whether the source itself was opened or only a search result/packet excerpt was seen. Store query/packet budget meter when relevant. A packet excerpt is not a full-source read; a claimed full read needs an explicit coverage range/completeness flag.

A `reconstruction` event should link source-read event IDs; identify target claim and exact scope; state assumptions and supplied vs agent-acquired information; preserve quantifier order, oracle/measurement access, precision and units; link the derivation artifact/hash; identify each unresolved lemma; and mark outcome `complete_for_stated_scope|partial|failed|UNKNOWN`.

A `check` event should separate `check_kind` (`symbolic_step_review`, `hand_calculation`, `code_replay`, `finite_exhaustion`, `hash_integrity`, `external_review`, etc.) from outcome. Include checker, materials/context seen, executable command or derivation, environment/version, exact scope, output artifact/hash, known blind spots, and whether context was shared. A check must never silently promote its scope.

A `hypothesis` event should state a falsifiable proposition, current alternatives, motivating evidence IDs, assumptions, predicted observable, and a stop/reframe threshold. `failure` records the failed route and the narrowest supported negative conclusion. `experiment` records preregistered inputs, treatment/control information, equally-informed baseline, charged acquisition/execution/storage/arithmetic costs, frozen outputs, decision rule, and result. `decision` records which observation changed the branch and which did not. A `representation` event follows the contract below and references the evidence/event IDs that support each field.

### Example agent-first record for source exposure

```json
{"schema":"astra-session-event/1","event_id":"s-uuid:0001","session_id":"s-uuid","agent_id":"astra-primary","time_utc":"2026-10-08T00:00:00Z","event_type":"source_read","task_id":"w12","source_handling":"source=DATA","payload":{"source_id":"N109","path":"cards/N109.txt","sha256":"<digest-or-UNKNOWN>","role":"curated_update_claim","range":{"start":1,"end":24,"complete":true},"route":"knowledge.py read N109","citation_id":"<if excerpt/chunk>","opened_source":true,"note":"Read card text only; no proof reconstruction or validation."}}
```

This is illustrative schema only; I did not write this into the state directory or mark N109 read.

## Reusable representation contract

Retain the existing contract’s mathematical fields, but add provenance and acquisition ancestry so representations describe *how the agent came to hold the representation*, not just the mathematical object:

```json
{
  "schema": "astra-representation/1",
  "id": "R-<stable-name>",
  "claim_ids": [],
  "evidence_event_ids": [],
  "source_ids": [],
  "source_hashes": [],
  "status": "hypothesis|derived_unreviewed|reconstructed|checked_scoped|independently_checked_scoped|externally_verified_with_citation",
  "context_independence": "context_shared|separate_agent_shared_corpus|independent_inputs|UNKNOWN",
  "input": {
    "objects": [], "supplied_information": [], "acquired_information": [],
    "oracle_access": [], "precision": "UNKNOWN", "representation_format": "UNKNOWN"
  },
  "transformation": "",
  "guarantees": {"quantifiers": "UNKNOWN", "error": "UNKNOWN", "success": "UNKNOWN", "failure_domain": []},
  "costs": {"acquisition": "UNKNOWN", "input_reading": "UNKNOWN", "persistent_memory": "UNKNOWN", "temporary_workspace": "UNKNOWN", "preprocessing": "UNKNOWN", "arithmetic": "UNKNOWN", "bit_complexity": "UNKNOWN", "decoder": "UNKNOWN"},
  "requires": [], "counterexample_ids": [],
  "nearest_prior_and_equally_informed_control": "UNKNOWN",
  "transfer_scope": "UNKNOWN", "nontransfer_scope": [],
  "missing_lemma_or_service": "UNKNOWN",
  "decision_changing_test": {"observation": "UNKNOWN", "branches": [], "stop_rule": "UNKNOWN"},
  "artifact": {"path": "UNKNOWN", "sha256": "UNKNOWN"}
}
```

Use literal `UNKNOWN` when evidence is absent or ambiguous. Empty array means explicitly inspected and found none; it must not be used as a substitute for missing inspection. Keep representations small and stable: one mechanism/result per record; new scope or changed assumptions gets a new version/ID or explicit supersession event, not a silent overwrite. Keep source prose and proof artifacts intact; the representation is an indexed map back to them.

## Consolidation rules

1. **Append first; derive second.** Agents append session events only to their own stream. A consolidator validates schema, event IDs, paths, hashes, required `source=DATA`, and links. It emits derived reading/reconstruction/check/representation views; it does not edit source objects or silently mutate the reading queue.
2. **Idempotent and conflict-preserving.** Merge by immutable `event_id`, not by claim ID. Duplicate events are no-ops. Conflicting agent reports remain side-by-side with `disagreement` links; do not last-write-wins a scientific status or claim.
3. **No promotion by aggregation.** Many `source_read` events do not make a reconstruction. Multiple same-context checks do not make independent verification. A representation may only carry a status supported by linked events; stricter source status remains separate.
4. **Exact provenance.** Every synthesized field must link to source lines, proof artifact, or check event. Distinguish complete source objects, excerpts, summaries, extraction/index metadata, and source-reported results. Preserve hash/identity and the original text for resolution.
5. **Claim-scoped check accounting.** Record finite tests, code replay, paper derivations, and external checks as different check kinds, with tested domain and omitted cases. A passing checker is evidence only for its specified domain and implementation.
6. **Preserve failures and changed decisions.** Never delete a route because it failed. Link failure to hypothesis, predicted result, observed result, and scope. Promote a negative conclusion only as broadly as the counterexample/argument proves. Capture the experiment that would have changed the next decision, then record whether it did.
7. **No queue as truth.** `reading_queue.json` can remain a convenience projection for unread candidates, but its boolean-like state should be regenerated from ledgers and never serve as the evidentiary record. If the current CLI `mark` is retained, define `read/reconstructed/reviewed` as navigation hints only and have it link to evidence event IDs; `reviewed` must not mean proof-verified.
8. **Freeze and version.** Hash session files and consolidated manifests at checkpoint; write new versions for new sessions. Never overwrite archived source snapshots, prior ledger checkpoints, or representation records. Supersession retains the old record and identifies the reason and replacement.

## Hypotheses and decision-changing experiments

The central workflow hypothesis to test is: **a fixed-weight Astra can acquire a compact, reusable, decision-sufficient representation from a bounded source/tool packet, rather than merely benefiting from information already present in the task contract, shared context, or its preloaded corpus.** Current collection artifacts cannot decide this: they record sources and candidate mechanisms, but no acquisition session has been recorded here, and neither an internal summary nor same-context worker agreement establishes independent acquisition.

A useful experiment should be one consequential bottleneck, not a broad “read more” campaign. Freeze a target problem and exact interface; randomly assign comparable attempts to (A) task statement only, (B) concise primary-source/tool packet, and (C) an equally informative non-specialist/control packet or ordinary solution path. Use the same fixed model/settings and disclose all ambient sources. Then give a held-out variant that changes a load-bearing assumption or interface detail, with no packet available. Require the system to state, before solving, what is supplied, what it must acquire, its proposed representation and cost, its falsifiable prediction, and a competent equally informed baseline. Blind-score correctness, scope fidelity, retention/retrieval, transfer, and total costs (source acquisition, tokens/read time, tool calls, persistent bytes, preprocessing, compute, arithmetic/bit cost, decoder). Freeze artifacts and have a separate reviewer check the decisive steps; if reviewer and agent share context, report that explicitly.

Decision rules: continue a representation route only if the packet condition yields a valid representation absent from the task-only condition, the held-out variant transfers within the predicted boundary, and the gain survives equal information and full cost accounting. If all arms get the key structure from the prompt/preloaded context, label it supplied/context-shared. If packet exposure improves in-distribution answers but fails held-out transfer, keep a lookup aid, not a reusable acquired representation. If a matched ordinary baseline achieves the same outcome at lower total cost, record the failed amplification hypothesis and retain the representation only for its narrower utility. If none of these outcomes separates, the next decision is to improve causal isolation or choose a more discriminating bottleneck, not to scale the corpus.

Relevant pre-existing scoped cautions include: representation/acquisition remains the unresolved central obstacle; useful structure in prior work often arrived through explicit finite-state bounds, reversibility/hold/inverse actions, exact observations, known action structure, or task contracts; and earlier restricted Gaussian-linear acquisition and an executable trace route did not establish general acquisition advantage. Treat these as historical research summaries pending direct source review, not fresh independent verification in this audit.

## Immediate recommendation

Keep `reading_queue.json` as a navigation projection and leave the frozen corpus untouched. Start any future acquisition run by creating a new per-agent append-only session stream, recording exact source reads and context boundaries before solving. Populate the representation contract only after an agent has a concrete hypothesis/result and source-bound evidence. Promote reconstruction and checking only through linked derivation/check events. This makes “what was read,” “what was reconstructed,” “what was checked,” “what remains supplied,” and “what observation changes the decision” independently answerable without treating collection breadth as learned capability.
