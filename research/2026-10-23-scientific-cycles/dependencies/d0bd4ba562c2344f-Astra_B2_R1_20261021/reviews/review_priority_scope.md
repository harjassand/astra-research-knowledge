# Bounded priority and scope crosscheck

21 October 2026. Question: do these nearby papers already establish the sharp reservoir law \(E_R^{\min}(J,\delta)=J\ln2/(2\delta)-\ln(1/\delta)+O_J(1)\), with exact Bell blocks, no fresh entanglement, and half trace return of the complete bipartite memory?

## Xing et al. (2024)

*Teleportation with embezzling catalysts*, Communications Physics 7, 357. [Published paper](https://www.nature.com/articles/s42005-024-01828-x); [published PDF](https://www.nature.com/articles/s42005-024-01828-x.pdf); [primary preprint](https://arxiv.org/html/2406.14386v1).

Read the published definitions and the preprint's Sections III.2–III.4 and V. The convex-split construction uses mixed catalysts \(\tau^{\otimes(n-1)}\), with \(\tau\) close to a Bell state and sufficiently supported. Its performance combines teleportation fidelity, approximate entanglement distillation, catalyst dimension, and purified-distance disturbance. Equations (20), (34)–(35) bound terminal catalyst disturbance; Theorem 4 and (74)–(75) guarantee approximate Bell production. The harmonic construction also permits output error. These results neither supply exact Bell blocks at finite parameters nor minimize the catalyst's \(E_R\). Their purified error is not numerically identical to half trace error: \(\delta_{\rm tr}\le P\le\sqrt{2\delta_{\rm tr}}\). The inspected statements supply no every-use complete-process theorem or matching \(E_R\) converse. Thus their mixed catalysts do not directly imply the specified sharp law. This is a scope comparison, not a claim of priority.

## Fang–Liu (2026)

*One-shot distillation with constant overhead using catalysts*, Nature Communications 17, 6010. [Published paper](https://www.nature.com/articles/s41467-026-72686-0); [published PDF](https://www.nature.com/articles/s41467-026-72686-0.pdf); [primary manuscript, version 3](https://arxiv.org/html/2410.14547v3).

Read Definitions 1–2, Theorems 3–4, Lemma 5, their construction/reuse proofs, and Discussion. Overhead counts fresh noisy source copies per target, with an unrestricted auxiliary catalyst, rather than minimizing catalyst \(E_R\). The deterministic reuse theorem preserves the entire catalyst marginal exactly at every use and preserves each output's marginal accuracy; outputs may remain correlated. Its proof explicitly supplies fresh resource states each round. Error is half trace distance; Lemma 5 bounds one output's decoupling by \(2\sqrt\varepsilon\). The discussion leaves approximate catalyst return and optimized catalyst size for further work. Consequently the result is neither a free-input Bell reservoir nor a sharp catalyst-cost law. Its every-use marginal guarantee should not be represented as an independent exact Bell process. Exact pure marginals would force factorization, but the stated finite-error guarantee does not. The source supply, rather than any failure of recurrence reasoning, explains compatibility with R1.

## Assessment

Neither inspected paper establishes the requested optimization theorem or its negative logarithmic term. Both belong in the related-work boundary. This bounded comparison cannot certify novelty; a mathematically equivalent result elsewhere remains possible. No additional investigation is proposed.

## Follow-up: Rubboli–Tomamichel references 34, 36, 37

The reference numbering was checked directly in https://arxiv.org/pdf/2111.13356, pp. 5–6. The paper's remark about known optimal embezzlement bounds should not be read as a claim about the present mixed-state optimization.

| Reference | Primary paper and inspected scope | Relationship to the exact mixed reservoir law |
| --- | --- | --- |
| 34 | Van Dam–Hayden, PRA 67, 060302 (2003), https://arxiv.org/pdf/quant-ph/0201041, Eqs. (4)–(7). Pure catalysts; approximate global production; Schmidt-rank/fidelity and reduced-state entropy-continuity bounds. | Its reduced-state full trace error is not the complete bipartite-memory return error. No mixed \(E_R\) optimization or negative logarithmic correction is supplied there. |
| 36 | Leung–Wang, PRA 90, 042331 (2014), https://arxiv.org/pdf/1311.6842, Sections 1–2 and 4–5. Pure universal families, local isometric permutation protocols, global fidelity; also pure-state entanglement costs and a target-specific sine ladder in Eq. (9). | The sine-ladder construction is prior art and must be attributed. The compared operation permits approximate output and does not optimize over mixed normal catalysts under the R1 contract. |
| 37 | Cleve–Liu–Paulsen, JMP 58, 012204 (2017), https://arxiv.org/pdf/1606.05061, Section 2, Theorem 2.1. Perfect pure-vector embezzlement is impossible under tensor-product local unitaries, including local ancillary registers; a different commuting-operator model permits it. | An inherited exact-embezzlement obstruction and important algebraic scope boundary. It is not the finite-error mixed-catalyst cost expansion. |

These actual references are not thermal-cost papers; Ng et al.'s thermal catalysis paper is reference **35**. None of the inspected statements supplies the sharp law being consolidated. This finding does not establish novelty.

Access note: publisher HTML sometimes redirected to an inaccessible identity endpoint. Public primary PDFs and arXiv versions supplied the relevant statements; no authentication or access restriction was bypassed. The arXiv version date of the second paper is recorded because it is later than the May 2026 publication.
