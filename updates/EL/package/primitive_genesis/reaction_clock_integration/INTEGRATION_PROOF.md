# Exact sparse clocks for uniformly reactive CRN batching

Status: internally reconstructed proof, with a numerical prototype. This is an algorithmic integration result in an idealized random-variate model; it is not a new distributional identity, a bit-complexity theorem, an implementation release, or an externally validated priority claim.

## 1. Result and early gate

The proposed compound-Poisson/gamma sampler has the correct distribution. More importantly, an equivalent sparse-geometric implementation samples exactly the same latent variables with no scan of the `k` rates. For fixed reaction order `o`, fixed uniform generativity `g >= 0`, and `k = O(sqrt(n))`, it uses an expected constant number of rate queries and random-variate operations. One binomial draw and a sparse scan resolve the fixed-time cutoff in expected constant work while preserving the joint law, provided exact binomial variates have uniformly bounded expected cost. A lazy beta tree provides an exact logarithmic-cost alternative with gamma primitives alone. Replacing the exact clock in Petrack--Doty Algorithm 5 removes its adaptive-rejection overhead, subject to the same discrete batching interface and an explicit bound on passive-event slowdown. The clock argument does not require repeated samples from one distribution.

The law of the clock remains valid after conditioning on a collision length because the uniformized total rate is independent of all embedded reaction choices. It does **not** remain valid after conditioning on a length chosen using the clocks themselves. A deterministic transformed-event block, as already used in Algorithm 5, is the cleanest integration interface.

The primary-source audit establishes that the underlying gamma series, geometric decomposition, and phase-type uniformization are classical. The potential contribution is the no-scan compiler for formula-specified close rates and its exact integration/cutoff proof, not those identities.

## 2. Source interface actually being replaced

The pinned source is Petrack and Doty, arXiv:2508.04079v2, revised 12 February 2026. Full source was downloaded. The relevant theorem and proof are in `sources/petrack_doty_v2/sections/making_time_work.tex`, lines 11--26 and 451--511. The fixed-time algorithm and correctness proof are lines 381--449; collision sampling and batch contents are in `sections/simulation.tex`. Section 7 is `sections/conclusion.tex` and has been read in full.

Theorem 5.1 has expected-time expression

\[
 O\!\left((2q)^o s\ell\log(n_{\max})/n_{\min}^{p}
       + n_{\max}^{2p/3}\ell^{1/3}\log(n_{\max})\right),\quad 0<p\le 1/2.
\]

Its second term comes from repeated exact hypoexponential sampling by adaptive rejection. The source assumes the claimed cube-root density-evaluation bound; the replacement below does not use that assumption. Algorithm 5 samples a deterministic block of `floor(n0^p)` **transformed events**, which can contain several collision batches and passive events. Its clock is therefore not conditional on an unknown ordering of original reaction types. Section 7 asks for a more efficient exact clock. [Paper](https://arxiv.org/html/2508.04079v2).

This replaces the exact theoretical branch. The implementation branch in Section 5.4 uses a moment-matched gamma approximation; a single uncorrected gamma is generally not exact.

## 3. Correct uniformization and the physical multiplier

Use the propensity convention

\[
 a_r(c)=\frac{k_r}{v^{|r|-1}}\prod_A {c(A)\choose r(A)}.
\]

Choose a uniform order `o>=max(1,maximum original reaction order)`, a uniform generativity `g>=max(0,maximum original generativity)`, and a catalyst count `m >= o`. For an original reaction with order `d`, add `delta=o-d` catalyst molecules to both sides and enough inert waste products to obtain generativity `g`. To preserve the displayed propensity convention, set

\[
 k'_r=k_r v^{\delta}/{m\choose\delta}.
\]

Let `kappa` be the maximum, over reactant multisets of size `o`, of the sum of the modified rate constants sharing that multiset. Add passive reactions to make every such sum `kappa`. A passive reaction returns its reactants and adds `g` waste molecules. Then, at an extended configuration of total population `N`, Vandermonde's identity gives

\[
 A'(N)=\frac{\kappa}{v^{o-1}}
       \sum_{|r|=o}\prod_A {c(A)\choose r(A)}
       = a{N\choose o},\qquad a=\kappa/v^{o-1}.
\]

Within one block, `m`, `kappa`, and `v` are held fixed. Every transformed event, active or passive, increases the total population by `g`, so its chronological total rates are exactly

\[
 \lambda_i=a{n+ig\choose o},\qquad 0\le i<k.
\]

The multiplier `a` must be charged and retained. It cancels from the probabilities used to compile the latent counts and scales the final gamma duration by `1/a`. When catalyst counts and rate constants are recomputed between blocks, `a` can change; block times are conditionally correct, not globally independent and identically distributed.

**Repairable source convention mismatch.** The source Eq. (1) uses binomial/factorial normalization, but Definition 2.7 and Algorithm 1 divide the catalyst correction by `m` falling-factorial `delta`, omitting `delta!`. With the source Eq. (1), a reaction padded by two catalyst molecules would run at half its original propensity. For example, a unary reaction padded to order three has an extra factor `binom(m,2)` and requires division by that binomial. This report uses the correctly normalized correction. Under the alternative no-factorial propensity convention, use the corresponding converted constants consistently. For fixed `o` the correction is a constant-factor normalization issue, not a change in the clock complexity.

**Projection proof.** Let `pi` delete catalysts and waste. For each active reaction, its propensity after padding is exactly its original propensity. A passive reaction has zero increment in `pi`. Thus, for every test function `f`,

\[
 Q'(f\circ\pi)(y)=(Qf)(\pi y).
\]

Resetting catalyst and waste counts at a block boundary preserves `pi` and this equality when rate constants are adjusted as above. Equivalently, while the projected configuration is `c`, its active hazards remain `a_r(c)` regardless of intervening passive events. Its next active holding time and active reaction selection therefore have the original Gillespie law. With nonexplosion, kernel composition proves the entire projected fixed-time law, including any number of reaction types.

For a joint claim about reaction counts, augment the original state by one counter for each labeled reaction. Its active transition increments the corresponding counter, while passive transitions increment none. The same generator identity then holds for test functions of both projected configuration and counters. This proves the joint count/configuration law, even for original reactions with no net state change. If syntactically identical transformed channels are combined, retain their labels by a proportional random split of their aggregate counts. Counts must be sampled from these same contents, not independently from the elapsed time or endpoint state.

## 4. Conditioning on a collision length

Fix the extended configuration and coefficients at a block start. Generate the embedded scheduler from a randomness stream `U`. Separately generate independent unit-rate exponentials `Z_0,Z_1,...`, independent of `U`, and put `T_i=Z_i/lambda_i`. Because `lambda_i` is deterministic given the start and the step index, the sequence `(T_i)` is independent of **the entire embedded scheduler**, not merely of each individual next-reaction choice.

Let `K` be any positive integer measurable with respect to `U` and the block-start information. In particular, `K` may be a collision-free run length, that length plus its collision, or a cap of that length. For every `k` with positive conditional probability and every measurable sets `B_0,...,B_(k-1)`,

\[
 \Pr(T_i\in B_i\ \forall i<k\mid K=k,U\text{-event})
   =\prod_{i<k}\Pr(\operatorname{Exp}(\lambda_i)\in B_i)
\]

whenever the conditioning event belongs to the embedded scheduler's sigma field. Therefore

\[
 H_K\mid\{K=k\}\ \overset d=\sum_{i=0}^{k-1}\operatorname{Exp}(\lambda_i),
\]

with independent summands. Reaction contents and the collision decision can be sampled before or after this clock, provided they retain their correct conditional law given `K`.

This fails if `K` is time-selected. For example, set `K=1` when `T_0>h` and `K=2` otherwise. Conditional on `K=1`, `T_0` is an exponential conditioned to exceed `h`, not an unconditional exponential. An adaptive physical-time cutoff must be sampled jointly, as in Section 7 below.

For a raw, untransformed CRN neither uniform order/generativity alone nor a nearly constant population is sufficient. For example, `A -> B` at rate 1 and `B -> A` at rate 100 conserve population but have state-dependent total intensity. A batch clock that ignores reaction types is invalid there. The passive-reaction uniformization is essential.

## 5. Exact count compiler: two equivalent constructions

Let positive rates `lambda_i <= b` be accessible by index. Define

\[
 p_i=\lambda_i/b,\quad q_i=1-p_i,\quad q_*=\max_i q_i<1.
\]

For the CRN formula with `g>=0`, `b=lambda_(k-1)` and `q_*=q_0`, so both are obtained from endpoints without searching.

### 5.1 Independent geometric stages

Independently let `G_i` have geometric law on nonnegative integers,

\[
 \Pr(G_i=m)=p_iq_i^m,\quad m=0,1,\ldots.
\]

Conditional on all `G_i`, let `Y_i` be independent `Gamma(1+G_i,b)` variables, using the shape/rate convention. For `s>=0`,

\[
 \mathbb E e^{-sY_i}
 =\sum_{m\ge0}p_iq_i^m\left(\frac b{b+s}\right)^{m+1}
 =\frac{p_i b}{s+b(1-q_i)}
 =\frac{\lambda_i}{s+\lambda_i}.
\]

The latent variables are independent across `i`, so the `Y_i` are independent exponentials with their respective required rates. Set `N=sum_i G_i`; then

\[
 H\mid(G_i)_i\sim\operatorname{Gamma}(k+N,b).
\]

Thus one gamma draw suffices once the sparse `G_i` have been compiled.

The no-scan compiler is:

1. Generate success indices of independent Bernoulli(`q_*`) variables on `0,...,k-1` by geometric gaps. Start at index `-1`; add independent `Geom1(success q_*)` gaps until the index is at least `k`.
2. At a candidate index `i`, query its rate and keep the candidate with probability `q_i/q_*`.
3. If kept, set `G_i=1+Geom0(success p_i)`; otherwise `G_i=0`. Indices not visited also have `G_i=0`.
4. Sum the kept extras and draw `Gamma(k+N,b)`. If needed for a cutoff, retain the sorted list `(i,G_i)`.

The compiler is exact: its nonzero indicator at each index is Bernoulli(`q_i`), independently across indices. Conditional on being nonzero, the specified positive geometric law gives `Pr(G_i=m)=p_i q_i^m` for every `m>=1`; its zero probability is `p_i`. Geometric gaps generate the same independent candidate indicators without examining the failures.

The expected number of queried candidate rates is exactly `k q_*`; the expected number of gap draws is `1+k q_*`; the expected number of stored nonzero indices is `sum_i q_i`; and

\[
 \mathbb E N=\sum_i\frac{q_i}{1-q_i}.
\]

No array of length `k`, coefficient product, density evaluation, or preprocessing scan is hidden in these bounds.

### 5.2 The proposed compound-Poisson construction

The pgf of `N` is

\[
 \mathbb E z^N=\prod_i\frac{1-q_i}{1-q_i z},\qquad
 \log\mathbb E z^N=\sum_i\sum_{r\ge1}\frac{q_i^r}{r}(z^r-1).
\]

Set `L_*=-log(1-q_*)`. Draw `M~Poisson(k L_*)`. For each of the `M` candidates choose an independent uniform index `I` in `0,...,k-1` and a logarithmic-series mark

\[
 \Pr(R=r)=q_*^r/(rL_*),\quad r\ge1.
\]

Accept with probability `(q_I/q_*)^R` and add `R` to the latent count at index `I`. Poisson marking and thinning give independent counts of accepted marks `(i,r)` with means `q_i^r/r`. Consequently the resulting `G_i` have the independent geometric laws above, and the final gamma is exact.

For completeness, a log-series mark can be generated by proposing `R~Geom1(success 1-q_*)` and accepting with probability `1/R`. The acceptance probability is `(1-q_*)L_*/q_*`, at least `1-q_*`. For close rates it is uniformly bounded below. If integer powering costs `O(log R)`, then this expected cost is also bounded because `E R` is bounded in the regime below. A Poisson variable of bounded mean can itself be sampled by elementary inter-arrival accumulation in bounded expected work. Thus the compound-Poisson version need not hide a rate scan or a new difficult primitive. The sparse-geometric version is simpler and avoids the Poisson and log-series steps.

## 6. Resource bounds for formula-specified rates and random lengths

Suppose `n>=2o`, with fixed `o,g`. Let `d=(k-1)g`. Then

\[
 1-q_* = \frac{{n\choose o}}{{n+d\choose o}}
        =\prod_{h=0}^{o-1}\frac{n-h}{n+d-h},
\]

and the product/union bound and `log(1+x)<=x` imply

\[
 q_*\le\frac{o g(k-1)}{n-o+1},\qquad
 -\log(1-q_*)\le\frac{o g(k-1)}{n-o+1}.
\]

Hence for `k<=C sqrt(n)`, both candidate expectations are `O(k^2/n)=O(1)`. Also `q_*=O(n^-1/2)` and

\[
 \mathbb E N\le k q_* /(1-q_*)=O(1).
\]

Each queried binomial uses `O(o)` arithmetic operations. With fixed `o` this is constant. The multiplier `a` affects only the final gamma scale. Conservative `g=0` and `k=1` have `q_*=0` and reduce exactly to one Erlang/gamma draw. Small populations can use an exact sequential fallback of constant size depending on `o,g,C`.

Uncapped random collision length is also affordable in expectation. Starting with no red molecules, let `L` be the number of collision-free reactions. The scheduler gives

\[
 \Pr(L\ge m)=\prod_{j=0}^{m-1}\prod_{h=0}^{o-1}
    \frac{n-oj-h}{n+gj-h},\quad L\le\lfloor n/o\rfloor.
\]

As long as the product is nonzero, each factor is at most `exp(-o j/n)`, so

\[
 \Pr(L\ge m)\le \exp[-o^2 m(m-1)/(2n)].
\]

Tail summation gives `E[(L+1)^r]=O_r(n^(r/2))` for every fixed positive integer `r`; in particular `E[(L+1)^2]=O(n)`. For `K=L+1` or a smaller cap, the candidate-query bound therefore has expectation `O(1)`. Moreover `K<=floor(n/o)+1` implies

\[
 \frac b{\lambda_0}
 \le \left(1+\frac{g n}{o(n-o+1)}\right)^o
 \le (1+2g/o)^o,
\]

so the count compiler's mark and extra-count expectations remain uniformly bounded after averaging over `K`. Random length causes no hidden linear cost.

These are bounds on arithmetic and random-variate operations and rate queries. They are not constant **bit** complexity. Candidate indices need `Theta(log k)` bits; binomial integers have `Theta(o log n)` bits; latent counts are unbounded, although their expected magnitude in this regime is bounded. Exact continuous samples require a random-real/stream representation or an explicit finite-output approximation contract. The proof assumes exact real arithmetic, exact uniforms, and uniformly bounded expected-cost gamma draws for shape at least 1; beta draws below are ratios of two such gammas. The stronger cutoff bound additionally assumes a uniformly bounded expected-cost binomial primitive at arbitrary integer size and real probability. This is consistent with the source's multinomial random-variate model, but is an explicit interface assumption here. A random-bit implementation must pay for deciding a binomial with probability `u/H`, especially near decision boundaries. Finite-precision logarithms, gamma routines, and probabilities in `clock_prototype.py` are diagnostic implementations only. No bit-exact implementation or uniform precision bound has been proved here.

## 7. Exact fixed-time cutoff from sparse gamma stages

A root duration alone is insufficient to determine the configuration at an interior physical time. Independent resampling of a shorter clock after observing that the root crosses the horizon can give the wrong conditional law. Retain the sparse latent `G_i` from Section 5 instead.

Put `a_i=1+G_i` and `A=sum_i a_i=k+N`. Conditional on the `G_i`, the required stage durations are independent `Gamma(a_i,b)`. Their sum is `Gamma(A,b)`, and their normalized proportions are a `Dirichlet(a_0,...,a_(k-1))` vector, independent of that sum. This follows directly by changing variables from positive stage durations to their total and simplex proportions: the joint gamma density factors into the gamma density of the total and the Dirichlet density of the proportions.

Therefore, first drawing the root total `H` and then allocating it with this Dirichlet law reproduces the full joint vector of independent exponential clocks after the `G_i` are marginalized. In particular, it preserves correlations between the endpoint timestamp and all prefix counts.

### 7.1 One binomial and a sparse scan

Because the shapes `a_i` are integers, represent stage `i` as the sum of `a_i` independent exponential microphases at rate `b`. There are `A=k+N` microphases. Conditional on their total `H=h`, their `A-1` interior arrival times are the order statistics of `A-1` independent uniform points on `(0,h)`. This follows either from the constant density of their normalized `Dirichlet(1,...,1)` spacings or by conditioning the product exponential density on its sum.

For `0<=u<h`, draw

\[
 W\mid(G_i)_i,H=h\sim\operatorname{Binomial}(A-1,u/h).
\]

This is exactly the number of interior microphase arrivals by `u`. The `j`th original stage finishes at microphase index

\[
 C_j=j+\sum_{i<j}G_i,\qquad 0\le j\le k.
\]

Consequently the desired original-stage prefix count is

\[
 J=\max\{j:C_j\le W\}.
\]

This samples the exact joint distribution of `(G,H,J)`, not just a marginal approximation for `J`. If `u>=H`, return `J=k`; if `u=0`, return `J=0`.

The inverse can be computed without inspecting all `k` stages. Initialize `J=W`. Scan sorted nonzero marks `(i,g_i)`. If `i>=J`, stop. Otherwise replace `J` by `max(i,J-g_i)` and continue. To prove the update, suppose earlier extras have already been removed from the microphase index. The next marked stage starts after original-stage index `i`; an index after its completion shifts down by `g_i`, an index inside that stage maps to `i`, and an index before the stage is unaffected. Those are exactly the three cases in the update. Induction over the sorted marks proves the inverse formula. At completion `0<=J<k` because `W<A`.

There is one binomial call and `O(1+M)` arithmetic work, where `M` is the number of retained nonzero stages. Thus the terminal cutoff costs expected `O(1)` per attempted block under the stated binomial primitive, with expected `O(1)` extra words. This is an unconditional per-attempt bound; conditioning on an exceptional overshoot can bias `M` upward. For several cut times inside the same retained root, sample microphase counts jointly by a multinomial law or compatible conditional binomial splits. Independent fresh binomials at different cuts would lose the joint law.

### 7.2 Beta-tree alternative without a binomial primitive

To locate `J=max{j<=k:sum_(i<j) T_i<=u}`:

* If `u>=H`, return `J=k`.
* Otherwise keep an interval `[l,r)` with its total duration `V` and remaining target `w` satisfying `0<=w<V`. Split at `m=floor((l+r)/2)`. Let `A_L=m-l+sum_(l<=i<m)G_i` and `A_R=r-m+sum_(m<=i<r)G_i`.
* Draw `B~Beta(A_L,A_R)`, set `V_L=B V`. If `w<V_L`, descend to `[l,m)` with `(V_L,w)`. Otherwise descend to `[m,r)` with `(V-V_L,w-V_L)`.
* At a singleton interval `[j,j+1)`, return `J=j`.

Both beta shapes are positive integers. The beta-split identity for independent same-rate gammas proves the correctness at each split. More formally, one can pre-sample all independent beta variables of the full binary allocation tree; the algorithm reveals only the path selected by the target. Adaptive revelation of this pre-existing tree does not change its law. Thus the terminal `J` has exactly the same joint distribution with `H` and the latent counts as sequential exponential simulation.

There are at most `ceil(log2 k)` splits. If `M` sparse nonzero indices are stored, a direct scan of the marks computes the shapes in `O(1+M)` work per level. The work is `O((1+M)log(k+1))` and memory is `O(1+M)` for an iterative single-query descent. Under Section 6, expected cutoff work per **attempted block** is `O(log(k+1))`. Do not assert a uniform bound conditioned on a rare crossing event: conditioning on an extremely large `H` can bias latent counts upward. The unconditional per-attempt bound suffices for the simulation theorem and is valid at every predictable block start. For multiple queries in one retained clock, store previously revealed tree nodes rather than redraw them.

### 7.3 Poisson microphase alternative for an integer prefix interface

A related uniformization route avoids generating a continuous root when only a single finite-block prefix count is needed. Given the latent marks, extend the independent rate-`b` microphases to a homogeneous Poisson process. At a supplied horizon `u`, draw

\[
 W\sim\operatorname{Poisson}(bu)
\]

independently of the marks. Return `J=k` if `W>=A`; otherwise apply the same sparse inverse `J=max{j:C_j<=W}`. This is exactly the number of original stages completed by `u`, capped at the finite block length. It is an integer-output interface with no root-duration comparison. With rational `bu` and an exact rational-parameter Poisson sampler it could be implemented without a continuous output, but no such bit-complexity implementation is established here.

If the endpoint duration is also required, its correct conditional law is explicit. When `W>=A`, the `A`th arrival among the `W` points in `(0,u)` has law

\[
 H\mid G,W\ overset d=\ u\operatorname{Beta}(A,W-A+1).
\]

When `W<A`, independent increments after `u` instead give

\[
 H\mid G,W\ overset d=\ u+\operatorname{Gamma}(A-W,b).
\]

Together these laws recover the same exact joint `(G,H,J)` distribution. In a full simulator a completed block still needs its duration to update the remaining horizon, so this alternative alone does not resolve continuous-time random-bit costs between blocks. A bounded expected-cost Poisson primitive at arbitrary mean `bu` is an additional assumption for constant real-model work; the compound-Poisson clock compiler in Section 5 only needed Poisson means bounded by a constant. Large Poisson counts also have an explicit integer-size cost. This is another use of classical phase-type uniformization, not a new distributional identity.

### Random collision length caveat at the cutoff

If a random length `K=L+1` was chosen from the scheduler, `J<K` lies inside a collision-free prefix. One must preserve this scheduler conditioning. It is generally wrong to discard `K` and sample an unconditional `J`-event embedded path, which would allow collisions. One can sample the first `J` disjoint original-molecule interactions under the conditional collision-batch law, because the future red/green collision probabilities depend only on their deterministic counts. If already materialized endpoint contents have been exposed, their conditional prefix must also be preserved.

Using Algorithm 5's deterministic transformed-event block avoids this issue entirely: `J` is independent of all embedded scheduler randomness. An ordinary exact `J`-event discrete simulation then has precisely the right law, including collisions.

## 8. Full fixed-time integration theorem and proof

Here is a self-contained integration statement with an explicit resource interface, rather than an unqualified transfer of every convention in the source theorem.

**Assumptions.** Fix a finite mass-action CRN and fixed volume. Let `tau` be the first time the original total propensity is zero; that state is absorbing. Until `min(t,tau)`, assume the original population is almost surely between deterministic bounds `n_min` and `n_max`, with `n_min` above a fixed small-population threshold. These are promises about the unconditional process law, not conditioning on a randomly selected future trajectory that happens to stay in range. Uniformize each block with the corrected constants in Section 3; retain fixed `m,kappa` within that block, and choose extended start population `n=Theta(original population)` and a deterministic block size `k=Theta(sqrt(n))`. Maintain these comparisons with constants depending only on the fixed network. Assume, before `tau`, the total transformed intensity satisfies

\[
 A'(Y_s)\le\rho A(\pi Y_s)\qquad(0\le s<\min(t,\tau))
\]

for some `rho>=1`. This is the precise passive-event slowdown condition. It is not removed by the clock improvement. Import the source's exact collision-batching content routine, whose cost is `D(n_max)=O(C_net log(n_max+2))` per collision batch in its idealized multinomial/hypergeometric model; for the displayed source comparison one may use its `(2q)^o` network factor. Charge initialization and network preprocessing separately as `I_net`.

**Algorithm.** At a block start, if the original total propensity is zero, return the same original state for the remaining horizon. Otherwise compile sparse counts and the root clock for the next deterministic `k` transformed events. If the root fits in the remaining horizon, simulate exactly `k` transformed embedded events by collision batching, advance time by the root, reset catalyst/waste as specified, and continue. If it crosses the horizon, locate `J` by Section 7, simulate exactly `J` transformed embedded events, project, and halt. Track active event counts from those same sampled contents if event counts are part of the requested output. The terminal test costs only the fixed-network propensity calculation and is charged to the block content work.

**Distributional proof.** At each block start, Section 3 gives the correct extended generator. Section 4 permits the whole length-`k` clock vector to be generated independently of the embedded scheduler. Section 5 gives its exact root law and latent representation. Section 7 gives the exact joint prefix count when the horizon lies inside the block. Since `k` is deterministic from the start information, `J` is independent of the embedded scheduler; simulating its first `J` events therefore produces the exact state at the horizon. When the whole block fits, the joint pair of endpoint state and endpoint time is also correct. Applying these correct conditional kernels after each block endpoint proves equality with the extended Gillespie law. Projecting gives the original fixed-time law by the generator identity. This is a proof for a changing population and any finite number of reaction types, not just for a single reaction repeated `k` times.

**Nonexplosion proof in the bounded regime.** During a block, extended population is at most `n+gk=O(n_max)`. Catalyst counts and corrected constants belong to bounded ranges determined by the fixed network, `v`, and the population bounds. Total transformed intensity is therefore bounded above by a finite constant depending on these inputs. Infinite transformed events before finite time have probability zero. If the original process becomes terminal inside a block, all subsequent projected increments are zero; at the next block boundary the algorithm detects this and halts. It need not detect the absorbing event inside aggregate batch contents. Alternatively the displayed slowdown bound and compensator argument below give finite expected event count when `E L_t<infinity`. No claim is made for exact detection of explosion or for sampling the cemetery state of arbitrary explosive CRNs.

**Expected collision-batch calls per block.** A collision-free run from a fresh color reset has probability bounded below by a positive constant of covering any remaining cap `r<=C sqrt(n)`. To see this, use the product in Section 6 and, for `j<=C sqrt(n)` and sufficiently large `n`, bound each ratio below by `1-C'j/n`; summing logarithms gives a constant lower bound `exp(-C'')`. Current population throughout the block remains within a constant factor of its start. At each fresh collision-batch call there is thus a uniform positive conditional probability of completing the remaining block. The number of calls is stochastically dominated by a geometric variable of constant mean. This argument counts **all transformed events** and does not assume independent active/passive labels.

**Event-count accounting.** Let `M_pre` be the number of transformed events through `min(t,tau)`, including the event that first reaches an absorbing original state, let `L_t` be the number of original active reactions by time `t`, and let `B` be the number of attempted deterministic clock blocks. Every full block entirely before `tau` completes at least `c sqrt(n_min)` transformed events. At most one attempted block straddles `tau`, and at most one block crosses `t`, so pathwise

\[
 B\le 2+M_{\rm pre}/(c\sqrt{n_{\min}}).
\]

The compensator identities and the slowdown assumption give

\[
 \mathbb E M_{\rm pre}=\mathbb E\int_0^{t\wedge\tau} A'(Y_s)\,ds
 \le\rho\,\mathbb E\int_0^{t\wedge\tau} A(\pi Y_s)\,ds
 =\rho\,\mathbb E L_t.
\]

Thus `E B=O(1+rho E L_t/sqrt(n_min))`. Conditional on every predictable block start, clock compilation and binomial terminal search each cost `O(1)` in expectation, and content sampling costs `O(D(n_max))` in expectation. Iterated conditional expectation, summing over the event that each block is reached, gives

\[
 \boxed{\quad
 \mathbb E\operatorname{work}
 =O\!\left(I_{\rm net}
 +[D(n_{\max})+1]
       \left(1+\frac{\rho\,\mathbb E L_t}{\sqrt{n_{\min}}}\right)\right).
 \quad}
\]

With the gamma/beta-only fallback, replace `[D(n_max)+1]` by `[D(n_max)+log(n_max+2)]`. Both versions give the displayed source-factor comparison below. There is no density-evaluation setup, repeated-distribution requirement, cube-root amortization, or terminal `sqrt(n_max)` scan in this theorem. Extra clock storage is expected `O(1)` words for one query. Counts and network state retain the storage of the discrete sampler. Random variate outputs and integer sizes remain subject to the model boundary in Section 6.

The source's scheduler factor `s` is intended to provide a bound of this kind after network-dependent padding constants. For a literal displayed-theorem comparison, retain the source's discrete batching and slowdown accounting as assumptions and replace only its second term. More generally, every fixed `0<p<=1/2` allows `k=Theta(n^p)`, with bounded expected clock work and the same geometric collision-batch bound; the denominator in the resource theorem becomes `n_min^p`. Choosing `p=1/2` is then optimal for the displayed upper bound and yields the candidate corrected counterpart

\[
 O\!\left(I_{\rm net}+(2q)^o\log(n_{\max}+2)
       \left[1+\frac{s\,\mathbb E L_t}{\sqrt{n_{\min}}}\right]\right).
\]

The additive startup/output term matters for very short runs, including zero-reaction runs; a runtime proportional only to `ell` cannot describe those cases. The rigorous statement above uses expected event counts because a fixed physical horizon generally produces a random reaction count. If a deterministic event budget `ell` is supplied through an existing discrete-simulation interface, use its corresponding event-budget accounting rather than silently treating the random count at a fixed time as a deterministic input.

For fixed network, bounded slowdown, and `n_min=Theta(n_max)=Theta(n)`, the bound is `tilde O(1+ell/sqrt(n))`, where `ell=E L_t`. It is `tilde O(1)` for `ell<=sqrt(n)` and `tilde O(ell/sqrt(n))` above that threshold. In particular it holds throughout the source's `n<=ell<n^(5/4)` regime as well as its longer-run regime. The source's `n^(2/5)` speedup at `ell=Theta(n)` becomes a `sqrt(n)` speedup in this matched model. This is the concrete extra complexity removed. These are unconditional expected-cost comparisons under the stated promises; no pathwise or conditional runtime guarantee is inferred by selecting trajectories after the fact. The first Section 7 question, passive-event slowdown at low reactant counts or disparate rates, remains unresolved.

## 9. What is and is not being output

A fixed transformed-event endpoint can be returned with its exact total timestamp and compressed reaction counts. A fixed physical-time configuration can be returned with the exact event count by the cutoff procedure. In the original CRN, original active-event count and transformed-event count are different quantities; the latter includes passive events. The formula `lambda_i=a binom(n+ig,o)` must count transformed events.

For a stopping index defined by an original active-reaction budget, its conditional clock law is valid only over a segment with a fixed uniformized generator, and scheduler conditioning must be retained. A reset of catalyst/waste or rate scale starts a new segment. One cannot simply replace `k` by the number of original active reactions in one hypoexponential formula.

Producing every original reaction identity and every timestamp takes at least linear output work. The claimed sublinear simulation concerns configurations, aggregate counts, and sparse observations, not an explicit full trajectory.

## 10. Primary prior-art comparison

The following is a bounded primary-source audit, not an exhaustive priority certification.

* **Moschopoulos (1985), pp. 542--543, Eqs. (2.3)--(2.9), all four scanned pages inspected.** Gives a positive gamma-series for sums of independent gammas and the same logarithmic transform coefficients `sum_i alpha_i q_i^r/r`. The present exponential-shape case is a specialization. Its stated procedure computes series coefficients recursively and evaluates/truncates the series; it does not state the no-scan, indexed sparse compiler or the CRN integration. [Publisher PDF](https://www.ism.ac.jp/editsec/aism/pdf/037_3_0541.pdf).
* **Devroye (1986), Chapter V, Theorem 2.2, pp. 209--210; Chapter X, Section 4, pp. 533--536.** The exponential/uniform spacing identity underlying the binomial cutoff is classical. The book discusses uniformly bounded expected binomial generation with squeeze methods or a unit-cost log-gamma function. The primitive is explicitly charged here rather than reproduced. [Author-hosted spacings chapter](https://luc.devroye.org/chapter_five.pdf), [author-hosted discrete distributions chapter](https://luc.devroye.org/chapter_ten.pdf).
* **Fiems (2024), Sections 2--3, full accepted manuscript read.** Uses phase-type uniformization, a discrete absorption count, and one gamma draw. Its generic alias approach has stated setup `O(k^3 M)` and table construction/storage `O(k(k+M))`, with generation reduced by the precomputed step parameter `M`. It supplies a strong existing exact gamma/count baseline but not the formula-oracle resource bound here. [Accepted manuscript](https://backoffice.biblio.ugent.be/download/01JQ282GP9CDPEPHEVAC52EAEN/01JQ28DPAN7K3EXP3AP616M7XM), [publication and DOI](https://biblio.ugent.be/publication/01JQ282GP9CDPEPHEVAC52EAEN).
* **Mjolsness et al. (2009), Sections 2.4--2.5, full primary preprint acquired and relevant derivation/cost proof read.** ER-leap proposes multinomial reaction counts and an Erlang total; a conditional simplex allocates times when exact rejection evaluation is needed. Its per-attempt cost is `O(R+(1-E P_early) k R)`. The late acceptance step examines ordered trajectories. This overlaps the use of a gamma total and conditional allocation but does not provide the sparse latent geometric count law or a universal no-scan bound for the uniformized clock. [Author-hosted full preprint](https://computableplant.ics.uci.edu/papers/2009/Exact_R_LeapTR08_09.pdf).
* **Orendorff and Mjolsness (2012), Sections 2--3, primary preprint acquired and relevant exact construction read.** HiER-leap retains the Erlang/conditional-simplex idea and exploits a hierarchy of reaction channels. It addresses additional network structure rather than formula-specified near-equal phase rates. [Primary preprint](https://arxiv.org/abs/1212.4080).
* **Cai and Wen (2009), Sections III--IV, author-uploaded full paper passages read.** Its exact DMK/ODMK still draws a clock and updates the state for each reaction; K-skip replaces the sum of clocks by an approximate gamma. Therefore its gamma shortcut is not a matched exact no-scan clock. [Author-uploaded full text](https://www.researchgate.net/publication/26752143_Efficient_exact_and_K-skip_methods_for_stochastic_simulation_of_coupled_chemical_reactions), [publication record](https://pubmed.ncbi.nlm.nih.gov/19691379/).
* **Berenbrink et al. (2020), full arXiv preprint acquired, Sections 1 and 3--4 and Appendix B relevant proofs read.** Supplies the exact collision-batching approach in a fixed-size population. The varying-rate clock issue is absent for uniformly conservative continuously timed interactions: it is already Erlang. This is the proper discrete baseline, not a reason to claim a new batching method. [Primary preprint](https://arxiv.org/abs/2005.03584), [published version](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2020.16).

Consequently, the answer to “is all this already a prior method?” is split. The law and major probabilistic operations are prior. The explicit expected constant **rate-query** compiler for endpoint-bounded formula rates, with a fully charged exact cutoff and the matched Petrack--Doty complexity substitution, is not supplied by the inspected methods. It is a legitimate candidate algorithmic improvement to that theorem, with external novelty and bit-exact implementation still open.

## 11. Verification and remaining gates

`clock_prototype.py` numerically implements sparse geometric compilation, the binomial cutoff, and the lazy beta fallback. For both cutoff methods it checks the joint law of the endpoint timestamp and prefix count against an analytic Yule-process formula and checks a two-type changing-population CRN against independent Yule laws. It also exhaustively checks the sparse microphase decoder on a finite integer range and records candidate-query scaling for `o=2,g=1,k=floor(sqrt(n))`. Results are in `validation_results.json`. The prototype needs Python 3.12 or later for its numerical binomial routine. These checks can find implementation/correlation mistakes; they do not certify an exact floating-point implementation or replace the proofs.

Remaining gates are external mathematical review of this integration, a broader priority search for sparse phase-type compilers and lazy Dirichlet bridges, and a precisely specified exact-random-bit or bounded-error implementation. The exact real-random-variable theorem and its stated query accounting do not depend on those empirical checks. Passive slowdown, unbounded/explosive original networks, and explicit full-path output are outside the improved guarantee.
