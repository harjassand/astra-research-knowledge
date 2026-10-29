# Connected diffusion consequence: derivation and physical scope review

29 October2026. Existing Astra P1 physical-mechanism role.

Reviewed file: CONNECTED_DIFFUSION_AND_LOCAL_FACTOR_PROGRAMS.md.
SHA256: 2bd97eae8661a6eebf1af4ddcce1fef84ac3e439876dc5aa14b5f7979f8618ef.
An exact snapshot is preserved beside this review. I also reread the inherited
SMOOTHING_OBSTRUCTION_AND_CONSEQUENCE_SCOPE.md and opened both primary papers
cited by the consequence. This review adds no fixtures or new workers.

## Verdict and one operator-domain clarification

The construction is mathematically sound with the NATURAL CONORMAL reflecting
boundary condition n dot A_i grad_i f=0. It gives a genuine continuous hidden
mathematical family with common sectorwise baseline sign law, exact local
target invariance, and no finite native predictive closure requirement.
Its physical resource and preparation qualifications are appropriate.

Please make that conormal boundary condition explicit. For a general positive
definite matrix with cross terms, merely writing 'reflecting x_i boundaries'
can also mean normal Skorokhod reflection, whose generator domain has
partial_(x_i)f=0. That boundary condition does NOT generally justify the
self-adjoint integration-by-parts identity in equation2. The intended
divergence-form/conormal realization is an entirely valid supplier; this is
a request to specify it, not to change the central mechanism.

Concrete distinction: take U=0 on[-1,1] times a2pi-periodic coordinate z,
and constant A=[[1,a],[a,1]],0<|a|<1. If ordinary normal Neumann conditions
f_x=0 are imposed, the interior generator is

    L=partial_xx+2a partial_xz+partial_zz.

Both f(x,z)=cos z and g(x,z)=sin(pi x/2)sin z satisfy those normal boundary
conditions. For normalized uniform mu,

    <f,Lg>_mu=a,             <Lf,g>_mu=0.

Thus normal reflection is not the claimed reversible realization. Conormal
conditions remove the boundary flux and recover the displayed Dirichlet
form. In the Ito description, the interior drift remains div A-A grad U
and noise covariance2A; the reflected SDE additionally needs its corresponding
conormal boundary term. A diagonal/no-normal-cross-term A would be another
valid restricted supplier, but no such restriction is necessary if the
natural conormal domain is stated.

## 1. Baseline signs and hidden coordinates

Each independent sign flip of x_i preserves Lebesgue measure and U_h.
The group of2^d flips therefore maps all orthants to each other with equal
mu_h mass. The zero hyperplanes are null because the density is smooth,
finite, and positive. Hence the joint visible sign law is exactly uniform
for every h. This does not require estimating U_h or its normalization.

The same argument works conditionally on all inactive coordinates and z:
the two signs of the active coordinate have equal conditional baseline mass.
The hidden magnitudes may remain strongly coupled to each other and to z;
their effect on transient sign kinetics can be arbitrarily complicated.
The lack of sign symmetry in A_i is harmless for the invariant law when
the complete divergence drift and the correct reflecting domain are kept.

## 2. Native operation and compiled factor law

At fixed h and inactive coordinates, the active leaf is the compact connected
cylinder[-1,1] times the z torus. Smooth uniform ellipticity and the natural
conormal/periodic domain give the stated symmetric nonpositive Dirichlet
form and L_i1=0. The fixed-time kernel therefore preserves the conditional
Gibbs density, and integrating over the inactive coordinates gives the common
mu_h. No kinetic prefactor needs to be estimated for that structural identity.

During update i, all factors not involving i are constants. The positive
rational product of incident factors gives exactly the desired local ratio;
clearing denominators does not change it. The counter's conditional balance
on each inactive-coordinate slice multiplies to the global full-state law
nu_h proportional to W(Y)mu_h. Fixed scans and independently chosen random
scans then preserve the same law. Arbitrary history-selected actuation is
not supplied by this argument.

Uniform baseline signs imply mu_h(W)=2^-d sum_y W(y), independent of h.
Consequently every h-sector has the same visible target. Retained records
can change sector weights without changing that common visible equilibrium,
provided the needed conditional within-sector convergence actually occurs.
This does not imply a uniform preparation time over h: the allowed mobility
can approach zero across sectors. Baseline initialization, conditional starts,
and convergence remain separate resources as the manuscript states.

The finite-factor statement concerns POSITIVE factors. Zero-weight hard
constraints are outside its finite-ratio premise. The phrase 'constraint/
factor models' should be understood as positive or softened constraint
factors; it does not add an exact hard-zero compiler.

## 3. Resource and phase-regime statements

For energy measured in units log2, the binary local ratio is
2^{|Delta_i E|}. The inherited binary compiler supplies the stated native-
call cap and finite residual-selector bits, while context sensing and
computation are additional. Equal conditional baseline sign masses give
2r/(1+r) as a target-stationary mean, even with evolving shared z; no
pointwise all-start or preparation bound follows from that average.

On a degree-four square lattice the neighbor sum is0,+/-2,+/-4, giving
local ratios1,16,256 for W=2^{sum s_i s_j}. The conversion from the cited
q=2 Potts critical point to the Ising coupling is correct: using
1_{s_i=s_j}=(1+s_i s_j)/2 gives K_c=(1/2)log(1+sqrt2), below log2.
This identifies a noncontractive/ordered family; it does not solve its
phase barriers. Boundaries of a finite open lattice have other degrees and
can have additional local ratios, so the stated set applies to the usual
degree-four bulk or periodic lattice.

## 4. Smoothing and actual physical scope

The inherited obstruction applies on each active connected leaf: the native
positive-time elliptic semigroup is smoothing and injective, while the sharp
sign indicator is nontrivial. It therefore cannot preserve a finite bounded
feature space containing that readout. For a proposed global finite space,
one can disintegrate its finitely many invariant-basis identities onto almost
every inactive-coordinate slice and obtain the same contradiction. No claim
of global strong Feller behavior across physically frozen coordinates is
needed.

The stopped endpoint kernel need not inherit the native smoothing property.
Thus its piecewise weighted invariant density is compatible with the
obstruction. Correct target invariance requires neither a finite predictive
model nor hidden resetting. It also does not establish finite predictive
rank for the compiled process; the separate frozen-continuum example
already exhibits exact target control with infinite predictive rank.

The supplier is a fully specified mathematical controlled diffusion once
its reflecting domain is explicit. It does not acquire an actuator capable
of fixing the other coordinates, a noninvasive exact sign sensor, controller
timing, or finite-resolution error bounds. Those remain explicit model
controls. Repeated use of one P leaves its raw path and native occupation
unchanged; local scheduling creates a different actuation program whose
wall-time law still requires separate analysis. No physical apparatus,
sampling speedup, or free preparation has been demonstrated.

## Primary-source check

Lau and Lubensky, arXiv0707.2234, primary abstract read: it supports the
need for the convention-dependent drift associated with state-dependent
diffusion. The multidimensional Ito drift used here also follows directly
by expanding the displayed divergence-form generator; no unseen boundary
theorem from that paper is used.

Beffara and Duminil-Copin, arXiv1006.5073, primary abstract read: it states
the square-lattice random-cluster critical point and corresponding Potts
relation. The factor-of-two conversion above is explicit reasoning from
the Ising/Potts identity. No hardware or mixing-time claim is imported.
