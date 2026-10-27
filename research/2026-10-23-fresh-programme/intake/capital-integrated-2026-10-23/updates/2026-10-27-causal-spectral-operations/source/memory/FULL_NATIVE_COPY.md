## ASTRA Pro3 — Acquiring reusable causal memory

The strongest new construction replaces the previous one-step intervention model with a learned causal response law that predicts entire future intervention sequences.

The experiment uses one controlled pulse and a matched sham run. By comparing their reciprocal boundary reactions at the same measurement times, the learner eliminates arbitrary shared physical baseline drift and instrument-gain drift. These nuisance quantities no longer need to be assumed affine.

For a stable, three-state linear causal memory, six acquired impulse-response coefficients were sufficient to reconstruct the recurrence

\\[ \boxed{ g\_{k+3}=-\frac{3}{32}g_k+\frac{5}{16}g\_{k+1}+\frac12g\_{k+2}. } \\]

This recurrence generates every subsequent impulse coefficient without further source measurements.

The procedure was executed using the existing native Schur-reaction interface: two matched experimental runs, 12 scalar reaction readings, and one reset between runs. It then correctly predicted two new 48-step intervention sequences and a separately specified 36-step digital-feedback programme.

All predictions matched an independent latent-state implementation in exact rational arithmetic.

The construction is conditional on a stable, linear, three-state memory model and reproducible experimental resets. Its mathematical ancestry includes classical Hankel realization and system identification.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://doi.org\&sz=32)

ScienceDirect

+1

&#x20;The important procedural advance is that the retained knowledge transfers from isolated intervention measurements to later multi-step experiments, while cancellation of shared nuisance drift requires no affine time model.



### Precision and a decisive model failure

The exact recurrence was extended to bounded adversarial sensor error. With reciprocal-reading errors of at most \\(10^{-9}\\), the learner obtains certified intervals for all subsequently predicted impulse coefficients, rather than treating a fitted recurrence as exact.

For two newly specified intervention sequences, these retained-data certificates reduced mean uncertainty by approximately 12,534× and 16,951× relative to a stability-only prior. These are conservative certificate comparisons on synthetic data, not minimax-optimal improvements.

The more consequential failure is nonlinear memory. Two sources can produce identical responses to every isolated pulse yet differ when interventions overlap.

I implemented a source with ten unknown pairwise interactions among its five most recent interventions. Reusing the acquired linear-memory law, the compiler recovered all ten coefficients with 11 additional scalar reaction readings at one measurement epoch. It subsequently predicted new overlapping-pulse experiments exactly.

An alternative source containing a third-order interaction matched all those acquisition readings, but failed a newly specified triple-pulse experiment by exactly \\(1/500\\) in reciprocal response. One additional targeted experiment recovered the missing coefficient.

Eight fresh randomized intervention histories then rejected the inadequate quadratic model and accepted the amended cubic model. Under a supplied degree-three polynomial contract and exact measurements, the probability of falsely accepting a wrong frozen model on all eight tests is at most

\\[ \left(\frac3{11}\right)^8\approx3.06\times10^{-5}. \\]

That guarantee does not establish the degree-three assumption itself. I also constructed a higher-degree source that agrees with every test on the entire finite validation grid yet differs at a new intervention amplitude.

### Further attack: acquiring causal memory without experimental resets

I tested an alternative interface where the experiment runs continuously and cannot be reset. Under a stronger contract—four-step finite impulse memory plus affine source and instrument drift—the measurements become a linear identification problem with eight unknown coefficients.

The executed procedure used 12 sequential shunt interventions and eight scalar reaction readings. It recovered all eight physical-response, calibration and memory parameters exactly, then predicted:

- 24 newly specified open-loop reactions.
- 24 steps of a newly specified raw-reaction feedback controller, with explicit \\(10^{-4}\\) actuator resolution.
- Zero additional learner source calls after identification.

The experiment design had exact nonzero determinant \\(-8399/21780000\\).

This is not uniformly better than the matched-reset method: it requires a more restrictive physical drift and memory model. I constructed an analytic nonaffine alternative that matches all eight historical readings but changes the next hidden response by \\(0.01\\).

### Scientific assessment

The principal advance is reusable causal acquisition rather than static response identification. The learner can generate predictions for intervention sequences and feedback rules not known when the original measurements were performed. It can also identify a nonlinear interaction missed by its original experiment design, revise its model, and test that revision on fresh histories.

The decisive unresolved problem remains obtaining trustworthy physical guarantees for memory order, reset reproducibility and intervention-induced nonlinearities. Classical realization and system-identification algorithms given the same information can reproduce the procedures; no exclusive architectural advantage or physical discovery is established.

All six executable investigations completed an isolated, byte-identical replay. An independent verifier performed 259 exact checks. The source scripts, actual outputs, proofs and integrity manifest are preserved.

Complete governing mathematical note

Acquisition theorems, finite-noise certificates, nonlinear intervention learning, fresh validation, reset-free transfer and impossibility constructions.

Download reproducible research bundle

17 files, including the proof note, native-source programmes, six results files, independent verification, clean replay and SHA-256 manifest.

The Astra GitHub repository was not modified.