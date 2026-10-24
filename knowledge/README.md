# Scientific knowledge, current public route

Describe the problem rather than guessing a card ID:

```
python3 knowledge/retrieve.py search "Compare quantum measurements by relative entropy with an untouched auxiliary quantum system"
python3 knowledge/retrieve.py search "persistent intermediates from successive dilute reactant arrivals"
python3 knowledge/retrieve.py packet N675
python3 knowledge/retrieve.py source N675 --evidence 0 --start 2 --end 80
python3 knowledge/retrieve.py bridge <source-unit-ID> <destination-unit-ID>
python3 knowledge/retrieve.py coverage
```

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
correction. Raw scientific sources and old authorities remain unchanged.

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
intake is byte-idempotent. Only cited ranges of registered material are searched;
unregistered raw archives and withheld sources are not silently published.
