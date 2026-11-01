# Prior matches and what this construction does not claim

This is an unreviewed discovery-to-validation join, not a new clustering method.

- Abid et al., *Contrastive Principal Component Analysis*, Section2, explicitly
  subtract weighted background covariance and use spectral directions to expose
  target structure. Background cancellation and contrastive spectral learning
  are therefore established. Our input is a pair of row-stochastic transition
  experiments rather than two covariance datasets; that distinction alone does
  not establish novelty. [Primary paper](https://arxiv.org/pdf/1709.06716)
- Lei--Zhu (2017), *Generic Sample Splitting for Refined Community Recovery in
  Degree Corrected Stochastic Block Models*, Section3/Algorithm1, turn an
  approximate clustering into exact recovery by fresh community-wise row
  statistics. This directly matches the cleanup principle. Their graph model
  has independent Bernoulli edges; our action-difference/multinomial-row model
  uses different noise accounting, not a new conceptual cleanup operation.
  [Primary paper](https://www3.stat.sinica.edu.tw/sstest/oldpdf/A27n413.pdf)
- Ordinary signed-graph spectral methods, SVD/randomized range methods and
  multi-view clustering get both full source datasets and all retained metadata.
  The dense exact sign filter is a constructive finite-bit backend, NOT a
  favorable timing baseline. A stable conventional SVD should be expected to
  outperform it computationally.

The particular success theorem now under construction joins: an arbitrary
common full-rank transition background; unknown balanced partition/rank; sampled
operator contrast with an ACQUIRED column cap; exact dyadic spectral filtering;
no-oracle coarse clustering; fresh named-row contrast cleanup; and a separate
uniform future-task reuse certificate. No supplied partition/prototypes/
reverse sampler/coupled seeds/optimal planner appear. The underlying separated
contrast class is a theorem hypothesis, not an empirically certified fact or
an assumption that every source satisfies it. Sampling/validation can refuse.

All source-row tags are legitimate metadata and available to competitors,
including tags from preliminary column-cap observations. The particular
sufficient proof uses fresh cleanup after the partition proposal. It does not
claim that an optimally retaining method must discard earlier metadata or buy
all those new samples; alternative valid adaptive/uniform confidence designs
can improve the bill. The current conservative sample totals are NOT lower
bounds and are not executed experiment counts.

The most informative failure is exact: a common background that does not reduce
the recovered partition cancels from both action contrasts yet creates a .405
error in a two-step observable. Hence recovering an action-effect partition
is not learning a dynamically sufficient state representation. Independent
reuse validation is indispensable. Discovering and cheaply validating useful
structure, rather than merely detecting action-dependent variation, remains
the substantive objective.

Matrix concentration uses Tropp's rectangular Bernstein inequality via
self-adjoint dilation, with the source-row variance calculated explicitly:
https://arxiv.org/pdf/1004.4389 . The cubic polar/sign iteration is also ordinary
numerical linear algebra, not an invented algorithm; see Higham--Schreiber,
*Fast Polar Decomposition of an Arbitrary Matrix*, including multiplication-
based iterations and earlier sources:
https://eprints.maths.manchester.ac.uk/340/1/covered/MIMS_ep2006_161.pdf .
The deliberately simple dyadic implementation merely makes a conservative
finite-bit proof executable. An ordinary certified SVD remains a legitimate
and likely superior backend. We will not optimize this dense filter's huge
generic ledger as a scientific destination.
