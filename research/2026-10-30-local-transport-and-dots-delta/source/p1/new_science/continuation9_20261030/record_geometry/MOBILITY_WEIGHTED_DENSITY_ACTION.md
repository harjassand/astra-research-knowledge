# A harmonic-current constraint generally changes rare density histories

Round-nine constructive target correction, existing record-geometry role. Root independently derived the traveling-wave gap after the initial message. This file proves a conditional variational statement and an explicit example. It does **not** prove a hydrodynamic or large-deviation limit for `NONLINEAR_PARTICLE_FIELD_ATTACK.md`, and is not a no-go theorem for every passive apparatus.

## 1. The precise ordinary comparison

Work on the unit circle. Let a smooth density stay in a compact subinterval of (0,1), let D>0 be constant, and define the current-noise strength

\[
\sigma(\rho)=2D\chi(\rho),\qquad \chi(\rho)=\rho(1-\rho).
\tag{1}
\]

Use the native exclusion action with this explicit clock convention,

\[
\mathcal I_{\rm nat}(\rho,j)
=\frac12\int_0^T\!dt\int_0^1\!dx\,
\frac{[j+D\partial_x\rho]^2}{\sigma(\rho)},
\qquad \partial_t\rho+\partial_xj=0.
\tag{2}
\]

For D=1/2 this is the current action proved for periodic symmetric exclusion by Bertini, De Sole, Gabrielli, Jona-Lasinio and Landim, *Large deviations of the empirical current in interacting particle systems*, [arXiv:math/0512394](https://arxiv.org/pdf/math/0512394), equation (1.2) and Theorem 2.2. Density large deviations follow by contraction over compatible currents. Other constant D values are time rescalings. These established facts supply the baseline; they do not supply a limit of the new particle-field apparatus.

The ordinary reciprocal metric constraint removes the harmonic current through a reaction force in that same direction. At a fixed density profile, write Sigma for multiplication by sigma(rho), and let `u=1`. The constrained current-noise operator is

\[
\Sigma_{\rm c}
=\Sigma-\Sigma u\,\langle u,\Sigma u\rangle^{-1}
\langle u,\Sigma\,\cdot\rangle.
\tag{3}
\]

The native thermodynamic response has the same projection, up to the chosen constant fluctuation-dissipation normalization. The unforced drift `b=-D rho_x` has zero spatial average. Its constrained projection is therefore still b. Typical unforced heat is compatible with (3).

For any a of zero spatial average, `Sigma_c Sigma^{-1} a=a`. Its inverse quadratic form on that subspace is consequently `integral a^2/sigma`. Thus the corresponding conditional target action is precisely (2) on currents with `integral j=0`, and infinity outside that constraint. This assertion is about the declared metric-constrained comparison law. Showing that a particular field elimination produces it remains a separate receiving theorem.

## 2. Exact contraction for a fixed density path

For a fixed smooth mass-conserving density path, continuity fixes the current up to a spatial constant. Let k(t,x) be the unique compatible current with zero spatial average, and write

\[
j(t,x)=k(t,x)+I(t),\qquad
a(t,x)=k(t,x)+D\partial_x\rho(t,x).
\]

Define

\[
h(t)=\int_0^1\frac{dx}{\sigma(\rho(t,x))},\qquad
\ell(t)=\int_0^1\frac{a(t,x)}{\sigma(\rho(t,x))}\,dx.
\tag{4}
\]

At each time the native action integrand is the scalar quadratic

\[
\frac12\int\frac{a^2}{\sigma}
+I\ell+\frac12hI^2.
\tag{5}
\]

The freely chosen harmonic current is therefore

\[
I_*(t)=-\frac{\ell(t)}{h(t)}.
\tag{6}
\]

The native density action and the density action under harmonic-current pinning satisfy the exact identity

\[
\boxed{\quad
\mathcal I_{\rm pin}^{\rho}(\rho)
-\mathcal I_{\rm nat}^{\rho}(\rho)
=\frac12\int_0^T\frac{\ell(t)^2}{h(t)}\,dt.
\quad}
\tag{7}
\]

The right side is generally strictly positive. A density trajectory fixes the divergence of current, but the native fluctuation can choose a circulation that lowers its mobility-weighted cost. The reciprocal constraint removes that optimization variable.

For exclusion,

\[
\int\frac{D\rho_x}{\sigma(\rho)}\,dx
=\frac12\int\frac{\rho_x}{\rho(1-\rho)}\,dx=0,
\tag{8}
\]

because the integrand is the derivative of a periodic function of rho. This does not make the k contribution vanish. For spatially constant sigma, in contrast, `integral a=0` implies ell=0. That is the special reason the homogeneous Gaussian program can retain all native density histories while deleting a harmonic current.

On an actual heat path, k=-D rho_x and a=0. Both actions have zero cost there. Thus equality of typical heat is entirely consistent with a strict difference for rare density histories.

## 3. An explicit strictly interior traveling-wave counterexample

Let

\[
\rho(t,x)=m+\varepsilon\cos[2\pi(x-vt)],
\quad 0<\varepsilon<\min(m,1-m),\quad v\ne0.
\tag{9}
\]

The compatible zero-mean current is `k=v(rho-m)`. This is a smooth nonflat path with a fixed specified initial profile. The quantities in (4) are independent of t. The elementary circle integral `integral (b+epsilon cos(2pi x))^{-1}dx=(b^2-epsilon^2)^{-1/2}` gives

\[
H=\int\frac{dx}{\chi(\rho)}
=\frac1{\sqrt{m^2-\varepsilon^2}}
 +\frac1{\sqrt{(1-m)^2-\varepsilon^2}},
\]

\[
A=\int\frac{\rho-m}{\chi(\rho)}\,dx
=\frac{1-m}{\sqrt{(1-m)^2-\varepsilon^2}}
 -\frac{m}{\sqrt{m^2-\varepsilon^2}}.
\tag{10}
\]

Hence `h=H/(2D)`, `ell=vA/(2D)`, and

\[
I_*=-vA/H,\qquad
\mathcal I_{\rm pin}^{\rho}-\mathcal I_{\rm nat}^{\rho}
=\frac{Tv^2A^2}{4DH}.
\tag{11}
\]

For the exact choice `m=1/4`, `epsilon=1/8`,

\[
A=\frac6{\sqrt{35}}-\frac2{\sqrt3}<0,
\qquad
H=\frac8{\sqrt3}+\frac8{\sqrt{35}}>0.
\tag{12}
\]

The gap in (11) is strictly positive. No boundary density, singular mobility, numerical fitting, or questionable exchange of limits is involved. The path stays between 1/8 and 3/8.

## 4. Two rings: coupling currents couples rare density histories

For two native rings, define `a_a`, `ell_a`, and `h_a` as in (4), using their own D_a and sigma_a. Without the apparatus, each fixed density path chooses its own circulation

\[
I_a^*=-\ell_a/h_a.
\]

The signed harmonic-current constraint requires `I_1=I_2=I`. Minimizing (5) jointly gives

\[
I_{\rm c}^*=-\frac{\ell_1+\ell_2}{h_1+h_2}.
\]

The exact difference between constrained and independently native density actions is

\[
\boxed{\quad
\Delta\mathcal I^\rho
=\int_0^T
\frac{h_1h_2}{2(h_1+h_2)}
(I_1^*-I_2^*)^2\,dt.
\quad}
\tag{13}
\]

Take ring 1 to follow (9)-(12), and ring 2 to remain at any strictly interior constant density. Then `I_1^*` is nonzero and `I_2^*=0`, so (13) is strictly positive. Both ordinary unforced heat solutions still have `a_1=a_2=0` and zero cost. The corrected nonlinear target can retain both mean heat equations while changing and coupling their rare density histories.

At the instantaneous noise level the same distinction is already visible. For the two-ring signed constant vector `u=(1,-1)`, the reciprocal projection subtracts

\[
\frac{(\Sigma u)\otimes(\Sigma u)}{\langle u,\Sigma u\rangle}.
\]

Applying the two density divergences subtracts a rank-one covariance involving `(-partial_x sigma_1,+partial_x sigma_2)`. This term vanishes for spatially constant mobilities, but generally not along nonflat exclusion profiles. A common stationary product measure or an unchanged deterministic drift does not remove it.

## 5. A different port can preserve the density action

This is not an impossibility statement for every passive architecture. Let Q be the Euclidean projector that removes the selected harmonic-current direction. The formally transformed noise operator

\[
\widetilde\Sigma=Q\Sigma Q
\tag{14}
\]

differs from (3). Since divergence annihilates the removed harmonic direction, `B Q=B` and `Q B*=B*`; therefore

\[
B\widetilde\Sigma B^*=B\Sigma B^*.
\tag{15}
\]

A simultaneous actual force/current transformation has a different response port and can retain the density noise operator. The formal path cost is obtained by minimizing the native action over removed harmonic components before assigning the physical constrained current. It is not the bare restriction used in (7). For one ring it assigns the pinned current exactly the native contracted density cost; the two-ring density contraction is likewise unchanged.

Equation (14) is not produced by merely rewriting a current record as QJ. If native particles actually moved by J, all of that displacement remains counted. A physical realization needs the different transduction, bath, and reaction operations, with their resource costs and complete actual-current accounting. The passive metric constraint of the given native port and a two-sided Euclidean transformation are distinct suppliers. The physical-mechanism role is examining the latter separately.

## 6. Consequence for the next nonlinear target

If the particle-field elimination is proved to realize the ordinary reciprocal metric constraint, its appropriate unforced joint action is (2) on the selected constrained currents, with the density contraction (7) or (13). “Both mean heat equations survive” is compatible with that result; “both native rare density histories remain unchanged” generally is not.

If unchanged density action is required, the target must specify an actual different port such as (14), or another mechanism that preserves the density noise operator. The bounded-current theorem and product invariant law alone select neither alternative. This file settles the variational distinction and explicit example, while leaving the microscopic nonlinear elimination unproved.
