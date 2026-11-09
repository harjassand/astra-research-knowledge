# P3 complete visible return

Source: https://chatgpt.com/c/6af1fcc7-7bcc-83ec-bc2e-2e1c39dd3ddb
Actual prompt: P3_FULL_ROBUST_KINETICS_AFTER_D123_XI_20261110.txt (SHA-256 d2ff5bd7a2da0df584c29090c0d162d2805e97943a2d748c4dd30eea4cc58479).
Model: GPT-6 standard, Extra High, per dispatch receipt. Response 8fe1ecdc-0738-4e11-824a-18d9171627bc. Visible UI shows final and idle; server status was systemError. No ZIP visible.

## Complete response (native copy)

## P3 continuation — robust catalytic kinetics

Universal status: OPEN. I have not established the required robust recurrence and polynomial moment bounds for arbitrary interacting higher-rank weakly reversible networks.

Two further structural results sharpen the problem. The first gives an exact finite-volume representation that preserves nominal conditional-Poisson stationarity without changing the reaction mechanisms. The second identifies a stronger obstruction to ordinary spectral perturbation arguments than the previously accepted zero-gap firing-chain example.

### 1. Exact cycle-preserving finite-volume approximation

The nominal catalytic construction has more structure than merely satisfying complex balance: its stationary probability flux decomposes into translated finite directed cycles with exactly constant flux around each cycle.

Write the positive integer circulation on the original complex graph as

\\[ a_r=\sum\_{C\ni r}m_C, \\]

where \\(C\\) runs over finitely many directed cycles and \\(m_C\\) are positive integers.

For a fixed cycle

\\[ C:\quad y_0\to y_1\to\cdots\to y\_{\ell-1}\to y_0, \\]

a catalyst \\(w\\), and a nonnegative population vector \\(u\\), consider the translated population cycle

\\[ u+w+y_0\to u+w+y_1 \to\cdots\to u+w+y_0. \\]

Every edge is an allowed original catalytic reaction. The nominal stationary flow contributed by this cycle to each edge is exactly

\\[ \boxed{ J\_{C,w,u} = \frac{c\\,m_C}{Z\_\Gamma} \frac{\lambda^{u+w}}{w!\\,u!}. } \tag{1} \\]

It is independent of the position on the cycle.

This identity follows directly by multiplying the mass-action rate by the conditional-Poisson probability. It holds on rare and infinite actual classes, and it requires no lower bound on \\(Z\_\Gamma\\).

#### Exact finite-volume construction

Fix an integer \\(B\ge |x_0|\_1\\). Retain precisely those translated cycles whose every population state lies in

\\[ \Gamma\cap\\{x:|x|\_1\le B\\}. \\]

Retain their complete edge contributions, not just individual transitions that happen to remain in the ball.

Let \\(\Gamma_B^\circ\\) be the communicating component containing \\(x_0\\) in this finite cycle network.

Then:

Theorem. The finite-volume nominal generator has exact stationary distribution

\\[ \boxed{ \pi_B(x)= \frac{\lambda^x/x!} {\displaystyle\sum\_{z\in\Gamma_B^\circ}\lambda^z/z!}, \qquad x\in\Gamma_B^\circ. } \tag{2} \\]

Furthermore:

- The sets \\(\Gamma_B^\circ\\) increase with \\(B\\) and exhaust the actual infinite class \\(\Gamma\\).
- For every fixed population \\(x\\), every original nominal transition intensity is recovered exactly once \\(B\\) is sufficiently large.
- Applying the same independent channel perturbation factor to every contribution from that channel gives finite perturbed generators converging pointwise to the desired infinite-state generator.

Proof. Every retained cycle has equal nominal probability flow through all its edges by (1). Consequently, its contribution has zero net flow at every state. Summing retained cycles preserves this property, establishing (2) on each communicating component.

Each original channel belongs to at least one finite complex cycle. Every enabled occurrence at a fixed state belongs to finitely many translated cycles, and all their populations are eventually included as \\(B\\) increases. Thus all channel intensities are eventually recovered.

Finally, weak reversibility supplies a finite original path in both directions between \\(x_0\\) and any \\(x\in\Gamma\\). Every edge of those paths belongs to a finite translated cycle. A sufficiently large \\(B\\) includes all these cycles, proving exhaustion.

The finite-volume modification is a proof device only; no truncation or state-dependent channel selection is proposed for the physical compiler.

### Why this matters

Ordinary finite-state truncation generally destroys the complex-balanced stationary law at the boundary. The construction above avoids that problem.

It gives a precise new characterization of the infinite-state robustness obstacle. Let \\(\mu_B\\) be the stationary distribution of the finite perturbed generator. If, uniformly in \\(B\\) and independently of all admitted coefficient errors, one can prove

\\[ \boxed{ \mathbb E\_{\mu_B}(1+|X|\_1)^s \le C_RW^{p_R}, \qquad s\ge D_R, } \tag{3} \\]

then the \\(\mu_B\\) are tight. Every subsequential limit is an invariant probability for the full perturbed generator, and its \\(s\\)-th moment obeys the same bound.

Indeed, fixed reaction vectors have bounded size. Therefore, for every finitely supported test function \\(f\\), the function \\(\widetilde Lf\\) also has finite support. Pointwise convergence of the finite generators permits passage to the limit in the stationary equations. The moment bound guarantees finite stationary reaction activity, yielding nonexplosion and positive recurrence on the irreducible actual class.

This eliminates a separate infinite-state stationary-existence problem conditional on (3). The remaining work is to establish (3) with polynomial constants and the required transient moment bounds. The previous conditional transfer theorem then addresses accuracy and firing cost.

### 2. New unconditional polynomial transient-moment theorem

A separate route yields a stronger conclusion directly from the accepted nominal stationary law. It does not assume a Foster–Lyapunov certificate.

Theorem — nominal semigroup moment propagation. Fix any positive integer \\(s\\). For every weakly reversible \\(R\\), every actual class \\(\Gamma\\), every activity \\(\lambda>0\\), every starting state \\(u\in\Gamma\\), and the accepted nominal catalytic process,

\\[ \boxed{ \sup\_{t\ge0} \mathbb E_u^{\rm nom}(1+|X(t)|\_1)^s \le C_s\left[V\_\lambda(1+|u|\_1)^2\right]^s. } \tag{4} \\]

Here \\(C_s\\) is an explicit computable constant depending on \\(s\\), not on the class, its rarity, its size or its reaction rates.

In fact, the result holds for any nonexplosive Markov chain with the same stationary conditional-Poisson law, irrespective of reversibility or its mixing rate.

#### Proof

Write \\(N(x)=|x|\_1\\), \\(\Lambda=\sum_i\lambda_i\\), and

\\[ H_u=\Lambda+\log(u!)-u\cdot\log\lambda. \\]

Because the conditional normalization satisfies \\(Z\_\Gamma\le e^\Lambda\\),

\\[ \pi\_\lambda(u)\ge e^{-H_u}. \\]

The elementary factorial and logarithm inequalities give

\\[ H_u\le 2V\_\lambda(1+N(u))^2. \\]

Select an integer

\\[ q=\left\lceil2V\_\lambda(1+N(u))^2\right\rceil+2, \qquad p=\frac q{q-1}. \\]

Let \\(h_t\\) be the nominal time-\\(t\\) distribution's density with respect to \\(\pi\_\lambda\\). Stationarity and the Markov property imply \\(L^p(\pi\_\lambda)\\) contraction, including for the adjoint semigroup. Hence

\\[ \\|h_t\\|\_p \le\\|h_0\\|\_p =\pi\_\lambda(u)^{-1/q} \le e. \tag{5} \\]

This holds for every \\(t\\), with no spectral-gap assumption.

Next, conditional-Poisson moments admit an explicit bound valid even when their order grows with the input. If \\(P\sim\operatorname{Pois}(\Lambda)\\), then

\\[ \mathbb E\_{\pi\_\lambda}(1+N)^m \le e^{H_u}\mathbb E(1+P)^m. \\]

The Poisson exponential moment and \\(z^m\le m!t^{-m}e^{tz}\\), with \\(t=m/(\Lambda+m)\\), yield

\\[ \bigl[\mathbb E(1+P)^m\bigr]^{1/m} \le e^3(1+\Lambda+m). \\]

Take \\(m=sq\\). Since \\(q\ge H_u\\),

\\[ \left[ \mathbb E\_{\pi\_\lambda}(1+N)^{sq} \right]^{1/q} \le e^{4s}(1+\Lambda+sq)^s. \tag{6} \\]

Finally, Hölder's inequality, (5), and (6) imply

\\[ \begin{aligned} \mathbb E_u^{\rm nom}(1+N(X_t))^s &=\mathbb E\_{\pi\_\lambda}[h_t(1+N)^s]\\\ &\le \\|h_t\\|\_p \left[\mathbb E\_{\pi\_\lambda}(1+N)^{sq}\right]^{1/q}\\\ &\le e^{4s+1}(1+\Lambda+sq)^s. \end{aligned} \\]

The last quantity is bounded by the right side of (4) with a fixed computable integer \\(C_s\\).

Although the proof chooses a potentially numerically large \\(q\\), the compiler need not enumerate moments of order \\(sq\\). It evaluates only the explicit fixed-power rational upper bound in (4), so this introduces no exponential binary computation.

#### Two useful consequences

First, taking \\(s=D_R\\), the maximum catalytic reactant degree, and using \\(\kappa\_{r,w}\le1\\), gives

\\[ \boxed{ \sup\_{t\ge0} \mathbb E_u^{\rm nom}q\_{\rm nom}(X_t) \le C_RV\_\lambda^{D_R}(1+|u|\_1)^{2D_R}. } \tag{7} \\]

Therefore, for every rational \\(T>0\\),

\\[ \boxed{ \mathbb E_u^{\rm nom} [\text{total channel firings by }T] \le C_RT\\,V\_\lambda^{D_R}(1+|u|\_1)^{2D_R}. } \tag{8} \\]

This pays for every nominal catalytic firing, including parallel channels, uniformly over time and without constructing a Lyapunov function.

Second, for any random initial population \\(U\\) supported on the same class,

\\[ \boxed{ \sup\_{t\ge0} \mathbb E^{\rm nom}(1+|X(t)|\_1)^s \le C_sV\_\lambda^s \mathbb E(1+|U|\_1)^{2s}. } \tag{9} \\]

In particular, if a perturbed stationary law is subsequently proved to have polynomial moments of order \\(2s\\), the required moment bound for nominal evolution started from that law follows automatically. That hypothesis in the earlier robustness-transfer theorem is no longer an independent proof obligation.

This is a genuine unconditional improvement to the nominal stochastic interface, but it does not establish the corresponding moments of the independently perturbed process.

### 3. The catalytic clock can also be chosen to satisfy a uniform logarithmic Sobolev inequality

There is a second consequence of the accepted canonical-path construction.

Theorem — weighted coercivity. For every fixed integer \\(m\ge0\\), the fixed catalytic degree \\(K_R\\) can be enlarged, depending only on \\(R,m\\), so that on every actual class,

\\[ \boxed{ \sum\_{x\in\Gamma} \pi\_\lambda(x)(1+|x|\_1)^m \bigl(f(x)-\mathbb E\_{\pi\_\lambda}f\bigr)^2 \le C\_{R,m}V\_\lambda^{p\_{R,m}} \mathcal E\_\pi(f,f). } \tag{10} \\]

To prove it, use the same deterministic pair paths as in the accepted nominal-gap proof. Jensen's inequality reduces the weighted variance to a sum over ordered pairs \\((x,y)\\).

For each pair, the extra weight satisfies

\\[ (1+|x|\_1)^m\le(1+|x+y|\_1)^m. \\]

Thus the original canonical-path congestion calculation acquires only an additional fixed polynomial factor in the pair sum. With \\(J=d+4\\) and the accepted stored-word comparison exponent \\(b_R\\), choosing

\\[ K_R\ge 3(J+m)+b_R \\]

makes the resulting edge congestion uniformly bounded. The previously established anchored conditional-Poisson moment estimate pays the partner-state sum.

Taking \\(m=2\\) yields something stronger than a Poincaré inequality.

For any \\(x\in\Gamma\\),

\\[ \log\frac1{\pi\_\lambda(x)} \le C V\_\lambda(1+|x|\_1)^2. \\]

If \\(g=f-\mathbb E\_\pi f\\) and \\(\nu(x)=\pi(x)g(x)^2/\mathbb E\_\pi g^2\\), then

\\[ \begin{aligned} \operatorname{Ent}\_\pi(g^2) &=\mathbb E\_\pi g^2\\,D(\nu\Vert\pi)\\\ &\le \sum_x\pi(x)g(x)^2\log\frac1{\pi(x)}\\\ &\le C_RV\_\lambda^{p_R}\mathcal E\_\pi(f,f). \end{aligned} \\]

The standard entropy-centering inequality transfers this bound from \\(g\\) to \\(f\\).

Consequently, the larger fixed catalytic augmentation satisfies the Gross logarithmic Sobolev inequality

\\[ \boxed{ \operatorname{Ent}\_{\pi\_\lambda}(f^2) \le C_RV\_\lambda^{p_R}\mathcal E\_\pi(f,f) } \tag{11} \\]

uniformly over every finite or infinite actual class.

Symmetry of the generator is not required: the inequality uses its stationary Dirichlet form. Applying the entropy-dissipation identity to the nominal adjoint semigroup then gives

\\[ \boxed{ D(\mathcal L_x^{\rm nom}(X_t)\Vert\pi\_\lambda) \le e^{-t/(C_RV\_\lambda^{p_R})} \log\frac1{\pi\_\lambda(x)}. } \tag{12} \\]

In particular, nominal mixing is now controlled in relative entropy, not just \\(L^2\\) or total variation.

This improves the nominal theorem for arbitrary \\(R\\). It also supplies a stronger analytic starting point for perturbation theory. However, applying (11) directly to independently perturbed generators still encounters an unbounded error in the nominal reference measure; logarithmic Sobolev control alone does not remove that obstruction.

### 4. A sector decomposition — and a sharper perturbation obstruction

The constant-cycle-flow identity (1) gives a further nominal operator theorem.

Let \\(\ell_R\\) be the maximum length of the finitely many directed complex cycles used in the positive circulation.

For functions \\(f,g\\), the cycle decomposition gives

\\[ \langle f,Lg\rangle\_\pi = \sum\_{C,w,u}J\_{C,w,u} \sum\_{j=0}^{\ell_C-1} f(x_j)\bigl(g(x\_{j+1})-g(x_j)\bigr). \\]

Subtract the arithmetic mean of \\(f\\) around each cycle. The sum of the increments of \\(g\\) around that cycle vanishes. Applying Cauchy–Schwarz and the elementary finite-cycle Poincaré inequality yields

\\[ \boxed{ |\langle f,Lg\rangle\_\pi| \le 2\ell_R \sqrt{\mathcal E\_\pi(f,f)\mathcal E\_\pi(g,g)}. } \tag{13} \\]

This is a strong sector condition, with a constant depending only on the fixed reaction structure.

Together with the weighted inequality (10), it gives compact embedding of the nominal Dirichlet-form domain into \\(L^2(\pi)\\): the contribution outside a population ball decreases uniformly with the ball radius, while the interior is finite-dimensional. Consequently, the closed nominal sectorial generator has compact resolvent.

Thus the enlarged catalytic realization has three useful nominal properties:

- A class-uniform polynomial numerical-activity gap.
- A class-uniform logarithmic Sobolev inequality.
- A fixed strong-sector bound and compact resolvent.

However, independent rate perturbations need not be small form perturbations in the nominal \\(L^2(\pi)\\) geometry.

#### Exact countercalculation

Return to the accepted network

\\[ \varnothing\rightleftarrows A+B, \qquad B\rightleftarrows2B, \\]

and fix \\(\lambda_A=\lambda_B=1\\).

Write \\(F_K(n)=\sum\_{j=0}^K\binom nj\\), and consider

\\[ u_n=(n,0),\qquad v_n=(n+1,1). \\]

The nominal forward and return rates are

\\[ q(u_n,v_n)=cF_K(n), \qquad q(v_n,u_n)=c(n+1)F_K(n). \\]

Choose admissible perturbations that increase every \\(\varnothing\to A+B\\) channel coefficient by \\(1+\delta\\), decrease every \\(A+B\to\varnothing\\) channel coefficient by \\(1-\delta\\), and leave the remaining channel coefficients unchanged.

Set

\\[ t=\frac{\delta}{1-\delta}, \quad f_n(u_n)=1,\quad f_n(v_n)=1+t, \\]

with \\(f_n=0\\) elsewhere.

Direct substitution gives

\\[ \begin{aligned} \frac{\langle f_n,\tilde Lf_n\rangle\_\pi} {c\\,\pi(u_n)F_K(n)} ={}&\frac{\delta^2}{1-\delta}\\\ &- \frac{(1+t)^2\big[(1+\delta)F_K(n+2)+F_K(n+1)\big]} {(n+1)F_K(n)}. \end{aligned} \tag{14} \\]

Because \\(F_K(n+j)/F_K(n)\to1\\) for every fixed \\(j\\), the second term tends to zero.

Meanwhile,

\\[ \\|f_n\\|\_{L^2(\pi)}^2 = \pi(u_n)\left(1+\frac{(1+t)^2}{n+1}\right). \\]

Therefore, for every fixed \\(0<\delta<1/4\\),

\\[ \boxed{ \frac{\langle f_n,\tilde Lf_n\rangle\_\pi} {\\|f_n\\|\_{L^2(\pi)}^2} \sim \frac{c\delta^2}{(1-\delta)K!}\\,n^K \longrightarrow+\infty. } \tag{15} \\]

The independently perturbed generator has unbounded positive numerical range in the nominal \\(L^2(\pi)\\) space, even for arbitrarily small positive coefficient tolerance.

This does not contradict the accepted robust positive-recurrence theorem for this network. Its actual perturbed stationary law changes the local balance between \\(u_n\\) and \\(v_n\\). The nominal Hilbert-space reference does not account for that adjustment.

It does establish a precise limitation: neither the stronger nominal logarithmic Sobolev inequality nor the strong-sector condition can be transferred by simply treating the independent coefficient errors as a uniformly small dissipative-form perturbation.

A successful operator approach would need a perturbation-dependent reference measure or a mechanism that eliminates the fast local imbalance before estimating the slower dynamics.

### 5. An unconditional all-\\(R\\) finite-horizon robustness result

The new nominal moment estimate (7) also gives a positive result for arbitrary \\(R\\), without assuming perturbed recurrence.

Choose a nominal mixing time \\(T\\), using the accepted Poincaré theorem or (12), such that

\\[ \operatorname{TV} (\mathcal L\_{x_0}^{\rm nom}(X(T)),\pi\_\lambda) \le\epsilon/4. \\]

By (7), calculate a rational polynomial bound

\\[ A_R(W)\ge \sup\_{t\ge0}\mathbb E\_{x_0}^{\rm nom}q\_{\rm nom}(X(t)). \\]

Choose

\\[ \delta\le \min\left\\{\frac14,\frac{\epsilon}{8TA_R(W)}\right\\}. \\]

The accepted channelwise coupling then gives

\\[ \Pr(\text{nominal and perturbed paths separate before }T) \le\delta TA_R(W)\le\epsilon/8. \\]

Before their first separation, the paths coincide. Since the nominal chain is nonexplosive, the perturbed chain cannot explode before that separation.

Consequently,

\\[ \boxed{ \Pr\_{\tilde\kappa}(\text{explosion before }T) \le\epsilon/8. } \tag{16} \\]

If explosion is represented by a cemetery state, the finite-horizon law satisfies

\\[ \boxed{ \operatorname{TV} \bigl(\mathcal L\_{\tilde\kappa}(X^\dagger(T)), \pi\_\lambda\bigr) \le3\epsilon/8. } \tag{17} \\]

The rates, \\(T\\), and \\(\delta^{-1}\\) all obey polynomial numerical-\\(W\\) and complete-binary resource bounds. The expected nominal firing count is polynomial as well.

This is unconditional across all weakly reversible structures and all actual classes. But it is deliberately not presented as the full physical realization theorem: a small probability of explosion is not nonexplosion, and a small probability of path separation does not control the perturbed process's unbounded first moments or total firing count.

### 6. Exact remaining problem

The research now has a sharper division of responsibilities.

The accepted nominal construction, combined with the results above, supplies class-uniform nominal mixing, entropy decay, high-order transient moments, and paid reaction activity. The finite-volume cycle construction supplies canonical positive perturbed stationary approximants on growing finite components.

The remaining decisive certificate is a uniform estimate, for all sufficiently small independently perturbed channel coefficients,

\\[ \boxed{ \sup_B \mathbb E\_{\mu_B^{\tilde\kappa}} (1+|X|\_1)^s \le C_RW^{p_R}, } \tag{18} \\]

together with the corresponding uniform-time moment bounds for the perturbed process started at \\(x_0\\), with \\(s\\) sufficiently large to pay for every catalytic firing and first-moment comparison.

One plausible next representation is a perturbation-dependent reference measure obtained by solving the finite fast-cycle balance equations before controlling motion between their effective classes. Equation (15) explains why that correction is necessary for a direct energy argument. Establishing a polynomial, dimension-independent hierarchy of these corrections is still a substantial unresolved problem, not a theorem supplied by this continuation.

The external recurrence literature also cautions against treating nominal complex balance as a general perturbed recurrence theorem. Published tier-structure results cover particular stochastic networks, while the ConStRAINeD research programme identifies arbitrary-dimensional weakly reversible stochastic recurrence as a broader unresolved problem.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.sciencedirect.com\&sz=32)

ScienceDirect+1



## Consolidated result

| Research objective                                                            | Status after this continuation |
| ----------------------------------------------------------------------------- | ------------------------------ |
| All finite actual classes                                                     | Accepted complete              |
| All stoichiometric-rank-one structures                                        | Accepted complete              |
| Explicit two-species trapping network                                         | Accepted complete              |
| Conditional robustness transfer                                               | Accepted complete              |
| Exact Poisson-preserving finite-volume cycle approximation                    | New, proved                    |
| Uniform nominal transient moments and charged nominal firings                 | New, proved                    |
| Weighted nominal Poincaré and logarithmic Sobolev inequalities                | New, proved                    |
| Strong-sector condition and compact nominal resolvent                         | New, proved                    |
| Unbounded positive numerical-range obstruction in nominal \\(L^2\\)           | New, proved                    |
| All-\\(R\\) finite-horizon TV control, allowing cemetery mass                 | New, proved                    |
| Uniform perturbed recurrence, moments and actual firing costs for all \\(R\\) | Open                           |
| Complete universal robust kinetic compiler                                    | Open                           |

Bottom line: This continuation establishes new global nominal analytical machinery and an all-structure finite-time perturbation bound. It also reduces stationary existence under perturbation to a concrete uniform-tightness problem for exact cycle-preserving finite-volume chains. It does not yet resolve the universal positive-or-negative existence question, and none of the conditional results should be promoted to that endpoint.

## Available visible activity

Worked for 41m 16s
    - paragraph: Assessed the problem and tested robustness limits
    - paragraph: I’ll pursue the unrestricted infinite-class case rather than repeat the completed subcases. The central issue is whether the catalytic rates can produce a uniform inward drift even where large reaction fluxes nearly cancel. I’ll examine that through a chemical-potential Lyapunov function and look for a counterexample if the cancellation cannot be controlled.
    - paragraph: Developed stability criteria and robustness bounds through Lyapunov analysis
    - paragraph: Assessed robustness, perturbation stability, and density growth limits
    - paragraph: Assessed robustness of the system
    - paragraph: Assessed robustness and stability barriers while framing rigorous finite-approximation arguments
    - paragraph: Derived and established nominal moment bounds
    - paragraph: Assessed robustness barriers and summarized progress toward nominal control
    - generic: Searched the web
