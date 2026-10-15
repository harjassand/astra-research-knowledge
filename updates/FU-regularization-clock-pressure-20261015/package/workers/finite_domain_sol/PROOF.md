# Prescribing an arbitrary open convex exponential-moment domain

Status: independent internally reconstructed theorem candidate, 2026-10-15. This is a mathematical proof attempt with an explicit construction. Historical priority, external mathematical review, formal verification, efficiency, and practical advantage have not been established.

Source comparison: the raw PR94 proof at `origin/pr-94:updates/FT-foundational-capability-v2-20261015/package/workers/mathematical_invention/PROOF.md` was read after the present convex-conjugate route had been identified. It supplies the compact-distribution/cone setting and the all-exponential-moment theorem. No other current worker's result was read. This document replaces the radial slow-slope construction by a barrier/conjugate/mollification construction, and permits any prescribed open convex moment domain, including unbounded and nonsymmetric ones.

## 1. Statement

Let \(m\ge1\), let \(E\) be a real Banach space, and let \(C\subsetneq E\) be a closed convex cone with nonempty interior. Pointedness is not required. Let \(T\) be an \(E\)-valued distribution of compact support in \(\mathbb R^m\), with \(T(1)=e\in\operatorname{int}C\). Define
\[
H(g)=T_y(e^{g\cdot y}),\qquad g\in\mathbb R^m.
\]
Let \(\Omega\subseteq\mathbb R^m\) be open and convex, with \(0\in\Omega\). No boundedness or central symmetry is assumed.

For a scalar probability measure \(\nu\), its effective real exponential-moment domain means
\[
\mathcal D(\nu)=\left\{g:\int e^{g\cdot x}\,\nu(dx)<\infty\right\}.
\]
For a compact set \(K\subset\Omega\), write \(h_K(x)=\sup_{g\in K}g\cdot x\).

**Theorem.** The following are equivalent.

1. \(H(g)\in\operatorname{int}C\) for every \(g\in\Omega\).
2. There is a scalar probability measure \(\nu\) with \(\Omega\subseteq\mathcal D(\nu)\) such that \(T*\nu\) is a \(C\)-positive distribution.
3. There is a strictly positive \(C^\infty\), strictly log-concave probability density \(p\) such that
   \[
   \mathcal D(p(x)\,dx)=\Omega,
   \tag{1}
   \]
   \[
   \int e^{h_K(x)}|\partial^\alpha p(x)|\,dx<\infty
   \quad\text{for every compact }K\subset\Omega\text{ and every }\alpha,
   \tag{2}
   \]
   and \((T*p)(x)\in\operatorname{int}C\) for every \(x\).

More precisely, for any \(0<\sigma<1\), the density can be written \(p=Z^{-1}e^{-W}\), where \(W\) is smooth with positive-definite Hessian, \(\nabla W(x)\in\Omega\), and
\[
(1-\sigma)p(x)H(\nabla W(x))
\preceq_C (T*p)(x)
\preceq_C (1+\sigma)p(x)H(\nabla W(x)).
\tag{3}
\]
Every derivative of \(T*p\) has the weighted norm integrability in (2), and \(\int(T*p)(x)\,dx=e\).

The density may be chosen invariant under every orthogonal transformation preserving \(\Omega\), even when \(T\) does not have those symmetries. In particular, for \(\Omega=B_a\), \(a>0\), it can be chosen radial, and for \(\Omega=\mathbb R^m\) this construction recovers a radial all-exponential-moment regularizer.

The theorem asserts no effective access to a positivity margin, no useful bound on the noise variance or scale, and no historical novelty.

## 2. Necessity only uses moments at the requested tilts

Choose finite-order seminorm data \(R\ge1\), \(N\ge0\), and \(C_T<\infty\) such that
\[
\|T(f)\|\le C_T\max_{|\alpha|\le N}\sup_{|y|\le R}|\partial^\alpha f(y)|.
\tag{4}
\]
The usual fixed cutoff equal to one near the support is absorbed into this notation and into \(C_T\).

Suppose condition 2 holds and put \(S=T*\nu\). Choose radial cutoffs \(\chi_A\) equal to one on \(B_A\), zero off \(B_{2A}\), between zero and one, with nonincreasing radial profile. For each fixed \(g\in\Omega\), finite \(\nu\)-moment at that one tilt implies
\[
S(e^{g\cdot x}\chi_A(x))\longrightarrow
\left(\int e^{g\cdot z}\nu(dz)\right)H(g)
\quad\text{in }E.
\tag{5}
\]
To justify this, apply (4) to
\[
\int e^{g\cdot(y+z)}\chi_A(y+z)\nu(dz).
\]
The zero-cutoff-derivative error is controlled by the tail of the integrable function \(e^{g\cdot z}\). Terms with a derivative on the cutoff have an additional factor \(A^{-j}\), \(j\ge1\), and tend to zero uniformly in the compact \(y\)-set. Thus convergence holds in the required \(C^N\) seminorm.

At \(g=0\), choose a finite \(A_0\) for which \(Q=S(\chi_{A_0})\in\operatorname{int}C\), since these quantities converge to \(e\). For \(A\ge2A_0\),
\[
e^{g\cdot x}\chi_A(x)-e^{-2A_0|g|}\chi_{A_0}(x)\ge0.
\]
Positivity and (5) show that the limit in (5) belongs to
\(e^{-2A_0|g|}Q+C\subset\operatorname{int}C\).
The scalar moment is strictly positive and finite, hence \(H(g)\in\operatorname{int}C\). No moments outside \(\Omega\) are used.

Condition 3 immediately implies condition 2. It remains to construct condition 3 from condition 1.

## 3. A positive Lipschitz minorant of the arbitrary margin

For \(g\in\Omega\), put
\[
\mu(g)=\operatorname{dist}(H(g),E\setminus C)>0,
\qquad A(g)=e^{R|g|}(1+|g|)^N.
\]
The function \(\mu\) is continuous. Define a continuous function \(r\) on \(\mathbb R^m\) by zero off \(\Omega\) and, on \(\Omega\), by
\[
r(g)=\min\left\{1,\frac{\mu(g)}{A(g)},
\operatorname{dist}(g,\mathbb R^m\setminus\Omega)\right\}.
\tag{6}
\]
When \(\Omega=\mathbb R^m\), omit the last entry. Let
\[
\delta(g)=\inf_{h\in\mathbb R^m}\{r(h)+|g-h|\}.
\tag{7}
\]
Then \(\delta\) is globally 1-Lipschitz, vanishes off \(\Omega\), is strictly positive on \(\Omega\), and
\[
0<\delta(g)\le\min\left\{1,\frac{\mu(g)}{A(g)}\right\}
\quad(g\in\Omega).
\tag{8}
\]
Positivity follows by splitting the infimum into a small neighborhood of a fixed interior \(g\), where continuity gives a positive lower bound for \(r\), and its complement, where the distance term has a positive lower bound. This construction imposes no quantitative lower bound on \(\mu\).

## 4. An explicit smooth convex exhaustion of every open convex domain

Define the polar
\[
P=\{u\in\mathbb R^m:u\cdot g\le1\text{ for every }g\in\Omega\}.
\tag{9}
\]
Since \(\Omega\) contains a ball about zero, \(P\) is compact. Let \(L=\operatorname{span}P\), \(k=\dim L\), and use relative Lebesgue measure \(\lambda_L\) on \(L\). If \(k=0\), use unit point mass at zero.

Separation of a point from the open convex set gives
\[
\Omega=\{g:h_P(g)<1\}.
\tag{10}
\]
Indeed, every interior point has strict inequality uniformly over compact \(P\); a separating functional for a point outside \(\Omega\) can be normalized to lie in \(P\), since its supremum on \(\Omega\) is strictly positive when \(\Omega\) contains a ball about zero.

On \(\Omega\), set
\[
\zeta(g)=|g|^2+
\int_P(1-u\cdot g)^{-(k+1)}\,d\lambda_L(u).
\tag{11}
\]
This is smooth and convex, and \(D^2\zeta\succeq2I\). Its sublevel sets are compact subsets of \(\Omega\).

Here is the boundary estimate. Suppose bounded \(g_n\in\Omega\) tend to the boundary, and let \(d_n=1-h_P(g_n)\to0\). Choose a maximizer \(u_n\in P\). For large \(n\), the set
\[
P_n=(1-d_n)u_n+d_nP
\]
lies in \(P\) and has relative volume \(d_n^k\lambda_L(P)\). On it,
\[
1-u\cdot g_n\le C d_n
\]
with a finite constant independent of \(n\), since \(P\) and \(g_n\) are bounded. The integral in (11) is therefore at least a positive constant times \(d_n^{-1}\), and diverges. The quadratic term controls escape to infinity. For \(k=0\), \(P=\{0\}\), \(\Omega=\mathbb R^m\), and \(\zeta=|g|^2+1\), so no boundary argument is needed.

This explicit exhaustion avoids assuming a smooth boundary, strict convexity, boundedness, or a preexisting barrier for \(\Omega\).

## 5. A barrier with any prescribed Hessian lower bound

Fix a small parameter \(\kappa>0\), whose upper bounds will be chosen later. There exists a smooth increasing convex function \(F:[0,\infty)\to[0,\infty)\), with \(F(0)=0\) and \(F'\ge1\), such that
\[
F'(\zeta(g))\ge\frac1{\kappa\delta(g)}.
\tag{12}
\]
For an explicit envelope, fix a smooth nondecreasing step \(\theta\) equal to zero on \(( -\infty,0]\) and one on \([1,\infty)\). Put
\[
a_n=1+\sup_{\zeta(g)\le n+2}\frac1{\kappa\delta(g)},\quad n\ge0,
\qquad
F'(t)=1+\sum_{n\ge0}a_n\theta(t-n+1),
\tag{13}
\]
where an empty supremum is zero, and integrate from zero. The sublevel sets from Section 4 make each \(a_n\) finite, and the sum is locally finite. The term \(n=\lfloor t\rfloor\) verifies (12).

Let \(b=F\circ\zeta\) on \(\Omega\), extended by \(+\infty\) elsewhere. Then \(b\) is smooth on \(\Omega\), tends to infinity at its finite boundary, and \(b(g)\ge|g|^2\). Its Hessian satisfies
\[
D^2b(g)\succeq\frac1{\kappa\delta(g)}I.
\tag{14}
\]
For each \(x\), the function \(g\mapsto b(g)-x\cdot g\) has a unique minimizer in \(\Omega\): coercivity controls infinity, boundary divergence controls the boundary, and the Hessian is positive definite. Its critical-point equation is \(\nabla b(g)=x\).

Consequently the convex conjugate
\[
V(x)=b^*(x)=\sup_{g\in\Omega}\{x\cdot g-b(g)\}
\tag{15}
\]
is finite and smooth everywhere. The inverse-function theorem gives
\[
G(x):=\nabla V(x)\in\Omega,\qquad
0\prec D^2V(x)=(D^2b(G(x)))^{-1}
\preceq\kappa\delta(G(x))I.
\tag{16}
\]
This is the adjustable local flatness needed for the cone argument.

## 6. Fixed mollification controls every higher jet

Choose once and for all a nonnegative radial \(\eta\in C_c^\infty(B_1)\) with integral one, and put
\[
W=\eta*V,\qquad g_x=\nabla W(x).
\tag{17}
\]
The Hessian of \(W\) is positive definite, as the average of positive-definite Hessians. Also \(g_x\in\Omega\): it is an average of a compact subset of \(\Omega\), whose convex hull is still a compact subset of the open convex set.

Because \(\delta\) is 1-Lipschitz, (16) and the elementary integral form of Gronwall's inequality imply, for any \(w,x\),
\[
\delta(G(w))\le e^{\kappa|w-x|}\delta(G(x)),
\]
\[
|G(w)-G(x)|\le(e^{\kappa|w-x|}-1)\delta(G(x)).
\tag{18}
\]
Assume
\[
\kappa\le\min\{\log(3/2),\ 1/(R+1)\}.
\tag{19}
\]
Using the second estimate over the mollifier support gives
\[
|g_x-G(x)|\le(e^\kappa-1)\delta(G(x)),\qquad
\delta(g_x)\ge\tfrac12\delta(G(x)).
\tag{20}
\]
For \(|y|\le R\) and \(|z|\le1\), (16), (18), and (20) yield
\[
\|D^2V(x-y-z)\|\le2e\kappa\delta(g_x).
\tag{21}
\]
For every \(j\ge2\), differentiating the compact mollifier \(j-2\) times gives a fixed finite constant \(c_j\) such that
\[
\sup_{|y|\le R}\|D^jW(x-y)\|
\le c_j\kappa\delta(g_x).
\tag{22}
\]
The constants depend on \(m,j,\eta\), not on \(x\), \(b\), or the margin function. Globally, the same formula and \(\delta\le1\) also give finite uniform bounds for every derivative of \(W\) of order at least two.

This step is material for arbitrary compact distributions. A Hessian estimate alone would only suffice for a finite vector measure; mollification upgrades it to all jets needed in the finite-order seminorm (4).

## 7. The distributional remainder and the cone estimate

For \(|y|\le R\), let
\[
Q_x(y)=W(x-y)-W(x)+g_x\cdot y.
\tag{23}
\]
Taylor's integral remainder handles derivative orders zero and one; (22) handles higher orders. Thus, for a finite constant \(B\) depending only on the fixed seminorm data and \(\eta\),
\[
\|Q_x\|_{C^N(B_R)}\le B\kappa\delta(g_x).
\tag{24}
\]
Choose additionally \(B\kappa\le1\). Product and chain rules on this bounded \(C^N\) ball give another fixed finite constant \(B'\) such that
\[
\|e^{-Q_x}-1\|_{C^N(B_R)}\le B'\kappa\delta(g_x).
\tag{25}
\]
With \(p=Z^{-1}e^{-W}\), the identity
\[
p(x-y)=p(x)e^{g_x\cdot y}e^{-Q_x(y)}
\]
is exact. It follows that
\[
\frac{(T*p)(x)}{p(x)}=H(g_x)+E_x,
\qquad
E_x=T_y\big(e^{g_x\cdot y}(e^{-Q_x(y)}-1)\big).
\tag{26}
\]
Equations (4), (25), and the derivative bounds for a linear exponential yield
\[
\|E_x\|\le B''\kappa A(g_x)\delta(g_x)
\le B''\kappa\mu(g_x).
\tag{27}
\]
All constants in \(B''\) are independent of \(\kappa\). Finally choose \(B''\kappa\le\sigma\), retaining the previous finite upper bounds on \(\kappa\).

If \(h\in\operatorname{int}C\) and \(\|v\|\le\sigma\operatorname{dist}(h,E\setminus C)\), cone homogeneity and closedness give
\(-\sigma h\preceq_C v\preceq_C\sigma h\). Apply this with \(h=H(g_x)\) and \(v=E_x\). This proves (3), including pointwise interior positivity.

## 8. Exact moment domain, including divergence at every boundary point

For each compact \(K\subset\Omega\), choose \(a_K>0\) such that \(K+a_K\overline B_1\) is a compact subset of \(\Omega\). The barrier is bounded above there. Since the mollifier has mean zero, (15) gives, for every \(h\in\Omega\),
\[
W(x)\ge h\cdot x-b(h).
\]
Taking \(h\) in \(K+a_K\overline B_1\) yields
\[
W(x)\ge h_K(x)+a_K|x|-B_K
\tag{28}
\]
with finite \(B_K\). In particular, \(0<Z=\int e^{-W}<\infty\), and all moments at interior tilts are finite.

Conversely fix \(g\notin\Omega\). Separation from the open convex set provides a unit vector \(u\) and a finite \(c\) with
\[
u\cdot h\le c\le u\cdot g\qquad(h\in\Omega).
\tag{29}
\]
For every \(t\ge0\) and \(z\in\mathbb R^m\), the conjugate formula gives
\[
V(tu+z)\le tc+V(z).
\]
Fixed mollification preserves this inequality:
\[
W(tu+z)\le tc+W(z).
\tag{30}
\]
Hence on the infinite cylinder \(t\ge0\), \(z\in u^\perp\cap B_1\),
\[
e^{g\cdot(tu+z)-W(tu+z)}
\ge e^{t(u\cdot g-c)}e^{g\cdot z-W(z)}
\ge e^{g\cdot z-W(z)}.
\tag{31}
\]
The last factor has a positive lower bound on the compact transverse ball. The cylinder has infinite volume, so the moment diverges. The same argument works when equality holds in (29), which is precisely the boundary case. In dimension one the transverse ball is a point and the cylinder is a half-line.

This establishes the exact open domain (1). It also covers unbounded \(\Omega\); no finiteness of its support function in arbitrary directions was assumed.

Finally, the global bounds on \(D^jW\), \(j\ge2\), imply \(|\nabla W(x)|\le C+\kappa|x|\). Repeated differentiation of \(e^{-W}\) therefore gives
\[
|\partial^\alpha p(x)|\le C_\alpha p(x)(1+|x|)^{|\alpha|}.
\tag{32}
\]
Combining (28) and (32) proves (2). The finite-order local supremum estimate for compact distributions then proves the same weighted norm integrability for all derivatives of \(T*p\), justifies interchange of \(T\) and integration, and gives \(\int T*p=T(1)\).

## 9. Symmetry and the ball case

If an orthogonal transformation \(U\) preserves \(\Omega\), it preserves \(P\), its relative measure, and \(\zeta\). Although the margin function need not be symmetric, \(b=F(\zeta)\) is symmetric: its scalar envelope uses the worst prescribed curvature on complete \(\zeta\)-sublevel sets. The conjugate and radial mollification preserve this symmetry.

For \(\Omega=B_a\), the polar is \(\overline B_{1/a}\), so \(\zeta,b,V,W,p\) are radial. Equations (1) and (2) specialize to
\[
\mathcal D(p)=B_a,\qquad
\int e^{b|x|}|\partial^\alpha p(x)|\,dx<\infty
\quad\text{for all }0\le b<a.
\]
Boundary divergence does not require an asymptotic expansion: (30) gives it directly. Thus the requested finite-radius theorem follows without a quantitative lower bound on the cone margin near \(|g|=a\).

## 10. Explicit example outside the all-moment theorem

Let \(\lambda>0\), and in \(\mathbb R^m\) take
\[
T=\delta-\lambda^{-2}\partial_1^2\delta,
\qquad H(g)=1-\lambda^{-2}g_1^2,
\qquad
\Omega=(-\lambda,\lambda)\times\mathbb R^{m-1}.
\]
The transform is strictly positive on the unbounded anisotropic slab, vanishes on its boundary, and is negative beyond it. Put
\[
p(x)=Z^{-1}\operatorname{sech}(\lambda x_1)
\exp\left(-\frac12\sum_{j=2}^m x_j^2\right).
\]
It is smooth, strictly positive, and strictly log-concave, with exact moment domain \(\Omega\). Since
\[
\frac{d^2}{dt^2}\operatorname{sech}(\lambda t)
=\lambda^2\operatorname{sech}(\lambda t)
\left(1-2\operatorname{sech}^2(\lambda t)\right),
\]
one has the explicit strictly positive regularization
\[
(T*p)(x)=2p(x)\operatorname{sech}^2(\lambda x_1)>0.
\tag{33}
\]
There is no all-exponential-moment positive regularizer for this \(T\), by the necessity argument at a tilt with \(|g_1|>\lambda\). Thus finite-domain regularization genuinely admits inputs excluded by the PR94 global condition.

For a nonsymmetric interval \((\beta-\lambda,\beta+\lambda)\) containing zero, take
\[
H(s)=\frac{\lambda^2-(s-\beta)^2}{\lambda^2-\beta^2},
\qquad
p(t)=Z^{-1}e^{-\beta t}\operatorname{sech}(\lambda t),
\quad |\beta|<\lambda.
\]
Then \(H(0)=1\), the exact moment domain is that interval, and
\[
H(-\partial)p
=\frac{2\lambda^2}{\lambda^2-\beta^2}\,
p(t)\operatorname{sech}^2(\lambda t)>0.
\tag{34}
\]
Multiplication by independent Gaussian factors gives the corresponding nonsymmetric slab in higher dimensions.

## 11. Precise extensions and obstructions

* **Singular finite matrix mass.** For \(\operatorname{Herm}_d\)-valued compact distributions without interior normalization, the localized analogue is: a scalar noise with finite moments on \(\Omega\) regularizes positively if and only if \(H(g)\succeq0\) on \(\Omega\) and \(\ker H(g)\) is constant there. Necessity follows by integrating the positive output and its exponential tilts. Sufficiency compresses to the common kernel's orthogonal complement and applies the theorem. Components annihilating that complement vanish as distributions because their entire Laplace transforms vanish on the nonempty open set \(\Omega\). This is a localized consequence, not an additional independent novelty claim.
* **A nonball cannot retain radial noise.** A radial probability density has an orthogonally invariant convex moment domain. If that domain is open and contains zero, it is a centered ball or all of \(\mathbb R^m\). General anisotropic domains therefore require dropping radiality, while strict log-concavity is retained.
* **Strict is not uniform log-concavity.** A globally positive lower bound on \(D^2W\) would force all exponential moments. It is incompatible with a proper prescribed \(\Omega\). The theorem supplies \(D^2W(x)\succ0\) pointwise, with no uniform positive lower bound.
* **Convexity and the origin are necessary for an exact open domain.** Every probability moment domain is convex by Hölder's inequality and contains zero. The domain in this theorem is prescribed to be open; moment domains with selected finite boundary points are a separate problem.
* **No Gaussian width can replace the construction in general.** Every Gaussian has all real exponential moments. Example (33) has negative transform outside its slab, so it admits no Gaussian positive regularizer at any width.
* **No effective scale follows.** The barrier envelope in (13) uses lower cone margins on compact sublevel sets, and those margins may be arbitrarily small. The theorem gives existence, not a computable or efficient noise prescription from unspecified input access.

## 12. Audit notes and unresolved status

The proof is self-contained apart from standard finite-dimensional separation, the inverse-function theorem, elementary compact-distribution estimates, and basic differentiation/integration results. The polar integral in (11), the prescribed-Hessian envelope, the mollification jet estimates, and the boundary cylinder argument are supplied explicitly. No numerical check is used as a proof premise.

The strongest result here is the arbitrary open convex exact-domain characterization, including unbounded nonsymmetric domains and arbitrary compact finite-order Banach-cone distributions. This is broader than simply changing the endpoint of the PR94 slow-slope sequence. It has not been compared exhaustively with the historical positive-convolution or convex-analysis literature, so neither priority nor exceptional significance is asserted.
