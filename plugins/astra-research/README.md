# Astra Research agent plugin

Read-only `search(query)` and `fetch(id)` over the existing public corpus.
The backend reuses canonical records, lexical/structured retrieval, evidence
navigation, operation capsules, reviews and corrections. It neither runs
scientific programs nor writes intake, branches or research state.

The portable command now enables published-corpus refresh on requests. See
[keeping the installed corpus current](PUBLISHED_CORPUS.md) for the exact
ordinary-intake contract, bounded cache, failure behavior and deployment check.

## Local backend

Use a committed checkout of this public repository, Python 3.12/3.13 and the
small MCP SDK dependency. The portable default requires no neural runtime,
private SQLite database, model API key or paid vector store.

```sh
python3 -m venv .venv-astra-mcp
.venv-astra-mcp/bin/python -m pip install -r plugins/astra-research/requirements.txt
.venv-astra-mcp/bin/python plugins/astra-research/server.py --root "$PWD"
```

The portable `plugin.json`/`mcp.json` package uses `uv` to run that pinned SDK.
When the plugin is installed separately from the full repository, set
`ASTRA_RESEARCH_ROOT` in the server's environment to the backend checkout.
The package does not silently clone or execute remote repository code. The
same server can be configured directly as a stdio MCP server using its Python
executable and `server.py --root /absolute/backend/path` arguments.

For an HTTP transport test:

```sh
.venv-astra-mcp/bin/python plugins/astra-research/server.py --root "$PWD" \
  --transport streamable-http --host 127.0.0.1 --port 8000
```

The endpoint is `/mcp`. This loopback address is **not a ChatGPT web endpoint**.
Web deployment still requires an existing approved reachable HTTPS host or
Secure MCP Tunnel plus account connection. No public MCP endpoint, directory
listing, native Pro installation or web connection is claimed by this package.
GitHub Pages continues to serve the static search, packets and original sources.
Do not replace a tested local route with a fabricated public URL.

## Retrieval and evidence contract

`search(query)` returns at most five record candidates and three deduplicated
source-version candidates. It merges ranks from existing structured and
full-content lexical lanes and searches admitted evidence, without treating
the scores as a scientific verdict. `--method agent` optionally enables the
existing local neural ranking backend; a missing runtime is explicitly
reported in search metadata and falls back to portable retrieval.

`fetch(id)` accepts a returned handle or a known current result/unit ID. Search
returns compact current-scope handles with linked source-reported history.
Duplicate citations use source-fetch references while retaining their original
annotations; conditions, corrections, review scopes and genuine gaps remain.
Legacy record/source handles keep their existing payload codecs. Record
capsules contain the actual statement, conditions/costs, full current notices,
version-bound reviews, evidence routes, reusable units, recorded transfers and
historical unit routes. Source handles read their actual declared bytes/range;
binary artifacts return an original route without an invented proof passage.
Hash-matched HTML extractions retain their extracted-text coordinates without
misleading HTML-file line anchors. Citation routes match bytes, not merely an
existing filename; locators distinguish the public artifact hash from a
contained text hash. Historical documents retain their historical
status alongside current context; current acceptance is not copied onto them.

Each fetch returns `id`, `title`, `text`, nonempty citation `url`, and metadata.
The SDK emits the same object as structured content and JSON text content, as
required by the [OpenAI search/fetch interface](https://developers.openai.com/api/docs/mcp).
The text is a UTF8 JSON payload capped at 24,000 bytes per page (the complete
wire response also contains MCP envelopes and a compatibility text copy).
If `metadata.next_id` is present, fetch it and concatenate text pages before
parsing. Byte ranges and the full payload SHA256 make missing/reordered pages
detectable. Every partial page explicitly says conditions/corrections remain
incomplete; no notice set is silently cut. A capsule is navigation: read its
actual governing passage before using a premise.

Handles bind the corpus input version; metadata also carries the Git revision,
record content version or source hash, and commit-pinned citation URLs. A
snapshot change or uncommitted corpus edit fails explicitly. Static mode serves
one immutable committed checkout. Published mode checks the public release and
adopts a separately validated immutable snapshot after ordinary build/check,
review and merge, without a restart for scientific intake. Old handles keep
their version; historical responses name current correction-context handles.
Older published sources also remain available through pinned Git versions.

Every search/fetch request, including continuation pages, also compares the
normalizer's current filesystem discovery inventory with the captured manifest.
New staged or untracked reviews, correction shards and other discovered intake
files therefore fail closed before the old snapshot is served. Unrelated notes
outside that inventory do not become an intake gate. Invalid or unreadable
discovery also refuses service, without returning a host-local path. Keep researcher-facing
backends on immutable committed snapshots; finish normal intake before published
mode can adopt its new release. These request-boundary guards do
not establish a public HTTPS endpoint or native Pro readiness.

## Validation and current limits

```sh
python3 -m unittest knowledge.test_mcp_adapter
.venv-astra-mcp/bin/python -m pip install -r plugins/astra-research/requirements-test.txt
.venv-astra-mcp/bin/python -m unittest discover -s plugins/astra-research/tests
```

Tests exercise real SDK stdio and streamable-HTTP discovery/calls, schemas,
current acceptance/corrections, source passage use, historical versions,
continuation and invalid IDs. The existing publication check runs the adapter
regressions, and the same CI job runs the transport checks. These checks do not
establish scientific correctness or native ChatGPT Pro behavior. Fresh problem
comparisons and retained misses are recorded separately in the evaluation.

The package follows the current [portable plugin format](https://developers.openai.com/plugins/build/plugins)
and uses the [official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).
The short skill routes scientific premise discovery; it adds no researcher
reporting form. Search coverage remains the admitted corpus, not all Astra
research, and no general superiority to other search systems is claimed.
## Qualified interface navigation

Search menus can include bounded `shared_consumer_navigation` previews and
fetch IDs. These are separately qualified providers of one explicit scientific
operation, not transfers between the providers. Fetch the named consumer for
its full bindings and each selected provider for all conditions, current
corrections and governing proof. Ordinary fetch pagination retains the entire
payload. No extra tool, account permission, service or database is introduced.
