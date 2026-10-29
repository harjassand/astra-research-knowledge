# Independent review: positive fragments and reflected histories

29 October 2026. Scope: sections 1, 2, and 4 of root's
`POSITIVE_FRAGMENTS_AND_HISTORY.md`, with a short algebra check of section 3.
The exact reviewed text and its hash are preserved separately as
`ROOT_POSITIVE_HISTORY_REVIEWED.md` and in `POSITIVE_HISTORY_REVIEW_SCOPE.json`.
This review does not establish a converse for a whole observed process.

## Finding

The reflected-history entropy theorem is correct under the stated
independent-half observation contract. Its midpoint factorization needs an
explicit unnormalized interpretation for the killed process. A shared random
midpoint readout needs a slightly enlarged midpoint variable. Arbitrary
reversal-invariant correlated readout noise is insufficient.

The CP deficit dual and nonlinear refinement are also correct. The nonlinear
derivation should use the symmetrized Jeffreys density on an ordered endpoint
bin, or combine the bin with its reflected partner. An ordered off-diagonal
endpoint bin is not itself reversal invariant.

The classical nonnegative midpoint factorization has a direct primary
antecedent. Consequently the prospective scientific addition should be
attached to the geometric path comparison, entropy bounds, and acquired
certification, not to the bare history Gram representation.

## 1. A complete finite-history proof

Let Q be a finite stationary CTMC generator with stationary distribution pi.
Restrict to its positive stationary support if necessary. All microscopic
states are even under the declared physical reversal. The window is the fixed
interval [-L,L], with T=2L. Let P be its stationary path law and Theta literal
time reversal. Put P^R=Theta_*P. The reversed generator has

    q^R_xy = pi_y q_yx / pi_x  (x != y),
    q^R_xx = q_xx.

Let K be the geometric killed generator with off-diagonal entries
sqrt(q_xy q^R_xy) and diagonal q_xx. Stationarity and Cauchy--Schwarz imply
K1<=0. Detailed balance holds with pi. On microscopic paths the finite measure
G with initial measure pi and killed generator K has density sqrt(p p^R).

Take the same nonnegative normalized half-path label kernels kappa_a on the
two halves, each viewed *outward from the midpoint*. Thus the right half is
u -> X_u and the left is u -> X_-u for 0<=u<=L. The kernels include only
independent half-specific randomization, unless a shared midpoint variable is
conditioned on as described below. The observation convention must make full
physical reversal swap the label pair. Then

    C_ab = integral kappa_a(left) kappa_b(right) dP,
    C_sym,ab = integral kappa_a(left) kappa_b(right) (p+p^R)/2,
    B_ab = integral kappa_a(left) kappa_b(right) sqrt(p p^R).

For the killed process started from x, define v_a(x) as the *unnormalized*
weight of a surviving half-path assigned label a. Detailed balance permits
the left half to be oriented away from x. Multiplication of the two half
weights therefore gives

    B_ab = sum_x pi_x v_a(x) v_b(x).

This is a finite nonnegative Gram factorization, hence B is CP. For finite
sampled histories it follows by ordinary multiplication of nonnegative
transition kernels and diagonal observation matrices. The full half-path
version follows by the Markov path measure factorization, or a monotone-class
extension of the cylinder formula. No observed Markov property is used.

The distinction between weights and probabilities matters. If
s(x)=sum_a v_a(x), then the midpoint mass of the full killed path measure is
pi_x s(x)^2, not pi_x. Conditional probabilities v_a(x)/s(x) are legitimate
only after replacing the midpoint weights by pi_x s(x)^2. A killed process
does not generally have pi as its stationary distribution.

Pointwise arithmetic-geometric mean gives C_sym-B>=0 entrywise. For a full
normalized partition,

    sum_ab (C_sym,ab-B_ab) = 1-integral sqrt(p p^R) = D.

The root's weaker inequality is safe. A subpartition gives an inequality.
Stationarity and all-even reversal give

    sigma*T = KL(P||P^R)
            = (1/2) integral (p-p^R) log(p/p^R)
            >= 4D.

The last step uses
(a-b)log(a/b)>=4(sqrt(a)-sqrt(b))^2. If reciprocal support fails and entropy
is infinite, the lower bound remains true; finite entropy is the interesting
case. For any symmetric copositive H, h_minus=max(0,-min H_ab), and
gamma=-<H,C_sym>>0,

    gamma <= -<H,C_sym-B> <= h_minus D,
    sigma >= 4 gamma/(T h_minus).

Here h_minus is necessarily positive. The factor T is the whole window
length. Conditional independence of two length-L halves does not divide the
entropy cost by two.

### Midpoint and sensor qualifications

1. A deterministic midpoint observation can appear in both halves. Once x is
   fixed, that shared observation is fixed, so it does not break the product.
   For a finite CTMC a jump exactly at the fixed midpoint has probability
   zero. No new stopping-time midpoint theorem is asserted.

2. If a single memoryless random midpoint emission Y is shared, with kernel
   r(dy|x), condition on (x,Y). Provided the other half noises are independent
   and the same observation rule is used on both sides,

       B_ab = sum_x pi_x integral r(dy|x) v_a(x,y) v_b(x,y).

   For a finite midpoint alphabet this is an explicit nonnegative Gram sum;
   for a general alphabet it lies in the closed finite-dimensional CP cone.
   Independent *replicated* midpoint emissions are a different observation
   experiment and also satisfy the original formula.

3. A correlated instrument with memory crossing the midpoint is not supplied
   by a one-time emission kernel. It must either satisfy the required
   conditional factorization or be included in a warranted reversible
   microscopic instrument model. Reversal covariance alone is insufficient.
   For example, a static hidden state combined with two antithetic fair label
   draws has symmetric joint [[0,1/2],[1/2,0]], which violates the copositive
   quadratic (z0-z1)^2. The antithetic rule is outside the theorem's independent
   half contract; it is not a physical zero-dissipation sensor construction.

4. If observed quantities have a parity transformation, the reflected test
   must include it. The same-index transpose relation needs the test rule to
   commute with the *declared physical* reversal. The theorem does not infer
   the correct microscopic parity from a visible path law.

### Refinement

At a fixed T, a deterministic refinement cannot weaken the family of
certificates. If A groups fine labels into coarse labels, C_coarse=A C_fine A^T.
A coarse copositive H lifts to A^T H A, still copositive. Its pairing is
unchanged and its negative-entry bound does not grow. The same argument works
for independent stochastic coarsening with column-stochastic A. The CP
deficit is also nondecreasing under refinement: a dominated CP fragment for
the fine matrix maps to a dominated CP fragment for the coarse matrix with
the same total deficit. No automatic monotonicity across *different window
lengths*, and no finite-generator full-process converse, follows.

## 2. CP deficit dual

Work in symmetric matrices with the full Frobenius pairing, so off-diagonal
entries are counted twice throughout. For C>=0, maximizing <J,B> subject to
B in CP and C-B>=0 has dual minimizing <C,Y> subject to Y>=0 and Y-J in COP.
The primal is feasible and bounded. Choose Y=tJ with t>1. Both Y and Y-J are
strictly feasible for their respective cones: for nonnegative unit z,
z^T J z=(sum z_i)^2>=1. Dual Slater therefore gives equality of the primal
and dual values even when C has zeros. Substituting H=Y-J proves root's
formula with a supremum. This argument need not promise dual attainment.

Compactness of the dominated CP fragments gives a primal minimizer. The
deficit is zero exactly when C is CP. Finding a good copositive witness or
factorizing a supplied CP matrix remains a separate computational problem.

The five-cycle primal fragment and Horn dual check exactly: the former has
diagonal 1 and neighbor entries 1/2, and the latter pairs to -2/3 with
I+(17/30)Adj(C5).

## 3. Nonlinear Jensen refinement

For s in (0,1], psi(s)=2 sqrt(1-s^2) atanh(sqrt(1-s^2)) is decreasing and
strictly convex, with psi(1)=0 and psi'(1)=-4. The derivatives in root's file
are correct. Its displayed power-series bound proves convexity, and the
tangent at one proves psi(s)>=4(1-s).

For path densities p,q and m=(p+q)/2, put a=sqrt(pq)/m on m>0. The identity

    (p-q)log(p/q)/2 = m psi(a)

has the stated constants. Jensen can be applied to the nonnegative Jeffreys
density on *any* fixed bin. An ordered endpoint bin (i,j) need not be
reversal invariant. Alternatively, combine (i,j) and (j,i) into one invariant
bin; the double count in the matrix sum then reproduces the same result.

For reversal-invariant weights phi between zero and one, multiplication by
phi leaves the density ratio unchanged; the omitted symmetrized entropy
contribution is nonnegative. This justifies summing disjoint weighted bins
within the earlier excursion interface. It does not justify summing ordinary
possibly negative one-sided KL integrands over arbitrary ordered bins.

Replacing the actual geometric matrix by all feasible dominated CP matrices
can only decrease the lower bound. The objective is an extended-real lower
semicontinuous convex perspective. Entries C_ij=0 contribute zero; if every
feasible fragment has B_ij=0 at some positive C_ij, the variational value may
be infinite. That case is consistent with a finite-entropy source being
impossible under the supplied exact constraints.

The section 3 value also checks algebraically: psi(15/17)=
(16/17)log(5/3), so the ten neighbor entries contribute
(16/3)log(5/3). This review does not independently re-establish the separate
native mirror-star attainability or the Skinner--Dunkel comparison.

## 4. Exact executable controls

`check_reflected_history.py` enumerates 243 microscopic five-time paths per
history control using exact fractions. Its stationary three-state skeleton
has clockwise probability 4/9, counterclockwise probability 1/9, and hold
probability 4/9. The geometric killed skeleton has hold 4/9 and each move
2/9. This is a discrete skeleton analogue; no CTMC embedding is asserted.

Both deterministic binary-history words (eight labels) and independent
randomized half labels satisfy the midpoint Gram formula exactly. Entrywise
domination and total affinity (8/9)^4 hold exactly. Rational enclosing
intervals verify the nonlinear Jensen bound, approximately 1.69202584665,
below the microscopic four-step entropy (4/3)log 4, approximately
1.84839248149. The coarse binary process has actual memory:

    P(Y2=0 | Y1=1,Y0=0) = 8/45,
    P(Y2=0 | Y1=1,Y0=1) = 37/117.

A separate reversible killed rational kernel with state-dependent survival
checks that normalizing the halves while keeping pi is incorrect. Two small
sensor checks verify the shared-midpoint repair and the failure of mere
reversal-symmetric antithetic noise. All tests pass. No native observations,
stationary preparations, or operational acquisition are performed.

## 5. Primary antecedent and priority scope

Jorgensen, Neeb and Olafsson, *Reflection Positive Stochastic Processes Indexed
by Lie Groups*, SIGMA 12 (2016), 058, [arXiv:1510.07445v3](https://arxiv.org/html/1510.07445v3),
Lemma 3.21, writes the joint nonnegative cylinder functional as an integral
of two nonnegative semigroup words evaluated at the common midpoint.
Using the same word family gives the nonnegative Gram structure directly.
Definition 3.2 and Proposition 3.3 also state the Markov/reflection-positive
relation. Thus the bare history factorization is classical, including more
than a PSD covariance claim. The paper credits Klein (1978) and
Klein--Landau (1975) for the relevant path-space reconstruction tradition.

This source does not establish the present quantitative entropy bound.
The present review is not an exhaustive novelty search for that bound.
The appropriate claim is an entropy certificate built from the classical
nonnegative midpoint factorization and the geometric path measure, with the
observation and parity conditions stated explicitly.
