# Foundational mathematics branch: finite-horizon phase-memory law

15 October 2026. Workspace: `/Users/harjas/Documents/ChatGPT/ultra`.
All files from this branch are contained in
`research/2026-10-15-foundational-capability-v1/workers/foundational_math/`.

**Strongest result:** an all-parameter proof with a matching construction for
the finite-horizon state complexity of a fixed badly-approximable irrational
phase. At every fixed error `0<epsilon<1/4`, the minimum number of classical
stochastic states is `Theta_(alpha,epsilon)(T^(1/3))`. At exactly zero error
it lies between `T` and `T+1`. An ideal qubit supplies the target terminal
probabilities with dimension two. The proof survived a targeted Sol Max audit
and the coordinator's independent reconstruction. Historical novelty and
exceptional significance remain **UNKNOWN**; the broader mission is not
established by this branch.

## Exact theorem and information contract

Fix `alpha in (0,1)` with `||q alpha||_(R/Z)>=kappa/q` for all `q>=1`,
and let `p_k=(1+cos(2pi alpha k))/2`. A classical simulator is any triple
`(mu,P,f)` with arbitrary initial probability `mu`, arbitrary homogeneous
row-stochastic `n by n` transition matrix `P`, and readout `f in [0,1]^n`.
Its output probability after `k` wait steps is `g_k=mu P^k f`. Model
parameters may depend on `T` and `epsilon`, and arbitrary real transition
probabilities are allowed in the lower bound. Transients, reducibility,
nonnormality and nonstationary initial distributions are all included.

If `|g_k-p_k|<=epsilon` for every integer `0<=k<=T`, then, with
`z=exp(2pi i alpha)`,

`n^3 >= kappa^2 [(T+1)(1/2-2epsilon)-|1-z^2|^(-1)]`.

Conversely, a two-shift stochastic walk on a suitable continued-fraction
denominator `N=O_(alpha)((T/epsilon)^(1/3))` gives the required error.
For the entirely specified computable phase `alpha=(sqrt(5)-1)/2`, one can
take `kappa=1/3` and use Fibonacci denominators.

At zero error the separate argument gives
`T <= N_alpha(T,0) <= T+1` for every integer `T>=1`. No assertion is made
about the precise minimum within those two values or about a uniform law
when positive `epsilon` tends to zero with `T`.

The models receive the same phase specification and identical wait commands,
followed by one terminal read command. There is no external integer step
counter supplied to the readout. This is a terminal acceptance-probability
problem, or separate prepare–wait–read trials; it does not preserve a repeated
measurement joint law or describe a nondisturbing autonomous ticking clock.

## Why the lower bound survives approximation

The main lemma is independent of spectral extraction:

`||(zI-P)^(-1)||_infinity <= 8n/min_(1<=q<=n)|1-z^q|^2`.

For an approximate unit-modulus eigenvector, positivity and the Markov
expectation place one of its `n` coordinates near each of `n+1` distinct
rotating phase points. Two coordinates coincide, forcing a short approximate
return of the phase. This gives the bound with no eigenvector-conditioning,
minimum-transition-probability, spectral-gap or stationarity assumption.
A finite Fourier witness then turns uniformly accurate cosine probabilities
into the cubic state lower bound. The upper construction mixes two cyclic
shifts so that its first Fourier eigenvalue has the exact desired argument
and radial loss `O(N^(-3))`.

The full statements, constants, proofs, stochastic construction, zero-error
Cayley-Hamilton argument and precision analysis are in
`PHASE_CLOCK_THEOREM.md`. The proof, rather than finite tests, supplies the
all-parameter result.

## Verification and audit

`verify_phase_clock.py` completed successfully on Python 3.14.3 with mpmath
1.3.0 at 100 decimal digits. `VERIFICATION.json` records five horizons at
error `1/16`:

| horizon `T` | constructed states | lag diagnostic |
|---:|---:|---|
| 30 | 34 | all lags; independent exact rational state propagation |
| 100 | 55 | all lags |
| 1,000 | 89 | all lags |
| 10,000 | 233 | all lags |
| 1,000,000 | 987 | at most 2,000 declared sampled lags |

The script checks the chord identity, radial-loss estimate, probabilities,
and an analytic error budget for rational transition/readout rounding. The
`T=30` check uses exact `Fraction` arithmetic for the rounded transition and
readout tables, independently of the Fourier formula, at all 31 times.
The million-step case does not claim exhaustive numerical lag checking.
No quantum circuit or physical experiment was executed.

Targeted auditor: `/root/foundational_math/phase_clock_audit`,
`gpt-6.1-sol`, reasoning `max`, fresh context. This was the only helper
spawned by the branch. `audit/AUDIT.md` gives the independent proof review
and bounded primary-literature comparison. The auditor found no gap after
requiring positive error, made the exact chord weights/shift convention
explicit, and supplied the zero-error boundary. The coordinator also read
and reconstructed both arguments. These are internal reviews; no formal or
external correctness certification is claimed. No token or dollar telemetry
was available or inferred.

## Closest prior art and novelty boundary

The cosine probability clock and qualitative separation are established:

- [Benvenuti and Farina, A Tutorial on the Positive Realization Problem,
  Example 4 and Theorem 15](https://sites.math.rutgers.edu/~sussmann/papers/res-farina-tutorial-positive-realization.pdf)
  treat the irrational cosine response and positive-realization order.
- [Gainutdinova and Yakaryilmaz, Unary probabilistic and quantum automata on
  promise problems](https://arxiv.org/abs/1502.01462) use the same qubit
  rotation mechanism for an infinite-input bounded-error separation.
- [Johnson and Paparella, A matricial view of the Karpelevic
  Theorem](https://arxiv.org/abs/1611.06970) give stochastic eigenvalue
  realizations and roots-of-unity polygon geometry.
- [Szehr, Eigenvalue estimates for the resolvent of a non-normal
  matrix](https://arxiv.org/abs/1305.7208) supplies a strong general
  spectral-resolvent comparator. The present lower proof instead directly
  uses stochastic positivity and phase recurrence.

The bounded searches did not locate the precise finite-horizon uniform-error
cube-root theorem. This is not a priority certificate. No claim is made that
the irrational rotation, classical infinite-horizon obstruction, polygon
geometry, or positive-realization framework is new.

## Supplied resources and limitations

Both constructions assume a supplied computable phase. For an ideal qubit,
an exact phase gate yields `p_k`; maintaining finite-horizon error requires
phase accuracy `O(epsilon/(T+1))`, hence `O(log((T+1)/epsilon))` precision
bits under direct error composition. Preparation, calibration, reset and
readout remain operations to be acquired in a physical setting.

The classical upper construction also needs finite parameter precision. Its
rational transition rounding can be `O(epsilon/(T+1))`, with readout rounding
`O(epsilon)`, and it has two outgoing transitions per state. Neither model
gets an uncharged perfect numerical parameter in an operational comparison.

The lower bound counts states. Its ordinary binary memory implication is
`Omega(log T)` bits, and storing the integer `k` and evaluating a cosine on a
conventional computer also uses `O(log T)` bits. There is no generic speed,
energy, acquisition, learning or physical-capability separation. Continuous
analog memory lies outside the finite-state comparator. Exceptional
foundational significance has not been demonstrated.

## Other preserved exact outcomes

The initial independent opportunity was eventual branchwise rank collapse.
`RANK_COLLAPSE.md` reconstructs the exterior-power cutoff
`binom(d,r+1)` and gives a sharp trace-preserving family when the outcome
count may grow. The route was killed as the main candidate because this
mechanism sits close to established exterior algebra and local automata.
An exhaustive restricted two-partial-injection search gave maxima 6, 10,
14 at dimensions 4, 5, 6, respectively. Thus an all-dimension binary
saturation extrapolation failed already at dimension six in that restricted
class. No upper bound for arbitrary two-Kraus matrices or untested dimensions
was inferred. Code and exact finite receipts are preserved.

`HIDDEN_SPECTRUM_COUNTEREXAMPLE.md` gives two equivalent fair-iid QHMMs
with full collision-transfer spectra `{1/2}` and `{1/2,1/4,1/8}`. It records
the exact source theorem hypotheses and a short quote before applying the
counterexample to the unrestricted full-spectrum-invariance statement in
arXiv:2412.12812v2. Hidden unobservable modes are the issue; only visible
scalar poles survive as invariants. `verify_hidden_spectrum.py` checked
tensor eigenvectors exactly and all 2,047 binary words through length ten.
The all-length equivalence has a separate exact proof. This standard
realization counterexample is not presented as a new foundational theorem.
No external message was sent.

## Capital provenance and final branch status

Initial retrieval followed `AGENTS.md`, `00_START_HERE.txt` and task concept
routes at capital revision `25fc24509a59aabee340b36b588c9e59a144253d`.
N636's exact source proof range was read before reusing its exterior-power
idea. Other inspected HMM and rounding dossiers were navigation/comparator
material and were not proof premises of the phase-clock theorem. Unreviewed
capital claims were not promoted. The phase-clock lemma and matching
construction were independently derived in this branch, then internally
audited; no other current campaign worker output was used to select them.

Final status: **SCOPED_MATHEMATICAL_RESULT_WITH_INTERNAL_AUDIT**.
Historical novelty: **UNKNOWN**. Exceptional foundational significance:
**NOT_ESTABLISHED**. Physical or practical capability: **NOT_ESTABLISHED**.
No publication, external validation, new axiom, formal proof or mission
completion is claimed.
