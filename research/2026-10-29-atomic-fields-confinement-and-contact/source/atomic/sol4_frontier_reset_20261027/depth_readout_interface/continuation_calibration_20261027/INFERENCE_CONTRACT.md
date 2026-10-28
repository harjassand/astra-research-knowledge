# Paired differential calibration: exact contract and numerical qualification

The acquisition records the same local scan before and after a proposed change.
The before state is assumed native. That preparation/verification is not acquired
here. Both exposures are charged. The software aggregates the detector/probe
categories using a partition chosen only from the training templates.

Let B_k and A_k be independent Poisson counts. For a candidate layer h,

    E B_k = k_b b_k,
    E A_k = k_a [b_k + delta_hk(w)],
    delta_h(w) = delta_h0 + w delta_h1,  0 <= w <= 1,
    b_k >= 0,  b_k + delta_hk(w) >= 0.

The native pattern b is arbitrary and unknown. Thermal/source/focus labels are
not supplied. The known quantities k_b=a D_before and k_a=a D_after require a
calibrated incident dose and count normalization. The **changed-state contrast
family** delta_h(w) remains an assumed transfer contract. Native observations
alone do not identify it. Its two endpoint contrasts come from rigid and
four-configuration sigma=0.1 Å multislice templates, not experimental calibration.
The five candidate classes are native and layers 10,11,15,16; this is not a full
17-state or unrestricted atom/species classifier.

The before-state native label is a preparation assumption, not an inference
from the arbitrary background. Without that preparation, h=0 means no calibrated
change relative to the reference, not a verified pristine atomic structure.
Unknown pre-existing defects can be absorbed into b without being identified;
they may also change the response law delta. Neither absolute atom count nor
all-species purity follows from learning b.

For fixed w, dropping count factorials, the log likelihood is

    ell(b,w) = sum_k [B_k log(k_b b_k) - k_b b_k
                    +A_k log(k_a(b_k+delta_k(w))) - k_a(b_k+delta_k(w))].

It is jointly concave on a convex feasible domain because the means are affine
in (b,w), and log is concave. Write u=k_b+k_a, T=B+A and delta=delta_k(w).
The maximizing b for each bin is

    b_hat = max(0, -delta,
       [T-u delta + sqrt((u delta+B-A)^2+4 B A)]/(2u)).

The profiled ell_h(w)=sup_b ell(b,w) is concave: convex combinations of two
feasible (b,w) pairs remain feasible, and joint concavity bounds the value at
their convex combination below by the corresponding value combination. This
proves a global scalar maximization problem, including boundary cases.

At an interior bin, the derivative with respect to delta is

    A/(b_hat+delta) - k_a.

At the boundary delta<0, b_hat=-delta and A=0, it is B/delta+k_b.
At delta=0 and A=B=0, any subgradient in [-k_a,k_b] is valid. Multiplication by
delta_h1 and summation gives a supporting slope for the profile. A supporting
line is a global upper bound. Taking the minimum of supporting lines on both
sides of the numerical maximizer, then maximizing this piecewise-linear upper
envelope on [0,1], upper-bounds the null likelihood supremum. This is how the
code avoids using a merely local numerical maximum as its denominator.

The derivative/upper-envelope computations are floating point. Thirty random
profiles were independently checked against a 1,001-point grid and a separate
bounded optimizer. The minimum upper slack was about 9.8e-8 log units; the
largest best-score difference was about 1.9e-9. These are numerical checks,
not outward-rounded interval certificates. **The implementation's coverage is
conditional on the supporting bounds remaining conservative.** The mathematical
coverage statement below concerns exact maxima or genuine upper bounds.

Counts are randomly thinned into two independent Poisson halves offline. This
does not add photons or acquisition dose. Fit each half independently. On the
opposite half, form a proper predictive density Q from an equal mixture of
(i) the fitted candidate contrast law and (ii) unconstrained before/after means.
Positive 0.5 pseudocounts avoid zero predictive means. These are predictive
densities, not extra specimen observations.

For each candidate h on the test half, use

    E_h = Q_test / sup_(b,w in class h) L_test(b,w).

For any true parameter in class h, the denominator is at least its likelihood.
Conditional on the training data, E[E_h] <= 1, because Q_test is a normalized
predictive distribution independent of the test half. Averaging the two swapped
split likelihood ratios retains that expectation bound even though the two
ratios are dependent. Markov's inequality gives P(E_h >= 1/alpha) <= alpha.

Keep C={h:E_h<1/alpha}. Report h only when C is a singleton; report ambiguity
when |C|>1, and model rejection when C is empty. If a covered h is true, a wrong
singleton or empty rejection requires excluding h, with probability at most
alpha. This is an unconditional wrong-report bound, **not** an error bound
conditional on acceptance, nor a success/yield guarantee. There is no factor of
five for the class list: only the true class needs coverage. Yield is measured
separately in the finite tests.

This uses ordinary [split/profile likelihood universal inference](https://pmc.ncbi.nlm.nih.gov/articles/PMC7382245/).
It is not a new statistical principle. An equally informed ordinary microscopy
controller receives the same counts, partition, likelihood, calibration and
rejection option. The full-data profile MLE is also evaluated on identical counts
as a strong ordinary point-decision comparator.

Coverage requires the grouped change to equal one delta_h(w), a static shared
background, known dose/count scale, and the assumed Poisson observation law.
Held-out sigma=0.065 Å with independent phonon seeds is not declared to be in
that family; its computed success is a finite forward-model sensitivity result.
Drift, multiple defects, species loss, strain/relaxation, contamination or state
changes during calibration may violate the contract. One successful rejection
control does not establish coverage or rejection of every such state.

The reference is not automatically needed anew before every write pulse: stable
reference reuse might amortize cost. This fixed-pair analysis does not validate
arbitrary data reuse, repeated confidence decisions or optional stopping. Those
require their own dependence-aware or sequential construction. Likewise, a
transition-aware read may track specimen changes rather than lose the run; it
requires an acquired observation/transition kernel beyond this static contract.
