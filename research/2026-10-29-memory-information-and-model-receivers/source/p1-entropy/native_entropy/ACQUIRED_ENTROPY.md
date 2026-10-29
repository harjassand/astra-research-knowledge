# What the native entropy assay acquired

29 October 2026, Brisbane.

## Declared consequence and source access

The target is a lower bound on stationary Markov entropy production of
EVERY compatible finite CTMC with all states even under the specified
reversal. Neither the hidden generator nor its state count is identified.

The native interface supplies five individually resettable microscopic
ports, equal calibrated stationary departure flux weights, native port
holding rate32/15, independent repetitions, return endpoints, an explicit
direct-jump marker, and duration intervals of width2^-20. These are
supplied source/instrument conditions. They are not learned by the assay.

The per-departure entropy certificate uses a bounded endpoint score and
requires no tail envelope or hidden rate ceiling. Conversion to a rate
per native time additionally uses the supplied conditional bound
P(tau>t)<=exp(-t/2) on interior duration. It bounds the unresolved tail
after truncation at24. Native initial holds are included; their mean15/32
comes from calibrated port rates.

## Actual individual acquisition

produce_native_entropy.py executed262144 independent preparations and
262144 uninterrupted native excursions, retaining every start/end port
and both duration intervals in run/native_record.npz.

The source incurred524288 native jumps,122692.80308161303 port-clock
units and261812.7898676988 interior-clock units:384505.59294931183 total.
There were122733 self-returns, each with positive interior duration.
These are individual trials; no aggregate Binomial query replaces them.
Software runtime was approximately0.67 seconds and is not physical time.

The implementation uses ordinary NumPy PCG64 uniform/exponential sampling.
It is a synthetic numerical assay, with no complete floating-law proof
or physical calibration. All quoted statistical confidence is the
mathematical ideal-law guarantee under the stated instrument contracts.

## Original bounded-window certificate

A predeclared Horn score H_ij in {-1,1}, multiplied by the indicator
0<tau<=1, had conservative observed sum -10380. Rational Hoeffding and
tail arithmetic certified, with joint failure <=1/1000,

    E/R>=0.12792568978874366 nats per native departure,
    sigma>=0.08206251553031438 nats per native time.

The negative observed score certifies a violation of a necessary
equilibrium nonnegative-Gram constraint, not a fitted hidden model.

## Stronger reuse of the same record

The full positive-duration endpoint score is also bounded and carries a
larger signal on this source. Retaining it is the stronger ordinary choice.
certify_native_entropy_reuse.py evaluates both fixed scores and the mean
bound with a simultaneous three-event confidence budget1/3000 each.
No witness matrix is fitted to these data, and no new source calls occur.

The full score sum is -16678. The simultaneous certificate is

    E/R>=0.22322364980255016,
    sigma>=0.14297416604265997,

with total failure <=1/1000 and mean complete cycle duration <=
1.5612866014965647. The time-window alternative is preserved and remains
valid, but is weaker here. The stronger reuse takes approximately0.051
software seconds; this is not a comparison against an optimized library.

The consumer reads only PUBLIC_CONTRACT.json and native_record.npz.
Its helper implements exact rational empirical sums, outward atanh-series
logarithm bounds, integer-square-root bounds and an inverse positive
Taylor bound for the exponential tail. It never reads PRIVATE_SOURCE.json.

## Truth and equally informed conventional comparison

The separately supplied15-state source has exact entropy rate
(16/47)log(5/3), approximately0.1738980846862947. Its observed port/interior
path law is exactly time-reversal symmetric, and its kernel
K(t)=exp(-t)[I+(17/30)Adj(C5)] is symmetric positive definite. Those
identities are generator proofs, not conclusions from finite observations.

A full endpoint-flux hidden-star optimization of the kind already
developed by Skinner and Dunkel is stronger at exact population input:
it attains the source value, while the linear copositive certificate
gives8/47=0.1702127659574468 from the complete endpoint population law.
The scalar coefficient4 in the universal certificate is nevertheless
optimal as a uniform guarantee, as the independent near-equilibrium
family demonstrates.

The new asset is the closed-form, dimension-independent witness with
a finite-data native acquisition and duration-bin/lag extensions. It
does not supersede a stronger conventional optimizer supplied the same
information. Finite observed zero counts do not prove exact graph support;
the acquired certificate does not assume such zeros.

## Reversal is substantive information

check_parity_scope.py verifies that the same abstract15-state generator
obeys generalized detailed balance when paired hidden stars are swapped
under an odd-state involution, while every native port is fixed.
Its generalized entropy under that convention is zero. Consequently
even complete native observations cannot supply the microscopic parity
convention. The positive thermodynamic interpretation is conditional
on the physically justified all-even Markov model, not on data alone.
No odd-state physical implementation has been built.

## Files and preservation

The producer, raw record, private truth, public contract, original
certificate, stronger reuse certificate, hashes, full clock costs and
arithmetic are retained together. Replaying the consumers uses no new
source observations. Replaying the producer redraws data and would be
a new assay; it is unnecessary for auditing the frozen result.

