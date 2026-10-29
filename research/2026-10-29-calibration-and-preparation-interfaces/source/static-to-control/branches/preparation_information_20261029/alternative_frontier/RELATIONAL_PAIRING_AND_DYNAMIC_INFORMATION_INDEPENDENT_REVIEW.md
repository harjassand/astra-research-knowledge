# Independent review: relational phase pairing and exact dynamical information

29 October 2026. Ordinary proof review by
producer-workspace/different_consequential_opening. No numerical test was needed.

Follow-up receipt: RELATIONAL_PHASE_PAIRING.md SHA256
2a209f65c1ec24d6195723838960056c6b782cb52a0d07a387577df95715311a
incorporates the fixed/independent-time qualification and the scalar tangent
exception. A small wording correction was relayed: selection of high velocity
changes the conditional increment law, especially its mean; conditional on
the full stopping history the residual Gaussian variance is not the stationary
variance and need not be larger. This follow-up was a targeted check of the
corrections, not a second full review.

## Reviewed versions and result

- causal_frontier/RELATIONAL_PHASE_PAIRING.md:
  SHA256 00f77454067b635c0e643e979e57234837f7fee6c9f8d1856eaf029140b4aac9.
- causal_frontier/EXACT_FORCE_FEATURE_DYNAMIC_INFORMATION.md:
  SHA256 5ffae82b10e325024a47b980e4bb4e92078f32fb8e44e554b0c49b7253e2602f.
- Its static-assay dependency,
  causal_frontier/NATIVE_REFERENCE_FRAME_IDENTIFIABILITY.md:
  SHA256 2340f9a39d648598151bb0bdf37df6e3e6d19914bdb8143db00c98e792601e2b.

**Verdict:** the paired-quadrature construction, the exact-force-path TV
counterexample, and the explicitly static adaptive-assay KL lower bound
pass. The phase-pair timing bound needs a fixed/independent sampling-time
qualification. That correction does not affect simultaneous pairing or
the dynamical counterexample.

This review checks the new load-bearing claims at the declared interface.
It does not certify an actual sensor, potential field or Gibbs preparation.

## 1. Relational pairing: ordinary proof

Write the unit vectors as complex numbers Z=exp(i n x) and
H=exp(i(nx+phi)). Their pointwise product H conjugate(Z)=exp(i phi).
Thus its real and imaginary parts are exactly the dot and oriented-cross
expressions in equation (4). No state-distribution assumption is required.
The ensemble cross-covariance R_phi/2 follows by averaging z z^T=I/2
under uniform phase, but is unnecessary for one-pair reconstruction.

For the unpaired-law assertion, the translation x->x+phi/n removes phi
from the local quadrature and every local receiver force alpha dot h_phi.
It preserves free driver dynamics, uniform preparation and thermal noise.
Under a causal policy using only this local record, the same random policy
seed and identical record histories produce identical controls. This proves
whole-transcript equivalence by the pathwise coupling. The separately
observed external reference path has the same marginal law for every phi,
but its joint coupling to the local record changes. Simultaneous/synchronized
joint data are expressly outside the unpaired experiment.

For a unit vector u and report v with ||v-u||<=epsilon<1, v is nonzero.
The largest ray angle compatible with the error ball is arcsin(epsilon),
obtained at a tangent from the origin. Applying this separately to h and z,
then using the triangle inequality on the circle, gives (6). Both
arcsines are below pi/2, so the sum is below pi and the circular bound
is unambiguous. No independent-error assumption enters.

For centered isotropic Gaussian marginal sensor error in two dimensions,
P(||error||>eta sqrt(2 log(2/alpha)))=alpha/2.
A union bound suffices even when the two channels' noises are correlated.
The claim still requires the warranted marginal noise/calibration laws;
unknown bias or a hidden common phase error is not supplied by this formula.

The operator rotation error 2 sin(d_circle/2) is exact. A single paired
vector fixes SO(2), whereas higher-dimensional stabilizers generally remain.
The stated stabilizer qualification is appropriate.

### Small wording refinement

With only a scalar f=sin(nx+phi) and a reference z, one obtains a linear
constraint on the unit coefficient vector (sin phi,cos phi). Generically
there are two solutions, related by reflection. At the tangent values
f=+1 or f=-1 the noiseless solution is unique. Therefore change “One f,z pair
leaves a reflection ambiguity” to “One f,z pair generally leaves a reflection
ambiguity.” There is still no uniform scalar one-pair identification claim.

Two geometrically noncollinear reference rows determine the coefficient
vector through ordinary linear inversion. Its condition number and actual
feature errors remain resources; statistical independence is irrelevant
to that deterministic inversion.

## 2. Needed correction: timing at adaptive sampling times

Equation (8) is correct for fixed deterministic t and fixed lag Delta,
or for times/lag selected independently of the free stationary process.
In that setting the integrated stationary OU velocity is centered Gaussian,
with variance

    V_x(Delta)=2tau/gamma_d
              [|Delta|-(1-exp(-gamma_d|Delta|))/gamma_d].

The Gaussian tail bound (9) follows. The small-lag expansion is
V_x(Delta)=tau Delta^2+O(|Delta|^3), hence the stated 1/n timing scale
at fixed confidence.

**Stationarity alone does not justify this law at a history-selected
sampling time.** For example, acquire the first feature at

    T_K=inf{t>=0: |v_t|>=K}.

An exact local quadrature record permits detecting |v|=||h'||/n, so this
is a legitimate adaptive selection if arbitrarily resolved local histories
are allowed. For t after T_K, the OU strong Markov formula gives

    x_(T_K+Delta)-x_T_K
      =v_T_K (1-exp(-gamma_d Delta))/gamma_d + G_Delta,

where, conditionally on the stopping information, G_Delta is centered
Gaussian and

    Var(G_Delta)
      =(2tau/gamma_d)
       [Delta-2(1-exp(-gamma_d Delta))/gamma_d
                    +(1-exp(-2gamma_d Delta))/(2gamma_d)]
      =(2gamma_d tau/3)Delta^3+O(Delta^4).

For small positive Delta the mean displacement has magnitude approximately
K Delta. Choosing K much larger than the stationary Gaussian quantile makes
(9), used without qualification, false. The random hitting-time cost is not
claimed bounded; the example disproves unrestricted use of the stationary
increment law.

**Repair:** specify fixed/independently scheduled acquisition times for
(8)--(9). For adaptive acquisition use the already stated actual velocity
bound, or a warranted conditional velocity/increment estimate. Truly
simultaneous pairing needs none of these lag assumptions. Noise-selected
stopping can similarly invalidate unconditional marginal sensor tails unless
those tails are valid conditionally on the selection rule.

The last observation is a scope caution: the report currently introduces
Gaussian noise as a measurement model for one actual pair, not a selected
best-of-many pair, so its written one-pair Gaussian result is valid.

## 3. Exact continuous force path: common score verified

Let q=nx, z=q+theta, f=sin z, and beta=sqrt(2gamma_d tau). The kinetic
driver has continuous v and continuously differentiable x, so f belongs
to C1 almost surely and f'=n cos(z)v.

Because z has finite variation, Ito's product rule gives

    d f' =[-n^2 sin(z)v^2-gamma_d f'
                       -n A cos(z)sin(z-theta)]dt
                       +n cos(z) beta dW.

No Ito correction from z has been omitted. On cos(z)!=0,

    f'^2/(1-f^2)=n^2v^2.

The excluded set has zero time measure: at each deterministic time the
stationary Gibbs phase has an absolutely continuous density, and Tonelli
applied to its indicator yields zero expected occupation time. At endpoints,
f' exists regardless; feature extrema occur with probability zero there.
Set the quotient arbitrarily on the exceptional set.

This defines a measurable exact-path functional. For example, derivatives
can be represented by limits of rational finite differences on the C1
support; use an arbitrary value off that support. The absolute integral is
finite because it agrees almost everywhere with n^2|f|v^2 on a finite
interval with continuous v.

After integration, the two large deterministic terms cancel exactly:

    H_h=-A integral_0^h cos(z)sin(z-theta)dt
                  +beta integral_0^h cos(z)dW.

For theta=+pi/2 the drift is +A cos^2(z), and for theta=-pi/2 it is
-A cos^2(z). The same observable H_h is used under both hypotheses;
no hidden phase branch, laboratory x value or Brownian path is read.

Under the common actuator potential, q has density proportional to
exp(c cos q), c=A/(n tau). Integration of
d[sin(q)exp(c cos q)] over the circle gives

    E cos(q)=c E sin^2(q).

Since cos^2(z)=sin^2(q) for both hypotheses, E cos^2(z)=r(c)/c.
Consequently the means in (3) have opposite signs and difference
2Ah r(c)/c. Positive Bessel series give I1(c)>=c/2; the integral formula
gives I0(c)<=exp(c), so this gap is at least Ah/e for 0<c<=1.
There is no approximation in these identities.

Let B=2A^2h^2+4gamma_d tau h. Bounded drift and Ito isometry yield
E H_h^2<=B under either law. The stochastic integrand is adapted even
though it is not itself reconstructed as cos(z); only its squared bound
is used in this proof.

For any common score H and laws P,Q,

    |E_P H-E_Q H|^2
       <=2 TV(P,Q)[E_P H^2+E_Q H^2].

This follows from Cauchy--Schwarz with measure P+Q and
(dP-dQ)^2/(dP+dQ)<=|dP-dQ|. Substitution yields exactly

    TV(P_+,P_-) >= A^2 h/[8e^2(A^2h+2gamma_d tau)],

for n>=A/tau. Thus even a single ideal dynamic trial has a uniformly
positive best-test advantage. This conclusion requires no n-dependent
number of independent trials. It does not assert that a low-resolution
instrument can evaluate the score.

## 4. The static assay lower bound remains valid

In the stronger one-time phase readout z, the distribution is the von Mises
location family p_theta proportional to exp(c cos(z-theta)).
The score derivative is c sin(z-theta). The preceding integration by parts
gives Fisher information c r(c). Direct integration of the log-density
ratio gives

    D(p_theta||p_theta')
      =c r(c)[1-cos(theta-theta')].

Termwise comparison of the I1 and I0 positive series gives r(c)<=c/2.
Hence each static prepared-state report has KL at most
c^2<=A^2/(n^2 tau^2), even after observing the stronger z rather than sin z.

For adaptive settings, compare the two models at the same transcript history:
the policy selects the same psi and u, so the parameter difference is still
phi-phi'. A genuinely fresh Gibbs preparation gives exactly the stated
conditional location family. The conditional KL bound therefore sums by
the chain rule, including common randomized policies. Independent preparation
conditional on the actual chosen setting is substantive; stationarity of
unreset repeated observations would not substitute for it.

Pinsker yields N>=2delta^2 n^2 tau^2/A^2 for transcript TV at least delta.
The proof covers one static readout from each preparation. Giving the
experiment a subsequent exact feature path changes the statistical channel,
and its KL need not inherit the one-time bound.

For the mean-probe sufficient schedule, the precise asymptotic wording is:
at saturation u=A/n, its fixed-confidence trial count is Theta(n^2);
under the ceiling alone it is at least of that order and may be larger if
a smaller amplitude is chosen. This is a wording refinement, not a failure
of the lower bound or the dynamic challenge.

## 5. Actual physical scope

The relational protocol acquires a simultaneous joint reference that separate
laws cannot contain. It requires calibrated quadratures and their relative
phase. The exact dynamic protocol instead supplies an unlimited-resolution
C1 feature path and its derivative. Neither operation is obtained simply by
declaring bounded actuator amplitude.

The dynamic score's quotient near |f|=1 and cancellation of terms of order n
make its numerical/sensor stability a separate obligation. No finite-noise,
finite-bandwidth implementation is proved. The source explicitly acknowledges
this, and its reference potential also changes the driver, outside the
receiver-only control class of earlier Gaussian transcript bounds.

The natural equally informed alternatives are ordinary phase calibration,
paired-feature regression and kinetic force inference. The checked addition
is the native interface separation and the precise failure of the static
information ceiling for a stronger dynamical experiment; no faster estimator
or thermodynamic acquisition advantage has been established.

