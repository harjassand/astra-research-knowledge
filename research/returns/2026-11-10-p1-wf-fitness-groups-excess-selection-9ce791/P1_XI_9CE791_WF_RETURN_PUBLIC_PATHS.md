# P1 Xi completed return — Wright–Fisher observation question

Source https://chatgpt.com/c/6af1a606-c6c8-83ec-b948-b552107573bf; response 9ce79149-573a-4ef4-b1c1-4ee92254cc6c; user turn 86fb2e88-247d-41e2-a8a2-f20be7833338.
Exact question: work/astra-renewed-pro-programmes-20261103/P1_FULL_WF_AFTER_13A08D_XI_20261110.txt; source SHA256 269f15634b9069ca977c721e71a3b6670c1c85381cd33efb43ca248f0eee3428, posted text SHA256 f04d52d0a527334c8aa5728b84963b9b7da7d631bb8e02c5ed06661c8130bc3d. Model at generation: GPT-6 Standard Extra High. No ZIP identified.

## Available visible activity

Worked for 32m 41s. Refined multitype selection research and balanced threshold gates.

ChatGPT said: I’m treating the all-K problem as a question of polynomial-time loss of dependence on the initial state. A polynomial mixing bound would let the accepted finite-horizon simulator and stationary compiler meet the full resource contract. The main difficulty is proving that bound uniformly when some mutation rates are very small and selection is arbitrarily strong.

Assessed coupling strategies. Explored connections between duality bounds and stationary duality. Strengthened coupling and spectral contraction analysis. Refined mixing arguments and structural reductions via spectral analysis. Analyzed a two-level case and reduced its fitness classes. Assessed selection and two-level mixing proofs and developed broader mixing bounds. Searched the web.

ChatGPT said: The two-class result now has a complete route: the class total follows the accepted two-allele process, while the within-class frequencies are neutral Wright–Fisher diffusions on clocks running at least as fast as ordinary time. This gives a polynomial cutoff independent of selection strength and a polynomial finite-bit construction below it. I’ve also derived a general-K contraction inequality for a Poisson–Dirichlet auxiliary count kernel, although it does not yet prove global mixing.

Compared grouped dynamics, mixing routes, spectral gaps, and extinction bounds. Assessed mixing results.

ChatGPT said: The broadest new consequence is a sharper ancestral extinction bound for every K: its exponential factor can be expressed in terms of (S − alpha0)+, not S. This gives a second polynomial-resource region even with many distinct fitnesses. I’m assembling the finite-bit cost certificates for both regions and will keep the unresolved strong-selection, three-or-more-fitness-level case explicit.

Refined tractable regimes.

## Complete native response

# Continuation: polynomial-resource results beyond two alleles

The unrestricted all-\(K\) problem remains open, but I obtain a stronger positive result than the accepted \(K=2\) theorem.

**For arbitrary \(K\), if the fitness coefficients have at most two distinct values, the complete Wright–Fisher observation contract admits a computably uniform polynomial-resource algorithm.**

This includes arbitrarily many alleles within either fitness class, arbitrary positive mutation parameters, strong selection, simplex-boundary starting points, arbitrary binary rational times, and the entire shared-latent \(r\)\-observation law.

## 1\. New structural theorem: an exact two-fitness-class decomposition

Partition the alleles into two nonempty sets \(H,D\), where

\[
\sigma_i=S\quad(i\in H),\qquad
\sigma_i=0\quad(i\in D).
\]

Set

\[
a=\sum_{i\in H}\alpha_i,\qquad
b=\sum_{i\in D}\alpha_i.
\]

Write the total frequency of the high-fitness class as

\[
U_t=\sum_{i\in H}X_{t,i}.
\]

The generator of \(U\) is exactly

\[
\boxed{
\mathcal L_U f
=\frac12u(1-u)f''
+\frac12[a-(a+b)u+Su(1-u)]f'.
}
\tag{1}
\]

Thus \(U\) is an autonomous, two-allele Wright–Fisher diffusion.

For \(0<U_t<1\), define the internal class frequencies

\[
Z^H_{t,i}=\frac{X_{t,i}}{U_t},\qquad
Z^D_{t,i}=\frac{X_{t,i}}{1-U_t}.
\]

Let \(\mathcal L_H^0,\mathcal L_D^0\) denote neutral Wright–Fisher generators with the corresponding within-class mutation parameters.

A direct change of variables in the complete multiallelic generator gives

\[
\boxed{
\mathcal L
=
\mathcal L_U+
\frac1u\mathcal L_H^0+
\frac1{1-u}\mathcal L_D^0.
}
\tag{2}
\]

There are no mixed second-order derivatives between these three processes.

Consequently, in the interior, the diffusion has the skew-product representation

\[
\boxed{
X_t=
\left(
U_t Z^H_{A_H(t)},\
(1-U_t)Z^D_{A_D(t)}
\right),
}
\tag{3}
\]

where \(U,Z^H,Z^D\) are independent before the random time changes, and

\[
A_H(t)=\int_0^t\frac{ds}{U_s},\qquad
A_D(t)=\int_0^t\frac{ds}{1-U_s}.
\]

In particular,

\[
A_H(t)\ge t,\qquad A_D(t)\ge t.
\tag{4}
\]

**This is the key improvement\:** arbitrarily strong selection affects the two-class frequency process, but internal allele composition evolves neutrally, with clocks that run at least as fast as ordinary time.

The representation extends to boundary starting points through the continuous entrance laws of the original diffusion. No interior-start promise is introduced.

## 2\. A second result: improved all-\(K\) mixing when mutation competes with selection

There is a separate improvement that applies to **arbitrary fitness patterns**, including three or more distinct selection coefficients.

Define

\[
\Delta=(S-\alpha_0)_+,\qquad D=\lceil\Delta\rceil,
\qquad B=1+L+V.
\]

**Theorem.** The unpruned ancestral process has a uniform expected extinction-time bound

\[
\boxed{
\sup_{n\ge1}\mathbb E T_n
\le16B\left(1+\frac{\Delta}{\alpha_0}\right)4^D.
}
\tag{5}
\]

Consequently, for the required complete observation law,

\[
\boxed{
\operatorname{TV}
\left(\mathcal O_{t,x}^{(r)},\mathcal O_\infty^{(r)}\right)
\le
2^{-\left\lfloor
t/[32B(1+\Delta/\alpha_0)4^D]
\right\rfloor}.
}
\tag{6}
\]

The important distinction from the accepted \(e^S\) estimate is that the exponential term depends on **selection exceeding total mutation**, not on selection alone.

In particular, if

\[
\boxed{
\lceil(S-\alpha_0)_+\rceil
\le\lfloor\log_2B\rfloor,
}
\tag{7}
\]

the mixing certificate is polynomial in \(B\), regardless of the number of distinct fitness coefficients.

This closes another genuine part of the full computational contract: all \(K\), arbitrary fitness profiles satisfying (7), arbitrary boundaries and all binary rational times.

### Proof of the sharper extinction estimate

The accepted ancestral-lineage chain has rates

\[
b_n=\frac{Sn}{2},\qquad
d_n=\frac{n(\alpha_0+n-1)}2.
\]

Let \(e_n=\mathbb ET_n\), with \(\Delta_n=e_n-e_{n-1}\)\. Its accepted birth–death recurrence has minimal nonnegative solution

\[
\Delta_n=
\sum_{j=n}^\infty
\frac1{d_j}
\prod_{\ell=n}^{j-1}
\frac{S}{\alpha_0+\ell-1}.
\tag{8}
\]

For every index interval, the product is bounded by

\[
\boxed{
\prod_{\ell=n}^{j-1}
\frac S{\alpha_0+\ell-1}
\le
\left(1+\frac{\Delta}{\alpha_0}\right)
\binom{2D}{D}
\le
\left(1+\frac{\Delta}{\alpha_0}\right)4^D.
}
\tag{9}
\]

Indeed, the factor at \(\ell=1\), when present, is at most \(1+\Delta/\alpha_0\)\. For \(\ell=k+1\ge2\), factors greater than one can occur only for \(k\le D\), and each is at most \(1+D/k\)\. Their product is \(\binom{2D}{D}\)\. Every subsequent factor is at most one.

Put \(F=(1+\Delta/\alpha_0)4^D\)\. For \(n\ge2\), the recurrence gives

\[
\Delta_n\le\frac{2F}{n-1},
\]

while

\[
\Delta_1\le F(2/\alpha_0+2).
\]

For \(n\) larger than \(2S+2\), every subsequent birth/death ratio is at most \(1/2\), improving the tail estimate to

\[
\Delta_n\le\frac4{n(n-1)}.
\]

Summing the resulting harmonic initial segment and summable tail gives

\[
\sup_ne_n
\le F\left(\frac2{\alpha_0}
+4+2\log(2S+4)\right)+4
\le16BF.
\]

This proves (5). Markov's inequality followed by the strong Markov property proves (6), without a cap or moment-generating-function assumption.

Under (7),

\[
4^D\le B^2,\qquad
1+\Delta/\alpha_0\le B^2,
\]

so the expected extinction time is at most \(16B^5\)\.

This is a **full all-\(K\) polynomial mixing certificate** in that parameter region, not just a two-allele comparison.

## 3\. General fitness-class lifting theorem

The decomposition in (2) actually holds for any number of fitness classes.

Suppose the distinct fitness values are \(\lambda_1,\ldots,\lambda_q\), with classes \(G_1,\ldots,G_q\)\. Define

\[
a_g=\sum_{i\in G_g}\alpha_i,
\qquad
U_g=\sum_{i\in G_g}X_i.
\]

The group-frequency vector \(U\) is itself a \(q\)\-allele selected Wright–Fisher diffusion with mutation parameters \(a_g\) and fitnesses \(\lambda_g\)\.

Conditional on the group-frequency path, the within-class compositions are independent neutral Wright–Fisher diffusions, running on clocks

\[
A_g(t)=\int_0^t\frac{ds}{U_g(s)}\ge t.
\]

The stationary tilted-Dirichlet law has the same factorization: selected group frequencies, followed by independent ordinary Dirichlet compositions within each group.

### Whole-observation mixing transfer

Write \(\mathcal O^{K,r}_{t,x}\) for the original \(K\)\-allele observation law and \(\mathcal O^{q,r}_{t,u}\) for its group-label observation law.

Let \(a_*=\min_g a_g\)\. Then

\[
\boxed{
\operatorname{TV}(\mathcal O^{K,r}_{t,x},\mathcal O^{K,r}_{\infty})
\le
\operatorname{TV}(\mathcal O^{q,r}_{t,u},\mathcal O^{q,r}_{\infty})
+r e^{-a_*t/2}.
}
\tag{10}
\]

To prove this, condition on the complete group path and the ordered group labels of the \(r\) observations.

Suppose \(n_g\) labels belong to group \(g\)\. Neutral ancestral coupling permits replacement of its internal observation distribution by stationary Dirichlet observations with TV error at most

\[
n_g e^{-a_g A_g(t)/2}.
\]

Summing across the groups gives

\[
\sum_g n_g e^{-a_g A_g(t)/2}
\le r e^{-a_*t/2}.
\]

After replacing the internal distributions, the procedure becomes a fixed Markov kernel applied to the ordered group-label observations. Data processing bounds the remaining error by the first term in (10).

This proves the assertion for interior starts. Continuity of the Wright–Fisher transition observation probabilities in the initial state extends the inequality to every simplex boundary point.

### Two-fitness consequence

When \(q=2\), the accepted two-allele OR ancestry gives

\[
\operatorname{TV}(\mathcal O^{2,r}_{t,u},
\mathcal O^{2,r}_{\infty})
\le r e^{-at/2},
\]

where \(a\) is the mutation parameter of the fitter group.

Combining this with (10),

\[
\boxed{
\operatorname{TV}(\mathcal O^{K,r}_{t,x},
\mathcal O^{K,r}_{\infty})
\le2r e^{-a_*t/2}.
}
\tag{11}
\]

This is uniform over \(K,S,x,r\) and all within-group mutation distributions.

A rational cutoff

\[
\boxed{
T_2=\frac{64r}{a_*\epsilon}
}
\tag{12}
\]

satisfies \(T_2\le64B^3\)\. At \(t\ge T_2\), using \(e^{-z}\le1/z\),

\[
\operatorname{TV}
(\mathcal O^{K,r}_{t,x},\mathcal O^{K,r}_{\infty})
\le\frac{\epsilon}{16}.
\]

For \(q=1\), the process is neutral and the corresponding bound is even simpler.

Thus the new polynomial cutoff is proved without introducing a continuous-state sampling oracle or treating repeated fitness classes as two individual alleles.

## 4\. Computably uniform finite-bit realization

Both new polynomial regimes can be handled by one uniform algorithm with the following branch structure.

| Input regime | Transition method | Resource dependence |
|--------|--------|--------|
| \(r=0\) | Empty row | Exact |
| \(t=0\) | Rational Cat\((x)\) draws | Polynomial |
| At most two fitness values | Finite ASG below \(T_2\); stationary compiler above | Polynomial in \(B\) |
| \(D\le\lfloor\log_2B\rfloor\) | Finite ASG below an excess-selection cutoff; stationary compiler above | Polynomial in \(B\) |
| All remaining inputs | Sharpened exponential-excess ASG compiler | Polynomial in \(B+4^D\) |

Every branch preserves the **whole ordered \(r\)\-row observation law** to the certified TV tolerance.

### Stationary sampling without continuous variables

For the two-fitness case, stationary group frequency has density proportional to

\[
e^{Su}\operatorname{Beta}(a,b)(du).
\]

Expand the exponential into positive terms. Define

\[
w_n=\frac{S^n}{n!}\frac{(a)_n}{(a+b)_n}.
\]

Sampling \(n\) with probability proportional to \(w_n\), followed by a Beta\((a+n,b)\) Pólya urn for the ordered group labels and independent within-class Dirichlet Pólya urns, generates the required shared-latent stationary row.

Choose

\[
J=16\left(\lceil S\rceil+
\lceil\epsilon^{-1}\rceil+2\right).
\]

Because \(w_n\le S^n/n!\), \(J\ge6S\), and \(w_0=1\), the total omitted probability satisfies

\[
\Pr(n>J)
\le\sum_{n>J}\frac{S^n}{n!}
\le2^{-J}
\le\frac{\epsilon}{64}.
\tag{13}
\]

Every weight through \(J\) is rational. Exact prefix sums and fair-bit rational selection generate the truncated distribution.

For arbitrary \(K\), the accepted N1795 positive degree-mixture compiler supplies the analogous operation. Its count weights are

\[
\pi(n)\propto
\frac{\prod_i(\alpha_i)_{n_i}\sigma_i^{n_i}/n_i!}
{(\alpha_0)_{|n|}}.
\]

The degree-\(k\) unnormalised mass equals

\[
\frac{\mathbb E_{\operatorname{Dir}(\alpha)}
[(\sigma\cdot Z)^k]}{k!}
\le\frac{S^k}{k!}.
\]

Thus the same polynomial truncation scale works.

Computing the individual rising-factorial coefficients, performing \(K\) truncated polynomial convolutions, sampling the degree, backtracking the count vector, and sampling \(r\) Pólya labels can all be performed using exact rational arithmetic. A conservative bound for this stationary subroutine is \(2^{200}B^{64}\) expected bit operations and fair bits, with no gamma or real-valued Dirichlet draw.

### Finite-horizon simulation

The accepted ASG can be simulated below a polynomial time cutoff using integer uniformisation.

For the two-fitness regime, choose

\[
H_{\rm line}=2^{20}B^8,\qquad
\Lambda=2H_{\rm line}^2,\qquad
M=2^{110}B^{50}.
\]

For \(t<T_2\), the uniformisation parameter obeys

\[
\mu=\Lambda t\le2^{47}B^{19}.
\]

Use \(M\) rational Bernoulli trials with probability \(\mu/M\) to approximate the Poisson number of uniformisation proposals.

The expected number of selection births before \(t\) is at most \(B^2t\), using the accepted logistic first-moment bound for the active-lineage chain.

Therefore,

\[
\Pr(\text{exceed lineage cap})\le\epsilon/64,
\]

and Le Cam's inequality gives

\[
\operatorname{TV}
(\operatorname{Bin}(M,\mu/M),\operatorname{Pois}(\mu))
\le\frac{2\mu^2}{M}\le\epsilon/64.
\]

Thus the finite-time output error is at most \(\epsilon/32\)\.

For the general excess-selection construction, put \(E=4^D\) and choose

\[
\begin{aligned}
T_{\rm exc}&=2^{12}B^5E,\\
H_{\rm line}&=2^{30}B^{14}E,\\
\Lambda&=2H_{\rm line}^2,\\
M&=2^{160}B^{90}E^8.
\end{aligned}
\tag{14}
\]

The new extinction bound guarantees stationary-observation error below \(\epsilon/8\) when \(t\ge T_{\rm exc}\)\.

For \(t<T_{\rm exc}\),

\[
\mu=\Lambda t\le2^{73}B^{33}E^3.
\]

The lineage-cap error is bounded by \(2^{-17}B^{-7}\), and the Poisson-to-binomial replacement error by \(2^{-13}B^{-24}E^{-2}\)\. Each is at most \(\epsilon/64\)\.

All event choices use rational rates. Selection marks can be represented by finitely many exact rational threshold categories. The algorithm never draws a continuous exponential waiting time.

### Explicit work and memory

Using schoolbook integer arithmetic, exact rational comparisons and fair-bit uniform-integer rejection, the resulting uniform implementation satisfies the conservative bounds

\[
\boxed{
\mathbb E[\text{bit work}],\
\mathbb E[\text{fair bits}],\
\text{peak memory bits},\
\text{output work}
\le
2^{600}(B+4^D)^{256}.
}
\tag{15}
\]

The cap, uniformisation proposal count, stored ancestry, mutations, branch marks, precision and preprocessing are all included.

If \(D\le\lfloor\log_2B\rfloor\), then \(4^D\le B^2\)\. Thus

\[
\boxed{
\mathbb E[\text{bit work}],\
\mathbb E[\text{fair bits}],\
\text{peak memory bits},\
\text{output work}
\le2^{1000}B^{512}.
}
\tag{16}
\]

For the two-fitness regime, the improved cutoff yields the sharper conservative bound

\[
\boxed{2^{600}B^{256}.}
\tag{17}
\]

These are explicit universal constants and exponents for the stated regions. The algorithms terminate almost surely, and their costs do not depend polynomially on the numerical magnitude of \(t\) or \(t^{-1}\)\.

The original \(r\)\-label output cost is included.

## 5\. A selection-independent spectral-gap corollary

The two-fitness result also proves a functional inequality for the entire multiallelic diffusion.

Let \(\mu\) be its stationary tilted-Dirichlet law, and define

\[
\mathcal E_\mu(f)
=\frac12\int\nabla f^\top
\bigl(\operatorname{diag}(z)-zz^\top\bigr)
\nabla f\,d\mu.
\]

**Corollary.** If the alleles have at most two distinct fitness values and \(a_*\) is the minimum total mutation parameter of the fitness classes, then

\[
\boxed{
\operatorname{Var}_\mu(f)
\le\frac2{a_*}\mathcal E_\mu(f).
}
\tag{18}
\]

Equivalently, the \(L^2(\mu)\) spectral gap is at least \(a_*/2\), independently of \(S\)\.

For a monomial \(f_y(z)=\prod_{j=1}^r z_{y_j}\), the expectation \(P_tf_y(x)\) is exactly the probability of the observation word \(y\)\. Equation (11) therefore gives

\[
\sup_x|P_tf_y(x)-\mu f_y|
\le2r e^{-a_*t/2}.
\]

Finite linear combinations give the same exponential rate for every polynomial, with a coefficient-dependent prefactor.

Polynomials are dense in \(L^2(\mu)\)\. Since the Wright–Fisher generator is self-adjoint under the tilted-Dirichlet stationary measure, the spectral theorem excludes nonconstant spectral mass below \(a_*/2\)\. This proves (18).

This is stronger than a numerical mixing observation: it is a quantitative Poincaré inequality for arbitrary-dimensional, strongly selected two-fitness-class Wright–Fisher diffusions.

## 6\. A further all-\(K\) result from the gamma-count representation

I also obtain a local contraction inequality for a finite-dimensional auxiliary kernel associated with the Sant–Jenkins–Ruggiero gamma dual. Their exact dual has a reversible count law coupled to standard Dirichlet fibres. citeturn187869view0

Consider the following discrete Gibbs kernel \(G\) on count vectors.

From \(n\), sample

\[
Z\sim\operatorname{Dir}(\alpha+n),
\]

and then independently sample

\[
n'_i\mid Z\sim\operatorname{Pois}(\sigma_iZ_i).
\]

This Gibbs kernel has the gamma-dual stationary count distribution \(\pi\), although it is not the continuous-time gamma dual itself.

Define the multiset edit metric

\[
d_{\rm edit}(n,m)=
\max\left\{
\sum_i(n_i-m_i)_+,\,
\sum_i(m_i-n_i)_+
\right\}.
\]

**Local contraction theorem.** For every \(n\) and \(i\),

\[
\boxed{
W_{d_{\rm edit}}
\bigl(G(n,\cdot),G(n+e_i,\cdot)\bigr)
\le\frac{S}{\alpha_0+|n|+1}.
}
\tag{19}
\]

### Proof

Put \(b=\alpha+n\), \(b_0=\alpha_0+|n|\)\.

Couple the two Dirichlet fibres using the gamma-addition identity\:

\[
Z\sim\operatorname{Dir}(b),\qquad
U\sim\operatorname{Beta}(1,b_0),
\]

independently, and

\[
Z'=(1-U)Z+Ue_i
\sim\operatorname{Dir}(b+e_i).
\]

Generate a common Poisson\((S)\) number of proposals. Each proposal has a label sampled from \(Z\)\. For the second process, replace that proposed label by \(i\) with probability \(U\)\.

Thin both proposals using the same uniform mark, accepting a label \(j\) with probability \(\sigma_j/S\)\.

Whenever no forced replacement occurs, the two resulting count contributions agree. Each forced replacement creates at most one multiset edit.

Consequently,

\[
\mathbb E[d_{\rm edit}(n'^{(1)},n'^{(2)})]
\le S\,\mathbb EU
=\frac{S}{b_0+1}.
\]

This proves (19).

In particular, when \(|n|\ge S\), this is a strict one-step contraction, with factor at most

\[
\frac{S}{S+\alpha_0+1}<1.
\]

The argument works for arbitrary \(K\), unequal mutation parameters and arbitrary nonnegative fitness coefficients.

It is significant because it avoids an \(e^S\) factor at high count levels. However, the factor need not be below one at low count levels. The Gibbs kernel is also not itself the entrance-law evolution required by the transition compiler. Therefore (19) is **not** a polynomial global-mixing theorem for the gamma dual.

## 7\. Exact remaining status

What is now established

- The full finite-bit, polynomial-resource observation contract holds for arbitrary \(K\) with at most two distinct fitness coefficients, even for unbounded numerical \(S\)\.
- It also holds for arbitrary \(K\) and arbitrary fitness patterns when \(\lceil(S-\alpha_0)_+\rceil\le\lfloor\log_2B\rfloor\)\.
- Every fitness-class partition admits the exact skew-product decomposition and observation-mixing transfer (10).
- Two-fitness-class diffusions have the selection-independent Poincaré bound (18).
- The gamma-count Gibbs kernel satisfies the all-\(K\) local contraction inequality (19).

The **unrestricted endpoint is not proved**\. In particular, the remaining difficult region includes

\[
\boxed{
\begin{gathered}
\text{at least three distinct fitness levels},\\
S-\alpha_0>\lfloor\log_2B\rfloor.
\end{gathered}
}
\]

No valid universal \(C,p\) has yet been established there, and no complexity-theoretic impossibility has been proved.

The major unresolved mathematical step is global, quantitative mixing or an alternative direct transition-sampling method whose cost is polynomial when strong selection dominates mutation and several fitness levels interact. The local gamma-count contraction (19) is not sufficient because small-count states can expand.

**Strongest conclusion\:** the accepted exponential-selection result is strengthened in two independent directions—arbitrary-dimensional two-level fitness and arbitrary-dimensional mutation-dominated selection—with complete finite-bit polynomial constructions at their stated scopes. The full all-\(K\), all-selection polynomial capability remains open.
