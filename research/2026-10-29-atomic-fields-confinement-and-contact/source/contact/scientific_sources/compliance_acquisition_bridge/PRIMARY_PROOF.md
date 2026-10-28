# Contact-aware compliance acquisition: exact conditional interface

This construction is a mathematical acquisition-to-decision interface for a
specified dilute crack model. No component measurement, contact-class bound,
finite-component correction, or nondestructive protocol has been acquired.
The underlying open/closed differential-compliance measurement is established
prior art. The new work here is the derived contact-weighted matrix bound and
its executable conservative service calculation. Novelty of that combination
is UNKNOWN.

## Contract and provenance

Input: generalized tangent-compliance measurements at two uniform preloads;
deterministic entrywise errors; a bound on all load-dependent material,
fixture, finite-boundary, interaction, and model errors; and independently
supported coverage/contact conditions below. Output: an upper bound on the
largest isolated-crack Mode-I service stress intensity, for arbitrary crack
count and depths in a supplied compact interval. Costs: eight load settings
per two-preload/two-mode central-difference acquisition, displacement and
rotation sensing, plus the calibration/model evidence. The numerical
certificate itself uses two-dimensional rational matrix algebra, monotone
scalar inversion and one-dimensional interval subdivision. No flaw image,
crack-count inference or pristine specimen is an input.

Primary exact elasticity source: Nishioka, Zhou & Fujimoto (2008), *On the
General Solutions for Mixed-Mode Penny-Shaped Crack and Their Applications*,
DOI [10.1299/jcst.2.34](https://doi.org/10.1299/jcst.2.34), full pinned PDF in
`sources/Nishioka2008.pdf`. Its uniform Mode-I SIF is Eq46, and the affine
bending result is §3.3/Eq60 (printed p43). Its infinite, homogeneous, isotropic
solid is the elasticity scope used here. The affine opening below is the
ordinary penny-crack solution; the source's tip coefficient independently
checks its factor 2/3. The energy integrals, contact variational bound and
decision interface below are derived here.

Peer convention: normal x; z is thickness coordinate; H is full thickness;
r=2z/H. Generalized loads p=(p0,p1) produce nominal axial stress p0+p1*r;
p0=F/A and p1=M_b*H/(2I). Conjugate coordinates are
q=(A*u_end, (2I/H)*theta_end). Each modeled crack is an internal circular
zero-thickness disk, normal x, radius a, center r. Cracks do not interact.
The material is linear elastic except for an explicitly bounded nuisance.

The API requires a_max < H*(1-max|r|)/2, so every disk in its rectangular
radius/depth input domain is strictly buried through the thickness. Lateral
burial, clearance to other boundaries and the infinite-medium-to-component
error enclosure are external geometric-admission obligations. The default
example has a_max=0.5mm and a minimum thickness-center clearance of1mm.

Coverage obligations:

1. At the positive preload all included cracks are fully open throughout
   both tangent probes; their tangent opening operator is the isolated-disk C.
2. At the negative preload the incremental normal-contact operator K obeys
   K >= k I in the L2 opening-displacement energy, with supplied k>0 in Pa/m.
   The closed opening response is (C^-1+K)^-1. A uniform homogenized spring
   model with stiffness at least k suffices. An average ultrasound stiffness
   or a few sampled interface points do not establish this coercivity.
3. After removing the crack contrast, the remaining symmetric tangent-matrix
   difference has a supplied operator-norm or stronger Loewner enclosure.
   Unknown linear background cancels. Nonlinear material response, contact
   fixtures, geometric stiffness, hysteresis and drift do not cancel for free.
4. The service load opens every modeled disk. A radius/depth bound and
   residual-stress envelope must establish this. The implementation refuses
   a service envelope lacking the sufficient affine all-open margin.

Hidden unswitched cracks lie outside this contact-matrix acquisition contract.
The parent's separate load-envelope result bounds that class; this file does
not recreate its observational-equivalence argument. Coupling the two classes
requires a valid coverage partition and the maximum of both K bounds.

## 1. A finite disk carries its own bending moment

Let zeta be local thickness coordinate within the disk and g the local stress
gradient. Write E'=E/(1-nu^2), beta=16/(3E'), and alpha=8/(pi E'). For affine
normal traction t=pc+g*zeta the ordinary opening is

    w = alpha * [pc+(2/3)g*zeta] * sqrt(a^2-y^2-zeta^2).

The odd part integrates to zero in crack volume. It does not integrate to
zero in bending energy. Direct disk integrals give

    integral sqrt(a^2-rho^2) dA = 2*pi*a^3/3,
    integral zeta^2*sqrt(a^2-rho^2) dA = 2*pi*a^5/15.

Thus Q=integral t*w dA (twice complementary energy) is

    Q(pc,g) = beta*a^3 * [pc^2+(2/15)*a^2*g^2].

This energy is independently recoverable without assuming the displacement
formula: the source's superposed uniform/bending rim SIF is
2*sqrt(a/pi)*[pc+(2/3)*g*a*cos(theta)]. For a uniform radius extension,
the ordinary energy-release identity gives

    dU*/da = a/E' * integral_0^(2pi) K(theta)^2 dtheta
           = 8*a^2*pc^2/E' + 16*a^4*g^2/(9E').

Integrating from a=0 gives exactly Q/2 above. Thus the 8/15 finite-disk
matrix correction follows independently from the primary SIF result and
energy release, rather than merely from the peer's opening formula.

For pc=p0+p1*r and g=2*p1/H, the open generalized matrix is

    C_open = beta*a^3 * [[1,r],[r,r^2+(8/15)*(a/H)^2]].             (1)

Consequently the full population's measured open matrix contains
M2_eff = sum a^3*r^2 + (8/(15H^2))*sum a^5. It is a Loewner upper bound
on the center-moment matrix. The peer's certificate can keep this positive
term without estimating it away. Treating the third measurement as exactly
the center second moment would be wrong.

The exact maximum rim intensity for a fully open affine disk is

    Kmax = 2*sqrt(a/pi) * [pc+(2/3)*abs(g)*a].                     (2)

Full nonnegative free opening requires pc >= (2/3)*abs(g)*a.
Zero opening is an admissible fully closed ideal Signorini state if
pc <= -abs(g)*a. Between these sufficient endpoints partial contact must be
solved. A constant compressive preload does not prove contact stiffness.

## 2. A contact-weighted lower matrix, without rigid closure

Let B map (p0,p1) to the affine disk traction and use the L2 disk inner product.
C is the positive self-adjoint open opening operator. First suppose K=k I.
Resolvent algebra gives

    D = C-(C^-1+kI)^-1 = C(C+k^-1 I)^-1 C.                       (3)

For actual K >= kI, resolvent monotonicity gives D_actual >= D. This is
ordinary positive-operator/parallel-sum algebra, not a new mathematical
principle (compare Anderson & Duffin1969, DOI10.1016/0022-247X(69)90200-5).

Set Q=B* C B and N=B* B. The variational identity for the inverse in (3),
restricted to trial functions v=Bz, yields for every generalized load p

    p* B* D B p
      = sup_v {2<v,CBp>-<v,(C+k^-1I)v>}
      >= sup_z {2z*Qp-z*(Q+N/k)z}
      = p* Q(Q+N/k)^-1 Q p.                                    (4)

No discretization of C or high-frequency elasticity is used in (4).
The same argument holds on the finite-dimensional trial space when C has
an unbounded inverse; C+k^-1I is coercive and its variational identity is
well-defined. In the (pc,g) coordinates both matrices are diagonal:

    Q = diag(beta*a^3, (2/15)*beta*a^5),
    N = diag(pi*a^2, pi*a^4/4).

Define eta0=beta*k*a/(pi+beta*k*a),
etag=8*beta*k*a/(15*pi+8*beta*k*a), v(r)=(1,r). Then

    D_actual/beta >= a^3*eta0 * v(r)v(r)*
                     + a^3*etag*(8/15)*(a/H)^2*diag(0,1)
                  >= h_k(a) * v(r)v(r)*,                        (5)

where h_k(a)=a^3*beta*k*a/(pi+beta*k*a). This is useful for every k>0;
unlike a crude C_closed<=N/k subtraction it never produces a negative
retention coefficient. Its derivative is positive:

    h'_k(a) = c*a^3*(4+3*c*a)/(1+c*a)^2, c=beta*k/pi.

The map h_k(a)~c*a^4 for weak contacts and tends to a^3 for rigid contacts.
It therefore charges loss of contrast as a radius-dependent sensitivity,
without inferring a contact state for every small crack or requiring a
minimum crack radius. Coercivity remains a supplied physical premise.

## 3. Measured contrast to a maximum crack bound

In dimensionless moment units (divide by beta*a_scale^3), suppose the
reported symmetric contrast is Mhat with absolute entry errors
(e00,e01,e11), and the remaining nuisance operator norm is at most b.
Then a valid upper is

    U = Mhat + diag(e00+e01+b, e11+e01+b).                       (6)

Indeed this diagonal dominates every symmetric error in the entry box by
the row-sum/diagonal-dominance inequality. Equations (5),(6) imply

    sum [h_k(a_i)/a_scale^3] v(r_i)v(r_i)* <= U.                 (7)

For each individual crack, positive summands and the rank-one Schur test give

    h_k(a)/a_scale^3 <= 1/[v(r)*U^-1*v(r)].                     (8)

For U>0 this is an elementary exact equivalence for its rank-one inequality.
Inverting the increasing h_k bounds a at each r. Combining it with the
known geometric radius cap and (2) gives a one-dimensional continuous-depth
upper on every crack, whatever the crack count. A singular U can be enlarged
by any declared positive rational diagonal before using this implementation.

`contact_certificate.py` encloses pi between explicit 40-digit rationals,
uses rational bisection for (8), and integer-square-root enclosures for (2).
For each depth interval it minimizes the convex quadratic v*U^-1v exactly,
uses that minimum to upper-bound radius, and uses the endpoint maximizing
service center stress to upper-bound K. Subdivision only tightens this
already valid bound. All leaves are retained. The reported lower is a lower
bound on this *certificate function*, not proof of an attainable worst flaw.
The final receipt serializes each rational leaf interval and its upper, the
full parameter tuple and input matrix, allowing coverage and bound replay.

If service residual center/gradient bounds are supplied, the implementation
adds them to the positive K envelope. It separately requires

    min_r(service0+service1*r)-rho_service
        >= (2/3)*(2*abs(service1)/H+rho_gradient)*a_max.

The result is conditional model arithmetic, not component qualification.

## 4. Acquisition and error costs

At each uniform preload +/-P, measure q at +/-h0*e0 and +/-h1*e1.
The four points estimate both columns of the tangent matrix by central
differences: eight vector measurements total. Maxwell reciprocity can average
the two off-diagonal estimates; inconsistency is a diagnostic, not an error
bound. Repeat measurements only reduce a declared stochastic term under
their actual dependence model; they do not remove systematic error.

If individual q-coordinate error is bounded by s_i, the open-minus-closed
central-difference entry error is at most 2*s_i/h_j. If the relevant third
derivative of q is bounded, central-difference truncation adds h_j^2/6
times that bound per preload. These budgets, load calibration and coordinate
cross-talk must fit into the supplied entry box.

For zero initial gap and affine residual center/gradient bounds rho0,rhog,
depth |r|<=R and radius a<=Amax, a sufficient ideal switching condition is

    P > rho0+Amax*rhog+max(h0, h1*(R+2*Amax/H)).                 (9)

The maximum uses the actual protocol's one-mode-at-a-time probe settings.
If combined probes occupy the whole h0/h1 rectangle, replace that maximum
by their sum; it is a different, more costly load protocol.

A finite initial aperture requires an additional acquired closure-pressure
bound; the code accepts its equivalent stress in (9). For a gap profile
proportional to sqrt(a^2-rho^2), that equivalent stress follows directly
from the uniform opening solution. Arbitrary apertures require an actual
contact calculation. Neither a geometric aspect ratio nor an average gap
alone proves (9) for arbitrary contact geometry.
This extra parameter controls switching only. A real finite-aperture void
also changes the opening operator and service SIF; preserving the disk law
requires a justified finite-aspect model-error enclosure. It is not silently
converted into a zero-thickness fracture by supplying a closure pressure.

An upper test opening intensity is

    2*sqrt(Amax/pi)*[P+rho0+(2/3)*Amax*rhog
                    +max(h0, h1*R+(4/3)*h1*Amax/H)].            (10)

This number must lie in an independently validated reversible/no-growth
load envelope, with yield, stability and cycle effects included. A fracture
toughness alone does not prove nondestructiveness. Compression also needs
its own yield/contact-damage bound. No such physical envelope is acquired
by this work.

Finite boundaries, crack interactions, unknown orientations, noncircular
shape, nonzero aperture, fluid filling/squirt flow, rough-surface normal/shear
coupling, frictional slip and hysteresis can invalidate this operator model.
The stiffness bound must concern the normal Schur complement after any
allowed tangential relaxation, at the actual probe frequency/rate and load
history. A homogenized k with no homogenization error or length-scale bound
is an assumption. These effects require justified multiplicative/additive
error enclosures before (7) applies to a component. The finite a^5 term is
treated exactly; it does not bound finite-component errors.

## 5. Strong ordinary comparisons and one retained failed repair

* Absolute total open compliance already upper-bounds defect compliance if
  the unknown elastic background is positive semidefinite in the additive
  model. It needs no pristine reference and no contact stiffness premise.
  It may be too loose for a service decision; the numerical receipt charges
  this comparator the same geometry, service load and observations.
* Open/closed differential compliance and fitting are established. Kovářík
  2025 derives and implements precisely such self-reference for breathing
  cracks, building on differential compliance from1995. VAM/CAN methods
  also use opening/closure and static/dynamic modulation; baseline freedom
  and amplitude scaling are not discoveries here.
* Given the same measurements/contact/error priors, an ordinary contact
  boundary-element solve plus interval decision calculation could also
  obtain a conservative K bound, and may be sharper. The operation above
  is an analytic conservative reduction avoiding that solve; no measured
  runtime or sharpness advantage over a matched certified solver is claimed.

A tempting repair for nonlinear background was tested and rejected as a
general protocol: let d(P)=C(+P)-C(-P), and form 2d(P)-d(2P). It cancels a
linear-in-preload tangent-background term while retaining a perfect step.
For a small contact with contrast d_c(P)=Q*t(P)/(1+t(P)), t(P)=c*P^m,
the extrapolated contrast is

    Q*[2*t/(1+t)-2^m*t/(1+2^m*t)].                              (11)

Its numerator after multiplication by the positive denominators is
t*[(2-2^m)+2^m*t]. It is negative whenever
0<t<1-2^(1-m), an open parameter regime for every m>1; this failure does
not depend on a rounded numerical example.

For m>1 this is negative at sufficiently small t. Arbitrarily many such
contacts could mask a different crack. Kim et al.2021's primary Table2
fits m=0.930,2.601,4.987,7.486 for rough aluminum block interfaces. Thus a
universal concave/Hertzian contact law cannot be assumed to justify this
repair. Those fitted mean stiffnesses are also not coercivity bounds for
hidden fatigue cracks. This failure is retained in the numerical receipt.
