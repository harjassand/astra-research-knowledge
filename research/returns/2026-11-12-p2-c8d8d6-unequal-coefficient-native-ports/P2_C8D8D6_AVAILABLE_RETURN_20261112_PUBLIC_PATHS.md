**I still do not have a complete affirmative architecture or an obstruction covering every allowed architecture.** The added interfaces do support further progress, though: the equal-diffusivity restriction in item 7 can be removed, and the resulting kernel gives an exact observable estimate for the full nonlinear weak equations.

The main advances from this round are:

| Component | Result established here |
|---|---|
| Linear magnetic/velocity response | One deterministic, summable port-response kernel for independently varying \(\nu,\rho\), uniformly in capacity |
| Full nonlinear weak evolution | A stress-to-port identity and estimate using the same summable kernel, with the Leray projector eliminated at the chosen ports |
| Probability interface | The weighted Poisson estimate extends to predictable weights with pathwise row and column budgets |
| Polynomial count amplification | Higher fixed moment cancellation can accommodate certain fixed-degree polynomial damage bounds |
| Canonical local reshaping | An explicit auxiliary scalar update restores arbitrary cell words to fixed bump profiles with quadratic error reduction |
| Native MHD implementation and uniform nonlinear energy | Still unproved |

The distinction in the second row matters: the nonlinear estimate contains **actual local field errors**, and I cannot yet bound those errors by fault counts while maintaining the native processor. Below are the derivations and the remaining boundary.

## 1. Independently varying viscosity and resistivity admit summable linear port weights

Write \(b=B-e_1\). Consider the linear comparison system
\[
u_t=\nu(t)\Delta u+\partial_1b,
\qquad
b_t=\rho(t)\Delta b+\partial_1u.
\tag{1}
\]
A common prescribed force cancels when comparing two solutions of this linear system.

Let
\[
w_+=u+b,\qquad w_-=u-b,
\]
and put
\[
\chi(t)=\frac{\nu(t)+\rho(t)}2,
\qquad
\delta(t)=\frac{\nu(t)-\rho(t)}2.
\]
Then
\[
\partial_t
\begin{pmatrix}w_+\\w_-\end{pmatrix}
=
\chi(t)\Delta
\begin{pmatrix}w_+\\w_-\end{pmatrix}
+
\begin{pmatrix}\partial_1&0\\0&-\partial_1\end{pmatrix}
\begin{pmatrix}w_+\\w_-\end{pmatrix}
+
\delta(t)\Delta
\begin{pmatrix}w_-\\w_+\end{pmatrix}.
\tag{2}
\]

For \(h=t-s\), define
\[
A=\int_s^t\chi(r)\,dr.
\]
The coefficient assumptions give
\[
(1-\zeta)h\le A\le(1+\zeta)h,
\qquad |\delta(r)|\le\zeta.
\tag{3}
\]

### 1.1 Expanding only the unequal-diffusivity part

The scalar heat evolution commutes with all the other spatial operators in (2). Expand the off-diagonal term \(\delta(t)\Delta\) in a time-ordered series.

For either starting Elsasser sign, the \(n\)-th term contains:

- \(n\) sign flips;
- \(\prod_{\ell=1}^n\delta(t_\ell)\);
- \(\Delta^nH_A\), where \(H_A\) is the scalar heat kernel;
- translation along an alternating \(+e_1,-e_1\) path.

There is no exponentially branching family of signs: after the starting sign is fixed, every flip is determined.

After writing
\[
t_\ell=s+hr_\ell,\qquad
0<r_1<\cdots<r_n<1,
\]
the translation is
\[
h\beta_n(r_1,\ldots,r_n)e_1,
\qquad |\beta_n|\le1.
\tag{4}
\]

The useful estimate is obtained from analyticity of the heat kernel in its heat-time variable. On the complex circle \(|z-A|=A/2\), the real part of \(z\) remains positive. Cauchy’s formula therefore gives, for each fixed spatial derivative order \(r\),
\[
|D^r\Delta^nH_A(x)|
\le
C_r\,n!\left(\frac2A\right)^n
A^{-(3+r)/2}
\exp\!\left(-\frac{|x|^2}{C_rA}\right).
\tag{5}
\]
The constant \(C_r\) is independent of \(n\). All dependence on \(n\) is displayed.

The ordered time simplex has volume \(h^n/n!\). Consequently its factorial cancels the factorial in (5), leaving the geometric factor
\[
\left(\frac{2\zeta h}{A}\right)^n
\le
\omega^n,
\qquad
\omega=\frac{2\zeta}{1-\zeta}<\frac23.
\tag{6}
\]

This yields a positive Gaussian-mixture majorant with bounded total mass, uniformly over all elapsed times. The argument actually needs only bounded measurable coefficient histories satisfying (3); the stated Lipschitz condition is more than enough.

### 1.2 An explicit majorant without an infinite mixture

The mixture can be simplified.

Under normalized Lebesgue measure on the ordered time simplex, the \(n+1\) time gaps have a uniform Dirichlet distribution. For \(n\ge1\), the fraction \(U\) of time spent with positive transport velocity has a beta distribution
\[
U\sim\operatorname{Beta}(r_+,r_-),
\qquad r_++r_-=n+1.
\]
Both parameters are positive integers. Its density satisfies
\[
f_U(v)
=
n\binom{n-1}{r_+-1}
v^{r_+-1}(1-v)^{r_--1}
\le n.
\tag{7}
\]
Thus the displacement parameter \(\beta=2U-1\) has density at most \(n/2\).

Summing the geometric weights uses
\[
\sum_{n\ge1}n\omega^n=\frac{\omega}{(1-\omega)^2}.
\]
The entire mixture is therefore dominated by two endpoint masses, at translations \(\pm he_1\), together with a bounded density over the segment \([-h,h]e_1\).

For \(h\ge1\), this gives the explicit derivative-kernel bound
\[
\begin{aligned}
C_rh^{-(3+r)/2}\Bigg[
&e^{-|x-he_1|^2/(C_rh)}
+e^{-|x+he_1|^2/(C_rh)}\\
&+\frac1h\int_{-h}^{h}
e^{-|x-ve_1|^2/(C_rh)}\,dv
\Bigg].
\end{aligned}
\tag{8}
\]
The smeared term obeys
\[
\frac1h\int_{-h}^{h}
e^{-|x-ve_1|^2/(Ch)}\,dv
\le
Ch^{-1/2}
e^{-\operatorname{dist}(x,[-h,h]e_1)^2/(C'h)}.
\tag{9}
\]

After pairing with fixed smooth ports and compact sources, short times can also be included. A convenient response envelope is
\[
\begin{aligned}
\mathsf K_r(h,x)
={}&C_r(1+h)^{-(3+r)/2}
\Bigg[
e^{-|x-he_1|^2/[C_r(1+h)]}\\
&\quad+
e^{-|x+he_1|^2/[C_r(1+h)]}\\
&\quad+
(1+h)^{-1/2}
e^{-\operatorname{dist}(x,[-h,h]e_1)^2/[C_r(1+h)]}
\Bigg].
\end{aligned}
\tag{10}
\]
For short times, the constants also include the fixed support sizes and port norms. Equation (10) is a bound on the integrated port responses; it does not assert that an unpaired heat-kernel derivative stays bounded as \(h\downarrow0\).

All constants in (10) can be bounded independently of the actual histories \(\nu,\rho\).

### 1.3 Spatial summation retains the needed time decay

Periodize (10) on the actual torus:
\[
\mathsf K_{r,M}(h,x)
=
\sum_{\ell\in\mathbb Z^3}
\mathsf K_r(h,x+aM\ell).
\tag{11}
\]

The endpoint Gaussians have spatial lattice sums of order \((1+h)^{3/2}\). The Gaussian tube around \([-h,h]e_1\) has length of order \(1+h\) and transverse widths of order \(\sqrt{1+h}\), so its lattice sum is of order \((1+h)^2\). The additional factor \((1+h)^{-1/2}\) in (10) makes both contributions satisfy
\[
\sup_i\sum_j
\mathsf K_{r,M}(h,a(i-j))
\le C(1+h)^{-r/2}.
\tag{12}
\]
The same estimate holds for column sums.

For \(r=3\),
\[
\boxed{
\sup_i\sum_j
\mathsf K_{3,M}(h,a(i-j))
\le C(1+h)^{-3/2}.
}
\tag{13}
\]
This is integrable in time, uniformly in \(M\).

Keeping the distribution of translations is essential. Taking a supremum over the entire ballistic segment before summing spatial cells discards the factor in (9) and can leave a borderline time estimate.

### 1.4 The specified ports provide three derivatives

Take a fixed compact solenoidal port
\[
\phi=\partial_1\operatorname{curl}A.
\]
It satisfies, componentwise,
\[
\int\phi=0,
\qquad
\int x_j\phi(x)\,dx=0.
\tag{14}
\]
An admitted kick has
\[
\int\xi=0.
\tag{15}
\]

The two port cancellations and the one kick cancellation allow a third-order Taylor remainder estimate for the convolution kernel. Thus, for a velocity or magnetic port in cell \(i\), and a kick in cell \(j\),
\[
\left|
\left\langle
\phi_i,[S(t,s)(\xi_u,\xi_B)]_\bullet
\right\rangle
\right|
\le
CK_0\,\mathsf K_{3,M}(t-s,a(i-j)).
\tag{16}
\]
Here \(S(t,s)\) is the propagator of (1), and \(\bullet\) selects the observed component. No compact vector potential for the kick is required.

For a fault whose time lies in a cell-period box, take the supremum over that time. The corresponding age changes by at most \(T\); the endpoint centers move by at most \(T\), and the ballistic segments are nested. Fixed enlargements of the Gaussian constants absorb this supremum.

Consequently there are deterministic clock-box weights \(w(a,z)\), independent of the coefficient histories, with
\[
|\text{linear port fault response at }a|
\le \sum_z w(a,z)N_z,
\tag{17}
\]
and
\[
\boxed{
\sup_a\sum_z w(a,z)\le W,
\qquad
\sup_z\sum_a w(a,z)\le W,
}
\tag{18}
\]
for a fixed computably bounded \(W\), uniformly in capacity.

The preparation perturbation also has a uniform linear port bound:
\[
\sup_i
\left|
\left\langle
\phi_i,[S(t,0)e_0]_\bullet
\right\rangle
\right|
\le C\gamma
\tag{19}
\]
when \(\sup_j\|e_0\|_{H^1(Q_j)}\le\gamma\). No cellwise mean-zero condition on \(e_0\) is needed.

This completes the unequal-coefficient **linear** extension of your item 7.

## 2. The same kernel gives an exact full nonlinear weak port estimate

The preceding propagator can be used as a test-function device inside the actual nonlinear system. It does not replace the driven nonlinear evolution.

Write \(z=(u,b)\), and use
\[
(\operatorname{div}R)_i=\partial_jR_{ij}.
\]
Define
\[
R_u(z)=u\otimes u-b\otimes b,
\qquad
R_b(z)=b\otimes u-u\otimes b.
\tag{20}
\]
The equations become
\[
z_t=L(t)z-
\begin{pmatrix}
\mathbb P\operatorname{div}R_u(z)\\
\operatorname{div}R_b(z)
\end{pmatrix}
+
\begin{pmatrix}f_*\\0\end{pmatrix}.
\tag{21}
\]

Choose a port
\[
\Phi_i=(\phi_i,0)
\quad\text{or}\quad
\Phi_i=(0,\phi_i).
\]
Every component of the backward test
\[
S(t,s)^*\Phi_i
\]
is solenoidal: each block of \(S\) is a scalar spatial convolution operator, and hence commutes with divergence.

It follows that
\[
\left\langle
[S(t,s)^*\Phi_i]_u,\,
\mathbb P\operatorname{div}R_u
\right\rangle
=
\left\langle
[S(t,s)^*\Phi_i]_u,\,
\operatorname{div}R_u
\right\rangle.
\tag{22}
\]

**At these ports, the Leray projector disappears exactly from the tested expression.** This avoids introducing a separate Riesz-transform tail into this observable estimate.

Let \(z^*=(u^*,b^*)\) be a reference realization with the same force and coefficient histories, and suppose faults occur only in \(z\). Put
\[
e=z-z^*,
\qquad
e_j(s)=\|e(s)\|_{L^2(Q_j)},
\qquad
E_j^*(s)=\|z^*(s)\|_{L^2(Q_j)}^2.
\]
The stress difference obeys
\[
\|R(z)-R(z^*)\|_{L^1(Q_j)}
\le
C\left(\sqrt{E_j^*}\,e_j+e_j^2\right).
\tag{23}
\]

Testing backward, integrating the stress divergence by parts, and using the two cancellations of \(\phi\) gives
\[
\begin{aligned}
|\langle\Phi_i,e(t)\rangle|
\le{}&
|\langle\Phi_i,S(t,0)e(0)\rangle|\\
&+
CK_0\sum_{\text{faults }s\le t}
\mathsf K_{3,M}(t-s,a(i-j_s))\\
&+
C\int_0^t\sum_j
\mathsf K_{3,M}(t-s,a(i-j))\\
&\hspace{28mm}\times
\left(\sqrt{E_j^*(s)}\,e_j(s)+e_j(s)^2\right)ds.
\end{aligned}
\tag{24}
\]

The first term is at most \(C\gamma\) under the preparation comparison in (19).

### Why this applies to energy-admissible weak realizations

On a finite torus and finite time interval, the quadratic stresses belong to \(L^\infty_tL^1_x\). The backward test is smooth in space and solenoidal. The weak equations can therefore be tested against it, using time cutoffs and then passing to the one-sided endpoint trace.

Each fault contributes its actual jump pairing. With post-jump observations, the sum includes \(s\le t\). No spatially weighted local energy inequality is being assumed, and the damaged realization need not remain strong. A reference need not be strong merely to justify the identity, although a controlled strong reference would be useful for later estimates.

The test function depends mathematically on the actual coefficient history. It is used only in the proof. The majorant (10) and the resulting weights are independent of that history.

### The estimate is still unclosed

The terms \(e_j\) in (24) measure the **full local physical error**. They are not determined by the finite port values. Equation (24) does not bound
\[
\sqrt{E_j^*}\,e_j+e_j^2
\]
by the weighted clock counts.

This is the remaining nonlinear step. A native renewal theorem would have to control these physical errors, including off-code fields, routing remnants and bulk modes, while producing the intended local update.

For fault tolerance, that comparison must also be organized around the rule applied to the **actual previous decoded symbols**. A fault can change a stored bit into another valid bit; later updates may obey the rule correctly while disagreeing indefinitely with the original fault-free computation. An integrable damage estimate should count defective updates, without imposing fading of every logical deviation.

## 3. The Poisson interface extends to predictable physical weights

The deterministic-weight lemma can be strengthened without conditioning on random weights.

Let \(w_a(i,s)\ge0\) be predictable with respect to the complete physical past, causal for update \(a\), and suppose almost surely
\[
\sup_{i,s}\sum_a w_a(i,s)\le W,
\tag{25}
\]
and
\[
\sup_a\sum_i\int_0^\infty
w_a(i,s)\,\frac{ds}{T}\le W.
\tag{26}
\]
Assume a defective update entails
\[
X_a:=\sum_i\int w_a(i,s)\,dN_i(s)\ge\beta.
\tag{27}
\]

Then, for every finite deterministic set \(A\) of updates,
\[
\boxed{
\Pr(A\text{ all defective})
\le
\left[
e^{\sqrt p-p}\,p^{\beta/(2W)}
\right]^{|A|}.
}
\tag{28}
\]

### Proof

Set
\[
s_A(i,s)=\sum_{a\in A}w_a(i,s).
\]
The pathwise budgets give
\[
0\le s_A\le W,
\qquad
\sum_i\int s_A(i,s)\,\frac{ds}{T}
\le W|A|.
\tag{29}
\]

Choose
\[
\theta=\frac{\log(1/p)}{2W}.
\]
The Poisson exponential martingale has compensator
\[
\frac pT\sum_i\int
\left(e^{\theta s_A(i,s)}-1\right)ds.
\]
Convexity on \([0,W]\) yields
\[
e^{\theta x}-1
\le
\frac{x}{W}\left(p^{-1/2}-1\right).
\]
Thus the compensator is bounded pathwise by
\[
(\sqrt p-p)|A|.
\tag{30}
\]
On the event that all updates in \(A\) are defective,
\[
\sum_i\int s_A\,dN_i
=\sum_{a\in A}X_a\ge\beta|A|.
\]
The exponential Markov estimate proves (28).

This permits a sensitivity budget to depend on the past fields. It does **not** permit weights chosen retrospectively from their future amplification. Expected row or column budgets also do not replace the pathwise bounds in (25)–(26).

If a separate, fully matched cellular construction supplied a rational threshold \(q_c\), and rational certified bounds \(W,\beta\) were available, then choosing
\[
m\ge\frac{2W}{\beta},
\qquad
p_0=
\min\left\{
\frac14,\left(\frac{q_c}{3}\right)^m
\right\}
\tag{31}
\]
would give an ordinary positive rational physical threshold. This is conditional threshold arithmetic. Neither the physical budgets nor a matched material implementation have been constructed here. The actual initialization and perturbation hypotheses of a cellular theorem, including those in Gács’s finite-horizon construction, still have to be verified. [cs-web.bu.edu](https://cs-web.bu.edu/faculty/gacs/papers/GacsReliableCA86.pdf?utm_source=chatgpt.com)

### A consequence of the column budget

For any finite observation horizon, the same domination implies
\[
\boxed{
\#\{\text{defective updates}\}
\le
\frac W\beta
\#\{\text{clock rings up to that horizon}\}.
}
\tag{32}
\]
This follows by summing the defect threshold and then using the column bound.

Thus this particular interface asks for more than a summable far-pressure estimate: its total defective-update burden is at most linear in total fault count. A different cluster representation could still support the full question if this interface proved too restrictive.

## 4. Higher fixed moment cancellation can pay for some polynomial count amplification

There is a useful conditional extension when a physical estimate is polynomial in local counts.

Suppose, for a fixed integer \(d\ge1\), a physical proof supplied
\[
a\text{ defective}
\quad\Longrightarrow\quad
\sum_z K_r(a,z)N_z^d\ge\beta.
\tag{33}
\]
Then
\[
\left(\sum_zK_r(a,z)N_z^d\right)^{1/d}
\le
\sum_zK_r(a,z)^{1/d}N_z.
\tag{34}
\]
The weighted Poisson lemma applies if these root weights have uniformly bounded rows and columns.

For the explicit kernel (10), the endpoint contribution to the spatial sum of \(K_r^{1/d}\) has order
\[
(1+h)^{3/2-(3+r)/(2d)}.
\]
The smeared contribution has order
\[
(1+h)^{2-(4+r)/(2d)}.
\]
Both are time summable provided
\[
r>5d-3,\qquad r>6d-4.
\]
For \(d\ge1\), it is enough that
\[
\boxed{r>6d-4.}
\tag{35}
\]

In particular:

- Linear count damage needs \(r=3\).
- Quadratic count damage can use \(r=9\).

For the quadratic case, a port of the form
\[
\phi=\partial_1^7\operatorname{curl}A
\tag{36}
\]
has eight derivatives and vanishing moments through degree seven. Together with the kick’s zero integral, it supplies nine kernel derivatives. A matching compact codelet can retain nonzero signal, for example through a nonzero multiple of \(\phi\).

Periodization preserves the root-weight estimate because
\[
\left(\sum_\ell K_\ell\right)^{1/d}
\le\sum_\ell K_\ell^{1/d}.
\]

This avoids the invalid step of applying a Poisson exponential-moment argument directly to \(N_z^2\), whose positive exponential moments diverge.

The qualification is substantial: **quadratic terms in the PDE do not prove a quadratic count bound for a recurrent processor.** A physical proof must control propagation, interactions and repeated renewal to obtain (33) with a fixed degree and the stated kernel. That estimate remains unavailable.

## 5. An explicit auxiliary map gives canonical reshaping for arbitrary cell words

There is also a constructive advance toward the clean local module. It concerns a scalar envelope update; its realization by the allowed mechanical MHD drive is not established.

Choose once a nonnegative compact bump \(\chi\), supported in a fixed ball, with \(\chi\) bounded below on a smaller ball. Let
\[
\chi_i(x)=\chi(x-c_i),
\qquad
m(x)=\sum_i\chi_i(x),
\]
with disjoint supports and cell spacing \(a\). The mask \(m\) is \(a\)-periodic.

Encode scalar bits by
\[
A_{\mathbf b}(x)=\sum_i b_i\chi_i(x),
\qquad b_i\in\{0,1\}.
\]
Suppose
\[
A=A_{\mathbf b}+e,
\qquad
\sup_i\|e\|_{H^1(Q_i)}\le E.
\tag{37}
\]

Choose a fixed nominal heat time \(h>0\), and define the known function
\[
q(x)=e^{h\Delta}(m^2)(x).
\tag{38}
\]
Because \(m^2\) is \(a\)-periodic, this is the same \(a\)-periodic function on every \(\Omega_M\).

On each bump support, its own positive heat contribution gives
\[
q(x)\ge q_*>0,
\tag{39}
\]
uniformly in \(M\). Choose a smooth cutoff \(\vartheta=1\) on the bump supports and supported in slightly larger fixed regions. The known multiplier
\[
c(x)=\frac{\vartheta(x)}{q(x)}
\tag{40}
\]
then has fixed bounded derivatives. No unknown value is divided out.

For
\[
v\in[(1-\zeta)h,(1+\zeta)h],
\]
form the auxiliary normalized signal
\[
s(x)=c(x)e^{v\Delta}(mA)(x).
\tag{41}
\]
On the support of \(\chi_i\),
\[
\begin{aligned}
s-b_i
={}&
b_i\frac{e^{v\Delta}(m^2)-q}{q}\\
&+\sum_{j\ne i}(b_j-b_i)
\frac{e^{v\Delta}(\chi_j^2)}q
+\frac{e^{v\Delta}(me)}q.
\end{aligned}
\tag{42}
\]

For every fixed derivative order \(k\), heat-kernel estimates give
\[
\boxed{
\|s-b_i\|_{C^k(\operatorname{supp}\chi_i)}
\le
C_k\left(E+\zeta+e^{-ca^2/h}\right).
}
\tag{43}
\]
The three terms respectively pay coefficient mismatch, neighbor leakage and input shape error. Gaussian lattice summation makes the constants independent of capacity.

Now let \(F\) be a fixed polynomial truth table for one output bit, and set
\[
G=R\circ F,
\qquad R(s)=3s^2-2s^3.
\]
At every Boolean input vector \(\mathbf b\),
\[
G(\mathbf b)=F(\mathbf b),
\qquad DG(\mathbf b)=0.
\tag{44}
\]
For finitely many input channels, including fixed cell translations for neighbor inputs, define
\[
A'(x)=m(x)G(s_1(x),\ldots,s_r(x)).
\tag{45}
\]
Taylor’s theorem and the chain rule give
\[
\boxed{
\sup_i
\left\|
A'-\sum_i b_i'\chi_i
\right\|_{H^1(Q_i)}
\le
C\left(E+\zeta+e^{-ca^2/h}\right)^2.
}
\tag{46}
\]

This is a direct physical-space estimate for arbitrary cell words. It includes all Bloch sectors. The auxiliary output vanishes outside the mask support, and its shape inside each support is close to the canonical bump.

The same estimate holds in sufficiently high fixed regularity. Applying a fixed differential encoding such as
\[
\mathcal C A=\partial_1\operatorname{curl}(e_jA)
\tag{47}
\]
therefore gives compact, solenoidal, mean-zero codelet profiles with a corresponding \(H^1\) restoration estimate. Matching probes have a fixed nonzero signal.

The parameter order can be fixed without dependence on a computation instance: choose the bump and \(h\), bound the restoration constants, choose a restoration radius, then choose \(a\) large and \(\zeta\) small, and finally approximate the known masks and normalizer to a fixed precision.

### What this construction does not implement

Equations (41) and (45) use scalar heat, known multiplication masks, translations and pointwise polynomial operations as **auxiliary target operators**. They are not additional permitted actuators.

To use this map, an affirmative must still implement those operations through the actual full MHD evolution, extract and copy the magnetic envelopes, and return velocity and all ancillary magnetic fields to a reusable class. The near-bit estimate (46) also does not control arbitrary large clusters outside its basin.

Thus this supplies a concrete canonical update to aim for; it does not supply the required \(f_*\).

## 6. Port stability still does not supply the bulk-energy theorem

The new kernel and reshaping estimates leave the uniform nonlinear energy-density requirement open.

There is a precise reason that moment-cancelled port control alone cannot establish it. Let \(L=aM\), \(\kappa=2\pi/L\), and consider
\[
b_M(x)=A_Me_3\cos(\kappa x_2).
\]
This field is solenoidal and has zero mean.

For any fixed translated probe with zero zeroth and first moments, Taylor expansion gives
\[
|\langle b_M,\phi_i\rangle|
\le C_\phi A_ML^{-2}.
\tag{48}
\]
Meanwhile,
\[
\frac1{V_M}\|b_M\|_2^2=\frac12A_M^2.
\tag{49}
\]
Taking \(A_M=L\), all such local port values tend to zero, while energy density grows as \(L^2\). The gradient-energy density remains bounded:
\[
\frac1{V_M}\|\nabla b_M\|_2^2=2\pi^2.
\tag{50}
\]

This is an observability counterexample, not an admitted initial condition or a constructed noisy trajectory. It proves that these port bounds and dissipation bounds cannot, by themselves, certify the required bulk-energy enclosure.

The accepted estimate remains
\[
\mathbb E E(t)+c\,\mathbb E\int_0^tD(s)\,ds
\le CV_M(1+t).
\]
A separate mechanism must establish
\[
\sup_{t\ge0}\mathbb E E(t)\le CV_M.
\tag{51}
\]
Once (51) holds, the absolute prescribed-work estimate follows from Cauchy–Schwarz and the fixed force bound.

I also did not obtain a universal negative from covariance rectification. Its long-wave contribution is of order \(|\kappa|\), while compensating driven Reynolds and Maxwell stresses can contribute at the same order. The order-one forcing domination used in the excluded coherent-force argument is absent.

## 7. The full construction still needs two physical theorems

The remaining work is now more narrowly identified.

**The first is a native recurrent realization theorem.** One fixed mechanical period must realize a local update such as (45), with actual copying and neighbor transfer, while renewing the complete physical state. It must cover arbitrary material words, all coefficient histories, the fixed preparation neighborhood and all relevant weak realizations.

**The second is a nonlinear fault-and-energy theorem for that realization.** It must control the actual stress term in (24), handle large clusters, and produce a valid weighted or cluster-based update-defect law. It must separately bound the slow bulk fields strongly enough to prove (51) on all paths.

The results above remove the unequal-diffusivity limitation from the linear interface, provide an all-weak nonlinear observable identity, strengthen the probability tools, and give a concrete auxiliary reshaper. They do not yet supply either of those two physical theorems.

Accordingly, I cannot yet emit justified architecture constants, a fixed force catalogue, a complete encoder and decoder, or a native threshold \(p_0\) satisfying the whole contract. I also have no argument showing that every allowed architecture must fail.
---

## Capture context

P2, GPT-6 Pro, chat https://chatgpt.com/c/6af4793b-ffe8-83ec-a7ab-863459a8d78d; final c8d8d6c1-9a6f-5cd5-a2ad-2f05f48f586a after user 3d3919be-faef-4b73-9e34-5405ddedbff2. Full final above copied from the UI; visible ending matches, and the native preview agrees. Complete native/database-byte equality is not asserted. Exact held prompt: P2_FULL_NATIVE_LOCAL_PROCESSOR_AFTER_WEIGHTED_FAULTS_PRO_20261112.txt, SHA-256 87222e82 (full source); the posted text omitted its single terminal LF.

The activity disclosure showed 24m 57s; Weighted mhd, Native gate, and Energy obstruction were named. One visible explanatory passage follows; remaining activity and expanded helper contents were not captured. Output/archive availability is unknown.

> I’ll build on the weighted-tail and energy estimates you’ve supplied. I’ll focus this round on extending the fault-response bounds to nonlinear driven MHD, constructing a reusable local update across all spatial modes, and testing whether the uniform energy requirement creates an obstruction that applies to every architecture.
