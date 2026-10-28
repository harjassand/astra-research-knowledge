# Keeping the installed corpus current

Ordinary Capital intake still uses `python3 knowledge/build.py build` and
`check`, followed by the reviewed actual-base publication path. The build now
also generates `knowledge/current/release.json`. It covers the same input
identity as cards, units, accepted subresults, sources and corrections; no
researcher supplies another form.

Published mode is enabled in the portable MCP command. An existing dedicated
installation uses the same server with `--published-main` and, optionally,
`--cache-dir PATH`. Static developer snapshots remain available without that
flag. The initial backend must be a clean committed snapshot in published
main's history, with the Astra public repository as its origin.

On requests, the server resolves the small public main Git ref and reads the
small release marker at that immutable revision. It therefore does not treat
a cached raw-main page as proof of freshness. Checks expire after30 seconds;
responses expose the checked revision/input identity, check time and actual
age. An idle server does no polling. This introduces no scheduled automation,
new service, model, account or permission.

When the input identity changes, the server fetches main into a separate,
immutable sparse worktree. Only manifest-declared inputs/outputs and runtime
readers are materialized. The normal library verifies every declared hash and
discovery membership before the active reader changes. Original scientific
programs are never executed. Missing support, invalid outputs, failed network
checks, busy cache or unsupported runtime code produce an explicit failure;
old results are not returned as current after a failed refresh.

Materialization uses a unique owned staging worktree. Its committed manifest
and complete index must exist before Git moves it to the revision cache; the
normal full library checks still precede active-reader switching. HEAD alone
is insufficient because `worktree add --no-checkout` sets HEAD before files
exist. Interrupted owned staging is retained under `failed-staging` without
force or deletion. A later request retries at a fresh path. An empty legacy
partial cache can be quarantined automatically; unknown files or edits to a
previously served snapshot cause an explicit blocker and remain untouched.
Network/metadata Git operations retain 45-second limits; a cold checkout has
an explicit 120-second budget. Timeout and nonzero-exit errors are distinct,
without exposing private Git stderr or host paths. These are request costs,
not background jobs. Retained failed copies require deliberate inspection;
the active-reader cache bound does not silently delete failure evidence.

The cache retains at most two active readers per server plus its bootstrap
snapshot. Clean cache copies may be evicted; every served version retains a
Git ref and registry entry and can be reconstructed for an old handle. A
shared cache lock serializes native/remote cache mutations. A reader whose
copy was evicted rematerializes its exact version before use. No edited copy
is forcibly removed. Historical responses are labelled historical and name
the current correction-context handles; source bytes are never rebound to a
new version. Legacy record/source codecs remain unchanged for existing page
chains. New search results offer a compact `current` view and linked `history`.
The first served Git revision for an input identity is permanent in the shared
cache and retained ref. A later documentation-only revision with identical
inputs cannot rebind its URLs/page bytes, including after another server starts
or the historical cache is reconstructed. The separately observed public main
revision remains visible in freshness metadata. Keep this registry/cache across
server restarts. Future format changes must use distinct handle kinds/codecs;
existing `record`, `source`, `current` and `history` page chains retain their bytes.

Current views retain all contracts, notices, current reviews and source-reported
gaps. Duplicate citations become source-fetch references with their original
annotations. Complete artifact selectors remain on source fetches. Historical
status/validation labels are linked separately and do not override scoped
current internal acceptance. Canonical scientific records and original source
bytes are unchanged by this presentation.

Exact identifiers use existing canonical IDs and unambiguous numeric prefixes,
including those embedded in a question. Multiple IDs remain separate results;
an ambiguous unit-family prefix is not silently resolved. This route changes
neither aliases nor scientific acceptance.

Reader-code changes require deploying the reviewed server. The server refuses
to interpret a new release using different unreviewed reader bytes. Ordinary
scientific intake with unchanged runtime code needs no backend copy or restart.
Existing memory-only tunnel authentication remains an operational requirement
for restarting that connection; corpus refresh itself never reads credentials.

After each reviewed integration, verify actual installed search and fetch
against the public input identity, read all continuation pages and inspect
the decisive source passage. A successful CLI, local SDK test or Pages build
does not certify the installed runtime. The freshness metadata is checked
evidence of a particular request, not a scientific correctness or advantage claim.
