# Attractive one-shot cascades: closest established routes and a continuous-path completion

## Conclusion

The closest established algorithm I found is Ei Ando's bounded-treewidth algorithm for stochastic project completion. It already supplies the general proof pattern of discretizing a deadline, bounding the accumulated horizontal shift, and converting that shift into a relative probability guarantee by dilation. Event-time variables and graphical-model elimination are also established. Those ingredients should not be presented as new.

The specific combination still worth checking is: arbitrary finite configuration-dependent **increasing** hazards, binary sites that fire at most once, possibly cyclic hazard graphs, relative error with a number of time bins independent of rate magnitudes and target probability, and continuous success-conditioned paths obtained without rejection. I did not locate a primary source proving this full contract. This is a bounded literature-search conclusion, not a priority claim.

The hidden qubit construction developed before this comparison is preserved in `CONSTRUCTION.md`, `learner.py`, `source_fixture.py`, `run_experiment.py`, and the JSON outputs beside this file. Its scientific conclusion remains that ordinary gate-set tomography covers the endpoint; its useful contribution here is a concrete implementation and honest accounting of the extra assumptions and failed attempts.

## Exact proposed contract

There are n initially inactive binary sites. Each changes from 0 to 1 at most once. In state x, inactive site i has time-homogeneous finite hazard λ_i(x_Pa(i)). The rate tables are nonnegative and coordinatewise increasing. The directed hazard graph can have cycles. A fixed set of initially active sites can be incorporated as constants and omitted from n.

The query is the probability p(T) that every member of a specified target set R is active by deadline T. The target restriction is important: these are unary terminal conditions, so adding the query does not enlarge the factor graph. A general Boolean terminal condition needs its own representation and width accounting.

Given exact rates and a tree decomposition of the moral graph with width k, the intended arithmetic-operation guarantee is a deterministic relative approximation in time polynomial in n and 1/ε for each fixed k, with no factor proportional to 1/p(T), max_i,x λ_i(x)T, or the ratio of largest to smallest positive hazard. The model is supplied or has already been acquired. Learning it and numerical bit complexity need separate bills.

The second output is a sampler whose **continuous path law** is within ε in total variation of the source law conditioned on target success. Reporting grid-valued event times would not satisfy that contract: except for atoms such as no event, the grid and continuous timing laws are singular.

## Primary comparators

| Established route | What it already supplies | Boundary relative to this contract |
|---|---|---|
| [Ando, stochastic longest paths, arXiv:1910.09791v4](https://arxiv.org/pdf/1910.09791) | Theorem 1: deterministic relative FPTAS for independent uniform edge durations in fixed-treewidth DAGs. Lemmas 6–7: deadline shift followed by a volume-dilation ratio. Theorem 4: exact polynomial arithmetic for independent standard Exp(1) edge durations. | AND-precedence/project-completion overlap is substantial. The exponential theorem explicitly assumes a common unit rate and unit-cost exponentiation. General-distribution results use derivative oracles and additive error. It does not state the arbitrary local-hazard, cyclic, heterogeneous-rate contract above. Its graph width is the underlying graph's width, which can be smaller than moral width. |
| [Galán and Díez, Networks of probabilistic events in discrete time, 2002](https://www.sciencedirect.com/science/article/pii/S0888613X02000713) | Represents one event by one variable whose values are occurrence times. This avoids making one state variable for every time slice. Temporal noisy gates encode uncertain event interactions. | Event-time compression is already known. This source does not establish the proposed rate-uniform relative discretization theorem. |
| [Du, Song, Gomez-Rodriguez, and Zha, Scalable Influence Estimation in Continuous-Time Diffusion Networks, NeurIPS 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC4704803/) | Independent edge transmission delays, arrival-time factorization, explicit discussion of time discretization and treewidth, and a scalable randomized influence estimator. | Theorem 1 is additive error for expected influence. The result does not provide a worst-case relative guarantee for an arbitrarily rare joint target event under general increasing local hazard tables. |
| [Sturlaugson and Sheppard, Inference Complexity in Continuous Time Bayesian Networks, UAI 2014](https://www.cs.montana.edu/sheppard/pubs/uai-2014.pdf) | Hardness of exact and approximate CTBN inference even with fixed initial states; a useful comparison against generic CTBN inference. | Its hardness construction is not the attractive binary one-shot bounded-moral-width class. General hardness should not be quoted as hardness of this restricted opening. |
| [Rao and Teh, Fast MCMC sampling for Markov jump processes and extensions, 2013](https://arxiv.org/abs/1208.4818) | Continuous posterior paths via uniformization and auxiliary-variable Gibbs sampling, without time-discretization bias. | It does not by itself supply a worst-case rate-independent mixing and relative-normalizer guarantee. Exactness of the stationary law is different from an explicit finite-time ε sampler. |
| [Zwirglmaier and Straub, A discretization procedure for rare events in Bayesian networks, 2016](https://www.sciencedirect.com/science/article/pii/S0951832016300229) | Rare-event-aware discretization for reliability BNs, based on FORM approximations and numerical optimization of posterior error. | The method is an important practical comparator, but it is not stated as a worst-case FPTAS for the cascade class. |

Ando's result is the strongest direct algorithmic comparison. The candidate should be described as an extension of a known approximation pattern to a different stochastic semantics if its proof survives, not as the discovery that event times and width enable relative approximation.

Two distinctions must be kept explicit. First, a hazard graph's moralization connects co-parents: a directed star can have underlying treewidth one but large moral treewidth. The algorithms therefore have different structural promises. Second, the existence of continuous posterior MCMC or practical rare-event discretization does not automatically imply the required uniform finite-resource guarantee.

## Positive factors and the continuous driver lift

The following construction is derived here to finish the continuous-path operation. It uses the candidate delayed-grid process and ordinary change of conditioning.

Let Δ=T/N. Assign independent E_i~Exp(1) to the sites. A site fires when its integrated local hazard first reaches E_i. Freeze the parent state within each grid interval; record all threshold crossings at that interval's right endpoint. Rates for the next interval use the updated grid state. All updates within a bin are simultaneous.

Write Y_i∈{1,…,N,∞} for the recorded grid time in units of Δ. For an assignment y, let

\[
A_i(k;y)=\Delta\sum_{\ell=0}^{k-1}
\lambda_i\bigl((\mathbf 1\{y_j\le\ell\})_{j\in\mathrm{Pa}(i)}\bigr),
\qquad A_i(0;y)=0.
\]

Only cumulative hazards up to the site's own event matter. The local factor is

\[
f_i(y_i,y_{\mathrm{Pa}(i)})=
\begin{cases}
e^{-A_i(k-1;y)}-e^{-A_i(k;y)},&y_i=k\le N,\\
e^{-A_i(N;y)},&y_i=\infty.
\end{cases}
\]

These factors are nonnegative. An equality at a threshold is a null event and can be assigned either convention.

**Product-preimage lemma.** The complete preimage of a grid assignment y in independent-driver space is the Cartesian product

\[
\prod_i I_i(y),\qquad
I_i(y)=
\begin{cases}
[A_i(k-1;y),A_i(k;y)),&y_i=k,\\
[A_i(N;y),\infty),&y_i=\infty.
\end{cases}
\]

Necessity follows by the first-threshold-crossing definition. For sufficiency, induct over grid bins. If the actual grid state agrees with y before bin k, its rates and cumulative hazards in that bin equal the displayed quantities. The interval membership says precisely which inactive sites cross in that bin. This proves agreement in bin k. The induction also proves the claim for cyclic graphs: no topological order of sites is required. Independence of the E_i now gives

\[
\Pr(Y=y)=\prod_i f_i(y_i,y_{\mathrm{Pa}(i)}).
\]

Consequently the factor product is normalized, including assignments whose factor product is zero. Each factor's scope is a moral clique. Positive variable elimination and backward sampling apply at the acquired moral width. A conservative bound for table formation and contraction is polynomial in n times (N+1)^{k+1}; precise constants depend on the supplied decomposition and representation of the local rate table.

Let A_N={Y_i≤N for every i∈R}. Sample y from the positive factor model conditioned on A_N. Then sample each E_i independently from Exp(1) restricted to I_i(y), and run the original continuous cascade with these sampled drivers. If I=[a,b) with b finite, one stable inverse-CDF formula is

\[
E=a-\log\bigl(1-U(1-e^{-(b-a)})\bigr),\qquad U\sim\mathrm{Unif}(0,1).
\]

For b=∞ use E=a+Exp(1). Zero-mass intervals are never selected by exact backward sampling. `expm1` and `log1p` are the appropriate numerical primitives for small interval widths.

By the product-preimage lemma, the resulting drivers have exactly their original product-exponential law conditioned on A_N. The continuous output path therefore has the true path law conditioned on A_N, not a rounded approximation to individual event times.

Suppose the monotone delay comparison has established A_N⊆A, where A is true target success by T. For nested events of positive probability,

\[
\|\mathcal L(E\mid A_N)-\mathcal L(E\mid A)\|_{\mathrm{TV}}
=1-\frac{\Pr(A_N)}{\Pr(A)}.
\]

Applying a deterministic continuous simulator cannot increase total variation. Thus

\[
\|\mathcal L(\mathrm{path}\mid A_N)-\mathcal L(\mathrm{path}\mid A)\|_{\mathrm{TV}}
\le 1-p_N(T)/p(T).
\]

This pays for continuous success-conditioned paths using the same relative probability calculation, with no rare-event rejection step.

## Why the proposed grid size has the right form

The two needed facts can be stated independently of numerical implementation.

**Delay comparison.** Use the same Exp drivers for the continuous and delayed processes. Attractiveness gives τ_i≤τ_i^N. If site i is the r-th site to fire in the continuous process, an induction on r gives τ_i^N≤τ_i+rΔ. The earlier continuous activations have each been delayed by at most (r−1)Δ. After shifting time by that amount, the delayed process's parent state dominates the original parent state before τ_i. Its integrated hazard therefore crosses by τ_i+(r−1)Δ, and recording at the next grid endpoint adds at most Δ. Consequently

\[
p(T-n\Delta)\le p_N(T)\le p(T),\qquad N>n.
\]

**Exponential-driver dilation.** Time homogeneity gives τ_i(cE)=cτ_i(E). Thus the driver set for success by cT is c times the driver set for success by T. A change of variables gives, for 0<c≤1,

\[
p(cT)=c^n\int_{A_T}e^{-c\sum_i E_i}\,dE
\ge c^n p(T).
\]

This dilation calculation uses finitely many independent exponential drivers and time homogeneity. Attractiveness is needed for the preceding delay sandwich, not for this change of variables.

With c=1−n/N, Bernoulli's inequality gives

\[
p_N(T)\ge(1-n/N)^n p(T)\ge(1-n^2/N)p(T).
\]

Hence N≥n²/ε is sufficient for relative underestimation at most ε and for the driver-lift TV guarantee above. The observation is consistent with the established shift-to-relative-error strategy; the specific driver semantics and cyclic attractive hazard class are the points needing a full priority check.

## Multiplicative rate error also permits conditioned continuous paths

The grid theorem for exact supplied rates does not alone transfer to a learned model. The following additional lemma handles that gap without dividing by the target probability.

Let λ be the true attractive rate table and κ a proposed rate table with the same zero pattern and

\[
e^{-\eta}\lambda_i(x)\le\kappa_i(x)\le e^\eta\lambda_i(x)
\]

for every local configuration. Assume p_λ(A)>0. Write P_λ^A and P_κ^A for their continuous path laws on [0,T], each conditioned on the same increasing terminal target event A. Then

\[
\|P_\lambda^A-P_\kappa^A\|_{\mathrm{TV}}
\le1-e^{-3n\eta}\le3n\eta.
\]

**Proof.** A path has at most n jumps. Let

\[
B_\lambda(\omega)=\int_0^T\sum_{i:X_i(t)=0}\lambda_i(X(t))\,dt.
\]

The standard finite-jump path likelihood gives, on their common support,

\[
r(\omega)=\frac{dP_\kappa}{dP_\lambda}(\omega)
\ge\exp[-n\eta-(e^\eta-1)B_\lambda(\omega)].
\]

Rate comparison with globally scaled copies of λ and the dilation inequality give a:=p_κ(A)/p_λ(A)≤e^{nη}. Thus

\[
\min(1,r/a)\ge e^{-2n\eta}e^{-(e^\eta-1)B_\lambda}.
\]

In the true Exp-driver representation, B_λ≤∑E_i: the accumulated hazard equals E_i for a fired site and is below E_i for a site not yet fired. Attractiveness makes A a decreasing event in every E_i. For an independent product law, two decreasing functions are positively associated. Apply this to 1_A and exp[−(e^η−1)∑E_i] to obtain

\[
\begin{aligned}
\mathbb E_\lambda[e^{-(e^\eta-1)B_\lambda}\mid A]
&\ge\mathbb E[e^{-(e^\eta-1)\sum_iE_i}\mid A]\\
&\ge\mathbb E[e^{-(e^\eta-1)\sum_iE_i}]
=(1+e^\eta-1)^{-n}=e^{-n\eta}.
\end{aligned}
\]

The overlap of the two conditioned measures is therefore at least e^{-3nη}. Total variation is one minus overlap. This proves the claim. The association inequality can also be proved by conditioning on one coordinate at a time and applying the elementary covariance inequality for two monotone functions.

If the proposed model is also attractive, perform grid sampling and driver lifting in that model. A grid debit ε_grid and rate-band debit η give total conditional-path error at most ε_grid+3nη by the triangle inequality. Numerical sampling and factor errors require their own additional debits.

A conservative one-sided candidate is sufficient and gives a sharper elementary alternative. If e^{-ρ}λ≤κ≤λ, the survival likelihood ratio is at least one and each of the at most n event-rate ratios is at least e^{-ρ}. Thus dP_κ/dP_λ≥e^{-nρ} pathwise. Monotone success gives p_κ(A)≤p_λ(A), so the same minorization holds after conditioning, yielding TV≤1−e^{-nρ}. The two-sided result shows that conservatism is a convenient sufficient implementation choice, not a necessary assumption for rarity-independent conditional-law stability.

## Costs and limitations that must stay visible

The computation theorem can be independent of rate magnitudes in its arithmetic-operation count. Its acquisition theorem cannot generally be independent of the time required to observe a positive hazard. Controlled exponential waiting-time experiments expose that time directly. Exact zero identification also needs an explicit support promise or a separate certificate; finite waiting cannot distinguish zero from an arbitrarily small positive rate.

Finite-bit arithmetic is a remaining implementation obligation, not a consequence of counting table entries. Survival factors may be extremely small and differences of exponentials may cancel. Positive arithmetic, exponent/mantissa or log representations, and directed error bounds can avoid avoidable numerical losses, but those details must be proved and implemented before calling the end-to-end executable a bit-model FPTAS. The final scalar probability for an increasing reachable target has a useful positive lower bound from a feasible activation sequence and the smallest positive hazards, whereas intermediate factors can be much smaller.

The structural promise is equally material. Bounded indegree alone does not bound moral treewidth. Learned or supplied width must be charged, and local tables with d parents have 2^d entries unless additional structure is given. The method does not immediately cover inhibition, recovery/repeated firing, time-varying external schedules, arbitrary non-monotone path evidence, or an unrepresented high-width target constraint.

The justified next claim is therefore a specific theorem and construction for attractive one-shot cascades, with explicit model acquisition and arithmetic assumptions. It is not a generic solution to CTBN inference, rare-event simulation, or hidden-state planning.
