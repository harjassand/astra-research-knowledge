# P1 completed return

Chat: https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2
Prompt: work/astra-renewed-pro-programmes-20261103/P1_FULL_ORIGINAL_QUARTIC_OPERATOR_REPRESENTATION_CONTINUATION_PRO_20261110.txt
Turn: 49460ba6-4e23-429c-8675-d4ef5bd3f483; response: bce9eb21-912e-5a9b-baa9-2b85a8368bb5.
Native response was returned in full without a truncation marker; serialization is native Markdown, not literal UI-byte identity. The original updated ZIP is supplied separately unchanged.

# Complete native response

**I have not resolved the full assertion for every \(k>1/3\). This continuation does prove the original inequality for every sufficiently large \(k\), with no restrictions on the affine mean or compatible gradient.** It also determines the sharp asymptotic value of the best universal relative reserve.

The two conclusions are
\[
\boxed{
\int_{\mathbb T^2}J_k(A+D\phi)\,dx-J_k(A)
\ge \frac19\int_{\mathbb T^2}J_k(D\phi)\,dx
\qquad(k\ge K_*),
}
\tag{1}
\]
for a finite constant \(K_*\) specified below, and
\[
\boxed{
\lim_{k\to\infty}
\inf_{\substack{A\in\mathbb R^{2\times2}\\
G=D\phi\ne0}}
\frac{\int_{\mathbb T^2}J_k(A+G)-J_k(A)}
{\int_{\mathbb T^2}J_k(G)}
=\frac13.
}
\tag{2}
\]

These concern the **original \(J_k\)**. The large-\(k\) result includes arbitrary amplitudes, frequencies, concentration and determinant fluctuations.

The complete proof, exact algebraic verifier and independent review are saved in the updated packet:

- :chatgpt-content-reference{index="3"}[LARGE_K_GLOBAL_QUASICONVEXITY.md](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/sharp_operator_continuation/LARGE_K_GLOBAL_QUASICONVEXITY.md)
- :chatgpt-content-reference{index="4"}[LARGE_PARAMETER_CONTINUATION_RESULTS.txt](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/LARGE_PARAMETER_CONTINUATION_RESULTS.txt)
- [:chatgpt-content-reference{index="2"}](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal)

## 1. Precise threshold and the new estimate

Let \(C_0\ge1\) be a finite universal constant in the established scalar interpolation inequality
\[
\|\partial_1 f\|_{8/3}^{\,2}
\le C_0\|\nabla f\|_4\|R_1\partial_1f\|_2
\tag{3}
\]
on the original unit torus. The proof file defines \(C_0\) precisely as the maximum of \(1\) and the corresponding supremum over smooth periodic scalar potentials with nonzero denominator. Its finiteness is supplied by the accepted interpolation theorem; no numerical optimization of this supremum is used.

Set
\[
D_0=\sqrt{13}\,(41+12C_0),
\qquad
K_*=780(41+12C_0)^2.
\tag{4}
\]
Then (1) holds for every real \(k\ge K_*\).

Thus the threshold is analytically finite and explicit in the established interpolation constant. **I have not certified a numerical value of \(C_0\), so I am not asserting an independent decimal cutoff for \(K_*\).**

The main new step is a parameter-uniform estimate for the signed minor term. After the normalization
\[
\varepsilon=k^{-1/2},
\qquad
f_\varepsilon(F)=J_k\!\left(F\operatorname{diag}(\varepsilon,1)\right),
\tag{5}
\]
write, for a compatible mean-zero \(G\),
\[
\begin{aligned}
c&=\int f_\varepsilon(G),&
b&=\int Df_\varepsilon(G),\\
H[F,F]&=\int D^2f_\varepsilon(F)[G,G],&
r&=\int D\lambda_\varepsilon(G)\det G.
\end{aligned}
\]
The estimate is
\[
\boxed{
|r:F|
\le D_0\varepsilon
\|G\|_4\|\det G\|_2^{1/2}
\sqrt{H[F,F]}
\qquad(0<\varepsilon\le1/16).
}
\tag{6}
\]
It holds for every constant real \(F\). In particular,
\[
r^TH^\dagger r
\le D_0^2\varepsilon^2
\|G\|_4^2\|\det G\|_2.
\tag{7}
\]

The factor \(\varepsilon\) is what makes the signed minor affordable for large \(k\). Establishing that factor uniformly requires resolving the acoustic degeneration at the parameter endpoint.

## 2. Normalize the density, retaining the original signed minor

Direct substitution into the original formula gives
\[
f_\varepsilon(F)
=
\frac{3-\varepsilon^2}{8(1+\varepsilon^2)}
(u-v+2\varepsilon j)^2
+\frac{3-\varepsilon^2}{4}uv+\varepsilon^2j^2,
\tag{8}
\]
where \(u,v,j\) now refer to \(F\).

The translated-Hessian multiplier becomes
\[
\lambda_\varepsilon(F)
=
\frac{3(3-\varepsilon^2)\varepsilon}
{2(3+\varepsilon^2)}(u-v)
+\frac{12\varepsilon^2}{3+\varepsilon^2}j.
\tag{9}
\]

For \(0<\varepsilon\le1\), minimizing the first and third terms of (8) over the scalar \(j\) gives
\[
\begin{aligned}
f_\varepsilon(F)
&\ge
\frac{3-\varepsilon^2}{4(5+\varepsilon^2)}
\bigl[u^2+v^2+(3+\varepsilon^2)uv\bigr]\\
&\ge \frac1{12}|F|^4.
\end{aligned}
\tag{10}
\]
Also,
\[
|\lambda_\varepsilon(F)|
\le \frac72\varepsilon|F|^2,
\qquad
|D\lambda_\varepsilon(G):E|
\le7\varepsilon|G||E|.
\tag{11}
\]

Consequently, with
\[
M=\|G\|_4,\qquad d=\|\det G\|_2,
\]
we have
\[
c\ge \frac{M^4}{12},
\qquad
d\le\frac{M^2}{2},
\qquad
M^2d\le6c.
\tag{12}
\]

Although \(f_\varepsilon\) converges coefficientwise to the convex quartic
\[
\frac38(u^2+v^2),
\]
that observation alone does not establish a uniform all-mean inequality. The next two steps control the degenerating directions directly.

## 3. Uniform control of every acoustic background

A constant left rotation, scalar normalization of the longer column, and, when necessary, an actual permutation of the source coordinates reduce a nonzero background to
\[
F=\begin{pmatrix}1&s\\0&h\end{pmatrix},
\qquad s^2+h^2\le1.
\]
Put
\[
F_\varepsilon=\operatorname{diag}(1,\varepsilon),
\qquad
\rho=h-\varepsilon,
\qquad
d_F^2=s^2+\rho^2.
\]

The resulting uniform acoustic comparison is
\[
\boxed{
D^2f_\varepsilon(F)[e\otimes\xi,e\otimes\xi]
\ge
\frac1{104}\left(
D^2f_\varepsilon(F_\varepsilon)[e\otimes\xi,e\otimes\xi]
+d_F^2|\xi|^2|e|^2
\right)
}
\tag{13}
\]
for \(0<\varepsilon\le1/16\).

Here is the algebra behind the constant. For \(e=(z_1,z_2)\), \(\xi=(p,q)\), define
\[
\begin{aligned}
D&=-\rho z_1+sz_2,
&
E&=sz_1+\rho z_2,\\
T&=(3+\varepsilon^2)pz_1+2\varepsilon qz_2,
&
V&=(1+\varepsilon^2)pz_2,
\end{aligned}
\]
and
\[
\alpha=\frac{2\varepsilon}{3+\varepsilon^2},
\qquad
\beta=1+\frac6{3+\varepsilon^2}.
\]
Set
\[
\widetilde T=T-\beta\varepsilon pD,
\qquad
C=qE+\alpha pD,
\qquad
\widetilde V=V+\varepsilon pE,
\]
together with
\[
\gamma=\frac{3-\varepsilon^2}{2(1+\varepsilon^2)},
\qquad
\delta=\frac{2\varepsilon^2}{3+\varepsilon^2}.
\]

The exact identity is
\[
\begin{aligned}
D^2f_\varepsilon(F)[e\otimes\xi,e\otimes\xi]
={}&\frac12\widetilde T^2+3\gamma C^2\\
&+\gamma\bigl[(qD)^2+\widetilde V^2
                 +2\delta(qD)\widetilde V\bigr].
\end{aligned}
\tag{14}
\]

For \(\varepsilon\le1\), \(\gamma\ge1/2\) and \(\delta\le1/2\). Thus (14) is at least one quarter of
\[
|\mathcal M|^2
=\widetilde T^2+\widetilde V^2+C^2+(qD)^2.
\]
Compare this with
\[
|\mathcal N|^2
=T^2+V^2+(qE)^2+(qD)^2.
\]
The explicit perturbation satisfies
\[
|\mathcal M-\mathcal N|^2
\le10\varepsilon^2d_F^2p^2|e|^2
\le40\varepsilon^2|\mathcal N|^2.
\tag{15}
\]
For \(\varepsilon\le1/16\), this yields
\[
D^2f_\varepsilon(F)[e\otimes\xi,e\otimes\xi]
\ge\frac1{16}|\mathcal N|^2.
\]
Meanwhile,
\[
D^2f_\varepsilon(F_\varepsilon)[e\otimes\xi,e\otimes\xi]
+d_F^2|\xi|^2|e|^2
\le\frac{13}{2}|\mathcal N|^2.
\]
Combining these proves (13).

Summing over the actual Fourier frequencies of a compatible gradient gives
\[
H[F,F]\ge
\frac1{104}\left(
H[F_\varepsilon,F_\varepsilon]+d_F^2\|G\|_2^2
\right).
\tag{16}
\]
No minimum angular separation or lower bound on the second moment is assumed.

The source permutation also respects the signed minor. If \(P\) swaps the columns, then
\[
f_\varepsilon(FP)=f_\varepsilon(F),
\qquad
\lambda_\varepsilon(FP)=-\lambda_\varepsilon(F).
\]
The determinant changes sign as well, so the two signs cancel in the relevant pairing. The simultaneous coordinate permutation preserves the original torus exactly.

## 4. Pay the critical mixed-minor term using compatibility

Write
\[
G=\begin{pmatrix}a&b_1\\c_1&d_1\end{pmatrix},
\]
and set
\[
A_\varepsilon=\frac{3+\varepsilon^2}{2},
\qquad
B_\varepsilon=\frac{(3-\varepsilon^2)(1+\varepsilon^2)}4,
\qquad
s_\varepsilon=A_\varepsilon a+\varepsilon d_1.
\]
At the critical background,
\[
q_\varepsilon
:=\int(s_\varepsilon^2+B_\varepsilon c_1^2)
=\frac12H[F_\varepsilon,F_\varepsilon].
\tag{17}
\]

Differentiating (9) gives the exact expression
\[
r:F_\varepsilon
=\varepsilon\left[
C_1\int s_\varepsilon j+C_2\int aj
\right],
\tag{18}
\]
where
\[
C_1=\frac{3(1+\varepsilon^2)}{3+\varepsilon^2}\le\frac32,
\qquad
C_2=
\frac{3(1+\varepsilon^2)(3-\varepsilon^2)}
{2(3+\varepsilon^2)}
\le2.
\]

The first integral in (18) is directly bounded by \(d\sqrt{q_\varepsilon}\). The second needs compatibility.

At frequency \((p,q)\), the second row satisfies
\[
q\,\widehat c_1=p\,\widehat d_1.
\]
Minimizing the quadratic expression in (17) over the second-row coefficient gives
\[
q_\varepsilon
\ge\frac{27}{16}\|R_{1,\varepsilon}a\|_2^2,
\qquad
R_{1,\varepsilon}(p,q)
=\frac{p}{\sqrt{p^2+\varepsilon^2q^2}}.
\tag{19}
\]

The scalar interpolation estimate has the anisotropic version
\[
\|a\|_{8/3}^{\,2}
\le C_0\|(a,\varepsilon b_1)\|_4
       \|R_{1,\varepsilon}a\|_2.
\tag{20}
\]
For rational \(\varepsilon=P/Q>0\), this follows by applying (3) to
\[
f(Qx,Py).
\]
The integer covering preserves normalized torus norms. Both derivative factors acquire \(Q\), which cancels. For irrational \(\varepsilon\), first pass through rational parameters on a finite Fourier potential and then use strong Sobolev approximation. The constant remains \(C_0\).

The other operator input is the supplied \(L^4\) Beurling bound. It gives
\[
\left\|
\frac{tpq}{p^2+t^2q^2}
\right\|_{L^4\to L^4}\le\frac32,
\tag{21}
\]
after the same integer-covering transfer. The external input here is the established Beurling estimate; the anisotropic transfer is part of this proof. :chatgpt-content-reference{index="0"}

Now choose \(0<\delta\le1\) and split
\[
a=a_L+a_H,
\qquad
\widehat a_L
=\frac{\delta^2\varepsilon^2q^2}
{p^2+\delta^2\varepsilon^2q^2}\widehat a.
\]
First-row compatibility gives the exact identity
\[
a_L=\delta\varepsilon M_{\delta\varepsilon}b_1,
\]
where \(M_t\) is the multiplier in (21). Hence
\[
\|a_L\|_4\le\frac32\delta\varepsilon M,
\qquad
\|a_H\|_2\le\delta^{-1}\sqrt{q_\varepsilon}.
\tag{22}
\]

Use
\[
j=\frac{a s_\varepsilon-A_\varepsilon a^2}{\varepsilon}
-b_1c_1.
\tag{23}
\]
Hölder and (20) give
\[
\left|\int a_Lj\right|
\le(5+3C_0)\delta M^2\sqrt{q_\varepsilon},
\]
where the factor \(\varepsilon\) in (22) cancels the apparent \(1/\varepsilon\) loss in (23). The high part satisfies
\[
\left|\int a_Hj\right|
\le\delta^{-1}d\sqrt{q_\varepsilon}.
\]
If \(d>0\), choose
\[
\delta=\frac{\sqrt d}{M}\le\frac1{\sqrt2}.
\]
If \(d=0\), the mixed term is zero. Therefore
\[
\left|\int aj\right|
\le(6+3C_0)M\sqrt d\,\sqrt{q_\varepsilon}.
\tag{24}
\]

Equations (18)–(24) prove
\[
|r:F_\varepsilon|
\le
\frac{27/2+6C_0}{\sqrt2}\,
\varepsilon M\sqrt d
\sqrt{H[F_\varepsilon,F_\varepsilon]}.
\tag{25}
\]

For a general normalized background, (11) gives
\[
|r:(F-F_\varepsilon)|
\le7\varepsilon d_F\|G\|_2d.
\]
Combining this with (16), (25), and
\[
d\le\frac{M\sqrt d}{\sqrt2}
\]
produces precisely
\[
|r:F|
\le\sqrt{13}(41+12C_0)
\varepsilon M\sqrt d\sqrt{H[F,F]}.
\]
Undoing the constant rotation, scalar normalization and source permutation proves (6) for every background.

This is the step that supplies uniformity in frequency and concentration. The determinant is controlled through the differential relations between the entries of \(G\).

## 5. Use the strain reserve once

The accepted strain identities transform algebraically under the right scaling. With \(T=\operatorname{diag}(\varepsilon,1)\), take
\[
S_\varepsilon(F,G)=S_k(FT,GT),
\qquad
\lambda_\varepsilon(F)=\det(T)\lambda_k(FT).
\]
This does not assume that \(GT\) is compatible on the original torus.

For the normalized density, the identities are
\[
H=K_G^*K_G,
\qquad
3b=K_G^*g+r,
\qquad
\|g\|_2^2=12c-2q,
\]
where
\[
q=\int\lambda_\varepsilon(G)\det G.
\]

Estimate (6) first implies \(r\in\operatorname{range}H\), and then (7). Thus
\[
z=g+K_GH^\dagger r
\]
is a feasible lift:
\[
K_G^*z=3b.
\]
Weighted Young gives
\[
\begin{aligned}
\|z\|_2^2
&\le\frac54\|g\|_2^2+5r^TH^\dagger r\\
&\le15c+
\left(\frac{35}{4}\varepsilon
      +5D_0^2\varepsilon^2\right)M^2d\\
&\le
\left(
15+\frac{105}{2}\varepsilon
+30D_0^2\varepsilon^2
\right)c.
\end{aligned}
\tag{26}
\]

If
\[
\varepsilon\le
\min\left\{\frac1{105},\frac1{\sqrt{60}D_0}\right\},
\]
the bracket is at most \(16\). The choice (4) guarantees these inequalities and \(\varepsilon\le1/16\).

The least-norm lift therefore satisfies
\[
9b^TH^\dagger b\le\|z\|_2^2\le16c.
\]
Using the exact all-mean polarization,
\[
\inf_A\left[\int f_\varepsilon(A+G)-f_\varepsilon(A)\right]
=c-\frac12b^TH^\dagger b
\ge\frac19c.
\tag{27}
\]

This proves the normalized inequality for all means, including singular integrated Hessians. The convex companion’s reserve has not been spent a second time.

## 6. Return to the original density and original torus

This passage is necessary because the right scaling in (5) does not itself preserve periodic gradient compatibility.

First obtain the compact-support inequality for \(f_\varepsilon\): extend a compactly supported potential by zero to a containing square, periodize, and rescale the square to the unit torus while scaling the potential so that its gradient values are unchanged.

For an original compactly supported potential \(\phi\), put
\[
T=\operatorname{diag}(\varepsilon,1),
\qquad
\psi(y)=\phi(T^{-1}y),
\qquad
B=AT^{-1}.
\]
Then
\[
(B+D_y\psi(y))T=A+D_x\phi(T^{-1}y),
\]
and consequently
\[
\begin{aligned}
f_\varepsilon(B+D\psi(y))
&=J_k(A+D\phi(T^{-1}y)),\\
f_\varepsilon(D\psi(y))
&=J_k(D\phi(T^{-1}y)).
\end{aligned}
\]
The common Jacobian factor \(\det T\) cancels from the two sides.

To recover periodic tests, cut off a smooth periodic potential on a square of integer side length \(N\), with a boundary layer of fixed width. The layer contributes \(O(N)\), while the interior contributes \(N^2\) times the torus integral up to \(O(N)\). Dividing by \(N^2\) and letting \(N\to\infty\) gives the original periodic inequality.

Finally, strong periodic \(W^{1,4}\) approximation pays the quartic-energy limit. The intermediate mixed estimate passes through strong \(L^4\) convergence of gradients, \(L^2\) convergence of determinants, and convergence of the quadratic and cubic moments. It passes first as an inequality for each fixed \(F\); **no continuity of \(H^\dagger\) is assumed.**

This completes (1) for the original \(J_k\), on the stated unit torus, for every real \(k\ge K_*\).

## 7. The asymptotic reserve is exactly \(1/3\)

Define
\[
\mathcal R(k)=
\inf_{\substack{A\\G=D\phi\ne0}}
\frac{\int J_k(A+G)-J_k(A)}{\int J_k(G)}.
\]

Before applying Young in (26), the triangle inequality gives
\[
\frac{\|z\|_2}{\sqrt c}
\le
\sqrt{12+42\varepsilon}+\sqrt6D_0\varepsilon.
\]
Therefore
\[
\boxed{
\mathcal R(k)\ge
1-\frac1{18}
\left[
\sqrt{12+\frac{42}{\sqrt k}}
+\frac{\sqrt6D_0}{\sqrt k}
\right]^2,
\qquad k\ge256.
}
\tag{28}
\]
Its right-hand side tends to \(1/3\).

For the matching upper bound, fix a nonzero rank-one matrix \(E=a\otimes e_1\). For \(0<p<1\), let
\[
g_p(x_1)=
\begin{cases}
1,&0<x_1<p,\\[2mm]
-\dfrac p{1-p},&p<x_1<1.
\end{cases}
\]
It has mean zero. Its periodic antiderivative gives an actual \(W^{1,\infty}\) vector potential with gradient
\[
G_p=E\,g_p(x_1).
\]

Writing \(m_i=\int g_p^i\), the admissible means \(A=\alpha E\) give
\[
\frac{\Delta_{G_p}(\alpha E)}{J_k(E)}
=m_4+4\alpha m_3+6\alpha^2m_2.
\]
The minimizing scalar is
\[
\alpha=-\frac{m_3}{3m_2},
\]
so exact integration yields
\[
\frac{\min_\alpha\Delta_{G_p}(\alpha E)}
{\int J_k(G_p)}
=
1-\frac23
\frac{(1-2p)^2}{1-3p+3p^2}
\longrightarrow\frac13
\qquad(p\downarrow0).
\tag{29}
\]
Hence \(\mathcal R(k)\le1/3\) for every \(k>1/3\). Combining (28) and (29) proves (2).

The conclusion is an asymptotic equality. It does not reinstate the already disproved exact \(c_G/3\) reserve at finite parameters.

## 8. Other completed work and actual finite costs

The construction branch tested **48 actual compatible periodic ridge-composition potentials** at
\[
k\in\left\{\frac{17}{50},\frac12,1,2\right\}.
\]
All 48 have determinant fluctuations.

| Calculation | Completed work | Rigorous outcome |
|---|---:|---|
| Initial composition search | 3,019 polygons; 9,316 band tests; 192 floating mean calculations with 17,280 bisections; 192 exact original-gap checks | No negative witness; measured runtime \(1.8002\) seconds |
| Independent affine-mean post-processing | 192 exact rational \(4\times4\) systems | Every Hessian positive definite and every optimized original gap strictly positive; runtime \(4.5444\) seconds |
| Acoustic identity verification | Seven fixed rational-polynomial identities | Every numerator exactly zero; internal runtime \(1.8194\) seconds under a 30-second cap |

For the fixed construction fields and four tested parameters, the exact mean calculation covers **every affine mean**, and homogeneity additionally covers every real scalar amplitude. It does not cover arbitrary fields or an interval of parameters. Definitions, exact moments, minimizing means and receipts are retained in :chatgpt-content-reference{index="5"}[INDEPENDENT_MEAN_POSTPROCESS.md](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/construction_sharp_continuation/INDEPENDENT_MEAN_POSTPROCESS.md) and the accompanying packet files.

The analytic theorem uses no numerical positivity inference. Its verifier checks the factorization against a direct Hessian contraction of the original normalized density. I reviewed the uniform estimates and source transfer, and the construction principal independently checked the factorization, constants and return to \(J_k\). The :chatgpt-content-reference{index="6"}[independent review](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/sharp_operator_continuation/CONSTRUCTION_INDEPENDENT_LARGE_K_REVIEW.md) records the scope and details.

The projection branch also completed a finite quasiconvex block using **both row potentials**. For \(K=K_1\times K_2\), separable convex \(g\), and \(c_0\in\mathbb R\), set
\[
E(F)=\sup_{Z\in\partial K}
\bigl[c_0\det Z+Dg(Z):(F-Z)\bigr],
\]
and use \(E\) outside \(K\), with \(\max(E,c_0\det)\) inside. Independent compatible scalar projections pay both work terms; product contact and
\[
\int\det Dw=\det A
\]
pay the determinant pairing. This gives a globally Lipschitz quasiconvex function. The complete result is in :chatgpt-content-reference{index="7"}[TWO_ROW_PRODUCT_PROJECTION_BLOCK.md](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/projection_sharp_continuation/TWO_ROW_PRODUCT_PROJECTION_BLOCK.md).

No touching minorant or representation of \(J_k\) has been obtained from that block.

## 9. What remains unresolved

For
\[
\boxed{\frac13<k<K_*}
\]
I still have neither the required universal affirmative nor an admissible compatible negative.

The unresolved assertion remains
\[
b_G^TH_G^\dagger b_G\le2c_G
\qquad\text{for every compatible }G.
\]

The large-\(k\) theorem does not propagate through the remaining interval merely by continuity. For fixed tests the gap depends continuously on \(k\), so the quasiconvex parameter set is relatively closed; the optimized reserve is an infimum of continuous test quotients and is upper semicontinuous. Those facts allow the reserve to reach zero at an intermediate parameter. The previously proved parameter rigidity also prevents a finite positive transformed-family decomposition from extending the result.

**The established advance is therefore a full original-density theorem on a large-parameter interval, together with the exact limit \(\mathcal R(k)\to1/3\). The full all-\(k\) question remains unresolved by this work.**

# Available visible activity excerpts

The expanded current activity was visible on screen; the accessibility history was limited to the first 500 items and did not expose this current activity. The following passages were transcribed from the visible screen and are not a complete activity capture. No private reasoning was requested or recovered.

> I’ll pursue the full endpoint from the new operator representation and the unrestricted compatible-field formulation. I’ll focus on whether the mixed terms admit a sharp integral estimate, or whether they lead to an actual compatible counterexample. The completed classifications and exclusions will remain accepted at their stated scopes.

> The composition search has produced no negative witness within its declared budget. Its stored potentials are now being checked with an independent affine mean using exact rational systems. On the analytic side, projecting both row potentials onto separate convex gradient constraints gives a valid quasiconvex block: both the projection work and determinant pairing are paid. The next question is whether those blocks can support the original quartic at every mean.

> The exact check of all 48 new composition fields found positive gaps at the four tested parameters, including after optimizing the affine mean. A more promising analytic result is under review: a proposed proof for all compatible gradients and all sufficiently large k. I’m checking the uniform constants and the transfer back to the original torus; even if it holds, the remaining parameter range still needs a proof or counterexample.

> The torus transfer also checks out. Rational anisotropic multipliers can be handled by integer coverings of the original torus; finite Fourier approximation then gives the result for real scaling factors. Thus the large-k proof does not need to identify an irrationally rescaled lattice with Z². The remaining issue is the smaller-k range, where the signed minor term is no longer small enough for this estimate.

> I’m preparing the complete large-k proof and its verification record. The threshold will be stated in terms of the established scalar interpolation constant; I won’t substitute an unverified numerical value. A separate review is checking the acoustic factorization directly against the original density, while the other analytic work continues to look for a way through the remaining parameter range.

> The remaining projection branch has no touching minorant or representation for J_k. It does have a proved quasiconvex block built by projecting both row potentials onto separate convex gradient constraints. I’m retaining that result at its stated scope. The conclusions about the original density from this continuation are the large-k theorem and the sharp limiting reserve; the full smaller-k question remains open here.
