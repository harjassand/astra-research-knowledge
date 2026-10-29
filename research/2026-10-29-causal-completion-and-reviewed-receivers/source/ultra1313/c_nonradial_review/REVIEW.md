# Independent whole challenge: full-angular hard-sphere completion

29 October 2026. Status: **ACCEPTED at the stated ideal-real mathematical scope.**

This is a new whole mathematical/code review of the nonradial extension. It
does not infer acceptance from the earlier radial review. I read all of
NONRADIAL_PROOF.md, CONTINUOUS_OUTPUT.md, the refinement obstruction, the prior
and ordinary-comparator dispositions, certify_nonradial.py, compile_nonradial.py,
certify_static.py, nonradial_query.py, run_consumer.py, smooth_weight.py,
suspect_resolution.py and finalize.py, together with the actual operator,
scalar, execution and final receipts. The floating screen/weight-preview
algorithms are proposals only and are not sign-admission premises.

No producer file was edited. The independent consumer below verifies their
frozen manifest and preservation. It runs no new kinetics, sampling cohort,
optimizer or all-speed grid.

## 1. Literal full-angular operator and normalization

The hard-sphere outgoing law has mass one, hence its conventional prefactor
in the solid-angle integral is 1/(4 pi). In the primary Hilbert representation
of Radtke--Hadjiconstantinou--Wagner, Eqs. 6--9, put c0=sqrt(2), rho0=1,
u0=0 and hard-sphere collision exponent one. Integrating the transverse
Maxwellian gives 2K1=4 M(v) exp(v_perp^2/2)/|v-w| and K2=M(v)|v-w|.
This is precisely the raw kernel used here. The primary's VHS exponent is
not the new Gaussian weight exponent beta=3/4.

With w=v-r n, x=|w|^2 and u=n dot v/|v|, the Jacobian r^2 and the angular
azimuth 2 pi turn the signed row into

    (sqrt(2 pi) phi(V))^-1 int_0^infty int_-1^1 g(V,r,u) du dr.

The remaining divisor nu(V) gives the stated relative row. The r=0 pole is
really absent from g; no omitted diagonal region or principal-value convention
is used. Absolute value is applied to the complete signed g before integration
over u. Rotation is used only to evaluate this absolute scalar row, not to
replace a vector child or a nonradial h by its spherical average.

The a+b w_parallel+c |w|^2 control is a linear combination of all conserved
moments. Only the component along v is needed in a particular row. Arbitrary
three-component momentum error still enters a finite homogeneous five-moment
ODE. All its coefficients are Gaussian integrals of bounded stepwise controls;
the arbitrary axis at V=0 is harmless. Zero initial moment error therefore
remains zero. There is no missing assumption of radial source data.

## 2. The actual derivative certifier covers the continuum

Write G=4r exp(E1)-Q exp(E0), Q=r^3+r^2 P. The exact inner weight is

    phi(x)=1+4[(x-4)(25-x)]^2/194481, 4<=x<=25.

For h=(x-4)(25-x), phi_x=8h(29-2x)/194481 and
phi_xx=8[(29-2x)^2-2h]/194481. Both joins have phi=1 and phi_x=0;
the maximum at x=29/2 is exactly 5/4. Thus the piecewise composition is C1
with locally bounded weak second derivatives, including boxes that cross a
join. Differentiating phi(sqrt(x)) via an actual square-root derivative would
be wrong near zero; the code correctly uses this polynomial in x instead.

I independently reconstructed every pure derivative in the certifier:

| variable | x_j | x_jj | (E1)_j | (E1)_jj | (E0)_j | (E0)_jj |
|---|---|---|---|---|---|---|
| r | 2(r-Vu) | 2 | -beta r+beta Vu | -beta | -beta r+beta Vu | -beta |
| u | -2Vr | 0 | beta Vr-V^2 u | -V^2 | beta Vr | 0 |
| V | 2(V-ru) | 2 | beta ru-Vu^2 | -u^2 | -V+beta ru | -1 |

The code's Q_j,Q_jj agree with differentiating its literal polynomial.
For each variable it uses exactly

    (phi G)_jj = phi G_jj + 2 phi_x x_j G_j
                 +(phi_xx x_j^2+phi_x x_jj)G.

The interval expression for x=(r-Vu)^2+V^2(1-u^2) is a valid nonnegative
enclosure on the full u interval. The specialized square routine encloses a
zero-crossing square rather than taking a generic interval power/log. The
phi_jet intersection and union include all inside/outside pieces; their
correlations may be lost, which only makes the bound conservative.

For tensor linear interpolation, replacing the V, r and u factors in sequence
gives the sum of their one-dimensional second-derivative errors. Each other
interpolator is a positive norm-one map. For fixed V the absolute interpolant
is bounded by the endpoint absolute-value trapezoid. All cells share the SAME
V interpolation weight, so max(sum endpoint0,sum endpoint1) is valid; summing
cellwise favorable signs would not be. The implementation uses the correct
summed endpoint maximum and pays area times each derivative error.

For r>=16 and V<=V_hi<=8, both Gaussian factors are bounded by
exp[-beta(r-V_hi)^2/2]. Expanding the nonnegative polynomial envelope gives
coefficients

    [0,4,|a|+|b|V_hi+|c|V_hi^2,1+|b|+2|c|V_hi,|c|].

The code translates r=y+V_hi, integrates y>=16-V_hi with the exact Gaussian
moment recurrence, and multiplies by 2*(5/4) for u and phi. It divides by
nu(V_lo) and the minimum endpoint phi. Radial convexity makes nu nondecreasing;
the unimodal bump has its minimum at an interval endpoint. The tail V>=8
uses a positive gain/loss envelope with zero controls and a monotonically
decreasing upper bound. No finite velocity cutoff or signed-angular
cancellation is hidden there.

The controls are exact dyadics; the fit only proposes them. Float priorities
choose subdivisions but never prove a sign. Even an unfortunate priority
would only prevent admission. Arb arithmetic, point-upper accumulation,
outward removal of old cells and the final exact dyadic upper endpoint preserve
the enclosure. All 47 admitted intervals close [0,8] with no gap, and the tail
closes the unbounded domain. I found no omitted continuum case.

## 3. Nonlinear identification, positivity and the weighted tree

The Maxwellian power identity at an elastic collision and 1<=phi<=5/4 give
the two nonlinear coefficient bounds in N8. Scaling and convexity give
nu_beta/nu<=Z_beta/sqrt(beta)<4, so the common 25/4 bound is conservative.
The D ball is invariant and the Lipschitz/offspring bound is

    199/200 + 4(25/4)/10000 = 399/400.

The controlled contraction is not, by itself, a proof of physical positivity.
The separate uncontrolled local argument supplies that missing step. On a
2D ball, lambda=(1+10D)nu exceeds nu_f because
2D*(5/4)*(nu_beta/nu)<10D. The positive Picard integrand is therefore
nonnegative. On V<=40 the raw-row/head-time contribution is at most
32*42*10^-6<1/500. The raw tail is below 1/40, the diagonal term costs 10D
and the nonlinear Lipschitz term at radius 2D costs 50D. Their sum is .033,
below 1/16, and the map sends a positive D-ball initial condition into the
2D ball. Moment cancellation already identifies the controlled solution as
uncontrolled. Local uniqueness identifies it with these positive iterates,
and the global controlled D bound permits repetition at every endpoint.
There is no assumed evolved positivity/norm/mixing oracle in this step.

Each native tree mark has magnitude at most one. Killing/short-circuiting a
product with a zero child preserves its mean. Independent fresh child draws
give the nonlinear product; the gain children are actual 3-vectors with the
elastic half-sum/relative-radius construction. Nonradial source evaluations
are at those vectors. State-dependent velocities and unbounded clocks do not
cause explosion: total potential nodes are dominated by a uniformly
subcritical offspring process, hence finite almost surely with mean<=400.
The explicit stack imposes no extra recursion cutoff.

The continuous-time alive-count bound also checks. A particle at v has loss
drift at least (1-399/400)nu(v), and nu(v)>=nu(0). Localizing and using the
nonnegative supermartingale pays the stated relaxation. It does not assume
an upper clock bound or a decay of the signed query variance.

## 4. Native vector sampling and the factory are paid

For the large-V gain proposal, the joint Rayleigh/normal/azimuth density after
t=V u has prefactor alpha V r/(2 pi)^(3/2). Multiplication by
4/(alpha V) yields the exact gain envelope. The |t|>V branch is genuine dummy
mass. Conditioning a normal on this event would be a different, unpaid oracle;
the implementation does not do it.

For V<1 the sphere/Rayleigh proposal gives the displayed exponential envelope.
Its exponent difference equals

    -beta(r-2c)^2/4+(beta-1/2)c^2-beta V^2/2 <= 0

for |c|<=V and beta=3/4. There is no singularity at V=0. The large and small
regimes are consistent at the code's V>=1 boundary, without requiring their
envelope masses to match. Gaussian, speed, axial-absolute and energy-biased
proposals have exactly the normal/chi laws claimed. The mixture density is
the sum of ALL physical envelopes, and the acceptance uses that whole sum,
not only the selected mixture component. I checked nonradial_query.py's
log-domain numerator, sign, phi ratio and dummy return against this algebra.

The base coin has mean L/(E+2nu(1-pQ)); C times it is the required conditional
linear-branch probability. The returned child is drawn by a separate correct
rejection sampler. Its small-L conditional cost is paid unconditionally by
(L/nu)*(E/L)=E/nu. All nonlinear proposals and their thinnings, including
killed branches, are retained in the offspring and work accounts.

I directly read Huber's primary 1308.1562v2, Section 2.2 and Theorem 1.
The code uses that GENERAL factory: the geometric success probability is
(C-1)/C, its mean is C/(C-1), the threshold is initialized before clipping
epsilon to .644, and the subsequent C/epsilon/threshold updates match the
published algorithm. This order is intentional, not a reversed geometric
coin. C>=2 bounds auxiliary geometric means by two. The exact receipt's
stronger epsilon>.004 is sufficient for the advertised coarser .003 and
213000 expected base-coin bound. Native work, waits, discarded candidates,
nonlinear partners and final proposals are charged. The 85.2-million
expected-coin query upper bound is a finite bound, not a practical speed claim.

## 5. Positive observations and one continuous law

For finite cells, proposing mass A_i+L B_i and querying a conditional beta
Gaussian gives accepted unnormalized mass int_Ci f. The point used within
that cell is NOT automatically distributed according to the conditional
target. The refinement obstruction correctly preserves that distinction.
The two angular cells, their Gaussian masses and their source anisotropy
identities check; no radial output is substituted.

For continuous output, pointwise clipping satisfies

    E(M+W H)_+ = f+b,  b=E(-M-WH)_+.

Thus repeated attempts produce exactly the normalized ONE law
g=(f+b)/(1+B), not an unnormalized signed estimate. The upper acceptance
bound is deterministic. TV(g,f)<=B/(1+B) follows without any lower density
oracle. Independence of complete attempts, not independence of a cost from
its own acceptance, justifies the expected-work identity.

The mark bound is D phi(V). On V<=5 the Gaussian ratio exceeds D_eff, so
negative realizations are impossible. Outside that region phi=1. Therefore
the actual bias is bounded by int(D M^(3/4)-M)_+, not merely the larger
D_eff envelope tail. The analytic threshold is R=8.256457580378004... and
the two known Gaussian survival integrals give

    TV(g_t,f_t) <= 3.573967442659345... * 10^-15

uniformly in finite t. The normalizing denominator is included. The native
continuous() method proposes the correct mixture at the SAME full v, calls
the full query and uses max(0,relative+mark)/(relative+D_eff). It implements
the ideal-real algorithm described by the proof.

This is approximate, not exact full-law output. Neither the proof nor this
review promotes binary64 or seeded random.Random to a 10^-12 numerical-law
contract. Ideal uniforms, normals, exponentials, elementary functions and
uniformly bounded exact source-evaluator work remain explicit premises.

## 6. Executed intake and what it establishes

check_extension.py and REPLAY.json are owned by this review. They:

* verify all 32 frozen manifest entries and source preservation;
* reconstruct the exact 47-interval cover and margin below 199/200;
* verify bump joins/maximum, nonlinear/factory budgets and native gain
  completion identities;
* recompute the clipping and all-speed tail constants at 200-bit Arb precision;
* independently differentiate via second-order jet algebra, checking 795
  one-sided/ordinary derivatives in nine declared boxes, including both joins,
  r=0, speed zero and the tail end;
* replay the already acquired MOST restrictive interval [55/16,7/2] with
  its fixed controls through the producer's pure certifier. It returns the
  identical rational upper bound after 3842 box evaluations in .20257s.

The complete intake took 1.4134s after imports. The single interval replay is
NOT a second independent quadrature implementation or a new all-speed
acquisition. The point checks supplement, rather than prove, the analytic
all-box derivative reconstruction above. No new dynamics or stochastic paths
were generated. The frozen cohort's zero nonlinear proposals and zero clipping
events are correctly not used to validate nonlinear or clipping laws.

## 7. Decision and the remaining capability gate

The extension is mathematically substantive: the global weighted query now
admits arbitrary angular source dependence, and the clipped consumer provides
one positive continuous approximate law instead of unrelated finite detectors.
Its scope remains a very small, source-qualified near-equilibrium class of a
normalized homogeneous hard-sphere equation. Real-gas/source qualification,
finite-bit cost/error and implementation-level numerical-law accuracy are
not acquired.

The strongest ordinary comparisons are admitted. Published Hilbert/LVDSMC
pre-cancellation and multidimensional near-equilibrium simulation already
exist; weighted branching, Huber factories and clipped-mean rejection are
established ingredients. The same-source normalized full-law lineage meets
the same accuracy target and won the one fixed timing test, 1.8814s versus
12.1663s. The new relaxation bound is also supplied to ordinary methods;
the exact-lineage/Gaussian hybrid already has finite uniform-time cost at
fixed tolerance. No practical, unique uniform-time, all-incumbent or world
priority advantage is accepted here.

I found no consequential missing mathematical interface within the declared
extension. The next operational gate would be a bit/interval-qualified
continuous sampler or a matched validated transient solver, with source
evaluator precision and Huber rare-stage work paid. Merely refining another
row, adding a floating cohort or invoking near-equilibrium closeness would
not close that gate. No such additional capability is claimed by this review.

Primary reads for this review:

* Radtke--Hadjiconstantinou--Wagner, 2011, pp. 1--4, Eqs. 2, 6--9 and the
  stated linearized versus nonlinear scope:
  https://web.mit.edu/ngh-group/pubs%20final%20website/Radtke_PoF.pdf .
* Huber, 1308.1562v2, Theorem 1 and Sections 2.1--2.3:
  https://arxiv.org/html/1308.1562v2 .

The preceding radial theorem, Fournier lineage admission and earlier generic
clipped consumer remain inherited inputs only, at their already stated scopes.
