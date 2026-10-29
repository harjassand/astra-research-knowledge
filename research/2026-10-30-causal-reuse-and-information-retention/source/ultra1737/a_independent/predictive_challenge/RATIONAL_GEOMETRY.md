# A fully rational fresh-spanner precision receiver

Independent construction for the proposed teacher compiler. This supplies an
elementary, deliberately slow alternative to a real-arithmetic SVD primitive.
It does not require a target singular-value lower bound, P conditional queries,
new examples or a numerical rerun. Liu–Moitra2411.07536v1 Claim5.5/Lemma5.6
provide the established volume-spanner/robust-truncation mechanism; the exact
finite arithmetic below makes its resource hypothesis explicit.

## 1. Acquired rational matrix and a known gap

Let U be the ideal M-by-N fresh-row sketch. After the target/teacher Markov
event, it has distance at most

    delta0=sqrt(N/M)*theta_geo

from a rank<=r matrix. The actual cached rational matrix Uhat has additional
operator error at most delta0/100. Ratios are computed using the paid uniform
mixture floor; no target density is evaluated. Thus sigma_(r+1)(Uhat)<1.01delta0.
The square delta0²=N theta_geo²/M is a KNOWN rational, even though delta0 need
not be rational. Choose a rational upper bound R>=||Uhat||op, for instance
R=4N² under the declared ratio/error bounds.

There are at most r eigenvalues of Uhat Uhatᵀ in[4delta0²,16delta0²]. Place r+1
pairwise disjoint CLOSED rational intervals there, with centers

    c_j=4delta0²+(12j+6)delta0²/(r+1), 0<=j<=r,

and half-width3delta0²/(r+1). At least one interval contains no eigenvalue.
It is found using exact rational inertia of Uhat Uhatᵀ minus the interval's
endpoints. Singularity at an endpoint marks that interval occupied. Symmetric
pivoted LDL/inertia uses polynomial rational bit work, not an eigenvalue oracle.
The count above its center gives a known integer d<=r. The d=0 case has empty
spanner and the corresponding residual bound; actual probability-row data at
the declared norm-preservation event have d>=1.

Normalize A=Uhat Uhatᵀ/R². The chosen cutoff s=c_j/R² has certified spectral
gap g=3delta0²/[(r+1)R²]. It lies strictly inside(0,1) whenever d>0; if all
eigenvalues are below the chosen interval, d=0 already handles it.

## 2. Rational approximate spectral projector

For a rational cutoff s and integer n define the binomial-tail polynomial

    p_n(lambda)=sum_(k>=ceil(ns)) binom(n,k)
                     lambda^k (1-lambda)^(n-k).

It lies in[0,1] on[0,1]. Ordinary binomial Hoeffding bounds imply that, once
n>=2/g and n>=8g^-2 log(2/e_B), it approximates the spectral step at s to
uniform error<=e_B on the two admitted spectral intervals. A rational integer
upper bound for that logarithm can be used. Hence

    F=p_n(A) is rational, ||F-Pi||op<=e_B,

where Pi is the EXACT retained spectral projector of rank d. Pi is used only
in the proof, never computed or supplied. Polynomial matrix evaluation is
finite rational arithmetic; its degree and bit work are polynomial in1/g and
log(1/e_B). Faster spectral algorithms may be used, but are not needed here.

## 3. Rational subspace acquisition with a paid inverse bound

Greedily select d columns of F by largest squared orthogonal residual, computed
exactly with rational Gram inverses. At step j<d, the next singular value of F
is at least1-e_B. Thus some column has residual at least(1-e_B)/sqrt(M).
For e_B<=1/2 every selected residual is at least1/(2sqrt(M)), while all columns
have norm<=2. The acquired M-by-d rational matrix B therefore has

    sigma_min(B)>=(4Md)^(-d)=:b0.

This is a conservative determinant/norm bound; no unknown conditioning is used.
Choose

    e_B<=min(1/2,b0/2,b0*delta0/(100R)).

One may replace delta0 by a known positive rational LOWER bound of half its
value when choosing this tolerance. Its logarithmic bit cost is
O(d log(Md)+log(R/delta0)). Since B differs from Pi B by at most e_B and its
columns span d dimensions, the equal-rank projector estimate gives

    ||Pi-Pi_B||op<=2e_B/b0,
    ||(I-Pi_B)Uhat||op<=4delta0+delta0/50.

All retained singular values of Pi Uhat are at least2delta0. Consequently
the rational compressed matrix Bᵀ Uhat has rank d and smallest singular value
at least b0 delta0. Its largest singular value has a known polynomial bound.

## 4. Exact volume swaps, no teacher-precision amplification

Run the ordinary2-barycentric-spanner algorithm on the RATIONAL columns of
Bᵀ Uhat. Greedy initial orthogonal residuals are at least its smallest singular
value/sqrt(N), giving initial volume at least(b0 delta0/sqrt(N))^d. Every exact
swap at coefficient magnitude>2 at least doubles volume; the known norm upper
bound caps it. The number of swaps is polynomial in d,N and
log[poly(d,N,M)/(b0 delta0)]. Exact rational comparisons decide coefficient2
boundaries; no equality of unknown real singular values is requested.

For the selected columns, every compressed column is an EXACT linear
combination with coefficients<=2. These rational computations may use
O(d log(dNR/delta0)) conditioning bits, in addition to input/cache arithmetic.
This is polynomial in r,N,M and the declared cache bits, not an unknown target
inverse condition. It does NOT require more accurate Q probabilities after
the sketch has been acquired.

Compressed equality implies equality of the Pi_B projections. Therefore the
full ideal-row sketch error, including cache/subspace approximation, is at most

    6(1+2r)sqrt(N)*theta_geo in L1.

Under theta_geo=zeta/[100(r+1)N] and N>=x^60>=4, this is strictly below zeta/10.
Thus replacing the ideal-real4 constant by6 leaves the declared geometric
budget and all global KL/Holder exponents unchanged. Actual selected rows,
not their approximate projections, are the fresh teacher basis.

## 5. Complete resource scope

The slow filter is still a FIXED polynomial in the proposed compiler's native
parameters: from N>=x^60, theta_geo>=x^-112 and M<=x^1200,
delta0²>=x^-1364, and R=4N² is a fixed polynomial in x. Hence1/g is a fixed
polynomial in x. The potentially exponential b0^-1 enters ONLY log(1/e_B),
which is polynomial in r,logM and log(1/delta0). All later exact arithmetic
has polynomial bit length in these finite input/work bounds.

This alternative makes zero additional P/Q calls and changes no conditional
closeness/noise event. It consumes only the finite cached rational table. It
does not claim the faster LM real-arithmetic runtime was implemented with a
specific finite-precision library, practical usefulness, or a new generic
spectral/spanner principle. No numerical fixture or arbitrary parameter case
was added. Its role is to close the general precision port at the actual
value-oracle resource contract.
