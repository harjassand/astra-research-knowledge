# Independent audit of the near-equal-rate hypoexponential clock

Audit date: 2026-10-12. Role: independent proof, falsification, cost and prior-art audit. All proofs below were reconstructed directly from transforms and elementary bounds; a source theorem is not used as a premise.

## Verdict

The proposed Gamma mixture and marked-Poisson sampler are correct. For

\[
\lambda_i=\binom{n+ig}{o},\quad 0\le i<k,\quad
n\ge o\ge1,\quad g\ge0,
\]

with fixed integer `o,g`, a deterministic cap `k <= c sqrt(n)`, and the sharp endpoint rate `b = lambda_(k-1)`, the correction stage uses a bounded expected number of proposals and rate evaluations, without enumerating the rates. An explicit Gamma rejection sampler below has fewer than two proposals in expectation uniformly over every integer shape, including shape one. Consequently the unconditional clock can be sampled in bounded expected elementary-real/word operations in the stated model.

This is **not** a deterministic bound on every execution, a constant bit-operation bound, a certified floating-point implementation of the exact continuous law, or an established new probability representation. The Gamma mixture is classical; the logarithmic compound-Poisson mechanism is classical; thinning is classical. The potentially useful contribution is the specialized small-correction implementation and its integration into the structured clock problem. Priority for that implementation remains unverified.

The exact finite discrete stage can avoid both logarithms and a logarithmic-series primitive by the rational envelope in Section 3. A lazy exact-continuous implementation appears feasible, but no verified lazy-real implementation or complete end-to-end bit-complexity theorem is delivered by this audit.

## 1. Exact distribution, independently derived

Let `k >= 1`, let the deterministic rates `lambda_i > 0` be finite, and let

\[
T=\sum_{i=0}^{k-1}X_i,\qquad X_i\sim\operatorname{Exp}(\lambda_i)
\]

independently. Pick `b >= max lambda_i` and define

\[
q_i=1-\lambda_i/b\in[0,1),\qquad z(s)=b/(b+s).
\]

For `s >= 0`, direct algebra gives

\[
\frac{\lambda_i}{\lambda_i+s}
=z(s)\frac{1-q_i}{1-q_i z(s)}.
\]

Let `G_i` be independent nonnegative geometric variables with

\[
\Pr(G_i=r)=(1-q_i)q_i^r,\quad r\ge0,
\qquad N=\sum_iG_i.
\]

Their product PGF is

\[
F_N(z)=\prod_i\frac{1-q_i}{1-q_i z}.
\]

Sample `N`, then independently sample `Y | N ~ Gamma(k+N, rate b)`. The Laplace transform of `Y` is

\[
\mathbb E[e^{-sY}]=z(s)^k F_N(z(s))
=\prod_i\frac{\lambda_i}{\lambda_i+s}
=\mathbb E[e^{-sT}].
\]

Uniqueness of the Laplace transform of a probability measure on `[0,infinity)` proves `Y =_d T`. Repeated rates and `q_i=0` cause no problem.

Expanding the elementary logarithm series, absolutely convergently for `|z| <= 1`,

\[
\log F_N(z)
=\sum_i\sum_{r\ge1}\frac{q_i^r}{r}(z^r-1).
\]

Thus `N` is a compound-Poisson variable with Levy masses

\[
\nu(i,r)=q_i^r/r,\qquad
\Lambda=\sum_i-\log(1-q_i)<\infty.
\]

This argument establishes the full law, including every tail; it is not a moment match or a truncated expansion.

As independent checks,

\[
\mathbb EN=\sum_i\frac{q_i}{1-q_i},\quad
\operatorname{Var}N=\sum_i\frac{q_i}{(1-q_i)^2},
\]

and therefore

\[
\mathbb ET=\frac{k+\mathbb EN}{b}=\sum_i\lambda_i^{-1},
\quad
\operatorname{Var}T=
\frac{k+\mathbb EN+\operatorname{Var}N}{b^2}
=\sum_i\lambda_i^{-2}.
\]

These checks do not replace the transform proof.

## 2. The proposed logarithmic-series thinning is exact

Let `Q = max_i q_i`. If `Q=0`, return `N=0`; the logarithmic-series formula is undefined at zero, so this branch is required.

For `0<Q<1`, let `L=-log(1-Q)` and:

1. Draw `M ~ Poisson(k L)`.
2. Independently for each candidate, draw `I` uniformly from `{0,...,k-1}` and a positive jump `R` with `Pr(R=r)=Q^r/(r L)`.
3. Keep that candidate with probability `(q_I/Q)^R` and add its jump if kept.

Before thinning the Poisson intensity at each `(i,r)` is

\[
(kL)\,(1/k)\,Q^r/(rL)=Q^r/r.
\]

After thinning it is `q_i^r/r`, exactly the Levy mass from Section 1. Independence of disjoint marked Poisson counts proves the output law.

One rate evaluation per candidate is sufficient. No sum over rates or Levy coefficients is required if `b,Q` are certified by the structured input.

The logarithmic-series primitive is also not intrinsically expensive when `Q <= 1/2`: propose `R` from the positive geometric law `(1-Q)Q^(r-1)` and accept with probability `1/r`. Its acceptance probability is `(1-Q)L/Q`, so its expected number of attempts is

\[
Q/[(1-Q)L]\le 1/(1-Q)\le2.
\]

The proposed jump has mean `Q/[(1-Q)L]`; the expected sum of all candidate jumps is

\[
\mathbb E\sum_{j=1}^M R_j=kQ/(1-Q).
\]

Consequently even implementing `(q_i/Q)^r` as `r` independent rational Bernoulli tests has bounded expected total work in the near-equal-rate regime.

## 3. A rational proposal removes the logarithmic-series routine

For rational rates, the following equivalent construction has a simpler exact-discrete interface:

\[
\mu=\frac{kQ}{1-Q}.
\]

Draw `M ~ Poisson(mu)`. For each candidate draw a uniform `I` and positive geometric `R` with

\[
\Pr(R=r)=(1-Q)Q^{r-1}.
\]

Accept with probability

\[
\frac1r\left(\frac{q_I}{Q}\right)^r.
\]

The intensity before thinning is

\[
\mu(1/k)(1-Q)Q^{r-1}=Q^r,
\]

and after thinning it is again `q_i^r/r`. This proves the full law independently of any approximate Poisson or Gamma library.

For integer endpoint rates `a=min lambda_i`, `b=max lambda_i`, write `D=b-a`. Then

\[
Q=D/b,\quad \mu=kD/a,\quad q_i/Q=(b-\lambda_i)/D.
\]

Every parameter in this discrete stage is rational. Compute differences as integer differences, rather than subtracting two nearly equal floating-point ratios.

The expected candidate count is `kQ/(1-Q)`. The expected total number of proposed jump units is

\[
\mathbb E\sum_{j=1}^M R_j=kQ/(1-Q)^2.
\]

Both are bounded if `Q <= 1/2` and `kQ=O(1)`.

## 4. Endpoint bounds for the binomial rate family

Assume `o,g` are fixed nonnegative integers, `n >= o`, and `k >= 1`. If `o=0` or `g=0` or `k=1`, all rates coincide and the correction is identically zero. Otherwise let

\[
h=(k-1)g,\quad a=\binom n o,\quad b=\binom{n+h}{o},
\quad A=\frac{oh}{n-o+1}.
\]

Monotonicity of the binomial coefficient on integer arguments at least `o` proves that these are the minimum and maximum rates. Only these two rates have to be evaluated. The product formula gives

\[
\log(b/a)
=\sum_{j=0}^{o-1}\log\left(1+\frac{h}{n-j}\right)
\le\sum_{j=0}^{o-1}\frac{h}{n-j}
\le A.
\]

Therefore

\[
Q=1-a/b\le\log(b/a)\le A,
\quad
k[-\log(1-Q)]=k\log(b/a)
\le\frac{ogk(k-1)}{n-o+1}.
\]

For a deterministic cap `k <= c sqrt(n)`, this is bounded uniformly for all sufficiently large `n`, with constants depending on `o,g,c`. No enumeration is hidden in the bound. A finite initial range of `n` can be handled by the same exact sampler or a direct sum; the asymptotic constant may depend on the fixed parameters.

When `A <= 1/2`, the rational envelope satisfies

\[
\mu=\frac{kQ}{1-Q}\le2kA,
\quad
\mathbb E\sum R_j\le4kA.
\]

If `k/sqrt(n) -> c`, then for fixed positive `o,g`,

\[
k\log(b/a)\longrightarrow ogc^2,
\quad
\Lambda=\sum_i\log(b/\lambda_i)\longrightarrow ogc^2/2.
\]

Moreover the mass of jumps of size at least two is at most

\[
\sum_i\sum_{r\ge2}q_i^r/r
\le \frac{kQ^2}{2(1-Q)}=O(n^{-1/2}).
\]

Thus `N` converges to `Poisson(og c^2/2)`. This limit is a useful sanity check; replacing `N` by that limiting Poisson would only be an approximation at finite `n`.

For fixed negative `g`, reverse the endpoint roles and use the minimum population `n+(k-1)g` in the denominator, provided it is at least `o`. If it stays comparable to `n` and `k=O(sqrt(n))`, the same asymptotic conclusion follows. The primary application takes `g>=0` after its CRN transformation.

## 5. Gamma sampling with a proof of bounded expected work

The Gamma primitive must not be implemented by adding `m` exponentials when `m=k+N`. The following independently derived rejection construction uses fewer than two proposals in expectation for every integer `m>=1`.

For a prospective `Gamma(m,1)` variable make the change of variables

\[
y=m\exp(z/\sqrt m).
\]

Its transformed density is proportional to

\[
h_m(z)=\exp\{\sqrt m z-m(\exp(z/\sqrt m)-1)\}.
\]

The log of `h_m` is concave, has maximum zero at `z=0`, and has derivative

\[
\ell_m'(z)=\sqrt m(1-\exp(z/\sqrt m)).
\]

At `z=-1`, putting `t=1/sqrt(m) in (0,1]` gives

\[
\ell_m'(-1)=(1-e^{-t})/t\ge1-e^{-1}>1/2.
\]

At `z=1`, `-ell_m'(1)=(e^t-1)/t >= 1`. Concavity and `ell_m(+-1)<=0` therefore prove the universal envelope

\[
h_m(z)\le e(z):=
\begin{cases}
\exp((z+1)/2),&z<-1,\\
1,&-1\le z\le1,\\
\exp(-(z-1)),&z>1.
\end{cases}
\]

The envelope has masses `2,2,1`, total `5`. Sample `Z` from `e/5` using a categorical draw with probabilities `2/5,2/5,1/5`:

- Left: `Z=-1-2E`, where `E~Exp(1)`.
- Center: `Z=2U-1`, where `U~Uniform(0,1)`.
- Right: `Z=1+E`, where `E~Exp(1)`.

Accept with probability `h_m(Z)/e(Z)` and return `Y=m exp(Z/sqrt(m))`. The change of variables computes the unnormalized integral exactly:

\[
I_m=\int_{\mathbb R}h_m(z)\,dz
=\frac{\sqrt m\,\Gamma(m)e^m}{m^m}.
\]

The usual lower Stirling bound for the integer factorial, applied to `m!` and divided by `m`, gives

\[
\Gamma(m)\ge\sqrt{2\pi}\,m^{m-1/2}e^{-m}.
\]

Hence `I_m>=sqrt(2 pi)`, acceptance is at least `sqrt(2 pi)/5`, and the expected number of proposals is at most

\[
5/\sqrt{2\pi}<1.995.
\]

**Shape one is included.** Directly, `I_1=e`, acceptance is `e/5`, and expected proposals are `5/e`. There is no singular `m-1` expression in this construction.

An implementation should evaluate the rejection threshold as

\[
D_m(z)+\log e(z),\quad
D_m(z)=m[\operatorname{expm1}(z/\sqrt m)-z/\sqrt m],
\]

and accept when an independent `Exp(1)` exceeds that nonnegative threshold. For tiny arguments use a stable remainder series for `expm1(t)-t`; subtracting two nearly equal floating-point numbers can corrupt the numerical acceptance test. Stability is not a proof of an exact floating-point output law.

The elementary construction is supplied to close a primitive cost in the real-operation model, not as a priority claim for a Gamma generator. Uniform expected-time Gamma generation has a long-established literature, including Marsaglia and Tsang (2000).

## 6. Cost model and exactness boundary

### 6.1 Rate evaluation and acquisition

For fixed `o`, evaluate `binom(x,o)` with `o` integer multiplications and divisions. Values have `O(o log(n+kg))` bits. Under unit-cost word/elementary-real arithmetic this is `O(1)`; under schoolbook integer arithmetic a conservative bound is `O((log n)^2)` bit operations in the capped regime.

An arbitrary explicit list of `k` rates does not come with free certified endpoints. Reading and validating such an input can cost `Omega(k)`. The sublinear claim uses a compressed, known rate formula or an evaluator supplied with a valid envelope. It does not solve the acquisition problem for unrestricted rate arrays.

### 6.2 Exact finite discrete stage

Use Section 3 with `mu=kD/a`, not a floating-point Poisson mean. To avoid assuming an exact Poisson library, split `mu` into `J=ceil(mu)` equal means `x=mu/J<=1` (the `mu=0` branch returns zero). `J` is bounded in the regime under consideration.

For each `Poisson(x)`, propose `R>=0` with `Pr(R=r)=2^(-r-1)` and accept with probability

\[
e^{-x}\frac{(2x)^r}{2r!}.
\]

The rational factor `(2x)^r/(2r!)` is at most one for all `x<=1`. Multiplying proposal mass by acceptance gives `e^(-x)x^r/(4r!)`; total acceptance is exactly `1/4`, and the accepted value is exactly `Poisson(x)`.

An exact `Bernoulli(e^(-x))` decision uses rational alternating Taylor upper/lower bounds and a lazily revealed uniform bit stream. At depth `j`, the bracket between the most recent even and odd partial sums has width at most `1/j!`; a `j`-bit uniform interval adds at most `2^(1-j)` to the probability of an unresolved comparison. The refinement depth therefore has bounded moments, uniformly for `x in [0,1]`.

Generate a rational Bernoulli coin `u/v` by an exact uniform integer in `{0,...,v-1}` and comparison with `u`. Standard rejection from `ceil(log2 v)` bits has fewer than two attempts in expectation. Generate candidate jumps by repeated `Bernoulli(Q)` continuation; these have mean `1/(1-Q)<=2`. Generate the power acceptance by `r` independent coins `(b-lambda_i)/D`, together with the `1/r` coin. Their total expected count is bounded by Section 3.

With `L=O(log n)` input bit lengths, this supplies a concrete finite-discrete algorithm with expected `O(L)` fair bits and conservative expected `O(L^2)` bit operations using schoolbook rational/integer arithmetic. The unbounded proposal integers and Taylor denominators have rapidly decreasing tails; no fixed maximum bit length is asserted. `audit_checks.py` implements this discrete reference mechanism with exact Python fractions and a reproducible PRNG in place of ideal fair bits.

### 6.3 Continuous output

A finite floating-point number cannot have the exact non-atomic hypoexponential law. More generally, any algorithm that terminates with a finite bit string interpreted as an ordinary rational or float has countable support. Exactness requires an exact-real model or an explicit lazy random-real output interface.

For the Gamma envelope, rejection decisions terminate almost surely under lazy computable-real arithmetic: the independent acceptance threshold has a continuous distribution and hence equals the computed threshold with probability zero. The selected proposal can be retained as an expression using `m,b`, a categorical branch, and a partially revealed uniform bit stream.

There is a plausible polynomial-cost route to obtaining `p` requested bits. For example,

\[
D_m(z)\le\tfrac12 z^2e^{\max(z,0)},\qquad
|D_m'(z)|\le |z|e^{\max(z,0)},
\]

uniformly for `m>=1`. The fixed proposal has exponentially decreasing tails in `|z|`; the independent exponential acceptance threshold has density at most one. With certified interval algorithms for `exp`, `log`, `sqrt`, and the stable remainder, these observations control refinement and suggest expected `poly(log n+p)` bit work. They do not by themselves certify an unimplemented interval engine, a production implementation, or the total precision needed after many clock additions and horizon comparisons.

**Status:** an implementability outline, not a completed or verified end-to-end bit theorem. Any final claim of a bit-exact CRN simulator must specify and implement the lazy-real interface, arithmetic, precision policy, and cutoff comparison logic.

### 6.4 Every-execution versus expected work

For `Q>0`, the proposed Poisson candidate count has unbounded support. For every fixed cap `B`, `Pr(M>B)>0`. The Gamma rejection count is also unbounded. These algorithms therefore do not have a deterministic constant runtime bound on every execution. Truncating either loop silently changes the law unless a correct fallback completes the work.

There are useful tail bounds. For the rational envelope, with `Q<=Q0<1` and `mu<=C`, the total proposed jump sum `J_total` has a uniformly bounded exponential moment for any `t<-log(Q0)`:

\[
\mathbb E e^{tJ_{\rm total}}
=\exp\left\{\mu\left(\frac{(1-Q)e^t}{1-Qe^t}-1\right)\right\}.
\]

Together with geometrically decreasing Gamma rejection counts, this gives logarithmic high-probability operation caps, not a sure cap. Exact-bit integer rejection and precision refinement add their own tails.

## 7. A simpler classical baseline: sparse nonzero geometricals

The identity `N=sum_i G_i` also permits a construction without compound Poisson machinery:

1. Generate independent Bernoulli candidate indicators `B_i~Bernoulli(Q)` by geometric skipping over `k` positions, or by a binomial count and a uniform subset.
2. At a candidate position `i`, keep it with probability `q_i/Q`.
3. At each kept position add `1+H_i`, where `H_i~Geom0(1-q_i)` independently.

The kept indicators are independent `Bernoulli(q_i)`. Their positive geometric sizes yield exactly `Pr(G_i=r)=(1-q_i)q_i^r`. Expected candidates are `kQ`; expected positive geometric work is bounded when `Q<=1/2`.

This is a strong simplicity/novelty baseline. It reaches the same rate-query bound with standard sparse Bernoulli thinning. A claim that the compound-Poisson representation is necessary for the speedup would be false.

**Important implementation distinction:** the skip length is positive geometric with small success probability `Q`, so drawing it by repeated Bernoulli trials costs `Theta(1/Q)` and loses the speedup. Inverse logarithms give bounded elementary-real work. An exact-bit skip needs a certified inverse/interval comparison algorithm; expanding large rational powers can itself create `Theta(k log n)`-bit integers. The rational compound-Poisson construction avoids that particular difficulty because its jump continuation probability is small, so its jump lengths have bounded mean.

## 8. Decisive counterexamples to overbroad claims

1. **Arbitrary upper endpoint:** if all `lambda_i=1` but `b=2`, then `Q=1/2` and the original candidate mean is `k log 2`. Thus `b>=max lambda_i` alone does not imply fast sampling, even for equal rates. The close endpoint choice is essential.
2. **Only an expected batch length:** let `K=n` with probability `n^(-1/2)` and `K=1` otherwise. Then `E K=Theta(sqrt(n))`, but for `o=g=1` the expected original candidate count is `Omega(sqrt(n))`. A first-moment batch-length statement cannot replace a deterministic cap or suitable second-moment/tail control.
3. **Growing order or generativity:** if `o` or `g` grows with `n`, the fixed-parameter spread bound need not be small. For example `g=Theta(sqrt(n))`, `k=Theta(sqrt(n))`, and fixed positive `o` produce a constant rate ratio and `Theta(k)` candidate work.
4. **Naive Gamma generation:** summing `k+N` exponentials makes Gamma generation `Theta(k)` despite a bounded correction stage.
5. **Finite PRNG and floats:** reproducible code with finite-state pseudorandomness and finite floats is a numerical implementation, not literal sampling from the exact continuous law.
6. **Conditional terminal batch:** the unconditional marginal clock sampler alone does not sample the constituent waiting times conditioned on crossing a horizon, nor the number of completed reactions at that horizon. A correct bridge or separate conditional/rejection procedure is required.
7. **Unknown rate input:** an unverified rate evaluator or upper envelope is not free data. Invalid `Q` can make thinning probabilities exceed one and destroys exactness.

## 9. Primary-source comparison and novelty status

The complete relevant original Moschopoulos pages were read, including scanned equations on pages 542-544. The primary sources below, not secondary summaries, support this comparison.

- **Moschopoulos (1985), The distribution of the sum of independent gamma random variables, AISM 37, 541-544.** Equations (2.3)-(2.7), Theorem 1, and its coefficient recursion contain precisely the Gamma-series mixture behind Section 1, in more general Gamma-shape parameters. The paper develops coefficient recursion and truncation; no no-enumeration marked thinning sampler for this binomial rate family was located in its four pages. [Original publisher PDF](https://www.ism.ac.jp/editsec/aism/pdf/037_3_0541.pdf).
- **Vellaisamy and Upadhye (2009), On the sums of compound negative binomial and gamma random variables, JAP 46, 272-283.** Theorem 2.3 and Remark 2.3 explicitly give the compound-Poisson/logarithmic-series representation; Theorem 3.1 gives a random-shape Gamma representation. Thus neither the discrete infinite-divisibility mechanism nor the random-shape interpretation can be claimed as new. [Original journal PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6222343EDD3B18402C190D2C5310F445/S0021900200005350a.pdf/on-the-sums-of-compound-negative-binomial-and-gamma-random-variables.pdf).
- **Lewis and Shedler (1979), Simulation of nonhomogeneous Poisson processes by thinning.** Dominating a Poisson intensity and deleting points by an intensity ratio is established simulation machinery. [Original journal page](https://onlinelibrary.wiley.com/doi/pdf/10.1002/nav.3800260304).
- **Petrack and Doty (2025), Exactly simulating stochastic chemical reaction networks in sub-constant time per reaction, arXiv:2508.04079v1.** Section 5.1 uses a partial-fraction density plus adaptive rejection across repeated clocks; Section 5.4 replaces the exact clock by a moment-matched Gamma in practice. The rate family is exactly the one audited here. Section 5.1 assumes a favorable adaptive-rejection evaluation rate and uses bounded molecular count to repeat the same law. The present small-correction sampler does not require learning that density. [Primary article, Sections 5.1-5.4](https://arxiv.org/html/2508.04079v1#S5).
- **Marsaglia and Tsang (2000), A simple method for generating gamma variables.** Large-shape Gamma generation without summing all exponentials is established. [Author institutional record](https://hub.hku.hk/handle/10722/89056), [DOI](https://doi.org/10.1145/358407.358414).
- **Kemp (1981), Efficient generation of logarithmically distributed pseudo-random variables.** Efficient logarithmic-series generators are established, separately from this specialized thinning choice. [Original journal page](https://academic.oup.com/jrsssc/article/30/3/249/6954031).
- **Devroye and James, The Double CFTP method (2010 preprint; published 2011).** Exact generalized-Gamma-convolution sampling is also established in a much broader setting. Its general construction does not automatically give a parameter-uniform constant cost for large total shape; the paper explicitly exhibits deterioration in a large-shape Dirichlet-mean example. [Author-hosted primary PDF](https://luc.devroye.org/devroye-james-doublecftp.pdf).

Targeted primary-source searches did not locate an earlier explicit constant-rate-query sampler for this particular near-equal binomial family. That is a bounded literature observation, **not** a priority result, exhaustive novelty certification, or proof that a paper-sized contribution exists. The simple sparse-geometric competitor especially lowers the novelty ceiling: an efficient integration theorem and a trustworthy implementation may be the main remaining value.

## 10. Reproducible evidence

`audit_checks.py` contains two kinds of checks:

- Exact rational comparisons of finite coefficient prefixes computed by independent geometric convolution and compound-Poisson recursion, exact first/second moment identities, and rate-envelope inequalities.
- Seeded numerical comparisons with directly summed independent exponentials, the explicit Gamma rejection envelope at shapes `1,2,10,10000,10^8`, and proposal-count scaling from populations `100` through `10^8`.

`audit_results.json` records results and the script hash. Monte Carlo is only a numerical sanity check; the full-law and cost conclusions rest on the proofs above. The reference Gamma code uses floating arithmetic and is not an interval-certified exact sampler. The rational discrete reference uses Python fractions, but its seeded PRNG is not an ideal infinite independent-bit source.

The recorded run passed 1,924 exact coefficient comparisons across 148 fixtures and 180 endpoint-bound fixtures. The three direct-exponential comparisons used 30,000 samples per method and had two-sample KS distances `0.00717`, `0.00880`, and `0.00533`. The rational-discrete scaling check used 4,000 samples at each of four population sizes; its theoretical candidate means were `1.89091`, `1.98990`, `1.99900`, and `1.99990`. Gamma checks used 20,000 samples for each of five shapes, including `1` and `10^8`; all declared numerical sanity checks passed. A sample average may exceed an expectation bound through sampling fluctuation, so these data are not used to prove the uniform Gamma bound.

Run with the bundled Python containing NumPy:

```text
/Users/harjas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 /Users/harjas/Documents/ChatGPT/astra/research/2026-10-12-primitive-genesis/gamma_clock_adversary/audit_checks.py
```

No commit, push, source modification, external messaging, or subagent launch was performed. All new files from this audit are inside `gamma_clock_adversary/`.
