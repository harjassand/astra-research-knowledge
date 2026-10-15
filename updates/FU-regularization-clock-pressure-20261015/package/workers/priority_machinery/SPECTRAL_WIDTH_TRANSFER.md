# Shift-invariant uniform regularization from spectral width

Status: independent internal derivation, 2026-10-15. This is a theorem-level transfer from the known Weyl support argument and the retained-tilt construction. Historical priority and independent external verification are UNKNOWN. No circuit, sampler, variance optimum, or practical advantage is asserted.

## Exact statement

For a finite tuple of bounded self-adjoint operators on any complex Hilbert space, put

\[
A(u)=\sum_{j=1}^m u_j A_j,\qquad
\Delta(A)=\sup_{|u|=1}\left(\sup\sigma A(u)-\inf\sigma A(u)\right).
\]

Fix \(m\), \(D>0\), \(0<c<1/D\), and \(0<\varepsilon<1\). There is a finite \(L_0(m,D,c,\varepsilon)\), independent of Hilbert-space dimension and of scalar offsets in the observables, with the following property. For every tuple with \(\Delta(A)\le D\), the same radial scalar density

\[
p_L(x)=Z_L^{-1}\exp[-V_L(x)],\quad
V_L(x)=cL\rho(x/L)\log\rho(x/L),\quad
\rho(z)=\sqrt{1+|z|^2},
\]

regularizes its Weyl distribution whenever \(L\ge L_0\):

\[
M_A=W_A*p_L\succeq0,\qquad
\int M_A(x)\,dx=I,\qquad
\widehat M_A(t)=\widehat p_L(t)e^{iA(t)}.
\]

The density is smooth, radial, strictly log-concave, and has every exponential moment, as do the absolute values of all its derivatives. Its radial logarithmic tail is \(c r\log r+O(r)\).

For \(m\ge2\), the supremum of universally permitted coefficients in this radial upper-tail class is exactly \(1/D\). Endpoint attainment is not asserted. When \(D=0\), every observable is scalar and no finite tail restriction of this kind is necessary.

The statement improves the supplied sufficient condition whenever absolute offsets enlarge its norm radius. It also avoids the loss from centering each coordinate and then enclosing the resulting tuple in a Euclidean norm ball. It does not claim a tuple-specific sharp threshold: commuting tuples can allow Gaussian noise despite nonzero spectral width.

## 1. The known support operation, with the infinite-dimensional detail supplied

Define the closed joint numerical-range body by half spaces,

\[
K_A=\{y\in\mathbb R^m:\inf\sigma A(u)\le u\cdot y\le\sup\sigma A(u)
\text{ for every }u\in\mathbb R^m\}.
\]

For finite matrices this is the mixed-state joint numerical range. For arbitrary Hilbert spaces use its closure, or equivalently the image of the full state space of the generated unital C*-algebra. Compactness follows in the finite-dimensional output space; norm compactness of density operators is not assumed.

The norm-valued distribution is defined by Fourier integration. Unitarity gives

\[
\|W_A(h)\|\le(2\pi)^{-m}\|\widehat h\|_1.
\tag{1}
\]

For real \(t,s\), the Trotter product formula, or the vector-norm differential inequality, gives

\[
\|e^{iA(t)-A(s)}\|\le e^{-\inf\sigma A(s)}.
\tag{2}
\]

Apply the scalar Paley-Wiener-Schwartz support theorem to every bounded linear functional of this entire operator-valued transform. Equation (2) supplies the supporting-function bound for \(K_A\), so \(\operatorname{supp}W_A\subseteq K_A\). Scalarization recovers operator-norm equality with zero off that body. This is the same support mechanism explicitly proved in Schwonnek-Werner, Property 1, PDF p. 3, Eqs. (6)-(9), extended here without the finite-matrix compact-state-space shortcut.

## 2. Uniform seminorms on a body-adapted cutoff

Let \(a_j=(\sup\sigma A_j+\inf\sigma A_j)/2\) and \(B_j=A_j-a_jI\). Then \(\|B_j\|\le D/2\), so

\[
K_B\subseteq[-D/2,D/2]^m,
\qquad\sup_{|u|=1}\big(h_{K_B}(u)+h_{K_B}(-u)\big)\le D.
\tag{3}
\]

Choose \(\delta>0\) with \(c(D+\delta)<1\). Smooth the indicator of the \(\delta/2\) neighborhood of \(K_B\) by a fixed probability bump supported in the \(\delta/4\) ball. The resulting cutoff \(\chi_B\) is one near \(K_B\), is supported in \((K_B)_\delta\), and has uniformly bounded derivatives of every fixed order, independently of \(B\) and dimension of the Hilbert space.

Take an integer \(k>m/2\) and \(N=2k\). Integrating by parts in the Fourier transform yields

\[
\|\widehat{\chi_B h}\|_1
\le \|(1-\Delta)^k(\chi_Bh)\|_1
\int_{\mathbb R^m}(1+|t|^2)^{-k}dt.
\]

All cutoff supports lie in the fixed ball of radius \(\sqrt m D/2+\delta\). Combining this with (1) gives a common finite-order distribution bound, depending only on \(m,D,\delta,N\). Derivative estimates below can therefore retain the sharper exponential factor \(e^{h_{K_B}(g)+\delta|g|}\); replacing the body by a round ball in that factor would unnecessarily lose the width improvement.

## 3. Retained exponential tilt and the width cancellation

Put \(z=x/L\), \(s=\log\rho(z)\), and \(g=\nabla V_L(x)\). Direct differentiation gives

\[
|g|\le c(1+s),\qquad
\|D^j(\rho\log\rho)(z)\|\le C_j(1+s)\rho^{1-j}\quad(j\ge2).
\tag{4}
\]

The tangential Hessian eigenvalue is \((1+\log\rho)/\rho>0\); the radial eigenvalue is \((|z|^2+1+\log\rho)/\rho^3>0\). Thus the potential is strictly convex.

For \(|y|\le\sqrt mD/2+\delta\), the exact remainder

\[
F_x(y)=V_L(x-y)-V_L(x)+g\cdot y
\]

satisfies, for all sufficiently large \(L\) depending only on the displayed fixed parameters,

\[
\|e^{-F_x}-1\|_{C^N}\le {C\over L}{1+s\over\rho}.
\tag{5}
\]

Taylor's integral remainder proves the zero and first derivative estimates; (4) proves the higher derivatives. Over a fixed \(y\)-ball, \(\rho(z-y/L)\) and \(\rho(z)\) differ by bounded factors and their logarithms by a bounded additive amount. The right-hand side of (5) is globally bounded by \(C/L\), so the exponential chain rule is uniform in all \(x\).

The exact identity \(p_L(x-y)=p_L(x)e^{g\cdot y}e^{-F_x(y)}\) gives

\[
{M_B(x)\over p_L(x)}=e^{B(g)}+E_x.
\]

The cutoff estimate and (5) imply

\[
\|E_x\|\le {C\over L}
e^{h_{K_B}(g)+\delta|g|}(1+|g|)^N{1+s\over\rho}.
\tag{6}
\]

Since \(\lambda_{\min}(e^{B(g)})=e^{\inf\sigma B(g)}\), (3) yields the decisive cancellation

\[
\begin{split}
\|e^{-B(g)/2}E_xe^{-B(g)/2}\|
&\le {C\over L}e^{(D+\delta)|g|}(1+|g|)^N{1+s\over\rho}\\
&\le {C'\over L}(1+s)^{N+1}
e^{-[1-c(D+\delta)]s}.
\end{split}
\tag{7}
\]

The last expression has a finite supremum on \(s\ge0\). Choosing \(L\) so that it is at most \(\varepsilon\) proves

\[
(1-\varepsilon)p_L(x)e^{B(g)}
\preceq M_B(x)\preceq
(1+\varepsilon)p_L(x)e^{B(g)}.
\tag{8}
\]

The upper bound is norm integrable because \(\|B(g)\|\le\sqrt mD|g|/2\), whereas \(V_L(x)/|x|\to\infty\). Fourier evaluation at zero then proves normalization. Scalar shifts satisfy \(M_A(x)=M_B(x-a)\); the scalar regularizer is unchanged. In (8), the corresponding centered comparison for \(A\) is evaluated at \(x-a\), not incorrectly at \(x\).

Every directional characteristic function is therefore \(\widehat p_L(tu)e^{itA(u)}\), which is exactly the spectral measurement of \(A(u)\) plus independent scalar noise \(u\cdot Z\).

## 4. Sharpness for the width-bounded class

Choose \(A_1=R\sigma_z\), \(A_2=R\sigma_x\), \(R=D/2\), and zero remaining coordinates. This tuple has maximal directional spectral width \(D\).

Let \(M\) be any positive normalized regularization with radial noise carrying every exponential moment. Its exponential moments are genuine. To see this directly, let \(\chi_r\) be smooth compact cutoffs increasing to one. For each real \(g\), the functions

\[
h_r(y)=\int e^{g\cdot(y+z)}\chi_r(y+z)p(z)\,dz
\]

converge in every fixed finite \(C^N\) seminorm near the compact support of \(W_A\) to \(m_p(g)e^{g\cdot y}\). Differentiating the cutoff contributes vanishing powers of \(r^{-1}\), and the remaining tail is dominated by the finite exponential moment of \(p\). Continuity of the distribution proves
\(\int e^{g\cdot x}\chi_r(x)M(dx)\to m_p(g)e^{A(g)}\) in norm. Scalar monotone convergence for the positive matrix measure identifies the limit with its genuine exponential moment. This is the compact-distribution cutoff operation of PR94, Section 3, specialized and spelled out here.

At tilt \((s,0)\), conjugating the tilted moment operators by \(e^{-sA_1/2}\) and taking the first/second-moment Schur complement gives

\[
\kappa_{22}(s,0)I+K_2(s)-K_1(s)^2\succeq0,
\quad
K_j=e^{-sA_1/2}\left.\partial_t^j e^{sA_1+tA_2}\right|_{t=0}e^{-sA_1/2}.
\]

The two-by-two exponential formula gives

\[
K_2-K_1^2=\operatorname{diag}(-d_R(s),d_R(s)),\quad
d_R(s)={\sinh(2Rs)-2Rs\over2s^2}.
\]

For radial noise, \(K(s)=\log\mathbb E e^{sZ_1}\) satisfies \(\kappa_{22}(s,0)=K'(s)/s\). Hence

\[
K'(s)\ge {\sinh(Ds)-Ds\over2s},\qquad
\liminf_{s\to\infty}{\log K(s)\over s}\ge D.
\tag{9}
\]

If instead \(p(z)\le C e^{-c_0|z|\log|z|}\) outside a fixed ball with \(c_0>1/D\), choose \(1/D<c'<c_0\). The elementary optimization

\[
\sup_{r>0}(sr-c'r\log r)=c'e^{s/c'-1}
\]

and integration of the remaining \(e^{-(c_0-c')r\log r}\) factor give \(K(s)\le C_1+C_2e^{s/c'}\). Its growth rate is smaller than \(D\), contradicting (9). This proves the sharp class supremum.

## Consequence and limits

For \(A_j=a_j I+B_j\), the noise cost depends on the non-scalar spectral spread, while \(a_j\) merely translates reported outputs. A large known or unknown scalar background cannot worsen this existence bound. For example, \(A_1=10^6I+\sigma_z\), \(A_2=\sigma_x\) permits every \(c<1/2\); substituting its uncentered absolute norm into the original sufficient formula would give only about \(5\times10^{-7}\).

An invertible real change of coordinates can similarly be applied to the tuple, then undone on the outputs; radial noise in the transformed coordinates becomes ellipsoidal noise in the original coordinates. This is ordinary affine transport, not a new quantum information resource.

The existence of \(L_0\) still contains derivative/cutoff constants and does not compile a measurement. The tail coefficient is sharp over the width-bounded class, not for every fixed tuple. The known support theorem supplies the geometric input; the relative-tail estimate supplies the new conditional transfer. Its historical priority has not been cleared.
