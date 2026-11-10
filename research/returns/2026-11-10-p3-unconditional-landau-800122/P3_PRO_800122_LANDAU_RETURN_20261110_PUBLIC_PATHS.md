# P3 completed return

Chat: https://chatgpt.com/c/6af2d882-ab10-83ec-8084-0f7bd9630455
Assistant final: 80012291-40fe-5b28-8a71-4e2a3df0cac2
Exact held prompt: work/astra-renewed-pro-programmes-20261103/P3_FULL_FINITE_MASS_LANDAU_WARM_CONTINUATION_PRO_20261110.txt
Model shown: Pro.

Native final complete as returned; expanded accessibility activity is limited by UI virtualization. No original ZIP visible.

## Native final as available

**I have not resolved the full global Cauchy problem.** I have neither a proof of global classical well-posedness for your entire class nor a genuine finite-mass obstruction. The additional estimates below therefore do **not** constitute an affirmative or negative answer.

There is a further unconditional estimate that can be proved from the actual finite-mass equation:
\[
\boxed{\int_0^T E_{7/8}(f(t))^{8/7}\,dt\le C_T.}
\]
Here \(C_T\) depends only on the fixed physical parameters and the initial particle numbers, energy, entropy and \(21\)-st velocity moment. The estimate does not assume bounded Fisher information or bounded \(E_{7/8}\) along the evolution. I also obtain unconditional polynomial moment bounds and a uniform bound for the large auxiliary-heat-time part of \(E_s\).

The remaining gap is substantive: this time-integrated bound does not provide the supremum bound required by the continuation argument in your prompt. I will give the proofs, specify the dependencies, and then explain precisely why the continuation step remains open in this work.

## 1. Setup and an unconditional weighted Fisher estimate

Let \([0,T_*)\) be the maximal classical interval supplied by the local theory. Everything below concerns the actual collision operator in the question, with the physical densities \(f_i\) and particle numbers \(n_i\) retained.

Write
\[
E_{\mathrm{kin}}
=\frac12\sum_i m_i\int |v|^2f_i^0(v)\,dv,
\qquad
H_0=\sum_i H(f_i^0),
\]
and define
\[
D(t)=\frac12\sum_{i,j}c_{ij}
\iint \frac{f_i(v)f_j(w)}{|v-w|}
\left|
P_{v-w}
\left(
\frac{\nabla\log f_i(v)}{m_i}
-\frac{\nabla\log f_j(w)}{m_j}
\right)
\right|^2\,dv\,dw.
\]
Thus the entropy inequality on the classical interval reads
\[
H(f(t))+\int_0^tD(r)\,dr\le H_0.
\]

For a fixed reference pair, take
\[
\overline M_i(v)
=n_i\left(\frac{m_i}{2\pi}\right)^{3/2}
e^{-m_i|v|^2/2},
\]
and put
\[
\mathscr H_0
=\sum_i\int f_i^0\log\frac{f_i^0}{\overline M_i}.
\]
Because the reference logarithms involve only species masses and total kinetic energy,
\[
\int_0^tD(r)\,dr\le \mathscr H_0
\qquad(t<T_*).
\tag{1}
\]
The reference pair need not have the initial momentum or temperature.

Define
\[
W_i(t)
=\int_{\mathbb R^3}\langle v\rangle^{-3}
|\nabla\sqrt{f_i(t,v)}|^2\,dv.
\]

The scalar Coulomb entropy-coercivity theorem gives
\[
W(h)\le C\bigl(1+D_0(h)\bigr),
\tag{2}
\]
where
\[
D_0(h)=\frac12\iint
\frac{h(v)h(w)}{|v-w|}
\left|P_{v-w}
\bigl(\nabla\log h(v)-\nabla\log h(w)\bigr)\right|^2\,dv\,dw.
\]
Its constant depends on mass, momentum, energy and an upper bound for absolute entropy. This is the precise weighted estimate in Desvillettes’ Theorem 1. :chatgpt-content-reference{index="0"}

### Making its constants uniform for each species

This application requires some care: individual species energies, momenta and entropies are not conserved.

Set
\[
B_i=\frac{2E_{\mathrm{kin}}}{m_i}.
\]
Then
\[
\int |v|^2f_i(t,v)\,dv\le B_i.
\]
Relative entropy against \(n_i\) times the standard Gaussian gives
\[
H(f_i(t))\ge
L_i:=n_i\log n_i-\frac{3n_i}{2}\log(2\pi)-\frac{B_i}{2}.
\]
Consequently,
\[
H(f_i(t))\le U_i:=H_0-L_j,\qquad j\ne i.
\tag{3}
\]

The elementary inequality
\[
x\log(1/x)\le |v|^2x+e^{-1-|v|^2}
\]
also gives
\[
\int f_i(t)|\log f_i(t)|
\le U_i+2B_i+2e^{-1}\pi^{3/2}.
\tag{4}
\]

To check that normalization in (2) cannot degenerate, let
\[
u_i(t)=\frac1{n_i}\int vf_i(t,v)\,dv,
\qquad
3n_i\sigma_i(t)^2
=\int |v-u_i(t)|^2f_i(t,v)\,dv.
\]
Then
\[
|u_i(t)|^2\le \frac{B_i}{n_i},
\qquad
\sigma_i(t)^2\le\frac{B_i}{3n_i}.
\]
The Gaussian entropy bound, together with (3), supplies the positive lower bound
\[
\sigma_i(t)^2\ge
\frac1{2\pi e}
\exp\!\left[
\frac23\left(\log n_i-\frac{U_i}{n_i}\right)
\right].
\tag{5}
\]
Thus translating and rescaling to unit mass, zero mean and normalized variance uses uniformly bounded, nondegenerate parameters. Equations (3)–(5) specify the data controlling the normalized absolute entropy as well.

It follows that
\[
W_i(t)\le C_i\bigl(1+D_0(f_i(t))\bigr),
\]
with fixed
\[
C_i=C_i(n_1,n_2,m_1,m_2,E_{\mathrm{kin}},H_0).
\]

The self-collision contribution to \(D\) is exactly
\[
\frac{c_{ii}}{m_i^2}D_0(f_i).
\]
Every other pair contribution is nonnegative. Therefore, with
\[
K_i=C_i\max\left\{1,\frac{m_i^2}{c_{ii}}\right\},
\]
we have
\[
\boxed{W_i(t)\le K_i(1+D(t)).}
\tag{6}
\]
In particular,
\[
\boxed{
\int_0^tW_i(r)\,dr
\le K_i(t+\mathscr H_0).
}
\tag{7}
\]

This uses only the strict positivity of \(c_{ii}\). It imposes no relation between self-collision and cross-collision strengths.

## 2. Unconditional propagation of polynomial moments

The weighted Fisher control gives a useful pointwise bound on the Coulomb potential.

Let
\[
U_j(v)=\int\frac{f_j(w)}{|v-w|}\,dw.
\]
Applying Sobolev to \(\langle v\rangle^{-3/2}\sqrt{f_j}\) yields
\[
\|f_j\langle\cdot\rangle^{-3}\|_{L^3}
\le C(W_j+n_j).
\tag{8}
\]

Put \(L=\langle v\rangle\). For \(0<R\le L/2\), the weights \(\langle w\rangle\) and \(L\) are comparable on \(|v-w|<R\). Hölder’s inequality, followed by the elementary far-field estimate, gives
\[
U_j(v)
\le C L^3R(W_j+n_j)+\frac{n_j}{R}.
\]
Optimizing \(R\), with the restriction \(R\le L/2\), gives
\[
U_j(v)
\le C L^{3/2}\sqrt{n_j(W_j+n_j)}.
\]
Using (6), define
\[
a_j=C\sqrt{n_j(K_j+n_j)}
\]
so that
\[
\boxed{
U_j(v)\le a_j\langle v\rangle^{3/2}\sqrt{1+D(t)}.
}
\tag{9}
\]

### The exact moment identity and its sign

For a common convex test function \(\phi\), integration by parts gives
\[
\begin{aligned}
\frac d{dt}\sum_i m_i\int f_i\phi
={}&
\sum_{i,j}\frac{c_{ij}}{m_i}
\iint f_i(v)f_j(w)\,
a(v-w):D^2\phi(v)\,dv\,dw\\
&+\frac12\sum_{i,j}c_{ij}
\left(\frac1{m_i}+\frac1{m_j}\right)
\iint f_i(v)f_j(w)\,
b(v-w)\cdot
[\nabla\phi(v)-\nabla\phi(w)]\,dv\,dw,
\end{aligned}
\tag{10}
\]
where
\[
b(z)=-\frac{2z}{|z|^3}.
\]
Convexity makes the second line nonpositive.

For
\[
M_q(t)=\sum_i m_i\int f_i(t,v)\langle v\rangle^q\,dv,
\qquad q\ge2,
\]
we have
\[
D^2\langle v\rangle^q
\le q(q-1)\langle v\rangle^{q-2}I.
\]
Since \(\operatorname{tr}a(z)=2/|z|\), (9)–(10) give
\[
M_q'(t)\le
\kappa_q\sqrt{1+D(t)}\,M_{q-1/2}(t),
\tag{11}
\]
where one may take
\[
\boxed{
\kappa_q
=2q(q-1)
\max_i\left\{
\frac1{m_i^2}\sum_jc_{ij}a_j
\right\}.
}
\tag{12}
\]

### Justifying propagation before assuming the moment is finite

For \(R>2\), define
\[
h_R(s)=
\begin{cases}
s^q,&s\le R,\\
qR^{q-1}s-(q-1)R^q,&s>R,
\end{cases}
\qquad
\phi_R(v)=h_R(\langle v\rangle).
\]
These functions are convex, increase to \(\langle v\rangle^q\), and grow only linearly at infinity. Their Hessians satisfy, almost everywhere,
\[
0\le D^2\phi_R(v)
\le C_q\phi_R(v)\langle v\rangle^{-2}I,
\tag{13}
\]
uniformly in \(R\). Smooth convex approximations preserve this bound up to a fixed factor.

The drift in (10) therefore retains its nonpositive sign for these truncated test functions. Equations (9) and (13) give a Gronwall estimate for the truncated moment with a constant independent of \(R\). Monotone convergence then establishes moment propagation. Thus using (11) afterwards is not circular.

For a sharper bound, suppose \(q>5/2\), and put
\[
\vartheta_q=\frac1{2(q-2)}.
\]
Interpolation against the conserved quantity
\[
M_2=\sum_i m_in_i+2E_{\mathrm{kin}}
\]
gives
\[
M_{q-1/2}\le M_2^{\vartheta_q}M_q^{1-\vartheta_q}.
\]
Integrating (11), using (1) and Cauchy–Schwarz in time, yields
\[
\boxed{
M_q(t)\le\mathscr R_q(t):=
\left[
M_q(0)^{\vartheta_q}
+\kappa_q\vartheta_qM_2^{\vartheta_q}
\sqrt{t(t+\mathscr H_0)}
\right]^{1/\vartheta_q}.
}
\tag{14}
\]

For the moment needed below, \(q=21\) and \(\vartheta_{21}=1/38\). The bound remains finite as \(t\) approaches any finite maximal endpoint.

## 3. A localization estimate for the actual heat–entropy functional

This step controls \(E_s\) itself, rather than merely a fractional Sobolev norm below it.

For one species, write
\[
E_s^{(m)}(h)
=s(1-s)\int_0^\infty
[H(h)-H(P_\tau^{m}h)]\,\tau^{-1-s}\,d\tau,
\qquad
P_\tau^m=e^{(\tau/m)\Delta}.
\]
De Bruijn’s identity and Tonelli’s theorem give
\[
E_s^{(m)}(h)
=\frac{1-s}{m}\int_0^\infty
\tau^{-s}I(P_\tau^m h)\,d\tau.
\tag{15}
\]
This formula also defines the functional for the nonnegative cutoff densities used below, with the usual convention \(0\log0=0\).

### Subadditivity

The pointwise Cauchy–Schwarz inequality implies
\[
I(h+k)\le I(h)+I(k).
\]
Hence (15) shows that \(E_s^{(m)}\) is convex, positively homogeneous, and subadditive.

For a countable decomposition \(h=\sum_kh_k\), apply the same pointwise inequality directly to
\[
P_\tau^mh=\sum_kP_\tau^mh_k
\]
and its gradient. At fixed positive \(\tau\), the Gaussian derivative convolutions converge absolutely because the total mass is finite. Tonelli then gives
\[
E_s^{(m)}(h)\le\sum_kE_s^{(m)}(h_k).
\tag{16}
\]
No interchange of an infinite series of signed entropy integrals is needed.

### Dyadic decomposition

Choose a smooth partition
\[
\sum_{k\ge0}\chi_k^2=1
\]
with finite overlap, annular radii \(R_k=2^k\), and
\[
\langle v\rangle\asymp R_k
\quad\text{on }A_k=\operatorname{supp}\chi_k,
\qquad
|\nabla\chi_k|\le C/R_k.
\]
Set
\[
h_k=\chi_k^2h,\qquad
N_k=\int_{A_k}h,\qquad
W_k=\int_{A_k}\langle v\rangle^{-3}|\nabla\sqrt h|^2.
\]
The product rule gives
\[
I(h_k)\le C\left(R_k^3W_k+R_k^{-2}N_k\right).
\tag{17}
\]

Apply the scalar heat–entropy bound from your premises:
\[
E_s^{(m)}(h_k)
\le \frac{(3/2)^{1-s}}s\,
m^{-s}\,n(h_k)^{1-s}I(h_k)^s.
\]
Because \(n(h_k)\le N_k\), equations (16)–(17) imply
\[
E_s^{(m)}(h)
\le C_sm^{-s}
\left[
\sum_kR_k^{3s}N_k^{1-s}W_k^s
+\sum_kR_k^{-2s}N_k
\right].
\tag{18}
\]

Choose
\[
q=\frac{3s}{1-s}.
\]
Discrete Hölder gives
\[
\sum_kR_k^{3s}N_k^{1-s}W_k^s
\le
\left(\sum_kR_k^qN_k\right)^{1-s}
\left(\sum_kW_k\right)^s.
\]
Finite overlap bounds these sums by the corresponding moment and weighted Fisher integral.

Writing
\[
N_q(h)=\int h(v)\langle v\rangle^q\,dv,
\qquad n=\int h,
\]
we obtain the static inequality
\[
\boxed{
E_s^{(m)}(h)
\le C_sm^{-s}
N_{3s/(1-s)}(h)^{1-s}\bigl(W(h)+n\bigr)^s.
}
\tag{19}
\]
It also holds when the unweighted Fisher information is infinite, provided the quantities on the right are finite.

### Specialization to \(s=7/8\)

Now \(q=21\), and (19) gives
\[
\left(E_{7/8}^{(m_i)}(f_i)\right)^{8/7}
\le C m_i^{-1}N_{21}(f_i)^{1/7}(W_i+n_i).
\]
Since
\[
(x+y)^{8/7}\le2^{1/7}(x^{8/7}+y^{8/7}),
\qquad
N_{21}(f_i)\le \frac{M_{21}}{m_i},
\]
we conclude
\[
E_{7/8}(f)^{8/7}
\le C M_{21}^{1/7}
\sum_i m_i^{-8/7}(W_i+n_i).
\]
Combining (7) and (14) proves the promised estimate:
\[
\boxed{
\int_0^T E_{7/8}(f(t))^{8/7}\,dt
\le
C\,\mathscr R_{21}(T)^{1/7}
\sum_i m_i^{-8/7}
\left[K_i(T+\mathscr H_0)+n_iT\right].
}
\tag{20}
\]

Every quantity on the right is determined by
\[
T,\quad m_i,\quad c_{ij},\quad n_i,\quad
E_{\mathrm{kin}},\quad H_0,\quad M_{21}(0).
\]
The constant \(C\) is universal once the fixed dyadic partition is chosen. The constants \(K_i,\kappa_q\) and \(\mathscr R_q\) were specified above.

## 4. Why this does not yet give continuation

Your established Sobolev estimate gives
\[
\|f_i(t)\|_{12/5}\le C m_i^{7/8}E_{7/8}(f(t)).
\]
Consequently, (20) implies
\[
f_i\in L_t^{8/7}L_v^{12/5}
\]
on every finite maximal classical interval.

The direct parabolic energy estimate needs a stronger time exponent. Indeed, for a test quantity \(u\),
\[
\begin{aligned}
\int f_ju^2
&\le \|f_j\|_{12/5}\|u\|_{24/7}^2\\
&\le C\|f_j\|_{12/5}
\|u\|_2^{3/4}\|\nabla u\|_2^{5/4}\\
&\le \varepsilon\|\nabla u\|_2^2
+C\varepsilon^{-5/3}
\|f_j\|_{12/5}^{8/3}\|u\|_2^2.
\end{aligned}
\tag{21}
\]
Thus this argument calls for time exponent \(8/3\), while (20) supplies \(8/7\).

The deficit is systematic. For general \(s\), (19) and fractional Sobolev give the mixed exponents
\[
r=\frac1s,\qquad q=\frac3{3-2s},
\]
which satisfy
\[
\frac2r+\frac3q=3.
\]
The reaction-energy calculation requires the stronger relation
\[
\frac2r+\frac3q=2.
\]
Changing \(s\) within this particular argument does not remove the gap.

A separate estimate such as
\[
\frac d{dt}E_{7/8}
\le A_T(1+E_{7/8})^{15/7}
\tag{22}
\]
with finite, data-controlled \(A_T\) would interact effectively with (20): finite-time blowup under (22) would force the \(8/7\)-th power to have a nonintegrable terminal lower bound. **I have not proved (22), an appropriate substitute, or a regularity theorem that upgrades (20) to continuation.**

In particular, finiteness of the time integral in (20) must not be substituted for the supremum bound in your continuation criterion.

## 5. Large auxiliary heat times are uniformly controlled

There is also a complete bound for the large-\(\tau\) portion of \(E_s\), using only entropy and energy.

Let
\[
N=n_1+n_2,
\qquad
d_i=\frac{2E_{\mathrm{kin}}}{3m_in_i}.
\]
The second moment of \(P_\tau^if_i\), divided by \(3n_i\), is at most
\[
d_i+\frac{2\tau}{m_i}.
\]
The Gaussian entropy lower bound therefore yields
\[
H(P_\tau^if_i)
\ge n_i\log n_i
-\frac{3n_i}{2}
\log\left[2\pi e\left(d_i+\frac{2\tau}{m_i}\right)\right].
\]

Fix \(R>0\), and define the data-dependent constant
\[
A_R=
H_0-\sum_i n_i\log n_i
+\frac32\sum_i n_i
\log\left[2\pi e\left(d_i+\frac{2R}{m_i}\right)\right].
\]
For \(\tau\ge R\),
\[
\sum_i[H(f_i)-H(P_\tau^if_i)]
\le A_R+\frac{3N}{2}\log(\tau/R).
\]
Integrating this bound against the exact auxiliary-time weight gives
\[
\boxed{
E_s^{\ge R}(f(t))
\le
(1-s)R^{-s}
\left(A_R+\frac{3N}{2s}\right).
}
\tag{23}
\]
Here
\[
E_s^{\ge R}
=s(1-s)\sum_i\int_R^\infty
[H(f_i)-H(P_\tau^if_i)]\,\tau^{-1-s}\,d\tau.
\]

Thus the large auxiliary-heat-time contribution cannot cause the missing supremum bound to fail. The unresolved part of this approach lies at small auxiliary heat scales.

## 6. A physical posterior sign calculation, and the cancellation it reveals

The generic covariance counterexample in your prompt can be strengthened to genuine physical product scores. However, the same example also shows why its pointwise sign cannot decide the integrated collision term.

Take any finite positive masses and particle numbers, and choose a common temperature \(\Theta>0\) with distinct drifts:
\[
f_\ell(v)
=n_\ell\left(\frac{m_\ell}{2\pi\Theta}\right)^{3/2}
\exp\left(-\frac{m_\ell|v-u_\ell|^2}{2\Theta}\right).
\]
These are admissible strictly positive Schwartz densities. Put
\[
d=u_i-u_j\ne0,\qquad
\beta=\frac d\Theta,\qquad
\mu=\frac{m_im_j}{m_i+m_j}.
\]
For the actual rotation scores,
\[
q_k(z)=L_k\log F=(e_k\times z)\cdot\beta.
\tag{24}
\]

Under the pair heat posterior at auxiliary time \(\tau>0\), the relative velocity \(Z\) has distribution
\[
Z\sim N(\zeta,\sigma^2I),
\]
where
\[
\sigma^2=\frac{2\tau\Theta}{\mu(\Theta+2\tau)},
\qquad
\zeta=
\frac{2\tau d+\Theta(y_v-y_w)}{\Theta+2\tau}.
\tag{25}
\]

Define
\[
U(\zeta)=\mathbb E|Z|^{-1}
=\frac{\operatorname{erf}(|\zeta|/(\sqrt2\sigma))}{|\zeta|}.
\]
Differentiating the Gaussian density gives the legitimate identity
\[
\operatorname{Cov}(Z,|Z|^{-3}Z)
=-\sigma^2D^2U(\zeta).
\]
This uses the integrable quantity \(Z/|Z|^3\); it does not introduce the divergent bare expectation of \(|Z|^{-3}\).

Using (24),
\[
\sum_k\operatorname{Cov}_{\mu_y}(q_k,\alpha q_k)
=
-\sigma^2\left(
|\beta|^2\Delta U-\beta^\top D^2U\,\beta
\right).
\tag{26}
\]
Choose \(\zeta\perp\beta\) and \(|\zeta|=4\sigma\). Then (26) equals
\[
-\frac{\sigma^2|\beta|^2}{|\zeta|^3}G(4),
\]
with
\[
G(x)=\operatorname{erf}(x/\sqrt2)
-\sqrt{\frac2\pi}e^{-x^2/2}(x^3+x).
\]
Mills’ bound gives
\[
G(4)>
1-\sqrt{\frac2\pi}e^{-8}\left(68+\frac14\right)>0.
\]
The last inequality needs no numerical evaluation: \(\sqrt{2/\pi}<1\) and
\[
e^8>\frac{8^4}{4!}=\frac{512}{3}>68+\frac14
\]
suffice.

Therefore the summed posterior covariance is negative on an open set of actual observations \(y\).

### Nevertheless, the integrated \(B_\tau\) is positive for these same data

The heat-smoothed score is
\[
q_{\tau,k}(Y)
=L_k\log(P_\tau F)
=(e_k\times Y)\cdot\frac d{\Theta+2\tau}.
\]
It is linear in \(Y\). Heat preserves linear functions, so
\[
\begin{aligned}
\int
\frac{P_\tau(\alpha Fq_k)P_\tau(Fq_k)}
{P_\tau F}
&=\int P_\tau(\alpha Fq_k)\,q_{\tau,k}\\
&=\int\alpha Fq_k\,P_\tau q_{\tau,k}\\
&=\frac{\Theta}{\Theta+2\tau}
\int\alpha Fq_k^2.
\end{aligned}
\]
Consequently,
\[
\boxed{
B_{\tau,k}
=\frac{2\tau}{\Theta+2\tau}
\int\alpha Fq_k^2\ge0.
}
\tag{27}
\]

These are instantaneous identities at the prescribed densities. No assumption is made that the nonlinear Landau evolution preserves a Gaussian family.

The calculation establishes two precise facts: physical posterior covariance positivity is false, even after summing the rotation fields; integration over posterior centers can restore the favorable sign. It supplies no counterexample to integrated \(E_s\) dissipation or to global regularity.

## 7. What the additional literature does and does not supply

The verified finite-mass results of Junné–Winter–Yoldaş do not cover arbitrary Coulomb cross interactions. Their compensated Coulomb theorem concerns the infinite-ion regime and retains its additional condition. Those results therefore cannot complete the missing step here. :chatgpt-content-reference{index="1"}

I also checked Merz–Zacher’s 2026 work on nonlocal Fisher information. It proves a lifting theorem for a different functional, using a tensor-sum auxiliary generator. That theorem does not establish the required finite-mass Coulomb collision inequality for \(E_{7/8}\). Its fractional Fisher finiteness theorem also has explicit tail hypotheses beyond arbitrary positive Schwartz data. :chatgpt-content-reference{index="2"}

All bounds and sign calculations reported above are analytic. The moment truncations have constants uniform in the truncation radius and are removed by convergence; the dyadic decomposition is handled by nonnegative integral inequalities. No numerical approximation or finite-dimensional positivity check is used to establish a claimed continuation bound.

**The full endpoint remains unproved in this response.** Equations (14), (20) and (23) give additional unconditional control, with the physical masses and coefficients retained. What is still missing is control strong enough to exclude finite-time concentration of the continuation norm—through a collision estimate for small auxiliary heat scales or through another argument. Without that step, I cannot claim the requested global existence and uniqueness theorem, and none of the calculations above is a genuine obstruction to it.

## Expanded visible accessibility activity and page material

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
								29 container (showing 0-500 of 636 items)
									30 splitter Today 6:40 PM
									31 heading You said:, Value: 4
										32 text You said:
									33 container
										34 text Global regularity for the finite-mass two-species Landau-Coulomb system  FULL QUESTION. Resolve global classical well-posedness of the spatially HOMOGENEOUS two-species Landau-Coulomb equation on velocity space R^3, for arbitrary positive finite particle masses and arbitrary smooth nonequilibrium data, as follows.  Fix ANY m_1,m_2>0 and positive symmetric coefficients c_ij=c_ji>0, i,j in {1,2}. Define P_z=I-z tensor z/|z|^2 and  Q_ij(f_i,f_j)(v)  = (c_ij/m_i) div_v integral _ (R3)  [P\_(v-w)/|v-w|]      \*[(f_j(w)/m_i) grad_v f_i(v)        -(f_i(v)/m_j) grad_w f_j(w)] dw. The equation is partial_t f_i=sum\_(j=1,2) Q_ij(f_i,f_j).  For EVERY pair of strictly positive Schwartz initial densities f_i^0 on R^3, with nonzero finite masses n_i=integral f_i^0 and finite mass-weighted Fisher information  I_m(f^0)=sum_i (1/m_i) integral |grad f_i^0|^2/f_i^0, does this Cauchy problem have a unique global nonnegative classical solution, smooth for positive times and attaining f_i^0 at t=0 in the usual finite-mass/energy strong-solution class?  The result must include finite-time a priori bounds sufficient for classical continuation for every finite T, with their dependence on the finite masses, coefficients and actual initial norms specified. In particular, a Fisher-information or other continuation bound must be proved rather than assumed. Retain each species mass, total momentum sum_i m_i integral v f_i, total kinetic energy (1/2)sum_i m_i integral |v|^2 f_i and the entropy inequality. No near-Maxwellian smallness, radial/even symmetry, infinite-mass species, frozen background, special mass ratio, artificial velocity cutoff or modified collision operator is part of the question.  A full affirmative must prove the stated global existence and uniqueness for the whole class. A negative must exhibit a genuine obstruction to that contract for admissible FINITE masses and data; growth of one proposed Lyapunov functional, failure of a particular estimate or an infinite-mass limiting example is not such an obstruction. This is an analytic mathematical question, not a requested numerical simulation. Any computation or approximation used must have its actual hypotheses, errors and costs accounted for; no solution, optimization or real-number oracle is supplied.  The suggested papers and supplied premises are starting points, not a limit on your research. You may read them, seek additional papers, literature, available Astra work or other sources, change mathematical representations, introduce different ideas and methods, and challenge my framing while pursuing the full question. You choose your sources and approach without further permission.  Useful starting mathematics and contrary results, not a prescribed method:  1. Single-species Fisher monotonicity does not automatically extend to Coulomb mixtures. For the mass-weighted I_m, the known general cross-species spherical criterion in dimension3 reaches |gamma_ij|<=sqrt(8), whereas Coulomb has gamma=-3. Diagonal same-species terms retain particle-exchange symmetry; cross terms generally do not. The exact lifted derivative separates a negative squared derivative of the angular collision field from a positive radial-coefficient term. The absence of a sign from that criterion is not a global blowup theorem.  2. There is an actual compensation mechanism in a distinct limiting problem. For one species interacting with a frozen infinite-mass ion background, the equation contains the spherical diffusion c_ei div(|v|^-1 P_v grad f). Write  J(f)=integral |v|^-1 |P_v grad log f|^2 f. An existing theorem constructs a nonnegative Lyapunov functional I(f)+a J(f)+R H(f|M) and obtains global regularity. In the Coulomb case its theorem includes the additional data/coupling condition  2+J(f^0)/I(f^0)^(3/2)+H(f^0|M)<=c_ei/K for a specified sufficiently large constant K. This is not an arbitrary-finite-mass or arbitrary-coupling result, and that extra condition is not imposed on the full question here.  3. The finite-mass pair geometry is explicit. For a pair (v,w), put z=v-w, Z=(m_i v+m_j w)/(m_i+m_j), mu_ij=m_i m_j/(m_i+m_j), and F_ij=f_i(v)f_j(w). At fixed Z the relative derivative is  D_z=mu_ij(grad_v/m_i-grad_w/m_j). The pair angular quantity  J_ij=integral\_(R6) F_ij |z|^-1 |P_z D_z log F_ij|^2 dv dw satisfies the exact entropy-dissipation identity  -partial_t sum_i integral f_i log f_i    =(1/2)sum\_(i,j) c_ij mu_ij^-2 J_ij. This identifies a finite-recoil counterpart of the limiting angular quantity. It does not supply a sign for its derivative: both marginals evolve, and differentiating introduces mixed collision terms. A compensation built from these quantities, a different representation or another mechanism is open.  4. Do not assume entropy dissipation is itself monotone. Even for the single-species Landau-Coulomb equation there are smooth near-Maxwellian examples where its time derivative is positive. Thus adding entropy dissipation to Fisher information needs a genuine estimate; thermodynamic entropy decrease alone does not provide it.  Optional primary starting points, in any order:  \* Zhu, [https://arxiv.org/html/2512.17905v1](https://arxiv.org/html/2512.17905v1), Theorem1.1 and Proposition2.2: mass-weighted mixture Fisher information, exact lifted derivative and the different diagonal/cross-species thresholds.  \* Junne, Winter and Yoldas, [https://arxiv.org/html/2512.17082v1](https://arxiv.org/html/2512.17082v1), Theorems1.1-1.3 and Sections2-3: finite-mass local theory, the contrary Fisher example, and the compensated infinite-ion theorem with its Coulomb condition retained.  \* Junne, Winter and Yoldas, [https://arxiv.org/html/2609.03847v1](https://arxiv.org/html/2609.03847v1), Theorem1.1: entropy dissipation can increase even near equilibrium. This concerns a Lyapunov shortcut, not failure of classical solutions.  The full endpoint is the finite-mass global Cauchy theory above. The choice of functional, representation, sources and proof strategy is yours.  you may use all subagents avaible
									35 button (expanded) Show less, Secondary Actions: Collapse
										36 text Show less
										37 image
									38 button Copy message
										39 image
									40 button Share prompt
									41 button Edit message
										42 image
									43 button (expanded) Worked for 21m 24s, Secondary Actions: Collapse
										44 text Worked for 21m 24s
										45 image
									46 text I’ll check the current results and work on several possible routes to the finite-mass problem in parallel. I’ll keep the full continuation requirement in view: a conditional estimate or a failed Lyapunov argument would not settle your question.
									47 text Searching arxiv.org
									48 container Subagent activity
										49 container
											50 button Fisher compensation
											51 text , 
											52 button Alternative continuation
											53 text  and 
											54 button Literature frontier
											55 text  started working
									56 text Searching arxiv.org
									57 text The finite-mass result I’ve read so far covers cross interactions only down to 
									58 container
										59 text 𝛾 = −
										60 text 8
									61 text , leaving Coulomb at 
									62 container
										63 text 𝛾 = − 3
									64 text  outside its theorem. I’m now testing whether finite recoil and the positive same-species collisions can close that gap. I’m also using the runtime skill for any symbolic checks needed in the derivations.
									65 container
										66 button (collapsed) Searched the web, Secondary Actions: Expand
										67 text Searched the web
									68 text Explored finite-mass symmetry
									69 text Searched 10 websites
									70 text Checked mass normalization and finite-mass scaling
									71 text Tested Fisher-growth and entropy-dissipation controls
									72 text The newer sources I’ve found still leave the arbitrary finite-mass Coulomb case open. One route I’m investigating is weaker than Fisher monotonicity: if Fisher growth can be bounded by entropy dissipation times Fisher information, the entropy inequality would give a finite-time bound. The question is whether that estimate survives the singular cross-collision terms.
									73 container Subagent activity
										74 container
											75 button Fisher compensation
											76 text  and 
											77 button Alternative continuation
											78 text  updated
									79 text Searching arxiv.org
									80 text Derived the direct first variation and tested spike-scale control Tested spike scaling and entropy coercivity
									81 container Subagent activity
										82 container
											83 button Fisher compensation
											84 text  updated
									85 text Explored weighted Fisher powers and tested finite-species entropy-dissipation obstructions Analyzed label symmetrization and tested scalar envelope
									86 container Subagent activity
										87 container
											88 button Alternative continuation
											89 text  and 
											90 button Fisher compensation
											91 text  updated
									92 text Searching arxiv.org
									93 text Derived symbolic derivative and weighted Lp law Tested reaction interpolation and pairwise Lp control Checked derivative weights, Renyi contractivity, and collision mixing Investigated fractional Fisher monotonicity
									94 container Subagent activity
										95 container
											96 button Alternative continuation
											97 text  updated
									98 text Derived the mass-Fisher functional and assessed interaction bounds and velocity scaling Assessed Lp control and balanced weighted exponents The entropy-based growth estimate has a serious scaling problem: small, concentrated components can make the prospective Fisher-growth term too large relative to the proposed bound. I’m also checking a cancellation at zero relative velocity in the Coulomb formulas; separating the positive and negative terms there can lose information. Neither issue establishes blowup.
									99 text Searched 30 websites
									100 text Tested shifted Fisher bounds and balanced entropy scaling
									101 text Assessed entropy control
									102 container
										103 button (collapsed) Searched the web, Secondary Actions: Expand
										104 text Searched the web
									105 text Derived moment and weighted moment bounds
									106 text Derived the M_q and q14 estimates
									107 text Computed the potential constant and derived weighted L² bounds
									108 container Subagent activity
										109 container
											110 button Literature frontier
											111 text  updated
									112 text Checked Fisher-integral bounds
									113 container Subagent activity
										114 container
											115 button Fisher compensation
											116 text  finished
									117 text Constructed annular perturbation and derived finite-mass counterexample
									118 text Tuned the positive seed and checked the Gaussian limit
									119 text Verified Aσ convergence
									120 container Subagent activity
										121 container
											122 button Fisher compensation
											123 text , 
											124 button Alternative continuation
											125 text  and 
											126 button Literature frontier
											127 text  updated
									128 text Analyzing T_t contraction
									129 text Derived kernel energy identity and checked anticommutator positivity
									130 text Checked the Hardy borderline and derived the weighted Hessian
									131 text Tested thin-shell behavior, shell-rate coupling, and 2x2 conditions
									132 text Estimated and checked stability threshold, leaving result unresolved
									133 text Constructed angular seed and checked angular derivative
									134 text Checked Fisher derivative signs and mixture scaling
									135 text I’ve closed a useful conditional step: a finite bound on the mass-weighted Fisher information would control the weighted 
									136 container
										137 text 𝐿 2
									138 text  norms needed to restart the local solution. The constants can be written in terms of the masses, collision coefficients, particle numbers and initial moments. The Fisher bound itself is still missing. I’m making one final pass on a weaker regularity functional that might avoid the failed monotonicity argument.
									139 container Subagent activity
										140 container
											141 button Alternative continuation
											142 text  updated
									143 text Explored posterior variance bounds and tested radial profile counterexamples Checked for missing estimates
									144 container
										145 button (collapsed) Used GitHub integration, searched the web, Secondary Actions: Expand
										146 text Used GitHub integration , searched the web
									147 text Verified entropy balance and Fisher derivative
									148 text Checked the coefficient
									149 container Subagent activity
										150 container
											151 button Fisher compensation
											152 text  updated
									153 text Prepared total-expansion notation and defined the remainder estimate
									154 text Formulated the blowup criterion
									155 container Subagent activity
										156 container
											157 button Alternative continuation
											158 text  updated
									159 text Checked Fermi mappings, lifted models, and radial spectral gaps
									160 text Formulated correlated Fisher pending full-text access
									161 text Checked the seed formula and verified the Hessian expansion
									162 text Derived and checked the entropy-gap bound
									163 text Refined selection of exponents greater than three-fourths
									164 text Checked tensorization normalization
									165 container Subagent activity
										166 container
											167 button Alternative continuation
											168 text  and 
											169 button Fisher compensation
											170 text  finished
									171 text Checked weighted L² adaptation
									172 text Refined the truncation argument and assembled the I_m' formula
									173 text Verified compensation formulas and checked J variation
									174 text Derived the dissipation formula
									175 text Checked Coulomb cutoff settings
									176 text Verified normalized coefficients
									177 heading ChatGPT said:, Value: 4
										178 text ChatGPT said:
									179 heading Status: the full global Cauchy problem is unresolved here, Value: 1
										180 text Status: the full global Cauchy problem is unresolved here
									181 text I have not proved the requested global classical well-posedness theorem, and I have not constructed an admissible finite-mass solution that violates it.
									182 text  The finite-time continuation bound required by your question remains missing. The primary literature I checked still leaves the general finite-mass Coulomb case outside its global theorem. Junné–Winter–Yoldaş explicitly identify the finite-mass-ratio problem below 
									183 container
										184 text 𝛾 = −
										185 text 8
									186 text  as open. Their compensated Coulomb theorem concerns the infinite-ion model and retains the additional data/coupling condition you stated. 
									187 link (collapsed) Value: arxiv.org/html/2512.17082v1?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: On the existence of solutions to the multi-species Landau equation, https://arxiv.org/html/2512.17082v1?utm_source=chatgpt.com
									188 text The work below gives three concrete results:
									189 content list
										190 container
											191 AXListMarker 1. 
											192 text An explicit conditional continuation estimate , with the mass and coefficient dependence retained.
										193 container
											194 AXListMarker 2. 
											195 text A construction showing that mass-weighted Fisher information can initially increase for strictly finite masses and strictly positive Schwartz data.  This concerns the functional, and is not a negative answer to global regularity.
										196 container
											197 AXListMarker 3. 
											198 text An alternative heat–entropy functional  with finite initial value, tensorization and useful fractional Sobolev control. I derive its remaining collision inequality, but do not prove that inequality.
									199 text I will distinguish these established calculations from the unresolved step throughout.
									200 heading 1. What the checked sources establish, Value: 2
										201 text 1. What the checked sources establish
									202 table
										203 row
											204 cell
												205 text Source
											206 cell
												207 text Applicable result
											208 cell
												209 text Limitation for your question
										210 row
											211 cell
												212 text Zhu, 
												213 text Fisher information for the multi-species Landau system
											214 cell
												215 text Mass-weighted Fisher monotonicity under different diagonal and cross-species conditions
											216 cell
												217 text In dimension three, the cross-species condition is  (
										218 row
											219 cell
												220 text Junné–Winter–Yoldaş, 
												221 text On the existence of solutions to the multi-species Landau equation
											222 cell
												223 text Finite-mass local strong theory; global theory in its stated softer-potential range; compensated infinite-ion theorem
											224 cell
												225 text No arbitrary-data, arbitrary-finite-mass Coulomb continuation estimate
										226 row
											227 cell
												228 text Junné–Winter–Yoldaş, September 2026 entropy-dissipation paper
											229 cell
												230 text Entropy dissipation can increase, including for perturbations close to equilibrium
											231 cell
												232 text Entropy decrease does not justify assuming that its dissipation decreases
										233 row
											234 cell
												235 text Duong–He, 
												236 text Multi-species kinetic models: GENERIC formulation and Fisher information
											237 cell
												238 text Thermodynamic formulations and Fisher results under collision-kernel assumptions
											239 cell
												240 text Does not supply the missing finite-mass Coulomb theorem
									241 container
										242 button Copy table
										243 pop up button (collapsed) Description: Expand table, Secondary Actions: Expand
									244 text These distinctions are supported by the theorem statements and the newer paper’s abstract. 
									245 link (collapsed) Value: arxiv.org/html/2512.17905v1?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: Fisher information for the multi-species Landau system, https://arxiv.org/html/2512.17905v1?utm_source=chatgpt.com, 3 additional sources
									246 text  A September 2026 author seminar also describes the recovered global result in the infinite-ion regime. 
									247 link (collapsed) Secondary Actions: Expand, Description: tudelft.nl: [AN] Jonathan Junné: Fisher information and well-posedness for multi-species Landau equation, https://www.tudelft.nl/evenementen/2026/ewi/diam/seminar-in-analysis-and-applications/an-jonathan-junne-fisher-information-and-well-posedness-for-multi-species-landau-equation?utm_source=chatgpt.com, Value: tudelft.nl/evenementen/2026/ewi/diam/seminar-in-analysis-and-applications/an-jonathan-junne-fisher-information-and-well-posedness-for-multi-species-landau-equation?utm_source=chatgpt.com
									248 text The relevant Astra records checked do not supply this missing estimate either. 
									249 link Description: N757, Value: github.com/harjassand/astra-research-knowledge/blob/main/cards/N757-conserving-finite-memory-coulomb-and-weighted-pair-acquisition.txt
									250 text  concerns a collision-generator construction with a retained ultraviolet cutoff and supplied regularity. 
									251 link Description: N1763, Value: github.com/harjassand/astra-research-knowledge/blob/main/knowledge/current/packets/N1763.json
									252 text  concerns the different Landau–Fermi–Dirac equation within an already-supplied global classical solution class.
									253 heading 2. Conservation and entropy for your exact normalization, Value: 2
										254 text 2. Conservation and entropy for your exact normalization
									255 text Write
									256 container
										257 text 𝑎 ( 𝑧 ) =
										258 container
											259 text 𝑃 𝑧
										260 container
											261 text ∣ 𝑧 ∣
										262 text , 𝐴 [ 𝑔 ] = 𝑎 ∗ 𝑔 , 𝑏 ( 𝑧 ) = div ⁡ 𝑎 ( 𝑧 ) = −
										263 container
											264 text 2 𝑧
										265 container
											266 text ∣ 𝑧
											267 text ∣
											268 text 3
										269 text .
									270 text Distributionally,
									271 container
										272 text div ⁡ 𝑏 = − 8 𝜋
										273 text 𝛿
										274 text 0
										275 text .
									276 text Your equation therefore has the divergence form
									277 container
										278 container
											279 text ∂
											280 text 𝑡
											281 text 𝑓
											282 text 𝑖
											283 text =
											284 text ∑
											285 text 𝑗
											286 text [
											287 container
												288 text 𝑐
												289 container
													290 text 𝑖 𝑗
												291 text 𝑚
												292 text 𝑖
												293 text 2
											294 text div
											295 text ⁡
											296 text (
											297 text 𝐴
											298 text [
											299 container
												300 text 𝑓 𝑗
											301 text ]
											302 text ∇
											303 container
												304 text 𝑓 𝑖
											305 text )
											306 text −
											307 container
												308 text 𝑐
												309 container
													310 text 𝑖 𝑗
												311 container
													312 text 𝑚 𝑖
												313 container
													314 text 𝑚 𝑗
											315 text div
											316 text ⁡
											317 text (
											318 container
												319 text 𝑓 𝑖
											320 text (
											321 text 𝑏
											322 text ∗
											323 container
												324 text 𝑓 𝑗
											325 text )
											326 text )
											327 text ]
											328 text .
										329 text (2.1)
									330 text Let
									331 container
										332 text 𝑑
										333 container
											334 text 𝑖 𝑗
										335 text ( 𝑣 , 𝑤 ) =
										336 container
											337 text ∇ log ⁡
											338 text 𝑓
											339 text 𝑖
											340 text ( 𝑣 )
										341 container
											342 text 𝑚 𝑖
										343 text −
										344 container
											345 text ∇ log ⁡
											346 text 𝑓
											347 text 𝑗
											348 text ( 𝑤 )
										349 container
											350 text 𝑚 𝑗
										351 text ,
										352 text 𝐹
										353 container
											354 text 𝑖 𝑗
										355 text =
										356 text 𝑓
										357 text 𝑖
										358 text ( 𝑣 )
										359 text 𝑓
										360 text 𝑗
										361 text ( 𝑤 ) .
									362 text On a classical interval, symmetrization gives
									363 container
										364 container
											365 text 𝑑
											366 container
												367 text 𝑑 𝑡
											368 text ∑
											369 text 𝑖
											370 text ∫
											371 text 𝜑
											372 text 𝑖
											373 text 𝑓
											374 text 𝑖
											375 text = −
											376 text 1
											377 text 2
											378 text ∑
											379 container
												380 text 𝑖 , 𝑗
											381 text 𝑐
											382 container
												383 text 𝑖 𝑗
											384 text ∬
											385 text 𝐹
											386 container
												387 text 𝑖 𝑗
											388 text 𝑎 ( 𝑣 − 𝑤 )
											389 text 𝑑
											390 container
												391 text 𝑖 𝑗
											392 text ⋅
											393 text (
											394 container
												395 text ∇
												396 container
													397 text 𝜑 𝑖
												398 text (
												399 text 𝑣
												400 text )
												401 text 𝑚
												402 text 𝑖
											403 text −
											404 container
												405 text ∇
												406 container
													407 text 𝜑 𝑗
												408 text (
												409 text 𝑤
												410 text )
												411 text 𝑚
												412 text 𝑗
											413 text )
											414 text 𝑑 𝑣 𝑑 𝑤 .
										415 text (2.2)
									416 text This directly yields the requested conserved quantities:
									417 content list
										418 container
											419 AXListMarker • 
											420 text Constant test functions give conservation of each 
											421 container
												422 text 𝑛 𝑖
											423 text .
										424 container
											425 AXListMarker • 
											426 text Taking 
											427 container
												428 text 𝜑
												429 text 𝑖
												430 text ( 𝑣 ) =
												431 text 𝑚
												432 text 𝑖
												433 text 𝑣
												434 text ℓ
											435 text  gives conservation of total momentum.
										436 container
											437 AXListMarker • 
											438 text Taking 
											439 container
												440 text 𝜑
												441 text 𝑖
												442 text ( 𝑣 ) =
												443 text 𝑚
												444 text 𝑖
												445 text ∣ 𝑣
												446 text ∣
												447 text 2
												448 text / 2
											449 text  gives conservation of total kinetic energy, because 
											450 container
												451 text 𝑎 ( 𝑧 ) 𝑧 = 0
											452 text .
									453 text Testing the entropy gives
									454 container
										455 container
											456 text −
											457 text 𝑑
											458 container
												459 text 𝑑 𝑡
											460 text ∑
											461 text 𝑖
											462 text ∫
											463 text 𝑓
											464 text 𝑖
											465 text log ⁡
											466 text 𝑓
											467 text 𝑖
											468 text =
											469 text 1
											470 text 2
											471 text ∑
											472 container
												473 text 𝑖 , 𝑗
											474 text 𝑐
											475 container
												476 text 𝑖 𝑗
											477 text ∬
											478 container
												479 text 𝐹
												480 text 𝑖
												481 text 𝑗
											482 container
												483 text ∣ 𝑣 − 𝑤 ∣
											484 text ∣
											485 text 𝑃
											486 container
												487 text 𝑣 − 𝑤
											488 text 𝑑
											489 container
												490 text 𝑖 𝑗
											491 text ∣
											492 text 2
											493 text 𝑑 𝑣 𝑑 𝑤 .
										494 text (2.3)
									495 text Since 
									496 container
										497 text 𝐷
										498 text 𝑧
										499 text =
										500 text 𝜇
										501 container
											502 text 𝑖 𝑗
										503 text (
										504 text ∇
										505 text 𝑣
										506 text /
										507 text 𝑚
										508 text 𝑖
										509 text −
										510 text ∇
										511 text 𝑤
										512 text /
										513 text 𝑚
										514 text 𝑗
										515 text )
									516 text , this is exactly
									517 container
										518 container
											519 text 𝐷
											520 text 𝐻
											521 text ( 𝑓 ) =
											522 text 1
											523 text 2
											524 text ∑
											525 container
												526 text 𝑖 , 𝑗
											527 text 𝑐
											528 container
												529 text 𝑖 𝑗
											530 text 𝜇
											531 container
												532 text 𝑖 𝑗
											533 container
												534 text − 2
											535 text 𝐽
											536 container
												537 text 𝑖 𝑗
											538 text .
										539 text (2.4)
									540 text These identities retain the actual particle numbers; no unit-mass normalization is implicit. For a useful nonnegative entropy, set
									541 container
										542 text 𝜌 =
										543 text ∑
										544 text 𝑖
										545 text 𝑚
										546 text 𝑖
										547 text 𝑛
										548 text 𝑖
										549 text , 𝑢 =
										550 text 𝑃
										551 text 𝜌
										552 text , Θ =
										553 container
											554 text 2 𝐸 − ∣ 𝑃
											555 text ∣
											556 text 2
											557 text / 𝜌
										558 container
											559 text 3 (
											560 text 𝑛
											561 text 1
											562 text +
											563 text 𝑛
											564 text 2
											565 text )
										566 text .
									567 text The assumptions imply 
									568 container
										569 text Θ > 0
									570 text . Define
									571 container
										572 text 𝑀
										573 text 𝑖
										574 text ( 𝑣 ) =
										575 text 𝑛
										576 text 𝑖
										577 container
											578 text (
											579 container
												580 text 𝑚 𝑖
											581 container
												582 text 2 𝜋 Θ
											583 text )
										584 container
											585 text 3 / 2
										586 text exp ⁡  ⁣
										587 text (
										588 text −
										589 container
											590 container
												591 text 𝑚 𝑖
											592 text ∣
											593 text 𝑣
											594 text −
											595 text 𝑢
											596 container
												597 text ∣ 2
											598 text 2
											599 text Θ
										600 text )
										601 text .
									602 text Then
									603 container
										604 text 𝐻 ( 𝑓 ∣ 𝑀 ) =
										605 text ∑
										606 text 𝑖
										607 text ∫
										608 text 𝑓
										609 text 𝑖
										610 text log ⁡
										611 container
											612 text 𝑓 𝑖
										613 container
											614 text 𝑀 𝑖
										615 text ≥ 0 ,
									616 text and, on the classical interval,
									617 container
										618 container
											619 text 𝐻 ( 𝑓 ( 𝑡 ) ∣ 𝑀 ) +
											620 text ∫
											621 text 0
											622 text 𝑡
											623 text 𝐷
											624 text 𝐻
											625 text ( 𝑓 ( 𝑠 ) ) 𝑑 𝑠 = 𝐻 (
											626 text 𝑓
											627 text 0
											628 text ∣ 𝑀 ) .
										629 text (2.5)
									630 text Thus entropy supplies a finite time integral of 
									631 container
										632 text 𝐷 𝐻
									633 text . It does not yet supply a supremum bound for Fisher information or another continuation norm.
									634 heading 3. An explicit Fisher-to-continuation estimate, Value: 2
										635 text 3. An explicit Fisher-to-continuation estimate
									636 text Here is a closed conditional implication. Its hypothesis is precisely identified so that it cannot be mistaken for the missing global estimate. Let 
									637 container
										638 text 𝑇 ∗
									639 text  be the maximal time of the local strong solution. Suppose, for some finite 
									640 container
										641 text 𝑇 ≤
										642 text 𝑇
										643 text ∗
									644 text ,
									645 container
										646 container
											647 text 𝑆
											648 text 𝑇
											649 text : =
											650 container
												651 text sup ⁡
											652 container
												653 text 0 ≤ 𝑡 < 𝑇
											654 text 𝐼
											655 text 𝑚
											656 text ( 𝑓 ( 𝑡 ) ) < ∞ .
										657 text (3.1)
									658 text Define
									659 container
										660 text 𝑀
										661 text 𝑞
										662 text ( 𝑡 ) =
										663 text ∑
										664 container
											665 text 𝑖 = 1
										666 text 2
										667 text 𝑚
										668 text 𝑖
										669 text ∫
										670 text 𝑓
										671 text 𝑖
										672 text ( 𝑡 , 𝑣 ) ⟨ 𝑣
										673 text ⟩
										674 text 𝑞
										675 text 𝑑 𝑣 , ⟨ 𝑣 ⟩ = ( 1 + ∣ 𝑣
										676 text ∣
										677 text 2
										678 text )
										679 container
											680 text 1 / 2
										681 text .
									682 text I will derive a bound for
									683 container
										684 text 𝑌
										685 text 7
										686 text ( 𝑡 ) =
										687 text ∑
										688 text 𝑖
										689 text ∫
										690 text 𝑓
										691 text 𝑖
										692 text ( 𝑡 , 𝑣
										693 text )
										694 text 2
										695 text ⟨ 𝑣
										696 text ⟩
										697 text 7
										698 text 𝑑 𝑣 ,
									699 text which is a weighted 
									700 container
										701 text 𝐿 2
									702 text  quantity of the type used by the local strong theory.
									703 heading 3.1 Fisher information controls , Value: 3
										704 text 3.1 Fisher information controls 
										705 container
											706 text 𝐿 3
									707 text Let 
									708 container
										709 text 𝐶 𝑆
									710 text  satisfy
									711 container
										712 text ∥ ℎ
										713 text ∥
										714 container
											715 text 𝐿 6
										716 text 2
										717 text ≤
										718 text 𝐶
										719 text 𝑆
										720 text ∥ ∇ ℎ
										721 text ∥
										722 container
											723 text 𝐿 2
										724 text 2
										725 text .
									726 text Since
									727 container
										728 text 𝐼 ( 𝑓 ) = 4 ∥ ∇
										729 text 𝑓
										730 text ∥
										731 text 2
										732 text 2
										733 text ,
									734 text we have
									735 container
										736 container
											737 text ∥
											738 text 𝑓
											739 text 𝑖
											740 text ∥
											741 text 3
											742 text = ∥
											743 container
												744 text 𝑓 𝑖
											745 text ∥
											746 text 6
											747 text 2
											748 text ≤
											749 container
												750 text 𝐶 𝑆
											751 text 4
											752 text 𝐼 (
											753 text 𝑓
											754 text 𝑖
											755 text ) ≤
											756 container
												757 text 𝐶 𝑆
											758 text 4
											759 text 𝑚
											760 text 𝑖
											761 text 𝑆
											762 text 𝑇
											763 text .
										764 text (3.2)
									765 heading 3.2 An explicit Coulomb-potential bound, Value: 3
										766 text 3.2 An explicit Coulomb-potential bound
									767 text For any 
									768 container
										769 text 𝑅 > 0
									770 text , Hölder’s inequality gives
									771 container
										772 container
											773 text ∫
											774 container
												775 text 𝑓 ( 𝑤 )
											776 container
												777 text ∣ 𝑣 − 𝑤 ∣
											778 text 𝑑 𝑤
										779 container
											780 text ≤ ∥ 𝑓
											781 text ∥
											782 text 3
											783 container
												784 text (
												785 text ∫
												786 container
													787 text ∣ 𝑧 ∣ < 𝑅
												788 text ∣ 𝑧
												789 text ∣
												790 container
													791 text − 3 / 2
												792 text 𝑑 𝑧 )
											793 container
												794 text 2 / 3
											795 text +
											796 text 𝑛
											797 text 𝑅
										798 container
											799 text =
											800 container
												801 text (
												802 container
													803 text 8 𝜋
												804 text 3
												805 text )
											806 container
												807 text 2 / 3
											808 text 𝑅 ∥ 𝑓
											809 text ∥
											810 text 3
											811 text +
											812 text 𝑛
											813 text 𝑅
											814 text .
									815 text Optimizing this elementary bound in 
									816 text 𝑅
									817 text ,
									818 container
										819 text ∥ ∣ ⋅
										820 text ∣
										821 container
											822 text − 1
										823 text ∗ 𝑓
										824 text ∥
										825 text ∞
										826 text ≤ 2
										827 container
											828 text (
											829 container
												830 text 8 𝜋
											831 text 3
											832 text )
										833 container
											834 text 1 / 3
										835 container
											836 text 𝑛 ∥ 𝑓
											837 text ∥
											838 text 3
										839 text .
									840 text Combining with (3.2),
									841 container
										842 container
											843 text ∥ ∣ ⋅
											844 text ∣
											845 container
												846 text − 1
											847 text ∗
											848 text 𝑓
											849 text 𝑖
											850 text ∥
											851 text ∞
											852 text ≤
											853 text 𝐶
											854 text 𝑃
											855 container
												856 text 𝑛
												857 text 𝑖
												858 text 𝑚
												859 text 𝑖
												860 text 𝑆
												861 text 𝑇
											862 text ,
											863 text 𝐶
											864 text 𝑃
											865 text =
											866 container
												867 text (
												868 container
													869 text 8 𝜋
												870 text 3
												871 text )
											872 container
												873 text 1 / 3
											874 container
												875 text 𝐶 𝑆
											876 text .
										877 text (3.3)
									878 heading 3.3 Higher moments then remain bounded, Value: 3
										879 text 3.3 Higher moments then remain bounded
									880 text Put 
									881 container
										882 text 𝜙
										883 text 𝑞
										884 text ( 𝑣 ) = ⟨ 𝑣
										885 text ⟩
										886 text 𝑞
									887 text , 
									888 container
										889 text 𝑞 ≥ 2
									890 text . Applying (2.1), integrating by parts, and symmetrizing gives
									891 container
										892 container
											893 container
												894 text 𝑀
												895 text 𝑞
												896 text ′
												897 text =
												898 text 1
												899 text 2
												900 text ∑
												901 container
													902 text 𝑖 , 𝑗
												903 text 𝑐
												904 container
													905 text 𝑖 𝑗
												906 text ∬
												907 text 𝐹
												908 container
													909 text 𝑖 𝑗
												910 text [
											911 container
												912 text 𝑎 ( 𝑣 − 𝑤 ) :
												913 text (
												914 container
													915 container
														916 text 𝐷 2
													917 container
														918 text 𝜙 𝑞
													919 text (
													920 text 𝑣
													921 text )
													922 text 𝑚
													923 text 𝑖
												924 text +
												925 container
													926 container
														927 text 𝐷 2
													928 container
														929 text 𝜙 𝑞
													930 text (
													931 text 𝑤
													932 text )
													933 text 𝑚
													934 text 𝑗
												935 text )
											936 container
												937 text +
												938 text (
												939 container
													940 text 1
													941 text 𝑚
													942 text 𝑖
												943 text +
												944 container
													945 text 1
													946 text 𝑚
													947 text 𝑗
												948 text )
												949 text 𝑏 ( 𝑣 − 𝑤 ) ⋅ ( ∇
												950 text 𝜙
												951 text 𝑞
												952 text ( 𝑣 ) − ∇
												953 text 𝜙
												954 text 𝑞
												955 text ( 𝑤 ) ) ] .
										956 text (3.4)
									957 text Convexity of 
									958 container
										959 text 𝜙 𝑞
									960 text  makes the second line nonpositive:
									961 container
										962 text 𝑏 ( 𝑣 − 𝑤 ) ⋅ ( ∇
										963 text 𝜙
										964 text 𝑞
										965 text ( 𝑣 ) − ∇
										966 text 𝜙
										967 text 𝑞
										968 text ( 𝑤 ) ) ≤ 0.
									969 text Also,
									970 container
										971 text tr ⁡ 𝑎 ( 𝑧 ) =
										972 text 2
										973 container
											974 text ∣ 𝑧 ∣
										975 text , ∥
										976 text 𝐷
										977 text 2
										978 text 𝜙
										979 text 𝑞
										980 text ( 𝑣 ) ∥ ≤ 𝑞 ( 𝑞 − 1 ) ⟨ 𝑣
										981 text ⟩
										982 container
											983 text 𝑞 − 2
										984 text .
									985 text Consequently,
									986 container
										987 text 𝑀
										988 text 𝑞
										989 text ′
										990 text ≤ 2 𝑞 ( 𝑞 − 1 )
										991 text ∑
										992 container
											993 text 𝑖 , 𝑗
										994 container
											995 text 𝑐
											996 text 𝑖
											997 text 𝑗
										998 container
											999 text 𝑚 𝑖
										1000 text ∫
										1001 text 𝑓
										1002 text 𝑖
										1003 text ( 𝑣 ) ⟨ 𝑣
										1004 text ⟩
										1005 container
											1006 text 𝑞 − 2
										1007 text ( ∣ ⋅
										1008 text ∣
										1009 container
											1010 text − 1
										1011 text ∗
										1012 text 𝑓
										1013 text 𝑗
										1014 text ) ( 𝑣 ) 𝑑 𝑣 .
									1015 text Define the finite constant
									1016 container
										1017 container
											1018 text 𝐾
											1019 text 𝑞
											1020 text = 2 𝑞 ( 𝑞 − 1 )
											1021 text 𝐶
											1022 text 𝑃
											1023 container
												1024 text max ⁡
											1025 container
												1026 text 𝑖 = 1 , 2
											1027 text [
											1028 container
												1029 text 1
												1030 text 𝑚
												1031 text 𝑖
												1032 text 2
											1033 container
												1034 text ∑
												1035 text 𝑗
												1036 text =
												1037 text 1
												1038 text 2
											1039 container
												1040 text 𝑐
												1041 text 𝑖
												1042 text 𝑗
											1043 container
												1044 text 𝑛
												1045 text 𝑗
												1046 text 𝑚
												1047 text 𝑗
											1048 text ]
											1049 text .
										1050 text (3.5)
									1051 text Then
									1052 container
										1053 text 𝑀
										1054 text 𝑞
										1055 text ′
										1056 text ≤
										1057 text 𝐾
										1058 text 𝑞
										1059 container
											1060 text 𝑆 𝑇
										1061 text 𝑀
										1062 container
											1063 text 𝑞 − 2
										1064 text ≤
										1065 text 𝐾
										1066 text 𝑞
										1067 container
											1068 text 𝑆 𝑇
										1069 text 𝑀
										1070 text 𝑞
										1071 text ,
									1072 text and hence
									1073 container
										1074 container
											1075 text 𝑀
											1076 text 𝑞
											1077 text ( 𝑡 ) ≤
											1078 text 𝑀
											1079 text 𝑞
											1080 text ( 0 )
											1081 text 𝑒
											1082 container
												1083 text 𝐾
												1084 text 𝑞
												1085 container
													1086 text 𝑆 𝑇
												1087 text 𝑡
											1088 text .
										1089 text (3.6)
									1090 text This argument need not assume that Schwartz tails have already propagated. Smooth convex radial truncations, with a linear continuation outside a large ball, retain the drift sign and allow the estimate to pass to the limit.
									1091 heading 3.4 The actual weighted bound, Value: 3
										1092 text 3.4 The actual weighted 
										1093 container
											1094 text 𝐿 2
										1095 text  bound
									1096 text Cauchy–Schwarz gives
									1097 container
										1098 container
											1099 text ∫
											1100 text 𝑓
											1101 text 𝑖
											1102 text 2
											1103 text ⟨ 𝑣
											1104 text ⟩
											1105 text 7
										1106 container
											1107 text = ∫ (
											1108 text 𝑓
											1109 text 𝑖
											1110 text 3
											1111 text )
											1112 container
												1113 text 1 / 2
											1114 text (
											1115 text 𝑓
											1116 text 𝑖
											1117 text ⟨ 𝑣
											1118 text ⟩
											1119 text 14
											1120 text )
											1121 container
												1122 text 1 / 2
										1123 container
											1124 text ≤ ∥
											1125 text 𝑓
											1126 text 𝑖
											1127 text ∥
											1128 text 3
											1129 container
												1130 text 3 / 2
											1131 container
												1132 text ( ∫
												1133 text 𝑓
												1134 text 𝑖
												1135 text ⟨ 𝑣
												1136 text ⟩
												1137 text 14
												1138 text )
											1139 container
												1140 text 1 / 2
											1141 text .
									1142 text Therefore
									1143 container
										1144 container
											1145 text 𝑌
											1146 text 7
											1147 text ( 𝑡 ) ≤
											1148 container
												1149 text (
												1150 container
													1151 text 𝐶 𝑆
												1152 text 4
												1153 text )
											1154 container
												1155 text 3 / 2
											1156 text (
											1157 text 𝑚
											1158 text 1
											1159 text +
											1160 text 𝑚
											1161 text 2
											1162 text )
											1163 text 𝑆
											1164 text 𝑇
											1165 container
												1166 text 3 / 2
											1167 container
												1168 text 𝑀
												1169 text 14
												1170 text ( 0 )
											1171 text exp ⁡  ⁣
											1172 text (
											1173 container
												1174 container
													1175 text 𝐾 14
												1176 container
													1177 text 𝑆 𝑇
												1178 text 𝑡
												1179 text 2
											1180 text )
											1181 text .
										1182 text (3.7)
									1183 text The local weighted-
									1184 container
										1185 text 𝐿 2
									1186 text  strong theory can be restarted from these bounds, together with the fixed particle numbers, masses, coefficients, energy and entropy bounds. Its relevant local statement is Lemma 2.7 of Junné–Winter–Yoldaş. 
									1187 link (collapsed) Value: arxiv.org/html/2512.17082v1?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: On the existence of solutions to the multi-species Landau equation, https://arxiv.org/html/2512.17082v1?utm_source=chatgpt.com
									1188 text For nonunit particle numbers, the normalization 
									1189 container
										1190 text 𝑓
										1191 text 𝑖
										1192 text =
										1193 text 𝑛
										1194 text 𝑖
										1195 text 𝑔
										1196 text 𝑖
									1197 text  gives effective coefficients 
									1198 container
										1199 text 𝑐
										1200 container
											1201 text 𝑖 𝑗
										1202 text 𝑛
										1203 text 𝑗
									1204 text . These satisfy weighted detailed balance,
									1205 container
										1206 text 𝑛
										1207 text 𝑖
										1208 text (
										1209 text 𝑐
										1210 container
											1211 text 𝑖 𝑗
										1212 text 𝑛
										1213 text 𝑗
										1214 text ) =
										1215 text 𝑛
										1216 text 𝑗
										1217 text (
										1218 text 𝑐
										1219 container
											1220 text 𝑗 𝑖
										1221 text 𝑛
										1222 text 𝑖
										1223 text ) ,
									1224 text and the entropy and Fisher quantities retain weights 
									1225 container
										1226 text 𝑛 𝑖
									1227 text . One must preserve these weights when adapting the probability-density formulation. Thus, within this local strong class,
									1228 container
										1229 container
											1230 text 𝑇
											1231 text ∗
											1232 text < ∞ ⟹
											1233 container
												1234 text sup ⁡
											1235 container
												1236 text 𝑡 <
												1237 text 𝑇
												1238 text ∗
											1239 text 𝐼
											1240 text 𝑚
											1241 text ( 𝑓 ( 𝑡 ) ) = ∞ .
										1242 text (3.8)
									1243 container
										1244 text What remains unproved is a bound on 
										1245 container
											1246 text 𝑆 𝑇
										1247 text  from the initial data.
									1248 text  Equation (3.7) proves that such a bound would accomplish continuation; it does not establish that bound.
									1249 heading 4. Fisher information can increase with finite masses, Value: 2
										1250 text 4. Fisher information can increase with finite masses
									1251 text The following auxiliary result strengthens the distinction between a failed functional and a failed Cauchy theorem.
									1252 container
										1253 text Auxiliary conclusion.  There exist strictly finite positive masses, positive symmetric collision coefficients, and strictly positive Schwartz probability densities for which
									1254 container
										1255 container
											1256 text 𝑑
											1257 container
												1258 text 𝑑 𝑡
											1259 text 𝐼
											1260 text 𝑚
											1261 text ( 𝑓 ( 𝑡 ) ) ∣
										1262 container
											1263 text 𝑡 = 0
										1264 text > 0.
									1265 text This does not imply finite-time blowup.
									1266 text Here is a construction in which the final data and masses are all finite.
									1267 heading 4.1 A strictly positive angular seed, Value: 3
										1268 text 4.1 A strictly positive angular seed
									1269 text Let
									1270 container
										1271 text ℎ
										1272 text 𝜎
										1273 text ( 𝑟 ) =
										1274 text 𝑍
										1275 text 𝜎
										1276 container
											1277 text − 1
										1278 text exp ⁡  ⁣
										1279 text [
										1280 text −
										1281 container
											1282 text (
											1283 container
												1284 text 𝑟 2
											1285 text −
											1286 text 1
											1287 container
												1288 text ) 2
											1289 text 𝜎
											1290 text 2
										1291 text ]
										1292 text ,
										1293 text ∫
										1294 container
											1295 text 𝑅 3
										1296 text ℎ
										1297 text 𝜎
										1298 text ( ∣ 𝑣 ∣ ) 𝑑 𝑣 = 1.
									1299 text Choose 
									1300 container
										1301 text 𝜒 ∈
										1302 text 𝐶
										1303 text 𝑐
										1304 text ∞
										1305 text ( ( 1 / 2 , 3 / 2 ) )
									1306 text , equal to 
									1307 text 1
									1308 text  on 
									1309 container
										1310 text [ 3 / 4 , 5 / 4 ]
									1311 text , and set
									1312 container
										1313 text 𝑎
										1314 text 0
										1315 text ( 𝑟 ) = 𝜒 ( 𝑟 )
										1316 text 𝑟
										1317 container
											1318 text 3 / 2
										1319 text , 𝑌 ( 𝜔 ) =
										1320 text 𝜔
										1321 text 1
										1322 text .
									1323 text For small 
									1324 text 𝜀
									1325 text , define
									1326 container
										1327 container
											1328 text 𝑓
											1329 text 𝜀
											1330 text ( 𝑣 ) =
											1331 text 𝑍
											1332 text 𝜀
											1333 container
												1334 text − 1
											1335 text ℎ
											1336 text 𝜎
											1337 text ( ∣ 𝑣 ∣ )
											1338 text 𝑒
											1339 container
												1340 text 𝜀
												1341 text 𝑎
												1342 text 0
												1343 text ( ∣ 𝑣 ∣ ) 𝑌 (
												1344 text 𝑣
												1345 text ^
												1346 text )
											1347 text .
										1348 text (4.1)
									1349 text This is strictly positive and Schwartz. The angular perturbation vanishes near the origin, so it is smooth there. For the auxiliary angular operator
									1350 container
										1351 text 𝐿 𝑓 = div ⁡  ⁣
										1352 text (
										1353 container
											1354 text 𝑃
											1355 text 𝑣
											1356 text ∣
											1357 text 𝑣
											1358 text ∣
										1359 text ∇
										1360 text 𝑓
										1361 text )
										1362 text =
										1363 text 𝑟
										1364 container
											1365 text − 3
										1366 text Δ
										1367 container
											1368 text 𝑆 2
										1369 text 𝑓 ,
									1370 text one obtains
									1371 container
										1372 container
											1373 container
												1374 text ⟨
												1375 text 𝐼
												1376 text ′
												1377 text (
												1378 text 𝑓
												1379 text 𝜀
												1380 text ) , 𝐿
												1381 text 𝑓
												1382 text 𝜀
												1383 text ⟩ =
											1384 container
												1385 text −
												1386 container
													1387 text 16 𝜋
												1388 text 3
												1389 text 𝜀
												1390 text 2
												1391 text ∫
												1392 text 0
												1393 text ∞
												1394 text ℎ
												1395 text 𝜎
												1396 text ( 𝑟 )
												1397 text 𝑟
												1398 container
													1399 text − 3
												1400 text [
												1401 container
													1402 text (
													1403 text 𝑟
													1404 container
														1405 text 𝑎 0 ′
													1406 text (
													1407 text 𝑟
													1408 text )
													1409 text −
													1410 container
														1411 text 3 2
													1412 container
														1413 text 𝑎 0
													1414 text (
													1415 text 𝑟
													1416 text )
													1417 text )
													1418 text 2
												1419 text −
												1420 container
													1421 text 1 4
												1422 container
													1423 text 𝑎 0
												1424 text (
												1425 text 𝑟
												1426 container
													1427 text ) 2
												1428 text ]
												1429 text 𝑑 𝑟
											1430 container
												1431 text + 𝑂 (
												1432 text 𝜀
												1433 text 4
												1434 text ) .
										1435 text (4.2)
									1436 text The constants follow from
									1437 container
										1438 text ∫
										1439 container
											1440 text 𝑆 2
										1441 text ∣ ∇ 𝑌
										1442 text ∣
										1443 text 2
										1444 text =
										1445 container
											1446 text 8 𝜋
										1447 text 3
										1448 text ,
										1449 text ∫
										1450 container
											1451 text 𝑆 2
										1452 text Γ
										1453 text 2
										1454 text ( 𝑌 ) =
										1455 container
											1456 text 16 𝜋
										1457 text 3
										1458 text .
									1459 text For fixed 
									1460 text 𝜎
									1461 text , the remainder is bounded by a finite constant times 
									1462 container
										1463 text 𝜀 4
									1464 text ; the expression is even in 
									1465 text 𝜀
									1466 text . Where 
									1467 container
										1468 text 𝜒 = 1
									1469 text , the bracket in (4.2) equals 
									1470 container
										1471 text −
										1472 text 𝑟
										1473 text 3
										1474 text / 4
									1475 text . The cutoff-transition contribution is exponentially small as 
									1476 container
										1477 text 𝜎 ↓ 0
									1478 text , and the integral tends to
									1479 container
										1480 text −
										1481 text 1
										1482 container
											1483 text 16 𝜋
										1484 text .
									1485 text Choose 
									1486 container
										1487 text 𝜎 > 0
									1488 text  small enough and then 
									1489 container
										1490 text 𝜀 > 0
									1491 text  small enough. This gives a fixed strictly positive Schwartz density 
									1492 text 𝑓
									1493 text  such that
									1494 container
										1495 container
											1496 text 𝐴
											1497 text 0
											1498 text : = ⟨
											1499 text 𝐼
											1500 text ′
											1501 text ( 𝑓 ) , 𝐿 𝑓 ⟩ > 0.
										1502 text (4.3)
									1503 heading 4.2 Replace the concentrated background by a smooth density, Value: 3
										1504 text 4.2 Replace the concentrated background by a smooth density
									1505 text Let 
									1506 container
										1507 text 𝑔 𝛿
									1508 text  be a centered Gaussian probability density with variance tending to zero as 
									1509 container
										1510 text 𝛿 ↓ 0
									1511 text . Set
									1512 container
										1513 text 𝐴
										1514 text 𝛿
										1515 text =
										1516 text ⟨
										1517 container
											1518 text 𝐼 ′
										1519 text (
										1520 text 𝑓
										1521 text )
										1522 text ,
										1523 text div
										1524 text ⁡
										1525 text (
										1526 text 𝐴
										1527 text [
										1528 container
											1529 text 𝑔 𝛿
										1530 text ]
										1531 text ∇
										1532 text 𝑓
										1533 text )
										1534 text ⟩
										1535 text .
									1536 text Then
									1537 container
										1538 container
											1539 text 𝐴
											1540 text 𝛿
											1541 text ⟶
											1542 text 𝐴
											1543 text 0
											1544 text .
										1545 text (4.4)
									1546 text For this particular 
									1547 text 𝑓
									1548 text , convergence follows directly from the unsplit first variation. Write
									1549 container
										1550 text Ψ
										1551 text 𝑓
										1552 text = − 2 Δ log ⁡ 𝑓 − ∣ ∇ log ⁡ 𝑓
										1553 text ∣
										1554 text 2
										1555 text ,
										1556 text 𝐼
										1557 text ′
										1558 text ( 𝑓 ) [ 𝑞 ] = ∫
										1559 text Ψ
										1560 text 𝑓
										1561 text 𝑞 .
									1562 text Then
									1563 container
										1564 text 𝐴
										1565 text 𝛿
										1566 text = ∫
										1567 text 𝑔
										1568 text 𝛿
										1569 text ( 𝑤 )
										1570 text 𝐾
										1571 text 𝑓
										1572 text ( 𝑤 ) 𝑑 𝑤 ,
									1573 text where
									1574 container
										1575 text 𝐾
										1576 text 𝑓
										1577 text ( 𝑤 ) = − ∫ 𝑎 ( 𝑣 − 𝑤 ) : [ ∇ 𝑓 ( 𝑣 ) ⊗ ∇
										1578 text Ψ
										1579 text 𝑓
										1580 text ( 𝑣 ) ] 𝑑 𝑣 .
									1581 text The tensor factor is Schwartz, and 
									1582 text 𝑎
									1583 text  is locally integrable. Thus 
									1584 container
										1585 text 𝐾 𝑓
									1586 text  is bounded and continuous, which proves (4.4). Fix one positive 
									1587 text 𝛿
									1588 text  such that 
									1589 container
										1590 text 𝐴 : =
										1591 text 𝐴
										1592 text 𝛿
										1593 text > 0
									1594 text , and write 
									1595 container
										1596 text 𝑔 =
										1597 text 𝑔
										1598 text 𝛿
									1599 text .
									1600 heading 4.3 Fix a finite second mass, Value: 3
										1601 text 4.3 Fix a finite second mass
									1602 text For convenience, define
									1603 container
										1604 text 𝐷
										1605 text ℎ
										1606 text 𝑘 = div ⁡ ( 𝐴 [ ℎ ] ∇ 𝑘 ) ,
										1607 text 𝐹
										1608 text ℎ
										1609 text 𝑘 = div ⁡ ( 𝑘 ( 𝑏 ∗ ℎ ) ) ,
									1610 text and the finite numbers
									1611 container
										1612 text 𝑆
										1613 container
											1614 text =
											1615 text 𝐼
											1616 text ′
											1617 text ( 𝑓 ) [
											1618 text 𝐷
											1619 text 𝑓
											1620 text 𝑓 −
											1621 text 𝐹
											1622 text 𝑓
											1623 text 𝑓 ] ,
										1624 text 𝐵
										1625 container
											1626 text =
											1627 text 𝐼
											1628 text ′
											1629 text ( 𝑓 ) [
											1630 text 𝐹
											1631 text 𝑔
											1632 text 𝑓 ] ,
										1633 text 𝐶
										1634 container
											1635 text =
											1636 text 𝐼
											1637 text ′
											1638 text ( 𝑔 ) [
											1639 text 𝐷
											1640 text 𝑓
											1641 text 𝑔 ] ,
										1642 text 𝐷
										1643 container
											1644 text =
											1645 text 𝐼
											1646 text ′
											1647 text ( 𝑔 ) [
											1648 text 𝐹
											1649 text 𝑓
											1650 text 𝑔 ] .
									1651 text Take
									1652 container
										1653 text 𝑚
										1654 text 1
										1655 text = 1 ,
										1656 text 𝑚
										1657 text 2
										1658 text = 𝑀 ,
										1659 text 𝑐
										1660 text 11
										1661 text =
										1662 text 𝑐
										1663 text 22
										1664 text = 1 ,
										1665 text 𝑐
										1666 text 12
										1667 text =
										1668 text 𝑐
										1669 text 21
										1670 text = 𝑐 .
									1671 text Since 
									1672 text 𝑔
									1673 text  is Gaussian, its same-species collision term vanishes. For the original finite-mass operator, the exact derivative is
									1674 container
										1675 container
											1676 text 𝐼
											1677 text 𝑚
											1678 text ′
											1679 text ( 0 ) = 𝑆 + 𝑐 𝐴 −
											1680 container
												1681 text 𝑐 𝐵
											1682 text 𝑀
											1683 text −
											1684 container
												1685 text 𝑐 𝐷
											1686 container
												1687 text 𝑀 2
											1688 text +
											1689 container
												1690 text 𝑐 𝐶
											1691 container
												1692 text 𝑀 3
											1693 text .
										1694 text (4.5)
									1695 text Choose
									1696 container
										1697 text 𝑐 =
										1698 container
											1699 text ∣ 𝑆 ∣ + 1
										1700 text 𝐴
										1701 text > 0 , 𝐾 = ∣ 𝐵 ∣ + ∣ 𝐶 ∣ + ∣ 𝐷 ∣ .
									1702 text Then 
									1703 container
										1704 text 𝑆 + 𝑐 𝐴 ≥ 1
									1705 text . Any finite
									1706 container
										1707 text 𝑀 > max ⁡ { 1 , 2 𝑐 𝐾 }
									1708 text makes the absolute value of the remaining terms less than 
									1709 container
										1710 text 1 / 2
									1711 text . Therefore
									1712 container
										1713 container
											1714 text 𝐼
											1715 text 𝑚
											1716 text ′
											1717 text ( 0 ) >
											1718 text 1
											1719 text 2
											1720 text .
										1721 text (4.6)
									1722 text The limiting arguments above only select fixed smooth densities and a fixed finite 
									1723 text 𝑀
									1724 text . Equation (4.5), which establishes the final claim, is exact for your collision operator. This rules out universal monotonicity of 
									1725 container
										1726 text 𝐼 𝑚
									1727 text  over the full parameter/data class. A global regularity proof could still allow controlled Fisher growth or use a different quantity.
									1728 heading 5. Why the finite-recoil compensation remains unclosed, Value: 2
										1729 text 5. Why the finite-recoil compensation remains unclosed
									1730 text Your 
									1731 container
										1732 text 𝐽
										1733 text 𝑖
										1734 text 𝑗
									1735 text  quantities have the correct entropy meaning. The unresolved issue is their evolution. In center/relative variables, write
									1736 container
										1737 text 𝐹 =
										1738 text 𝐹
										1739 container
											1740 text 𝑖 𝑗
										1741 text , Ψ = log ⁡ 𝐹 , 𝑟 = ∣ 𝑧 ∣ .
									1742 text Then
									1743 container
										1744 text 𝐽
										1745 container
											1746 text 𝑖 𝑗
										1747 text = ∫ 𝐹
										1748 text 𝑟
										1749 container
											1750 text − 3
										1751 text ∣
										1752 text ∇
										1753 container
											1754 text 𝑆 2
										1755 text Ψ
										1756 text ∣
										1757 text 2
										1758 text 𝑑 𝑍 𝑑 𝑧 .
									1759 text Its first variation is
									1760 container
										1761 container
											1762 container
												1763 text 𝛿
												1764 text 𝐽
												1765 container
													1766 text 𝑖 𝑗
											1767 container
												1768 text 𝛿 𝐹
											1769 text = −
											1770 text 𝑟
											1771 container
												1772 text − 3
											1773 text (
											1774 text 2
											1775 container
												1776 text Δ
												1777 text 𝑆
												1778 text 2
											1779 text Ψ
											1780 text +
											1781 text ∣
											1782 container
												1783 text ∇
												1784 text 𝑆
												1785 text 2
											1786 text Ψ
											1787 container
												1788 text ∣ 2
											1789 text )
											1790 text = :
											1791 text Φ
											1792 container
												1793 text 𝑖 𝑗
											1794 text .
										1795 text (5.1)
									1796 text Along the actual mixture,
									1797 container
										1798 text ∂
										1799 text 𝑡
										1800 text 𝐹
										1801 container
											1802 text 𝑖 𝑗
										1803 text =
										1804 text ∑
										1805 text 𝑘
										1806 text [
										1807 container
											1808 text 𝑄
											1809 text 𝑖
											1810 text 𝑘
										1811 text (
										1812 container
											1813 text 𝑓 𝑖
										1814 text ,
										1815 container
											1816 text 𝑓 𝑘
										1817 text )
										1818 text (
										1819 text 𝑣
										1820 text )
										1821 container
											1822 text 𝑓 𝑗
										1823 text (
										1824 text 𝑤
										1825 text )
										1826 text +
										1827 container
											1828 text 𝑓 𝑖
										1829 text (
										1830 text 𝑣
										1831 text )
										1832 container
											1833 text 𝑄
											1834 text 𝑗
											1835 text 𝑘
										1836 text (
										1837 container
											1838 text 𝑓 𝑗
										1839 text ,
										1840 container
											1841 text 𝑓 𝑘
										1842 text )
										1843 text (
										1844 text 𝑤
										1845 text )
										1846 text ]
										1847 text .
									1848 text Consequently,
									1849 container
										1850 container
											1851 text 𝑑
											1852 container
												1853 text 𝑑 𝑡
											1854 text 𝐽
											1855 container
												1856 text 𝑖 𝑗
											1857 text =
											1858 text ∑
											1859 text 𝑘
											1860 text ∬
											1861 text Φ
											1862 container
												1863 text 𝑖 𝑗
											1864 text [
											1865 container
												1866 text 𝑄
												1867 text 𝑖
												1868 text 𝑘
											1869 text (
											1870 container
												1871 text 𝑓 𝑖
											1872 text ,
											1873 container
												1874 text 𝑓 𝑘
											1875 text )
											1876 text (
											1877 text 𝑣
											1878 text )
											1879 container
												1880 text 𝑓 𝑗
											1881 text (
											1882 text 𝑤
											1883 text )
											1884 text +
											1885 container
												1886 text 𝑓 𝑖
											1887 text (
											1888 text 𝑣
											1889 text )
											1890 container
												1891 text 𝑄
												1892 text 𝑗
												1893 text 𝑘
											1894 text (
											1895 container
												1896 text 𝑓 𝑗
											1897 text ,
											1898 container
												1899 text 𝑓 𝑘
											1900 text )
											1901 text (
											1902 text 𝑤
											1903 text )
											1904 text ]
											1905 text 𝑑 𝑣 𝑑 𝑤 .
										1906 text (5.2)
									1907 text Substituting the collision operators introduces mixed triple integrals. Both groups in (5.2) matter for finite recoil. A proposed functional such as
									1908 container
										1909 text 𝐼
										1910 text 𝑚
										1911 text +
										1912 text ∑
										1913 container
											1914 text 𝑖 , 𝑗
										1915 text 𝑎
										1916 container
											1917 text 𝑖 𝑗
										1918 text 𝐽
										1919 container
											1920 text 𝑖 𝑗
										1921 text + 𝑅 𝐻 ( 𝑓 ∣ 𝑀 )
									1922 text therefore needs an estimate for those mixed terms. The entropy identity controls the time integral of the 
									1923 container
										1924 text 𝐽
										1925 text 𝑖
										1926 text 𝑗
									1927 text , while this proposal needs control of their derivatives. The known possibility that entropy dissipation increases prevents replacing that estimate by a monotonicity assertion. 
									1928 link (collapsed) Value: arxiv.org/abs/2609.03847?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: A counterexample to McKean's conjecture for the Landau-Coulomb equation, https://arxiv.org/abs/2609.03847?utm_source=chatgpt.com
									1929 text There is also an endpoint integrability issue. For generic cross-species data near 
									1930 container
										1931 text 𝑧 = 0
									1932 text , the completed-square Fisher decomposition has pieces with logarithmically divergent integrals. Their cancellation must be retained. The finite-mass construction above uses the unsplit first variation and avoids subtracting separately divergent expressions. I have not obtained the required estimate for (5.2).
									1933 heading 6. An alternative functional with a precise remaining inequality, Value: 2
										1934 text 6. An alternative functional with a precise remaining inequality
									1935 text I also pursued a different representation that measures regularity below one full derivative. For 
									1936 container
										1937 text 0 < 𝑠 < 1
									1938 text , let
									1939 container
										1940 text 𝑃
										1941 text 𝜏
										1942 container
											1943 text ( 𝑖 )
										1944 text =
										1945 text 𝑒
										1946 container
											1947 text ( 𝜏 /
											1948 text 𝑚
											1949 text 𝑖
											1950 text ) Δ
									1951 text be an auxiliary Gaussian heat flow, and define
									1952 container
										1953 container
											1954 text 𝐸
											1955 text 𝑠
											1956 text ( 𝑓 ) = 𝑠 ( 1 − 𝑠 )
											1957 text ∑
											1958 text 𝑖
											1959 text ∫
											1960 text 0
											1961 text ∞
											1962 text [
											1963 text 𝐻
											1964 text (
											1965 container
												1966 text 𝑓 𝑖
											1967 text )
											1968 text −
											1969 text 𝐻
											1970 text (
											1971 container
												1972 text 𝑃 𝜏
												1973 text (
												1974 text 𝑖
												1975 text )
											1976 container
												1977 text 𝑓 𝑖
											1978 text )
											1979 text ]
											1980 container
												1981 text 𝑑 𝜏
											1982 container
												1983 text 𝜏
												1984 text 1
												1985 text +
												1986 text 𝑠
											1987 text .
										1988 text (6.1)
									1989 text Here 
									1990 text 𝜏
									1991 text  is auxiliary heat time, distinct from the physical collision time.
									1992 heading 6.1 Its initial value is controlled by the supplied data, Value: 3
										1993 text 6.1 Its initial value is controlled by the supplied data
									1994 text The heat entropy identity gives
									1995 container
										1996 text 𝐸
										1997 text 𝑠
										1998 text ( 𝑓 ) = ( 1 − 𝑠 )
										1999 text ∫
										2000 text 0
										2001 text ∞
										2002 text 𝜏
										2003 container
											2004 text − 𝑠
										2005 text 𝐼
										2006 text 𝑚
										2007 text (
										2008 text 𝑃
										2009 text 𝜏
										2010 text 𝑓 ) 𝑑 𝜏 .
									2011 text Set
									2012 container
										2013 text 𝑁 =
										2014 text 𝑛
										2015 text 1
										2016 text +
										2017 text 𝑛
										2018 text 2
										2019 text , 𝐾 =
										2020 container
											2021 text 3 𝑁
										2022 text 2
										2023 text ,
										2024 text 𝐼
										2025 text 0
										2026 text =
										2027 text 𝐼
										2028 text 𝑚
										2029 text ( 𝑓 ) .
									2030 text The heat-flow estimates
									2031 container
										2032 text 𝐼
										2033 text 𝑚
										2034 text (
										2035 text 𝑃
										2036 text 𝜏
										2037 text 𝑓 ) ≤ min ⁡
										2038 text {
										2039 container
											2040 text 𝐼 0
										2041 text ,
										2042 container
											2043 text 𝐾 𝜏
										2044 text }
									2045 text yield, by splitting at 
									2046 container
										2047 text 𝜏 = 𝐾 /
										2048 text 𝐼
										2049 text 0
									2050 text ,
									2051 container
										2052 container
											2053 text 0 ≤
											2054 text 𝐸
											2055 text 𝑠
											2056 text ( 𝑓 ) ≤
											2057 container
												2058 text 𝐾
												2059 container
													2060 text 1 − 𝑠
												2061 text 𝐼
												2062 text 0
												2063 text 𝑠
											2064 text 𝑠
											2065 text .
										2066 text (6.2)
									2067 text Thus this candidate is finite for every datum in your question.
									2068 heading 6.2 It controls fractional regularity, Value: 3
										2069 text 6.2 It controls fractional regularity
									2070 text The entropy Jensen gap bounds
									2071 container
										2072 text 𝐻 ( 𝑓 ) − 𝐻 (
										2073 text 𝑃
										2074 text 𝜏
										2075 text 𝑓 ) ≥ ∥
										2076 text 𝑓
										2077 text ∥
										2078 text 2
										2079 text 2
										2080 text − ∥
										2081 text 𝑃
										2082 text 𝜏
										2083 text 𝑓
										2084 text ∥
										2085 text 2
										2086 text 2
										2087 text .
									2088 text Integrating in 
									2089 text 𝜏
									2090 text  gives
									2091 container
										2092 container
											2093 text 𝐸
											2094 text 𝑠
											2095 text ( 𝑓 ) ≥
											2096 text 2
											2097 text 𝑠
											2098 text Γ ( 2 − 𝑠 )
											2099 text ∑
											2100 text 𝑖
											2101 text 𝑚
											2102 text 𝑖
											2103 container
												2104 text − 𝑠
											2105 text ∥
											2106 container
												2107 text 𝑓 𝑖
											2108 text ∥
											2109 container
												2110 text 𝐻
												2111 text ˙
												2112 text 𝑠
											2113 text 2
											2114 text .
										2115 text (6.3)
									2116 text The Fourier convention here gives 
									2117 container
										2118 text − Δ
									2119 text  the multiplier 
									2120 container
										2121 text ∣ 𝜉
										2122 text ∣
										2123 text 2
									2124 text . Fractional Sobolev embedding then controls
									2125 container
										2126 container
											2127 text 𝑓
											2128 text 𝑖
											2129 text ∈
											2130 text 𝐿
											2131 container
												2132 text 𝑝 𝑠
											2133 text ,
											2134 text 𝑝
											2135 text 𝑠
											2136 text =
											2137 text 3
											2138 container
												2139 text 3 − 2 𝑠
											2140 text .
										2141 text (6.4)
									2142 text In particular, 
									2143 container
										2144 text 𝑠 > 1 / 2
									2145 text  gives 
									2146 container
										2147 text 𝑝
										2148 text 𝑠
										2149 text > 3 / 2
									2150 text , making this functional relevant to continuation. It also has the needed product structure: it tensorizes on probability products and is marginal-superadditive, because independent heat channels decrease mutual information. Its first variation at a product is additive across the velocity blocks. These properties are established calculations. They do not imply dissipation under Landau collisions.
									2151 heading 6.3 The exact collision term whose sign is missing, Value: 3
										2152 text 6.3 The exact collision term whose sign is missing
									2153 text For a pair, let
									2154 container
										2155 text 𝐹 =
										2156 text 𝑓
										2157 text 𝑖
										2158 text ( 𝑣 )
										2159 text 𝑓
										2160 text 𝑗
										2161 text ( 𝑤 ) , 𝛼 ( 𝑧 ) = ∣ 𝑧
										2162 text ∣
										2163 container
											2164 text − 3
										2165 text .
									2166 text Choose the three rotation fields
									2167 container
										2168 text 𝑏
										2169 text 𝑘
										2170 text ( 𝑧 ) ∈ {
										2171 text 𝑒
										2172 text 1
										2173 text × 𝑧 ,
										2174 text 𝑒
										2175 text 2
										2176 text × 𝑧 ,
										2177 text 𝑒
										2178 text 3
										2179 text × 𝑧 } ,
									2180 text and define
									2181 container
										2182 text 𝐿
										2183 text 𝑘
										2184 text =
										2185 container
											2186 text 𝑏
											2187 text 𝑘
											2188 text ( 𝑧 ) ⋅
											2189 text ∇
											2190 text 𝑣
										2191 container
											2192 text 𝑚 𝑖
										2193 text −
										2194 container
											2195 text 𝑏
											2196 text 𝑘
											2197 text ( 𝑧 ) ⋅
											2198 text ∇
											2199 text 𝑤
										2200 container
											2201 text 𝑚 𝑗
										2202 text ,
										2203 text 𝑞
										2204 text 𝑘
										2205 text =
										2206 text 𝐿
										2207 text 𝑘
										2208 text log ⁡ 𝐹 .
									2209 text The pair heat semigroup
									2210 container
										2211 text 𝑃
										2212 text 𝜏
										2213 text =
										2214 text 𝑒
										2215 container
											2216 text 𝜏 (
											2217 text Δ
											2218 text 𝑣
											2219 text /
											2220 text 𝑚
											2221 text 𝑖
											2222 text +
											2223 text Δ
											2224 text 𝑤
											2225 text /
											2226 text 𝑚
											2227 text 𝑗
											2228 text )
									2229 text commutes with each 
									2230 container
										2231 text 𝐿 𝑘
									2232 text . For sufficiently regular profiles, first restricting the auxiliary heat integral to a compact interval, the entropy-gap calculation gives the pair expression
									2233 container
										2234 container
											2235 text 𝐵
											2236 container
												2237 text 𝑖 𝑗 , 𝑘
											2238 text ( 𝜏 ) = ∫ 𝛼 𝐹
											2239 text 𝑞
											2240 text 𝑘
											2241 text 2
											2242 text − ∫
											2243 container
												2244 text 𝑃
												2245 text 𝜏
												2246 text ( 𝛼 𝐹
												2247 text 𝑞
												2248 text 𝑘
												2249 text )
												2250 text 𝑃
												2251 text 𝜏
												2252 text ( 𝐹
												2253 text 𝑞
												2254 text 𝑘
												2255 text )
											2256 container
												2257 text 𝑃
												2258 text 𝜏
												2259 text 𝐹
											2260 text .
										2261 text (6.5)
									2262 text After assembling ordered pairs, the corresponding formal full-range identity is
									2263 container
										2264 container
											2265 text 𝑑
											2266 container
												2267 text 𝑑 𝑡
											2268 text 𝐸
											2269 text 𝑠
											2270 text ( 𝑓 ( 𝑡 ) ) = −
											2271 container
												2272 text 𝑠 ( 1 − 𝑠 )
											2273 text 2
											2274 text ∑
											2275 container
												2276 text 𝑖 , 𝑗
											2277 text 𝑐
											2278 container
												2279 text 𝑖 𝑗
											2280 text ∑
											2281 text 𝑘
											2282 text ∫
											2283 text 0
											2284 text ∞
											2285 text 𝐵
											2286 container
												2287 text 𝑖 𝑗 , 𝑘
											2288 text ( 𝜏 )
											2289 container
												2290 text 𝑑 𝜏
											2291 container
												2292 text 𝜏
												2293 text 1
												2294 text +
												2295 text 𝑠
											2296 text .
										2297 text (6.6)
									2298 text Passing from truncated auxiliary intervals to (6.6) requires appropriate bounds; it is not an additional regularity assumption that can be inserted into a global proof without justification. For constant 
									2299 text 𝛼
									2300 text , a contraction argument gives the desired sign. For Coulomb, the two numerator factors in (6.5) contain different weights. The radial coefficient does not commute with heat. A naive weighted Cauchy–Schwarz argument introduces 
									2301 container
										2302 text 𝑃
										2303 text 𝜏
										2304 text ( 𝛼 𝐹 )
									2305 text , which is generally divergent at 
									2306 container
										2307 text 𝑧 = 0
									2308 text . In contrast,
									2309 container
										2310 text 𝛼 𝐹
										2311 text 𝑞
										2312 text 𝑘
										2313 text = 𝑂 ( ∣ 𝑧
										2314 text ∣
										2315 container
											2316 text − 2
										2317 text ) , 𝛼 𝐹
										2318 text 𝑞
										2319 text 𝑘
										2320 text 2
										2321 text = 𝑂 ( ∣ 𝑧
										2322 text ∣
										2323 container
											2324 text − 1
										2325 text ) ,
									2326 text are locally integrable for smooth product profiles. Preserving those score factors is essential.
									2327 text I have not proved that the integrated expression in (6.6) is nonnegative, or bounded below by a quantity that yields a closed finite-time growth estimate.
									2328 text  Moreover, as 
									2329 container
										2330 text 𝑠 ↑ 1
									2331 text , the normalized functional approaches 
									2332 container
										2333 text 𝐼 𝑚
									2334 text ; the strict Fisher-growth examples prevent simply asserting monotonicity for all 
									2335 text 𝑠
									2336 text  close to one.
									2337 heading 7. The remaining mathematical obligation, Value: 2
										2338 text 7. The remaining mathematical obligation
									2339 text The explicit continuation calculation reduces one sufficient route to proving
									2340 container
										2341 container
											2342 text sup ⁡
										2343 container
											2344 text 0 ≤ 𝑡 < 𝑇
										2345 text 𝐼
										2346 text 𝑚
										2347 text ( 𝑓 ( 𝑡 ) ) ≤
										2348 text 𝐵
										2349 text 𝑇
										2350 text  ⁣
										2351 text (
										2352 container
											2353 text 𝑚 𝑖
										2354 text ,
										2355 container
											2356 text 𝑐
											2357 text 𝑖
											2358 text 𝑗
										2359 text ,
										2360 container
											2361 text 𝑛 𝑖
										2362 text ,
										2363 text 𝐸
										2364 text ,
										2365 text 𝐻
										2366 text (
										2367 container
											2368 text 𝑓 0
										2369 text ∣
										2370 text 𝑀
										2371 text )
										2372 text ,
										2373 container
											2374 text 𝐼 𝑚
										2375 text (
										2376 container
											2377 text 𝑓 0
										2378 text )
										2379 text ,
										2380 text specified initial weighted norms
										2381 text )
										2382 text < ∞
									2383 text for every finite 
									2384 text 𝑇
									2385 text . An alternative regularity functional could replace Fisher information, but its evolution and continuation implications must both be proved. The heat–entropy construction above supplies a candidate and an exact remaining collision inequality; it does not supply that inequality’s sign.
									2386 text The full affirmative theorem and a genuine negative obstruction both remain unestablished by this work.
									2387 text  The finite-mass Fisher-growth construction eliminates one universal monotonicity claim, while the conditional estimate shows exactly how a successful a priori regularity bound would complete the Cauchy theory.
									2388 button Copy
										2389 image
									2390 pop up button (collapsed) Description: Rate response, ID: radix-_r_1lh_, Secondary Actions: Expand
									2391 checkbox Description: Read aloud, Value: 0
									2392 button Share
									2393 pop up button (collapsed) Description: More actions, ID: radix-_r_1ln_, Secondary Actions: Expand
									2394 heading You said:, Value: 4
										2395 text You said:
									2396 container
										2397 text Global finite-mass Landau-Coulomb Cauchy theory  FULL QUESTION. Resolve global classical well-posedness of the spatially HOMOGENEOUS two-species Landau-Coulomb equation on R^3 for arbitrary positive finite particle masses and arbitrary smooth nonequilibrium data.  Fix ANY m_1,m_2>0 and c_ij=c_ji>0. Put a(z)=(I-z tensor z/|z|^2)/|z| and  Q_ij(f_i,f_j)(v)  = (c_ij/m_i) div_v integral a(v-w)      * [(f_j(w)/m_i)grad_v f_i(v)-(f_i(v)/m_j)grad_w f_j(w)]dw. The equation is partial_t f_i=sum\_(j=1,2)Q_ij(f_i,f_j).  For EVERY strictly positive Schwartz initial pair f_i^0, with n_i=integral f_i^0>0 and finite I_m(f^0)=sum_i m_i^-1 integral |grad f_i^0|^2/f_i^0, does the system have a unique global nonnegative classical solution, smooth for positive times and attaining f_i^0 at t=0 in the finite-mass/energy strong-solution class?  Prove finite-time a priori bounds sufficient for continuation for EVERY finite T, with their dependence on the actual masses, c_ij, n_i and initial norms specified. Preserve each n_i, total momentum sum_i m_i integral v f_i, total kinetic energy (1/2)sum_i m_i integral |v|^2 f_i and the entropy inequality. No near-equilibrium condition, symmetry, frozen or infinite-mass species, special mass ratio, artificial velocity cutoff or altered collision operator is assumed. A full affirmative must construct the whole Cauchy theory; a negative must give a genuine obstruction for admissible finite masses/data. A failed functional or conditional continuation criterion alone does not settle this question. Account for the actual hypotheses, errors and costs of any computation or approximation used; no solution, optimization or real-number oracle is provided.  The suggested papers and supplied premises are starting points, not a limit on your research. You may read them, seek additional papers, literature, available Astra work or other sources, change mathematical representations, introduce different ideas and methods, and challenge my framing while pursuing the full question. You choose your sources and approach without further permission.  New available mathematics, to use or bypass:  1. Your completed work has not resolved the full question. It establishes the exact conservation/entropy normalization, an explicit Fisher-to-weighted-L2 continuation estimate, and strictly FINITE positive masses/coefficients and strictly positive Schwartz data with I_m'(0)>0. The last construction selects a smooth angular seed, a fixed narrow Gaussian background and a finite sufficiently large second mass; it is a functional-growth example, not blowup. The separate pieces of a completed-square Fisher formula can diverge at zero relative velocity, so preserve their cancellation. The infinite-ion compensation theorem and the spherical cross threshold sqrt(8) do not supply an arbitrary finite-recoil estimate.  2. Your alternative heat-entropy functional has a complete continuation interface below one derivative. Define  P_tau^i=exp((tau/m_i)Delta), H(f)=integral f log f,  E_s=s(1-s)sum_i integral_0^infinity[H(f_i)-H(P_tau^i f_i)]tau^(-1-s)d tau. It obeys  E_s <= (3(n_1+n_2)/2)^(1-s) I_m^s/s,  E_s >= 2^s Gamma(2-s)sum_i m_i^-s||sqrt(f_i)||dotHs^2, and tensorizes on probability products. These are not collision-dissipation assertions.  For the FIXED s=7/8, a finite K=sup\_(t\<T)E\_(7/8)(f(t)) on any finite maximal classical interval is sufficient to restart the actual strong solution. Here is the quantitative bridge. Fractional Sobolev gives ||f_i||\_(12/5)<=C m_i^(7/8)K. Splitting the Coulomb potential into a ball and its complement and optimizing gives  |||.|^-1\*f_i||infinity<=C n_i^(3/7)m_i^(1/2)K^(4/7). Let M_q=sum_i m_i integral f_i\<v>^q. The exact symmetrized moment equation has a nonpositive drift contribution because b(z)=-2z/|z|^3 and \<v>^q is convex. The diffusion contribution then gives  M_q(t)<=M_q(0)exp(C_q K^(4/7)t), q>=2, with explicit C_q depending on q,m_i,c_ij,n_i. Convex radial truncations justify propagation without assuming it first. Holder gives  Y_7:=sum_i integral f_i^2\<v>^7  <= C(sum_i m_i^(17/14))K^(12/7)M_25(0)^(2/7)exp((2/7)C_25 K^(4/7)t). For each species the interpolation uses ||f_i||\_(12/5)^(12/7)(integral f_i\<v>^(49/2))^(2/7). Thus the local weighted-L2 theory applies with the physical n_i retained. In its probability formulation f_i=n_i g_i, weighting the i-th equation by n_i restores symmetric n_i n_j c_ij cross weights. The full question's Schwartz data supply M_25(0). In general the same direct bridge works for any s>3/4 with moment q>=14s/(4s-3). An s>1/2 fractional embedding alone is not this weighted-L2 bridge.  This criterion does NOT bound E\_(7/8) along collisions; a continuation norm's controlled growth could suffice without monotonicity. You need not use this functional.  3. The heat collision term has an exact score-preserving covariance representation. For a pair F=f_i(v)f_j(w), alpha=|v-w|^-3 and rotation field b_k(z)=e_k cross z, let  L=b_k(v-w).grad_v/m_i-b_k(v-w).grad_w/m_j, q=L log F,  P_tau=exp(tau(Delta_v/m_i+Delta_w/m_j)). L commutes with P_tau. The truncated-heat-time calculation gives  B_tau=integral alpha Fq^2-integral P_tau(alpha Fq)P_tau(Fq)/(P_tau F). If K_tau(y,x) is the pair Gaussian kernel, p_tau=P_tau F and mu_y(dx)=K_tau(y,x)F(x)dx/p_tau(y), then exactly  B_tau=integral p_tau(y)Cov\_(mu_y)(q,alpha q)dy. For independent x,x' under mu_y its covariance equals  (1/2)E[(sqrt(alpha)q-sqrt(alpha')q')^2]  -(1/2)E[(sqrt(alpha)-sqrt(alpha'))^2 q q']. This separates a positive square and a radial-coefficient commutator while retaining q=O(|v-w|). Alpha Fq and alpha Fq^2 are locally integrable; the bare posterior alpha average generally diverges and is not introduced. Generic covariance positivity is false: equal weights on (alpha,q)=(1,2),(4,1) give -1/2. That algebraic example is not a physical-product-score or full-functional counterexample. The posterior kernel is state-dependent, so a free convolution Hardy bound is not automatically available. Small/large auxiliary-heat limits and the required collision growth estimate remain unproved.  Optional primary starting points: Junne-Winter-Yoldas, [https://arxiv.org/html/2512.17082v1](https://arxiv.org/html/2512.17082v1), Lemma2.7 and its proof, Corollary2.8, Lemma2.9 and Section2.4 for the actual local-continuation interface; Zhu, [https://arxiv.org/html/2512.17905v1](https://arxiv.org/html/2512.17905v1), vector fields(2.3)-(2.5), Property(v) and Proposition2.2 for mass-weighted heat/rotation commutation and the unsplit derivative. Neither supplies the missing global finite-mass Coulomb bound. The full endpoint above remains the question, and the functional, representation and proof strategy remain yours.  you may use all subagents avaible
									2398 button (collapsed) Show more, Secondary Actions: Expand
										2399 text Show more
										2400 image
									2401 button Copy message
										2402 image
									2403 button Share prompt
									2404 button Edit message
										2405 image
									2406 button (expanded) Worked for 30m 25s, Secondary Actions: Collapse
										2407 text Worked for 30m 25s
										2408 image
									4331 text I’ll continue from the completed estimates and focus on proving a bound along the actual finite-mass evolution. I’ll use all three research branches: one for the heat–entropy collision term, one for direct continuation estimates, and one for alternative representations and relevant literature.
									4332 container Subagent activity
										4333 container
											4334 button Heat collision bound
											4335 text , 
											4336 button Direct cauchy routes
											4337 text  and 
											4338 button New representations
											4339 text  started working
									4340 text Prepared targeted fractional-Fisher searches
									4341 text Searched 30 websites
									4342 container Subagent activity
										4343 container
											4344 button New representations
											4345 text  updated
									4346 text Derived sharp scaling inequality and evaluated radial counterexample
									4347 text Checked posterior factorization and integrated q under μ
									4348 text Assembled the Bτ formula and rewrote the cross term
									4349 text Derived Coulomb heat identity and checked dissipation
									4350 text Compared heat-weighted covariance and assessed adaptive heat entropy
									4351 text Checked entropy control
									4352 text I found a 2026 paper on lifting nonlocal Fisher information that may offer another way to treat the collision term. I’m checking its exact hypotheses and operator, especially whether it applies to the singular Coulomb coefficient. A valid lifting construction alone would not give the evolution bound.
									4353 text Searching arxiv.org
									4354 text Checked entropy finiteness for full and truncated jumps Derived the heat commutator and tested Gaussian spectral coefficients Tested radial Hardy positivity and computed shifted-Gaussian Fisher information Tested radial perturbations and checked cutoff regularity Checked fractional energy and set up two-mode calculation Analyzed fractional Hardy bounds and radial D5 operator
									4355 container Subagent activity
										4356 container
											4357 button Heat collision bound
											4358 text  updated
									4359 text Bounded posterior covariance and integrated the middle term Checked B positivity and tested Gaussian-channel MMSE Tested label-information and Fisher bounds Defined a label-entropy bound and checked mutual-information control
									4360 container Subagent activity
										4361 container
											4362 button New representations
											4363 text  updated
									4364 text Checked matrix positivity and analyzed weighted composition Estimated transformed operator entries and Schur sum Searched radial counterexamples and compared shell scaling Assessed E_s monotonicity Analyzed small-scale heat control and estimated small-τ heat deficit Tested weighted Fisher interpolation Derived unequal-mass momentum form and bounded label-score Dirichlet Checked aggregate coercivity
									4365 container Subagent activity
										4366 container
											4367 button Direct cauchy routes
											4368 text  updated
									4369 text Searching arxiv.org
									4370 text Verified the covariance formula Checked covariance positivity Checked Gaussian functional derivative Derived the pair-gap coefficient Explored posterior covariance bounds Verified dyadic energy bounds There is a new estimate worth pursuing: entropy dissipation appears to give an unconditional bound on
									4371 container
										4372 text ∫
										4373 text 0
										4374 text 𝑇
										4375 text 𝐸
										4376 container
											4377 text 7 / 8
										4378 text ( 𝑓 ( 𝑡 )
										4379 text )
										4380 container
											4381 text 8 / 7
										4382 text 𝑑 𝑡
									4383 text , with the required velocity moments propagated from the data. This is weaker than the supremum bound needed for continuation. I’m checking the proof and whether the collision equation supplies enough control on growth to rule out a terminal spike.
									4384 container Subagent activity
										4385 container
											4386 button Direct cauchy routes
											4387 text , 
											4388 button Heat collision bound
											4389 text  and 
											4390 button New representations
											4391 text  updated
									4392 container
										4393 button (collapsed) Searched the web, Secondary Actions: Expand
										4394 text Searched the web
									4395 text Investigated subFisher and fractional Fisher monotonicity
									4396 text Checked heat semigroup contraction and derived covariance identity
									4397 container Subagent activity
										4398 container
											4399 button New representations
											4400 text  updated
									4401 text Investigated entropy compensation, dipole control, and Fisher monotonicity
									4402 text Prepared rigorous moment bounds and checked coercivity constants
									4403 text Derived nonlinear fractional entropy and tested energy monotonicity
									4404 text Searched 33 websites
									4405 text Audited entropy bounds and computed relative entropy
									4406 text Checked coercivity bounds and expanded the first term
									4407 text Checked moment-growth constants
									4408 text Verified convex radial truncations
									4409 text Audited dyadic mass factors
									4410 text Bound Fisher-energy integral
									4411 text Checked BKM integrability bounds
									4412 text Refined the scaling obstruction
									4413 text The moment and space–time estimates check out so far. They use the positive self-collision coefficients and total entropy dissipation, without a restriction on the mass ratio or the size of the cross coefficients. I also verified that negative posterior covariances can occur for genuine Gaussian product data, while their integral in the heat-collision formula remains positive for those same data. A pointwise sign argument therefore misses a real cancellation. Derived entropy bound using canonical Maxwellian reference Verified posterior covariance sign Derived the heat-kernel identity
									4414 container Subagent activity
										4415 container
											4416 button Direct cauchy routes
											4417 text  and 
											4418 button Heat collision bound
											4419 text  updated
									4420 text Analyzed operator-sign thresholds and checked Toeplitz sign structure Checked Schur-complement positivity and semigroup sectoriality
									4421 container Subagent activity
										4422 container
											4423 button Heat collision bound
											4424 text  updated
									4425 text Showed D/mass weak forms Derived polynomial moment bounds Checked ODE contradiction The available continuation estimates still leave a gap. The direct energy estimate requires an 
									4426 container
										4427 text 𝐿 𝑡
										4428 text 8
										4429 text /
										4430 text 3
									4431 text  bound on the relevant 
									4432 container
										4433 text 𝐿 𝑣
										4434 text 12
										4435 text /
										4436 text 5
									4437 text  norm; the new entropy argument gives only 
									4438 container
										4439 text 𝐿 𝑡
										4440 text 8
										4441 text /
										4442 text 7
									4443 text . Thus the space–time estimate does not yet rule out finite-time concentration. I’m finishing the checks on the new lemmas and will state exactly what they prove.
									4444 text Searching arxiv.org
									4445 container Subagent activity
										4446 container
											4447 button Heat collision bound
											4448 text  finished
									4449 text Derived the Coulomb operator and checked pair dissipation Checked local entropy inequality and specified constant dependence Derived the weighted bound Refined moment constants Assessed fractional-energy control and checked Gaussian error bounds
									4450 container Subagent activity
										4451 container
											4452 button Direct cauchy routes
											4453 text  finished
									4454 text Audited Gaussian pair derivatives and standardized energy notation Refined the entropy bound Defined entropy constants
									4455 text Searching arxiv.org
									4456 container Subagent activity
										4457 container
											4458 button New representations
											4459 text  finished
									4460 text Organized bounds and constants Defined φ_R and shifted φ_R test functions Justified moment estimates and clarified the weighted Fisher estimate Checked Gaussian entropy bound and relative-rotation noncommutation Clarified Gaussian entropy
									2409 heading ChatGPT said:, Value: 4
										2410 text ChatGPT said:
									2411 text I have not resolved the full global Cauchy problem.
									2412 text  I have neither a proof of global classical well-posedness for your entire class nor a genuine finite-mass obstruction. The additional estimates below therefore do 
									2413 text not
									2414 text  constitute an affirmative or negative answer. There is a further unconditional estimate that can be proved from the actual finite-mass equation:
									2415 container
										2416 text ∫
										2417 text 0
										2418 text 𝑇
										2419 text 𝐸
										2420 container
											2421 text 7 / 8
										2422 text ( 𝑓 ( 𝑡 )
										2423 text )
										2424 container
											2425 text 8 / 7
										2426 text 𝑑 𝑡 ≤
										2427 text 𝐶
										2428 text 𝑇
										2429 text .
									2430 text Here 
									2431 container
										2432 text 𝐶 𝑇
									2433 text  depends only on the fixed physical parameters and the initial particle numbers, energy, entropy and 
									2434 text 21
									2435 text -st velocity moment. The estimate does not assume bounded Fisher information or bounded 
									2436 container
										2437 text 𝐸
										2438 text 7
										2439 text /
										2440 text 8
									2441 text  along the evolution. I also obtain unconditional polynomial moment bounds and a uniform bound for the large auxiliary-heat-time part of 
									2442 container
										2443 text 𝐸 𝑠
									2444 text . The remaining gap is substantive: this time-integrated bound does not provide the supremum bound required by the continuation argument in your prompt. I will give the proofs, specify the dependencies, and then explain precisely why the continuation step remains open in this work.
									2445 heading 1. Setup and an unconditional weighted Fisher estimate, Value: 2
										2446 text 1. Setup and an unconditional weighted Fisher estimate
									2447 text Let 
									2448 container
										2449 text [ 0 ,
										2450 text 𝑇
										2451 text ∗
										2452 text )
									2453 text  be the maximal classical interval supplied by the local theory. Everything below concerns the actual collision operator in the question, with the physical densities 
									2454 container
										2455 text 𝑓 𝑖
									2456 text  and particle numbers 
									2457 container
										2458 text 𝑛 𝑖
									2459 text  retained. Write
									2460 container
										2461 text 𝐸
										2462 container
											2463 text k i n
										2464 text =
										2465 text 1
										2466 text 2
										2467 text ∑
										2468 text 𝑖
										2469 text 𝑚
										2470 text 𝑖
										2471 text ∫ ∣ 𝑣
										2472 text ∣
										2473 text 2
										2474 text 𝑓
										2475 text 𝑖
										2476 text 0
										2477 text ( 𝑣 ) 𝑑 𝑣 ,
										2478 text 𝐻
										2479 text 0
										2480 text =
										2481 text ∑
										2482 text 𝑖
										2483 text 𝐻 (
										2484 text 𝑓
										2485 text 𝑖
										2486 text 0
										2487 text ) ,
									2488 text and define
									2489 container
										2490 text 𝐷 ( 𝑡 ) =
										2491 text 1
										2492 text 2
										2493 text ∑
										2494 container
											2495 text 𝑖 , 𝑗
										2496 text 𝑐
										2497 container
											2498 text 𝑖 𝑗
										2499 text ∬
										2500 container
											2501 text 𝑓
											2502 text 𝑖
											2503 text ( 𝑣 )
											2504 text 𝑓
											2505 text 𝑗
											2506 text ( 𝑤 )
										2507 container
											2508 text ∣ 𝑣 − 𝑤 ∣
										2509 container
											2510 text ∣
											2511 text 𝑃
											2512 container
												2513 text 𝑣 − 𝑤
											2514 text (
											2515 container
												2516 text ∇
												2517 text log
												2518 text ⁡
												2519 container
													2520 text 𝑓 𝑖
												2521 text (
												2522 text 𝑣
												2523 text )
												2524 text 𝑚
												2525 text 𝑖
											2526 text −
											2527 container
												2528 text ∇
												2529 text log
												2530 text ⁡
												2531 container
													2532 text 𝑓 𝑗
												2533 text (
												2534 text 𝑤
												2535 text )
												2536 text 𝑚
												2537 text 𝑗
											2538 text )
											2539 text ∣
										2540 text 2
										2541 text 𝑑 𝑣 𝑑 𝑤 .
									2542 text Thus the entropy inequality on the classical interval reads
									2543 container
										2544 text 𝐻 ( 𝑓 ( 𝑡 ) ) +
										2545 text ∫
										2546 text 0
										2547 text 𝑡
										2548 text 𝐷 ( 𝑟 ) 𝑑 𝑟 ≤
										2549 text 𝐻
										2550 text 0
										2551 text .
									2552 text For a fixed reference pair, take
									2553 container
										2554 container
											2555 text 𝑀 ‾
										2556 text 𝑖
										2557 text ( 𝑣 ) =
										2558 text 𝑛
										2559 text 𝑖
										2560 container
											2561 text (
											2562 container
												2563 text 𝑚 𝑖
											2564 container
												2565 text 2 𝜋
											2566 text )
										2567 container
											2568 text 3 / 2
										2569 text 𝑒
										2570 container
											2571 text −
											2572 text 𝑚
											2573 text 𝑖
											2574 text ∣ 𝑣
											2575 text ∣
											2576 text 2
											2577 text / 2
										2578 text ,
									2579 text and put
									2580 container
										2581 text 𝐻
										2582 text 0
										2583 text =
										2584 text ∑
										2585 text 𝑖
										2586 text ∫
										2587 text 𝑓
										2588 text 𝑖
										2589 text 0
										2590 text log ⁡
										2591 container
											2592 text 𝑓 𝑖 0
										2593 container
											2594 text 𝑀
											2595 text ‾
											2596 text 𝑖
										2597 text .
									2598 text Because the reference logarithms involve only species masses and total kinetic energy,
									2599 container
										2600 container
											2601 text ∫
											2602 text 0
											2603 text 𝑡
											2604 text 𝐷 ( 𝑟 ) 𝑑 𝑟 ≤
											2605 text 𝐻
											2606 text 0
											2607 text ( 𝑡 <
											2608 text 𝑇
											2609 text ∗
											2610 text ) .
										2611 text (1)
									2612 text The reference pair need not have the initial momentum or temperature. Define
									2613 container
										2614 text 𝑊
										2615 text 𝑖
										2616 text ( 𝑡 ) =
										2617 text ∫
										2618 container
											2619 text 𝑅 3
										2620 text ⟨ 𝑣
										2621 text ⟩
										2622 container
											2623 text − 3
										2624 text ∣ ∇
										2625 container
											2626 text 𝑓
											2627 text 𝑖
											2628 text ( 𝑡 , 𝑣 )
										2629 text ∣
										2630 text 2
										2631 text 𝑑 𝑣 .
									2632 text The scalar Coulomb entropy-coercivity theorem gives
									2633 container
										2634 container
											2635 text 𝑊 ( ℎ ) ≤ 𝐶 ( 1 +
											2636 text 𝐷
											2637 text 0
											2638 text ( ℎ ) ) ,
										2639 text (2)
									2640 text where
									2641 container
										2642 text 𝐷
										2643 text 0
										2644 text ( ℎ ) =
										2645 text 1
										2646 text 2
										2647 text ∬
										2648 container
											2649 text ℎ ( 𝑣 ) ℎ ( 𝑤 )
										2650 container
											2651 text ∣ 𝑣 − 𝑤 ∣
										2652 container
											2653 text ∣
											2654 text 𝑃
											2655 container
												2656 text 𝑣 − 𝑤
											2657 text ( ∇ log ⁡ ℎ ( 𝑣 ) − ∇ log ⁡ ℎ ( 𝑤 ) ) ∣
										2658 text 2
										2659 text 𝑑 𝑣 𝑑 𝑤 .
									2660 text Its constant depends on mass, momentum, energy and an upper bound for absolute entropy. This is the precise weighted estimate in Desvillettes’ Theorem 1. 
									2661 link (collapsed) Value: arxiv.org/html/1408.6025v2?utm_source=chatgpt.com, Secondary Actions: Expand, Description: arxiv.org: Entropy dissipation estimatesfor the Landau equationin the Coulomb case and applications, https://arxiv.org/html/1408.6025v2?utm_source=chatgpt.com
									2662 heading Making its constants uniform for each species, Value: 3
										2663 text Making its constants uniform for each species
									2664 text This application requires some care: individual species energies, momenta and entropies are not conserved. Set
									2665 container
										2666 text 𝐵
										2667 text 𝑖
										2668 text =
										2669 container
											2670 text 2
											2671 text 𝐸
											2672 container
												2673 text k i n
										2674 container
											2675 text 𝑚 𝑖
										2676 text .
									2677 text Then
									2678 container
										2679 text ∫ ∣ 𝑣
										2680 text ∣
										2681 text 2
										2682 text 𝑓
										2683 text 𝑖
										2684 text ( 𝑡 , 𝑣 ) 𝑑 𝑣 ≤
										2685 text 𝐵
										2686 text 𝑖
										2687 text .
									2688 text Relative entropy against 
									2689 container
										2690 text 𝑛 𝑖
									2691 text  times the standard Gaussian gives
									2692 container
										2693 text 𝐻 (
										2694 text 𝑓
										2695 text 𝑖
										2696 text ( 𝑡 ) ) ≥
										2697 text 𝐿
										2698 text 𝑖
										2699 text : =
										2700 text 𝑛
										2701 text 𝑖
										2702 text log ⁡
										2703 text 𝑛
										2704 text 𝑖
										2705 text −
										2706 container
											2707 text 3
											2708 text 𝑛
											2709 text 𝑖
										2710 text 2
										2711 text log ⁡ ( 2 𝜋 ) −
										2712 container
											2713 text 𝐵 𝑖
										2714 text 2
										2715 text .
									2716 text Consequently,
									2717 container
										2718 container
											2719 text 𝐻 (
											2720 text 𝑓
											2721 text 𝑖
											2722 text ( 𝑡 ) ) ≤
											2723 text 𝑈
											2724 text 𝑖
											2725 text : =
											2726 text 𝐻
											2727 text 0
											2728 text −
											2729 text 𝐿
											2730 text 𝑗
											2731 text , 𝑗 ≠ 𝑖 .
										2732 text (3)
									2733 text The elementary inequality
									2734 container
										2735 text 𝑥 log ⁡ ( 1 / 𝑥 ) ≤ ∣ 𝑣
										2736 text ∣
										2737 text 2
										2738 text 𝑥 +
										2739 text 𝑒
										2740 container
											2741 text − 1 − ∣ 𝑣
											2742 text ∣
											2743 text 2
									2744 text also gives
									2745 container
										2746 container
											2747 text ∫
											2748 text 𝑓
											2749 text 𝑖
											2750 text ( 𝑡 ) ∣ log ⁡
											2751 text 𝑓
											2752 text 𝑖
											2753 text ( 𝑡 ) ∣ ≤
											2754 text 𝑈
											2755 text 𝑖
											2756 text + 2
											2757 text 𝐵
											2758 text 𝑖
											2759 text + 2
											2760 text 𝑒
											2761 container
												2762 text − 1
											2763 text 𝜋
											2764 container
												2765 text 3 / 2
											2766 text .
										2767 text (4)
									2768 text To check that normalization in (2) cannot degenerate, let
									2769 container
										2770 text 𝑢
										2771 text 𝑖
										2772 text ( 𝑡 ) =
										2773 text 1
										2774 container
											2775 text 𝑛 𝑖
										2776 text ∫ 𝑣
										2777 text 𝑓
										2778 text 𝑖
										2779 text ( 𝑡 , 𝑣 ) 𝑑 𝑣 , 3
										2780 text 𝑛
										2781 text 𝑖
										2782 text 𝜎
										2783 text 𝑖
										2784 text ( 𝑡
										2785 text )
										2786 text 2
										2787 text = ∫ ∣ 𝑣 −
										2788 text 𝑢
										2789 text 𝑖
										2790 text ( 𝑡 )
										2791 text ∣
										2792 text 2
										2793 text 𝑓
										2794 text 𝑖
										2795 text ( 𝑡 , 𝑣 ) 𝑑 𝑣 .
									2796 text Then
									2797 container
										2798 text ∣
										2799 text 𝑢
										2800 text 𝑖
										2801 text ( 𝑡 )
										2802 text ∣
										2803 text 2
										2804 text ≤
										2805 container
											2806 text 𝐵 𝑖
										2807 container
											2808 text 𝑛 𝑖
										2809 text ,
										2810 text 𝜎
										2811 text 𝑖
										2812 text ( 𝑡
										2813 text )
										2814 text 2
										2815 text ≤
										2816 container
											2817 text 𝐵 𝑖
										2818 container
											2819 text 3
											2820 text 𝑛
											2821 text 𝑖
										2822 text .
									2823 text The Gaussian entropy bound, together with (3), supplies the positive lower bound
									2824 container
										2825 container
											2826 text 𝜎
											2827 text 𝑖
											2828 text ( 𝑡
											2829 text )
											2830 text 2
											2831 text ≥
											2832 text 1
											2833 container
												2834 text 2 𝜋 𝑒
											2835 text exp ⁡  ⁣
											2836 text [
											2837 container
												2838 text 2 3
											2839 container
												2840 text ( log ⁡
												2841 text 𝑛
												2842 text 𝑖
												2843 text −
												2844 container
													2845 text 𝑈 𝑖
												2846 container
													2847 text 𝑛 𝑖
												2848 text )
											2849 text ]
											2850 text .
										2851 text (5)
									2852 text Thus translating and rescaling to unit mass, zero mean and normalized variance uses uniformly bounded, nondegenerate parameters. Equations (3)–(5) specify the data controlling the normalized absolute entropy as well. It follows that
									2853 container
										2854 text 𝑊
										2855 text 𝑖
										2856 text ( 𝑡 ) ≤
										2857 text 𝐶
										2858 text 𝑖
										2859 text ( 1 +
										2860 text 𝐷
										2861 text 0
										2862 text (
										2863 text 𝑓
										2864 text 𝑖
										2865 text ( 𝑡 ) ) ) ,
									2866 text with fixed
									2867 container
										2868 text 𝐶
										2869 text 𝑖
										2870 text =
										2871 text 𝐶
										2872 text 𝑖
										2873 text (
										2874 text 𝑛
										2875 text 1
										2876 text ,
										2877 text 𝑛
										2878 text 2
										2879 text ,
										2880 text 𝑚
										2881 text 1
										2882 text ,
										2883 text 𝑚
										2884 text 2
										2885 text ,
										2886 text 𝐸
										2887 container
											2888 text k i n
										2889 text ,
										2890 text 𝐻
										2891 text 0
										2892 text ) .
									2893 text The self-collision contribution to 
									2894 text 𝐷
									2895 text  is exactly
									2896 container
										2897 container
											2898 text 𝑐
											2899 text 𝑖
											2900 text 𝑖
										2901 container
											2902 text 𝑚 𝑖 2
										2903 text 𝐷
										2904 text 0
										2905 text (
										2906 text 𝑓
										2907 text 𝑖
										2908 text ) .
									2909 text Every other pair contribution is nonnegative. Therefore, with
									2910 container
										2911 text 𝐾
										2912 text 𝑖
										2913 text =
										2914 text 𝐶
										2915 text 𝑖
										2916 text max ⁡
										2917 text {
										2918 text 1
										2919 text ,
										2920 container
											2921 text 𝑚
											2922 text 𝑖
											2923 text 2
											2924 text 𝑐
											2925 container
												2926 text 𝑖 𝑖
										2927 text }
										2928 text ,
									2929 text we have
									2930 container
										2931 container
											2932 text 𝑊
											2933 text 𝑖
											2934 text ( 𝑡 ) ≤
											2935 text 𝐾
											2936 text 𝑖
											2937 text ( 1 + 𝐷 ( 𝑡 ) ) .
										2938 text (6)
									2939 text In particular,
									2940 container
										2941 container
											2942 text ∫
											2943 text 0
											2944 text 𝑡
											2945 text 𝑊
											2946 text 𝑖
											2947 text ( 𝑟 ) 𝑑 𝑟 ≤
											2948 text 𝐾
											2949 text 𝑖
											2950 text ( 𝑡 +
											2951 text 𝐻
											2952 text 0
											2953 text ) .
										2954 text (7)
									2955 text This uses only the strict positivity of 
									2956 container
										2957 text 𝑐
										2958 text 𝑖
										2959 text 𝑖
									2960 text . It imposes no relation between self-collision and cross-collision strengths.
									2961 heading 2. Unconditional propagation of polynomial moments, Value: 2
										2962 text 2. Unconditional propagation of polynomial moments
									2963 text The weighted Fisher control gives a useful pointwise bound on the Coulomb potential. Let
									2964 container
										2965 text 𝑈
										2966 text 𝑗
										2967 text ( 𝑣 ) = ∫
										2968 container
											2969 text 𝑓
											2970 text 𝑗
											2971 text ( 𝑤 )
										2972 container
											2973 text ∣ 𝑣 − 𝑤 ∣
										2974 text 𝑑 𝑤 .
									2975 text Applying Sobolev to 
									2976 container
										2977 text ⟨ 𝑣
										2978 text ⟩
										2979 container
											2980 text − 3 / 2
										2981 container
											2982 text 𝑓 𝑗
									2983 text  yields
									2984 container
										2985 container
											2986 text ∥
											2987 text 𝑓
											2988 text 𝑗
											2989 text ⟨ ⋅
											2990 text ⟩
											2991 container
												2992 text − 3
											2993 text ∥
											2994 container
												2995 text 𝐿 3
											2996 text ≤ 𝐶 (
											2997 text 𝑊
											2998 text 𝑗
											2999 text +
											3000 text 𝑛
											3001 text 𝑗
											3002 text ) .
										3003 text (8)
									3004 text Put 
									3005 container
										3006 text 𝐿 = ⟨ 𝑣 ⟩
									3007 text . For 
									3008 container
										3009 text 0 < 𝑅 ≤ 𝐿 / 2
									3010 text , the weights 
									3011 container
										3012 text ⟨ 𝑤 ⟩
									3013 text  and 
									3014 text 𝐿
									3015 text  are comparable on 
									3016 container
										3017 text ∣ 𝑣 − 𝑤 ∣ < 𝑅
									3018 text . Hölder’s inequality, followed by the elementary far-field estimate, gives
									3019 container
										3020 text 𝑈
										3021 text 𝑗
										3022 text ( 𝑣 ) ≤ 𝐶
										3023 text 𝐿
										3024 text 3
										3025 text 𝑅 (
										3026 text 𝑊
										3027 text 𝑗
										3028 text +
										3029 text 𝑛
										3030 text 𝑗
										3031 text ) +
										3032 container
											3033 text 𝑛 𝑗
										3034 text 𝑅
										3035 text .
									3036 text Optimizing 
									3037 text 𝑅
									3038 text , with the restriction 
									3039 container
										3040 text 𝑅 ≤ 𝐿 / 2
									3041 text , gives
									3042 container
										3043 text 𝑈
										3044 text 𝑗
										3045 text ( 𝑣 ) ≤ 𝐶
										3046 text 𝐿
										3047 container
											3048 text 3 / 2
										3049 container
											3050 text 𝑛
											3051 text 𝑗
											3052 text (
											3053 text 𝑊
											3054 text 𝑗
											3055 text +
											3056 text 𝑛
											3057 text 𝑗
											3058 text )
										3059 text .
									3060 text Using (6), define
									3061 container
										3062 text 𝑎
										3063 text 𝑗
										3064 text = 𝐶
										3065 container
											3066 text 𝑛
											3067 text 𝑗
											3068 text (
											3069 text 𝐾
											3070 text 𝑗
											3071 text +
											3072 text 𝑛
											3073 text 𝑗
											3074 text )
									3075 text so that
									3076 container
										3077 container
											3078 text 𝑈
											3079 text 𝑗
											3080 text ( 𝑣 ) ≤
											3081 text 𝑎
											3082 text 𝑗
											3083 text ⟨ 𝑣
											3084 text ⟩
											3085 container
												3086 text 3 / 2
											3087 container
												3088 text 1 + 𝐷 ( 𝑡 )
											3089 text .
										3090 text (9)
									3091 heading The exact moment identity and its sign, Value: 3
										3092 text The exact moment identity and its sign
									3093 text For a common convex test function 
									3094 text 𝜙
									3095 text , integration by parts gives
									3096 container
										3097 container
											3098 container
												3099 text 𝑑
												3100 container
													3101 text 𝑑 𝑡
												3102 text ∑
												3103 text 𝑖
												3104 text 𝑚
												3105 text 𝑖
												3106 text ∫
												3107 text 𝑓
												3108 text 𝑖
												3109 text 𝜙 =
											3110 container
												3111 text ∑
												3112 container
													3113 text 𝑖 , 𝑗
												3114 container
													3115 text 𝑐
													3116 text 𝑖
													3117 text 𝑗
												3118 container
													3119 text 𝑚 𝑖
												3120 text ∬
												3121 text 𝑓
												3122 text 𝑖
												3123 text ( 𝑣 )
												3124 text 𝑓
												3125 text 𝑗
												3126 text ( 𝑤 ) 𝑎 ( 𝑣 − 𝑤 ) :
												3127 text 𝐷
												3128 text 2
												3129 text 𝜙 ( 𝑣 ) 𝑑 𝑣 𝑑 𝑤
											3130 container
												3131 text +
												3132 text 1
												3133 text 2
												3134 text ∑
												3135 container
													3136 text 𝑖 , 𝑗
												3137 text 𝑐
												3138 container
													3139 text 𝑖 𝑗
												3140 text (
												3141 container
													3142 text 1
													3143 text 𝑚
													3144 text 𝑖
												3145 text +
												3146 container
													3147 text 1
													3148 text 𝑚
													3149 text 𝑗
												3150 text )
												3151 text ∬
												3152 text 𝑓
												3153 text 𝑖
												3154 text ( 𝑣 )
												3155 text 𝑓
												3156 text 𝑗
												3157 text ( 𝑤 ) 𝑏 ( 𝑣 − 𝑤 ) ⋅ [ ∇ 𝜙 ( 𝑣 ) − ∇ 𝜙 ( 𝑤 ) ] 𝑑 𝑣 𝑑 𝑤 ,
										3158 text (10)
									3159 text where
									3160 container
										3161 text 𝑏 ( 𝑧 ) = −
										3162 container
											3163 text 2 𝑧
										3164 container
											3165 text ∣ 𝑧
											3166 text ∣
											3167 text 3
										3168 text .
									3169 text Convexity makes the second line nonpositive. For
									3170 container
										3171 text 𝑀
										3172 text 𝑞
										3173 text ( 𝑡 ) =
										3174 text ∑
										3175 text 𝑖
										3176 text 𝑚
										3177 text 𝑖
										3178 text ∫
										3179 text 𝑓
										3180 text 𝑖
										3181 text ( 𝑡 , 𝑣 ) ⟨ 𝑣
										3182 text ⟩
										3183 text 𝑞
										3184 text 𝑑 𝑣 , 𝑞 ≥ 2 ,
									3185 text we have
									3186 container
										3187 text 𝐷
										3188 text 2
										3189 text ⟨ 𝑣
										3190 text ⟩
										3191 text 𝑞
										3192 text ≤ 𝑞 ( 𝑞 − 1 ) ⟨ 𝑣
										3193 text ⟩
										3194 container
											3195 text 𝑞 − 2
										3196 text 𝐼 .
									3197 text Since 
									3198 container
										3199 text tr ⁡ 𝑎 ( 𝑧 ) = 2 / ∣ 𝑧 ∣
									3200 text , (9)–(10) give
									3201 container
										3202 container
											3203 text 𝑀
											3204 text 𝑞
											3205 text ′
											3206 text ( 𝑡 ) ≤
											3207 text 𝜅
											3208 text 𝑞
											3209 container
												3210 text 1 + 𝐷 ( 𝑡 )
											3211 text 𝑀
											3212 container
												3213 text 𝑞 − 1 / 2
											3214 text ( 𝑡 ) ,
										3215 text (11)
									3216 text where one may take
									3217 container
										3218 container
											3219 text 𝜅
											3220 text 𝑞
											3221 text = 2 𝑞 ( 𝑞 − 1 )
											3222 container
												3223 text max ⁡
											3224 text 𝑖
											3225 text {
											3226 container
												3227 text 1
												3228 text 𝑚
												3229 text 𝑖
												3230 text 2
											3231 container
												3232 text ∑ 𝑗
											3233 container
												3234 text 𝑐
												3235 text 𝑖
												3236 text 𝑗
											3237 container
												3238 text 𝑎 𝑗
											3239 text }
											3240 text .
										3241 text (12)
									3242 heading Justifying propagation before assuming the moment is finite, Value: 3
										3243 text Justifying propagation before assuming the moment is finite
									3244 text For 
									3245 container
										3246 text 𝑅 > 2
									3247 text , define
									3248 container
										3249 text ℎ
										3250 text 𝑅
										3251 text ( 𝑠 ) =
										3252 text {
										3253 container
											3254 container
												3255 text 𝑠
												3256 text 𝑞
												3257 text ,
											3258 container
												3259 text 𝑠 ≤ 𝑅 ,
											3260 container
												3261 text 𝑞
												3262 text 𝑅
												3263 container
													3264 text 𝑞 − 1
												3265 text 𝑠 − ( 𝑞 − 1 )
												3266 text 𝑅
												3267 text 𝑞
												3268 text ,
											3269 container
												3270 text 𝑠 > 𝑅 ,
										3271 text 𝜙
										3272 text 𝑅
										3273 text ( 𝑣 ) =
										3274 text ℎ
										3275 text 𝑅
										3276 text ( ⟨ 𝑣 ⟩ ) .
									3277 text These functions are convex, increase to 
									3278 container
										3279 text ⟨ 𝑣
										3280 text ⟩
										3281 text 𝑞
									3282 text , and grow only linearly at infinity. Their Hessians satisfy, almost everywhere,
									3283 container
										3284 container
											3285 text 0 ≤
											3286 text 𝐷
											3287 text 2
											3288 text 𝜙
											3289 text 𝑅
											3290 text ( 𝑣 ) ≤
											3291 text 𝐶
											3292 text 𝑞
											3293 text 𝜙
											3294 text 𝑅
											3295 text ( 𝑣 ) ⟨ 𝑣
											3296 text ⟩
											3297 container
												3298 text − 2
											3299 text 𝐼 ,
										3300 text (13)
									3301 text uniformly in 
									3302 text 𝑅
									3303 text . Smooth convex approximations preserve this bound up to a fixed factor. The drift in (10) therefore retains its nonpositive sign for these truncated test functions. Equations (9) and (13) give a Gronwall estimate for the truncated moment with a constant independent of 
									3304 text 𝑅
									3305 text . Monotone convergence then establishes moment propagation. Thus using (11) afterwards is not circular. For a sharper bound, suppose 
									3306 container
										3307 text 𝑞 > 5 / 2
									3308 text , and put
									3309 container
										3310 text 𝜗
										3311 text 𝑞
										3312 text =
										3313 text 1
										3314 container
											3315 text 2 ( 𝑞 − 2 )
										3316 text .
									3317 text Interpolation against the conserved quantity
									3318 container
										3319 text 𝑀
										3320 text 2
										3321 text =
										3322 text ∑
										3323 text 𝑖
										3324 text 𝑚
										3325 text 𝑖
										3326 text 𝑛
										3327 text 𝑖
										3328 text + 2
										3329 text 𝐸
										3330 container
											3331 text k i n
									3332 text gives
									3333 container
										3334 text 𝑀
										3335 container
											3336 text 𝑞 − 1 / 2
										3337 text ≤
										3338 text 𝑀
										3339 text 2
										3340 container
											3341 text 𝜗 𝑞
										3342 text 𝑀
										3343 text 𝑞
										3344 container
											3345 text 1 −
											3346 text 𝜗
											3347 text 𝑞
										3348 text .
									3349 text Integrating (11), using (1) and Cauchy–Schwarz in time, yields
									3350 container
										3351 container
											3352 text 𝑀
											3353 text 𝑞
											3354 text ( 𝑡 ) ≤
											3355 text 𝑅
											3356 text 𝑞
											3357 text ( 𝑡 ) : =
											3358 container
												3359 text [
												3360 text 𝑀
												3361 text 𝑞
												3362 text ( 0
												3363 text )
												3364 container
													3365 text 𝜗 𝑞
												3366 text +
												3367 text 𝜅
												3368 text 𝑞
												3369 text 𝜗
												3370 text 𝑞
												3371 text 𝑀
												3372 text 2
												3373 container
													3374 text 𝜗 𝑞
												3375 container
													3376 text 𝑡 ( 𝑡 +
													3377 text 𝐻
													3378 text 0
													3379 text )
												3380 text ]
											3381 container
												3382 text 1 /
												3383 text 𝜗
												3384 text 𝑞
											3385 text .
										3386 text (14)
									3387 text For the moment needed below, 
									3388 container
										3389 text 𝑞 = 21
									3390 text  and 
									3391 container
										3392 text 𝜗
										3393 text 21
										3394 text = 1 / 38
									3395 text . The bound remains finite as 
									3396 text 𝑡
									3397 text  approaches any finite maximal endpoint.
							4306 container
								4307 text ChatGPT can make mistakes. Check important info.
							4308 container
								4309 button Scroll to bottom
								4310 heading Latest response, Value: 4
									4311 text Latest response
								4312 container
									4313 container
										4314 button (collapsed) Description: Add files and more, Secondary Actions: Expand
										4315 text entry area (settable) Description: Ask ChatGPT, Value: 

											4316 container
												4461 text Ask ChatGPT
										4318 pop up button (collapsed) Description: Select ChatGPT model, ID: radix-_r_51_, Secondary Actions: Expand
											4319 text Pro
										4320 button Dictate
										4321 button Start Voice
						4322 container
							4323 heading Activity, Value: 3
								4324 text Activity
							4325 button 6 used
								4326 text Subagents
								4327 text 6 used
							4328 button (expanded) Outputs, Secondary Actions: Collapse
							4329 text No outputs yet
		4330 text Response complete

The focused UI element is 2406 button (expanded) Worked for 30m 25s, Secondary Actions: Collapse
```
