# Prior match, contribution boundary, and failures of the large construction

This is an unreviewed extension of the separately frozen exact/finite-
observation package. Earlier independent receipts do not cover these files.

## What is standard, and what is actually assembled/proved here

* Learning aggregation from transition data is prior art, not our new learner.
  Duan, Ke and Wang, *State Aggregation Learning from Markov Transition Data*
  (NeurIPS 2019), explicitly learns aggregation/disaggregation maps by spectral
  and convex-hull operations. Its primary abstract and problem summary were
  read; this is not a theorem-by-theorem comparison to our interface.
  https://papers.neurips.cc/paper_files/paper/2019/hash/070dbb6024b5ef93784428afc71f2146-Abstract.html
* Collision statistics and sublinear quadratic-functional testing are prior
  art. Diakonikolas, Gouleakis, Peebles and Price, *Collision-based Testers are
  Optimal for Uniformity and Closeness*, arXiv:1611.03579v1, confirms these
  exact methodological antecedents. Only its primary abstract has yet been
  checked here; our Q3/Q4 variance identity is proved directly and tested,
  not attributed as historically new. https://arxiv.org/abs/1611.03579v1
* The variance-aware Bernoulli intervals are directly Maurer--Pontil (2009),
  Theorem 4, whose displayed statement was checked in the primary paper.
  The executable uses an upward dyadic square root and ceil(log2(x))>=ln(x).
  https://arxiv.org/pdf/0907.3740
* Matrix concentration and randomized power-norm estimation are standard.
  Tropp's rectangular matrix Bernstein inequality supplies the spectral
  observation event; the fresh finite-alphabet anti-concentration and
  bounded-grid implementation have ordinary explicit proofs here. Neither
  power iteration nor the concept of a posteriori random norm estimation
  is new. https://arxiv.org/abs/1004.4389
  https://arxiv.org/abs/0909.4061
* Prior goal-oriented residual products, positive Markov aggregation and
  equilibrium second-order aggregation are separately mapped in
  PRIOR_MATCH_AND_SCOPE.md. Vantilborgh's 1985 full theorem remains unread
  because both primary full-text endpoints returned 403; we have not
  retried/bypassed those endpoints. Its existence prevents a first-ever
  quadratic-aggregation claim, but the title alone does not prove exact
  historical equivalence to this finite-observation all-word certificate.

The actual construction here is a mixed positive-retained/L2-discarded
uniform word-error certificate, attached to an ordinary acquired partition,
with acquired column mass, a fresh finite-bit norm check, and direct
quadratic-functional validation of both leakages. No good partition,
stationary law, column-balance constant, useful probe or fine action is
supplied. The observed partition proposal is checked, not guaranteed to be
found on every problem. Its exact prior match remains open. Ordinary methods
using this acquired certificate get its capability; that does not by itself
erase a certificate contribution, nor establish its novelty.

## A substantive testing limitation, not a contradiction of known lower bounds

Our small-leak completeness is in the stronger scaled L2 quantity
v=n||Qp||2², not merely total variation. For a single uniform target block,
take k disjoint pairs and replace their uniform masses 1/n by
(1+c)/n,(1−c)/n. Then

    TV(p,uniform)=kc/n,       v=2kc²/n=2c TV(p,uniform).

Even bounded n*p_max<=1+c and TV<=theta/4 do not imply v<=theta²/16.
For fixed c and small theta, a TV-near distribution can fail our stronger
L2 completeness condition. Thus this is not a generic tolerant-TV tester
with sqrt(n) samples. The primary abstract of Canonne, Jain, Kamath and Li,
*The Price of Tolerance in Distribution Testing*, arXiv:2106.13414v2, explicitly
describes the much larger price of general tolerance. We do not import its
lower bounds beyond that stated setting. https://arxiv.org/abs/2106.13414v2

## Current executable and what it does not establish

The retained 4096-state test learns four balanced blocks. It uses 942,957,056
represented ordinary transition calls, not 942,957,056 individually executed
queries. Synthetic multinomials compress source simulation. The count
algebra, confidence inequalities and common-denominator replay are executed;
physical iid access and trustworthy random-source provenance are premises.
This is not practical deployment or a historical/civilisation-scale result.

The task is fixed source-region initial distribution and fixed target-region
terminal indicator, with arbitrary future words of length at most 24.
Those two task observables reveal two regions, but not the remaining hidden
partition. It is NOT one acquisition valid for arbitrary future observables,
arbitrary horizons, or arbitrary microscopic initial conditions.

The downstream operation evaluates an explicitly supplied list of 50,000
schedules and returns its best. It pays for reading/evaluating that list and
prefix retention. Uniform epsilon prediction yields 2epsilon list-best
regret; it does not solve unrestricted policy search or feedback planning.

The output spread rules out a constant epsilon predictor. However the tested
same-action-count order spread is only .037109375 at epsilon=.02. This does
not yet rule out a separate, cheaply certified action-count approximation.
Noncommuting generators alone are not a sufficient richness demonstration.

A separate stronger fixture changes the hidden routing fraction from .02
to .04, leaving the learner unchanged. It pays 3,298,951,680 represented
calls and obtains error bound .0150513. Two length-24 words with identical
action counts have model spread .09375 and certified true spread at least
.0636474 > 2*.02. Therefore no action-count-only predictor can uniformly
meet epsilon=.02 on that fixture. This is an actual richness falsification,
not a general lower bound on all alternative representations. All 50,000
integer predictions are emitted in a separate streamed TSV artifact.

The strongest implemented improvement is ordinary retention: the outgoing
validation batches already provide iid fine block-action samples. A second
simultaneous confidence event allows reusing them without independence from
the leakage test. This stops one round earlier and avoids all separate fine
sampling, reducing the first 4.315-billion-call schedule to .943 billion.
Both schedules and failed acquisitions remain saved, rather than concealing
the improvement behind a weak baseline.

Other explicit failure regimes: B=Theta(n) for a constant point reset; a
microscopic initial state is not preserved by the balanced projection and
forcing a singleton raises the outgoing kappa bound by 1024 in this fixture;
no complement gap or no task-compatible low-rank partition; fresh probes
replaced by an adaptively orthogonal probe; and non-iid or outcome-stopped
observation batches. The first-action boundary lemma offers an alternative
for some microscopic sources, but is not executed in this fixture.
