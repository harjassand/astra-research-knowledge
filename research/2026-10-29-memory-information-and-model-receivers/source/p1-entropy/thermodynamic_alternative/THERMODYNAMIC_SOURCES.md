# Primary comparison and Astra source scope

29 October 2026, Brisbane. Targeted retrieval supports opportunity selection;
this is not an exhaustive priority review. No biological procedure or native
physical operation was constructed. The task is abstract stochastic dynamics.

## Primary literature actually read

1. Dominic J. Skinner and Joern Dunkel, *Estimating Entropy Production from
   Waiting Time Distributions*, Physical Review Letters 127, 198101 (2021),
   DOI 10.1103/PhysRevLett.127.198101.
   Author PDF: https://math.mit.edu/~dunkel/Papers/2021SkDu_PRL.pdf
   Web source turn479view2. Read pages 1-4 as parsed, especially equations
   (2)-(7), formulation of minimization over hidden models with the same
   waiting-time distributions or moments, and scalar variance/entropy curve.
   Their broad program already asks the thermodynamic cost of hidden models
   consistent with observed waiting-time moments. This must be credited as a
   close antecedent. A new scalar variance-to-entropy proposal alone would
   not justify choosing a new foundational direction.

2. Jann van der Meer, Benjamin Ertel and Udo Seifert, *Thermodynamic inference
   in partially accessible Markov networks: A unifying perspective from
   transition-based waiting time distributions*, Physical Review X 12,
   031025 (2022), arXiv:2203.12020.
   https://arxiv.org/pdf/2203.12020 ; DOI 10.1103/PhysRevX.12.031025.
   Web source turn481view1. Read introduction, setup and early definitions
   (pages 1-3). Their transition-resolved waiting-time estimator and emphasis
   on the correct physical reversal directly warn against naively reversing
   a boundary-held semi-Markov record. The current proof avoids that issue
   by defining a microscopic excursion intensity measure without initial
   boundary holds, then applying the actual microscopic path reversal.
   Later proofs were not audited in full; no theorem is imported without
   the self-contained path calculation supplied in the new note.

3. Benjamin Ertel, Jann van der Meer and Udo Seifert, *Operationally Accessible
   Uncertainty Relations for Thermodynamically Consistent Semi-Markov
   Processes*, Physical Review E 105, 044113 (2022), arXiv:2111.13113.
   https://arxiv.org/pdf/2111.13113 ; DOI 10.1103/PhysRevE.105.044113.
   Web sources turn479view3 and turn481view2. Read abstract and pages 1-3:
   general semi-Markov versus underlying-Markov TUR distinction, direction-
   time independence, path weights, and initial-age treatment. Full proof
   of their TUR not read, and the new bounds do not depend on importing it.

4. Martinez et al., *Inferring broken detailed balance in the absence of
   observable currents*, Nature Communications 10, 3542 (2019),
   https://doi.org/10.1038/s41467-019-11051-w . Search returned the paper's
   endpoint-conditioned waiting-time claim, but direct Nature retrieval
   redirected to an inaccessible sign-in service and PMC returned a
   reCAPTCHA page. Full text was NOT read. This is a search lead rather
   than a proof premise. Do not represent the blocked retrieval as success.

## Astra corpus

Searched the current Astra Research plugin for entropy production, clocks,
memory and residence information. Current corpus version returned was
5788b3479627421d3a67e1e6fced19f66323e94e01ccdaf4bf094a14547aa8b9,
revision ad7ff1b9d15a774d4b4d8362314c7070cac030e5.

Fetched the complete current capsule for
N185-hidden-metastable-EP-obstruction, content version
49ae42620a150e2435a1d8df07c25a87d58272abdcc846b356c85ca0ac06c320,
and its governing proof excerpt (extracted lines 35-158) with source text
SHA256 fe1694476ca32b651c056ffd2633fb0ec4fb6c07c7315bd2ece6cd61b4661d44.
Both responses were single pages with next_id absent. Exact source:
https://github.com/harjassand/astra-research-knowledge/blob/ad7ff1b9d15a774d4b4d8362314c7070cac030e5/web/pages/d-d8dac5da22a5dead.html

The proof reads as a hidden-metastability limitation on uniformly honest
entropy inference from finite stationary trajectories over an extension-
closed model class. It explicitly distinguishes independent stationary
starts, supplied mixing, interventions and nonstationary access. It
reinforces why the present exact-record inequalities do not themselves
provide acquired statistical certificates. The new constructions are
proved directly and do not require re-auditing this prior theorem.
N186 appeared as a linked confidence-sequence repair, but its current
correction-bearing capsule and full proof were not fetched; its result
is NOT used as a premise.

## Strong equally informed alternative and proposed addition

### Additional primary comparison for the CP extension

5. Pietro Caputo, Zongchen Chen, Yuzhou Gu and Yury Polyanskiy,
   *Entropy Contractions in Markov Chains: Half-Step, Full-Step and
   Continuous-Time* (2024 author preprint, arXiv:2409.07689).
   https://people.lids.mit.edu/yp/homepage/data/2024_sdpi_mlsi.pdf
   Web sources turn493view0 and turn494view0. Read introduction and Section
   2.3 through Lemmas 2.7-2.9, especially the proof on page 11 establishing
   that a nonnegative PSD reversible kernel need not factor as KK*, via
   classical complete positivity in dimensions at least five. Thus the
   CP/nonnegative-Gram obstruction for reversible two-stage kernels is an
   established antecedent, not a new matrix notion introduced by Astra.
   Their entropy-contraction results concern mixing, not the stationary
   thermodynamic entropy production minimized in the present construction.

6. Max Pfeffer and Jose Alejandro Samper, *The Cone of 5x5 Completely
   Positive Matrices*, Discrete & Computational Geometry 71, 442-466
   (2024), DOI 10.1007/s00454-023-00620-y.
   https://link.springer.com/article/10.1007/s00454-023-00620-y
   Web sources turn493view1 and turn494view1. Read definition of CP and
   copositive dual cones, the n<=4 versus n>=5 distinction, and Section
   2.2 through the Horn-zero characterization (Theorems 2.2-2.3). The
   Horn matrix and separation from doubly nonnegative matrices are classical.
   We supply an elementary C5 copositivity proof and exact rational example,
   rather than importing the paper's later algebraic boundary calculations.
   The paper's broad complexity description is not imported as a complexity
   theorem for our calibrated network-completion problem.

Search also found *When the gravity path integral describes a statistical
average*, arXiv:2609.16113. Only its official abstract was read. It is a
different use of positivity/ensemble constraints and supplies no premise
for the present finite-CTMC result. Search results about completely positive
QUANTUM MAPS are a distinct meaning of the term and were not used as CP
matrix-factorization antecedents.

An observer given the same exact mean record can already apply ordinary
Schur solves for all declared mean queries. A thermodynamic observer with
full endpoint/time distributions can apply established path-KL or waiting-
time inference. Neither becomes harder because a positive representative
has many states. Hidden-model entropy minimization is also established.

The proposed new scope is narrower and concrete: an all-hidden-dimensions
closed-form entropy minimum for one FIXED calibrated oriented mean record
as native clock budgets vary, plus a general state-independent lower bound
in return budget, clock ceiling and residence moments. The uniformization
equality removes arbitrary hidden topology, after which a binary Jeffreys
inequality solves the optimization. These ingredients are classical; the
specific calibrated-record resource frontier needs a further priority
comparison before any historical originality claim.

The five-state invisible-cycle family also makes a useful limit precise:
the minimal compatible thermodynamic implementation is not the original
source's entropy. Identical complete boundary event-time laws and fixed
finite clock ceilings leave its entropy unbounded because hidden affinity
is unconstrained. No additional baseline sampling fixes that identification
problem. The purpose is to guide which intervention-coupled record is
needed, not declare a ceiling on discovery.
