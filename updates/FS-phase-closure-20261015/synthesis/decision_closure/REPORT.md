# Dynamic decision closure from joint pulse-response calibration

**Status:** internally proved conditional results and synthetic calculations.
No new laboratory data, validated material model, historical novelty,
physical advantage or qualifying major scientific operation was acquired.

The retained advance is a precise way to extend a steady dark-control
comparison to all dynamic schedules in a small, explicitly acquired kinetic
class. It uses stored-inventory geometry, joint pulse-history calibration
moments and a cost-aware dual witness. It also gives an exact limit: sparse
calibration cannot bound arbitrary untested joint controls without such a
structural class. Existing transient kinetic experiments, dissipativity,
moment optimization and direct control trials are strong competitors.

## Reconstruction and exact scope

Source main pin is `846f185763ed3a27310fad4ce9471ba324d1e5f4`. Read the supplied
closure README and script, decisive narrative sections and current N804,
N820, N799 and N821 scopes. No incoming files, frozen earlier packets or
repository files were changed. Root handles the incoming audit replay;
this worker executed only its separate calculations.

The source's two positive-Arrhenius populations give methane selectivity
0.60 at every common temperature but approximately 0.948264 under selective
thermal heating. Its corrected local Minkowski-sum model is necessary.
The surviving finite module/resource LP is a valid outer bound for that
declared steady library, conditional on actual response/cost acquisition
and common detector/context. It does not cover arbitrary dynamic operation
and does not turn fractional time-sharing into an acquired device.

Our additional model is an adsorption/conversion inventory x:

\[
 \dot x=a(1-x)-b(t)x,\qquad r(t)=b(t)x,
 \quad b(t)=b_0+(b_1-b_0)u(t),\quad u\in\{0,1\}.
\]

It is a restricted dark kinetic model, with a>0 fixed and b0,b1>0. The
normalized running resource is hot duty, after subtracting a measured base
cost and scaling by the measured mode-cost difference. Model errors,
inventory initialization, actual switching waveforms and all additional
energy/feed/reset costs remain explicit.

## Strongest theorem and a dynamic failure of steady closure

For hot-duty budget f, let bar b=b0+(b1-b0)f. Every schedule, including
adaptive switching, obeys

\[
 \int_0^T r\,dt\le T\frac{a\bar b}{a+\bar b}
       +V_p(x(0))-V_p(x(T)),
 \quad V_p(x)=x-p\log x,
 \quad p=\left(\frac{a}{a+\bar b}\right)^2.
\]

The proof is the exact identity
\(r-pb+\dot V_p=a(1-x)(1-p/x)\), whose gap from
\(a(1-\sqrt p)^2\) is \(a(x-\sqrt p)^2/x\ge0\). Thus there is no
Markovian state-estimation or history-enumeration oracle hidden in the
online bound. The kinetic equation and its uniform error allowance must
nevertheless have been acquired.

With cyclic endpoints, the sharp ideal average bound is
\(C(f)=a\bar b/(a+\bar b)\). For a=1, b0=.1, b1=10, f=.5, steady-mode
time-sharing gives only 0.5, whereas C=101/121≈0.834710744. The synthetic
period-.1 schedule with duty .48 and a separately charged .001 cost per
transition gives 0.828254532 at total normalized cost .5 under instantaneous
ideal mode dynamics. This is a memory/resource counterexample, not a
measured reactor performance claim.

Arbitrarily fast switching attains C only in the ideal zero-transition-cost
model. A constant intermediate b=bar b at the same complete cost already
attains the same benchmark and is a mandatory comparator whenever available.
Actual thermal settling can invalidate the assumed waveform; it must be
measured or included as another dynamic mode/residual. The theorem retains
initial/final inventory. An empty reset needs a separately charged loading
prefix before the logarithmic potential can be applied.

## A conditional two-history physical acquisition interface

For acquired empty inventory and a common stable detector scale/offset,
the two mode transients have the form
\(y_j(t)=d_0+A_j(1-e^{-k_jt})\). Distinct poles identify the entire restricted
joint model via

\[
 P=(k_1A_1-k_0A_0)/(k_1-k_0),\quad
 a=k_0-k_0A_0/P,\quad b_j=k_j-a,\quad g=P/a.
\]

This eliminates an independently supplied detector scale or microscopic
site count for a detector-space decision; an unknown constant inventory
scale can be absorbed into g. The common offset comes from the empty-state
rate. Two actual transient history families can therefore replace an
unbounded binary-history library within this model.

This is elementary transient identification, already within the territory
of TAP/SSITKA and model-based experimental design. Close/coincident poles,
uncertain empty preparation, heterogeneous sums of exponentials, detector
drift/nonlinearity or a wrong kinetic class break the inverse. Fit quality
on two traces is not a uniform guarantee for untested histories. A chemical
yield claim also needs a product-calibrated detector; a raw detector-space
contrast does not itself establish methane yield or energy efficiency.

An unknown common stable linear detector filter can also cancel exactly.
After common background removal and zero detector memory, the two Laplace
responses satisfy
\(Y_1(s)/Y_0(s)=(b_1/b_0)(s+k_0)/(s+k_1)\). Three distinct positive arguments
identify this rational function and recover a,b0,b1 without deconvolving
detector bandwidth or gain. Finite truncated integrals need a measured rate
envelope/tail allowance and nonvanishing denominators. DC gain, product
calibration and finite-window detector storage remain paid inputs; no
zero-shift response is inferred from finite positive-shift data. A
mode-dependent filter or unequal initial detector memory defeats the
cancellation. This is a conditional measurement reduction, not a new
general blind-identification claim.

## Joint heterogeneity: bound the decision, not every type

Let theta carry a whole correlated tuple of adsorption/conversion rates,
positive task weight and resource coefficient. Let mu be the fixed unknown
population measure over an acquired compact type class. Execute complete
pooled calibration histories l; their means are
\(m_l=\int\phi_l(\theta)d\mu\). In particular, a cold-hot pulse history
depends on both mode kinetics through retained inventory. It constrains
their joint association instead of separately estimating marginal rate
histograms and assuming a pairing.

For a resource price beta, compute the type support
\(h_\beta(\theta)=\max_{0\le f\le1}[q_\theta C_\theta(f)-\beta e_\theta f]\).
Any global majorant
\(\lambda_0+\lambda\cdot\phi(\theta)\ge h_\beta(\theta)\) yields

\[
 J_{dark}\le\beta B+\lambda_0+\lambda\cdot m,
\]

plus finite-inventory/model-error terms. The generalized-moment dual is
sharp for its declared population and type-addressable outer control class
under the stated compactness/interior conditions. Type-addressability and
zero-cost limiting controls are not claimed to be physical capabilities.
The bound is conservative for a smaller real control class.

All calibrations and the challenge use the SAME mu and the SAME common
detector nuisance. A joint confidence ellipsoid adds
\(\rho\sqrt{\lambda^T\Sigma\lambda}\), retaining covariance. A common gain
and background remain common variables in all equations. Detector drift,
reaction/transport coupling and parameter-domain misspecification require
their own acquired allowances; arbitrary such effects are not solved by
the moment program.

In a supplied twelve-type synthetic class, two single-mode pulse integrals
give dark upper bound 0.641442361. Adding one joint cold-hot pulse lowers it
to 0.628798404 without recovering the twelve weights. Five pulse moments
give 0.625135732; the deliberately known true mixture's relaxed capacity
is 0.617464681. A synthetic decision threshold of 0.64 is unresolved by the
two-moment bound and resolved by the three-moment bound before acquisition
error is included. The threshold is not an illuminated laboratory result.

These are numerical exercises of an exact dual theorem on a finite supplied
class. The continuum support inequality is not certified by checking a
parameter grid. Sparse optimal latent measures likewise do not acquire the
true physical type class.

## Calibration compression has a precision price

For a witness fixed before confirmatory data, independent full-history
blocks with sub-Gaussian noise proxies sigma_l and costs c_l have optimal
variance proxy

\[
 \frac{(\sum_l|\lambda_l|\sigma_l\sqrt{c_l})^2}{C}
\]

at total cost C. This follows directly from Cauchy-Schwarz and gives the
optimal allocation \(n_l\propto|\lambda_l|\sigma_l/\sqrt{c_l}\). Reset,
settling, gas, detector calibration and catalyst-aging costs belong in c_l;
closely spaced detector readings are not independent reactor blocks.
Shared-block estimates use their actual covariance instead.

In the synthetic example the three-moment certificate has coefficient
norm 17.0842; the tightest five-moment certificate has norm 147.0281. At
equal unit costs/noise proxies and threshold 0.64, the five-moment witness
requires approximately 42.1 times the confirmatory exposure cost of the
three-moment witness despite its tighter noiseless bound. A larger library
can of course reuse the earlier cheaper witness. The correct optimization
target is the decision bound with its acquisition error/cost, not the
tightest noiseless endpoint.

## Exact limit and strongest matched competitors

Without a structural response class, M legal joint histories need M exact
queries in the deterministic worst case to certify their maximum below
one: an untested history can hide a unit spike while all queried histories
agree at zero. Under a uniformly placed spike, k queries find it with
probability at most k/M. Sparse calibration therefore cannot provide
assumption-free closure of arbitrary coupled controls or detector nuisances.
An algorithm may decline to certify, but then it has not resolved the
all-zero decision.

The closest methods already cover the proposed primitives:

- [Willems, dissipative systems](https://doi.org/10.1007/BF00276493) supplies
  storage/supply inequalities. Our scalar potential is a model-specific
  explicit instance, not a new theory of dynamic certification.
- [Catalytic resonance theory](https://pubs.rsc.org/en/content/articlelanding/2019/cy/c9cy01543d)
  already studies dynamic catalytic enhancement and pumping. A gain over
  steady-mode mixing does not establish new scientific access.
- [Kim, O'Connor and Reece, transient site kinetics](https://www.nature.com/articles/s41467-024-46496-1)
  uses actual pulse experiments, isotope labeling, kinetic modeling and
  DRIFTS to separate pathways. It is a substantially stronger physical
  competitor than an uninformative bulk thermometer.
- [Model-based TAP experimental design](https://arxiv.org/abs/2309.15786)
  already selects pulse intensity, delay and temperature to estimate or
  distinguish kinetic models. An equally informed baseline may select the
  same joint pulse and use the same parameter/moment geometry.
- [Huang, Benesty and Chen, SIMO cross-relations](https://www.jingdongchen.com/conferencespapers/%282003%29Adaptive%20blind%20identification%20of%20SIMO%20systems%20using%20channel%20cross-relation%20in%20the%20frequency%20domain.pdf)
  is established multichannel blind-identification prior art. Our common
  detector cancellation is a restricted rational transfer-ratio calculation;
  its kinetic parameterization and acquisition costs do not justify a claim
  to invent common-factor elimination.
- [Bertsimas and Popescu, moment optimization](https://www.mit.edu/~dbertsim/papers/MomentProblems/Optimal-inequalities-in-probability-theory-A-convex-optimization-approach-SIAM15.pdf)
  gives the established dual-majorant framework. Standard support-function
  optimization/column generation computes our bound from the same inputs.
- [Baffou et al., photothermal controls](https://www.nature.com/articles/s41377-020-00345-0)
  provides existing physical procedures for separating thermal explanations.
  These controls remain required when a mechanistic claim is made.

Direct randomized complete-policy trials already choose between executable
dark/illuminated policies. The extra closure certificate earns its cost only
if excluding a broad admitted dark family changes a further decision, such
as stopping an optical-development route or validating a new operating
envelope, more cheaply than informed direct policy search and trial. No
matched empirical advantage was established here.

## Highest-value next test and unresolved physical premise

Use one stable, mass-balanced microreactor with two finite metered dark
waveforms. Acquire empty preparation, two complete transients and one joint
pulse, preserving their common detector and kinetic uncertainty. Estimate
the actual switch/settling waveform and energy, gas and reset costs. Fix one
decision witness on discovery data and use independent whole blocks for
confirmation. The exact same detector-space decision and total exposure
budget go to an informed transient-model/support-function baseline and
direct policy trials. A constant intermediate thermal mode at matched full
cost is included whenever available.

Hold out finite pulse histories specifically chosen to stress stored
inventory, state preparation and detector drift. A violation rejects the
admitted model/certificate. Passing held-out tests is useful validation but
does not logically certify all hidden heterogeneity or arbitrary histories.
Any claimed universal extension still needs an acquired structural class
and uniform residual envelope; this is the strongest missing physical
premise. No bare finite calibration can supply it in the unrestricted class.

## Reproduction and evidence status

`PROOFS.md` gives the exact storage, identification, joint-moment, precision
allocation and sparse-query statements. `calculate.py` checks the algebra
symbolically, 256 finite schedules, finite periodic controls, exact rational
transient recovery and finite-type moment duals. All final assertions pass.
The largest final finite-type support correction is 8.35e-9; it is a floating
calculation allowance, not instrument precision or an interval proof.

An initial column-generation run did not meet a stopping target tighter than
the solver's default tolerances. `calculation_failures.txt` preserves that
failure and the explicit solver/stopping correction. Source bytes were
untouched. `calculation_results.json`, stdout/stderr, source receipts and
the final hash inventory make the scope reproducible. There is no claim of
a new experimentally obtained closure or of completion of the broad mission.
