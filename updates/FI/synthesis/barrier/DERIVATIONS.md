# Derivations and scoped consequences

All energies below are per active-material volume unless a total volume `V` is
shown. The order parameter `q` is scalar. The exact identities hold in the
specified polynomial model; finite-rate and finite-noise results add the
explicit dynamics or statistical assumptions stated in each section.

## 1. Coexistence sextic and global minima

Let

\[
 f_0(q)=\frac a2q^2-\frac b4q^4+\frac c6q^6,
 \qquad b,c>0,
 \qquad a=\frac{3b^2}{16c},
 \qquad q_B^2=\frac{3b}{4c}.
\]

Substitution and collection give

\[
 f_0(q)=\frac c6q^2(q^2-q_B^2)^2\geq0.
\]

Thus `0`, `+qB`, and `-qB` are equal-energy global minima. The zero-field
endpoint is degenerate; the path below selects one branch only while at least
one control remains engaged.

With gate `u>=0` and conjugate field `h`, set

\[
 f(q;u,h)=f_0(q)+\frac u4q^4-hq.
\]

**Engagement.** At `h=0`,

\[
 f(q;u,0)=f_0(q)+uq^4/4\geq0.
\]

For `u>0`, `q=0` is the unique global minimizer; at `u=0`, the three
coexistence minima return.

**Traversal.** Hold `u=U` and choose

\[
 h(q)=f'_0(q)+Uq^3=aq+(U-b)q^3+cq^5,
 \qquad 0\leq q\leq q_B.
\]

The selected `q` is stationary. The curvature at every competing scalar
coordinate `x` is

\[
 f''(x;U,h(q))=a-3(b-U)x^2+5cx^4.
\]

For `U>=b`, this is at least `a`. For `0<=U<b`, minimizing the quadratic in
`x^2` gives

\[
 \mu=a-\frac{9(b-U)^2}{20c}.
\]

If `mu>0`, the full tilted potential is strongly convex, so the selected
stationary point is its unique global minimum. At `U=11b/20=0.55b`,
`mu/a=257/500=0.514`. The strong-convexity threshold is
`U/b > 1-sqrt(5/12) = 0.3545027756...`.

**Tangent-compensated removal.** Hold `q=qB`, lower `u` from `U` to zero, and
set `h=u qB^3`. For every real `q`,

\[
 f(q;u,uq_B^3)-f(q_B;u,uq_B^3)
 =f_0(q)+\frac u4(q-q_B)^2(q^2+2q_Bq+3q_B^2)\geq0.
\]

The second factor is `(q+qB)^2+2qB^2`, hence strictly positive. For `u>0`,
`qB` is the unique global minimum. At `u=0`, all three minima are tied again.
Its curvature during removal is `4a+3u qB^2`, bounded below by `4a`.

The second term in the difference is the Bregman divergence

\[
 D_G(q,q_B)=G(q)-G(q_B)-G'(q_B)(q-q_B),\qquad G(q)=q^4/4,
\]

which is nonnegative because `G` is convex. In a vector state `x`, the same
argument gives `u D_G(x,B)>=0` whenever `G` is convex and the compensated
control is `u grad G(B)`. This proves a global-minimum statement only when the
other endpoint contribution `F0(x)-F0(B)` is already nonnegative; it does not
prove that a mechanically realizable field implements every component of
`grad G(B)`.

## 2. Local elastic elimination and preload

For an active strain `e` with natural value `alpha q^2`, coupled to a
zero-rest-strain shunt,

\[
 f_{el}(q,e;K)=\frac C2(e-\alpha q^2)^2+\frac K2e^2,
 \qquad C,K>0,
\]

stationarity in `e` gives

\[
 e_* = \frac{C\alpha q^2}{C+K},\qquad
 f_{el}(q,e_*;K)=\frac12\frac{CK}{C+K}\alpha^2q^4
 =\frac{u(K)}4q^4,
\]

where `u(K)=2 alpha^2 C K/(C+K)` and `u_max=2C alpha^2`. The actuator work
conjugate to `K` is

\[
 \partial_K f_{el}(q,e_*;K)=e_*^2/2=(q^4/4)u'(K).
\]

For a requested `0<U<u_max`, `K/C=U/(u_max-U)`. This only synthesizes a pure
quartic correction when the shunt has zero preload and the assumed strain
coordinate is realizable.

If the shunt rest strain is `e0`, replace `K e^2/2` by
`K(e-e0)^2/2`. Elimination gives

\[
 f_{el,*}=\frac{u(K)}4q^4-\frac{u(K)e_0}{2\alpha}q^2
                     +\frac{u(K)e_0^2}{4\alpha^2}.
\]

Therefore the quadratic coefficient becomes `a_eff=a-u e0/alpha`, and
engaging the gate at nominal `q=0` now costs work. The exact spring-port
derivative is

\[
 \partial_K f_{el,*}=\frac12(e_*-e_0)^2
 =u'(K)\left(\frac{q^4}{4}-\frac{e_0q^2}{2\alpha}
                    +\frac{e_0^2}{4\alpha^2}\right).
\]

Preload cannot be silently absorbed into a quartic-only fit.

## 3. Ideal and finite-time work

The generalized reversible work density is

\[
 dw=h\,dq+\frac{q^4}{4}\,du.
\]

During constant-`U` traversal,

\[
 W_{field}^{qs}=\int_0^{q_B}[f_0'(q)+Uq^3]dq
 =f_0(q_B)-f_0(0)+Uq_B^4/4=Uq_B^4/4.
\]

Removal at fixed `qB` returns `W_gate=-UqB^4/4`, so the ideal isothermal,
quasistatic, equal-free-energy scalar stroke has zero net control work. This is
one conversion stroke, not a refrigerator cycle or a complete energy boundary.

For overdamped Landau-Khalatnikov tracking with constant friction `zeta`,

\[
 \zeta\dot q=h-[f_0'(q)+Uq^3].
\]

Enforcing a path `q(t)` adds `zeta qdot` to the quasistatic field. Hence

\[
 W_{field}=Uq_B^4/4+\zeta\int_0^\tau\dot q^2dt,
 \qquad W_{gate}=-Uq_B^4/4.
\]

Cauchy-Schwarz gives `int qdot^2 dt >= (qB-0)^2/tau`, with equality for a
constant-speed path. Thus

\[
 W_{net}\geq\frac{\zeta q_B^2}{\tau}.
\]

At `U=0.55b`, relative to the ideal circulated work,

\[
 \frac{W_{net}}{Uq_B^4/4}
 \geq \frac{20}{11}\frac{\tau_{rel}}{\tau},
 \qquad \tau_{rel}=\zeta/a.
\]

This is a conditional lower bound for a specified scalar overdamped tracking
model. It excludes mechanical hysteresis, dielectric loss, leakage, field and
stiffness generation, heat transfer, and any non-Landau kinetic process.

## 4. Finite-volume fluctuations and endpoint selection

For a single uniform coordinate in volume `V`, take the canonical density
`rho(q) proportional exp[-V f(q)/(kBT)]`. At the zero-control coexistence
point, the three nondegenerate minima have curvatures `a,4a,4a`. Laplace's
method assigns a local Gaussian weight proportional to `1/sqrt(f''(q_i))`,
so the asymptotic basin probabilities are

\[
 p(0)=1/2,\qquad p(+q_B)=1/4,\qquad p(-q_B)=1/4.
\]

At the first engagement stage (`h=0`, small positive `u`), each polar basin
acquires an energy penalty `u qB^4/4+O(u^2)`. Its Gaussian prefactor is half
the central-basin prefactor, so the total polar-to-central ratio is
`exp(-x/4)+o(1)`, with `x=V u qB^4/(kBT)`. A central-basin probability of at
least `1-epsilon` therefore requires
`x >= 4 ln((1-epsilon)/epsilon)` in the small-`u` Laplace regime. For
`epsilon=0.01`, this is `4 ln(99)=18.38...`.

This is a model-specific one-coordinate equilibrium result. It does not
describe domain multiplicity, interfaces, defects, or nucleation in a real
sample. It does show that the exact zero-control endpoints are not pure
equilibrium states in this finite-noise model. Restricting equilibrium to the
central basin or to the `+qB` basin has coarse-grained reversible costs
`kBT ln(2)` and `kBT ln(4)`, respectively, under this asymptotic measure.

In the strongly convex middle stage, the Gibbs density has curvature at least
`V mu/(kBT)`. The Brascamp-Lieb variance inequality gives

\[
 \operatorname{Var}(q)\leq\frac{k_BT}{V\mu}.
\]

This is an equilibrium fluctuation bound; it does not quantify dynamic lag or
domain nucleation.

Near the end of tangent-compensated removal, let `h=u qB^3` and
`x=V u qB^4/(kBT)`. For small positive `u`, the central basin is higher than
`+qB` by `3u qB^4/4+O(u^2)`, and the opposite-polarization basin by
`2u qB^4+O(u^2)`. Curvature prefactors give

\[
 \frac{p_{central}}{p_{+}}\sim2e^{-3x/4},\qquad
 \frac{p_{-}}{p_{+}}\sim e^{-2x}.
\]

For a 99% target probability in the `+qB` basin, the leading Laplace ratios
require `2 exp(-3x/4)+exp(-2x) <= 0.01/0.99`, whose solution is
`x >= 7.0511218...`. Thus, asymptotically, retaining equilibrium selectivity
requires

\[
 u\gtrsim 7.0511\frac{k_BT}{Vq_B^4},\qquad
 h\gtrsim 7.0511\frac{k_BT}{Vq_B}.
\]

Both controls cannot be taken fully to zero while maintaining that equilibrium
success probability. Full restoration can instead leave the system in a
metastable history-selected phase, but its retention time and the work to
prepare and recover the phase must then be measured. These estimates are
asymptotic qualifications for the uniform scalar model, not BaTiO3 predictions.

## 5. A sufficient spatial theorem for a genuinely local gate

Consider a finite lattice with scalar site variables `q_i`, onsite
coexistence energies `f0(q_i)`, and nonnegative quadratic coupling
`kappa q^T L q/2`, where `L` is any symmetric positive-semidefinite graph
Laplacian (`L 1=0`) and `kappa>=0`. Add the sitewise gate
`u sum_i q_i^4/4` and a spatially uniform conjugate field.

For engagement at zero field, every onsite term `f0(q_i)+u q_i^4/4` is
nonnegative and vanishes only at `q_i=0` when `u>0`; the Laplacian energy is
also nonnegative. Thus the all-zero configuration is the unique global
minimum. For traversal along the homogeneous state `q_i=s`, use the uniform
field `h(s)=f0'(s)+Us^3`. Since `L 1=0`, this state is stationary. The full
Hessian is

\[
 H(q)=\operatorname{diag}\bigl(f_0''(q_i)+3Uq_i^2\bigr)+\kappa L.
\]

The onsite diagonal is bounded below by `mu=a-9(b-U)^2/(20c)`. Therefore
`H>=mu I` in the Loewner order whenever
`U/b>1-sqrt(5/12)`, and the finite-lattice potential is strongly convex
throughout traversal. At removal, choose `h=u qB^3`. Relative to the uniform
endpoint `qB 1`, the energy gap is

\[
 \sum_i\left[f_0(q_i)+uD_G(q_i,q_B)\right]
       +\frac{\kappa}{2}q^TLq\geq0,
 \qquad G(q)=q^4/4.
\]

For `u>0`, strict convexity of `G` makes the uniform `+qB` state the unique
global minimum; when `u=0`, coexistence minima return. This gives a finite-size
stability theorem for an ideal architecture with a local gate at every site
and only positive-semidefinite quadratic coupling. It does not show that a
compatible elastic shunt realizes that local term or supplies the required
uniform bias; the actual strain map and kernel remain implementation gates.

## 6. Mean-only spatial gate counterexample

For `N` scalar cells, let

\[
 F_{mean}=\sum_i f_0(q_i)+\frac{U}{4N}\left(\sum_iq_i^2\right)^2
                         -h\sum_iq_i.
\]

At a homogeneous state `q_i=q`, the gate Hessian is
`Uq^2 I+(2Uq^2/N)11^T`. A zero-mean perturbation removes the rank-one term,
leaving curvature

\[
 \lambda_{mean}(q)=a-(3b-U)q^2+5cq^4,
 \qquad \min_q\lambda_{mean}=a-\frac{(3b-U)^2}{20c}
\]

when `U<3b`. At `U=b`, this minimum is `-a/15`; at `U=0.55b` it is exactly
`-(901/1500)a`. A pointwise local gate instead has curvature
`a-3(b-U)q^2+5cq^4`, whose minimum at `U=0.55b` is `0.514a>0`.
Homogeneous energy matching is insufficient to infer stability of spatial
modes. Positive gradient energy adds a wave-number-dependent term but does not
fix the long-wavelength limit in arbitrarily large samples.

## 7. Positive elastic kernels need not give a convex order-parameter gate

Eliminating a compatible displacement from linear elasticity generally gives a
nonlocal positive-semidefinite quadratic form in the electrostrictive source
`r_i=q_i^2`, rather than independent local springs. In a finite discretization
write one such abstract quartic as

\[
 G(q)=\frac14 r^T J r,\qquad r_i=q_i^2,\qquad J=J^T\succeq0.
\]

Its order-parameter Hessian is

\[
 \nabla_q^2G=\operatorname{diag}(Jr)
           +2\operatorname{diag}(q)J\operatorname{diag}(q).
\]

The second term is positive semidefinite. The first term need not be: positive
semidefiniteness of `J` does not imply `Jr>=0` entrywise. An exact two-cell
countermodel is

\[
 J=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\succeq0,\qquad
 G(q_1,q_2)=\frac14(q_1^2-q_2^2)^2\geq0.
\]

At `(q1,q2)=(1,0)`, its Hessian is `diag(3,-1)`. Thus a positive
elastic-energy quartic can destabilize an order-parameter mode. A sufficient
condition for this kernel class is symmetric `J` positive semidefinite and
entrywise nonnegative: then `Jr>=0` for `r>=0` and both Hessian terms are
positive semidefinite. A quantitative path still needs a uniform lower bound
on the full Hessian after adding `f0` and the applied field.

This is an abstract compatibility-kernel countermodel, not the kernel of a
measured BaTiO3 shunt. The primary preprint's own multidomain calculation
emphasizes that elastic stresses must satisfy mechanical equilibrium and
computes nonlocal Fourier-projected kernels. It reinforces the need to derive
the actual kernel and boundary conditions before identifying a real shunt
with a pointwise local quartic gate.
