# W05 — Token-efficient representation check

## Question and method

Compared three representative glued-word entries in `outputs/ASTRA_KNOWLEDGE/exports/ASTRA_BRIEF.txt` (L02, N06, N77) with four hand-written alternatives: readable prose/notation, one-record JSONL, compact labeled notation, and multiline TSV-style field/value routing. Token counts use the vendored `tiktoken` package and `o200k_base` encoding from `work/token_count_deps`; byte counts and counts below are for these exact strings, without enclosing Markdown or a shared schema header. The alternatives retain the original stated interfaces, assumptions, numerical bounds, provenance/availability, acquisition cost or obstacle, and explicit limits. This is a manual information-preservation check, not a formal equivalence proof.

## Measured counts

| Entry | Current glued text | Readable notation | JSONL | Compact labeled | TSV fields |
|---|---:|---:|---:|---:|---:|
| L02 game tail | 113 | 118 | 128 | 123 | 115 |
| N06 CAT(−1) candidate | 95 | 101 | 109 | 100 | 101 |
| N77 reaction-network counterexample | 88 | 99 | 104 | 99 | 96 |
| **Total** | **296** | **318** | **341** | **322** | **312** |
| **Change vs current** | — | **+7.4%** | **+15.2%** | **+8.8%** | **+5.4%** |

For these samples, none of the clear formats saves tokens under this tokenizer. TSV is the smallest clear alternative, at 312 versus 296 tokens; its field labels and separators cost more than the glued text saves. JSONL has the highest structural overhead. Readable notation improves spacing and readability but likewise costs tokens. The samples are small and selected for diverse content, so these figures do not estimate the whole corpus.

## Candidate TSV forms

These illustrate what was counted. The TSV field/value style keeps each scope dimension explicit and can support field-level retrieval; its labels are part of the measured cost.

```text
L02	interface	arbitrary commuting strategies; finite 2-player game; v<1; answer-product d; resampling gap σ
bound	k≥1, 0<δ<1−v: Pr[W_k≥ceil((v+δ)k)]≤exp(−σδ³k/[2048(1+log d)])
method	algebra-preserving transport; bounded forms; spectral barycenters; half-erasure gives σ≥1/4
limits	efficient sampling does not acquire σ; no locality, positive sparse enforcement, or quantum PCP

N06	source	OA252
witness	approximate permutations; Δ≤r²(S_inc δ+Nλ/8); defects≤1/(100rq) impossible
construction	changed triangle angles; girth≥14; candidate torsion-free nonsofic CAT(−1) hyperbolic group
acquisition	explicit recursive common-kernel word after astronomical finite acquisition; no tables emitted
limits	no unitary/linear/property-T/direct-finiteness transfer; external review/priority open

N77	network	2C→A+B+C→3A+2B→2C; 2C↔2C+D
conditions	explicit deficiency-zero; one-linkage
constraint	A−B(B+1)/2=n
result	infinite irreducible positive-recurrent classes; Poisson(1) stationary laws escape in same B+C=2 plane despite common ODE attractor
scope	refutes classwise uniform tightness; not component recurrence
```

## Interpretation and limits

A readability or routing choice can still be worthwhile even when it does not reduce raw tokens: TSV/JSONL make fields easier to address mechanically, while prose makes scope easier to read. Those benefits were not tested here, and no model-retrieval or reasoning evaluation was run. Token savings alone would not establish any capability gain. `o200k_base` is only the repository's documented estimate; Astra's deployed tokenizer is unknown, so actual Astra counts and relative ordering may differ. The report does not test compression bytes or hidden/private codes, which would require accounting for decoding instructions and tool/runtime cost.
