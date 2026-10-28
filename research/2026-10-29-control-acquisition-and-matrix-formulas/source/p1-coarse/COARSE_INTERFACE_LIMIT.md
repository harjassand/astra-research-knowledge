# A generic cost obstruction for reusable coarse composition models

29 October 2026, Brisbane. The coarse cover succeeds on the executed source.
The next attack asks whether a better representation could make its all-word
acquisition uniformly polynomial. The answer is no over the declared coarse
access class, even with a known strict global gap. A hidden-coloring source
gives an exponential lower bound with only four operations. The information
argument uses ordinary coupling and testing, not a new general inequality.

## Statement

For every d>=2 there is a family of symmetric, nonnegative substochastic
sources with four primitive controls, the same uniform preparation in every
hypothesis, exact live/absorbed reports, and known source norm cap

    c=1-1/(20d)<1.

All individual-action lifetime laws are identical. Suppose an acquisition
procedure returns a reusable predictor whose simultaneous absolute error is
<=1/16 for every word of length <=3d+2, with unconditional probability >=2/3
on every source in the family. It may adapt controls, stopping and preparation
requests to its entire observed history. Then, under the baseline source,

    expected informative preparations >=(2^d-1)/6,
    expected primitive applications >=(2^d-1)/6.

Thus the obstruction is exponential in the relevant program horizon even
with a fixed alphabet and inverse gap O(d). This is not a claim against a
polynomial dependence on hidden-state complexity: the hidden source is large.
It rules out removing that complexity without replacing it by another
meaningful structural resource or stronger access.

A procedure allowed to abstain forever is not covered by the success premise.
A false-emission guarantee alone does not imply this lower bound on time to
emit, because it does not require an emission.

## Source and common preparation

Let G=F_2^d. A hidden state consists of a Boolean table H:G->{0,1} and a
position x in G. Prepare H and x uniformly and independently at each fresh
preparation. The same hidden state space and uniform preparation are used in
all hypotheses. H is retained during a trajectory but is never observed.

The source is either baseline or has a fixed unknown nonzero secret w. The
baseline loss test K reads H(x): color zero kills, color one preserves the
state. In source w, K instead reads H(rep_w(x)), where rep_w(x) is a fixed
representative of {x,x+w}. Thus it queries an independent fair color for each
two-point coset, shared by its two positions. Unused H bits are harmless.

The other controls are permutations of the position:

- X flips coordinate zero.
- R0 reflects coordinate indices j to -j modulo d.
- R1 reflects coordinate indices j to 1-j modulo d.

Each is an involution, so its live kernel is symmetric. K is diagonal. Every
primitive additionally kills independently with probability 1-c. Hence all
live kernels are symmetric, nonnegative and have norm <=c. Uniform preparation
is a common reversible reference law, with A_i v<=c v. These kernels are not
all positive semidefinite: an involutive permutation can have negative
eigenvalues. The theorem is for symmetric nonnegative kernels.

Only live/dead reports leave the source. A fresh preparation draws a fresh
H. There is no cloning, restoration of a dead sample, rewind, or ability to
retain a selected H across a fresh preparation. Even granting preparations
as unit operations gives the lower bound; efficient physical construction
of exponentially large Boolean tables is not asserted.

## Constant-length-alphabet mixed witnesses

The product R=R1 R0 rotates coordinate indices by one. For j=0,...,d-1,
optionally apply X according to bit w_(-j mod d), then apply R0 and R1.
After d cycles the rotation is identity and the resulting translation is
x->x+w. Its length is 2d+|w|<=3d.

Let W_w be K, this translation, then K. Its length ell_w<=3d+2 and survival
is exactly

    baseline: c^ell_w/4,
    secret w: c^ell_w/2.

Bernoulli's inequality gives c^ell_w>=4/5, so the response gap is at least
1/5, exceeding twice 1/16. Repeating any permutation control has survival
c^h; repeating K has survival c^h/2 for h>=1. Therefore every single-action
lifetime distribution is identical in all hypotheses, even with exact
infinite marginal data.

## Adaptive coarse transcripts cannot find the secret cheaply

Analyze the baseline. An episode begins at a fresh preparation and ends at
death, voluntary replacement or stopping. Let D be the number of distinct
positions where K is queried, including a final color-zero query. Before a
new distinct query, its color is still an independent fair bit, regardless
of past adaptive controls. Reaching r such positions requires the preceding
r-1 new colors to be one. Independent killing or stopping only shortens this:

    Pr(D>=r | history before that episode's first K)<=2^(-(r-1)),
    E[binom(D,2) | that history]<=2.

These are conditional entrance bounds. They remain valid for a random
number N of episodes executing K; Tonelli and conditional expectation give
E sum_e binom(D_e,2)<=2 E N. No independence from N is assumed.

Now choose one secret W uniformly from the M=2^d-1 nonzero possibilities,
independently of the entire baseline experiment. Keep it fixed across every
preparation. In each episode, collect the nonzero differences of distinct
K-queried positions. Their union R contains at most sum_e binom(D_e,2)
candidates. Positions may depend on hidden x and adaptive controls; the
whole baseline trajectory is still independent of W.

Couple the secret experiment using identical controls, external randomness
and independent-killing coins. Until queried positions differ by W, all
queried secret cosets are distinct, so their fresh fair colors can be coupled
to baseline colors. Full observations, choices and stopping decisions agree.
Consequently

    TV(baseline transcript, uniform-secret mixture transcript)
      <=Pr(W in R)<=2 E_0 N/M.                         (1)

For a uniformly accurate reusable predictor, inspect its answers on the M
finite witnesses W_w without further source calls. Declare a secret when
some prediction exceeds 3c^ell_w/8. On its success event this distinguishes
baseline from every secret, since the midpoint margin is >=1/10>1/16.
Success >=2/3 forces transcript TV>=1/3. Equation (1) gives E_0 N>=M/6.
Every informative episode spends at least one preparation and one source
application. This proves both advertised resource bounds.

The offline reduction may enumerate exponentially many words. That is valid
for a lower bound on source acquisition. It does not supply an efficient
program-search algorithm. A sharper terminal-zero coupling can improve the
constant, but the conservative statement above does not need that refinement.

## A strong equally informed upper route

Grant both learner and lower-bound argument knowledge of this whole family,
including c. For every nonzero z, test W_z. Its survival is c^ell_z/4 except
when z is the secret, when it is c^ell_z/2. Using

    n=ceil(50 log(2M/delta))

fresh trials per z, Hoeffding's inequality and a union bound resolve all M
midpoint tests jointly at failure <=delta. This costs M n preparations and
at most (3d+2)M n source applications. Reading after the first K allows an
early stop on observed death; otherwise charge every intervening control,
with a second report after the final K. Reports are at most 2M n. Replacing
this scan by standard best-arm techniques may improve logarithmic factors;
no optimal logarithmic factor is claimed.

Once baseline or w is known, the entire response law is specified. For a
general word, its queried positions are affine functions of initial x; the
number of distinct queried cosets can depend on x. The exact response is

    c^h * 2^(-d) sum_x 2^(-r_w(x,word)),

where baseline uses distinct sites and secret w uses distinct two-point
cosets. This may require exponential arithmetic. The witness translation
words avoid that extra average because their two endpoints differ by z
for every x. The upper matches the exponential acquisition scale up to
polynomial and logarithmic factors; it is not a free exact predictor.

## Consequence for the research agenda

A single specified word can always be tested directly at ordinary Bernoulli
cost. The exponential requirement arises from reusable simultaneous coverage
of all possible consequential words. It is a limitation of the coarse access
contract, not evidence that the particular prefix-tree algorithm is optimal.

The positive target is therefore a certificate whose resource bound depends
on a genuinely small observable context family. Finite covers supply one
such conditional resource; physical boundary recognition supplies another.
The next construction must discover or acquire that simplifying structure,
not merely assume a small fitted model has closed.

Independent ordinary proofs and exact small cases are retained in
branches/physical/COARSE_COLORING_LOWER_BOUND_REVIEW.md and its verifier.
That note distinguishes the original d+1-control construction from the
four-control strengthening and records their precise constants and scopes.
