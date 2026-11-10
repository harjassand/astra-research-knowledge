# P3 completed Landau-Coulomb return

Chat: https://chatgpt.com/c/6af2d882-ab10-83ec-8084-0f7bd9630455
Model: Pro, as displayed. Final response: a6950319-9efc-565d-92d3-97a0ad1bdab8.
Exact prompt source: work/astra-renewed-pro-programmes-20261103/P3_FULL_FINITE_MASS_LANDAU_COULOMB_PRO_20261110.txt, SHA-256 efaa8be93dfbde358525f01c19d38197770fad0bc7585697d29506aaeb9154f3; one terminal LF omitted when posted.

No original ZIP was visible; Outputs showed none. Native answer is limited to its first 20,000 characters; the expanded visible accessibility tree below includes the rest of the displayed response and available activity, but its equation and table serialization is imperfect.

## Native response prefix (truncated by reader)

# Status: the full global Cauchy problem is unresolved here

**I have not proved the requested global classical well-posedness theorem, and I have not constructed an admissible finite-mass solution that violates it.** The finite-time continuation bound required by your question remains missing.

The primary literature I checked still leaves the general finite-mass Coulomb case outside its global theorem. Junné–Winter–Yoldaş explicitly identify the finite-mass-ratio problem below \(\gamma=-\sqrt8\) as open. Their compensated Coulomb theorem concerns the infinite-ion model and retains the additional data/coupling condition you stated. :chatgpt-content-reference{index="0"}

The work below gives three concrete results:

1. **An explicit conditional continuation estimate**, with the mass and coefficient dependence retained.
2. **A construction showing that mass-weighted Fisher information can initially increase for strictly finite masses and strictly positive Schwartz data.** This concerns the functional, and is not a negative answer to global regularity.
3. **An alternative heat–entropy functional** with finite initial value, tensorization and useful fractional Sobolev control. I derive its remaining collision inequality, but do not prove that inequality.

I will distinguish these established calculations from the unresolved step throughout.

## 1. What the checked sources establish

| Source | Applicable result | Limitation for your question |
|---|---|---|
| Zhu, *Fisher information for the multi-species Landau system* | Mass-weighted Fisher monotonicity under different diagonal and cross-species conditions | In dimension three, the cross-species condition is \(|\gamma_{ij}|\le\sqrt8\), excluding Coulomb |
| Junné–Winter–Yoldaş, *On the existence of solutions to the multi-species Landau equation* | Finite-mass local strong theory; global theory in its stated softer-potential range; compensated infinite-ion theorem | No arbitrary-data, arbitrary-finite-mass Coulomb continuation estimate |
| Junné–Winter–Yoldaş, September 2026 entropy-dissipation paper | Entropy dissipation can increase, including for perturbations close to equilibrium | Entropy decrease does not justify assuming that its dissipation decreases |
| Duong–He, *Multi-species kinetic models: GENERIC formulation and Fisher information* | Thermodynamic formulations and Fisher results under collision-kernel assumptions | Does not supply the missing finite-mass Coulomb theorem |

These distinctions are supported by the theorem statements and the newer paper’s abstract. :chatgpt-content-reference{index="1"} A September 2026 author seminar also describes the recovered global result in the infinite-ion regime. :chatgpt-content-reference{index="2"}

The relevant Astra records checked do not supply this missing estimate either. [N757](https://github.com/harjassand/astra-research-knowledge/blob/main/cards/N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition.txt) concerns a collision-generator construction with a retained ultraviolet cutoff and supplied regularity. [N1763](https://github.com/harjassand/astra-research-knowledge/blob/main/knowledge/current/packets/N1763.json) concerns the different Landau–Fermi–Dirac equation within an already-supplied global classical solution class.

## 2. Conservation and entropy for your exact normalization

Write
\[
a(z)=\frac{P_z}{|z|},\qquad
A[g]=a*g,\qquad
b(z)=\operatorname{div}a(z)=-\frac{2z}{|z|^3}.
\]
Distributionally,
\[
\operatorname{div}b=-8\pi\delta_0.
\]

Your equation therefore has the divergence form
\[
\partial_t f_i
=
\sum_j\left[
\frac{c_{ij}}{m_i^2}\operatorname{div}\big(A[f_j]\nabla f_i\big)
-\frac{c_{ij}}{m_im_j}
\operatorname{div}\big(f_i(b*f_j)\big)
\right].
\tag{2.1}
\]

Let
\[
d_{ij}(v,w)
=
\frac{\nabla\log f_i(v)}{m_i}
-\frac{\nabla\log f_j(w)}{m_j},
\qquad
F_{ij}=f_i(v)f_j(w).
\]
On a classical interval, symmetrization gives
\[
\begin{aligned}
\frac{d}{dt}\sum_i\int \varphi_i f_i
=
-\frac12\sum_{i,j}c_{ij}
\iint F_{ij}\,a(v-w)d_{ij}\cdot
\left(
\frac{\nabla\varphi_i(v)}{m_i}
-\frac{\nabla\varphi_j(w)}{m_j}
\right)\,dv\,dw.
\end{aligned}
\tag{2.2}
\]

This directly yields the requested conserved quantities:

- Constant test functions give conservation of each \(n_i\).
- Taking \(\varphi_i(v)=m_i v_\ell\) gives conservation of total momentum.
- Taking \(\varphi_i(v)=m_i|v|^2/2\) gives conservation of total kinetic energy, because \(a(z)z=0\).

Testing the entropy gives
\[
-\frac{d}{dt}\sum_i\int f_i\log f_i
=
\frac12\sum_{i,j}c_{ij}
\iint \frac{F_{ij}}{|v-w|}
|P_{v-w}d_{ij}|^2\,dv\,dw.
\tag{2.3}
\]
Since \(D_z=\mu_{ij}(\nabla_v/m_i-\nabla_w/m_j)\), this is exactly
\[
D_H(\mathbf f)
=
\frac12\sum_{i,j}c_{ij}\mu_{ij}^{-2}J_{ij}.
\tag{2.4}
\]

These identities retain the actual particle numbers; no unit-mass normalization is implicit.

For a useful nonnegative entropy, set
\[
\rho=\sum_i m_i n_i,\qquad
u=\frac{P}{\rho},\qquad
\Theta=\frac{2E-|P|^2/\rho}{3(n_1+n_2)}.
\]
The assumptions imply \(\Theta>0\). Define
\[
\mathcal M_i(v)
=
n_i\left(\frac{m_i}{2\pi\Theta}\right)^{3/2}
\exp\!\left(-\frac{m_i|v-u|^2}{2\Theta}\right).
\]
Then
\[
\mathcal H(\mathbf f\mid\boldsymbol{\mathcal M})
=
\sum_i\int f_i\log\frac{f_i}{\mathcal M_i}\ge0,
\]
and, on the classical interval,
\[
\boxed{
\mathcal H(\mathbf f(t)\mid\boldsymbol{\mathcal M})
+\int_0^t D_H(\mathbf f(s))\,ds
=
\mathcal H(\mathbf f^0\mid\boldsymbol{\mathcal M}).
}
\tag{2.5}
\]

Thus entropy supplies a finite time integral of \(D_H\). It does not yet supply a supremum bound for Fisher information or another continuation norm.

## 3. An explicit Fisher-to-continuation estimate

Here is a closed conditional implication. Its hypothesis is precisely identified so that it cannot be mistaken for the missing global estimate.

Let \(T_*\) be the maximal time of the local strong solution. Suppose, for some finite \(T\le T_*\),
\[
S_T:=\sup_{0\le t<T}I_m(\mathbf f(t))<\infty.
\tag{3.1}
\]

Define
\[
M_q(t)=\sum_{i=1}^2m_i\int f_i(t,v)\langle v\rangle^q\,dv,
\qquad
\langle v\rangle=(1+|v|^2)^{1/2}.
\]

I will derive a bound for
\[
Y_7(t)=\sum_i\int f_i(t,v)^2\langle v\rangle^7\,dv,
\]
which is a weighted \(L^2\) quantity of the type used by the local strong theory.

### 3.1 Fisher information controls \(L^3\)

Let \(C_S\) satisfy
\[
\|h\|_{L^6}^2\le C_S\|\nabla h\|_{L^2}^2.
\]
Since
\[
I(f)=4\|\nabla\sqrt f\|_2^2,
\]
we have
\[
\|f_i\|_3
=
\|\sqrt{f_i}\|_6^2
\le \frac{C_S}{4}I(f_i)
\le \frac{C_S}{4}m_iS_T.
\tag{3.2}
\]

### 3.2 An explicit Coulomb-potential bound

For any \(R>0\), Hölder’s inequality gives
\[
\begin{aligned}
\int\frac{f(w)}{|v-w|}\,dw
&\le
\|f\|_3
\left(\int_{|z|<R}|z|^{-3/2}\,dz\right)^{2/3}
+\frac{n}{R}\\
&=
\left(\frac{8\pi}{3}\right)^{2/3}R\|f\|_3
+\frac nR.
\end{aligned}
\]
Optimizing this elementary bound in \(R\),
\[
\big\||\,\cdot\,|^{-1}*f\big\|_\infty
\le
2\left(\frac{8\pi}{3}\right)^{1/3}
\sqrt{n\|f\|_3}.
\]
Combining with (3.2),
\[
\boxed{
\big\||\,\cdot\,|^{-1}*f_i\big\|_\infty
\le C_P\sqrt{n_i m_iS_T},
\qquad
C_P=\left(\frac{8\pi}{3}\right)^{1/3}\sqrt{C_S}.
}
\tag{3.3}
\]

### 3.3 Higher moments then remain bounded

Put \(\phi_q(v)=\langle v\rangle^q\), \(q\ge2\). Applying (2.1), integrating by parts, and symmetrizing gives
\[
\begin{aligned}
M_q'
=\frac12\sum_{i,j}c_{ij}\iint F_{ij}
\Bigg[
&a(v-w):
\left(\frac{D^2\phi_q(v)}{m_i}
+\frac{D^2\phi_q(w)}{m_j}\right)\\
&+\left(\frac1{m_i}+\frac1{m_j}\right)
b(v-w)\cdot
\big(\nabla\phi_q(v)-\nabla\phi_q(w)\big)
\Bigg].
\end{aligned}
\tag{3.4}
\]

Convexity of \(\phi_q\) makes the second line nonpositive:
\[
b(v-w)\cdot
\big(\nabla\phi_q(v)-\nabla\phi_q(w)\big)\le0.
\]
Also,
\[
\operatorname{tr}a(z)=\frac2{|z|},
\qquad
\|D^2\phi_q(v)\|
\le q(q-1)\langle v\rangle^{q-2}.
\]
Consequently,
\[
M_q'
\le
2q(q-1)\sum_{i,j}\frac{c_{ij}}{m_i}
\int f_i(v)\langle v\rangle^{q-2}
\big(|\,\cdot\,|^{-1}*f_j\big)(v)\,dv.
\]
Define the finite constant
\[
\boxed{
K_q=
2q(q-1)C_P
\max_{i=1,2}
\left[
\frac1{m_i^2}\sum_{j=1}^2c_{ij}\sqrt{n_jm_j}
\right].
}
\tag{3.5}
\]
Then
\[
M_q'\le K_q\sqrt{S_T}\,M_{q-2}
\le K_q\sqrt{S_T}\,M_q,
\]
and hence
\[
\boxed{
M_q(t)\le M_q(0)e^{K_q\sqrt{S_T}\,t}.
}
\tag{3.6}
\]

This argument need not assume that Schwartz tails have already propagated. Smooth convex radial truncations, with a linear continuation outside a large ball, retain the drift sign and allow the estimate to pass to the limit.

### 3.4 The actual weighted \(L^2\) bound

Cauchy–Schwarz gives
\[
\begin{aligned}
\int f_i^2\langle v\rangle^7
&=
\int (f_i^3)^{1/2}
(f_i\langle v\rangle^{14})^{1/2}\\
&\le
\|f_i\|_3^{3/2}
\left(\int f_i\langle v\rangle^{14}\right)^{1/2}.
\end{aligned}
\]
Therefore
\[
\boxed{
Y_7(t)
\le
\left(\frac{C_S}{4}\right)^{3/2}
(m_1+m_2)\,
S_T^{3/2}\sqrt{M_{14}(0)}
\exp\!\left(\frac{K_{14}\sqrt{S_T}\,t}{2}\right).
}
\tag{3.7}
\]

The local weighted-\(L^2\) strong theory can be restarted from these bounds, together with the fixed particle numbers, masses, coefficients, energy and entropy bounds. Its relevant local statement is Lemma 2.7 of Junné–Winter–Yoldaş. :chatgpt-content-reference{index="3"}

For nonunit particle numbers, the normalization \(f_i=n_i g_i\) gives effective coefficients \(c_{ij}n_j\). These satisfy weighted detailed balance,
\[
n_i(c_{ij}n_j)=n_j(c_{ji}n_i),
\]
and the entropy and Fisher quantities retain weights \(n_i\). One must preserve these weights when adapting the probability-density formulation.

Thus, within this local strong class,
\[
\boxed{
T_*<\infty
\quad\Longrightarrow\quad
\sup_{t<T_*}I_m(\mathbf f(t))=\infty.
}
\tag{3.8}
\]

**What remains unproved is a bound on \(S_T\) from the initial data.** Equation (3.7) proves that such a bound would accomplish continuation; it does not establish that bound.

## 4. Fisher information can increase with finite masses

The following auxiliary result strengthens the distinction between a failed functional and a failed Cauchy theorem.

> **Auxiliary conclusion.** There exist strictly finite positive masses, positive symmetric collision coefficients, and strictly positive Schwartz probability densities for which
> \[
> \left.\frac{d}{dt}I_m(\mathbf f(t))\right|_{t=0}>0.
> \]
> This does not imply finite-time blowup.

Here is a construction in which the final data and masses are all finite.

### 4.1 A strictly positive angular seed

Let
\[
h_\sigma(r)=Z_\sigma^{-1}
\exp\!\left[-\frac{(r^2-1)^2}{\sigma^2}\right],
\qquad
\int_{\mathbb R^3}h_\sigma(|v|)\,dv=1.
\]
Choose \(\chi\in C_c^\infty((1/2,3/2))\), equal to \(1\) on \([3/4,5/4]\), and set
\[
a_0(r)=\chi(r)r^{3/2},
\qquad
Y(\omega)=\omega_1.
\]
For small \(\varepsilon\), define
\[
f_\varepsilon(v)
=
Z_\varepsilon^{-1}h_\sigma(|v|)
e^{\varepsilon a_0(|v|)Y(\widehat v)}.
\tag{4.1}
\]
This is strictly positive and Schwartz. The angular perturbation vanishes near the origin, so it is smooth there.

For the auxiliary angular operator
\[
L f=\operatorname{div}\!\left(\frac{P_v}{|v|}\nabla f\right)
=r^{-3}\Delta_{\mathbb S^2}f,
\]
one obtains
\[
\begin{aligned}
\langle I'(f_\varepsilon),Lf_\varepsilon\rangle
={}&-\frac{16\pi}{3}\varepsilon^2
\int_0^\infty h_\sigma(r)r^{-3}
\left[
\left(ra_0'(r)-\frac32a_0(r)\right)^2
-\frac14a_0(r)^2
\right]\,dr\\
&+O(\varepsilon^4).
\end{aligned}
\tag{4.2}
\]

The constants follow from
\[
\int_{\mathbb S^2}|\nabla Y|^2=\frac{8\pi}{3},
\qquad
\int_{\mathbb S^2}\Gamma_2(Y)=\frac{16\pi}{3}.
\]
For fixed \(\sigma\), the remainder is bounded by a finite constant times \(\varepsilon^4\); the expression is even in \(\varepsilon\).

Where \(\chi=1\), the bracket in (4.2) equals \(-r^3/4\). The cutoff-transition contribution is exponentially small as \(\sigma\downarrow0\), and the integral tends to
\[
-\frac1{16\pi}.
\]
Choose \(\sigma>0\) small enough and then \(\varepsilon>0\) small enough. This gives a fixed strictly positive Schwartz density \(f\) such that
\[
A_0:=\langle I'(f),Lf\rangle>0.
\tag{4.3}
\]

### 4.2 Replace the concentrated background by a smooth density

Let \(g_\delta\) be a centered Gaussian probability density with variance tending to zero as \(\delta\downarrow0\). Set
\[
A_\delta=
\left\langle I'(f),
\operatorname{div}(A[g_\delta]\nabla f)\right\rangle.
\]
Then
\[
A_\delta\longrightarrow A_0.
\tag{4.4}
\]

For this particular \(f\), convergence follows directly from the unsplit first variation. Write
\[
\Psi_f=-2\Delta\log f-|\nabla\log f|^2,
\qquad
I'(f)[q]=\int\Psi_f q.
\]
Then
\[
A_\delta=\int g_\delta(w)K_f(w)\,dw,
\]
where
\[
K_f(w)
=
-\int a(v-w):
\big[\nabla f(v)\otimes\nabla\Psi_f(v)\big]\,dv.
\]
The tensor factor is Schwartz, and \(a\) is locally integrable. Thus \(K_f\) is bounded and continuous, which proves (4.4).

Fix one positive \(\delta\) such that \(A:=A_\delta>0\), and write \(g=g_\delta\).

### 4.3 Fix a finite second mass

For convenience, define
\[
\mathscr D_h k=\operatorname{div}(A[h]\nabla k),
\qquad
\mathscr F_h k=\operatorname{div}\big(k(b*h)\big),
\]
and the finite numbers
\[
\begin{aligned}
S&=I'(f)[\mathscr D_f f-\mathscr F_f f],\\
B&=I'(f)[\mathscr F_g f],\\
C&=I'(g)[\mathscr D_f g],\\
D&=I'(g)[\mathscr F_f g].
\end{aligned}
\]
Take
\[
m_1=1,\quad m_2=M,\quad
c_{11}=c_{22}=1,\quad c_{12}=c_{21}=c.
\]
Since \(g\) is Gaussian, its same-species collision term vanishes. For the original finite-mass operator, the exact derivative is
\[
\boxed{
I_m'(0)
=
S+cA-\frac{cB}{M}
-\frac{cD}{M^2}
+\frac{cC}{M^3}.
}
\tag{4.5}
\]

Choose
\[
c=\frac{|S|+1}{A}>0,
\qquad
K=|B|+|C|+|D|.
\]
Then \(S+cA\ge1\). Any finite
\[
M>\max\{1,2cK\}
\]
makes the absolute value of the remaining terms less than \(1/2\). Therefore
\[
I_m'(0)>\frac12.
\tag{4.6}
\]

The limiting arguments above only select fixed smooth densities and a fixed finite \(M\). Equation (4.5), which establishes the final claim, is exact for your collision operator.

This rules out universal monotonicity of \(I_m\) over the full parameter/data class. A global regularity proof could still allow controlled Fisher growth or use a different quantity.

## 5. Why the finite-recoil compensation remains unclosed

Your \(J_{ij}\) quantities have the correct entropy meaning. The unresolved issue is their evolution.

In center/relative variables, write
\[
F=F_{ij},\qquad \Psi=\log F,\qquad r=|z|.
\]
Then
\[
J_{ij}
=
\int F\,r^{-3}|\nabla_{\mathbb S^2}\Psi|^2\,dZ\,dz.
\]
Its first variation is
\[
\frac{\delta J_{ij}}{\delta F}
=
-r^{-3}
\left(
2\Delta_{\mathbb S^2}\Psi
+|\nabla_{\mathbb S^2}\Psi|^2
\right)
=:\Phi_{ij}.
\tag{5.1}
\]

Along the actual mixture,
\[
\partial_tF_{ij}
=
\sum_k
\left[
Q_{ik}(f_i,f_k)(v)f_j(w)
+
f_i(v)Q_{jk}(f_j,f_k)(w)
\right].
\]
Consequently,
\[
\boxed{
\frac{d}{dt}J_{ij}
=
\sum_k\iint\Phi_{ij}
\left[
Q_{ik}(f_i,f_k)(v)f_j(w)
+
f_i(v)Q_{jk}(f_j,f_k)(w)
\right]\,dv\,dw.
}
\tag{5.2}
\]

Substituting the collision operators introduces mixed triple integrals. Both groups in (5.2) matter for finite recoil.

A proposed functional such as
\[
I_m+\sum_{i,j}a_{ij}J_{ij}
+R\mathcal H(\mathbf f\mid\boldsymbol{\mathcal M})
\]
therefore needs an estimate for those mixed terms. The entropy identity controls the time integral of the \(J_{ij}\), while this proposal needs control of their derivatives. The known possibility that entropy dissipation increases prevents replacing that estimate by a monotonicity assertion. :chatgpt-content-reference{index="4"}

There is also an endpoint integrability issue. For generic cross-species data near \(z=0\), the completed-square Fisher decomposition has pieces with logarithmically divergent integrals. Their cancellation must be retained. The finite-mass construction above uses the unsplit first variation and avoids subtracting separately divergent expressions.

I have not obtained the required estimate for (5.2).

## 6. An alternative functional with a precise remaining inequality

I also pursued a different representation that measures regularity below one full derivative.

For \(0<s<1\), let
\[
P_\tau^{(i)}=e^{(\tau/m_i)\Delta}
\]
be an auxiliary Gaussian heat flow, and define
\[
\boxed{
\mathcal E_s(\mathbf f)
=
s(1-s)\sum_i
\int_0^\infty
\left[H(f_i)-H(P_\tau^{(i)}f_i)\right]
\frac{d\tau}{\tau^{1+s}}.
}
\tag{6.1}
\]
Here \(\tau\) is auxiliary heat time, distinct from the physical collision time.

### 6.1 Its initial value is controlled by the supplied data

The heat entropy identity gives
\[
\mathcal E_s(\mathbf f)
=
(1-s)\int_0^\infty
\tau^{-s}I_m(P_\tau\mathbf f)\,d\tau.
\]
Set
\[
N=n_1+n_2,\qquad K=\frac{3N}{2},\qquad I_0=I_m(\mathbf f).
\]
The heat-flow estimates
\[
I_m(P_\tau\mathbf f)\le
\min\left\{I_0,\frac K\tau\right\}
\]
yield, by splitting at \(\tau=K/I_0\),
\[
\boxed{
0\le\mathcal E_s(\mathbf f)
\le\frac{K^{1-s}I_0^s}{s}.
}
\tag{6.2}
\]

Thus this candidate is finite for every datum in your question.

### 6.2 It controls fractional regularity

The entropy Jensen gap bounds
\[
H(f)-H(P_\tau f)
\ge
\|\sqrt f\|_2^2-\|P_\tau\sqrt f\|_2^2.
\]
Integrating in \(\tau\) gives
\[
\boxed{
\mathcal E_s(\mathbf f)
\ge
2^s\Gamma(2-s)
\sum_i m_i^{-s}
\|\sqrt{f_i}\|_{\dot H^s}^2.
}
\tag{6.3}
\]
The Fourier convention here gives \(-\Delta\) the multiplier \(|\xi|^2\).

Fractional Sobolev embedding then controls
\[
f_i\in L^{p_s},
\qquad
p_s=\frac{3}{3-2s}.
\tag{6.4}
\]
In particular, \(s>1/2\) gives \(p_s>3/2\), making this functional relevant to continuation.

It also has the needed product structure: it tensorizes on probability products and is marginal-superadditive, because independent heat channels decrease mutual information. Its first variation at a product is additive across the velocity blocks.

These properties are established calculations. They do not imply dissipation under Landau collisions.

### 6.3 The exact collision term whose sign is missing

For a pair, let
\[
F=f_i(v)f_j(w),\qquad
\alpha(z)=|z|^{-3}.
\]
Choose the three rotation fields
\[
b_k(z)\in\{e_1\times z,e_2\times z,e_3\times z\},
\]
and define
\[
L_k=
\frac{b_k(z)\cdot\nabla_v}{m_i}
-\frac{b_k(z)\cdot\nabla_w}{m_j},
\qquad q_k=L_k\log F.
\]
The pair heat semigroup
\[
P_\tau=e^{\tau(\Delta_v/m_i+\Delta_w/m_j)}
\]
commutes with each \(L_k\).

For sufficiently regular profiles, first restricting the auxiliary heat integral to a compact interval, the entropy-gap calculation gives the pair expression
\[
B_{ij,k}(\tau)
=
\int\alpha Fq_k^2
-
\int
\frac{
P_\tau(\alpha Fq_k)\,
P_\tau(Fq_k)
}{
P_\tau F
}.
\tag{6.5}
\]
After assembling ordered pairs, the corresponding formal full-range identity is
\[
\frac{d}{dt}\mathcal E_s(\mathbf f(t))
=
-\frac{s(1-s)}2
\sum_{i,j}c_{ij}\sum_k
\int_0^\infty
B_{ij,k}(\tau)\frac{d\tau}{\tau^{1+s}}.
\tag{6.6}
\]
Passing from truncated auxiliary intervals to (6.6) requires appropriate bounds; it is not an additional regularity assumption that can be inserted into a global proof without justification.

For constant \(\alpha\), a contraction argument gives the desired sign. For Coulomb, the two numerator factors in (6.5) contain different weights. The radial coefficient does not commute with heat.

A naive weighted Cauchy–Schwarz argument introduces \(P_\tau(\alpha F)\), which is generally divergent at \(z=0\). In contrast,
\[
\alpha Fq_k=O(|z|^{-2}),\qquad
\alpha Fq_k^2=O(|z|^{-1}),
\]
are locally integrable for smooth product profiles. Preserving those score factors is essential.

**I have not proved that the integrated expression in (6.6) is nonnegative, or bounded below by a quantity that yields a closed finite-time growth estimate.** Moreover, as \(s\uparrow1\), the normalized functional approaches \(I_m\); the strict Fisher-growth examples prevent simply asserting monotonicity for all \(s\) close to one.

## 7. The remaining mathematical obligation

The explicit continuation calculation reduces one sufficient route to proving
\[
\sup_{0\le t<T}I_m(\mathbf f(t))
\le
B_T\!\left(
m_i,c_{ij},n_i,E,
\mathcal H(\mathbf f^0\mid\boldsymbol{\mathcal M}),
I_m(\mathbf f^0),
\text{specified initial weighted norms}
\right)
<\infty
\]
for every finite \(T\).

An alternative regularity functional could replace Fisher information, but i

## Expanded visible accessibility tree

```text
Browser tab: 1463921647, Title: "Global Wellposedness Status", URL: "https://chatgpt.com/c/6af2d882-ab10-83ec-8084-0f7bd9630455".
0 AXWebArea Global Wellposedness Status, URL: chatgpt.com/c/6af2d882-ab10-83ec-8084-0f7bd9630455
	1 container
		2 container root
			3 container
				4 link Description: Skip to content, Value: chatgpt.com/c/6af2d882-ab10-83ec-8084-0f7bd9630455#_r_42_
				5 container
					6 container app-shell-sidebar
						7 container App navigation
							8 button (collapsed) Home, Secondary Actions: Expand
							9 button (collapsed) Space, Secondary Actions: Expand
							10 button (collapsed) Scheduled, Secondary Actions: Expand
							11 button (collapsed) Plugins, Secondary Actions: Expand
							12 pop up button (collapsed) Explore, Secondary Actions: Expand
							13 button Sites
							14 button (collapsed) Codex, Secondary Actions: Expand
							15 button Projects
							16 container
								17 pop up button (collapsed) Description: Usage, ID: radix-_r_31_, Secondary Actions: Expand
								18 pop up button (collapsed) Description: Open profile menu, ID: radix-_R_9esujeiud9iqr7dcchej9arad5_, Secondary Actions: Expand
					19 container
						20 button New chat
							21 image
						22 pop up button (collapsed) Global Wellposedness Status, ID: radix-_r_5a_, Secondary Actions: Expand
						23 button Share
						24 checkbox Description: Toggle pinned summary, Value: 1
							25 image
					26 container
						27 container Conversation
							28 container
								29 heading You said:, Value: 4
									30 text You said:
								31 container
									32 text Global regularity for the finite-mass two-species Landau-Coulomb system  FULL QUESTION. Resolve global classical well-posedness of the spatially HOMOGENEOUS two-species Landau-Coulomb equation on velocity space R^3, for arbitrary positive finite particle masses and arbitrary smooth nonequilibrium data, as follows.  Fix ANY m_1,m_2>0 and positive symmetric coefficients c_ij=c_ji>0, i,j in {1,2}. Define P_z=I-z tensor z/|z|^2 and  Q_ij(f_i,f_j)(v)  = (c_ij/m_i) div_v integral _ (R3)  [P\_(v-w)/|v-w|]      \*[(f_j(w)/m_i) grad_v f_i(v)        -(f_i(v)/m_j) grad_w f_j(w)] dw. The equation is partial_t f_i=sum\_(j=1,2) Q_ij(f_i,f_j).  For EVERY pair of strictly positive Schwartz initial densities f_i^0 on R^3, with nonzero finite masses n_i=integral f_i^0 and finite mass-weighted Fisher information  I_m(f^0)=sum_i (1/m_i) integral |grad f_i^0|^2/f_i^0, does this Cauchy problem have a unique global nonnegative classical solution, smooth for positive times and attaining f_i^0 at t=0 in the usual finite-mass/energy strong-solution class?  The result must include finite-time a priori bounds sufficient for classical continuation for every finite T, with their dependence on the finite masses, coefficients and actual initial norms specified. In particular, a Fisher-information or other continuation bound must be proved rather than assumed. Retain each species mass, total momentum sum_i m_i integral v f_i, total kinetic energy (1/2)sum_i m_i integral |v|^2 f_i and the entropy inequality. No near-Maxwellian smallness, radial/even symmetry, infinite-mass species, frozen background, special mass ratio, artificial velocity cutoff or modified collision operator is part of the question.  A full affirmative must prove the stated global existence and uniqueness for the whole class. A negative must exhibit a genuine obstruction to that contract for admissible FINITE masses and data; growth of one proposed Lyapunov functional, failure of a particular estimate or an infinite-mass limiting example is not such an obstruction. This is an analytic mathematical question, not a requested numerical simulation. Any computation or approximation used must have its actual hypotheses, errors and costs accounted for; no solution, optimization or real-number oracle is supplied.  The suggested papers and supplied premises are starting points, not a limit on your research. You may read them, seek additional papers, literature, available Astra work or other sources, change mathematical representations, introduce different ideas and methods, and challenge my framing while pursuing the full question. You choose your sources and approach without further permission.  Useful starting mathematics and contrary results, not a prescribed method:  1. Single-species Fisher monotonicity does not automatically extend to Coulomb mixtures. For the mass-weighted I_m, the known general cross-species spherical criterion in dimension3 reaches |gamma_ij|<=sqrt(8), whereas Coulomb has gamma=-3. Diagonal same-species terms retain particle-exchange symmetry; cross terms generally do not. The exact lifted derivative separates a negative squared derivative of the angular collision field from a positive radial-coefficient term. The absence of a sign from that criterion is not a global blowup theorem.  2. There is an actual compensation mechanism in a distinct limiting problem. For one species interacting with a frozen infinite-mass ion background, the equation contains the spherical diffusion c_ei div(|v|^-1 P_v grad f). Write  J(f)=integral |v|^-1 |P_v grad log f|^2 f. An existing theorem constructs a nonnegative Lyapunov functional I(f)+a J(f)+R H(f|M) and obtains global regularity. In the Coulomb case its theorem includes the additional data/coupling condition  2+J(f^0)/I(f^0)^(3/2)+H(f^0|M)<=c_ei/K for a specified sufficiently large constant K. This is not an arbitrary-finite-mass or arbitrary-coupling result, and that extra condition is not imposed on the full question here.  3. The finite-mass pair geometry is explicit. For a pair (v,w), put z=v-w, Z=(m_i v+m_j w)/(m_i+m_j), mu_ij=m_i m_j/(m_i+m_j), and F_ij=f_i(v)f_j(w). At fixed Z the relative derivative is  D_z=mu_ij(grad_v/m_i-grad_w/m_j). The pair angular quantity  J_ij=integral\_(R6) F_ij |z|^-1 |P_z D_z log F_ij|^2 dv dw satisfies the exact entropy-dissipation identity  -partial_t sum_i integral f_i log f_i    =(1/2)sum\_(i,j) c_ij mu_ij^-2 J_ij. This identifies a finite-recoil counterpart of the limiting angular quantity. It does not supply a sign for its derivative: both marginals evolve, and differentiating introduces mixed collision terms. A compensation built from these quantities, a different representation or another mechanism is open.  4. Do not assume entropy dissipation is itself monotone. Even for the single-species Landau-Coulomb equation there are smooth near-Maxwellian examples where its time derivative is positive. Thus adding entropy dissipation to Fisher information needs a genuine estimate; thermodynamic entropy decrease alone does not provide it.  Optional primary starting points, in any order:  \* Zhu, [https://arxiv.org/html/2512.17905v1](https://arxiv.org/html/2512.17905v1), Theorem1.1 and Proposition2.2: mass-weighted mixture Fisher information, exact lifted derivative and the different diagonal/cross-species thresholds.  \* Junne, Winter and Yoldas, [https://arxiv.org/html/2512.17082v1](https://arxiv.org/html/2512.17082v1), Theorems1.1-1.3 and Sections2-3: finite-mass local theory, the contrary Fisher example, and the compensated infinite-ion theorem with its Coulomb condition retained.  \* Junne, Winter and Yoldas, [https://arxiv.org/html/2609.03847v1](https://arxiv.org/html/2609.03847v1), Theorem1.1: entropy dissipation can increase even near equilibrium. This concerns a Lyapunov shortcut, not failure of classical solutions.  The full endpoint is the finite-mass global Cauchy theory above. The choice of functional, representation, sources and proof strategy is yours.  you may use all subagents avaible
								33 button (expanded) Show less, Secondary Actions: Collapse
									34 text Show less
									35 image
								36 button Copy message
									37 image
								38 button Share prompt
								39 button Edit message
									40 image
								41 button (expanded) Worked for 21m 24s, Secondary Actions: Collapse
									42 text Worked for 21m 24s
									43 image
								2286 text I’ll check the current results and work on several possible routes to the finite-mass problem in parallel. I’ll keep the full continuation requirement in view: a conditional estimate or a failed Lyapunov argument would not settle your question.
								2287 text Searching arxiv.org
								2288 container Subagent activity
									2289 container
										2290 button Fisher compensation
										2291 text , 
										2292 button Alternative continuation
										2293 text  and 
										2294 button Literature frontier
										2295 text  started working
								2296 text Searching arxiv.org
								2297 text The finite-mass result I’ve read so far covers cross interactions only down to 
								2298 container
									2299 text 𝛾 = −
									2300 text 8
								2301 text , leaving Coulomb at 
								2302 container
									2303 text 𝛾 = − 3
								2304 text  outside its theorem. I’m now testing whether finite recoil and the positive same-species collisions can close that gap. I’m also using the runtime skill for any symbolic checks needed in the derivations.
								2305 container
									2306 button (collapsed) Searched the web, Secondary Actions: Expand
									2307 text Searched the web
								2308 text Explored finite-mass symmetry
								2309 text Searched 10 websites
								2310 text Checked mass normalization and finite-mass scaling
								2311 text Tested Fisher-growth and entropy-dissipation controls
								2312 text The newer sources I’ve found still leave the arbitrary finite-mass Coulomb case open. One route I’m investigating is weaker than Fisher monotonicity: if Fisher growth can be bounded by entropy dissipation times Fisher information, the entropy inequality would give a finite-time bound. The question is whether that estimate survives the singular cross-collision terms.
								2313 container Subagent activity
									2314 container
										2315 button Fisher compensation
										2316 text  and 
										2317 button Alternative continuation
										2318 text  updated
								2319 text Searching arxiv.org
								2320 text Derived the direct first variation and tested spike-scale control Tested spike scaling and entropy coercivity
								2321 container Subagent activity
									2322 container
										2323 button Fisher compensation
										2324 text  updated
								2325 text Explored weighted Fisher powers and tested finite-species entropy-dissipation obstructions Analyzed label symmetrization and tested scalar envelope
								2326 container Subagent activity
									2327 container
										2328 button Alternative continuation
										2329 text  and 
										2330 button Fisher compensation
										2331 text  updated
								2332 text Searching arxiv.org
								2333 text Derived symbolic derivative and weighted Lp law Tested reaction interpolation and pairwise Lp control Checked derivative weights, Renyi contractivity, and collision mixing Investigated fractional Fisher monotonicity
								2334 container Subagent activity
									2335 container
										2336 button Alternative continuation
										2337 text  updated
								2338 text Derived the mass-Fisher functional and assessed interaction bounds and velocity scaling Assessed Lp control and balanced weighted exponents The entropy-based growth estimate has a serious scaling problem: small, concentrated components can make the prospective Fisher-growth term too large relative to the proposed bound. I’m also checking a cancellation at zero relative velocity in the Coulomb formulas; separating the positive and negative terms there can lose information. Neither issue establishes blowup.
								2339 text Searched 30 websites
								2340 text Tested shifted Fisher bounds and balanced entropy scaling
								2341 text Assessed entropy control
								2342 container
									2343 button (collapsed) Searched the web, Secondary Actions: Expand
									2344 text Searched the web
								2345 text Derived moment and weighted moment bounds
								2346 text Derived the M_q and q14 estimates
								2347 text Computed the potential constant and derived weighted L² bounds
								2348 container Subagent activity
									2349 container
										2350 button Literature frontier
										2351 text  updated
								2352 text Checked Fisher-integral bounds
								2353 container Subagent activity
									2354 container
										2355 button Fisher compensation
										2356 text  finished
								2357 text Constructed annular perturbation and derived finite-mass counterexample
								2358 text Tuned the positive seed and checked the Gaussian limit
								2359 text Verified Aσ convergence
								2360 container Subagent activity
									2361 container
										2362 button Fisher compensation
										2363 text , 
										2364 button Alternative continuation
										2365 text  and 
										2366 button Literature frontier
										2367 text  updated
								2368 text Analyzing T_t contraction
								2369 text Derived kernel energy identity and checked anticommutator positivity
								2370 text Checked the Hardy borderline and derived the weighted Hessian
								2371 text Tested thin-shell behavior, shell-rate coupling, and 2x2 conditions
								2372 text Estimated and checked stability threshold, leaving result unresolved
								2373 text Constructed angular seed and checked angular derivative
								2374 text Checked Fisher derivative signs and mixture scaling
								2375 text I’ve closed a useful conditional step: a finite bound on the mass-weighted Fisher information would control the weighted 
								2376 container
									2377 text 𝐿 2
								2378 text  norms needed to restart the local solution. The constants can be written in terms of the masses, collision coefficients, particle numbers and initial moments. The Fisher bound itself is still missing. I’m making one final pass on a weaker regularity functional that might avoid the failed monotonicity argument.
								2379 container Subagent activity
									2380 container
										2381 button Alternative continuation
										2382 text  updated
								2383 text Explored posterior variance bounds and tested radial profile counterexamples Checked for missing estimates
								2384 container
									2385 button (collapsed) Used GitHub integration, searched the web, Secondary Actions: Expand
									2386 text Used GitHub integration , searched the web
								2387 text Verified entropy balance and Fisher derivative
								2388 text Checked the coefficient
								2389 container Subagent activity
									2390 container
										2391 button Fisher compensation
										2392 text  updated
								2393 text Prepared total-expansion notation and defined the remainder estimate
								2394 text Formulated the blowup criterion
								2395 container Subagent activity
									2396 container
										2397 button Alternative continuation
										2398 text  updated
								2399 text Checked Fermi mappings, lifted models, and radial spectral gaps
								2400 text Formulated correlated Fisher pending full-text access
								2401 text Checked the seed formula and verified the Hessian expansion
								2402 text Derived and checked the entropy-gap bound
								2403 text Refined selection of exponents greater than three-fourths
								2404 text Checked tensorization normalization
								2405 container Subagent activity
									2406 container
										2407 button Alternative continuation
										2408 text  and 
										2409 button Fisher compensation
										2410 text  finished
								2411 text Checked weighted L² adaptation
								2412 text Refined the truncation argument and assembled the I_m' formula
								2413 text Verified compensation formulas and checked J variation
								2414 text Derived the dissipation formula
								2415 text Checked Coulomb cutoff settings
								2416 text Verified normalized coefficients
								44 heading ChatGPT said:, Value: 4
									45 text ChatGPT said:
								46 heading Status: the full global Cauchy problem is unresolved here, Value: 1
									47 text Status: the full global Cauchy problem is unresolved here
								48 text I have not proved the requested global classical well-posedness theorem, and I have not constructed an admissible finite-mass solution that violates it.
								49 text  The finite-time continuation bound required by your question remains missing. The primary literature I checked still leaves the general finite-mass Coulomb case outside its global theorem. Junné–Winter–Yoldaş explicitly identify the finite-mass-ratio problem below 
								50 container
									51 text 𝛾 = −
									52 text 8
								53 text  as open. Their compensated Coulomb theorem concerns the infinite-ion model and retains the additional data/coupling condition you stated. 
								54 link (collapsed) Value: arxiv.org/html/2512.17082v1?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: On the existence of solutions to the multi-species Landau equation, https://arxiv.org/html/2512.17082v1?utm_source=chatgpt.com
								55 text The work below gives three concrete results:
								56 content list
									57 container
										58 AXListMarker 1. 
										59 text An explicit conditional continuation estimate , with the mass and coefficient dependence retained.
									60 container
										61 AXListMarker 2. 
										62 text A construction showing that mass-weighted Fisher information can initially increase for strictly finite masses and strictly positive Schwartz data.  This concerns the functional, and is not a negative answer to global regularity.
									63 container
										64 AXListMarker 3. 
										65 text An alternative heat–entropy functional  with finite initial value, tensorization and useful fractional Sobolev control. I derive its remaining collision inequality, but do not prove that inequality.
								66 text I will distinguish these established calculations from the unresolved step throughout.
								67 heading 1. What the checked sources establish, Value: 2
									68 text 1. What the checked sources establish
								69 table
									70 row
										71 cell
											72 text Source
										73 cell
											74 text Applicable result
										75 cell
											76 text Limitation for your question
									77 row
										78 cell
											79 text Zhu, 
											80 text Fisher information for the multi-species Landau system
										81 cell
											82 text Mass-weighted Fisher monotonicity under different diagonal and cross-species conditions
										83 cell
											84 text In dimension three, the cross-species condition is  (
									85 row
										86 cell
											87 text Junné–Winter–Yoldaş, 
											88 text On the existence of solutions to the multi-species Landau equation
										89 cell
											90 text Finite-mass local strong theory; global theory in its stated softer-potential range; compensated infinite-ion theorem
										91 cell
											92 text No arbitrary-data, arbitrary-finite-mass Coulomb continuation estimate
									93 row
										94 cell
											95 text Junné–Winter–Yoldaş, September 2026 entropy-dissipation paper
										96 cell
											97 text Entropy dissipation can increase, including for perturbations close to equilibrium
										98 cell
											99 text Entropy decrease does not justify assuming that its dissipation decreases
									100 row
										101 cell
											102 text Duong–He, 
											103 text Multi-species kinetic models: GENERIC formulation and Fisher information
										104 cell
											105 text Thermodynamic formulations and Fisher results under collision-kernel assumptions
										106 cell
											107 text Does not supply the missing finite-mass Coulomb theorem
								108 container
									109 button Copy table
									110 pop up button (collapsed) Description: Expand table, Secondary Actions: Expand
								111 text These distinctions are supported by the theorem statements and the newer paper’s abstract. 
								112 link (collapsed) Value: arxiv.org/html/2512.17905v1?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: Fisher information for the multi-species Landau system, https://arxiv.org/html/2512.17905v1?utm_source=chatgpt.com, 3 additional sources
								113 text  A September 2026 author seminar also describes the recovered global result in the infinite-ion regime. 
								114 link (collapsed) Secondary Actions: Expand, Description: tudelft.nl: [AN] Jonathan Junné: Fisher information and well-posedness for multi-species Landau equation, https://www.tudelft.nl/evenementen/2026/ewi/diam/seminar-in-analysis-and-applications/an-jonathan-junne-fisher-information-and-well-posedness-for-multi-species-landau-equation?utm_source=chatgpt.com, Value: tudelft.nl/evenementen/2026/ewi/diam/seminar-in-analysis-and-applications/an-jonathan-junne-fisher-information-and-well-posedness-for-multi-species-landau-equation?utm_source=chatgpt.com
								115 text The relevant Astra records checked do not supply this missing estimate either. 
								116 link Description: N757, Value: github.com/harjassand/astra-research-knowledge/blob/main/cards/N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition.txt
								117 text  concerns a collision-generator construction with a retained ultraviolet cutoff and supplied regularity. 
								118 link Description: N1763, Value: github.com/harjassand/astra-research-knowledge/blob/main/knowledge/current/packets/N1763.json
								119 text  concerns the different Landau–Fermi–Dirac equation within an already-supplied global classical solution class.
								120 heading 2. Conservation and entropy for your exact normalization, Value: 2
									121 text 2. Conservation and entropy for your exact normalization
								122 text Write
								123 container
									124 text 𝑎 ( 𝑧 ) =
									125 container
										126 text 𝑃 𝑧
									127 container
										128 text ∣ 𝑧 ∣
									129 text , 𝐴 [ 𝑔 ] = 𝑎 ∗ 𝑔 , 𝑏 ( 𝑧 ) = div ⁡ 𝑎 ( 𝑧 ) = −
									130 container
										131 text 2 𝑧
									132 container
										133 text ∣ 𝑧
										134 text ∣
										135 text 3
									136 text .
								137 text Distributionally,
								138 container
									139 text div ⁡ 𝑏 = − 8 𝜋
									140 text 𝛿
									141 text 0
									142 text .
								143 text Your equation therefore has the divergence form
								144 container
									145 container
										146 text ∂
										147 text 𝑡
										148 text 𝑓
										149 text 𝑖
										150 text =
										151 text ∑
										152 text 𝑗
										153 text [
										154 container
											155 text 𝑐
											156 container
												157 text 𝑖 𝑗
											158 text 𝑚
											159 text 𝑖
											160 text 2
										161 text div
										162 text ⁡
										163 text (
										164 text 𝐴
										165 text [
										166 container
											167 text 𝑓 𝑗
										168 text ]
										169 text ∇
										170 container
											171 text 𝑓 𝑖
										172 text )
										173 text −
										174 container
											175 text 𝑐
											176 container
												177 text 𝑖 𝑗
											178 container
												179 text 𝑚 𝑖
											180 container
												181 text 𝑚 𝑗
										182 text div
										183 text ⁡
										184 text (
										185 container
											186 text 𝑓 𝑖
										187 text (
										188 text 𝑏
										189 text ∗
										190 container
											191 text 𝑓 𝑗
										192 text )
										193 text )
										194 text ]
										195 text .
									196 text (2.1)
								197 text Let
								198 container
									199 text 𝑑
									200 container
										201 text 𝑖 𝑗
									202 text ( 𝑣 , 𝑤 ) =
									203 container
										204 text ∇ log ⁡
										205 text 𝑓
										206 text 𝑖
										207 text ( 𝑣 )
									208 container
										209 text 𝑚 𝑖
									210 text −
									211 container
										212 text ∇ log ⁡
										213 text 𝑓
										214 text 𝑗
										215 text ( 𝑤 )
									216 container
										217 text 𝑚 𝑗
									218 text ,
									219 text 𝐹
									220 container
										221 text 𝑖 𝑗
									222 text =
									223 text 𝑓
									224 text 𝑖
									225 text ( 𝑣 )
									226 text 𝑓
									227 text 𝑗
									228 text ( 𝑤 ) .
								229 text On a classical interval, symmetrization gives
								230 container
									231 container
										232 text 𝑑
										233 container
											234 text 𝑑 𝑡
										235 text ∑
										236 text 𝑖
										237 text ∫
										238 text 𝜑
										239 text 𝑖
										240 text 𝑓
										241 text 𝑖
										242 text = −
										243 text 1
										244 text 2
										245 text ∑
										246 container
											247 text 𝑖 , 𝑗
										248 text 𝑐
										249 container
											250 text 𝑖 𝑗
										251 text ∬
										252 text 𝐹
										253 container
											254 text 𝑖 𝑗
										255 text 𝑎 ( 𝑣 − 𝑤 )
										256 text 𝑑
										257 container
											258 text 𝑖 𝑗
										259 text ⋅
										260 text (
										261 container
											262 text ∇
											263 container
												264 text 𝜑 𝑖
											265 text (
											266 text 𝑣
											267 text )
											268 text 𝑚
											269 text 𝑖
										270 text −
										271 container
											272 text ∇
											273 container
												274 text 𝜑 𝑗
											275 text (
											276 text 𝑤
											277 text )
											278 text 𝑚
											279 text 𝑗
										280 text )
										281 text 𝑑 𝑣 𝑑 𝑤 .
									282 text (2.2)
								283 text This directly yields the requested conserved quantities:
								284 content list
									285 container
										286 AXListMarker • 
										287 text Constant test functions give conservation of each 
										288 container
											289 text 𝑛 𝑖
										290 text .
									291 container
										292 AXListMarker • 
										293 text Taking 
										294 container
											295 text 𝜑
											296 text 𝑖
											297 text ( 𝑣 ) =
											298 text 𝑚
											299 text 𝑖
											300 text 𝑣
											301 text ℓ
										302 text  gives conservation of total momentum.
									303 container
										304 AXListMarker • 
										305 text Taking 
										306 container
											307 text 𝜑
											308 text 𝑖
											309 text ( 𝑣 ) =
											310 text 𝑚
											311 text 𝑖
											312 text ∣ 𝑣
											313 text ∣
											314 text 2
											315 text / 2
										316 text  gives conservation of total kinetic energy, because 
										317 container
											318 text 𝑎 ( 𝑧 ) 𝑧 = 0
										319 text .
								320 text Testing the entropy gives
								321 container
									322 container
										323 text −
										324 text 𝑑
										325 container
											326 text 𝑑 𝑡
										327 text ∑
										328 text 𝑖
										329 text ∫
										330 text 𝑓
										331 text 𝑖
										332 text log ⁡
										333 text 𝑓
										334 text 𝑖
										335 text =
										336 text 1
										337 text 2
										338 text ∑
										339 container
											340 text 𝑖 , 𝑗
										341 text 𝑐
										342 container
											343 text 𝑖 𝑗
										344 text ∬
										345 container
											346 text 𝐹
											347 text 𝑖
											348 text 𝑗
										349 container
											350 text ∣ 𝑣 − 𝑤 ∣
										351 text ∣
										352 text 𝑃
										353 container
											354 text 𝑣 − 𝑤
										355 text 𝑑
										356 container
											357 text 𝑖 𝑗
										358 text ∣
										359 text 2
										360 text 𝑑 𝑣 𝑑 𝑤 .
									361 text (2.3)
								362 text Since 
								363 container
									364 text 𝐷
									365 text 𝑧
									366 text =
									367 text 𝜇
									368 container
										369 text 𝑖 𝑗
									370 text (
									371 text ∇
									372 text 𝑣
									373 text /
									374 text 𝑚
									375 text 𝑖
									376 text −
									377 text ∇
									378 text 𝑤
									379 text /
									380 text 𝑚
									381 text 𝑗
									382 text )
								383 text , this is exactly
								384 container
									385 container
										386 text 𝐷
										387 text 𝐻
										388 text ( 𝑓 ) =
										389 text 1
										390 text 2
										391 text ∑
										392 container
											393 text 𝑖 , 𝑗
										394 text 𝑐
										395 container
											396 text 𝑖 𝑗
										397 text 𝜇
										398 container
											399 text 𝑖 𝑗
										400 container
											401 text − 2
										402 text 𝐽
										403 container
											404 text 𝑖 𝑗
										405 text .
									406 text (2.4)
								407 text These identities retain the actual particle numbers; no unit-mass normalization is implicit. For a useful nonnegative entropy, set
								408 container
									409 text 𝜌 =
									410 text ∑
									411 text 𝑖
									412 text 𝑚
									413 text 𝑖
									414 text 𝑛
									415 text 𝑖
									416 text , 𝑢 =
									417 text 𝑃
									418 text 𝜌
									419 text , Θ =
									420 container
										421 text 2 𝐸 − ∣ 𝑃
										422 text ∣
										423 text 2
										424 text / 𝜌
									425 container
										426 text 3 (
										427 text 𝑛
										428 text 1
										429 text +
										430 text 𝑛
										431 text 2
										432 text )
									433 text .
								434 text The assumptions imply 
								435 container
									436 text Θ > 0
								437 text . Define
								438 container
									439 text 𝑀
									440 text 𝑖
									441 text ( 𝑣 ) =
									442 text 𝑛
									443 text 𝑖
									444 container
										445 text (
										446 container
											447 text 𝑚 𝑖
										448 container
											449 text 2 𝜋 Θ
										450 text )
									451 container
										452 text 3 / 2
									453 text exp ⁡  ⁣
									454 text (
									455 text −
									456 container
										457 container
											458 text 𝑚 𝑖
										459 text ∣
										460 text 𝑣
										461 text −
										462 text 𝑢
										463 container
											464 text ∣ 2
										465 text 2
										466 text Θ
									467 text )
									468 text .
								469 text Then
								470 container
									471 text 𝐻 ( 𝑓 ∣ 𝑀 ) =
									472 text ∑
									473 text 𝑖
									474 text ∫
									475 text 𝑓
									476 text 𝑖
									477 text log ⁡
									478 container
										479 text 𝑓 𝑖
									480 container
										481 text 𝑀 𝑖
									482 text ≥ 0 ,
								483 text and, on the classical interval,
								484 container
									485 container
										486 text 𝐻 ( 𝑓 ( 𝑡 ) ∣ 𝑀 ) +
										487 text ∫
										488 text 0
										489 text 𝑡
										490 text 𝐷
										491 text 𝐻
										492 text ( 𝑓 ( 𝑠 ) ) 𝑑 𝑠 = 𝐻 (
										493 text 𝑓
										494 text 0
										495 text ∣ 𝑀 ) .
									496 text (2.5)
								497 text Thus entropy supplies a finite time integral of 
								498 container
									499 text 𝐷 𝐻
								500 text . It does not yet supply a supremum bound for Fisher information or another continuation norm.
								501 heading 3. An explicit Fisher-to-continuation estimate, Value: 2
									502 text 3. An explicit Fisher-to-continuation estimate
								503 text Here is a closed conditional implication. Its hypothesis is precisely identified so that it cannot be mistaken for the missing global estimate. Let 
								504 container
									505 text 𝑇 ∗
								506 text  be the maximal time of the local strong solution. Suppose, for some finite 
								507 container
									508 text 𝑇 ≤
									509 text 𝑇
									510 text ∗
								511 text ,
								512 container
									513 container
										514 text 𝑆
										515 text 𝑇
										516 text : =
										517 container
											518 text sup ⁡
										519 container
											520 text 0 ≤ 𝑡 < 𝑇
										521 text 𝐼
										522 text 𝑚
										523 text ( 𝑓 ( 𝑡 ) ) < ∞ .
									524 text (3.1)
								525 text Define
								526 container
									527 text 𝑀
									528 text 𝑞
									529 text ( 𝑡 ) =
									530 text ∑
									531 container
										532 text 𝑖 = 1
									533 text 2
									534 text 𝑚
									535 text 𝑖
									536 text ∫
									537 text 𝑓
									538 text 𝑖
									539 text ( 𝑡 , 𝑣 ) ⟨ 𝑣
									540 text ⟩
									541 text 𝑞
									542 text 𝑑 𝑣 , ⟨ 𝑣 ⟩ = ( 1 + ∣ 𝑣
									543 text ∣
									544 text 2
									545 text )
									546 container
										547 text 1 / 2
									548 text .
								549 text I will derive a bound for
								550 container
									551 text 𝑌
									552 text 7
									553 text ( 𝑡 ) =
									554 text ∑
									555 text 𝑖
									556 text ∫
									557 text 𝑓
									558 text 𝑖
									559 text ( 𝑡 , 𝑣
									560 text )
									561 text 2
									562 text ⟨ 𝑣
									563 text ⟩
									564 text 7
									565 text 𝑑 𝑣 ,
								566 text which is a weighted 
								567 container
									568 text 𝐿 2
								569 text  quantity of the type used by the local strong theory.
								570 heading 3.1 Fisher information controls , Value: 3
									571 text 3.1 Fisher information controls 
									572 container
										573 text 𝐿 3
								574 text Let 
								575 container
									576 text 𝐶 𝑆
								577 text  satisfy
								578 container
									579 text ∥ ℎ
									580 text ∥
									581 container
										582 text 𝐿 6
									583 text 2
									584 text ≤
									585 text 𝐶
									586 text 𝑆
									587 text ∥ ∇ ℎ
									588 text ∥
									589 container
										590 text 𝐿 2
									591 text 2
									592 text .
								593 text Since
								594 container
									595 text 𝐼 ( 𝑓 ) = 4 ∥ ∇
									596 text 𝑓
									597 text ∥
									598 text 2
									599 text 2
									600 text ,
								601 text we have
								602 container
									603 container
										604 text ∥
										605 text 𝑓
										606 text 𝑖
										607 text ∥
										608 text 3
										609 text = ∥
										610 container
											611 text 𝑓 𝑖
										612 text ∥
										613 text 6
										614 text 2
										615 text ≤
										616 container
											617 text 𝐶 𝑆
										618 text 4
										619 text 𝐼 (
										620 text 𝑓
										621 text 𝑖
										622 text ) ≤
										623 container
											624 text 𝐶 𝑆
										625 text 4
										626 text 𝑚
										627 text 𝑖
										628 text 𝑆
										629 text 𝑇
										630 text .
									631 text (3.2)
								632 heading 3.2 An explicit Coulomb-potential bound, Value: 3
									633 text 3.2 An explicit Coulomb-potential bound
								634 text For any 
								635 container
									636 text 𝑅 > 0
								637 text , Hölder’s inequality gives
								638 container
									639 container
										640 text ∫
										641 container
											642 text 𝑓 ( 𝑤 )
										643 container
											644 text ∣ 𝑣 − 𝑤 ∣
										645 text 𝑑 𝑤
									646 container
										647 text ≤ ∥ 𝑓
										648 text ∥
										649 text 3
										650 container
											651 text (
											652 text ∫
											653 container
												654 text ∣ 𝑧 ∣ < 𝑅
											655 text ∣ 𝑧
											656 text ∣
											657 container
												658 text − 3 / 2
											659 text 𝑑 𝑧 )
										660 container
											661 text 2 / 3
										662 text +
										663 text 𝑛
										664 text 𝑅
									665 container
										666 text =
										667 container
											668 text (
											669 container
												670 text 8 𝜋
											671 text 3
											672 text )
										673 container
											674 text 2 / 3
										675 text 𝑅 ∥ 𝑓
										676 text ∥
										677 text 3
										678 text +
										679 text 𝑛
										680 text 𝑅
										681 text .
								682 text Optimizing this elementary bound in 
								683 text 𝑅
								684 text ,
								685 container
									686 text ∥ ∣ ⋅
									687 text ∣
									688 container
										689 text − 1
									690 text ∗ 𝑓
									691 text ∥
									692 text ∞
									693 text ≤ 2
									694 container
										695 text (
										696 container
											697 text 8 𝜋
										698 text 3
										699 text )
									700 container
										701 text 1 / 3
									702 container
										703 text 𝑛 ∥ 𝑓
										704 text ∥
										705 text 3
									706 text .
								707 text Combining with (3.2),
								708 container
									709 container
										710 text ∥ ∣ ⋅
										711 text ∣
										712 container
											713 text − 1
										714 text ∗
										715 text 𝑓
										716 text 𝑖
										717 text ∥
										718 text ∞
										719 text ≤
										720 text 𝐶
										721 text 𝑃
										722 container
											723 text 𝑛
											724 text 𝑖
											725 text 𝑚
											726 text 𝑖
											727 text 𝑆
											728 text 𝑇
										729 text ,
										730 text 𝐶
										731 text 𝑃
										732 text =
										733 container
											734 text (
											735 container
												736 text 8 𝜋
											737 text 3
											738 text )
										739 container
											740 text 1 / 3
										741 container
											742 text 𝐶 𝑆
										743 text .
									744 text (3.3)
								745 heading 3.3 Higher moments then remain bounded, Value: 3
									746 text 3.3 Higher moments then remain bounded
								747 text Put 
								748 container
									749 text 𝜙
									750 text 𝑞
									751 text ( 𝑣 ) = ⟨ 𝑣
									752 text ⟩
									753 text 𝑞
								754 text , 
								755 container
									756 text 𝑞 ≥ 2
								757 text . Applying (2.1), integrating by parts, and symmetrizing gives
								758 container
									759 container
										760 container
											761 text 𝑀
											762 text 𝑞
											763 text ′
											764 text =
											765 text 1
											766 text 2
											767 text ∑
											768 container
												769 text 𝑖 , 𝑗
											770 text 𝑐
											771 container
												772 text 𝑖 𝑗
											773 text ∬
											774 text 𝐹
											775 container
												776 text 𝑖 𝑗
											777 text [
										778 container
											779 text 𝑎 ( 𝑣 − 𝑤 ) :
											780 text (
											781 container
												782 container
													783 text 𝐷 2
												784 container
													785 text 𝜙 𝑞
												786 text (
												787 text 𝑣
												788 text )
												789 text 𝑚
												790 text 𝑖
											791 text +
											792 container
												793 container
													794 text 𝐷 2
												795 container
													796 text 𝜙 𝑞
												797 text (
												798 text 𝑤
												799 text )
												800 text 𝑚
												801 text 𝑗
											802 text )
										803 container
											804 text +
											805 text (
											806 container
												807 text 1
												808 text 𝑚
												809 text 𝑖
											810 text +
											811 container
												812 text 1
												813 text 𝑚
												814 text 𝑗
											815 text )
											816 text 𝑏 ( 𝑣 − 𝑤 ) ⋅ ( ∇
											817 text 𝜙
											818 text 𝑞
											819 text ( 𝑣 ) − ∇
											820 text 𝜙
											821 text 𝑞
											822 text ( 𝑤 ) ) ] .
									823 text (3.4)
								824 text Convexity of 
								825 container
									826 text 𝜙 𝑞
								827 text  makes the second line nonpositive:
								828 container
									829 text 𝑏 ( 𝑣 − 𝑤 ) ⋅ ( ∇
									830 text 𝜙
									831 text 𝑞
									832 text ( 𝑣 ) − ∇
									833 text 𝜙
									834 text 𝑞
									835 text ( 𝑤 ) ) ≤ 0.
								836 text Also,
								837 container
									838 text tr ⁡ 𝑎 ( 𝑧 ) =
									839 text 2
									840 container
										841 text ∣ 𝑧 ∣
									842 text , ∥
									843 text 𝐷
									844 text 2
									845 text 𝜙
									846 text 𝑞
									847 text ( 𝑣 ) ∥ ≤ 𝑞 ( 𝑞 − 1 ) ⟨ 𝑣
									848 text ⟩
									849 container
										850 text 𝑞 − 2
									851 text .
								852 text Consequently,
								853 container
									854 text 𝑀
									855 text 𝑞
									856 text ′
									857 text ≤ 2 𝑞 ( 𝑞 − 1 )
									858 text ∑
									859 container
										860 text 𝑖 , 𝑗
									861 container
										862 text 𝑐
										863 text 𝑖
										864 text 𝑗
									865 container
										866 text 𝑚 𝑖
									867 text ∫
									868 text 𝑓
									869 text 𝑖
									870 text ( 𝑣 ) ⟨ 𝑣
									871 text ⟩
									872 container
										873 text 𝑞 − 2
									874 text ( ∣ ⋅
									875 text ∣
									876 container
										877 text − 1
									878 text ∗
									879 text 𝑓
									880 text 𝑗
									881 text ) ( 𝑣 ) 𝑑 𝑣 .
								882 text Define the finite constant
								883 container
									884 container
										885 text 𝐾
										886 text 𝑞
										887 text = 2 𝑞 ( 𝑞 − 1 )
										888 text 𝐶
										889 text 𝑃
										890 container
											891 text max ⁡
										892 container
											893 text 𝑖 = 1 , 2
										894 text [
										895 container
											896 text 1
											897 text 𝑚
											898 text 𝑖
											899 text 2
										900 container
											901 text ∑
											902 text 𝑗
											903 text =
											904 text 1
											905 text 2
										906 container
											907 text 𝑐
											908 text 𝑖
											909 text 𝑗
										910 container
											911 text 𝑛
											912 text 𝑗
											913 text 𝑚
											914 text 𝑗
										915 text ]
										916 text .
									917 text (3.5)
								918 text Then
								919 container
									920 text 𝑀
									921 text 𝑞
									922 text ′
									923 text ≤
									924 text 𝐾
									925 text 𝑞
									926 container
										927 text 𝑆 𝑇
									928 text 𝑀
									929 container
										930 text 𝑞 − 2
									931 text ≤
									932 text 𝐾
									933 text 𝑞
									934 container
										935 text 𝑆 𝑇
									936 text 𝑀
									937 text 𝑞
									938 text ,
								939 text and hence
								940 container
									941 container
										942 text 𝑀
										943 text 𝑞
										944 text ( 𝑡 ) ≤
										945 text 𝑀
										946 text 𝑞
										947 text ( 0 )
										948 text 𝑒
										949 container
											950 text 𝐾
											951 text 𝑞
											952 container
												953 text 𝑆 𝑇
											954 text 𝑡
										955 text .
									956 text (3.6)
								957 text This argument need not assume that Schwartz tails have already propagated. Smooth convex radial truncations, with a linear continuation outside a large ball, retain the drift sign and allow the estimate to pass to the limit.
								958 heading 3.4 The actual weighted bound, Value: 3
									959 text 3.4 The actual weighted 
									960 container
										961 text 𝐿 2
									962 text  bound
								963 text Cauchy–Schwarz gives
								964 container
									965 container
										966 text ∫
										967 text 𝑓
										968 text 𝑖
										969 text 2
										970 text ⟨ 𝑣
										971 text ⟩
										972 text 7
									973 container
										974 text = ∫ (
										975 text 𝑓
										976 text 𝑖
										977 text 3
										978 text )
										979 container
											980 text 1 / 2
										981 text (
										982 text 𝑓
										983 text 𝑖
										984 text ⟨ 𝑣
										985 text ⟩
										986 text 14
										987 text )
										988 container
											989 text 1 / 2
									990 container
										991 text ≤ ∥
										992 text 𝑓
										993 text 𝑖
										994 text ∥
										995 text 3
										996 container
											997 text 3 / 2
										998 container
											999 text ( ∫
											1000 text 𝑓
											1001 text 𝑖
											1002 text ⟨ 𝑣
											1003 text ⟩
											1004 text 14
											1005 text )
										1006 container
											1007 text 1 / 2
										1008 text .
								1009 text Therefore
								1010 container
									1011 container
										1012 text 𝑌
										1013 text 7
										1014 text ( 𝑡 ) ≤
										1015 container
											1016 text (
											1017 container
												1018 text 𝐶 𝑆
											1019 text 4
											1020 text )
										1021 container
											1022 text 3 / 2
										1023 text (
										1024 text 𝑚
										1025 text 1
										1026 text +
										1027 text 𝑚
										1028 text 2
										1029 text )
										1030 text 𝑆
										1031 text 𝑇
										1032 container
											1033 text 3 / 2
										1034 container
											1035 text 𝑀
											1036 text 14
											1037 text ( 0 )
										1038 text exp ⁡  ⁣
										1039 text (
										1040 container
											1041 container
												1042 text 𝐾 14
											1043 container
												1044 text 𝑆 𝑇
											1045 text 𝑡
											1046 text 2
										1047 text )
										1048 text .
									1049 text (3.7)
								1050 text The local weighted-
								1051 container
									1052 text 𝐿 2
								1053 text  strong theory can be restarted from these bounds, together with the fixed particle numbers, masses, coefficients, energy and entropy bounds. Its relevant local statement is Lemma 2.7 of Junné–Winter–Yoldaş. 
								1054 link (collapsed) Value: arxiv.org/html/2512.17082v1?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: On the existence of solutions to the multi-species Landau equation, https://arxiv.org/html/2512.17082v1?utm_source=chatgpt.com
								1055 text For nonunit particle numbers, the normalization 
								1056 container
									1057 text 𝑓
									1058 text 𝑖
									1059 text =
									1060 text 𝑛
									1061 text 𝑖
									1062 text 𝑔
									1063 text 𝑖
								1064 text  gives effective coefficients 
								1065 container
									1066 text 𝑐
									1067 container
										1068 text 𝑖 𝑗
									1069 text 𝑛
									1070 text 𝑗
								1071 text . These satisfy weighted detailed balance,
								1072 container
									1073 text 𝑛
									1074 text 𝑖
									1075 text (
									1076 text 𝑐
									1077 container
										1078 text 𝑖 𝑗
									1079 text 𝑛
									1080 text 𝑗
									1081 text ) =
									1082 text 𝑛
									1083 text 𝑗
									1084 text (
									1085 text 𝑐
									1086 container
										1087 text 𝑗 𝑖
									1088 text 𝑛
									1089 text 𝑖
									1090 text ) ,
								1091 text and the entropy and Fisher quantities retain weights 
								1092 container
									1093 text 𝑛 𝑖
								1094 text . One must preserve these weights when adapting the probability-density formulation. Thus, within this local strong class,
								1095 container
									1096 container
										1097 text 𝑇
										1098 text ∗
										1099 text < ∞ ⟹
										1100 container
											1101 text sup ⁡
										1102 container
											1103 text 𝑡 <
											1104 text 𝑇
											1105 text ∗
										1106 text 𝐼
										1107 text 𝑚
										1108 text ( 𝑓 ( 𝑡 ) ) = ∞ .
									1109 text (3.8)
								1110 container
									1111 text What remains unproved is a bound on 
									1112 container
										1113 text 𝑆 𝑇
									1114 text  from the initial data.
								1115 text  Equation (3.7) proves that such a bound would accomplish continuation; it does not establish that bound.
								1116 heading 4. Fisher information can increase with finite masses, Value: 2
									1117 text 4. Fisher information can increase with finite masses
								1118 text The following auxiliary result strengthens the distinction between a failed functional and a failed Cauchy theorem.
								1119 container
									1120 text Auxiliary conclusion.  There exist strictly finite positive masses, positive symmetric collision coefficients, and strictly positive Schwartz probability densities for which
								1121 container
									1122 container
										1123 text 𝑑
										1124 container
											1125 text 𝑑 𝑡
										1126 text 𝐼
										1127 text 𝑚
										1128 text ( 𝑓 ( 𝑡 ) ) ∣
									1129 container
										1130 text 𝑡 = 0
									1131 text > 0.
								1132 text This does not imply finite-time blowup.
								1133 text Here is a construction in which the final data and masses are all finite.
								1134 heading 4.1 A strictly positive angular seed, Value: 3
									1135 text 4.1 A strictly positive angular seed
								1136 text Let
								1137 container
									1138 text ℎ
									1139 text 𝜎
									1140 text ( 𝑟 ) =
									1141 text 𝑍
									1142 text 𝜎
									1143 container
										1144 text − 1
									1145 text exp ⁡  ⁣
									1146 text [
									1147 text −
									1148 container
										1149 text (
										1150 container
											1151 text 𝑟 2
										1152 text −
										1153 text 1
										1154 container
											1155 text ) 2
										1156 text 𝜎
										1157 text 2
									1158 text ]
									1159 text ,
									1160 text ∫
									1161 container
										1162 text 𝑅 3
									1163 text ℎ
									1164 text 𝜎
									1165 text ( ∣ 𝑣 ∣ ) 𝑑 𝑣 = 1.
								1166 text Choose 
								1167 container
									1168 text 𝜒 ∈
									1169 text 𝐶
									1170 text 𝑐
									1171 text ∞
									1172 text ( ( 1 / 2 , 3 / 2 ) )
								1173 text , equal to 
								1174 text 1
								1175 text  on 
								1176 container
									1177 text [ 3 / 4 , 5 / 4 ]
								1178 text , and set
								1179 container
									1180 text 𝑎
									1181 text 0
									1182 text ( 𝑟 ) = 𝜒 ( 𝑟 )
									1183 text 𝑟
									1184 container
										1185 text 3 / 2
									1186 text , 𝑌 ( 𝜔 ) =
									1187 text 𝜔
									1188 text 1
									1189 text .
								1190 text For small 
								1191 text 𝜀
								1192 text , define
								1193 container
									1194 container
										1195 text 𝑓
										1196 text 𝜀
										1197 text ( 𝑣 ) =
										1198 text 𝑍
										1199 text 𝜀
										1200 container
											1201 text − 1
										1202 text ℎ
										1203 text 𝜎
										1204 text ( ∣ 𝑣 ∣ )
										1205 text 𝑒
										1206 container
											1207 text 𝜀
											1208 text 𝑎
											1209 text 0
											1210 text ( ∣ 𝑣 ∣ ) 𝑌 (
											1211 text 𝑣
											1212 text ^
											1213 text )
										1214 text .
									1215 text (4.1)
								1216 text This is strictly positive and Schwartz. The angular perturbation vanishes near the origin, so it is smooth there. For the auxiliary angular operator
								1217 container
									1218 text 𝐿 𝑓 = div ⁡  ⁣
									1219 text (
									1220 container
										1221 text 𝑃
										1222 text 𝑣
										1223 text ∣
										1224 text 𝑣
										1225 text ∣
									1226 text ∇
									1227 text 𝑓
									1228 text )
									1229 text =
									1230 text 𝑟
									1231 container
										1232 text − 3
									1233 text Δ
									1234 container
										1235 text 𝑆 2
									1236 text 𝑓 ,
								1237 text one obtains
								1238 container
									1239 container
										1240 container
											1241 text ⟨
											1242 text 𝐼
											1243 text ′
											1244 text (
											1245 text 𝑓
											1246 text 𝜀
											1247 text ) , 𝐿
											1248 text 𝑓
											1249 text 𝜀
											1250 text ⟩ =
										1251 container
											1252 text −
											1253 container
												1254 text 16 𝜋
											1255 text 3
											1256 text 𝜀
											1257 text 2
											1258 text ∫
											1259 text 0
											1260 text ∞
											1261 text ℎ
											1262 text 𝜎
											1263 text ( 𝑟 )
											1264 text 𝑟
											1265 container
												1266 text − 3
											1267 text [
											1268 container
												1269 text (
												1270 text 𝑟
												1271 container
													1272 text 𝑎 0 ′
												1273 text (
												1274 text 𝑟
												1275 text )
												1276 text −
												1277 container
													1278 text 3 2
												1279 container
													1280 text 𝑎 0
												1281 text (
												1282 text 𝑟
												1283 text )
												1284 text )
												1285 text 2
											1286 text −
											1287 container
												1288 text 1 4
											1289 container
												1290 text 𝑎 0
											1291 text (
											1292 text 𝑟
											1293 container
												1294 text ) 2
											1295 text ]
											1296 text 𝑑 𝑟
										1297 container
											1298 text + 𝑂 (
											1299 text 𝜀
											1300 text 4
											1301 text ) .
									1302 text (4.2)
								1303 text The constants follow from
								1304 container
									1305 text ∫
									1306 container
										1307 text 𝑆 2
									1308 text ∣ ∇ 𝑌
									1309 text ∣
									1310 text 2
									1311 text =
									1312 container
										1313 text 8 𝜋
									1314 text 3
									1315 text ,
									1316 text ∫
									1317 container
										1318 text 𝑆 2
									1319 text Γ
									1320 text 2
									1321 text ( 𝑌 ) =
									1322 container
										1323 text 16 𝜋
									1324 text 3
									1325 text .
								1326 text For fixed 
								1327 text 𝜎
								1328 text , the remainder is bounded by a finite constant times 
								1329 container
									1330 text 𝜀 4
								1331 text ; the expression is even in 
								1332 text 𝜀
								1333 text . Where 
								1334 container
									1335 text 𝜒 = 1
								1336 text , the bracket in (4.2) equals 
								1337 container
									1338 text −
									1339 text 𝑟
									1340 text 3
									1341 text / 4
								1342 text . The cutoff-transition contribution is exponentially small as 
								1343 container
									1344 text 𝜎 ↓ 0
								1345 text , and the integral tends to
								1346 container
									1347 text −
									1348 text 1
									1349 container
										1350 text 16 𝜋
									1351 text .
								1352 text Choose 
								1353 container
									1354 text 𝜎 > 0
								1355 text  small enough and then 
								1356 container
									1357 text 𝜀 > 0
								1358 text  small enough. This gives a fixed strictly positive Schwartz density 
								1359 text 𝑓
								1360 text  such that
								1361 container
									1362 container
										1363 text 𝐴
										1364 text 0
										1365 text : = ⟨
										1366 text 𝐼
										1367 text ′
										1368 text ( 𝑓 ) , 𝐿 𝑓 ⟩ > 0.
									1369 text (4.3)
								1370 heading 4.2 Replace the concentrated background by a smooth density, Value: 3
									1371 text 4.2 Replace the concentrated background by a smooth density
								1372 text Let 
								1373 container
									1374 text 𝑔 𝛿
								1375 text  be a centered Gaussian probability density with variance tending to zero as 
								1376 container
									1377 text 𝛿 ↓ 0
								1378 text . Set
								1379 container
									1380 text 𝐴
									1381 text 𝛿
									1382 text =
									1383 text ⟨
									1384 container
										1385 text 𝐼 ′
									1386 text (
									1387 text 𝑓
									1388 text )
									1389 text ,
									1390 text div
									1391 text ⁡
									1392 text (
									1393 text 𝐴
									1394 text [
									1395 container
										1396 text 𝑔 𝛿
									1397 text ]
									1398 text ∇
									1399 text 𝑓
									1400 text )
									1401 text ⟩
									1402 text .
								1403 text Then
								1404 container
									1405 container
										1406 text 𝐴
										1407 text 𝛿
										1408 text ⟶
										1409 text 𝐴
										1410 text 0
										1411 text .
									1412 text (4.4)
								1413 text For this particular 
								1414 text 𝑓
								1415 text , convergence follows directly from the unsplit first variation. Write
								1416 container
									1417 text Ψ
									1418 text 𝑓
									1419 text = − 2 Δ log ⁡ 𝑓 − ∣ ∇ log ⁡ 𝑓
									1420 text ∣
									1421 text 2
									1422 text ,
									1423 text 𝐼
									1424 text ′
									1425 text ( 𝑓 ) [ 𝑞 ] = ∫
									1426 text Ψ
									1427 text 𝑓
									1428 text 𝑞 .
								1429 text Then
								1430 container
									1431 text 𝐴
									1432 text 𝛿
									1433 text = ∫
									1434 text 𝑔
									1435 text 𝛿
									1436 text ( 𝑤 )
									1437 text 𝐾
									1438 text 𝑓
									1439 text ( 𝑤 ) 𝑑 𝑤 ,
								1440 text where
								1441 container
									1442 text 𝐾
									1443 text 𝑓
									1444 text ( 𝑤 ) = − ∫ 𝑎 ( 𝑣 − 𝑤 ) : [ ∇ 𝑓 ( 𝑣 ) ⊗ ∇
									1445 text Ψ
									1446 text 𝑓
									1447 text ( 𝑣 ) ] 𝑑 𝑣 .
								1448 text The tensor factor is Schwartz, and 
								1449 text 𝑎
								1450 text  is locally integrable. Thus 
								1451 container
									1452 text 𝐾 𝑓
								1453 text  is bounded and continuous, which proves (4.4). Fix one positive 
								1454 text 𝛿
								1455 text  such that 
								1456 container
									1457 text 𝐴 : =
									1458 text 𝐴
									1459 text 𝛿
									1460 text > 0
								1461 text , and write 
								1462 container
									1463 text 𝑔 =
									1464 text 𝑔
									1465 text 𝛿
								1466 text .
								1467 heading 4.3 Fix a finite second mass, Value: 3
									1468 text 4.3 Fix a finite second mass
								1469 text For convenience, define
								1470 container
									1471 text 𝐷
									1472 text ℎ
									1473 text 𝑘 = div ⁡ ( 𝐴 [ ℎ ] ∇ 𝑘 ) ,
									1474 text 𝐹
									1475 text ℎ
									1476 text 𝑘 = div ⁡ ( 𝑘 ( 𝑏 ∗ ℎ ) ) ,
								1477 text and the finite numbers
								1478 container
									1479 text 𝑆
									1480 container
										1481 text =
										1482 text 𝐼
										1483 text ′
										1484 text ( 𝑓 ) [
										1485 text 𝐷
										1486 text 𝑓
										1487 text 𝑓 −
										1488 text 𝐹
										1489 text 𝑓
										1490 text 𝑓 ] ,
									1491 text 𝐵
									1492 container
										1493 text =
										1494 text 𝐼
										1495 text ′
										1496 text ( 𝑓 ) [
										1497 text 𝐹
										1498 text 𝑔
										1499 text 𝑓 ] ,
									1500 text 𝐶
									1501 container
										1502 text =
										1503 text 𝐼
										1504 text ′
										1505 text ( 𝑔 ) [
										1506 text 𝐷
										1507 text 𝑓
										1508 text 𝑔 ] ,
									1509 text 𝐷
									1510 container
										1511 text =
										1512 text 𝐼
										1513 text ′
										1514 text ( 𝑔 ) [
										1515 text 𝐹
										1516 text 𝑓
										1517 text 𝑔 ] .
								1518 text Take
								1519 container
									1520 text 𝑚
									1521 text 1
									1522 text = 1 ,
									1523 text 𝑚
									1524 text 2
									1525 text = 𝑀 ,
									1526 text 𝑐
									1527 text 11
									1528 text =
									1529 text 𝑐
									1530 text 22
									1531 text = 1 ,
									1532 text 𝑐
									1533 text 12
									1534 text =
									1535 text 𝑐
									1536 text 21
									1537 text = 𝑐 .
								1538 text Since 
								1539 text 𝑔
								1540 text  is Gaussian, its same-species collision term vanishes. For the original finite-mass operator, the exact derivative is
								1541 container
									1542 container
										1543 text 𝐼
										1544 text 𝑚
										1545 text ′
										1546 text ( 0 ) = 𝑆 + 𝑐 𝐴 −
										1547 container
											1548 text 𝑐 𝐵
										1549 text 𝑀
										1550 text −
										1551 container
											1552 text 𝑐 𝐷
										1553 container
											1554 text 𝑀 2
										1555 text +
										1556 container
											1557 text 𝑐 𝐶
										1558 container
											1559 text 𝑀 3
										1560 text .
									1561 text (4.5)
								1562 text Choose
								1563 container
									1564 text 𝑐 =
									1565 container
										1566 text ∣ 𝑆 ∣ + 1
									1567 text 𝐴
									1568 text > 0 , 𝐾 = ∣ 𝐵 ∣ + ∣ 𝐶 ∣ + ∣ 𝐷 ∣ .
								1569 text Then 
								1570 container
									1571 text 𝑆 + 𝑐 𝐴 ≥ 1
								1572 text . Any finite
								1573 container
									1574 text 𝑀 > max ⁡ { 1 , 2 𝑐 𝐾 }
								1575 text makes the absolute value of the remaining terms less than 
								1576 container
									1577 text 1 / 2
								1578 text . Therefore
								1579 container
									1580 container
										1581 text 𝐼
										1582 text 𝑚
										1583 text ′
										1584 text ( 0 ) >
										1585 text 1
										1586 text 2
										1587 text .
									1588 text (4.6)
								1589 text The limiting arguments above only select fixed smooth densities and a fixed finite 
								1590 text 𝑀
								1591 text . Equation (4.5), which establishes the final claim, is exact for your collision operator. This rules out universal monotonicity of 
								1592 container
									1593 text 𝐼 𝑚
								1594 text  over the full parameter/data class. A global regularity proof could still allow controlled Fisher growth or use a different quantity.
								1595 heading 5. Why the finite-recoil compensation remains unclosed, Value: 2
									1596 text 5. Why the finite-recoil compensation remains unclosed
								1597 text Your 
								1598 container
									1599 text 𝐽
									1600 text 𝑖
									1601 text 𝑗
								1602 text  quantities have the correct entropy meaning. The unresolved issue is their evolution. In center/relative variables, write
								1603 container
									1604 text 𝐹 =
									1605 text 𝐹
									1606 container
										1607 text 𝑖 𝑗
									1608 text , Ψ = log ⁡ 𝐹 , 𝑟 = ∣ 𝑧 ∣ .
								1609 text Then
								1610 container
									1611 text 𝐽
									1612 container
										1613 text 𝑖 𝑗
									1614 text = ∫ 𝐹
									1615 text 𝑟
									1616 container
										1617 text − 3
									1618 text ∣
									1619 text ∇
									1620 container
										1621 text 𝑆 2
									1622 text Ψ
									1623 text ∣
									1624 text 2
									1625 text 𝑑 𝑍 𝑑 𝑧 .
								1626 text Its first variation is
								1627 container
									1628 container
										1629 container
											1630 text 𝛿
											1631 text 𝐽
											1632 container
												1633 text 𝑖 𝑗
										1634 container
											1635 text 𝛿 𝐹
										1636 text = −
										1637 text 𝑟
										1638 container
											1639 text − 3
										1640 text (
										1641 text 2
										1642 container
											1643 text Δ
											1644 text 𝑆
											1645 text 2
										1646 text Ψ
										1647 text +
										1648 text ∣
										1649 container
											1650 text ∇
											1651 text 𝑆
											1652 text 2
										1653 text Ψ
										1654 container
											1655 text ∣ 2
										1656 text )
										1657 text = :
										1658 text Φ
										1659 container
											1660 text 𝑖 𝑗
										1661 text .
									1662 text (5.1)
								1663 text Along the actual mixture,
								1664 container
									1665 text ∂
									1666 text 𝑡
									1667 text 𝐹
									1668 container
										1669 text 𝑖 𝑗
									1670 text =
									1671 text ∑
									1672 text 𝑘
									1673 text [
									1674 container
										1675 text 𝑄
										1676 text 𝑖
										1677 text 𝑘
									1678 text (
									1679 container
										1680 text 𝑓 𝑖
									1681 text ,
									1682 container
										1683 text 𝑓 𝑘
									1684 text )
									1685 text (
									1686 text 𝑣
									1687 text )
									1688 container
										1689 text 𝑓 𝑗
									1690 text (
									1691 text 𝑤
									1692 text )
									1693 text +
									1694 container
										1695 text 𝑓 𝑖
									1696 text (
									1697 text 𝑣
									1698 text )
									1699 container
										1700 text 𝑄
										1701 text 𝑗
										1702 text 𝑘
									1703 text (
									1704 container
										1705 text 𝑓 𝑗
									1706 text ,
									1707 container
										1708 text 𝑓 𝑘
									1709 text )
									1710 text (
									1711 text 𝑤
									1712 text )
									1713 text ]
									1714 text .
								1715 text Consequently,
								1716 container
									1717 container
										1718 text 𝑑
										1719 container
											1720 text 𝑑 𝑡
										1721 text 𝐽
										1722 container
											1723 text 𝑖 𝑗
										1724 text =
										1725 text ∑
										1726 text 𝑘
										1727 text ∬
										1728 text Φ
										1729 container
											1730 text 𝑖 𝑗
										1731 text [
										1732 container
											1733 text 𝑄
											1734 text 𝑖
											1735 text 𝑘
										1736 text (
										1737 container
											1738 text 𝑓 𝑖
										1739 text ,
										1740 container
											1741 text 𝑓 𝑘
										1742 text )
										1743 text (
										1744 text 𝑣
										1745 text )
										1746 container
											1747 text 𝑓 𝑗
										1748 text (
										1749 text 𝑤
										1750 text )
										1751 text +
										1752 container
											1753 text 𝑓 𝑖
										1754 text (
										1755 text 𝑣
										1756 text )
										1757 container
											1758 text 𝑄
											1759 text 𝑗
											1760 text 𝑘
										1761 text (
										1762 container
											1763 text 𝑓 𝑗
										1764 text ,
										1765 container
											1766 text 𝑓 𝑘
										1767 text )
										1768 text (
										1769 text 𝑤
										1770 text )
										1771 text ]
										1772 text 𝑑 𝑣 𝑑 𝑤 .
									1773 text (5.2)
								1774 text Substituting the collision operators introduces mixed triple integrals. Both groups in (5.2) matter for finite recoil. A proposed functional such as
								1775 container
									1776 text 𝐼
									1777 text 𝑚
									1778 text +
									1779 text ∑
									1780 container
										1781 text 𝑖 , 𝑗
									1782 text 𝑎
									1783 container
										1784 text 𝑖 𝑗
									1785 text 𝐽
									1786 container
										1787 text 𝑖 𝑗
									1788 text + 𝑅 𝐻 ( 𝑓 ∣ 𝑀 )
								1789 text therefore needs an estimate for those mixed terms. The entropy identity controls the time integral of the 
								1790 container
									1791 text 𝐽
									1792 text 𝑖
									1793 text 𝑗
								1794 text , while this proposal needs control of their derivatives. The known possibility that entropy dissipation increases prevents replacing that estimate by a monotonicity assertion. 
								1795 link (collapsed) Value: arxiv.org/abs/2609.03847?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: A counterexample to McKean's conjecture for the Landau-Coulomb equation, https://arxiv.org/abs/2609.03847?utm_source=chatgpt.com
								1796 text There is also an endpoint integrability issue. For generic cross-species data near 
								1797 container
									1798 text 𝑧 = 0
								1799 text , the completed-square Fisher decomposition has pieces with logarithmically divergent integrals. Their cancellation must be retained. The finite-mass construction above uses the unsplit first variation and avoids subtracting separately divergent expressions. I have not obtained the required estimate for (5.2).
								1800 heading 6. An alternative functional with a precise remaining inequality, Value: 2
									1801 text 6. An alternative functional with a precise remaining inequality
								1802 text I also pursued a different representation that measures regularity below one full derivative. For 
								1803 container
									1804 text 0 < 𝑠 < 1
								1805 text , let
								1806 container
									1807 text 𝑃
									1808 text 𝜏
									1809 container
										1810 text ( 𝑖 )
									1811 text =
									1812 text 𝑒
									1813 container
										1814 text ( 𝜏 /
										1815 text 𝑚
										1816 text 𝑖
										1817 text ) Δ
								1818 text be an auxiliary Gaussian heat flow, and define
								1819 container
									1820 container
										1821 text 𝐸
										1822 text 𝑠
										1823 text ( 𝑓 ) = 𝑠 ( 1 − 𝑠 )
										1824 text ∑
										1825 text 𝑖
										1826 text ∫
										1827 text 0
										1828 text ∞
										1829 text [
										1830 text 𝐻
										1831 text (
										1832 container
											1833 text 𝑓 𝑖
										1834 text )
										1835 text −
										1836 text 𝐻
										1837 text (
										1838 container
											1839 text 𝑃 𝜏
											1840 text (
											1841 text 𝑖
											1842 text )
										1843 container
											1844 text 𝑓 𝑖
										1845 text )
										1846 text ]
										1847 container
											1848 text 𝑑 𝜏
										1849 container
											1850 text 𝜏
											1851 text 1
											1852 text +
											1853 text 𝑠
										1854 text .
									1855 text (6.1)
								1856 text Here 
								1857 text 𝜏
								1858 text  is auxiliary heat time, distinct from the physical collision time.
								1859 heading 6.1 Its initial value is controlled by the supplied data, Value: 3
									1860 text 6.1 Its initial value is controlled by the supplied data
								1861 text The heat entropy identity gives
								1862 container
									1863 text 𝐸
									1864 text 𝑠
									1865 text ( 𝑓 ) = ( 1 − 𝑠 )
									1866 text ∫
									1867 text 0
									1868 text ∞
									1869 text 𝜏
									1870 container
										1871 text − 𝑠
									1872 text 𝐼
									1873 text 𝑚
									1874 text (
									1875 text 𝑃
									1876 text 𝜏
									1877 text 𝑓 ) 𝑑 𝜏 .
								1878 text Set
								1879 container
									1880 text 𝑁 =
									1881 text 𝑛
									1882 text 1
									1883 text +
									1884 text 𝑛
									1885 text 2
									1886 text , 𝐾 =
									1887 container
										1888 text 3 𝑁
									1889 text 2
									1890 text ,
									1891 text 𝐼
									1892 text 0
									1893 text =
									1894 text 𝐼
									1895 text 𝑚
									1896 text ( 𝑓 ) .
								1897 text The heat-flow estimates
								1898 container
									1899 text 𝐼
									1900 text 𝑚
									1901 text (
									1902 text 𝑃
									1903 text 𝜏
									1904 text 𝑓 ) ≤ min ⁡
									1905 text {
									1906 container
										1907 text 𝐼 0
									1908 text ,
									1909 container
										1910 text 𝐾 𝜏
									1911 text }
								1912 text yield, by splitting at 
								1913 container
									1914 text 𝜏 = 𝐾 /
									1915 text 𝐼
									1916 text 0
								1917 text ,
								1918 container
									1919 container
										1920 text 0 ≤
										1921 text 𝐸
										1922 text 𝑠
										1923 text ( 𝑓 ) ≤
										1924 container
											1925 text 𝐾
											1926 container
												1927 text 1 − 𝑠
											1928 text 𝐼
											1929 text 0
											1930 text 𝑠
										1931 text 𝑠
										1932 text .
									1933 text (6.2)
								1934 text Thus this candidate is finite for every datum in your question.
								1935 heading 6.2 It controls fractional regularity, Value: 3
									1936 text 6.2 It controls fractional regularity
								1937 text The entropy Jensen gap bounds
								1938 container
									1939 text 𝐻 ( 𝑓 ) − 𝐻 (
									1940 text 𝑃
									1941 text 𝜏
									1942 text 𝑓 ) ≥ ∥
									1943 text 𝑓
									1944 text ∥
									1945 text 2
									1946 text 2
									1947 text − ∥
									1948 text 𝑃
									1949 text 𝜏
									1950 text 𝑓
									1951 text ∥
									1952 text 2
									1953 text 2
									1954 text .
								1955 text Integrating in 
								1956 text 𝜏
								1957 text  gives
								1958 container
									1959 container
										1960 text 𝐸
										1961 text 𝑠
										1962 text ( 𝑓 ) ≥
										1963 text 2
										1964 text 𝑠
										1965 text Γ ( 2 − 𝑠 )
										1966 text ∑
										1967 text 𝑖
										1968 text 𝑚
										1969 text 𝑖
										1970 container
											1971 text − 𝑠
										1972 text ∥
										1973 container
											1974 text 𝑓 𝑖
										1975 text ∥
										1976 container
											1977 text 𝐻
											1978 text ˙
											1979 text 𝑠
										1980 text 2
										1981 text .
									1982 text (6.3)
								1983 text The Fourier convention here gives 
								1984 container
									1985 text − Δ
								1986 text  the multiplier 
								1987 container
									1988 text ∣ 𝜉
									1989 text ∣
									1990 text 2
								1991 text . Fractional Sobolev embedding then controls
								1992 container
									1993 container
										1994 text 𝑓
										1995 text 𝑖
										1996 text ∈
										1997 text 𝐿
										1998 container
											1999 text 𝑝 𝑠
										2000 text ,
										2001 text 𝑝
										2002 text 𝑠
										2003 text =
										2004 text 3
										2005 container
											2006 text 3 − 2 𝑠
										2007 text .
									2008 text (6.4)
								2009 text In particular, 
								2010 container
									2011 text 𝑠 > 1 / 2
								2012 text  gives 
								2013 container
									2014 text 𝑝
									2015 text 𝑠
									2016 text > 3 / 2
								2017 text , making this functional relevant to continuation. It also has the needed product structure: it tensorizes on probability products and is marginal-superadditive, because independent heat channels decrease mutual information. Its first variation at a product is additive across the velocity blocks. These properties are established calculations. They do not imply dissipation under Landau collisions.
								2018 heading 6.3 The exact collision term whose sign is missing, Value: 3
									2019 text 6.3 The exact collision term whose sign is missing
								2020 text For a pair, let
								2021 container
									2022 text 𝐹 =
									2023 text 𝑓
									2024 text 𝑖
									2025 text ( 𝑣 )
									2026 text 𝑓
									2027 text 𝑗
									2028 text ( 𝑤 ) , 𝛼 ( 𝑧 ) = ∣ 𝑧
									2029 text ∣
									2030 container
										2031 text − 3
									2032 text .
								2033 text Choose the three rotation fields
								2034 container
									2035 text 𝑏
									2036 text 𝑘
									2037 text ( 𝑧 ) ∈ {
									2038 text 𝑒
									2039 text 1
									2040 text × 𝑧 ,
									2041 text 𝑒
									2042 text 2
									2043 text × 𝑧 ,
									2044 text 𝑒
									2045 text 3
									2046 text × 𝑧 } ,
								2047 text and define
								2048 container
									2049 text 𝐿
									2050 text 𝑘
									2051 text =
									2052 container
										2053 text 𝑏
										2054 text 𝑘
										2055 text ( 𝑧 ) ⋅
										2056 text ∇
										2057 text 𝑣
									2058 container
										2059 text 𝑚 𝑖
									2060 text −
									2061 container
										2062 text 𝑏
										2063 text 𝑘
										2064 text ( 𝑧 ) ⋅
										2065 text ∇
										2066 text 𝑤
									2067 container
										2068 text 𝑚 𝑗
									2069 text ,
									2070 text 𝑞
									2071 text 𝑘
									2072 text =
									2073 text 𝐿
									2074 text 𝑘
									2075 text log ⁡ 𝐹 .
								2076 text The pair heat semigroup
								2077 container
									2078 text 𝑃
									2079 text 𝜏
									2080 text =
									2081 text 𝑒
									2082 container
										2083 text 𝜏 (
										2084 text Δ
										2085 text 𝑣
										2086 text /
										2087 text 𝑚
										2088 text 𝑖
										2089 text +
										2090 text Δ
										2091 text 𝑤
										2092 text /
										2093 text 𝑚
										2094 text 𝑗
										2095 text )
								2096 text commutes with each 
								2097 container
									2098 text 𝐿 𝑘
								2099 text . For sufficiently regular profiles, first restricting the auxiliary heat integral to a compact interval, the entropy-gap calculation gives the pair expression
								2100 container
									2101 container
										2102 text 𝐵
										2103 container
											2104 text 𝑖 𝑗 , 𝑘
										2105 text ( 𝜏 ) = ∫ 𝛼 𝐹
										2106 text 𝑞
										2107 text 𝑘
										2108 text 2
										2109 text − ∫
										2110 container
											2111 text 𝑃
											2112 text 𝜏
											2113 text ( 𝛼 𝐹
											2114 text 𝑞
											2115 text 𝑘
											2116 text )
											2117 text 𝑃
											2118 text 𝜏
											2119 text ( 𝐹
											2120 text 𝑞
											2121 text 𝑘
											2122 text )
										2123 container
											2124 text 𝑃
											2125 text 𝜏
											2126 text 𝐹
										2127 text .
									2128 text (6.5)
								2129 text After assembling ordered pairs, the corresponding formal full-range identity is
								2130 container
									2131 container
										2132 text 𝑑
										2133 container
											2134 text 𝑑 𝑡
										2135 text 𝐸
										2136 text 𝑠
										2137 text ( 𝑓 ( 𝑡 ) ) = −
										2138 container
											2139 text 𝑠 ( 1 − 𝑠 )
										2140 text 2
										2141 text ∑
										2142 container
											2143 text 𝑖 , 𝑗
										2144 text 𝑐
										2145 container
											2146 text 𝑖 𝑗
										2147 text ∑
										2148 text 𝑘
										2149 text ∫
										2150 text 0
										2151 text ∞
										2152 text 𝐵
										2153 container
											2154 text 𝑖 𝑗 , 𝑘
										2155 text ( 𝜏 )
										2156 container
											2157 text 𝑑 𝜏
										2158 container
											2159 text 𝜏
											2160 text 1
											2161 text +
											2162 text 𝑠
										2163 text .
									2164 text (6.6)
								2165 text Passing from truncated auxiliary intervals to (6.6) requires appropriate bounds; it is not an additional regularity assumption that can be inserted into a global proof without justification. For constant 
								2166 text 𝛼
								2167 text , a contraction argument gives the desired sign. For Coulomb, the two numerator factors in (6.5) contain different weights. The radial coefficient does not commute with heat. A naive weighted Cauchy–Schwarz argument introduces 
								2168 container
									2169 text 𝑃
									2170 text 𝜏
									2171 text ( 𝛼 𝐹 )
								2172 text , which is generally divergent at 
								2173 container
									2174 text 𝑧 = 0
								2175 text . In contrast,
								2176 container
									2177 text 𝛼 𝐹
									2178 text 𝑞
									2179 text 𝑘
									2180 text = 𝑂 ( ∣ 𝑧
									2181 text ∣
									2182 container
										2183 text − 2
									2184 text ) , 𝛼 𝐹
									2185 text 𝑞
									2186 text 𝑘
									2187 text 2
									2188 text = 𝑂 ( ∣ 𝑧
									2189 text ∣
									2190 container
										2191 text − 1
									2192 text ) ,
								2193 text are locally integrable for smooth product profiles. Preserving those score factors is essential.
								2194 text I have not proved that the integrated expression in (6.6) is nonnegative, or bounded below by a quantity that yields a closed finite-time growth estimate.
								2195 text  Moreover, as 
								2196 container
									2197 text 𝑠 ↑ 1
								2198 text , the normalized functional approaches 
								2199 container
									2200 text 𝐼 𝑚
								2201 text ; the strict Fisher-growth examples prevent simply asserting monotonicity for all 
								2202 text 𝑠
								2203 text  close to one.
								2204 heading 7. The remaining mathematical obligation, Value: 2
									2205 text 7. The remaining mathematical obligation
								2206 text The explicit continuation calculation reduces one sufficient route to proving
								2207 container
									2208 container
										2209 text sup ⁡
									2210 container
										2211 text 0 ≤ 𝑡 < 𝑇
									2212 text 𝐼
									2213 text 𝑚
									2214 text ( 𝑓 ( 𝑡 ) ) ≤
									2215 text 𝐵
									2216 text 𝑇
									2217 text  ⁣
									2218 text (
									2219 container
										2220 text 𝑚 𝑖
									2221 text ,
									2222 container
										2223 text 𝑐
										2224 text 𝑖
										2225 text 𝑗
									2226 text ,
									2227 container
										2228 text 𝑛 𝑖
									2229 text ,
									2230 text 𝐸
									2231 text ,
									2232 text 𝐻
									2233 text (
									2234 container
										2235 text 𝑓 0
									2236 text ∣
									2237 text 𝑀
									2238 text )
									2239 text ,
									2240 container
										2241 text 𝐼 𝑚
									2242 text (
									2243 container
										2244 text 𝑓 0
									2245 text )
									2246 text ,
									2247 text specified initial weighted norms
									2248 text )
									2249 text < ∞
								2250 text for every finite 
								2251 text 𝑇
								2252 text . An alternative regularity functional could replace Fisher information, but its evolution and continuation implications must both be proved. The heat–entropy construction above supplies a candidate and an exact remaining collision inequality; it does not supply that inequality’s sign.
								2253 text The full affirmative theorem and a genuine negative obstruction both remain unestablished by this work.
								2254 text  The finite-mass Fisher-growth construction eliminates one universal monotonicity claim, while the conditional estimate shows exactly how a successful a priori regularity bound would complete the Cauchy theory.
								2255 button Copy
									2256 image
								2257 pop up button (collapsed) Description: Rate response, ID: radix-_r_1lh_, Secondary Actions: Expand
								2258 checkbox Description: Read aloud, Value: 0
								2259 button Share
								2260 pop up button (collapsed) Description: More actions, ID: radix-_r_1ln_, Secondary Actions: Expand
							2261 container
								2262 text ChatGPT can make mistakes. Check important info.
							2263 container
								2264 button Scroll to bottom
								2265 heading Latest response, Value: 4
									2266 text Latest response
								2267 container
									2268 container
										2269 button (collapsed) Description: Add files and more, Secondary Actions: Expand
										2270 text entry area (settable) Description: Ask ChatGPT, Value: 

											2271 container
												2417 text Ask ChatGPT
										2273 pop up button (collapsed) Description: Select ChatGPT model, ID: radix-_r_51_, Secondary Actions: Expand
											2274 text Pro
										2275 button Dictate
										2276 button Start Voice
						2277 container
							2278 heading Activity, Value: 3
								2279 text Activity
							2280 button 3 used
								2281 text Subagents
								2282 text 3 used
							2283 button (expanded) Outputs, Secondary Actions: Collapse
							2284 text No outputs yet
		2285 text Response complete

The focused UI element is 41 button (expanded) Worked for 21m 24s, Secondary Actions: Collapse
```
