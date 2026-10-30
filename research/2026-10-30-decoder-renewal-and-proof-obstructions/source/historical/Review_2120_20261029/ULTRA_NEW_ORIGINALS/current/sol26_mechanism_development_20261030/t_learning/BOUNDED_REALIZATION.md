# Bounded native-state realization and unconditional statistical acquisition

30 October 2026. Complete finite-horizon mathematical construction. This is
NOT a polynomial-time solution to conditional-sample low-logit learning. It
does not require conditional samples at all, but pays exponential deterministic
search. No new source instance, optimizer or scientific benchmark is executed.

## 1. Consequence and honest incumbent

Uniformly acquiring rare logits, common Fisher coordinates, or arbitrary logit
mixtures can cost exponentially many native samples; the separate exact lower
bounds in this directory pay those claims. They do NOT show that the unknown
whole trajectory law itself requires exponentially many observations. Here is
a condition-free construction separating these issues:

* Every bounded, low-logit-rank source has a time-dependent continuous-state
  realization with ALL transition entries and ALL native reachable state
  coordinates in [-1,1]. No singular-value lower bound is needed.
* A uniform trajectory-TV net has polynomial LOG cardinality in horizon,
  alphabet, dimension, log boundedness and log requested accuracy.
* Ordinary minimum-distance selection on unconditional iid trajectories then
  learns a compact teacher-free sequential law from polynomially many samples.
  The fully specified search takes exponential time/space; this is charged.

This is a bounded-realization/finite-class construction, not a claim that a new
practical learner or a new general statistical-learning principle was invented.
Strong ordinary global fitting/finite-class selection gets the whole operation.
The point is the exact conditioning-free normal form and the resulting access
localization. Historical priority is UNKNOWN.

Primary predecessors screened: Golowich--Liu--Shetty2512.09892v1 gives the ISAN
equivalence and the polynomial-time logit-query learner, and explicitly discusses
computational/noisy-parity obstacles for passive samples. Balle--Mohri1610.07883v1
develops statistical generalization for norm-bounded weighted automata, mostly
in a labeled function-learning setting; it is strong precedent for the broad
statistical-versus-algorithmic distinction, not a free density-learning oracle.
Max-volume/barycentric coordinates and finite-candidate minimum-distance
selection are established ordinary methods. We give their needed proofs here.

## 2. Exact source contract

P is a full-support law on [O]^T, O>=2, T>=1. At every cut t=0,...,T-1 let

    R_t(h)[f,y] = ell_(hf)(y),
    ell_h(y) = log p_h(y)-mean_z log p_h(z),

where |h|=t and 0<=|f|<=T-t-1. Assume the full finite matrix of these rows has
rank<=d. Assume GIVEN a warranted rational alpha>=1 giving the GLS bounded-
factor property; in particular every entry obeys |ell_h(y)|<=alpha^2. We only
need that entry bound for the following proof. Put L=ceil(alpha^2)>=1.

The learner gets d,T,O,alpha,epsilon,delta and independent FULL P trajectories.
No conditional P queries, logit/probability VALUE, basis histories, realization
matrices, ground-truth gradients or singular vectors are provided. The rank
and boundedness metadata are not verified by the learner. The ordinary encoded
input lengths, including alpha,epsilon,delta, are charged.

## 3. A max-volume state at every cut

Let r_t be the rank of the row set of R_t. Choose any orthonormal coordinate
system in its r_t-dimensional row span. Among all r_t-tuples of actual rows,
choose a tuple H_t=(h_(t,1),...,h_(t,r_t)) of maximal absolute determinant in
these coordinates. Its determinant is nonzero when r_t>0. Every actual row has
a unique expansion

    R_t(h)=sum_i x_t(h)_i R_t(h_(t,i)).                (1)

Replacing basis row i by R_t(h) multiplies its determinant, in absolute value,
by |x_t(h)_i|. Maximality gives

    ||x_t(h)||_infinity<=1 FOR EVERY native history.   (2)

This holds even when the maximizing volume is arbitrarily small. The proof
uses the unavailable full matrix only to establish existence of a bounded
parameterization; the algorithm below enumerates ALL bounded parameterizations
and does not call a max-volume or exact-rank supplier.

For a token o, the child row R_(t+1)(ho) is the fixed column restriction of
R_t(h) selecting columns (of,y). Apply this LINEAR restriction to (1). Write
the children of the selected basis histories in the next max-volume basis:

    A_(t,o)[:,i]=x_(t+1)(h_(t,i)o).

Then

    x_(t+1)(ho)=A_(t,o) x_t(h),
    |A_(t,o)[j,i]|<=1.                               (3)

For emissions use

    B_t[y,i]=ell_(h_(t,i))(y),  |B_t[y,i]|<=L,
    ell_h=B_t x_t(h).                                (4)

All statements are exact, including the transition relation. Prefix-dependent
normalization of probabilities does not appear: the state rows consist of
mean-centered LOGITS, and prepending o is a linear column restriction on those
rows. This is why a probability-rank surrogate is unnecessary.

Pad each state to d coordinates using zeros. If R_0 is nonzero, its sole row
is its basis and x_0=e_1. If it is zero, all future logits are zero and the
uniform law is represented by zero emissions/transitions, again with x_0=e_1.
Zero-rank cuts are handled by zero states; their restrictions are also zero.
Thus one fixed initial vector e_1 works for the whole parameter class.

There are

    p_A=(T-1) O d^2,  p_B=T O d, p=p_A+p_B           (5)

entries in the padded parameter boxes. No assumption that operator norms of
A_(t,o) are <=1 is made; their infinity norm can be d. Only NATIVE reachable
states have (2). Arbitrary convex/linear state mixtures are not claimed to be
physically preparable. The candidate models below are mathematical predictors.

## 4. A condition-free uniform net, including transient amplification

For epsilon in (0,1/4), choose dyadic grid spacings a=2^-b_A and b=2^-b_B with

    a <= epsilon/[100 T d L (d+1)^(T+1)],
    b <= epsilon/[100 T d].                           (6)

Enumerate every A entry in [-1,1] on the a grid, and every B entry in [-L,L]
on the b grid. The intervals have integer endpoints, so nearest grid points
can remain in the parameter box. Fix initial state e_1 for all candidates.
For the candidate rounding the true bounded realization, let e_t be the
maximum infinity-norm state error over ALL histories of length t. From (2)
and the parameter boxes,

    e_0=0, e_(t+1)<=d e_t+d a,
    e_t<=a d sum_(j=0)^(t-1)d^j <=a(d+1)^(t+1).       (7)

This explicitly pays the possible exponential TRANSIENT magnitude. Its inverse
spacing is exponential in T, but its required BIT precision is only
O(T log(d+1)+log L+log(Td/epsilon)). No good conditioning is being presumed.
Using (4), (6), (7) gives for every possible prefix and next symbol

    |ellhat_h(y)-ell_h(y)|<=d L e_t+d b
                          <epsilon/(50T).            (8)

For any two real logit vectors u,v,

    TV(softmax(u),softmax(v))<=||u-v||_infinity.       (9)

For completeness, along the straight path u+s(v-u), the derivative of its
probabilities is p_y[delta_y-E_p delta]. Half the sum of absolute derivatives
is at most ||delta||_infinity, because the mean absolute deviation of a random
variable in [-c,c] is at most c (or by its variance<=c^2). Integrate to get (9).
Sequential maximal coupling and (8) give a whole-law discrepancy<epsilon/50
for the exact-softmax candidate. This is a UNIFORM all-prefix proof; no transfer
from typical prefixes to counterfactual futures is used.

Let ell_L be the ordinary bit length of L. The total number M of grid models
obeys M<=2^U for

    U=p_A(b_A+3)+p_B(b_B+ell_L+3).                    (10)

The A grid has at most 2^(b_A+1)+1 points and the B grid at most
2L 2^b_B+1. Thus U is polynomial in T,d,O,log alpha,log(1/epsilon) and the
encoded metadata lengths. This is a bound on log M, NOT on the time needed
to visit all M candidates. The exponential search will be retained.

## 5. Literal rational emissions, without a numerical exponential oracle

Replace each candidate softmax by a fixed rational computation. Given its
dyadic state/logits, subtract the exact largest logit, obtaining weights
w_y=exp(-z_y), z_y>=0 rational, and at least one z_y=0. Compute deterministic
rational LOWER bounds l_y<=w_y with w_y-l_y<=zeta, where

    zeta=epsilon/(100 T O),  l_y=1 if z_y=0.

Then sum_y l_y>=1 and define its actual categorical output

    q_h(y)=l_y/(sum_z l_z).                            (11)

This is exactly normalized with nonnegative RATIONAL probabilities. Since
sum(w-l)<=O zeta and sum(w)>=1, elementary normalization gives

    TV(q_h,softmax(ellhat_h))<=O zeta=epsilon/(100T).  (12)

There is a completely finite polynomial-bit lower-exponential evaluator. Let
H=ceil(log2(2/zeta)). If z>=H, return0, since e>2 gives e^-z<=2^-H<=zeta/2.
For 0<z<H form S_n=sum_(j=0)^n z^j/j!, taking n=2m with

    m>=max(2H^2, ceil(log2(4/zeta)),2).

The remaining positive-exponential tail is at most
2 z^(n+1)/(n+1)!: after this term the term ratio is <=1/2. Also
(2m)!>=m^m and H^(2m)/(2m)!<=(H^2/m)^m<=2^-m,
so z^(n+1)/(n+1)!<=2^-m (using H/(2m+1)<=1).
Consequently E_n=2^(1-m) is a rational upper tail bound <=zeta/2, and

    l=1/(S_n+E_n) <= e^-z,
    e^-z-l <= E_n/[S_n(S_n+E_n)]<=zeta/2.             (13)

Every term is rational, with polynomial numerator/denominator bit length in
the rational argument bits and log(1/zeta). n=O(log^2(1/zeta)). The integer
H can be obtained by rational comparisons with powers of2; no real logarithm
is needed to choose it. When z is enormous the threshold comparison exits
before a long exponential series. The z=0 branch is exact and avoids a tie
or floor decision about transcendental values. No native probability VALUE
has been used.

For an arbitrary grid model, even if it is not near P, its state/logits have
polynomial bit length: the state is a product of T dyadic matrices with at
most d^T magnitude and T b_A denominator bits. Equations(11)--(13) therefore
define a valid finite-bit law for EVERY candidate. Its word density is an
exact product of T rational row probabilities, with polynomial bit length.
The representation and each word-density evaluation are polynomial-size/time
in the input dimensions and grid-bit budgets. The predictor may have nonlinear
rounded emission behavior; it is not claimed to retain exact output logit rank.

Combining (8), (9), (12) and sequential coupling, at least one candidate i*
satisfies

    TV(P,P_(i*))<3epsilon/100<epsilon/16.              (14)

The true source is full support, but candidates are permitted to have zeros.
This causes no undefined inference: each candidate state/readout is specified
at EVERY word irrespective of that word's candidate probability.

## 6. A complete unconditional learner and its exponential search bill

Use n iid full P trajectories. For every pair of candidates define the
Yatracos/Scheffe set

    E_ij={x:P_i(x)>P_j(x)},  x in [O]^T.

Comparison here is exact rational arithmetic using Section5. Let Y be ALL
these at most M^2 sets. With e=epsilon/8, Hoeffding/union gives

    sup_(E in Y)|Phat_n(E)-P(E)|<=e                  (15)

with probability>=1-delta when, for example,

    n>=ceil[(32/epsilon^2)(2U+ceil(log2(2/delta)))].   (16)

This is polynomially many UNCONDITIONAL trajectories, nT returned symbols;
there are ZERO conditional or value queries.

For candidate i define d_i=max_(E in Y)|P_i(E)-Phat_n(E)|. Its set probabilities
are computed with finite deterministic work, not supplied as a new oracle.
For each E, enumerate all O^T words. Evaluate P_i(x) exactly, include it if
x in E, and round each included contribution downward to a common denominator
D=2^b_D with D>=16 O^T/epsilon. Summing integers over D gives a set probability
within eta=epsilon/16. This uses b_D=O(T log O+log(1/epsilon)) bits and avoids
unbounded denominator multiplication across the exponentially many words.
The empirical set probability is a rational count/n, evaluated exactly on the
same predicate. Let dhat_i be the maximum score using these approximate set
probabilities; |dhat_i-d_i|<=eta. Select any minimum dhat_i, with a fixed tie rule.

On (15), the candidate i* in (14) has d_(i*)<=e+epsilon/16. If i is selected,
then d_i<=d_(i*)+2eta. For the set E_(i,i*) we have

    TV(P_i,P_(i*))<=d_i+d_(i*)
                   <=2e+epsilon/8+2eta.

Adding (14) yields

    TV(P,P_i)<=3epsilon/16+2e+2eta
               =9epsilon/16<epsilon.                 (17)

Thus the algorithm outputs a compact teacher-free rational sequential model
with TV<=epsilon and confidence>=1-delta. It uses only (16) actual P trajectories.
The central cost is the search, not a suppressed native measurement supplier:
naively at most M^3 O^T times polynomial per-word arithmetic, plus the empirical
predicate evaluations. With (10) this is 2^poly(T,d,O,log alpha,log(1/epsilon)),
not a polynomial-time algorithm. Storing all candidates/scores is likewise
exponential (or can be reduced by repeated enumeration, at increased time).
No benchmark is claimed from writing this complete finite algorithm.

Each final inference step computes (3)'s state update and (11)'s rational
probabilities with polynomial bit work. Exact categorical sampling uses a
uniform integer below the known denominator, implemented by rejection of iid
fair bits with expected polynomial bit cost. A deterministic per-output cap
requires a separately paid per-output approximation allowance. The sampling
source P is never called after compilation.

## 7. Scope of the acquired principle

This construction works for EVERY source satisfying Section2, without a global
probability floor, a K variation promise, temperature control, conditional
P samples, or measurable native logit values. It is not just a finite-parameter
claim with hidden unbounded/ill-conditioned realization coefficients: (2)--(6)
and the exact dyadic grid give the missing uniform bounds and bit budget.
Nor is max-volume basis acquisition granted free: its unavailable basis is
used only in the covering proof, while explicit exhaustive fitting selects
from the entire bounded predictor family using measured trajectory statistics.

The operation does NOT make the unknown low-logit structure computationally
easy to acquire. Ordinary exhaustive density fitting already has precisely
this strength once given the bounded realization/net. The GLS logit-query
result buys polynomial TIME by an actually stronger acquisition service.
Our trace-qualified adapter separately makes that service investigable, but
does not give universal polynomial-budget success. The IBS/Fisher and pooling
barriers cannot be promoted to sample lower bounds for the law: (16) disproves
that promotion at the declared exact-rank/boundedness scope.

The meaningful remaining general question is a computational search/transition-
representation operation that keeps the statistical guarantee while avoiding
the exponentially many nonlinear candidates. No such operation, physical
measurement advantage, universal sample-only polynomial compiler, historical
novelty or civilizational capability is claimed here.

Primary links:

* GLS: https://arxiv.org/html/2512.09892v1
* Balle--Mohri: https://arxiv.org/html/1610.07883v1

The latter's supervised WFA setting is not identified with whole-trajectory
softmax density learning. The elementary finite-class proof above supplies the
specific operation instead of transferring that theorem outside its premises.
