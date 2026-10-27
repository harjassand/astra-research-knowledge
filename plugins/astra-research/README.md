# Astra Research agent plugin

Read-only `search(query)` and `fetch(id)` over the existing public corpus.
The backend reuses canonical records, lexical/structured retrieval, evidence
navigation, operation capsules, reviews and corrections. It neither runs
scientific programs nor writes intake, branches or research state.

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

`fetch(id)` accepts a returned handle or a known current result/unit ID. Record
capsules contain the actual statement, conditions/costs, full current notices,
version-bound reviews, evidence routes, reusable units, recorded transfers and
historical unit routes. Source handles read their actual declared bytes/range;
binary artifacts return an original route without an invented proof passage.
Hash-matched HTML extractions retain their extracted-text coordinates without
misleading HTML-file line anchors. Historical documents retain their historical
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
snapshot change or uncommitted corpus edit fails explicitly. Serve an immutable
committed backend checkout, then restart after ordinary intake has run the
existing `knowledge/build.py build`, `check`, review and commit path. A stale
handle fails instead of silently resolving to a changed result. Older published
snapshots remain available through their pinned Git versions.

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
