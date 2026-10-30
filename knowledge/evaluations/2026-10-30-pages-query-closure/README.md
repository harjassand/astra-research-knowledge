# Natural-query publication closure

The first actual bounded public view at source
`c3b706040687ff8ecb500f92a548defad63dcea3`, publication
`898355920196792d9f348a8f31eb00e3320d0138`, passed exact-identifier packet and
immutable-source tests. Its real browser natural query
`finite bandwidth covariance outside envelope sensor floor` then failed:
`Access failure: current/lexical/d4.json unavailable`.
All256lexical shards had been omitted from the projection. The exact-ID route
does not request either query lane, so those earlier passing tests did not
establish usable natural search. The failure remains part of the release record.
See [actual visible failure](ACTUAL_LIVE_BROWSER_FAILURE.json).

The publisher now copies the canonical lexical views and validates every shard
named by both catalog.shards and catalog.lexical_shards. Missing declarations or
files fail even if all remaining publication hashes match. The current scientific
records, ranking/index bytes, source statements, reviews and native reader runtime
are unchanged; this fixes their web projection. Originals and publication history
remain intact. The same existing Pages publisher/source branch is used.
The full canonical manifest is byte-identical to merged276; publisher/test files
do not force a new scientific corpus identity. [Nonregression](SCIENTIFIC_NONREGRESSION.json)
records that scope.

Thirteen real-Git/source tests include a staged natural-language browser query
that actually requests both lanes, opens the packet and inspects its pinned
source URL. The missing-shard regression removes a file and its manifest entry
without corrupting the remaining hashes, and also tests an omitted canonical
view declaration. The test corpus is generic; no scientific query alias or
ranking rule is introduced.

`verify_browser_query.cjs` executes the actual staged or public browser script on
two already exposed, source-known scientific questions. It checks the returned
family, compact packet and immutable source URLs, and requires real posting and
lexical fetches. It is a small DOM harness, not an independent browser or a new
held-out benchmark. Actual GUI and governing-source HTTP/range checks remain
separate release checks. Reproduce with:

```
node knowledge/evaluations/2026-10-30-pages-query-closure/verify_browser_query.cjs /absolute/staged-view /tmp/query-check.json
node knowledge/evaluations/2026-10-30-pages-query-closure/verify_browser_query.cjs https://harjassand.github.io/astra-research-knowledge/ /tmp/public-query-check.json
```

An interim generated-view repair may restore only the omitted exact shards from
the already reviewed merged source while the permanent correction undergoes
required PR CI. It preserves that source/input identity and changes no canonical
data or scientific acceptance. Final closeout requires the corrected publisher's
reviewed main merge, actual deployment, natural query, packet/source and native
verification; a push or exact-ID success is insufficient.

The interim repair publication `b356f00f177c0b46e96ae185e54ff7c1cab6b004` retains
the failed publication as its parent and adds the exact declared shards from
merged276. [Existing Pages deployment40980454869](https://github.com/harjassand/astra-research-knowledge/actions/runs/40980454869)
passed. Both actual anonymous HTTP natural queries, compact packets and pinned
source routes [pass](ACTUAL_INTERIM_PUBLIC_NATURAL_QUERIES.json). The real browser
also now returns N1338first for the same previously failing query, shows the
correct corpus identity and renders the corrected conditions with immutable
source links. [Restoration scope](INTERIM_PUBLIC_RESTORATION.json) keeps that
interim repair distinct from the permanent PR release.
