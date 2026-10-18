# Publication continuity audit, 19 October 2026

Public baseline: `b862002a3bf216aa583f49d897bdb1d80c3ac508`, PR #108,
16 October 2026 at 23:06:29 Australia/Brisbane. This is a repository/workflow
audit, not a validation of the scientific corpus.

At this snapshot no later main update exists. Five older draft PRs remain open:
#84, #85, #87 and #88 conflict with main; #95 is mergeable. They retain their
research and were not force-merged, closed or rewritten by this repair. The
publication gap does not establish that independent research stopped, or why a
particular researcher did not submit an update.

## Observed blockers

The original seven publisher fixtures pass while normal validation fails first
with `evidence path is absent at source_revision: updates/CR/README.md`. A normal
full-history clone lacks an original source commit retained by squashed PR #23.
Fetching the exact recorded `80d2eff466f81b1b22cf69ed6465f16f928337a9` restores all
21 recorded source-reference checks in four checkpoints: every original hash
matches. No source pin or ancestry is corrected, and no revision-check waiver
is needed. The old message incorrectly conflated missing Git-object transport
with an absent path. Explicit source recovery now precedes the ordinary checks.

The next blocker is three schema-less historical records from the DT intake.
The old publisher loads and validates every historical checkpoint before writing
any new one, so these unrelated records block all branches. Later updates
document repeated individually checked drafts/new-only workarounds rather than
repairing that path. Those records and their source bytes remain preserved.

There are 169 original checkpoint files: 166 schema-v1 and three schema-less.
The old registry has 106 routes, 102 of them worker routes; 101 routes have only
one checkpoint. Built-in route heads date from 10–11 October, and the newest
canonical checkpoint dates from 15 October. Top-level update directories contain
25 draft/version files on 14 additional worker routes, none canonical. A draft
and a merged scientific update can therefore coexist with stale shared heads.
The recovery index links their exact existing bytes without changing their
draft status or claiming the producer is currently active.

At this baseline GitHub's green checks are generated Pages build/deploy checks;
there is no tracked publication-integrity workflow. The access projection and
its seven fixtures pass, but those checks do not exercise the failing publisher.

## Complexity and the repair boundary

PR #108 changed 472 paths for six routes. Its changes include preserved research,
mirrors, generated access views, receipts and multiple shared registries. That
fan-out is observable; it does not prove every file was unnecessary. Requiring
that full intake for every exploratory run would nevertheless couple research
to publication and encourage stale sidecar handoffs.

The default is now one optional selected-event compiler into the existing
schema-v1 checkpoint tree. It derives mechanical fields and hashes, preserves
unknown statuses, and uses the existing locked writer. A minimal shared event
needs its selected evidence, one checkpoint, a branch view and the registry.
Curated card/bridge/gate intake remains available when useful; it is not a
prerequisite for independent research or an ordinary publication handoff.

Only three exact historical navigation adapters are retained, pinned to original
record bytes and public baseline. Every available evidence file is still
checked. Their missing ancestry stays `UNKNOWN`. No historical checkpoint,
proof, script, dataset, scientific claim authority or source revision is edited.
The theoretical-pro fork is reconciled as an archival handoff with all three
topic/record links retained. It does not consolidate their mathematics or direct
any researcher's next work. Branch views show history and current activity as
`UNKNOWN`, rather than treating a dated publication as a live worker status.

[PUBLICATION.md](PUBLICATION.md) gives the short route. The one-command local/CI
check validates actual PR-base append-only history, current evidence, metadata,
compatibility limits, concurrency fixtures and access freshness. These are
publication/software results only. Original scientific conclusions retain their
original reported/internal/external/experimental boundaries.
