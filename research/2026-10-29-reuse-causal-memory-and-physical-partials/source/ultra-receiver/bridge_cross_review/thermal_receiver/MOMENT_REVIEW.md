# Directed moment boundary: independent whole intake

**ACCEPTED at the two locked N32 moment-input scopes.** I whole-read
acquire_moments.py, MOMENTS.json, its actual interval backend and the
frozen A INTERFACE/long-exposure input. I independently reconstructed
the quadrature, remainder, tails and physical normalization. I did
not rerun the program, exponential nodes, model, trajectory or source
cases. The budget/calibration/comparator receiver is still a separate
live intake; this note does not accept its unfinished software.

## 1. Actual integral and source normalization

At theta=1 and Delta=1/2, let d=R_vv and g=R_pv. Standardizing
X=sqrt(d) u gives density proportional to

    exp[-u^2/2-beta u^4/4], beta=Delta*d^2=d^2/2.

The half-line moments are I_m=int_0^infinity u^m exp[-u^2/2-beta u^4/4]du.
Evenness cancels the factor two in I2/I0. Therefore

    v(Delta)=d I2/I0,
    s=g^2/d [1-I2/I0].                                 (1)

This is exactly the code's normalization. It is specialized to the
locked theta and Delta, not a generic-temperature implementation.
No Bessel-function oracle, limiting-temperature derivative, empirical
fit or simulated equilibrium sample is used.

For K3=3I-A_path, the source is A's exact N32 endpoint interface:
d=10610209857723/27777890035288, g=1/27777890035288.
For the assigned K2=2I-A_path control, d=32/33 and g=1/33.
Both match the frozen geometry p=1,v=32. The distinct shunt access
is kept explicit; the second law is not the same physical hardware
with a free change of stiffness.

## 2. Simpson bounds are directed enclosures

Write q(u)=u^2/2+beta u^4/4 and f_m(u)=u^m exp[-q(u)]. If
f_m^(k)=P_k exp(-q), then

    P_(k+1)=P_k'-(u+beta u^3)P_k.                      (2)

derivative_four implements this recurrence exactly in rational beta.
It then rounds the absolute polynomial coefficients outward. For a
panel [l,r] in [0,12], q is nondecreasing and

    sup |f_m^(4)|
       <=exp[-q(l)] sum_k |P_4,k| r^k.                 (3)

The code takes the upper interval endpoint of the exponential at l
and evaluates the absolute polynomial at r using upward Horner
arithmetic. Thus it does not substitute a sampled derivative for a
supremum. The possible cancellations in P_4 are safely discarded.

The 2048 Simpson panels each have width h=12/2048=3/512 and one
midpoint. Their scalar remainder is h^5 sup|f^(4)|/2880, as used.
The 4097 node values per case are interval evaluations, Simpson
weights are integrated with directed interval operations, and every
panel error is summed upward. The panel count is distinct from the
4096 half-step subintervals. The saved 8194 exponential-node count
for both cases is correct.

Although some Decimal grid operations use the global context, these
particular dyadic grid values and products terminate exactly and fit
well inside its 96 digits. This is not an all-arbitrary-cell-count
claim. beta and all derived coefficient fractions enter through
outward rational-to-interval conversion. No binary floating endpoint
is used in the scientific interval.

The backend explicitly uses separate downward/upward contexts for
algebra. Decimal exp is evaluated correctly rounded to nearest and
expanded by one adjacent number outward. At the actual positive
integrals/ranges there is no underflow or zero-crossing denominator.
Correct rounding of the Decimal backend is a computational premise;
this review is a whole-code/algebra intake, not a second interval
implementation or a formal arithmetic proof.

## 3. Infinite tails and ratio orientation

beta>=0 gives the global Gaussian envelope. At L=12,

    int_L^infinity exp(-u^2/2)du<=exp(-L^2/2)/L,
    int_L^infinity u^2 exp(-u^2/2)du
                         <=(L+1/L)exp(-L^2/2).         (4)

The second follows by integration by parts and the first. The code
adds zero to the lower finite-domain estimate and the directed bound
to its upper estimate, so it encloses the infinite integrals rather
than merely truncating them. The recorded bounds around 4.49e-33
and 6.51e-31 have the correct Gaussian scale.

I0's lower endpoint is positive. Directed interval division therefore
gives the correct I2/I0 enclosure, followed by (1). No uncharged
quadrature-library success flag appears. The strict upper moment
bound below one and positive contrast are actually checked.

The saved directed contrasts are accepted:

* K3: [4.9905915109104339847e-28,
        4.9905915130917906278e-28], with the exact long endpoints in JSON;
* K2: [.0003889778489184566663,
        .0003889778491015631040], likewise retaining JSON endpoints.

These displays summarize intervals; the full strings are authoritative.
They are known-model moment inputs, not physical observed contrasts.

## 4. Scope and remaining receiver intake

The saved moment acquisition costs .582605708 s after imports,
with 8194 directed exponential nodes, two assigned accesses and zero
trajectories or physical readouts. The two case times and old A
continuant/retention acquisition remain charged. Backend import and
its unused legacy spectral constants are nonzero initialization
costs outside this after-import number, not part of the two moment
laws. Scientific/source reading and review are not comprehensively
timed, and this receipt establishes no comparative speed advantage.

The source-version hash and exact interface bytes must be retained
when the final receiver is composed. A's accepted long-exposure
theorem is a separate dependency: its travel-survival contrast,
non-Gaussian Dirichlet variance and raw-read correlation bounds are
not numerical evidence from these scalar integrals. Their full
bath/metric/M-matrix/one-quartic/stationarity hypotheses remain intact.

The completed moment stage alone supplies no zero-start burn-in,
exposure/PSD calibration, actual decision, active mean budget,
finite-alternative likelihood optimum or high-peak/work comparison.
Those will be accepted only after the producer freezes and provides
the actual proof/code/receipt. Physical bath, geometry, classical
model validity, initialization, detector and calibration gates remain
unacquired here.
