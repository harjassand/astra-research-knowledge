# Decision-specific quantum assay: one extra quadrature breaks an exact response fibre

## Result

For the exact two-model observation fibre in N768, repeated use of its
original local Ramsey `X` contrast cannot decide whether the source-certified
`D(V0)` is above or below `0.603`: the full `X` transcript laws are identical,
so any classifier has worst-case error at least `1/2`, for every shot count.
One additional local readout setting, logical `Y` at the same preparation and
interrogation time, is both sufficient and minimal in this two-point task.
The exact `Y`-mean gap is
`e^-1 * 32 * 132098 tan(1/200) / (257(1024-65025 tan^2(1/200)))`
(`0.0295925435008` numerically). With total per-model expectation bias at most
`10^-4`, 50,000 independent `Y` shots classify the two response regimes with
error below `0.01` by an exact Hoeffding certificate. The interrogation part
costs 25,000 native time units; preparation, reset, switching, readout and
axis calibration costs remain unmeasured. The high-response model has the
lower `Y` mean, so the classifier selects it below the midpoint threshold.
For the broader two-parameter qubit family, the two-quadrature map has
orthogonal Jacobian columns of length `tau exp(-d tau)`; throughout the box,
its smallest singular value exceeds `0.1749` and its local inverse sensitivity
is below `5.72`. The single `X` setting has rank one and cannot invert both
parameters.

This is an acquired-data decision certificate, not a state or Hamiltonian
reconstruction. It is conditional on the exact two-model promise and on the
N768 response intervals. The original N768 one-contrast policy remains the
better-supported route when the only goal is choosing a near-optimal `V`: it
already reports global regret below `8.7804e-5` at 262,144 independent `X`
shots, under its source assumptions. The added `Y` axis is needed for this
absolute-response threshold decision, not for that near-optimal-action goal.

## Scientific object and evidence boundary

The threshold task uses `V0=1109/512` and the two N768 parameter points
`(U,d)=(3.99,1.918655813574...)` and
`(4.01,2.078116561483...)`. The source reports their `D(V0)` enclosures as
`[0.6134535792,0.6137844323]` and
`[0.5928974757,0.5931093049]`; thus the rational threshold `0.603` separates
the enclosures. N768 defines `D` as the long-time infinite-chain
density-response second-moment coefficient for its specified interacting,
physically dephased chain. Its exact model, all-sector infinite-temperature
reference, local six-spin probe, uncertainty box and acquisition assumptions
are read from the current dossier and original research note.

The new derivation is only the local qubit information calculation and the
finite-shot `Y`-threshold test. I independently derived the same-`X`-law
identity and `Y` gap from the supplied equations and checked the formulas
with rational arithmetic and floating diagnostics. The macroscopic response
certificates remain source-derived and unreviewed; no device was prepared or
measured here. A practical decision needs a real engineering threshold with
the same meaning as `0.603`, verified model membership, and calibrated
physical access.

## Resource and comparator summary

The added setting uses the existing six-spin preparation with hopping frozen
on the block, the central Bell-like one-excitation state, four fixed neighbour
occupations, and `tau=1/2`. A `pi/2` analyzer rotation measures logical `Y`.
For the two-point test, no `X` samples are required because the hypotheses
are already fixed; for deployment as a supplement to a broad-box `X` policy,
the `Y` samples add to its existing acquisition burden. A separate `Y`-axis
mean-bias bound of `10^-4` must be acquired; the existing N768 bound applies
to the original `X` assay and does not imply it.

The exact `Y` measurement is also the single-copy Helstrom measurement for
equal-prior discrimination of these two reduced qubit states because their
density-operator difference is `(Delta_Y/2)Y`. This is a strongest
one-copy POVM comparator, not a proof of optimal collective multi-copy
sample complexity. The selected primary literature records established
quantum semiparametric estimation and active Hamiltonian-learning methods;
neither is a matched-cost baseline for this promised two-hypothesis response
screen. No sample-complexity superiority or novelty claim is made.

The paired source/destination contract is: N768 supplies the exact local
state family, a one-axis `X` outcome law, and source-reported `D(V0)` intervals;
the destination requests one bit about those response intervals, not the
state or unknown Hamiltonian. The algebraic `X`-law no-go and `Y`-gap theorem
are proved for the two-point family. This is an established mathematical
interface conditional on the specified `Y` POVM. Its physical status remains
a candidate until a separate `Y`-axis calibration, preparation/reset protocol
and independence assumption are acquired. The N768 `X` bias certificate does
not discharge that added experimental obligation.

The N661 complete-SLD channel-order capital was read with its actual
quantifiers and access boundary. It is a separate source-derived,
unreviewed all-reference order result; its finite certificate assumes
unnormalized Choi matrices are supplied, and its independent reconstruction
gate remains open. The present calculation uses the ordinary two-parameter
SLD information matrix of one explicitly prepared logical qubit at a trivial
reference. It does not infer complete channel order or access a Choi oracle.

## Validation and artifacts

`assay_cost.py` uses exact `Fraction` arithmetic to verify the rational lower
bound `Delta_Y>0.02959`, the `10^-4` bias-adjusted gap `>0.02939`, the
50,000-shot Hoeffding exponent and the rational bound `exp(5.3)>200`. It also
prints approximate means, threshold and SLD matrix values for readability.
`RESULT.json` contains that script output. These checks verify the displayed
finite-dimensional calculations; they do not validate the N768 response
theorem, model-to-device match, lab calibration, or historical priority.

The read ledger gives exact source hashes and line scopes. `MANIFEST.json`
lists final owned-artifact hashes, byte counts and scopes; it excludes itself.
