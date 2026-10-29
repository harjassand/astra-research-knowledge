# A full-angular, nonradial uniform-time hard-sphere observation operation

29 October 2026. This consumes the actual normalized homogeneous3D equation
with collision rate |v-w| and uniform outgoing direction of total mass1.
There is no radial source assumption, future density oracle, finite population,
time mesh, supplied mixing rate or signed final output. Ideal real arithmetic
and independent uniform/exponential/normal primitives are explicit. Literal
fair-bit output and full continuous-velocity output are separate, unpaid tasks.

## 1. Input and changed representation

Let M(v)=(2pi)^(-3/2)exp(-|v|^2/2), beta=3/4 and

    phi(V)=1+4[(V^2-4)(25-V^2)]^2/194481, 2<=V<=5,
           1 otherwise.                                  (N1)

The positive C1 weight satisfies1<=phi<=5/4. Its second derivatives are
bounded on either side of the joins and its first derivative is continuous.
It is a bounded norm change, not a new Gaussian exponent or assumed evolved
anisotropy. Supply a nonnegative source f0 with exact mass1, mean0, energy3,
an evaluator with a warranted uniform ideal-primitive cost bound, and
the warranted bound

    ||(f0-M)/(M^beta phi)||_infinity <=D=1/10000.           (N2)

An independent source sampler is supplied/constructed for the ordinary
comparator. Set h=(f-M)/(M^beta phi). The representation uses a radial WEIGHT;
the unknown h can have unrestricted angular dependence. The narrower fixed
Gaussian weight preview is retained as an inconclusive near-threshold screen;
no sign was inferred from either quadrature's disagreement. The analytic
bounded multiplier changes the row-to-row weighting and keeps the nonlinear
algebra controlled. Its coefficients were not fitted to an input trajectory.

## 2. Full angular kernel and all conserved controls

The established Hilbert/Carleman linearized kernel has, for v,w and r=|v-w|,

    k(v,w)=4 exp(v_perp^2/2)/r-r,
    v_perp^2=|v|^2-(v dot(v-w)/r)^2.

With V=|v|, subtract P_v(w)=a(V)+b(V)(w dot v/V)+c(V)|w|^2.
At V=0 choose any fixed axis; its value at one point has no moment effect.
Mass, all THREE momentum coordinates and energy are controlled, not just
their radial subset. The weighted controlled kernel is

    Kc(v,dw)=M(v)^(1-beta) M(w)^beta phi(|w|)/phi(V)
                 [k(v,w)-P_v(w)]dw.                    (N3)

The actual acquired certificate NONRADIAL_CERTIFICATE.json establishes

    integral |Kc(v,dw)| <=eta nu(V), eta=199/200,
    EVERY v in R^3,                                    (N4)

where nu(V)=E_(W~M)|v-W|. Rotational covariance makes its scalar absolute row
depend only on V even though its tested functions h are NOT radial. Absolute
value is taken BEFORE the angular integral. No average-of-unknown-h oracle or
radial cancellation is inserted into (N4). The47 speed intervals cover[0,8]
completely with dyadic controls; the remaining unbounded tail is analytic.

## 3. Why the interval receiver proves a continuum row

Use w=v-r n, r>=0, u=n dot v/V in[-1,1]. Let x=|w|^2=V^2+r^2-2Vru,

    E0=-(1-beta)V^2/2-beta x/2,
    E1=-beta(r-Vu)^2/2-(1-beta)V^2u^2/2,
    P=a+b(V-ru)+c x,
    g(V,r,u)=phi(sqrt(x))[4r exp(E1)-(r^3+r^2P)exp(E0)]. (N5)

The row divided by nu is exactly

    [sqrt(2pi) phi(V) nu(V)]^(-1)
                         integral_0^infinity integral_-1^1 |g|du dr.

The factor r^2 in spherical volume has REMOVED the apparent r=0 pole.
The exponents are nonpositive quadratic forms. The receiver does not try to
bound1/r on a singular box or silently drop a diagonal cell.

On a box in(V,r,u), tensor linear interpolation L has sup error at most

    (dV^2 sup|g_VV|+dr^2 sup|g_rr|+du^2 sup|g_uu|)/8.    (N6)

This follows by applying the one-dimensional interpolation error successively;
each other interpolation operator has sup norm1. The C1 piecewise-polynomial
weight lies in W^(2,infinity) on compact sets, so the same integral-remainder
bound holds at its joins. For fixed V, convexity of absolute value bounds
the integral of |Lg| by the tensor trapezoid of the absolute endpoint values.
After summing boxes, the V interpolation is a single common convex weight;
take the maximum of the TWO summed endpoint trapezoids, not an unproved
pointwise sign or a statistical quadrature estimate. Add each box's area
times (N6). Pure second derivatives are explicitly enclosed in
certify_nonradial.py. The exact phi-polynomial, Gaussian derivatives and
product/chain rules determine those formulas. No mixed derivative is needed.

All scalar admission arithmetic is outward Arb at112bits. Every proposed
control is rounded to an exact24bit dyadic; the floating LAD optimizer only
proposes a table. Its convergence/optimality is no theorem premise. Adaptive
box selection uses floats only to order already bounded boxes. Neither that
ordering nor a floating branch establishes any admitted sign.

For r>=16>=Vhi, both exp(E0),exp(E1)<=exp[-beta(r-Vhi)^2/2], and

    |P|<=|a|+|b|(r+Vhi)+|c|(r+Vhi)^2.

Integrate the resulting degree4 polynomial times this Gaussian by exact
incomplete Gaussian moment recurrences. This bounds the entire integration
tail, with no source/target velocity cutoff. The factor denominator uses
nu(Vlo) (nu is radial convex/nondecreasing) and min phi on the V interval;
phi is unimodal between its joins, so its minimum is at an endpoint.

For V>=8 use a=b=c=0 and phi(V)=1, phi(|w|)<=5/4. Angular integration is
permitted for the NONNEGATIVE gain/loss envelope, not for signed unknown h.
The existing native positive-gain calculation gives

    row/nu <=(5/4){4/[beta(1-beta)V^2]
       +beta^(-3/2)exp[-(1-beta)V^2/2]
          [1+2sqrt(2/(pi beta))/V]}.                    (N7)

It decreases in V; at8 it is below.417461. The full executed compiler admits
47 speed intervals after62 attempted covers and331862 box evaluations in
23.9012seconds after imports. Failed coarse covers are retained; none is
silently promoted to a theorem. The maximum admitted row upper is below
.99499932. This is a finite mathematical operator certificate, not empirical
acquisition or historical novelty.

## 4. Nonlinear closure and identification with the physical equation

Energy conservation implies M^beta(p)M^beta(q)=M^beta(v)M^beta(w).
The two nonlinear terms in the h equation are exactly

    gain: integral M^beta(w)|v-w| E_sigma
                    [phi(p)phi(q)/phi(v) h(p)h(q)]dw,
    loss: -h(v) integral M^beta(w)phi(w)|v-w|h(w)dw.       (N8)

Let nu_beta=int M^beta(w)|v-w|dw. Gaussian scaling and convexity give
nu_beta/nu<=C_beta=Z_beta/sqrt(beta)<4. Gain/loss coefficient bounds are
respectively(25/16)nu_beta and(5/4)nu_beta, hence each is at most
Cstar nu, Cstar=25/4. The mild map with diagonal killing nu preserves the
D ball because eta+2Cstar D<1, and contracts because

    eta+4Cstar D=399/400<1.                            (N9)

This constructs the global controlled solution for every time horizon.
Its total original collision term, including M and both perturbation orders,
conserves all five moments even for signed Gaussian-decaying functions.
Control changes the physical equation only by -M(v)P_v paired with the five
moment errors. Thus those errors solve a homogeneous5x5 linear ODE with zero
initial value. Compact-head dyadic controls are bounded, so its coefficients
are finite. All five errors vanish identically. No actual time-dependent
moment or density bound is an input to the algorithm.

Positivity follows by the same local gain/loss Picard identification as in
the reviewed radial proof, now in the full angular norm. The uncontrolled
weighted row tends to0 by (N7), and its explicit native envelope below
uniformly bounds it on the head. On a2D ball, nu_f<=nu+2D(5/4)nu_beta;
choose lambda=(1+10D)nu. The positive Picard integrand is
Qplus(f,f)+(lambda-nu_f)f. Split speeds at R=40; the tail row is<1/40,
and the head satisfies nu<=42 and raw row/nu<32. At T=1/1000000 the head
contribution is<1/500; added diagonal<=10D, and nonlinear Lipschitz on the
2D ball<=8Cstar D=50D. The contraction is<1/40+1/500+60D<1/16.
It maps the2D ball into itself from a D-ball positive source. Its iterates
are positive; uniqueness identifies the controlled D-ball solution with it.
Repeat on successive intervals. Hence f=M+M^beta phi h is the positive,
mass/mean/energy-matching ORIGINAL hard-sphere solution for every finite t.
The scalar constants are consumed separately in STATIC_CERTIFICATE.json.

## 5. Bounded full-vector branching query

Scale z=h/D. At v with remaining t, wait Exp(nu(V)). If the wait exceeds t,
return z0(v). Otherwise, after reducing t:

* with probability L(v)/nu(V), L=int|Kc|, sample |Kc|/L, multiply its sign
  and request that FULL VECTOR child;
* with probability D(25/16)nu_beta/nu, draw the actual relative-speed-biased
  beta-Gaussian partner and uniform elastic p,q; with probability
  phi(p)phi(q)/[(25/16)phi(v)] request and multiply two children, else kill;
* with probability D(5/4)nu_beta/nu, draw that partner; with probability
  phi(w)/(5/4) request children v,w with a minus sign, else kill;
* otherwise return0.

Every mark is in[-1,1]. The expected children are bounded by(N9), so mean
nodes<=400 for ALL v,t and the tree is almost surely finite. Conditioning
on the first event and the unique mild map identifies E z=h/D. The public
raw query is H_t(v)=D phi(V) z_t(v), with

    |H_t(v)|<=D_eff=5D/4=1/8000,
    E H_t(v)=(f_t(v)-M(v))/M(v)^beta.                  (N10)

There is no radial projection of a requested child or of its source value.
An explicit stack avoids a fixed language recursion-depth limitation.

## 6. Native full-vector envelope; no conditional-angular oracle

The gain sampling construction is easiest in the same relative coordinates
w=v-r n, c=v dot n. Before multiplication by phi(w)/phi(v), its positive
measure is

    4 M0 r exp[-beta(r-c)^2/2-(1-beta)c^2/2] dr dOmega(n),
    M0=(2pi)^(-3/2).                                   (N11)

For V>=1, draw r from the Rayleigh law with precision alpha=beta(1-beta),
then t=beta r+Normal(0,1). If |t|>V produce a dummy rejection; otherwise
draw n with cos(n,v)=t/V and uniform azimuth. The completed-square identity

    alpha r^2+(t-beta r)^2=beta r^2-2beta rt+t^2

shows that on the valid branch its measure times the KNOWN mass
E_G(V)=4/[beta(1-beta)V] is EXACTLY (N11). Invalid t contributes only dummy
mass. It never requires a rare-event conditional normal sampler.

For0<=V<=1, draw n uniformly on the sphere and r^2=4Exp(1)/beta.
Use the envelope mass E_G=8sqrt(2/pi)exp(beta V^2/2)/beta. Its physical
gain/envelope factor is

    exp[-beta(r-c)^2/2-(1-beta)c^2/2
                              +beta r^2/4-beta V^2/2]<=1.

The inequality follows by completing the r square, |c|<=V and beta<=1.
It remains valid at V=0, avoiding a1/V sampling singularity.

For both regimes multiply the envelope by(5/4)/phi(V). Add

    [(5/4)/phi(V)] M(v)^(1-beta)M(w)^beta
             [V+|w|+|a|+|b||w_parallel|+|c||w|^2].      (N12)

This dominates the absolute physical controlled row pointwise. Its terms are
known beta-Gaussian, speed-biased chi4, axial-absolute-biased Gaussian and
energy-biased chi5 measures. For the axial term the parallel coordinate is
a signed Rayleigh with squared magnitude2Exp/beta and the perpendicular
coordinates are independent normals. The sphere/basis/azimuth are generated
explicitly, giving an actual VECTOR. Chi3 and chi5 use a squared normal plus
one/two independent chi2 exponentials, so no free special distribution is
assumed. Zero-norm exact endpoints have probability0 in the ideal model.

The total envelope mass E(v) is computable. Its uniform cost bound is
E/nu<64, using the actual largest dyadic controls and

    E_G/nu <=max{4exp(beta/2)/beta,4/[beta(1-beta)]},
    D_beta(V)(V+E|W_beta|)/nu
        <=beta^(-3/2)[1+E|W_beta|/nu(0)].

Both inequalities include every dummy gain proposal. The uncontrolled row
omits control terms and its same envelope is<32nu; this pays the local
positivity constants in Section4.

Let pQ=D(45/16)nu_beta/nu<=9/8000 denote the two nonlinear PROPOSAL events,
including their later thinnings. On their complement the known envelope
coin, with extra dummy mass2nu(1-pQ), has mean L/[E+2nu(1-pQ)]. Huber's
GENERAL linear Bernoulli factory amplifies it by

    C=2+E/[nu(1-pQ)]<67,
    epsilon=1-eta(V)/(1-pQ)>3/1000.

It supplies the exact conditional linear branch probability without an L
integral oracle. Its established bound is at most213000 expected base coins.
After choosing the linear branch, sample its child by ordinary envelope
rejection. The branch probability L/nu cancels the conditional mean E/L:
the unconditional child-sampling work is E/nu<64. A tiny L is not silently
given a constant conditional cost. The beta-Gaussian relative-speed partner
for(N8) is a mixture weighted by V+|w|, accepted with |v-w|/(V+|w|), with
mean proposals<=2. All failed candidates, waits, thinnings, base coins and
factory geometric draws count. Thus the mean ideal primitive work is finite
and independent of t and v; the conservative bound is VERY large.

## 7. Positive nonradial finite-observation output

For ANY finite partition C_i with acquired Gaussian masses A_i=int_Ci M,
B_i=int_Ci M^beta and conditional beta-Gaussian samplers, require
A_i>D_eff B_i. Propose i proportional to A_i+D_eff B_i. Draw v from the
conditional beta Gaussian, call raw H_t(v) from(N10), and accept with

    [A_i+B_i H_t(v)]/[A_i+D_eff B_i].                  (N13)

Every realized probability is in[0,1]; its expected numerator is the TRUE
nonradial cell probability. The accepted labels are normalized iid draws
from the exact finite observation law. Mean proposals are1+D_eff Z_beta.
This is not retaining a proposal point or assuming independently sampled
partitions form a projective coupling. REFINEMENT_BARRIER.md gives the
precise obstruction to that old fixed-amplitude completion.

The explicit discriminator is the TWO angular cells

    Cplus={v:v_x^2>=v_y^2}, Cminus=its complement.

Both have A_i=1/2, B_i=Z_beta/2, and conditional Gaussian sampling uses a
factor2 rejection, including its failed draws. They cover ALL velocities,
with no radial overflow, while distinguishing a genuinely anisotropic source

    f_delta(v)=M(v)[1+delta A(v)],
    A(v)=(v_x^2-v_y^2)/(1+|v|^2), delta=2^-14.          (N14)

Since |A|<=1 this is positive. Mass and energy matching follow from swapping
x,y; momentum vanishes by coordinate evenness. The source obeys(N2) because
|h0|<=|delta| M0^(1-beta)<D. More generally all |delta|<=D are admitted
by this conservative sufficient bound. Its source sampler is Gaussian
rejection with factor(1+delta A)/(1+|delta|), mean1+|delta|. Its exact initial
anisotropy is nonzero:

    P0(Cplus)=1/2+(delta/2) [4/(3pi)] q,
    E0[v_x^2-v_y^2]=(4delta/15)(3-q),
    q=sqrt(pi/2)exp(1/2)erfc(1/sqrt2).                 (N15)

For a uniform direction, E|n_x^2-n_y^2|=4/(3pi) and
E(n_x^2-n_y^2)^2=4/15. The independent chi3 radial integrals are
E[r^2/(1+r^2)]=q and E[r^4/(1+r^2)]=3-q. These establish the discriminator
analytically; a small finite sample does not resolve its tiny signal.

## 8. Paid ordinary approximation and remaining boundary

The dominating genealogy has offspring<=399/400 and every clock>=nu0.
The same nonnegative alive-count supermartingale as in the reviewed radial
proof gives

    |h_t(v)|<=D exp(-nu0 t/400),
    TV(f_t,M)<=D_eff Z_beta exp(-nu0 t/400)/2.           (N16)

This explicit bound is also given to an ordinary Gaussian observation sampler.
At any tolerance it already pays, querying the kinetic tree is unnecessary.
The new result is not an all-ordinary-method speed claim. Nonlinear LVDSMC,
conservative Fourier/spectral integration, rigorous residual control and the
ordinary finite-time recursive full-law operation receive the SAME analytic
source, moments, invariants, kernel, norm admission and new relaxation bound.

The finite cover/compiler, native marked query and positive angular consumer
are substantive new constructions in this packet. Historical priority of this
particular combination is UNKNOWN; Hilbert kernels, weighted norms, invariant
controls, nonlinear branching, Bernoulli factories and rejection sampling are
established. Mathematical source qualification is not measured-gas acquisition.
Floating diagnostics do not establish literal iid bits or continuum CPU-error
control. The interval row proof is rigorous at its explicit finite-model scope.
Arbitrary initial nonequilibrium states, all infinite refinements and full
continuous normalized velocity output remain unacquired by this operation.
