# Independent derivation of the elastic moving-face model

This cross-line review was requested by root. I read the whole governing
`new_opportunity/ELASTIC_INTERFACE.txt` and its predecessor `CONSTRUCTION.txt`,
then derived the elasticity, moving-face transport, sufficient stability
bounds and finite-amplitude column statement independently. The current
reviewed interface note has SHA256
`1320071569052b5f2963c1f13ab55ace52d934434e3e7a71b5604c374d295b96`.
The owner added the explicit constitutive and flat-equilibrium qualifications
after root and this review independently identified them. No owner file was
edited by this reviewer.

The algebra and the supplied fixture pass for the declared frozen-coefficient
linear model. The separate finite-amplitude column theorem passes with a
stationary flat reference. The calculation does not establish the physical
conjunction of a loaded anisotropic ionic skin and the nonlinear skeleton.
The distinction is load-bearing: the stress-free incremental operator and
fixed spatial conductivity are prescribed constitutive assumptions, not
consequences of the measured-film source.

## 1. Derive the normal elastic two-port

Let upward displacement be positive on BOTH faces of an isotropic skin,
`0<z<b`; take a Fourier factor `exp(i q x)`, `q>0`, and plane strain in the
omitted direction. An Airy stress amplitude `Phi` gives

`sigma_xx=Phi''`, `sigma_zz=-q^2 Phi`, `sigma_xz=-i q Phi'`,
`(d_z^2-q^2)^2 Phi=0`.

The plane-strain Hooke relations and shear strain give the vertical
displacement throughout the layer:

`w=(1-nu_p^2) Phi'''/(E q^2)`
`  -(1+nu_p)(2-nu_p) Phi'/E`.

On shear-free faces `Phi'=0`, only the first term remains. Set
`c_e=(1-nu_p^2)/E`, `t=q(z-b/2)`, `ell=q b/2`.
The upward forces conjugate to the two face displacements are

`t_bottom=+q^2 Phi(0)`, `t_top=-q^2 Phi(b)`.

These signs follow from the opposite outward normal VECTORS. Giving both
scalar pressures the same outward sign would produce the wrong stiffness.

For equal upward face displacements, use the odd Airy solution

`Phi=A sinh(t)+B t cosh(t)`,
`A=-B[1+ell tanh(ell)]`.

At the top face,
`Phi=B[-sinh(ell)+ell/cosh(ell)]` and
`d_t^3 Phi=2B cosh(ell)`. The two conjugate face forces are equal, and their
ratio to the common displacement is

`k_plus=q/(2c_e)[tanh(ell)-ell sech^2(ell)]`.

For opposite face displacements, use

`Phi=A cosh(t)+B t sinh(t)`,
`A=-B[1+ell coth(ell)]`.

At the top,
`Phi=-B[cosh(ell)+ell/sinh(ell)]`,
`d_t^3 Phi=2B sinh(ell)`. This gives

`k_minus=q/(2c_e)[coth(ell)+ell csch^2(ell)]`.

Hence the complete normal stiffness in the stated face convention is
`[[a,c],[c,a]]`, with `a=(k_plus+k_minus)/2` and
`c=(k_plus-k_minus)/2<0`. Both eigenvalues are strictly positive.
Indeed `tanh(ell)-ell sech^2(ell)` is the integral of
`2t tanh(t) sech^2(t)` from zero, and `k_minus>k_plus` follows directly.

A positive top foundation adds energy `K_w v^2/2`. Minimizing over `v`
gives exactly

`m=v/h=-c/(a+K_w)`,
`k_eff=a-c^2/(a+K_w)`.

Thus `0<m<1`, `k_eff>0`. If `M_e=1/c_e`, then as `q->0`,

`m->1/(1+K_w b/M_e)`, `k_eff->K_w m`.

For `K_w=0`, the small-q expansion gives
`k_eff=B_plate q^4+o(q^4)`,
`B_plate=b^3/(12c_e)`. For `q b->infinity`,
`m->0`, `k_eff~q/(2c_e)`. These agree with the bending and half-space
limits. The `q->0` plane-strain limit is a long-wavelength limit; an exact
uniform deformation with separately prescribed lateral strain can have a
different zero-mode modulus. The note removes the uniform galvanostatic mode
and uses the limit, so that distinction causes no gap.

## 2. Derive the moving-face ionic transfer

This section assumes the DECLARED spatial constitutive law
`k_n u''-k_t q^2 u=0`, with fixed positive coefficients. Let the flat
potential gradient be `G=j0/k_n`. Evaluating the total potential on the
bottom face `z=h` adds `G h`; evaluating on the top `z=b+v` adds `G v`.
To first order the declared kinetic and top termination laws are therefore

`u0=r j_b+(chi-G)h`, `u_b=W-Gv`,
`j_b=k_n u'(0)`, `j_t=k_n u'(b)`,
`W=-(R+Z_b)j_t-j0 R_v v`.

The fixed upper backing is material here: the variable pore thickness
already lies in `R(d)`. A further geometric bulk-potential term cannot be
silently added or removed without changing that boundary geometry.

Put `p=q sqrt(k_n k_t)`, `C=cosh(q b sqrt(k_t/k_n))`,
`S=sinh(q b sqrt(k_t/k_n))`. Solving the homogeneous ODE gives

`u_b=C u0+(S/p)j_b`, `j_t=p S u0+C j_b`.

Substitute the lower boundary value and add `Gv` to obtain

`W=(rC+S/p)j_b+C(chi-G)h+Gv`,
`j_t=(C+r pS)j_b+pS(chi-G)h`.

Eliminating `W,j_t` and using `v=mh` gives precisely

`j_b/h=[(G-chi)(C+L pS)-m(G+j0 R_v)]`
`       /[rC+S/p+L(C+r pS)]`, `L=R+Z_b`.

The denominator is positive. It has units `ohm m^2`, the numerator has
units `V/m`, and the quotient has units `A/m^3`. At long wavelength,

`D0=r+b/k_n+L0`,
`N0=G(1-m0)-nu_m K_w m0-m0 j0 R_v`.

The residual `G(1-m0)` is real skin-thickness shortening. Replacing the
upper displacement by `h` without mechanical equilibrium would lose it.
Varying the minimized conservative mechanical energy gives the incremental
force `k_eff h`; multiplying by actual metal volume per charge gives the
reaction-voltage shift `nu_m k_eff h`. This explains the mechanical part of
`chi=Gamma q^2+nu_m k_eff`; it is not a free phenomenological sign.

## 3. General all-q certificate and a simpler independent fixture proof

I checked the note's general E6-E7 route. The Mittag-Leffler identity gives

`ell coth(ell)+ell^2 csch^2(ell)`
` =2+4ell^4 sum_(n>=1)(ell^2+pi^2 n^2)^(-2)`.

It proves `k_minus>=2/(b c_e)` and monotonicity. The formula for `m` is
increasing in `k_minus` and decreasing in `k_plus`, so the stated `m_min`
is uniform when its numerator is positive. The integral in Section 1 gives
the stated bending lower bound. Also
`d k_eff/d K_w=m^2`, so integrating the uniform lower bound on `m` gives
the additive `K_w m_min^2` term. Finally, the positive power series of
`H(q^2)` proves the convex chord upper bound. On `chi<G`, both the true
factor `1-chi/G` and its polynomial upper bound are positive, so the
multiplication direction in E7 is correct. For `chi>=G`, negativity is
immediate. This closes all q, not just sampled wavelengths.

I independently established the supplied fixture with coarser rational
inequalities that do not use the owner's Bernstein computation. The complete
proof object is `independent_fixture_certificate.py`; it imports no owner
code. All parameters are supplied design specifications.

Choose `q_bar=22500/m`, so `ell=9/40`. The integral bound `tanh(t)<=t`
implies `k_plus(q)<=B_plate q^4/2`. Together with the lower bound on
`k_minus`, this gives uniformly below `q_bar`

`m>=7993165625/8007986799>99/100`.

With `beta^2=(q_bar b)^2(k_t/k_n)=81/40`, geometric tails of the positive
hyperbolic series give

`cosh(beta)<=1+(beta^2/2)/(1-beta^2/12)=295/133<9/4`,
`sinh(beta)/beta<=1+(beta^2/6)/(1-beta^2/20)=989/719<7/5`.

The exact coefficient multiplying `sinh(beta)/beta` in `H(q_bar^2)` is
`L_max k_n (k_t/k_n)b q_bar^2=6903/5000<7/5`. Hence

`H<=H(q_bar^2)<421/100=4.21`,
`m(1+k_n R_v)>(99/100)(129/25)=12771/2500=5.1084`.

Since `chi>=0`, the first quantity upper bounds the possible positive part
of `N/G`; thus `N<0` on the entire lower interval without even using the
negative bending term there. For the higher interval,

`cosh(ell)<=6535/6373<103/100`,
`k_plus(q_bar)>=[B_plate q_bar^4/2](100/103)^3`.

The latter follows by integrating
`tanh(t) sech^2(t)>=t/cosh(ell)^3`. It gives

`chi(q_bar)/G >1421705427507365949/1180835763464000000>1`.

Monotonicity of `Gamma q^2+nu_m k_plus(q)` closes every higher q. These
two strict rational inequalities independently certify the declared model.

The identical-skin attribution test retains the SAME mechanical foundation,
normal compliance, transport coefficients and base resistance, and sets only
`R_v=0`. At `q=10000/m`, use
`k_eff<=2k_plus+K_w<=B_plate q^4+K_w` and
`tanh(x)>=x-x^3/3` for the actual finite bulk. The independent positive-series
lower bound gives

`(N/G)_ordinary >=421493737070718527/2374435546875000000>0.1775`.

This confirms a sign reversal attributable to the derivative in the declared
model. It is not proof that a physical separator can independently vary
`R_v` while keeping the same `R,K_w`, and it does not compare against every
equally informed conventional architecture. The source mechanism of
pressure-induced pore closure remains an incumbent.

## 4. The paid skeleton and the nonlinear column scope

For the supplied incompressible-pillar ansatz, `d=d0-v`, constant solid
volume per cell area `s`, and `lambda=d/d_ref`, direct differentiation gives

`R=d^2/[k_l(d-s)]`,
`R_v=[s^2/(d-s)^2-1]/k_l`,
`E_s=s mu_s[lambda^2+2/lambda-3]/2`,
`p_s=(s mu_s/d_ref)(lambda^(-2)-lambda)`,
`K_w=(s mu_s/d_ref^2)(2lambda^(-3)+1)`.

The range `s<d<2s` gives positive resistance feedback during plating.
The mechanical work and stiffness are thus charged. Drainage, fixed cell
area, stable pillars, attachment and continuous film contact remain physical
requirements; incompressibility alone does not acquire them.

For the DISTINCT local column law, let `Z=Y^(-1)`, let `D_i>0` be actual
kinetic secants, and put `K=Z+diag(D)`. On the mean-zero height subspace,
galvanostatic elimination yields exactly

`delta j=-A grad F`,
`A=K^(-1)-K^(-1)1 1^T K^(-1)/(1^T K^(-1)1)`.

Here `A1=0` and `A` is positive on `1-perp`; its restriction is the inverse
of `P K P` there. Therefore `A>=1/K_max` on that subspace if
`D_i+||Z||<=K_max`, and

`Fdot=-nu_m grad F^T A grad F<=0`.

The condition `P grad E_mech(0)=0` is needed to make the flat reference
stationary, with `F(0)=min F=0`. With restricted Hessian `>=alpha>0`,
`||P grad F||^2>=2alpha F`, which gives E12 and the invariant sublevel
`F_initial<alpha a^2/2` inside `|h_i|<a`. Strong convexity alone would
not put the minimum at zero; the owner has explicitly added this condition.
For signed operating currents the resistance contribution to the Hessian is
`inf_h[j0 R_tot'(h)]`; the shorthand `j0 inf R_tot'` used in the plating
scope presumes `j0>=0`.

For the quadratic mechanical energy in the note, the spectral minimum of
`A0 lambda+nu_m B_plate lambda^2`, `lambda>=0`, is bounded below by
`-max(-A0,0)^2/(4nu_m B_plate)`. Thus its stated sufficient alpha and the
signed thin-plate buckling threshold have the right constants. None of this
derives the local column law for a laterally conducting moving skin. The
note properly retains that distinction; a linear E4 stability certificate
cannot substitute for a nonlinear free-boundary basin.

## 5. Physical constitutive boundary and strongest retained explanations

The fixed diagonal transport tensor is an explicit Eulerian constitutive
law. It is not automatic when anisotropic material axes rotate. For
`K0=diag(k_t,k_n)` and small physical rotation
`theta=(partial_x w-partial_z u_x)/2`, rotation alone gives

`delta K_xz=(k_t-k_n)theta`,
`k_n u''-k_t q^2 u=-i q G(k_t-k_n)theta`.

Stretch-dependent conductivity may add more terms. Those are first-order
effects at the declared anisotropy ratio 10. The owner has now stated that
E4 excludes them and is separately constructing that different law. This
review does not inherit or certify the owner's new convected-axis work.

Likewise the skeleton's nonzero normal preload passes through the skin.
The exact incremental operator of a finitely loaded body can include
initial-stress, deformed-boundary traction and tangent-modulus corrections.
`p_s/E` about `6.7e-5` suggests a small scale but is not a uniform error
bound on the coupled instability calculation. E1 is exact as its prescribed
unstressed linear boundary-value problem, not yet the acquired tangent of
this loaded material. This qualification is not a proof of physical
instability.

I personally read the relevant actual primary Li3N film source,
[Li et al. 2018](https://doi.org/10.1021/acscentsci.7b00480), including its
mechanical and conductivity sections. It explicitly attributes bending
robustness to cooling-induced compression. Its liquid-cell 20-micrometre
normal-conductivity measurement and 200-micrometre solid fixture are
different operations. They do not provide this synthetic film's same-state
elastic tensor, in-plane ionic conductivity, preload tangent or shear-free
substrate boundary law. The model should not be assigned to that film.

Pressure-induced pore closure, ordinary conservative elastic stabilization,
chemical levelers and contact/creep are competent existing explanations;
the conditional sign attribution does not exclude them. On the precise
declared model the proof passes. Physical conjunction, finite-amplitude
continuum-skin leveling and reversible cycling remain unacquired.
