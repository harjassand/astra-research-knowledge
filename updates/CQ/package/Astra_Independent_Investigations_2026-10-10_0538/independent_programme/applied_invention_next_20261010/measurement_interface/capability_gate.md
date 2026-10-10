# Decision: preserve construction, do not promote novelty

The derived interface measures a signed antisymmetric endpoint amplitude of a fixed, input-modulated reciprocal ladder. Swapping its initial/readout endpoint exactly compares a signal with its temporal reversal, without reversing the physical source. A clock-augmented hierarchy is complete for bounded classical signal laws. Proof, finite-shot bounds, finite-coupling remainder, and local numerical checks are in `proposal.md`.

## What is actually new here?

Potentially the packaging as a complete autonomous endpoint-reciprocity hierarchy, and a precise compiler from an ordered-integral word to two endpoint experiments. The searched primary literature did not establish this exact combined formulation. That absence is not evidence of novelty, and the theorem is close to a corollary of sparse path-characteristic-function theory.

## What is not new?

- Encoding order with noncommuting evolution, Chen iterated integrals, Lie-bracket control.
- Coherent nearest-neighbor ladder couplings, dark/reference Ramsey interferometry, measuring propagator amplitudes.
- A rotating-field handedness response: the three active matrices form the spin-1 representation, within Rabi's 1937 treatment of arbitrary angular momentum.
- Probe-based temporal-asymmetry sensing: SENSIT already includes intrinsic time-reversal breaking in its final 2025 publication and demonstrates an NMR experiment.
- Acquiring multitime correlations: quantum nonlinear spectroscopy already does this.
- Computing a task-specific function before reading a sensor: quantum computational sensing already does this, including experimental demonstrations.

## Acquisition advantage actually proved

A strict distinction from constant commuting integrators, not from existing sensing in general. A stationary randomly phased rotating two-channel input has identical integrated-input laws for opposite rotations, but the ladder returns opposite endpoint contrasts. At one exact parameter choice they are +1.6 and -1.6. This is a valid bounded comparison against a weak baseline, not an unprecedented observable.

## Missing capability claim

No concrete physical target has been shown to possess an observable that current native sensors cannot acquire but this interaction can. The assumed signal-to-ladder transduction may itself be the hardest unavailable resource. There is no invented new hardware primitive and no established practical advantage. Thus this branch **fails the requested genuinely-new-capability gate at present**.

## Preserved deliverables

- `proposal.md`: self-contained construction and theorem/proof route, exact assumptions, resource bounds, explicit prior-art boundaries.
- `verify_probe.py`: deterministic checks, only small matrices and ODEs.
- `verification_results.json`: reversal identity residual <=3.34e-16; chiral formula residual <=5.94e-12; leading coefficients and reference readout checked.

Primary sources are linked in `proposal.md`. No physical experiment, paid computation, external contact, publishing, or user-computer access was used.
