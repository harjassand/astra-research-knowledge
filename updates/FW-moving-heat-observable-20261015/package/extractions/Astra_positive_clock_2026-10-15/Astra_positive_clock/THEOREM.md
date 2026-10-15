# Positive spectral rounding and a compact stationary hitting law

Research derivation, 15 October 2026. This is a mathematical candidate, not a novelty or implementation claim.

Let independent finite nonnegative spectral variables Z_i have exactly rational positive masses and exactly rational support, with positive zero masses. Let q=P(sum Z_i=0)>0, and assume the stationary reversible renewal identity for H:

E exp(-sH)=q/[q+s E(1/(s+Lambda); Lambda>0)], Lambda=sum Z_i.

## Deterministic spectral coupling

Choose a positive quantizer R with R(0)=0 and R(x)<=x<=r R(x) for x>0. Set T_0=0, T_i=R(T_{i-1}+Z_i). Induction gives T_i<=sum_{j<=i} Z_j<=r^i T_i. Exact positive convolution computes the law of T_n without signed cancellations; its zero mass is exactly q.

Use the same N~Geom(q) on {0,1,...} and the same iid exponential unit marks to couple H=sum_{j<=N} E_j/Lambda_j with H_R=sum_{j<=N} E_j/T_{n,j}, coupling each conditional positive spectral pair by the construction. Then H<=H_R<=r^n H almost surely. This includes the exact atom at zero. In particular F_H(t/r^n)<=F_{H_R}(t)<=F_H(t). There is no q^{-1} amplification of deterministic relative rate error.

If R rounds downward to b significant binary bits, r=1+2^{1-b} is valid. Every positive rounded support has a b-bit mantissa and a binary exponent within the encoded input rate span and n. The number of possible supports is polynomial in n/epsilon and the encoded logarithmic rate span when r^n<=1+epsilon. Each dyadic support has polynomial bit length. Exact rational probability convolution has polynomial bit length (a common denominator is the product of input denominators).

## Reusable positive exponential mixture

Write the distinct positive T_n supports as 0<lambda_1<...<lambda_K, with weights w_j>0 summing to 1-q. Define

D(s)=q+s sum_j w_j/(s+lambda_j).

For r in any pole-free interval, f(r)=D(-r)=q-r sum_j w_j/(lambda_j-r) has derivative -sum_j w_j lambda_j/(lambda_j-r)^2<0. There is exactly one root r_j in (lambda_{j-1},lambda_j), with lambda_0=0. The endpoint signs follow directly, including f(0)=q. Hence all roots are positive and simple.

Partial fractions give

q/D(s)=q+sum_j a_j r_j/(s+r_j),
a_j=q/[r_j sum_k w_k lambda_k/(lambda_k-r_j)^2]>0.

At s=0, sum_j a_j=1-q. Thus H_R is atom q at zero plus a positive K-component exponential mixture. Once its roots and weights are acquired, repeated ideal-real draws need a categorical choice and one exponential; no geometric expansion or per-draw mark compression remains.

The same secular equation is the rank-one downdate D_lambda-zz^T with z_j=sqrt(w_j lambda_j), but forming it numerically can erase tiny q. Preserve q explicitly in the scalar equation; do not compute it by subtracting sum weights from one.

## Bit and evidence gates

For exact rational supports and masses, clearing denominators gives a degree-K polynomial of polynomial coefficient height. Rational root isolation and algebraic residue evaluation provide a polynomial-bit acquisition route. This is a complexity argument, not evidence that generic polynomial arithmetic is practical at K in the thousands. A stable interval secular implementation is still needed.

For approximate upstream masses, naive mark-law total-variation errors can accumulate over N, whose expectation is (1-q)/q. A safe budget requires O(delta q) total mark error. Native algebraic weights may meet this with polynomial precision because log(1/q) is encoded-polynomial, but that precision must actually be charged. This issue does not apply to the exact rational binary examples.

Finite-bit mixture sampling needs independent bounds on root relative error, total categorical error, exponential approximation, and the zero atom. Neither finite rational output TV closeness to an unquantized continuous law nor physically valid generators follow.

The exact renewal identity and exponential-mixture/interlacing theory are established prior machinery. Positive rate-convolution rounding and its comparative value require focused prior-art investigation. The output is stationary-start first passage to one joint target, not a trajectory or arbitrary-start law.
