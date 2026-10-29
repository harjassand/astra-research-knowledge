# Scientific knowledge, current public route

Describe the problem rather than guessing a card ID:

```
python3 knowledge/retrieve.py search "your scientific task" --method content
python3 knowledge/retrieve.py search "a single experiment distinguishing action choices" --method agent
python3 knowledge/retrieve.py search "a reduction from hidden moments to a decision bound" --method semantic
python3 knowledge/retrieve.py search "certify a proposed intervention" --method agent --object "nonlinear conductance matrix" --unavailable "calibration" --available "scalar reaction intervals"
python3 knowledge/retrieve.py evidence "hidden actuator above an untested dose" --method agent
python3 knowledge/retrieve.py search "Compare quantum measurements by relative entropy with an untouched auxiliary quantum system"
python3 knowledge/retrieve.py search "persistent intermediates from successive dilute reactant arrivals"
python3 knowledge/retrieve.py packet N675
python3 knowledge/retrieve.py card N557
python3 knowledge/retrieve.py source N675 --evidence 0 --start 2 --end 80
python3 knowledge/retrieve.py bridge <source-unit-ID> <destination-unit-ID>
python3 knowledge/retrieve.py coverage
```

Start with fast portable `--method content`; cross-check `structured` when the
problem is poorly named or source/field weighting may matter. `--method agent`
adds semantic relevance, within-family navigation and explicit premise triage.
It is a complement: fresh evaluation retained cases where either lexical or
structured search beat the model, and a case every method missed. See
[the source-use comparison](evaluations/2026-10-27-agent-retrieval/README.md).
Agent ranking also compares separate bounded views of each candidate's actual
requirements, returned capability, conditions, costs, units and obstruction, and
one query-selected current notice. These excerpts rank relevance only; complete
fields stay in the packet and supplied/unavailable facts never become positive
ranking terms or discharged assumptions. Notice matches expose `next.notice_source`:
`source <record-ID> --notice <notice-ID> --evidence <index>` reads that notice's
actual citation, independently of the record's evidence array. The ordinary
source range/hash checks, complete corrections and byte budget still apply.

The [qualification-view comparison](evaluations/2026-10-28-qualification-views/README.md)
retains eight source-informed scientific-use problems, the exposed version-review
regression, lexical comparators, extra navigation steps and measured CPU costs.
This changes the optional neural lane; portable CLI/web/MCP retrieval remains
available without that runtime or a private database.

For the optional local agent runtime, once per environment,
install the free optional CPU runtime with `python3.13 -m venv .astra-local/agent`
then `.astra-local/agent/bin/pip install -r knowledge/requirements-agent.txt`;
run the commands with `.astra-local/agent/bin/python`. Python 3.12/3.13 are the
supported dependency targets. The pinned Apache-2.0 cross-encoder and MIT BGE contextual encoder/tokenizers
ship in `knowledge/runtime/`; inference makes no network requests. Missing or
changed model/runtime bytes fail explicitly. Fully built portable `structured`,
`content`, `field`, `lexical` and web reading need only the standard library.
Ordinary intake uses that same local CPU runtime only for missing/changed
semantic text vectors; unchanged-vector build/check remains stdlib. No service,
private database or researcher form is added.

Agent search fuses four independent family ranks: contextual operation/condition
vectors, the existing source-aware cross-encoder, structured BM25 and matched
full-content BM25. It retains each method's leading family without combining
cosines and logits. `--method semantic` exposes the contextual lane alone;
`--method content` is the independent full-content lexical baseline. The
contextual encoder uses two deterministic current views per canonical record,
CLS pooling and unit normalization, with a512-token limit per view. Costs,
units, complete conditions, notices and governing passages remain in packets.
The public model artifact uses float16 weight storage restored to the original
float32 graph; provenance, license and exact offline reproduction are in
`runtime/contextual/` and `store_contextual_weights.py`. The evaluated int8
alternative lost a chronological-memory case and was not selected.

`--object` and `--operation` describe the scientific object and capability.
Repeat the existing `--available` and `--unavailable` flags to inspect literal
and semantically related verbatim conditions, costs and units. These facts are
inspection inputs, never positive ranking terms; no cosine threshold discharges
a premise, establishes a conflict or validates a supplied fact. Negations,
quantifiers and unit compatibility still require the complete source. Only
explicit source-supported version-bound bridges establish composition.

`next.packet` and `next.source` are executable argument arrays. A winning
source-passage view routes to its actual S-id, never an arbitrary first
citation. For operation/semantic views choose the packet's actual evidence
scope/index; one citation may support only part of a statement. Family packets
retain all units and up to three separately ranked alternatives are shown in
agent results. Family membership itself confers no compatibility or acceptance.
The MCP server defaults to the agent fusion and explicitly falls back to
portable routes if local inference is unavailable; `--method portable` remains
available. The static web search continues to use public BM25 projections.

Older canonical summaries sometimes contain only a historical status. Operation
views also expose verbatim scientific card excerpts and labelled claim/interface/
assumption/cost passages with exact card lines. Unlabelled text has no inferred
role. `card ID --start N --end M` reads the actual checked card bytes with current
notices/reviews; it does not substitute a card for its proof. Original canonical
records/status labels remain unchanged, and excerpts confer no new acceptance.

`evidence` is a separate discovery lane over all nested current-record citations
(including current/historical reviews, corrections and relationship support),
version-bound transfer evidence,
and explicit entries of recognized selected-public-source indexes. E-id reads
return the exact matching range plus citation context/current notices. They can
expose code, data, reviews or an uncited original without manufacturing a lemma
or acceptance. `current/evidence/artifacts.jsonl` gives source hashes, ranges,
citing records and citation roles, declaring index and exclusion reasons; `documents.jsonl` and
sharded postings are public deterministic projections. External/binary containers,
scoped derived extractions and operational artifacts are not silently expanded.
Raw sources remain separate. Metadata-only artifacts have original public paths.
Other source-index formats and unregistered/withheld archives remain unassessed;
this is not a claim that every existing research artifact has been reviewed.

The same precomputed field-BM25 postings power [static web search](index.html).
It loads a small catalog and only query-term posting shards, not the archive.
No private SQLite database, embedding service, model call or paid dependency is
required. The stable facade is `knowledge/retrieve.py`; v1–v5 remain historical
snapshots, not current intake endpoints. Pin the Git commit actually fetched.
Each browser search refreshes the manifest and keeps its catalog, shards and
verified packet in one dataset version. Projection requests bypass HTTP caches
and include their expected hash. If publication overtakes an old result, search
again rather than using a mixed packet. Raw `current/` URLs can advance; use a
commit-pinned raw GitHub base for historical evidence. Optional Node.js fixtures
exercise browser cache/update races when running the knowledge test suite.
A web-only reader can fetch `knowledge/current/packets/N675.json` directly from
the pinned raw GitHub base. Without executable search or a known ID, use
`knowledge/current/browse/index.txt` and one topic TSV (for example
`browse/chemistry.tsv`, `browse/biology.tsv` or `browse/learning.tsv`), then a
packet. These are compact generated statement previews, not a new reporting
form, complete field taxonomy or a proof. Follow its exact source path, hash and inclusive
lines. HTML source exports may have several preformatted blocks: the source
block is the one matching the recorded text hash, not the first block.

## What retrieval does and does not establish

One normalized schema (`astra.knowledge.v1`) represents results, reusable units,
existing lemma entries and technology records. Requirements, operated-on object,
returned capability, assumptions, costs, units and removed obstruction live in a
contract. Source windows expose mechanisms buried below a title without
inventing a theorem from a paragraph. Windows are explicitly not complete proofs.
Packets keep actual review scope, corrections, prerequisite alerts and source
routes; large packets fail their explicit byte budget instead of truncating a
correction. When a review cites sources already listed in that packet, its
`evidence_ref_indices` point to the exact zero-based entries in the packet's
`evidence` array; the full review and its evidence remain at the review's
`authority` path. Raw scientific sources and old authorities remain unchanged.

Search combines full statements, contracts, card content, exact cited source
windows and curator-owned scientific concept expansions. Expansions are shown,
not silently substituted for the original question. When not already present,
the strongest independent full-card lexical candidate occupies the last slot;
this explicit safety lane protects against field-weighting regressions. Its
score has a separate scale. `--method field` retains the unguarded diagnostic.
`--method lexical` is a
standard full-card BM25 baseline with the same tokenizer and no concept
expansion. Neither method is a theorem prover or general semantic interpreter.
An irrelevant hit is not an answer, and no hit is not a proof of impossibility.
Field coverage and the unknown denominator of eligible mechanisms are explicit
in `current/coverage.json`.

Composition requires an explicit version-bound source-supported bridge. The
reader keeps documented compatibility, conjectured analogy, incompatible
assumptions and refuted transfers separate. Matching words/types alone produce
`NO SUPPORTED CONNECTION`, never a verified composition. Read both source
contracts, their remaining obligations and current notices.

A substantive completed internal agent audit is sufficient for Astra scientific
acceptance at its actual version and scope. Current review overlays record this
as `accepted_internally_verified`; they do not rewrite historical source text or
turn a partial audit into acceptance of the whole card. Genuine proof gaps stay
open. Mathematical acceptance does not acquire a measurement, working device,
novelty or practical advantage. Those evidence dimensions remain separate.

## Maintain it

[INTAKE.md](INTAKE.md) is the exact Capital integration contract. Researchers
continue producing ordinary scientific artifacts; no new reporting form is
required. The compiler owns normalized records and all current projections.
Edit existing authoritative source/status/card formats, not generated files.

```
python3 knowledge/build.py build
python3 knowledge/build.py check
python3 -m unittest discover -s knowledge -p 'test_*.py'
```

Build validates all required support before writing anything. Missing bytes,
wrong hashes, absent quote anchors, wrong-card current-unit mappings and
conflicting identities fail explicitly. A prior-version audit remains visible
as historical and cannot confer acceptance on a revised result. Search refuses stale
inputs, new unprocessed shards or changed output bytes. Repeating unchanged
intake is byte-idempotent. Operation views and the evidence lane are generated by
that same command; Capital supplies no extra scientist form. A declared selected
original with missing bytes/hash/length fails ingestion even if metadata-only.
Unregistered raw archives and withheld sources are not silently published.
## Navigate through a shared scientific operation

After search, `python3 knowledge/retrieve.py peers <returned-ID>` follows
version-bound providers of a documented consumer input. The named quantity,
units, qualification and actual source remain explicit. This can reveal a
useful premise in another representation without asserting a transfer between
the providers. Use `--offset` and `--limit` for the complete candidate list;
`bridge` retains its separate supported/unsupported conclusion. The initial
curated slice is described in
[`2026-10-28-task-bound-interfaces`](../research/2026-10-28-task-bound-interfaces/README.md).

Explicit current acceptance appears before historical review labels in current
consumer views and search previews. A curator projection is bound to the existing
authority and exact accepted scientific versions; it is not a new audit. Source
contracts and historical assessments remain available, while the generated
current consumer retains actual scientific assumptions, costs and scope. See
[the intake contract](INTAKE.md#current-consumer-authority). New interface links
prefer compact current capsules; older version handles preserve their bytes.
