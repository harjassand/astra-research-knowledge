# N853 targeted primary-acquisition gate, 2026-10-15

Reference pin: 6fde70a4668f877bc9988bc8f20c570ef4513d08. Read supplied N853.txt and PRIMARY_COMPARISON.md. No canonical edits.

## Outcome

Diamond–Essén full text was NOT acquired. Its original theorem, proof hypotheses, and relationship to arbitrary compact distributions and strict Laplace positivity remain UNKNOWN. The access failure gives no evidence of novelty. No independent external correctness certification was obtained.

A substantive refinement of the known Katkova–Vishnyakova overlap is available: in its admitted scalar class, elementary postprocessing gives an even smooth strictly positive probability kernel with every exponential moment and strictly positive output. Thus those output properties cannot individually be used as separating features. Strict log-concavity, arbitrary input distributions, higher-dimensional radiality, and matrix/Banach-cone scope remain unresolved by this argument.

## Primary text actually inspected

Katkova–Vishnyakova, Positivity 5 (2001), 1–11, DOI 10.1023/A:1009847605313. The institutional PDF was acquired and its extracted theorem text checked: https://ekhnuir.karazin.ua/bitstreams/41e252c6-eba5-435f-bbbb-66a8582ace7e/download . Saved as KV2001.pdf (252576 bytes; SHA-256 f24e4260a54627f5ad68e0bfdba4c13bdf82e2d327453222a8cede43999b8925), with KV2001.txt extraction. Author-uploaded full text (identified as uploaded by Anna Vishnyakova) was also readable:
https://www.researchgate.net/publication/235701306_A_Continual_Analogue_of_a_Theorem_by_M_Fekete_and_G_Polya

Theorem 2 assumes continuous real f on [a,b], positive endpoint values and L_f(s)>0 for every real s. For every sufficiently small lattice spacing h, all sufficiently large λ give f*μ≥0, where μ({kh})=λ^k/k!. Theorem 1 instead allows continuous half-line f, absolute exponential integrability at every nonnegative parameter, nonnegativity outside a bounded middle interval, and a positive point in each outside region, together with strict real Laplace positivity. Neither requires a quantitative global transform margin. The final remark gives an incommensurate four-atom obstruction to this particular lattice multiplier. It does not exclude arbitrary positive kernels. The paper identifies Diamond–Essén as a predecessor but does not reproduce its exact theorem.

## Derived scalar overlap: full proof

This deduction is ours, not a theorem attributed verbatim to the paper. Let f be any nonzero integrable real function with L_f(0)>0 for which the inspected theorem supplies μ. Normalize ν=e^{-λ}μ; it is a probability measure. Then q=f*ν≥0 and ∫q=L_f(0)>0. For h>0,

L_ν(s)=exp(λ(exp(hs)-1))

is finite for all real s. Define reflected measure ν̌(A)=ν(-A), and let γ_σ be any centered nondegenerate Gaussian probability density on R. Set

p=ν*ν̌*γ_σ.

1. p is an even probability density, hence radial in one dimension.
2. p is smooth and positive everywhere, since γ_σ is smooth and positive and ν*ν̌ is a probability measure. Differentiation is legitimate because every Gaussian derivative is bounded.
3. Its transform is

L_p(s)=exp(λ(exp(hs)+exp(-hs)-2)+σ²s²/2),

finite for every real s. Consequently ∫exp(a|x|)p(x)dx is finite for every a>0.
4. Every derivative also has every absolute exponential moment: for η=ν*ν̌,

∫e^{a|x|}|p^{(j)}(x)|dx ≤ (∫e^{a|y|}dη(y))(∫e^{a|z|}|γ_σ^{(j)}(z)|dz)<∞.

5. By associativity, f*p=q*ν̌*γ_σ. The measure q*ν̌ has positive finite mass and is nonnegative. Its convolution with the everywhere-positive Gaussian is positive at every real point.

This proves smoothness, evenness, every exponential moment, weighted derivative integrability, and strict output positivity within the admitted scalar class. It proves no log-concavity claim.

Moreover, a compactly supported smooth f with zero endpoint values is not automatically outside the older result: if it is nonnegative in neighborhoods of both support endpoints, with positive points there, a translation places it in Theorem 1. Theorem 2’s positive endpoint values alone are not the correct boundary for the full paper. Inputs with sign changes accumulating at a support endpoint are not covered by this observation.

## Acquisition receipts and remaining gap

- Publisher record: https://www.sciencedirect.com/science/article/pii/0022247X78900914 identifies Diamond–Essén, JMAA 63(2), April 1978, 463–489, DOI 10.1016/0022-247X(78)90091-4, and labels it Open archive. Search retrieval displayed bibliographic metadata only.
- Web opens of that article and its /pdf and /pdfft routes returned internal fetch errors, with no article text.
- A direct ordinary request to /pdfft returned a 195-byte HTML Site Unavailable page, saved separately as publisher.response. No article text or theorem was returned.
- The public Illinois author profile https://math.illinois.edu/directory/profile/hdiamond linked https://faculty.math.illinois.edu/~diamond/ . Following that link timed out; a subsequent web open was unavailable, and an ordinary direct request returned HTTP 502.
- Exact-title, DOI/PII, author/title, PDF, Illinois, and DiVA repository searches surfaced metadata and citing papers, not a legitimate accessible copy of the original.
- The ResearchGate citation target https://www.researchgate.net/publication/243008224_Functions_with_non-negative_convolutions returned cache-miss errors. No author outreach/request-copy action was taken.
- The public Elsevier unkeyed content endpoint was unavailable through the web tool. It was not treated as theorem evidence.
- KV’s institutional landing page https://ekhnuir.karazin.ua/items/1a762cd4-301a-4eff-97f4-46d87aab8384 was indexed with POLYA.pdf, and web-tool retrieval failed; ordinary direct retrieval subsequently succeeded, exposed its citation_pdf_url, and that public PDF download succeeded. Its first two pages confirmed the theorem assumptions above. The linked ResearchGate PDF returned 404.

Needed to close the Diamond–Essén acquisition gate: an accessible legitimate scan or full text, then extraction of exact theorem numbers, spaces/support/decay assumptions, kernel class, strict versus weak conclusion, and any multivariate/distribution extension. Until then, do not infer that either the scalar criterion or its arbitrary-margin aspect is new. The present result is a strengthened overlap analysis plus documented primary-access failure, not the requested complete predecessor reconstruction.
