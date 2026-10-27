# Agent retrieval comparison and source-use review

The upgrade makes existing scientific operations, intermediate constructions and
registered evidence easier to navigate. It does not establish superiority over
Google, a universal semantic interpreter, or a new scientific/physical capability.
A strong matched-content lexical baseline is part of the delivered system, not a
baseline discarded in favour of a model.

## Frozen comparisons and prior context

Implementation round 1 was frozen at
`4ebc97f23bc73327a813b6bfcce15ff95c1b530a` before the 17 questions in
[round1-problems.json](round1-problems.json) were written. The same owner selected
source-supported mechanisms and wrote/evaluated the questions. Scientific
families and some earlier context were already known. This is fresh formulation
after a code freeze, **not blind, independent, or a held-out general benchmark**.
Questions/answers did not become ranking aliases. The original 23-probe review,
N675/N684 diagnostics and the 18 response/physical-interface probes were already
exposed development material.

Every compared method receives the same query/object/operation text and five
family slots. `lexical` means full **card** BM25. `content_lexical` means ordinary
BM25 over the **same complete record/source content** available to structured
search, without field weights or expansions. `structured` is the previous
field-weighted method with visible concept expansion and a full-card safety
slot. `agent` uses local relevance reranking, family expansion and the safety
slot. Available/unavailable declarations do not boost relevance; they trigger
premise inspection. A family hit is navigation, not an answered question.

| First fresh round | First-family hits | Top-five family hits |
| --- | ---: | ---: |
| Full-card BM25 | 7/15 | 11/15 |
| Matched-content BM25 | 11/15 | 15/15 |
| Previous structured route | 10/15 | 12/15 |
| Field-seeded agent v1 | 11/15 | 14/15 |

The denominator is the 15 source-supported/condition-check tasks. F15 and F16
are separate unsupported positive-capability requests. All outputs, including
failures, are in [round1-results.json](round1-results.json).

**F04 was a real failure.** The required future-address/retry passage was the
81st unique field-ranked record, so an 80-record candidate cutoff excluded it.
Unweighted matched-content BM25 found its family third. The general repair
interleaves both independent candidate generators before the same bounded
reranker/family expansion. No query text, target ID or special scientific alias
was added to ranking code. A development replay then recovered F04 first. That
replay is exposed development, not an additional fresh success claim.

The revised implementation was frozen at
`fe1eb5299c62a15800015a1bb430171bf6559dc3` before the nine different target-family
questions in [round2-problems.json](round2-problems.json) were written. The following table measures that frozen revision. A later broad legacy-card
repair exposes verbatim card sections instead of historical status summaries;
its source/line fidelity and additional navigation evaluation are recorded
separately below. No question strings, target IDs or concept aliases were added
to ranking code.

| Second fresh round | First-family hits | Top-five family hits |
| --- | ---: | ---: |
| Full-card BM25 | 4/9 | 5/9 |
| Matched-content BM25 | 6/9 | 7/9 |
| Previous structured route | 3/9 | 8/9 |
| Interleaved agent v2 | 6/9 | 7/9 |

All nine are source-supported tasks. [round2-results.json](round2-results.json)
retains the actual candidates, ranges, premise checks, timings and misses.
There is no measured universal winner. G02's multivalent clearance is fifth in
matched-content search and third in structured search but absent from agent's
five families. G09's non-atomic no-jump obstruction is first in agent/structured
and absent from both lexical top fives. G06's exact example of information with
no value for a particular signed task is missed by every tested method. The
union of methods can help, but consuming more candidate slots is a larger read
budget and is not a fair five-slot win.

The 18 previously exposed response/physical probes are retained separately in
[exposed-development-results.json](exposed-development-results.json): agent v1
16/16 supported families versus full-card 8/16 and structured 14/16. These were
implementation diagnostics, not unseen questions. Full-card lexical ranking
alone was not treated as a validated solution.

## Actual scientific use, beyond family hits

[passage-assessments.json](passage-assessments.json) binds the 24 supported tasks
to their actual current unit versions, exact inspected ranges, short anchors,
conditions and reproducible source commands. Twenty-six decisive passages were
read for this assessment; additional first citations/context were also inspected.
Gold-unit reads for failed retrievals document missed opportunities, not successes.
This is a completed, accepted internal navigation/source-support review, not a
new blanket mathematical audit of every retrieved claim. Existing current
scientific acceptance and genuine proof/acquisition gaps remain authoritative.

A realistic agent workflow allows five displayed families, selects a candidate,
reads its packet, and follows the applicable unit/source ranges. A related unit
or family packet is an additional navigation/read action and is counted as such.
Representative results:

| Problem | What the researcher can obtain | What it enables and what remains required |
| --- | --- | --- |
| F01 noisy cell lineage | Full-card and old structured top fives miss N461; content finds it fourth, agent v1 second. The N461 packet links U461; `updates/BL/package/lineage/research_note.md:16–115` derives the nonzero-lag pencil and variance formula. | Estimate inheritance variability from the specified noisy population moments without knowing noise variance. Requires stationary independent random-affine pairs, iid errors independent of the latent process, finite fourth moments and invertible covariance. This does not acquire a cell experiment or justify correlated segmentation noise. |
| F04 unsuccessful synthesis pulses | Agent v1 and old structured miss N1083; content finds the actual source window third. The revised candidate generator finds U1083 directly. The native construction explicitly pays downstream activation on every retry. | Use the correct eventual-yield product and its inverse-success-probability exposure factor to decide which activation operation is missing. Rates and chemistry remain supplied/hypothetical; no long-programme yield or apparatus is acquired. |
| F08 joint sampling instead of inversion | Agent v1 returns a different N1015 boundary unit first: a **family hit alone is insufficient**. The family packet's unit list leads to U1015-forward-joint-cover and the actual sampled-seed construction. The revised response shows separately ranked within-family units plus the complete family route. | Generate the two-branch joint object with one known forward permutation call and paid seed/address work, without receiving an arbitrary preexisting witness. General branches require a verified forward cover; this does not implement a generic inverse or remove guard/acquisition costs. |
| F17 correlated camera errors | The lineage unit is returned, and premise triage highlights iid/noise assumptions without declaring them satisfied. The actual source explicitly names correlated segmentation errors as invalidating the model. | Reject the proposed iid-to-correlated transfer or acquire a different noise model. Literal triage is not an entailment or contradiction prover; the source passage makes the incompatibility substantive. |
| G02 multivalent wash | Content/structured reach U1016 through N1016; agent misses the family. The actual source gives the birth–death clearance sum and exponential rebinding lower bound, with a real absorbing-sink premise. | Compare mechanisms that suppress rebinding with merely waiting longer. No real PNA arm rates, cooperativity model, active displacement or physical sink is supplied by retrieval. This remains an agent-ranker failure. |
| G06 task-specific value of information | No tested method returns N1069 in five families. A gold-source inspection at `ASTRA_PRO3_ACQUIRED_SPECTRAL_MEMORY_AND_TASK_SHAPING.md:97–126` finds an eight-fold component-interval reduction that leaves the signed task interval unchanged. | A useful missed premise for choosing measurements by the future task rather than model uncertainty. Finding it by the supplied gold ID is **not** a successful search. |

Other inspected passages include finite-conductor four-sign projection (F05),
Gaussian contact/actual re-registration (F06), a persistent sensor gauge (F07),
finite-arm truncation versus integrator error (F09), fixed-metal zero-mode
cancellation (F10), joint versus conditional acceptance probability (F11), paid
positive group-query reduction (F12), equal-rank projection entropy (F13), and
product-support Werner positivity versus the unrestricted open target (F14).
The second round checks precursor stock, expected assembly cost versus
worst-case support, force versus work, all-monotone-sensor stochastic dominance,
finite-error spectral thresholds, hidden passive motion and no-jump smoothing.
These routes expose usable premises without upgrading hypothetical models to
measurements, devices, advantages or universal theorems.

F15's universal NP-hard optimisation advantage is not established by its returned
busy-beaver/Gibbs candidates. F16 returns candidate materials/energy interfaces;
the retrieved molecular-work record explicitly says no acquired advantage and
requires actual reaction/return/reset/throughput evidence. Neither request
received a supported positive answer in the inspected candidates. Search itself
does not synthesize an answer or certify abstention; it labels candidates and
requires source inspection. This is not a proof that the entire corpus lacks
any relevant theorem.

## Source navigation findings and repairs

1. A card's located proofs previously suppressed its other available evidence
   windows. Both sets are now indexed. A separate evidence lane admits every
   current record citation plus explicit selected-public-source-index entries.
   Code/data/reviews/originals remain evidence navigation, not accepted lemmas.
2. A search window could inherit its parent range's quote anchor even when the
   anchor lay outside the window. Governing citations are retained, while each
   window now claims only an anchor present within its own range. A check opens
   every current scientific search-window reference.
3. A first citation can support only one part of a reusable statement. F02's
   first range proves the shared-shutdown/Jensen comparison; the algebraic tail
   and guaranteed-time remedy are in evidence 1 and 2. F06's geometric argument
   is evidence 1 rather than its undocking-only first citation. G03's rebuild
   theorem is evidence 1, not the connectivity-check first citation. Agent
   operation hits now require selecting the packet's scoped evidence index;
   only an actual matched source view supplies a direct S-id command. No
   arbitrary first citation is presented as proof of the entire statement.
4. Returning one family winner can bury another useful intermediate. The new
   response includes up to three separately ranked units plus the complete
   family packet. Shared family remains navigation, never a compatibility proof.

## Negative trials, runtime costs and coverage

The static embedding-only trials are retained: Potion base-8M 256-dimensional
9/16, Potion retrieval-32M 256-dimensional 8/16 and 512-dimensional 9/16 on the
16 exposed supported families. They did not justify an embedding-only service.
Early cross-encoder first-record/source-first trials each recovered 14/16 and
introduced regressions; family expansion reached 15/16; complementary lexical
safety reached 16/16. Their JSON files retain the failed rankings. The shipped
model is a pinned free local relevance scorer, not an additional LLM worker.

Within a reused Library process on this Mac, first-round median query times were
0.008s full-card, 0.082s matched-content, 0.271s structured and 5.332s agent v1.
Second-round medians were 0.009s, 0.046s, 0.965s and 6.000s respectively. These
are small workload timings under concurrent checks, not controlled throughput
benchmarks. The first agent query includes model initialization; setup and
Library freshness/loading costs are outside these per-query medians. Building
the in-memory comparison's content index took 24.38s in round 1; production now
ships that index, so portable content queries do not rebuild it. Model/tokenizer/
license metadata occupy 23,928,492 bytes. Current projections occupy 467,659,095
bytes, including 124,227,524 content-index bytes, 106,782,132 evidence-navigation
bytes and 3,858,681 operation-view bytes at the frozen revision. These are real
storage/installation/read costs, not free scientific acquisition.

There are 1,811 canonical scientific records: 1,141 results, 235 atlas lemmas,
389 other reusable units and 46 technology records. Their scientific content and content
versions remain unchanged from PR239's main. Current review/notice metadata
additionally recognizes the completed N557 audits at their actual version. Scientific source windows increase
from 10,245 to 24,527; windows overlap and are not discoveries. Evidence
navigation has 7,810 `(public path, SHA256, read_path)` artifact keys, 7,766 with
searchable ranges, 19,200 text windows and 44 metadata-only documents, using all
53 recognized selected-public-source indexes. Aliases may share bytes.

Current record-topic associations include analysis 615, physics 346, engineering
72, materials 72, chemistry 98, biology 30 and learning 122. These overlap and use
an incomplete taxonomy; the corpus is heavily mathematical. Eligible reusable
mechanisms and unregistered/withheld archives have an **unknown** completeness
denominator. Containers, scoped extractions, empty/operational artifacts retain
explicit exclusion reasons. None are quietly accepted or widened to full
third-party publications/private transcripts.

The next substantive improvement is a source-bound representation of the
requested decision/functional and the observation's effect on its ambiguity
class. G06 describes that role without the source's `g3/g4` vocabulary; neither
field/content matching nor this relevance model recovers it. G02 also shows the
need to protect useful literal candidates from neural analogy errors. More
aliases for these exact questions or a larger unvalidated index would not
establish a solution.

Reproduce comparisons with the pinned code/source revisions and optional local
runtime:

```
python knowledge/compare.py --cases knowledge/evaluations/2026-10-27-agent-retrieval/round1-problems.json --output round1-replay.json
python knowledge/compare.py --cases knowledge/evaluations/2026-10-27-agent-retrieval/round2-problems.json --output round2-replay.json
```

A replay on later code is exposed regression evidence, not the original frozen
measurement. Normalization remains the one existing build/check path; no
researcher reporting form is added.

## Legacy-card normalization repair

The source audit found 606 literal `status=` statement fallbacks and, more
generally, 762 summaries copied from a card's historical header. Some actual
claims/interfaces were present below that header but invisible in the compact
statement. The final projection locates verbatim labelled sections and
unlabelled scientific passages with their exact original card lines. Portable
and agent responses expose those excerpts while retaining historical reported
status separately. A labelled claim remains the author's claim; an unlabelled
passage has no inferred theorem role. Existing canonical scientific content, content
versions and genuine unknown contracts remain unchanged. Existing review
bindings are preserved; the separate completed-audit recognition below is added.

The new bounded `card` reader validates the actual status-to-card path/hash,
retains current notices/reviews and sends readers onwards to governing proofs.
This repairs summary usability without manufacturing a lemma or reclassifying
unaudited work. The intake fixture was updated to include the new source files
and pinned model assets; its initial omission caused the first CI failure,
which is retained in the review history. Additional checks cover malformed or
entry-less source indexes and evidence candidate flooding by many windows of
one artifact. Evidence budgeting now counts distinct artifacts.

## Final legacy navigation and completed-audit recognition

The scientific-card view was frozen at
`10295172353bd3543551eecf675aa13563d476fd`.
[legacy-problems.json](legacy-problems.json) contains four new source-informed
formulations (H01–H04) and two explicitly exposed diagnostics (H05/N557 was
already a regression fixture; H06/N405 was already inspected). The four new
formulations recover their expected family in five slots for structured and
agent search (4/4 each), and 3/4 for either lexical baseline. First-place hits
are content 3/4, full-card 2/4, structured 1/4 and agent 1/4. This again does not
show a universal ranker winner. H03/H04 ask for archived claims and their
representation/import boundaries; navigation is not acceptance of a candidate
theorem. [legacy-results.json](legacy-results.json) retains all outputs and
timings. These are same-owner, known-corpus, source-informed formulations, not
blind or held-out evidence.

The final exposed replay in [exposed-final-results.json](exposed-final-results.json)
recovers all 16 supported response/physical families with content and agent
search, versus 8/16 full-card and 14/16 structured. Those questions remain
exposed. The final scientific view has 1,132 exact card excerpts and 296 labelled
interfaces. Card/source-line fidelity is checked directly against original bytes.

The subsequent source-support audit inspected all three actual final N557
reviews, not just `review_resolutions.json`. Their full reconstructions and final
delta checks identify no remaining required mathematical fix and explicitly bind
the currently stored manuscript hash
`cfdbb6a0ca85861788d39c8843ce7533a641633c4cabab8070ac09b9d41d170d`.
The current [A557 review overlay](../../reviews/A557-completed-internal-cfdb.json)
therefore records **accepted_internally_verified** for the actual independent-input,
finite-mode, finite-energy main theorem. External/formal review is not a
prerequisite to that status. The proof/card/source bytes and all scientific
content versions remain unchanged; current review/notice metadata is updated.
The [scope comparison](../../audits/2026-10-27-amplifier-review-recognition.md)
retains failed strengthenings, the later heated log-tail correction and its
contrary programme-status assertion. It does not quietly blend those different
arguments or invent physical acquisition, novelty or advantage. No other
unaudited result is promoted by this recognition.

That review also exposed an ingestion gap: direct `record.evidence` is not every
registered citation. Current/historical review, notice, relationship and
version-bound transfer support now enter evidence discovery with separate
citation roles. An audit checked 14,016 distinct pre-recognition nested
references without a missing/wrong quoted passage; the added review sources
then pass the same compiler and all-citation membership checks. Scientific
ranking rules/weights/aliases were not tuned from the additional questions.

Final code/data scope is
`2ec67aaf373b809c7bf97fe9a7a42c89aff0e950`, dataset
`7bcdeb2e181fb8d6239e05a1bed5a9ae312aa96bdfb206314fd84671deba1958`.
It has 7,893 artifact keys, 7,850 with text ranges, 19,401 evidence text windows,
43 metadata-only documents and 53 selected-public-source indexes. This final
denominator includes **all nested registered current-record citations**,
version-bound transfer evidence and declared selected originals. Exclusion
mentions can coexist with permitted cited ranges; they are not a count of
distinct excluded artifacts. Scientific source windows remain 24,527 and
recoverable exact source versions are 6,512. Unregistered/private/withheld
archives and the count of still-unextracted useful mechanisms remain unassessed.
Final current projections occupy 474,437,014 bytes, including 6,822,077 operation
view bytes, 109,348,200 evidence bytes and 124,179,542 matched-content index bytes.
The earlier storage counts above describe the frozen pre-repair revision.

Five previously usable default packets would have exceeded 32 KB after adding
card previews. The compiler now omits only the optional preview text or provides
a card-reader locator, explicitly, while preserving every original condition,
review and correction. Previously oversized packets such as N557/N830 remain
explicit large-packet cases; the complete default `card N557` route fits 32 KB
with the current accepted review/notices. Thirty-seven targeted operation,
source, intake, runtime and fixture checks pass locally. The full required
publication check on the actual PR head is a separate merge gate; its current
result is visible on [PR241](https://github.com/harjassand/astra-research-knowledge/pull/241).
