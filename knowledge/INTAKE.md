# Capital integration contract

The same build/check now generates lossless operation views and evidence
navigation from existing record citations and recognized selected-public-source
indexes (`astra.intake-source-index.v1`, `selected_frozen_source_index`, or
`astra.scientific-source-selection.v1`). The last format uses its explicit
`repository_path` relative to the index directory; `original_path` is provenance
and is never followed. Both `INDEX.json` and `SOURCE_INDEX.json` declarations
are discovered. Keep
using those existing formats; no producer form or neural inference is required
for intake. Their explicit public entries must retain exact SHA256/byte length;
missing declared originals fail ingestion. Private `origin` paths are never
followed. Index admission gives evidence discoverability, not scientific
acceptance. Scoped extractions retain their cited-range boundary. See
`knowledge/current/coverage.json` for the exact admitted denominator/exclusions.

Current/historical review, correction and transfer citations enter that same
evidence view with their actual roles; indexing never inherits acceptance.
`coverage.json` lists each admitted index, exact original count and existing
source-version record contexts. Uncited originals remain a semantic-curation
gap; a file count is not result completeness. Original/read-path aliases at the
same path and byte hash share correction context without widening statement
support or conferring acceptance.
Read actual completed internal reviews and their reviewed-artifact versions;
external/formal next-gate boilerplate is not a prerequisite to scoped internal
acceptance. Keep genuine gaps and conflicting later source assessments visible.

1. Start from current merged main in your own intake checkout. Preserve original
   source bytes and stable result identities. Keep raw originals separate from
   derived text. Use existing claim/status/catalog/alias/notice shards; do not ask
   scientific producers for another form. Register new or revised support in the
   existing scoped frontier status sidecar and aggregate/shard together.
2. Read the decisive source passage and any substantive completed internal audit.
   Preserve quantifiers, supplied/acquired access, units, error and cost model.
   Record actual conditional internal acceptance at the reviewed source version
   and scope using a small curator-owned `knowledge/reviews/*.json` overlay;
   hashing, intake checks or a source's assertion of an audit are not themselves
   that audit. Do not require specialist/external review. Keep physical evidence,
   practical advantage, novelty, genuine gaps and unresolved imports separate.
3. A changed card, source, accepted subresult, correction or supersession uses the
   same path: `python3 knowledge/build.py build`, then
   `python3 knowledge/build.py check`. This normalizes all registered cards,
   existing atlas entries, reusable units, latest technology versions and cited
   source windows into one current corpus and regenerates packets, search
   postings, coverage and manifest. No per-run manual tags are required.
4. Reusable extractions are selective curator work, not a producer requirement.
   Add a stable ID under `knowledge/units/<ID>/v0001.json`, with exact supporting
   quote/range and a requirements/provides/assumptions/costs/units/obstruction
   contract. Changed meaning gets the next immutable version linked by the
   previous file hash. Existing `literature/LEMMA_ATLAS.jsonl` plus its sidecar is
   also an accepted input format; no duplicated scientific statement is needed.
   Read the actual passage, not just the title or stored hash. Bridges require
   exact endpoint content versions, cited argument, scope and remaining
   obligations; no bridge is inferred from topical proximity.
5. Run `python3 state/check_current.py --base-revision <actual-PR-base-SHA>` and relevant
   knowledge tests. Inspect the changed packet, follow its source route and read
   the affected passage. Repeat build/check once to demonstrate idempotence.
   Review and merge the focused PR under existing authorization. Return verified
   public links through the normal dispatcher route.

An ingestion error is a stop for that intake, not permission to share the old
generated views as current. Required support must be present and correct before
publication. Conflicting assertions remain separate, scoped notices; neither
chronology nor indexing resolves the science. Source revisions, historic cards,
old manifests and previous versions remain available. Producer research does
not wait for a programme-wide idle gate.
## Optional named consumer inputs

A curated reusable unit may declare `contract.input_slots`, each with an `id`,
description and `required_binding_fields` (including `units` and
`qualification`). A version-bound `ESTABLISHED COMPATIBLE INTERFACE` transfer
may add `slot_binding`: the declared slot plus its explicit field values.
The transfer still needs its actual supporting proof passage and remaining
obligations. Other transfer states cannot silently become typed providers.

The ordinary build generates `interface_navigation` in canonical records:
bindings once on the consumer and routes on the exact provider and its parent.
Missing fields, unknown/ambiguous slots and stale endpoint versions fail
ingestion. Common-consumer peers are navigation candidates; no transfer between
providers or inherited acceptance is generated. All qualifications, costs,
corrections and field-specific acquisition obligations remain. These optional
annotations are intake-agent work for selected useful interfaces, not a new
researcher form or a requirement to classify every source.

Large packets may omit optional navigation excerpts whose complete locators
already occur in `evidence`. Exact duplicate legacy gap citations can use the
existing `evidence_ref_indices` convention; `evidence_ref_annotations` retains
any original per-source metadata. The actual gap scope and every correction,
condition and review remain. Conflicting references are kept separately.

For an explicitly identified public path-portability derivative, use the existing
source-index entry with its actual public path/hash/bytes and `kind` set to
`public_path_portability_derivative`; `original_path` is a repository-relative
original identity and `original_sha256` its full hash. Originals stay privately
frozen. Those provenance locations are never opened. Current support must bind
the actual public derivative. An older immutable unit/review may show an explicit
public-copy route only when this exact original identity is declared and its old
quoted scientific range still validates there. Both source identities remain
visible; this neither asserts old full-byte availability nor confers acceptance.
Missing current support, undeclared historical support, wrong hashes, changed
quotations and ambiguous copy mappings fail ingestion. Rebind actual new units
and current scoped reviews through the normal build/check path.

Before any public push, commit the reviewed candidate locally and run
`python3 state/check_current.py --base-revision <actual-PR-base-SHA> --preflight-only`.
This checks unchanged historical evidence and newly added literal local-source
locators before a draft can expose them. It does not run the full suite or
accept science. The existing full current-base gate and actual source-use
verification remain required before merge; producer research continues.
