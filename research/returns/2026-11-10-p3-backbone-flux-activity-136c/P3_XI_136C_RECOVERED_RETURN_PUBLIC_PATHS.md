# P3 return after 8FE1 and interruption

Chat: https://chatgpt.com/c/6af1fcc7-7bcc-83ec-bc2e-2e1c39dd3ddb
Original exact prompt: P3_FULL_ROBUST_KINETICS_AFTER_8FE1_XI_20261110.txt; SHA-256 0491cece241c54c57a98c1f850f92f9e05537039d5e93795bd0e13d5ddd839b4.
Model at dispatch: GPT-6 Standard, Extra High 4/4.
The prior turn timed out without a final; the authorized exact continuation was “please continue.”, user turn 77f99880-c0f7-4587-b5d9-71e62ead5105. Final response 136c6637-6763-4518-a1a7-4409672f6cfc. No ZIP identified.

## Visible activity before interruption

Developed stability proofs using drift methods and supersolutions

Bounded perturbation growth while seeking a universal construction

Assessed recurrence proofs

Searched the web

## Visible activity after continuation

Worked for 32m 10s

Planned the research

I’ll continue with the unrestricted higher-rank case. I’ll test whether the exact cycle decomposition can support a perturbation-stable drift estimate, and distinguish any new theorem from a conditional reduction that still depends on unproved recurrence.

Established entropy bounds and evaluated robustness under perturbations

Evaluated and reassessed robustness arguments

Refined the construction and stability argument

Searched the web

The entropy calculation is valid, but it exposes a specific obstacle: it contains the expected firing rate, and the nominal weighted inequality does not generally control that rate. Fast trapping cycles can make firing activity much larger than the effective escape rate. I’m testing a different catalyst schedule that makes a reversible birth–death subsystem dominate the additional reactions without losing exact nominal stationarity.

Evaluated robust stability and robustness strategies

Evaluated robustness

Assessed recurrence, stabilization, catalyst design, and mixing criteria

Searched the web

## Completed response (verbatim)

## P3 continuation — a new route through stationary flux and entropy

**The unrestricted robust kinetic-realization problem remains open.** The main difficulty is still obtaining polynomial moment bounds for every independently perturbed rate vector on interacting higher-rank infinite classes.

I found a useful alternative to the previous cycle-preserving finite-volume construction: a finite-state approximation that inherits the full nominal weighted Poincaré inequality with exactly the same constant. It also yields an entropy estimate for arbitrary independent rate perturbations.

### 1\. Stationary-flux lumping preserves the nominal coercivity constant

Fix any actual infinite communicating class \(\Gamma\), and let \(Q\) be its accepted nominal generator with stationary conditional-Poisson law \(\pi\)\.

For \(B\ge |x_0|_1\), define

\[
A_B=\{x\in\Gamma:|x|_1\le B\}.
\]

Replace the entire complement by one auxiliary state \(\star\)\. This state exists only in the mathematical approximation, not in the physical reaction system.

For \(x,y\in A_B\), keep the original transition rates. Define

\[
Q_B(x,\star)=\sum_{z\notin A_B}Q(x,z),
\]

and

\[
\boxed{
Q_B(\star,x)=
\frac{\sum_{z\notin A_B}\pi(z)Q(z,x)}
{\pi(\Gamma\setminus A_B)}.
}
\tag{1}
\]

The stationary law on this finite chain is exactly

\[
\pi_B(x)=\pi(x),\qquad
\pi_B(\star)=\pi(\Gamma\setminus A_B).
\]

This follows by aggregating the original stationary probability flows.

The construction has two important features.

First, all independently perturbed physical channels can be aggregated using their actual perturbed coefficients. Each nonzero off-diagonal rate of the resulting perturbed finite chain remains within relative error \(\delta\) of its nominal rate.

Second, for any function \(f_B\) on the finite chain, extend it to \(\Gamma\) by setting \(f=f_B(\star)\) outside \(A_B\)\. Then

\[
\boxed{
\mathcal E_{Q_B,\pi_B}(f_B,f_B)
=
\mathcal E_{Q,\pi}(f,f).
}
\tag{2}
\]

For a population weight \(w(x)=(1+|x|_1)^m\), assign

\[
w_B(\star)=
\mathbb E_\pi[w(X)\mid X\notin A_B].
\]

The weighted variance expressions also agree exactly. Therefore every previously established inequality

\[
\sum_\Gamma\pi(x)w(x)(f(x)-\pi f)^2
\le G\mathcal E_{Q,\pi}(f,f)
\]

holds on **every finite lumped chain with the identical constant \(G\)**\.

This removes the boundary-coercivity problem that occurs when one simply deletes cycles crossing the truncation boundary.

Moreover, as \(B\to\infty\), the finite perturbed generators agree with the actual perturbed generator at each fixed population once its bounded reaction neighbourhood lies inside \(A_B\)\.

### 2\. A perturbative entropy-production inequality

Let \(\mu_B\) be the unique stationary law of a perturbed lumped chain and set

\[
h(x)=\frac{\mu_B(x)}{\pi_B(x)}.
\]

Define nominal entropy dissipation

\[
D(h)=
\sum_{x,y}\pi_B(x)Q_B(x,y)
\left[
h(x)\log\frac{h(x)}{h(y)}
-h(x)+h(y)
\right].
\]

Nominal stationarity ensures that this is precisely

\[
D(h)=-\langle h,Q_B\log h\rangle_{\pi_B}\ge0.
\]

The elementary scalar inequality

\[
\delta|\log z|
\le\frac12(z-1-\log z)+2\delta^2,
\qquad z>0,\quad0<\delta\le\tfrac14,
\]

combined with perturbed stationarity, yields

\[
\boxed{
D(h)\le4\delta^2\,\mathbb E_{\mu_B}q_B(X),
}
\tag{3}
\]

where \(q_B\) denotes the total nominal transition intensity of the lumped chain.

This inequality is valid for arbitrary independent channel perturbations. It does not require detailed balance or a known perturbed stationary density.

Now set \(g=\sqrt h\)\. Since

\[
D(h)\ge2\mathcal E_{Q_B,\pi_B}(g,g),
\]

the accepted weighted Poincaré inequality gives

\[
\boxed{
\mathbb E_{\mu_B}w_B
\le
2\mathbb E_{\pi_B}w_B
+4G\delta^2\mathbb E_{\mu_B}q_B.
}
\tag{4}
\]

Equation (4) is a quantitative bridge between the nominal coercivity theorem and perturbed stationary moments. It holds uniformly in the truncation radius \(B\)\.

The limitation is important: the last term contains actual expected reaction activity, which is not yet bounded. The previously accepted uniform catalytic clock can have very fast local cycles, so it would be unjustified to replace that term by a controlled moment without a further argument.

### 3\. A complete interacting higher-rank class: networks with an immigration–degradation backbone

There is a new affirmative result beyond the previously completed rank-one and disjoint-product cases.

**Theorem.** Let \(R\) be any fixed finite weakly reversible reaction structure that contains, for every species \(i\), the two reactions

\[
\varnothing\longrightarrow X_i,
\qquad
X_i\longrightarrow\varnothing.
\]

All other reactions may have arbitrary fixed molecularity, couple any number of species, and belong to arbitrary linkage classes.

Then the **entire robust catalytic realization contract is achievable**, including independent channel errors, exact nominal product-Poisson stationarity, all four accuracy requirements, polynomial bit work, and polynomial actual firing cost.

The additional reactions need not form disjoint subsystems.

#### Construction

Let \(D=\max_r|y_r|_1\)\. Retain the accepted full catalytic baseline of degree \(K_0\), with its positive complex-balanced circulation.

Superimpose a separate reversible catalytic circulation on every pair \(\varnothing\rightleftarrows X_i\), using all catalyst vectors of degree at most

\[
K_b=K_0+D+3.
\]

If both circulations contribute to the same labelled channel, add their nominal rate constants. Choose their rational scales to be positive and bounded above and below by reciprocal fixed powers of

\[
V_\lambda=1+\sum_i(\lambda_i+\lambda_i^{-1}),
\]

while ensuring every individual resulting rate is at most one.

Both circulations are complex balanced at \(\lambda\), so their sum preserves the exact product-Poisson law. All channels have original reaction vectors and preserve the entire directed state graph.

Write \(N=|x|_1\)\. The additional immigration intensity for each species is

\[
q_i^+(x)=c_b F_{K_b}(N),
\]

and the additional degradation intensity is

\[
q_i^-(x)=c_b\frac{x_i}{\lambda_i}F_{K_b}(N-1).
\]

Here \(F_K(n)=\sum_{j=0}^K\binom nj\)\.

For every independent perturbation with \(\delta\le1/4\), positivity gives

\[
\sum_i\tilde q_i^-(x)
\ge c_RV_\lambda^{-a_R}(1+N)^{K_b+1}
\]

for all sufficiently large \(N\)\. Meanwhile,

\[
\sum_i\tilde q_i^+(x)
\le C_RV_\lambda^{a_R}(1+N)^{K_b},
\]

and the entire original baseline has intensity at most

\[
C_RV_\lambda^{a_R}(1+N)^{K_0+D}.
\]

Because \(K_b>K_0+D\), degradation has **strictly higher population degree than every possible population-increasing contribution**\.

#### Robust Foster estimates

For each fixed integer \(s\ge1\), use

\[
H_s(x)=(1+|x|_1)^s.
\]

Each added degradation firing decreases \(N\) by exactly one. Each other reaction changes it by a fixed bounded amount. The preceding degree separation implies that, outside a polynomial-\(V_\lambda\) population ball,

\[
\tilde LH_s(x)
\le-c_{R,s}V_\lambda^{-a_{R,s}}
(1+N)^{s+K_b}.
\]

Enlarging the finite interior bound yields explicit polynomially controlled constants \(A_s,b_s>0\) satisfying

\[
\boxed{
\tilde LH_s\le A_s-b_sH_s
}
\tag{5}
\]

uniformly for every admitted collection of perturbed channel coefficients.

The case \(s=1\), combined with bounded reaction jumps, proves nonexplosion. Irreducibility and (5) give positive recurrence and uniqueness. For every fixed \(s\),

\[
\sup_{t\ge0}\mathbb E_{x_0}^{\tilde\kappa}H_s(X_t)
\le H_s(x_0)+A_s/b_s,
\]

and

\[
\mathbb E_{\mu_{\tilde\kappa}}H_s
\le A_s/b_s.
\]

These are polynomial in \(W\)\.

Choose \(s\) large enough to dominate the full augmented reaction degree. The accepted conditional robustness-transfer theorem supplies polynomial rational \(T,\delta^{-1}\), stationary and transient total-variation accuracy, both absolute first-moment requirements, and the expected number of all actual firings.

All rate constants and Foster majorants use fixed-exponent rational arithmetic. Their binary construction cost is polynomial in the complete input length.

**This is a genuinely interacting higher-rank result\:** arbitrary nonlinear weakly reversible reactions may couple the species, while the high-degree reversible backbone supplies robust global confinement.

It does not settle networks lacking such a degradation backbone. In particular, it does not manufacture missing \(\varnothing\rightleftarrows X_i\) transitions, which would violate the graph-preservation requirement.

### 4\. A nominal-only sufficient criterion for the entire robust compiler

The finite-volume and entropy estimates lead to a stronger reduction than the previously accepted moment-to-robustness transfer.

Let \(a(x)\) denote the total nominal intensity of **all labelled firings**, including zero-population-change channels.

Suppose a fixed graph-preserving, exactly conditional-Poisson-stationary catalytic clock has computable polynomial-\(W\) bounds satisfying

\[
\boxed{
\sum_{x\in\Gamma}
\pi(x)a(x)(f(x)-\pi f)^2
\le G_R(W)\mathcal E_\pi(f,f)
}
\tag{6}
\]

for every actual class, together with

\[
a(x)\ge c_RW^{-p_R}(1+|x|_1)^2
\tag{7}
\]

on every nonsingleton class and

\[
\mathbb E_\pi a(X)\le C_RW^{p_R}.
\tag{8}
\]

Call (6) the **activity-weighted Poincaré inequality**\. It is considerably stronger than the accepted physical-time Poincaré inequality.

**Sufficient-criterion theorem.** If a fixed catalytic construction satisfies (6)–(8), and its nominal coefficients and auxiliary constants obey the required compiler bounds, then that construction admits the complete robust kinetic compiler under arbitrary independent sufficiently small relative coefficient errors.

In particular, no separate perturbed recurrence theorem, perturbed Lyapunov construction, perturbed density comparison or perturbed spectral-gap theorem is required.

#### Proof: stationary recurrence and moments

Apply (6) to \(g=\sqrt{\mu_B/\pi_B}\) on the finite lumped chains, using the exact inheritance from Section 1.

Because \(a_B(x)\) bounds the nominal transition intensity \(q_B(x)\), (3)–(4) give

\[
D(h)\le4\delta^2\mathbb E_{\mu_B}a_B
\le4\delta^2\left(G_RD(h)+2\mathbb E_\pi a\right).
\]

Choose

\[
16\delta^2G_R\le1.
\]

Absorption yields

\[
\boxed{
D(h)\le16\delta^2\mathbb E_\pi a,
\qquad
\mathbb E_{\mu_B}a_B\le4\mathbb E_\pi a.
}
\tag{9}
\]

Both estimates are independent of the finite-volume radius.

Since the auxiliary-state weight is the conditional mean of \(a\) in the omitted tail, condition (7) implies

\[
a_B(\star)\ge c_RW^{-p_R}(1+B)^2.
\]

Thus (9) gives \(\mu_B(\star)\to0\), tightness of the remaining masses, and a uniform second-population-moment bound.

Every subsequential limit \(\mu\) is a probability measure on the original actual class, with

\[
\boxed{
\mathbb E_\mu(1+|X|_1)^2\le C_RW^{p_R'}.
}
\tag{10}
\]

The local stationary equations pass to the limit because original reaction increments are bounded. Nonexplosion follows from the transient argument below. Irreducibility then gives positive recurrence and uniqueness.

The ordinary nominal gap and (9) also bound the stationary total variation through the Hellinger distance\:

\[
\boxed{
\operatorname{TV}(\mu,\pi)
\le C_R\delta W^{p_R'}.
}
\tag{11}
\]

Combining this TV bound with the second moments in (10) and the accepted nominal second-moment estimate gives

\[
\max_i|\mathbb E_\mu X_i-\mathbb E_\pi X_i|
\le C_RW^{p_R'}\sqrt{\delta}.
\tag{12}
\]

Choosing a sufficiently small reciprocal-polynomial rational \(\delta\) pays both stationary accuracy requirements.

#### Proof: transient firing cost without a transient Foster function

Let \(\nu_t\) be the distribution of a perturbed finite lumped chain started at \(u\), and put

\[
H(t)=D(\nu_t\Vert\pi_B).
\]

The same scalar entropy inequality gives

\[
H'(t)\le
-\tfrac12 D(h_t)+2\delta^2\mathbb E_{\nu_t}a_B.
\]

The activity-weighted Poincaré inequality supplies

\[
\mathbb E_{\nu_t}a_B
\le G_RD(h_t)+2\mathbb E_\pi a.
\]

After reducing \(\delta\) if necessary and integrating,

\[
\boxed{
\int_0^T\mathbb E_{\nu_t}a_B(X_t)\,dt
\le
4G_R\log\frac1{\pi(u)}
+4T\mathbb E_\pi a.
}
\tag{13}
\]

This bound has no dependence on the truncation radius.

Pass to the actual minimal perturbed process using agreement of the finite approximations until their first exit from \(A_B\)\. By monotone convergence, (13) bounds its expected number of labelled firings.

The bound is finite for every fixed \(u,T\), so the actual process cannot explode. Moreover, the accepted conditional-Poisson atom estimate gives

\[
\log\frac1{\pi(u)}
\le C_RV_\lambda(1+|u|_1)^2.
\]

Consequently, for arbitrary starting populations \(u\in\Gamma\),

\[
\boxed{
\mathbb E_u^{\tilde\kappa}
[\text{actual firings by }T]
\le
C_RW^{p_R'}\bigl((1+|u|_1)^2+T\bigr).
}
\tag{14}
\]

The bound pays for zero-change and parallel-channel firings as well as population-changing reactions.

#### Proof: absolute transient means

Couple nominal and perturbed paths until their first unmatched firing. Its intensity, while the paths agree, is at most \(\delta a(X_t)\)\.

If the first discrepancy occurs at population \(z\), the two populations immediately differ by at most the fixed maximum reaction jump \(J_R\)\.

Equation (14), applied from either resulting population, bounds the expected number of subsequent actual firings by a polynomial in \(W,T,1+|z|_1\)\. The nominal process has the analogous bound from the accepted automatic nominal moment theorem.

Conditioning on the first discrepancy and integrating its intensity gives

\[
\begin{aligned}
&\mathbb E\left[
|X_i^{\tilde\kappa}(T)-X_i^{\rm nom}(T)|
\right]\\
&\quad\le
C_R\delta\int_0^T
\mathbb E_{x_0}^{\rm nom}
\left[
a(X_t)\,
\operatorname{poly}_R(W,T,1+|X_t|_1)
\right]dt\\
&\quad\le C_R\delta W^{p_R'}(1+T)^{p_R'}.
\end{aligned}
\tag{15}
\]

The final inequality uses the accepted unconditional nominal moment bounds at a sufficiently high fixed order.

Choose the nominal mixing time \(T\) polynomially in \(W\), then choose a reciprocal-polynomial rational \(\delta\) small enough for (11), (12), (15), and the usual first-discrepancy TV bound.

This proves all four accuracy requirements and all resource bounds under (6)–(8).

#### The exact unresolved part of this criterion

The accepted all-catalyst nominal clock satisfies (7) and (8), but **does not generally satisfy (6)**\. The previously established trapping-network example has a zero spectral gap for its embedded firing chain, which prevents a uniform activity-weighted inequality for that particular clock.

Thus this theorem is a new sufficient mechanism, not a completed universal construction.

Its advantage is that the remaining certificate is **entirely nominal**\: if a differently graded finite catalyst design can be made to satisfy (6), then independent-error robustness, recurrence, moments, and physical firing costs all follow without constructing a perturbed Lyapunov function.

### 5\. An exact adversarial gauge transformation

There is also a useful necessary tolerance condition for any globally complex-balanced nominal catalytic design.

Let \(v_e=y_r+w\) denote the augmented source complex of channel \(e=(r,w)\), and fix species \(i\)\. Put

\[
M_i=\max_e(v_e)_i.
\]

Suppose \(M_i\ge1\)\. For any rational \(s>0\), define

\[
\lambda_i'=\lambda_i(1+s),
\qquad
\lambda_j'=\lambda_j\quad(j\ne i),
\]

and independently perturb every channel coefficient according to

\[
\boxed{
\tilde\kappa_e
=
\kappa_e(1+s)^{-(v_e)_i}.
}
\tag{16}
\]

If \(s\le\delta/M_i\), every relative coefficient change is at most \(\delta\)\.

But this perturbation has an exact consequence. At every augmented complex \(v_e\),

\[
\tilde\kappa_e(\lambda')^{v_e}
=
\kappa_e\lambda^{v_e}.
\]

Thus **all original complex-balanced flux equations remain exactly satisfied**, now at activity vector \(\lambda'\)\.

The perturbed process therefore has the exact stationary conditional-Poisson law \(\pi_{\lambda'}\)\.

This gives an adversarial family that does not rely on approximations, perturbation theory, or unknown stationary measures.

For an actual class equal to \(\mathbb N^d\),

\[
\mathbb E_{\pi_{\lambda'}}X_i-
\mathbb E_{\pi_\lambda}X_i
=\lambda_i s.
\]

Taking \(s=\delta/M_i\) forces the necessary condition

\[
\boxed{
\delta\le \frac{M_i\epsilon}{\lambda_i}.
}
\tag{17}
\]

For general actual classes, the exact corresponding identity is

\[
\boxed{
\mathbb E_{\pi_{\lambda'}}X_i-
\mathbb E_{\pi_\lambda}X_i
=
\int_0^{\log(1+s)}
\operatorname{Var}_{\pi_{\lambda e^{t e_i}}}(X_i)\,dt.
}
\tag{18}
\]

It follows from differentiating the conditional-Poisson log partition function.

This extends the previously accepted immigration–death tolerance stress test to arbitrary globally complex-balanced catalytic networks. It confirms that absolute mean accuracy can force activity-dependent perturbation tolerances even when exact product-form stationarity survives the perturbation.

It is compatible with the desired polynomial-\(W\) resource bound, so it is not a universal impossibility theorem.

### 6\. Research frontier after this continuation

The current literature still separates deterministic weak reversibility from stochastic recurrence. Recent work announces stronger deterministic permanence results for weakly reversible mass-action systems, but these do not imply polynomial stochastic moments under independently perturbed channel rates. The ConStRAINeD project reports two-species stochastic recurrence while identifying the arbitrary-dimensional case as unresolved; its announced manuscript is not being treated here as a quantitative theorem. citeturn905487view0turn709251search0

The main new results of this continuation are\:

| Result | Scope | Status |
|--------|--------|--------|
| Stationary-flux finite-state lumping with exact weighted-coercivity inheritance | Every nominal weakly reversible catalytic process | Proved |
| Finite-volume entropy-production bound for independent rate errors | Every fixed catalytic design | Proved |
| Complete robust compiler with a full immigration–degradation backbone and arbitrary additional weakly reversible reactions | Interacting, arbitrary-dimensional networks satisfying the backbone condition | Proved |
| Activity-weighted nominal Poincaré criterion implies the complete robust compiler | Every design satisfying explicit computable conditions (6)–(8) | Proved conditionally |
| Exact activity-shift adversarial perturbation | Globally complex-balanced catalytic designs | Proved |
| Existence of an activity-weighted-gap catalytic design for every weakly reversible structure | All \(R\) | Open |
| Universal robust stochastic realization | All \(R\), all actual classes | **Open** |

The most significant new direction is the activity-weighted criterion (6). It replaces the difficult task of directly proving perturbed recurrence with a potentially certifiable **nominal firing-chain inequality**\. Unlike the previous moment-transfer principle, it derives nonexplosion, positive recurrence, stationary moments and finite-horizon firing bounds from that one inequality.

However, the accepted trapping-network example proves that the original uniform catalytic menu cannot satisfy this criterion universally. The next central mathematical challenge is therefore precise: determine whether **finite, reaction-specific and catalyst-specific degree assignments** can eliminate every persistent firing-chain bottleneck while retaining exact complex balance and polynomial numerical resources.

That assertion has not been proved or disproved. The universal question remains open, but the new higher-rank positive class and the nominal-only robustness theorem materially extend the accepted results.

