# A finite-output contract for the conditional path construction

This auxiliary lemma addresses a genuine limitation: a finite stored
trajectory is atomic, so its law cannot be close in total variation to a
nonatomic real-valued path law.  It does not assert that the floating
prototype implements a complete bit-cost theorem.

## Randomized relative-resolution timestamps

For h>0 and a real y, let

    Q_h(y) = floor(y/h + U),     U uniform on [0,1].

Thus Q_h(y) is an integer giving randomized rounding of y/h to the two
adjacent integers.  Use independent rounding uniforms across nodes.  The
finite observation of a positive failure time tau is Q_h(log tau).
Decoding it as exp(h Q_h(log tau)) has multiplicative resolution exp(h).

For any y,z, coupling by the same U gives

    TV(Q_h(y),Q_h(z)) <= min(1,abs(y-z)/h).                 (F1)

For abs(y-z)<h, the two floors differ only on an interval of uniform
measure at most abs(y-z)/h.  For greater differences the trivial bound
one suffices.  Independent coordinate couplings and a union bound give
total variation at most sum_i abs(y_i-z_i)/h for the vector output.

This deliberately specifies a randomized rounding contract.  It is not a
claim that arbitrary deterministic threshold tests are insensitive to
finite precision.

## Relative threshold errors do not amplify through a cascade

Under the attractive exposure model, the failure-time vector is
coordinatewise nondecreasing in the threshold vector.  It is also
homogeneous: tau(cE)=c tau(E).  Therefore if

    exp(-u) E_i <= Etilde_i <= exp(u) E_i for every i,

then, for every finite positive failure time,

    exp(-u) tau_i(E) <= tau_i(Etilde) <= exp(u) tau_i(E).    (F2)

In particular, failure order can change, but log timestamps change by at
most u.  One need not assume separated event times or a derivative bound
for the path map.  A known initially failed node is recorded separately;
an inaccessible infinite-time node is likewise separate.  The simplest
full-vector contract assumes positive baseline rates so every noninitial
node eventually fails at a finite positive time.

Combining (F1) and (F2), approximating the sampled thresholds to relative
log error u and then replaying the exact learned rates changes the
randomized log-timestamp law by at most nu/h.  If the approximation fails
with probability at most delta, add delta.  If evaluation of each log
timestamp has an additional absolute error v, add nv/h.  The ideal-law
learning and held-process errors transfer through the same randomized
rounding kernel by data processing.

Consequently the complete error ledger for this specified finite output
can take the form

    [learned path-law error]
    + [conditional held-event error]
    + [conditional bin-sampling error]
    + delta + n(u+v)/h
    + [finite categorical-rounding error].                 (F3)

This avoids a distribution-specific anti-concentration argument at every
timestamp grid boundary.  It does not remove the need to implement the
threshold draws and arithmetic with their stated errors.

## Exact rational replay avoids unstable floating event comparisons

After acquisition, choose rational retained rates and rational positive
threshold approximations Etilde.  The next-event replay uses only rational
addition, multiplication, division, and comparison, with at most n jumps.
For any fixed failure order, the equations for event times are triangular
linear equations whose coefficients are differences of retained rates
and whose right hand sides are thresholds.  Clearing the denominators
of the at most n^2 coefficients and applying the ordinary determinant
bound gives polynomial rational bit growth in n and the input bit
length.  Exact rational comparison resolves nearly coincident events;
arbitrary deterministic tie handling defines a path if an approximated
threshold vector happens to land exactly on a tie.  Bound (F2) still
controls its times under monotonicity/homogeneity.  No inverse spectral
gap or separation between event times is assumed.

Computing logarithms of positive rational timestamps to absolute error v
and sampling the two-point rounding probabilities to a specified total
variation tolerance are conventional finite-precision operations.  Their
input size, requested precision, and resulting integer-output size are
charged.  This paragraph is a cost route, not a completed implementation.

## An explicit lower bound for positive partition arithmetic

Assume an activating order i_1,...,i_m has been found, with positive local
rate b_k=a_{i_k}({i_1,...,i_{k-1}}), and that reaching these components
implies the desired upward event.  Attractiveness implies that the
threshold event

    E_{i_k} <= b_k T/m,   every k,

forces completion of this sequence by T, even when other components also
fail.  Hence

    p(T) >= product_{k=1}^m F_{i_k}(b_k T/m).               (F4)

For the held process, using b_k Delta instead gives the analogous lower
bound when N>=m.  The order is acquired from local table values by a
simple reachability closure; it is not a rare trajectory supplied as an
oracle.  In the positive-baseline case, any component ordering works.

Condition (A1) from AGING_GENERALIZATION.md implies

    F_i(c x) >= c^kappa_i F_i(x),    0<c<=1.

A known reference point x_i with F_i(x_i)>=q_i>0 therefore gives an
explicit lower bound

    F_i(z) >= q_i * min(1,z/x_i)^kappa_i.                  (F5)

For rational rates, deadlines, and bounded explicit clock parameters,
the logarithm of this probability lower bound has polynomial description
length.  Precision may depend on log(1/p), while the count of arithmetic
operations need not depend on 1/p.

For example, approximating every local factor on q-bin variables to
absolute error eta changes the unnormalized joint mass by at most
n q^n eta: each factor is between zero and one, and the product error
telescopes.  Selecting eta relative to the explicit lower bound (F4)
costs only an additional n log q plus log(1/p_lower) precision bits.
Nonnegative rational approximate factors can be passed to exact rational
variable elimination and categorical sampling.  This is conservative;
more careful positive arithmetic can reduce the precision budget.

The bit complexity of evaluating each known clock interval mass still
must be supplied.  A density scaling inequality alone is not a clock
evaluation algorithm.  The Weibull and Gamma examples have conventional
special-function machinery, but the present floating files do not certify
its uniform bit complexity or rounding error.
