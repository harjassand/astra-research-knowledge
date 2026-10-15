# Source receipts

Accessed 2026-10-15. Local PDF checksums use SHA-256. Page numbers below refer to the published pagination when available; for scanned/local PDFs, PDF page numbers are also noted as needed.

## Decisive scalar sources

- **Diamond–Essén (1978), “Functions with non-negative convolutions.”** *J. Math. Anal. Appl.* 63(2), 463–489. DOI: [10.1016/0022-247X(78)90091-4](https://doi.org/10.1016/0022-247X(78)90091-4). [ScienceDirect record](https://www.sciencedirect.com/science/article/pii/0022247X78900914) labels the work “Open archive.” Full theorem text was not acquired: ScienceDirect article/PDF requests were intercepted by a Cloudflare 403/challenge and Elsevier's unkeyed TDM endpoint returned minimized metadata. The title, authors, pages, and DOI are verified against Crossref and the publisher record. The description of its subject as existence of a nonnegative Borel convolution measure comes from Katkova–Vishnyakova (2001), p. 2, not from a direct reading of Diamond–Essén.

- **Katkova–Vishnyakova (2001), “A Continual Analogue of a Theorem by M. Fekete and G. Pólya.”** *Positivity* 5, 1–11. DOI: [10.1023/A:1009847605313](https://doi.org/10.1023/A:1009847605313). Full author-uploaded manuscript inspected at [ResearchGate](https://www.researchgate.net/publication/235701306_A_Continual_Analogue_of_a_Theorem_by_M_Fekete_and_G_Polya); publisher record at [Springer](https://link.springer.com/article/10.1023/A:1009847605313). Exact hypotheses/conclusion: Theorem 1 (pp. 1–2 in manuscript) and compact-support Theorem 2 (p. 2); interpretation as convolution and comparison with Diamond–Essén (pp. 2–3); fixed-multiplier counterexample (Remark, pp. 10–11). No local copy or checksum was retained.

## Local primary-source PDFs

| Source | Exact location used | Local file | SHA-256 |
|---|---|---|---|
| Handelman (1986), “Deciding eventual positivity of polynomials,” *ETDS* 6, 57–79. [DOI](https://doi.org/10.1017/S0143385700003291), [Cambridge PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B83D582D94552C65E8B09AD6A68D84C2/S0143385700003291a.pdf/deciding_eventual_positivity_of_polynomials.pdf) | Easier multiplier criterion, § I, pp. 57–58; eventual-power Theorems A/B, pp. 60–61 and § IV. | `sources/handelman_1986_eventual_positivity.pdf` | `21822de2b89736cf9f3dc8550c4fbe3968f06d00b4158984c0eb01be4dd202e3` |
| Handelman (1988), “Representing polynomials by positive linear functions on compact convex polyhedra,” *Pacific J. Math.* 132, 35–62. [DOI](https://doi.org/10.2140/pjm.1988.132.35), [MSP PDF](https://msp.org/pjm/1988/132-1/pjm-v132-n1-p04-s.pdf) | Theorem 1.3, printed p. 39 (local PDF p. 6). | `sources/handelman_1988_compact_polyhedra.pdf` | `f7959c8ca0f6bf9d7483d7cc47e69c422560092e1e23f8b7b505ee94b03dcd09` |
| Lê–Dư (2018), “Handelman’s Positivstellensatz for polynomial matrices positive definite on polyhedra,” *Positivity* 22, 449–460. [DOI](https://doi.org/10.1007/s11117-017-0520-y), [arXiv](https://arxiv.org/abs/1603.07611) | Theorems 2.1 and 3.1, local PDF pp. 4, 7–8. | `sources/le_du_2018_matrix_handelman.pdf` | `24298bff9f51554bf6a63ef32b7522a7a21fa8892011a6286a55bbd8e4397946` |
| Cimprič–Zalar (2013), “Moment problems for operator polynomials,” *J. Math. Anal. Appl.* 401, 307–316. [DOI](https://doi.org/10.1016/j.jmaa.2012.12.027), [arXiv](https://arxiv.org/abs/1209.1492) | Abstract; Haviland extension, Theorem 3, local PDF pp. 1, 5; compact operator extension, Theorem 5, p. 10; infinite-dimensional operator discussion and complete-positivity condition, pp. 7–10. | `sources/cimpric_zalar_2013_operator_moments.pdf` | `8a898140f29b7f73fcc348e8fa81d133db7c17219442f2d47cb54d4df66b74ac` |

The saved copies were checked as readable PDFs with `pypdf`; the recorded hashes allow later integrity checking. These receipts document source access and identify where claims were checked; they do not substitute for reading the inaccessible Diamond–Essén theorem.
