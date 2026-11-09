# P3 complete Xi return

Source: https://chatgpt.com/c/6af11227-f57c-83ec-80e4-caf25a4bae01
Response: 80d54538-3d58-4644-8a0e-3f6891a1e12e; latest continuation: f098012a-cf4d-4c74-a500-82cbd81e4b9c.
Actual original prompt: P3_FULL_MEAN_CALIBRATION_AFTER_D137_XI_20261109.txt; SHA-256 37c17959011782910ddb6f61f2c06557dc029aa56b8fdf937806f3daf6f4276c. Two subsequent actual user turns each: "please continue."
Model: GPT-6 standard; Extra High shown at check. No ZIP identified in the completed response.

## Available visible activity

Original turn: Developed a structural proof using convexity, moment identities, and bounded-core arguments; Developed geometric bounds and proof for boundary layers; Searched 8 websites.
First continuation: Analyzed geometric assumptions, midpoint structure, support density, and parameter bounds; Strengthened the theorem via congruence geometry and convex proximity; Developed a proof using midpoint compression and balanced congruence classes; Searched 18 websites.
Latest continuation: Worked for 42m 9s. Formulated proof strategy and refined entropy geometry; Developed a geometric proof with locality, support, approximation, and convergence bounds; Developed bounds, convexity, lattice geometry, and midpoint support lemmas; Searched 12 websites.

> A separate structural route is promising: fixed-lattice fibres admit a bounded midpoint-balancing operation. Repeated balancing gives exact local convex witnesses, even when the original populations are exponentially large. I’m checking how much of that operation transfers from the buffered fibres to the entire actual reaction class; that transfer is essential before it can support a universal inverse-height claim.

Refined a structural approach to assess a midpoint balance theorem; Refined inverse bounds and the theorem; Extending the analysis; Searched 21 websites.

## Complete response (verbatim)

# P3 — Further progress on the unrestricted inverse-height problem

**The full polynomial-binary mean-calibration theorem remains unresolved.** The strongest new direction is a discrete-convexity argument that replaces potentially enormous population decompositions with nearby exact convex witnesses.

The argument is complete for the buffered lattice fibres appearing in the accepted E0C/DDB1 geometry. Extending it to an entire communicating class requires an additional compatibility step, which I address separately below.

## 1\. New theorem: uniform local convex witnesses in lattice fibres

Let \(\Lambda\subseteq\mathbb Z^k\) be a fixed integer lattice, and consider

\[
S=(b+\Lambda)\cap\{x\in\mathbb Z_{\ge0}^k:x\ge\ell\},
\]

where the translation \(b\) and lower bound \(\ell\) may be arbitrarily large.

### Theorem

There is a computable constant \(H_\Lambda\), depending only on \(\Lambda\), such that every

\[
m\in\overline{\operatorname{conv}}(S)
\]

has an exact convex decomposition

\[
\boxed{
m=\sum_{j=1}^{k+1}\alpha_jx^{(j)},\qquad
\alpha_j\ge0,\quad\sum_j\alpha_j=1,
}
\tag{1}
\]

where

\[
\boxed{
x^{(j)}\in S,\qquad
\|x^{(j)}-m\|_\infty\le H_\Lambda.
}
\tag{2}
\]

The bound is independent of the translation, population size and target location.

### Proof by Graver midpoint balancing

Let \(\mathcal G(\Lambda)\) be the finite Graver basis, including signed vectors, and define

\[
H_\Lambda=\sum_{g\in\mathcal G(\Lambda)}\|g\|_\infty.
\]

Given \(x,y\in S\), write their difference as a sign-compatible Graver decomposition\:

\[
y-x=\sum_g n_gg,\qquad n_g\in\mathbb Z_{\ge0}.
\]

Put

\[
h=\sum_g\left\lfloor\frac{n_g}{2}\right\rfloor g.
\]

Then

\[
u=x+h,\qquad v=y-h
\]

both belong to \(S\), because they remain coordinatewise between \(x\) and \(y\), and \(h\in\Lambda\)\.

Their sum is preserved\:

\[
u+v=x+y.
\]

Furthermore,

\[
v-u=\sum_g(n_g\bmod2)g,
\]

so

\[
\boxed{\|u-v\|_\infty\le H_\Lambda.}
\tag{3}
\]

Now take a rational convex representation of \(m\) by points of \(S\)\. Clearing its rational weights produces a finite multiset whose arithmetic mean is exactly \(m\)\.

Whenever two points in this multiset differ by more than \(H_\Lambda\) in maximum norm, replace them by their balanced pair \(u,v\)\.

The replacement preserves the sum but strictly decreases

\[
\sum_{\text{points }x}\|x\|_2^2,
\]

because

\[
\|x\|_2^2+\|y\|_2^2
=\frac12\|x+y\|_2^2+\frac12\|x-y\|_2^2.
\]

The energy is a nonnegative integer, so balancing terminates. At termination every pair of multiset points differs by at most \(H_\Lambda\)\. Since their mean is \(m\), every point is within \(H_\Lambda\) of \(m\)\.

Carathéodory's theorem reduces the representation to at most \(k+1\) points without changing that property.

For a limit point in the closed convex hull, take a convergent sequence of finite convex combinations. All resulting nearby witnesses lie in one fixed finite integer box, so a subsequence yields an exact representation of the limit.

This proves the theorem.

### Polynomial-binary witness extraction

The proof used a potentially enormous multiset, but the resulting witness can be computed without constructing that multiset.

For a given rational \(m\), enumerate the integer points satisfying

\[
|x_i-m_i|\le H_\Lambda.
\]

There are at most

\[
(2H_\Lambda+2)^k
\]

such points, a constant for fixed \(\Lambda\) and \(k\)\.

Test their membership in \(b+\Lambda\) using precomputed integer-lattice normal forms, retain those satisfying \(x\ge\ell\), and solve a fixed-size rational linear feasibility problem to obtain (1).

All populations, coefficients and barycentric weights have polynomial binary lengths. The resulting witness construction costs \(\operatorname{poly}_\Lambda(L)\) bit operations.

**This is stronger than merely finding one nearby population\:** it gives a complete mean-preserving probability law supported within a fixed radius of the target.

## 2\. New full inverse theorem: modular population classes of arbitrary rank

A separate construction gives another complete high-rank endpoint. Unlike the multipartite creation family, this one uses a **finite-index lattice congruence** rather than conserved differences between species groups.

Fix integers \(d\ge2\) and \(k\ge1\)\. Consider all reversible reactions

\[
\boxed{
0\rightleftarrows y
\quad\text{for every }y\in\mathbb Z_{\ge0}^d
\text{ with }\sum_i y_i=k.
}
\tag{4}
\]

This is a finite weakly reversible network, with zero complex and arbitrary fixed molecularity \(k\)\.

Its stoichiometric rank is \(d\), so the result applies at genuinely higher rank.

### Exact communicating classes

Let

\[
r=\left(\sum_i x_{0i}\right)\bmod k.
\]

Then

\[
\boxed{
\Gamma_r=
\{x\in\mathbb Z_{\ge0}^d:\sum_i x_i\equiv r\pmod k\}.
}
\tag{5}
\]

To prove this, note that every reaction changes the total population by \(k\), preserving the residue.

Conversely, whenever \(x_i\ge1\), the two-reaction word

\[
0\to(k-1)e_i+e_j,\qquad ke_i\to0
\]

changes \(x\) into \(x-e_i+e_j\)\. Thus individual molecules can be exchanged between species.

Any population of size at least \(k\) can also lose any chosen \(k\)\-molecule subpopulation, because every complex of total molecularity \(k\) is present.

These operations connect all populations sharing the residue \(r\), proving (5) without replacing actual reachability by a formal lattice fibre.

### Reduction to one scalar inverse

Set

\[
t=\sum_i\lambda_i,\qquad p_i=\frac{\lambda_i}{t}.
\]

Under the class-conditioned law, the total population

\[
N=\sum_iX_i
\]

has weights

\[
\Pr_t(N=n)\propto\frac{t^n}{n!},
\qquad n\equiv r\pmod k.
\]

Conditionally on \(N=n\),

\[
X\sim\operatorname{Multinomial}(n;p_1,\ldots,p_d).
\]

Therefore

\[
\boxed{
\mathbb E[X_i]=p_i f_r(t),\qquad
f_r(t)=
\frac{\displaystyle\sum_{n\equiv r\ (k)}n\,t^n/n!}
{\displaystyle\sum_{n\equiv r\ (k)}t^n/n!}.
}
\tag{6}
\]

Feasibility of the target \(m\) is equivalent to

\[
M:=\sum_i m_i\ge r.
\]

Choose a positive rational smoothing parameter

\[
\delta=\frac{\epsilon}{100d}
\]

and proportions

\[
p_i=\frac{m_i+\delta}{M+d\delta}.
\]

These have polynomial binary encoding length, and

\[
|Mp_i-m_i|\le d\delta=\epsilon/100.
\]

It remains to find one positive rational \(t\) with \(f_r(t)\) sufficiently close to \(M\)\.

### Explicit polynomial-bit brackets

The consecutive admissible weights satisfy

\[
\frac{w_t(n+k)}{w_t(n)}
=\frac{t^k}{(n+1)\cdots(n+k)}.
\]

Set

\[
t_{\rm lo}=\frac{\epsilon}{100kd}.
\]

Comparing all admissible populations to \(n=r\) gives

\[
r\le f_r(t_{\rm lo})
\le r+\frac{k\,t_{\rm lo}^{k}}{(1-t_{\rm lo}^{k})^2}.
\tag{7}
\]

Thus if \(M-r\le\epsilon/4\), the lower bracket already provides the requested accuracy after accounting for the smoothing.

Otherwise, choose the least \(s\equiv r\pmod k\) with

\[
s\ge\lceil M\rceil+k+4
\]

and put

\[
t_{\rm hi}=4(s+k).
\]

For \(n<s\), every backward \(k\)\-step weight ratio is at most \(4^{-k}\)\. Consequently,

\[
f_r(t_{\rm hi})
\ge s-k\sum_{j\ge1}j4^{-kj}
>M.
\tag{8}
\]

Both brackets have \(O_{d,k}(L)\) binary digits.

The function \(f_r\) is strictly increasing, since

\[
f_r'(t)=\frac{\operatorname{Var}_t(N)}t>0.
\]

A direct geometric-tail bound on the ratios above gives a uniform second-moment bound

\[
\mathbb E_t[N^2]\le C_k(1+t_{\rm hi}+k)^2
\]

throughout the bracket, for a computable constant \(C_k\)\. Hence

\[
f_r'(t)\le
\frac{C_k(1+t_{\rm hi}+k)^2}{t_{\rm lo}}.
\tag{9}
\]

The right side is numerically possibly enormous but has \(O_{d,k}(L)\) binary digits.

Use rational bisection, evaluating \(f_r(t)\) through the accepted paid DDB1 moment routine at activities \(\lambda_i=tp_i\)\. Explicit moment-error margins and the Lipschitz bound (9) terminate the search after \(O_{d,k}(L)\) steps.

Return

\[
\boxed{\lambda_i=tp_i.}
\tag{10}
\]

Then

\[
|\mathbb E[X_i]-m_i|
\le |f_r(t)-M|+\epsilon/100
<\epsilon.
\]

Every output is a positive ordinary rational; all calls, precision, arithmetic and returned numerator/denominator lengths are polynomial in \(L\)\.

### Scope and compiler consequence

This proves the full polynomial-binary calibration contract for the network (4), including all boundary targets and all residue classes. Its classes are infinite, and no conservative physical population bound is used.

Moreover, the accepted global Presburger class predicate makes the following condition decidable for any fixed weakly reversible \(R\)\:

\[
\forall x,y\ge0,\qquad
x\sim_R y
\iff
\sum_i x_i\equiv\sum_i y_i\pmod k.
\]

Whenever this identity is certified for a fixed \(R\), the same scalar inverse algorithm applies. The decision and its finite preprocessing cost depend only on \(R\)\.

This identifies an effectively recognizable family with a complete inverse compiler, extending beyond the explicit reaction presentation (4).

## 3\. A decidable global midpoint property for actual reaction classes

The lattice theorem above does not automatically extend to an entire communicating class containing exceptional boundary populations. In particular, normalizing two populations into a buffered core does not by itself justify applying their inverse normalization words after balancing.

There is, however, a way to decide the required structural property for **each fixed reaction network**, using the accepted global Presburger class predicate.

Define \(\operatorname{BAL}(R,H)\) to mean that for every \(x,y\) in the same actual communicating class, there are \(u,v\) in that class such that

\[
\boxed{
u+v=x+y,\qquad \|u-v\|_\infty\le H.
}
\tag{11}
\]

Using the accepted Presburger relation \(\Psi_R\), this is the sentence

\[
\begin{aligned}
\forall x,y\ge0\quad \Psi_R(x,y)\Longrightarrow
\exists u,v\ge0:\;&
\Psi_R(x,u)\land\Psi_R(x,v)\\
&\land\ u+v=x+y\\
&\land\ \bigwedge_i|u_i-v_i|\le H.
\end{aligned}
\tag{12}
\]

The assertion

\[
\boxed{\exists H\in\mathbb Z_{\ge0}:\operatorname{BAL}(R,H)}
\tag{13}
\]

is itself a Presburger sentence.

Therefore a deterministic compiler can decide (13) for any fixed \(R\)\. If true, it can compute a suitable integer \(H_R\)\. All quantifier elimination is paid during finite fixed-network compilation.

This yields an exact structural dichotomy, not merely a heuristic test.

### When the test succeeds

The multiset-balancing proof from Section 1 applies verbatim, giving

\[
\boxed{
m\in\overline{\operatorname{conv}}(\Gamma)
\Longrightarrow
m\in\operatorname{conv}
\left(\Gamma\cap[m-H_R,m+H_R]^d\right).
}
\tag{14}
\]

Because \(H_R\) and \(d\) are fixed, all candidate populations inside that box can be enumerated in a constant number of membership checks. Exact rational linear algebra then constructs a distribution

\[
\mu=\sum_{j=1}^{d+1}\alpha_j\delta_{x^{(j)}},
\qquad
\mathbb E_\mu X=m,
\]

with polynomial binary encoding length.

Thus, for networks passing (13), **a locally supported exact mean witness can be constructed in polynomial binary time**, with no supplied decomposition or interior margin.

### Limitation

I have not proved that every weakly reversible reaction structure passes (13).

Failure of the test would establish failure of this particular uniform balancing property, not failure of polynomial-bit equilibrium calibration. The logical distinction matters: (13) is a stronger structural condition than the requested inverse-height conclusion.

## 4\. A quantitative entropy improvement when local balancing holds

Suppose the compiler has certified (13).

Let

\[
\lambda_i^{(0)}=m_i+1,
\qquad
P_0=\bigotimes_i\operatorname{Poisson}(\lambda_i^{(0)}).
\]

The locally supported mean witness from (14) gives an immediate quantitative improvement over the raw factorial-entropy bounds.

### 4.1 Conditioning is not extremely rare at the target-centred activities

For every witness population \(x\),

\[
|x_i-m_i|\le H_R.
\]

Elementary Stirling bounds show that

\[
P_0(Y=x)\ge 2^{-c_R(1+L)}
\]

for a computable constant \(c_R\)\.

Since at least one such \(x\) belongs to \(\Gamma\),

\[
\boxed{
\Pr_{P_0}(Y\in\Gamma)\ge2^{-c_R(1+L)}.
}
\tag{15}
\]

This applies even if the class is exceptionally rare under other activity vectors.

Let \(\pi_0=P_0(\cdot\mid\Gamma)\)\. The local witness \(\mu\) then satisfies

\[
\boxed{
D_{\mathrm{KL}}(\mu\|\pi_0)\le c_R(1+L).
}
\tag{16}
\]

The entropy bound uses a mean-exact witness close to \(m\), rather than the absolute factorial entropy of potentially enormous populations.

### 4.2 A better quantitative inverse radius

Write \(\theta_0=\log\lambda^{(0)}\) and

\[
F(h)=\log\mathbb E_{\pi_0}
\exp\left(h\cdot(X-m)\right).
\]

The Gibbs variational inequality and (16) imply

\[
F(h)\ge-D_{\mathrm{KL}}(\mu\|\pi_0)\ge-K,
\qquad K=c_R(1+L).
\]

Also \(F(0)=0\)\.

Minimize

\[
F(h)+\frac{\tau}{2}\|h\|_2^2,
\qquad
\tau=\frac{\epsilon^2}{8192(K+1)}.
\]

At its minimizer \(h_\tau\),

\[
\frac{\tau}{2}\|h_\tau\|_2^2\le K,
\qquad
\nabla F(h_\tau)=-\tau h_\tau.
\]

Consequently,

\[
\|\nabla F(h_\tau)\|_2
\le\sqrt{2K\tau}<\frac{\epsilon}{64}
\]

and

\[
\boxed{
\|h_\tau\|_2\le\frac{128(K+1)}{\epsilon}.
}
\tag{17}
\]

Since \(\|\theta_0\|_2=O_R(L)\), the accepted radius-to-selector construction now has an explicit sufficient numerical radius

\[
\boxed{
B=O_R\left(\frac{1+L}{\epsilon}\right).
}
\tag{18}
\]

This is substantially sharper than the earlier bound based on absolute factorial entropy, whose numerical size could already be exponential in the population's binary length before accounting for accuracy.

It gives a deterministic calibration algorithm with bit cost

\[
\operatorname{poly}_R(L+\epsilon^{-1})
\]

for every network certified by (13).

In particular, it satisfies the full polynomial-in-\(L\) contract whenever \(\epsilon^{-1}\) is polynomially bounded in \(L\)\.

It still does **not** establish the unrestricted accuracy-bit endpoint, because \(\epsilon^{-1}\) can itself be exponential in \(L\)\.

## 5\. An intrinsic concentration result for calibrated laws

There is another useful consequence that avoids choosing a reference activity vector.

Let

\[
\varphi(x)=\sum_i\log\Gamma(x_i+1).
\]

Its Hessian is bounded\:

\[
0\le\frac{d^2}{dt^2}\log\Gamma(t+1)
=\sum_{n=1}^\infty\frac1{(t+n)^2}
<2,\qquad t\ge0.
\]

Therefore the local mean witness \(\mu\), supported within \(H_R\) of \(m\), satisfies

\[
0\le
\mathbb E_\mu\varphi(X)-\varphi(m)
\le dH_R^2.
\tag{19}
\]

Now suppose \(m\) lies in the relative interior of the class mean polyhedron, so that an exact calibrated Gibbs distribution \(\pi_\theta\) exists.

Among laws with mean \(m\), this Gibbs distribution maximizes

\[
H(\nu)-\mathbb E_\nu\varphi(X).
\]

Its Shannon entropy is bounded by the entropy of independent geometric variables with the same coordinate means\:

\[
H(\pi_\theta)\le
\sum_i\left[
(m_i+1)\log(m_i+1)-m_i\log m_i
\right]
=O_R(1+L).
\]

Comparing \(\pi_\theta\) with \(\mu\), using Jensen's inequality and (19), gives

\[
\boxed{
\mathbb E_{\pi_\theta}\varphi(X)-\varphi(m)
\le O_R(1+L).
}
\tag{20}
\]

Even more specifically,

\[
D_{\mathrm{KL}}(\mu\|\pi_\theta)
=
\mathbb E_\mu\varphi
-\mathbb E_{\pi_\theta}\varphi
+H(\pi_\theta)-H(\mu)
\le O_R(1+L).
\tag{21}
\]

Since \(\mu\) has at most \(d+1\) support points, at least one has \(\mu\)\-probability at least \(1/(d+1)\)\. Equation (21) then implies that some population \(x\) satisfies

\[
\boxed{
\|x-m\|_\infty\le H_R,
\qquad
\pi_\theta(x)\ge2^{-c'_R(1+L)}.
}
\tag{22}
\]

Thus every exactly calibrated equilibrium law in a balance-certified class assigns non-negligible mass—in the binary-complexity sense—to at least one population a fixed distance from its mean.

This is a structural restriction on possible calibrated distributions. It is relevant to inverse height because it provides a near-target anchor whose equilibrium probability cannot be arbitrarily small.

However, a single high-probability local anchor does not yet bound all components of \(\theta\), particularly outward normal directions approaching a boundary face.

## 6\. Current frontier

The new results alter the research picture as follows.

| Result | Mathematical scope | Status |
|--------|--------|--------|
| Uniform local convex witnesses | Buffered lattice fibres with fixed lattice | Proved |
| Full polynomial-bit inverse | Complete fixed-degree creation networks; arbitrary rank and total-residue classes | Proved |
| Deciding global uniform midpoint balancing | Every fixed weakly reversible \(R\), using accepted Presburger class access | Proved |
| Local mean witnesses and target-centred Poisson lower bounds | Networks passing the midpoint test | Proved |
| Inverse radius \(O_R((L+1)/\epsilon)\) | Same certified networks | Proved |
| Polynomial-in-\(L\) inverse for inverse-polynomial accuracy | Same certified networks | Follows |
| Universal polynomial numerical log-activity radius | All fixed weakly reversible \(R\), all binary accuracies | **Open** |

The standard Graver-basis theory provides the fixed finite sign-compatible move sets used in the lattice proof. citeturn831362search4 The broader discrete-midpoint-convexity literature gives related proximity methods, although the exact lattice-balancing result here follows from the explicit construction rather than being imported as an already established general reaction-class theorem. citeturn977593academia37

### What remains to close the full question

Two barriers remain distinct.

First, the bounded midpoint-balancing property has been proved for the lattice cores, but its universal transfer across all exceptional actual-class boundary structures is not established. The Presburger compiler makes this transfer question decidable for each fixed \(R\)\.

Second, even with exact local mean witnesses and relative entropy \(O_R(L)\), the current regularization argument still produces a numerical radius proportional to \(\epsilon^{-1}\)\. A genuinely new quantitative argument is needed to replace that dependence by a polynomial in \(\log(1/\epsilon)\)\.

**Final assessment\:** The full unrestricted inverse-height theorem is not resolved. The strongest new advances are an exact local Carathéodory theorem for fixed lattice fibres, a complete inverse compiler for arbitrary-rank modular population networks, an effective test for global midpoint balancing, and polynomial relative-entropy certificates near feasible target means.

No counterexample to the requested full fixed-network calibration contract has been established.
