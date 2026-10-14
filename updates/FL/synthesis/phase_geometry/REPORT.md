# Phase geometry: a sheared non-affine positive family and the exact curvature obstruction

## Result and scope

This note derives the signed term created by a variable phase and proves a periodic Jensen family with a non-affine phase and a genuinely two-variable amplitude. Every homogeneous rank-one-convex quartic in the full nine-coefficient left-$SO(2)$-invariant planar class has a nonnegative gap on this family after minimizing over **all** affine backgrounds. The proof needs no near-line hypothesis or strict rank-one lower bound.

This is a structured periodic-gradient theorem. It does not prove quasiconvexity of the full nine-coefficient cone, cover arbitrary phases and amplitudes, or construct a negative Jensen gap. N794, N809, and N806 remain source-derived and externally unreviewed. This note is an internal analytic derivation with exact symbolic checks, not external validation or priority certification.

## Variable-phase flux identity

Let $F:\mathbb R^{m\times n}\to\mathbb R$ be $C^2$ and rank-one convex. Let $V$ be a periodic $C^2$ curve with $W=V'$ and $V''(\theta)=-a(\theta)V(\theta)$, where $a\geq0$. For a smooth periodic real amplitude $r$ and phase $\theta(x)$, put
$$
k=\nabla\theta,\qquad \varphi=rV(\theta),\qquad
P=rW\otimes k,\qquad Q=V\otimes\nabla r.
$$
Then $D\varphi=P+Q$, and both summands are pointwise rank one. Define
$$
\mathcal R_F(C,Q)=F(C+Q)-F(C)-DF(C)[Q]
$$
and, with $\theta_{ij}=\partial_i k_j$,
$$
\mathcal E_F(x)=\sum_{i,j}\theta_{ij}(x)
\int_0^{r(x)}s\,D^2F(B+sW\otimes k)
[W\otimes e_j,V\otimes e_i]\,ds.
\tag{1}
$$
The exact identity is
$$
\boxed{
\begin{aligned}
\left\langle F(B+D\varphi)-F(B)\right\rangle
={}&\left\langle\mathcal R_F(B+P,Q)\right\rangle\\
&+\left\langle a(\theta)\int_0^r sD^2F(B+sW\otimes k)
[V\otimes k,V\otimes k]\,ds\right\rangle
-\langle\mathcal E_F\rangle .
\end{aligned}}
\tag{2}
$$
Here $\langle\cdot\rangle$ is normalized torus average. To prove it, take the spatial flux
$$
\mathcal A_i(x)=\int_0^{r(x)}DF(B+sW(\theta(x))\otimes k(x))
[V(\theta(x))\otimes e_i]\,ds.
$$
Differentiating the upper limit gives $DF(B+P)[Q]$. The phase derivative uses $V'=W$ and $W'=-aV$; after summing over $i$, its terms are $F(B+P)-F(B)$ and the negative acoustic integral in (2). Differentiating $k$ gives exactly (1), with a plus sign in $\operatorname{div}\mathcal A$. Since the flux is periodic, its divergence has zero mean. Substitution into the rank-one Bregman identity gives (2). The correction in the Jensen gap therefore enters with a **minus** sign.

Rank-one convexity makes the first two terms on the right of (2) nonnegative: $Q$ is rank one, and the acoustic variation $V\otimes k$ is rank one. The term (1) pairs two rank-one directions, but rank-one convexity does not sign their mixed Hessian.

## A curvature equation at zero background

For a planar homogeneous quartic invariant under left $SO(2)$, write
$$
F=A u^2+B_0v^2+Cuv+Ew^2+Guw+Hvw+q(Lu+Mv+Nw),
$$
where $u=|A_1|^2$, $v=|A_2|^2$, $w=A_1\cdot A_2$, and $q=\det A$. Take the circular carrier $V=(\cos\theta,\sin\theta)$, $W=V'$. At $B=0$, homogeneity and output-rotation invariance reduce (1) to
$$
\boxed{\mathcal E_F=\frac{r^4}{4}\operatorname{div}\Xi(\nabla\theta),\qquad
\Xi(k)=(Lk_1^2+Mk_2^2+Nk_1k_2)(k_2,-k_1).}
\tag{3}
$$
The six reflection-even coefficients make no contribution to $\Xi$. For the orientation-odd part, $\Xi_i(k)=DF(W\otimes k)[V\otimes e_i]$; differentiating this in $k$ gives (1) at $B=0$.

Writing $k=(p,q_0)$ and $D^2\theta=\begin{psmallmatrix}a&b\\b&c\end{psmallmatrix}$, the three independent curvature coefficients are
$$
\begin{aligned}
\operatorname{div}(k_1^2(k_2,-k_1))&=2p q_0a-2p^2b,\\
\operatorname{div}(k_2^2(k_2,-k_1))&=2q_0^2b-2p q_0c,\\
\operatorname{div}(k_1k_2(k_2,-k_1))&=q_0^2a-p^2c.
\end{aligned}
\tag{4}
$$
The coefficients $L,M,N$ can be varied independently while retaining rank-one convexity: add a sufficiently small multiple of any one of these three quartics to $|A|^4$, whose Legendre-Hadamard Hessian is strictly positive away from $A=0$. Thus universal zero-background cancellation for every rank-one-convex member of this cone forces (4) to vanish term by term. At each point with $k\ne0$, this is equivalent to
$$
D^2\theta=\lambda\,\nabla\theta\otimes\nabla\theta.
\tag{5}
$$
For example, when $p,q_0\ne0$, the first two equations in (4) give $b=q_0a/p$ and $c=q_0^2a/p^2$; the axis cases follow from the other two equations. Equation (5) says the gradient is constant along each regular level set. More directly, on a patch where $k\ne0$, differentiating $k/|k|$ and using $Dk=\lambda k\otimes k$ gives $D(k/|k|)=0$. Its direction is locally constant, so $\theta=f(\ell\cdot x)$ locally on regular patches. This gives a non-affine straight-front class at $B=0$, but does not by itself handle arbitrary affine backgrounds.

There is a real all-background obstruction to simply extending the affine-phase flux argument. For the globally convex quartic $F_0(A)=|A|^4$, at a point with $V=e_1,W=e_2$, let $\alpha_j=W\cdot B_j$ and $\beta_i=V\cdot B_i$. As $r\to0$, (1) has the expansion
$$
\mathcal E_{F_0}(B,r,\theta)=4r^2\,\beta^T(D^2\theta)\alpha+O(r^3).
\tag{6}
$$
The vectors $\alpha,\beta$ can be chosen independently by choosing the columns of $B$. Every nonzero phase Hessian therefore produces a nonzero mixed correction for some affine background, even for the globally convex quartic $F_0$. This rules out a universal all-background derivation that drops the correction pointwise. It does not rule out a different proof that controls it against the positive terms.

## Non-affine all-background theorem

Let $F:\mathbb R^{2\times2}\to\mathbb R$ be a homogeneous rank-one-convex quartic invariant under left $SO(2)$. Work on the standard $2\pi$-periodic torus with coordinates $(x,y)$. Let $n\in\mathbb Z\setminus\{0\}$, let $g$ be a periodic $C^2$ function, and set
$$
\theta(x,y)=ny+g(x),\qquad
\varphi(x,y)=r(x,y)(\cos\theta,\sin\theta).
\tag{7}
$$
Assume $r$ is smooth and periodic, with half-turn symmetry
$$
r(x,y+\pi/|n|)=r(x,y),
\tag{8}
$$
and define $m(x)=(2\pi)^{-1}\int_0^{2\pi}r(x,y)^4\,dy$. It is enough that
$$
\int_0^{2\pi}m(x)g''(x)\,dx=0,\qquad
\int_0^{2\pi}m(x)g'(x)g''(x)\,dx=0.
\tag{9}
$$
Then the **complete affine-background gap** is nonnegative:
$$
\boxed{
\inf_{B\in\mathbb R^{2\times2}}
\left\langle F(B+D\varphi)-F(B)\right\rangle
=\langle F(D\varphi)\rangle\geq0.}
\tag{10}
$$
A constant $m(x)$ satisfies (9) for every periodic $g$. The theorem includes nonconstant $g$, amplitudes depending on both coordinates, and fields with full-rank gradients. It requires no smallness assumption and no positive lower bound on $F$ over rank-one matrices.

**Proof.** Write $X=D\varphi$, $k=(g',n)$, $P=rW\otimes k$, and $Q=V\otimes\nabla r$. At $B=0$, the acoustic term in (2) equals
$$
\frac{r^4}{4}D^2F(W\otimes k)[V\otimes k,V\otimes k]\geq0
$$
by quartic homogeneity and rank-one convexity. Also $\mathcal R_F(P,Q)\geq0$. From (3),
$$
\operatorname{div}\Xi(k)=n(2Lg'+nN)g'',
$$
where $L,N$ are the coefficients of the given $F$. Hence
$$
\langle\mathcal E_F\rangle
=\frac{n}{8\pi}\left(2L\int m g'g''\,dx+nN\int m g''\,dx\right)=0
$$
by (9). Equation (2) proves $c:=\langle F(X)\rangle\geq0$.

The shift $y\mapsto y+\pi/|n|$ changes $(V,W)$ to $(-V,-W)$, while (8) leaves $r,\nabla r,k$ unchanged. Thus $X\mapsto-X$. Since $DF$ is cubic, $b:=\langle DF(X)\rangle=0$.

Finally put $H:=\langle D^2F(X)\rangle$. For any constant matrix $A$, quartic tensor symmetry gives
$$
A:HA=\langle D^2F(X)[A,A]\rangle
=\langle D^2F(A)[X,X]\rangle\geq0.
$$
For the last inequality expand the compatible periodic gradient $X=D\varphi$ in Fourier modes. Each nonzero mode is a complex rank-one matrix $z\otimes\xi$; its real and imaginary parts are rank one. The acoustic Hessian $D^2F(A)$ is nonnegative on both by rank-one convexity. Parseval therefore gives $H\succeq0$. Exact quartic expansion and $\langle X\rangle=0$ give
$$
\left\langle F(B+X)-F(B)\right\rangle
=c+b:B+\frac12 B:HB
=c+\frac12 B:HB\geq c.
$$
Equality holds at $B=0$, proving (10). $\square$

An explicit genuinely two-variable member is
$$
g(x)=\tfrac14\sin x,\qquad
h(x)=\tfrac13\sin(2x),\qquad
r(x,y)=1+\tfrac15\cos(2(y+h(x))),\qquad
\theta=y+g(x).
\tag{11}
$$
Here $r\in[4/5,6/5]$, $r(x,y+\pi)=r(x,y)$, and
$$
m(x)=\left\langle r^4\right\rangle_y
=1+3(1/5)^2+\tfrac38(1/5)^4=5603/5000
$$
independent of $x$. Both $g''$ and the $x$- and $y$-dependence of $r$ are nonzero. Since the amplitude modulus depends on $y$, (11) is not a one-coordinate complex envelope $z(x)e^{iny}$. Its gradient determinant is $r\,r_y(h'-g')$, which is nonzero on an open set; it is not a pointwise rank-one profile either. Its affine-optimized Jensen gap is nonnegative for every rank-one-convex left-$SO(2)$ quartic by (10).

## Exact sign counterexample and the precise boundary

The variable-phase correction cannot be assigned a favorable sign. For the globally convex invariant quartic
$$
F_c=(u+v-2q)^2,
$$
take $\theta=x+\sin y$ and the smooth positive amplitude determined by
$$
r(y)^4=1-\tfrac12\sin(2y).
$$
The identity $u+v-2q=(a-d)^2+(b+c)^2$ shows that $F_c$ is the square of the squared norm of a linear map, hence convex. For this energy $L=M=-4,N=0$, so $\operatorname{div}\Xi=-4\sin(2y)$. Formula (3) gives
$$
\langle\mathcal E_{F_c}\rangle
=\left\langle-\sin(2y)+\tfrac12\sin^2(2y)\right\rangle
=\frac14.
$$
Changing the sign in $r^4$ gives $-1/4$. This is an exact compatible counterexample to discarding the variable-phase term or assigning it a fixed sign, not a negative Jensen gap; convexity of $F_c$ still gives nonnegative Jensen gaps.

The sheared theorem avoids that failure by imposing exact weighted curvature cancellation and a separate half-turn symmetry that closes the complete affine optimization. It is a structured family, not a general phase-straightening operation. Flattening $ny+g(x)$ by a change of coordinates right-multiplies the input gradient by a variable shear; that coefficient remains correlated with $r$ and with $D^2F$. The missing general operation is a bound or exact cancellation for this signed mixed-Hessian transport term **after** affine optimization.

## Relation to the pinned capital and prior art

N794 isolates the open nine-moment compatibility completion behind the full cone. The present theorem gives positivity only for the explicit profile family (7)–(9); it does not supply a completion for arbitrary gradients. N809 controls all affine directions near transverse contacts using a moving acoustic eigenvector, covariance regression, and the actual Schur denominator. N806 controls a compatible cubic at fixed tangent contacts using Hodge/curl identities. Neither result controls (1) for arbitrary phase Hessians, and replacing its reduced denominator by an unreduced contact quantity would not address this transport term.

The primary comparison inspected was Astala, Iwaniec, Prause, and Saksman, *A hunt for sharp $L^p$-estimates and rank-one convex variational integrals*, arXiv:1403.1095v1, Section 5, Proposition 5.1. It proves a rank-one-concave integral inequality for radially linear maps $f(x)=\Lambda(|x|)x$ by integrating a rank-one tangent inequality over spherical shells. This is established prior art for a different geometric family and for rank-one concavity; this targeted comparison is not priority clearance for (7)–(10). Link: <https://arxiv.org/html/1403.1095v1>.

## Verification and limits

phase_geometry_checks.py uses SymPy exact symbolic algebra. It verifies the variable-phase flux identity for all 35 planar quartic monomials with symbolic affine background, carrier, amplitude, amplitude gradient, and symmetric phase Hessian; reconstructs the nine-term $\Xi$ formula and the sheared curvature equation; checks the all-background leading defect (6); checks the signed convex example and its sign reversal; and checks the transported-amplitude fourth moment and straight-front cancellation. All 60 exact assertions passed. These are finite symbolic checks; the general conclusions above rest on the displayed analytic proofs, not on the checks.

The only supplied/acquired mathematical inputs are the coefficients of $F$, the integer $n$, and the specified smooth periodic profiles $r,g$. No laboratory, measurement, calibration, or external inference service is involved. The exact-check script evaluates fixed symbolic identities; no asymptotic or empirical claim is inferred from runtime. No external correctness review, formal proof-assistant check, historical novelty clearance, or counterexample to Morrey's implication was obtained. The result remains scoped to the periodic family (7)–(9).
