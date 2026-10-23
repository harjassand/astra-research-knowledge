# Spider review: status, actual costs, and source use

Reviewer: `/root/cycle8_structural_scope`, Cycle9.

## Accepted mathematical claims

`REVIEW.md` checks the intrinsic K_(2,k) block-tree construction, all-depth
spider classification, exact LS noise bound, matched five-coordinate star
control, and a quantitative failure when a middle meets more than two blocks.
It subsequently checks the root's direct K_(p,k) generalization, the exact
worst-case star count 2p+1, and the exact uniformly stable unit-coordinate
count p+2. After reading the port contributor's actual new congruence proof,
it also independently verifies the extension to real signed/unequal
single-coordinate row amplitudes, with the weaker lower rate Gamma^(1/4).

These are internal analytical reviews, not external scientific acceptance or
historical novelty determinations. The full arbitrary-real design question
remains separate. For p>=3 the general graph class is triangle-free but need
not be chordless; that change is stated explicitly.

## Actual implementation correction

Reading the first native implementation exposed a real unbounded-degree cost
defect: per-cut membership in a list of a block's middles could total
Theta(k^2). Root replaced it with one cached middle set per block. The
corrected generalized source was then read, and both the set correction and
common-p/full-bipartite role validation are present. `SOURCE_BINDINGS.json`
pins the corrected source inspected for this conclusion.

## New independent diagnostic

`check_spider_claims.py` imports no producer modules. It checks the exact
quadratic identity in Q(sqrt5), constructs one branching graph to check the
four-coordinate spiders and five-coordinate stars, and constructs one exact
full-action double-star witness after dropping the block-membership cap.
There is no old gate replay, graph-size sweep, parameter sweep, fitted
eigenvalue, or full programme duplication.

Its first recorded body took 0.0008718409999346477 seconds, with process
maximum RSS 9344 KiB. The all-size/general-p conclusions are the proofs in
`REVIEW.md`; they are not inferred from this finite diagnostic. Full inference,
source authoring, review, and integration costs remain unknown. The root's
native action/reconstruction computations and other independent validators
are separately owned and must be charged in their own records.

## What changed because of the received work

The Cycle5 cut-balance witness is used to prove instability for every smaller
coordinate design on an actual block path. The Cycle8 triangle-free star-LS
bound supplies a stronger-conditioning matched control. The current port
contributor's congruence argument expands the lower's scope to signed and
unequal row amplitudes. The result is a representation-specific distinction
between star compression and stable recovery, with an actual native query
operation rather than a coloring summary alone.

The implementation fix changes accepted total preparation cost. None of these
facts implies a causal advantage from a particular prompt, agent count,
reset strategy, archival receipt, or timing run.
