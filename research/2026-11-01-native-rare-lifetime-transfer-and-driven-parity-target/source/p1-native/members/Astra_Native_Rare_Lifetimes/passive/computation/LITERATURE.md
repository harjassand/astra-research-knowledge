# Primary comparison record: passive acquisition and model mismatch

Read during the current task; no prior research chats were used. Parent
must open/search each source itself before using child web references in
the final response. No historical-priority conclusion follows from this
selective search. Earlier screened-capacity and lifetime sources are in
research_work/computation/LITERATURE.md.

## Gaitonde, Moitra and Mossel (COLT2026)

Publisher record: https://proceedings.mlr.press/v336/gaitonde26a.html

Author-linked full paper: https://arxiv.org/html/2507.15173v1

Published title: Learning Ising Models from Evolutions. Preprint title:
Better Models and Algorithms for Learning Ising Models from Dynamics.
Read Theorems1.1--1.2 and Section6, especially Algorithm3/Theorem6.5.
They use full unmarked continuous-time trajectories from arbitrary initial
states, estimate local rates, and recover Ising parameters for reversible
single-site dynamics. Their broader regime does not require the strong
mixing assumed in our easier path example. The displayed parameter-learning
runtime has accuracy exponent4, degree factor2^d, and other bounded-width
and nondegeneracy constants. Their theorem does not apply verbatim to
directed two-site cycles. That scope difference is not an impossibility:
ordinary CTMC count/exposure likelihood suffices for our supplied local
architecture and fast-mixing class. References: turn62view0,turn63view0,
turn63view1; publisher turn60view0.

## Pascal Lezaud (2001)

Chernoff and Berry--Esseen inequalities for Markov processes.
ESAIM Probability and Statistics5,183--201; DOI10.1051/ps:2001108.
Primary full text: https://numdam.org/item/PS_2001__5__183_0.pdf

Read Theorem1.1 and Feynman--Kac Lemmas2.1--2.2. The estimates include
nonreversible processes, using the symmetric-part spectral gap and an
initial-density L2 prefactor. This establishes that concentration of local
occupation times is ordinary machinery. Our elementary proof in
PASSIVE_BASELINE.md states its own conservative constants and separates
confidence validity from calendar-time coverage. Reference turn75view1.

## Leonard Gross (1975)

Logarithmic Sobolev Inequalities. American Journal of Mathematics97(4),
1061--1083. DOI https://doi.org/10.2307/2373688 .
Original paper OCR of the JSTOR scan was accessible at
https://studylib.net/doc/27852139/gross-1975 ; the publisher endpoint failed.
This is original-source text on a third-party host, not a secondary account.

Read Theorem3 pp1068--1069 (two-point projection B), equation(2.14), and
the tensorization passage pp1071--1072. It gives q−1=(p−1)e^(2t) for
e^(−tB); setting -H=2c sum_i B_i gives exponent4ct for rate-c bit flips.
The extension to a noncommuting invariant Markov K is the elementary
Trotter argument explicitly preserved in MISMATCH_AUDIT.md. It should be
credited as an application of existing hypercontractivity. References
turn88view1,turn89view2,turn90view0. Gross's Cornell page confirms the
bibliography: https://math.cornell.edu/leonard-gross (turn87search0).

Guionnet--Zegarlinski2002 is an additional primary authored lecture source,
not needed for novelty: https://www.numdam.org/item/SPS_2002__36__1_0.pdf
(turn88view2). Its introductory discussion explicitly connects uniform
ergodicity, L2 ergodicity, and hypercontractivity.

## Thiede, Van Koten and Weare (2015)

Sharp Entrywise Perturbation Bounds for Markov Chains.
SIAM Journal on Matrix Analysis and Applications36(3),917--941.
DOI10.1137/140987900. Full author manuscript:
https://pmc.ncbi.nlm.nih.gov/articles/PMC4610747/

Read Introduction, Theorems2--5, and comparisons in Section6. Their global
relative stationary bound is a sum over edges of transition perturbations
weighted by inverse killed hitting probabilities Q_ij(S). Its generic
evaluation is O(N^3) for N states. Crucially, the introduction explicitly
allows analytical estimates using a simple dominated reference, so this
cost is not an unconditional obstacle for compact chains. Using only
Q_ij(S)>=S_ij gives a pessimistic contribution per global edge for our
cube. Better analytical estimates remain a serious comparator. They also
record a prior all-entry relative bound with exponentN. Neither statement
alone is our stationary-conditional all-target mean theorem. References
turn94view1; turn91search2. Avoid saying all existing perturbation theory
requires trajectories as long as the rare hitting mean.

## Solan and Vieille (2003)

Perturbed Markov Chains. Journal of Applied Probability40(1),107--122.
DOI10.1239/jap/1044476830.
Accessible original preprint: https://arxiv.org/pdf/math/0306248
Author published PDF, indexed but retrieval timed out:
https://www.math.tau.ac.il/~eilons/result14.pdf

Read Section2 and Section4.3. Their stationary theorem in the arXiv
version (Theorem2) uses L=sum_(k=1)^(N−1) binom(N,k)k^N and gives
relative error<=18 beta L with beta<2^(−N) and another epsilon condition.
The all-set duration comparison (Theorem5) has factor2N^2. Its K_C is
the mean length of a visit initialized at stationary entrance flux, equal
pi(C)/flux(C,Cc); it is not the stationary-conditional residual waiting
time studied here. The paper allows substantial changes to sufficiently
infrequent transitions and has a statistical motivation, so it is a real
conceptual predecessor. Its stated bounds do not furnish our compact
dimension-polynomial tight certificate; analytical refinements are not
excluded. References turn103view1,turn104view0,turn104view1. The arXiv PDF
has a later automatic compilation date, while the version is2003v1.

## Jeffrey J. Hunter (2002; later published developments)

Generalized Inverses, Stationary Distributions and Mean First Passage
Times with applications to Perturbed Markov Chains.
Research Letters in Information and Mathematical Sciences3,99--116.
Primary repository full text:
https://mro.massey.ac.nz/bitstreams/4314b4da-0ed4-4e0c-8129-f8fcdb0849ea/download

Read the abstract, introductory construction, and generalized-inverse
setup; did not fully audit every later updating formula. The paper gives
mean-passage and stationary updates through successive small transition
perturbations. It is a primary warning that exact hitting-time sensitivity
is established territory. No compact analytical all-target certificate
matching our constants was located in the read sections. Reference
turn96view2; repository record turn94view2. The2005 Linear Algebra and
Applications article has DOI-linked record
https://www.sciencedirect.com/science/article/pii/S0024379505003903
(abstract only,turn91search0).

## Other relevant primary results, limited retrieval

Mitrophanov2004, The spectral gap and perturbation bounds for reversible
continuous-time Markov chains: https://doi.org/10.1239/jap/1101840568 .
Abstract read; it covers stationary and transient sensitivity. This source
does not justify a claim that ordinary bounds necessarily grow with time.

Huang--Mao2018, Variational principles of hitting times for non-reversible
Markov chains: https://doi.org/10.1016/j.jmaa.2018.08.036 . Abstract and
publisher details read; full proof not retrieved. It gives nonreversible
hitting variational formulas and comparisons, so our use of adjoint
equilibria and energy comparison belongs to an established framework.
The author lecture
https://math0.bnu.edu.cn/probab/Workshop2018/Lectures/July%2016-afternoon/6-Huang.pdf
is search-indexed with the reciprocal mean variational formula on slide17
(turn120search26); direct retrieval returned483. The related authored
preprint arXiv:2011.04334 by Huang--Kim--Mao--Wang2020 extends exit-time
variational principles to semi-Dirichlet forms; only indexed excerpts were
read in this subtask. These are comparison leads, not fully audited
sources for a claim about their sharpest constants.

## Birrell, Katsoulakis and Rey-Bellet (2021)

Quantification of model uncertainty on path-space via goal-oriented relative
entropy. ESAIM M2AN55,131--169; DOI10.1051/m2an/2020070.
https://www.numdam.org/item/10.1051/m2an/2020070.pdf

Read Theorem3.6, Remark3.8, Corollaries4.3--4.5, and AppendixD.2. This is
direct existing model-form-uncertainty machinery for hitting means and
CDFs. The task-derived coarse-cube instantiation and exact failure threshold
are preserved in STOPPED_ENTROPY_FAILURE.md and entropy_comparator.py.
Its failure is specific to Corollary4.5 and Corollary4.3 Eq(4.3) with the
stopped entropy compensator, including after irrelevant-coordinate
reduction. Smaller-sigma-algebra comparison is Corollary4.3 Eq(4.2) and
data processing; Remark3.8 discusses constant versus random entropy
budgets. Other full-path variants using independently earned finite
stopped-KL or mean bounds may remain finite but weak. The example does not
refute the whole goal-sigma-algebra framework; earning a sharper
observable-level divergence could improve the result.
References turn106view0,turn108view0,turn108view1,turn108view2.

## Mitrophanov (2005): mixing-envelope perturbation

Sensitivity and convergence of uniformly ergodic Markov chains.
Journal of Applied Probability42(4),1003--1014.
DOI https://doi.org/10.1239/jap/1134587812 . Full publisher PDF:
https://www.cambridge.org/core/services/aop-cambridge-core/content/view/26A9854BCB8D103B3A63A9B272616EC0/S0021900200001066a.pdf/sensitivity-and-convergence-of-uniformly-ergodic-markov-chains.pdf

Read Theorem3.1 and Corollary3.1. The paper sums the contraction envelope
min(1,C rho^k) to obtain uniform-in-time and invariant-distribution
perturbation bounds. This is explicit prior credit for the integrated
mixing-envelope strategy. Its norm is total variation of signed measures;
our relative-density L-infinity Poisson bootstrap is written separately
with all norm conventions and constants. References turn115view0,
turn118view2. The paper cites Mitrophanov2003, Stability and exponential
convergence of continuous-time Markov chains, J.Appl.Prob40,970--979,
DOI10.1239/jap/1067436094, for the continuous-time precursor (abstract
read at turn119search0; full proof not yet retrieved).

## Coolen-Schrijner and van Doorn (2001 memorandum; 2002 journal)

The deviation matrix of a continuous-time Markov chain.
Probability in the Engineering and Informational Sciences16(3),351--366.
DOI10.1017/S0269964802163066. Author-institution memorandum record:
https://research.utwente.nl/en/publications/the-deviation-matrix-of-a-continuous-time-markov-chain/

The primary abstract explicitly defines the deviation matrix as the time
integral of P(t)-Pi and discusses existence and representations. The
linked memorandum PDF returned403; no unexamined detailed theorem is
attributed to it. This is supporting terminology and historical credit,
not a substitute for the finite-state Poisson identity proved in
MISMATCH_AUDIT.md. Reference turn115view1.

## Duncan, Lelievre and Pavliotis (2016)

Variance Reduction Using Nonreversible Langevin Samplers.
Journal of Statistical Physics163,457--491.
DOI10.1007/s10955-016-1491-2. Full author PDF:
https://www.ma.imperial.ac.uk/~pavl/nonreversible.pdf

Read Lemma3 Eq(29), its proof, and Eq(31). The symmetric part of an
inverse with a skew perturbation is expressed through a symmetric
positive correction, equivalently through an inverse of I minus the
square of a skew operator. The resulting quadratic form is no larger
than the reversible inverse. This is the direct established algebraic
mechanism behind the reversible-reference improvement in Section7 of
MISMATCH_AUDIT.md. Our killed finite-matrix calculation makes target and
weight conventions explicit; it is not a new general inverse principle.
References turn118view0,turn119view0,turn119view2.

## Lin, Liu and Smith (2025)

Perturbation analysis of Markov chain Monte Carlo for graphical models.
Journal of Applied Probability62(3),950--971.
DOI10.1017/jpr.2024.102. Full publisher article:
https://www.cambridge.org/core/journals/journal-of-applied-probability/article/perturbation-analysis-of-markov-chain-monte-carlo-for-graphical-models/346CD64D0C320E924DF9806F3F22537A

Read the introduction, assumptions around Theorem2, and the theorem.
It improves permissible kernel perturbations for structured graphical
models, under a common factorization of both stationary measures and
associated Gibbs samplers satisfying additional local assumptions. The
output distance is Hellinger distance. It is an important compact-model
comparator, but does not apply verbatim to our actual source with unknown
possibly non-Gibbs stationary law; small global Hellinger distance alone
also does not certify relative rare-target waiting times. No optimality
claim is made against refinements of this work. References turn117view2,
turn118view1.

## Defensible interpretation

The passive observation primitive, occupation concentration, cube
hypercontractivity, and ordinary variational/hitting machinery are existing
ingredients. The task-developed contribution under review is a concrete
certificate linking simultaneous local rate uncertainty to relative rare
means and deadline risks without requiring the actual source to have the
tractable reference's stationary representation. This record establishes
neither a universal failure of prior methods nor a publication-level
novelty claim. The complete explicit theorem, its conditions, and executable
checks remain useful regardless of historical priority.

The independent-flip cylinder subcase has since been solved by a stronger
ordinary comparison: see CYLINDER_COUPLING_BASELINE.md. Biased independent
processes bracket every actual single-bit source inside the rate box by
an explicit graphical coupling, even without actual attractiveness. The
exact m+1-state birth-death calculation gives the rare mean and full
deadline brackets. It is therefore a successful comparator, not evidence
for a new capability of the more general certificate. Relabeling coordinates
for each singleton further proves the all-state density bound
(1-eta)^n<=pi/pi0<=(1+eta)^n. Coupled with ordinary symmetric/skew inverse
comparison, this supplies all-target rare means for the pure independent-
flip reference, including nonmonotone targets. General stochastic
comparison is classical; Massey1987, DOI10.1287/moor.12.2.350, is a primary
historical reference (publisher abstract read, turn125search0). The note
proves the specific coupling directly instead of relying on unexamined
theorem conditions.
