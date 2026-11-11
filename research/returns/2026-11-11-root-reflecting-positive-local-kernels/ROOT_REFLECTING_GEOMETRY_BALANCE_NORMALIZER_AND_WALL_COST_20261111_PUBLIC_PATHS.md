Reflecting geometry: balance, paid normalizers and actual wall cost

1. Geometry and a rational local balance operation

Let Omega be a full-dimensional rational convex polytope in[-1,1]^3,
given by F rational half-spaces. A rational centre c and0<kappa<=1
certify B_kappa(c) contained in Omega. Put V=volume(Omega), and let
 K_r(z)=1_[-r,r]^3(z)/(2r)^3, 0<r<=1/8,
 w_r(x)=int_Omega K_r(y-x)dy,
 q=(1/V)int_Omega w_r(x)dx.
No periodic wrap is used. Then0<q<=1.

The cube c+[-kappa/2,kappa/2]^3 is inside Omega. For x in the smaller
cube c+[-kappa/4,kappa/4]^3, all y in x+[-a,a]^3 are inside Omega,
a=min(r,kappa/4). Since a/r>=kappa/4 and V<=8,
 q>=kappa^6/4096.
Also V>=kappa^3. These lower bounds depend on no facet-angle oracle.

For a known balanced well-mixed pair b_f A+B<->b_b C, use a chemical
slowdown h and coefficients c_f=b_f/(hq),c_b=b_b/(hq). At x,y in Omega
the ordered binding intensity per pair is
 c_f V K_r(y-x),
and C is placed at the designated first position x. For each C at x,
run release attempts at constant rate c_b, draw Z with density K_r,
and, when x+Z is in Omega, keep A at x and place B at x+Z. Otherwise
the attempt is a HIDDEN unary null mark and no particle changes. Count
EVERY attempt in actual chemical work. This hidden-null branch is an
additional fixed channel, not an uncharged attempt or observed original
firing. Unary conversions use b_e/h at the same position.

Under independent uniform positions, successful binding and release
average to exactly b_f(z)_alpha/h and b_b(z)_beta/h. The extra null
branch changes no counts. It can be included in a reference Markov
marked process and then hidden, without deleting any waiting time.

Use the Poisson point-process reference with intensities a_s/V, where
a_s are the original COUNT-activity parameters. The forward Palm flux
factor is
 c_f(a_A a_B/V) K_r(y-x) dxdy;
the reversed successful-release factor is
 c_b(a_C/V) K_r(y-x) dxdy.
They agree exactly under c_f a_A a_B=c_b a_C. Ordered DISTINCT identical
reactants retain the falling-factorial convention without a new factor2.
The hidden null mark balances itself at each position. A common factor
1/q for a binding/release pair preserves the rational chemical activity
certificate. The boundary-dependent successful release hazard must NOT
be replaced by a constant normalized release at every x: that changes
the flux identity. No measurement-based software correction is supplied.

2. Exact geometry is paid in fixed dimension

V is the volume of a rational3D polytope. The numerator Vq is (2r)^-3
times the volume of the rational6D polytope
 { (x,y):x,y in Omega, -r<=x_j-y_j<=r for j=1,2,3 }.
Both can be computed exactly with polynomial bit cost because these
dimensions are fixed. One explicit finite algorithm is as follows.
For dimension k=3 or6, enumerate all k-subsets of facet hyperplanes,
solve independent systems by rational determinants, retain feasible
vertices and deduplicate. Every face is the intersection with a set
of at most k independent facet hyperplanes; enumerate those sets and
their vertex sets, deduplicate faces and order them by inclusion.
Take barycentres of face vertices. Maximal flags of nested faces give
the barycentric triangulation. Sum absolute simplex determinants/k!.
The candidate and flag counts have a FIXED polynomial degree, for
example a coarse F^(k(k+1)) majorant, and all determinant dimensions
are at most6. Rational addition may enlarge bit lengths polynomially
in the number of flags; no population, class or high-dimensional
configuration polytope is enumerated. Thus q is an actual computable
rational, with q^-1<=4096kappa^-6, not a volume/real oracle.
Outputting the local placement/null-branch rule needs only its rational
offset cube and the original facet tests; no position mesh is emitted.

3. An actual wall-local-time budget

Consider a conservative fine network with n<=N0 and particle positions
in Omega. For type s let D_s(t) be unknown symmetric matrices with
d0 I<=D_s(t)<=I and Lipschitz norm<=Lambda. At a face with outward UNIT
normal n_f, prescribe the physical inward reflection direction
 -D_s(t)n_f.
Use this SAME specified boundary law at zero faults and under covariance
faults. It is a law of the model, not an observation of D_s by a compiler.
At corners allow nonnegative face-clock decompositions. Their support
is the corresponding boundary face. Actual covariance may be a bounded
predictable joint matrix near the nominal block diagonal, and bounded
predictable drifts are allowed. Consider every admitted reflected
semimartingale realization with these properties.

For a particle of type s use the proof function
 f_s(t,x)=(1/2)(x-c)^T D_s(t)^-1(x-c).
It is uniformly bounded by C/d0; its time derivative is bounded a.e.
by C Lambda/d0^2. At an active face,
 grad f_s . D_s n_f=(x-c).n_f>=kappa.
Therefore the reflected part of Ito's formula contributes at most
 -kappa sum_f dL_(particle,f).
The covariance and drift terms are bounded above by
 C(d0^-1+delta d0^-1)dt per particle. Chemical births/deaths/conversions
change the sum of the f_s by at most C/d0 per firing. Summing lifetimes,
localizing and taking expectations proves
 kappa E sum_(lifetimes,faces) L_(particle,f)(t)
 <= C N0/d0
  +C N0( Lambda/d0^2+(1+delta)/d0)t
  +(C/d0) E F_all(t).
All constants have fixed dimension. Since |D_s n_f|<=1, the left side
also controls the sum of absolute wall-push lengths. This is a genuine
actual-history boundary-work surrogate, not energy or number of wall
hits. Brownian boundary contacts may be infinite in number.

The budget is linear in physical time when the actual conserved model's
chemical attempt intensity is bounded, and polynomial in kappa^-1,
d0^-1,Lambda and the chemical resources. There is no exp(Lambda t).
This does not establish a reflected pair-occupation approximation.
Wall motion has zero quadratic variation; the earlier covariance,
particle-time and drift-variation accounts remain distinct.

4. The constructive constant-matrix comparison and its unpaid extension

If D_s is constant on a chemical-free gap, couple actual and nominal
motion from the SAME positions with the same Brownian innovations.
For Delta_i=X_i-Y_i, test Delta_i^T D_s^-1 Delta_i. Convexity makes
both reflection terms nonpositive, since D_s cancels exactly. The
square-root/Sylvester covariance bound then gives, for any gap g,
 E|Delta_i|^2<=poly(d0^-1)delta^2(g+g^2),
by choosing the elementary Young parameter1/g rather than generating
an exponential in g. Pair differences follow by adding two such
bounds; no global3n-dimensional position TV is assumed. Transforming
by D_s^-1/2 sends the nominal reflection to normal reflection on a
convex polytope with diameter increased by at most d0^-1/2. These are
analysis constructions, not applied coordinate changes or new controls.

For time-dependent D_s(t), differentiating that perturbation metric
adds a term of size C Lambda d0^-2 E|Delta_i|^2. The direct estimate
is exponential in the physical gap. That estimate is not a true lower
bound, but it is insufficient for a UNIVERSAL polynomial disturbance
tolerance after a long kinetic slowdown. The wall-cost estimate above
does not remove this occupation/stability problem. A weak conditional
contact-law estimate, a different metric or another construction can
be more useful than a strong whole-path coupling. Merely citing a
reflection existence theorem does not pay this quantitative operation.

The successful torus compiler's independent augmented proposal clock
and conditional CHANNEL coupling remain applicable once appropriate
reflected occupation estimates are proved. Its exact event times,
arbitrary post-event positions, all hidden/null marks and external
fault filtration must be retained. No successful release kernel may
silently use a boundary-independent normalization.

5. Primary scope and access boundary

The actually read Zhang--Isaacson2201.04099v3 SectionIII and IV.A.2
one-pair balance constraints motivate the boundary-dependent release
law, not the full network/cost/transport conclusions above.

After completed local hold checks, the DISTINCT primary
 https://arxiv.org/pdf/1011.2335v1
Nystrom--Onskog, Theorems1.2--1.3/1.9 and assumptions1.10--1.21 were
read. Their reflection-cone continuity/closed-graph, geometric/projection
conditions and bounded CONTINUOUS coefficient assumptions are actual
conditions. They give existence/continuity in their class, not this
arbitrary-history compiler or polynomial bound; no automatic coverage
of every polytope corner or every adapted covariance is asserted.
This source is a different2010 paper, not a recovery of a failed1979
source or permission to import that source's governing theorem.

NEW HOLD: the first exact opening of
 https://doi.org/10.32917/hmj/1206135203
returned not accessible via the web tool. No governing passage of that
Tanaka paper was read. No retry, alternate publisher/archive/version,
export or title/provider recovery follows. Search metadata and later
bibliography references are not imported as its theorem. Every prior
known/unknown access/transfer hold persists.
