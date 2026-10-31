# Prior matching: established ingredients, derived compositions, open consequence

31 October 2026. Author research note, not a historical-novelty review. The
frozen earlier checkpoint is unchanged. This continuation must be compared
against ordinary methods **plus any certificate derived here**; their ability
to adopt it neither erases its contribution nor establishes historical novelty.

## Confirmed primary-source matches

* **Mixed-precision subspace/projection template:** Xu, Zhang, Chen, Saad and
  Xi, *Mixed Precision Orthogonalization-Free Projection Methods for Eigenvalue
  and Singular Value Problems*, arXiv:2505.00281v1. Sections 2–3 and the
  implementation discussion use low-precision bases with more accurate small
  projected problems. This rules out presenting that numerical template as
  newly discovered. Their eigen/SVD setting is not an automatic theorem for
  unknown stochastic generators and every later noncommuting word.
  https://arxiv.org/html/2505.00281v1

* **Matrix concentration:** Tropp, *User-Friendly Tail Bounds for Sums of
  Random Matrices*, Theorem 1.6 supplies the rectangular Bernstein inequality
  used verbatim as an established theorem. The present notes derive the
  access-specific moments, protocol conditioning and leverage accounting;
  these are applications, not a new concentration inequality.
  https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf

* **Two-rate statistical orthogonality:** Mackey, Syrgkanis and Zadik (2018),
  *Orthogonal Machine Learning: Power and Limitations*, Sections 1–2 and
  Theorem 1, makes the first-order-insensitive nuisance/fourth-root-rate
  principle explicit. Foster and Syrgkanis' COLT 2019 primary abstract states
  a nonasymptotic two-stage sample-splitting result with second-order nuisance
  error for excess risk. Thus coarse nuisance accuracy plus a fine independent
  target stage is emphatically not new as a general learning principle.
  https://proceedings.mlr.press/v80/mackey18a/mackey18a.pdf
  https://proceedings.mlr.press/v99/foster19c.html

* **Sequential doubly robust estimation:** Kallus and Uehara (2020), *Double
  Reinforcement Learning for Efficient Off-Policy Evaluation in Markov Decision
  Processes*, introduction and problem definition, studies a given target
  policy using cross-fold value/density-ratio estimation and fourth-root
  nuisance rates. This is an essential comparator, not a claim that pointwise
  OPE automatically provides our finite all-word operator certificate. Full
  theorem-by-theorem comparison of its policy-class extensions remains open.
  https://jmlr.org/papers/volume21/19-827/19-827.pdf

* **Learning Markov features and partitions:** Zhang and Wang, *Spectral State
  Compression of Markov Processes*, IEEE TIT 66(5), 3202–3231 (2020), analyzes
  spectral estimation, leading feature spaces, aggregation and lumpable
  partitions from observed trajectories. The introduction, structural results
  and theorem sections have been inspected. The current greedy row clustering
  is an ordinary proposal mechanism, not a new discovery algorithm. Its weak
  guarantees must not be contrasted against only naive caching.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7971158/

* **Positive aggregation and transient error:** Michel and Siegle (2024),
  *Markov Chain Aggregation with Error Bounds on Transient Distributions*,
  Sections 2–3 explicitly forms stochastic aggregate/disaggregate operators,
  allows uniform within-block weights, checks compatible initial distributions
  and derives a retained residual bound for transient distribution error.
  Equations (4)–(6) are first-order full-distribution bounds; adding a task-
  dual residual is the older goal-oriented mechanism, not a new aggregation
  representation. The later journal page returned 403; no retry or bypass was
  attempted. The accessible author PDF is the source used here.
  https://www.unibw.de/technische-informatik/mitarbeiter/professoren/siegle/publikationen/asmta_2024.pdf

* **Active nonintrusive MOR validation:** Zhuang et al. (2023), *Active-learning-
  based nonintrusive model order reduction*, Sections 3.1–3.2 learns a POD
  solution region and gives a distributional one-step validation criterion.
  That is relevant acquisition/validation prior, but the inspected criterion
  is not a worst-case every-word guarantee. No assertion about every possible
  extension of this method is made.
  https://doi.org/10.1017/dce.2022.39

The earlier frozen PRIOR_AND_CONTRIBUTION_MAP.md separately documents the
primal–dual residual product in goal-oriented reduced-basis theory. It remains
capital, not something erased by the present change of norms.

Additional unread primary lead: Hendrik Vantilborgh, *Aggregation with an
Error of O(epsilon^2)*, JACM 32(1), 162–190 (1985), DOI
https://doi.org/10.1145/2455.214107 . Its bibliographic existence is confirmed
by other primary papers' references. Both the ACM article page and direct PDF
returned 403 on 31 October 2026; neither was retried or bypassed. The full
theorem is NOT claimed read or matched here. This lead is another reason not
to claim second-order aggregation itself as new.

## What is actually derived and executable here

1. An elementary Schur-complement lemma bounds the excess operator norm caused
   by an acquired nonstationary metric quadratically in its stationary defect,
   conditional on a checked mean-zero gap. It fixes a real obstruction to a
   naive coarse/fine budget, but is not claimed historically new matrix theory.
2. Conditional fresh projected sampling has explicit acquired-leverage and
   incoming-mass sample budgets. Its composition with the uniform scalar
   certificate is checked without giving the learner true matrices or a useful
   basis. Every failed acquisition and finite replay cost is retained.
3. A stronger positive-projection alternative dispenses with global stationary
   geometry on partitionable tasks. Qualitative complement certification,
   fine-enough two-sided cross-block validation and very fine small transition
   estimation have different paid budgets. The stratified validation exploits
   block-averaging of independent non-identical rows, not exact lumpability.
4. The current synthetic kernels have imperfect block invariance and no common
   stationary law. Their long-word outputs do not collapse to one constant.
   These are tests of applicability, not a broad benchmark or a new learner.

The unverified historical question is whether an existing result already
implies this exact reusable, all-word, acquired-geometry/positive-projection,
statistical and bounded-bit composition under the same access language. The
unearned consequence question is whether it survives better selective
sampling, direct/retained query evaluation, variance-adaptive confidence,
compression cost and useful large-scale tasks. A small fixture, even after
all costs are honestly displayed, does not establish a major capability.
