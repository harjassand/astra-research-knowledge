# Capital intake and provenance | local draft

This local draft prepares a route for selected evidence from a fresh research programme. It is deliberately not linked from public navigation or published as a programme announcement. It remains separate from the dated scientific cycles already archived in this repository. Reusing an older result requires an explicit source link and a scoped reason; similar topics alone do not connect claims.

## Initial source pin and readiness

- Repository: [`harjassand/astra-research-knowledge`](https://github.com/harjassand/astra-research-knowledge)
- Default branch at initial retrieval: `main`
- Retrieved revision: `e606bfc587c76bdcae8b8fa3ec33e721efa2fbac`
- Retrieval date: 23 October 2026 (Australia/Brisbane)
- Read first: [`00_START_HERE.txt`](../../00_START_HERE.txt), followed by [`AGENTS.md`](../../AGENTS.md), [`UPDATE_PROTOCOL.txt`](../../UPDATE_PROTOCOL.txt), and the publication/continuity routes below.
- Intake state: `READY_FOR_FIRST_CLEARED_PACKET`. At setup, this Capital intake had received no programme-cleared evidence packet. No new scientific result is integrated here. This records only this intake's receipt state; it does not report whether work exists in other research workspaces.
- Directly retrievable now: this procedure in the local working branch. It has no public repository destination yet.
- Not established by setup: scientific correctness, independent review, novelty, empirical validation, practical advantage, or programme success. Each remains `UNKNOWN` unless the corresponding evidence is supplied and checked at its stated scope.
- Exact next intake: the first producer with a cleared item supplies one packet using the template below; the coordinator identifies the governing source and the disclosure state for each selected artifact. If no item is cleared, report `none yet`. No public PR is opened for this setup-only note.

## Minimum packet to submit

Send one selected packet with the fields below. An absent field must be marked `UNKNOWN`, `NOT_SUPPLIED`, or `NOT_APPLICABLE` with a short reason; do not fill it from inference.

```text
packet_id:
producer / branch:
source thread or workspace reference:
source revision and retrieval date:
source artifact paths:
archive identity and member manifest, if applicable:
SHA-256 for every selected source artifact:
disclosure state for each artifact: already_public | explicitly_approved_for_publication | private
approval reference and exact covered artifacts, if approval is required:
result type: theorem | conditional result | computation | simulation | acquired measurement | failure | handoff
exact statement or failure, assumptions, quantifiers, units, and validity scope:
producer's interpretation and status:
proof / code / data / primary-source routes:
reproduction command, environment, and saved receipt, if applicable:
supplied information versus newly acquired information:
known time / compute / memory / precision / sample / energy / equipment / acquisition costs:
failed approaches, counterexamples, corrections, and omitted evidence:
producer's unresolved obligations and next decisive test:
coordinator assessment (separate from producer statement):
independent review (reviewer, method, exact scope, evidence; or UNKNOWN):
```

## Intake and integration steps

1. **Establish disclosure item by item.** Mark material `already_public` only with its public source and exact version. For previously private material, require explicit human authorization covering the particular files or claims to be disclosed. A useful result, a coordinator's approval, or permission to message a researcher is not disclosure approval. Keep unapproved material in the source owner's private workspace; do not copy its names, contents, conclusions, hashes, or transport references into public files.
2. **Bind the source before summarising.** Record the producer, source revision, paths, retrieval method and date. Compute SHA-256 for selected files and every archive member. Preserve the exact supplied bytes and original layout when they are cleared for publication. Keep Capital notes, corrected transcriptions, redactions, and generated files separate, with their own hashes and an explicit relation to the original. If material cannot be included, record the public URL/version and exact omission reason only after its disclosure is permitted.
3. **Keep evidence and voices distinct.** Quote or summarise the producer's claim at its original scope. Record Capital deductions separately and label them as integration assessments. Preserve independent reviews under the reviewer's own name/role, method, and limited scope. Coordination is not scientific authorship. Keep proof status, external correctness, novelty/priority, measurement, advantage and mission relevance as separate axes; missing evidence stays `UNKNOWN`.
4. **Make the claim retrievable.** Start with this repository's current dossier and scoped correction routes as directed by [`00_START_HERE.txt`](../../00_START_HERE.txt). Read the decisive proof and prerequisites before claiming applicability. Link each consequential claim to its exact proof, implementation, data, source version, costs, counterexamples, and remaining obligation. Do not use a topic match, graph edge, repository check, or finite fixture as a proof premise.
5. **Publish only selected, cleared material.** After a packet has explicit disclosure clearance, put a new immutable intake under `research/2026-10-23-fresh-programme/intake/<packet_id>/`, with a concise `README.md`, a source manifest, and only the necessary cleared originals or exact public source links. Do not rewrite older files or overwrite a prior version. Keep exploratory work and private candidates outside the public repository. Use [`state/PUBLICATION.md`](../../state/PUBLICATION.md) for a selected result, correction, decisive negative or useful handoff; use [`UPDATE_PROTOCOL.txt`](../../UPDATE_PROTOCOL.txt) only when changing canonical claim authority or generated access routes.
6. **Check and report the destination.** Verify source hashes, relative links and the staged diff. If the intake changes canonical records or generated access, run the repository's prescribed check against the actual PR base; otherwise use the PR's documentation checks. For cleared material, open a focused PR, inspect all applicable checks and material review comments, then merge only after checks pass and conflicts are resolved. Record the PR and actual remote merge commit. A local file, hash match, or check pass proves neither publication nor scientific correctness.

## Checkpoint format

At each substantive integration checkpoint, update the packet's `README.md` with:

- **Changed:** files and exact source versions added or corrected.
- **Retrievable:** direct paths to original sources, proofs, code, data and reviews that were actually present and checked.
- **Unresolved:** scope limits, missing evidence, remaining costs, and the next decisive action.
- **Destination:** PR URL, check result, and verified merge commit; before merge, state `NOT_YET_MERGED`.
- **Continuation:** warm continuation, fresh instance, independent fork, compact handoff or bounded help, with the concrete reason.

Continue through all cleared packets available at the checkpoint. Do not treat the first packet, a readiness note, an internal check, or the PR itself as completion of the research objective.

## Later authorization and integration | 23 October 2026

The preceding receipt-state section records the position before a later direct human instruction. On 23 October, Harjas instructed Capital to integrate the fresh programme’s selected results into GitHub after noting that Ultra had finished and the two Pro results should have been integrated. This later authorization is scoped to the selected Ultra, P1, P3, and Dots scientific evidence in `intake/capital-integrated-2026-10-23/`; the earlier `PRIVATE_NOT_CLEARED_FOR_PUBLICATION` labels remain accurate historical receipt states. Whole delivery archives, account-level usage receipts, coordination-only notes, and unrelated private context are omitted.

The selected handoff keeps claim scopes, resource boundaries, failures, review depth, and unresolved gates separate. A later Dots status about conflicting ferrite data was relayed to Capital but could not be directly inspected in this review, so the thermochemical arithmetic remains conditional and no physical exclusion is claimed. This intake does not update canonical claim authority or imply scientific validation.
