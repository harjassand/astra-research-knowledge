# Finite-mean bit receiver: exact ingredients and implementation boundary

29 October 2026. Independent derivation for the actual fixed Maxwell prototype
with a=1,b=11/10,C=b^(3/2), rational nonnegative t and bin width1/4. It does
not transfer to the new hard-sphere construction. Mathematical conclusions
below use the usual unbounded-workspace bit machine. No small numerical
universal bit-cost constant or practical advantage is asserted.

## 1. Required cost statement

Almost-sure finite refinement does not imply finite expected bits. A mean
proof must control the costs of the ideal genealogy, small occupied-child
norms, strict comparisons, Gaussian inversion, reused factory thresholds and
final floors. The target here is finite expected bit work for each fixed
rational t and fixed rational input catalog, not a uniform-in-t bound.

A constructive sufficient implementation contract is: iterative arithmetic
DAG evaluation, outward elementary rational/ball operations, and bit work
polynomial in requested precision, expression length and the argument/
conditioning heights specified in Section6. Such elementary evaluators need
no new oracle: rational interval Taylor series plus range reduction implement
exp/erf, an atanh series implements log after binary rescaling, and bisection/
Newton implements sqrt. Arb supplies enclosure validity; its documentation
is not by itself a measured worst-case software-runtime bound.

Under this explicit implementation contract the finite-bin algorithm has
finite expected fair-bit consumption and finite expected bit work. Sections2--6
pay its probabilistic/conditioning summability. Section8 separates this
mathematical construction from the specific Python execution boundary.

## 2. Marked degree, raw loop counts and small norms

Conditional on proposal v, query frequency xi is standard3-normal,
z=xi-i v/b and q~Poisson(h||z||^2/2), h=1/20. Every fixed moment of q and
||xi|| is bounded by a polynomial in1+||v||. The top norm is
||z||^2=||xi||^2+||v||^2/b^2. Its negative logarithm has finite moments;
even at v=0 the three-dimensional Gaussian small-ball bound suffices.

The four-rotation kernel pays a split probability at least delta=1/4 for
every complex unit direction and q>=2. There are at most q-1 splits.
Raw iterations are dominated by a sum of O(q) independent geometric(delta)
variables; terminal horizon exits only shorten this. All fixed raw-count
moments are polynomial in q. The literal Binomial(q,U) loop uses q uniform
coin comparisons, not an unpriced O(1) binomial oracle; total work is still
polynomial in degree/raw count. Each singleton has four scalar exp-coins,
one bounded-denominator categorical and one initial quadratic.

Small norms must be paid only when their child is occupied. At degree q,

    P(child occupied | U)=1-(1-U)^q <= qU.

For every x>=0, even with arbitrary direction-dependent U,

    P(child occupied AND -log U>x | past) <= q exp(-x).    (B1)

Likewise for1-U. Exact U=0 causes no normalization because that child is
unoccupied. Thus every fixed occupied-log moment is finite, uniformly over
direction; no lower bound on U is assumed.

Combine (B1) with the geometric raw-count tail. On N<=n there are <=2n child
logs; if their sum exceeds x, one exceeds x/(2n). A union bound gives
4nq exp(-x/(2n))+P(N>n). Taking n of order q+sqrt(x) proves a stretched-
exponential tail and fixed moments polynomial in q. This avoids assuming
independence of loop length and near-zero child norms.

## 3. Stronger factory-stage bound than 'continuation <1/3'

Let e=ell(v)/C be the ORIGINAL margin, d=1-2p=R(v)/C>=e,
e_bar=min(e,161/250), and stages l=0,1,.... The code has

    k_l=(23/(5e))2^l,
    e_l=e_bar 2^-l,
    c_l=2 product_(j<l)(1+e_bar 2^-j/2) <4.

The threshold uses original e before the clamp. At upper exit i>=k_l,
continuation is (1+e_l/2)^(-i). For this prototype it is uniformly
<=rho=6/25<1/4:

* If e<=161/250, log(1+e_l/2)>=e_l/2-e_l^2/8 gives
  k_l log(1+e_l/2)>1.9.
* Otherwise C>23/20 implies k_0>529/100, while
  log(1+e_bar/2)>=161/500-(161/500)^2/2. Their product
  exceeds log(25/6). Later stages only increase this exponent.

certify.py checks the latter strict comparison via a positive rational
Taylor lower bound for exp. A bound1/3 alone would NOT pay the crude4^l
stage-work estimate below.

The integer walk has drift (1-c_l p)/(c_l-1), with
1-c_l p>=d2^-l by induction. Its upper-exit geometric overshoot has mean
<=2. Thus conditional mean stage-l p-coins are O(4^l/(e d)). A starting
overshoot beyond the next threshold incurs at most one extra mandatory
repeat-loop step, covered by the same bound.

Do not integrate a spurious1/ell^2. The FIRST-stage martingale (2p)^i gives

    P(exit high) <= d/[1-(1-d)^k0] <= d/D,
    D=1-exp(-23/5)>0.

The first-stage mean coins are O(1/e), by the elementary stopped-walk
identity (Huber's Lemmas3--4). Its high-exit factor d cancels later1/d.
Therefore for l>=1,

    E[stage-l p-coins | v] <= A rho^l 4^l/e,             (B2)

with A=24 sufficient; first-stage mean coins are at most8/e. In detail use
D>15/16, c_l-1<3 and the drift bound to get conditional stage mean
<= (104/5)4^l/(ed), then multiply by d rho^l/D. Multiplication by ANY fixed polynomial in l
still gives a convergent sum since4rho=24/25<1. This uses Huber's ordinary
martingale/walk with the explicit correct continuation bound above; no
false pointwise inequality log(1+x)>=x is imported.

Geometric auxiliary success is (c_l-1)/c_l>=1/2, so its count and log-
overshoot have all moments. log i and log1/e_l cost O(l+log1/e+log(1+G)),
where G is geometric overshoot. Continuation powers use O(log i) products,
not i products. Their positive intermediate magnitude has logarithm
O(1+e_l G), also paid by the geometric tail. Thus stage precision/auxiliary
work has only polynomial dependence on l beyond the p-coin count in (B2).

## 4. Fresh comparisons, Normal inversion and Poisson thresholds

For a fresh uniform U and previously constructed P in[0,1],
P(|U-P|<eta | P)<=2eta. Additional strict-comparison precision therefore
has exponential tail after paying expression accuracy height. This includes
P=0 or1. A fresh exponential wait has density<=1, giving the analogous
remaining-time comparison bound. Uniform endpoint logarithms are integrable.

Normal.enclose reuses U; its bisections cannot be treated as fresh uniforms.
At depth j its rational-x interval has dyadic spacing, and its CDF interval
is comparable to that spacing times the Gaussian density on the bracket.
The active CDF-endpoint distance logarithm costs
O(j+1+X^2+log(1+|X|)) in every fixed conditional-average moment. Summing the
O(P+log(1+|X|)) bisections for P output bits gives polynomial work in P and
1+|X|. Bracket doubling has Gaussian tails. This is the ordinary exact
inverse-CDF construction, not free already-rounded normal access.

Inverse Poisson also reuses U. First restrict to q<=Q: at most Q+1 adjacent
cumulative thresholds have eta-neighborhood mass <=2(Q+1)eta. Poisson tails
pay the complement with Q a suitable constant times rate plus log-tail
level. Thus count and adjacent-threshold log margins have fixed moments
polynomial in1+rate. The present random rate is quadratic Gaussian and has
all moments. Its factorial/rate recurrence and cumulative addition have
polynomial precision cost.

An all-requests height makes this literal, strengthening the preceding
averaged description (root independently supplied this formulation). For
every m,j>=0 include all dyadics q=k2^-j in[-2^m,2^m], and define H by

    |U-Phi(q)| >= 2^[-3(j+m)-H] for ALL these points.

There are <=3*2^(j+m) points per (j,m). A union bound gives
P(H>s)<=min(1,(32/3)2^-s). Thus H has all moments, and EVERY adaptively
requested inverse-CDF precision is covered simultaneously. The needed
probability bits are O(j+m+H), with the scalar-CDF accuracy paid separately.
No bound conditional on the exact normal X is assumed; that X can be
arbitrarily close to the dyadic grid. The earlier 'conditional-average'
description must always be consumed through this global random height.

For reused inverse-Poisson U, conditional on its rate, the analogous
simultaneous event |U-F_q(rate)|>=2^(-2q-H) for all q>=0 has exponential
H tail by a one-dimensional union bound. O(q+H) probability bits therefore
cover every possible adaptive cumulative comparison. Poisson moments pay
that polynomial q dependence; fresh threshold uniforms are not invented.

## 5. Nonfresh factory comparisons and final bins

The clamp e versus161/250 and integer i versus k_l(v) reuse proposal v.
Under proposal density weighted by1/ell, s=||v||^2 has density proportional
to s^(1/2)exp(-alpha s), with

    alpha=1/b-1/2=9/22>0,
    e(v)=exp(-s/22)/C,
    k_l(v)=(23C/5)2^l exp(s/22).

The clamp is one nondegenerate radial level; its log-distance is integrable
to every fixed power under this Gamma-type density. For the threshold,
|i-k_l|>=dist(k_l,Z); this avoids pretending adaptive i is independent of v.
The density of y=k_l is a dilation w_l(y)=2^-l w_0(2^-l y).
w_0 has finite total variation: square-root behavior at its endpoint and a
decaying power of y times log-polynomials at infinity. The same properties
hold after multiplying the radial density by any fixed polynomial in s.

The integral of [-log dist(y,Z)]_+^p over a unit interval is finite.
Summed interval suprema of w_l are bounded by its integral plus total
variation, uniformly in l. Thus all integrated integer-margin log moments
are finite uniformly in l, or with an allowed polynomial in l. Thresholds
are not assumed to stay a warranted distance from integers.

The Normal bisection estimate can be made independent of any heuristic
'typical Gaussian density': for each allowed bracket and depth j there
are <=2^j possible CDF thresholds. A union bound on their eta-neighborhoods
gives2^(j+1)eta. Sum the finitely many bracket sizes up to a chosen bound;
Gaussian tails pay larger brackets. This proves the logarithmic margin
cost in Section4. Proposal weighting does not spoil it: Holder with
E_Gb ell^(-p)<infinity for some p>1 transfers the exponential margin tail
to another exponential tail. For this prototype p=2 works. This also pays
proposal normal refinement when the same normal is reused through many queries.

The accepted coordinate law is a mixture of Gaussian variances in[1,11/10].
Its density is bounded by a constant times exp(-x^2/(2b)). Summing around
the1/4-grid bounds the fractional-part density. Final boundary-distance
logs therefore have all moments. Gaussian tails also pay integer output
length. This is a quantization-cost argument, not merely zero boundary mass.

## 6. From logarithmic conditioning to finite bit work

For a finite query let H include its degree/raw-count polynomial; occupied
child log norms; initial norm log; Gaussian squared magnitudes; wait/uniform
endpoint logs; and strict-comparison log margins. Every fixed moment of H
is polynomial in1+||v|| except the proposal-only margins integrated above.

The elementary expression has polynomially many nodes in degree/raw count.
Differentiating sum, product, inverse, sqrt, log, exp and integer powers
bounds the logarithm of a sufficient interval error-amplification constant
by a polynomial in H. All small denominators are the occupied/top norms,
positive uniforms or factory margins already charged. Phase exponentials
have bounded modulus. Integer exponents cost logarithmic exponent length
in binary powering; their conditioning contributes degree and log i.
Factory intermediate magnitude has logarithm O(1+e_l G), covered by the
geometric overshoot. erf has bounded derivative; inverse-normal sensitivity
has its log height paid by the Gaussian squared magnitude.

Thus a P-bit accuracy request can be met with precision polynomial in P+H.
Elementary rational interval evaluation then has polynomial bit cost in
that quantity; doubling precision costs another polynomial factor. The
log-margin and normalization tails proved above give finite expected
complete p-coin bit cost, with polynomial velocity factors and the integrated
proposal-only margins. This supplies the sufficient local evaluator cost
contract from Section1, rather than an oracle for a rounded real answer.

Queries are requested using only past outcomes. A fresh query cost may
correlate with its own p-coin output, but not with the event of being requested.
Consequently the stopped-sum argument charges its mean against (B2), with
no false within-query independence. Stage overhead is polynomial in l and
log1/e and is paid by (24/25)^l. Shared proposal refinement is covered by
Section5; it is not silently resampled or omitted.

All remaining radial integrals are of the form

    int G_b(v)/ell(v) poly(||v||) dv < infinity,

and the same integral with the clamp/integer log margins. alpha=9/22>0 and
Section5 pay them. Independent proposal renewal multiplies finite mean work
by C; the final floors have finite mean by Section5. This proves finite
expected fair bits and bit work for the constructive iterative elementary-
interval implementation, for each fixed rational t. It does not provide a
small numerical bound, a measured software-time guarantee or uniform-in-t
bit complexity. Actual library complexity beyond this explicit evaluator
contract is not inferred from finite sample counts.

## 7. Ordinary comparison and priority

Exact Wild has the same bit-source/bin target but usual mean leaves exp(t),
which is not a lower bound on every method. The independently checked
equilibrium receiver is a paid, cheaper large-time alternative at a specified
TV tolerance. Exact rounded normals, lazy random reals, inverse CDFs and
Bernoulli factories are established tools (Karney2013/2016; Huber2014).
The mathematical operation here pays their composition with the nonlinear
marked query. Historical novelty and practical all-solver advantage are
UNKNOWN, not supplied by finite expected work.

## 8. Literal Python obstruction and repair intake

The first reviewed Real.at recursively evaluated its DAG. The retained
DEPTH_CONTROL.json exhibits1500 finite additions raising RecursionError at
the default limit1000. Unbounded finite depth occurs with positive probability
in marked output products/normalizations, so this was a genuine prototype
failure, not a measure-zero equality. No producer file was edited by me.

The repaired explicit dependency/postorder evaluator has now been whole-read:
every arithmetic node is evaluated from cached dependency values. Normal
leaf calls enter only the constant-depth Uniform/CDF comparison subroutine.
The same independent1500-addition counter now returns exactly1500 at the
unchanged recursion limit; REPAIRED_DEPTH_CONTROL.json preserves this, next
to the old failure. Root's depth10000 and identical600-output/bit replay
are separately retained producer controls, not additional independent sampling.
Thus the identified arithmetic-depth obstruction is repaired. The finite-
mean theorem above still belongs to the explicit elementary-evaluator cost
contract, not a benchmark or an assertion about every internal operation
of a particular python-flint build.
