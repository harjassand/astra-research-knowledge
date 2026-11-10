# P3 Xi return — full robust realization continuation

Source: https://chatgpt.com/c/6af1fcc7-7bcc-83ec-bc2e-2e1c39dd3ddb
Response: af33ef35-4c83-4200-9c70-35aa61deba8b; latest human turn 494291c9-8eff-43fb-9c71-7fce67487382 (“continue”).
Original question: work/astra-renewed-pro-programmes-20261103/P3_FULL_ROBUST_KINETICS_AFTER_136C_XI_20261110.txt; source SHA-256 96879bfae8b6843884f8815bf7c58e9617ccc316003693a8df0e8492a0f37119.
Model shown: Extra High. Captured 2026-11-10 approximately 04:22 UTC. No ZIP identified in the visible return.

The native read is capped at 20,000 characters and stops mid-sentence. The final visible text follows as a marked transcription; formatting in that tail is reconstructed. No result text has been intentionally omitted.

## Available visible activity

Previous human continuations and their expanded activities:
- “continu4”: Assessed robustness.
- “please continue”: Evaluated stabilization strategies balancing stationarity, reaction rates, robustness, and structure. Developed and refined a robust catalytic framework with spectral and stability proofs. Searched the web.
- “continue”: Evaluated reaction-network dynamics. Tested stability, strengthened the network, and refined recurrence strategy. Searched the web.

Latest “continue” — worked for 27m 24s:
Assessed mathematical plan and developed robustness arguments. Reconciled reaction geometry. Developed robust recurrence, stability, and entropy criteria with boundary controls. Assessed robust constructions and balanced polynomial degrees. Searched the web.

ChatGPT said: The new construction extends the completed backbone case: maximal-molecularity pure-source reactions can provide the required robust inward drift, even when their products create other species. I’m checking whether the same degree argument can be extended from single reactions to short reaction words; that is the potential route toward networks with no direct population-decreasing reaction on a boundary face.

Developed robust catalyst designs using graded drift arguments. Derived graded-clock robustness beyond pure drains. Aligned dominant faces. Computed normalized drift ratios.

ChatGPT said: A second result is taking shape at the structural level. By translating linkage classes with catalysts built from complexes in the other linkages, their leading source degrees can be aligned in every nonnegative population-growth direction. This gives a precise way to eliminate cross-linkage dominance in the bulk, but boundary states can disable the descending reactions, so it is not yet a recurrence proof.

Developed a construction plan. Refined construction and reduced boundary behavior.

## Native response, first 20,000 characters

## P3 — further continuation of the full robust realization problem

**The unrestricted all-\(R\) assertion remains open.** I have obtained another constructive sufficient condition for the full robust compiler. It covers genuinely interacting higher-rank networks that do not possess the previously required immigration–degradation backbone.

The key idea is to assign different fixed catalytic degrees to different original linkage classes, so that population-decreasing reactions have strictly higher total polynomial degree than every population-increasing reaction.

### 1\. A new robust realization theorem: pure-source maximal drains

Let \(\mathcal L_1,\ldots,\mathcal L_m\) be the linkage classes of the original weakly reversible reaction graph. Define

\[
d_\ell=\max_{y\in\mathcal L_\ell}|y|_1,
\qquad
D=\max_\ell d_\ell.
\]

Suppose that for **every species \(i\)** there exists a linkage class \(\mathcal L_{\ell(i)}\) containing an original reaction

\[
\boxed{
d_{\ell(i)}e_i\longrightarrow z_i,
\qquad |z_i|_1<d_{\ell(i)}.
}
\tag{1}
\]

Thus each species has a population-decreasing reaction whose reactant consists entirely of that species and is a maximum-molecularity complex in its linkage class. The product may involve other species.

**Theorem.** Every fixed weakly reversible network satisfying (1) admits the full graph-preserving, independently perturbation-robust conditional-Poisson kinetic compiler, for every original communicating class, rational activity vector and accuracy input, with the stipulated polynomial bit and numerical-resource bounds.

This condition does not require any \(\varnothing\rightleftarrows X_i\) pair, independent species dynamics, or a fully open state space.

#### Catalytic design

Retain the accepted baseline nominal catalytic construction of fixed degree \(K_0\), including all \(w=0\) channels and its polynomial numerical-activity spectral gap.

Choose a larger fixed integer

\[
H\ge K_0+D+3.
\]

For each linkage class selected by condition (1), add a separate positive circulation, using every catalyst vector with

\[
|w|_1\le H-d_\ell.
\]

The coefficient for a selected channel is proportional to

\[
\frac{a_r}{w!\lambda^{y_r}},
\]

where the \(a_r\) form a positive integer circulation in that original linkage class. The added circulation and the baseline can be scaled by a common rational reciprocal-polynomial function of \(V_\lambda=1+\sum_i(\lambda_i+\lambda_i^{-1})\), so that all resulting coefficients are positive, at most one, and have polynomially bounded inverses.

Each translated circulation remains complex balanced at \(\lambda\)\. Summing the circulations therefore preserves the exact conditional-Poisson nominal stationary law on every actual class.

All new channels are original reactions with extra nonnegative catalysts, so the entire population-transition graph is unchanged.

#### Why this construction gives robust inward drift

Let

\[
N=|x|_1.
\]

Consider any selected linkage \(\mathcal L_\ell\)\. A reaction that increases \(N\) must satisfy

\[
|y_r|_1<|z_r|_1\le d_\ell.
\]

Hence \(|y_r|_1\le d_\ell-1\)\. After its catalytic augmentation, every population-increasing channel in that linkage has total reactant molecularity at most

\[
(d_\ell-1)+(H-d_\ell)=H-1.
\]

All population-increasing channels in the baseline also have molecularity at most \(K_0+D\le H-3\)\.

Since there are only finitely many channels, their combined contribution to the positive part of the generator drift of \(N\), under any independently perturbed coefficients with \(\delta\le1/4\), is bounded by

\[
\boxed{
(\widetilde LN)_+(x)
\le C_RV_\lambda^{a_R}(1+N)^{H-1}.
}
\tag{2}
\]

On the other hand, choose a coordinate \(i\) such that

\[
x_i=\max_jx_j\ge N/d.
\]

Condition (1) supplies a decreasing reaction with source \(d_{\ell(i)}e_i\)\. Its added catalyst menu includes

\[
w=(H-d_{\ell(i)})e_i.
\]

The corresponding channel has pure reactant \(He_i\), and therefore intensity

\[
\tilde q_i(x)
\ge c_RV_\lambda^{-b_R}(x_i)_{\underline H}
\ge c_R'V_\lambda^{-b_R}N^H
\]

whenever \(N\ge2Hd\)\.

Every firing of this channel decreases the total population by at least one. Thus

\[
\boxed{
\widetilde LN(x)
\le
-c_RV_\lambda^{-b_R}N^H
+C_RV_\lambda^{a_R}(1+N)^{H-1}.
}
\tag{3}
\]

Crucially, this is valid for **every admitted independent coefficient perturbation**, not merely perturbations preserving complex balance.

The negative term has one extra power of population. Consequently, outside a computable polynomial-\(V_\lambda\) radius,

\[
\widetilde LN(x)\le-c_RV_\lambda^{-b_R'}N^H.
\]

The same degree separation applies to every fixed polynomial moment. For each integer \(s\ge1\), the bounded reaction increments and the finite-difference expansion of \((1+N)^s\) give

\[
\boxed{
\widetilde L(1+N)^s
\le
A_{R,s}(V_\lambda)
-b_{R,s}(V_\lambda)(1+N)^s,
}
\tag{4}
\]

where \(A_{R,s}\) and \(b_{R,s}^{-1}\) have explicit computable polynomial bounds in \(V_\lambda\)\.

These inequalities establish nonexplosion, positive recurrence and uniqueness on nonsingleton classes. They also imply uniform-in-time transient moments and stationary moments of every fixed order, polynomial in \(W\)\.

All channels have reactant molecularity at most \(H\)\. Taking \(s\ge H\) therefore bounds the full labelled firing rate. The accepted moment-to-robustness transfer completes the four requested stationary/transient TV and absolute-mean guarantees, with rational \(T,\delta\), paid firings and polynomial complete-binary compiler work.

Singleton classes remain exact.

**This proves the complete resource-constrained stochastic contract for the new structural class (1).**

### 2\. A genuinely coupled example with no immigration or ordinary degradation

Consider the two-species network

\[
\boxed{
3A\rightleftarrows A+B
\rightleftarrows3B.
}
\tag{5}
\]

There is one linkage class, whose maximum molecularity is three.

It contains both decreasing reactions

\[
3A\longrightarrow A+B,
\qquad
3B\longrightarrow A+B.
\]

The first has pure source \(3e_A\), the second pure source \(3e_B\)\. Both decrease total population from three to two.

The two independent stoichiometric directions are

\[
(-2,1),\qquad (1,-2),
\]

so the network has stoichiometric rank two. Its reactions genuinely couple \(A\) and \(B\)\.

There is no zero complex and no reaction \(X_i\to\varnothing\)\. Nevertheless, the theorem above applies on every actual communicating class, including any infinite class.

Thus this network admits a fixed finite graph-preserving catalytic realization of every specified conditional-Poisson law, robust to independent relative errors, with polynomial accuracy, time and expected actual firing costs.

### 3\. Resolving the two competing firing-chain bottlenecks in the trapping example

The previously supplied calculation showed a sharp tradeoff for

\[
\varnothing\rightleftarrows A+B,\qquad B\rightleftarrows2B.
\]

If both linkages receive the same catalytic degree, the embedded firing chain has zero spectral gap. If the \(B\)\-linkage receives at least two additional degrees, a different tail cut again forces zero gap.

Exactly one additional degree avoids both identified obstructions, but avoiding those cuts did not prove a gap.

I can now close that remaining point **at \(\lambda_A=\lambda_B=1\)**\.

**Proposition.** Give the \(\varnothing\rightleftarrows A+B\) linkage every catalyst of degree at most \(K\ge2\), and give the \(B\rightleftarrows2B\) linkage every catalyst of degree at most \(K+1\)\. Use equal reversible circulation coefficients \(c/w!\)\.

Then the embedded firing chain has a strictly positive Poincaré spectral gap. Equivalently, the nominal continuous-time process satisfies

\[
\boxed{
\sum_x\pi(x)a(x)(f(x)-\pi f)^2
\le G_K\mathcal E_\pi(f,f),
}
\tag{6}
\]

where \(a(x)\) is the total rate of actual channel firings and \(G_K<\infty\) is computable.

The proof establishes an exponential Foster function for the embedded chain, not just positivity of the two previously examined conductance cuts.

#### Construction of the Foster function

Let \(m=K+1\), choose sufficiently small positive rational numbers \(\theta,\alpha,\zeta,\eta\) with

\[
\alpha=\frac{\theta}{4},
\qquad
\zeta=\frac{\alpha}{2m},
\qquad
\eta=\frac{\theta}{100(m+1)},
\]

and put \(r=1+\theta\), \(u=1+\eta\)\.

Define

\[
V(A,B)=r^Ah(B),
\]

where

\[
h(0)=r(1+\zeta),\quad h(1)=1,\quad
h(B)=(1-\alpha)u^{B-2}\quad(B\ge2).
\]

The function is positive and tends to infinity whenever \(A+B\to\infty\)\.

At \(B=0\), only the pair-creation reaction is enabled, and

\[
\frac{PV(A,0)}{V(A,0)}
=\frac1{1+\zeta}<1.
\]

For every fixed \(B\ge1\), let \(A\to\infty\)\. After dividing all intensities by \(cA^{K+1}/(K+1)!\), the limiting rates of pair-death, \(B\)\-birth and \(B\)\-death are, respectively,

\[
mB,\qquad B,\qquad B(B-1).
\]

Pair-birth is lower order.

The limiting generator drift of \(V/r^A\), divided by \(B\), is

\[
m\bigl(r^{-1}h(B-1)-h(B)\bigr)
+\bigl(h(B+1)-h(B)\bigr)
+(B-1)\bigl(h(B-1)-h(B)\bigr).
\tag{7}
\]

At \(B=1\), this equals

\[
m\zeta-\alpha=-\alpha/2<0.
\]

At \(B=2\), it equals

\[
m\bigl(r^{-1}-(1-\alpha)\bigr)
+(1-\alpha)\eta+\alpha<0
\]

for the chosen sufficiently small \(\theta\)\.

For \(B\ge3\), division by \(h(B)\) gives

\[
m\left(\frac1{ru}-1\right)
+(u-1)+(B-1)(u^{-1}-1)<0.
\]

These strict inequalities handle every fixed \(B\) as \(A\to\infty\)\.

For large \(B\), uniformly over \(A\ge0\), the \(B\)\-death intensity dominates \(B\)\-birth and pair-birth. Pair-death also decreases \(V\)\. Direct comparisons of the fixed-degree polynomials \(F_K\) and \(F_{K+1}\) therefore give a computable \(B_0\) and a positive \(\gamma_K\) such that the normalized drift is at most \(-\gamma_K\) for \(B\ge B_0\)\.

For the finitely many values \(B<B_0\), the preceding asymptotics give a computable \(A_0\) with the same strict drift outside \(A<A_0\)\.

Thus

\[
\boxed{
PV\le(1-\gamma_K)V
\quad\text{outside a finite computable set }C.
}
\tag{8}
\]

#### Converting drift into the activity-weighted gap

The embedded chain is reversible with stationary measure

\[
\rho(x)=\frac{\pi(x)a(x)}{\mathbb E_\pi a}.
\]

For any positive \(V\), reversibility gives the ground-state inequality

\[
\mathcal E_P(f,f)
\ge
\sum_x\rho(x)
\left(1-\frac{PV(x)}{V(x)}\right)f(x)^2.
\tag{9}
\]

Apply it to \(f-f(o)\), where \(o=(0,0)\)\. Outside \(C\), (8) controls its squared magnitude. Inside \(C\), finitely many positive-rate original paths connect all states to \(o\), providing a finite path-comparison constant.

Together these inequalities yield

\[
\operatorname{Var}_\rho(f)\le C_K\mathcal E_P(f,f).
\]

Finally, \(a(x)\ge cF_K(A+B)\ge c>0\) and \(\mathbb E_\pi a<\infty\), so the \(\rho\)\-centering can be replaced by \(\pi\)\-centering at finite cost. This proves (6).

The nominal-only robustness theorem from the previous continuation now applies to this graded design at \(\lambda=(1,1)\), giving another complete robust realization for these activities.

More importantly, it proves that the earlier trapping-network zero-gap phenomenon is **not an unavoidable property of its reaction graph**\. A finite one-degree linkage grading removes it while retaining exact product-Poisson stationarity and every original transition edge.

It does not establish an all-activity polynomial gap, nor does it prove that such gradings exist for arbitrary weakly reversible networks.

### 4\. An all-network structural construction: align the leading source faces of every linkage

The previous positive theorem requires pure-source decreasing reactions. The following construction applies to **every fixed weakly reversible network**, without that restriction.

It provides a robust inward-drift property along every fixed, strictly positive polynomial population-growth ray. The property is not sufficient on its own to prove global recurrence.

#### Construction

Let \(C_1,\ldots,C_m\) be the original linkage-class complex sets, and write

\[
P_\ell=\operatorname{conv}(C_\ell).
\]

Choose \(K\ge K_0\), where \(K_0\) is the accepted nominal-gap catalyst degree, and let

\[
U_K=\{u\in\mathbb N^d:|u|_1\le K\}.
\]

For every original reaction in linkage \(\ell\), include the catalyst shifts

\[
\boxed{
w=u+\sum_{j\ne\ell}v_j,
\qquad
u\in U_K,\quad v_j\in C_j.
}
\tag{10}
\]

Also retain the accepted baseline catalyst menu, including \(w=0\)\.

All these sets are finite and depend only on \(R\)\. Assign a positive circulation separately to every translated linkage copy, with positive rational coefficients proportional to \(a_r/\lambda^{y_r}\)\. Rescale to keep every nominal channel coefficient at most one.

The result preserves exact nominal conditional-Poisson stationarity and every original population-transition edge.

#### Equal-support lemma

For \(\alpha\in\mathbb R_{\ge0}^d\), let

\[
h_\ell(\alpha)=\max_{y\in C_\ell}\alpha\cdot y.
\]

Because all complexes and catalysts are nonnegative, the largest exponent \(\alpha\cdot(y_r+w)\) among the augmented source complexes of **each** linkage is exactly

\[
\boxed{
H(\alpha)=
\sum_{\ell=1}^m h_\ell(\alpha)
+K\max_i\alpha_i.
}
\tag{11}
\]

The key point is that \(H(\alpha)\) does not depend on the linkage index.

Indeed, the support function of the translated source set is

\[
h_\ell(\alpha)+
\sum_{j\ne\ell}h_j(\alpha)
+h_{U_K}(\alpha)=H(\alpha).
\]

The baseline menu cannot exceed this value because \(K\ge K_0\) and \(h_j(\alpha)\ge0\)\.

Suppose there is an original reaction with \(\alpha\cdot(z_r-y_r)\ne0\)\. In its strongly connected linkage, take a maximum-\(\alpha\) complex and follow a directed path to a lower-\(\alpha\) complex. Somewhere on that path, an edge leaves the set of maximum complexes, giving

\[
\alpha\cdot(z_r-y_r)<0.
\]

Translate this reaction by catalysts maximizing the other linkage supports. Its augmented source exponent is exactly \(H(\alpha)\)\.

Furthermore, **no** augmented reaction with source exponent \(H(\alpha)\) can have positive \(\alpha\)\-drift: its original source is a maximizer within its linkage, so its product has no larger \(\alpha\)\-value.

Thus

\[
\boxed{
\begin{gathered}
\text{Every linkage has the same maximal source exponent;}\\
\text{all top-exponent reactions have nonpositive }\alpha\cdot\Delta;\\
\text{at least one has strictly negative }\alpha\cdot\Delta
\text{ whenever }\alpha\notin S^\perp.
\end{gathered}
}
\tag{12}
\]

Here \(S\) is the original stoichiometric subspace.

#### Consequence for actual stochastic drift

Fix \(\alpha\in\mathbb Q_{>0}^d\) with \(\alpha\notin S^\perp\), and positive constants \(c_i\)\. Consider the populations

\[
x_i(n)=\lfloor c_i n^{\alpha_i}\rfloor.
\]

Every fixed reactant is eventually enabled, and

\[
(x(n))_{\underline{y_r+w}}
\sim
\left(\prod_i c_i^{y_{ri}+w_i}\right)
n^{\alpha\cdot(y_r+w)}.
\]

By (12), the leading term of the perturbed generator applied to the linear function \(x\mapsto\alpha\cdot x\) is strictly negative. All positive-drift terms have strictly smaller polynomial exponent.

Therefore

\[
\boxed{
\limsup_{n\to\infty}
n^{-H(\alpha)}
\bigl(\widetilde L(\alpha\cdot X)\bigr)(x(n))
<0
}
\tag{13}
\]

uniformly over all independent coefficient perturbations satisfying \(\delta\le1/2\)\.

For each fixed rational \(\alpha\) and fixed positive \(c_i\), the negativity threshold is computable from the finite reaction table and nominal rate bounds. No claim of a threshold uniform over all varying growth exponents is needed for (13).

This is an unconditional structural result for every weakly reversible \(R\)\.

**Its limitation is the boundary.** If some coordinates remain zero or too small to enable a top-exponent reaction, the negative-leading-degree argument can fail. In the trapping network, for example, at \((A,B)=(n,0)\), the only available population-changing reaction initially increases total mass. Yet the whole process can still be recurrent through subsequent reactions.

Thus (13) solves the *interior leading-linkage dominance problem*, but not the interacting boundary-layer problem or the complete kinetic compiler.

### 5\. Reducing the remaining boundary problem to finitely many kinetic regimes

The all-\(R\) alignment construction fails precisely where the leading descending channels are disabled by small species populations. There is, however, an exact finite classification of these possible enablement regimes.

Fix any finite catalytic augmentation, and set

\[
M_R=\max_{r,w,i}(y_{ri}+w_i).
\]

For every state \(x\), define its threshold signature

\[
\sigma_i(x)=\min(x_i,M_R).
\]

Two populations with the same signature enable **exactly the same labelled channels**\. This follows immediately because no channel requires more than \(M_R\) molecules of any species.

There are at most

\[
\boxed{(M_R+1)^d}
\]

such signatures, a finite constant depending only on the compiled network.

Within one signature\:

- Every coordinate below \(M_R\) has a fixed exact value.
- Every other coordinate is at least \(M_R\), so its falling factorials are uniformly comparable to ordinary monomials, with computable constants depending only on \(R\)\.
- All channel intensities are fixed-degree polynomials in the remaining variable populations.
- Their possible leading source faces are described by the normal fans of finitely many computable convex polytopes.

Consequently, **the possible asymptotic enablement and dominant-degree patterns admit finite fixed-\(R\) precompilation**\.

This is useful, but it is not yet the required Foster theorem. Having finitely many regimes does not guarantee that their stochastic transitions combine into a uniformly inward process. Near a boundary, the chain may require several population-increasing or mass-neutral reactions before a population-decreasing transition becomes available. The associated fast-cycle probabilities can depend polynomially on the large coordinates.

The trapping-network calculations demonstrate both sides: the uniform catalytic clock produces a firing-chain bottleneck, while a one-degree grading removes it. For arbitrary higher-rank networks, there is no established universal procedure for selecting mutually compatible gradings across every boundary regime.

The external recurrence literature also makes this distinction important: structural inward-pointing conditions alone are not sufficient for stochastic recurrence in full generality. Strongly endotactic stochastic networks can even be transient, and the broader weakly reversible stochastic recurrence problem remains unresolved in arbitrary dimension. citeturn784125search7turn784125search1

## Consolidated status of this continuation

| Result | Mathematical scope | Status |
|--------|--------|--------|
| Pure-source maximal-drain catalytic compiler | Arbitrary-dimensional weakly reversible networks satisfying condition (1) | **Complete positive** |
| Coupled \(3A\rightleftarrows A+B\rightleftarrows3B\) example | Rank two, no zero complex or ordinary immigration–degradation backbone | Covered by new theorem |
| One-degree linkage grading eliminates the full embedded-chain gap obstruction | The specified trapping network at \(\lambda=(1,1)\) | **Positive gap proved** |
| Minkowski catalyst translation aligns source supports | Every finite weakly reversible network, all nonnegative growth directions | **Constructed** |
| Robust strict leading drift on fixed positive polynomial population rays | Every weakly reversible network with the aligned augmentation | **Proved** |
| Finite classification of channel-enablement regimes and leading source faces | Every fixed finite catalytic augmentation | **Proved** |
| Polynomial stochastic recurrence and moment bounds across every interacting boundary regime | Arbitrary weakly reversible networks | **Open** |
| Full universal compiler satisfying every independent-error and resource requirement | Every \(R\), every actual class | **Open** |

### What is needed for the full endpoint

The remaining

## Continuation of the final sentence and visible tail (transcribed from the web view)

decisive issue is not nominal sampling, normalization, the class geometry, or physical-time mixing. Those operations have accepted solutions.

It is the existence of a universal finite catalytic design whose independently perturbed dynamics remain quantitatively confining across all interacting boundary regimes, including regimes where no single enabled reaction points inward and recurrence depends on sequences of firings.

The new pure-source theorem establishes this confinement by strict degree dominance. The graded trapping example establishes it through a nonradial exponential Foster function. The all-network Minkowski construction removes linkage dominance in the interior, but does not yet control the boundary.

Final determination: This continuation advances the affirmative side with a new higher-rank robust compiler class and an exact graded-clock spectral-gap result. It also supplies an all-network leading-face alignment construction. Neither a full universal affirmative construction nor a universal impossibility proof has been obtained.
