# Certify small leakage norms; do not first estimate every leakage vector

Working derivation, not independently reviewed. The separate large-n executable
now instantiates it; execution is not itself a proof of statistical coverage.
This is quadratic-functional/property-testing methodology, not a
claim to invent U-statistics. It sharpens the acquisition step for the mixed
positive/L2 certificate in LARGE_AMBIENT_MIXED_CERTIFICATE.md.

The partition is fixed before these validation batches. All generators are
row-stochastic, H=I/n, P=ZW is uniform conditional expectation and Q=I-P.
All source calls and all failed validation batches are charged. Radius
selection uses either a fixed schedule or fresh batches with a summable
confidence allocation; no optional stopping is hidden inside a batch.

## 1. A reusable upper-confidence inversion

Suppose a scalar unbiased statistic S estimates v>=0 and

    Var(S) <= a v+b.

For a fixed q in (0,1/2), Chebyshev implies, with failure at most q,

    v <= U(S) = S_+ + a/(2q)
                    + sqrt((a/q)S_+ + a^2/(4q^2)+b/q).          (Q1)

Indeed v-S<=sqrt((a v+b)/q), and solving the quadratic inequality after
replacing S by S_+=max(S,0) gives (Q1). Use outward rational square roots.

Repeat on k independent batches, k odd, and take the median of the k upper
bounds. The failure probability is at most

    sum_(j=(k+1)/2)^k binom(k,j) q^j (1-q)^(k-j).                (Q2)

Choose k before drawing these batches; q=1/16 permits an exact rational
binomial-tail schedule. This logarithmic-confidence median wrapper is
deliberately elementary, not claimed statistically optimal. Conditional on
an independently acquired variance envelope, the same proof applies.

## 2. Outgoing leakage from collisions in a pooled block distribution

For source block g, choose a row uniformly in g, then draw one true transition.
This samples the distribution p=(W A)[g,:]. Let X=Q e_J, mu=E X=Q p^T and

    v=n||mu||_2^2 = ||(W A Q)[g,:]||_(H^-1)^2.

For N iid draws, the order-two U-statistic

    S = n/[N(N-1)] sum_(i!=j) X_i^T X_j                       (Q3)

is unbiased for v. It is computed from destination counts, not by explicitly
enumerating N^2 pairs. If c_j are counts and C_h their totals in target block h,
its numerator divided by n is

    sum_j c_j^2 - sum_h C_h^2/|h| - N + sum_h C_h/|h|.

Let Sigma=Cov(X). Since Q is orthogonal,
||Sigma||_2<=p_max and tr(Sigma)<=1. The standard centered expansion gives

    Var(S) = 4n^2/N mu^T Sigma mu
               + 2n^2/[N(N-1)] tr(Sigma^2)
           <= 4kappa v/N + 2kappa n/[N(N-1)],                 (Q4)

where kappa>=n p_max. Crucially kappa is not a hidden uniformity promise:
an acquired bound B on every true column sum gives

    p_j <= B/|g|,       kappa_g = n B/|g| = B/pi_g.

A bad incoming-mass bound or a microscopic source block is explicitly costly.
Combine (Q4) with (Q1)–(Q2), unioned over generators and source blocks.
When v is small, the upper squared norm scales as roughly
sqrt(kappa n)/N (plus kappa/N), rather than kappa n/N. Thus pooled source
calls for squared-norm precision theta^2 have a sqrt(n), not n, leading
dependence. This is certification of a quadratic functional, not accurate
estimation of the n-vector p.

## 3. Incoming projected-Frobenius leakage from two per-row halves

Write pi_h=|h|/n and use the weighted block indicator
Y=e_(block(J))/sqrt(pi_(block(J))). Its mean in row i is M_i.
Let M be the n-by-r mean matrix. Then

    v = ||Q M||_F^2/n >= ||Q A P||_H^2.                       (Q5)

For EACH named row, acquire two independent batches of N transitions.
Let X_i and Y_i be their empirical weighted-block vectors. With independent
rows and halves, the statistic

    S = <Q X,Q Y>_F/n                                         (Q6)

is unbiased for v, even though rows have different transition laws. It needs
only n-by-r block counts. No irrational coordinates are stored: expanding
the inner product uses the rational factors 1/pi_h.

Let Sigma_i be the covariance of one weighted-block vector in row i.
Acquire/enclose ||Sigma_i||_2<=sigma and sum_i tr(Sigma_i)<=T. Always valid
fallbacks are sigma<=1/pi_min and T<=n/pi_min. Then

    Var(S) <= 2sigma v/(n N) + sigma T/(n^2 N^2).              (Q7)

Proof: write X=M+E, Y=M+F. The two linear error terms have total variance
2/(n^2 N) sum_i (Q M)_i^T Sigma_i (Q M)_i, bounded by the first term.
They are uncorrelated with the bilinear term because the other half has
mean zero. The bilinear variance is
tr[(Q tensor I) Cov(E) (Q tensor I) Cov(F)]/n^2, at most
(sigma/N)(T/N)/n^2 by PSD order and orthogonality of Q. QED.

At v near zero and balanced blocks, (Q1) gives squared-norm precision of order
r/(sqrt(n)N), before confidence logarithms. Total source calls 2nN therefore
have order r sqrt(n)/theta^2, subject to N>=1 and all constants/failures.
This is the important distinction from per-row vector confidence balls.

## 4. Acquiring a sharper covariance envelope

For row block probabilities p_i, the unweighted categorical covariance has
trace 1-sum_h p_ih^2 <=2(1-max_h p_ih). Hence

    tr(Sigma_i), ||Sigma_i||_2
         <= min(1,2(1-max_h p_ih))/pi_min.                    (Q8)

A fresh pilot with simultaneous lower confidence bounds on all block masses
can supply these upper bounds; its calls, confidence and storage are paid.
Standard empirical Bernstein or KL bounds may be used instead of worst-case
Hoeffding. The maximizing label may be selected only under the simultaneous
event. Fix the resulting sigma,T before the independent U-statistic batches.
In a mostly-within-community routing regime, this can materially beat the
worst-case sigma=r fallback. It is not an assumption that transition variance
is automatically small, and unbalanced blocks remain explicitly expensive.

## 5. Explicit sufficient acquisition/completeness calculation

Let a target squared norm be theta² and suppose its actual v<=theta²/16.
If a<=q theta²/16 and b<=q theta⁴/16, then with probability >=1−q,
S<=v+sqrt((av+b)/q)<=theta²/2. Substitution into (Q1) gives

    U(S) <= (17+sqrt(97)) theta²/32 < theta².

Thus the same median wrapper has both soundness and small-leak completeness;
there is no claim that an arbitrary residual must be small. Sufficient
fixed per-replicate sample counts are

    N_in >= max(1, 32sigma/(n q theta²),
                   4sqrt(sigma T)/(n sqrt(q) theta²)),
    N_out >= max(2, 64kappa/(q theta²),
                     1+sqrt(32kappa n/q)/theta²).

The constants are deliberately loose and not necessary prices. There are
2mn N_in incoming and mr N_out outgoing calls per replicate (use actual
separately allocated repetition counts in a ledger). For balanced fixed r,
bounded acquired B, sigma=O(r), T=O(nr), these are O(sqrt(n)/theta²), up to
confidence factors and the floor of one observation per named row.

If alpha<=1−g and both norm targets equal theta, compression is at most
L theta²/g. Choosing theta² proportional to epsilon g/L makes this stage
O(sqrt(n)L/(epsilon g)), apart from r,B,confidence constants. Fine coarse-
action estimation remains separately O(poly(r)L²/epsilon²) and a coarse
spectral/community pass costs O(n B polylog(n)/t²), plus sparse arithmetic.
This separates ambient-dimensional certification of small quadratic leaks
from fine r-dimensional action estimation. It does not prove a new minimax
rate or outperform all existing aggregation/property-testing compositions.
Nonzero leakage, bad column mass, small blocks, bad complement gap, or a
failed partition proposal can destroy this regime.

## 6. Scope and executable

The actual scalar admission uses square roots of these upper squared norms
in (M1), together with the acquired discarded spectral bound and separately
measured fine stochastic block action. All words are covered by the one
intersection event, including adaptively selected future schedule queries.

This does not remove acquisition of the partition or complement gap, and is
not a generic low-rank assumption. The executable tests variance identities
and count formulas exactly; large_acquisition.py separately runs the acquired
pipeline at n=4096. Its synthetic aggregate sampling uses floating NumPy
multinomials and seeded pseudorandom streams. Exact count arithmetic does not
certify ideal iid provenance, physical model truth, or NumPy randomness. An
exact rational forward source could implement the fixture with integer branch
selection and uniform indexed choices at the charged number of calls; those
billions of ordinary calls were NOT individually executed.
Known distribution testing, U-statistic and testing-lumpability theory are
strong primary-prior leads; neither novelty nor minimax optimality is claimed.
