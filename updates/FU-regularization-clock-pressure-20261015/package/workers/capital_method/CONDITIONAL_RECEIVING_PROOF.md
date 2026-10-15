# Conditional anisotropic-to-critical-trace transfer

Written after freezing the original independent audit, at root's explicit request to examine a new anisotropic G certificate. This file proves the **receiving implication conditional on that certificate**. Its existence or numerical feasibility is not assumed established here. The separate final receiving audit must record an actual exact certificate check before using the implication for G.

Write

\[
\mathcal C A=(a-d,b+c),\qquad H(A)=|\mathcal C A|^4,
\quad A=\begin{pmatrix}a&b\\c&d\end{pmatrix}.
\]

Assume the all-background quasiconvexity of

\[
G-\eta H,\qquad \eta=3/16000,
\]

on planar zero-boundary maps and its periodic extension. This is a different hypothesis from the impossible isotropic subtraction `G−epsilon|A|^4` in the original report.

## The width-independent differential estimate

For a compactly supported smooth map u:R²→R², put f=u₁+i u₂ and use

\[
\partial f=(f_x-if_y)/2,\quad
\bar\partial f=(f_x+if_y)/2.
\]

Then \(\mathcal C Du=2(\operatorname{Re}\bar\partial f,
\operatorname{Im}\bar\partial f)\), and

\[
|Du|^2=2(|\partial f|^2+|\bar\partial f|^2).
\]

The established coarse Beurling bound \(\|\mathcal B\|_{L^4(\mathbb C)}\le\sqrt{24}\), together with \(\partial f=\mathcal B\bar\partial f\), gives

\[
\begin{aligned}
\|Du\|_4^4
&\le4(\|\partial f\|_4^2+\|\bar\partial f\|_4^2)^2\\
&\le4(24+1)^2\|\bar\partial f\|_4^4
=\frac{625}{4}\|\mathcal C Du\|_4^4.
\end{aligned}
\tag{1}
\]

The norm is the complex-scalar L4 norm. A statement only for real input functions would not suffice without a complexification argument. The numerical norm premise requires its own primary-source receipt; the rest of (1) is direct algebra and Minkowski's inequality.

Now let u∈W^(1,4)((0,L)×T;R²), with zero traces at both x endpoints and arbitrary finite width L. Zero-extend u in x to R×T. The zero traces ensure a W^(1,4) extension; no derivative matching is needed. Unwrap the periodic y coordinate. For a fixed smooth nonzero compact cutoff χ, apply (1) to u_N(x,y)=χ(y/N)u(x,y), after standard smooth approximation.

For each fixed u and L, the main fourth-power integrals scale as N times the one-period integrals, with factor `integral |chi|^4 / period`. The L4 norm of the cutoff derivative error is O(N^(-3/4)) times the finite one-period L4 norm of u. After division by N^(1/4), that error tends to zero. Letting N tend to infinity proves (1) on the cylinder with **the same constant, independent of L**. No uniform Poincare estimate in L is used or required. This order of limits matters: u and its finite strip are fixed before N grows.

The same plane estimate applies directly after zero extension for W₀^(1,4) maps on any planar Lipschitz domain. A periodic torus follows by large cutoffs in both coordinates. Mean constants are irrelevant because only derivatives enter.

## All-background pure fourth-power Jensen coercivity

For the convex quartic h(z)=|z|⁴, its one-dimensional convex quartic restriction gives

\[
h(z+w)-h(z)-Dh(z)\cdot w\ge |w|^4/3.
\tag{2}
\]

This estimate is uniform in z,w; it does not assert a positive uniform quadratic curvature. Using quasiconvexity of G−eta H, the vanishing integral of Dφ, (2), and then (1), yields

\[
\int[G(B+D\varphi)-G(B)-DG(B):D\varphi]
\ge\frac\eta3\int|\mathcal C D\varphi|^4
\ge\gamma\int|D\varphi|^4,
\tag{3}
\]

where

\[
\gamma=\frac{\eta}{3}\frac4{625}=\frac1{2500000}.
\]

For a closed cylinder strip, first use its periodic all-background Jensen inequality, or its x-zero extension and the same large-y-cutoff argument for the polynomial relative action. Each fixed strip has finite L2, L3, L4 norms; the cutoff errors vanish after period normalization. Thus (3) is valid on the closed strips needed for gluing, uniformly in their width.

Equation (3) does **not** supply `|B|² ||Dphi||₂²` coercivity on arbitrary-width strips. At the acoustic null of G that stronger quadratic assertion is false. The subsequent proof avoids it.

## Incoming storage and a fixed-width return

Use normalized y averaging and the exact incoming-path class in FR `HEAT_TO_CRITICAL_TRACE.md`, lines 37–104. Let

\[
f_B(A)=G(B+A)-G(B)-DG(B):A,
\quad J_B(\Phi)=\int f_B(D\Phi),
\quad p_B(U)=\inf_{T>0,\,\Phi(0)=0,\,\Phi(T)=U}J_B(\Phi).
\]

All finite-width W^(1,4) paths are allowed, including moving transverse means. For mean-zero U∈W^(3/4,4)(T;R²), take the fixed bounded unit-slab trace extension E with endpoints 0,U, and write e_p(U)=||D(EU)||_p. Its reflected return RU has the same gradient norms and endpoints U,0. Reflection invariance of G is neither needed nor asserted.

Choose constants C₀,C₁ such that

\[
|f_B(A)|\le C_0(|B|^2|A|^2+|A|^4),
\quad |Df_B(A)|\le C_1(|B|^2|A|+|A|^3).
\tag{4}
\]

These exist by quartic polynomial growth. One conservative explicit choice for the retained G is C₀=2542 and C₁=5084: a triangle bound on the absolute coefficient sum is 1271/6, hence ||D²G(A)||≤2542|A|²; integral Taylor estimates yield (4). Optimal constants are not claimed.

Put

\[
M_B(U)=C_0(|B|^2e_2(U)^2+e_4(U)^4).
\]

Concatenating any incoming Phi with RU gives a W^(1,4) map continuous across its seam and zero at the outer x faces. Applying (3) and bounding its return action gives

\[
J_B(\Phi)\ge\gamma\|D\Phi\|_4^4-M_B(U).
\tag{5}
\]

The fixed extension itself gives p_B(U)≤M_B(U), and (5) gives p_B(U)≥−M_B(U). If Phi has action at most p_B(U)+rho, then

\[
\|D\Phi\|_4^4\le\gamma^{-1}[2M_B(U)+\rho].
\tag{6}
\]

This is duration-independent **pure L4** control, sufficient for the next step.

## Only the terminal unit slab is perturbed

For U,W in the mean-zero trace space, prepend a zero strip to any near-minimizing Phi for U until its width is at least one. Add the translate of E(W−U) on the terminal unit slab, extended by zero earlier. Its zero left trace makes the new path W^(1,4) without a seam jump, and it ends at W.

Let d=e₄(W−U) and

\[
K=\left[\frac{2\max\{M_B(U),M_B(W)\}}\gamma\right]^{1/4}.
\]

The integral difference is supported on that unit-measure slab. There, L2 norms are bounded by L4 norms. Equation (4), Holder, and (6), with rho tending to zero, give

\[
|p_B(W)-p_B(U)|
\le C_1\bigl[|B|^2(K+d)+(K+d)^3\bigr]d.
\tag{7}
\]

Exchange U,W for the other direction. If |B|≤B_* and e₄(U),e₄(W)≤R, take

\[
K_R=\left[\frac{2C_0(B_*^2R^2+R^4)}\gamma\right]^{1/4},
\quad
L_{B_*,R}=C_1[B_*^2(K_R+2R)+(K_R+2R)^3].
\]

Then (7) is a uniform Lipschitz bound on that bounded trace ball with constant L_(B*,R) in the extension norm e₄. The chosen trace extension makes e₄ equivalent to the critical W^(3/4,4) norm on mean-zero profiles. The potentially width-dependent full-strip L2 norm never enters this estimate.

The adjusted storage is invariant under adding an output constant: prepend an arbitrarily slow constant ramp and use its action O_B(|c|²/L+|c|³/L²+|c|⁴/L³)→0, then argue in both directions. For the original unsubtracted action restore the necessary affine mean term

\[
P_B(U)=G_1(B)\cdot\mathbb E_yU+p_B(U-\mathbb E_yU).
\]

Concatenation proves domination of every compatible strip action, including moving means. No minimizing incoming path is asserted to exist. Neither the infinite-width infimum nor the optimal extension is supplied by a finite algorithm.

Bounded-ball Lipschitz continuity does not make finite Fourier projections uniformly adequate on a bounded critical ball: the actual critical tail must be bounded or acquired. It also does not close the full invariant quartic cone, give weak topology continuity, determine historical novelty, or establish a physical capability.
