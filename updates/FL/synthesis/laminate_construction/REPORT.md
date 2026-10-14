# Finite laminates for modulation laws

## Finding

For every bounded-gradient periodic or zero-boundary modulation covered by the incoming global theorem, the Jensen conclusion for **all continuous rank-one-convex tests** is valid. Convolution of a continuous test preserves rank-one convexity, and the smoothed tests converge uniformly on the compact gradient range. Thus the gradient law is a laminate in the usual Jensen-measure sense.

There is also a classical existence theorem that upgrades this to weak-* approximation by finite-order laminates. It is not an explicit construction: its approximants are confined only to an open neighborhood of the full rank-one-convex hull of the support, and the theorem supplies neither a splitting tree nor an error rate. In particular, the source's Jensen proof alone does not give a uniform gradient cap for such trees.

An explicit, reusable construction does work for the **phase-only subclass** $\phi(x)=\gamma(k\cdot x)$, including $\gamma(s)=R(s)V(s)$. Every gradient then lies in one affine subspace whose pairwise differences have rank at most one. Conditional averages on $N$ phase intervals give an exact-barycenter finite-order laminate with a uniform gradient bound and a $W_1$ error of order $N^{-1}$. The full theorem allows $r$ to depend on transverse coordinates; this construction does not cover that case.

## Jensen laminate statement under the exact incoming hypotheses

Let $\mathbb T^n=(\mathbb R/2\pi\mathbb Z)^n$ have normalized Lebesgue measure. Let $V\in C^2(\mathbb R;\mathbb R^m)$ be periodic with

\[
V''(s)=-a(s)V(s),\qquad a(s)\ge 0,
\]

let $k\in\mathbb Z^n$, and let $r\in C^\infty(\mathbb T^n;\mathbb R)$. Set

\[
\phi(x)=r(x)V(k\cdot x),\qquad
\mu=(B+D\phi)_\# dx.
\]

Then $\bar\mu=B$, since $\int_{\mathbb T^n}D\phi=0$, and

\[
\operatorname{supp}\mu\subset \overline B(B,M),\qquad
M=\|r\|_\infty\|V'\|_\infty|k|+\|V\|_\infty\|Dr\|_\infty.
\]

For a bounded Lipschitz domain and smooth $r\in W^{1,\infty}_0$, use normalized volume and the same law; the boundary integral gives $\int D\phi=0$. The incoming flux identity applies in both cases. If $F:\mathbb R^{m\times n}\to\mathbb R$ is continuous and rank-one convex, take a compactly supported smooth mollifier $\rho_\epsilon$ and set $F_\epsilon=F*\rho_\epsilon$. Each $F_\epsilon$ is smooth and rank-one convex, so the incoming theorem gives

\[
\int F_\epsilon\,d\mu\ge F_\epsilon(B).
\]

On the compact set $\operatorname{supp}\mu\cup\{B\}$, $F_\epsilon\to F$ uniformly. Letting $\epsilon\downarrow0$ proves

\[
F(B)\le\int F(A)\,d\mu(A)
\quad\text{for every continuous rank-one-convex }F.
\]

This argument uses the bounded-gradient condition exactly where needed: it keeps the law supported on a compact set, so no growth condition on $F$ is needed. The claim is a Jensen inequality for this specific law, not a claim that every gradient law has this property.

## What finite-order approximation follows abstractly

Müller–Šverák, *Convex integration with constraints and applications to phase transitions and partial differential equations*, JEMS 1 (1999), Theorem 3.1, state that if $K\subset\mathbb R^{m\times n}$ is compact and $\nu$ is a laminate supported in $K$, then for every open set $O\supset K^{rc}$ there is a sequence of finite-order laminates $\nu_j\in L(O)$ converging weak-* to $\nu$. Here $K^{rc}$ is the functional rank-one-convex hull. Their proof uses separation and Hahn–Banach; it is an existence proof, not an algorithm with a prescribed tree or rate.

The topology is weak-* convergence against continuous tests. If one separately proves $K^{rc}\subset B_R$, one can choose a bounded $O\subset B_{R+\epsilon}$ and obtain a uniform support bound $R+\epsilon$ for the finite laminates. The cited theorem does not prove that $K^{rc}$ is bounded for a given modulation support, does not quantify the required order as a function of an error tolerance, and does not give a $W_1$ rate. Its finite-order microstructure lemma realizes a specified finite tree by piecewise-linear gradients up to a small exceptional fraction, but likewise gives no explicit mesh or frequency cost.

This distinction matters: the finite-order splitting hull can be strictly smaller than the functional rank-one-convex hull at the level of sets. Müller–Šverák give a four-well $2\times2$ example with no rank-one connections while its functional rank-one-convex hull contains a square. Their measure-approximation theorem bridges the two only by allowing intermediate leaves near the full functional hull. This is why the theorem is useful as an existence result but does not by itself supply a bounded, explicit tree for the present arbitrary-amplitude laws.

## Explicit operation when the amplitude is phase-only

Take any $2\pi$-periodic $C^2$ curve $\gamma:\mathbb R\to\mathbb R^m$, any nonzero $k\in\mathbb Z^n$, and $\phi(x)=\gamma(k\cdot x)$. The curve may be $\gamma(s)=R(s)V(s)$, but no curvature condition on $V$ is needed for this construction. Let

\[
g(s)=\gamma'(s),\qquad
M_1=\|\gamma'\|_\infty,\qquad M_2=\|\gamma''\|_\infty.
\]

Then $D\phi(x)=g(k\cdot x)\otimes k$, and $k\cdot x\pmod{2\pi}$ is uniform on the circle under normalized torus measure. Partition the phase circle into $N$ equal intervals $I_j$ of width $h=2\pi/N$, and define

\[
\bar g_j=\frac1h\int_{I_j}g(s)\,ds,\qquad
\mu_N=\frac1N\sum_{j=1}^N\delta_{B+\bar g_j\otimes k}.
\]

Because $\int_0^{2\pi}g=\gamma(2\pi)-\gamma(0)=0$, the finite law has **exact barycenter $B$**. For any two leaves,

\[
(\bar g_i-\bar g_j)\otimes k
\]

has rank at most one. A balanced binary tree on the $N$ leaves is therefore a valid finite splitting tree: at each node split the mean of its index set into the means of its two children, with weights equal to their relative cardinalities. The root is $B$; there are $N-1$ split nodes and, when groups are bisected, maximum depth $\lceil\log_2N\rceil$. Every intermediate matrix is a convex combination of leaves, so

\[
|A-B|\le |k|M_1
\]

throughout the entire tree.

The same leaves are realized exactly by a piecewise-linear compatible field. Let $g_N(s)=\bar g_j$ on $I_j$, and set

\[
\gamma_N(s)=\gamma(0)+\int_0^s g_N(t)\,dt.
\]

The exact zero mean of $g_N$ makes $\gamma_N$ periodic. The gradient of $x\mapsto\gamma_N(k\cdot x)$ takes precisely the values $\bar g_j\otimes k$, each on a phase slab of measure $1/N$. Thus its gradient law is exactly $\mu_N$, and its interfaces are compatible because every jump has the same right factor $k$.

For $s\in I_j$, conditional averaging and the Lipschitz bound on $g$ give

\[
|g(s)-\bar g_j|
\le \frac1h\int_{I_j}|g(s)-g(t)|\,dt
\le M_2\frac1h\int_{I_j}|s-t|\,dt
\le M_2\frac h2.
\]

Coupling $s$ to its interval mean yields the quantitative estimate

\[
W_1(\mu,\mu_N)\le |k|M_2\frac{\pi}{N}.
\]

Equivalently, for every $L$-Lipschitz test $\Psi$,

\[
\left|\int\Psi\,d\mu-\int\Psi\,d\mu_N\right|
\le L|k|M_2\frac{\pi}{N}.
\]

For any continuous test on the common compact support, replace $L\delta$ by its modulus of continuity $\omega_\Psi(\delta)$. The construction takes $O(N)$ interval-integral evaluations and $N-1$ rank-one split operations; its exact arithmetic cost depends on the representation of $\gamma$. In the trigonometric example below, all interval integrals are closed form. This is a genuine quantitative bounded-gradient construction, but only for a single phase variable.

Each $\mu_N$ satisfies Jensen for every rank-one-convex test by the finite splitting tree. Since $W_1(\mu,\mu_N)\to0$ and all laws share a compact support, expectations of every continuous test converge. Hence the phase-only law itself is a laminate, with an explicit bounded finite-order approximating sequence.

### Exact example

Let $n=m=2$, $k=e_1$, $V(s)=(\cos s,\sin s)$, $R(s)=1+\tfrac12\cos s$, and $\gamma=RV$. Then

\[
g(s)=\gamma'(s)=
\begin{pmatrix}
-\sin s-\tfrac12\sin 2s\\
\cos s+\tfrac12\cos 2s
\end{pmatrix},
\qquad
\|g\|_\infty\le\tfrac32,
\qquad
\|g'\|_\infty\le2.
\]

For $N=8$, the eight exact atoms from conditional interval means have barycenter zero, support norm at most $3/2$, seven rank-one split nodes, tree depth three, and

\[
W_1(\mu,\mu_8)\le\frac\pi4.
\]

The exact atoms and the tree checks are recorded in `checker_results.json`. The atom norms there are also printed numerically as a finite fixture; the $3/2$, $2$, and $\pi/4$ bounds follow from the analytic estimates above.

## Why the general all-coordinate profile is not already a split tree

For the full theorem,

\[
D\phi=P+Q,\qquad P=rV'(k\cdot x)\otimes k,\qquad Q=V(k\cdot x)\otimes Dr.
\]

Both summands are pointwise rank one, but they need not be rank-one connected to one another. In the incoming full-rank example, take $k=e_2$, $V(y)=(\cos y,\sin y)$, $r(x,y)=1+\tfrac12\cos x$. Writing $r_x=\partial_xr$,

\[
\det(P-Q)=-r r_x.
\]

At $x=\pi/2$, this determinant is $1/2$, so $P-Q$ has rank two. Therefore $P,Q$ cannot be the two children of a rank-one split. This is a precise failure of the obvious pointwise splitting route; it does **not** rule out a more elaborate tree. The flux identity proves the Jensen property for this example, and the Müller–Šverák density theorem gives abstract finite-order approximants, but an explicit bounded tree and a rate for this transverse-amplitude law remain unresolved here.

The same calculation marks why the phase-only construction stops at a strict subfamily. If $r=R(k\cdot x)$, then $Dr=R'(k\cdot x)k$ and both $P,Q$ have the common input direction $k$. If $r$ depends on transverse coordinates, $Dr$ generally points elsewhere and the two rank-one summands are not compatible as a binary split.

## Prior art and exact scope boundaries

Astala, Iwaniec, Prause and Saksman, arXiv:1403.1095v1, Proposition 5.1, prove a Jensen bound for the radial family $f(x)=\Lambda(|x|)x$ and every continuous rank-one-concave integrand. Their proof mollifies the integrand, applies the rank-one supporting inequality to the rank-one radial derivative term in $Df=\Lambda(|x|)+\Lambda'(|x|)x\otimes x/|x|$, integrates over spheres, and compares against the linear boundary extension $\Lambda(R)x$. Applying the inequality to $E=-F$ gives the rank-one-convex Jensen form. This is a strong direct calibration for a radial family, but it supplies no finite splitting tree or quantitative approximation rate. Its radial matrix profile and the incoming arbitrary scalar-amplitude/affine-phase family are distinct classes; no priority or novelty conclusion follows from this comparison.

The incoming theorem is more general in the amplitude: $r$ may depend on every coordinate, with no smallness or frequency-separation requirement. Its carrier phase is fixed and affine, and its loop satisfies $V''=-aV$, $a\ge0$. It proves an exact flux identity for every $C^2$ rank-one-convex integrand, then uses convolution to cover all continuous rank-one-convex tests when gradients are bounded. It does not assert that arbitrary compatible gradients are laminates.

If every zero-boundary gradient law had this Jensen property for every rank-one-convex $F$, the defining quasiconvex inequality would hold for every such $F$; this would settle the full rank-one-convex-to-quasiconvex implication. The global packet expressly leaves the planar $2\times2$ question unresolved. The pinned capital record N803 likewise leaves universal compatible-law Jensen open for the full nine-coefficient left-$SO(2)$-invariant quartic class. The present result gives a special profile class and does not close that gate.

## Read status and reproducibility

`READ_LEDGER.md` records the exact pinned inputs, frozen global packet, capital context, and primary-source passages read. `check_phase_only.py` rechecks every byte count and SHA-256 in the frozen global manifest, verifies the phase-only formulas and $N=8$ split tree symbolically, checks the transverse determinant obstruction, and writes `checker_results.json`. Forty-six checks passed. These checks establish the stated finite algebra and input integrity; they do not replace the analytic bounds above, prove a general bounded-tree result, or establish novelty.

The effective cost of the phase-only procedure is $N$ exact interval means plus $N-1$ tree splits, $O(N)$ symbolic/numeric work for a closed-form carrier. For an arbitrary smooth input curve, exact integration and bit complexity are not specified. The nonconstructive density theorem has no reported numerical or asymptotic work bound. No laboratory, physical-acquisition, financial, or aggregate inference cost is involved in this mathematical operation.
