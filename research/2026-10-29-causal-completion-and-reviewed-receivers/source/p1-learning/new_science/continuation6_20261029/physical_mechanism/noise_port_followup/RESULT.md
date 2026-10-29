# Replay/noise-port follow-up: a real route and its precise limit

29 October 2026. The completed response-design unit is unchanged. This separate
follow-up studies an additional physical source port rather than another
gradient estimator. The governing proof is
`REPLAYABLE_NOISE_PORT_AND_RESIDUAL_COST.md`.

## Constructive supplier and three information costs

A stable unknown analog level theta drives a comparator. A reference U is
presented, and B=1{U<theta} toggles a visible bit. Reading the bit before and
after recovers B, with no reset or microscopic copy. When U is uniform, the
native operation is exactly a reversible binary flip of probability theta.
Comparator, reference DAC and clocked toggle logic are conventional components.
The special threshold architecture is explicit; it is not inferred from an
arbitrary native jump process with the same averaged flip probability.

The following interfaces have different parameter-resolution costs:

| Actual source interface | Calls for absolute precision delta, apart from confidence factors |
| --- | ---: |
| Only native flip outcomes are observed | Order delta^(-2) |
| The realized random reference is also recorded | Order delta^(-1) |
| A calibrated reference port can set new thresholds | Order log(1/delta) |

The first result is ordinary Bernoulli estimation. The second uses the bracket
between the nearest observed reference values on either side of theta; a
matching two-hypothesis error is exactly (1-Delta)^n/2. The third is ordinary
successive-approximation conversion. It supplies a constructive route around
a sample-count burden by changing the actual experiment, without learning or
copying the hidden state.

This reference is the innovation at the source's transition decision. It is
not the already recorded random selector that chooses an opaque operation.
Nor does replaying a finite reference catalog supply arbitrary new thresholds.
The source port, monotone architecture, precision and stability are all extra
physical information/resources.

## Full retained records change the horizon conclusion

For T native bit outcomes, parameter error delta gives a TV bound of order
sqrt(T)delta. If the T fresh reference values are also retained, the exact TV
is instead

    1-(1-delta)^T.

Thus reference disclosure can improve calibration while making the future
prediction task more demanding. The complete reference-retained task needs
precision of order epsilon/T. Its active binary-search comparison count is
still logarithmic, but the DAC/comparator must actually supply that precision.
The passive recorded-reference acquisition then costs order T/epsilon.

References reconstructible from an old retained seed cannot be averaged away.
Conditional on that seed, discrepancy is the indicator of a threshold
disagreement. A separate same-record union bound is given for early iid
references even when the chosen estimate depends on them. Old calibration
records retain their actual law throughout; no rare-record guarantee is claimed.

## Intrinsic noise and real selective checkpoints

If each adaptive comparison contains fresh independent Gaussian residual
noise of width sigma, data processing gives conditional KL at most
Delta^2/(2sigma^2). Adaptive threshold selection, external replay and unlimited
computation therefore still require at least

    (2sigma^2/Delta^2) log[1/(4beta)]

comparisons to distinguish both thresholds with error beta. Holding one noisy
sample instead does not help: unlimited comparisons of theta+eta acquire at
most one Gaussian observation of theta. The bound then counts independent
held-sample blocks.

A real selective checkpoint can reduce this residual. If the apparatus also
measures R=eta+xi, with independent Gaussian checkpoint noise of variance nu^2,
the effective remaining variance is exactly

    sigma_eff^2=sigma^2 nu^2/(sigma^2+nu^2).

This is an extra physical measurement, not information supplied by a software
noise seed. Ordinary switched-capacitor noise-cancellation circuits provide a
concrete related supplier. The primary Gu et al. 2024 design freezes and
cancels one capacitor's noise while retaining uncancelled presampling noise
on another capacitor. Its stated results are circuit simulations. This strong
comparator prevents claiming a universal raw kT/C floor for augmented sensing;
the residual after all actual checkpoints is the relevant quantity.

The proof also states the genuine reversible-logic checkpoint alternative:
if noise-conditioned operations have actual inverses, reverse-order execution
restores the logical state without copying it. Physical gate errors, all
forward/backward calls, stored history and baseline sampling remain paid.
Detailed balance alone does not supply this operation: even an equilibrium
heat-bath kernel can erase its starting state on every realized call.

## Disposition

There is a real positive route: instrumenting or controlling the physical
innovation, or acquiring a selective noise memory, can change the statistical
experiment and reduce learning cost. The strongest constructive implementations
are already ordinary ADC metrology, correlated-noise cancellation and reversible
computation. They are not supplied by the inherited opaque operation menu.

The decisive difficulty is obtaining an actual low-residual source port or
noise-conditioned inverse without assuming it. Known common random numbers,
action-selector keys, stationary laws or a held specimen do not suffice.
This unit does not establish a general defeat of a controller-horizon lower
bound, a new apparatus, or a novel learning mechanism. It identifies a concrete
boundary such a theorem must state and a conventional supplier that can cross
it in a different architecture.

The elementary proofs and exact source links/read scopes are in the governing
file. No new numerical fixture was needed for these analytic identities and
testing bounds. All previous files remain unchanged.
