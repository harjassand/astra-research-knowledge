# Independent primary-proof audit: arXiv:2609.28311v1

**Outcome:** the actual scalar-potential projection argument has been reconstructed without a gap found in this audit. The reconstruction below covers the stated two-dimensional periodic quasiconvexity result and supplies the omitted integral-transform and norm steps. No counterexample to the paper's actual Lemma 4, Theorem 1, or Corollary 2 was found. Explicit counterexamples below instead reject three tempting substitutions: a linear Hodge projection, pointwise gradient clipping, and pointwise energy positivity.

**Admission boundary:** this is a worker proof audit, with ordinary mathematical reasoning and reproducible symbolic checks. It is not independent community acceptance, a formal proof, or authorization to import the sharp constant into Astra. Its machine-readable status is AUDIT_RECONSTRUCTED_NOT_ADMITTED; premise_admission is false. The source report global_compatible_positivity needs only its established complex nonsharp Beurling bound \(\sqrt{24}\), which this worker has neither edited nor replaced.

## 1. Exact source and provenance

The audited item is [Agazzi et al., Sharp Higher Integrability Theory, Part I: The \(L^p\)-norm of the Beurling–Ahlfors transform, arXiv:2609.28311v1](https://arxiv.org/abs/2609.28311v1), submitted 23 September 2026 at 15:55:17 UTC. The exact-version [PDF](https://arxiv.org/pdf/2609.28311v1), [TeX archive](https://arxiv.org/src/2609.28311v1), [HTML](https://arxiv.org/html/2609.28311v1), and abstract page were acquired directly from arxiv.org. Acquisition times, response headers, redirected URLs, byte counts, and SHA256 digests are in acquisition_receipts.json.

| Item | SHA256 |
|---|---|
| PDF, seven pages | 74b462471cddb5f4a2d51de4117b9ba926ac72af05b351dcb0a73731887468ce |
| TeX source archive | 86ad8aeff1bb27f46d688c5341f5c9a2b8657a54d806932c0c91e65d1e619150 |
| Extracted main.tex | 1678c7eda2618bf8f148ab6a1d9bbd51043cd39663314dd1e01706ea448bb0ad |
| HTML | 961ebfc5b63a92503dcf21558a9c974c61783bb356453dc432d3377b2b334e20 |

The PDF was visually inspected on pages 1, 3, and 4, covering the disclosure, theorem, and entire projection proof. The TeX locations are:

- Lines 276–291: definition of \(L\) and Theorem 1.
- Lines 295–324: \(B_p\), transform convention, and Corollary 2.
- Lines 341–382: row representation, Lemma 3.
- Lines 385–405: proof of Theorem 1.
- Lines 409–453: scalar-potential projection, Lemma 4.
- Lines 246–250 and PDF page 1: AI-disclosure attribution.

The PDF and TeX attribute the key ideas to a system called ChatGPT 6.0 Astra. The downloaded HTML conversion omits that disclosure. The attribution is a statement by the source's authors; this audit does not independently establish the system's identity, capabilities, causal role, or relationship to the present Astra workspace. The preliminary-version notice appears in the source and PDF.

No other current worker report was read. No W/source/GitHub files were edited. The supplied W pin was checked read-only and matched ab5118e70a7e6a0dd39e75dd563d3a3f50b06b25.

## 2. Exact objects and quantifiers

Write a real-linear map of the plane as
\[
A z=a_+z+a_-\bar z,\qquad x=|a_+|,\quad y=|a_-|,\quad s=x+y.
\]
The norm used in the paper is the **operator norm**, \(s\), rather than the Frobenius norm. Also \(\det A=x^2-y^2\). Define
\[
L(A)=
\begin{cases}
\det A,&s\leq1,\\
2x-1,&s>1.
\end{cases}
\]
Theorem 1 asserts, for the unit torus \(Q=\mathbb R^2/\mathbb Z^2\),
\[
\forall A\in\mathbb R^{2\times2}\quad
\forall\varphi\in C^\infty_{\rm per}(Q;\mathbb R^2):
\quad
\int_Q L(A+D\varphi)\,dx\geq L(A).
\]
Thus the background is arbitrary and the perturbation is an arbitrary vector-valued gradient. The theorem does not assume \(A+D\varphi\) stays in a cone, that its determinant is positive, or that \(\varphi\) is the gradient of a scalar. The latter restriction is described as a prior result, not used as a substitute here.

For Lemma 4, use \(b\) for the fixed vector called \(p\) in the paper, avoiding confusion with the integrability exponent. Its data are:
\[
K\subset\mathbb R^2\ \hbox{nonempty, compact, convex},\quad
b\in K,\quad
\eta\in W^{1,\infty}_{\rm per}(Q;\mathbb R).
\]
The metric projection is in **\(L^2(Q)\) of scalar potentials**:
\[
\zeta=\mathop{\rm argmin}_{\xi\in\mathcal C}\|\eta-\xi\|_{L^2}^2,\qquad
\mathcal C=\{\xi\in W^{1,\infty}_{\rm per}(Q):b+D\xi\in K\ {\rm a.e.}\}.
\]
Put \(u=b\cdot x+\eta\), \(w=b\cdot x+\zeta\), \(h=\eta-\zeta\).
The claimed conclusions are
\[
Dw=Du\ \hbox{or}\ Dw\in\partial K\quad{\rm a.e.},
\qquad
\int_Q Dw\cdot(Du-Dw)\,dx\geq0. \tag{P}
\]
The alternatives need not be disjoint. The boundary is the ambient boundary; if \(K\) has empty interior, \(K=\partial K\).

## 3. Reconstruction of the nonlinear projection lemma

### 3.1 Existence and the variational inequality

Nonemptiness follows from \(0\in\mathcal C\), because \(b\in K\). Convexity follows by taking convex combinations of the gradients and using convexity of \(K\).

For closedness in \(L^2\), suppose \(\xi_n\in\mathcal C\) and \(\xi_n\to\xi\) in \(L^2\). Compactness of \(K\) gives a common bound
\[
|D\xi_n|\leq M:=\max_{k\in K}|k-b|.
\]
Their means are bounded by the \(L^2\) bound. A common Lipschitz bound and bounded means give a common uniform bound on the compact torus. Arzelà–Ascoli yields a uniformly convergent subsequence, whose limit agrees with the \(L^2\) limit. Its gradient remains in \(K-b\): this follows either from weak-star convergence of the gradients and weak-star closedness of a pointwise closed convex constraint, or from all support half-space inequalities. Hence \(\xi\in\mathcal C\).

The Hilbert-space projection theorem now gives a unique \(\zeta\) and
\[
\int_Q h(\xi-\zeta)\,dx\leq0\qquad(\xi\in\mathcal C). \tag{VI}
\]
This is a one-sided variational inequality. There is no assertion that \(h\) is orthogonal to \(\mathcal C\). Constant shifts are admissible, so \(\int_Qh=0\).

### 3.2 Saturation where the potentials differ

Lipschitz representatives make \(h\) continuous. On the zero set of a Lipschitz function, its weak gradient is zero almost everywhere; therefore \(Dw=Du\) almost everywhere on \(\{h=0\}\).

Suppose \(K\) has nonempty interior and choose a differentiability point \(x_0\) of \(w\), with \(h(x_0)>0\) and \(b_0=Dw(x_0)\in\operatorname{int}K\). Choose \(\rho>0\) with \(B_\rho(b_0)\subset K\). The support function
\[
H(v)=\max_{k\in K} k\cdot v
\]
is Lipschitz, has \(DH\in K\) almost everywhere, and obeys
\[
H(v)\geq b_0\cdot v+\rho|v|.
\]
Choose a small torus chart \(B_r(x_0)\) where \(h>0\), and use differentiability to obtain
\[
|w(x_0+v)-w(x_0)-b_0\cdot v|\leq(\rho/2)|v|
\quad(|v|\leq r).
\]
For \(0<\varepsilon<\rho r/2\), set
\[
c(x)=w(x_0)+\varepsilon-H(x_0-x).
\]
Its gradient is \(DH(x_0-x)\in K\), with the plus sign resulting from differentiating both minus signs. On the boundary of the ball,
\[
c(x)-w(x)\leq\varepsilon-\rho r/2<0,
\]
while \(c(x_0)>w(x_0)\). Thus \(v=(c-w)_+\) is a nonzero nonnegative Lipschitz function compactly supported in the ball.

Scalar maximum closure is essential: replacing \(w\) by \(\max\{w,c\}\) selects the gradient of one branch almost everywhere. Both branches have gradients in \(K\), so \(\zeta+v\in\mathcal C\). But (VI) would give \(\int_Qhv\leq0\), contradicting \(h>0\) on the support and \(v>0\) on an open set.

For \(h(x_0)<0\), no symmetry assumption on \(K\) is needed. Use explicitly
\[
c_-(x)=w(x_0)-\varepsilon+H(x-x_0),
\]
which lies above \(w\) on the ball's boundary and below it at \(x_0\). Replace \(w\) by \(\min\{w,c_-\}\); the perturbation is negative and (VI) again contradicts its pairing with negative \(h\). This expands the source's brief sign-change remark.

Rademacher differentiability then implies \(Dw\in\partial K\) almost everywhere on \(\{h\neq0\}\). This proves the first conclusion of (P).

### 3.3 Integrated gradient pairing from translations

The feasible set is invariant under translations of a potential: for every coordinate vector \(e_i\),
\[
\zeta(\cdot+te_i),\quad \zeta(\cdot-te_i)\in\mathcal C.
\]
Adding their two variational inequalities gives
\[
0\geq
\int_Qh(x)\,[\zeta(x+te_i)+\zeta(x-te_i)-2\zeta(x)]\,dx
=-\int_Q\delta_t h\,\delta_t\zeta\,dx,
\]
where \(\delta_tf(x)=f(x+te_i)-f(x)\). The equality uses periodic change of variables.

Divide by \(t^2\). Strong convergence of Sobolev difference quotients in \(L^2\), applicable because both functions are Lipschitz, yields
\[
\int_Q\partial_i h\,\partial_i\zeta\,dx\geq0.
\]
Summing and using \(\int_QDh=0\),
\[
\int_QDw\cdot(Du-Dw)\,dx
=\int_Q(b+D\zeta)\cdot Dh\,dx
=\int_QD\zeta\cdot Dh\,dx\geq0.
\]
This proves the second conclusion of (P).

The derivation uses translation invariance and a gradient constraint, in addition to the projection theorem. It supplies an integrated energy comparison. It does not assert \(Dw\cdot(Du-Dw)\geq0\) pointwise, pointwise gradient contraction, or orthogonality of the gradients.

## 4. Reconstruction of all-background quasiconvexity of \(L\)

Let \(r=A^1\), \(q=A^2\) denote the rows and \(J(v_1,v_2)=(-v_2,v_1)\). Define
\[
G_z(r,q)=\det(z,q)+z\cdot(r-z),\qquad
F(A)=2|a_+|-1=|q+Jr|-1.
\]
The unit-circle supremum of \(G_z\) is \(F\), a convex function of \(A\). Including \(z=r\) when \(|r|\leq1\) also includes \(\det A\). The identities
\[
\det A-F(A)=(1-x-y)(1-x+y),
\qquad |x-y|\leq |r|\leq x+y
\]
show exactly that
\[
L(A)=\sup_{z\in\mathcal Z(r)}G_z(r,q),\qquad
\mathcal Z(r)=S^1\cup
\begin{cases}\{r\},&|r|\leq1,\\\varnothing,&|r|>1.\end{cases} \tag{R}
\]
In particular \(L\geq F\) globally.

Fix arbitrary \(A,\varphi\) from Theorem 1 and \(U=Ax+\varphi\).
If \(|A|>1\), Jensen's inequality gives
\[
\int_QL(DU)\geq\int_QF(DU)\geq F(A)=L(A).
\]
If \(|A|\leq1\), apply the scalar projection lemma to \(u=U^1\), \(b=A^1\), \(K=\overline B_1(0)\). It gives an affine-periodic scalar \(w\) with \(|Dw|\leq1\), and either \(Dw=DU^1\) or \(|Dw|=1\) almost everywhere. Therefore \(Dw\in\mathcal Z(DU^1)\), including the case where \(Dw=DU^1\), since that row then has norm at most one. Formula (R) gives the pointwise comparison
\[
L(DU)\geq\det(Dw,DU^2)+Dw\cdot(DU^1-Dw). \tag{C}
\]
The determinant integrates to \(\det A\). To see this at the actual regularity, write \(w=A^1\cdot x+\zeta\), \(U^2=A^2\cdot x+\varphi^2\), expand, and integrate. Linear terms vanish by periodicity; the remaining term \(\det(D\zeta,D\varphi^2)\) integrates to zero by periodic integration by parts, justified with \(\zeta\in W^{1,\infty}\).

After integrating (C), the proven gradient-pairing inequality yields
\[
\int_QL(DU)\geq\det A=L(A).
\]
This handles every background and every allowed perturbation. The pointwise comparison (C) is algebraic; only its integrated remainder is nonnegative. The proof does not require the perturbation \(\varphi\) itself to be a scalar gradient.

## 5. Filling the cited bridge to every \(B_p\)

The source cites earlier arguments rather than writing this bridge. It can be obtained directly, without using the cited symmetric-matrix result.

For \(1<p<2\), the convergent signed integral identity is
\[
\int_0^\infty L(tA)\,\frac{dt}{t^{p+1}}
=\frac{2}{p(2-p)}B_p(A). \tag{M<}
\]
For \(p>2\), the necessary determinant subtraction gives
\[
\int_0^\infty [L(tA)-t^2\det A]\,\frac{dt}{t^{p+1}}
=\frac{2}{p(p-1)(p-2)}B_p(A). \tag{M>}
\]
Both identities follow by splitting at \(t=1/s\), with the zero-matrix case taken separately. For example, the left side of (M>) is
\[
s^{p-1}\left[\frac{2x}{p-1}-\frac{s}{p}-\frac{x-y}{p-2}\right].
\]
The analogous bracket in (M<) is
\[
\frac{x-y}{2-p}+\frac{2x}{p-1}-\frac{s}{p}.
\]
The coefficients in (M<) and (M>) are positive on their respective ranges. These exact algebraic identities are independently checked in checks.py.

Apply Theorem 1 to \(tA,t\varphi\) for every \(t>0\), then integrate against the positive weight. In (M>) the determinant terms cancel after spatial integration because the determinant is a null Lagrangian. Fubini is legitimate: \(A+D\varphi\) is bounded; for (M<) the small-\(t\) integrand is \(O(t^2)\) and the large-\(t\) integrand is \(O(t)\); for (M>) it vanishes for sufficiently small \(t\), uniformly in space, and is \(O(t^2)\) at infinity. These give integrable majorants precisely in the stated exponent ranges.

Thus \(B_p\) satisfies the same all-background quasiconvexity inequality for every \(p\neq2\). At \(p=2\), \(B_2=-\det\) and the inequality is equality. No sign restriction on \(B_p(A+D\varphi)\) was introduced.

## 6. Filling the sharp complex Beurling norm bridge

### 6.1 A pointwise scalar majorization

For \(p\geq2\), set \(c=p-1\) and
\[
\alpha_p=p(1-1/p)^{p-1}.
\]
The elementary inequality needed here is
\[
c^p y^p-x^p
\ \geq\ \alpha_p(cy-x)(x+y)^{p-1}
=\alpha_pB_p(A),\qquad x,y\geq0. \tag{B}
\]
It has the indicated direction. To check it for \(p>2\), divide by \(s^p\) and put \(a=x/s\). The difference is
\[
f(a)=c^p(1-a)^p-a^p-\alpha_p(c-pa),\quad 0\leq a\leq1.
\]
It vanishes at \(a_0=c/p\). Write
\[
f'(a)=p[\alpha_p-k(a)],\qquad
k(a)=c^p(1-a)^{p-1}+a^{p-1}.
\]
The function \(k\) is convex, \(k(a_0)=\alpha_p\), and \(k'(a_0)\leq0\), so \(k(a)\geq\alpha_p\) for \(a\leq a_0\). Also \(k(1)=1\leq\alpha_p\), so convexity gives \(k(a)\leq\alpha_p\) between \(a_0\) and 1. Consequently \(f\) decreases to zero and then increases. The bound \(\alpha_p\geq1\) follows by differentiating its logarithm from \(p=2\): the derivative is \(\log(1-1/p)+2/p\geq0\). At \(p=2\), (B) is equality.

### 6.2 From zero-background quasiconvexity to the transform upper bound

The all-background result in particular gives \(\int B_p(Df)\geq0\) for smooth compactly supported plane maps \(f:\mathbb C\to\mathbb C\), by placing the support in a sufficiently large periodic cell and rescaling the cell. Here \(a_+=\partial_zf\), \(a_-=\partial_{\bar z}f\). Combining this with (B) gives
\[
\|\partial_zf\|_p\leq(p-1)\|\partial_{\bar z}f\|_p.
\]
Apply the same conclusion to the map \(\bar f\), which interchanges the magnitudes of the two derivatives, to obtain
\[
\|\partial_{\bar z}f\|_p\leq(p-1)\|\partial_zf\|_p. \tag{U}
\]
This reflection is needed to match the paper's convention \(\mathcal S\partial_z=\partial_{\bar z}\).

The compact-support inequality extends to Schwartz \(f\) by smooth spatial cutoffs and convergence in \(W^{1,p}\). The \(p\)-growth continuity estimate for \(B_p\) also preserves its integral inequality under that convergence. For Schwartz \(g\) with Fourier support compact and separated from the origin, the nonzero symbol of \(\partial_z\) can be inverted to produce a Schwartz \(f\) with \(\partial_zf=g\). This is a dense subspace of \(L^p\), \(1<p<\infty\). Inequality (U) therefore gives a unique bounded extension satisfying
\[
\|\mathcal S\|_{L^p(\mathbb C;\mathbb C)\to L^p(\mathbb C;\mathbb C)}\leq p-1
\quad(p\geq2).
\]
For \(1<p<2\), duality gives the constant \(p'-1=(p-1)^{-1}\): the adjoint multiplier is \(\overline{m}\), and complex conjugation conjugates \(\mathcal S\) to its adjoint because \(m(-\xi)=m(\xi)\). Conjugation preserves every complex \(L^p\) norm. At \(p=2\), \(|m|=1\) gives the norm one directly.

### 6.3 A direct sharpness sequence

The lower bound need not be taken on authority. On an annulus let
\[
f(z)=z|z|^{-\gamma},\qquad \gamma=2/p.
\]
Its two derivative magnitudes are
\[
|\partial_zf|=(1-1/p)|z|^{-2/p},\qquad
|\partial_{\bar z}f|=(1/p)|z|^{-2/p}.
\]
Use smooth radial cutoffs so that the map agrees with this expression on \(\varepsilon<|z|<1\), vanishes on \(|z|<\varepsilon/2\) and \(|z|>2\), and has uniformly scaled cutoff derivatives. The \(p\)-th-power integrals on the annulus have leading terms \(2\pi\log(1/\varepsilon)\) times the displayed coefficients to power \(p\). Both cutoff regions contribute \(O(1)\), because \(p\gamma=2\).

For \(1<p\leq2\), this gives
\[
\frac{\|\partial_{\bar z}f_\varepsilon\|_p}{\|\partial_zf_\varepsilon\|_p}
\longrightarrow(p-1)^{-1}.
\]
For \(p\geq2\), conjugate the maps to reverse the derivative magnitudes and get the limit \(p-1\). These are smooth compactly supported test maps for the same transform convention. Together with the upper bound, this reconstructs the equality claimed in Corollary 2 within the stated planar complex \(L^p\) setting.

## 7. Exact falsifiers of projection substitutions

These examples contradict shortcuts, not the source's actual assertions.

### 7.1 A linear gradient projection does not enforce the restriction

The orthogonal Hodge projection onto periodic gradient vector fields leaves a gradient \(D\eta\) unchanged. For any nonconstant periodic scalar \(\zeta\) with \(|D\zeta|=1\) almost everywhere, \(D(2\zeta)\) is still a gradient but violates \(|D\xi|\leq1\). Thus Hodge projection cannot replace the metric projection onto \(\mathcal C\).

The latter projection is nonlinear: it fixes feasible \(\zeta\), while it cannot map \(2\zeta\) to \(2\zeta\). Neither fact refutes the actual convex metric projection.

### 7.2 A true metric projection can increase gradient magnitude locally

On \(Q\), let \(\zeta(x_1,x_2)=\min\{x_1,1-x_1\}-1/4\), periodically extended, so \(D\zeta=(\sigma,0)\), where \(\sigma=\operatorname{sign}\sin(2\pi x_1)\). Take \(b=0\), \(K=\overline B_1(0)\), and
\[
\lambda=\frac1{30\pi^2},\quad
v(x_1)=\lambda\sin^3(2\pi x_1),\quad
h=-v',\quad \eta=\zeta+h.
\]
For every feasible \(\xi\),
\[
\int_Qh(\xi-\zeta)
=\int_Qv(\partial_1\xi-\sigma)\leq0.
\]
Indeed \(\partial_1\xi\leq1\) where \(v\geq0,\sigma=1\), and \(\partial_1\xi\geq-1\) where \(v\leq0,\sigma=-1\). Hence \(\zeta\) is exactly the unique \(L^2\) projection of \(\eta\) onto the source's feasible set.

At \(x_1=1/12\), an interior differentiability point of all functions,
\[
\partial_1\zeta=1,\qquad h'=-1/4,\qquad\partial_1\eta=3/4.
\]
Thus
\[
D\zeta\cdot(D\eta-D\zeta)=-1/4<0,\qquad
|D\zeta|=1>|D\eta|=3/4.
\]
The strict inequalities persist on an open strip. Nevertheless the integrated pairing is zero, exactly as allowed by (P): integrate \(-v''\) separately on the two half periods and use \(v'(0)=v'(1/2)=v'(1)=0\).

Also
\[
\int_Qh\zeta=\int_Qv\sigma
=\frac{4\lambda}{3\pi}>0.
\]
This is an explicit failure of potential-space orthogonality. Replacing \(v\) by a positive multiple of \(\sin(2\pi x_1)\) gives another exact metric projection with integrated gradient pairing \(8\pi\lambda>0\), rejecting any assertion that the pairing must always be zero.

### 7.3 Radial clipping of a gradient need not remain a gradient

Take the smooth periodic potential
\[
\eta(x_1,x_2)=\sin(2\pi x_1)\sin(2\pi x_2)
\]
and clip its gradient radially:
\[
V=\frac{D\eta}{\max\{1,|D\eta|\}}.
\]
At \((x_1,x_2)=(1/12,1/8)\), \(|D\eta|=\sqrt2\pi>1\) and direct differentiation gives
\[
\partial_1V_2-\partial_2V_1=\frac{\pi\sqrt3}{2}\neq0.
\]
The clipped field fails the distributional curl-free condition even locally, so it cannot be the gradient of the projected potential. This rejects pointwise clipping as an implementation or explanation of Lemma 4.

## 8. What this audit establishes and leaves open

The actual load-bearing proof uses two different mechanisms: scalar max/min competitors force saturation, and translation competitors force an integrated gradient pairing. The algebraic row representation and determinant null-Lagrangian identity then connect those mechanisms to arbitrary vector perturbations. The integral transforms and scalar majorization above reconstruct the claimed planar norm consequence without importing the cited symmetric-matrix paper.

No decisive mathematical falsifier of that exact chain was found. The proof's importance is not evidence either for or against its correctness. The exact counterexamples supplied here apply only to stronger or different projection statements.

The audit has not verified the announced higher-dimensional or differential-form generalizations, quasiconformal applications beyond the displayed planar norm chain, journal acceptance, later-version corrections, or the causal AI attribution. Symbolic checks certify their displayed algebraic identities, not the whole infinite-dimensional argument. The reconstructed argument remains source_derived_unreviewed for Astra integration, and this worker authorizes no premise promotion.

Reproduction: run checks.py with R/.venv/bin/python. checks.json records exact symbolic outputs and limited diagnostic checks. acquisition_receipts.json pins the source bytes, while manifest.json inventories the saved audit artifacts.
