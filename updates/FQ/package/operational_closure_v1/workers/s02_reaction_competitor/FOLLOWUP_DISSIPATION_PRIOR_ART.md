# Priority screen: stationary no-exit differences and hidden dissipation

**Finding, 15 October 2026.** A dimension-free entropy-production floor for the exact law $P_{1/20}$ was disclosed on 3 October 2026 in [Anonymous, *An architecture-independent dissipation floor for alternating-renewal observations*](https://www.evidencepress.org/releases/hidden-dissipation-floor/) and its [versioned proof source](https://github.com/ipitchford/hidden-dissipation-floor/blob/main/PAPER.tex). This is an **unrefereed candidate**, not an independently validated theorem, but it is direct prior disclosure. A positive *forward* third finite difference of stationary no-exit probability gives a weaker bound by applying its existing additive-reversibilization, path-KL and spectral-mixture lemmas. Do not present the operation or the contradiction of $V_\infty(P_{1/20})=0$ as new without addressing this candidate.

## Exact overlap and source history

| Primary source | Result and scope | Priority implication |
| --- | --- | --- |
| [Aznagulov, arXiv:2609.14623v1](https://arxiv.org/html/2609.14623), [submitted 13 September 2026](https://arxiv.org/abs/2609.14623) | §6 explicitly conjectures $V_\infty(P_{1/20})=0$. Theorem 9 proves $V_n(P_q)>0$ at each feasible *fixed* $n$, using the reversible exponential-mixture restriction and fixed-dimension attainment. It explicitly leaves uniformity in $n$ open. | Supplies the target and gap, not the all-dimension answer. |
| [Skinner–Dunkel, PRL 2021, supplement S6–S10](https://arxiv.org/pdf/2105.08681) | Derives positive exponential-mixture complete waiting-time densities at equilibrium, hence complete monotonicity and $\mathrm{CV}^2\ge1$. The main paper formulates hidden-model optimization and reports a numerical variance–dissipation curve. | The spectral obstruction and waiting-time inference are inherited. Numerical convergence alone does not certify an exact-law all-dimension constant. |
| [Aznagulov, arXiv:2609.37205v1](https://arxiv.org/html/2609.37205v1), 29 September 2026 | Uses $R=(Q+Q^\dagger)/2$ as a reversible comparator sharing the stationary law, exit rates and activity, for finite-resolution detection. | Additive reversibilization itself is already prior art. |
| [Anonymous candidate, version 1.1.0](https://github.com/ipitchford/hidden-dissipation-floor/blob/main/PAPER.tex), [released 3 October 2026](https://github.com/ipitchford/hidden-dissipation-floor/releases/tag/v1.1.0-candidate) | Proves in the stated finite stationary deterministic-observation, even-variable CTMC class $D_{\rm KL}(\mathcal P_Q^T\Vert\mathcal P_R^T)\le T\sigma(Q)/4$. Its fixed-window certificate reports $V_\infty(P_{1/20})>0.017568198744$ at $t=3/10$, with no bound on hidden dimension, rates or activity. For finite-realizable stationary ergodic two-label alternating-renewal laws, its theorem claims $V_\infty(P)=0$ iff both complete dwell laws are hyperexponential iff a finite reversible exact realization exists. | Directly preempts both the proposed qualitative result and a weaker finite-difference certificate. |

The [release page](https://www.evidencepress.org/releases/hidden-dissipation-floor/) links [Zenodo DOI 10.5281/zenodo.23118474](https://doi.org/10.5281/zenodo.23118474), the [GitHub release](https://github.com/ipitchford/hidden-dissipation-floor/releases/tag/v1.1.0-candidate), proof and verifiers. The GitHub release is timestamped 3 October 2026, 09:39 UTC. Its [provenance record](https://github.com/ipitchford/hidden-dissipation-floor/blob/main/PROVENANCE.md) names the scholarly creator *Anonymous* and Evidence Press as publisher; records supplied research and referee-audit ZIP hashes; credits the stronger fixed-window corollary to the supplied audit; and calls Codex and coordinated-agent checks internal. Original model identity and human scientific contribution were not established. Repo ownership is not authorship evidence. Its [dated source audit](https://github.com/ipitchford/hidden-dissipation-floor/blob/main/SOURCES.md) describes a bounded search, and its [review response](https://github.com/ipitchford/hidden-dissipation-floor/blob/main/REVIEW_RESPONSE.md) expressly disclaims external human peer review and formal proof. I checked the critical argument structure, not every algebraic step.

## Third difference: sign and quantitative corollary

For stationary visible block $B$, put $p=\Pr(Y_0=B)$ and
$$
H_Q(t)=\Pr_Q\{Y_u=B\text{ for all }0\le u\le t\},\qquad
\Delta_h^3H_Q=H_Q(3h)-3H_Q(2h)+3H_Q(h)-H_Q(0).
$$
For a reversible hidden CTMC, the killed block generator $S$ is self-adjoint in $L^2(\pi|_B)$. Hence
$$
H_R(t)=\langle\mathbf1,e^{tS}\mathbf1\rangle_{\pi|_B}
      =\int_0^\infty e^{-\lambda t}\,\mu(d\lambda),\quad \mu\ge0,
$$
and $\Delta_h^3H_R=\int(e^{-\lambda h}-1)^3\mu(d\lambda)\le0$. Thus a **positive forward** $\Delta_h^3H_Q$ violates the equilibrium cone. If the convention is $H(0)-3H(h)+3H(2h)-H(3h)$, the violating sign is **negative**.

For any compatible finite $Q$, let $R=(Q+Q^\dagger)/2$. The prior candidate proves $D_{\rm KL}(\mathcal P_Q^{3h}\Vert\mathcal P_R^{3h})\le3h\sigma(Q)/4$ and $Q,R$ share $p$. Conditional on $Y_0=B$, let $E_k$ indicate no exit through $kh$ and set $G=-1+3E_1-3E_2+E_3$. Nested events make $G\in\{-1,0,2\}$, a range of width three, and $p\mathbb E_QG=\Delta_h^3H_Q$. For $d:=\Delta_h^3H_Q>0$, reversible complete monotonicity gives $\mathbb E_RG\le0$. Conditional Pinsker plus the path-KL chain rule therefore gives
$$
d\le 3\sqrt{\frac{3hp\,\sigma(Q)}8},
\qquad
\boxed{\sigma(Q)\ge\frac{8d^2}{27ph}}.
$$
This is uniform over hidden state count and activity. It is a straightforward **corollary of the prior candidate's two key lemmas**, not a separate novelty claim. A sharper four-outcome information projection could replace Pinsker, but would follow the same proof template.

For its ring target $q=1/20$, $s=1+q$, $u=\sqrt q$ and $p=2/3$, the killed two-state block gives
$$
H_q(t)/p=e^{-st}\left[\cosh(ut)+\frac{s}{2u}\sinh(ut)\right].
$$
At $h=3/10$, high-precision numerical evaluation gives $d=0.0025741190021822943430\ldots>0$ and the simple floor $\sigma>9.81642761095699\times10^{-6}$. These numbers are diagnostics, not rigorous interval enclosures. The earlier candidate's *certified* fixed-window bound $0.017568198744$ is about 1,790 times larger. It uses only $p,H(h),H(2h)$; the third difference also needs $H(3h)$. This is the decisive same-information competitor.

## Strongest matched certificate and other methods

The [3 October manuscript's fixed-window corollary](https://github.com/ipitchford/hidden-dissipation-floor/blob/main/PAPER.tex) uses uninterrupted persistence on $[-t,0]$ and $[0,t]$, conditional on $Y_0=B$. Its two Bernoulli tests have marginal success $a=H(t)/p$ and joint success $b=H(2t)/p$. For reversible hidden dynamics, past and future are independent given the central microscopic state and have the same conditional success probability. Mixing gives $b\ge a^2$. If the target has $b<a^2$, its information-projection lemma and a $2t$ path comparison give
$$
\sigma(Q)\ge\frac{2p}{t}I(a,b),
$$
where $I(a,b)$ is the mutual information of the target two-bit law. The paper gives an exact rational/log enclosure $0.017568198744<B_{3/10}<0.017568198745$ for this **chosen certificate**. It does not identify the physical optimum; the ring gives only $V_\infty\le(19/20)\log20\approx2.84595$. The broader zero-cost theorem uses Pinsker convergence of reversible persistence functions, weak closure of positive spectral measures, and finite target realizability plus Cayley–Hamilton to force finite positive mixtures; alternating-renewal independence gives the reversible converse. This proof structure is plausible on inspection but remains unrefereed.

- [Skinner–Dunkel 2021](https://arxiv.org/html/2105.08681) already detects $P_{1/20}$ as nonequilibrium from its complete $B$-dwell $\mathrm{CV}_B^2=481/842<1$. It explicitly notes ordinary current TURs yield no nontrivial bound for the two-state observation without visible currents. Its increasing-state trade-off curve is numerical and should not be silently promoted to the exact-law optimum.
- [Ehrich 2021](https://arxiv.org/html/2105.08803v2) fits discrete-time partially observed hidden models to sharpen entropy bounds and discusses hidden-state count; it does not provide this continuous-time no-exit floor.
- [Nitzan–Ghosal–Bisker 2023](https://arxiv.org/html/2212.01783) optimizes entropy using transition/waiting-time constraints under a hypothesized topology. Simpler-topology performance is numerical, and the authors leave universal topology reduction open. It is a hard fixed-architecture comparator, not an unrestricted proof.
- [Transition-based waiting-time inference](https://arxiv.org/abs/2203.12020) and [visible irreversibility without currents](https://www.nature.com/articles/s41467-019-11051-w) use richer time-direction information. The exact stationary two-label alternating-renewal target is visibly time-reversal invariant, so its visible forward/reverse path KL and antisymmetric current are zero. A certificate based only on observed time asymmetry cannot establish this hidden floor.

## Countermodels and decision

1. **Visibly reversible, microscopically dissipative.** The three-state ring $Q_q$ with labels $A,B,B$ has independent alternating visits, so its stationary visible path law is time-reversal invariant, while $\sigma(Q_q)=(1-q)\log(1/q)>0$ for $0<q<1$. Current and visible path-KL estimators miss it.
2. **Genuine reversible hidden mixture.** A reset chain with $Q_{A_iB_j}=\lambda_i\beta_j$, $Q_{B_jA_i}=\mu_j\alpha_i$ and stationary masses proportional to $\alpha_i/\lambda_i,\beta_j/\mu_j$ is reversible and generates hyperexponential complete dwell laws. Its stationary no-exit $H$ has $\Delta_h^3H\le0$ for every $h$. The positive-difference test is one-sided, not a full characterization for nonrenewal observations.
3. **Variance misses a spectral defect.** The 3 October candidate supplies a finite four-state realization with $\mathrm{CV}_B^2=324697/112903>1$ but a negative exponential residue in its complete $B$-dwell density. Its all-dimension classification gives a positive floor even though the elementary variance test is inconclusive.

**Priority verdict:** record the proposed $P_{1/20}$ third-difference route as a rediscovery or weaker witness of the 3 October candidate. Worthwhile pivots are independent proof audit, a demonstrably stronger *certified* bound from matched observations, sharp optimum/attainment, dependence-aware finite-sample confidence, or a theorem in an explicitly excluded model class. Keep stationarity, deterministic labels, even-variable reversal and the full cost convention fixed when comparing claims.
