# Native killed-duration and residence-numerator proof candidate

**Status:** a self-contained, computer-assisted mathematical proof candidate for one specified finite Ising model. It has internal independent reviews, exact scalar receipts, directed numerical certificates and finite implementation checks. It is **not formally verified**, independently peer-reviewed, a practical first-passage estimator, or a claim to have achieved the North Star.

## Proposed result
On the1600×1600 torus, with physical energy E(S)=8P(S)−|S|/25 and independent rate-one-per-site heatbath clocks, start from all-minus a and stop on first majority B={|S|≥1280000}.

The construction proposes a native killed-chain congestion bound below e1000. Combined with a paid rare-departure calculation, it gives the hard-source residence numerator

1 ≤ N*/w(a) <1+1.087×10^-7.

For the **hard** capacity C*=cap(a,B), the exact identity is E_aτ_B=N*/C*. Thus the residence numerator is controlled to the displayed precision; capacity uncertainty remains a separate input. This does not identify hard and soft capacities.

## Read these first
1. `research_notes/creative_landscape_20261114/COMPLETE_KILLED_PATH_PROOF.md`: analytic assembly, exact model, path rules, entropy bounds, native clock and phase sum.
2. `research_notes/source_reconstructed_20261114/HARD_RESIDENCE_COROLLARY.md`: proposed implication for the numerator and mean.
3. `research_notes/source_reconstructed_20261114/GLOBAL_KILLED_PROOF_REVIEW.md`: independent weight/entropy/scalar review and limitations.
4. `research_notes/bridge_resume_20261114/GLOBAL_CANONICAL_RECORD_CHECK.md`: independent reconstruction, winding, seam, stopping and multiplicity review.
5. `research_notes/sampler_resume_20261114/DURATION_INDEPENDENT_AUDIT.md`: separate native-rate, contour-root and scalar audit.

Older development notes retain their original conditional language and thresholds. The complete assembly and this cover identify the intended current result. Historical filenames such as `conditional_duration_numerator.py` are preserved: the script verifies a modular implication, while the separate analytic assembly supplies its congestion premise.

6. `research_notes/residual_duration_20261114/WHOLE_CONGESTION_CHALLENGE.md`: whole-chain challenge and finite spectral/clock diagnostic.

## What is supplied
- Original recovered model/source material and its dependencies under `flow_resume_recovery/unpacked/`.
- Directed upward magnetic-moment tables, the repaired positive-recurrence source and arithmetic incident/repair notes.
- Current hull, confined-strip, full-cylinder, erosion and raw-face/renewal proofs and scalar receipts.
- Independent reviews, small exact/exhaustive tests and scaled-torus path checks.
- `reproduce.py`, a fresh-copy runner, and `saved_reproduction.json`, the observed result for this package.

No regenerable23GB contour-word caches, compiled binaries, or heuristic guide arrays are required or included.

## Reproduction
Python3 with NumPy is required for the complete default test set. From this directory run:

    python reproduce.py

It checks the package manifest, copies the files into a fresh temporary directory, reruns exact scalar tests, recomputes hull bounds using saved upward moments, regenerates the small confined-strip certificate, and reruns the listed finite geometry/reconstruction checks. It does **not** silently overwrite the preserved receipts.

**The default run does not regenerate the large magnetic recurrences.** The saved moment tables are reused. Their positive-recurrence source and earlier receipts are included. To regenerate all four M1900 activities as well, with a compatible64-bit-mantissa long-double C++ environment:

    python reproduce.py --full-moments

That optional mode requires g++ and uses explicit rounding flags. It was not run during this package reproduction unless `saved_reproduction.json` explicitly says otherwise. Finite geometry tests are supporting evidence, not substitutes for the general proofs or full-size scalar certificates.

## Important boundaries
- The uniform killed-duration bound is enormous; it does not establish efficient trajectory completion.
- There is no controlled variance/work result for a practical guided sampler here.
- The theorem candidate is for these finite parameters, not arbitrary system sizes or temperatures.
- Winding, thermal companions, repeated visits, first-majority stopping, native site-clock rates and edge-occurrence multiplicity must remain as stated in the proof.
- Any withdrawn contour certificate or reconstruction premise would make the residence implication conditional again.
- This is a reusable mathematical partial result, not a new engineering capability or civilisation-changing breakthrough.
