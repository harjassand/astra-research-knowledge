# Independent check: rare branch versus scalar Esscher tilting

Date: 2026-10-15. Scope: exact mathematical model, an independent internal proof, and deterministic numerical checks. No other worker output was read. No physical, acquisition, historical-priority, or practical-advantage claim follows from this calculation.

## Result

Let $M\ge2$, $p=M^{-3}$, and independently let $X\sim\mathrm{Exp}(\text{mean }1)$, $J\sim\mathrm{Bernoulli}(p)$, and $Y\sim\mathrm{Exp}(\text{mean }M)$. Put $T=X+JY$, $A=\{T>M\}$, $q=P(A)$, and

\[
 \frac{dP_\theta}{dP}=\frac{e^{\theta T}}{K(\theta)},\qquad
 K(\theta)=E e^{\theta T}.
\]

For the unbiased estimator $Z_\theta=1_AK(\theta)e^{-\theta T}$, define the relative second moment

\[
 \mathcal R_M(\theta)=\frac{E_\theta Z_\theta^2}{q^2}.
\]

The full finite-second-moment domain is **$-1/M<\theta<1/M$**. The sharp leading optimum is

\[
 \inf_\theta\mathcal R_M(\theta)\sim\frac1{2p}=\frac{M^3}{2}.
\]

In fact the same leading optimum holds over **all probability mixtures of scalar Esscher laws of $T$**, even if individual mixture components have infinite second moments. Mixing scalar tilt parameters cannot repair this obstruction. Reweighting the known branch independently of its conditional law does give bounded relative variance; the supplied toy law also admits an explicit deterministic answer.

## 1. Exact formulas and the negative-parameter domain

Write

\[
 d=\frac{pM}{M-1},\quad a=1-d,\quad u=ae^{-M},\quad v=de^{-1},\quad q=u+v.
\]

For $M\ge2$, $a>0$, and the density and event probability are

\[
 f_T(t)=ae^{-t}+\frac{p}{M-1}e^{-t/M},\quad t>0,
\]

\[
 q=(1-p)e^{-M}+p\frac{Me^{-1}-e^{-M}}{M-1}
   =ae^{-M}+de^{-1}.
\]

The moment-generating function is

\[
 K(\theta)=\frac{1-p+p/(1-M\theta)}{1-\theta},\qquad\theta<1/M.
\]

The upper endpoint is strict: the $J=1$ component makes $K(\theta)=\infty$ for $\theta\ge1/M$. There is no restriction on negative parameters for normalizing the Esscher law, because $T\ge0$.

However, the estimator second moment is

\[
 E_\theta Z_\theta^2=K(\theta)H(\theta),\qquad
 H(\theta)=E[e^{-\theta T};T>M].
\]

Its slow-tail integrand is a positive constant times $e^{-(1/M+\theta)t}$. Thus $H(\theta)=\infty$ at and below $-1/M$. On the finite domain,

\[
 H(\theta)=\frac{ae^{-(1+\theta)M}}{1+\theta}
          +\frac{de^{-1-M\theta}}{1+M\theta}.
\]

Consequently the finite-second-moment domain is exactly $(-1/M,1/M)$, including negative tilts above its lower endpoint. Omitting those negative tilts does not change the infimum, as shown next.

## 2. Exact sharp infimum as a unique one-dimensional root

Set $s=M\theta\in(-1,1)$ and $\eta=(Mu+v)/q$. Direct simplification gives

\[
 \boxed{\mathcal R_M(s/M)=
 \frac{e^{-s}M[1-(1-p)s](M+\eta s)}
 {q(M^2-s^2)(1-s^2)}.}
\]

This is an exact formula, not a heavy-tail approximation. The minimizing $s_\star\in(0,1)$ is the unique root of

\[
 -1-\frac{1-p}{1-(1-p)s}
 +\frac{\eta}{M+\eta s}
 +\frac{2s}{M^2-s^2}+\frac{2s}{1-s^2}=0.
\]

Substitution of that root in the boxed expression is an exact characterization of the sharp infimum for each finite $M\ge2$.

To prove uniqueness, $\log K+\log H$ is strictly convex: its second derivative is the sum of variances under the normalized measures proportional to $e^{\theta T}dP$ and $e^{-\theta T}1_A dP$, respectively. At zero, its first derivative is

\[
 E[T]-E[T\mid T>M]<0.
\]

The strict inequality holds because both $A$ and its complement have positive probability and every value of $T$ on $A$ exceeds every value on its complement. The second moment diverges at both finite-domain endpoints. Therefore there is exactly one interior minimum, it has $s_\star>0$, and every negative tilt has $\mathcal R_M(\theta)>\mathcal R_M(0)=1/q$.

An equivalent root equation is often better conditioned near the upper endpoint. Define

\[
 \delta=1-s,\quad m=M-1,\quad
 \epsilon=\frac uv=\left(\frac{M-1}{pM}-1\right)e^{1-M}.
\]

Then the exact expression is

\[
 p\mathcal R_M=\frac{e^\delta(1-p+p/\delta)}
 {(2-\delta)(1+\delta/m)}\,
 \frac{1+\epsilon r(\delta)}{(1+\epsilon)^2},\qquad
 r(\delta)=\frac{M(2-\delta)}{M+1-\delta}.
\]

Its unique minimizer lies in $0<\delta_\star<1$ and solves

\[
 1+\frac1{2-\delta}-\frac1{m+\delta}
 -\frac{p}{\delta((1-p)\delta+p)}
 -\frac{\epsilon M(M-1)}{(M+1-\delta)^2[1+\epsilon r(\delta)]}=0.
\]

## 3. A finite-$M$ inequality valid for every scalar tilt

Define

\[
 \alpha_M=\frac32-\frac1{M-1}\in[1/2,3/2),\qquad
 C_M^{\rm LB}=\left(\sqrt{1-p}+\sqrt{\alpha_Mp}\right)^2.
\]

For every finite-second-moment scalar Esscher tilt,

\[
 \boxed{\mathcal R_M(\theta)\ge
 \frac{C_M^{\rm LB}}{2p(1+\epsilon_M)^2}.}
\]

Proof for $\theta\ge0$: $0<\delta\le1$, $\epsilon\ge0$, and

\[
 B(\delta)=\frac{e^\delta}{(2-\delta)(1+\delta/m)}
 \quad\hbox{satisfies}\quad
 (\log B)'=1+\frac1{2-\delta}-\frac1{m+\delta}\ge\alpha_M.
\]

The derivative on the right increases with $\delta$, so $B(\delta)\ge\tfrac12e^{\alpha_M\delta}\ge\tfrac12(1+\alpha_M\delta)$. Hence

\[
 2p\mathcal R_M(1+\epsilon)^2
 \ge(1+\alpha_M\delta)(1-p+p/\delta)
 \ge1-p+\alpha_Mp+2\sqrt{\alpha_Mp(1-p)}=C_M^{\rm LB},
\]

where the second inequality is arithmetic-geometric mean. For negative $\theta$, the preceding convexity argument gives $\mathcal R_M\ge1/q$. This also exceeds the displayed bound because

\[
 2p(1+\epsilon)^2/q=2e(1-1/M)(1+\epsilon)\ge e,
 \qquad C_M^{\rm LB}\le1+\alpha_M\le5/2<e.
\]

As $M\to\infty$, $\epsilon_M=O(M^3e^{-M})\to0$ and $C_M^{\rm LB}\to1$. This proves the proposed uniform $(1-o(1))/(2p)$ lower bound. The correction $(1+\epsilon_M)^{-2}$ matters at small $M$: the uncorrected $1/(2p)$ bound is false, for example at $M=4$.

## 4. Sharp asymptotics, including the optimizing parameter

Let

\[
 \beta_M=\frac{\alpha_M^2}{2}+\frac18+\frac1{2(M-1)^2},\qquad
 \kappa_M=\alpha_M-1+\frac{\beta_M}{\alpha_M}.
\]

For $p=M^{-3}$, the exponentially small $\epsilon_M$ contributes below every algebraic order. Uniform Taylor expansion near $\delta=0$ gives

\[
 \boxed{\delta_\star=
 \sqrt{p/\alpha_M}-\frac{\beta_M}{\alpha_M^2}p+O(p^{3/2}),
 \qquad \theta_\star=\frac{1-\delta_\star}{M}.}
\]

\[
 \boxed{\inf_\theta\mathcal R_M(\theta)=
 \frac1{2p}+\sqrt{\frac{\alpha_M}{p}}+\frac{\kappa_M}{2}+O(\sqrt p).}
\]

In particular $1-M\theta_\star\sim\sqrt{2p/3}$, and

\[
 \inf_\theta\mathcal R_M(\theta)=
 \frac{M^3}{2}+\sqrt{\frac32}M^{3/2}
 -\frac1{\sqrt6}M^{1/2}+\frac23+O(M^{-1/2}).
\]

For completeness, the expansion follows from

\[
 2B(\delta)=1+\alpha_M\delta+\beta_M\delta^2+O(\delta^3),
\]

multiplied by $1-p+p/\delta$. Differentiation shows the balancing scale $\delta\asymp\sqrt p$; writing $\delta=c\sqrt p+dp+O(p^{3/2})$ yields $c=\alpha_M^{-1/2}$ and $d=-\beta_M/\alpha_M^2$. Substitution yields the stated minimum. Strict convexity and the divergent endpoint terms justify using the local root as the global optimizer. The Taylor coefficients and remainders are uniformly bounded for $M\ge2$ and $\delta\le1/2$.

Under the optimizing law, the branch probability is

\[
 P_{\theta_\star}(J=1)=\frac{p}{p+(1-p)\delta_\star}
 \sim\sqrt{\alpha_Mp}\sim\sqrt{3p/2}.
\]

Given this branch, the tilted $Y$ has mean $M/\delta_\star$. Thus increasing the rare-branch probability is inseparably coupled to producing very long overshoots and dispersed likelihood weights.

## 5. Stronger obstruction: arbitrary mixtures of scalar Esscher laws

Let $Q=\int P_\theta\,\pi(d\theta)$, for any probability distribution on all legal normalizing parameters $\theta<1/M$. The estimator uses the **marginal mixture density** $g_Q=dQ/dP$, so this result covers the potentially better balance-heuristic estimator, not merely a random choice of scalar estimator.

For $t\ge M\ge2$,

\[
 g_\theta(t)=\frac{e^{\theta t}}{K(\theta)}
 \le\frac{(1-\theta)e^{\theta t}}{1-p}
 \le\frac{(1-1/M)e^{t/M}}{1-p}.
\]

The last inequality follows by differentiating $\log[(1-\theta)e^{\theta t}]$: its derivative is $t-1/(1-\theta)\ge0$ for every $\theta<1/M$ when $t\ge M\ge2$. Mixtures inherit the same pointwise envelope. Consequently,

\[
 \frac{E_Q[(1_A/g_Q(T))^2]}{q^2}
 =\frac{E_P[1_A/g_Q(T)]}{q^2}
 \ge\frac{1-p}{1-1/M}\frac{H(1/M)}{q^2}
 \ge\boxed{\frac{1-p}{2p(1+\epsilon_M)^2}}.
\]

Here $H(1/M)$ is a finite tail integral; it does not assert that $P_{1/M}$ exists. The heavy density term gives $H(1/M)\ge de^{-2}/2$, proving the final inequality. A single tilt from section 4 attains $\mathcal R_M\sim1/(2p)$, so

\[
 \boxed{\inf_{Q\in\operatorname{conv}\{P_\theta:\theta<1/M\}}
 \frac{E_Q[(1_A\,dP/dQ)^2]}{q^2}\sim\frac1{2p}.}
\]

This does **not** exclude mixtures based on other statistics, latent-cause tilts, state-dependent changes of measure, stratification, splitting, or analytical integration.

## 6. Generic light-base / rare-scale theorem

The effect is not specific to exponential $X$, threshold $M$, or exponent 3. Suppose $X\ge0$ has a fixed law with $E e^{\eta X}<\infty$ for some $\eta>0$. Fix $c,k>0$, let $p_M=M^{-k}$, $Y_M=M E$ with $E\sim\mathrm{Exp}(\text{mean }1)$, and set

\[
 T_M=X+J_MY_M,\quad J_M\sim\mathrm{Bernoulli}(p_M),\quad
 A_M=\{T_M>cM\}.
\]

All variables are independent. Then

\[
 P(A_M)\sim p_Me^{-c},\qquad
 \boxed{\inf_{Q\in\operatorname{conv}\{P_{M,\theta}:\theta<1/M\}}
 \frac{E_Q[(1_{A_M}dP_M/dQ)^2]}{P(A_M)^2}
 \sim\frac1{2p_M}.}
\]

The parameter domain is as before for all sufficiently large $M$. The convex hull here permits arbitrary probability mixtures, not only finite mixtures.

Proof: exponential integrability gives $P(X>cM)=o(p_M)$ and $E[e^{X/M};X\le cM]\to1$. Conditioning on $X$ yields

\[
 P(X+Y_M>cM)=e^{-c}E[e^{X/M};X\le cM]+P(X>cM)\to e^{-c},
\]

and

\[
 E[e^{-T_M/M};A_M]\sim\tfrac12p_Me^{-2c}.
\]

For the uniform lower bound, fix any finite $b$ with $r_b=P(X\le b)>0$, and take $cM\ge b$. For $0\le\theta<1/M$, $K_M(\theta)\ge1-p_M$, hence $g_\theta(t)\le e^{t/M}/(1-p_M)$. For negative $\theta$, $K_M(\theta)\ge(1-p_M)r_be^{\theta b}$, hence for $t\ge cM\ge b$,

\[
 g_\theta(t)\le[(1-p_M)r_b]^{-1}
 \le\frac{e^{t/M}}{(1-p_M)r_b}.
\]

Every mixture therefore has relative second moment at least $(1-p_M)r_b E[e^{-T_M/M};A_M]/P(A_M)^2\sim r_b/(2p_M)$. Taking $b\to\infty$ proves the uniform liminf $1/2$. For the upper bound choose $M\theta=1-\sqrt{p_M}$. Then $K_M(\theta)\to1$, while direct conditioning on $X$ gives $H_M(\theta)\sim p_Me^{-2c}/2$; the fast-component contribution is exponentially small. This yields the matching limsup.

Thus the supplied rare-branch interface is the relevant operation. Optimizing one scalar sufficient statistic, or mixing its tilt parameters, cannot obtain bounded relative variance throughout this family.

## 7. What a supplied branch interface can do

Define $a_0=e^{-M}$ and $a_1=(Me^{-1}-e^{-M})/(M-1)\to e^{-1}$. If a sampler can choose $J\sim\mathrm{Bernoulli}(r)$ with fixed $0<r<1$ while preserving the known conditional laws, its exact likelihood-ratio estimator has

\[
 E_QZ^2=\frac{(1-p)^2a_0}{1-r}+\frac{p^2a_1}{r},\qquad
 \frac{E_QZ^2}{q^2}\longrightarrow\frac{e}{r}.
\]

This preserves both branches and is unbiased for the entire $q$. Taking $r=1/2$ gives limiting relative second moment $2e$. The variance-minimizing branch allocation is

\[
 r_\star=\frac{p\sqrt{a_1}}{(1-p)\sqrt{a_0}+p\sqrt{a_1}},
\]

with minimum second moment $[(1-p)\sqrt{a_0}+p\sqrt{a_1}]^2$, and limiting relative second moment $e$.

If the fast contribution is evaluated analytically, draw just $X,Y\$ under the $J=1$ law and use

\[
 \widehat q=(1-p)e^{-M}+p1_{\{X+Y>M\}}.
\]

This is unbiased and its relative variance tends to $e-1$. Forcing $J=1$ **without** including or separately estimating the $J=0$ contribution is biased at finite $M$. Sampling from the full event-conditional law can produce zero variance only with the relevant normalization or an equivalent supplied interface; this should not be counted as free acquisition.

In this toy model, $q$ itself is already in closed form. The strongest matched comparator is therefore deterministic evaluation of that formula, not brute-force Monte Carlo. The calculation establishes a proposal-family obstruction, not a simulation advantage over the full known-model baseline.

For $N$ independent draws, relative mean-square error is $(\mathcal R-1)/N$. Crude Monte Carlo has $\mathcal R=1/q\sim e/p$; the optimum scalar family, including mixtures, has $\mathcal R\sim1/(2p)$. Thus it improves per-draw variance by only the constant factor $2e$, retaining an order-$1/p$ draw requirement for fixed relative accuracy.

If $T$ is interpreted and charged as a physical trajectory duration, its cost under the scalar tilt is also relevant:

\[
 E_\theta T=\frac1{1-\theta}
 +\frac{Mp}{\delta((1-p)\delta+p)}.
\]

At the per-draw variance optimizer this is asymptotic to $3M/2$. Optimizing variance per draw therefore need not optimize expected elapsed cost. This conditional clock observation does not impose physical duration costs on an abstract random-number sampler; a cost model and implementable change of dynamics must be specified separately.

## 8. General mixture decomposition and operation decision

For any labeled mixture $P=\sum_j p_jP_j$, event probabilities $a_j=P_j(A)>0$, component MGFs $k_j(\theta)$, and $h_j(\theta)=E_j[e^{-\theta T};A]$, define

\[
 r_j(\theta)=\frac{p_jk_j(\theta)}{\sum_\ell p_\ell k_\ell(\theta)},\qquad
 w_j=\frac{p_ja_j}{P(A)},\qquad
 \rho_j(\theta)=\frac{k_j(\theta)h_j(\theta)}{a_j^2}\ge1.
\]

The scalar Esscher relative second moment decomposes exactly as

\[
 \boxed{\mathcal R(\theta)=\sum_j\frac{w_j^2}{r_j(\theta)}\rho_j(\theta).}
\]

It exposes both failure modes: underallocated event-bearing branches $r_j\ll w_j$, and large within-branch weight variance $\rho_j\gg1$. In the present optimum, $w_1\to1$, $r_1\asymp\sqrt p$, and $\rho_1\asymp1/\sqrt p$; their product produces $1/(2p)$.

The stronger operation decision is: **do not spend further effort fitting scalar Esscher parameters or their mixtures to this family.** Use the explicit conditional/cause law, a genuinely larger controllable statistic or proposal class, or exact integration. When that cause law is not supplied, the proof does not establish that it can be acquired cheaply, selected physically, or calibrated from ordinary observations. An acquisition theorem is a separate obligation.

## 9. Closest verified prior art and scope of originality

The broad failure-and-repair phenomenon is established prior art. The present note does not claim novelty for exponential-tilt failure, mixture importance sampling, conditional Monte Carlo, or cause stratification.

- Glasserman and Wang, **Counterexamples in importance sampling for large deviations probabilities**, *Annals of Applied Probability* 7 (1997), 731–746. Their examples show that changes of measure motivated by large deviations can have poor or infinite variance; alternatives account for distinct ways the rare event occurs. This is the closest conceptual predecessor verified here. [Author-hosted paper](https://business.columbia.edu/sites/default/files-efs/pubfiles/4272/glasserman_wang.pdf).
- Brereton, Chan, and Kroese, **Fitting mixture importance sampling distributions via improved cross-entropy**, Winter Simulation Conference (2011). Sections 2–4 discuss failures of exponential twisting and repairs through disjoint-event decomposition, state-dependent proposals, and mixtures. Their mixture proposals are not restricted to the bounded scalar-$T$ Esscher family excluded above. [UQ-hosted paper](https://people.smp.uq.edu.au/DirkKroese/ps/WSC_BCK.pdf).
- Chan and Lai, **Efficient importance sampling for Monte Carlo evaluation of exceedance probabilities**, *Annals of Applied Probability* 17 (2007), 440–473. They establish asymptotic optimality for suitable mixtures of exponentially twisted measures in their models. This reinforces why the statistic/proposal class must be specified before claiming that mixtures repair an obstruction. [Author preprint](https://arxiv.org/abs/math/0703910).
- Asmussen and Kroese, **Improved algorithms for rare event simulation with heavy tails**, *Advances in Applied Probability* 38 (2006), 545–558. Conditional Monte Carlo and component-focused importance sampling provide bounded-relative-error comparators in different heavy-tailed sum models. The present $M$-indexed law is light-tailed at each finite $M$, so their setting is related methodology rather than the same theorem. [Author publication list with paper link](https://people.smp.uq.edu.au/DirkKroese/publications.html).
- Lam, **Efficient importance sampling under partial information**, Winter Simulation Conference (2012). Sections 1–3 explicitly charge learning an unknown function before constructing an importance sampler and compare that two-stage procedure with mixture proposals. This supports keeping acquisition separate from supplied-model sampling; its unknown-function model does not establish the present hidden-branch theorem. [Author-hosted paper](https://www.columbia.edu/~khl2114/files/a41-lam.pdf).

Limited searches did not locate this exact $p=M^{-3}$ toy model, its finite-$M$ bound, sharp expansion, or the all-scalar-mixtures envelope theorem. Their historical priority remains **UNKNOWN**; absence from this search is not a novelty certificate.

## 10. Replay artifacts

`check.py` independently integrates the original density, checks the exact rational and endpoint formulas, optimizes the full second moment, checks the finite inequality over negative and positive tilts, tests mixtures including a negative component with infinite individual second moment, verifies the first three asymptotic terms, and checks generic-family examples. `RESULTS.json` and `NUMERICS.md` record its deterministic results. These are numerical diagnostics of the stated mathematics, not substitutes for the proofs above.
