# What extra source access changes in the finite-noise obstruction

Date: 2026-10-15. Status: an internally derived mathematical intervention and
synthetic checks, with explicit extra instrument assumptions. Physical access,
fabrication, novelty and end-to-end advantage are unestablished.

The point is to change a missing measurement operation, rather than improve an
inverse algorithm on the same uninformative scalar records. The result below is
for the supplied accretive needle family, including unknown permutations of its
stage labels. It is not a recovery theorem for arbitrary accretive plants.

## 1. Self-contained interface

Let m>=1, epsilon=m^-2, and let s in {0,1}^m label a plant. In some stage order,
write y0 for a source coordinate, x_i for the m internal coordinates, and z for
the detector coordinate. The original source fixes y0=1 and the stage equations
are

    (epsilon+u_i)x_i = epsilon*y_(i-1),
    y_i = x_i                    if s_i=0,
    y_i = y_(i-1)-x_i            if s_i=1,
    z = y_m.

These are implemented by the real lower-triangular (m+2)-state matrix B_s from
the supplied small-port construction. It has the common control matrix
P0=[0;I_m;0], source b0=epsilon*e_source, and detector c0=e_detector. The source
response is

    F_s(u)=product_i r_(s_i)(u_i),
    r_0(u)=epsilon/(epsilon+u), r_1(u)=u/(epsilon+u).

The source's energy identity proves

    sym(B_s+P0 diag(u) P0^T) >= epsilon/[4(m+1)^2] I

for u>=0. This is the same polynomially conditioned admissible family used by
the exponential finite-noise lower bound, not a newly assumed noiseless system.

**Extra physical operation.** With the original source turned off, independently
inject the calibrated source b_j=epsilon*e_internal-j through any selected
control-port direction p_j, retaining the same signed scalar detector c0. This
is a source change. Knowing that a shunt load can be tuned at a port does not
give this excitation operation.

The response to this probe is denoted h_j(u). The plant and load map must remain
the same while the source is switched. The order of internal coordinates may be
known for the first procedure or unknown for the second.

## 2. Exact probe formula and constant contrast

With local source j, y0=0, and all earlier stages are zero. At stage j,

    x_j=epsilon/(epsilon+u_j),
    y_j=(1-2s_j)*epsilon/(epsilon+u_j).

All later stages multiply the preceding y by r_(s_i)(u_i). Therefore

    h_j(u)=(1-2s_j)*epsilon/(epsilon+u_j)
                         * product_(i later than j) r_(s_i)(u_i).       (1)

Suppose every later bit is already known and its control is set to u_i=s_i,
while u_j=0. Then

    h_j(u)=(1-2s_j)*(1+epsilon)^(-k),

where k is the number of later one-bits. Its sign gives s_j and its magnitude
is at least 4/5. Indeed k<=m-1 and

    (1+1/m^2)^(-k)
      = (1-1/(m^2+1))^k
      >= 1-k/(m^2+1)
      >= 4/5.

The last inequality follows from (m-2)(m-3)>=0 for integer m>=1. Thus this
intervention has a constant signal gap; it is not a decoder for exponentially
small differences.

**Known order.** Start at the final stage and work backward. Probe j at u_j=0,
decode its sign, then set u_j to that bit. Exactly m signed scalar probes recover
all bits. The original source can then be restored and the decoded binary action
u=s achieves F_s(s)=(1+epsilon)^(-|s|)>=1/2.

## 3. Unknown stage ordering

The order need not be learned. Start every control at zero. In each round probe
every unresolved port under that same control vector. Previously classified
one-bits are at u=1 and classified zero-bits remain at u=0.

For an unresolved port j, equation (1) has exactly two possibilities:

* A later unresolved one-bit exists. Its u=0 factor kills h_j exactly.
* No later unresolved one-bit exists. Every later factor is either 1 or
  1/(1+epsilon), so |h_j|>=4/5 and sign(h_j)=1-2s_j.

At least the final unresolved stage is in the second case. After a round,
classify every observed nonzero signed response and activate every newly found
one-bit. At least one port is resolved per round. Hence there are at most m
rounds and at most

    Q_probe <= m+(m-1)+...+1 = m(m+1)/2

scalar probes. The bound is attained for an all-one chain under roundwise scans.
The procedure does not use the hidden bits or hidden order in choosing sources
or decoding the observations.

A threshold of 1/4 separates exact zero from the nonzero branch under total
absolute response error strictly below 1/4. The threshold is conservative given
the 4/5 gap. Each round must abstain if no port is classifiable; the code does so.

## 4. Precision, source strength and model perturbations

The same constant-margin scaling used in the source theorem preserves (1).
Take lambda=4m^2(m+1)^2, A_s=lambda*B_s, P=sqrt(lambda)*P0, and take source and
detector amplitudes both equal to 2(m+1). Their product is lambda*epsilon, so
both the original source response and every local-source response are unchanged.
The source/detector norms are O(m), the actuator norm O(m^2), the matrix norm and
condition bound O(m^4), and sym(A_s)>=I. This does not assert all port strengths
and the dissipation margin can simultaneously stay independent of m.

For a full-matrix perturbation ||Delta||<=1/2, the resolvent identity gives

    sup_u |h_(j,Delta)(u)-h_j(u)|
      <= 2*C_m*||Delta||, C_m=4(m+1)^2.                    (2)

The estimate applies equally to every source in this new source list because
their norms agree. Thus inverse-polynomial matrix perturbations preserve the
constant readout gap. Arbitrarily small generic perturbations from the supplied
density argument can be chosen inside this robust neighborhood. The finite
stress tests do not certify membership of that generic locus.

Each factor in (1) is at most one in magnitude and has derivative magnitude at
most 1/epsilon. If the applied controls deviate from the intended controls in
sup norm by delta_u, the telescoping product estimate gives

    |h_j(u_actual)-h_j(u_intended)| <= m*delta_u/epsilon
                                                = m^3*delta_u.          (3)

An off-state leakage and value error O(m^-3) therefore suffices for constant
response-error tolerance. The number of control-value bits is O(log m), although
the physical ability to maintain that leakage and repeatability is not supplied.

A source direction error d_j in the constant-margin normalization is bounded
conservatively by C_m*||d_j|| using ||A_s(u)^-1||<=1. Inverse-polynomial direction
calibration suffices. On the exact chain family a tighter bound follows because
every normalized coordinate source has detector response of magnitude <=1:
the error is at most ||d_j||_1. Neither calibration bound is a free measurement
operation. Unknown source gains, direct source-to-detector leakage, phase/sign,
and changes to the DUT while connecting the source require measured bounds.

For example reserve at most 1/16 each for matrix/model error, source calibration
error and mean readout error. Their total is 3/16<1/4. An additional control error
must be included in this same budget, rather than added without accounting.
The numerical stress uses (2)+(3)<=3/128 and no source-direction error.

For independent N(0,sigma^2) raw response noise, r independent repeats per probe
have mean noise variance sigma^2/r. A union bound over a fixed worst-case probe
budget Q gives |mean error|<=1/16 at every adaptive query with probability at
least 1-delta when

    r >= 512*sigma^2*log(2Q/delta).

This yields O(m^2 sigma^2 log(m/delta)) raw reads for unknown order, plus source
calibration, switching, settling and reset. A lower known-order budget follows
with Q=m. The constants are deliberately conservative; no hardware measurement
time, energy, spectral density or signal-voltage range is assigned.

## 5. The changed resource is the information, not clever fitting

For the original fixed source, the supplied family satisfies sum_s F_s(u)=1.
The zero-transcript argument therefore forces, for bounded error eta, at least

    Q >= eta*(p*2^m-4)

queries for uniform success p at response threshold 1/4. With adaptive Gaussian
precision and total inverse-variance V, the source gives

    V >= 4*2^m*(max(p-4/2^m,0))^2.

Unlimited fitting computation and interior controls do not remove these bounds.
The new oracle h_j is not in that contract, so the polynomial reconstruction
does not contradict the lower bound.

For a general matrix M(u)=A+P diag(u)P^T,

    d f/du_j = -(c^T M^-1 p_j)*(p_j^T M^-1 b).

Passive load dithering observes this product. Independent source injection
reveals the first factor, which is multiplied by an unknown, possibly vanishing
local state under the fixed source. It cannot be simulated at a guaranteed
nonzero strength by merely changing the diagonal load. This identifies the
physical interface whose absence mattered.

Give an equally informed system-identification competitor the same independently
addressable sources, same signed readout and same chain-family promise. It can
use exactly the same sign procedure; no algorithmic or hardware advantage over
that competitor is established. The result is an intervention separation for
this hard family, not a discovery of a superior general instrument.

## 6. A decisive failure and the remaining physical gate

With intensity-only detection, the ordered sign procedure fails already at
m=1: the two local probe amplitudes are +1 and -1 and both intensities are 1.
A calibrated coherent reference could recover a real signed cross term via
|r+h|^2-|r-h|^2=4rh, but this adds phase-stable source addition and reference
calibration. Existing network-analysis/phase-retrieval methods are the comparator.

The supplied raw-data gate acquires none of the local sources above. Real
metasurface controls can be loadable while remaining inaccessible for excitation.
A specimen-specific intervention test must show that each port is independently
drivable without changing A, that its source direction/gain and the detector
sign are calibrated, and that the full repeated acquisition is stable. It must
also acquire sufficient evidence for the chain-family promise or replace it with
a justified wider model. No such test occurred here.

## 7. Reproduction and check scope

Run `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 probe_experiment.py` in this
directory. The script contains independent closed-form matrix coefficients,
exact Fraction forward substitutions, direct matrix solves, two oracle-only
reconstruction routines, bounded-error tests and perturbation/leakage stress.
It reads immutable supplied JSON only to recompute the fitting comparison.

RESULTS.json distinguishes the finite checks from the analytic proof. All 510
labels for m=1,...,8 are checked in each reconstruction/noise mode, with 3,586
exact rational identities. Unknown-order stress includes m=64. These are
synthetic observations, never raw physical measurements. The code does not
prove arbitrary-plant acquisition, achievable hardware calibration, historical
novelty, or a complete-resource advantage.
