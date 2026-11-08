# P1 Xi completed return

Source: https://chatgpt.com/c/6af0b593-f530-83ec-a894-70d5375a14b0
Model: normal-web GPT-6 standard, Extra High. Turn: 6bf12d3b-b531-4ec8-9e13-296604c380a8. Response: d5eda5fb-453d-4014-96ac-405704972292. Completed: 2026-11-08T18:06:14.942Z.
ZIP: none supplied in the visible return.

## Actual prompt

Resolve the FULL deterministic-stirring regularization problem below. You own all ideas, methods, representations and source order and may challenge the framing.

Work on the unit three-dimensional torus. Input is ANY explicit finite rational polynomial vector field F=(F_1,...,F_s), positive rational molecular diffusivities kappa_i, a positive rational reference c*, and rational K>=1, chi>0. Assume only:
(1) quasi-positivity: F_i(z)>=0 whenever z>=0 and z_i=0;
(2) Boltzmann-entropy dissipation: sum_i F_i(z)*log(z_i/c_i*)<=0 for EVERY z in (0,infinity)^s.
There is no degree bound, common diffusion coefficient, near-equilibrium assumption, boundary-equilibrium exclusion or lower bound on the initial species densities.

Construct ONE uniform deterministic finite algorithm which, from this data alone, outputs a smooth TIME-INDEPENDENT divergence-free velocity b(x) on T^3 with a FINITE rational trigonometric description, and finite computable constants C,A. For EVERY smooth nonnegative initial profile 0<=u_0,i<=K, the SAME b must make
    partial_t u_i + b dot grad u_i = kappa_i*Delta u_i + F_i(u)
have a unique global nonnegative classical solution satisfying
    sup_{t>=0} max_i ||u_i(t)||_infinity <= C,
    ||u(t)-bar u(t)||_{L2(T^3;R^s)}
       <= A*exp(-chi*t)*||u_0-bar u_0||_L2  for ALL t>=0,
where bar u(t)=integral_T3 u(t,x) dx. This is spatial homogenization; no unproved shadowing by a homogeneous ODE or equilibrium convergence is assumed.

Give finite computable bounds, in the supplied data, for controller construction/description, amplitude, spatial frequencies, ||b||_{W1,infinity}, numerical precision and C,A. No polynomial efficiency is presumed, but no free mixing-time/semigroup/PDE-solution oracle, uncertified numerical mixing, sampled Brownian path, time-varying feedback, increased molecular diffusivity or infinite-mode/limiting controller. One field must work uniformly over the whole stated initial-data class, not a separately chosen path for each profile. Physical actuation/continuing service is a separate cost, not a free-energy or hardware claim.

Actually read scoped machinery:
* Iyer-Xu-Zlatos, Convection-Induced Singularity Suppression in the Keller-Segel and Other Non-linear PDEs, author full PDF https://www.math.cmu.edu/~gautam/sj/research/papers/201908-mixblowup.pdf : Definition1.1/Theorem1.3/Proposition4.2/Theorem5.5/Remark5.6/Examples5.7-5.8. Smooth steady cellular flows in dimensions2,3 have arbitrarily small linear dissipation times after amplitude AND cell-size rescaling. Proposition4.2 turns dissipation time into uniform mean-zero L1->Linfinity control. Its nonlinear Theorem1.2 assumes specific H1-H2 bounds and is not already a theorem for the arbitrary polynomial entropy class above. The3D effective-diffusivity/amplitude choices and all different kappa_i must actually be paid.
* Agresti-Kniely-Tang, arXiv:2608.13332v1, https://arxiv.org/html/2608.13332v1 : Theorems3.4-3.5 give high-probability global classical solutions and homogenization using finite-mode TRANSPORT NOISE for complex-balanced networks under their mass/no-boundary contracts. Proposition6.5 is deterministic HIGH-diffusivity machinery. Neither operation supplies the deterministic fixed controller requested here; an Ito correction or a favorable random path does not remove that gap.

Optional intuition: entropy gives an a priori mean bound; a uniformly short-time Linfinity restart and genuine linear smoothing may make it usable for nonlinear closure. Discard this suggestion and choose any route. Pursue FULL resolution persistently. A negative answer requires an actual counterexample to this uniform-controller statement, not failure of one flow or method.

you may use all subagents avaible
All inherited source/access/transfer holds apply to every subagent, including every unknown held identity. No retries, alternate versions/routes/mirrors, identifying recovery or held-source injection. Preserve ALL old programme holds, including Dots failed transfers, OpenAI Uniform-Permanence tree, Golding-Henderson/Serre/CarloAlberto and root2410.23225v3/TR26-272. No attachments, new model/worker/resource/account/spending, Sol or Dots action.

## Available user-visible activity

Worked for 17m 22s

I’ll examine the two specified papers first, then test whether their deterministic linear estimates can be closed for arbitrary entropy-dissipating polynomial reactions. I’ll track the dependence on every diffusivity and on the finite flow description. I’ll distinguish a complete construction from any conditional or partial theorem.

Refined bootstrap proof and established entropy-controlled decay

Constructed certificates and explicit bounds for effective homogenization and mixing

Summarized certificate construction

Searched 2 websites

Example 5.8 supplies a three-dimensional cellular flow that can be written with rational trigonometric coefficients. I’ve derived a finite Fourier certificate for its linear semigroup: it uses explicit high-frequency error bounds, rational approximations to 2π, and exact positive-definiteness tests. I’m checking the certificate’s completeness and the simultaneous choice for unequal diffusivities.

Constructed and certified the proof certificate

## Complete response

# Deterministic stirring regularization: constructive resolution

The entropy assumptions admit a global nonlinear closure using a sufficiently dissipative fixed flow. Crucially, this closure does **not** require complex balance, a positive lower bound on concentrations, a degree restriction, or control of the homogeneous reaction ODE beyond the entropy bound.

The construction has two parts\:

1. Establish a uniform \(L^\infty\) bound from entropy-controlled mass and a fixed-time smoothing estimate.
2. Construct and rigorously certify a single finite-mode, stationary, divergence-free flow whose linear dissipation is strong enough for both nonlinear closure and exponential homogenization.

The second part requires a certification algorithm, not merely an existence argument based on arbitrarily large effective diffusivity.

## 1\. The nonlinear estimate

Write

\[
h_i(z)=z\log(z/c_i^*)-z+c_i^*,
\qquad h_i(0)=c_i^*.
\]

The entropy is

\[
\mathcal H(u)=\int_{\mathbb T^3}\sum_{i=1}^s h_i(u_i(x))\,dx.
\]

Quasi-positivity preserves nonnegativity locally. The reaction entropy inequality, incompressibility and diffusion imply

\[
\mathcal H(u(t))\leq \mathcal H(u_0)
\]

throughout the interval of classical existence.

This assertion remains valid when species vanish. One can apply the entropy calculation to \(h_i(u_i+\varepsilon)\), use the assumed inequality at \(u+\varepsilon\mathbf1\), and then pass to \(\varepsilon\downarrow0\)\. On every bounded interval of classical existence, the reaction-approximation error is \(O(\varepsilon(1+|\log\varepsilon|))\)\.

Because \(\log r\leq r-1\),

\[
\mathcal H(u_0)\leq
E:=\sum_{i=1}^s\left(c_i^*+\frac{K^2}{c_i^*}\right).
\]

Also, for every \(z\geq0\),

\[
z\leq h_i(z)+8c_i^*.
\]

Consequently, every local nonnegative solution satisfies the uniform total-mass estimate

\[
\boxed{
\sum_{i=1}^s\int_{\mathbb T^3}u_i(t,x)\,dx
\leq M:=E+8\sum_{i=1}^s c_i^*.
}
\]

Here \(E\) and \(M\) are explicitly computable rational numbers.

Choose the proposed global concentration bound

\[
\boxed{C=8(K+M+1).}
\]

Let \(Q\) be any rational coefficient-based bound for \(\max_i|F_i(z)|\) on \([0,2C]^s\), and let \(L\) be a rational Lipschitz bound for \(F\) on \([0,C]^s\)\.

Choose a positive rational time \(T\) so that

\[
TQ\leq C/8,
\qquad
T^{-1}\geq\chi+2L.
\]

Suppose a fixed divergence-free flow has scalar advection–diffusion semigroups \(S_i(t)\), one for each \(\kappa_i\), satisfying

\[
\boxed{
\|S_i(T)P_0\|_{L^1\to L^\infty}\leq\frac14,
}
\]

where \(P_0f=f-\int_{\mathbb T^3}f\)\.

Then the nonlinear \(L^\infty\) bound follows.

Indeed, start any interval of length \(T\) with \(\max_i\|u_i\|_\infty\leq C/2\)\. The maximum principle and the reaction bound keep the solution below \(C\) throughout that interval. At its endpoint, Duhamel's formula and the mass estimate give

\[
\begin{aligned}
\|u_i(t+T)\|_\infty
&\leq \overline u_i(t)
+\frac14\|u_i(t)-\overline u_i(t)\|_1+TQ\\
&\leq M+\frac M2+\frac C8\\
&\leq\frac{5C}{16}<\frac C2.
\end{aligned}
\]

Since \(\|u_{0,i}\|_\infty\leq K<C/2\), induction yields

\[
\boxed{\sup_{t\geq0}\max_i\|u_i(t)\|_\infty\leq C.}
\]

The continuation criterion for semilinear parabolic systems then excludes finite-time blow-up.

This argument is uniform over every permitted initial profile. The remaining task is to produce one stationary rational-trigonometric velocity satisfying the required smoothing and contraction estimates for all diffusivities simultaneously.

## 2\. An explicit three-dimensional stationary controller

Define the trigonometric vector field

\[
B(x)=
\begin{pmatrix}
-\sin(2\pi x_1)\cos(2\pi x_2)\cos(2\pi x_3)\\
-\cos(2\pi x_1)\sin(2\pi x_2)\cos(2\pi x_3)\\
2\cos(2\pi x_1)\cos(2\pi x_2)\sin(2\pi x_3)
\end{pmatrix}.
\]

Direct differentiation gives

\[
\nabla\cdot B=0.
\]

Its Fourier coefficients are rational, its Fourier support is finite, and it satisfies the coordinate-reflection symmetries used by Iyer–Xu–Zlatoš.

Consider the two-integer controller family

\[
\boxed{b_{a,n}(x)=-anB(nx),\qquad a,n\in\mathbb N.}
\]

These are smooth, time-independent, divergence-free vector fields with rational trigonometric descriptions.

This is the normalized version of the three-dimensional cellular flow in Example 5.8 of Iyer–Xu–Zlatoš. Their example establishes that the minimum coordinate effective diffusivity of \(aB\) diverges as \(a\to\infty\), and their Theorem 5.5 relates effective diffusivity and cell size to the finite-time \(L^2\) contraction. citeturn735465view0citeturn895315view1

### Simultaneous contraction for unequal diffusivities

Let \(S_{\kappa,b}(t)\) denote the scalar semigroup generated by

\[
\kappa\Delta-b\cdot\nabla.
\]

The key existence statement is\:

**Lemma.** For every finite collection \(\kappa_1,\ldots,\kappa_s>0\), every \(t_*>0\), and every \(q_*>0\), there are positive integers \(a,n\) such that

\[
\max_{1\leq i\leq s}
\|S_{\kappa_i,b_{a,n}}(t_*)P_0\|_{2\to2}<q_*.
\]

**Proof.** Divide the equation for species \(i\) by \(\kappa_i\) in time. The unit-diffusivity drift becomes

\[
-\frac{an}{\kappa_i}B(nx).
\]

Set

\[
D_i(a)=\min_{j=1,2,3}D_{e_j}\!\left(\frac a{\kappa_i}B\right).
\]

Example 5.8 gives

\[
D_i(a)\longrightarrow\infty
\qquad(a\to\infty)
\]

for every fixed \(\kappa_i>0\)\.

For sufficiently large \(a\), use the parameters

\[
\alpha_i=D_i(a)^{-1/4},
\qquad
\mu_i=\left\lfloor D_i(a)^{1/48}\right\rfloor.
\]

The contraction factor in Theorem 5.5 is then bounded by a constant times \(D_i(a)^{-1/16}\), which tends to zero.

Choose \(n\) to be a sufficiently large common multiple of the finitely many \(\mu_i\)\. In the time threshold (5.12), the first term tends, as \(n\to\infty\) with \(a\) fixed, to

\[
\frac1{4\alpha_i^2D_i(a)}
=\frac1{4\sqrt{D_i(a)}}.
\]

The second term tends to zero with \(n\), while the remaining term is bounded asymptotically by

\[
O\left(\frac{\log D_i(a)}{D_i(a)^{1/48}}\right).
\]

Thus the required contraction can occur before physical time \(t_*\kappa_i\), simultaneously for all finitely many diffusivities.

This proves the lemma. \(\square\)

Notice that this argument does not claim that amplitude rescaling alone suffices. Both \(a\) and \(n\) are essential.

## 3\. Contraction implies the required smoothing and homogenization

We now make the linear targets explicit.

For every incompressible drift, the scalar semigroup satisfies the drift-independent estimate

\[
\boxed{
\|S_{\kappa,b}(r)\|_{1\to2},
\quad
\|S_{\kappa,b}(r)\|_{2\to\infty}
\leq25\left(1+\frac1{\kappa r}\right).
}
\tag{3.1}
\]

Here is an elementary justification of the constant.

For \(v=S_{\kappa,b}(r)f\), set

\[
Y(r)=\frac{\|v(r)\|_2^2}{\|f\|_1^2}.
\]

Fourier splitting on the unit torus shows that whenever \(Y\geq432\),

\[
\|\nabla v\|_2^2
\geq\frac14\|f\|_1^2Y^{5/3}.
\]

Because incompressible advection cancels from the \(L^2\) energy identity,

\[
Y'\leq-\frac\kappa2Y^{5/3}.
\]

Integrating gives

\[
Y(r)\leq
\max\left\{432,\left(\frac3{\kappa r}\right)^{3/2}\right\}.
\]

This yields the first estimate in (3.1). The second follows by duality, since the adjoint has drift \(-b\)\.

Define the computable rational quantities

\[
H_i=25\left(1+\frac4{\kappa_iT}\right),
\qquad
q=\min\left\{\frac14,\frac1{4\max_iH_i^2}\right\}.
\]

It now suffices to find \(b\) such that

\[
\boxed{
\|S_{\kappa_i,b}(T/2)P_0\|_{2\to2}\leq q
\quad\text{for every }i.
}
\tag{3.2}
\]

Indeed, split time \(T\) into \(T/4,T/2,T/4\)\. Estimate (3.1) and (3.2) give

\[
\|S_{\kappa_i,b}(T)P_0\|_{1\to\infty}
\leq H_i^2q\leq\frac14.
\]

Thus Section 1 proves global existence and the uniform bound \(C\)\.

For homogenization, (3.2) and the semigroup property imply

\[
\|S_{\kappa_i,b}(t)P_0\|_{2\to2}
\leq2e^{-t/T},
\qquad t\geq0.
\]

Write \(w=u-\bar u\)\. Its reaction forcing is

\[
F(u)-\overline{F(u)}
=P_0(F(u)-F(\bar u)).
\]

Consequently,

\[
\|F(u)-\overline{F(u)}\|_2
\leq L\|w\|_2.
\]

Duhamel's formula yields

\[
\|w(t)\|_2
\leq2e^{-t/T}\|w(0)\|_2
+2L\int_0^t e^{-(t-r)/T}\|w(r)\|_2\,dr.
\]

Gronwall's inequality gives

\[
\|w(t)\|_2
\leq2e^{-(T^{-1}-2L)t}\|w(0)\|_2.
\]

Since \(T^{-1}\geq\chi+2L\),

\[
\boxed{
\|u(t)-\bar u(t)\|_2
\leq2e^{-\chi t}\|u_0-\bar u_0\|_2.
}
\]

Thus the requested constant can be taken to be

\[
\boxed{A=2.}
\]

This estimate is relative to the *actual evolving spatial mean*\. No convergence of \(\bar u\) to a particular equilibrium is required.

---

## 4\. Turning the existence theorem into a finite deterministic algorithm

The existence lemma alone is insufficient for the question. We must replace the unknown dissipation time by a finite, rigorously verifiable computation.

The following certificate does that.

### 4.1 Explicit semigroup truncation error

Fix a candidate \(b=b_{a,n}\) and put \(t=T/2\)\.

The controller satisfies the rational bounds

\[
B_0:=4an\geq\|b\|_\infty,
\qquad
B_1:=84an^2\geq\|\nabla b\|_\infty.
\]

Let \(P_m\) project onto nonzero Fourier modes with \(|k|_\infty\leq m\), and choose \(R\geq m\)\.

Let

\[
L_{R,i}=P_R(\kappa_i\Delta-b\cdot\nabla)P_R
\]

on the finite-dimensional mean-zero Fourier space.

Define

\[
G_i=2^{\lceil2B_1t\rceil}
\left(1+\frac1{\kappa_i t}\right)
\]

and

\[
X_i=\frac{t}{2\kappa_i}
\left(147m^2+\frac{B_1}{\kappa_i}\right).
\]

Then

\[
\boxed{
\begin{aligned}
\|S_{\kappa_i,b}(t)P_0\|_{2\to2}
\leq{}&
\|e^{tL_{R,i}}P_m\|_{2\to2}\\
&+\frac{G_i}{6m}
+\frac{G_i+B_0(1+X_i)}{6R}.
\end{aligned}
}
\tag{4.1}
\]

To verify this estimate, the \(H^1\) energy inequality gives

\[
\|\nabla S_{\kappa_i,b}(t)\|_{2\to2}
\leq\frac{e^{B_1t}}{\sqrt{\kappa_i t}}
\leq G_i.
\]

The same bound holds for the adjoint semigroup, proving that inputs above frequency \(m\) contribute at most \(G_i/(6m)\)\.

For an initial datum supported in \(P_m\), the differentiated energy identity gives

\[
\int_0^t\|\Delta S_{\kappa_i,b}(r)f\|_2^2\,dr
\leq
\frac{147m^2+B_1/\kappa_i}{2\kappa_i}\|f\|_2^2.
\]

Comparing the full equation with its Fourier–Galerkin projection, and using the fact that the Laplacian commutes with \(P_R\), bounds the remaining error by the second line of (4.1).

This is an explicit estimate for every candidate, including very large drift amplitudes.

### 4.2 Rational approximation of the finite matrix exponential

Let \(p_j\) be the rational approximation to \(2\pi\) obtained by truncating Machin's formula,

\[
2\pi=32\arctan(1/5)-8\arctan(1/239),
\]

using \(j+4\) terms of each alternating arctangent series.

The alternating-series remainder gives

\[
|p_j-2\pi|<2^{-j},
\qquad 6<p_j<7.
\]

Replace \(2\pi\) by \(p_j\) in the Fourier matrix \(L_{R,i}\)\. Denote the resulting rational complex matrix by \(\widetilde L_{R,i}\)\.

Its entries are explicitly

\[
(\widetilde L_{R,i})_{k\ell}
=
-\kappa_i p_j^2|k|^2\delta_{k\ell}
-ip_j\,\widehat b(k-\ell)\cdot\ell.
\]

Because the Fourier coefficients of \(b\) are rational and satisfy the divergence-free identities, all entries have rational real and imaginary parts. Both the original projected generator and its rational approximation generate \(L^2\)\-contractions.

The matrix perturbation obeys

\[
\|L_{R,i}-\widetilde L_{R,i}\|_{2\to2}
\leq (42\kappa_iR^2+B_0R)2^{-j}.
\]

Next define the rational Taylor matrix

\[
W_i=
\left[
\sum_{\ell=0}^{p}
\frac{(t\widetilde L_{R,i})^\ell}{\ell!}
\right]P_m.
\]

Put

\[
U_i=t(147\kappa_iR^2+7B_0R).
\]

Since \(\|t\widetilde L_{R,i}\|\leq U_i\), the Taylor remainder is at most

\[
2^{\lceil2U_i\rceil}\frac{U_i^{p+1}}{(p+1)!}.
\]

To avoid unnecessarily huge intermediate exponentials, the algorithm rejects a trial immediately unless \(p\geq2U_i+1\)\.

Combining these estimates with (4.1), define the entirely rational error bound

\[
\boxed{
\begin{aligned}
\delta_i={}&
\frac{G_i}{6m}
+\frac{G_i+B_0(1+X_i)}{6R}\\
&+t(42\kappa_iR^2+B_0R)2^{-j}\\
&+2^{\lceil2U_i\rceil}
\frac{U_i^{p+1}}{(p+1)!}.
\end{aligned}
}
\tag{4.2}
\]

We have the certified inequality

\[
\boxed{
\|S_{\kappa_i,b}(t)P_0\|_{2\to2}
\leq\|W_i\|_{2\to2}+\delta_i.
}
\tag{4.3}
\]

No infinite-dimensional PDE solve or uncertified spectral calculation appears in this bound.

### 4.3 An exact rational acceptance test

For every species, require

\[
\delta_i<\frac q4
\]

and require the rational Hermitian matrix

\[
\boxed{
\left(\frac q2\right)^2I-W_i^*W_i
}
\]

to be strictly positive definite.

Strict positive definiteness can be decided by exact rational elimination or Sylvester's criterion. No eigenvalue oracle or numerical tolerance is needed.

If these tests pass, then

\[
\|W_i\|_{2\to2}<q/2,
\]

and therefore, by (4.3),

\[
\|S_{\kappa_i,b}(T/2)P_0\|_{2\to2}<3q/4<q.
\]

The certificate consequently implies every required nonlinear and homogenization estimate.

### 4.4 The terminating search

Use exhaustive deterministic enumeration over

\[
(a,n,m,R,p,j)\in\mathbb N^6,
\qquad m\leq R.
\]

Process tuples in increasing order of their maximum coordinate, breaking ties lexicographically. For each tuple, construct the rational Fourier matrices for all \(s\) diffusivities and perform the preceding acceptance tests.

Return the first passing \(b_{a,n}\)\.

**Termination proof.** Section 2 guarantees that, for sufficiently large integers \(a,n\), the true semigroup norm is less than \(q/8\) for every species.

Fix such a candidate. In (4.2), the first error can be made arbitrarily small by increasing \(m\)\. With \(m\) fixed, the Galerkin error can be made arbitrarily small by increasing \(R\)\. With \(R\) fixed, the irrational-coefficient error vanishes as \(j\to\infty\), and the Taylor error vanishes as \(p\to\infty\)\.

Thus there is a finite tuple for which all errors are sufficiently small and every strict positive-definiteness test passes.

Exhaustive enumeration eventually visits that tuple. Hence the algorithm terminates on every promised input. \(\square\)

This is the central computability step: nonquantitative existence of effective diffusivity enhancement is combined with a **semidecidable, rigorous finite certificate**\. The algorithm never calls an effective-diffusivity oracle, mixing-time oracle, or PDE-solution oracle.

---

## 5\. Finite computable resource bounds

Here is a precise way to express the resulting bounds.

For the input datum \(D=(F,\kappa,c^*,K,\chi)\), let

\[
H(D)=\min\left\{
h\geq1:
\begin{array}{l}
\text{some tuple }1\leq a,n,m,R,p,j\leq h,\\
m\leq R,\text{ passes every certificate test}
\end{array}
\right\}.
\]

The preceding termination proof establishes that \(H(D)\) is a finite, computable integer on the full promised input class. Its computation is exactly the deterministic enumeration described above; this definition hides no external oracle.

Write \(H=H(D)\)\.

| Quantity | Finite computable bound |
|--------|--------|
| Controller parameters | \(1\leq a,n\leq H\) |
| Largest Fourier coordinate frequency | \(n\leq H\) |
| Nonzero real trigonometric terms | At most 12 after expansion |
| Velocity magnitude | \(\\|b\\|_\infty\leq4H^2\) |
| Velocity gradient | \(\\|\nabla b\\|_\infty\leq84H^3\) |
| Full \(W^{1,\infty}\) norm | \(4H^2+84H^3\) |
| Fourier verification radius | \(R\leq H\) |
| Maximum Galerkin dimension | \((2H+1)^3-1\) |
| Precision for \(2\pi\) | Error less than \(2^{-j}\), \(j\leq H\) |
| Arctangent-series terms | At most \(H+4\) in each series |
| Matrix exponential Taylor degree | \(p\leq H\) |
| Global concentration bound | \(C=8(K+M+1)\) |
| Homogenization prefactor | \(A=2\) |

For completeness, one entirely rational choice of the nonlinear quantities is

\[
Q=1+\sum_{i,\alpha}|f_{i,\alpha}|(2C)^{|\alpha|},
\]

\[
L=1+\sum_{i,j,\alpha:\alpha_j>0}
|f_{i,\alpha}|\alpha_j C^{|\alpha|-1},
\]

where \(F_i(z)=\sum_\alpha f_{i,\alpha}z^\alpha\)\.

Then set

\[
J=1+\left\lceil
\max\left\{1,\frac{8Q}{C},\chi+2L\right\}
\right\rceil,
\qquad T=J^{-1}.
\]

All quantities above are computable from finite rational arithmetic.

If \(B'\) denotes the total binary length of the input and these explicitly derived rational quantities, the certificate enumeration through shell \(H\) uses at most \(O(sH^8(2H+1)^9)\) rational arithmetic operations, apart from lower-order preprocessing. The matrix construction, factorial calculations, common-denominator Taylor arithmetic and fraction-free positive-definiteness tests have polynomially bounded operand bit lengths in \(B'+s+H\)\. Hence the complete bit work is finite and computably bounded in the input.

These are **recursive, search-defined bounds**, not practical closed-form amplitude estimates. In particular, the proof makes no claim of polynomial, elementary, or economically reasonable dependence on the original binary input length. It does account for the search, truncation, precision, arithmetic and final controller description.

## 6\. Scope relative to the two papers

The argument uses three distinct ingredients.

Iyer–Xu–Zlatoš supply the existence of smooth stationary cellular flows with arbitrarily short dissipation times. Their Proposition 4.2 independently establishes the usefulness of short dissipation times for \(L^1\)\-to-\(L^\infty\) smoothing. citeturn895315view0

The nonlinear restart argument above is an additional closure for the entropy-dissipating polynomial class. It does not follow directly from their nonlinear Theorem 1.2 and does not assume its \(H1\)–\(H2\) hypotheses.

Agresti–Kniely–Tang establish high-probability results using transport noise, as well as deterministic high-diffusivity results under their additional reaction-network conditions. Their results do not themselves provide the stationary deterministic controller constructed here. citeturn829451view5citeturn735465view3

The construction uses neither an Itô correction nor a selected stochastic realization.

## Conclusion

The proposed resolution is affirmative, with an important distinction between **computability and quantitative efficiency**\.

The argument gives a specific stationary rational-trigonometric controller family, a terminating exact-arithmetic search, explicit finite-dimensional error certificates, and uniform PDE estimates. Under the stated quasi-positivity and Boltzmann-entropy assumptions, the resulting controller is common to the entire initial-data class and all specified unequal diffusivities.

The claimed outputs are

\[
\boxed{
\begin{gathered}
b(x)=-anB(nx)\quad\text{for certified integers }a,n,\\[2mm]
\sup_{t\geq0}\max_i\|u_i(t)\|_\infty
\leq8(K+M+1),\\[2mm]
\|u(t)-\bar u(t)\|_2
\leq2e^{-\chi t}\|u_0-\bar u_0\|_2.
\end{gathered}
}
\]

No homogeneous-ODE shadowing, boundary-equilibrium exclusion, future moment estimate, stochastic forcing or time-dependent feedback is required.

The limitation is the magnitude of the search-defined bounds: they establish finite computability, not a usable actuation budget. The mathematical proof and certificate design presented here are also an independent argument, not a formally verified or peer-reviewed result; the strongest claim justified by this response is the construction and proof as written, rather than an externally certified new theorem.
