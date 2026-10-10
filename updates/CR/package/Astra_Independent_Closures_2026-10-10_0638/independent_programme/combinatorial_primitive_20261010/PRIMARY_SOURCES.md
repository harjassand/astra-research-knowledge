# Selective primary-literature check

Checked on 2026-10-10. These sources establish context; none is being used as a substitute for the proofs in `RESULT.md`.

- Alweiss, Lovett, Wu, Zhang, *Improved bounds for the sunflower lemma*, arXiv:1908.08483, version 3 (2021), Annals-related revision. https://arxiv.org/abs/1908.08483 . The authors establish a logarithmic-base bound and explain that their robust strengthening has a matching lower-order barrier. This motivated working directly with the exact sunflower relation rather than trying to improve a robust random-set sampling lemma to a constant spread parameter.
- Anup Rao, *The story of sunflowers*, Journal of the London Mathematical Society 113 (2026), e70380, first published 2026-01-07. https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70380 . The survey describes the general `O(r log w)^w` scale and the missing logarithm relative to the conjecture.
- Ryan Alweiss, *Set System Blowups*, Combinatorica (2025). https://link.springer.com/article/10.1007/s00493-025-00163-1 . This is a stronger structural direction with quantitative dependence on the sunflower bound. It is not a proof of alphabet-independent compression.
- Gábor Hegedűs, *About sunflowers*, arXiv:1804.10050. https://arxiv.org/abs/1804.10050 . This explicitly discusses the all-equal/all-distinct code formulation and bounds retaining alphabet dependence. The code representation itself is standard, not an originality claim.
- Barnabás Janzer, Zhihan Jin, Benny Sudakov, Kewen Wu, *Sunflowers and Ramsey problems for restricted intersections*. Author-hosted manuscript: https://people.math.ethz.ch/~sudakovb/sunflowers-ramsey-restricted-intersections.pdf . Their color-certificate and delta-system methods have quantitative dependence on rank; one cannot silently treat a rank-dependent constant as absolute. The manuscript's displayed variant has `(25 * 2^k * k * m)^(-k)` retention, which is not the constant-per-rank target sought here.

## Newer claims separated from established baseline

- Junichiro Fukuyama, *Sunflower Bound with a Sub-Logarithmic Base*, arXiv:2510.19037v2, revised 2025-12-01: https://arxiv.org/abs/2510.19037 . Its abstract claims a `log w / log log w` base. The author subsequently discusses incompleteness/instability in the relevant proof work on his own research blog: https://sites.psu.edu/sunflowerconjecture/ . The present pass did not verify this proof and does not rely on or validate the claimed improvement.
- Ge, Wang, Xu, Zhao, *Bounded VC-dimension implies the Erdős–Rado sunflower conjecture*, arXiv:2609.18995: https://arxiv.org/abs/2609.18995 . Its abstract claims the bounded-VC-dimension case. That is a restricted-family statement and is not the general theorem requested here. Only the abstract was checked in this pass, not the full proof.

This is a selective status check, not a certified exhaustive survey of all submissions through the check date. The general-bound target is used as a research objective; no claim of a solved conjecture or of novelty of our negative constructions is made.
