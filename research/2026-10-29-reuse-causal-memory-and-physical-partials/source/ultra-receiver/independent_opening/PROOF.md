# A query-first radial-blur invariant for particle-motion currents

Private constructive investigation, 29 October 2026. This is a conditional
mathematical acquisition operation. No torque measurement, new optical access,
historical novelty or practical advantage is claimed. The public-data consumer
and its source qualifications are separate from the theorem.

## 1. Question and strongest ordinary starting point

Can one acquire a mechanically meaningful quadratic motion query directly from
raw particle images, without first estimating a velocity field, a particle-image
diameter, or the full displacement distribution? Pressure-free force identities,
virtual-work fields, single-pixel PIV/Reynolds-stress inference and holomorphic
blur-invariant moments already exist. They are the ordinary starting point, not
results invented here. The construction below combines their query-first
viewpoints and discriminates which virtual loads are compatible with exact
radial-blur invariance.

The native output is a finite-lag displacement current. Converting it to a
hydrodynamic torque requires the additional conditions in section 7. The
translational-force counterpart fails within the stated harmonic-field package.

## 2. Classification of the blur-compatible quadratic query

Identify R^2 with C. Let S(x) be a C^2 real symmetric 2-by-2 matrix on a domain
not containing its singularities, and put

    f(x,y) = (y-x)^T S(x) (y-x).

For every x,y in an open product domain, invariance under every sufficiently
small radial probability perturbation of x and y, independently, holds if and
only if f is harmonic separately in x and y. Necessity follows by using uniform
probability on circles of radius t and the expansion

    average_circle f = f + t^2 Delta f/4 + o(t^2).

Sufficiency is the harmonic mean-value theorem, followed by integrating over
the radial distribution of the perturbation. It requires the entire supporting
disk to lie in a harmonic neighborhood. It is not a statement about arbitrary
unknown support or about kernels crossing a pole.

Writing D=y-x gives the literal identities

    Delta_y f = 2 tr S,
    Delta_x f = D^T (Delta S) D - 4 (div S) . D + 2 tr S.

Since D ranges over an open set, separate harmonicity is equivalent to

    tr S = 0,       div S = 0,       Delta S = 0.                 (2.1)

In two dimensions the last condition follows from the first two: for
S=[[a,b],[b,-a]], the equations a_x+b_y=b_x-a_y=0 are the Cauchy--Riemann
equations for a-i b. Thus this is the space of holomorphic quadratic
differentials, expressed in real coordinates.

If S=sym grad w and div w=0, then div S=Delta w/2. Therefore a solenoidal
virtual field is compatible precisely when it is also componentwise harmonic.
This classification concerns this quadratic-query family, not every possible
image estimator or mechanical experiment.

## 3. Annular load: rotation works, translation does not

On a<|x|<R define J(x1,x2)=(-x2,x1) and

    beta = a^2 R^2/(R^2-a^2),       alpha = -a^2/(R^2-a^2),
    w(x) = (alpha + beta/|x|^2) Jx.

Then w=Jx at the inner circle and w=0 at the outer circle; direct
differentiation gives div w=Delta w=0. Its symmetric gradient S satisfies

    D^T S(z) D = -beta Im[D^2/z^2].                            (3.1)

For a translating inner boundary, w=e1 at r=a and w=0 at r=R, the unique
componentwise harmonic Dirichlet solution is

    w(x) = (log(R/|x|)/log(R/a), 0).

Its divergence is -x1/(|x|^2 log(R/a)), which is not identically zero. Thus no
componentwise harmonic solenoidal field has those full Dirichlet data. This
excludes universal radial-blur invariance for that virtual-field translation
load. It is neither an impossibility of force measurement nor an obstruction
to calibrated PSF corrections, pressure-free formulas or more general queries.

## 4. Exact image-blur identity and its support contract

For z != 0 and an endpoint zeta define the real kernel

    K(z,zeta) = -beta Im[zeta^2/z^2 - 2 zeta/z]
              = -beta Im[(zeta-z)^2/z^2].                      (4.1)

Let xi,eta be independent radial random vectors, independent of the particle
pair. Assume |xi|<=rho<|z| almost surely and that the start-blur disk lies in
the accessible harmonic neighborhood. The endpoint blur has finite second
moment. Radial symmetry implies E eta=E eta^2=0, using complex squares, so

    E_eta[(zeta+eta-z-xi)^2/(z+xi)^2]
      = (zeta-z-xi)^2/(z+xi)^2.

As a function of xi the right side is holomorphic throughout the disk |xi|<=rho.
Its radial average is its value at zero. Therefore

    E K(z+xi,zeta+eta) = K(z,zeta).                            (4.2)

The start and endpoint PSFs need not be equal or Gaussian and their radial
profiles need not be known. Their independence, radiality, moment and support
conditions are real inputs. A PSF with support crossing z+xi=0 is excluded:
the holomorphic mean-value argument fails and the integral can fail absolute
integrability. A square pixel is not silently treated as a radial PSF.

## 5. Connected raw-image covariance and real query count

One sufficient acquisition model is a Poisson point process of matched
particle pairs (x_j,y_j) with finite positive intensity measure nu(dx,dy).
Each carries marks B0_j,B1_j, independent across particles and independent of
the positions, with finite second moments and finite positive mixed moment
m01=E B0 B1>0. In particular their first moments and absolute mixed moment
exist. Images are sums of the corresponding PSFs plus deterministic
backgrounds and independent between-frame zero-mean electronics. Assume all
displayed weighted random image sums lie in L^2, so their means and
covariances exist; finite m01 alone would not imply this. For weighted image
sums A=integral a I0, B=integral b I1, the Poisson covariance identity gives

    Cov(A,B) = m01 integral E[a(x+xi)b(y+eta)] nu(dx,dy).         (5.1)

This is a positive pair measure before the signed query weights are applied.
For a common random flow and Poisson seeding conditional on that flow, the
same identity holds after averaging only if the conditional image means do
not add an unqualified between-flow covariance. Uniform seeding transported
by a volume-preserving flow on the full observed particle domain is one
sufficient condition. Arbitrary illumination, finite-field entry/exit,
common pulse-gain fluctuations, correlated electronics, non-Poisson seeds,
camera nonlinearity/saturation, tracer inertia and out-of-plane loss require
extra calibration or bounds.

Use complex bilinear covariance Cov(A,B)=E[(A-EA)(B-EB)], without conjugation.
With A_k=integral z^(-k) I0 and B_k=integral zeta^k I1, the unnormalized query is

    Q = -beta Im[ Cov(A_2,B_2) - 2 Cov(A_1,B_1) ].             (5.2)

It uses TWO COMPLEX covariances. For the real torque-shaped functional,

    Im Cov(A,B) = Cov(Re A,Im B) + Cov(Im A,Re B).

Thus (5.2) needs FOUR REAL covariance measurements, not two or three.
An optional normalization N=Cov(integral I0,integral I1) adds one real
covariance: FIVE real covariances in total. Each frame pair needs four real
Laurent-weighted start sums and four real polynomial endpoint sums. Totals
add two more real sums, giving ten real weighted sums per pair. The empirical
covariance coefficients can be accumulated with constant memory after these
sums. No full image-pair covariance tensor need be materialized.

If both frames capture the complete matched particle population and the
background/electronics conditions hold, N=m01 nu(total), so Q/N acquires
the normalized finite-lag current independently of the unknown particle
density and common mixed brightness mark. This cancellation does not apply
automatically to field-of-view losses or a changing observed particle domain.

## 6. Finite aperture, tails, pixels and empirical arithmetic

### 6.1 A qualified tail repair

Suppose every true pair is in declared guard regions. Let the independent
radial PSFs have calibrated tail probabilities epsilon0,epsilon1 outside
declared radii, and let epsilon=epsilon0+epsilon1<1. On the good event both
blurs stay within those radii, the start disk avoids the pole, and both camera
apertures capture the entire blurred pair. Truncating a radial law to a disk
preserves radiality; hence the normalized good conditional query is exactly
the unblurred query. The good-event probability pG is independent of the
true pair and is at least 1-epsilon.

Implement a bounded query on the visible pixels, with |K_obs|<=M. Assume
|K_true|<=Mtrue on the declared true pair domain. Write the observed positive
normalizer mass as pG+q after normalizing the full pair measure to one, with
0<=q<=epsilon. Its numerator is pG F + b with |b|<=q M and |F|<=Mtrue.
Therefore

    |(pG F+b)/(pG+q)-F|
          <= epsilon (M+Mtrue)/(1-epsilon).                    (6.1)

This controls the normalized population query. It does not estimate epsilon
from the same finite aperture. An arbitrary unknown tail can be invisible
outside the camera; no finite aperture alone certifies (6.1)'s input.

The guard condition does not silently cover all fluid adjacent to a wall or
an optical obstruction. If true particles in a boundary strip are excluded,
their query mass must be bounded separately. For known uniform spatial
seeding and a supplied speed bound U, the omitted instantaneous mechanical
integral over a strip E is at most U^2 integral_E ||S(x)|| dx. Its area being
small does not itself bound a high-shear contribution without such an input.
Radial shift-invariant imaging near an occluding wall is also not automatic.

### 6.2 Deterministic integrated-pixel bound

Root independently supplied the derivative interface in
../root_raw_image_query/PIXEL_INTERFACE.txt. Whole differentiation checks:
on true-to-pixel-center segments with |x|>=a0>0 and |y|<=b0,

    Lx=2|beta|(b0^2/a0^3+b0/a0^2),
    Ly=2|beta|(b0/a0^2+1/a0).

For pixel side lengths h0,h1, replacing continuous locations by pixel centers
changes the normalized positive-pair query by at most

    Lx h0/sqrt(2) + Ly h1/sqrt(2).                            (6.2)

This applies to integrated photon mass regardless of its distribution within
a pixel. Mask boundary strips and PSF tails are separate, not Lipschitz errors.

### 6.3 Arithmetic and statistics are distinct

A finite-record covariance is an empirical statistic; its exact arithmetic
does not establish the population model (5.1), independence or a sample size.
Independent frame-pair records permit ordinary bounded U-statistic or
empirical-Bernstein confidence methods after bounding/clipping the image sums.
For example (A_2k-A_2k-1)(B_2k-B_2k-1)/2 is unbiased for Cov(A,B) for iid
paired records. Time-correlated PIV requires a justified mixing/blocking
contract. No iid or mixing promise is inferred from a sequence filename.

The consumer quantizes each real weight to a dyadic interval. Each image sum
then has an explicit interval using the total nonnegative pixel intensity.
Products and the sample-covariance formula are evaluated as rational interval
expressions. This certifies the supplied finite record only. Computational
cost is O(P) weighted pixel work per pair, O(P) precomputation/storage or a
streamed coordinate table, and constant-size covariance accumulation. The
ordinary comparator can also use these moments; no universal speed advantage
over an equally informed query-specific method is asserted.

## 7. Additional hydrodynamic torque interpretation

For a steady or stationary-mean two-dimensional incompressible Newtonian flow
in the full annulus, constant density rho and viscosity mu, no normal flow at
the two walls, no body forcing, and prescribed wall angular velocities
Omega_i,Omega_o, satisfying the Navier--Stokes momentum balance, the
fluid-on-inner-body torque per axial length is

    T_body = rho integral_annulus E[u u]:S dx
             - 4 pi mu beta (Omega_i-Omega_o).                 (7.1)

Proof: multiply steady mean div(rho uu)=div sigma by the virtual field w,
integrate by parts, use div w=0, Delta w=0, the two wall values, and the
symmetry of the stress. The convective boundary term is zero. Integrating
Du:Dw once more leaves the prescribed-velocity boundary term
2 mu integral_boundary u . Dw n =4 pi mu beta(Omega_i-Omega_o).
The remaining stress traction is the torque on the fluid at the inner wall,
opposite to T_body. For laminar Couette, u_r=0 and the first term vanishes,
giving the expected resisting torque sign.

Known body forcing adds its virtual work rho integral w.b dx to (7.1).
A nonstationary finite-time record also has the storage term
-rho integral w.partial_t u dx. Neither term is silently inferred to vanish
from an image sequence.

Axially periodic three-dimensional domains admit the corresponding volume
identity. A finite-height experiment has additional endcap traction terms;
a planar PIV slice does not acquire their full volume integral automatically.
Density, viscosity, geometry, wall speeds and spatial sampling measure must
be supplied or calibrated.

The normalized particle query in section 5 is an area average only under the
stated uniform spatial seeding. In that case its instantaneous limit must be
multiplied by the full observed area before insertion in (7.1). A guarded or
cropped particle domain additionally needs the omitted-volume correction
above. A rectangular jet image is not transformed into an annular experiment
by choosing an annular-looking analytic weight.

Frames separated by delta acquire D/delta rather than instantaneous u.
If speed <=U and material acceleration <=A along each particle path, then
|D/delta-u(0)|<=A delta/2, and the quadratic-current discrepancy is at most

    ||S|| [U A delta + A^2 delta^2/4]                           (7.2)

pointwise. This dynamic input is not acquired from two pictures. Brownian
motion and finite-size tracer response need their own model. Without these
gates, the valid output remains the finite-lag image-motion current, not (7.1).

## 8. What the result does and does not buy

It avoids estimating a full covariance/velocity field for this one quadratic
motion query, and it precisely identifies a radial-blur-compatible rotational
load and an incompatible translational load in the same virtual-field class.
It does not remove aperture, angular PSF anisotropy, background/gain, seeding,
finite-lag, sampling or mechanical-model costs. Generic complex-moment blur
invariants, connected particle-image correlations and virtual-work mechanics
are established prior; the result is an internal query-specific composition.
Historical priority and a practical advantage are NOT_ESTABLISHED. The public
raw-data investigation must retain any failure to meet the physical contract.
