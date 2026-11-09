# P3 complete visible return

Source: https://chatgpt.com/c/6af1fcc7-7bcc-83ec-bc2e-2e1c39dd3ddb
Prompt: P3_FULL_ROBUST_CATALYTIC_KINETIC_REALIZATION_XI_20261110.txt (SHA-256 8ff30a489c717bc6ca197e503ad1314fceede85a45890ffe3ea2fce812510054)
Model: GPT-6 standard, Extra High (dispatch receipt). Response d123e202-ada7-4649-8b44-40668b009ab7. Captured 2026-11-09 UTC. No ZIP visible.

## Complete response (native copy)

## Robust catalytic realization: research continuation

Status: the full universal assertion remains open. The accepted nominal catalytic construction provides a polynomial physical-time spectral gap, but that alone does not establish stability under independently perturbed reaction rates.

I identified a concrete obstruction to one natural robustness strategy, and a separate route that gives a complete perturbation argument on finite classes.

### 1. A population-uniform nominal gap does not imply a gap for the reaction-count chain

Consider the weakly reversible network

\\[ \varnothing\rightleftarrows A+B, \qquad B\rightleftarrows 2B. \\]

Use the supplied catalytic construction, with every catalyst vector of total degree at most a fixed \\(K\\).

For large \\(n\\), consider the two-state set

\\[ S_n=\\{(n,0),(n+1,1)\\}. \\]

At \\((n,0)\\), the next actual firing necessarily enters \\((n+1,1)\\). At \\((n+1,1)\\):

- The reaction returning to \\((n,0)\\) has intensity of order \\(n^{K+1}\\).
- The reactions escaping \\(S_n\\) have combined intensity of order \\(n^K\\).

Consequently, the probability of escaping this set on the next firing is \\(O(1/n)\\).

Let \\(P\\) be the embedded discrete-time chain recording successive firings, with invariant distribution

\\[ \rho(x)=\frac{\pi\_\lambda(x)q(x)} {\mathbb E\_{\pi\_\lambda}q(X)}, \\]

where \\(q(x)\\) is total nominal firing intensity. Testing its stationary Dirichlet form on \\(1\_{S_n}\\) gives

\\[ \frac{\mathcal E_P(1\_{S_n},1\_{S_n})} {\operatorname{Var}\_\rho(1\_{S_n})} =O(n^{-1}). \\]

Since \\(\rho(S_n)\to0\\), the embedded chain has zero \\(L^2(\rho)\\) spectral gap, despite the accepted positive, population-uniform continuous-time gap.

This is not a counterexample to the full realization question. It proves that converting the nominal physical-time gap into a jump-chain gap, then applying a bounded Markov-kernel perturbation theorem, cannot establish robustness for this particular catalytic clock.

The distinction matters: a state may undergo many rapid firings without taking much physical time. Reaction-count mixing and physical-time mixing are therefore different mathematical requirements.

### 2. A robust finite-class realization theorem

There is a complete positive result for finite actual communicating classes, using the accepted nominal construction without changing its catalysts.

Theorem — finite-class robust compilation. For every fixed weakly reversible \\(R\\), the nominal catalytic augmentation admits a deterministic polynomial-bit choice of \\(\delta,T\\) that satisfies all the requested stationary, transient, first-moment, recurrence, and firing-cost conditions on every finite actual class.

The argument does not require knowing or enumerating the individual states of that class.

Step A — bound finite-class size.

The accepted fixed-\\(R\\) global Presburger formula for actual-class membership implies a computable constant \\(b_R\\) such that, whenever \\(\Gamma_R(x_0)\\) is finite,

\\[ \max\_{x\in\Gamma_R(x_0)}|x|\_\infty \le B:=b_R(1+|x_0|\_1). \\]

This follows by fixed-formula Presburger elimination: any bounded feasible fibre has coordinate extrema bounded by fixed-coefficient linear inequalities in the input parameters. The constants can be enlarged to handle congruence cells.

Therefore, with \\(N=|\Gamma|\\),

\\[ N\le \bar N:=(B+1)^d. \\]

Both \\(B\\) and \\(\bar N\\) have polynomial binary descriptions, even though their numerical values may be large.

Step B — bound every perturbation of the stationary law.

For a finite irreducible continuous-time chain, the Markov-chain tree formula expresses its stationary weight at each state as a sum of products of \\(N-1\\) transition rates.

Each aggregated transition rate remains within relative error \\(\delta\\), because it is a positive sum of independently perturbed channel rates.

Consequently, for nominal \\(\pi\\) and perturbed stationary \\(\mu\\),

\\[ \left(\frac{1-\delta}{1+\delta}\right)^{N-1} \le\frac{\mu(x)}{\pi(x)} \le \left(\frac{1+\delta}{1-\delta}\right)^{N-1}. \\]

In particular, for sufficiently small \\(\delta N\\),

\\[ \sup_x\left|\frac{\mu(x)}{\pi(x)}-1\right| \le 8\delta N. \\]

Choose, for example,

\\[ \boxed{ \delta=\min\left\\{ \frac1{16\bar N}, \frac{\epsilon}{128\bar N(1+B)} \right\\}. } \\]

This immediately yields

\\[ \operatorname{TV}(\mu,\pi)<\epsilon/4, \\]

and, using \\(X_i\le B\\),

\\[ \max_i|\mathbb E\_\mu X_i-\mathbb E\_\pi X_i| <\epsilon/4. \\]

Notice that the moment requirement is paid separately through \\(B\\). It is not inferred from total variation without a population bound.

Step C — preserve rapid physical-time mixing.

Let the nominal spectral gap be

\\[ \gamma\ge(C_RV\_\lambda^{p_R})^{-1}. \\]

Since the perturbed stationary density is uniformly comparable to \\(\pi\\), and perturbed edge rates are comparable to nominal edge rates, the stationary Dirichlet forms and variances satisfy

\\[ \mathcal E\_\mu^{\rm pert}(f,f) \ge \tfrac14\mathcal E\_\pi^{\rm nom}(f,f), \qquad \operatorname{Var}\_\mu(f) \le2\operatorname{Var}\_\pi(f). \\]

Thus the perturbed physical-time chain retains a gap

\\[ \boxed{\tilde\gamma\ge\gamma/8.} \\]

This uses stationary variance dissipation and remains valid without detailed balance.

Starting from \\(x_0\\),

\\[ \operatorname{TV}(\mathcal L(X(T)),\mu) \le \frac{e^{-\tilde\gamma T}} {2\sqrt{\mu(x_0)}}, \\]

and

\\[ |\mathbb E X_i(T)-\mathbb E\_\mu X_i| \le \frac{B e^{-\tilde\gamma T}} {\sqrt{\mu(x_0)}}. \\]

An explicit polynomial upper bound for \\(\log(1/\mu(x_0))\\) follows from

\\[ \pi(x_0)\ge e^{-\sum_i\lambda_i} \frac{\lambda^{x_0}}{x_0!}, \qquad \mu(x_0)\ge\tfrac12\pi(x_0). \\]

Selecting a sufficiently large rational

\\[ T=C_RV\_\lambda^{p_R} \operatorname{poly}\big(B,V\_\lambda,\epsilon^{-1}\big) \\]

makes both transient errors less than \\(\epsilon/4\\). Adding stationary and transient errors satisfies the required \\(\epsilon\\) bounds.

Step D — pay for every firing.

All states satisfy \\(x_i\le B\\). Since the finite augmentation has fixed maximum reactant degree \\(D_R\\),

\\[ \sup\_{x\in\Gamma,\tilde\kappa} q\_{\tilde\kappa}(x) \le C_R(1+B)^{D_R}. \\]

Hence

\\[ \mathbb E\_{\tilde\kappa} [\text{total channel firings up to }T] \le C_R T(1+B)^{D_R} \le C_RW^{p_R'} \\]

for a computable fixed exponent \\(p_R'\\). The same polynomial bounds apply to \\(T,\delta^{-1}\\), inverse nominal rates and all compiler bit operations.

This closes the full resource contract on finite actual classes, including arbitrarily rare finite classes. It is not yet a proof for infinite classes.

### 3. A general robustness-transfer principle

The preceding finite-state argument is not the only way to control stationary perturbations. A more promising method for infinite classes is to compare the finite-time paths of the nominal and perturbed processes.

Write

\\[ q(x)=\sum\_{r,w}\kappa\_{r,w}(x)\_{y_r+w}. \\]

As long as the two processes occupy the same population, couple their common channel firings at the smaller of the two intensities. Unmatched firings have total rate at most \\(\delta q(x)\\).

If their common initial distribution is \\(\nu\\), and the nominal process has finite expected reaction activity, then

\\[ \boxed{ \Pr(\text{the coupled paths separate by }T) \le \delta\int_0^T\mathbb E\_\nu^{\rm nom}q(X_t)\\,dt. } \tag{1} \\]

This comparison remains valid with independent errors for every labelled catalytic channel. It charges all firings, including the extra catalytic ones.

It also provides a first-moment bound. If the second moments of both processes at time \\(T\\) are at most \\(M_2\\), then Cauchy–Schwarz gives

\\[ \boxed{ |\mathbb E X_i^{\rm pert}(T) -\mathbb E X_i^{\rm nom}(T)| \le 2\sqrt{M_2\\,p_T}, } \tag{2} \\]

where \\(p_T\\) denotes the separation probability.

This avoids the invalid step of inferring first-moment accuracy directly from total variation.

#### The transfer theorem

Suppose a fixed catalytic realization has the accepted nominal gap and, uniformly for all sufficiently small admitted perturbations, possesses:

1. Nonexplosion, positive recurrence and a unique perturbed stationary law.
2. Polynomial-\\(W\\) stationary moments of order \\(s\ge\max(2,D_R)\\), where \\(D_R\\) is the maximum catalytic reactant degree.
3. Polynomial-\\(W\\) moments of the same order for both nominal and perturbed processes started at \\(x_0\\), and for the nominal process started from the perturbed stationary law, uniformly over time.

Here \\(s,D_R\\) are fixed because the augmentation is fixed.

Then the entire robust realization contract follows, with polynomial-\\(W\\) choices of \\(\delta^{-1},T\\), and expected firing cost.

To see the stationary step, initialize the nominal process at \\(\mu\_{\tilde\kappa}\\). Since \\(\mu\_{\tilde\kappa}\\) is stationary under the perturbed process,

\\[ \begin{aligned} \operatorname{TV}(\mu\_{\tilde\kappa},\pi\_\lambda) \le {}& \operatorname{TV}(\mu\_{\tilde\kappa}P_T,\pi\_\lambda)\\\ &+\delta\int_0^T \mathbb E\_{\mu\_{\tilde\kappa}}^{\rm nom}q(X_t)\\,dt. \end{aligned} \tag{3} \\]

The second term is at most \\(\delta T\operatorname{poly}\_R(W)\\).

For the first term, truncate the initial distribution for the proof, not the chemical network. The assumed second-moment bound makes its mass outside a polynomial radius arbitrarily small. Within that radius, the nominal \\(L^2(\pi)\\) gap gives uniform polynomial-time mixing because

\\[ -\log\pi\_\lambda(x) \le \sum_i\lambda_i +\sum_i x_i|\log\lambda_i| +\sum_i\log(x_i!), \\]

which is polynomially bounded in \\(W\\) and the truncation radius.

Equations (1)–(3), together with second-moment bounds, control stationary TV, stationary means, transient TV and transient means. Higher moments control expected firings.

Thus independent coefficient errors do not require a separate perturbed spectral-gap theorem once sufficiently strong uniform stochastic moment bounds are available.

This reduces the remaining universal obstacle to a structural question:

> Can one construct a fixed catalytic circulation with a uniform, polynomially quantitative recurrence and moment certificate under independent relative coefficient errors on every infinite actual class?

The nominal gap resolves the mixing interface; it does not by itself provide that certificate.

### 4. A complete robust result for one-dimensional stoichiometric systems

The transfer theorem can be completed on infinite classes when the stoichiometric subspace has dimension at most one.

Theorem — rank-one robust catalytic realization. Let \\(R\\) be any fixed finite weakly reversible reaction structure satisfying

\\[ \dim\operatorname{span}\_{\mathbb R} \\{z_r-y_r:r\in R\\}\le1. \\]

Then the full robust realization assertion is affirmative for \\(R\\), including infinite actual communicating classes, arbitrary rational activities, independently perturbed catalytic coefficients, both absolute first-moment requirements, and the polynomial bit/firing resource constraints.

This uses the accepted catalytic augmentation and a new perturbation argument.

#### Proof: dominant reaction degrees provide robust recurrence

First consider one species, with population \\(n\\).

Ignore zero-population-change reactions for the drift calculation, but retain their firings in the resource accounting. Let

\\[ M=\max\_{r:z_r\ne y_r}y_r. \\]

Weak reversibility gives two facts:

- Every reaction increasing population has \\(y_r\<M\\).
- At least one reaction with source \\(M\\) strictly decreases population.

The second fact follows because a nontrivial outgoing reaction from a globally maximal complex cannot lead to a larger complex.

For the fixed catalytic augmentation of maximum catalyst degree \\(K\\), write

\\[ b\_{\tilde\kappa}(n) =\sum\_{z_r>y_r,w}\tilde q\_{r,w}(n), \qquad d\_{\tilde\kappa}(n) =\sum\_{z_r\<y_r,w}\tilde q\_{r,w}(n). \\]

The increasing reactions have polynomial degree at most \\(M+K-1\\), whereas the decreasing reactions include a strictly positive term of degree \\(M+K\\).

Writing \\(V=1+\lambda+\lambda^{-1}\\), the accepted nominal rate formula and any relative perturbation \\(\delta\le1/2\\) therefore give computable fixed constants such that, for sufficiently large \\(n\\),

\\[ \boxed{ b\_{\tilde\kappa}(n) \le C_RV^{a_R}(1+n)^{M+K-1}, } \\]

\\[ \boxed{ d\_{\tilde\kappa}(n) \ge c_RV^{-a_R}n^{M+K}. } \\]

Crucially, these inequalities hold for every independent choice of perturbed coefficients.

Let \\(J_R\\) be the maximum absolute population change of a reaction. For

\\[ n\ge C_RV^{b_R}, \\]

the negative reaction intensity dominates the positive intensity by enough to offset the factor \\(J_R\\).

For each fixed positive integer \\(s\\), the generator therefore satisfies

\\[ \tilde L(1+n)^s \le -c\_{R,s}V^{-a\_{R,s}} (1+n)^{s+M+K-1} \\]

outside a polynomially bounded population interval. Enlarging a polynomial bound over the remaining finite interval gives

\\[ \boxed{ \tilde L(1+n)^s \le A\_{R,s}(V)-b\_{R,s}(V)(1+n)^s, } \tag{4} \\]

where \\(A\_{R,s}\\) and \\(b\_{R,s}^{-1}\\) have computable polynomial bounds in \\(V\\).

This yields:

\\[ \sup\_{\tilde\kappa}\sup\_{t\ge0} \mathbb E\_{x_0}^{\tilde\kappa}(1+X(t))^s \le (1+x_0)^s+\frac{A\_{R,s}}{b\_{R,s}}, \\]

and

\\[ \sup\_{\tilde\kappa} \mathbb E\_{\mu\_{\tilde\kappa}}(1+X)^s \le\frac{A\_{R,s}}{b\_{R,s}}. \\]

The linear-population drift also proves nonexplosion by stopping at increasing population levels; a Foster–Lyapunov argument then gives positive recurrence and uniqueness on every nonsingleton class.

Because \\(s\\) can be any fixed integer, choose it larger than both twice the moment degree and the largest catalytic reactant degree. All expected firing rates, transient second moments and stationary second moments are consequently polynomially bounded.

Applying the transfer theorem proves the four distributional and moment error requirements with rational

\\[ \delta^{-1},T\le C_RW^{p_R}. \\]

No perturbed invariant density, perturbed spectral-gap estimate or stationary sampler is used.

#### Extension to arbitrary species count with rank-one stoichiometry

Choose a primitive integer direction \\(v\\) for the stoichiometric subspace.

If \\(v\\) has both positive and negative coordinates, a strictly positive linear conservation law exists. Every class is consequently finite, and Section 2 applies.

Otherwise orient \\(v\ge0\\). All accessible populations lie on an affine integer line

\\[ x=x_0+kv. \\]

Coordinates with \\(v_i=0\\) are conserved. They determine which reaction linkages can be active, using only comparisons with fixed reactant thresholds.

For every active linkage, degree in the growing coordinates plays the role of reactant order in the one-species proof. A population-increasing reaction strictly increases that degree, and its product complex must be a source in the same linkage. Thus the maximum active source degree has strictly decreasing reactions and no increasing reactions.

For sufficiently large \\(|x|\_1\\), the highest-degree decreasing catalytic intensity dominates every increasing intensity. The threshold and coefficient bounds are polynomial in \\(1+|x_0|\_1+V\_\lambda\\), since fixed conserved populations enter only through fixed-degree falling factorials.

The same Foster estimates follow with \\(1+|x|\_1\\) in place of \\(1+n\\). The transfer theorem then supplies robustness, finite-time accuracy, moments and charged firing costs.

All required constants are computable from the fixed reaction/catalyst tables and the accepted nominal-gap constants. Their rational polynomial majorants can be assembled by fixed-exponent arithmetic, so variable-input bit work remains polynomial in the complete binary length.

This establishes an infinite-class extension of the finite-state result. It does not cover arbitrary higher-dimensional stoichiometric subspaces.

### 5. The supplied two-species trapping example also admits robust realization

The zero-jump-gap example from Section 1 has a stronger positive property: its continuous-time dynamics admit an explicit Lyapunov function that tolerates independent coefficient perturbations.

Write \\(a=\lambda_A\\), \\(b=\lambda_B\\), and use equal positive circulation weights on both reversible reaction pairs. Define

\\[ F_K(n)=\sum\_{j=0}^K\binom nj \\]

and the nominal rates

\\[ \begin{aligned} q_1(A,B)&=cF_K(A+B),\\\ q_2(A,B)&=\frac{cAB}{ab}F_K(A+B-2),\\\ q_3(A,B)&=\frac{cB}{b}F_K(A+B-1),\\\ q_4(A,B)&=\frac{cB(B-1)}{b^2}F_K(A+B-2). \end{aligned} \\]

As usual, disabled rates are zero. These are exactly the rates produced by the permitted catalytic channels.

Consider the rational, norm-like function

\\[ \boxed{ H(A,B)=(A-B)^2+\beta B^2 +(\beta+a)\mathbf1\_{\\{B=0\\}}, \qquad \beta=2+\frac{2a}{b}. } \\]

The main quadratic term tracks the difference \\(A-B\\), which is preserved by the potentially very fast reaction pair \\(\varnothing\rightleftarrows A+B\\). The boundary correction gives negative drift at \\(B=0\\) without introducing a large positive drift when that fast reaction reverses.

At \\(B=0\\), the only population-changing reaction is \\(\varnothing\to A+B\\), and

\\[ H(A+1,1)-H(A,0)=-a. \\]

Thus \\(\tilde LH(A,0)<0\\) at every \\(A\\), for every admitted positive perturbation.

At \\(B=1\\), the nominal drift simplifies to

\\[ \frac{LH(A,1)}c = 3\beta F_K(A+1) +\frac A b F_K(A-1) +\frac{-2A+3+3\beta}{b}F_K(A). \\]

For \\(A\\) sufficiently large relative to a polynomial in \\(a+a^{-1}+b+b^{-1}\\), its leading term is strictly negative. The strict margin survives independent relative coefficient errors bounded by \\(1/4\\).

For \\(B\ge2\\), collecting the negative terms of the exact nominal drift gives

\\[ \begin{aligned} \frac{LH}{c}={}& -ABF_K(N-2) \left(\frac{2(2B-1)}{ab}+\frac{2B}{b^2}\right)\\\ &-\frac{2AB}{b}F_K(N-1)\\\ &-\frac{(1+\beta)B(B-1)(2B-1)}{b^2}F_K(N-2)\\\ &+\frac{(1+\beta)B(2B+1)}bF_K(N-1) +\beta(2B+1)F_K(N), \end{aligned} \\]

where \\(N=A+B\\).

The negative \\(AB^2\\) and \\(B^3\\) terms dominate the positive terms outside a polynomially bounded population region. Their leading-coefficient margins also persist under independently perturbed rates with \\(\delta\le1/4\\).

Because the accepted catalytic degree is at least two, the resulting drift estimates can be lifted from \\(H\\) to every fixed power \\(H^s\\): the negative leading drift dominates the finite-difference quadratic corrections at large populations. This yields computable polynomial-\\(V\_\lambda\\) Foster bounds

\\[ \boxed{ \tilde L(1+H)^s \le A_s(V\_\lambda)-b_s(V\_\lambda)(1+H)^s, \qquad s=1,2,\ldots } \\]

for all independently perturbed coefficient choices in that range.

Since \\(H\\) is comparable to \\((A+B)^2\\), up to polynomial activity factors, the bounds supply all stationary and transient population moments needed by Section 3.

Conclusion for this particular network: the accepted nominal catalytic clock, combined with this nonradial Foster function and the coupling transfer, satisfies the complete robust stochastic realization and resource requirements, including on its infinite class.

This example demonstrates that a zero spectral gap per firing need not prevent polynomial physical-time robustness. It also illustrates why a universal proof may need class- and boundary-sensitive Lyapunov functions rather than a simple total-population drift.

### 6. Explicit polynomial-resource compiler for the completed cases

The preceding results can be made into one deterministic quantitative construction.

Let

\\[ m_R=\max\left(2,\max\_{r,w}|y_r+w|\_1\right), \\]

and use the established Foster estimates to calculate a rational polynomial majorant

\\[ M=C_RW^{q_R} \\]

for all necessary order-\\(m_R\\) moments, including the perturbed stationary moments and the nominal and perturbed transient moments.

Let \\(Q_R\\) denote the fixed number of labelled catalytic channels. Set

\\[ \zeta=\frac{\epsilon^2}{10^5(1+M)}, \qquad B=|x_0|\_1+\left\lceil\frac M\zeta\right\rceil, \\]

and define the rational bound

\\[ A= 1+\sum_i\lambda_i +B\sum_i(\lambda_i+\lambda_i^{-1}) +d(B+1)^2. \\]

The conditional-Poisson normalization bound implies

\\[ \log\frac1{\pi\_\lambda(x)}\le A \quad\text{for every }x\in\Gamma,\ |x|\_1\le B. \\]

Let \\(\Gamma_0=C_RV\_\lambda^{p_R}\\) be a computable upper bound on the reciprocal nominal gap. Choose

\\[ \boxed{ T=\left\lceil4\Gamma_0(A+\zeta^{-1}+1)\right\rceil } \\]

and

\\[ \boxed{ \delta=\min\left\\{ \delta\_{\rm drift}, \frac14, \frac{\zeta}{4Q_RTM} \right\\}, } \\]

where \\(\delta\_{\rm drift}\\) is the rational tolerance certified by the applicable Foster argument. In the rank-one case and the two-species example above, it can be taken at least \\(1/4\\).

These choices give the nominal mixing estimate

\\[ \sup\_{\substack{x\in\Gamma\\\\|x|\_1\le B}} \operatorname{TV}(P_T(x,\cdot),\pi\_\lambda) \le\zeta. \\]

The coupling inequality gives a separation probability at most \\(\zeta/4\\). Stationary tail truncation costs at most \\(\zeta\\). Thus the stationary and transient TV errors are bounded by small multiples of \\(\zeta\\).

Using the second-moment majorant \\(M\\), their corresponding absolute first-moment errors are bounded by a constant times

\\[ \sqrt{M\zeta}<\epsilon. \\]

Finally,

\\[ \sup\_{\tilde\kappa} \mathbb E[\text{actual firings up to }T] \le2Q_RTM. \\]

All quantities are rational or integers, assembled through fixed-exponent rational arithmetic. Consequently,

\\[ T,\quad\delta^{-1},\quad \max\_{r,w}\kappa\_{r,w}^{-1},\quad \mathbb E[\text{firings}] \le C_R'W^{p_R'} \\]

and the complete binary compiler complexity is polynomial in \\(L\\).

This is a complete compiler extraction wherever the required Foster estimates have been established. Disjoint-species products of such reaction networks also inherit the construction, allowing higher-dimensional examples with multiple independent stoichiometric directions.

### 7. Remaining universal obstacle

The unresolved case is a general infinite communicating class with interacting stoichiometric directions and boundary regimes.

The accepted marked-pair geometry establishes polynomial nominal relaxation. What has not been established is a general construction of a norm-like function, or an equivalent stopping-time certificate, that gives uniformly over independent coefficient errors:

\\[ \tilde L H_s(x) \le A_s-b_s H_s(x), \\]

with polynomially controlled constants and sufficient domination of population moments and firing intensities.

The rank-one proof obtains this from maximal reactant degrees. The two-species proof obtains it from a boundary-corrected quadratic Lyapunov function. Neither mechanism has yet been extended to every weakly reversible reaction graph.

The literature reinforces the need to distinguish these claims. Anderson–Cappelletti–Fan–Kim show that complex-balanced stationary laws need not have a positive physical-time spectral gap without further conditions; Kim–Kim investigate trapping structures responsible for slow convergence.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://arxiv.org\&sz=32)

arXiv+1

&#x20;A research project also reports a proof of the broader weak-reversibility recurrence conjecture in two species, while listing the arbitrary-dimensional conjecture as open; that recurrence result by itself does not supply the quantitative robustness and firing bounds required here.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://constrained.polito.it\&sz=32)

ConStRAINeD



## Final research status

| Scope                                                                                             | Result            |
| ------------------------------------------------------------------------------------------------- | ----------------- |
| Fixed graph, exact conditional-Poisson nominal law                                                | Accepted          |
| Population-uniform nominal physical-time gap                                                      | Accepted          |
| Arbitrary finite actual classes, robust resource-bounded realization                              | Constructed above |
| Infinite classes with stoichiometric rank at most one                                             | Constructed above |
| The specified two-species trapping network, under independent perturbations                       | Constructed above |
| General reduction from robust moment estimates to all four accuracy requirements and firing costs | Constructed above |
| All weakly reversible structures in arbitrary dimension                                           | Open              |
| Universal negative obstruction for every allowed catalytic augmentation                           | Not established   |

The strongest outcome of this continuation is the robustness-transfer principle: the missing stochastic sensitivity and finite-time accuracy interfaces can be handled using nominal mixing, finite-time coupling and moment bounds. The remaining task is to construct a polynomially quantitative, perturbation-stable moment certificate for every interacting higher-rank weakly reversible network.

No full universal affirmative or negative conclusion is justified by the results obtained here.

## Available visible activity

Worked for 53m 6s.

Strengthened robustness analysis through perturbation and drift testing I’ll focus on the missing robustness step: whether the fixed catalytic construction can tolerate independent rate errors while retaining recurrence, whole-law accuracy, absolute moment accuracy, and polynomial firing cost. I’ll first test a perturbation argument using the nominal gap, then look for a uniform drift estimate or a genuine obstruction. Proved stability and embedded gap bounds for jump dynamics Assessed robustness and refined perturbation analysis for shifted weights Assessed perturbation stability and robustness Assessed robustness limits and challenges Developed and assessed one-dimensional robustness and stability routes
Searched 27 websites
The finite-class result is now constructive: a polynomial bound on class size, the Markov-chain tree formula, and the nominal gap supply explicit perturbation and mixing bounds. For infinite classes, a more useful route has emerged: control the moments of the perturbed dynamics directly, then use finite-time coupling to obtain stationary and transient accuracy without needing a perturbed spectral gap. Developed one-dimensional proof and assessed robustness Proved one-dimensional robustness and rank-one stability theorem Assessed robustness and developed partial results Assessed robustness Assessed partial results and refined robustness arguments Assessed robustness Assessed robustness, tested drift, and extended recurrence progress
Searched 11 websites
Assessed recurrence robustness and consolidated results
Used python tool

### Visible Python analysis

```python
import sympy as sp
A,B,a,b,ff0,ff1,ff2=sp.symbols('A B a b F0 F1 F2', positive=True)
beta=2+2*a/b
h=beta+a
H=lambda A,B,indicator: (A-B)**2+beta*B**2+h*indicator
# B>=2 all
d1=sp.expand(H(A+1,B+1,0)-H(A,B,0))
d2=sp.expand(H(A-1,B-1,0)-H(A,B,0))
d3=sp.expand(H(A,B+1,0)-H(A,B,0))
d4=sp.expand(H(A,B-1,0)-H(A,B,0))
expr = d1*ff0+d2*A*B/(a*b)*ff2+d3*B/b*ff1+d4*B*(B-1)/b**2*ff2
target= (-A*B*ff2*(2*(2*B-1)/(a*b)+2*B/b**2)
-2*A*B/b*ff1
-(1+beta)*B*(B-1)*(2*B-1)/b**2*ff2
+(1+beta)*B*(2*B+1)/b*ff1
+beta*(2*B+1)*ff0)
print('differences', [sp.simplify(x) for x in (d1,d2,d3,d4)])
print('zero difference?',sp.simplify(expr-target)==0, sp.factor(sp.simplify(expr-target)))
print('B0 d1', sp.simplify(H(A+1,1,0)-H(A,0,1)))
print('B1 d2', sp.simplify(H(A-1,0,1)-H(A,1,0)))
print('B1 d3', sp.simplify(H(A,2,0)-H(A,1,0)))

```

```text
differences [4*B*a/b + 4*B + 2*a/b + 2, -4*B*a/b - 4*B + 2*a/b + 2, (4*B*a + 2*a + b*(-2*A + 6*B + 3))/b, (-4*B*a + 2*a + b*(2*A - 6*B + 3))/b]
zero difference? True 0
B0 d1 -a
B1 d2 a
B1 d3 -2*A + 6*a/b + 9
```
