# W02 retrieval audit: `tools/knowledge.py`

Scope: read-only audit of retrieval, packet/read budgets, aliases, and source pointers in `outputs/ASTRA_KNOWLEDGE`. I did not modify implementation or index data. The local script is self-contained apart from optional `tiktoken`; when unavailable it reports UTF-8 byte counting. All ingested text and historical instructions were treated as data. No retrieved statement is promoted beyond its stored source status.

## Findings

### 1. Search citations are not accepted by the `read` command (confirmed functional break)

`search()` sets `citation` equal to the chunk ID at [knowledge.py:62](/Users/harjas/Documents/Codex/2026-10-07/com/outputs/ASTRA_KNOWLEDGE/tools/knowledge.py:62), and packet blocks expose that value as their `id` at line 98. But `get_doc()` resolves only document ID, path, or card ID (lines 68–75); it never maps chunk ID to its parent document. I ran `search 'adaptive predictive feature acquisition'` and then `read 'd-7a16721d57edc620:0'`; read fails with `Unknown source/card ID or virtual path`. This breaks the natural “open this citation” workflow for the exact citation produced by search and shown in packets. The packet trailer says to open the source by ID, and `included[].id` is the source ID, so that alternate path works, but users must notice and select a different identifier than the citation.

**Minimal fix:** accept chunk IDs in `get_doc()` by looking up `chunks.id`, then resolve its `doc_id`; preserve chunk and line metadata separately if `read` should open the cited excerpt. Alternatively, make `citation` a source ID plus line span and ensure that exact identifier works with `read`.

**Failure-specific check:** obtain a search result; call `read(result.citation)`; assert it resolves the same `source_id` and includes the cited line interval. This directly covers the broken handoff.

### 2. `read --max-bytes` is not a hard ceiling for the first line (confirmed)

At [knowledge.py:81–85](/Users/harjas/Documents/Codex/2026-10-07/com/outputs/ASTRA_KNOWLEDGE/tools/knowledge.py:81), the size guard only runs when `chosen` is already nonempty, deliberately allowing an overlong first line. A `read W-metric-acquisition --max-bytes 0` returned a 43-byte line and `over_byte_limit: true`. The field makes the exception visible, but callers cannot rely on the requested ceiling to bound response size. For API/UI use, a single pathological line can exceed the requested budget by an arbitrary amount.

**Minimal fix:** either make `max_bytes` a strict limit and return no line when the first line cannot fit (with an explicit `next_line`/oversize indicator), or rename/document the parameter as a soft limit and add a separate maximum line size/truncation mechanism. Avoid silent truncation if exact evidence text is required.

**Failure-specific check:** request a zero-byte limit and a limit smaller than the first encoded line; assert returned text does not exceed the declared strict bound, or that an explicit soft-limit response includes a bounded preview and continuation information.

### 3. Invalid start line produces an impossible line range (confirmed)

`read()` clamps `start` only below at 1, then clamps `end` to the source length, but does not clamp `start` to the source length at [knowledge.py:78–85](/Users/harjas/Documents/Codex/2026-10-07/com/outputs/ASTRA_KNOWLEDGE/tools/knowledge.py:78). `read W-metric-acquisition --start 999` returned empty text with `start_line: 999`, `end_line: 998`, `total_lines: 29`. That range is internally inconsistent and is awkward for continuation clients and citation logic.

**Minimal fix:** validate positive `start` and define out-of-range behavior explicitly (prefer a clear error or a normalized empty response with `start_line=end_line=null`); calculate `end_line` only when at least one line was returned.

**Failure-specific check:** request a start beyond EOF and assert no reported end precedes the start and the response follows the chosen error/empty convention.

### 4. Alias routing eligibility counts stopwords/punctuation tokens (likely recall defect)

Alias matching tokenizes the raw query at [knowledge.py:42–47](/Users/harjas/Documents/Codex/2026-10-07/com/outputs/ASTRA_KNOWLEDGE/tools/knowledge.py:42), while the threshold denominator includes every token, including stopwords and common fillers. For example, adding “what is the” to a three-term alias query raises the required overlap from 2 to 4 and makes alias routing impossible. This can suppress the curated route on normal question phrasing even though `word_query()` separately removes many stopwords. The hard `hit < 2` minimum also means short valid aliases cannot route.

**Minimal fix:** normalize alias-query terms with the same tokenizer/stopword policy as lexical search; compare overlap against normalized query terms and safely handle an empty set. Keep the threshold conservative and inspect existing aliases before changing it.

**Failure-specific check:** take one existing alias fixture and compare its minimal phrase with a natural-language form padded only by stopwords; assert both route to the same card. This tests the observed normalization asymmetry, not the implementation in isolation.

## Budget and dependency semantics

- `packet()` counts the complete rendered packet string, including its header and optional trailer, at [knowledge.py:87–109](/Users/harjas/Documents/Codex/2026-10-07/com/outputs/ASTRA_KNOWLEDGE/tools/knowledge.py:87). A 1,500-unit packet for the representative query returned 409 units with no sources included and listed two not-fitting IDs; at 6,000 it returned 4,942 and included one record. This is honest accounting, though a too-small budget can yield a mostly empty packet rather than a targeted, truncated useful excerpt. Search has already loaded up to 16 hit documents/chunks before packet packing, so `budget` bounds emitted text, not retrieval computation or intermediate memory.
- With the observed environment's `tiktoken` unavailable, mode was `conservative_utf8_byte_upper_bound`; therefore `budget=6000` meant 6,000 UTF-8 bytes of packet text, not 6,000 model tokens. With `tiktoken`, it counts `o200k_base` tokens of emitted text. Neither mode includes the surrounding model prompt/system overhead. This is acceptable if clearly understood; callers must not compare these numbers across modes as the same unit.
- `read` uses UTF-8 byte counts regardless of whether `tiktoken` is installed, unlike packet counting. The separate `max_bytes` name is clear, but users can mistakenly expect one common budget unit across commands.
- `tiktoken` is optional and import failure is swallowed, so offline operation survives. This is useful portability; dependency variation changes the packet budget unit and is exposed via `budget_meter`.
- `packet` deduplicates hits at source level and marks full cards as complete only when the whole card fits. Large-card fallback is explicitly partial. No token-count accounting bug was observed for emitted packet text in representative calls.

## Evidence paths and information load

- Search result `web_page` points to `web/pages/<source_id>.html` at line 62. The referenced page existed for the representative result (`d-7a16721d57edc620.html`), and the collection has the expected HTML page directory. This path mapping is sound for the tested item.
- Packet source blocks carry source ID, virtual path, role, cycle and completeness label (line 98); this supports provenance. The packet's `id` is the chunk citation, however, so the broken citation-to-read handoff above remains the primary provenance usability bug.
- A non-card hit can contribute both an 850-character source opening and the matched chunk (lines 95–99); fallback can contribute a 700-character opening plus the matched chunk (line 102). Those repeated passages spend packet budget without increasing evidence coverage. This is modest but systematic information overhead, especially for a query whose match is already at the beginning of the source.
- Curated aliases prepend routed cards before lexical FTS hits (lines 56–58). This provides useful recall but can crowd out direct matches under the `limit`; the current validation explicitly scopes fixtures rather than claiming perfect recall. Any ranking change should compare direct lexical matches and alias routes on current fixtures, not infer general retrieval quality.

## Minimal implementation sequence

1. Repair citation resolution and establish one usable citation convention across search, packet, and read.
2. Make `read` range and byte-limit contracts internally consistent; keep exact-source text and explicitly label any oversize/partial behavior.
3. Normalize aliases consistently with lexical query terms; rerun existing fixtures plus the stopword-padded regression.
4. Consider removing duplicated source-opening text only after checking representative packets where opening context changes interpretation. Preserve matched excerpt, source path, role, cycle and completeness labels.
5. Document that packet budget counts serialized packet content only and that its unit depends on the reported meter; document read's byte unit separately.

These are retrieval-interface findings only. Search/index hits, alias matches, source metadata, and finite fixtures do not establish proof correctness, novelty, or external validation.

## Implementation and measured checks (2026-10-08)

Implemented the fixes in [knowledge.py](/Users/harjas/Documents/Codex/2026-10-07/com/outputs/ASTRA_KNOWLEDGE/tools/knowledge.py) and added the focused read-only regression runner [w02_checks.py](/Users/harjas/Documents/Codex/2026-10-07/com/work/astra_system_audit/w02_checks.py). `get_doc()` now resolves chunk citations through the chunk's `doc_id`; `read()` defaults a citation to its stored line span, enforces the UTF-8 byte cap including `[L…]` labels, returns an empty bounded response when the first line does not fit, and raises clear errors for invalid starts or reversed ranges. Alias eligibility now uses the same stopword-normalized terms as lexical FTS. The new `route` CLI/API returns up to five card metadata records with stored status, topics, and local/web pointers, without excerpts. `packet --max-bytes` and the API equivalent enforce an exact UTF-8 ceiling over the serialized packet; the response reports byte count, excluded IDs, and whether the trailer was omitted by that ceiling. Existing token/byte meter reporting remains explicit.

Measured checks: `py_compile` passed for both files; `python3 work/astra_system_audit/w02_checks.py` passed all six targeted checks, including CLI invocation for citation read, route, and packet. The representative citation `d-7a16721d57edc620:0` opened source `d-7a16721d57edc620` at lines 1–33. A zero-byte read emitted 0 bytes and a continuation pointer to line 1. The bounded packet used 4,942 UTF-8 bytes (and 4,942 units under the active `conservative_utf8_byte_upper_bound` meter) with a 5,000-byte cap, included one source, and reported the second source as excluded by the cap. The padded query `what is the passive noisy parity lpn predictive acquisition` routed to `N13-passive-parity-boundary`; the route result contained metadata and pointers only. Checks read the existing SQLite database and index files; they did not mutate them.
