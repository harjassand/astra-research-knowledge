# P1 completed return

Chat: https://chatgpt.com/c/6af1a606-c6c8-83ec-b948-b552107573bf
Actual human continuation: Please continue. (e018337d-e4ff-4bbb-ad97-a01113b68040)
Preceding exact scientific question: work/astra-renewed-pro-programmes-20261103/P1_FULL_BATCH_MINIMAX_AFTER_91EA_C9_XI_20261110.txt (source SHA256 e456b27e508b21962f5e5f575d52c361c14bbb8281678bf7105dfe247c06f401; actual posted composer SHA256 d4de5eee63f8086fa8cc30fdb17e30838db74e5b8f1e46d736df5cae739761bd).
Response: cac733fc-13d6-4199-9c89-64194487bc17. GPT-6 Standard and Extra High verified at scientific-question send; model throughout continuation not independently established. No ZIP identified in visible return.

## Available user-visible activity

Worked for 38m 45s. Explored and developed exact coupling strategies; refined adaptive coupling through pooled count-level matching; investigated shared-state factories and designed adaptive count archives. Searched the web.

> The fixed-archive route appears to have a stronger limitation than the accepted independent-length theorem: with deterministic source and target sample budgets, universal exactness forces a specific conditional distribution given both histograms. I’m testing whether this yields a rigorous optimality statement for the entire fixed-budget class, including algorithms that rearrange records more cleverly than the standard matcher.

Analyzed binary reductions and evaluated coupling limits; evaluated parallel coupling strategies and strengthened archive results. Searched the web.

> I have a rigorous fixed-budget result: when the algorithm is allowed exactly N − m extra P-samples and N fresh Q-samples, the standard N-archive matcher is optimal among all universally exact algorithms with those budgets, not merely among histogram matchers. The proof uses uniqueness of the Bernstein coefficients in both unknown laws. I’m also checking a convexity identity that would settle whether independently randomizing the archive size helps in expectation.

Established budget optimality, matching bounds, fixed-budget limits, and budget frontiers; strengthened budget bounds and established capped-budget results; proved fixed-budget limits.

## Complete response as returned

# Continuation: an exact fixed-budget optimality theorem

The accepted unrestricted minimax bounds remain

\[
\boxed{
c\left(m+\frac{d+\sqrt{md}}{\eta}\right)
\le C^*(d,m,\eta)
\le C\min\left\{\frac{md}{\eta},\ m+\frac d{\eta^2}\right\}.
}
\tag{1}
\]

I have not closed this all-regimes gap. The strongest new result I can establish is an **exact optimality theorem covering every algorithm with fixed balanced source-query caps**, not just the known histogram matcher.

## 1\. Exact optimality of the fixed archive

**Theorem.** Fix any \(N\ge m\)\. Consider all source-rate-free algorithms that satisfy the exact \(Q^m\) requirement and, on every execution, make at most

\[
N-m\text{ fresh }P\text{ calls},\qquad N\text{ fresh }Q\text{ calls}.
\]

Their expected changed fraction is necessarily at least

\[
\boxed{
D_N(P,Q)=
\mathbb E\operatorname{TV}
\left(\widehat P_N,\widehat Q_N\right).
}
\tag{2}
\]

The accepted \(N\)\-record archive matcher attains equality **simultaneously for every \(P,Q\)**\.

This remains true if the algorithm adaptively interleaves its calls, exploits both complete sample orders, uses arbitrary fair-bit computations, or tries a different transport rule.

It is not merely optimal among histogram matching algorithms.

### Exact minimax consequence

Using the accepted empirical-excess extremum,

\[
\sup_{P,Q}\{D_N(P,Q)-\operatorname{TV}(P,Q)\}
=\delta(d,N),
\]

we obtain

\[
\boxed{
\inf_{\substack{\text{universally exact algorithms}\\
N_P\le N-m,\ N_Q\le N\ {\rm a.s.}}}
\sup_{P,Q}
\left\{\mathbb E[\text{changed fraction}]
-\operatorname{TV}(P,Q)\right\}
=\delta(d,N).
}
\tag{3}
\]

Thus the precise feasibility condition for these deterministic query budgets is

\[
\boxed{\delta(d,N)\le\eta.}
\]

Define the computable integer

\[
N_{\min}(d,m,\eta)
=\min\{N\ge m:\delta(d,N)\le\eta\}.
\]

Within this balanced-budget model, the minimum total number of new calls needed to obtain the required universal accuracy is exactly

\[
\boxed{2N_{\min}(d,m,\eta)-m.}
\tag{4}
\]

This is a complete optimality result for fixed balanced budgets. The unrestricted problem can do better by using adaptive unbounded stopping, so (4) is **not** a proposed formula for \(C^*\)\.

## 2\. Proof: two-law Bernstein coefficient rigidity

The proof gives a stronger conditional statement than the mismatch bound.

Pre-sample, for analysis, complete independent lists

\[
U=(X_1,\ldots,X_m,U_{m+1},\ldots,U_N)\sim P^N,
\qquad Z\sim Q^N.
\]

The algorithm may inspect only the prefixes it actually requests. Unused entries are analytical padding, not charged algorithmic resources.

Let \(A=\operatorname{hist}(U)\), \(B=\operatorname{hist}(Z)\)\. For every output word \(y\in[d]^m\), write

\[
K_{a,b}(y)=\Pr(Y=y\mid A=a,B=b).
\]

Conditional on both histograms, the two complete source lists are independently uniform over their respective type classes. Consequently \(K_{a,b}(y)\) is independent of the numerical source probabilities.

Universal exactness gives

\[
\sum_{a,b}
\operatorname{Mult}(N,p;a)
\operatorname{Mult}(N,q;b)K_{a,b}(y)
=\prod_{j=1}^m q_{y_j}.
\tag{5}
\]

First apply uniqueness of the degree-\(N\) multinomial Bernstein representation in \(p\)\. Since the right-hand side does not depend on \(p\), every coefficient indexed by \(a\) must equal the same expression in \(q\)\.

Next apply uniqueness in \(q\)\. Writing \(v_i(y)\) for the number of occurrences of \(i\) in \(y\), one obtains

\[
\boxed{
K_{a,b}(y)=
\frac{\prod_{i=1}^d(b_i)_{v_i(y)}}{(N)_m}.
}
\tag{6}
\]

Here \((r)_k=r(r-1)\cdots(r-k+1)\)\.

The right-hand side is precisely the probability of obtaining the ordered word \(y\) by sampling \(m\) elements without replacement from a population with histogram \(b\)\.

In particular,

\[
\boxed{
Y\ \perp\ A\mid B
}
\tag{7}
\]

for every algorithm in this fixed-budget class.

Conditionally on \(A=a,B=b\), each original coordinate has marginal \(a/N\), whereas each output coordinate has marginal \(b/N\)\. The coupling inequality then gives

\[
\Pr(Y_j\ne X_j\mid A=a,B=b)
\ge\operatorname{TV}(a/N,b/N).
\]

Averaging proves (2). The archive matcher attains equality, completing the theorem.

This argument handles arbitrary zero probabilities by first proving the polynomial identity in the full-support simplex and then restricting to feasible boundary histograms.

## 3\. An even broader fixed-budget characterization

The balanced requirement is not necessary for coefficient rigidity.

Suppose the deterministic caps instead are \(r-m\) fresh \(P\)\-calls and \(s\) fresh \(Q\)\-calls, with \(r,s\ge m\)\. After padding, let the full histograms be \(a,b\), of sizes \(r,s\)\.

The same argument forces

\[
\mathcal L(Y\mid A=a,B=b)
=\operatorname{HypergeomWord}(b,s,m),
\]

while

\[
\mathcal L(X\mid A=a,B=b)
=\operatorname{HypergeomWord}(a,r,m).
\]

Define \(\mathsf H_{r,a}^{(m)}\) as the distribution on count vectors \(c\), \(|c|=m\), with

\[
\mathsf H_{r,a}^{(m)}(c)
=
\frac{\prod_i\binom{a_i}{c_i}}{\binom rm}.
\]

Then define the finite optimal-transport problem

\[
\mathcal W_m(a,r;b,s)=
\min_{\pi\in\Pi(\mathsf H_{r,a}^{(m)},\mathsf H_{s,b}^{(m)})}
\sum_{c,t}\pi(c,t)\,
\frac{\|c-t\|_1}{2m}.
\tag{8}
\]

**Exact fixed-budget classification\:**

\[
\boxed{
\inf_{\mathcal A}\mathbb E[\text{changed fraction}]
=
\mathbb E_{A\sim\operatorname{Mult}(r,P),\,
B\sim\operatorname{Mult}(s,Q)}
\mathcal W_m(A,r;B,s).
}
\tag{9}
\]

The infimum is attained by one universal parameter-free algorithm: compute the rational optimal transport of the conditional hypergeometric count distributions, sample the coupled output type, and uniformly align as many original labelled positions as possible.

The resulting conditional output word distribution is the required hypergeometric law, so averaging over \(B\) produces exact \(Q^m\)\.

Thus (9) is not just a lower bound; it is an exact characterization, with a computable finite rational transport algorithm, for **every pair of deterministic source-query caps**\.

When \(r=s=N\),

\[
\mathcal W_m(a,N;b,N)=\operatorname{TV}(a/N,b/N),
\]

recovering the efficient archive matcher.

The distinction for unequal budgets is real. For \(d=2,m=2\), take \(r=2,a=(1,1)\) and \(s=4,b=(2,2)\)\. The normalized full histograms agree, so their TV is zero, yet

\[
\mathcal W_2(a,2;b,4)=\frac16.
\]

The target prefix sometimes has two equal labels, whereas the original prefix necessarily has one of each.

## 4\. New deterministic \(Q\)\-cap obstruction

There is a separate consequence that does **not** restrict the number of fresh \(P\)\-calls.

**Theorem.** If a universally exact algorithm makes at most \(s\) fresh \(Q\)\-calls on every run, with arbitrary adaptive and unbounded \(P\)\-sampling permitted, then

\[
\boxed{
\mathbb E[\text{changed fraction}]
\ge
\mathbb E_{B\sim\operatorname{Mult}(s,Q)}
\operatorname{TV}(P,B/s).
}
\tag{10}
\]

Indeed, pad the \(Q\)\-stream to length \(s\) and condition only on its histogram \(B=b\)\. Bernstein uniqueness in \(q\) alone forces

\[
\mathcal L(Y\mid B=b)
=\operatorname{HypergeomWord}(b,s,m).
\]

The original \(X\) is independent of the entire fresh \(Q\)\-stream. Hence, conditional on \(B=b\), each original coordinate still has law \(P\), while the corresponding output coordinate has law \(b/s\)\.

At \(P=Q=\operatorname{Unif}[d]\), (10) gives

\[
\eta\ge
\frac d{2s}\mathbb E\left|
\operatorname{Bin}(s,1/d)-s/d
\right|.
\tag{11}
\]

The accepted fourth-moment estimate now yields

\[
\boxed{
s\ge\frac{d-1}{16\eta^2}
\qquad(0<\eta\le1/8).
}
\tag{12}
\]

This is the \(Q\)\-only counterpart of the accepted \(P\)\-only deterministic-cap obstruction. Even unlimited adaptive \(P\)\-queries cannot compensate for too small a deterministic target-query cap.

It also clarifies why the accepted one-original-row algorithm, whose expected cost is \(O(d/\eta)\), cannot be replaced by an equally cheap deterministically capped target sampler.

## 5\. Exact convexity: random archive lengths cannot help in the independent-horizon class

A further new result strengthens the accepted independent-random-archive expected-cost barrier.

**Theorem.** For every \(d\ge2\), the integer sequence

\[
n\longmapsto\delta(d,n)
\]

has a strictly decreasing, strictly convex extension to all real \(n>0\)\.

### Proof

Put

\[
u=\frac{d-1}{d^2},\qquad
a(t)=1-2u(1-\cos t).
\]

Since \(d\ge2\), we have \(0\le a(t)\le1\)\. The accepted characteristic-function identity for independent binomial count differences gives

\[
\delta(d,n)=
\frac d{2\pi}
\int_0^\pi
\frac{1-a(t)^n}{n(1-\cos t)}\,dt.
\tag{13}
\]

For \(0<a<1\), observe that

\[
\frac{1-a^n}{n}
=(-\log a)\int_0^1a^{nv}\,dv.
\tag{14}
\]

For each \(v\in[0,1]\), the function \(n\mapsto a^{nv}\) is decreasing and convex. At \(a=0\), the integrand's numerator divided by \(n\) becomes \(1/n\), which is also decreasing and convex.

Integrating against the nonnegative weight in (13) proves the claim.

### Sharp expected-cost implication

Now choose a nonnegative integer archive extension \(K\) independently of both entire source streams, including the original \(X\)\. Require exact output law \(Q^m\) conditional on each possible \(K=k\), and cap the conditional calls by \(k\) fresh \(P\) and \(m+k\) fresh \(Q\)\.

The exact fixed-budget theorem shows that the smallest worst-case mismatch excess within this class equals

\[
\boxed{\mathbb E[\delta(d,m+K)].}
\tag{15}
\]

The fixed archive matcher at each realized size attains equality. Convexity gives

\[
\boxed{
\mathbb E[\delta(d,m+K)]
\ge \delta(d,m+\mathbb EK).
}
\tag{16}
\]

More precisely, for a prescribed real mean \(\mathbb EK\), the optimal integer-valued distribution for \(K\) is supported on the two adjacent integers surrounding that mean. It is never beneficial to introduce a heavy-tailed independent archive length.

This settles the exact expected-cost trade-off for that class, rather than only proving an order-\(d/\eta^2\) barrier.

The distinction in scope remains important: the theorem does not cover a horizon selected adaptively from the \(P/Q\) observations, or exactness obtained only after mixing different stopping outcomes.

## 6\. Computational realization

The balanced-budget optimum is computably uniform with explicit finite local work.

Let \(B\) denote the combined binary input length and set

\[
N_{\max}
=\max\left\{
m,\left\lceil\frac{d-1}{2\eta^2}\right\rceil
\right\}.
\]

The previously accepted upper estimate guarantees \(\delta(d,N_{\max})\le\eta\)\.

The exact rational value of \(\delta(d,n)\) can be evaluated using

\[
\delta(d,n)=
\frac{d}{2n\,d^{2n}}
\sum_{a,b=0}^n
|a-b|\binom na\binom nb
(d-1)^{2n-a-b}.
\tag{17}
\]

Because \(\delta(d,n)\) decreases, exact integer arithmetic and binary search find \(N_{\min}\) in finitely many steps. No real-valued probability evaluation is needed.

After that, the attaining algorithm acquires the \(N_{\min}-m\) additional \(P\) observations and \(N_{\min}\) fresh \(Q\) observations, then performs the exchangeable archive matching and projects onto the original \(m\) positions.

A conservative uniform upper bound on expected local bit work, including parameter construction and exact integer sampling, is

\[
\boxed{
O\bigl((N_{\max}+d+B+1)^8\bigr).
}
\tag{18}
\]

The working memory can be bounded by

\[
O\bigl(N_{\max}(\log(N_{\max}+2)+\log(d+2))+B\bigr)
\]

bits, including the stored original and output lists. Fair-bit rejection for finite uniform integer choices has a finite expected number of attempts.

For unequal fixed budgets, the hypergeometric optimal transport in (8) is a finite rational linear program. Exact rational min-cost flow or exhaustive vertex enumeration gives a computably uniform implementation, although its complexity can be exponential in the number \(\binom{m+d-1}{d-1}\) of possible output types.

For fixed \(d\) and \(n\to\infty\), the central limit theorem additionally yields the sharp asymptotic

\[
\delta(d,n)\sim\sqrt{\frac{d-1}{\pi n}}.
\]

Thus, for fixed \(d,m\) as \(\eta\downarrow0\), the balanced fixed-budget optimum has

\[
N_{\min}(d,m,\eta)\sim\frac{d-1}{\pi\eta^2}.
\]

These are explicit algorithms and complexity bounds for the new restricted results. They are not a substitute for the still-missing unrestricted minimax attaining algorithm.

## 7\. Updated scientific status

| Result | Status |
|--------|--------|
| One-original-row \(C^*(d,1,\eta)=\Theta(d/\eta)\) | Accepted, complete |
| Exact \(C^*=m\) threshold via \(\delta(d,m)\) | Accepted, complete |
| Unrestricted expected lower \(\Omega(m+(d+\sqrt{md})/\eta)\) | Accepted, complete |
| Exact conditional-output law for any two deterministic source caps | **New, proved** |
| Exact optimal transport and cost for those fixed budgets | **New, proved** |
| Sharp convexity and independent random-horizon optimality | **New, proved** |
| Deterministic \(Q\)\-only cap barrier with unrestricted \(P\)\-sampling | **New, proved** |
| Matching unrestricted expected-query upper and lower | **Open** |

The most consequential new mathematical finding is the **two-law Bernstein rigidity theorem**\: at fixed source budgets, exactness determines the entire conditional target-word distribution given the two observed histograms, and optimal transport then determines the best achievable original-row retention. There is no improvement available through a more sophisticated fixed-budget algorithm.

This establishes that any improvement over the \(O(m+d/\eta^2)\) archive upper bound must genuinely exploit adaptive stopping or another mechanism outside those fixed-budget constraints.

It does not prove that such an improvement exists. In particular, I have obtained neither a construction matching \(\Omega(m+(d+\sqrt{md})/\eta)\) nor a stronger unrestricted expected-query lower bound that closes the gap.

**The full all-regimes minimax question therefore remains open, with the accepted bounds in (1) unchanged.**
