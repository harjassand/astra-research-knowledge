P2 completed return; chat https://chatgpt.com/c/6aed7c5f-9954-83ec-8e3e-12eb8200d2f7
Actual prompt source: producer-workspace/P2_FULL_COULOMB_LFD_THERMALIZATION_FINAL_20261108.txt; sent turn 90d5f24c-e899-4f20-9619-56d4824a80f7.
Collected 2026-11-08 UTC. At collection viewer 5.6 Medium; capabilities reduced until November 10; Pro at dispatch, exact response model unconfirmed. No new ZIP supplied. Source/access holds retained, including failed Golding-Henderson and Serre 2024 bodies. Math is transcribed from visible formula annotations.

=== COMPLETE RESPONSE ===

Status: the full same-energy thermalization statement remains unresolved

I have not proved the requested limit
$H(f(t)\mid F_{M,P,E})\longrightarrow0,$
and I have not constructed an admissible nonthermalizing trajectory.

I can establish an unconditional partial convergence theorem within the solution class supplied in your question. It identifies the remaining issue precisely: whether the limiting distribution retains the conserved kinetic energy.

Partial convergence theorem

Write
$\mathcal S(f)
=
-\int_{\mathbb T^3\times\mathbb R^3}
\bigl[f\log f+(1-f)\log(1-f)\bigr]\,dx\,dv.$
For every trajectory in the stipulated class, there is a positive-temperature homogeneous Fermi–Dirac distribution
$F_*(v)
=
\frac{1}{1+\exp\!\left(\alpha_*+\beta_*|v-P/M|^2\right)},
\qquad \beta_*>0,$
such that
$\boxed{
\int \langle v\rangle^q\,|f(t,x,v)-F_*(v)|\,dx\,dv
\longrightarrow0
\quad\text{for every }0\le q<2.
}
\tag{1}$
It has the same mass and momentum, but the argument establishes only
$M_*=M,\qquad P_*=P,\qquad E_*\le E.$
Its entropy is exactly the limiting entropy of the trajectory:
$\mathcal S(F_*)=\lim_{t\to\infty}\mathcal S(f(t)).
\tag{2}$
Consequently, with $F=F_{M,P,E}$ as in the question and
$\Delta=E-E_*\ge0,$
the requested relative entropy has the precise limit
$\boxed{
\lim_{t\to\infty}H(f(t)\mid F)
=
\mathcal S(F)-\mathcal S(F_*)
=
H(F_*\mid F)+\beta\,\Delta.
}
\tag{3}$
Thus the full question is equivalent to proving $\Delta=0$.

No future uniform moment, regularity, or desaturation bound is assumed in this partial theorem. Below I give the conservation and entropy passages, the compactness and rigidity argument, stronger dynamical estimates obtained along the way, and an explicit family showing why the energy issue cannot be dismissed.

1. Conservation and entropy for the actual solution class

All convolutions below are in velocity, at the same spatial point. The collision operator remains spatially local throughout.

Set
$g=f(1-f),\qquad
\ell=\log\frac{f}{1-f},$
and, with exactly the kernel normalization in the question,
$a(z)=\frac{\Pi(z)}{|z|},
\qquad
b(z)=\operatorname{div}a(z)=-\frac{2z}{|z|^3},
\qquad
\operatorname{div}b=-8\pi\delta_0.$
Define
$A_f=a*g,\qquad B_f=b*f,\qquad
J=A_f\nabla_vf-gB_f.$
Then
$(\partial_t+v\cdot\nabla_x)f=\nabla_v\cdot J.
\tag{4}$
The fermionic entropy and collision structure here are classical LFD machinery. Alonso–Bagland–Desvillettes–Lods develop that structure and a homogeneous weighted Fisher-information estimate. Their Theorem 1.8 retains its normalized homogeneous hypotheses; I do not use it as a spatial coercivity theorem. Springer Nature Link

Conservation without assuming derivative tails

For a smooth velocity test $\psi$, integration by parts gives the derivative-free weak identity
$\begin{aligned}
\int \psi(v)Q(f)(v)\,dv
=
\iint f(v)g(w)\Big[
&a(v-w):D^2\psi(v)\\
&+b(v-w)\cdot\bigl(\nabla\psi(v)-\nabla\psi(w)\bigr)
\Big]\,dv\,dw.
\end{aligned}
\tag{5}$
For $\psi=1,v_i,|v|^2$, the bracket vanishes. In the energy case,
$a(z):2I=\frac4{|z|},
\qquad
b(z)\cdot2z=-\frac4{|z|}.$
To justify removing velocity cutoffs, let
$\rho(t,x)=\int f(t,x,v)\,dv,\qquad
e(t,x)=\int |v|^2f(t,x,v)\,dv.$
The cap $f\le1$ implies
$\rho\le C e^{3/5}.
\tag{6}$
Also, splitting the Coulomb potential at radius $\rho^{1/3}$,
$\sup_v\int\frac{f(w)}{|v-w|}\,dw
\le (2\pi+1)\rho^{2/3}.
\tag{7}$
Therefore
$\int_{\mathbb T^3}\iint
\frac{f(v)f(w)}{|v-w|}\,dv\,dw\,dx
\le C\int\rho^{5/3}\,dx
\le C E(t).
\tag{8}$
Cutoffs of the collision invariants have uniformly bounded Hessians, so (8) dominates their collision terms. Before conservation is established, the supplied finite-horizon bounds control $E(t)$ on each finite interval. Dominated convergence in (5), followed by spatial integration over the torus, then proves
$\int f(t)=M,\qquad
\int vf(t)=P,\qquad
\int |v|^2f(t)=E
\tag{9}$
at every finite time.

The exact Coulomb information identity

Define
$I_A(f)=\int
\frac{\nabla f^T A_f\nabla f}{f(1-f)}$
and the entropy dissipation
$D(f)=\frac12\int_{x,v,w}
g(v)g(w)
\frac{
\left|\Pi(v-w)\bigl(\nabla\ell(v)-\nabla\ell(w)\bigr)\right|^2
}{|v-w|}.
\tag{10}$
The Coulomb kernel yields
$\boxed{
D(f)=I_A(f)-8\pi\int f^2.
}
\tag{11}$
In particular,
$I_A(f)\le D(f)+8\pi M.
\tag{12}$
There is a potential circularity here: one should not use (11) to justify an entropy integration by parts that already presupposes $I_A<\infty$. The following cutoff argument avoids it.

For any fixed $p\in(3/5,1)$, the Pauli cap and energy give
$\int f(x,v)^p\,dv\le C_p e(x)^{3/5}.
\tag{13}$
Indeed, splitting at $R$,
$\int_{|v|\le R}f^p\le CR^3,\qquad
\int_{|v|>R}f^p\le C_p e^pR^{3-5p},$
and $R=e^{1/5}$ gives (13).

Together with
$A_f\le Ce^{2/5}I,\qquad |B_f|\le Ce^{1/5},$
and
$g\ell^2+g|\ell|\le C_p f^p,$
this proves
$\int g\ell^2\operatorname{tr}A_f\le CE,
\qquad
\int(f+g|\ell|)|B_f|\le CE^{4/5}.
\tag{14}$
Now take a squared cutoff $\chi_R(v)=\zeta(v/R)^2$, and put
$\Phi(r)=r\log r+(1-r)\log(1-r),\qquad
I_R=\int\chi_R\frac{\nabla f^TA_f\nabla f}{g}.$
On a fixed interval $0<t_0<T$, the supplied compact particle–hole positivity permits the logarithmic test. Its exact localized identity is
$\begin{aligned}
\frac d{dt}\int\chi_R\Phi(f)+I_R
={}&8\pi\int\chi_Rf^2\\
&-\int(f-\ell g)B_f\cdot\nabla\chi_R
-\int\ell A_f\nabla f\cdot\nabla\chi_R.
\end{aligned}
\tag{15}$
Because
$\frac{|\nabla\chi_R|^2}{\chi_R}\le C/R^2,$
the last term is bounded by
$\frac12I_R+\frac{CE}{R^2},$
and the preceding boundary term by $CE^{4/5}/R$.

Integration of (15) gives a bound on $\int_{t_0}^T I_R\,dt$ independent of $R$. Fatou therefore establishes
$I_A\in L^1(t_0,T).$
The cross term in the expansion of (10) is now absolutely integrable by matrix Cauchy–Schwarz. Two velocity cutoffs give
$\iint\nabla f(v)^Ta(v-w)\nabla f(w)\,dv\,dw
=8\pi\int f^2,$
with cutoff errors controlled by $CE^{4/5}/R+CE/R^2$. This justifies (11).

The entropy flux is integrable as well:
$\int |\ell J|
\le C\sqrt{E I_A}+CE^{4/5}.$
Thus $R\to\infty$ in (15) is legitimate. The passage $t_0\downarrow0$ follows from the classical initial trace and the uniform entropy-tail bound proved next. We obtain
$\boxed{
\mathcal S(f(t))-\mathcal S(f_0)
=\int_0^tD(f(s))\,ds.
}
\tag{16}$
Since $F$ maximizes entropy at the conserved invariants,
$H(f(t)\mid F)+\int_0^tD(f(s))\,ds
=H(f_0\mid F),
\tag{17}$
and hence
$\int_0^\infty D(f(t))\,dt<\infty.
\tag{18}$
These passages use finite-horizon information from the stipulated class, not a bound uniform over all future times.

2. Entropy tails and a persistent particle–hole population

The binary entropy $s(r)=-\Phi(r)$ satisfies
$s(r)\le zr+\log(1+e^{-z}),\qquad z\ge0.$
Taking $z=|v|^2/R$ on $|v|>R$, for $R\ge1$, gives the explicit uniform estimate
$\boxed{
\sup_{t\ge0}\int_{|v|>R}s(f(t))
\le
\frac ER+(2\pi R^2+\pi R)e^{-R}.
}
\tag{19}$
Thus entropy cannot disappear into velocity infinity. This assertion concerns entropy; it does not give uniform integrability of kinetic energy.

The initial particle–hole ball implies
$S_0:=\mathcal S(f_0)>0.$
Choose $R$ so that the right side of (19) is at most $S_0/4$. Then choose $\eta\in(0,1/2)$ so that
$|B_R|s(\eta)\le S_0/4.$
Since $\mathcal S(f(t))\ge S_0$, the set
$\{(x,v):|v|\le R,\ \eta\le f(t,x,v)\le1-\eta\}$
has measure at least $S_0/(2\log2)$. Consequently,
$\boxed{
\int_{\mathbb T^3\times B_R}f(t,x,v)(1-f(t,x,v))\,dx\,dv
\ge c_0>0
}
\tag{20}$
uniformly in time.

This is a global phase-space statement. It does not assume or establish a uniform lower bound at every spatial point of the actual trajectory.

3. Compactness of late-time trajectories

Vanishing collision sources on fixed late windows

The flux has the pair representation
$J(v)=\int a(v-w)g(v)g(w)
\bigl(\nabla\ell(v)-\nabla\ell(w)\bigr)\,dw.$
Matrix Cauchy–Schwarz, (8), and (11) give
$\boxed{
\|J\|_{L^1_{x,v}}\le C\sqrt{E D(f)}
}
\tag{21}$
and
$\boxed{
\int|\nabla f\cdot J|
\le \frac14\sqrt{2D(f)\bigl(D(f)+8\pi M\bigr)}.
}
\tag{22}$
For every $\vartheta\in C^2([0,1])$,
$(\partial_t+v\cdot\nabla_x)\vartheta(f)
=
\nabla_v\cdot\bigl(\vartheta'(f)J\bigr)
-\vartheta''(f)\nabla f\cdot J.
\tag{23}$
On an interval $I$ of fixed length $L$, write $D_I=\int_I D\,dt$. Equations (21)–(22) bound the two terms by quantities tending to zero with $D_I$, including
$C\sqrt{ELD_I},
\qquad
C_\vartheta\sqrt{D_I(D_I+8\pi ML)}.$
By (18), these vanish on every fixed-length window translated to late times.

In particular, both $f$ and $g=f-f^2$ become free-transport solutions in late-time limits.

The averaging step with only $L^1$ sources

The needed compactness does not require assuming a stronger source norm.

Suppose, after fixed time and velocity cutoffs,
$(\partial_t+v\cdot\nabla_x)u_k
=\nabla_v\cdot\mathcal F_k+\mathcal G_k,$
where $u_k$ is bounded in $L^2$ and $\mathcal F_k,\mathcal G_k$ are bounded in $L^1$. Then smooth compactly supported velocity averages of $u_k$ are relatively compact in $L^1_{\rm loc}(t,x)$.

Here is the frequency estimate. On the spacetime shell $|\xi|\asymp2^j$, with $\xi=(\omega,k)$, split into
$|\omega+k\cdot v|\le\delta|\xi|$
and its complement. The resonant velocity slab has measure $O(\delta)$, giving an $L^2$ bound $C\delta^{1/2}\|u_k\|_2$.

Off resonance, divide by $i(\omega+k\cdot v)$ and integrate the velocity divergence by parts. The resulting dyadic multipliers and their first velocity derivatives have convolution-kernel $L^1$ bounds
$C2^{-j}\delta^{-20}.$
The exponent $20$ is a conservative fixed choice for the finitely many frequency derivatives in four spacetime dimensions. Periodizing the Euclidean kernels preserves their $L^1$ bounds.

Thus, on a fixed compact spacetime set $K$,
$\left\|P_j\int \psi(v)u_k\,dv\right\|_{L^1(K)}
\le
C_K\delta^{1/2}\|u_k\|_2
+C2^{-j}\delta^{-20}
\bigl(\|\mathcal F_k\|_1+\|\mathcal G_k\|_1\bigr).$
Choosing $\delta=2^{-j/40}$ makes both high-frequency tails summable. The low-frequency parts are precompact. Cutoff commutators are bounded in the same source class.

Apply this to $f$ and $g$ using (23).

Strong convergence wherever particle–hole mass survives

Take any $t_k\to\infty$, and extract time-shift limits, on all bounded shifted-time intervals,
$f_k(t,x,v)=f(t_k+t,x,v)\rightharpoonup f^\infty,
\qquad
g_k\rightharpoonup\bar g.$
Both limits solve free transport, and their velocity averages converge strongly locally in $(t,x)$.

Consider a set where
$\int_{B_{R_0}}\bar g(t,x,v)\,dv\ge2a>0.$
Strong convergence of the averages gives
$\int_{B_{R_0}}g_k\,dv\ge a$
outside a spacetime exceptional set whose measure tends to zero.

Since $g_k\le1/4$, this mass cannot concentrate in an arbitrarily thin cylinder. Excluding a cylinder around each line $v+\mathbb R\xi$ proves, on every fixed velocity ball,
$A_{f_k}(v)\ge
c\,\frac{a^2}{R_0(R+R_0)^3}I,
\qquad |v|\le R.
\tag{24}$
Together with (12), this controls $\nabla_vf_k$ in $L^2$ on those sets.

Velocity mollification now upgrades the averaged compactness to strong compactness of $f_k$. For a mollifier $\varphi_\zeta$,
$\|f_k-f_k*\varphi_\zeta\|_2
\le C\zeta\|\nabla_vf_k\|_2.$
For fixed $\zeta$, the mollified functions converge strongly by velocity averaging. The exceptional sets cost vanishing error because $0\le f_k\le1$. Exhausting the sets with positive limiting particle–hole mass gives
$f_k\to f^\infty\quad\text{strongly locally there},
\qquad
\bar g=f^\infty(1-f^\infty).
\tag{25}$
4. Zero-dissipation limits are homogeneous Fermi–Dirac distributions

There are two distinct operations here: identifying local collision equilibria and then using transport to make them homogeneous.

Local collision rigidity

Because $g(v)g(w)\le1/16$, (10) implies
$D(f_k)\ge
8\int_{x,v,w}\frac{
\left|\Pi(v-w)
\bigl(g_k(w)\nabla f_k(v)-g_k(v)\nabla f_k(w)\bigr)\right|^2
}{|v-w|}.$
The shifted dissipation tends to zero. On the sets in (25), strong convergence of $g_k$ and weak $H^1_v$ convergence therefore give
$\Pi(v-w)
\bigl(g(w)\nabla f(v)-g(v)\nabla f(w)\bigr)=0.
\tag{26}$
Choose a compactly supported nonnegative $\psi$ with $\int g\psi>0$. Integrating (26) against $a(v-w)\psi(w)$ gives
$A[g\psi](v)\nabla f(v)
=
g(v)\int a(v-w)\psi(w)\nabla f(w)\,dw.
\tag{27}$
The matrix on the left is locally uniformly positive. The field on the right, before multiplication by $g$, is locally bounded: $\nabla f\in L^2_{\rm loc}$ and $|z|^{-1}\in L^2_{\rm loc}(\mathbb R^3)$.

Thus
$\nabla f=f(1-f)W,\qquad W\in L^\infty_{\rm loc}.$
Logarithmic comparison propagates one particle–hole point to strict positivity and desaturation at every finite velocity. The logit is locally Lipschitz, and (26) becomes
$\Pi(v-w)\bigl(\nabla\ell(v)-\nabla\ell(w)\bigr)=0.$
Three noncollinear velocity points force the gradient to have one affine scalar slope. Hence
$\ell(v)=a+b\cdot v+c|v|^2.
\tag{28}$
Finite positive mass requires $c<0$. Every such slice is a positive-temperature local Fermi–Dirac distribution.

Transport eliminates spatially varying local equilibria

Equation (20) ensures that $\bar g$ has positive total mass in a fixed velocity ball at almost every shifted time. At a generic time $s$, its warm spatial set therefore has positive measure. On that set, the preceding argument gives $\bar g(s,x,v)>0$ for every finite velocity.

Free transport yields
$\bar g(t,x,v)=\bar g(s,x-(t-s)v,v).
\tag{29}$
For $t\ne s$, a velocity cube of side $1/|t-s|$ maps onto the torus under
$v\mapsto x-(t-s)v.$
The inverse image of the warm spatial set has positive velocity measure for almost every $x$. Consequently, almost every later spacetime point is warm. The strong convergence in (25) therefore extends throughout compact spacetime regions.

One must still justify taking the logit of the limiting transport equation. Choose a positive-measure subset of the source warm set on which the coefficients in (28) are bounded. On any compact time interval separated from $s$, (29) then bounds the later logit polynomial on a subset of a fixed velocity ball having uniformly positive measure.

A quadratic polynomial bounded on such a set has bounded coefficients. To see this, normalize a hypothetical sequence of unbounded coefficient vectors. A subsequence would converge to a nonzero quadratic vanishing on a set of positive measure, which is impossible.

Thus the logit is locally bounded and satisfies free transport distributionally. Substitution of
$\ell(t,x,v)=a(t,x)+b(t,x)\cdot v+c(t,x)|v|^2$
gives
$\nabla_xc=0,\qquad
\operatorname{sym}\nabla_xb+c_tI=0,\qquad
b_t+\nabla_xa=0,\qquad a_t=0.
\tag{30}$
Averaging over the torus forces $c_t=0$. A periodic vector field with zero symmetric gradient is spatially constant; the remaining equations then force $b_t=0$ and $\nabla_xa=0$. All coefficients are constant.

Every late-time limit is therefore a homogeneous, time-independent Fermi–Dirac distribution.

Identifying one limit and obtaining convergence at every time

Energy gives uniform mass and momentum tails:
$\int_{|v|>R}f(t)\le E/R^2,\qquad
\int_{|v|>R}|v|f(t)\le E/R.$
Hence every limiting profile retains $M,P$. Its energy is at most $E$ by lower semicontinuity.

Strong local convergence and (19) retain entropy:
$\mathcal S(F_*)=\mathcal S_\infty.$
At fixed $M,P$, Fermi–Dirac entropy is strictly increasing with energy. Indeed, if $E_2>E_1$,
$\mathcal S(F_{E_2})-\mathcal S(F_{E_1})
=
H(F_{E_1}\mid F_{E_2})
+\beta_{E_2}(E_2-E_1)>0.
\tag{31}$
Thus $M,P,\mathcal S_\infty$ determine a unique limiting profile.

The argument so far gives strong convergence on translated time windows. To obtain convergence at every time, set
$W(t)=\|f(t)-F_*\|_2^2.$
Using (21)–(23),
$|W'(t)|
\le
\frac12\sqrt{2D(t)(D(t)+8\pi M)}
+C_{F_*}\sqrt{E D(t)}.
\tag{32}$
Its integral over late unit windows tends to zero. The window average of $W$ also tends to zero by the strong spacetime convergence. Therefore $W(t)\to0$ at every time.

Finally,
$\|f(t)-F_*\|_1
\le |B_R|^{1/2}\|f(t)-F_*\|_2+\frac{E+E_*}{R^2},$
which proves $L^1$ convergence. The same truncation argument with $\langle v\rangle^q$ proves (1) for every $q<2$.

This completes the partial convergence theorem.

5. Additional dynamical control: a uniform spacetime density bound and polynomial moment growth

The actual conservation laws yield a useful estimate beyond compactness.

Define the kinetic stress tensor
$\mathbb A=
\begin{pmatrix}
\rho & j^T\\
j & \Pi_f
\end{pmatrix},
\qquad
j=\int vf\,dv,\qquad
\Pi_f=\int v\otimes vf\,dv.$
It is positive semidefinite and divergence-free in $(t,x)$.

Serre’s 2018 bounded-domain compensated-integrability theorem applies to such tensors. On a bounded convex domain in dimension four, it controls $\int(\det\mathbb A)^{1/3}$ by the $4/3$ power of the $L^1$ normal trace. This is Theorem 2.3 of the successfully read 2018 paper. ems.press

Here the Pauli cap supplies an explicit determinant lower bound. Let
$V_6=|B_{\sqrt6}\subset\mathbb R^3|.$
At a point with $\rho>0$, normalize the velocity covariance to the identity. The resulting probability density has at least half its mass in $B_{\sqrt6}$, while its maximum is bounded by the transformed Pauli cap. This gives
$\det\mathbb A\ge\frac{\rho^6}{4V_6^2}.
\tag{33}$
Apply Serre’s theorem to a unit time interval and a shifted fundamental spatial cube. Periodicity and Fubini allow the three spatial seams to be chosen so that
$\|\mathbb A n\|_{L^1(\partial\Omega)}
\le 2M+8\sqrt{ME}+6E.$
Therefore
$\boxed{
\sup_{s\ge0}\int_s^{s+1}\int_{\mathbb T^3}\rho(t,x)^2\,dx\,dt
\le K_\rho(M,E),
}
\tag{34}$
where one explicit choice is
$K_\rho=
\frac{(4V_6^2)^{1/3}}{4|\mathbb S^3|^{1/3}}
\bigl(2M+8\sqrt{ME}+6E\bigr)^{4/3}.$
This is uniform in time, although it is a spacetime integral rather than a pointwise bound on local density.

Let
$M_q(t)=\int\langle v\rangle^qf(t,x,v)\,dx\,dv.$
Using $\psi=\langle v\rangle^3$ in (5), convexity makes the $b$-term nonpositive. Since
$D^2\langle v\rangle^3\le6\langle v\rangle I,$
equation (7) and Hölder give
$M_3'(t)
\le
12(2\pi+1)M_3(t)^{1/3}
\left(\int\rho(t,x)^2\,dx\right)^{2/3}.$
Integrating with (34),
$\boxed{
M_3(t)\le
\left[
M_3(0)^{2/3}
+8(2\pi+1)K_\rho^{2/3}(1+t)
\right]^{3/2}.
}
\tag{35}$
For $0<\eta\le1$, interpolation with the conserved $M_2=M+E$ yields
$\boxed{
M_{2+\eta}(t)
\le
(M+E)^{1-\eta}
\left[
M_3(0)^{2/3}
+8(2\pi+1)K_\rho^{2/3}(1+t)
\right]^{3\eta/2}.
}
\tag{36}$
These are completed dynamical estimates. They improve exponential growth to polynomial growth, but
$\int_{|v|>R}|v|^2f(t)\le R^{-\eta}M_{2+\eta}(t)$
still does not become small uniformly over all $t$ by choosing $R$ once.

6. Why the remaining energy issue is real

There is a smooth same-invariant family with vanishing dissipation and a strictly positive limiting entropy gap.

For clarity take $P=0$. Choose $\Delta_0>0$ with
$E-\Delta_0>
E_{\rm P}(M,0),
\qquad
E_{\rm P}(M,P)=\frac{|P|^2}{M}
+\frac35\left(\frac3{4\pi}\right)^{2/3}M^{5/3}.$
Fix a Gaussian variance $\sigma^2>0$, and set
$m_R=\frac{\Delta_0}{R^2+3\sigma^2}.$
Let $C_R$ be the homogeneous Fermi–Dirac state with mass $M-m_R$, momentum zero, and energy $E-\Delta_0$. Define
$K_R(v)=\frac{m_R}{2}
\left[G_\sigma(v-Re_1)+G_\sigma(v+Re_1)\right],
\qquad
f_R=C_R+K_R.
\tag{37}$
For sufficiently large $R$, every $f_R$ is a smooth Schwartz density satisfying the admissibility conditions, with exact invariants
$M(f_R)=M,\qquad P(f_R)=0,\qquad E(f_R)=E.$
The family has a uniform particle–hole ball and uniform global desaturation,
$f_R\le1-\kappa.$
Nevertheless,
$f_R\longrightarrow F_{M,0,E-\Delta_0}
\quad\text{in }L^1,$
and
$H(f_R\mid F_{M,0,E})
\longrightarrow
\mathcal S(F_{M,0,E})-
\mathcal S(F_{M,0,E-\Delta_0})>0.
\tag{38}$
Its dissipation satisfies
$\boxed{D(f_R)\le C m_R=O(R^{-2})\longrightarrow0.}
\tag{39}$
The estimate includes the denominator and cross terms. Since $C_R$ stays in a compact positive-temperature parameter family,
$\frac1{1-C_R-K_R}
\le\frac{1+C m_R}{1-C_R},$
and
$g(C_R+K_R)\le g(C_R)+K_R.$
For any positive semidefinite matrix $A$,
$\frac{|\nabla(C+K)|_A^2}{C+K}
\le
\frac{|\nabla C|_A^2}{C}
+\frac{|\nabla K|_A^2}{K}.$
Furthermore,
$\|a*K_R\|_\infty=O(m_R),
\qquad
\int\frac{|\nabla K_R|^2}{K_R}\le\frac{3m_R}{\sigma^2}.$
These inequalities give
$I_A(f_R)\le(1+C m_R)I_A(C_R)+C m_R.$
Because $C_R$ is an equilibrium,
$I_A(C_R)=8\pi\int C_R^2,$
and $\int f_R^2\ge\int C_R^2$. Equation (11) proves (39).

This family rules out an entropy-production bound bounded away from zero on positive entropy-gap intervals using only the fixed invariants and the displayed uniform core/desaturation information.

It is not a negative resolution of the question. Each $f_R$ is a different initial density. No single solution following this family, or carrying a positive energy defect to infinity, has been constructed.

7. The exact unresolved assertion and source boundaries

The partial theorem makes the energy defect explicit. For every fixed $R$,
$\lim_{t\to\infty}\int_{|v|>R}|v|^2f(t,x,v)\,dx\,dv
=
E-\int_{|v|\le R}|v|^2F_*(v)\,dv.$
Hence
$\boxed{
\lim_{R\to\infty}\lim_{t\to\infty}
\int_{|v|>R}|v|^2f(t,x,v)\,dx\,dv
=\Delta.
}
\tag{40}$
Also,
$\lim_{t\to\infty}H(f(t)\mid F_*)=\beta_*\Delta,$
despite the $L^1$ convergence. Relative entropy detects energy that unweighted convergence can lose.

Given the finite-time bounds, the full requested theorem is therefore equivalent to proving uniform integrability of the actual trajectory’s kinetic energy:
$\lim_{R\to\infty}\sup_{t\ge0}
\int_{|v|>R}|v|^2f(t,x,v)\,dx\,dv=0.
\tag{41}$
Equation (41) has not been proved here. It is an identified missing assertion, not an additional premise being assumed. If it were established, (3) would give the requested entropy limit, and binary relative entropy gives the correctly mass-scaled Pinsker estimate
$\|f(t)-F\|_1^2\le2M\,H(f(t)\mid F).$
The source and access boundaries are:

Golding–Henderson: I use the global solution and finite-horizon properties exactly at the accepted scope supplied in your prompt. The attempted governing HTML retrieval failed; no alternative body recovery was made. I therefore do not claim an independent read of that theorem body.

Alonso–Bagland–Desvillettes–Lods, 2021: the body, including Theorem 1.8, was successfully read. Its homogeneous normalization and entropy/moment conditions remain intact; neither its hard-potential theorem nor a spatial coercivity conclusion is imported. Springer Nature Link

Serre, 2018: the bounded-domain theorem was successfully read and used for (34). The separate 2024 body timed out and was not recovered; the torus estimate above is derived from the distinct 2018 result.

A broad search incidentally displayed introductory material from the held Carlo Alberto document. No theorem from that exposure enters this argument, and no follow-up recovery was attempted.

All estimates above use the fixed Pauli cap $\epsilon=1$. No uniform classical-limit claim is made.

The completed result is convergence to a uniquely identified homogeneous Fermi–Dirac profile, together with an exact characterization of the possible energy defect. The required assertion that this defect vanishes—and therefore the full unconditional entropic thermalization question—remains unresolved.


=== VISIBLE WORKING ACTIVITY ===
Worked for 72m 41s

I’ll use the finite-time spreading and regularity results as the starting point and work on the missing infinite-time step. I’ll read the governing equation and entropy theorem, then investigate whether entropy dissipation and transport can force convergence while controlling velocity tails and Pauli saturation. I’ll preserve the source holds and keep any conditional result distinct from the full claim.

Lfd compactness, Lfd entropy and Lfd rigidity updated
Searching link.springer.com

Analyzed entropy bounds and tails

Bounded collision coefficients and established particle-hole seedball

Assessed uniform-bound prerequisites and checked cold-state degeneracy

Checked saturated-state flux and derived weak-form bounds

Derived local flux bounds and checked velocity averages

Checked compactness and energy-defect control

The Golding–Henderson body request failed, so I have placed it under the same no-retry hold and will rely on the finite-time and global-existence scope you supplied. The 2021 entropy paper is readable. A central distinction is emerging: finite total entropy dissipation gives late-time windows with small collision dissipation, but the proof still has to turn those windows into spatial equilibration and account for all conserved kinetic energy.

Lfd compactness, Lfd entropy and Lfd rigidity updated
Searched the web

Checked moment-growth bounds and entropy tails

Checked moment conservation

Checked high-velocity cancellation and symmetrized the weak form

Checked saturated-tail diffusion and estimated weighted moment growth

Assessed entropy growth bounds and screened new papers

Formalized free-flow mixing and tested entropy compactness

Checked warm-cold mixing and established transport positivity

Proved entropy coercivity and checked local entropy positivity

Derived local matrix relation and built warm-set entropy bound

Formalized compactness via smoothing and controlled entropy error

Tested Fermi-ball rigidity

Tested energy-escape bounds and bounded drift coefficients

Investigated stationary solutions and occupancy

Derived inequalities bounding local moment growth

Developed dispersion estimates and compared 3D Bony bounds

Verified the uniform Fisher bound and finite-window approximation

Tracked defect-measure transport and established warm-set compactness

Developed zero-D classification

Tested energy recovery and near-equilibrium stability

Assessed tail moment bounds and tested tangential-tail residence

Lfd entropy, Lfd compactness and Lfd rigidity updated

I derived a uniform estimate that was not apparent from the finite-time bounds: conserved energy and 
0
≤
𝑓
≤
1
0≤f≤1 control the velocity tails of the binary entropy density. This keeps a positive amount of particle-hole mixing in a bounded velocity region at every time. An exact Coulomb identity also makes bounded smooth functions of 
𝑓
f approximately free-transported on late windows with small dissipation. I’m testing whether these estimates can supply the missing compactness and prevent kinetic energy from escaping to larger velocities.

Searched 6 websites
Lfd entropy updated
Searched 6 websites
Lfd entropy, Lfd compactness and Lfd rigidity updated
Searched the web

Derived the determinant bound

Lfd entropy, Lfd compactness and Lfd rigidity updated

Checked velocity-averaging compactness

Bounded third-moment growth

Checked moment estimates

Checked angular cancellation and local moment scaling

Checked uniform and inhomogeneous moment bounds

Developed renormalized transport limit and checked energy-retention proof

Checked weighted Fisher control and supporting passages

Prepared weak-form cutoff tests and verified stress transport

Checked regularized dissipation

Checked cutoff entropy estimates

Lfd rigidity and Lfd compactness finished

Checked velocity averaging bounds and compactness tails

Refined averaging-lemma proof and checked singular-factor control

Proved local Lipschitzness and gradient rigidity

Derived affine F structure and selected a valid time

Proved m_g positivity and checked direct invariance proof

Bounded quadratic coefficients and compared polynomial terms

Proved entropy monotonicity

Derived window oscillation decay and checked invariant-based ellipticity

Tested Harnack bounds and assessed heat-kernel control

Tested truncated energy moments and estimated inward energy flux

Checked tail-collision bounds and density integrability

Tested counterexample feasibility and checked nonthermalizing states

Checked uniform transport estimates and verified flux L1 bounds

Proved and tested warm-set convergence limits

Constructed measurable coefficient selections and verified g’s free flow

Established global current and flux bounds

Estimated tail entropy and Coulomb entropy coupling

Verified entropy-flux bounds

Lfd rigidity and Lfd entropy updated

Derived and expanded the localized entropy balance identity

Bounded localized entropy and Smax uniformly

Established entropy-flux and hφ lower bounds

Bounded local entropy and estimated small-mass entropy

Verified localized entropy bounds

Derived warm-set measure and g-integral bounds

Lfd entropy and Lfd rigidity updated

A further consequence of local conservation is now established. Using the kinetic stress tensor and Serre’s earlier compensated-integrability theorem, I get a uniform bound on the space-time integral of 
𝜌
2
ρ
2
 over every unit time interval. This improves the available growth bound for moments between orders two and three to a polynomial one. It still does not rule out a vanishing amount of mass carrying finite energy to ever larger velocities; I’m checking that remaining issue separately from the compactness argument.

Tested stress-defect invariants and energy escape

Checked high-velocity tail bounds

Derived truncated-energy bounds

Bounded tail collision terms

Verified the weaker theorem and established the entropy-defect identity

Proved positive-temperature F_ and checked Coulomb identity

Checked coercivity identities and source scope

Bounded the density integral

Estimated third-moment growth

Checked energy retention and tail tightness

The compactness argument now appears to support convergence in 
𝐿
1
L
1
 to a homogeneous Fermi–Dirac profile. The unresolved point is whether that profile retains all the conserved energy: 
𝐿
1
L
1
 convergence alone permits vanishing mass to carry finite energy to large velocities. I’m testing whether the dynamics rule out that loss before drawing a conclusion about the requested relative entropy.

Lfd compactness, Lfd rigidity and Lfd entropy updated
Searched 20 websites

Checked convergence bounds and estimated high-moment drift

Estimated beam mixing and tested a moment estimate

Checked Serre and y-scaled boundary terms

Checked kinetic Harnack bounds and uniform moment estimates

Explored tail-energy bounds and bounded high-high terms

Estimated weighted tail errors and expanded the cubic moment

Tested cutoff-flux bounds and growth

Estimated energy-escape bounds and tested radial recurrence

Searched 20 websites

Checked Fourier resonance estimates and projected-gradient rigidity

Derived the quadratic equilibrium form

Established Fermi-Dirac coefficient and flux-based B bounds

Verified weak conservation formula

Verified entropy flux bounds

Checked entropy-limit proof

Constructed Gaussian halo family

Tested the energy-retention argument

Sharpened tail-growth bounds

Assessed entropy cascade costs

Checked the determinant bound

Checked the moment estimate

Estimated the Bψ3 bound

Tested weighted tensor multiplier

Checked weighted tensor estimates

The remaining issue is substantive. I checked a family of smooth densities with the same mass, momentum and energy whose collision dissipation tends to zero while their relative entropy to the prescribed equilibrium stays positive. They are separate test densities, not a nonthermalizing trajectory. Thus they do not answer the question negatively; they show why small dissipation and the conserved quantities alone cannot finish the proof.

Lfd entropy and Lfd rigidity updated

Checked entropy proof and analyzed time-shift limits

Established global positivity and confirmed strong local convergence

Checked uniform ellipticity

Assessed dissipation-based M3 control

Tested tail-energy and fixed-R flux

Lfd compactness and Lfd rigidity updated

Checked the current excerpt

Refined entropy notation

Formalized energy-defect equivalences

Checked velocity-averaging estimates

Refined dyadic compactness estimates

Checked explicit moment bounds

Checked the Hölder estimate

Verified entropy cutoff estimates

Constructed admissible test densities

Verified entropy and global cutoff bounds

Finalized the J-matrix estimate

Established warm-set lower bounds

Searched the web

Checked theorem assumptions

Verified finite-time moment bounds

Tested local-FD perturbations and checked bad-set bounds

Tested a functional counterexample

Lfd compactness and Lfd entropy updated

The proof review has isolated an exact energy defect, 
Δ
=
𝐸
−
𝐸
∗
≥
0
Δ=E−E
∗
	​

≥0, and established

lim
⁡
𝑡
→
∞
𝐻
(
𝑓
(
𝑡
)
∣
𝐹
𝐸
)
=
𝐻
(
𝐹
∗
∣
𝐹
𝐸
)
+
𝛽
𝐸
Δ
.
t→∞
lim
	​

H(f(t)∣F
E
	​

)=H(F
∗
	​

∣F
E
	​

)+β
E
	​

Δ.

The conservation and entropy passages are justified within the supplied finite-time solution class. I have not found a dynamical estimate forcing 
Δ
=
0
Δ=0, or an admissible trajectory with 
Δ
>
0
Δ>0; the full question therefore remains unresolved.

Awaited entropy report

Checked F_* uniqueness

Lfd compactness updated

Refined entropy and derivative bounds

Refined coercivity limitations and checked entropy finiteness

Verified cutoff details

Checked finite-slice estimates and bounded the energy derivative

Refined compactness proof and fixed box-periodic constants

Lfd compactness updated

Prepared collision-kernel notation

Refined entropy-flux estimates

Checked resonant-slab bounds

Clarified radius-bound scope

Lfd compactness finished

Located exact Theorem 2.3

Refined uniform limit bounds

=== LFD COMPACTNESS VISIBLE TREE ===
Lfd compactness
Status
Done
Final response

The closing attempt did not establish 
𝐸
∗
=
𝐸
E
∗
	​

=E. The actual-dynamics functional 
𝑊
(
𝑓
)
=
∫
log
⁡
⟨
𝑣
⟩
 
𝑑
𝐵
(
𝑓
∣
𝐹
∗
)
W(f)=∫log⟨v⟩d
B
	​

(f∣F
∗
	​

) would detect escaped energy, and its exact derivative consists of negative weighted entropy production plus commutators involving 
𝑢
=
\logit
𝑓
−
\logit
𝐹
∗
u=\logitf−\logitF
∗
	​

 and 
∇
𝑢
∇u. Those commutators have not been controlled by strong 
𝐿
𝑞
1
L
q
1
	​

 convergence for 
𝑞
<
2
q<2, finite total dissipation, the uniform unit-window 
𝜌
2
ρ
2
 estimate, or polynomial 
𝑀
3
M
3
	​

 growth. In particular, these inputs do not supply a uniform positive core at every spatial position, and a generic estimate 
𝑊
′
≤
𝐶
(
1
+
𝑊
)
𝐷
W
′
≤C(1+W)D has the first-variation difficulty near Fermi–Dirac profiles different from the reference. Preserve this functional as an unclosed route, and preserve the polynomial moment estimates at their proved scope. No energy-retention theorem or admissible nonthermalizing trajectory has been constructed; full entropic thermalization remains unresolved.

=== LFD ENTROPY VISIBLE TREE ===
Lfd entropy
Status
Done
Final response
Status

The entropy and compactness route yields a substantial partial theorem: the solution converges in 
𝐿
1
L
1
 to a homogeneous positive-temperature Fermi–Dirac state, but the argument does not retain all the energy in that limit. The remaining operation is precisely

𝐸
∞
=
𝐸
.
E
∞
	​

=E.

I do not have a proof of that identity or an admissible nonthermalizing trajectory. The Gaussian-halo construction below rigorously shows why an invariant-only entropy-production estimate, even supplemented by a uniform local Fermi–Dirac core and global desaturation, cannot supply that identity by itself.

What follows consolidates the partial theorem and its proof. It uses only the accepted finite-horizon properties of the actual solution class, never a uniform late-time regularity or desaturation assumption.

1. Partial theorem

Write

Φ
(
𝑧
)
=
𝑧
log
⁡
𝑧
+
(
1
−
𝑧
)
log
⁡
(
1
−
𝑧
)
,
𝑆
(
𝑓
)
=
−
∫
𝑇
3
×
𝑅
3
Φ
(
𝑓
)
,
Φ(z)=zlogz+(1−z)log(1−z),S(f)=−∫
T
3
×R
3
	​

Φ(f),

and let the torus have unit volume. The Pauli ground-state energy is

𝐸
P
(
𝑀
,
𝑃
)
=
∣
𝑃
∣
2
𝑀
+
3
5
(
3
4
𝜋
)
2
/
3
𝑀
5
/
3
.
E
P
	​

(M,P)=
M
∣P∣
2
	​

+
5
3
	​

(
4π
3
	​

)
2/3
M
5/3
.

For a global classical solution in the accepted class, there is a number

𝐸
P
(
𝑀
,
𝑃
)
<
𝐸
∞
≤
𝐸
E
P
	​

(M,P)<E
∞
	​

≤E

such that, with 
𝐹
∞
=
𝐹
𝑀
,
𝑃
,
𝐸
∞
F
∞
	​

=F
M,P,E
∞
	​

	​

,

∥
𝑓
(
𝑡
)
−
𝐹
∞
∥
𝐿
𝑥
,
𝑣
1
⟶
0.
∥f(t)−F
∞
	​

∥
L
x,v
1
	​

	​

⟶0.
	​


Moreover,

𝑆
(
𝑓
(
𝑡
)
)
⟶
𝑆
(
𝐹
∞
)
,
S(f(t))⟶S(F
∞
	​

),

and therefore

lim
⁡
𝑡
→
∞
𝐻
(
𝑓
(
𝑡
)
∣
𝐹
𝑀
,
𝑃
,
𝐸
)
=
𝑆
(
𝐹
𝑀
,
𝑃
,
𝐸
)
−
𝑆
(
𝐹
∞
)
.
t→∞
lim
	​

H(f(t)∣F
M,P,E
	​

)=S(F
M,P,E
	​

)−S(F
∞
	​

).
	​


This is the desired conclusion if and only if 
𝐸
∞
=
𝐸
E
∞
	​

=E.

The partial theorem also identifies any missing energy exactly:

lim
⁡
𝑅
→
∞
lim
⁡
𝑡
→
∞
∫
∣
𝑣
∣
>
𝑅
∣
𝑣
∣
2
𝑓
(
𝑡
,
𝑥
,
𝑣
)
 
𝑑
𝑥
 
𝑑
𝑣
=
𝐸
−
𝐸
∞
.
R→∞
lim
	​

t→∞
lim
	​

∫
∣v∣>R
	​

∣v∣
2
f(t,x,v)dxdv=E−E
∞
	​

.

Thus the sole defect left by this proof is kinetic energy escaping to arbitrarily large velocities. Mass, momentum, entropy, and the entire finite-velocity distribution are retained.

2. Exact Coulomb identities

Put

𝑔
=
𝑓
(
1
−
𝑓
)
,
ℎ
=
log
⁡
𝑓
1
−
𝑓
,
g=f(1−f),h=log
1−f
f
	​

,

and use the specified normalization

𝑎
(
𝑧
)
=
Π
(
𝑧
)
∣
𝑧
∣
,
𝑏
(
𝑧
)
=
∇
⋅
𝑎
(
𝑧
)
=
−
2
𝑧
∣
𝑧
∣
3
,
∇
⋅
𝑏
=
−
8
𝜋
𝛿
0
.
a(z)=
∣z∣
Π(z)
	​

,b(z)=∇⋅a(z)=−
∣z∣
3
2z
	​

,∇⋅b=−8πδ
0
	​

.

Set

𝐴
[
𝑔
]
=
𝑎
∗
𝑔
,
𝐵
[
𝑓
]
=
𝑏
∗
𝑓
.
A[g]=a∗g,B[f]=b∗f.

Then

𝑄
(
𝑓
)
=
∇
𝑣
⋅
𝐽
,
𝐽
=
𝐴
[
𝑔
]
∇
𝑣
𝑓
−
𝑔
𝐵
[
𝑓
]
.
Q(f)=∇
v
	​

⋅J,J=A[g]∇
v
	​

f−gB[f].

The equivalent pair representation is

𝐽
(
𝑣
)
=
∫
𝑎
(
𝑣
−
𝑤
)
𝑔
(
𝑣
)
𝑔
(
𝑤
)
(
∇
ℎ
(
𝑣
)
−
∇
ℎ
(
𝑤
)
)
 
𝑑
𝑤
.
J(v)=∫a(v−w)g(v)g(w)(∇h(v)−∇h(w))dw.

Define

𝐷
(
𝑓
)
=
1
2
∫
𝑥
,
𝑣
,
𝑤
𝑔
(
𝑣
)
𝑔
(
𝑤
)
(
∇
ℎ
(
𝑣
)
−
∇
ℎ
(
𝑤
)
)
𝑇
𝑎
(
𝑣
−
𝑤
)
(
∇
ℎ
(
𝑣
)
−
∇
ℎ
(
𝑤
)
)
,
D(f)=
2
1
	​

∫
x,v,w
	​

g(v)g(w)(∇h(v)−∇h(w))
T
a(v−w)(∇h(v)−∇h(w)),

and

𝐼
(
𝑓
)
=
∫
𝑥
,
𝑣
∇
𝑓
𝑇
𝐴
[
𝑔
]
∇
𝑓
𝑔
.
I(f)=∫
x,v
	​

g
∇f
T
A[g]∇f
	​

.

The decisive Coulomb identity is

𝐷
(
𝑓
)
=
𝐼
(
𝑓
)
−
8
𝜋
∫
𝑓
2
.
D(f)=I(f)−8π∫f
2
.
	​


Consequently,

𝐼
(
𝑓
)
≤
𝐷
(
𝑓
)
+
8
𝜋
𝑀
.
I(f)≤D(f)+8πM.
	​


Indeed, expanding the square leaves the cross term

∫
𝑥
,
𝑣
,
𝑤
∇
𝑓
(
𝑣
)
𝑇
𝑎
(
𝑣
−
𝑤
)
∇
𝑓
(
𝑤
)
=
8
𝜋
∫
𝑓
2
.
∫
x,v,w
	​

∇f(v)
T
a(v−w)∇f(w)=8π∫f
2
.

Once 
𝐼
I is integrable, absolute integrability of the cross term follows from the matrix Cauchy inequality; spatial and velocity cutoffs justify the integrations by parts. Section 3 constructs that integrability before using the global identity.

3. Conservation and the entropy law for the actual solution class

Only finite-horizon bounds enter this section.

3.1 Derivative-free weak form

For smooth velocity tests,

∫
𝜓
(
𝑣
)
𝑄
(
𝑓
)
(
𝑣
)
 
𝑑
𝑣
=
∬
𝑓
(
𝑣
)
𝑔
(
𝑤
)
[
𝑎
(
𝑣
−
𝑤
)
:
𝐷
2
𝜓
(
𝑣
)
+
𝑏
(
𝑣
−
𝑤
)
⋅
(
∇
𝜓
(
𝑣
)
−
∇
𝜓
(
𝑤
)
)
]
 
𝑑
𝑣
 
𝑑
𝑤
.
∫ψ(v)Q(f)(v)dv=∬f(v)g(w)[a(v−w):D
2
ψ(v)+b(v−w)⋅(∇ψ(v)−∇ψ(w))]dvdw.

For 
𝜓
=
1
,
𝑣
𝑖
,
∣
𝑣
∣
2
ψ=1,v
i
	​

,∣v∣
2
, the bracket vanishes. For energy, explicitly,

𝑎
(
𝑧
)
:
2
𝐼
=
4
∣
𝑧
∣
,
𝑏
(
𝑧
)
⋅
2
𝑧
=
−
4
∣
𝑧
∣
.
a(z):2I=
∣z∣
4
	​

,b(z)⋅2z=−
∣z∣
4
	​

.

Let

𝜌
(
𝑥
)
=
∫
𝑓
(
𝑥
,
𝑣
)
 
𝑑
𝑣
,
𝑒
(
𝑥
)
=
∫
∣
𝑣
∣
2
𝑓
(
𝑥
,
𝑣
)
 
𝑑
𝑣
.
ρ(x)=∫f(x,v)dv,e(x)=∫∣v∣
2
f(x,v)dv.

The Pauli bound gives

𝜌
≤
𝐶
𝑒
3
/
5
,
𝜌
5
/
3
≤
𝐶
𝑒
.
ρ≤Ce
3/5
,ρ
5/3
≤Ce.

Also, splitting the Newton potential at an optimized radius yields

sup
⁡
𝑣
∫
𝑓
(
𝑤
)
∣
𝑣
−
𝑤
∣
 
𝑑
𝑤
≤
𝐶
𝜌
2
/
3
.
v
sup
	​

∫
∣v−w∣
f(w)
	​

dw≤Cρ
2/3
.

Hence

∫
𝑥
,
𝑣
,
𝑤
𝑓
(
𝑣
)
𝑔
(
𝑤
)
∣
𝑣
−
𝑤
∣
≤
𝐶
∫
𝜌
5
/
3
 
𝑑
𝑥
≤
𝐶
𝐸
.
∫
x,v,w
	​

∣v−w∣
f(v)g(w)
	​

≤C∫ρ
5/3
dx≤CE.

Use cutoffs of the collision invariants whose Hessians are uniformly bounded. The collision brackets are dominated by 
𝐶
/
∣
𝑣
−
𝑤
∣
C/∣v−w∣. The accepted finite-horizon weighted bounds first ensure finiteness of the moments on every finite interval; dominated cutoff passage then gives exact conservation of 
𝑀
,
𝑃
,
𝐸
M,P,E. Periodicity eliminates the integrated transport terms.

3.2 Pauli interpolation and logarithmic weights

For every fixed 
𝑝
∈
(
3
/
5
,
1
)
p∈(3/5,1),

∫
𝑓
(
𝑥
,
𝑣
)
𝑝
 
𝑑
𝑣
≤
𝐶
𝑝
𝑒
(
𝑥
)
3
/
5
.
∫f(x,v)
p
dv≤C
p
	​

e(x)
3/5
.

A direct proof splits at radius 
𝑅
R:

∫
∣
𝑣
∣
≤
𝑅
𝑓
𝑝
≤
𝐶
𝑅
3
,
∫
∣
𝑣
∣
>
𝑅
𝑓
𝑝
≤
𝐶
𝑝
𝑒
𝑝
𝑅
3
−
5
𝑝
,
∫
∣v∣≤R
	​

f
p
≤CR
3
,∫
∣v∣>R
	​

f
p
≤C
p
	​

e
p
R
3−5p
,

and chooses 
𝑅
=
𝑒
1
/
5
R=e
1/5
.

The coefficient estimates are

𝐴
[
𝑔
]
≤
𝐶
𝜌
2
/
3
≤
𝐶
𝑒
2
/
5
,
∣
𝐵
[
𝑓
]
∣
≤
𝐶
𝜌
1
/
3
≤
𝐶
𝑒
1
/
5
.
A[g]≤Cρ
2/3
≤Ce
2/5
,∣B[f]∣≤Cρ
1/3
≤Ce
1/5
.

Since

𝑔
∣
ℎ
∣
+
𝑔
ℎ
2
≤
𝐶
𝑝
𝑓
𝑝
,
g∣h∣+gh
2
≤C
p
	​

f
p
,

we obtain the global bounds

∫
𝑔
ℎ
2
tr
⁡
𝐴
[
𝑔
]
≤
𝐶
𝐸
,
∫gh
2
trA[g]≤CE,
	​


and

∫
(
𝑓
+
𝑔
∣
ℎ
∣
)
∣
𝐵
[
𝑓
]
∣
≤
𝐶
𝐸
4
/
5
.
∫(f+g∣h∣)∣B[f]∣≤CE
4/5
.
	​


The unit spatial volume is used in the latter estimate.

3.3 Cutoff entropy identity

Fix 
0
<
𝑎
<
𝑇
<
∞
0<a<T<∞, and take

𝜒
𝑅
(
𝑣
)
=
𝜁
(
𝑣
/
𝑅
)
2
.
χ
R
	​

(v)=ζ(v/R)
2
.

The accepted compact particle/hole positivity permits the logarithmic test on the bounded velocity support. With

𝐼
𝑅
=
∫
𝜒
𝑅
∇
𝑓
𝑇
𝐴
[
𝑔
]
∇
𝑓
𝑔
,
I
R
	​

=∫χ
R
	​

g
∇f
T
A[g]∇f
	​

,

the exact localized identity is

𝑑
𝑑
𝑡
∫
𝜒
𝑅
Φ
(
𝑓
)
+
𝐼
𝑅
=
8
𝜋
∫
𝜒
𝑅
𝑓
2
−
∫
(
𝑓
−
ℎ
𝑔
)
𝐵
[
𝑓
]
⋅
∇
𝜒
𝑅
−
∫
ℎ
𝐴
[
𝑔
]
∇
𝑓
⋅
∇
𝜒
𝑅
.
dt
d
	​

∫χ
R
	​

Φ(f)+I
R
	​

=8π∫χ
R
	​

f
2
−∫(f−hg)B[f]⋅∇χ
R
	​

−∫hA[g]∇f⋅∇χ
R
	​

.

Because

∣
∇
𝜒
𝑅
∣
2
𝜒
𝑅
≤
𝐶
𝑅
2
,
χ
R
	​

∣∇χ
R
	​

∣
2
	​

≤
R
2
C
	​

,

the diffusion boundary term is bounded by

1
2
𝐼
𝑅
+
𝐶
𝐸
𝑅
2
.
2
1
	​

I
R
	​

+
R
2
CE
	​

.

The drift boundary term is at most 
𝐶
𝐸
4
/
5
/
𝑅
CE
4/5
/R. Therefore,

𝑑
𝑑
𝑡
∫
𝜒
𝑅
Φ
(
𝑓
)
+
1
2
𝐼
𝑅
≤
8
𝜋
𝑀
+
𝐶
𝐸
4
/
5
𝑅
+
𝐶
𝐸
𝑅
2
.
dt
d
	​

∫χ
R
	​

Φ(f)+
2
1
	​

I
R
	​

≤8πM+
R
CE
4/5
	​

+
R
2
CE
	​

.

The entropy magnitude is bounded using 
𝑀
,
𝐸
M,E, so integration gives a bound on 
∫
𝑎
𝑇
𝐼
𝑅
∫
a
T
	​

I
R
	​

 independent of 
𝑅
R. Fatou gives 
𝐼
∈
𝐿
1
(
𝑎
,
𝑇
)
I∈L
1
(a,T). In turn,

∫
∣
ℎ
𝐽
∣
≤
𝐶
𝐸
𝐼
+
𝐶
𝐸
4
/
5
,
∫∣hJ∣≤C
EI
	​

+CE
4/5
,

which makes the remaining cutoff fluxes vanish. The Coulomb identity in Section 2 is now justified and gives

𝑆
(
𝑓
(
𝑇
)
)
−
𝑆
(
𝑓
(
𝑎
)
)
=
∫
𝑎
𝑇
𝐷
(
𝑓
(
𝑡
)
)
 
𝑑
𝑡
.
S(f(T))−S(f(a))=∫
a
T
	​

D(f(t))dt.

The passage 
𝑎
↓
0
a↓0 uses classical local convergence to the initial data and the uniform entropy-tail estimate below. Thus

𝑆
(
𝑓
(
𝑡
)
)
−
𝑆
(
𝑓
0
)
=
∫
0
𝑡
𝐷
(
𝑓
(
𝑠
)
)
 
𝑑
𝑠
.
S(f(t))−S(f
0
	​

)=∫
0
t
	​

D(f(s))ds.
	​


Since the equilibrium with the conserved invariants maximizes entropy,

∫
0
∞
𝐷
(
𝑓
(
𝑡
)
)
 
𝑑
𝑡
≤
𝑆
(
𝐹
𝑀
,
𝑃
,
𝐸
)
−
𝑆
(
𝑓
0
)
<
∞
.
∫
0
∞
	​

D(f(t))dt≤S(F
M,P,E
	​

)−S(f
0
	​

)<∞.
	​

4. Entropy tails and persistent particle-hole mass

Let 
𝑠
(
𝑧
)
=
−
Φ
(
𝑧
)
s(z)=−Φ(z). For every 
𝑏
≥
0
b≥0,

𝑠
(
𝑧
)
≤
𝑏
𝑧
+
log
⁡
(
1
+
𝑒
−
𝑏
)
.
s(z)≤bz+log(1+e
−b
).

Taking 
𝑏
=
𝜆
∣
𝑣
∣
2
b=λ∣v∣
2
 gives

sup
⁡
𝑡
≥
0
∫
∣
𝑣
∣
>
𝑅
𝑠
(
𝑓
(
𝑡
)
)
≤
𝜆
𝐸
+
∫
∣
𝑣
∣
>
𝑅
𝑒
−
𝜆
∣
𝑣
∣
2
 
𝑑
𝑣
.
t≥0
sup
	​

∫
∣v∣>R
	​

s(f(t))≤λE+∫
∣v∣>R
	​

e
−λ∣v∣
2
dv.

First choose 
𝜆
λ small, then 
𝑅
R large. Therefore entropy tails are uniformly tight:

lim
⁡
𝑅
→
∞
sup
⁡
𝑡
∫
∣
𝑣
∣
>
𝑅
𝑠
(
𝑓
(
𝑡
)
)
=
0.
R→∞
lim
	​

t
sup
	​

∫
∣v∣>R
	​

s(f(t))=0.

This is an entropy-tail statement. It is not energy-tail uniform integrability.

The initial seed ball gives 
𝑆
(
𝑓
0
)
>
0
S(f
0
	​

)>0. Choose 
𝑅
R so that the entropy in 
∣
𝑣
∣
≤
𝑅
∣v∣≤R is at least 
𝑆
(
𝑓
0
)
/
2
S(f
0
	​

)/2 for every time. Then choose 
𝛿
>
0
δ>0 with

∣
𝐵
𝑅
∣
𝑠
(
𝛿
)
≤
𝑆
(
𝑓
0
)
/
4.
∣B
R
	​

∣s(δ)≤S(f
0
	​

)/4.

It follows that

∣
{
(
𝑥
,
𝑣
)
:
∣
𝑣
∣
≤
𝑅
,
 
𝛿
≤
𝑓
(
𝑡
,
𝑥
,
𝑣
)
≤
1
−
𝛿
}
∣
≥
𝑆
(
𝑓
0
)
4
log
⁡
2
.
∣{(x,v):∣v∣≤R, δ≤f(t,x,v)≤1−δ}∣≥
4log2
S(f
0
	​

)
	​

.

Consequently,

∫
𝑥
,
∣
𝑣
∣
≤
𝑅
𝑓
(
𝑡
,
𝑥
,
𝑣
)
(
1
−
𝑓
(
𝑡
,
𝑥
,
𝑣
)
)
 
𝑑
𝑥
 
𝑑
𝑣
≥
𝑐
0
>
0.
∫
x,∣v∣≤R
	​

f(t,x,v)(1−f(t,x,v))dxdv≥c
0
	​

>0.
	​


The bound is global in phase space. It does not assert a positive particle-hole mass at every spatial point.

5. Flux bounds and asymptotically free renormalized transport

Define

𝑑
(
𝑥
,
𝑣
)
=
∫
𝑔
(
𝑣
)
𝑔
(
𝑤
)
(
∇
ℎ
(
𝑣
)
−
∇
ℎ
(
𝑤
)
)
𝑇
𝑎
(
𝑣
−
𝑤
)
(
∇
ℎ
(
𝑣
)
−
∇
ℎ
(
𝑤
)
)
 
𝑑
𝑤
.
d(x,v)=∫g(v)g(w)(∇h(v)−∇h(w))
T
a(v−w)(∇h(v)−∇h(w))dw.

Then 
∫
𝑑
=
2
𝐷
∫d=2D, and matrix Cauchy gives

𝐽
𝑇
𝐴
[
𝑔
]
†
𝐽
≤
𝑔
 
𝑑
.
J
T
A[g]
†
J≤gd.

Two useful consequences are

∫
∣
∇
𝑓
⋅
𝐽
∣
≤
1
4
2
𝐷
(
𝐷
+
8
𝜋
𝑀
)
,
∫∣∇f⋅J∣≤
4
1
	​

2D(D+8πM)
	​

,
	​


and

∫
∣
∇
ℎ
⋅
𝐽
∣
≤
2
𝐷
(
𝐷
+
8
𝜋
𝑀
)
.
∫∣∇h⋅J∣≤
2D(D+8πM)
	​

.
	​


Furthermore,

∫
∣
ℎ
𝐽
∣
≤
𝐶
𝐸
𝐷
.
∫∣hJ∣≤C
ED
	​

.
	​


There is also a global, rather than merely local, unweighted flux bound. Indeed,

∫
𝑔
 
tr
⁡
𝐴
[
𝑔
]
≤
𝐶
∫
𝜌
5
/
3
 
𝑑
𝑥
≤
𝐶
𝐸
,
∫gtrA[g]≤C∫ρ
5/3
dx≤CE,

so

∥
𝐽
∥
𝐿
𝑥
,
𝑣
1
≤
𝐶
𝐸
𝐷
.
∥J∥
L
x,v
1
	​

	​

≤C
ED
	​

.
	​


For 
𝛽
∈
𝐶
2
(
[
0
,
1
]
)
β∈C
2
([0,1]),

(
∂
𝑡
+
𝑣
⋅
∇
𝑥
)
𝛽
(
𝑓
)
=
∇
𝑣
⋅
(
𝛽
′
(
𝑓
)
𝐽
)
−
𝛽
′
′
(
𝑓
)
∇
𝑓
⋅
𝐽
.
(∂
t
	​

+v⋅∇
x
	​

)β(f)=∇
v
	​

⋅(β
′
(f)J)−β
′′
(f)∇f⋅J.

On an interval 
𝐼
I of length 
𝐿
L, writing 
𝐷
𝐼
=
∫
𝐼
𝐷
D
I
	​

=∫
I
	​

D,

∥
𝛽
′
′
(
𝑓
)
∇
𝑓
⋅
𝐽
∥
𝐿
1
(
𝐼
)
≤
∥
𝛽
′
′
∥
∞
4
2
𝐷
𝐼
(
𝐷
𝐼
+
8
𝜋
𝑀
𝐿
)
.
∥β
′′
(f)∇f⋅J∥
L
1
(I)
	​

≤
4
∥β
′′
∥
∞
	​

	​

2D
I
	​

(D
I
	​

+8πML)
	​

.

Because 
𝐷
D is integrable on 
[
0
,
∞
)
[0,∞), both source terms tend to zero on every fixed-length late-time window. In particular, both

𝑓
,
𝑔
=
𝑓
−
𝑓
2
f,g=f−f
2

are asymptotically free-transport solutions on such windows. The logarithmic bounds also give the analogous statement for entropy itself, although it is not necessary for the compactness argument below.

6. A velocity-averaging lemma with the needed source class

The source remainder above is only 
𝐿
1
L
1
. The following elementary Fourier argument avoids assuming an unavailable stronger averaging theorem.

Suppose 
𝑢
𝑘
u
k
	​

 are bounded in 
𝐿
2
(
𝑡
,
𝑥
,
𝑣
)
L
2
(t,x,v), compactly supported in time and velocity, and

(
∂
𝑡
+
𝑣
⋅
∇
𝑥
)
𝑢
𝑘
=
∇
𝑣
⋅
𝐹
𝑘
+
𝐺
𝑘
,
(∂
t
	​

+v⋅∇
x
	​

)u
k
	​

=∇
v
	​

⋅F
k
	​

+G
k
	​

,

where 
𝐹
𝑘
,
𝐺
𝑘
F
k
	​

,G
k
	​

 are bounded in 
𝐿
1
L
1
. Then compactly supported velocity averages of 
𝑢
𝑘
u
k
	​

 are relatively compact in 
𝐿
l
o
c
1
(
𝑡
,
𝑥
)
L
loc
1
	​

(t,x).

For completeness, on a spacetime frequency shell 
∣
𝜉
∣
≍
2
𝑗
∣ξ∣≍2
j
, split at

∣
𝜔
+
𝑘
⋅
𝑣
∣
≤
𝛿
∣
𝜉
∣
.
∣ω+k⋅v∣≤δ∣ξ∣.

The resonant velocity slab has measure 
𝑂
(
𝛿
)
O(δ), or is empty when the temporal frequency dominates. Cauchy and Plancherel bound its averaged contribution in 
𝐿
2
L
2
 by

𝐶
𝛿
1
/
2
∥
𝑢
𝑘
∥
2
.
Cδ
1/2
∥u
k
	​

∥
2
	​

.

For the nonresonant part, divide the transport equation by 
𝑖
(
𝜔
+
𝑘
⋅
𝑣
)
i(ω+k⋅v), integrate the velocity divergence by parts, and use the dyadic cutoff. The multiplier and its first velocity derivative have convolution-kernel 
𝐿
1
L
1
 bounds

𝐶
2
−
𝑗
𝛿
−
𝑁
C2
−j
δ
−N

for a fixed integer 
𝑁
N; taking 
𝑁
=
20
N=20 is more than sufficient for the finitely many frequency derivatives needed in four spacetime dimensions. Thus, on a fixed spacetime compact set 
𝐾
K,

∥
𝑃
𝑗
∫
𝑢
𝑘
 
𝑑
𝑣
∥
𝐿
1
(
𝐾
)
≤
𝐶
𝐾
𝛿
1
/
2
∥
𝑢
𝑘
∥
2
+
𝐶
2
−
𝑗
𝛿
−
𝑁
(
∥
𝐹
𝑘
∥
1
+
∥
𝐺
𝑘
∥
1
)
.
	​

P
j
	​

∫u
k
	​

dv
	​

L
1
(K)
	​

≤C
K
	​

δ
1/2
∥u
k
	​

∥
2
	​

+C2
−j
δ
−N
(∥F
k
	​

∥
1
	​

+∥G
k
	​

∥
1
	​

).

Choose

𝛿
=
2
−
𝑗
/
(
2
𝑁
)
.
δ=2
−j/(2N)
.

The high-frequency bounds are summable uniformly in 
𝑘
k; the low-frequency parts are compact. Time and velocity cutoffs add only bounded 
𝐿
1
L
1
 commutators.

Apply this lemma to cutoffs of 
𝑓
f and 
𝑔
=
𝑓
−
𝑓
2
g=f−f
2
, using Section 5.

7. Every late-time limit is homogeneous Fermi–Dirac

Take any 
𝑡
𝑘
→
∞
t
k
	​

→∞, and consider

𝑓
𝑘
(
𝑡
,
𝑥
,
𝑣
)
=
𝑓
(
𝑡
𝑘
+
𝑡
,
𝑥
,
𝑣
)
.
f
k
	​

(t,x,v)=f(t
k
	​

+t,x,v).

By diagonal extraction, limits are defined for all finite positive and negative shifted times. Let

𝑓
𝑘
⇀
𝑓
∞
,
𝑔
𝑘
=
𝑓
𝑘
(
1
−
𝑓
𝑘
)
⇀
𝑔
ˉ
.
f
k
	​

⇀f
∞
	​

,g
k
	​

=f
k
	​

(1−f
k
	​

)⇀
g
ˉ
	​

.

Both limits solve free transport. Their velocity averages converge strongly locally in spacetime by Section 6.

The mass and momentum tails are uniformly controlled by energy:

∫
∣
𝑣
∣
>
𝑅
𝑓
𝑘
≤
𝐸
/
𝑅
2
,
∫
∣
𝑣
∣
>
𝑅
∣
𝑣
∣
𝑓
𝑘
≤
𝐸
/
𝑅
.
∫
∣v∣>R
	​

f
k
	​

≤E/R
2
,∫
∣v∣>R
	​

∣v∣f
k
	​

≤E/R.

Hence the limit retains 
𝑀
,
𝑃
M,P, while its energy is at most 
𝐸
E.

7.1 Strong convergence on warm slices

Call a spacetime point warm when

∫
𝑔
ˉ
(
𝑡
,
𝑥
,
𝑣
)
 
𝑑
𝑣
>
0.
∫
g
ˉ
	​

(t,x,v)dv>0.

The uniform particle-hole mass in Section 4 ensures that warm points have positive spatial measure at almost every time.

On a measurable subset where

∫
𝐵
𝑅
0
𝑔
ˉ
 
𝑑
𝑣
≥
2
𝑎
>
0
,
∫
B
R
0
	​

	​

	​

g
ˉ
	​

dv≥2a>0,

strong convergence of velocity averages and Egorov’s theorem give

∫
𝐵
𝑅
0
𝑔
𝑘
 
𝑑
𝑣
≥
𝑎
∫
B
R
0
	​

	​

	​

g
k
	​

dv≥a

outside an arbitrarily small spacetime exceptional set.

Since 
𝑔
𝑘
≤
1
/
4
g
k
	​

≤1/4, this implies a quantitative ellipticity bound on every fixed velocity ball:

𝐴
[
𝑔
𝑘
]
(
𝑣
)
≥
𝑐
 
𝑎
2
𝑅
0
(
𝑅
+
𝑅
0
)
3
𝐼
,
∣
𝑣
∣
≤
𝑅
.
A[g
k
	​

](v)≥c
R
0
	​

(R+R
0
	​

)
3
a
2
	​

I,∣v∣≤R.

One proof excludes a thin cylinder around the line 
𝑣
+
𝑅
𝜉
v+Rξ. Its 
𝑔
𝑘
g
k
	​

-mass is at most one quarter its volume; choosing the cylinder radius to leave at least 
𝑎
/
2
a/2 of the mass outside gives the displayed estimate.

The uniform bound on 
∫
𝐼
(
𝑓
𝑘
)
∫I(f
k
	​

) therefore controls 
∇
𝑣
𝑓
𝑘
∇
v
	​

f
k
	​

 in 
𝐿
2
L
2
 on these good sets. Velocity mollification gives

∥
𝑓
𝑘
−
𝑓
𝑘
∗
𝜑
𝜂
∥
𝐿
2
≤
𝐶
𝜂
∥
∇
𝑣
𝑓
𝑘
∥
𝐿
2
.
∥f
k
	​

−f
k
	​

∗φ
η
	​

∥
L
2
	​

≤Cη∥∇
v
	​

f
k
	​

∥
L
2
	​

.

For fixed 
𝜂
η, the mollified functions converge strongly by velocity averaging. Exhausting the warm set gives strong local convergence of 
𝑓
𝑘
f
k
	​

 there, and

𝑔
ˉ
=
𝑓
∞
(
1
−
𝑓
∞
)
g
ˉ
	​

=f
∞
	​

(1−f
∞
	​

)

on the warm set.

7.2 Zero dissipation gives a Fermi–Dirac profile on each warm slice

The identity

𝐷
(
𝑓
𝑘
)
=
1
2
∫
∣
𝑎
(
𝑣
−
𝑤
)
1
/
2
(
𝑔
𝑘
(
𝑤
)
∇
𝑓
𝑘
(
𝑣
)
−
𝑔
𝑘
(
𝑣
)
∇
𝑓
𝑘
(
𝑤
)
)
∣
2
𝑔
𝑘
(
𝑣
)
𝑔
𝑘
(
𝑤
)
D(f
k
	​

)=
2
1
	​

∫
g
k
	​

(v)g
k
	​

(w)
	​

a(v−w)
1/2
(g
k
	​

(w)∇f
k
	​

(v)−g
k
	​

(v)∇f
k
	​

(w))
	​

2
	​


and 
𝑔
𝑘
(
𝑣
)
𝑔
𝑘
(
𝑤
)
≤
1
/
16
g
k
	​

(v)g
k
	​

(w)≤1/16 imply

𝐷
(
𝑓
𝑘
)
≥
8
∫
∣
𝑎
(
𝑣
−
𝑤
)
1
/
2
(
𝑔
𝑘
(
𝑤
)
∇
𝑓
𝑘
(
𝑣
)
−
𝑔
𝑘
(
𝑣
)
∇
𝑓
𝑘
(
𝑤
)
)
∣
2
.
D(f
k
	​

)≥8∫
	​

a(v−w)
1/2
(g
k
	​

(w)∇f
k
	​

(v)−g
k
	​

(v)∇f
k
	​

(w))
	​

2
.

Since the shifted dissipation tends to zero, strong convergence of 
𝑔
𝑘
g
k
	​

 and weak 
𝐻
𝑣
1
H
v
1
	​

 convergence yield

Π
(
𝑣
−
𝑤
)
(
𝑔
(
𝑤
)
∇
𝑓
(
𝑣
)
−
𝑔
(
𝑣
)
∇
𝑓
(
𝑤
)
)
=
0
Π(v−w)(g(w)∇f(v)−g(v)∇f(w))=0

on almost every warm slice.

Choose a compactly supported 
𝜓
≥
0
ψ≥0 with 
∫
𝑔
𝜓
>
0
∫gψ>0. Integrating the identity against 
𝜓
(
𝑤
)
ψ(w) gives

𝐴
[
𝑔
𝜓
]
∇
𝑓
=
𝑔
 
𝐵
𝜓
,
𝐵
𝜓
(
𝑣
)
=
∫
𝑎
(
𝑣
−
𝑤
)
𝜓
(
𝑤
)
∇
𝑓
(
𝑤
)
 
𝑑
𝑤
.
A[gψ]∇f=gB
ψ
	​

,B
ψ
	​

(v)=∫a(v−w)ψ(w)∇f(w)dw.

The matrix 
𝐴
[
𝑔
𝜓
]
A[gψ] is uniformly positive on bounded velocity sets. Also 
𝐵
𝜓
B
ψ
	​

 is locally bounded because 
∇
𝑓
∈
𝐿
l
o
c
2
∇f∈L
loc
2
	​

 and 
1
/
∣
𝑧
∣
∈
𝐿
l
o
c
2
(
𝑅
3
)
1/∣z∣∈L
loc
2
	​

(R
3
). Thus

∇
𝑓
=
𝑓
(
1
−
𝑓
)
𝑊
∇f=f(1−f)W

with 
𝑊
W locally bounded.

Logistic comparison along line segments propagates one particle-hole point to

0
<
𝑓
(
𝑣
)
<
1
for every finite 
𝑣
.
0<f(v)<1for every finite v.

The logit is locally Lipschitz, and

Π
(
𝑣
−
𝑤
)
(
∇
ℎ
(
𝑣
)
−
∇
ℎ
(
𝑤
)
)
=
0.
Π(v−w)(∇h(v)−∇h(w))=0.

Mollifying by common translations reduces this to the elementary smooth rigidity statement: if every gradient difference is parallel to 
𝑣
−
𝑤
v−w, then the Hessian is a scalar multiple of the identity, and that scalar is constant. Consequently,

ℎ
(
𝑣
)
=
𝑎
+
𝑏
⋅
𝑣
+
𝑐
∣
𝑣
∣
2
.
h(v)=a+b⋅v+c∣v∣
2
.

Finite positive mass requires 
𝑐
<
0
c<0. Each warm slice is therefore a positive-temperature Fermi–Dirac profile.

7.3 Free transport propagates warmth to all spatial points

Choose a time 
𝑠
s at which the warm spatial set has positive measure. Restrict to a positive-measure subset 
𝑌
Y on which the finite Fermi–Dirac parameters are bounded. Then, for every fixed bounded velocity ball,

𝑔
ˉ
(
𝑠
,
𝑦
,
𝑣
)
≥
𝑐
>
0
(
𝑦
∈
𝑌
)
.
g
ˉ
	​

(s,y,v)≥c>0(y∈Y).

Free transport gives

𝑔
ˉ
(
𝑡
,
𝑥
,
𝑣
)
=
𝑔
ˉ
(
𝑠
,
𝑥
−
(
𝑡
−
𝑠
)
𝑣
,
𝑣
)
.
g
ˉ
	​

(t,x,v)=
g
ˉ
	​

(s,x−(t−s)v,v).

For 
𝑡
≠
𝑠
t

=s, a bounded velocity cube maps onto the torus under

𝑣
↦
𝑥
−
(
𝑡
−
𝑠
)
𝑣
.
v↦x−(t−s)v.

The inverse image of 
𝑌
Y has positive velocity measure for almost every 
𝑥
x. Thus every spatial point is warm, up to null sets, at almost every 
𝑡
≠
𝑠
t

=s.

It follows that the strong convergence established in Section 7.1 holds locally throughout spacetime.

7.4 Periodic free transport makes the Fermi–Dirac parameters constant

On compact time intervals separated from 
𝑠
s, the preceding construction supplies, at every spatial point, a positive-measure subset of a fixed velocity ball on which 
𝑔
ˉ
≥
𝑐
g
ˉ
	​

≥c. Hence the quadratic logit is bounded on a set of uniformly positive velocity measure.

A finite-dimensional polynomial argument bounds all its coefficients uniformly. Otherwise normalized quadratics would converge to a nonzero quadratic vanishing on a set of positive measure, which is impossible.

Thus the logit is locally integrable in spacetime and itself satisfies free transport:

(
∂
𝑡
+
𝑣
⋅
∇
𝑥
)
(
𝑎
(
𝑡
,
𝑥
)
+
𝑏
(
𝑡
,
𝑥
)
⋅
𝑣
+
𝑐
(
𝑡
,
𝑥
)
∣
𝑣
∣
2
)
=
0.
(∂
t
	​

+v⋅∇
x
	​

)(a(t,x)+b(t,x)⋅v+c(t,x)∣v∣
2
)=0.

Comparison of polynomial coefficients gives

∇
𝑥
𝑐
=
0
,
∇
x
	​

c=0,
sym
⁡
∇
𝑥
𝑏
+
𝑐
𝑡
𝐼
=
0
,
sym∇
x
	​

b+c
t
	​

I=0,
∇
𝑥
𝑎
+
𝑏
𝑡
=
0
,
𝑎
𝑡
=
0.
∇
x
	​

a+b
t
	​

=0,a
t
	​

=0.

Periodicity forces 
𝑐
𝑡
=
0
c
t
	​

=0, makes 
𝑏
b spatially constant, then gives 
𝑏
𝑡
=
0
b
t
	​

=0 and 
∇
𝑥
𝑎
=
0
∇
x
	​

a=0. All parameters are constant.

Every shifted limit is therefore one homogeneous Fermi–Dirac state.

8. Uniqueness of the limiting equilibrium and convergence at every time

Strong local convergence and uniform entropy tails give

𝑆
(
𝐹
∞
)
=
lim
⁡
𝑡
→
∞
𝑆
(
𝑓
(
𝑡
)
)
=
:
𝑆
∞
.
S(F
∞
	​

)=
t→∞
lim
	​

S(f(t))=:S
∞
	​

.

At fixed 
𝑀
,
𝑃
M,P, Fermi–Dirac entropy is strictly increasing with energy. Indeed, for 
𝐸
2
>
𝐸
1
E
2
	​

>E
1
	​

,

𝑆
(
𝐹
𝐸
2
)
−
𝑆
(
𝐹
𝐸
1
)
=
𝐻
(
𝐹
𝐸
1
∣
𝐹
𝐸
2
)
+
𝛽
𝐸
2
(
𝐸
2
−
𝐸
1
)
>
0.
S(F
E
2
	​

	​

)−S(F
E
1
	​

	​

)=H(F
E
1
	​

	​

∣F
E
2
	​

	​

)+β
E
2
	​

	​

(E
2
	​

−E
1
	​

)>0.

Therefore 
𝑀
,
𝑃
,
𝑆
∞
M,P,S
∞
	​

 determine one Fermi–Dirac state. Every shifted subsequence has the same limit, giving convergence in 
𝐿
1
L
1
 on late unit windows.

To exclude time spikes, set

𝑊
(
𝑡
)
=
∥
𝑓
(
𝑡
)
−
𝐹
∞
∥
2
2
.
W(t)=∥f(t)−F
∞
	​

∥
2
2
	​

.

The renormalized 
𝑓
2
f
2
 equation and the global flux estimate give

∣
𝑊
′
(
𝑡
)
∣
≤
1
2
2
𝐷
(
𝑡
)
(
𝐷
(
𝑡
)
+
8
𝜋
𝑀
)
+
𝐶
𝐹
∞
𝐸
𝐷
(
𝑡
)
.
∣W
′
(t)∣≤
2
1
	​

2D(t)(D(t)+8πM)
	​

+C
F
∞
	​

	​

ED(t)
	​

.

Its integral on late unit windows tends to zero. The average of 
𝑊
W on those windows tends to zero by the already established 
𝐿
1
L
1
 convergence and 
0
≤
𝑓
,
𝐹
∞
≤
1
0≤f,F
∞
	​

≤1. Hence

𝑊
(
𝑡
)
→
0
W(t)→0

at every time. Velocity mass tails then give

∥
𝑓
(
𝑡
)
−
𝐹
∞
∥
1
→
0.
∥f(t)−F
∞
	​

∥
1
	​

→0.

This completes the partial theorem.

9. The energy-retention gap cannot be removed by instantaneous invariant-only coercivity

Here is the fully checked Gaussian-halo family.

Take 
𝑃
=
0
P=0, choose 
𝛿
>
0
δ>0 such that

𝐸
−
𝛿
>
𝐸
P
(
𝑀
,
0
)
,
E−δ>E
P
	​

(M,0),

and fix a Gaussian variance 
𝜎
2
>
0
σ
2
>0. Let

𝑚
𝑅
=
𝛿
𝑅
2
+
3
𝜎
2
.
m
R
	​

=
R
2
+3σ
2
δ
	​

.

Let 
𝐶
𝑅
C
R
	​

 be the Fermi–Dirac state with mass 
𝑀
−
𝑚
𝑅
M−m
R
	​

, momentum zero, and energy 
𝐸
−
𝛿
E−δ. Put

𝐻
𝑅
(
𝑣
)
=
𝑚
𝑅
2
(
𝐺
𝜎
(
𝑣
−
𝑅
𝑒
1
)
+
𝐺
𝜎
(
𝑣
+
𝑅
𝑒
1
)
)
,
𝑓
𝑅
=
𝐶
𝑅
+
𝐻
𝑅
.
H
R
	​

(v)=
2
m
R
	​

	​

(G
σ
	​

(v−Re
1
	​

)+G
σ
	​

(v+Re
1
	​

)),f
R
	​

=C
R
	​

+H
R
	​

.

For all sufficiently large 
𝑅
R, these are admissible smooth, spatially homogeneous Schwartz densities with exact invariants

𝑀
(
𝑓
𝑅
)
=
𝑀
,
𝑃
(
𝑓
𝑅
)
=
0
,
𝐸
(
𝑓
𝑅
)
=
𝐸
.
M(f
R
	​

)=M,P(f
R
	​

)=0,E(f
R
	​

)=E.

They have a uniform particle-hole seed ball and a uniform global desaturation bound

𝑓
𝑅
≤
1
−
𝜅
.
f
R
	​

≤1−κ.

They converge in 
𝐿
1
L
1
 to 
𝐹
𝑀
,
0
,
𝐸
−
𝛿
F
M,0,E−δ
	​

, while

𝐻
(
𝑓
𝑅
∣
𝐹
𝑀
,
0
,
𝐸
)
⟶
𝑆
(
𝐹
𝑀
,
0
,
𝐸
)
−
𝑆
(
𝐹
𝑀
,
0
,
𝐸
−
𝛿
)
>
0.
H(f
R
	​

∣F
M,0,E
	​

)⟶S(F
M,0,E
	​

)−S(F
M,0,E−δ
	​

)>0.

Nevertheless,

𝐷
(
𝑓
𝑅
)
=
𝑂
(
𝑚
𝑅
)
⟶
0.
D(f
R
	​

)=O(m
R
	​

)⟶0.
	​


Here are the denominator and cross-term details.

Since 
𝐶
𝑅
C
R
	​

 stays in a compact positive-temperature parameter family,

sup
⁡
𝐶
𝑅
≤
1
−
𝜅
0
,
sup
⁡
𝐻
𝑅
≤
𝐶
𝜎
𝑚
𝑅
.
supC
R
	​

≤1−κ
0
	​

,supH
R
	​

≤C
σ
	​

m
R
	​

.

Therefore

1
1
−
𝐶
𝑅
−
𝐻
𝑅
≤
1
+
𝐾
𝑚
𝑅
1
−
𝐶
𝑅
.
1−C
R
	​

−H
R
	​

1
	​

≤
1−C
R
	​

1+Km
R
	​

	​

.

Also

𝑔
(
𝐶
𝑅
+
𝐻
𝑅
)
≤
𝑔
(
𝐶
𝑅
)
+
𝐻
𝑅
,
g(C
R
	​

+H
R
	​

)≤g(C
R
	​

)+H
R
	​

,

so

𝐴
[
𝑔
(
𝑓
𝑅
)
]
≤
𝐴
[
𝑔
(
𝐶
𝑅
)
]
+
𝐴
[
𝐻
𝑅
]
A[g(f
R
	​

)]≤A[g(C
R
	​

)]+A[H
R
	​

]

in the positive-semidefinite order.

For any positive-semidefinite matrix 
𝐴
A, the perspective inequality gives

∣
∇
(
𝐶
+
𝐻
)
∣
𝐴
2
𝐶
+
𝐻
≤
∣
∇
𝐶
∣
𝐴
2
𝐶
+
∣
∇
𝐻
∣
𝐴
2
𝐻
.
C+H
∣∇(C+H)∣
A
2
	​

	​

≤
C
∣∇C∣
A
2
	​

	​

+
H
∣∇H∣
A
2
	​

	​

.

Applying it before the 
1
/
(
1
−
𝑓
𝑅
)
1/(1−f
R
	​

) estimate yields

𝐼
(
𝑓
𝑅
)
≤
(
1
+
𝐾
𝑚
𝑅
)
(
𝐼
(
𝐶
𝑅
)
+
𝐶
𝑚
𝑅
)
.
I(f
R
	​

)≤(1+Km
R
	​

)(I(C
R
	​

)+Cm
R
	​

).

The error estimates are

∥
𝐴
[
𝐻
𝑅
]
∥
∞
=
𝑂
(
𝑚
𝑅
)
,
∥
𝐴
[
𝑔
(
𝐶
𝑅
)
]
∥
∞
=
𝑂
(
1
)
,
∥A[H
R
	​

]∥
∞
	​

=O(m
R
	​

),∥A[g(C
R
	​

)]∥
∞
	​

=O(1),
∫
∣
∇
𝐻
𝑅
∣
2
𝐻
𝑅
≤
3
𝑚
𝑅
𝜎
2
,
∫
∣
∇
𝐶
𝑅
∣
2
𝐶
𝑅
=
𝑂
(
1
)
.
∫
H
R
	​

∣∇H
R
	​

∣
2
	​

≤
σ
2
3m
R
	​

	​

,∫
C
R
	​

∣∇C
R
	​

∣
2
	​

=O(1).

Thus every cross contribution is charged. Finally,

𝐼
(
𝐶
𝑅
)
=
8
𝜋
∫
𝐶
𝑅
2
,
∫
𝑓
𝑅
2
≥
∫
𝐶
𝑅
2
,
I(C
R
	​

)=8π∫C
R
2
	​

,∫f
R
2
	​

≥∫C
R
2
	​

,

and the exact Coulomb identity gives 
𝐷
(
𝑓
𝑅
)
≤
𝐶
𝑚
𝑅
D(f
R
	​

)≤Cm
R
	​

.

This family rules out an instantaneous inequality of the form

𝐷
(
𝑓
)
≥
Ψ
(
𝐻
(
𝑓
∣
𝐹
𝑀
,
𝑃
,
𝐸
)
)
,
Ψ
(
𝑧
)
>
0
 for 
𝑧
>
0
,
D(f)≥Ψ(H(f∣F
M,P,E
	​

)),Ψ(z)>0 for z>0,

whose constants use only the fixed invariants and the displayed uniform core/desaturation information.

It is not a nonthermalizing trajectory. Each 
𝑓
𝑅
f
R
	​

 is a different possible initial condition. It does not rule out a dynamical estimate using the fixed initial high moments.

10. Independent energy-retention test

The homogeneous 
𝐿
1
L
1
 limit does not make relative entropy to that limit vanish. Exactly,

𝐻
(
𝑓
(
𝑡
)
∣
𝐹
∞
)
=
𝑆
(
𝐹
∞
)
−
𝑆
(
𝑓
(
𝑡
)
)
+
𝛽
∞
(
𝐸
−
𝐸
∞
)
,
H(f(t)∣F
∞
	​

)=S(F
∞
	​

)−S(f(t))+β
∞
	​

(E−E
∞
	​

),

so

lim
⁡
𝑡
→
∞
𝐻
(
𝑓
(
𝑡
)
∣
𝐹
∞
)
=
𝛽
∞
(
𝐸
−
𝐸
∞
)
.
t→∞
lim
	​

H(f(t)∣F
∞
	​

)=β
∞
	​

(E−E
∞
	​

).

This is the energy defect itself.

A potentially sufficient dynamical route would combine a sharp high-moment growth estimate with a Coulomb tail-dissipation bound. For example, bounds of the schematic form

𝑀
𝑠
(
𝑡
)
≲
(
1
+
𝑡
)
(
𝑠
−
2
)
/
3
M
s
	​

(t)≲(1+t)
(s−2)/3

and

𝐷
(
𝑡
)
≳
(
persistent energy defect
)
 
𝑞
𝑀
𝑠
(
𝑡
)
3
/
(
𝑠
−
2
)
D(t)≳
M
s
	​

(t)
3/(s−2)
(persistent energy defect)
q
	​


would force a nonintegrable 
1
/
𝑡
1/t dissipation cost if the defect were positive.

I have not established those estimates for the inhomogeneous equation. In particular:

Global 
𝐿
1
L
1
 convergence does not give a uniform local-in-
𝑥
x warm core for the actual solution.
The spacetime 
𝜌
2
ρ
2
 estimate obtained by the root from compensated integrability does not automatically control the mixed local moments needed in this argument.
A naive bound such as 
𝑀
3
′
≲
∫
𝜌
2
M
3
′
	​

≲∫ρ
2
 is not justified. A narrow anisotropic velocity cloud boosted to a large local mean velocity can create a large 
∣
𝑣
∣
3
∣v∣
3
-moment derivative during stress relaxation while leaving its density unchanged.
Uniform local cores alone do not fix instantaneous entropy coercivity, as the halo family already has such cores.

A genuinely dynamical estimate preventing the persistent transfer of fixed energy into vanishing mass at increasing velocities remains necessary.

11. Source and exposure record

The full successful governing read in this branch was Alonso–Bagland–Desvillettes–Lods, About the Use of Entropy Production for the Landau–Fermi–Dirac Equation (2021), including Theorem 1.8 and its normalized homogeneous scope. Its weighted Fisher estimate is credited, but no spatial coercivity or hard-potential/small-quantum-parameter conclusion is imported. The argument above derives the particular Coulomb identities and compactness steps directly.

The Golding–Henderson body was not successfully read: the initial HTML request failed with DisabledError, and no retry or alternative recovery was made. Its finite-horizon/global solution properties are used solely at the accepted scope supplied in the task.

The held Serre 2024 body was not recovered. The root’s separate use of the successfully read Serre 2018 convex-box theorem is independent capital; it is not needed for the partial theorem above.

The root reports accidental first-page introduction exposure from the held Carlo Alberto PDF during a broad search. No theorem from that exposure is used here, and no further recovery was attempted.

The full requested same-energy entropic thermalization theorem remains unresolved. The precise missing assertion is 
𝐸
∞
=
𝐸
E
∞
	​

=E; no actual countertrajectory has been constructed.

=== LFD RIGIDITY VISIBLE TREE ===
Lfd rigidity
Status
Done
Final response
Consolidated audit

The proposed argument supports the following weaker, unconditional conclusion within the supplied finite-time classical solution class:

𝑓
(
𝑡
)
⟶
𝐹
∗
in 
𝐿
1
(
𝑇
3
×
𝑅
3
)
,
f(t)⟶F
∗
	​

in L
1
(T
3
×R
3
),

where 
𝐹
∗
F
∗
	​

 is a homogeneous Fermi–Dirac distribution with

𝑀
∗
=
𝑀
,
𝑃
∗
=
𝑃
,
𝐸
∗
≤
𝐸
.
M
∗
	​

=M,P
∗
	​

=P,E
∗
	​

≤E.

Its entropy is the limiting entropy of the actual trajectory:

𝑆
(
𝐹
∗
)
=
lim
⁡
𝑡
→
∞
𝑆
(
𝑓
(
𝑡
)
)
.
S(F
∗
	​

)=
t→∞
lim
	​

S(f(t)).

I found no fatal gap in the conservation, entropy, averaging, warming, rigidity, or all-time convergence steps once written as described below. The equality 
𝐸
∗
=
𝐸
E
∗
	​

=E remains unproved. Consequently this does not yet establish convergence to the equilibrium specified in the full question.

1. Conservation and entropy passages

Conservation can be established first from the symmetrized weak collision formula, which depends on 
𝑓
f rather than its derivatives. The Pauli cap gives

𝜌
(
𝑥
)
≤
𝐶
𝑒
(
𝑥
)
3
/
5
,
∬
𝑓
(
𝑣
)
𝑓
(
𝑣
∗
)
∣
𝑣
−
𝑣
∗
∣
 
𝑑
𝑣
 
𝑑
𝑣
∗
≤
𝐶
𝑒
(
𝑥
)
.
ρ(x)≤Ce(x)
3/5
,∬
∣v−v
∗
	​

∣
f(v)f(v
∗
	​

)
	​

dvdv
∗
	​

≤Ce(x).

Cutoffs of 
1
,
𝑣
𝑖
,
∣
𝑣
∣
2
1,v
i
	​

,∣v∣
2
 therefore pass to the limit using finite-horizon energy bounds. The energy integrand cancels exactly for the specified Coulomb kernel.

The squared-cutoff entropy estimate is also valid. For

𝑔
=
𝑓
(
1
−
𝑓
)
,
ℎ
=
log
⁡
𝑓
1
−
𝑓
,
g=f(1−f),h=log
1−f
f
	​

,

the inequalities

∫
𝑓
𝑝
 
𝑑
𝑣
≤
𝐶
𝑝
𝑒
3
/
5
(
3
/
5
<
𝑝
<
1
)
,
∫f
p
dv≤C
p
	​

e
3/5
(3/5<p<1),
𝐴
𝑔
≤
𝐶
𝑒
2
/
5
𝐼
,
∣
𝐵
𝑓
∣
≤
𝐶
𝑒
1
/
5
,
A
g
	​

≤Ce
2/5
I,∣B
f
	​

∣≤Ce
1/5
,

give

∫
𝑔
ℎ
2
∥
𝐴
𝑔
∥
≤
𝐶
𝐸
,
∫
(
𝑓
+
𝑔
∣
ℎ
∣
)
∣
𝐵
𝑓
∣
≤
𝐶
𝐸
4
/
5
.
∫gh
2
∥A
g
	​

∥≤CE,∫(f+g∣h∣)∣B
f
	​

∣≤CE
4/5
.

They pay the entropy-cutoff boundary terms and yield finite integrated weighted Fisher information.

Once that information is finite, pairwise Cauchy–Schwarz makes the cross term absolutely integrable. Two velocity cutoffs then give

𝐷
(
𝑓
)
=
𝐼
𝐴
(
𝑓
)
−
8
𝜋
∫
𝑓
2
,
D(f)=I
A
	​

(f)−8π∫f
2
,

with errors bounded by

𝐶
𝐸
4
/
5
/
𝑅
+
𝐶
𝐸
/
𝑅
2
.
CE
4/5
/R+CE/R
2
.

No unverified derivative-tail bound or future uniform regularity is needed for these passages.

2. The compactness mechanism is viable

The estimates

∫
∣
∇
𝑓
⋅
𝐽
∣
≤
1
4
2
𝐷
(
𝐷
+
8
𝜋
𝑀
)
∫∣∇f⋅J∣≤
4
1
	​

2D(D+8πM)
	​


and

∥
𝐽
∥
1
≤
𝐶
𝐸
𝐷
∥J∥
1
	​

≤C
ED
	​


make every 
𝐶
2
C
2
 renormalization almost freely transported on late windows of fixed length. In particular, both 
𝑓
f and 
𝑔
=
𝑓
(
1
−
𝑓
)
g=f(1−f) have this property.

The required velocity-averaging compactness can be proved directly. For dyadic spacetime frequency 
2
𝑗
2
j
, split at resonance width

𝛿
𝑗
=
2
−
𝑗
/
24
.
δ
j
	​

=2
−j/24
.

The resonant velocity average has an 
𝐿
2
L
2
 bound 
𝑂
(
2
−
𝑗
/
48
)
O(2
−j/48
); the nonresonant term has an 
𝐿
1
L
1
 bound 
𝑂
(
2
−
𝑗
/
2
)
O(2
−j/2
). These follow from the velocity-slab estimate and a conservative multiplier-kernel bound

𝐶
2
−
𝑗
𝛿
𝑗
−
12
.
C2
−j
δ
j
−12
	​

.

Their tails are summable, while low-frequency averages are precompact locally.

Strong averages of 
𝑔
g identify warm sets. On each warm set, the Pauli cap and positive 
𝑔
g-mass provide local ellipticity. The Fisher-information bound then controls velocity gradients. Velocity mollification combined with strong averages makes 
𝑓
f strongly compact there. The masks used to remove exceptional points depend only on 
(
𝑡
,
𝑥
)
(t,x), so they do not disrupt the velocity derivative argument.

3. Warming and Fermi–Dirac rigidity are legitimate

The zero-dissipation residual on a warm slice can be integrated against a compact velocity test to obtain

𝐴
𝜒
∇
𝑓
=
𝑔
𝐵
𝜒
.
A
χ
	​

∇f=gB
χ
	​

.

The matrix 
𝐴
𝜒
A
χ
	​

 is locally elliptic. The field 
𝐵
𝜒
B
χ
	​

 is locally bounded because 
∇
𝑓
∈
𝐿
l
o
c
2
∇f∈L
loc
2
	​

 and the Coulomb kernel belongs to 
𝐿
l
o
c
2
L
loc
2
	​

 in three dimensions. Thus

∇
𝑓
=
𝑔
𝑊
,
𝑊
∈
𝐿
l
o
c
∞
.
∇f=gW,W∈L
loc
∞
	​

.

Applying this to 
log
⁡
(
𝑓
+
𝜂
)
log(f+η) and 
log
⁡
(
1
−
𝑓
+
𝜂
)
log(1−f+η), then letting 
𝜂
↓
0
η↓0, gives strict particle–hole positivity throughout velocity space. The pair identity forces the logit to be quadratic in 
𝑣
v, giving a local Fermi–Dirac profile.

The free-transport limit of 
𝑔
g spreads a positive-measure warm spatial set to almost every spatial point at every nonzero time displacement. A velocity fundamental cell of side 
1
/
∣
𝑡
−
𝑡
0
∣
1/∣t−t
0
	​

∣ makes this change-of-variables argument explicit.

The coefficient-control argument is sound as well. At a generic source time, select a positive-measure spatial subset with bounded Fermi–Dirac coefficients. Free transport bounds the later logit polynomial on a velocity subset of uniformly positive measure. A finite-dimensional Remez argument bounds all its coefficients. Two generic source times cover a compact time interval, ensuring that the logit is locally integrable and satisfies the transport equation distributionally.

The resulting polynomial coefficient equations on the torus force a homogeneous, time-independent 
𝐹
∗
F
∗
	​

.

4. Spacetime convergence upgrades to convergence at every time

Let

𝐴
(
𝑡
)
=
∫
𝑓
(
𝑡
)
2
,
𝐵
(
𝑡
)
=
∫
𝑓
(
𝑡
)
𝐹
∗
.
A(t)=∫f(t)
2
,B(t)=∫f(t)F
∗
	​

.

The established flux bounds give vanishing late-window oscillations of both quantities. Spacetime strong convergence gives a vanishing window average of

∥
𝑓
(
𝑡
)
−
𝐹
∗
∥
2
2
=
𝐴
(
𝑡
)
−
2
𝐵
(
𝑡
)
+
∥
𝐹
∗
∥
2
2
.
∥f(t)−F
∗
	​

∥
2
2
	​

=A(t)−2B(t)+∥F
∗
	​

∥
2
2
	​

.

Vanishing oscillation therefore gives all-time 
𝐿
2
L
2
 convergence. Finally,

∥
𝑓
(
𝑡
)
−
𝐹
∗
∥
1
≤
∣
𝐵
𝑅
∣
1
/
2
∥
𝑓
(
𝑡
)
−
𝐹
∗
∥
2
+
𝐸
+
𝐸
∗
𝑅
2
∥f(t)−F
∗
	​

∥
1
	​

≤∣B
R
	​

∣
1/2
∥f(t)−F
∗
	​

∥
2
	​

+
R
2
E+E
∗
	​

	​


gives all-time 
𝐿
1
L
1
 convergence.

Uniform entropy-tail control identifies 
𝑆
(
𝐹
∗
)
=
𝑆
∞
S(F
∗
	​

)=S
∞
	​

. The mass, momentum and entropy uniquely identify 
𝐹
∗
F
∗
	​

: at fixed mass and momentum, the entropy of a positive-temperature Fermi–Dirac distribution is strictly increasing with its energy.

The exact unclosed operation

The second moment is only lower semicontinuous in the compactness argument. A vanishing mass may carry a positive energy defect to velocities tending to infinity.

Writing

Δ
=
𝐸
−
𝐸
∗
≥
0
,
Δ=E−E
∗
	​

≥0,

the actual relative entropy has the precise limiting expression

lim
⁡
𝑡
→
∞
𝐻
(
𝑓
(
𝑡
)
∣
𝐹
)
=
𝐻
(
𝐹
∗
∣
𝐹
)
+
𝛽
Δ
.
t→∞
lim
	​

H(f(t)∣F)=H(F
∗
	​

∣F)+βΔ.
	​


Thus the full target is equivalent to proving 
Δ
=
0
Δ=0.

The earlier static family shows why this cannot be inferred from the existing instantaneous bounds. It has fixed 
𝑀
,
𝑃
,
𝐸
M,P,E, a uniform particle–hole seed, uniform desaturation, 
𝐷
→
0
D→0, and strong 
𝐿
1
L
1
 convergence to a colder Fermi–Dirac distribution. It is not an actual nonthermalizing trajectory.

Optional defect-measure restriction

A compactification of the energy measures produces a nonnegative defect

𝜈
(
𝑑
𝑡
 
𝑑
𝑥
 
𝑑
𝜔
)
,
𝜔
∈
𝑆
2
,
ν(dtdxdω),ω∈S
2
,

with total mass 
Δ
Δ per time slice. Testing with

𝜑
(
𝑡
,
𝑥
)
∣
𝑣
∣
𝑎
(
𝑣
/
∣
𝑣
∣
)
𝜂
(
∣
𝑣
∣
/
𝑅
)
φ(t,x)∣v∣a(v/∣v∣)η(∣v∣/R)

and using the global 
𝐿
1
L
1
 flux bound gives

𝜔
⋅
∇
𝑥
𝜈
=
0.
ω⋅∇
x
	​

ν=0.

This is a genuine restriction, but it does not exclude the defect. For example,

𝜈
=
Δ
 
𝑑
𝑡
 
𝑑
𝑥
 
𝑑
𝜎
(
𝜔
)
ν=Δdtdxdσ(ω)

satisfies it. No usable time-evolution law eliminating this measure follows from the current order-one tests. The required weighted collision control remains absent.

I therefore support the cooler-equilibrium 
𝐿
1
L
1
 partial theorem, but not the full same-energy entropic thermalization claim.

No new source retrieval occurred during this audit. The root’s accidental broad-search exposure to the first-page introduction of the held Carlo Alberto original is preserved; there was no follow-up retrieval or theorem import.
