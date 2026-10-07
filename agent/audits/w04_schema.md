# W04 — agent-readable scientific card schema

## Corpus inspection and design constraint

Inspected the claims-index records and full card text for ten diverse entries: `L01-cyclic-grid`, `L04-block-cover-obstruction`, `L09-egyptian-supply`, `N06-nonsofic-hyperbolic`, `N18-cost-detection`, `N24-acquired-rational-rounding`, `N33-endotactic-permanence`, `N36-query-gaussian-converse`, `N37-sequence-archive-costs`, and `N95-positive-word-relative-kernels`. These span short curated claims and long supplied proof packages; theoretical bounds, constructions, algorithms, a counterexample, and an explicitly missing acquisition step.

The existing index is already useful for identity and provenance: `id`, `title`, `path`, `topics`, `status`, `source_ids`, `source_paths`, dependencies, token count, and record type. It generally does not encode the claim's quantifiers, oracle/measurement contract, what is supplied versus acquired, or cost units. Those are card-level content and should be exposed as typed fields without replacing the source prose. A lossy semantic extraction must never be presented as a stronger source claim.

## Stable ontology (JSON-compatible YAML)

Use one record per claim, retaining the original index ID and exact source references. Required top-level keys are shown below; a value may be the literal string `UNKNOWN` when absent or ambiguous in inspected evidence. `UNKNOWN` is a value, not null, false, zero, or an invitation to infer. Empty arrays mean the source explicitly supplies no such item only when stated; otherwise use `UNKNOWN`.

```yaml
schema: astra-card/1
claim_id: string                         # claims.jsonl id
title: string
claim_kind: theorem | bound | construction | algorithm | obstruction | counterexample | empirical | mixed | UNKNOWN
statement: string                       # concise faithful statement with quantifiers/scope
quantifiers:                             # preserve order and dependency of choices
  - binder: string
    domain: string
    dependency: [string]
    condition: string
interface:
  object: string                         # mathematical objects/problem
  supplied: [string]                     # input/model facts available to claimant
  acquired: [string]                     # data/oracles/objects that must be produced
  oracle_or_observation: string
  output_or_success: string
  exclusions: [string]                   # explicit nonclaims / forbidden shortcuts
costs:
  - measure: string                      # e.g. queries, returned entries, bits, operations
    bound: string
    unit: string
    charged: [string]
    excluded_or_unaccounted: [string]
status:
  epistemic: source_reported | internally_reconstructed | finite_checked | externally_verified | conditional | candidate | refuted | UNKNOWN
  source_label: string                   # exact card/index status text
  scope: string                          # what evidence status applies to
  checks: [string]
dependencies:
  - id: string
    relation: string
    required_scope: string
counterexamples_or_failures:
  - target: string
    witness_or_reason: string
    scope: string
next_gap: [string]
sources:
  claim_record: string                   # path in corpus
  card: string
  evidence:
    - {id: string, path: string}
extraction:
  confidence: high | medium | low
  unknown_fields: [string]
  notes: string
```

### Field rules

1. **Quantifiers are ordered binders, not decorative prose.** Preserve phrases such as “for every diagram, first choose one common set, then for every initial state and measurable rate path”; do not commute choices. If the card says “for every C>…”, retain the strict inequality. Avoid silently expanding a claim beyond the exact interface.
2. **Interface separates supplied from acquired.** A supplied matrix, source package, known covariance, or exact oracle differs from a data-dependent object that the proposed method must discover, emit, or compile. Record acquisition as `UNKNOWN` if the card does not say. “Efficient acquisition unprovided” is an explicit gap, not an acquisition guarantee.
3. **Costs are a vector.** Never collapse queries, arithmetic operations, bit complexity, output volume, memory, precision, and setup into one “polynomial cost.” State the unit and charged components per bound. Put specifically omitted costs in `excluded_or_unaccounted`; use `UNKNOWN` if the source gives no accounting. Distinguish expected from worst-case and finite-block from asymptotic costs.
4. **Status is evidence-scoped.** Preserve the exact source status string and separately normalize its epistemic meaning. “Finite checks SOURCE-REPORTED” supports neither replay nor proof verification. Indexing, model agreement, compilation, or inclusion in a complete package do not promote status. Record branch-specific status rather than assigning one status to every dependent claim.
5. **Counterexamples have a target.** Attach each obstruction or failure to the precise interface/mechanism it defeats. An obstruction to independently charged complete-block covers does not refute all selective products. If none is stated, write `UNKNOWN` unless the source explicitly says none.
6. **Next gap is actionable and source-grounded.** Copy the stated gate (for example, acquire a concrete family, verify a named lemma, or obtain independent review); do not manufacture an attractive research direction. `UNKNOWN` if absent.
7. **Provenance is immutable.** Keep source IDs and paths exactly as in `indexes/claims.jsonl`; cite the card path as well. For a derived field, attach a short extraction note and confidence. Never synthesize an evidence ID.

## Example conversions

Examples below are faithful extraction examples, not new mathematical validation. `UNKNOWN` is deliberately retained for fields the card does not specify.

```yaml
schema: astra-card/1
claim_id: L04-block-cover-obstruction
title: Selective-output complete-block-cover obstruction
claim_kind: obstruction
statement: >-
  For integer X in Z^(N x D), Y in Z^(D x N), D=N^(1/4), and arbitrary
  selected output set W with |W|<=N^(15/8), some legal masks force Omega(N^2)
  work for decompositions using independently charged complete-block covers.
quantifiers:
  - {binder: N, domain: positive integer, dependency: [], condition: UNKNOWN}
  - {binder: X,Y, domain: integer matrices of stated dimensions, dependency: [N], condition: UNKNOWN}
  - {binder: W, domain: output mask with |W|<=N^(15/8), dependency: [N,X,Y], condition: some legal mask gives the lower bound}
interface:
  object: Selectively charged outputs of matrix product XY
  supplied: ["X,Y; arbitrary selective output mask W; dimensions and entry domain"]
  acquired: UNKNOWN
  oracle_or_observation: UNKNOWN
  output_or_success: Compute selected entries under a fully charged subquadratic selective-product model
  exclusions: ["Only independently charged complete-block-cover decompositions are ruled out", "Shared output-local arithmetic remains permitted", "Earlier G partial interface D<=N^(1/7) is separate"]
costs:
  - measure: work
    bound: Omega(N^2) for some legal masks
    unit: fully charged arithmetic/work (finer machine unit UNKNOWN)
    charged: ["independent complete-block cover charges"]
    excluded_or_unaccounted: ["shared output-local arithmetic is permitted", "precise bit-height/runtime accounting UNKNOWN"]
status:
  epistemic: candidate
  source_label: source_derived_unreviewed
  scope: "Source-derived obstruction scoped to independently charged complete-block covers; not a general lower bound for all algorithms"
  checks: UNKNOWN
dependencies: []
counterexamples_or_failures:
  - target: "Claim that released all-field 9/4 result alone supplies coordinates/decoder"
    witness_or_reason: "Card says it does not supply the required coordinates/decoder"
    scope: "This construction route"
next_gap: ["Find shared computation respecting actual mask incidence"]
sources:
  claim_record: outputs/ASTRA_KNOWLEDGE/indexes/claims.jsonl
  card: outputs/ASTRA_KNOWLEDGE/cards/L04-block-cover-obstruction.txt
  evidence:
    - {id: d-efd7fb715443bfdc, path: literature/results/root_cycle19/REPORT.md}
    - {id: d-d2ebdc4e16ec4b31, path: literature/notes/frontier_tensor_bridge/cycle19/SELECTIVE_OUTPUT_AUDIT.md}
extraction:
  confidence: high
  unknown_fields: ["exact machine unit", "oracle", "check execution/replay", "full bit-complexity"]
  notes: "Selected as a negative result; lower bound scope is explicitly restricted in the card."
```

```yaml
schema: astra-card/1
claim_id: N36-query-gaussian-converse
title: Gaussian memory lower survives later coordinate-specific quantum measurements
claim_kind: bound
statement: >-
  For one blind X~N(theta,I_d), theta in {+/-r e_i}, 0<r<=1, and the stated
  finite total hybrid archive of dimension at most D at every public-seed value,
  if after storage one chosen coordinate i is measured by an arbitrary
  i-dependent POVM with sign-conditioned output TV<=epsilon, then
  ln D >= (d/2) ln(r/epsilon) - (5/4+ln 2)d.
quantifiers:
  - {binder: d, domain: positive integer, dependency: [], condition: UNKNOWN}
  - {binder: r, domain: real, dependency: [d], condition: 0<r<=1}
  - {binder: epsilon, domain: real, dependency: [d,r], condition: UNKNOWN}
  - {binder: encoder/archive, domain: stated blind finite total hybrid archive, dependency: [d,r,epsilon], condition: dimension<=D at every seed}
  - {binder: i, domain: {1,...,d}, dependency: [archive], condition: query selected after storage}
  - {binder: POVM_i, domain: arbitrary coordinate-dependent POVM, dependency: [i,archive], condition: sign-conditioned output TV<=epsilon}
interface:
  object: "Gaussian location needle archive with a later single-coordinate quantum measurement"
  supplied: ["blind X~N(theta,I_d); theta is one of +/-r e_i; independent public seed allowed"]
  acquired: ["archive must be formed before query i is selected"]
  oracle_or_observation: "After storage, one chosen coordinate i may be measured with an arbitrary i-dependent POVM"
  output_or_success: "Distinguish sign distributions for queried coordinate to total variation error at most epsilon"
  exclusions: ["No common joint output vector", "No nondestructive or repeated measurements", "Encoder given i before storage voids this lower bound", "No null reconstruction premise", "No correlated side information or free entangled reference"]
costs:
  - measure: archive_dimension
    bound: "ln D >= (d/2) ln(r/epsilon) - (5/4+ln 2)d"
    unit: natural logarithm of Hilbert-space dimension
    charged: ["all branches' total dimension d_j summed as D", "all input-dependent records"]
    excluded_or_unaccounted: ["public seed is independent; ancillary/measurement implementation cost UNKNOWN"]
status:
  epistemic: internally_reconstructed
  source_label: "source_derived_unreviewed;COMPLETE supplied P evidence package;branch-specific internal proof/audit status below,external correctness/priority unresolved;checks SOURCE-REPORTED unless marked otherwise."
  scope: "Full converse and audits supplied; internal checks do not establish external correctness or priority"
  checks: ["Source reports proof/audits supplied", "No external proof verification recorded"]
dependencies:
  - {id: N31-spectral-gaussian, relation: strengthens, required_scope: "Later-query quantum converse contract"}
  - {id: N30-gaussian-multiscale, relation: related_not_premise, required_scope: "Weak-signal result; not a proof premise"}
counterexamples_or_failures:
  - target: "Using a common joint output distribution for incompatible coordinate POVMs"
    witness_or_reason: "Card explicitly says no common joint vector is assumed; converse instead uses per-query Holevo bounds"
    scope: "Proof shortcut rejected"
next_gap: ["Acquire/validate the measurement model and Gaussian bridge if extending the result beyond this exact interface", "External correctness and priority remain unresolved"]
sources:
  claim_record: outputs/ASTRA_KNOWLEDGE/indexes/claims.jsonl
  card: outputs/ASTRA_KNOWLEDGE/cards/N36-query-gaussian-converse.txt
  evidence:
    - {id: d-09516fa0e77f5538, path: updates/P/package/outputs/gaussian_archive_converse.txt}
    - {id: d-378e64d8fdae0e24, path: updates/P/package/work/agents/sparse_gaussian_converse/report.md}
    - {id: d-ad2bd6455b0245cb, path: updates/P/package/work/agents/gaussian_sequence_audit/report.md}
    - {id: d-ab35de5815e7abec, path: updates/P/package/work/agents/sparse_gaussian_upper/report.md}
extraction:
  confidence: medium
  unknown_fields: ["epsilon's full domain is not printed on card", "implementation cost of arbitrary POVM"]
  notes: "The statement preserves the card's precise query timing and per-coordinate measurement contract."
```

## Extractability verdict

The schema is extractable from this corpus at useful fidelity, with human or strong-agent review for the statement and ordered quantifiers. Metadata, provenance, and source status are already structured. Interface and cost often appear in prose but can be parsed conservatively; unknown is common and expected. The long cards contain enough explicit detail to encode acquisition, charged units, limitations, and next gates. Compact cards such as L09 deliberately defer quantifiers and counting units to cited proof material, so the card alone cannot support a complete formal record. Do not fill those fields from title, topic, sibling cards, or agent intuition: mark `UNKNOWN` and point to the cited evidence that must be opened.

The useful optimization is readable mathematical notation plus explicit interface/cost/status fields, not private token codes. Keep a lossless link to the source text and permit a field to say `UNKNOWN`; concise machine-readable summaries can then improve retrieval while agents retain the exact claim boundary.
