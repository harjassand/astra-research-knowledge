# A local two-network construction for passive finite-scale phase separation

24 October 2026. Sol's next physical construction after the frozen
q/Klein–Gordon unit. No continuation of that model and no new numerical
fixture, material experiment, purchase, outreach or export.

Frozen after the root consequential proof check: PASS at the literal
periodic, mean-zero finite-model scope, supported by the bounded checks
identified below. This is internal checking, not external certification,
novelty clearance, a finite-temperature theorem or material validation.

The scientific need is to retain finite-scale composition structure while
all regions can exchange material. A growth-rate maximum at a finite
wavenumber alone does not answer this need: ordinary spinodal decomposition
also starts with a finite fastest mode and later coarsens.

Three routes were compared. Chemical reaction-maintained droplets consume
chemical free energy continuously. A single strain-stiffening network has
strong existing elastic-arrest and viscoelastic-ripening precedents. The
selected construction instead uses a second passive elastic displacement
field and local connections between the two networks. Its target is an
explicit local energy that, after relaxation, has a finite-scale equilibrium
preference and compatible finite-rate passive dynamics.

## 1. Strong ancestry and the literal question

[Qiang, Luo and Zwicker, PRX 14, 021009 (2024)](https://doi.org/10.1103/PhysRevX.14.021009)
already explain equilibrium elastic microphase patterns using nonlocal
elasticity. Their supplementary derivation includes finite-separation
positive spring interactions and a Gaussian-chain endpoint network. Thus
neither passive equilibrium patterns nor positive-spring ancestry is new
here. Their chosen Fourier kernel is Gaussian, rather than the rational
screened kernel below. Their paper references the experimentally observed
reversible, cooling-rate-independent structures in swollen PDMS.

Screened repulsion competing with interfacial energy is also established;
for example [Fall's primary pattern analysis](https://arxiv.org/abs/1711.10825)
constructs periodic stationary sets for a surface-plus-Yukawa energy.
We do not claim a new screened-pattern principle or infer a new material
from a kernel representation. The bounded question is whether one can
derive the kernel from a fully specified **local** positive mechanical
model, then establish a nonlinear finite-scale statement using that same
model's dynamics and boundary conditions.

The local mechanism and calculations below are Sol's construction. The
bounded source comparison is in
`luna_random_lag_sources/PRIMARY_PRIOR_NOTE.md`; it is not global novelty
clearance. Its IPN predecessor reports crosslinking/topological frustration,
not this exact equilibrium two-field elimination.

## 2. One specimen contract and an explicit positive-spring model

Start in one spatial dimension. The composition/order parameter `phi` is
a signed deviation from its specified mean, with
`integral_0^L phi dx=0`. Displacements `u,v` describe two distinguishable
networks. All three fields are periodic; mean strains are zero and the
common rigid translation is fixed as a gauge. The specimen length is fixed.
The coordinate is a fixed reference coordinate and the conserved amount
is per reference cell. A finite-strain swelling model would need its
Jacobian and transport law; it is not identified with this small-strain
chemoelastic model.

The exact continuum model is

```
F[phi,u,v] = integral_0^L {
 a phi^2/2 + b phi^4/4 + kappa phi_x^2/2
 + C(u_x−alpha phi)^2/2 + D v_x^2/2 + K(u−v)^2/2
} dx,
```

with `b,kappa,C,D,K>0`. Only the mixing curvature `a` may be negative.
The `alpha phi` term is a supplied chemoelastic natural-strain coupling,
not a reprogrammable actuator. Both network energies and the relative
connection energy are positive. The second network and all connections
are part of the specimen inventory.

There is also an exact finite lattice version, so a continuum truncation
is not being used to hide a high-wavenumber instability. On `N` periodic
sites of spacing `h`, take node variables `u_i,v_i` and bond variables
`phi_i`, with zero mean `phi`. Its energy is `h` times the sum of

```
a phi_i^2/2+b phi_i^4/4
+kappa (phi_i−phi_(i−1))^2/(2h^2)
+C[(u_(i+1)−u_i)/h−alpha phi_i]^2/2
+D[(v_(i+1)−v_i)/h]^2/2+K(u_i−v_i)^2/2.
```

This finite-dimensional positive-spring/phase-field Hamiltonian is the
owned exact model. A leading-order material interpretation is two
longitudinal bars or networks joined by a shear-compliant layer, with
`K=G_layer*width/thickness`. A vertical unstressed pin-ended axial rung
does **not** give this longitudinal harmonic stiffness: its extension is
quadratic in the relative longitudinal motion. The scalar coupling may
not be silently identified with such a rung. Layer axial/bending terms,
interfaces, frame constraints, physical `alpha` and actual gel constitutive
calibration remain unacquired; no material realization is asserted.

## 3. Exact elimination and the mean-mode distinction

For each nonzero continuum wavenumber `k`, the mechanical quadratic block
has diagonal factors `C k^2+K`, `D k^2+K` and off-diagonal `−K`. Its
determinant is

```
k^2[K(C+D)+CD k^2]>0.
```

First `v=K u/(K+Dk^2)`. Eliminating both displacements leaves

```
F_eff[phi] = integral(a phi^2/2+b phi^4/4+kappa phi_x^2/2)
            + (E0/2) <phi,(1−xi^2 partial_xx)^−1 phi>,

E0=alpha^2 CD/(C+D),
xi^2=CD/[K(C+D)].
```

The elastic quadratic Fourier coefficient is exactly
`E(k)=E0/(1+xi^2 k^2)`. The inverse is on the periodic mean-zero sector.
The real-line version has the positive exponential kernel
`exp(−|x|/xi)/(2xi)`. This interaction is obtained by minimizing positive
local mechanical energies, not imposed as a negative spring or an active
controller. The hidden relative displacement supplies a measurable length.

The exact lattice calculation has the same formula with
`k^2` replaced by `q_h(k)=4sin^2(kh/2)/h^2`. The bond/node phase factor
does not change this quadratic coefficient. Only the actual discrete
wavenumbers are admissible; a continuum optimum beyond the Brillouin zone
cannot be claimed as a physical pattern. The elimination was independently
checked in `luna_resolvent_algebra/ELIMINATION_AUDIT.md`.

The exact uniform mode is **not** inferred from the limit of nonzero modes.
Under strictly periodic fixed-length displacements its elastic coefficient
would be `C alpha^2`, since a uniform eigenstrain cannot be relieved by
an affine stretch. If a common affine strain is allowed and minimized,
the coefficient becomes `E0`. Here the mean composition is fixed to zero,
so the exact uniform mode is absent; all long-wavelength comparisons use
the same fixed-length, mean-zero contract. Thus `E0` below is the
`k->0`, `k!=0` limit, not an unnoticed change to free boundaries.

## 4. An explicit finite-wavelength sector

The relaxed quadratic coefficient is

```
lambda(k)=a+kappa k^2+E0/(1+xi^2 k^2).
```

There is a nonzero minimizing wavenumber exactly when `E0 xi^2>kappa`:

```
k_*^2=[sqrt(E0 xi^2/kappa)−1]/xi^2,
lambda_min=a+2sqrt(E0 kappa)/xi−kappa/xi^2.
```

Consequently the open interval

```
−E0<a<kappa/xi^2−2sqrt(E0 kappa)/xi
```

has `lambda(0+)=a+E0>0` and `lambda_min<0`. Its width is
`(sqrt(E0)−sqrt(kappa)/xi)^2>0`. There is a bounded negative band
`B={k:lambda(k)<0}`, separated both from zero and from infinity.

The limits are useful controls. For `K->infinity`, the relative motion is
locked, `xi->0`, and the coefficient tends to the local positive shift
`E0`; in the stated sector the uniform mixture is stable. For `K->0` at
any fixed nonzero `k`, the elastic penalty vanishes and ordinary coarsening
is recovered. The `K->0`, `k->0` and sample-size limits do not commute.
Any finite sample must contain admissible modes in the negative band.

This calculation identifies an instability but is not yet equilibrium
selection. The next argument supplies the nonlinear statement.

## 5. A nonlinear finite-band bound, not just a dispersion maximum

Normalize Fourier coefficients so that
`sum_k |phi_hat(k)|^2=(1/L)integral phi^2`. Let
`mu=−min_{allowed k} lambda(k)>0`, and denote the mean-square mass in
the negative band by

```
m_B=sum_{lambda(k)<0}|phi_hat(k)|^2.
```

The positive part of the quadratic energy can be dropped, and Jensen
gives `average(phi^4)>=average(phi^2)^2>=m_B^2`. Therefore, for every
configuration,

```
F_eff/L >= −mu m_B/2+b m_B^2/4.
```

An allowed cosine mode with `lambda(k_t)=−nu<0` has energy density
`−nu A_t^2/4+3b A_t^4/32`. Minimization gives

```
A_t^2=4nu/(3b),   F_trial/L=−nu^2/(6b)<0.
```

For the lattice use a mode whose second and fourth harmonics do not alias
to the zero mode; such modes are available in the continuum-resolved
large-sample regime. Otherwise use its actual discrete fourth moment
instead of `3/8`.

If `F_eff/L<=−q<0`, the preceding lower bound requires

```
m_B >= [mu−sqrt(mu^2−4bq)]/b >0.
```

The square root is real for every such configuration because the same
quadratic lower bound is at least `−mu^2/(4b)`. Total mean-square
amplitude is bounded as well: with `P=average(phi^2)`,
`F_eff/L>=−mu P/2+bP^2/4`, so a negative energy implies `P<2mu/b`.
There is thus a strictly positive fraction of spectral power in a band
bounded away from zero whenever the negative energy-density gap is fixed.

For a global minimizer the cosine trial supplies `q=nu^2/(6b)`. In a
sequence of larger specimens with an allowed mode approaching `k_*`,
`nu` tends to a fixed positive value and the lower bound is uniform in
sample length. A minimizing sequence cannot move **all** composition
contrast to wavenumber zero or into a single macroscopic domain.

This is the actual equilibrium conclusion. It does not prove a unique
period, a striped ground state, a droplet shape, absence of mixed
morphologies, or that every initial condition finds the global minimum.
Partial coarsening of defects or coexistence with other structures remains
possible. It also does not give a uniform claim as the negative density
gap vanishes at onset. The argument and its qualifications were
independently checked in
`luna_single_port/ENERGY_SPECTRAL_WEIGHT_AUDIT.md`.

There is an operational version. For an actual nonrelaxed configuration,
`F_eff(phi)<=F(phi,u,v)`. If a passive trajectory has reached
`F/L<=−q<0`, energy monotonicity gives the **same finite-band lower bound
for every subsequent time**. It therefore supplies a deterministic
retention statement for finite-scale composition content, without
assuming convergence or mechanically instantaneous motion. The inputs
include the negative-energy initial state or an observed crossing of that
sublevel; an exactly homogeneous unseeded deterministic state does not
start moving by itself.

## 6. Compatible finite-rate dynamics

Use conserved diffusion in the composition field and finite drag for
both mechanical fields:

```
mu_chem=a phi+b phi^3−kappa phi_xx−C alpha(u_x−alpha phi),
phi_t=M partial_xx mu_chem,
Gamma_u u_t=C partial_x(u_x−alpha phi)−K(u−v),
Gamma_v v_t=D v_xx+K(u−v),
```

with finite `M,Gamma_u,Gamma_v>0`. At fixed model parameters,

```
dF/dt=−M integral |partial_x mu_chem|^2
      −Gamma_u integral |u_t|^2−Gamma_v integral |v_t|^2 <=0.
```

The exact lattice uses conservative difference fluxes and the same
positive-gradient descent for `u,v`. It conserves the composition sum,
has a coercive quartic energy modulo common translation, and its finite
ODE exists on bounded energy sublevels. The sublevel retention statement
in Section 5 is therefore an actual property of the owned finite-rate
model.

For each allowed nonzero mode its full linear generator is `−Mob_k H_k`,
with positive diagonal mobility and the full three-field Hessian. It is
similar to the Hermitian matrix `−Mob_k^(1/2)H_k Mob_k^(1/2)`. Since the
mechanical block is positive definite, a negative Schur complement
`lambda(k)` makes the full Hessian indefinite and gives a positive real
growth eigenvalue for **any** finite positive rates. The actual rate is
not the quasistatic rate and may be arbitrarily slow. No fast-mechanics
limit is needed for the sign or for the nonlinear energy-retention result.

Conversely `lambda(k)>0` for every allowed nonzero mode makes the
homogeneous Hessian positive on those modes. The common translation and
the exactly conserved composition mean remain separately excluded zero
modes. This was checked in
`luna_boxcar/FINITE_RATE_COMPATIBILITY.md`.

## 7. Why an extra displacement field changes the locality question

There is a simple scoped obstruction for one-field local elasticity. Let
its one-dimensional energy be

```
F1=integral[f(phi)+kappa phi_x^2/2+W(u_x,phi)] dx,
```

with the same prescribed mean composition/mean strain and no other
length-bearing term. This includes nonlinear local elastic laws `W`;
convexity of `W` is not needed for the following comparison. Dilate an
admissible periodic pattern by factor `ell>1`:

```
phi_ell(x)=phi(x/ell),  u_ell(x)=ell u(x/ell).
```

Both means and the local strain distribution are unchanged. Per unit
length the `f+W` energy is unchanged, while the capillary-gradient energy
is divided by `ell^2`. Repeating the dilated cell inside larger commensurate
specimens gives a strictly lower density for any nonconstant smooth
pattern. More literally, if the original cell has period `p`, compare its
`m*ell` repetitions with `m` repetitions of the dilated cell in the **same**
specimen of length `m*ell*p`, taking integer `ell>1`. Their composition
inventories and mean strains coincide; the latter has lower total energy.
Thus the comparison does not switch the specimen's mechanical contract.
Such a model cannot select a global optimal finite period
independent of sample size. Local kinetic traps are not excluded.

Two fields with energies depending only on their gradients have the same
dilation issue. In the selected construction the relative displacement
term `K(u−v)^2` breaks that scaling: maintaining the same strains while
dilating would multiply this part of the density by `ell^2`. It provides
the internal transfer length `xi` without a long-range spring being
postulated. Thus “local elasticity” must specify its retained fields and
connections; a one-deformation-field locality obstruction does not apply
unchanged after an internal displacement mode is introduced and relaxed.

This is a representation distinction within conventional screened
frustration physics. Higher strain gradients, finite-range network bonds,
anchored substrates and other known length-bearing mechanisms also evade
the displayed one-field premises. No general claim that local materials
cannot pattern is intended.

## 8. Preparation, full return, measurements and remaining material gate

A compatible model operation is a uniformly mixed two-network sample,
with fixed mean composition and fixed length, brought into the specified
phase-separating parameter sector. A small finite-band composition seed
and relaxed `u,v` can be chosen with negative density using the cosine
construction. Alternatively the energy condition can be verified after
initial growth. This is an explicit input condition, not a guarantee that
an arbitrary noisy quench produces a particular structure.

For a physical mixture the mixing curvature, capillarity, selective
swelling coefficient and two-network mechanics must be independently
calibrated. Model predictions include `E0,xi` from `C,D,K,alpha`, relaxed
mechanical transfer `v_hat/u_hat=K/(K+Dk^2)`, and the finite spectral band.
Composition imaging/scattering gives `|phi_hat(k)|^2`; relative-network
displacement/strain readout tests the separate internal mode. A fitted
structure factor alone does not identify that mechanism: Gaussian or
other screened/nonlocal models are strong conventional alternatives.

A useful matched constitutive control is visible without assigning
fictitious material numbers. For common uniform strain `e`,

```
C(e−alpha phi)^2/2+D e^2/2
 =(C+D)(e−C alpha phi/(C+D))^2/2+E0 phi^2/2.
```

This bulk quadratic response is independent of `K`, while the finite-wave
kernel and instability sector depend on `K`. A sufficiently strongly
coupled two-network model is homogeneous in the stated sector; a weaker
finite coupling can admit the negative finite band with the same `C,D,
alpha,a,b,kappa`. Thus bulk modulus and uniform response alone do not
establish the internal relaxation mechanism. Changing a real coupling
layer can also change mass, failure, transport and other parameters;
those are comparison costs, not assumed equal merely because the model
holds its other coefficients fixed. The already demonstrated nonlocal-gel
incumbent remains stronger than an unbuilt two-network material proposal.

The construction's extra network, shear connections, any frame/clamp,
solute inventory, preparation temperature/interaction change and reset
are all resources. For an isothermal externally varied parameter model,

```
dF/dt=W_param−dissipation,
W_param= a_dot integral phi^2/2+K_dot integral (u−v)^2/2
```

when only `a,K` are changed. Returning both state and control parameters
requires net control work equal to the dissipated amount. A physical
temperature quench additionally requires heat/entropy and bath accounting;
it cannot be declared free from this isothermal identity. No device
efficiency or full-cycle energy saving has been computed.

The deterministic mean-field dynamics omits thermal fluctuations. At
finite thermal noise the trajectory energy need not be monotone; the
all-time pathwise sublevel result is not automatically a finite-temperature
retention theorem. Nor does a one-dimensional model establish true
long-range periodic order at nonzero temperature. Large strains, network
creep, damage, interfacial failure and component transport can change the
energy itself; none has been silently included through arbitrary fitted
constants.

The bounded achievement is an exact local positive mechanical model with
an explicit screened relaxation kernel, a nonlinear finite-band energy
and passive finite-rate retention statement, and a transparent one-field
scaling obstruction. Broad pattern physics is established ancestry;
novelty and any actual two-network material advantage remain unestablished.
The accepted source is frozen; later material/representation investigations
must preserve these hypotheses and cannot silently extend this result.
