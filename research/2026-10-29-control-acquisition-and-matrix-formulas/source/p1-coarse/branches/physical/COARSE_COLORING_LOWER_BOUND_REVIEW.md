# Independent check: a four-action hidden-coloring query lower bound

28 October 2026. The constant-alphabet strengthening is valid under the
observation and preparation contract stated below. It uses four actions,
a known strict norm cap, and separating words of length at most H=3d+2.
Its clean conclusion is

\[
\boxed{\mathbb E_0N\ge\frac{2^d-1}{6}},\qquad d\ge2,
\]

for a learner producing a reusable predictor with simultaneous absolute error
at most 1/16 even just for words of length at most H, with unconditional
probability at least 2/3 on every source. Here N counts preparations whose ensuing episode executes
at least one K. The expectation is under the baseline source. Total
preparations and primitive applications are both at least N.

The stopping, adaptive-query and shared-secret mixture arguments have no
remaining hole under this contract. A sharper coupling, proved separately
below, improves 1/6 to 1/3; the displayed conservative bound does not depend
on that sharpening. This is a scoped verification, not a priority claim.

## Exact source and access contract

Let G=F_2^d, M=2^d-1 and c=1-1/(20d). Each preparation independently draws
a hidden coloring F and a uniform x in G. The source parameter is either
the baseline or one fixed secret w!=0, retained across all preparations.

- Baseline: the colors F(y) are independent fair bits over y in G.
- Secret w: the colors are independent fair bits on the two-point cosets
  {y,y+w}, and constant inside each coset.

The controls are X:x->x+e_0, the two coordinate reflections
R_0:e_j->e_{-j}, R_1:e_j->e_{1-j}, with indices modulo d, and K. Reflections
act on the position x only, leaving F unchanged. Thus they remain valid
permutations within each secret's state space; no invariance of w under
reflection is required. Control K kills the live state when F(x)=0 and
otherwise leaves it unchanged. Every primitive additionally survives an
independent Bernoulli(c) kill. All three motion controls are involutions.
The resulting live kernels are symmetric nonnegative substochastic operators:
a motion control is c times an involutive permutation, and K is c times a
diagonal zero-one projection.
Every primitive has norm at most c<1. The preparation distribution is uniform
on the corresponding finite hidden state space and is common to all actions.

The learner may observe alive/dead after every operation, use private
randomness, choose subsequent actions and stopping times adaptively, and
request a fresh preparation even while alive. A fresh preparation draws a new
independent coloring. Death ends that prepared trajectory. No additional
cloning, checkpoint restoration, resurrection, or preparation operation that
retains a chosen F is available. Ordinary control sequences, including inverse
motions returning to a previously visited x, are fully allowed; their repeated
color queries are already covered by the proof. Hidden colors and positions
are never reported. An episode is the part of one
preparation used before death, voluntary reset, or stopping.

If identical hidden dimension and identical uniform preparation across
hypotheses are desired, use the common space
Omega={H:G->{0,1}} times G, with uniform H,x in every source. Baseline K reads
H(x), while secret K_w reads H(rep_w(x)), where rep_w(x)=min{x,x+w} in any
fixed ordering. Unused H bits are ignored. This realizes exactly the stated
observable laws with the same flips, the same preparation vector and the
same finite hidden space in every hypothesis. All hypotheses and their
formulae may be disclosed to the learner; only which hypothesis is executed
remains unknown. The lower bound grants unit-cost preparation and does not
assert that preparing a huge random coloring is physically efficient.

## Exact translation synthesis with three motion controls

Let R=R_1 R_0, meaning chronological execution R_0 then R_1. It sends e_j to
e_{j+1}. Given w, write b_t=w_{-t mod d}, t=0,...,d-1. In cycle t execute
X if b_t=1, followed by R_0 and R_1. The complete map is

\[
x\longmapsto R^d x+\sum_{t=0}^{d-1}b_tR^{d-t}e_0
=x+\sum_{t=0}^{d-1}w_{-t}e_{-t}=x+w.
\]

The motion word T_w therefore has length 2d+|w|<=3d. This order of the
coefficient schedule is material: the sequence of optional flips uses bits
w_0,w_{d-1},w_{d-2},...,w_1. At d=2 one reflection is the identity; the
four-label alphabet is still valid. All three motions are nontrivial for d>=3.

## Identical individual actions; separated mixed words

For any repeated motion control, survival after n operations is c^n. For n>=1 repeated
K operations it is c^n/2. These are identical for every source and every n.
Consequently the complete individual-action absorption-time laws agree.

For each nonzero w, let W_w be K, then T_w, then K. Its length is
ell_w=2d+|w|+2<=3d+2=H. Its survival is

\[
p_0(W_w)=\frac{c^{\ell_w}}4,\qquad
p_w(W_w)=\frac{c^{\ell_w}}2.
\]

The baseline queries two independent bits, whereas secret w queries the same
coset bit twice. Bernoulli's inequality gives

\[
c^{\ell_w}\ge c^{3d+2}\ge1-\frac{3d+2}{20d}\ge\frac45,
\]

so the survival gap is at least 1/5. The gap exceeds twice 1/16.

## Why adaptivity does not evade the per-episode bound

Work entirely under the baseline law. In an episode, record the actual
distinct positions at which K is executed. Under arbitrary reflection and
flip controls these positions are affine functions of the hidden initial x,
and their differences can depend on x. The analysis may use these hidden
positions; the learner is not granted them. Let D be their number, including
a terminal query that kills the trajectory.

Condition on the complete history just before the first K in that episode.
Earlier motion controls and their independent survival outcomes have disclosed
no colors. One may additionally condition on the hidden initial position,
which is independent of the fresh baseline coloring. Every newly queried
color is still an independent fair bit, including
when its location is chosen adaptively from previous observations. Reaching
r distinct K queries requires the preceding r-1 distinct queried colors all
to be one. Voluntary stopping and independent killing can only decrease this
probability. Thus

\[
\mathbb P_0(D\ge r\mid\text{history before first K})\le2^{-(r-1)},
\quad r\ge1,
\]

and consequently

\[
\mathbb E_0\binom D2\le
\sum_{r=2}^{\infty}(r-1)2^{-(r-1)}=2,
\qquad
\mathbb E_0(D-1)\le1.
\]

The conditioning is before the episode's first K, not on its eventual outcome
or on the final total N. Applying conditional expectation separately at each
such episode entrance, then Tonelli's theorem, yields

\[
\mathbb E_0\sum_{e:\,D_e\ge1}\binom{D_e}{2}
\le2\mathbb E_0N.
\]

This is valid for adaptive numbers of episodes and arbitrary stopping. It
does not assume independence between N and the episode lengths. If the
expectation is infinite, the asserted lower bound is already true.

## Baseline versus a fixed-secret mixture

Draw W uniformly from G\{0}, independently of the entire baseline experiment,
including its hidden starting positions and colorings.
Importantly, draw it once, not anew at each preparation. Let R be the union,
over baseline episodes, of all nonzero differences between distinct K-queried
positions in the same episode. Differences between different preparations
convey no color relation and are excluded.

Couple a secret-W experiment to this baseline using the same controller
randomness and independent-killing coins. In each fresh secret episode,
assign a fair bit to each coset when it is first queried. Until two queried
positions differ by W, all queried cosets are distinct, so their colors can
be coupled exactly to the baseline's fresh independent colors. The complete
observed transcripts, next actions, resets and stopping decisions therefore
agree until such a collision. After the first possible disagreement, continue
the secret experiment with its correct conditional law.

Since R is generated by the baseline independently of W,

\[
\begin{aligned}
\operatorname{TV}(\mathcal L_0,\overline{\mathcal L})
&\le\mathbb P(W\in R)
=\frac{\mathbb E_0|R|}{M}\\
&\le\frac1M\mathbb E_0\sum_e\binom{D_e}{2}
\le\frac{2\mathbb E_0N}{M}.
\end{aligned}
\]

Here the laws include the complete adaptive transcript and predictor output,
and the bar denotes the mixture over a single persistent W. The argument
uses no independence between different collision events. Repeated differences
only make the union smaller.

## Reduction from all-word accuracy to testing

After acquisition, evaluate the reusable predictor on the finite family of
M words W_w, using no further source calls. Test for the secret mixture when
there exists w such that

\[
\widehat p(W_w)>\frac38c^{\ell_w}.
\]

On a baseline run with simultaneous error <=1/16, this test returns baseline.
On a secret-w run with the same accuracy, W_w makes it return secret. The
midpoint margin is c^(ell_w)/8>=1/10>1/16. With success probability at least
2/3 in every source, the test's secret probability is at most 1/3 under the
baseline and at least 2/3 under the mixture. Hence TV>=1/3. Combining this
with the coupling inequality proves E_0 N>=M/6. The argument already applies
to simultaneous accuracy over the finite family of horizon-H witness words.

The offline test may inspect exponentially many words. That is legitimate
for a lower bound on source access: it adds no source applications. The
claim requires an actual reusable predictor with unconditional success. A
false-emission guarantee permitting perpetual abstention is insufficient.

## Optional sharpening: only a terminal zero can disagree

The preceding coupling may continue even after paired positions are queried,
provided the baseline returns one: all earlier queried colors in a still-live
episode are one, so the secret's already assigned coset bit is also one.

For each baseline episode ending in a color-zero K query at z, with the
independent-killing coin successful, define

\[
C_e=\{z-y:y\text{ was a distinct earlier K-queried position}\}.
\]

Put C_e empty for voluntary stops and independent deaths. The terminal zero
cannot be at a previously queried position. Therefore |C_e|=D_e-1 when it
is nonempty, and otherwise |C_e|=0.

Assign secret coset colors lazily from the first baseline color queried in
each coset. A new coset's first query uses a fresh fair baseline bit and thus
has the correct secret law. Repeated coset queries returning one are
consistent. At a terminal baseline zero, the secret agrees unless z's partner
was queried earlier; precisely this exception is W in C_e. With common
independent-killing coins, all observed behavior agrees until that exception.
Afterward the two experiments may be completed separately with their proper
conditional laws. This proves a valid coupling, including after benign
collisions, and gives

\[
\operatorname{TV}(\mathcal L_0,\overline{\mathcal L})
\le\frac{\mathbb E_0|\bigcup_e C_e|}{M}
\le\frac{\mathbb E_0N}{M}.
\]

The same conditional-entrance argument justifies the last inequality via
E(D_e-1)<=1. Thus under the stated contract the stronger conclusion is
E_0N>=M/3. The M/6 result remains a valid simpler presentation.

## Exact checks and practical scope

`coarse_coloring_lower_bound_checks.py` ran successfully using exact rational
arithmetic. It checks every synthesized translation at every initial position
for d=2,3,4,5. It exhaustively enumerates colorings and starting positions for
d=2,3 to check the witness laws, individual-action formulas, and a general
word with K queries between reflections. It also
computes full absorption-time transcript laws for Gray-code query paths and
checks the coupling bounds. A two-episode policy stops early after survival
and selects a second word from the observed first death time; its mixture is
formed with the same secret in both episodes.

| Check | d=2 | d=3 |
|---|---:|---:|
| Minimum mixed-word gap | 0.2041629509 | 0.2078013585 |
| Gray-path transcript TV | 0.1348955895 | 0.0618078964 |
| Terminal-zero coupling upper bound | 0.1683954907 | 0.0954309685 |
| E(D-1) | 0.6932826101 | 0.7741326444 |
| E binomial(D,2) | 1.0362799428 | 1.3586781958 |

For the adaptive d=2 policy, E_0N is approximately 1.7906021016, transcript TV
is approximately 0.1103062431 and the terminal-zero union bound is approximately
0.1249220697.
The complete fractions are saved in `coarse_coloring_lower_bound_checks.json`.
These checks corroborate finite instances; the proof handles arbitrary policies.

There are exactly four action labels, the known inverse norm gap is 20d,
and H=3d+2. At fixed accuracy and confidence, the lower bound is exponential
in d, hence exponential in this horizon even with a fixed alphabet. It excludes
a uniform polynomial source-query bound in horizon and inverse gap independent
of hidden-state complexity for this coarse interface. It does not exclude
polynomial dependence on the enormous hidden-state dimension, or a better
bound under stronger observation/preparation access. Bit flips have negative
eigenvalues, so the demonstrated class is symmetric nonnegative kernels, not
a class additionally restricted to positive-semidefinite primitives. The gap
is strict and known but decreases with d; no exponential lower bound with a
dimension-independent gap and fixed accuracy is asserted.

## Complete upper bound when the family is known

There is a straightforward matching exponential-scale acquisition procedure.
For each nonzero z, run W_z on

\[
n=\left\lceil50\log\frac{2M}{\delta}\right\rceil
\]

fresh preparations and estimate its survival probability. Compare its empirical
mean with 3c^(ell_z)/8. A source with secret w has the high mean c^(ell_z)/2
exactly when z=w; every other z has mean c^(ell_z)/4, as does the baseline.
The threshold margin is at least 1/10. Hoeffding's inequality and a union
bound give probability at most 2M exp(-n/50)<=delta of any wrong decision.
On the complementary event, the vector of decisions identifies baseline or
the unique secret exactly.

This uses M n fresh preparations, at most H M n primitive applications, and
at most 2 M n observations if each trial is read at the first K and its end.
An observed first-K death permits immediate stopping. Otherwise every scheduled
intermediate motion is charged even if an unobserved independent death already
occurred. The bound does not rely on free stopping at hidden deaths.

After identification, any fixed word omega of length h has the exact response

\[
p_w(\omega)=c^h\,2^{-d}\sum_{x\in G}2^{-r_w(x,\omega)},
\]

where r_w counts distinct secret-w cosets at K-queried positions along the
deterministic controlled path from x. In the baseline r_0 counts distinct
sites instead. Reflections make these counts depend on x in general; replacing
the average by a single starting position would be incorrect. For W_z the
path difference is the translation z, so the earlier spike formula is exact.

The formula gives a reusable predictor with no new source trials on the
identification event, but its arithmetic cost may itself be exponential in d.
The acquisition lower and upper bounds agree in exponential scale, up to
polynomial and logarithmic factors. Neither the constants, the d factor, nor
the log M factor are claimed optimal. The full family is known to both the
upper-bound learner and the learner in the lower bound.
