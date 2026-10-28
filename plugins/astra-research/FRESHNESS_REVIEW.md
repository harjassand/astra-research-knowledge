# Published-corpus maintenance review

This is a bounded maintenance change to the existing search/fetch server.
Scientific records, source bytes, result identities, acceptance decisions and
ranking models are unchanged.

## Failure and resulting behavior

The installed backend remained at8d51d607/inputa1681a9f after published intake
had reachedca9174c0/inputd611210e. Actual installed search missed N1127/N1129;
older search and source transport worked. After the existing connection was
restored, installed N1129 search, its complete two-page capsule and complete
source fetch matchedca9174c0/d611210e. PR253 then advanced main to718dc9fb and
input341f1159 while that server still served the preceding snapshot. Successful
GitHub publication or Pages therefore did not imply connector freshness.

Published mode now checks the public Git main ref on requests and reads a
small generated marker at that immutable revision. A mutable raw-main cache
cannot establish freshness. Changed input identities stage a separate sparse
snapshot. The ordinary library verifies all input/output hashes and discovery
membership before the reader changes. A network, missing-support, invalid-view,
busy-cache or runtime-code failure returns a blocker; the old snapshot is not
presented as newly current. Check time, identity and age remain explicit.

Every served version keeps a Git ref and registry entry. Clean owned cache
copies can be removed and reconstructed; edited files are never forcibly
removed. A shared cache lock serializes native/remote mutations. Historical
handles retain their version and identify current correction contexts before
reuse. Reader code must match the reviewed runtime, and bootstrap snapshots
must belong to published main history. This is a data refresh, not a scheduler,
research-worker pool, private database or scientific-code execution path.

Subsequent PR review found a real continuation failure: two published commits
can share the same input identity, while revision-pinned URLs change their
payload bytes. Re-registering the later revision overwrote the retained binding.
The corrected code permanently retains the first served revision/ref, recovers
a registry entry from that ref if necessary, and makes another server bootstrap
at the canonical retained snapshot. A real Git regression publishes an identical
tree at a later commit, re-registers it, evicts the cache and starts another
server. All old page bytes and payload hashes remain identical; freshness still
names the later observed public revision separately. This is a completed review
finding and correction, not a claim that the original head passed it.

## Identifier and scope presentation

Canonical identifiers and unambiguous numeric prefixes are routed before
relevance candidates. Case variants and identifiers inside questions work;
multiple IDs stay separate and ambiguous unit-family prefixes are not guessed.
No query-specific alias or scientific-status change is introduced.

New search results use a distinct `current` handle kind. Contracts, all current
notices/reviews, source-reported gaps and transfer qualifications remain.
Duplicate references retain their original annotations and actual source-fetch
routes. Source-reported status/validation and historical versions move to a
linked `history` handle. Complete artifact selectors remain on source fetches.
The legacy `record` and `source` codecs stay unchanged, so their previously
issued continuation offsets do not acquire differently formatted bytes.

For the actual N557 data, the legacy capsule is83323 bytes; the current-scope
view fits two24000-byte pages rather than four. This reduces repeated citation
locators and separates status history; it does not shorten scientific
conditions or silently confer acceptance. Lossless expansion tests recover
the exact notices, reviews, gaps and transfers. The linked history recovers
the original assessment. Actual previously installed N1129 record/source
payloads were also reproduced byte for byte with the new legacy reader.

## Evidence and limits

Review also retained direct-current-ID fetch compatibility and closed a cached-snapshot runtime-check bypass. The runtime guard covers the server itself as well as readers; historical reads remain possible at their original scope. Both behaviors have regression tests.

The synthetic ordinary-intake test changes a card, introduces a new source
version, revises an immutable unit, accepts a new subresult and adds a current
correction through the existing build path. The reader advances without a
restart, reaches the changed source, preserves old page chains and scopes,
refuses missing support/network failure, and recovers after support returns.
Sparse Git staging and historical rematerialization are exercised with real
Git repositories. A committed but unpublished revision is rejected. The
release probe test verifies immutable-revision fetching and its size bound.

A real SDK stdio test performs that intake transition over the unchanged two
tools, including current acceptance, correction and actual source passage.
The initial test harness omitted its dynamically loaded module from
`sys.modules`, which prevented Pydantic from resolving output schemas. The
harness was fixed and the output-schema assertion retained; this was not a
production-server or scientific result failure. Identifier routing and
current-view reconstruction were additionally checked against the actual
published corpus data. These are controlled engineering diagnostics, not a
held-out scientific-discovery or autonomous-agent benchmark.

Full actual-base CI, reviewed deployment, actual installed latest-merge
search/fetch, and another ordinary scientific intake remain separate release
checks. A local SDK result alone does not close those obligations. Source
claims retain their original scope, and the earlier P08 neural omission stays
reported; this maintenance does not establish general search superiority.
