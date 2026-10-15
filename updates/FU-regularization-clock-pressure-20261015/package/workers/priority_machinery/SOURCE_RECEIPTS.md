# Source receipts and actual read scope

Date: 2026-10-15. Hashes below are SHA-256 of saved bytes. Actual theorem read ranges are in `READ_RANGES.json`; acquisition URLs, status, MIME and times are in `ACQUISITION_RECEIPTS_01.json` through `_10.json`. Original supplied input and repository pins are in `PIN_RECEIPT.json`.

| Source | Primary acquisition URL | Saved bytes / hash | Read scope |
|---|---|---|---|
| Mattner1999 | [primary full text](https://ems.press/content/serial-article-files/25848?nt=1) | 235057 / `7889f23e486e94c9144e7e1ec6da75df7c83272680284129ca36073d1648b190` | PDF15–17, printed615–617; visually read |
| Katkova–Vishnyakova2001 | [primary full text](https://ekhnuir.karazin.ua/bitstreams/41e252c6-eba5-435f-bbbb-66a8582ace7e/download) | 252576 / `f24e4260a54627f5ad68e0bfdba4c13bdf82e2d327453222a8cede43999b8925` | PDF1–4,10–11; theorem page visually checked |
| Pomatto–Strack–Tamuz2019 | [primary full text](https://arxiv.org/pdf/1807.06927) | 293604 / `f7b5af4ecc6354bd392b08d889a0580b471b763172a36eadcbb2127e3c7c7555` | PDF15–17,21–23; exact signed-measure proof |
| Schwonnek–Werner | [primary full text](https://arxiv.org/pdf/1802.08343v1) | 6292703 / `42d8490086845273eeb5aae83d1339a5f524e7bbbd808029da78130b71460cfa` | PDF1–3; support proof; interior-date caveat |
| Sabbagh et al.2025 | [primary full text](https://arxiv.org/pdf/2505.00245) | 358824 / `75c18e120b7704099fdb357daf8f0251a50272a6db15d320115e0be5d47d4e40` | PDF1–2, visually checked |
| Luef–Skrettingland2017 | [primary full text](https://arxiv.org/pdf/1705.03253) | 394999 / `6866f13b53f8c0a530282384ea625714b93c56849df95a065cb255f5cf4b4ceb` | PDF9–12; representation, convolutions, normalization |
| Borwein–Vanderwerff2001 | [primary full text](https://journalofconvexanalysis.com/articles/jca08030/jca08030.pdf?v=2) | 198429 / `01abaac72095b9aa8630d84ccc9639eb6060affe37f8968151fcdf1fedb1b910` | PDF9–10, Section4 theorem and proof |
| Vervaat1972 | [primary full text](https://ir.cwi.nl/pub/19565/19565A.pdf) | 13646749 / `ce030b5e2331116d9cb5575300aae06942c335cd0dea3aa350712f0066f427dd` | PDF96–102; original scanned pages visually read |
| Iksanov–Iksanov2026 | [primary full text](https://arxiv.org/pdf/2604.14396v2) | 358147 / `d3000a925681f0bc3b253d3af3ee2ffa8348601981c3c41eabe5516d7c7d4022` | PDF1–5,21–23; comparison and route to Vervaat |

The PR94 full proof pin is `df8e6dac844f1832e79cea6cd40d0915307b12bb`; `sources/pr94_cone_proof.md` is the immutable acquired copy. It already states the Banach-cone theorem and arbitrary unital C*-algebra consequence. The parent-coordinated extension proof hashes and original paths are in `COORDINATED_SOURCE_RECEIPTS.json`.

OpenAI/math was read at `1581d4cbdd69a0faf34b2089614fe2a814316a6a`, selective structural Crouzeix statements and positive-density proof. The source is [pinned main.tex](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-complete-Crouzeix-theorem-September-23-2026/build/main.tex). No Lean target or constant-two proof was independently verified.

Missing original fulltexts remain gates: Diamond–Essen1978, Anderson1969/1970, Ruzsa1983, Kamynin–Ostrovskii1982 and Werner1984. Metadata, abstract, access response or secondary citation files do not close them. The apparent Kamynin English `.pdf` response is HTML. Hensley1986 PDF was blocked, but the precise original generalized-Dickman theorem was obtained directly from Vervaat1972. See `FAILURES_AND_LIMITS.md`.
