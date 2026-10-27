# Conditional finite-record covariance confidence interface

Parent construction for the independently developed finite-record affinity
route. The sector-to-affinity bridge is a separate theorem; this note does not
assert a physical affinity from the existing camera data. Statistical and
instrument assumptions below are actual inputs, not inferred from sample size.

## Input and centering operation

Acquire 2m independent, identically distributed complex three-channel records
Y,Y', paired without selection. The same linear instrument and common prefilter
window apply in every repeat. Separately acquired envelopes satisfy |Y_i|<=B_i
with B_i>0. A maximum observed amplitude is not such an envelope. Saturation or
clipping cannot be inserted to obtain bounded data while silently retaining a
linear filter model.
Statistical clipping of estimator contributions is a different allowed
operation when an acquired tail bound transports its bias back to the true
unclipped covariance; no such correction is implicit in this bounded-data
section. The peer's later empirical-Bernstein construction uses that alternative.

Set Z_i=(Y_i-Y'_i)/(2B_i). Then |Z_i|<=1 and

    C=E ZZ* = (1/2) diag(1/B_i) Cov(Y) diag(1/B_i).

Thus no population mean needs to be known. Real diagonal congruence and scalar
rescaling do not change normalized closure or the phase-minimized matrix
functional. Pairing costs two records per replicate; independence, stationarity,
gating/filter memory, noise ordering and drift control remain supplied inputs.

## Simultaneous confidence, including a rational 99% specialization

Let Chat=m^-1 sum Z Z*. There are nine real Hermitian components. Hoeffding's
inequality and a union bound give, with failure probability at most delta,

    |C_ii-Chat_ii| <= sqrt(log(18/delta)/(2m)),
    |C_ij-Chat_ij| <= 2 sqrt(log(18/delta)/m), i<j.

The offdiagonal inequality is a complex disk obtained from separate real and
imaginary errors. Each diagonal variable has range[0,1]; each offdiagonal real
or imaginary variable has range[-1,1]. No Gaussian observations or moment
closure are assumed.

At delta=.01, log1800<8 (the exponential's positive Taylor sum through degree9
at8 already exceeds1800). Therefore the rational radii

    e_diag = ceil_sqrt(4m)/m,
    e_off  = ceil_sqrt(32m)/m

are conservative, where ceil_sqrt is exact integer ceiling square root. This
claim concerns the assumed IID law, not a proof that a finite PRNG run supplies
IID physical records.

## A scalar certificate without numerical phase optimization

Let the three cyclic offdiagonal entries be a=Chat12,b=Chat23,c=Chat31, and
let their valid complex-disk radii be e_a,e_b,e_c. Put u_a=|Re a|+|Im a|,
and similarly for b,c. These rational upper bounds avoid uncertified square
roots. Define

    Eprod = (u_a+e_a)(u_b+e_b)(u_c+e_c)-u_a u_b u_c,
    Lprod = max(0, |Im(a b c)|-Eprod),
    Udiag = product_i (Chat_ii+e_ii).

Expanding the product shows that Eprod bounds every nonempty error term in
the true cyclic product. Use the certificate only with positive variance
lower guards Chat_ii-e_ii>0. Then

    eta_lower=Lprod/Udiag <= |Im(C12 C23 C31)|/(C11 C22 C33).

All arithmetic can be exact for rational records and rational supplied disks.
The guard or Lprod may return zero: that is no certified signal, not proof of
equilibrium.

Conditional on the independently established three-channel phase-functional
bound F>=4 eta^2/27 and the separate affinity bridge Fmax>=pi sqrt(F), this gives

    Fmax >= (2 pi/sqrt27) eta_lower

at the same confidence. This is maximum simple-cycle affinity of the stated
finite-state even-observable Markov model, not an entropy-production RATE or a
physical claim outside that model. The ordinary affinity-inference method
receives exactly the same records, envelopes, timing and calibration inputs.

No old optical-binding tracking fixture acquires the required envelopes,
independent stationary repetitions, prefilter gate, tail or noise contract.
These remain open physical interfaces; this note supplies the conditional
centering/confidence operation rather than assuming those interfaces away.

## Unbounded Cox-count alternative

The peer's later positive photon-counting contract has unbounded Poisson data,
so bounded-record Hoeffding cannot be applied to it without a different acquired
input. Here is a replacement using explicit moment bounds, without clipping.
Assume the conditional total photon mean per gated record in channel i is at
most an acquired Lambda_i, including the supplied capture/tail/noise contract.
Conditional on the intensity paths, channel counts are independent Poisson.
Here Y_i(omega) is the sum of unit-modulus Fourier phasors of detected photon
events. An analog response with arbitrary pulse weights needs its own acquired
gain/moment bound; it does not inherit the unit-weight inequality by notation.
For two independent records, their summed count has conditional mean at most
M_i=2Lambda_i. With D_i=Y_i-Y'_i, |D_i| is at most that summed count. Thus for
W_ij=D_i conjugate(D_j),

    E|W_ij|^2 <= (M_i^2+M_i)(M_j^2+M_j), i!=j,
    E W_ii^2 <= M_i^4+6M_i^3+7M_i^2+M_i.

These follow from the second/fourth Poisson moments and their positive
coefficients, then conditional channel independence. Correlated Cox intensities
are allowed; conditional dependence of the counting noise changes the bound.
Independent read noise needs its own charged moment budget.

Call the relevant bound V. Divide kb independent record pairs into k odd
blocks of b pairs. For each real covariance component, take its block average
and then its median. At radius2sqrt(V/b), Chebyshev gives each block failure
at most1/4. Independent blocks and Hoeffding on their bad indicators give
median failure at most exp(-k/8). A complex entry uses separate real/imaginary
medians and disk radius2sqrt(2V/b); the assembled estimate need not itself be
PSD. The true population matrix is PSD, and simultaneous component disks are
enough for the deterministic closure certificate above.

For all nine covariance real components, k=55 gives total failure<.01: the
positive Taylor sum for exp(55/8) through degree11 exceeds900 (independently
checked by exact Fraction arithmetic), so9exp(-55/8)<.01. This consumes110b
physical records. Mean, DC, dark and other calibration estimates need additional
failure allocation; k55 does not certify them too. In general J components
cost at most J exp(-k/8). Their simultaneous confidence sets may be correlated;
the union bound needs no independence between estimators.

This operation handles the unbounded count law under acquired intensity/moment
bounds and independent repetitions. It does not acquire Lambda_i, reset hidden
slow modes, make camera traces IID, or validate source stationarity. Its value
is to specify that missing statistical operation precisely rather than replace
Poisson counting with a bounded synthetic fixture.

## Strong ordinary mean-referenced two-channel operation

The peer identified that the same passive common gate supplies phase
calibration: after a separately acquired dark-mean subtraction,
m_i=E Y_i=mu_i H_i W with mu_i>0 and nonzero gate transform W. Multiplying by
diag(exp(-i arg m_i)) removes H's individual phases, leaving only a common
phase and positive real gains. This capability belongs equally to an ordinary
two-channel affinity method. Step/mean response calibration is existing
system-identification machinery; it is not invented here.

One can propagate uncertainty without estimating any angle. Given simultaneous
disks for C12,m1,m2, form P=C12 conjugate(m1)m2. Its imaginary part equals
|m1 m2| times the calibrated cross-covariance's imaginary part. Apply the same
three-factor L1/disk product bound above to obtain L_P<=|Im P| and rational
upper magnitude bounds M1,M2 for the means. With positive diagonal variance
upper bounds A1,A2,

    r_lower = L_P/(M1 M2 sqrt(A1 A2))

is a conservative lower bound on the calibrated canonical imaginary radius:
the exact denominator uses sqrt(C11 C22-(Re C12_cal)^2), which is no larger
than sqrt(C11 C22). Nonzero mean/variance guards are required. Values r_lower>=1
are an inconsistent-data/premise guard, not an infinite-affinity discovery.
The sector/cycle bridge then gives

    Fmax >=2 pi r_lower/sqrt(1-r_lower^2).

All mean/dark/covariance estimates need a JOINT failure budget. Their estimates
may share records: simultaneous disks, not an independence claim between
estimators, justify the deterministic product inequality. Source positivity,
nonzero mean, dark stability and the gate/tail contracts are acquired inputs.
This construction gives no photon-data result until those inputs are supplied.

Exact cancellation is not free phase acquisition. At fixed nonzero frequency,
a rectangular gate of lengthT has |W|<=2/|omega| while its stationary fluctuation
variance often grows withT. Its mean anchor can therefore become poorly
conditioned or vanish at a sinc zero as the observation window grows. A common
nonnegative modulated gate can supply a growing mean Fourier component, but
changes the source-spectrum average and needs an actual implemented modulator;
separate calibration gates/records also cost resources. A finite-confidence
mean disk must resolve this conditioning rather than replace it with an exact
population phasor.

A concrete ordinary alternative is w(t)=[1+epsilon cos(omega t)]/2 for an
integerM full periods,0<epsilon<=1. It is a nonnegative passive transmittance
bounded by1, and its target-frequency transform is EXACTLY epsilon T/4.
The uniform cone remains valid for the changed finite covariance. For a fixed
finite mixing source, choosing epsilon=M^(-gamma),0<gamma<1/2, permits a growing
phase anchor while asymptotic relative spectral sidebands vanish; that
asymptotic supplies no uniform hidden-mixing cost. Even without invoking it,
the exact nonzero transform gives a finite gate design for the joint moment
confidence operation. Known waveform, amplitude/phase accuracy, modulator,
full capture and records/time must be charged to both methods. This is existing
modulated/lock-in calibration machinery, not a new general calibration theorem.
