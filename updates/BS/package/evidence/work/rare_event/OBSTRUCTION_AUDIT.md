# Independent audit: low-order marginal checks and rare-event acquisition

Status: the stated construction and chi-square identity are correct. This is an internally reconstructed obstruction, not an externally certified result or a supported novelty claim. A standard high-order Fourier construction below strengthens it. No builder implementation was read.

## 1. Exact audit of the proposed pair

Assume integers `0 <= k < d`, `r=k+1`, and `0<a<=1/2`. Let `p=a^d`, `P0=Bern(a)^{⊗d}`, and

\[
\Delta(x)=p(-1)^{z(x)}\mathbf1\{x_1=\cdots=x_{d-r}=1\},
\qquad P_1=P_0+\Delta,
\]

where `z` counts zeros in the last `r` coordinates. The empty prefix is allowed.

**Validity.** On the affected face, `P0(x)=p((1-a)/a)^z >= p`. A negative perturbation therefore never creates negative mass. Also
\[
\sum_x\Delta(x)=p\sum_{z=0}^r\binom rz(-1)^z=0.
\]
Hence `P1` is a probability law. At `a=1/2`, some masses can be zero, which causes no difficulty.

**Marginals.** A set of at most `k=r-1` observed coordinates necessarily misses a suffix coordinate. Summing `Delta` over that coordinate cancels its two signs, with all other coordinates held fixed. Thus every joint marginal of order at most `k` agrees exactly under the two laws. In fact any marginal missing even one suffix coordinate agrees, regardless of its total order.

**Target.** At `x=1^d`, the perturbation is `p`, so `P1(1^d)=2p`.

**Chi-square.** Because `P0` has full support,
\[
\chi^2(P_1\Vert P_0)
=\sum_x\frac{\Delta(x)^2}{P_0(x)}
=p\sum_{z=0}^r\binom rz\left(\frac a{1-a}\right)^z
=\frac p{(1-a)^r}=:c.
\]

## 2. Sampling guarantee and useful constants

The claim must specify success probability and access. Suppose an estimator receives `n` iid full vectors from an unknown law in `{P0,P1}`. It may be supplied `d,a,k`, all low-order marginals, both candidate laws, and the construction for free. Assume under **each** law it achieves relative error at most `epsilon<1/3` with probability at least `1-delta`, where `0<delta<1/2`.

The target intervals `[p(1-epsilon),p(1+epsilon)]` and `[2p(1-epsilon),2p(1+epsilon)]` are disjoint. Thresholding between them gives a test with both errors at most `delta`. Write
\[
B_\delta=(1-2\delta)\log\frac{1-\delta}{\delta}.
\]
Binary KL data processing, additivity, and the order-2 Renyi bound give
\[
nD(P_1\Vert P_0)\ge B_\delta,
\qquad
D(P_1\Vert P_0)\le\log(1+c)\le c.
\]
Consequently
\[
\boxed{\quad n\ge\frac{B_\delta}{D(P_1\Vert P_0)}
\ge\frac{B_\delta}{\log(1+p/(1-a)^r)}
\ge B_\delta\frac{(1-a)^r}{p}.\quad}
\]
These explicit constants improve the immediate Pinsker consequence `n >= 2(1-2delta)^2/c`. They are lower-bound constants, not a claim of an exact finite-sample minimax testing solution. For example, `B_(1/4)=(log 3)/2` and `B_(1/10)=0.8 log 9`.

For an exactly computable sharper denominator, put `t=a/(1-a)` and `g(u)=(1+u)log(1+u)-u`, with `g(-1)=1`. Then
\[
D(P_1\Vert P_0)=p\sum_{z=0}^r\binom rz t^{-z}g((-t)^z).
\]
This follows by subtracting the mean-zero linear term. At `a=1/2`, it becomes `2^{-(d-r)} log 2`. For fixed `r`, its ratio to `p` tends to `2 log 2 - 1` as `a` tends to zero.

**Scope.** For fixed `k` and fixed `a`, the bound is exponential in `d`. It is not uniformly exponential in growing `k`: when `a=1/2` and `r=d`, the alternative is a parity-conditioned uniform law and a constant number of full samples gives constant-confidence detection. The theorem concerns passive iid sampling, and does not bound interventions or conditional-sampling oracles. It also does not apply when exact full independence is supplied as a trusted assumption; then `p=a^d` is already known. The point is that low-order marginals alone cannot certify that assumption. Under the two-law promise, marginal information by itself provides no distinguishing information at all.

## 3. Stronger extension: the closest high-order perturbation

This section is an independent derivation using standard orthogonal expansion machinery; novelty is not asserted.

Let `b=1-a`, and for every subset `S` let
\[
\phi_S(x)=\prod_{i\in S}\frac{x_i-a}{\sqrt{ab}},
\]
the orthonormal product basis of `L²(P0)`. Define
\[
L(x)=\sum_{|S|\le k}\phi_S(x)\phi_S(\mathbf1),\quad
H(x)=\sum_{|S|>k}\phi_S(x)\phi_S(\mathbf1),
\]
\[
S_k=L(\mathbf1)=\sum_{j=0}^k\binom dj(b/a)^j,
\qquad K=H(\mathbf1)=p^{-1}-S_k.
\]
When `S_k<=K`, set `Pstar(x)=P0(x)(1+H(x)/K)`.

**Proof of all claims.** The full reproducing kernel equals `1{x=1}/p`; hence `H(x)=-L(x)` for `x!=1`. Since `a<=1/2`, every absolute product `|phi_S(x)phi_S(1)|` is at most `(b/a)^|S|`, giving `|L(x)|<=S_k<=K`. This proves nonnegativity off the target; at the target the likelihood ratio is exactly two. All terms of `H` have positive degree, giving zero mean and normalization. Orthogonality to every degree-at-most-`k` function proves equality of all the required marginals. Finally, `E0 H²=K`, so
\[
\chi^2(P_\star\Vert P_0)=1/K.
\]
The condition is precisely
\[
\Pr\{\operatorname{Bin}(d,1-a)\le k\}\le\tfrac12,
\]
because `p S_k` is this binomial CDF. It implies `K>=1/(2p)`, so `chi²<=2p` and the preceding argument gives
\[
\boxed{n\ge B_\delta/\log(1+1/K)\ge B_\delta K\ge B_\delta/(2p).}
\]
Thus the full rare-event sampling order survives exact low-order information through much larger orders than fixed `k`; the displayed CDF condition is the exact stated regime. For the unbiased case it includes `k<=floor((d-1)/2)`.

**Optimality for this local criterion.** For any other law `Q` with the same low-order marginals and `Q(1)=2p`, write `h=Q/P0-1`. Its Fourier coefficients vanish in degrees at most `k`, and `h(1)=1`. Cauchy–Schwarz yields
\[
1=\left(\sum_{|S|>k}\widehat h_S\phi_S(1)\right)^2
\le K\sum_{|S|>k}\widehat h_S^2
=K\chi^2(Q\Vert P_0).
\]
Therefore `1/K` is the exact minimum chi-square divergence among these laws whenever the sufficient positivity condition holds. This is chi-square optimality, not a proof of optimality for KL divergence or every testing criterion.

**Executable representation.** No exponentially long vector is needed to specify the law. If `x` has `m` ones, `L(x)` is the sum through degree `k` of the coefficients of `(1+(b/a)t)^m(1-t)^(d-m)`. It can be computed by a finite coefficient recurrence. A full sampling implementation still needs its own arithmetic, precision, preprocessing, and runtime accounting; none is claimed here.

## 4. Predecessors and novelty boundary

1. Benjamini, Gurel-Gurevich and Peled, *On K-wise Independent Distributions and Boolean Functions*, Proposition 26, section 4.9, printed p. 10 / PDF p. 11. Their explicit construction uses parity at bias one-half, then coordinatewise AND with independent bits for smaller bias, obtaining zero all-ones mass while preserving `k`-wise independence. [Primary manuscript](https://arxiv.org/pdf/1201.3261).

   Independently pushing a uniform parity law through independent `Bern(2a)` thinning gives exactly `Q_±(z)=Bern(a)^r(z) ± a^r(-1)^(number of zeros)`. The paper uses the sign removing the all-ones event; the opposite sign doubles it. Activating the latter only when an independent product prefix is all ones gives the audited construction exactly. The paper explicitly supplies parity plus thinning; this opposite-sign prefix gating is an elementary derivation, not an exact formula located in its text.

2. Rubinfeld and Xie, *Testing Non-uniform k-wise Independent Distributions over Product Spaces* (ICALP 2010), Theorem 4.3 in the full manuscript: nonuniform `k`-wise independence is characterized by vanishing nonconstant Fourier coefficients through degree `k`. The audited likelihood perturbation is `1{prefix=1} product_suffix ((x_i-a)/(1-a))`, whose minimum Fourier degree is `k+1`. [Primary manuscript](https://people.csail.mit.edu/ningxie/papers/RX09.pdf).

3. Berend, Ernst, Kontorovich and Kumar, *Exact expressions for the maximal probability that all k-wise independent bits are 1* (2024), Theorem 2.2 and Corollary 2.4, study the corresponding extremal all-ones mass, including `M(n,n-1,a)=a^(n-1)` for `a<=1/2`. The doubling perturbation generally is not extremal for event mass. [Primary manuscript](https://arxiv.org/html/2407.18688v1).

4. The reduction from separated target values to testing a close pair is the classical Le Cam two-point method. See Bin Yu, *Assouad, Fano, and Le Cam* (1997). [Primary chapter](https://web.stanford.edu/class/stats300a/REFS/yu1997assouad.pdf).

This was a targeted predecessor check, not an exhaustive novelty search. The optimal-kernel specialization is closely related to standard reproducing-kernel / moment-problem arguments and must not be promoted as a new foundational mechanism without further comparison.

## 5. Verification and implication

An independent exact-rational enumeration passed all 63 parameter triples with `1<=d<=6`, `a in {1/2,1/3,1/5}`, and `0<=k<d`: original normalization, positivity, every required marginal, target doubling, and chi-square identity; and the same properties for every kernel extension satisfying its condition. These checks support implementation of the formulas but do not replace the proofs or constitute external validation.

The consequential obstruction is acquisition: even extremely rich exact marginal information can leave rare-event probability statistically uncertain by a factor of two, with full-vector acquisition still costing order `1/p`. An escape must introduce a stronger, justified structural assumption or additional informative access. A local-computation speedup using trusted full independence does not remove this barrier.
