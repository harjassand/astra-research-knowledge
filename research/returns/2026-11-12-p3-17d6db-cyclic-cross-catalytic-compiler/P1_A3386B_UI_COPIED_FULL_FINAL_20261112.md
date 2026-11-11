**Yes—using the accepted well-mixed compiler as a primitive, the spatially inhomogeneous extension can be constructed with universal polynomial costs.**

The additional argument needs two ingredients that were absent from the spatially homogeneous proof:

1. A wall potential whose conormal derivative remains positive when \(D(t,x)\) varies with position.
2. A short-interval comparison, followed by a summation using nominal mixing, that controls contact probabilities without accumulating an exponential factor over the physical horizon.

A suitable potential is the squared distance, in the metric \(D(t,x)^{-1}\), to a slightly contracted copy of the container. It supplies both the actual wall-work bound and the short-time exponential wall moments needed for the comparison.

I give the construction below. The smooth reflected-diffusion results cited in the proof are used at their stated scopes; the passage to polytope corners and the polynomial estimates are included explicitly.

## 1. Constants and the compiler

Write \(R=\mathsf R_{\rm num}\). Run the accepted conservative well-mixed compiler with accuracy \(\epsilon/4\). Denote its coefficients by \(b_e\), its clock by \(H_{\rm kin}\), and its species, decoder and activities by
\[
\mathcal S,\qquad P,\qquad \widetilde a.
\]
Thus \(0<b_e\le1\). Put
\[
T=H_{\rm kin}\tau.
\]

For each release channel, add one hidden, self-reverse unary rejection channel on its parent species. Let \(M\) count all directed channels after these additions. This addition depends only on the emitted reaction structure, hence only on \(R\) and its supplied reverse involution.

Compute exactly
\[
V=\operatorname{Vol}_3(\Omega),
\]
and
\[
q=
\frac{\operatorname{Vol}_6
 \{(x,y)\in\Omega^2:\ |x_j-y_j|\le r,\ j=1,2,3\}}
 {V(2r)^3}.
\]
Use the supplied bound
\[
\frac{\kappa^6}{4096}\le q\le1.
\]

Here are deliberately generous rational constants for the transport estimates:
\[
\begin{aligned}
\mathsf K&=2^{40}(1+\Lambda)^4d_0^{-8},\\
\ell&=
\frac{2^{-64}\kappa^2d_0^5}
 {(1+8\mathsf K)^2(1+\Lambda)^2},\\
G&=\frac{2^{16}}{d_0\ell},\\
B_{\rm mix}&=2^{16}\kappa^{-2}G,\\
I&=2\ell+\frac{10(1+B_{\rm mix})}{d_0},\\
W&=2^{20}\left[
 1+\kappa^{-2}G+\mathsf K(1+r^{-1})
 +G\mathsf K\left(1+\frac I\ell\right)
 \right].
\end{aligned}                                                    \tag{1}
\]

Set \(v=(2r)^3\), and define
\[
L_*=\frac{4(1+M)(1+N_0)^2(1+8/v)}q,
\qquad
J=1+L_*T.
\]
Choose
\[
\boxed{
h=
\left\lceil
\max\left\{
1,\ q^{-1},\ L_*,
\frac{16L_*IJ}{\epsilon}
\right\}
\right\rceil ,
\qquad
\delta=\left(\frac{\epsilon}{1024WJ}\right)^9,
\qquad
H=hH_{\rm kin}.
}                                                               \tag{2}
\]

The emitted coefficients are as follows.

| Fine channel | Emitted coefficient |
|---|---:|
| Binding \(A+B\to C\) | \(b_e/(hq)\) |
| Its successful reverse release | \(b_{\bar e}/(hq)\) |
| The associated hidden rejection branch | \(b_{\bar e}/(hq)\) |
| Other unary channels and global \(0\to0\) marks | \(b_e/h\) |

The rejection coefficient in this table multiplies its **local rejection kernel**. It is not multiplied again by the averaged rejection probability \(1-q\).

Because \(h\ge q^{-1}\), every coefficient lies in \((0,1]\). All these quantities are rational. The compiler’s numerical operations are rational arithmetic, the fixed-dimensional volume calculation, and the accepted kinetic compilation.

The rest of the proof establishes why these choices work.

## 2. A wall potential for spatially varying conormal reflection

Fix a species and suppress its index. Put
\[
M(t,x)=D(t,x)^{-1},
\qquad
K_\theta=c+(1-\theta)(\Omega-c),
\]
and define
\[
F_\theta(t,x)=
\frac12\min_{y\in K_\theta}
(x-y)^\top M(t,x)(x-y).                                         \tag{3}
\]

This minimization is an analytic proof device. Its minimizer is not computed by the compiler.

Take
\[
0<\theta\le
\theta_{\max}
=\frac{\kappa d_0^3}{128(1+\Lambda)}.
\]

Let \(y_*(t,x)\) be the unique minimizer and \(z=x-y_*\). Using the candidate \(y=(1-\theta)x+\theta c\),
\[
0\le F_\theta(t,x)\le\frac{6\theta^2}{d_0},
\qquad
|z|\le\sqrt{12}\,\theta d_0^{-1/2}.                              \tag{4}
\]

The envelope derivative is
\[
\nabla F_\theta=Mz+e,
\qquad
e_j=\frac12z^\top(\partial_jM)z.
\]
Since
\[
\|\partial_jM\|_{\rm op}\le\Lambda d_0^{-2},
\]
we have
\[
|e|\le6\sqrt3\,\Lambda\theta^2d_0^{-3}.
\]

If \(x\) lies on an active face with outward unit normal \(n_f\), every \(y\in K_\theta\) satisfies
\[
(x-y)\cdot n_f\ge\theta\kappa.
\]
Consequently,
\[
\boxed{
\nabla F_\theta(t,x)\cdot D(t,x)n_f
\ge\frac{\theta\kappa}{2}.
}                                                               \tag{5}
\]

This holds separately for every active face at a corner. It also holds for redundant inequalities that are active there.

### Regularity and Itô’s formula

The metric-projection variational inequalities give
\[
\operatorname{Lip}(y_*)\le
d_0^{-1}+C\Lambda\theta d_0^{-5/2}.
\]
Together with inverse-matrix differentiation, this yields the uniform bounds
\[
\begin{aligned}
\|\nabla F_\theta\|_\infty
&\le8\theta d_0^{-3/2},\\
\operatorname{Lip}(\nabla F_\theta)
&\le256(1+\Lambda)^2d_0^{-4},\\
\|\partial_tF_\theta\|_\infty
&\le6\Lambda\theta^2d_0^{-3}.
\end{aligned}                                                    \tag{6}
\]

The function is \(C^{1,1}\) in space. An entirely interior regularization makes ordinary Itô’s formula applicable:
\[
F^\eta(t,x)=
\int
F_\theta\!\left(
t,(1-\eta)x+\eta c+\frac{\eta\kappa}{2}z
\right)\varphi(z)\,dz,
\]
where \(\varphi\) is a smooth mollifier supported in the unit ball. Convexity keeps all sampled points inside \(\Omega\). Gradients converge uniformly, Hessians remain uniformly bounded, and sufficiently small regularizations retain a positive fixed fraction of (5). Time mollification handles the Lipschitz time dependence.

Thus no differentiability of a polyhedral projection at an active-set change is assumed.

### Actual wall work

For an actual particle,
\[
|g(t,x)|\le3\Lambda,
\qquad
\|A_{ii}\|_{\rm op}\le\frac32.
\]
The drift term in Itô’s formula for \(F_\theta\) is bounded by
\[
C(1+\Lambda)^2d_0^{-4}.
\]

Sum the potentials over all currently present particles. A chemical firing changes this sum by at most \(C\theta^2/d_0\), because an elementary channel affects at most three particles. Applying (5), localizing, and then removing the localization gives
\[
\begin{aligned}
\mathbb E\sum_{\text{lifetimes},f}L_{if}(t)
\le C\bigg[
&\frac{\theta}{\kappa d_0}
 \bigl(N_0+\mathbb EF_{\rm all}(t)\bigr)\\
&+\frac{(1+\Lambda)^2}{\theta\kappa d_0^4}N_0t
\bigg].
\end{aligned}                                                    \tag{7}
\]

Taking \(\theta=\theta_{\max}\) proves
\[
\boxed{
\mathbb EW_{\rm wall}(t)
\le C\left[
N_0+\mathbb EF_{\rm all}(t)
+N_0(1+\Lambda)^3\kappa^{-2}d_0^{-7}t
\right].
}                                                               \tag{8}
\]

Here \(|Dn_f|\le1\), so the sum of face-clock increments bounds the requested wall-push length.

Correlations between particles do not create a dimension factor in this calculation: the Hessian of the summed potential is block diagonal.

### Conditional exponential wall moments

The same potential supplies the stronger local estimate needed below. On a chemical-free interval, let \(\mathcal L_t\) be the sum of the face clocks for at most four coupled particle coordinates—an actual pair and its nominal comparison pair.

The martingale in the summed-potential calculation has
\[
d[M]_t\le C\theta^2d_0^{-3}\,dt.
\]
The exponential-martingale inequality therefore gives, conditionally on any preceding full history,
\[
\mathbb E e^{\lambda\mathcal L_t}
\le
\exp\left[
 C\frac{\lambda\theta}{\kappa d_0}
 +C\frac{\lambda(1+\Lambda)^2t}{\theta\kappa d_0^4}
 +C\frac{\lambda^2t}{\kappa^2d_0^3}
\right].                                                        \tag{9}
\]

This calculation uses bounded predictable characteristics, not a Markov property of the faulty position process.

With
\[
\lambda=8\mathsf K,
\qquad
\theta=\frac{\kappa d_0}{2^{24}(1+8\mathsf K)},
\]
the value of \(\ell\) in (1) makes the exponent in (9) smaller than \(\log2\). The constants have sufficient slack also for smooth inner convex approximations with inradius \(\kappa/2\). Hence
\[
\boxed{
\mathbb E\!\left[
e^{8\mathsf K\mathcal L_t}\mid\mathcal F_{\rm start}
\right]\le2,
\qquad 0\le t\le\ell.
}                                                               \tag{10}
\]

## 3. The local comparison under correlated, adaptive faults

On a chemical-free interval, start an actual selected pair \(Q\) and a nominal pair \(Y\) from the same positions. Drive the nominal particles by the corresponding independent Brownian innovations used in the full system.

Use
\[
E_t=\sum_{i=1}^2
(Q_i-Y_i)^\top D_i(t,Q_i)^{-1}(Q_i-Y_i).
\]

There are two contributions to the noise difference:
\[
\sqrt{A(t)}-\sqrt{A_0(t,Q)}
\quad\text{and}\quad
\sqrt{D_i(t,Q_i)}-\sqrt{D_i(t,Y_i)}.
\]
The square-root Sylvester estimate, followed by projection onto the selected six coordinates, gives
\[
\|\sigma_Q-\sigma_Y\|_F^2
\le
C\left[
\delta^2d_0+
\frac{\Lambda^2}{d_0}|Q-Y|^2
\right].                                                        \tag{11}
\]
The constant is independent of the total number of particles.

For the reflection terms, the leading actual term is
\[
-2(Q_i-Y_i)\cdot n_f\le0,
\]
and the leading nominal term is
\[
2(Q_i-Y_i)\cdot n_f\le0.
\]
Spatial variation of \(D\), and differentiation of \(D^{-1}\), produce additional terms bounded by \(C E_t\,d\mathcal L_t\).

Using the coefficient derivative bounds gives
\[
\begin{aligned}
dE_t
&\le
\mathsf K E_t(dt+d\mathcal L_t)
+\mathsf K\delta^2dt+dM_t,\\
d[M]_t
&\le\mathsf K(E_t^2+\delta^2E_t)\,dt.
\end{aligned}                                                    \tag{12}
\]
No derivative of the faulty covariance, drift, multiplier or policy occurs.

Set
\[
Z_t=e^{-\mathsf K(t+\mathcal L_t)}E_t.
\]
Direct first- and second-moment estimates give
\[
\mathbb EZ_t\le\mathsf K\delta^2t,
\qquad
\mathbb EZ_t^2
\le\frac32\mathsf K^2e^{\mathsf Kt}\delta^4t^2.
\]
Combining these with (10), and using \(\ell\le1/\mathsf K\), proves
\[
\boxed{
\mathbb E|Q_t-Y_t|^2
\le16\mathsf K\delta^2t,
\qquad
\mathbb E|Q_t-Y_t|
\le4\sqrt{\mathsf K}\,\delta\sqrt t,
\quad t\le\ell.
}                                                               \tag{13}
\]

These estimates hold after conditioning on arbitrary preceding hidden history. They are the new local stability input for the supplied conditional-clock operation.

## 4. Nominal existence, smoothing and mixing, including corners

### Existence of the specified conormal model

The nominal equation is the variational equation
\[
dX+D(t,X)N_\Omega(X)(dt)
\ni
\operatorname{div}D(t,X)\,dt+\sqrt{2D(t,X)}\,dW.                   \tag{14}
\]

The relevant convex-reflection framework is the oblique-subgradient formulation of Gassous, Răşcanu and Rotenstein. Their Theorem 7 establishes strong existence and uniqueness for a symmetric positive \(C_b^2\) reflection matrix \(H(x)\); choosing the convex function to be an indicator gives the full normal cone of a convex set. Their theorem is not itself a statement for the time-dependent field in this question. [arxiv.org](https://arxiv.org/html/1102.3634v4?utm_source=chatgpt.com)

Here is the required extension and boundary passage.

Take smooth inner convex domains
\[
\Omega_j\Subset\Omega,\qquad
B_{\kappa/2}(c)\subset\Omega_j,\qquad
\overline{\Omega_j}\to\Omega
\]
in Hausdorff distance. Smooth \(D\) spatially inside \(\Omega\) and in time. Matrix averaging preserves the exact bounds
\[
d_0I\le D_j\le I
\]
and the required derivative bounds. Smooth approximate equations exist; equivalently, smooth time dependence can be handled by adjoining deterministic time in the variational existence proof.

The wall-potential calculation works uniformly on these convex domains. In particular, choosing \(\theta=\sqrt u\) on sufficiently short intervals gives
\[
\mathbb E[
\mathcal L_{s+u}-\mathcal L_s\mid\mathcal F_s]
\le C_{\rm loc}\sqrt u,
\]
where \(C_{\rm loc}\) is polynomially bounded. Conditional iteration supplies all fixed-order moments of these increments. Together with the bounded diffusion and drift characteristics, this gives continuous-path tightness of positions and normal regulators.

Write a normal regulator as \(dK_j=n_j\,dL_j\). Convexity gives
\[
(X_j-z_j)\cdot dK_j\ge0
\quad\text{for every }z_j\in\Omega_j.
\]
This inequality passes to the limit, identifies \(dK\in N_\Omega(X)(dt)\), and identifies the conormal term as \(\int D(t,X)\,dK\).

The \(\delta=0\) version of (12), localized at finite regulator variation, proves pathwise uniqueness. Thus the limit defines the nominal model from **every** point of \(\Omega\), including corners. The first time derivative introduced in the metric calculation is bounded almost everywhere; time mollification justifies the Lipschitz case.

For a polytope, the normal regulator decomposes into the listed face normals. The inball inequality prevents cancellation by positive combinations of active normals, so the face-clock sum is controlled as above even with redundant inequalities.

### Uniform volume and instantaneous symmetry

The nominal form is
\[
\mathcal E_t(f,g)=
\frac1V\int_\Omega
\nabla f^\top D(t,x)\nabla g\,dx,
\qquad
\operatorname{Dom}\mathcal E_t=H^1(\Omega).                       \tag{15}
\]
Its generator is precisely
\[
\operatorname{div}(D(t,x)\nabla),
\]
with the specified conormal boundary condition. It is symmetric at each time and preserves
\[
\mu(dx)=dx/V.
\]

The same identification follows by passing the smooth-domain variational equations to the limit. The inball geometry supplies uniform \(H^1\) extensions, and the energy estimates identify the limiting Neumann evolution. Uniform volume invariance also passes directly from the smooth approximations.

### Short-time Lipschitz smoothing

For the nominal diffusion, introduce the Riemannian metric
\[
\mathfrak g_t=D(t,\cdot)^{-1}.
\]
Then
\[
\operatorname{div}(D\nabla)
=
\Delta_{\mathfrak g_t}
+\frac12D\nabla\log\det D\cdot\nabla.                             \tag{16}
\]

On a smooth convex approximation, the coefficient bounds imply
\[
\operatorname{Ric}_{\mathfrak g_t}
-\nabla^{\mathfrak g_t}\!\left(\tfrac12D\nabla\log\det D\right)
-\tfrac12\partial_t\mathfrak g_t
\ge-K_0\mathfrak g_t,
\]
and
\[
\mathrm{II}_{\mathfrak g_t}\ge-\sigma_0\mathfrak g_t,
\]
where
\[
K_0\le C(1+\Lambda)^2d_0^{-4},
\qquad
\sigma_0\le C\Lambda d_0^{-3}.                                   \tag{17}
\]

The second inequality is uniform over the convex approximations: their Euclidean second fundamental form contributes a nonnegative term. Only derivatives of \(D\) contribute to its negative part. Large positive curvature introduced by rounding a corner causes no loss.

The smooth Bismut formula in Cheng–Zhang, Theorem 2.5, bounds its derivative multiplicative functional by
\[
\exp\{K_0(t-s)+\sigma_0(\mathcal L_t-\mathcal L_s)\}.
\]
Its hypotheses include smooth coefficients and boundary, nonexplosion, and the corresponding exponential integrability. We apply it to the smooth approximations, where (10) supplies that integrability. [arxiv.org](https://arxiv.org/html/1211.3623v2?utm_source=chatgpt.com)

The formula and Itô isometry yield
\[
\operatorname{Lip}(P^0_{s,s+a}f)
\le\frac{C}{\sqrt{d_0a}}\|f\|_\infty,
\qquad a\in[\ell/2,\ell].
\]
The \(G\) in (1) dominates both the one-particle bound and the bound for a pair of independent nominal particles.

To pass this estimate to corners, first use smooth terminal functions satisfying the terminal conormal condition. These are uniformly dense in continuous functions on each smooth closed domain: flatten the function in a thin terminal-metric normal collar. The resulting bound is independent of the approximating function’s derivatives. Weak convergence of the reflected processes then passes the bound to continuous tests on \(\Omega\). Duality against continuous functions for finite regular measures extends it to all bounded Borel tests.

Thus
\[
\boxed{
\operatorname{Lip}(P^0_{s,s+a}f)\le G\|f\|_\infty
}
                                                               \tag{18}
\]
holds for all starting points in the closure.

### A paid mixing envelope

Convexity and \(\operatorname{diam}\Omega\le2\sqrt3\) give the Poincaré bound
\[
\operatorname{Var}_\mu f
\le\frac{\operatorname{diam}(\Omega)^2}{\pi^2}
\int|\nabla f|^2\,d\mu
\le2\int|\nabla f|^2\,d\mu.
\]
The diameter bound for the convex-domain Poincaré constant is dimension independent. [arxiv.org](https://arxiv.org/abs/1309.6211?utm_source=chatgpt.com)

Applied to the actual backward evolution, this gives
\[
\|P^0_{s,s+g}f-\mu f\|_2^2
\le e^{-d_0g}\|f-\mu f\|_2^2.                                   \tag{19}
\]

For every \(x\in\Omega\) and \(0<\rho\le1\), convexity and the inball give
\[
\mu(B(x,\rho)\cap\Omega)
\ge\frac{\kappa^3\rho^3}{1024}.                                 \tag{20}
\]
Combining (18)–(20) converts the \(L^2\) decay to an all-start supremum bound. For an independent nominal pair, a valid nonincreasing TV envelope is
\[
b(g)=\min\{1,B_{\rm mix}e^{-d_0g/10}\},
\qquad
\int_0^\infty b(g)\,dg\le I.                                    \tag{21}
\]

This argument uses the nonautonomous evolution in its correct order. It does not assume that the time-ordered transition operator is selfadjoint.

## 5. Contact estimates uniform over the whole gap

The local comparison (13) controls smooth tests. Binding also needs the indicator
\[
f(x,y)=\mathbf1_{\{|y-x|_\infty\le r\}}.
\]

Consider a final comparison interval of length \(a\in[\ell/2,\ell]\). From (18), invariance, and (20), a nominal particle assigns a set of volume \(O(w)\) probability at most
\[
C\kappa^{-2}G\,w^{1/4}.
\]
Conditioning on the first endpoint of the independent nominal pair therefore gives
\[
\Pr\{\text{nominal relative endpoint is within }w
\text{ of the contact boundary}\}
\le64\kappa^{-2}G\,w^{1/4}.                                     \tag{22}
\]

Combining this with (13),
\[
e_{\rm contact}
\le
\frac{16\mathsf K\delta^2\ell}{w^2}
+64\kappa^{-2}G\,w^{1/4}.
\]
Choose \(w=\delta^{8/9}\). Then
\[
\boxed{
e_{\rm contact}
\le
(16\mathsf K\ell+64\kappa^{-2}G)\delta^{2/9}.
}                                                               \tag{23}
\]

For release, the success function
\[
w_r(x)=\int_\Omega K_r(y-x)\,dy
\]
is Lipschitz with constant at most \(6/r\). Thus the local comparison also controls both successful and rejected release probabilities.

Now partition a longer gap into intervals of lengths in \([\ell/2,\ell]\). Telescope the conditional expectations using the nominal backward functions. Subtract their common invariant mean before applying (18). Their future Lipschitz constants then decay with the remaining mixing envelope \(b\).

Using the supplied summable interface, or this direct telescope, gives
\[
\left|
\mathbb Ef(Q_g)-P^0_{0,g}f(Q_0)
\right|
\le
e_{\rm contact}
+2Ge\left(2+\frac{2I}{\ell}\right),
\]
where \(e\le4\mathsf K\delta\) is sufficient by (13).

Consequently, for every gap length and every preceding history,
\[
\boxed{
\begin{aligned}
\left|\mathbb Ef(Q_g)-\mu^{\otimes2}f\right|
&\le b(g)+W\delta^{2/9}
&&\text{for binding contact},\\
\left|\mathbb Ew_r(Q_g)-q\right|
&\le b(g)+W\delta^{2/9}
&&\text{for release success},\\
\left|\mathbb E(1-w_r(Q_g))-(1-q)\right|
&\le b(g)+W\delta^{2/9}
&&\text{for rejection}.
\end{aligned}
}                                                               \tag{24}
\]

For short gaps, \(b(g)=1\) supplies the trivial bound.

This is a conditional occupation estimate. It makes no claim that the faulty positions are stationary, independent, reversible, or close in joint-position TV to equilibrium.

## 6. Complete marked-path accuracy

For the emitted system, the total actual chemical intensity is bounded by
\[
\frac{L_*}{h}.
\]
This includes binding, successful release, failed release, all other hidden channels, original null marks and global marks. It permits independent faults on the success and rejection branches.

Apply the accepted deterministic-rate proposal augmentation at this rate. At each proposal, condition on the full previous history and the next independent gap. Couple the conditional **channel** probabilities after averaging the spatial uncertainty. Retain the actual conditional trajectory, tuple, offset, rejection and subsequent policy.

Under uniform positions, the averaged binding rate for a specified eligible ordered pair is
\[
\frac{b_e}{hq}\frac Vv
\mu^{\otimes2}\{|y-x|_\infty\le r\}
=\frac{b_e}{h}.
\]
The averaged successful-release rate is likewise \(b_{\bar e}/h\). The averaged rejection rate is
\[
\frac{b_{\bar e}(1-q)}{hq};
\]
it is a hidden null rate in the reference process.

Equation (24), and the separate bound on chemical multipliers, bound the per-proposal discrepancy by
\[
b(g)+W\delta^{2/9}+\delta.
\]
On physical horizon \(hT\), summing gives
\[
\boxed{
d_{\rm TV}(\text{actual fine marked path},
           \text{reference fine marked path})
\le
\frac{L_*I}{h}(1+L_*T)
+W(1+L_*T)\delta^{2/9}
+(1+L_*T)\delta .
}                                                               \tag{25}
\]

With (2), the three terms are bounded by
\[
\frac{\epsilon}{16},
\qquad
\frac{\epsilon^2}{2^{20}WJ},
\qquad
J\left(\frac{\epsilon}{1024WJ}\right)^9.
\]
Their sum is less than \(\epsilon/4\).

Hide the reference rejection marks and rescale by \(h\). The remaining reference count process is exactly the nominal fine process produced by the kinetic compiler. Its decoded path at clock \(H_{\rm kin}\) is within \(\epsilon/4\) of the target. Therefore
\[
\boxed{
d_{\rm TV}\!\left(
\mathcal L(\text{observed path of }PZ(H\cdot)),
\mathcal L(X)
\right)<\epsilon.
}                                                               \tag{26}
\]

The coupling keeps event times exactly. Original null and parallel labels remain separate marks. The first proposal gap is included in (25), so the proof includes arbitrary initial placements without inserting or deleting an initial waiting period.

## 7. Balance, exact graph and spatial support

### Exact nominal balance

For a binding/release pair, the ordered Palm flux densities are
\[
\frac{\widetilde a_A}{V}
\frac{\widetilde a_B}{V}
c_eVK_r(y-x)
=
\frac{c_e\widetilde a_A\widetilde a_B}{V}K_r(y-x)
\]
and
\[
\frac{c_{\bar e}\widetilde a_C}{V}K_r(y-x),
\]
restricted to \(x,y\in\Omega\).

They agree because
\[
c_e\widetilde a_A\widetilde a_B
=c_{\bar e}\widetilde a_C.
\]
Scaling both directions by \(1/(hq)\) preserves this identity.

For \(2A\), the ordered factorial Palm measure gives exactly the required convention, with no factor \(1/2\). Rejection branches are self-reverse null events. Unary and global channels retain their paired balance identities.

Equation (15) supplies instantaneous diffusion symmetry. These identities also hold after restriction to any actual invariant chemical class; its normalizer is unnecessary.

### Chemical graph

The species, decoder, reverse map and observed-label map are inherited from the accepted compiler. The additional rejection branches are hidden unary loops. Hence:

- Every decoder column is nonzero, and original columns remain the identity.
- Every hidden channel preserves \(P\).
- Every observed label has its required decoded increment and enabling condition.
- All-state reachability equivalence and exact class preimages remain intact.
- All weights \(w_s=\omega P_s\ge1\) remain conserved.
- Initialization is precisely the supplied original population, with zero auxiliaries.

### Positive spatial realization of finite count paths

A qualitative support argument is needed in addition to the occupation estimates.

Fix an interior target point \(y\), a starting point \(x\in\Omega\), and the linear guide
\[
\phi(t)=x+\frac tT(y-x).
\]
On a finite interval, uniform ellipticity permits an equivalent drift-only Girsanov change under which the total drift is \(\phi'\). This is a proof of positive probability, not an emitted force.

For
\[
E_t=(Q_t-\phi(t))^\top D(t,Q_t)^{-1}(Q_t-\phi(t)),
\]
the guide comparison gives
\[
dE_t\le
\mathsf K E_t\bigl((1+|\phi'|)dt+d\mathcal L_t\bigr)
+Cdt+dM_t,
\qquad
d[M]_t\le CE_t\,dt.
\]
Under this bounded guide drift, the wall estimate becomes
\[
\mathbb E[\mathcal L_{s+u}-\mathcal L_s\mid\mathcal F_s]
\le C_{\rm loc}(\sqrt u+|\phi'|u).
\]
Subdivision gives finite exponential wall moments uniformly as \(T\downarrow0\), since
\[
|\phi'|T=|y-x|\le\operatorname{diam}\Omega.
\]
The weighted first- and second-moment argument then yields
\[
\mathbb EE_T\le C'T\longrightarrow0.
\]

A continuous Girsanov density leaves the chemical compensators unchanged. Taking \(T\) sufficiently small gives positive probability of reaching the desired interior neighborhood without a chemical firing.

Place eligible particles in a small common interior neighborhood for binding, a parent in an interior neighborhood for successful release, or near the relative interior of a genuine facet for a rejected release. The required reaction then has positive intensity, including under the admitted multipliers. Iteration proves positive-probability realization of every finite allowed count path.

The constant in this qualitative support argument need not be polynomial: no compiler parameter or cost estimate uses it.

## 8. Actual event, movement and wall costs

Conservation gives, pathwise,
\[
|Z(t)|_1\le\sum_s w_sZ_s(t)=N_0.
\]

Because \(h\ge L_*\), the actual total firing intensity is at most one. Thus the untruncated process is nonexplosive and
\[
\boxed{
\mathbb EF_{\rm all}(t)\le t,
\qquad
\mathbb EF_{\rm all}(H\tau)\le L_*T.
}                                                               \tag{27}
\]
Every failed release and every null firing is counted.

The movement bounds are
\[
\begin{aligned}
\int_0^t|Z(s)|_1\,ds&\le N_0t,\\
\text{continuous coordinate quadratic variation}
&\le9N_0t,\\
\text{perturbing-drift variation}
&\le\delta N_0t,\\
\text{intrinsic-drift variation}
&\le3\Lambda N_0t,\\
\text{local reaction displacement}
&\le\sqrt3\,rF_{\rm all}(t).
\end{aligned}                                                    \tag{28}
\]

Combining (8) and (27),
\[
\boxed{
\mathbb EW_{\rm wall}(t)\le CR^{13}(1+t).
}                                                               \tag{29}
\]
This is a bound on the actual accumulated wall-push length, including all lifetimes and corners.

## 9. Universal numerical and binary costs

Increase the accepted kinetic compiler’s fixed universal exponent to \(p_0\ge2\), if necessary, so that
\[
M,\ H_{\rm kin},\ \max b_e^{-1},\
\max_s(\widetilde a_s+\widetilde a_s^{-1}),\
\max_{i,s}P_{is}
\le C_0R^{p_0},
\]
and its bit cost is bounded by \(C_0(1+L+R)^{p_0}\).

Running it at \(\epsilon/4\) preserves this form of bound. Indeed, the associated \(U\) grows by at most four, so
\[
\Gamma_{\epsilon/4}\le4^D\Gamma_\epsilon\le\Xi\Gamma_\epsilon.
\]
The structure size of the paired-prefix construction is a fixed polynomial in the explicitly expanded reaction list.

The added numerical bounds are:

| Quantity | Bound up to a universal constant |
|---|---:|
| \(\mathsf K\) | \(R^{12}\) |
| \(\ell^{-1}\) | \(R^{33}\) |
| \(G\) | \(R^{34}\) |
| \(I\) | \(R^{37}\) |
| \(W\) | \(R^{116}\) |
| \(L_*\) | \(R^{p_0+11}\) |
| \(J\) | \(R^{2p_0+12}\) |
| \(h\) | \(R^{3p_0+61}\) |
| \(H,\ \max_e c_e^{-1}\) | \(R^{4p_0+61}\) |
| \(H\tau\) | \(R^{4p_0+62}\) |
| \(\delta^{-1}\) | \(R^{18p_0+1161}\) |
| \(\mathbb EF_{\rm all}(H\tau)\) | \(R^{2p_0+12}\) |

For reciprocal coefficients, the binary/release scaling gives
\[
c_e^{-1}=hq/b_e\le h/b_e,
\]
so an additional \(q^{-1}\) factor is unnecessary.

The exact-volume calculation uses only dimensions three and six. Enumerate independent fixed-size facet intersections, identify faces, and sum the determinants in a barycentric triangulation indexed by maximal face flags. Redundant inequalities and degeneracies are handled by exact rational comparisons. A conservative fixed bit-operation exponent of \(150\) suffices; no dimension proportional to the particle population occurs.

The remaining parameters use a fixed number of rational operations, fixed powers, comparisons and a ceiling. The normals have finite algebraic descriptions
\[
n_f=\frac{a_f}{\sqrt{a_f^\top a_f}}
\]
from the rational facet vectors.

Consequently one common exponent is
\[
\boxed{p=18p_0+1200,}                                            \tag{30}
\]
with a universal constant computable from the accepted kinetic compiler’s constants and the displayed numerical constants. It covers the numerical requirements, compiler bit operations, working memory, output size and individual descriptions.

The compiler computes \(N_0\) by a binary dot product. Its operations do not enumerate particles, population balls or communicating classes. The potentials, nominal evolutions, smooth approximations and changes of measure above establish correctness; they are not numerical subroutines or observations of the unknown medium.

**The spatial dependence of \(D\) therefore does not obstruct the requested compiler.** The positive conormal derivative in (5), the conditional short-time wall moment in (10), and the summable contact estimate in (24) supply the additional control. Together with the accepted kinetic and conditional-clock constructions, they give the full marked-path, graph, balance, initialization and actual-cost assertions in the question.