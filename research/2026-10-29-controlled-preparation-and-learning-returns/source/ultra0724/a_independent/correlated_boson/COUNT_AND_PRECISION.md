# Count probability and finite precision without an oracle

This supplements `PROOF.md`. The number local-limit statement is ordinary lattice Fourier analysis, reconstructed here to expose its input/threshold costs. The explicit arithmetic source setup is a separate exact Fraction program; the large trajectory execution remains binary64.

## 1. The homogeneous onsite density saddle is acquired

Fix finite `u=beta U>=0`, `rho>0`, and put

`q(r)=sum_(k,l>=0) r^(k+l) exp[-u(k-l)^2]`

`=A(r)/(1-r^2)`, `A(r)=1+2sum_(d>=1) r^d exp(-u d^2)`.

Under the normalized single-site law `P_r(k,l)=r^(k+l) exp[-u(k-l)^2]/q(r)`,

`rho(r)=E k=E l=r^2/(1-r^2)+r A'(r)/(2A(r))`.

It is strictly increasing: its log-r derivative is half the variance of k+l. Its limits are zero and infinity. There is a unique saddle r for every prescribed finite density. Geometric series bound every displayed sum and its derivatives; bisection with outward evaluations acquires the saddle to arbitrary precision. At density one, u4, the compiler uses a 48-bit dyadic bracket and an exact mean-density interval, not a fitted chemical potential. A radius error O(1/M) keeps the requested count within a bounded displacement of the saddle; tighter tolerances are inexpensive in bits. The actual M64 input uses total saddle-mean error below 2.10e-13.

Let X=(k,l) have this distribution and let S_M be its iid sum. Then

`p_K,diag=P(S_M=(K,K))/P(sum_i(k_i-l_i)=0)`

when `K=rho M`. This is conditioning on balance before selecting K, so its scale is M^-1/2, not the M^-1 scale of the unconditioned two-dimensional point probability.

## 2. An effective Fourier proof of that scale

The probabilities `p00,p10,p01` are strictly positive for every FINITE u and r in (0,1), and p10=p01. The covariance Sigma is positive definite. In fact, using an independent copy of X in the variance identity gives

`t^T Sigma t >= p00 p10 (t1^2+t2^2)`.

All exponential moments in a neighborhood of zero exist because r<1. Bounds for all raw/central moments are obtained by dropping `exp[-u(k-l)^2]<=1` and evaluating geometric sums, with q>=1. No local occupation cutoff or empirical variance promise is used.

For the characteristic function chi on [-pi,pi]^2, retain the (0,e1) and (0,e2) pairs in its squared modulus:

`|chi(t)|^2 <=1-2p00 p10[(1-cos t1)+(1-cos t2)]`.

Consequently `|chi(t)|<=exp(-c|t|^2)` for any `0<c<=p00 p10/5`, using pi^2<10. This is a GLOBAL aperiodicity estimate, not an assumption that a Gaussian approximation remains valid away from zero. The difference variable k-l has the same type of bound in one dimension, since its masses at zero and one are at least p00 and p10.

Center X at its mean. With `B2>=E|X-E X|^2`, `B3>=E|X-E X|^3`, Taylor remainder gives, throughout the Fourier square,

`|chi_centered(t)-exp[-t^T Sigma t/2]| <= C3 |t|^3`,

`C3=B3/6+pi sqrt(2) B2^2/8`.

For a,b of modulus at most exp(-c|t|^2), the elementary identity for a^M-b^M bounds it by `M|a-b| exp[-c(M-1)|t|^2]`. Integrating this error over the plane is O(M^-3/2) with an explicit finite constant, because

`integral_R2 |t|^3 exp(-a|t|^2)dt=(3 pi^(3/2)/4)a^(-5/2)`.

The comparison Gaussian outside the Fourier square has an exponentially small integral, bounded using the covariance lower eigenvalue. Thus beyond a COMPUTABLE fixed M0,

`P(S_M=(K,K)) >=1/[4pi M sqrt(det Sigma)]`.

For the difference count, the global characteristic bound yields

`P(sum_i(k_i-l_i)=0) <=1/[2sqrt(pi M c)]`.

Their ratio is at least

`sqrt(c)/[2sqrt(pi) sqrt(det Sigma)] M^(-1/2)`.

The corresponding usual asymptotic constant is `1/sqrt[pi M(Sigma11+Sigma12)]`; only the conservative lower bound is needed. Choosing M0 so the displayed O(M^-3/2) and Gaussian-tail errors are each below one quarter of the main Gaussian integral is an explicit algorithm on the acquired moments and covariance. It can be extremely conservative. The finite number of smaller sizes can be covered by positive canonical coefficient acquisition, or a correspondingly poor fixed lower constant. This does not assert a useful uniform numerical prefactor merely from an asymptotic theorem.

At fixed parameters the low-trace receiver is therefore polynomial. As u grows, p10 and the threshold constants deteriorate; the strictly constrained u=infinity model is not silently admitted by this argument. For inhomogeneous sites or the extensive bounded-cut class, this particular iid proof is not reused. Their count gate stays as stated in the main proof.

## 3. Exact acquisition of the actual diagonal grand normalizer

At u4 and rational r, each Fourier coefficient of A is `a_d=r^|d| exp(-4d^2)`. `acquire.py` brackets exp4 by its positive Taylor sum and a geometric remainder, inverts it, and outward-rounds q=exp(-4) to dyadics. For |d|<=D it brackets a_d with common denominator 2^bits. Raising this finite Laurent polynomial to the Mth power uses positive INTEGER convolutions and one common denominator 2^(bits M). Its constant coefficient gives the truncated balanced grand normalizer, times `(1-r^2)^(-M)`.

For the omitted coefficient l1 tail after D, write `x=r^(D+1) q_upper^((D+1)^2)` and `a=r q_upper^(2D+3)`. Then

`tail_A<=2x/(1-a)`.

The constant-coefficient error in A^M is at most `M tail_A A_upper(0)^(M-1)`. Derivatives have the similarly explicit factor `(D+1)/(1-a)+a/(1-a)^2`. These exact positive bounds pay the saddle and normalizer acquisition. No huge-denominator string, MP decimal, or a source manifest substitutes for the mathematical bounds.

The existing frozen M64 canonical Z_diag interval is REUSED with its source hash. The new compiler does not rerun that diagonal DP and does not call it the noncommuting result. Dividing by the newly acquired grand normalizer gives the exact Fraction interval for pK0, and (3) of the main proof gives the explicit interacting finite-L acceptance floor.

## 4. From exact-real laws to a finite-bit operation

The Gaussian source and all accepted histories in the mathematical operation are continuous. A finite-bit consumer must specify a rounded output law; atomic approximations are not TV-close to the unrounded continuous measure.

All determinant factors have a uniform inverse bound 1/(1-r). A phase perturbation at one site/slice changes B by a rank-one derivative of trace norm at most one. Hence its log determinant magnitude-squared has derivative at most `2r/(1-r)`. A merge log-ratio sees at most the parent and one child contribution. Phase rounding and interval evaluation can therefore be allocated over the explicit polynomial expected number of operations, without an exponential small-acceptance or arbitrary conditioning parameter.

For canonical characters, zeros forbid a relative error promise. Instead, on contractions the symmetric-power derivative gives `|d h_K|<=K D_K ||dB||`, while `|h_K|<=D_K`. At fixed density, log D_K=O(M). An absolute probability error budget is met with O(M+log(1/epsilon)+log L) phase/matrix precision bits; refining further only when a Bernoulli uniform is near an interval endpoint gives an equivalent adaptive construction. The division by G is safe because G>=1. The count-filter step additionally spends the acquired 1/bK budget.

Truncate normal quantiles with a union tail budget over a total work cap, and round quantiles to the allocated phase tolerance. Inverse normal CDF bisection with directed exp/integral enclosures uses polynomial bit work at that truncation and accuracy. Uniform integers, dyadic coins, matrix Taylor/Pade enclosures, rational Gram/LDL determinant evaluation, and bounded log-sum-exp can all be acquired at the stated precisions. A single global cap at the known expected work divided by its failure budget prevents rare arithmetic/source tails from creating an uncharged worst case. No favorable-runtime restarting is used.

This specifies a finite-bit approximate operation. It has NOT been implemented end-to-end in the present consumer. The actual run uses one seeded PCG64 raw word per 52-bit midpoint uniform, inverse-normal ndtri, and binary64 matrix algebra. It records every raw word and rejected branch but does not claim those finite seeded variables satisfy the independent-fair-bit probability theorem or that its arithmetic is interval-certified. Its statistical confidence displays belong to the corresponding ideal iid variables until the numerical/RNG approximation debt is separately paid.
