# Positive boundary events with noncommuting retained dynamics

28 October 2026. This constructs preparation, observation, statistical
acquisition, certificate acceptance and reuse for three observable boundary
states. The source is simulated in software; no apparatus or norm warranty
has been acquired.

## Result and scope

One acquisition of 10,000,000 logical trials per action and initial boundary
produced a three-dimensional predictor. With joint false-premise
probability below 0.001, its original uniform absolute error bound is
0.0602079226 for every finite action word and every boundary-to-boundary
entry. A stronger treatment of the same transition-count uncertainty gives
0.0399340295. Both are proved bounds, not extrapolations from sampled programs.

For transport from boundary 0 to boundary 2, the twenty-step programs
0^10 1^10 and 1^10 0^10 have exact checker probabilities approximately
0.1789166382 and 0.0584503454. The acquired shared-data difference interval
is [0.0664102655, 0.1741518660]. The same data support an ordinary robust
Galerkin calculation with a tighter interval [0.1011906500, 0.1394358478].

The acquisition used 70,353,830 primitive applications, 62,376,821
categorical observations, and 8,801,332 resets with known-boundary reuse.
A fresh direct endpoint experiment settled this one pair using 400,000
primitive applications and 13,708 resets. The reusable route does not win
this finite decision. Its additional capability is one confidence event
covering every future word and all nine boundary entries.

The access is stronger than the predecessor's scalar reset/read port:
three boundary preparations and nonintrusive categorical boundary reports
are additional operations. Source symmetry in a common state metric, a
known contraction cap, and faithful categorical reports are explicit premises.

## 1. Physical and statistical interface

Let A_i be symmetric, entrywise nonnegative, substochastic matrices on an
unknown state space, with a warranted common bound ||A_i||_2≤a<1. The
argument also permits a countable state space when these are bounded
operators on the common counting-measure Hilbert space. No hidden
dimension or exact hidden rank is supplied to the learner.

The observable boundary is B={0,1,2}. The interface prepares any e_j with
j∈B and reports the current boundary ID or a single outside symbol without
changing the process. Missing row probability leads to an absorbing
cemetery state, also reported only as outside. Reports never identify a
hidden or cemetery state.

Trials can use a reset or start from the known current boundary left by a
previous trial. Conditional on the current Markov state, fresh transition
randomness has the required law. This regenerative reuse saves preparation
without selecting favorable trials or changing the trial distribution.

Put V=(e_0,e_1,e_2), P=VV*, Q=I−P. Then G=V*V=I. Define

\[
T_i^\circ=V^*A_iV,\qquad D_i^\circ=QA_iV.
\]

The true boundary restriction T_i^∘ is an unknown matrix, not a single
scalar. Its off-diagonal entries retain transport and noncommutativity.

## 2. A positive event measures each required diagonal form

For k≥0, start at boundary j and apply action i exactly 2k+2 times. Use

\[
E_{i,j,k}=\{X_1\notin B,\ X_{2k+1}\notin B,\ X_{2k+2}=j\}.
\]

The intervening times are unrestricted: boundary visits between the two
designated outside reports are allowed. Symmetry and path expansion give

\[
\Pr(E_{i,j,k})=e_j^*A_iQ A_i^{2k}Q A_i e_j
=[(D_i^\circ)^* A_i^{2k}D_i^\circ]_{jj}.              \tag{1}
\]

This is a positive probability rather than a difference of large noisy
means. Both designated predicates exclude the entire boundary; excluding
only the initial boundary state would compute a different form.

For depth K and M=1/(1−a²), put

\[
P_{i,K}=\sum_{k=0}^{K-1}(D_i^\circ)^*A_i^{2k}D_i^\circ
       +M(D_i^\circ)^*A_i^{2K}D_i^\circ.
\]

The already established finite spectral-tail inequality gives

\[
Q_i^\circ:=(D_i^\circ)^*(I-A_i^2)^{-1}D_i^\circ
\preceq P_{i,K}.                                    \tag{2}
\]

Select k independently with weights 1 for k<K and M for k=K. With Z=K+M,
the mixed event probability is (P_{i,K})_{jj}/Z. For simultaneous upper
confidence endpoints u_ij,

\[
Q_i^\circ\preceq\operatorname{tr}(Q_i^\circ)I
\preceq q_iI,\qquad q_i=Z\sum_{j\in B}u_{ij}.          \tag{3}
\]

The trace bound introduces observable-boundary dimension dependence. No
hidden transition matrix is reconstructed. The first report of every
trial, including immediately rejected trials, also estimates a column of
T_i^∘. Kernel acquisition requires no separate source trials.

## 3. Statistical acquisition and exact acceptance

The run uses K=4, a=99/100, M=10000/199 and Z=10796/199. A uniform integer
on {0,…,10795} selects k=0,1,2,3 with 199 labels each and k=4 with the
remaining 10,000 labels. Maximum trial length is ten primitive applications.

Each action and boundary has N=10,000,000 trials. A diagonal kernel entry
uses its own first-step count. Symmetry permits pooling j→k and k→j
counts for j≠k: the result is binomial with 2N trials and their common
probability. Different inferred quantities need not be independent; a
union bound supplies the simultaneous confidence event.

For a binomial count x of n, write p̂=x/n and use

\[
\Pr_p(X\le nq)\le\exp[-n d(q\|p)]\quad(q<p),\qquad
d(q\|p)=q\log(q/p)+(1-q)\log[(1-q)/(1-p)],
\]

and the analogous upper-tail bound. This follows from Markov's inequality
applied to exp(tX), the binomial moment-generating function
(1−p+p exp t)^n, and minimization over t. It is ordinary Chernoff machinery;
no new concentration principle is claimed. Original primary source:
H. Chernoff, *A Measure of Asymptotic Efficiency for Tests of a Hypothesis
Based on the Sum of Observations*, Annals of Mathematical Statistics 23
(1952), 493–507, doi:10.1214/aoms/1177729330.

Numerical endpoints are accepted only after exact rational lower bounds
prove n d(p̂||p)≥12. For x=0, the upper endpoint 12/n follows directly
from (1−p)^n≤exp(−np); x=n is analogous. Logarithms are bounded by binary
scaling into [1,2] and the convergent series

\[
\log z=2\sum_{m=0}^{L-1}\frac{t^{2m+1}}{2m+1}+\epsilon_L,
\quad t=(z-1)/(z+1),\quad
0\le\epsilon_L\le\frac{2t^{2L+1}}{(2L+1)(1-t^2)}.
\]

Each checkpoint uses twelve unique kernel entries with two tails, six row
masses with two tails, and six event probabilities with one tail: 42
tails. The two predetermined checkpoints N=10 and 20 million have joint
failure at most 84 exp(−12)<0.001. An exact exponential Taylor partial sum
verifies this inequality. Stopping after a valid first-checkpoint order
certificate is covered. The second checkpoint was not needed.

This is a frequentist false-certificate guarantee, not a posterior
probability conditional on the observed counts.

## 4. Proposed-map compiler and bilinear endpoint proof

Let T_i be the symmetric count proposal. Entry intervals give an exact
row-sum bound ||Δ_i||_2≤δ_i, where Δ_i=T_i^∘−T_i. The proposed defect is

\[
D_i=A_iV-VT_i=D_i^\circ+V\Delta_i.
\]

Because ||(I−A_i²)^{-1/2}||≤√M and V is an isometry, the triangle
inequality in that weighted norm proves

\[
D_i^*(I-A_i^2)^{-1}D_i
\preceq(\sqrt{q_i}+\delta_i\sqrt M)^2I=:\widehat q_iI. \tag{4}
\]

The code upper-encloses square roots rationally. It forms R_i=I−T_i*T_i
and accepts θ_i² and ζ_i only after exact checks of

\[
R_i\succ0,\qquad\widehat q_iI\preceq\theta_i^2R_i,
\qquad\delta_iI\preceq\zeta_iR_i.                    \tag{5}
\]

Floating-point generalized eigenvalues only propose these constants;
rational principal minors certify the inequalities.

For chronological w=(i_1,…,i_h), initial boundary j and receiver k, use
α_0=e_j, α_t=T_{i_t}α_{t−1}, β_h=e_k and β_{t−1}=T_{i_t}β_t. The exact
signed correction to the raw prediction is

\[
\sum_t\beta_t^*\Delta_{i_t}\alpha_{t-1}.              \tag{6}
\]

The dissipation theorem applies with distinct primal and dual endpoints:
initial primal error is zero and the terminal dual source is V e_k. Its
Julia-operator proof gives a corrected remainder at most 2 max_i θ_i²,
since both endpoint norms are one. Equation (5) implies

\[
|\beta^*\Delta_i\alpha|
\le\zeta_i\sqrt{\beta^*R_i\beta}\sqrt{\alpha^*R_i\alpha}.
\]

Cauchy–Schwarz across time and the two telescoping energy budgets bound
(6) by max_i ζ_i. Therefore

\[
\boxed{\
|e_k^*A_{i_h}\cdots A_{i_1}e_j
 -e_k^*T_{i_h}\cdots T_{i_1}e_j|
\le2\max_i\theta_i^2+\max_i\zeta_i.
\ }                                                   \tag{7}
\]

The finite confidence event proves (7) simultaneously for every finite
word and all j,k∈B, including future queries chosen after seeing the data.
No union bound over future programs is required.

### Preserve row-mass information

First reports also estimate the total probability of remaining in the
boundary. Let s_j bound the error in row j's sum and r_jk bound the
off-diagonal entry error. Symmetry gives the exact identity

\[
\Delta_i=\operatorname{diag}(\Delta_i\mathbf1)
 -\sum_{j<k}(\Delta_i)_{jk}(e_j-e_k)(e_j-e_k)^*.
\]

Consequently −Π_i≤Δ_i≤Π_i, where

\[
\Pi_i=\operatorname{diag}(s_j)
 +\sum_{j<k}r_{jk}(e_j-e_k)(e_j-e_k)^*.
\]

An exact check Π_i≤ζ_i^str R_i supplies the same correction bound with
ζ_i^str. This separates transition redistribution from loss of boundary
mass using already observed quantities. It improves the executed uniform
bound from 0.0602079226 to 0.0399340295.

For individual program pairs the code also combines their signed
correction coefficients before applying uncertainty. One uncertain kernel
entry is not treated as a fresh error on each appearance. Actual finite-
word computational energy losses replace their upper bound of one. These
are deterministic consequences of the same simultaneous confidence event.

## 5. Stronger equally informed robust Galerkin route

The true T_i^∘ is unknown but lies in the same entry intervals. Its
correction is zero because V*D_i^∘=0. Observed boundary row-mass upper
endpoints, together with symmetry and nonnegativity, give a cap
||T_i^∘||≤ρ_i^∘<1. Thus

\[
Q_i^\circ\preceq q_iI
\preceq\frac{q_i}{1-(\rho_i^\circ)^2}
       [I-(T_i^\circ)^*T_i^\circ].
\]

The energy theorem bounds the error of the true Galerkin product by

\[
\varepsilon_{\mathrm{Gal}}
=2\max_i\frac{q_i}{1-(\rho_i^\circ)^2}.
\]

Nonnegative interval matrices L_i≤T_i^∘≤U_i preserve componentwise order
under composition, giving

\[
e_k^*L_{i_h}\cdots L_{i_1}e_j
\le e_k^*T_{i_h}^\circ\cdots T_{i_1}^\circ e_j
\le e_k^*U_{i_h}\cdots U_{i_1}e_j.
\]

The boundary-only product sums a subset of the full source's nonnegative
paths. Its error therefore has known sign. A source interval is

\[
\left[e_k^*L_w e_j, e_k^*U_w e_j+\varepsilon_{\mathrm{Gal}}\right]
\cap[0,1].                                            \tag{8}
\]

This avoids the model-estimation term in (4). In the run,
ε_Gal=0.01387442542. The same-data comparator resolves tested block-order
routing at lengths 20,30,40,50 and 60; the original shared-correction
interval resolves lengths 20 and 30.

Equation (8) is ordinary robust Galerkin and positive interval computation
using the new acquired source form. It demonstrates that familiar model
reduction can adopt the positive-event operation. It defeats a claim that
this proposed-map implementation is superior to an equally informed route.

## 6. Executed source and noncommuting witness

For g=1/5 define

\[
L_0=0.1I+0.9\operatorname{Lap}(0,1)+0.05\operatorname{Lap}(1,2),
\]

\[
L_1=0.1I+0.9\operatorname{Lap}(1,2)+0.05\operatorname{Lap}(0,2),
\]

with Lap(j,k)=(e_j−e_k)(e_j−e_k)*. True boundary blocks are I−gL_i.
Each boundary j connects symmetrically to hidden state j with probability
1/500. Both hidden diagonal blocks are diag(1/4,1/3,2/5).

The checker matrices are rational, symmetric and nonnegative. Strict
diagonal dominance proves positive definiteness. Their maximum row sum
0.982 verifies the supplied 0.99 cap for this synthetic source. Neither
the matrices nor their six-dimensional size enter inference.

The noncommuting count proposals are

\[
T_0=\begin{pmatrix}
.7998416&.1800265&0\\
.1800265&.7900377&.01003215\\
0&.01003215&.9700497
\end{pmatrix},\quad
T_1=\begin{pmatrix}
.9699428&0&.0100307\\
0&.799825&.180006\\
.0100307&.180006&.7901512
\end{pmatrix}.
\]

Those finite decimals are exact sample proportions. Positive mixed event
counts were [2,1,1] for action 0 and [1,1,1] for action 1.

| Length | Exact routing difference | Shared-correction interval | Same-data Galerkin interval |
| --- | ---: | --- | --- |
| 20 | 0.120466293 | [0.0664103, 0.174152] | [0.101191, 0.139436] |
| 30 | 0.086244032 | [0.0274810, 0.144571] | [0.0654167, 0.106757] |
| 40 | 0.060658342 | [−0.0008714, 0.121740] | [0.0389353, 0.0821105] |
| 50 | 0.042584279 | [−0.0205088, 0.105246] | [0.0204568, 0.0645044] |
| 60 | 0.029889859 | [−0.0340029, 0.0933834] | [0.0077235, 0.0519163] |

Each row reverses two equal-size action blocks for start 0 and receiver 2.
Reciprocity equates a reversed program with the transposed transition, not
these two off-diagonal probabilities. The self-return comparison between
blocks and interleaving is separately retained and also resolved at length 20.

## 7. Complete execution and preparation ledger

These counts describe one acquisition. A deterministic software replay
reproduced every original receipt field while adding a stored final-report
witness for exact reset accounting. It is not a second independent
statistical dataset.

| Resource | Reusable acquisition | Direct experiment for one pair |
| --- | ---: | ---: |
| Logical trials | 60,000,000 | 20,000 |
| Primitive applications | 70,353,830 | 400,000 |
| Categorical boundary observations | 62,376,821 | 20,000 |
| Resets with known-boundary reuse | 8,801,332 | 13,708 |
| Fresh-reset execution upper bound | 60,000,000 | 20,000 |
| Maximum trial length | 10 | 20 |

The compiler also uses one random mixture label per logical trial. Kernel
estimation has no additional source trials. A categorical read has four
possible reports; it is not charged as an unspecified single binary bit.
Symmetry, the norm cap, reset fidelity and the readout contract remain
separate warranted resources.

If the first report is in B, the event is false and the trial stops while
retaining its kernel sample. If the penultimate report is in B, the event
is false and the last transition is saved. All other scheduled steps and
reports are charged. An outside report does not identify absorption. The
simulator's cemetery knowledge saves redundant software random-number
generation, never source operations.

The resulting exact operation ledger is

\[
N+\sum_k n_{\mathrm{first\ out},k}(2k+1)
-n_{\mathrm{penultimate\ in}}.
\]

For observation counts, a k=0 trial reuses its first report as the
penultimate report; other first-outside trials require both a penultimate
and final report unless the penultimate predicate rejects.

For one action/start-boundary group, let c_j count terminal reports equal
to the requested boundary and let l_j indicate that the last report equals
it. The exact reset count is

\[
N-c_j+l_j.
\]

There is one initial reset followed by a reset precisely when the previous
terminal report is not j. Repeated independently initialized groups add
their last-report indicators. All ingredients are stored in the receipts.
Rescheduling to a different currently occupied boundary could reduce
resets further, but it is not implemented or credited here.

Future point predictions use two 3×3 matrices and cost O(h r²) arithmetic
for a length-h word, r=3. Program-specific intervals use finite 3×3
coefficient accumulations or positive interval products. They make no
further source calls. Arithmetic precision, model storage and certificate
evaluation remain computational resources, not physical primitive steps.

## 8. Direct comparator and actual addition

The direct comparator starts at boundary 0 and runs each twenty-step
program on 10,000 logical trials. It observes 1,723 and 599 arrivals at
boundary 2. Its exact KL-Chernoff intervals give the difference interval
[0.0820982914,0.1423427194]. Four confidence tails also put its joint
failure probability below 0.001. Known returns to boundary 0 are reused
for subsequent preparation even though the target receiver is boundary 2.

The reusable acquisition spends about 175.9 times as many primitive
applications on this one pair. Its future certificate can amortize across
a sufficiently large later query family. A break-even calculation would
not be an estimator lower bound: direct sequential or task-adaptive
methods may be stronger than this fixed-sample comparator. The resource
vector must be retained if preparation or readout dominates execution.

Projection, Markov path expansion, contraction dilation and confidence
inversion are established ingredients. The energy and switched-model-
reduction antecedents are documented in `DISSIPATION_WEIGHTED_REVIEW.md`.
Meyer, *Stochastic Complementation, Uncoupling Markov Chains, and the Theory
of Nearly Reducible Systems*, SIAM Review 31 (1989),
doi:10.1137/1031050, is a primary antecedent for eliminating hidden Markov
excursions. Only its primary abstract/introduction was retrieved for this
continuation; no exact equivalence of its theorems is asserted.

The addition established here is the complete positive-event acquisition
of defect information through accessible boundary predicates, shared
kernel estimation, and a reusable noncommuting composition certificate.
It is not hidden-system identification, a new concentration theorem, or an
unconditional speedup. The same operation supplies familiar robust
Galerkin machinery, which is stronger in this executed comparison.

Rare events are measured through an assumed faithful categorical
interface. This does not acquire a perfect detector from the original
noisy scalar instrument. Preparation or report errors would need their
own warranted bounds and propagation. The symmetry and source-norm
warranties also remain additional source information; boundary readings
alone do not establish them.

## 9. Independent verification and reproducible artifacts

The simulator uses integer transition probabilities and a fixed declared
seed. Source matrices are confined to simulation and later checks. The
inference function receives only categorical receipts, depth, and the
stated norm cap.

An independent replay, without regenerating trajectories, checked 42
inference confidence endpoints and four direct endpoints using a separate
40-term rational logarithm enclosure. It also checked matrix domination,
the row-mass uncertainty form, 30 positive-path identities, ten bilinear
programs, the robust Galerkin intervals, and the exact reset, operation
and observation ledgers. Its scope and result are preserved alongside
the dynamic branch review.

- `multiboundary_positive_events.py`: integer trajectory simulation,
  inference, exact statistical and matrix acceptance, source checks,
  program comparisons, and direct comparator.
- `MULTIBOUNDARY_RAW_RECEIPTS.json`: categorical acquisition checkpoint.
- `MULTIBOUNDARY_POSITIVE_EVENTS_RESULTS.json`: complete rational
  certificate, receipts, source checks, comparisons and costs.
- `../dynamics/MULTIBOUNDARY_ORDER_RESULTS.json`: independent rational
  order witnesses.
- `../dynamics/replay_multiboundary_review.py` and
  `../dynamics/MULTIBOUNDARY_COMPILER_REVIEW_RESULTS.json`: independent
  receipt replay, without new stochastic experiments.

Default execution uses ten million trials per action/boundary. It would
use the predetermined twenty-million checkpoint only if the primary
shared-data routing certificate did not resolve order. The recorded run
stopped at ten million.
