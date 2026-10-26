# Q95 scientific notes and abandoned constructions

The question selected after reading the assignment and common evidence was whether short, safe experiments can *certify* long-term mechanical behavior of a passive material without a preselected finite relaxation spectrum. This is consequential for materials screening and long-life design. The intended opening was acquisition of a missing long-time operation, not another fit inside an assumed source family. No externally measured material data were acquired.

## First construction considered: passive-spectrum continuation

I initially considered recovering a positive relaxation/retardation spectrum and deriving tight future-response envelopes from it. Positivity looked like extra structure that might make an extrapolation certificate possible. Primary searches immediately located both competent nonnegative-spectrum recovery and Brown–Grabovsky's direct treatment of feasible completely monotone extrapolation. Generic passive continuation and its instability are established. A new parameterization or better-looking fit would not supply the absent slow-mode information. This route was abandoned before claiming a new algorithm; no passive-fit benchmark victory is asserted.

## Stronger route constructed: bounded adaptive interrogation

The next proposed bridge was to design chirps, reversals and feedback to force otherwise hidden slow modes to reveal themselves. I represented a possible slow component as a Maxwell spring/dashpot replacing a permanent spring of the same instantaneous modulus. The difference in their stress responses is a positive causal filter of strain. This gives a simultaneous pointwise envelope attained by an ordinary maximum-amplitude step.

A squared-distance bound alone would not establish that adaptivity cannot help. I therefore constructed an exact causal Gaussian simulator: attenuate each ordinary step observation by the ratio of the proposed response contrast to the step contrast, and add independent noise to restore the detector variance. This reproduces the proposed adaptive experiment's conditional law. The construction is explicitly parameter independent for the fixed binary pair. The discrete proof covers arbitrary lower-triangular positive contrast matrices and arbitrary bounded randomized feedback, not only a selected waveform fixture.

The broad comparison-of-experiments mechanism is established. A targeted search found an explicit adaptive-collapse theorem in Song's 2026 preprint, making it especially inappropriate to call the abstract argument a discovery. The additional work here is its positive-kernel constitutive application, exact acquisition-time expression, conditional whole-spectrum minimax test, and equilibrium-modulus minimax obstruction. Their priority has not been established, and these are not labeled an accepted scientific advance.

## Positive conditional result and the missing physical operation

An independently justified upper bound on all relaxation times permits a least-favorable-spectrum matched test. I constructed that test and proved its exact minimax error across every nonnegative spectrum above the rate floor. I then removed the floor. A single arbitrarily slow Maxwell mode defeats every finite bounded policy, and the uniform equilibrium-modulus MSE equals that of the constant midpoint estimate. A smallest *fitted* rate does not establish the required physical support condition. This is the actual unresolved operation.

## Stronger physical route checked: acceleration by temperature

BOTTS already demonstrates practical acceleration of compatible master-curve acquisition. That performance is real at its stated material/protocol scope; it is not displaced by the Q95 no-go. I considered granting an ideal known bounded acceleration factor for every hidden mode. Even under that generous assumption the hidden rate can be chosen sufficiently small to retain the obstruction. For arbitrary materials the common factor is also a separate hypothesis, and thermorheological complexity is a published obstacle. No compatible universal mode-exclusion primitive was constructed. The thermal argument is preserved in Section 7 of the proof, rather than assumed away.

## Stress checks actually executed

The executable compares exact Gaussian risk for five waveform types across seven rates, exhausts every 16-bin amplitude-saturating waveform, checks a 1,000-spectrum least-favorable comparison, and implements the same adaptive policy directly and by the step-observation simulator. The latter Monte Carlo is a diagnostic of implementation; the exact law equality is proved independently. The ordinary likelihood-ratio comparator is globally optimum in the declared experiment class. A simple chirp shown in the table is a diagnostic candidate, not a claimed implementation of BOTTS.

I deliberately tested the one-sign hypothesis against two passive RC filters with a sign-changing impulse contrast. A sinusoid wins decisively there. Thus neither passivity alone nor a step response of one sign warrants the theorem. No broader statement that all adaptive material characterization is pointless is supported.

The first numerical run produced floating-point warnings from NumPy matrix products despite finite values and passing recurrence comparisons. I did not suppress the warnings. All relevant products were replaced by explicit `einsum(..., optimize=False)` contractions, avoiding that path. The complete scientific run then passed with Python warnings promoted to errors. The initial warning behavior is recorded here; the cause in the installed numerical backend was not independently diagnosed. The change affects implementation, not the analytical result.

## Stopping decision

A complete proof and executable scientific unit was available within the allotted first stage. The attempted universal long-time certification capability is blocked in the declared class, while the conditional optimum requires an operation the trial did not acquire. Continuing to adjust a waveform after the exact domination proof would not resolve that blocker. No civilisation-changing claim, physical material discovery, or externally validated apparatus result was obtained.
