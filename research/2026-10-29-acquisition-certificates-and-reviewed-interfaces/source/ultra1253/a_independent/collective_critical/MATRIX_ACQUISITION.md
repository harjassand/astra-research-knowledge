# Native matrix functions and finite output: no oscillator/coefficient oracle

29 October 2026. This supplies an accuracy-controlled acquisition algorithm
for the matrix quantities in the companion proofs. Dense matrix operations
are charged; a dense many-body state, permanent or Gibbs element is not used.

## 1. Certified square-root and inverse-square-root polynomials

The exact rational input supplies T, T1=0, a PROVED lower gap lambda>0 on
Q=1^perp and norm upper Lambda. Let P=11^T/M, S=T+P, ell=max(1,Lambda),
mu=min(1,lambda), and A=S/ell. Thus mu/ell<=A<=I. Set Y0=I and iterate

`Y_(n+1)=Y_n(3I-A Y_n^2)/2`.

In EXACT arithmetic Y_n is a polynomial in A. For each eigenvalue x, its
residual r_n=1-x y_n^2 lies in[0,1) and obeys

`r_(n+1)=r_n^2(3+r_n)/4 <=r_n^2`.

Hence r_n<=(1-mu/ell)^(2^n)=:rbar_n. The acquired matrix enclosures are

`sqrt(T)=sqrt(ell) A Y_n-P + E_s`,

`(T_Q)^(-1/2)=Y_n/sqrt(ell)-P + E_i`,

with ||E_s||<=sqrt(ell)rbar_n and
||E_i||<=rbar_n/sqrt(mu). They act as zero on the uniform vector. The
error estimates include the uniform eigenvalue too; subtracting its exact
projector causes no issue. Every entry error is bounded by these same
operator-norm bounds. Outward ball arithmetic encloses the exact polynomial
operations and then pads EVERY entry by the analytic tail. Rounded iterates
are not silently treated as exactly commuting polynomials.

To obtain an operator error delta takes
O(log((ell/mu) log(ell/(mu delta)))) iterations. Dense arithmetic takes
O(M^3) scalar operations per iteration. The precision must also pay the
arithmetic enclosure widths, which are explicitly checked in the consumer.
This is an elementary ordinary Newton--Schulz matrix-function algorithm;
it is not claimed as a new square-root method.

The pseudoinverse is acquired as `(T+P)^(-1)-P` using an outward matrix
inverse. Diagonal pressure is evaluated with its Q projection. Its analytic
upper `(Tr T)/lambda` is an available fallback, so a numerical inverse is
not a scientific premise.

## 2. Stable determinant formulas without a nearly zero eigenvalue

With G=sqrt(MU/2)(T_Q)^(-1/2), let z=4sqrt(K)/M. The trial normalizer proxy
is computed as

`p0=[det(I+z(G+P))/(1+z)]^(-1/2)`.

This is exactly det_Q(I+zG)^(-1/2). Adding P inside the large-scale matrix
and dividing its KNOWN uniform eigenvalue avoids a gratuitously ill-
conditioned determinant with one eigenvalue1 and all othersO(sqrt(K)).

Likewise the error receiver uses

`Rdet=sqrt(det[I+M/(4sqrt(K))*sqrt(2/(MU))*sqrt(T)])`.

All determinants are ordinary M-by-M acquisitions; their outward intervals
must be finite and positive. Dimension and K enter the bit budget and the
explicit source error bounds. No interacting partition function is being
computed by this determinant.

## 3. A positive n-outcome coarse charge instrument

For any real zero-sum physical vector w and scalar s, set
theta=s w.q/K^(1/4). For n>=2 define

`p_j(q)=|sum_(l=0)^(n-1) exp[il(theta-2pi j/n)]|^2/n^2`.

Every p_j is nonnegative and sum_j p_j=1 EXACTLY, by finite Fourier
orthogonality. This is a specified bounded postprocessing of a charge
measurement, with no oscillator state reconstruction. Its canonical law
uses only chi(h s w), |h|<n. The Gaussian proxy uses

`p_j^G=(1/n)[1+2sum_(h=1)^(n-1)(1-h/n)`

`             exp(-h^2 v/2) cos(2pi h j/n)]`,

`v=(2sqrt(aK)/sqrt(UM)) s^2 w^T sqrt(T) w`.

It is itself a positive normalized law: it is the SAME instrument averaged
under the explicitly normalized real Gaussian theta~N(0,v). This observation
proves positivity, rather than presuming that a floating Fourier sum is
positive. The companion Stein bound yields

`TV(p_actual,p_G)<=sum_(h=1)^(n-1)(1-h/n)Err_K(h s|w|)`. (A1)

For n=2 this contains the binary cosine query; general fixed n gives a
finite coarse charge histogram. Each coefficient is a scalar Gaussian
moment acquired from the native matrix. The Gaussian is a computational
proxy with a proved query error, not a supplied physical ensemble.

## 4. Exact finite-bit proxy output

The consumer acquires outward intervals for all p_j^G, chooses a dyadic
probability table with denominator2^B, and bounds half the sum of the
entrywise rounding/enclosure errors. A known B-bit FAIR uniform integer
and cumulative integer table then sample that DYADIC law exactly. One
output costs B fair bits plus O(log n) comparisons, or O(n) for the simple
saved scan. There is no rejection/overlap probability or unknown normalizer.
Actual fair-bit generation is an explicitly declared primitive, separate
from deterministic probability compilation; no PRNG realization is called
an iid proof. The saved run compiles the law and emits no random samples.

The final TV bound is (A1) plus the table error. It concerns THIS finite
instrument at fixed beta and exact canonical K,K. It says nothing about
continuous/lattice TV, full occupations, arbitrary observables, trace norm
of Gibbs states, real-time dynamics, or laboratory detector acquisition.
