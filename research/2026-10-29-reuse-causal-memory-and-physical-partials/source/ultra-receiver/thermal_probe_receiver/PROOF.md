# Paid thermal scalar qualification: construction and its limits

The output is a set of finite, correlated-record classification contracts
and actual directed scalar inputs. It is NOT a measured physical decision.
The missing instrument/bath/calibration premises stay explicit. Strong
ordinary source-aware Gibbs inference, passive calibration and driven
mean measurements receive the same information.

## 1. Locked scientific accesses and root input review

The two assigned sources have N32, p1,v32, theta1, Delta1/2 and exactly
one unknown quartic alpha at v. Their matrices are SEPARATE warranted
accesses, K3=3I-A_path and K2=2I-A_path. K2 still has the boundary
pinning encoded by its literal matrix; an ungrounded singular graph
Laplacian is not substituted. All other quartics are known absent.

The model is `dX=-grad V dt+sqrt(2theta)dW`, V=X^TKX/2+alpha Xv^4/4,
with calibrated Euclidean mobility and distributed independent bath
noise at EVERY node. It is not automatically an RC Johnson-noise law.
No actual device, zero initialization, temperature record, gain, readout
or physical conversion of model time units has been acquired.

Root's `root_thermal_probe/PROOF.txt` was whole-read. Gaussian elimination,
the scalar monotonicity/derivative, nonasymptotic positive signal bound,
Gaussian moment domination, gap/read bounds and zero/general-initial
coupling are sound at their stated interfaces. The event calculation
in its loose derivative floor gives the claimed9/(128pi) constant.
Mobility/temperature factors are consistent. In particular the variance
contrast is

    s_alpha=(g/d)^2[theta d-v(alpha)],
    g=R_pv, d=R_vv, b=R_pp, R=K^-1,
    v(alpha)=Var_alpha Xv.

It increases with alpha. Both connected endpoint paths have g>0; a
disconnected port with g0 would not have a strict signal. The generic
strict-signal condition was made explicit in the updated BLUR_PROOF.
A's archived earlier BLUR input remains historical; its actual connected
K3 source and frozen numerical interface are unchanged.

The independent scalar input is `MOMENTS.json`. Write

    z=Xv/sqrt(theta d), beta=alpha theta d^2,
    I_m(beta)=integral_0^infinity z^m exp(-z^2/2-beta z^4/4)dz.

Then v(Delta)=theta d I2/I0 and
`s_Delta=theta g^2(1-I2/I0)/d`. Directed intervals give

| Access | v(Delta) | s_Delta |
|---|---:|---:|
| K3 |[.32578365214036,.32578365216492]|[4.99059151091e-28,4.99059151310e-28]|
| K2 |[.57138365221696,.57138365240448]|[.000388977848918,.000388977849102]|

The known endpoints are g3=1/F66,d3=b3=F64/F66 and
g2=1/33,d2=b2=32/33. No matrix simulation supplies these values.

## 2. Directed infinite-domain acquisition

`acquire_moments.py` integrates on[0,12] with2048 Simpson panels.
For f_m(z)=z^m exp(-z^2/2-beta z^4/4), define

    P_0=z^m, P_(j+1)=P_j'-(z+beta z^3)P_j.

Thus f_m''''=P_4 exp(-z^2/2-beta z^4/4). On each panel[l,r],
`exp(-q(l)) sum_k |P4_k|r^k` bounds its fourth derivative. The panel
Simpson error is at most h^5/2880 times that bound. Every node value,
sum, derivative bound and ratio is rounded outwards. The Gaussian
tail enclosures are

    tail0<=exp(-L^2/2)/L,
    tail2<=(L+1/L)exp(-L^2/2), L12.

No adaptive quadrature success flag or special-function error estimate
is assumed. The two cases acquired8194 exponential nodes in0.5826s
after imports. The finite moment intervals were independently whole-
reviewed by B in `bridge_cross_review/thermal_receiver/MOMENT_REVIEW.md`.
That review is scoped and does not stand for unfinished receiver review.

Classical quartic partition/Bessel representations and univariate
integration are strong ordinary alternatives. No novelty or speed
advantage for evaluating this one-dimensional law is asserted.

## 3. Relative blur and long exposures

`BLUR_PROOF.md` proves the exact covariance-column Duhamel relation.
For the cooperative M-matrix dynamics its nonlinear forcing term is
nonnegative, so for stationary covariances

    C0_pp(t)-Calpha_pp(t)
       >=s_alpha L_N(t),
    L_N(t)=(exp(-Kt)R)_pv/g.                              (1)

The weaker bound exp(-Kpp*t) retains2/e of the contrast at exposure
1/Kpp. There is also a short proof of forcing positivity suggested by
B's independent reconstruction. Reversible integration by parts gives

    Cov_pi(Xp,P_t Xv^3)
       =theta integral_0^infinity E[partial_p P_(s+t)Xv^3]ds>=0.

The flow derivative is entrywise nonnegative, so the integrand equals
an expectation of3Xv(s+t)^2 J_vp(s+t)>=0. Domination by the harmonic
kernel and Gaussian second moments justifies the integral. FKG is an
alternative established proof, not an additional native measurement.

A's accepted `thermal_time_trace/LONG_EXPOSURE_INTERFACE.md` supplies
the useful endpoint travel-law refinement. It extends to literal K2
by the same determinant identity: if D_N(c)=det(cI-A_path),

    integral exp(-zt)(exp(-Kt))_pv/g dt
       =D_N(c)/D_N(c+z)=product_j lambda_j/(lambda_j+z).

Thus the positive density is that of a sum T of independent exponential
variables with rates lambda_j, and L_N is its survival function. This
is an auxiliary mathematical distribution, not sampled hidden data.
Let mu=TrR, w=TrR^2. For a rectangular exposure delta,

    variance contrast >=s_Delta B_N(delta),
    B_N(delta)>=2mu/delta-(mu^2+w)/delta^2.

The single analytic choice

    delta=3(mu^2+w)/(2mu),
    retention>=8mu^2/[9(mu^2+w)]                          (2)

is used, with no exposure grid search or optimality claim. For K3
the exact scalars are consumed from A's frozen INTERFACE.json. For K2
the same continuant and its two derivatives are acquired with93
integer recurrence updates. They yield delta381.25 at N32. All32
spectral modes per access are also outward enclosed to compute the
actual harmonic exposure reference/proxy, rather than withholding
that available tightening from the ordinary method.

## 4. Variance, covariance, and zero-start costs

Let F_j be an exposure mean and Z_j=F_j+eta_j, where independent
centered Gaussian electronics have variance Sdet/delta or a stated
upper bound. The PSD contract is Sdet=1/100 in these model units.
It is not an acquired detector and is not kept constant per read
when exposure changes.

The accepted product-Poincare lemma gives a pointwise derivative-form
bound by the harmonic exposure variance V_delta. It uses
0<=J(t,s)<=exp[-K(t-s)] and the entrywise positivity of R. Initially
Brascamp--Lieb gives theta R; tensorize with Wiener Poincare and
electronics. For S_delta=V_delta+Sdet/delta,

    Var Z_j^2<=4S_delta^2.

Conditioning separated blocks on endpoints and applying the equilibrium
gap bounds the cross-read covariance. At starts separated by
h=delta+1/kappa,

    Var[Q^-1 sum Z_j^2]<9S_delta^2/Q.                    (3)

The executable JSON uses RAW squares Z_j^2 with reference
V_delta+sigma_delta^2. BLUR_PROOF's earlier debiased convention uses
Z_j^2-sigma_delta^2 with reference V_delta. They are equivalent ONLY
when matched; no noise variance is subtracted from the raw-score
consumer's supplied reference. Cross and mean plans also use their
explicit raw score expressions.

No nonlinear exposure is assumed Gaussian and no raw reads are IID.
The harmonic reference is evaluated by its positive spectral sum:

    V_delta=sum_j theta w_j/lambda_j
           *2(lambda_j delta-1+exp(-lambda_j delta))/(lambda_j delta)^2,
    w_j=2 sin^2(j pi/33)/33.

Pi has an exact Machin arctangent enclosure and sine/cosine use
explicit Taylor remainders. These64 spectral modes are paid finite
source computations. The arithmetic contract is80-digit directed
Decimal algebra and correctly rounded sqrt/exp with adjacent widening.

For a scalar signal lower sL, reference-side combined mean error at most
sL/8, and risk zeta1/20, choose

    Q>=128*9*S_delta^2/(zeta*sL^2).                     (4)

The source starts at zero; this is a mathematical initialization input,
not an acquired laboratory reset. Instead of silently assuming
equilibrium after a free burn-in, average the root's synchronous
coupling error over ALL the actual record times. Put

    M=theta TrR, qd=(1-exp(-kappa delta))/(kappa delta),
    A=2sqrt(M S_delta)qd, B=M qd^2.

At burn t0 and start spacing H, the average score coupling error is
bounded by

    [A exp(-kappa t0)/(1-exp(-kappa H))
       +B exp(-2kappa t0)/(1-exp(-2kappa H))]/Q.           (5)

Geometric numerators were bounded by1; a huge-Q exponential is never
evaluated or underflowed. The program finds a finite integer t0 making
(5)<=zeta*sL/16. At these actual large budgets t0=0 qualifies: the
initial transient is DILUTED AND BOUNDED, not absent. The proof for
general initial second-moment M0 replaces M in the coupling distance
by2M0+2M. No arbitrary unbounded initial law is covered.

Markov at threshold sL/8 bounds coupling failure by zeta/2, and
Chebyshev with(3),(4) bounds stationary error by zeta/2. Threshold the
measured decrease at sL/2. Including calibration, each hypothesis has
risk at most zeta and the plan returns after its finite record.
The compiler computes budgets, not a hypothesis in the absence of data.

## 5. Paying coarse electronics rather than inventing precision

The ordinary square-score plan uses the calibrated reference
V_delta+sigma^2. If sigma^2 is unknown, it is not legitimate to subtract
it to extremely high precision for free. The receiver supplies two
qualified alternatives, retaining temperature/gain/model obligations.

First, if only0<=sigma_j^2<=Sdet_max/delta is known, use raw squares and
reference V_delta. Under the null their mean is AT LEAST V_delta;
under the alternative it is at most V_delta-s+Sdet_max/delta. Therefore
the effective signal is

    s_robust=s-Sdet_max/delta-reference_enclosure_width.  (6)

If it is positive, (3)--(5) apply with this smaller signal, without
noise-variance subtraction or precision calibration. If it is not
positive, this particular rule is marked NOT_QUALIFIED. That failure
is not an impossibility theorem for the full record. At actual K2
long exposure, (6)>0.0002204490489607; it needs937983404 raw reads
and at most4.61180307509e11 model time units. At K3 it fails because
the coarse electronics envelope dwarfs the signal.

Second, pair adjacent nonoverlapping exposures and use product Z1 Z2.
Its expectation contains no independent centered electronics variance.
Take delta=mu/4. Every lag in the pair is at mostmu/2; Cantelli applied
to the auxiliary travel time gives

    contrast >=s_Delta*mu^2/(mu^2+4w).                   (7)

The harmonic reference is
`sum theta w_j/lambda_j *[(1-exp(-lambda_j delta))/(lambda_j delta)]^2`.
Pointwise derivative-form Cauchy--Schwarz gives
Var(Z1 Z2)<=4S_delta^2. Pair starts at2delta+1/kappa again give the
correlated9S_delta^2/Q bound. Formula(5) also bounds its zero-start
coupling: use the same supremum bound for each of the two adjacent
exposure errors. There are2Q actual readouts. These variance/covariance
plans are alternatives for different calibration contracts, not extra
independent evidence manufactured from the same nonexistent data.

This cross plan needs only a coarse PSD upper and independent zero-mean
electronics, but still needs calibrated zero offsets/gain and a
qualified reference. Unknown correlated/colored detector drift can
change its mean and must not be hidden inside an independent-noise model.

## 6. Calibration and actual consumer qualification

Every plan lists its required combined SCORE-MEAN error <=sL/8. This
includes reference physics, gain, noise subtraction if used, offset,
digitization/overflow and timing/model errors. Source K/theta/mobility
are scientific premises, not parameters established by these numerical
integrals. A known mathematical reference does not supply a physical
calibration certificate.

The displayed gain tolerances are conservative reference-side
sensitivities when they alone use the entire budget. Their observation
convention is Z=G F+eta: gain acts on the physical exposure F BEFORE
independent additive electronics eta. For squares or
products, |G-1|<=sL/(24Rref) implies
|G^2-1|Rref<=sL/8 for |G-1|<=1. Variance/covariance under every
alternative is between0 and its harmonic reference. For mean scores
|G-1|<=sL/(8Rref) pays that error. These are NOT a joint uncertainty
rectangle for an unknown theta or K: the alternative contrast must be
requalified if those scientific parameters vary. The JSON says so.

In particular, the coarse-PSD variance rule uses Rref=Vdelta because
electronics are added AFTER this physical gain. If an instrument instead
applies gain to the complete raw read, its square-mean sensitivity must
use Vdelta+sigma_max; the displayed Vdelta-based gain number must not be
used for that instrument. The governing externally warranted combined
score-mean error bound covers either convention once qualified. This
clarification changes no numerical plan, signal, count or risk bound.

Without qualification the actual receiver returns NO_QUALIFIED_RECORD;
it never interprets its computed read count, a model hash, or a source
PDF as measured calibration. No data or calibration readout has been
generated for this work. Full-cycle physical performance is therefore
NOT_ACQUIRED.

Long exposure can improve the required background calibration too.
For K2, its electronics variance upper is only2.623e-5, less than the
proved thermal contrast. The coarse-noise plan needs a combined
variance-mean error below2.756e-5 and its one-source gain tolerance is
about2.066e-4. These are required tolerances, not obtained laboratory
accuracies. Original K3 still requires extraordinarily small absolute
score error despite the better exposure.

There is a sharp limitation at the scope of a supplied variance-only
calibration contract: if the allowed electronics-variance uncertainty
can shift by the whole blurred contrast, harmonic and nonlinear
hypotheses can have exactly the SAME raw variance. Infinite averaging
does not resolve that statistic. This is not a full-distribution or
time-series impossibility claim; cross-covariances and likelihoods
have more information, and the constructive alternatives above use it.

## 7. Strong same-model active comparators, actually acquired

An equally informed method receives all other nodes' exact linearity.
At constant force U e_p the hidden equilibrium variable has scalar
density proportional to

    exp[-(x-Ug)^2/(2theta d)-alpha x^4/(4theta)].

The port mean is U(b-g^2/d)+(g/d)E X. The zero-field susceptibility
is Var(Y)/theta, so SAME-bath small-drive contrast is also order g^2.
The passive g^2 versus deterministic g^4 distinction changes the bath
interface; it does not show passive beating active on identical hardware.

`acquire_active.py` pays finite U1, rather than equating a derivative
to a finite difference. For h=Ug/sqrt(theta d), let

    r_h=E_beta[z^2 sinhc(hz)]/E_beta[cosh(hz)].

Then the port mean decrease is U g^2(1-r_h)/d. For U1 the already
acquired m2 and Gaussian absolute-moment domination give

    m2 exp(-h^2/2)<=r_h
       <=m2+(h^2/6)(h^4+6h^2+3)exp(h^2/2).

The upper follows from `sinhc(t)-1<=t^2 cosh(t)/6` and the ordinary
Gaussian tilted fourth moment. No new weak-field quadrature is needed.

For U=1/g, h is order1, so directed tilted integrals actually acquire
the comparator. `sinhc(hz)=integral_0^1 cosh(thz)dt` supplies an absolute
fourth-derivative bound without dividing a tiny field. Positive-coefficient
derivative envelopes and shifted Gaussian tails close its2048-panel
Simpson integrals. For all alpha>=Delta the mean decrease is at least
its Delta value: the absolute scalar likelihood ratio decreases with
alpha and `z tanh(hz)` increases. Actual high-peak signals are
about1.95833e-14(K3) and0.01365895(K2).

Contiguous readouts of duration delta equal one continuous time average.
The derivative/Poincare domination is unaffected by a CONSTANT added
force, so a stronger ordinary mean plan uses

    Var(mean over T)<= [2theta(R^2)_pp+Sdet]/T.            (8)

It does not pay an artificial independent-read spacing. The compiler
rounds T up to a whole number of actual exposure reads. It pays zero-
start transient using

    E_U||X||^2<=theta TrR+U^2(R^2)_pp.

Indeed the forced mean is componentwise between0 and U R_.p: the
scalar tilted mean is between0 and Ug, and its conditional Gaussian
Schur covariance is entrywise nonnegative for this M-matrix. Covariance
is at most theta R by Brascamp--Lieb. Synchronous averaging gives
coupling <=sqrt(M)min[1,1/(kappa T)]exp(-kappa t0). This forced M,
not the unforced burn constant, is used even at U1/g.

The no-internal-bath DC comparison is also paid on the SAME one-quartic
model. Its exact scalar root is

    x+Delta d x^3=Ug, y_ref-y_alt=Delta g x^3.

One hundred exact rational bisection steps qualify the root. Electronics
averaging needs T>=128Sdet/(zeta signal^2), and deterministic settling
is bounded by U sqrt((R^2)_pp)exp(-kappa t0). This comparator is NOT
T's more general all-quartic promise or its conservative U~1/N plan.

U1/g charges peak27777890035288(K3) or33(K2), reference displacement
10610209857723 or32, and reference quadratic loading energy
147364621339579114964664612 or528. The last quantities are recoverable
stored/load energy, NOT irreversible full-cycle work or power U*y.
Mechanical work is integral U dY; equilibrium holding can have zero
mean work, and reversible return can recover energy. Native actuator
limits, preparation, detector linear range and gain at those amplitudes
are not acquired merely by reporting the much lower read count.

## 8. Actual budgets and what survived comparison

All results below are sufficient95% contracts in native MODEL time
units; they are not observed stopping times or seconds. Initial start
zero is explicit. The actual averaged-transient bounds qualify t0=0
at these large required records; no IID/stationarity shortcut is used.

| Access/plan | Raw readouts | Model observation duration |
|---|---:|---:|
| K3 passive long, calibrated electronics variance |3.0640e55|7.0812e56|
| K3 passive adjacent-product, coarse PSD only |1.8249e57|7.3637e57|
| K3 same-bath driven mean U1 |1.6340e56|3.6144e57|
| K3 same-bath driven mean U1/g |1.0612e29|2.3473e30|
| K2 passive long, calibrated electronics variance |749115554|3.6832e11|
| K2 passive long, coarse PSD only |937983404|4.6119e11|
| K2 passive adjacent-product, coarse PSD only |61384477958|6.1719e12|
| K2 same-bath driven mean U1 |935016657|3.5648e11|
| K2 same-bath driven mean U33 |756538|2.8844e8|

The no-bath deterministic DC U1 durations are3.6299e109(K3) and
1.4441e14(K2); U1/g durations are1.7855e29 and517505.5, with their
charged peak/displacement/loading promises. These are different bath
interfaces and cannot establish same-hardware thermal superiority.

Compared with the fixed-short-exposure sufficient variance plans, the
long-window duration upper is about0.02990(K3) or0.01610(K2) times as
large. This is a qualified refinement of a conservative construction,
not a lower bound on optimal experiment cost. The same-bath U1 mean
plan already slightly beats the K2 variance plan's duration; high peak
can change the trade-off dramatically. No passive algorithmic winner
over the strongest ordinary same-access methods is established.

There is a useful analytic scaling improvement before calibration and
physical-model costs. For K2 and general N,

    mu=N(N+2)/6,
    w=N(N+2)(2N^2+4N+9)/180,
    delta=(7N^2+14N+9)/20,
    retention=40N(N+2)/[9(7N^2+14N+9)],
    (R^2)_pp=N(2N+1)/[6(N+1)].

The conditional scalar signal is Theta(N^-2), while S_delta=O(N^-1).
Thus this long-exposure construction admits Q=O(N^2) and duration
O(N^4), plus O(N^2 log(N/zeta)) burn-in when needed, rather than the
short/gap-spaced sufficient O(N^6) duration. It is not a full time-series
lower bound. Gain/reference relative accuracy scales O(N^-1) because
the long background is O(N^-1); electronics variance is O(N^-2), so
a fixed-relative coarse PSD bound can suffice. Qualification of the
literal K2 topology, other quartics' absence, temperature, clocks and
long-term drift is still an unpaid physical cost. Direct known-spectrum
reference acquisition is O(N), not a free all-N oracle. Executable
receipts here are only the assigned two N32 sources.

For fixed-gap K3 the analogous long-window scaling remains exponential
in depth: sufficient duration O(g^-4/N). A's separate accepted full-port
trace information theorem also gives a finite-Delta zero-start duration
lower above7.4499e22 model units at this actual source. It is stronger
than an IID-snapshot-only comparison but does not match our sufficient
bound; no g^-4 full-trajectory optimum is inferred.

## 9. Prior, costs, and final capability judgment

Perez-Garcia et al., [arXiv2305.07245](https://arxiv.org/pdf/2305.07245),
sections2--3, equations19--25 and32--36, was read in the primary
30-page preprint. It already accounts for finite-integration covariance,
non-Markovian sampled records and likelihood/calibration alternatives
for a harmonic optical trap. It is an equally informed antecedent,
not a method intentionally deprived of blur or sampling information.
The nonlinear one-hidden-quartic retention is paid separately here;
the harmonic full-record likelihood is not declared exact for that
alternative. No demonstrated32-node noiseI mechanical device is
inferred from a single-trap paper. PMC returned a browser challenge
and a public CNR PDF returned403; they were left intact. The public
arXiv governing text was then acquired and read. No paid source or
access-control bypass was used.

Gaussian conditioning, FDT, scalar potential inference, birth-death
travel laws, FKG/cooperative dynamics, Poincare, correlated averaging,
long integration and calibration-aware statistics are established.
The result is their explicit source-qualified finite receiver, not a
new generic calibration or fluctuation-dissipation principle. Existing
Astra Gaussian-elimination/electrothermal work is credited at its
actual covariance/noise scope. Historical priority is UNKNOWN.

Recorded after-import costs:0.5826s stationary scalar acquisition,
1.6925s strong thermal comparator inputs,0.06487s initial budget
compiler, then0.06829s after adding the coarse-noise variance rule.
The final metadata-convention run cost0.08522s; numerical
inputs/protocols were unchanged. Both earlier receipts are preserved.
A's exact K3 scalar
packet cost0.0000876s; own K2 has93 new integer recurrence updates.
The two high-field quadratures acquired8194 additional nodes.
Source/model derivation, imports, failed downloads, primary reading,
tool overhead and physical acquisition are not comprehensively timed
or free. No trajectory, physical readout or calibration sample occurred.

The fixed-gap source is not a useful deep-sensing operation at its paid
cost. K2 yields a polynomial conditional construction and a weaker
electronics-calibration contract, but no actual instrument/time-unit
mapping or practical advantage is acquired. A strong ordinary driven
mean method can match or beat the actual passive budget under its
additional actuator access. The consequential remaining resource is
physical qualification of the bath/model/gain/reference/initialization
and native clock, rather than another supplied-moment calculation.
