# P3 completed return — finite-mass Landau-Coulomb

Source chat: https://chatgpt.com/c/6af2d882-ab10-83ec-8084-0f7bd9630455
User turn: 2596fb8c-2417-4fd8-86cb-c97ebb884b25
Assistant final: 6ca03f0f-e2fc-5fb0-bc0c-4e18f017aec7
Model: Pro, visible in source chat.
Prompt: work/astra-renewed-pro-programmes-20261103/P3_FULL_FINITE_MASS_LANDAU_INTEGRATED_CONTROL_CONTINUATION_PRO_20261110.txt (SHA-256 679221ff41c0e3b98cd5e1dbc2f8dade6edbb8b58f1419dc8cf7f1efa509de53).
Capture: complete native final; the source page accessibility view was limited to the first 500 history items, so the current turn’s activity is not included here. The original chat retains its visible history. No output ZIP was visible.

## Complete available final

**I have not resolved the full finite-mass Cauchy problem you asked for.** I have neither a proof of global classical well-posedness for the entire stated class nor an admissible finite-mass obstruction to it.

The further investigation did produce two additional estimates: a uniform Fisher bound for the exact isolated two-particle collision semigroup, and a two-sided characterization of \(E_s\) by fractional Sobolev norms of square roots. Neither supplies the missing nonlinear continuation estimate. Below I give the proofs and identify exactly where the transfer to the actual two-species evolution remains unproved.

The primary sources I checked do not close that gap. Junné–Winter–Yoldaş’s finite-mass theorem retains the cross-interaction threshold \(\gamma\ge-\sqrt8\); their Coulomb compensation theorem concerns the infinite-mass model and retains its additional data/coupling condition. Zhu’s spherical criterion likewise does not cover arbitrary Coulomb cross interactions. These statements do not imply a negative answer to your question. :chatgpt-content-reference{index="0"}

## 1. A uniform \(9/8\) Fisher bound for an isolated finite-mass pair

This estimate retains arbitrary positive finite particle masses and the exact Coulomb pair operator.

Fix a pair \(i,j\), and write
\[
M=m_i+m_j,\qquad
\mu=\frac{m_im_j}{M},\qquad
Z=\frac{m_iv+m_jw}{M},\qquad
z=v-w=r\omega.
\]
For a joint density \(F(v,w)\), define
\[
\mathcal I_{ij}(F)
=
\int F\left(
\frac{|\nabla_v\log F|^2}{m_i}
+
\frac{|\nabla_w\log F|^2}{m_j}
\right)\,dv\,dw.
\]

The exact isolated pair generator is
\[
\mathcal A_{ij}
=
\frac{c_{ij}}{\mu^2}\,r^{-3}\Delta_{\mathbb S^2}.
\]
Thus its semigroup is defined, for \(r>0\), by
\[
S_tF(Z,r,\omega)
=
\exp\!\left(
\frac{c_{ij}t}{\mu^2r^3}\Delta_{\mathbb S^2}
\right)F(Z,r,\omega).
\]
It acts on the angular variable while preserving \(Z\) and \(r\).

### Proposition

For every nonnegative finite-mass joint density with finite \(\mathcal I_{ij}\),
\[
\boxed{
\mathcal I_{ij}(S_tF)
\le \frac98\,\mathcal I_{ij}(F),
\qquad t\ge0.
}
\tag{1}
\]
The factor \(9/8\) is independent of \(t,m_i,m_j,c_{ij}\) and the total mass of \(F\).

For an unnormalized product,
\[
\mathcal I_{ij}(f_i\otimes f_j)
=
\frac{n_j}{m_i}I(f_i)+\frac{n_i}{m_j}I(f_j),
\]
so no probability normalization is being silently imposed in (1).

### Proof

Put \(\ell=\log F\). The mass-weighted Euclidean metric decomposes exactly as
\[
\mathcal I_{ij}=I_Z+I_r+I_\omega,
\]
where
\[
I_Z=\frac1M\int F|\nabla_Z\ell|^2,
\qquad
I_r=\frac1\mu\int F|\partial_r\ell|^2,
\qquad
I_\omega=\frac1\mu\int Fr^{-2}|\nabla_{\mathbb S^2}\ell|^2.
\]
Here and below the integration measure is
\[
dZ\,r^2\,dr\,d\omega=dv\,dw.
\]

Consider
\[
\mathcal J_\lambda(F)=I_Z+I_r+\lambda I_\omega,
\qquad \lambda\ge1.
\tag{2}
\]
This is uniformly equivalent to the original Fisher information:
\[
\mathcal I_{ij}(F)
\le \mathcal J_\lambda(F)
\le \lambda\mathcal I_{ij}(F).
\tag{3}
\]

First restrict the integrals to \(\varepsilon<r<R\). Along the isolated pair flow, angular integration by parts gives
\[
\begin{aligned}
\frac{d}{dt}\mathcal J_\lambda(F)
={}&
-\frac{2c_{ij}}{M\mu^2}
\int Fr^{-3}
\bigl|\nabla_{\mathbb S^2}\nabla_Z\ell\bigr|^2
\\
&-\frac{2c_{ij}}{\mu^3}
\int Fr^{-3}
\left|
\nabla_{\mathbb S^2}\partial_r\ell
-\frac{3}{2r}\nabla_{\mathbb S^2}\ell
\right|^2
\\
&-\frac{2c_{ij}}{\mu^3}
\int Fr^{-5}
\left[
\lambda\Gamma_2(\ell)-\frac94\Gamma(\ell)
\right].
\end{aligned}
\tag{4}
\]
On the unit sphere,
\[
\Gamma(\ell)=|\nabla_{\mathbb S^2}\ell|^2,
\qquad
\Gamma_2(\ell)
=
|\nabla_{\mathbb S^2}^2\ell|_{\mathrm{HS}}^2
+
|\nabla_{\mathbb S^2}\ell|^2.
\]

The spherical inequality needed here is the unrestricted one:
\[
\int_{\mathbb S^2}F\Gamma_2(\log F)
\ge
2\int_{\mathbb S^2}F\Gamma(\log F).
\tag{5}
\]
It requires no antipodal symmetry; it is the \(d=3\) case of Zhu’s Lemma 3.2. :chatgpt-content-reference{index="1"}

Consequently, after angular integration, the last line of (4) is nonpositive whenever
\[
2\lambda-\frac94\ge0.
\]
Taking \(\lambda=9/8\) gives
\[
\mathcal J_{9/8}(S_tF)\le \mathcal J_{9/8}(F).
\tag{6}
\]

The treatment of \(r=0\) matters. Equation (4) is used on annuli and integrated in time before removing the annular restrictions. There is no radial integration by parts and hence no radial boundary term. Monotone convergence removes the restrictions in the nonnegative functional \(\mathcal J_\lambda\). This does not assert that the separate terms of (4) have finite integrals at \(r=0\), or that \(\mathcal J_\lambda(S_tF)\) has a finite derivative at \(t=0\).

For general finite-Fisher data, use positive approximations
\[
F_k=\chi_k^2F+\delta_kG,
\]
where \(\chi_k\) are smooth compact cutoffs, \(\delta_k\downarrow0\), and \(G\) is a fixed positive Gaussian. The cutoff error in the square-root gradient is controlled by
\[
\int F|\nabla\chi_k|^2,
\]
which tends to zero with the usual expanding cutoffs; the Gaussian contribution tends to zero by convexity and homogeneity of \(\mathcal J_\lambda\). The angular semigroup contracts \(L^1\). Lower semicontinuity of the quadratic square-root-gradient functional then passes (6) to the limit.

Combining (3) and (6) proves (1).

These cutoffs justify an estimate for the original pair operator; no velocity cutoff remains in the proposition.

## 2. Why that bound does not presently yield the nonlinear theorem

A bound for one application of \(S_t\) does not give a time-uniform bound under repeated collision and marginalization steps. Iterating a factor \(9/8\) over increasingly small time steps provides no useful continuum estimate.

The corrected functional also lacks a property that would allow the standard lifting argument to transfer its monotonicity directly to the marginals. This can be demonstrated explicitly.

For probability marginals, a natural attempted transfer would require
\[
\mathcal J_\lambda(F)
\ge
\mathcal J_\lambda(F_v\otimes F_w),
\tag{7}
\]
with equality at product densities. Inequality (7) is false for every \(\lambda>1\).

This is an obstruction to this particular lifting argument. It is not an obstruction to global classical solutions.

### An explicit fixed-marginal variation

Take
\[
m_i=m_j=1,\qquad \mu=\frac12,
\]
and the strictly positive Gaussian marginals
\[
f_i(v)=(2\pi)^{-3/2}e^{-|v-e_1|^2/2},
\qquad
f_j(w)=(2\pi)^{-3/2}e^{-|w|^2/2}.
\]
Let \(F=f_i\otimes f_j\).

Define
\[
K(F)=\int F|P_z\nabla_z\log F|^2.
\]
Then
\[
\mathcal J_\lambda(F)
=
\mathcal I_{ij}(F)+2(\lambda-1)K(F).
\tag{8}
\]

The first variation of \(K\) at this Gaussian product is
\[
V(z):=\frac{\delta K}{\delta F}
=
\frac{2z_1}{|z|^2}
-\frac14|P_ze_1|^2.
\tag{9}
\]
For example, this follows from
\[
\frac{\delta K}{\delta F}
=
-2\nabla_z\cdot(P_z\nabla_z\log F)
-|P_z\nabla_z\log F|^2,
\]
using
\[
\nabla_z\log F=-\frac12(z-e_1).
\]

Choose the four centers
\[
v_1=0,\qquad v_2=e_1,\qquad
w_1=2e_1,\qquad w_2=3e_1.
\]
Their rectangular difference is exactly
\[
\begin{aligned}
&V(v_1-w_1)-V(v_1-w_2)
-V(v_2-w_1)+V(v_2-w_2)
\\
&\qquad
=-1-\left(-\frac23\right)-(-2)+(-1)
=\frac23.
\end{aligned}
\tag{10}
\]

Let \(\eta\) be a fixed nonnegative smooth bump, supported in the unit ball and equal to one on the half ball. Set
\[
\delta=\frac1{1000},\qquad \eta_\delta(x)=\eta(x/\delta),
\]
and
\[
U(v)=\eta_\delta(v-v_1)-\eta_\delta(v-v_2),
\]
\[
W(w)=\eta_\delta(w-w_1)-\eta_\delta(w-w_2).
\]
Define
\[
g(v,w)=\frac{U(v)W(w)}{F(v,w)}.
\]
This is smooth, bounded and compactly supported. Moreover,
\[
\int F(v,w)g(v,w)\,dw=0,
\qquad
\int F(v,w)g(v,w)\,dv=0.
\tag{11}
\]

The sign in (10) survives these finite bumps with a controlled error. Every relative point in their supports is within \(2\delta\) of its corresponding center, and all intervening segments satisfy \(|z|>1/2\). On that region,
\[
|\nabla V(z)|\le26.
\]
Writing \(Z_\delta=\int\eta_\delta\), we therefore obtain
\[
S:=\int FVg
\ge
\left(\frac23-208\delta\right)Z_\delta^2
=
\frac{172}{375}Z_\delta^2>0.
\tag{12}
\]
This sign uses an exact rectangle calculation and an explicit error bound.

Now put
\[
F_\epsilon=F(1-\epsilon g).
\]
For \(\epsilon\|g\|_\infty<1\), this is a strictly positive Schwartz density. Equation (11) says that its two marginals are exactly \(f_i,f_j\).

The first variation of ordinary joint Fisher information vanishes in this direction: at a product, its variational derivative is the sum of a function of \(v\) and a function of \(w\). Hence, by (8),
\[
\left.\frac{d}{d\epsilon}\mathcal J_\lambda(F_\epsilon)
\right|_{\epsilon=0}
=
-2(\lambda-1)S<0.
\tag{13}
\]

There is also an exact finite-\(\epsilon\) remainder estimate. If
\[
G\ge\|g\|_\infty,\qquad
B=\int F\bigl(|\nabla_vg|^2+|\nabla_wg|^2\bigr),
\]
then, for \(\epsilon G\le1/2\),
\[
\mathcal J_\lambda(F_\epsilon)-\mathcal J_\lambda(F)
\le
-2\epsilon(\lambda-1)S
+2\epsilon^2\lambda B.
\]
Thus any
\[
0<\epsilon\le
\min\left\{
\frac1{2G},
\frac{(\lambda-1)S}{2\lambda B}
\right\}
\]
gives
\[
\mathcal J_\lambda(F_\epsilon)<\mathcal J_\lambda(F).
\tag{14}
\]
The constants can be bounded directly using the fixed bump, its derivative bound, and the Gaussian lower bound on the four compact supports. No optimization or numerical sign determination is involved.

Since \(F_\epsilon\) has the same marginals as \(F\), equation (14) disproves (7). Therefore the isolated-pair estimate does not, through this lifting argument, become a monotone functional for the nonlinear mixture. A different argument could still use it; none has been completed here.

## 3. An additional two-sided characterization of \(E_s\)

The accepted lower bound for \(E_s\) has a converse. In particular, \(E_s\) is equivalent to the squared homogeneous \(H^s\) norm of the square root, with the prescribed particle-mass weights.

For \(0<s<1\), define
\[
C_3
=
\frac6e\left(\frac94\right)^{3/2}
\left[\left(\frac43\right)^{3/2}+1\right].
\]
Then, for the data under consideration,
\[
\boxed{
\begin{aligned}
2^s\Gamma(2-s)
\sum_i m_i^{-s}\|\sqrt{f_i}\|_{\dot H^s}^2
&\le E_s(f)
\\
&\le
\frac{2C_3\,4^s\Gamma(2-s)}{s}
\sum_i m_i^{-s}\|\sqrt{f_i}\|_{\dot H^s}^2.
\end{aligned}}
\tag{15}
\]
The homogeneous Sobolev convention here has Fourier multiplier \(|\xi|^{2s}\).

The lower bound is among your established premises. Here is a proof of the upper bound.

### A Gaussian-kernel estimate

It suffices first to take one species with \(m=1\). Write
\[
g=\sqrt f,\qquad
p_t=P_tf,\qquad
a_t=P_tg,
\]
and let \(K_t\) be the Gaussian heat kernel.

Because \(\int\nabla K_t=0\),
\[
\nabla p_t(x)
=
\int\nabla K_t(z)
\bigl(g(x-z)-a_t(x)\bigr)
\bigl(g(x-z)+a_t(x)\bigr)\,dz.
\tag{16}
\]
Apply Cauchy–Schwarz with weight \(K_{3t/4}\). Its second factor satisfies
\[
\begin{aligned}
\int K_{3t/4}(z)
\bigl(g(x-z)+a_t(x)\bigr)^2\,dz
&\le
2\left[\left(\frac43\right)^{3/2}+1\right]p_t(x),
\end{aligned}
\tag{17}
\]
using \(a_t^2\le p_t\) and the pointwise Gaussian-kernel comparison.

For the first factor, direct calculation gives
\[
\frac{|\nabla K_t(z)|^2}{K_{3t/4}(z)}
\le
\frac{3}{et}\left(\frac94\right)^{3/2}K_{3t}(z).
\tag{18}
\]
Combining (16)–(18), dividing by \(p_t(x)\), and integrating yields
\[
I(P_tf)
\le
\frac{C_3}{t}
\iint K_{3t}(z)
\bigl|g(x-z)-P_tg(x)\bigr|^2\,dz\,dx.
\]
Jensen’s inequality followed by Gaussian convolution gives
\[
\boxed{
I(P_tf)
\le
\frac{C_3}{t}
\iint K_{4t}(x-y)|g(x)-g(y)|^2\,dx\,dy.
}
\tag{19}
\]

### Integration over the auxiliary heat time

Use the exact heat representation
\[
E_s^{(1)}(f)
=
(1-s)\int_0^\infty t^{-s}I(P_tf)\,dt.
\]
By Plancherel,
\[
\iint K_{4t}(x-y)|g(x)-g(y)|^2\,dx\,dy
=
2\int
\bigl(1-e^{-4t|\xi|^2}\bigr)|\widehat g(\xi)|^2\,d\xi.
\]
All relevant integrands are nonnegative, so Tonelli applies. The scalar integral is
\[
\int_0^\infty
t^{-1-s}\bigl(1-e^{-4t|\xi|^2}\bigr)\,dt
=
\frac{4^s\Gamma(1-s)}s|\xi|^{2s}.
\]
Substitution in (19) proves
\[
E_s^{(1)}(f)
\le
\frac{2C_3\,4^s\Gamma(2-s)}s
\|\sqrt f\|_{\dot H^s}^2.
\]
Changing variables from heat time \(t\) to \(t/m\) supplies the factor \(m^{-s}\), proving (15).

For the admitted Schwartz data with finite Fisher information, these calculations are directly justified. More general finite-\(H^s\) square-root data can be handled by the positive-kernel estimate and approximation; no differentiation along the collision evolution is used.

### What this changes

Equation (15) identifies the continuation functional as an equivalent fractional square-root Sobolev quantity. It does **not** give either functional a favorable collision derivative.

In particular, it does not upgrade
\[
\int_0^T E_{7/8}(f(t))^{8/7}\,dt<\infty
\]
to
\[
\sup_{t<T}E_{7/8}(f(t))<\infty.
\]
Nor does equivalence of two functionals transfer monotonicity from one to the other without an additional evolution argument.

## 4. The unresolved continuation step

The actual nonlinear estimates available in your prompt remain stronger than the isolated-pair statements in one essential respect: they hold along the genuine two-species evolution. But their time integrability still falls short of the continuation interface.

This shortfall also appears directly under the exact Coulomb scaling. Set
\[
g_i(s,x)
=
\rho^2f_i(t_0+\rho^2s,v_0+\rho x).
\]
The functions \(g_i\) solve the same collision system with the same \(m_i,c_{ij}\), while
\[
\int g_i(s,x)\,dx=\frac{n_i}{\rho}.
\]
The heat-entropy scaling is
\[
E_s(g(s))
=
\rho^{2s-1}E_s(f(t_0+\rho^2s)).
\]
Consequently,
\[
\int_{-1}^0E_{7/8}(g(s))^{8/7}\,ds
=
\rho^{-8/7}
\int_{t_0-\rho^2}^{t_0}
E_{7/8}(f(t))^{8/7}\,dt.
\tag{20}
\]
Absolute continuity of the established time integral makes the last integral tend to zero, but supplies no prescribed rate that cancels \(\rho^{-8/7}\). Thus it does not itself give a uniformly bounded concentration limit.

The same issue affects an attempt to force a small concentrating core to be Maxwellian using entropy dissipation. Normalizing a core of particle mass \(\nu\) and width \(\varepsilon\) uses
\[
\widehat f_i(s,x)
=
\frac{\varepsilon^3}{\nu}
f_i\!\left(
t_0+\frac{\varepsilon^3}{\nu}s,u+\varepsilon x
\right).
\]
For the exact entropy dissipation,
\[
\int D(\widehat f(s))\,ds
=
\frac1\nu\int D(f(t))\,dt.
\tag{21}
\]
Vanishing dissipation of the normalized core would therefore require an \(o(\nu)\) entropy action on the corresponding original interval. The established finite entropy action provides \(o(1)\), which is insufficient for that conclusion.

Neither scaling observation describes a blowup solution. They locate what a compactness argument would still have to prove.

The remaining requirement is therefore unchanged: an estimate along the **actual nonlinear finite-mass evolution** that either bounds a continuation norm on every finite interval or prevents concentration strongly enough to restart the strong solution. The isolated bound (1), its fractional counterparts, and the equivalence (15) do not provide that estimate.

Accordingly, the conservation laws, entropy inequality, propagated moments and spacetime bounds remain established on the maximal classical interval. I have not proved that its endpoint is infinite, and I have not constructed admissible data for which it is finite. **The requested full global existence-and-uniqueness theorem remains unresolved in this work.**
