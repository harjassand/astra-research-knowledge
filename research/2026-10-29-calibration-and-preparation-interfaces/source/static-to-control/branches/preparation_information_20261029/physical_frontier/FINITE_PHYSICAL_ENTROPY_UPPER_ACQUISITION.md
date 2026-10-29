# Finite physical-entropy upper acquisition from native snapshots

29 October 2026. Ordinary robust-mean contract supplying a physical UPPER
entropy premise. No sample, calibration, preparation or assay was executed.

## 1. Physical and sampling assumptions

Use the stationary native torus class: unit masses, all d momenta in one
known calibrated bath gamma,tau>0, smooth position-only force ||F||<=A,
and the accepted stationary entropy/integration-by-parts domain. Then

    sigma=(gamma/tau)(E|p|^2-d tau).                    (1)

This is not an identity for arbitrary observed reversal divergence,
partial thermostat observation or velocity-dependent active forcing.

Acquire N genuinely iid FULL baseline configurations (q_i,p_i). Within
a trial, q_i and p_i may be dependent. Independence across trials needs
an actual justified preparation/sampling contract; a visible fit or a
chosen waiting time does not establish it.

The proved bounded-force stationary moment estimate gives

    E|p|^4<=C4,
    C4=(A/gamma+sqrt(tau)[d(d+2)]^(1/4))^4.              (2)

No force derivatives or hidden mixing constants enter this bound.

## 2. A real finite-range observation contract

Choose R>0, Y=|p|^2 and Y_R=min(Y,R). A direct saturated energy channel
is admissible if its calibrated error for Y_R includes saturation and
overflow. Alternatively use the component-clipped momentum vector

    c_R(p)_j=clip(p_j,-sqrt(R),sqrt(R)).

Exactly min(|c_R(p)|^2,R)=min(|p|^2,R): if a component overflows, both
capped energies equal R; otherwise the vectors are unchanged.

Require reported vectors hat_c_i to satisfy
|hat_c_i-c_R(p_i)|<=delta_p uniformly on a stated calibration event.
The function g_R(x)=min(|x|^2,R) is globally 2sqrt(R)-Lipschitz, hence

    |g_R(hat_c_i)-Y_R,i|<=2sqrt(R)delta_p.               (3)

This is a finite-range contract, not a uniform approximation of unbounded
true p. Per-component errors delta_component give delta_p<=sqrt(d)
delta_component. A quantizer of grid step Delta on the stated range
contributes at most sqrt(d)Delta/2, in addition to analog uncertainty.
Actual range, bit depth, thresholds and overflow behavior must be
calibrated; unflagged clipping at an unrelated range is insufficient.

Assign certified overflow its capped energy rather than discarding the
trial or its correlated position measurement. Let e_meas bound each
capped-energy report error, e.g. 2sqrt(R)delta_p plus evaluation error.
Let e_arith bound remaining block-average/median arithmetic error.
These bounds hold jointly on a metrology event of probability at least
1-delta_met. Correlated measurement errors are allowed under this uniform
event and are not mislabeled as iid readout noise.

## 3. Median-of-means certificate with constants

Use k odd independent blocks, each of m trials, N=km, with predetermined
partition. Write mu_R=E Y_R. Since Var(Y_R)<=E Y_R^2<=C4,

    P(|block_mean-mu_R|>2sqrt(C4/m))<=1/4.

Independence of blocks and Hoeffding's Bernoulli bound show

    P(|MOM_true-mu_R|>2sqrt(C4/m))<=exp(-k/8).           (4)

For confidence delta_stat, choose odd k>=8log(1/delta_stat). Uniform
sample perturbations of size e_meas perturb each block mean and its
median by at most e_meas; add the stated arithmetic tolerance.

For every y>=0, (y-R)_+<=y^2/(4R), so
E(Y-Y_R)<=C4/(4R). For M the median of reported block means, define

    mu_upper=M+2sqrt(C4/m)+C4/(4R)+e_meas+e_arith,
    s_upper=max{0,(gamma/tau)(mu_upper-d tau)}.           (5)

With probability at least 1-exp(-k/8)-delta_met,

    E|p|^2<=mu_upper,    sigma<=s_upper.                 (6)

The tail bound C4/R is also safe, but the factor 1/4 follows from
(y-2R)^2>=0 on y>=R. Numeric constants must be evaluated outward or
covered by e_arith. If gamma,tau,A have calibrated intervals, use C4
valid throughout them and maximize the entropy upper expression over
the warranted parameter set. Momentum tolerance alone does not account
for uncertain bath calibration.

The upper bound can be loose. Executing the estimator does not by itself
establish a small entropy rate, and a lower entropy certificate cannot
replace (6).

## 4. Acquisition, range and precision costs

The physical sampling cost is N=km actual iid baseline preparations.
There are dN saturated momentum-component readings, plus the complete
position readouts required by static fitting and the actual overflow or
timing channels. One vector notation does not convert d readings into a
single calibrated acquisition unless that vector sensor is supplied.

An energy statistical radius a requires m>=4C4/a^2. A saturation-tail
allowance b requires R>=C4/(4b). A momentum contribution <=c requires
delta_p<=c/(2sqrt(R)), before extra arithmetic/analog uncertainty. These
separate count, range and precision requirements. Increasing range reduces
tail bias but tightens momentum precision for fixed energy accuracy.
Certifying entropy near zero resolves a small excess above d tau and
therefore also requires corresponding bath-calibration precision.

This is ordinary robust mean estimation, with no speed advantage claim.
For repeated data-dependent stopping, allocate confidence across the
attempted certificates or supply a confidence sequence; the fixed-N
statement is not automatically an anytime guarantee.

## 5. Shared data and future service

The SAME N configurations can supply position fitting and the energy
certificate. Dependence of q,p within a trial is harmless. A union bound
combines their confidence events; the two certificates need not be
independent. The selected Gibbs potential may depend on all these data.

A future controlled service then needs a genuinely fresh independent
baseline initialization, or a justified JOINT physical-state/calibration-
history TV bound. Retaining a record while reusing its correlated source
state does not supply the population initial-state premise.

With a shared calibration record, a uniform conditional service error
epsilon on a calibration event of probability >=1-delta_cal yields joint
calibration/service error <=delta_cal+epsilon. This does not create a
reset, independent samples, a sensor, or a numerical dynamics solver.
Those actual preparation, metrology and execution resources remain
attached to any operational claim.
