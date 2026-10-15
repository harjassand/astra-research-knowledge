# Fixed linear heat misses every smooth nonlinear convex determinant energy

Independent elementary deduction extending the supplied det-square
example. No historical-first claim is made.

**Statement.** Let g:R->R be C2, convex and nonaffine. For every fixed
positive-definite constant input diffusion D, some smooth affine-periodic
compatible map has increasing integral g(det Dv) under componentwise
D-heat. Consequently no universally zero-integral correction can make
that same flow's dissipation nonnegative for all compatible maps.

**Isotropic proof.** Since g is C2, convex and nonaffine, there exists a
nonzero s with g''(s)>0. On the normalized 2pi-periodic torus, take

    v(x,y)=(s(x+sin y), y+sin(x+sin y)).

This is an affine map diag(s,1)(x,y) plus a smooth periodic perturbation.
It is a composition of two shears and a target scaling. Its Jacobian
determinant is identically s. Let v_t evolve its periodic perturbation
by ordinary componentwise heat, leaving the affine background fixed,
and put J_t=det Dv_t.

For any smooth map,

    partial_t J_t = Delta J_t
                    -2 sum_i det(partial_i Dv_t).

At t=0 the displayed shear map gives

    h:=partial_t J_t|0
      =2s sin y cos y sin(x+sin y),
    average h=0, average h^2=s^2/4>0.

The verifier checks the Jacobian, heat derivative, determinant evolution
identity and exact square average. The x average of the shifted sine
square is 1/2, while average sin^2 y cos^2 y=1/8.

The null-Lagrangian mean identity gives average J_t=s for all t. Thus
E(t)=average g(J_t) satisfies

    E'(0)=0,
    E''(0)=g''(s) average h^2 =g''(s)s^2/4>0.

Equivalently, a second-order Taylor expansion at s and the exact mean
identity give E(t)=g(s)+g''(s)s^2 t^2/8+o(t^2). This argument only needs
g C2. Hence E(t)>E(0) for all sufficiently small positive t, and E'(t)>0
for some positive times. The increase starts at a constant-Jacobian
map that already attains the determinant-Jensen lower bound.

**Other constant diffusions.** Set L=D^(1/2), y=L^(-1)x and compose the
isotropic construction with this input map. It solves D-heat on the
transformed lattice. The determinant is divided by det L. Choose the
isotropic target scale s det L to keep the receiving determinant value
s. The resulting strict energy increase survives this positive change
of variables. The torus lattice is allowed to change; this proof is not
a claim that L maps the square lattice to itself.

For any proposed correction N[v] with integral N[v]=0 for every compatible
map, pointwise nonnegative corrected dissipation would imply nonnegative
integrated dissipation and hence decreasing E. The strict increase is a
contradiction. Thus the obstruction concerns the operation, and cannot be
removed merely by replacing Gram SOS with a larger class of null terms.

Every g(det A) here remains polyconvex and quasiconvex, by the usual
minor-Jensen argument. The example is not a QC violation. It excludes
universal monotonicity under the specified fixed linear heat flow, while
leaving separate minor-Jensen channels, nonlinear flows and other
Lyapunov quantities available.
