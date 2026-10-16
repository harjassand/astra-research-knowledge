# Empirical calibration gate

## Established optical route

The fixed Bell receiver has an established same-photon polarization/path implementation. Encode the prepared output as polarization and the reference as path; use a polarization-independent path-preparation stage followed by a polarizing beam splitter and diagonal-polarization analysis at both output ports. This is a standard conceptual four-outcome analyzer, not a new physical operation or a claim that an apparatus is available.

Primary precedents include Yoon-Ho Kim, Single-photon two-qubit entangled states: preparation and measurement, https://arxiv.org/abs/quant-ph/0303125 , and Rosenfeld et al., Remote preparation of an atomic quantum memory, Fig. 2 and the preparation/analyzer discussion, https://arxiv.org/pdf/quant-ph/0608229 . These demonstrate compatible primitives. They do not certify the mixed-state preparation, score distributions, or source optimum in the present task. The same-photon architecture does not inherit the usual restriction for Bell analysis of two independently encoded photons.

For the preferred design the prepared output is a 95:5 mixture of orthogonal eigenstates. The conditional reference Bloch vector is (ell i 6/11,0,9/11), with a nonzero minority eigenweight. Replacing that mixture with a pure state changes the fixture. Preparation randomization is conditional on label and input; target receivers must not be given those labels or hidden mixture indices. Use emitted/heralded trial weights, not weights selected retrospectively from successful detections.

## What would establish an actual advantage

1. Calibrate actual conditional reference states, input and reveal probabilities, erased-reference states, and transport changes, with uncertainty regions and drift accounting. Do not assume the ideal equality of reference marginals survives implementation.
2. Obtain a rigorous lower confidence bound on the actual source's optimal binary squared-error risk, by solving its blockwise Sylvester problem over the allowed calibration region. Best-fit tomography alone is not such a bound.
3. Freeze target preparation, Bell analyzer, outcome labels and scores. Evaluate actual target squared loss on independent randomized held-out trials and obtain an upper confidence bound. Retain no-click/loss events or an explicit justified trial model; do not silently postselect unequal efficiencies away.
4. An actual receiver advantage requires target-risk upper bound below source-optimum lower bound. If claiming the full channel-order reversal, separately certify the implemented ordinary reference-free channel ordering.

Direct target-risk evaluation already includes actual target receiver imperfections; do not deduct a separate receiver-error budget a second time. Average Bell fidelity, a four-Bell-state confusion matrix, or an unrelated published coincidence rate cannot replace this task-specific comparison.

## Conditional source symmetry shortcut

If the experimental preparation really satisfies tau_-=Z tau_+ Z, with tau_+=(I+xX+yY+zZ)/2, and input i is independently uniform, the erased reference hides the label and the source optimum is exactly 1-q(x²+y²). A joint confidence region for q,x,y then gives lower bound 1-sup q(x²+y²). The ideal point has x=6/11,y=0.

This shortcut requires certified conjugation symmetry, randomization, and loss behavior. A nominal Z gate or two measured Pauli expectations alone does not establish those prerequisites. Quantify deviations, including erased-branch leakage, or enlarge the source confidence set.

## Current boundary

The algebra specifies a simpler receiver and finite faithful preparation. Existing optics literature supports the architecture, but no task-specific calibrated experimental realization or practical advantage has been established. The next useful evidence is preparation/calibration counts and held-out score data, or a validated model of those quantities. Recompute statistical guarantees for that actual model and account separately for calibration, switching, drift, and losses. The ideal 25,283-per-arm evaluation count is not a promised laboratory budget.
