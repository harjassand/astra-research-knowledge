# Independent ordinary review: lag witnesses and equilibrium closure

29 October2026, Brisbane. Scope: sections1–4 of the root's
`COPOSITIVE_PATH_CERTIFICATES.md`, including its equation(1) and the factor4
entropy bound. This is an internal mathematical review, not external
acceptance or a review of the later excursion/statistical sections.

The exact reviewed section text is retained as `ROOT_LAG_SECTIONS_REVIEWED.md`,
SHA25637e59fed200bed177e913c768afdf5b6bbcadc4c72a6ca2ea57a848a04b9afcf.
The full root file at capture had SHA256
efc7ecb7bc29ca5c32a6bc63f8c67eb72782c8612c39ab632c9644a4eafca544.
Subsequent root edits need not have that hash.

## Conclusion and required observation qualification

The lag theorem and constructive converse are valid at their stated finite
stationary all-even CTMC scope. The factor4 in sigma*t>=4D is correct.
The refresh formula, irreducibility, finite-rate bound and closure argument
are correct. No hidden-dimension ceiling is needed for the negative witness.

One qualification should be explicit for a stochastic emission kernel:
the formula E^T diag(pi) exp(tQ) E represents conditionally independent
emission draws at the two sample times. Correlated sensor memory is not
specified by a one-time emission kernel. At t=0 it represents two replicated
emissions, whereas the joint of a single observed variable with itself is
diagonal. Deterministic labels avoid this issue. Use t>0 for the operational
lag theorem. Unnormalized nonnegative features need the stated extra scale.

In section3 the phrase "If E is infinite" should read "If sigma is infinite"
or explicitly define the entropy symbol; E is also the emission matrix there.

## 1. Geometric generator and the path identity

For positive stationary pi, the reversed generator has
q*_xy=pi_y q_yx/pi_x. Its total departure rate at x equals q_x=-q_xx by
stationary balance. Thus Cauchy–Schwarz gives

    sum_y!=x sqrt(q_xy q*_xy) <= sqrt(q_x q*_x)=q_x.

The geometric generator with diagonal -q_x is a valid killed generator.
Its weighted off-diagonal flow is symmetric. For each microscopic jump path,
the geometric jump-rate product is the geometric mean of the forward and
reversed jump products. Holding factors are identical. Both laws start in
pi, so their stationary initial factors agree. This proves the full-path
subprobability identity directly. No observed-path likelihood is substituted
for that microscopic identity.

The geometric semigroup is reversible and entrywise nonnegative. In sqrt(pi)
coordinates its half-time exponential is a nonnegative matrix. Multiplying
by the nonnegative label matrix gives a nonnegative Gram factor for C_geo.
It may be substochastic due to killing; that does not affect CP membership.

For each fixed endpoint pair, arithmetic mean minus geometric mean of path
weights is nonnegative. Summing paths and labels proves Delta>=0. Because
label rows sum to1, summing all entries gives

    D=1-integral sqrt(p*q).

These observations also show why the symmetric joint is needed: the
geometric path weight is bounded by the arithmetic mean of forward and
reversed weights, not separately by either one.

## 2. Entropy constants and the witness inequality

Reversal is an involution preserving the reference path integration, so
KL(P||P_rev)=KL(P_rev||P). Under stationarity and all-even reversal,

    KL(P||P_rev)=sigma*t
      =1/2 integral (p-q)log(p/q).

Using (a-b)log(a/b)>=4(sqrt(a)-sqrt(b))² gives

    sigma*t>=2 integral (sqrt(p)-sqrt(q))²=4D.

The distinct Renyi bound is sigma*t>=-2log(1-D). Both are valid; neither
should be substituted for the other by an incorrect factor convention.
If reciprocal support fails, sigma is infinite and both bounds remain true.
For a finite CTMC at finite t the path affinity is positive, since paths
with no jumps have positive overlap.

Let H be symmetric copositive. Its pairing with C_geo is nonnegative, and
Delta is entrywise nonnegative. Thus for gamma=-<H,C_sym>>0,

    gamma<=-<H,Delta><=h_minus D,
    h_minus=max(0,-min H_ab)>0.

The two root lower bounds follow, including the logarithm's valid domain.
The geometric argument is model-wide; it makes no claim that the source's
hidden generator, parity or stationary preparation has been acquired.

## 3. Exact refresh construction and closure

Given C=sum v_k v_k^T, normalize each nonzero vector into a probability
r_k=v_k/s_k and assign weight w_k=s_k². Normalization of C gives sum w_k=1.
Let hidden stationary mass be mu_ka=w_k r_ka, deleting zero-mass states.

Let T_W be the stochastic kernel that refreshes the visible label from r_k
while retaining mode k, and T_G the kernel with every row equal to mu. Then

    T_W²=T_W, T_G²=T_G, T_W T_G=T_G T_W=T_G.

The generator Q=R(T_W-I)+epsilon(T_G-I) satisfies detailed balance because
within-mode flow is R*w_k*r_ka*r_kb and global flow is epsilon*mu_x*mu_y.
Every pair of distinct positive-mass hidden states has a positive global
refresh rate if epsilon>0, proving irreducibility. State-changing departure
is R(1-r_ka)+epsilon(1-mu_ka)<=R+epsilon.

The commuting projection identities imply

    exp(tQ)=exp(-epsilon*t)[exp(-Rt)I+(1-exp(-Rt))T_W]
            +(1-exp(-epsilon*t))T_G.

Observed projection maps the three terms to diag(p), C, and pp^T respectively,
giving the root's equation(1). Each is a normalized probability matrix, so
the root TV bound follows by convexity and 1-exp(-epsilon*t)<=epsilon*t.

For a target tolerance eta>0, choose R>=log(2/eta)/t and
0<epsilon<=eta/(2t). Finite clocks suffice at every positive tolerance.
The epsilon->0 limit introduces long inter-mode mixing times; stationary
preparation should not be treated as operationally free. Exact boundary
realization is not asserted by this approximation theorem.

Normalized CP matrices are exactly the convex hull of rr^T for r in the
probability simplex. This hull is compact in finite dimension, hence closed.
Necessity plus the explicit approximation establishes the claimed closure.
A supplied CP factorization is essential to this construction; deciding
membership or finding a factorization is not solved by it. If real factors
are only approximated, their approximation/normalization error must be added.
Rational weights and within-mode laws give rational generator coefficients.

## 4. Executed four-state check of equation(1)

The independent checker uses w=(2/5,3/5),
r_1=(2/3,1/3,0), r_2=(0,1/4,3/4), so there are four positive hidden states.
It chooses R=3/2, epsilon=1/7, t=2/3. It checks projection identities,
commutation, detailed balance, irreducibility and departure ceilings exactly
with rational arithmetic. Rational exponential enclosures give interval
entries of the displayed lag formula and a strict TV-bound check.
A full floating matrix exponential is an additional numerical control,
not the logical basis for the identity.

## 5. Finite all-even CTMC with fully reversible visible paths but non-CP lag

The following100-state source makes the difference from ordinary negative
correlations explicit. Its hidden states are (p,k), p in Z/5Z and
k in {0,...,19}. Visible output is p. At rate a=20 the phase increments;
at a forward wrap it resets to0 and changes p to p+1 or p-1, each with
probability1/2. At rate b=1/1000 the phase decrements; at a reverse wrap it
resets to19 and likewise changes p by an independent equiprobable sign.
All hidden states are stipulated even under the physical reversal.

The source is irreducible, has reciprocal support and uniform stationary
law. Its departure rate is20001/1000 at every state. The involution
R(p,k)=(p,19-k) conjugates Q to Q^T and fixes the visible label. Consequently
the ENTIRE stationary visible path law is time-reversal invariant. This
follows for every finite sequence of times by inserting R between the
transition matrices and diagonal visible-label projectors. It is not merely
equality of a two-time covariance.

Consider lag t=11/20. Translation and spatial reflection make the visible
transition matrix circulant symmetric. First compare with the forward-only
chain b=0. If N~Poisson(20t) and the initial phase is uniform, the number W
of wraps has E W=t. Conditional on W, its visible Fourier mode is c^W,
where c=cos(2*pi*l/5). For every integer W>=0 and c in [-1,1],

    c^W>=1-W(1-c).

For c>=0 this is Bernoulli's inequality; for c<0 the cases W=0,1 are
equalities, and for W>=2 the right side is at most-1. Hence every
nonconstant forward-only mode is at least1-t(1-c).

Couple in the reverse clock independently. Paths agree unless a reverse
event occurs, a probability at most b*t. An observable of modulus<=1 changes
in expectation by at most2bt. Therefore each eigenvalue of the normalized
two-time joint C is at least

    [1-t(5+sqrt(5))/4-2bt]/5 > 0.00078813061875.

The final displayed decimal is represented by an outward rational bound in
the checker, not used as an exact decimal equality.

Let s be the probability that the visible positions at lag t are adjacent
on the five-cycle. For the forward-only chain, each one-wrap path is an
adjacent transition. Since E[W|N]=N/20,

    s_0>=t-t*P(Poisson(11)>=19).

Indeed E[W;W>=2]<=E[W;N>=20]=t*P(Poisson(11)>=19). The tail admits the
positive-term bound

    P(Poisson(11)>=19)
      <= exp(-11)*11^19/19! /(1-11/20).

Reverse-clock insertion loses at most bt from s. For the Horn copositive
matrix H=11^T-2Adj(C5), the pairing is1-2s, so gamma=2s-1. Rational
exponential enclosures establish

    gamma >= 0.0783738609204790,
    sigma >=4gamma/t >= 0.5699917157853019 nats/time.

Thus the observed lag joint is strictly positive definite, entrywise
positive, symmetric, and outside CP, while every observed time-reversal
test gives zero. No hidden clock ceiling or state limit is used by the
inference from gamma. The supplied source itself has finite entropy

    sigma=(20-1/1000) log(20000).

The independent full100-by100 floating exponential gives min eigenvalue
approximately0.0013056652876 and Horn gap0.098181766286, consistent with the
rigorous lower bounds. The numerical exponential is not the certificate.

This source also illustrates the parity boundary: if R were stipulated as
an odd-state physical reversal instead, it would satisfy the corresponding
generalized balance. The visible data alone do not acquire microscopic
parity or thermodynamic interpretation.

## 6. Executed scope

`check_copositive_lag.py` and `COPOSITIVE_LAG_INDEPENDENT_CHECKS.json` preserve
the four-state closure construction, the100-state lag witness and16 rational
interval checks of both entropy/affinity bounds on homogeneous biased cycles.
Every result is supplied-generator mathematics. Native observations,
preparations, physical measurements and physical device validations are zero.

## 7. Optional scalar sharpening, separately derived

The factor4 and logarithmic bounds are valid. A stronger pure-information
inequality is available if desired; no novelty is claimed for this scalar
divergence relation. Put m=(p+q)/2, u=(p-q)/(p+q), and a=sqrt(1-u²). Then

    KL(P||Q)=E_m[2u atanh(u)],  affinity=E_m[a].

The function f(a)=2sqrt(1-a²)atanh(sqrt(1-a²)) is convex decreasing on(0,1),
with f(1)=0. Writing z=sqrt(1-a²),

    f''(a)=2[z/(1-z²)-atanh(z)]/z³ >=0.

Jensen yields KL>=f(affinity). Thus with d=gamma/h_minus,

    sigma*t >=2sqrt(2d-d²) atanh(sqrt(2d-d²)).

Two-point probability pairs related by an involution attain the underlying
divergence inequality. Attainment by a finite CTMC together with a prescribed
copositive witness is not asserted. The root need not use this sharpening
for its stronger structural conclusion.
