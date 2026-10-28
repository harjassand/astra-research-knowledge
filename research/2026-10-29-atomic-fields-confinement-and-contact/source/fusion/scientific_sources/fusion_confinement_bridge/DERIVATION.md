# A passing-particle obstruction in the specified López torus

This construction concerns the concrete field and domain in [López,
arXiv:2610.29921v1](https://arxiv.org/html/2610.29921v1), not every exact
nonsymmetric vacuum field. The paper proves field-line nesting; the particle
extension tested here is a separate question. The irrational Sengupta families
are not covered by this obstruction.

## Geometry and units

Write the source coordinates as `(λ,β,φ)`, let `h=|X_φ|`, and use its identities

\[
 B=X_\phi/h^2=\nabla\phi,\qquad |B|=1/h,
 \qquad\nabla\lambda\times\nabla\beta=2\lambda B.
\]

The prescribed physical domain is the image of

\[
 Q=900(\lambda-3/20)^2+100(\beta-1/50)^2<1.
\]

Its entire label disk lies in the rectangle
`R=[7/60,11/60]×[−2/25,3/25]`. Neither λ nor β is periodic on this disk.
Every fixed `(λ,β)` gives a closed field line. This degeneracy is relevant to
particle drifts; field-line closure does not supply a third particle invariant.

The dimensionless Lorentz equations are

\[
 \dot x=v,\qquad\dot v=v\times B/\epsilon,
 \qquad |v(0)|=1,\qquad
 \epsilon={m v_0\over q B_{\rm unit} L_{\rm unit}}>0.
\]

Physical coordinates are `L_unit x`, fields `B_unit B`, and time
`L_unit/v0` times the reported time. Length, field strength and speed are
independent resources. No choice of these units or of a coil realization is
provided at zero cost. Reversing the charge reverses the drift orientation;
the absence of a closed action contour below is unchanged.

## An elementary metric function

With `t=√λ`, `u=t cosφ`, `v=t sinφ`, `d=1+λ`, the source algebra gives

\[
 h={\sqrt{\lambda(D_r^2+D_i^2)}\over d},
\]
\[
 D_r=2\beta+{4u[(1-\lambda)-(\lambda^2+2\lambda+3)v]\over d^2},
 \qquad
 D_i={4v+2(3+\lambda)(\lambda-2v^2)\over d}.
\]

One derivation starts from `ζ=√λ exp(iφ)`, the complex null vector
`N=(1−ζ²,i(1+ζ²),2ζ)`, `H=2ζ²+2iζ³`, and the source map
`X=(Re(H)Re(N)+Im(H)Im(N))/d²+(β−κ_g)n`.
Here `n=(2Reζ,2Imζ,λ−1)/d` and
`κ_g=4λ Reζ(1−Imζ)/d²`. The identities `N'·n=−2` and
`N'·Nbar=4d ζbar` yield
`D=H'−2H ζbar/d+2(β−κ_g)`, with real and imaginary parts as above, and
`h²=λ|D|²/d²`. Thus no numerical field-line acquisition is needed to evaluate
this particular metric function.

`lopez_native.py` evaluates this expression independently of the copied source
map, as well as analytic Cartesian derivatives of the implicit-root field.
`verify_formulas.py` compares the two evaluations and checks the Clebsch
identity, vacuum identities and guiding-center coordinate change. Those finite
checks do not replace the source's geometric existence proof.

## Exact equations within the first-order guiding-center model

A local vector potential is `A=(logλ/2)∇β`; hence `curl A=B`. Also
`b·dX=h dφ`, because the two transverse source coordinate vectors are
orthogonal to `X_φ`. The usual [first-order guiding-center variational
formulation (Littlejohn, 1983)](https://doi.org/10.1017/S002237780000060X)
therefore has one-form and Hamiltonian

\[
 \gamma={\log\lambda\over2\epsilon}\,d\beta+w h\,d\phi,
 \qquad H={w^2\over2}+{\mu\over h}.
\]

Its equations, without bounce or transit averaging, are

\[
 C=2\epsilon\lambda\left({w^2\over h}+{\mu\over h^2}\right),
 \quad \dot\lambda=C h_\beta,\quad\dot\beta=-C h_\lambda,
 \quad\dot\phi={w\over h},\quad\dot w={\mu h_\phi\over h^3}.
\]

They conserve `H` exactly as mathematical equations. Numerical conservation
error is measured separately. These are exact **within this first-order
model**, not the exact Lorentz equations.

There is an independent Cartesian check. For a static vacuum field,
`b·curl b=0`, `curl b=b×∇B/B`, and curvature is `∇⊥B/B`. The same
first-order equations reduce to

\[
 \dot R=w b+\epsilon {w^2+\mu B\over B^2}\,b\times\nabla B,
 \qquad\dot w=-\mu b\cdot\nabla B.
\]

Transforming these by the inverse source-map Jacobian reproduces the four
coordinate equations. This equality was checked numerically by
`verify_formulas.py`, including the sign of the β drift.

## Transit action and the certified sign

At energy `E=1/2`, put `κ=μ/E=2μ`. Uniformly passing particles have
`|w|=√(1−κ/h)` on the frozen field line. Their positive transit action is

\[
 J(\lambda,\beta,\kappa)=\int_0^{2\pi}\sqrt{h^2-\kappa h}\,d\phi.
\]

The leading slow displacement per *physical* transit, for either parallel
direction, is

\[
 \Delta\lambda=2\epsilon\lambda J_\beta+O(\epsilon^2),
 \qquad\Delta\beta=-2\epsilon\lambda J_\lambda+O(\epsilon^2).
\]

For negative parallel velocity, both `dβ/dφ` and the orientation of the φ
integration reverse. They cancel, so reversing parallel direction does not
remove the physical-time β drift. These are standard action-averaged
guiding-center relations, not a new confinement principle.

The construction is an interval certificate for **every**
`(λ,β)∈R`, `κ∈[0,1/10]`, not a scan at selected points. Define

\[
 f_1={4\sqrt\lambda(1-\lambda)\over d^2},\quad
 f_2=-4\lambda-{8\lambda\over d^2},\quad
 g_1={4\sqrt\lambda\over d},\quad
 g_2=2\lambda+{4\lambda\over d}.
\]

Then `D_r=2β+f1 cosφ+f2 cosφ sinφ` and
`D_i=g1 sinφ+g2 cos2φ`. Their λ derivatives are explicit:

\[
 f_1'={2(1-3\lambda)\over\sqrt\lambda d^2}
       -{8\sqrt\lambda(1-\lambda)\over d^3},\quad
 f_2'=-4-{8(1-\lambda)\over d^3},\quad
 g_1'={2(1-\lambda)\over\sqrt\lambda d^2},\quad g_2'=2+{4\over d^2}.
\]

Writing `r=√(D_r²+D_i²)`, interval evaluation uses

\[
 h_\lambda={(1-\lambda)r\over2\sqrt\lambda d^2}
       +{\sqrt\lambda(D_rD_{r,\lambda}+D_iD_{i,\lambda})\over d r}.
\]

Finally

\[
 J_\lambda=\int h_\lambda F(\kappa/h)\,d\phi,
 \quad F(a)={2-a\over2\sqrt{1-a}}.
\]

On `0≤a<1`, `F` is increasing and `F≥1`. In each interval cell, the
code multiplies the **signed interval** for `h_λ` by `[1,F(a_max)]`.
It does not assume that the pointwise derivative `h_λ` is positive.

`verify_passing_action.py` uses mpmath interval arithmetic at 30 decimal
digits, 8×8 label boxes, and 512 φ intervals covering the complete circle.
All constants, π, trigonometric functions, square roots and sums in the
enclosure use interval operations. Conversion of the final endpoints to JSON
floats is rounded outward with `nextafter`. The stored output is

\[
 h\ge0.1488166013419809>0.1,\qquad
 J_\lambda\ge11.91784956603872>0.
\]

No box failed. The passing margin is therefore also enclosed over the whole
label rectangle and pitch interval.

Since `J_λ>0`, a level of `J` intersects any fixed β at most once.
There is no closed regular action contour contained in this label disk.
The leading averaged β displacement has a definite negative sign. Replacing
the displayed magnetic surfaces by another choice of nested `Q(λ,β)` inside
the same volume cannot create the absent passing-action contours.

This is the precise obstruction: a common passing class lacks an enclosed
averaged drift surface **inside this prescribed source volume**. There is no
quantitative averaging-remainder certificate here. It does not prove that
every finite-ε Lorentz orbit exits, exclude exceptional finite-ε islands,
exclude a useful global extension of the field, constrain all pitches, or
apply to the irrational Sengupta fields.

## Independent dynamical tests and numerical costs

`guiding_center_ensemble.py` integrates the unaveraged equations above with
RK4 and terminates at an endpoint crossing of `Q=1`, interpolating the exit
time. Its finite step refinement is reported, rather than treating this as a
continuous-time enclosure. The prescribed passing and initially trapped
launches, including their rejected/lost trajectories, are retained in JSON.

`full_orbit_boris.py` integrates the Lorentz equations with drift-half,
magnetic Boris rotation, drift-half. It follows the prescribed complex cubic
root with Newton continuation. It never replaces that root by whichever root
happens to minimize Q after an exit. The last numerical step can require a
local analytic continuation across the boundary; no post-loss confinement is
inferred. Exit flags and interpolated times are numerical, not validated-ODE
enclosures. A uniform-field guiding-center control, energy error, root
residual estimate, step refinement, and comparison at two ε values are saved.

All runs were local CPU computations with `OPENBLAS_NUM_THREADS=2`, no paid
compute and no physical acquisition. A particle trace is not a plasma. Coil
generation, field metrology, collisions, electric fields, finite pressure,
collective response, wall loads, recovery after losses and engineering cost
are not included; they cannot turn this diagnostic into a device claim.
