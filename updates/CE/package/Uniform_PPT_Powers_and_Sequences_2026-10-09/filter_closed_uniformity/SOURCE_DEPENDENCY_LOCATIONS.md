# Exact source locations and dependency statements

9 October 2026. All statements below are paraphrases; formulas use the notation of this proof. Download hashes and pinned versions are in SOURCE_PROVENANCE.json. Full third-party text is excluded from the proof bundle.

1. Sanz, Perez-Garcia, Wolf and Cirac, arXiv:0909.5347v2, PDF page 3, Theorem 1: a primitive channel on M_d with r Kraus operators has full Kraus-span index i(A)<=(d^2-r+1)d^2. PDF page 2, Proposition 3: primitivity and eventual full Kraus rank are equivalent. Section II defines i(A) and states persistence of the full span at later lengths. Choi rank is the dimension of the Kraus span. Therefore q=d^4 is one simultaneous length at which every primitive channel has strictly positive Choi matrix, while every nonprimitive channel fails this test. This is stronger than one-step output positivity and is the precise dependency used.

   https://arxiv.org/pdf/0909.5347v2

2. Carbone and Jencova, arXiv:1905.00857v1, pp. 9-10, Definition 1, Proposition 5 and Corollary 2: an irreducible unital quantum channel with a faithful invariant state has orthogonal cyclic projections whose sum is identity. Applying the source to the TP channel's adjoint yields Phi*(P_j)=P_(j-1). The full proof then derives the Kraus support and direct-sum assertions explicitly. It does not assume that arbitrary invariant corners annihilate all cross-input images.

   https://arxiv.org/pdf/1905.00857v1

3. Hanson, Rouze and Stilck Franca, arXiv:1902.08173v2, PDF page 34, Theorem 3.14: a CP PPT map with positive-definite left and right eigenmatrices at its spectral radius has a finite EB power. PDF page 29, Theorem 3.10 gives the faithful-channel input. The arbitrary-CP theorem avoids confusing a unital adjoint with a bistochastic channel. The source appeared in Annales Henri Poincare 21 (2020), 1517-1571.

   https://arxiv.org/pdf/1902.08173v2
   https://link.springer.com/article/10.1007/s00023-020-00906-4

4. Park, arXiv:2608.13551v2, Theorem 1.1 and Section 1.2: the pointwise conclusion uses a map-dependent exponent. Section 1.2 leaves a channel-independent bound open; Theorem 1.2's constants 3 and 5 require additional DSP hypotheses. This comparison is documented in PRIMARY_PRIORITY_COMPARISON.md; no unrelated claim from Section 5 is needed.

   https://arxiv.org/html/2608.13551v2

5. Compact semialgebraic Lojasiewicz inequality: for nonnegative continuous semialgebraic f,h on compact semialgebraic K with {f=0} contained in {h=0}, there are C,alpha>0 such that h<=C f^alpha. A primary reference for a version with weaker continuity requirements is Ferrarotti, Fortuna and Wilson, Local Approximation of Semialgebraic Sets, Annali della Scuola Normale Superiore di Pisa, series 5, volume 1 (2002), pp. 1-11, Lemma 2.1. The present proof uses only the continuous compact case. Powers-Stormer's square-root inequality is proved directly in the review, while the elementary separable ball and faithful-word bound are proved in the main text.

   https://www.numdam.org/article/ASNSP_2002_5_1_1_1_0.pdf
