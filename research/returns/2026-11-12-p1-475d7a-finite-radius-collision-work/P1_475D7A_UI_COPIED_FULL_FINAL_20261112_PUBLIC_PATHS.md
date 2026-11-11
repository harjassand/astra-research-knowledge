**I cannot yet give a full affirmative or a full negative for this finite-radius extension.** I found no obstruction to the allowed design class, but I did not close the quantitative many-particle estimate needed for complete timed-path accuracy.

There is substantial progress beyond the supplied openings: **the actual wall and pair-collision work can be bounded polynomially, including from simultaneous-contact configurations and for every admitted clock decomposition.** The same construction gives the local reflection estimates needed for nominal existence and robustness. Exact balance, rejection-branch selection, and qualitative spatial reachability also survive.

The remaining issue is quantitative: obtaining a universally polynomial mixing or small-radius comparison bound for a variable number of mutually excluding particles. Below I give the new work estimate, explain the completed qualitative parts, and state a precise sufficient theorem that would finish the compiler. I will keep that missing theorem explicit rather than treat small excluded volume as a substitute for it.

## 1. What is established, and what remains missing

| Part of the contract | Status of this analysis |
|---|---|
| Abstract decoder graph, conservation, original labels and zero-auxiliary initialization | Inherited from the accepted compiler |
| Correct structural list of rejection branches | Established |
| Strictly feasible configurations for every count in the mass cap | Established |
| Exact nominal hard-core reaction balance | Established |
| Nominal conormal dynamics from every feasible configuration | Obtained by the local estimates and an existence/uniqueness passage described below |
| Qualitative spatial realization of finite allowed count paths | Established |
| Actual all-time event, movement, wall and pair-push bounds | Polynomial in the charged parameters and \(\rho^{-1}\) |
| Short-interval robustness under the full predictable fault box | Polynomial local estimates |
| Uniform polynomial accumulation into complete timed-path accuracy | **Not established** |
| An obstruction to every allowed compiler | **Not found** |

In particular, the missing accuracy estimate is not a failure of exact hard-core balance, a packing contradiction outside the mass cap, or an uncontrolled positive circulation of contact clocks.

## 2. A stronger contact cone: its angle need not shrink with \(\rho\)

Fix a current species list with \(n\le N_0\), and put
\[
r_i=\rho d_i,\qquad
\sum_i d_i\le N_0.
\]
Use inward gap functions
\[
g_{if}(q)=b_f-n_f\cdot q_i-r_i,
\qquad
g_{ij}(q)=|q_i-q_j|-r_i-r_j.
\]
Their gradients have norms \(1\) and \(\sqrt2\), respectively.

Form clusters by connecting every pair whose gap is at most \(\rho\). For a cluster \(C\), let
\[
R_C=\sum_{i\in C}r_i,
\]
and let \(z_C\) be the arithmetic mean of its centers. A spanning path gives
\[
\operatorname{diam} C\le 3R_C.
\]

Define
\[
t_C=\frac{16R_C}{\kappa},
\qquad
v_i=t_C(c-z_C)+(q_i-z_C),\quad i\in C.                         \tag{1}
\]

For a near-contact pair in \(C\),
\[
\nabla g_{ij}(q)\cdot v
=e_{ij}\cdot(v_i-v_j)
=|q_i-q_j|
\ge 2\rho.                                                    \tag{2}
\]

For a wall whose gap at \(q_i\) is at most \(\rho\), the inball and cluster diameter imply
\[
n_f\cdot(c-z_C)\le-\kappa+5R_C\le-\frac{\kappa}{2}.
\]
The dilution assumption therefore gives
\[
n_f\cdot v_i
\le -8R_C+3R_C
=-5R_C\le-5\rho.                                              \tag{3}
\]

Meanwhile,
\[
|v_i|\le \frac{60R_C}{\kappa},
\qquad
|v|\le \frac{60\rho N_0^{3/2}}{\kappa}.
\]

After normalization, a conservative common inward margin is
\[
\boxed{
\alpha=\frac{\kappa}{2^{10}(1+N_0)^2}
}                                                            \tag{4}
\]
for all constraints whose gap is at most \(\rho\).

Thus the near-contact range is proportional to \(\rho\), but **the normalized cone margin is independent of \(\rho\)**. This improves the supplied cone estimate and makes the short-time work bound below uniform at the natural time scale \(\rho^2\).

### No positive zero-force circulation

Let
\[
\mathcal D(t,q)=\operatorname{diag}(D_{s(i)}(t,q_i)).
\]
For any nonnegative coefficients \(\lambda_j\) on active constraints, the common inward vector gives
\[
(\mathcal D^{-1}v)\cdot
\sum_j\lambda_j\mathcal D\nabla g_j
\ge \alpha\sum_j\lambda_j.
\]
Since \(\|\mathcal D^{-1}v\|\le d_0^{-1}\),
\[
\boxed{
\left|\sum_j\lambda_j\mathcal D\nabla g_j\right|
\ge d_0\alpha\sum_j\lambda_j.
}                                                            \tag{5}
\]

A nonzero positive combination of the prescribed conormal pushes cannot vanish. This addresses the clock-decomposition issue directly.

## 3. A configuration-core potential pays every wall and pair clock

Let
\[
\mathcal K=\{q:g_j(q)\ge0\text{ for every constraint}\},
\]
and tighten every constraint by a small common amount:
\[
\mathcal K_\eta=\{q:g_j(q)\ge\eta\text{ for every constraint}\}.
\]

Choose
\[
0<\eta\le\eta_{\max},
\qquad
\eta_{\max}
=c_0\frac{\alpha^2\rho d_0^3}{1+\Lambda},                       \tag{6}
\]
where \(c_0>0\) is a sufficiently small fixed rational.

### 3.1 The tightened core lies nearby

From any \(q\in\mathcal K\), move distance \(2\eta/\alpha\) in its normalized near-contact direction.

Near wall constraints increase linearly. Near pair constraints satisfy the convex first-order lower bound for the Euclidean norm, so they also increase sufficiently. Far constraints can decrease by at most \(\sqrt2\) times the displacement. With (6),
\[
\boxed{
\operatorname{dist}(q,\mathcal K_\eta)\le \frac{2\eta}{\alpha}.
}                                                            \tag{7}
\]

This also proves that the tightened core is nonempty.

### 3.2 A nearby metric projection is unique despite nonconvexity

Define
\[
\Phi_\eta(t,q)=
\frac12\min_{y\in\mathcal K_\eta}
(q-y)^\top\mathcal D(t,q)^{-1}(q-y).                           \tag{8}
\]

The minimization is a proof object. The compiler never evaluates it.

Let \(y_*\) be a minimizer, \(z=q-y_*\), and \(M=\mathcal D^{-1}\). Equation (7) gives
\[
0\le\Phi_\eta(t,q)\le
\frac{2\eta^2}{\alpha^2d_0},
\qquad
|z|\le\frac{2\eta}{\alpha\sqrt{d_0}}.                          \tag{9}
\]

The cone condition supplies the multiplier qualification:
\[
Mz=-\sum_j\lambda_j\nabla g_j(y_*),
\qquad
\lambda_j\ge0,
\qquad
\sum_j\lambda_j\le\frac{|Mz|}{\alpha}.                         \tag{10}
\]

For an active wall constraint and any \(y'\in\mathcal K_\eta\),
\[
\nabla g_j(y_*)\cdot(y'-y_*)\ge0.
\]
For an active pair constraint, expanding the squared pair distance gives
\[
\nabla g_j(y_*)\cdot(y'-y_*)
\ge-\frac{|y'-y_*|^2}{2\rho}.                                 \tag{11}
\]

Consequently, the increase in the quadratic objective from \(y_*\) to \(y'\) is at least
\[
\left(
\frac12-\frac{|z|}{2\alpha\rho d_0}
\right)|y'-y_*|^2.
\]
The choice of \(\eta\) makes this strictly positive unless \(y'=y_*\). Thus the minimizer is unique.

The same inequalities at two nearby query points yield polynomial Lipschitz bounds for the projection and for \(\nabla\Phi_\eta\). In particular,
\[
\|\nabla\Phi_\eta\|_\infty
\le C\frac{\eta}{\alpha d_0^{3/2}},
\qquad
\operatorname{Lip}(\nabla\Phi_\eta)
\le C(1+\Lambda)^2d_0^{-4}.                                   \tag{12}
\]

These are operator-norm estimates. Their constants do not grow exponentially with the configuration dimension.

### 3.3 Each individual contact decreases the potential

At an original pair contact, write \(u=q_i-q_j\), with \(|u|=a\ge2\rho\). For \(y_*\in\mathcal K_\eta\), the corresponding pair vector \(u'\) satisfies \(|u'|\ge a+\eta\). Therefore
\[
\nabla g_{ij}(q)\cdot(y_*-q)
\ge \eta-\frac{|y_*-q|^2}{2\rho}.                             \tag{13}
\]
For a wall, the same lower bound holds without the quadratic error.

The envelope derivative of (8) is
\[
\nabla\Phi_\eta=Mz+e,
\qquad
|e|\le C\Lambda d_0^{-2}|z|^2.
\]
Combining this with (9), (13), and (6),
\[
\boxed{
\nabla\Phi_\eta(t,q)\cdot
\mathcal D(t,q)\nabla g_j(q)
\le-\frac{\eta}{2}
}                                                            \tag{14}
\]
for every active wall or pair constraint.

This controls each clock separately, rather than only a resultant force.

The projection remains unique on a sufficiently small open neighborhood of \(\mathcal K\). Each center is also at least \(\rho\) from the original container boundary. Ordinary spatial convolution on that neighborhood, followed by time regularization, justifies Itô’s formula while retaining the bounds. No high-dimensional optimization or geometric enumeration is executed by the compiler.

### 3.4 Actual all-time work

Let
\[
\mathcal L(t)=
\sum_{\text{lifetimes},f}L_{if}(t)
+
\sum_{\text{unordered common lifetimes}}L_{ij}(t).
\]

The full faulty covariance may have off-diagonal blocks. Nevertheless,
\[
|A:\nabla^2\Phi_\eta|
\le Cn\|\nabla^2\Phi_\eta\|_{\rm op}.
\]
The intrinsic drift, perturbing drift and time derivative have polynomial bounds of the same order.

A chemical firing changes the species list, dimension or core, but both the pre-firing and post-firing potentials lie in the interval in (9). Hence its potential jump is bounded by
\[
C\eta^2/(\alpha^2d_0).
\]

Itô’s formula and localization give
\[
\boxed{
\mathbb E\mathcal L(t)
\le C\left[
\frac{\eta}{\alpha^2d_0}
\bigl(1+\mathbb EF_{\rm all}(t)\bigr)
+
\frac{N_0(1+\Lambda)^2}{\eta d_0^4}\,t
\right].
}                                                            \tag{15}
\]

Each wall-clock increment contributes push length at most its size; each shared pair-clock increment contributes at most twice its size. With \(\eta=\eta_{\max}\),
\[
\boxed{
\begin{aligned}
\mathbb E[W_{\rm wall}(t)+W_{\rm pair}(t)]
\le C\bigg[
&\rho\bigl(1+\mathbb EF_{\rm all}(t)\bigr)\\
&+\frac{N_0(1+\Lambda)^3}
{\alpha^2\rho d_0^7}\,t
\bigg].
\end{aligned}
}                                                            \tag{16}
\]

Substituting (4) makes every numerical exponent explicit and fixed:
\[
\frac{N_0(1+\Lambda)^3}
{\alpha^2\rho d_0^7}
\le
C\frac{N_0(1+N_0)^4(1+\Lambda)^3}
{\kappa^2\rho d_0^7}.
\]

Thus a polynomially paid positive radius gives polynomial actual wall and pair work for all physical times. This estimate covers every admitted predictable fault rule and every clock decomposition satisfying the stated law.

### 3.5 Short intervals

The potential can use any \(0<\eta\le\eta_{\max}\). On a chemical-free interval of length \(u\le\eta_{\max}^2\), choose \(\eta=\sqrt u\). Then
\[
\boxed{
\mathbb E[
\mathcal L(s+u)-\mathcal L(s)\mid\mathcal F_s]
\le P_{\rm loc}\sqrt u,
}                                                            \tag{17}
\]
where
\[
P_{\rm loc}
=C\left[
\alpha^{-2}d_0^{-1}
+N_0(1+\Lambda)^2d_0^{-4}
\right].
\]
The coefficient \(P_{\rm loc}\) is independent of \(\rho\); the available interval length is \(\rho^2\) times a reciprocal polynomial in the other parameters.

Conditional iteration or an exponential-martingale calculation supplies exponential regulator moments on appropriately shorter polynomial windows.

**Limitation:** the time coefficient in (16) grows like \(\rho^{-1}\). The estimate pays work, but does not prove that total collision influence over a fixed positive horizon vanishes as \(\rho\to0\).

## 4. The qualitative and exact parts can be retained

### Nominal conormal dynamics

The fixed-count nominal form is
\[
\mathcal E_t(f,g)
=
\frac1{|\mathcal K|}
\int_{\mathcal K}
\nabla f^\top A_0(t,q)\nabla g\,dq,
\qquad
\operatorname{Dom}\mathcal E_t=H^1(\mathcal K).                  \tag{18}
\]

The common-cone and exterior-sphere estimates give the required local domain geometry. Fradon’s globule theorem supplies the normal-reflection framework and constraint-clock decomposition, but it is not directly the present variable conormal theorem. [emis.de](https://emis.de/ft/42699?utm_source=chatgpt.com)

Chen’s construction handles spatially varying symmetric conormal coefficients and identifies the divergence-form generator, initially outside an exceptional set of starting points. Its starting-point qualification must be retained. [link.springer.com](https://link.springer.com/content/pdf/10.1007/BF01199246.pdf?utm_source=chatgpt.com)

The extension here proceeds by freezing the deterministic fields on time grids and passing to a limit. The estimates above give uniform tightness of positions and regulators while initial points approach any feasible boundary configuration. The limiting clocks retain their correct face supports.

For uniqueness, compare two solutions using
\[
E(q,q')=(q-q')^\top A_0(t,q)^{-1}(q-q').
\]
At a pair contact, feasibility of the other configuration gives the hypomonotonicity estimate
\[
(z_i-z_j)\cdot e_{ij}
\le\frac{|z_i-z_j|^2}{2(r_i+r_j)}.
\]
After localization at finite total regulator,
\[
dE\le K E(dt+d\mathcal L+d\mathcal L')+dM,
\qquad
d[M]\le K E^2dt,
\]
with polynomial \(K\). The integrating-factor argument proves uniqueness of positions. Individual clocks at redundant faces need not be unique; (16) covers them all.

Uniform volume on \(\mathcal K\) is invariant for every frozen nominal step and for the limit. Equation (18) establishes instantaneous symmetry without computing \(|\mathcal K|\).

### Strict feasibility and qualitative connectivity

Every mass-capped count has a strictly feasible configuration: put the balls in separated slots along a line segment inside \(B_\kappa(c)\). The total required length is \(O(\rho N_0)\).

There is also a feasible path from any labeled configuration to such a parking arrangement. A touching cluster has diameter at most twice the sum of its radii. Translate it rigidly toward \(c\), stopping and merging at the first contact with another cluster. Convexity keeps the balls wall-feasible. After finitely many mergers, all centers can be gathered near \(c\).

Extract a foremost particle along a fixed direction, move it to a clear staging lane inside the inball, and then to its assigned parking slot. Repeat. The dilution condition leaves ample room for the lanes and slots.

A drift-only Girsanov argument along a finite feasible guide path, using (17) and the metric comparison, gives positive probability of reaching any desired interior neighborhood. This proves support; it supplies no physical steering operation and needs no polynomial lower bound on that probability.

At suitable interior placements, any allowed successful reaction has positive rate. The same applies to the rejection placements described next. Induction gives positive spatial realization of each finite allowed count path.

### The rejection list can be chosen structurally

The following criterion depends only on the retained slots and decoder payload sizes:

| Base channel | Rejection branch is needed exactly when |
|---|---|
| \(1\to2\) | Always: sufficiently small offsets make the offspring overlap |
| \(1\to1\) | The retained slot grows |
| \(2\to2\) | At least one retained slot grows |
| \(2\to1\) | The anchored product is larger than the anchored reactant |

Identity placements for true null channels are always feasible, so those marks remain observed.

For a growing slot, near-wall placements give an open set of feasible sources with infeasible targets. This does not require a wide facet: a closest supporting face to the supplied inball center provides such placements. Other particles can be parked away from the affected sites.

Conversely, if every retained slot decreases or stays unchanged, removal of other reactants and radius reduction preserve feasibility. Adding a rejection branch in that case would be incorrect.

### Exact hard-core balance

For \(A+B\to C\), with untouched configuration \(\eta\), the successful forward flux has the common geometric factor
\[
K_r(y-x)\,
\mathbf1_{\mathcal K}(\eta+A_x+B_y)\,
\mathbf1_{\mathcal K}(\eta+C_x).
\]
Its activity/coefficient factor is
\[
\frac{c_e\widetilde a_A\widetilde a_B}{V}.
\]
The reverse flux has the identical geometric factor and coefficient
\[
\frac{c_{\bar e}\widetilde a_C}{V}.
\]
Detailed balance makes them equal.

The same calculation handles retained-slot \(2\to2\) channels. Ordered identical reactants use the factorial Palm measure with no extra symmetry factor. Rejections are diagonal fluxes.

These are exact identities. They do not use a dilute approximation or a hard-core normalizer.

## 5. Radius choice and ordinary costs do not create a parameter circle

Let the accepted kinetic compiler have fine horizon
\[
T=H_{\rm kin}\tau,
\]
and let \(M\) include the necessary rejection branches. A proposal numerator can be chosen as
\[
L_*=
\frac{C(1+M)(1+N_0)^2(1+8/v)}q,
\qquad
J=1+L_*T.                                                     \tag{19}
\]
It is independent of \(\rho\).

Write
\[
\zeta_N(\rho)
=
\frac{3\rho N}{\kappa}
+\frac{\rho^3N^4}{\kappa^3}.
\]
The supplied equilibrium comparison pays the steric rate bias through a polynomial multiple of \(\zeta_{2N_0}(\rho)\).

It is therefore possible to choose a positive rational radius, with polynomial reciprocal, satisfying all three requirements:

\[
\begin{aligned}
\rho(1+N_0+P_{\max})
&\le \frac{\min(\kappa,r)}{2^{16}},\\
\rho
&\le \frac{\kappa}{C(1+N_0)^2},\\
J\,C_{\rm stat}(1+8/v)\zeta_{2N_0}(\rho)
&\le \epsilon/16.
\end{aligned}                                                 \tag{20}
\]

The second condition ensures that the feasible-uniform law is dominated by twice the original product-uniform law. The first dilution ceiling alone need not ensure that domination when one relatively large particle coexists with very many small particles.

All quantities in (20) are known before choosing an additional spatial slowing clock.

The ordinary costs are then straightforward. Conservation gives
\[
|Z(t)|_1\le N_0.
\]
For coefficients bounded by one, the total attempt intensity is bounded by
\[
C M(1+N_0)^2(1+8/v),
\]
including independently perturbed success and rejection branches. Slowing can make this bound at most one.

The remaining pathwise charges obey
\[
\begin{aligned}
\text{particle-time}&\le N_0t,\\
\text{continuous coordinate quadratic variation}&\le9N_0t,\\
\text{perturbing-drift variation}&\le\delta N_0t,\\
\text{intrinsic-drift variation}&\le3\Lambda N_0t,\\
\text{placement displacement}&\le\sqrt3\,rF_{\rm all}(t),\\
\text{radius-change variation}&\le4\rho P_{\max}F_{\rm all}(t).
\end{aligned}                                                 \tag{21}
\]

Together with (16), these are polynomial costs whenever the radius and observation clock have polynomial reciprocals or sizes as required. What remains unproved is the accuracy estimate that would certify such a clock.

## 6. A precise sufficient missing theorem

One concrete route would be a uniform, explicitly computable polynomial Poincaré bound:

> For every mass-capped species list and a radius chosen as in (20), uniform measure \(\mu_{\mathcal K}\) on its labeled feasible configuration domain satisfies
> \[
> \operatorname{Var}_{\mu_{\mathcal K}}f
> \le C_P\int_{\mathcal K}\sum_i|\nabla_i f|^2\,d\mu_{\mathcal K},
> \]
> where
> \[
> C_P\le
> C(1+N_0+F+\kappa^{-1}+\rho^{-1})^p
> \]
> with explicitly computable universal constants.

**I have not proved this bound.** It is a sufficient route, not a necessary condition for every possible compiler design.

There are two useful points about the reduction.

### High configuration dimension can be handled after such a bound

The core estimates give short exponential regulator moments. Smooth inner approximations can be made with a soft minimum of the gap functions:
\[
g_a=-a\log\sum_j e^{-g_j/a}.
\]
Their Hessians satisfy
\[
\nabla^2g_a
=
\sum_jw_j\nabla^2g_j
-\frac1a\operatorname{Cov}_w(\nabla g_j)
\le \frac C\rho I.
\]
The cone bounds their boundary gradients away from zero. Hence the negative part of boundary curvature is polynomially bounded; the large positive curvature caused by smoothing is harmless. The metric Bismut argument then gives a polynomial short-time smoothing constant. Local boundary charts convert the gradient estimate to Euclidean Lipschitz control.

If \(m=3n\), the cone-volume argument has the form
\[
\mu_{\mathcal K}(B(q,s)\cap\mathcal K)
\ge
\left(\frac{c\alpha s}{\sqrt m}\right)^m
\]
on a polynomially controlled local scale.

Combining this with \(L^2\) decay from the proposed Poincaré inequality gives
\[
\sup_q|P^0_{s,s+g}f(q)-\mu_{\mathcal K}f|
\le
A\exp\!\left[-\frac{2d_0g}{C_P(m+2)}\right],
\]
where \(A\) is polynomial. The power \(m\) in the volume estimate is removed by taking an \((m+2)\)-th root; it becomes a polynomial factor in the mixing time.

Thus a polynomial \(C_P\) would give a polynomial integrated mixing envelope without computing a \(3n\)-dimensional volume or heat kernel.

### Contact accuracy need not acquire a \(\delta^{1/n}\) exponent

The all-particle local comparison gives
\[
dE\le K E(dt+d\mathcal L)+Kn\delta^2dt+dM,
\]
\[
d[M]\le K(E^2+n\delta^2E)\,dt.
\]
The short regulator moments yield a local endpoint error
\[
e\le P_e\delta
\]
with polynomial \(P_e\).

For a successful or rejected branch predicate \(f\), use Lipschitz sandwiches
\[
f_w^-\le f\le f_w^+,
\qquad
\operatorname{Lip}(f_w^\pm)\le\frac{C(N_0+F)}w.
\]
Their difference is supported near only the affected wall, pair-distance and kernel boundaries. Three-dimensional slab and shell estimates, together with
\(\mu_{\mathcal K}\le2\mu_{\rm product}\), give
\[
\mu_{\mathcal K}(f_w^+-f_w^-)\le P_{\rm tube}w.
\]
Release offsets can be included in the same calculation.

The summable backward telescope would then give
\[
b(g)+P_1\delta+\frac{P_2\delta}{w}+P_3w.
\]
Taking \(w=\sqrt\delta\) gives a fixed exponent:
\[
\boxed{b(g)+P_{\rm err}\sqrt\delta.}                            \tag{22}
\]

With a polynomial mixing integral \(I\), the complete proposal/channel coupling would have error bounded by
\[
\frac{L_*I}{h}J
+
JP_{\rm err}\sqrt\delta
+
JC_{\rm stat}(1+8/v)\zeta_{2N_0}(\rho)
+
J\delta.                                                      \tag{23}
\]

The order of choices would be valid: choose the kinetic horizon, then \(\rho\) from the stationary bias, then \(h\) from mixing, and finally \(\delta\). No condition of the form “\(\rho\) times the subsequently enlarged physical horizon is small” would be needed.

The unproved Poincaré or equivalent mixing estimate is therefore a specific remaining mathematical input.

## 7. Why the shortcuts checked do not fill it

### Conditional one-particle inequalities can fail even for tiny balls

There is a simple cage example. Take two equal balls of radius \(a\) near a corner of a cube. In coordinates measured from the smallest allowed center position, the first center has \(u_i\ge0\). Fix the second center at
\[
(h,h,h),\qquad h=\frac54a.
\]

The corner \(u=0\) is feasible because
\[
\sqrt3\,h>2a.
\]
But every point of the simplex
\[
u_i\ge0,\qquad u_1+u_2+u_3=h
\]
lies inside the second ball’s exclusion region:
\[
|u-(h,h,h)|^2\le2h^2<4a^2.
\]

Thus the first particle’s conditional allowed region has a trapped corner component. This persists for arbitrarily small \(a\), so low total volume fraction does not justify a conditional one-particle Poincaré inequality.

Both particles are mobile in the actual model, and the full configuration is not trapped. This example defeats that particular comparison argument; it is not a counterexample to the compiler.

### Small excluded volume gives only a defective inequality by an elementary argument

A product-measure segment comparison does give
\[
\operatorname{Var}_{\mu_{\mathcal K}}f
\le
C\int_{\mathcal K}|\nabla f|^2\,d\mu_{\mathcal K}
+
C\kappa^{-3}\sum_{i\ne j}(r_i+r_j)^2
\,\operatorname{osc}(f)^2.                                    \tag{24}
\]

The error comes from one-coordinate line segments that hit an excluded ball. Averaging the other center pays a three-dimensional tube volume, so every power in (24) is fixed.

But (24) leaves an \(L^2\) relaxation floor of order \(\operatorname{poly}(N_0)\rho^2\). It is not a full spectral gap. Converting that residual to an all-start bound can lose the required uniformity in \(n\).

### Individual cluster estimates do not control repeated mergers

For an isolated free-space group with constant matrices, put
\[
M_i=D_i^{-1},\qquad
\xi=\left(\sum_iM_i\right)^{-1}\sum_iM_iQ_i,
\]
and
\[
V=\sum_i(Q_i-\xi)^\top M_i(Q_i-\xi).
\]
There is an exact identity
\[
dV=dM+6(n-1)\,dt+
2\sum_{i<j}(r_i+r_j)\,dL_{ij},
\qquad
d[M]=8V\,dt.
\]
Consequently,
\[
d(V^{-1/2})
=
d\widetilde M
-3(n-2)V^{-3/2}dt
-\sum_{i<j}(r_i+r_j)V^{-3/2}dL_{ij}.                           \tag{25}
\]

For two particles, this gives a small-radius bound on total collision regulator, including a touching start. For arbitrary \(n\), distant particles can make \(V\) large while a close pair continues colliding. A cluster decomposition must control splitting and subsequent merging; counting only \(n-1\) splits is invalid. I did not close that renewal argument.

### The located literature has narrower quantitative scopes

The Cattiaux–Fradon–Kulik–Roelly hard-ball diffusion paper explicitly treats two or three particles with mutual attraction in free space. It does not provide the required variable-population bound. [mfradon.plil.fr](https://mfradon.plil.fr/FichiersPageWeb/CFKR_Bernoulli.pdf?utm_source=chatgpt.com)

The spectral-gap result for continuous gas in Wu’s paper concerns Glauber birth/death dynamics. That jump-process Dirichlet form does not itself bound the conservative reflecting-diffusion form here. [sciencedirect.com](https://www.sciencedirect.com/science/article/pii/S0246020303000700?utm_source=chatgpt.com)

These scope checks do not establish that the needed theorem is impossible or absent from all literature. They establish that those results cannot be used as the missing estimate.

## Conclusion

The finite-radius extension has a workable exact chemical and spatial structure, and the configuration-core argument above supplies **polynomial actual wall and pair-push costs**, including all touching configurations and all permitted clock decompositions.

What I have not established is the uniform quantitative transport statement needed to certify \(H\), \(\delta\), and the complete observed timed-path error simultaneously. A polynomial hard-ball Poincaré bound would complete one route; a quantitative small-radius comparison from arbitrary touching clusters would complete another.

**Accordingly, this full compiler question remains unresolved in this analysis.** The work above is a partial theorem and a conditional closing argument, not a full affirmative and not an all-design negative.