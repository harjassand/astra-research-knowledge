# Rare-event comparator audit

Audit date: 2026-10-10. Primary sources inspected online. Scope changed during the audit from local second-moment certificates to the proposed unknown-product-law / DNF composition. No claim of exhaustive novelty clearance or external mathematical validation.

## 1. Decisive comparator for the proposed product-law theorem

**Kuntz, Crucinio and Johansen, Product-form estimators: exploiting independence to scale up Monte Carlo, Statistics and Computing 32:12 (2022), published 21 December 2021.** [Primary article](https://link.springer.com/article/10.1007/s11222-021-10069-9), [arXiv](https://arxiv.org/abs/2102.11575).

Their estimator is exactly the proposed empirical product integral:

\[
\mu_\times^N(\varphi)=N^{-K}\sum_{n_1,\ldots,n_K=1}^N
\varphi(X_1^{n_1},\ldots,X_K^{n_K})=(\otimes_k\widehat\mu_k)\varphi.
\]

Theorem 1 proves unbiasedness for integrable functions, exact finite-sample variance for square-integrable functions, consistency and a CLT. Its Eq. (8), equivalently the orthogonal ANOVA decomposition, gives

\[
\operatorname{Var}(\mu_\times^N\varphi)
=\sum_{\emptyset\ne A\subseteq[K]}N^{-|A|}\|\varphi_A\|_{L^2(\mu)}^2.
\]

Here \(\varphi_A\) are the canonical centered Hoeffding components. Theorem 2 proves minimum variance among estimators unbiased for every product distribution. Corollary 2 combines product-form estimation with importance sampling. The paper identifies the estimator as a multisample U-statistic and explicitly distinguishes sample acquisition from exponentially expensive generic evaluation; factorized functions and sums of products permit cheaper computation.

**Novelty judgment:** the estimator and its basic finite-sample theory are established prior art. The proposed Bernoulli relative bound below was not located verbatim; it is a short specialization, not evidence of a new estimation principle.

## 2. Independent reconstruction of the proposed Bernoulli specialization

This section derives the specific statement received from the parent; it is not attributed as a literal theorem in the preceding paper.

Let \(P=\otimes_{j=1}^d\mathrm{Bern}(p_j)\), take \(n\) independent full vectors, and form unsmoothed empirical marginals \(\widehat P_j\). Assume \(0<p_j<1\), fixed \(f\ge0\), and \(Pf>0\). Put \(m_j=\min(p_j,1-p_j)\). Coordinatewise independence gives

\[
\mathbb E[\widehat P f]=Pf,\qquad
\frac{\mathbb E[(\widehat P f)^2]}{(Pf)^2}
\le C_n:=\prod_{j=1}^d\left(1+\frac{1/m_j-1}{n}\right).
\]

Proof: for a single coordinate with mass function \(q\),

\[
\mathbb E[\widehat q(x)\widehat q(y)]
=(1-1/n)q(x)q(y)+(1/n)q(x)\mathbf1_{x=y}.
\]

Its ratio to \(q(x)q(y)\) is \(1-1/n\) off the diagonal and \(1+(1/q(x)-1)/n\) on it. Tensorize, bound each factor by its largest diagonal value, and sum against the nonnegative weights \(f(x)f(y)P(x)P(y)\). The bound is **sharp**: choose \(f\) as the indicator of the full assignment taking the least-probable bit in every coordinate.

If \(p_j\in[a,1-a]\), this yields

\[
C_n\le\left(1+\frac{1-a}{na}\right)^d
\le \exp\!\left(\frac{d(1-a)}{na}\right).
\]

This removes rarity from the required training-sample count only because all coordinates are observed, true independence is supplied, each marginal atom is bounded below, and the event is fixed. Computing \(\widehat Pf\) remains a separate task.

Checks: a data-adaptively selected \(f\) is outside this statement; clipping or smoothing empirical marginals generally breaks exact unbiasedness. Raw empirical probabilities can be zero even when true probabilities are bounded away from zero.

## 3. Classical DNF computation and the proposed composition

**Karp, Luby and Madras, Monte-Carlo approximation algorithms for enumeration problems, Journal of Algorithms 10 (1989), 429–448.** [Primary paper PDF](https://www.math.cmu.edu/users/af1p/Teaching/MCC17/Papers/KLM.pdf), [DOI](https://doi.org/10.1016/0196-6774(89)90038-2).

Section 3 constructs a union estimator from component sizes, component sampling and membership tests. Section 5, p. 435, explicitly uses scores with conditional expectation equal to reciprocal coverage. Section 6, pp. 437–438, extends the scheme to DNF probability under arbitrary supplied independent Bernoulli probabilities. Its self-adjusting algorithm has an \((\epsilon,\delta)\) relative guarantee with work linear in input length times \(\epsilon^{-2}\log(1/\delta)\); the stopping-rule estimator is not necessarily unbiased. This is a stronger total-work comparator than repeatedly evaluating every clause solely to count coverage.

The fixed-budget reciprocal-coverage construction and the following composition are independently reconstructed from the proposed mechanism. For clause events \(A_i\), \(S=\sum_i Q(A_i)\), select clause proportional to its mass and sample conditionally. Its marginal proposal is \(Q(x)c(x)/S\), where \(c(x)\in\{1,\ldots,M\}\) on the union. Return \(Y=S/c(x)\). Then

\[
\mathbb E[Y\mid Q]=Q(A),\qquad
\frac{\mathbb E[Y^2\mid Q]}{Q(A)^2}
=\mathbb E_{Q(\cdot\mid A)}c\;\mathbb E_{Q(\cdot\mid A)}(1/c)
\le B_M:=\frac{(M+1)^2}{4M}.
\]

The last bound is the elementary Kantorovich bound for a random variable in \([1,M]\). Conditional averaging of \(L\) independent draws yields the factor \(1+(B_M-1)/L\). Setting \(Q=\widehat P\) and using Section 2 proves

\[
\frac{\mathbb E[\bar Y^2]}{P(A)^2}
\le C_n\left(1+\frac{B_M-1}{L}\right).
\]

If \(\widehat P(A)=0\), all empirical clause masses vanish and the correct conditional output is zero; no conditional sampler is invoked. Deduplicate/resolve contradictory literals first.

**Judgment:** mathematically useful repaired regime; no original foundational mechanism established. The exact combined bound was not found verbatim. It follows by composing known estimators and the conditional second-moment identity. A fair report must retain that distinction.

## 4. Exact local variance certificates are established prior art

**Blanchet and Glynn, Efficient rare-event simulation for the maximum of heavy-tailed random walks, Annals of Applied Probability 18 (2008), 1351–1378.** [Primary PDF](https://web.stanford.edu/~glynn/papers/2008/BlanchetG08.pdf), DOI 10.1214/07-AAP485.

Section 2 works on general measurable Markov state spaces. For target \(A\) inside the stopping boundary, proposal \(Q\), likelihood ratio \(r=dP/dQ\), define the killed second-moment operator \(Kg(x)=\int_{\mathrm{interior}}r(x,y)P(x,dy)g(y)\), and \(\eta(x)=\int_A r(x,y)P(x,dy)\). Theorem 2 says the second moment is the minimal nonnegative solution of \(s=\eta+Ks\), equals \(\sum_{k\ge0}K^k\eta\), and satisfies \(s\le g\) whenever finite \(g\ge0\) obeys \(Kg\le g-\eta\).

Theorem 1 describes the zero-variance Doob transform. Proposition 2 already treats approximate transforms \(Q(x,dy)=P(x,dy)v(y)/(Pv)(x)\) with a Lyapunov correction. Thus approximate committors plus local second-moment certificates are not new. Their computation, normalization, proposal sampling, and verification still require construction.

## 5. Local slack and HJB subsolutions

**Blanchet, Glynn and Leder, On Lyapunov inequalities and subsolutions for efficient importance sampling, ACM TOMACS 22(3), Article 13 (2012).** [Author publication record](https://web.stanford.edu/~glynn/papers/2012/BlanchetGLeder12.html), [inspected author preprint, 20 December 2009](https://web.stanford.edu/~jblanche/papers/LyapSub7_Dec20_2009.pdf).

Preprint Lemma 1: if \(e^\delta v(x)\ge E_P[r(x,X_1)v(X_1)]\), \(v\ge0\), and terminal \(v\ge\rho f^2\), then

\[
E_Q[e^{-\delta T}Z^2]\le v(x)/\rho.
\]

If \(T\le m/\delta\), then \(E_QZ^2\le e^m v(x)/\rho\). The proof uses a nonnegative supermartingale. Sections 4–5 explain how exponential tilting and limiting Isaacs subsolutions arise from these inequalities, and how prelimit Lyapunov bounds can sharpen mollified subsolution guarantees. Consequently even the “local residual accumulates over a bounded horizon” extension is explicit prior art.

## 6. Quantitative instability of approximate optimal diffusion controls

**Hartmann and Richter, Nonasymptotic bounds for suboptimal importance sampling, SIAM/ASA JUQ 12(2) (2024).** [Primary preprint](https://arxiv.org/pdf/2102.09606), [journal DOI](https://doi.org/10.1137/21M1427760).

Lemma 2.1 identifies squared relative error with \(\chi^2(P^*\Vert Q)\). For a controlled diffusion with actual control \(u\), optimal control \(u^*\), and \(\delta=u^*-u\), Proposition 3.3 expresses

\[
1+r(u)^2=E\exp\!\left(\int_0^T|\delta(X_s^{u+2\delta},s)|^2ds\right)
\]

under the paper's admissibility/Girsanov assumptions. Corollary 3.6 gives

\[
e^{\int h_1^2}-1\le r(u)^2\le e^{\int h_2^2}-1
\]

when \(h_1(t)\le|\delta(x,t)|\le h_2(t)\) uniformly. Componentwise error bounds \(\varepsilon_1,\varepsilon_2\) therefore give \(e^{dT\varepsilon_1^2}-1\le r^2\le e^{dT\varepsilon_2^2}-1\). These results already quantify dimension/horizon amplification. The optimal control remains unknown; a small empirical training loss does not supply the required global error bound.

## 7. Adaptive splitting comparator

**Cérou, Delyon, Guyader and Rousset, On the asymptotic normality of adaptive multilevel splitting (2019).** [Primary preprint](https://arxiv.org/pdf/1804.08494), [journal DOI](https://doi.org/10.1137/18M1187477).

Under Assumptions 1–3 (Feller regularity, strict entrance, and uniform positive success probability), Proposition 2.6 gives \(E[(\widehat p-p)^2]\le6/N\). Corollary 2.8 gives a CLT with

\[
\sigma^2=-p^2\log p-2\int_0^1\operatorname{Var}_{\eta_t}(q)\,p_t\,dp_t,
\qquad -p^2\log p\le\sigma^2\le2p(1-p).
\]

Here \(q\) is the committor and \(\eta_t\) the level-hitting law. Committor level sets minimize this asymptotic variance. This is not a uniform finite-N relative bound, and the optimal reaction coordinate requires solving the committor problem. Corollary 2.9 gives \(J=-N\log p+O_P(\sqrt N)\) for fixed problem as \(N\to\infty\); it does not charge arbitrary trajectory-generation cost or provide a joint dimension/rarity complexity guarantee.

## 8. Contemporary acquisition comparator

**Arief et al., Certifiable deep importance sampling for rare-event simulation of black-box systems (2021 preprint).** [Primary PDF](https://arxiv.org/pdf/2111.02204).

Theorem 3 combines orthogonally monotone event sets, learned one-sided set approximations and mixture tilting through dominating points. Its certificate deliberately estimates an upper bound: Definition 4 requires \(\Pr(\widehat\mu-\mu<-\epsilon\mu)\le\delta\) with sample count polynomial in \(\log(1/\mu)\) in their notation. It does not guarantee a tight relative estimate of the true event probability. Theorem 4's conservativeness bound contains a coverage term of order \(((\log n+d\log M+\log(1/\delta))/(nq_l))^{1/d}\), plus learning errors. Searching all dominating points and model construction are additional burdens. This is relevant positive prior art for acquisition-aware certification, with explicit structural and tightness restrictions.

## Research decision

The general local-certificate route and the empirical-product estimator both collide directly with established methods. The proposed product-law/DNF composition is a sound candidate for a reproducible, carefully scoped theorem-and-code package after independent checking, but it should be described as a derived combination with a sharp Bernoulli specialization, not an established historic breakthrough. The consequential barrier remains affordable learning and certification when the useful factorization or rare-event geometry is not supplied, particularly when hidden dependence changes exponentially rare probabilities.
