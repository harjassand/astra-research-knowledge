# Scientific knowledge, current public route

Describe the problem rather than guessing a card ID:

```
python3 knowledge/retrieve.py search "your scientific task" --method content
python3 knowledge/retrieve.py search "a single experiment distinguishing action choices" --method agent
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
For the optional local agent runtime, once per environment,
install the free optional CPU runtime with `python3.13 -m venv .astra-local/agent`
then `.astra-local/agent/bin/pip install -r knowledge/requirements-agent.txt`;
run the commands with `.astra-local/agent/bin/python`. Python 3.12/3.13 are the
supported dependency targets. The pinned Apache-2.0 relevance model and tokenizer
ship in `knowledge/runtime/`; inference makes no network requests. Missing or
changed model/runtime bytes fail explicitly. Build/intake and the portable
`structured`, `field`, `lexical` and web routes need only the standard library.

Agent search interleaves independent field and matched-content BM25 candidates, expands reusable units of promising
families before grouping, then ranks operation/statement and exact source views
with a local cross-encoder. It retains an independent full-card lexical safety
slot. Ranking text has a 512-token model limit, reported per hit; source and
packet reads retain their actual byte budgets and are never silently truncated.
Scores are relevance logits, not probabilities of truth or applicability.
`--object` and `--operation` add scientific object/capability descriptions.
Repeat `--available` and `--unavailable` to surface verbatim requirements,
conditions, units and costs needing inspection. This is conservative literal
premise triage, including negated mentions; it neither discharges a requirement
nor decides logical compatibility. Assumption declarations do not positively
boost ranking. `next.packet` and `next.source` are executable argument arrays
for the stable facade. Read the packet before using a premise. A winning source
view routes to its actual S-id, never an arbitrary first citation. Operation
views require selecting the packet's actual evidence scope/index; one citation
may support only part of a statement. Each hit also shows up to three separately
ranked units from its family and the family packet route, so grouping cannot
silently hide all intermediate constructions. This menu confers no compatibility.
`--method content` exposes the independent matched-content BM25 baseline over
the same complete record/source content without field weights or expansions.

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
