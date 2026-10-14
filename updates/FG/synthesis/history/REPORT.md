# Molecular-history obtainability: integration audit and new interfaces

14 October 2026. The selected opening mission guided this continuation; the
worker transcript and supplied calculations were treated as evidence. Source
files and previous FE capital were preserved. All new investigation files are
under work/FG-history. No repository edits, publication, external contact or
laboratory action were performed by this investigator.

The new packet advances the experimental proposal: ground-Zeeman label parking
removes the leading differential electronic Stark operator, and a transverse
loaded reference can test return visibility without assuming molecular optical
coherence. Its momentum-coded separator is a real multilevel conditional result.
The packet also corrects the earlier optimistic nonlinear acquisition estimate.
These justify a scoped continuation of N796, with original history retained.
The claimed operation, joint visibility, affordable science and novelty remain
unestablished.

## Physical and source audit

The complete README, 378-line narrative and all five producer Python files were
read. Supplied result/log objects and manifests were inspected; exact hashes,
ranges and structured comparisons are in the read/replay ledgers. The current
additional capital revision is unmerged PR83 head
865a399dc8a1119a9cd5119b7ea68181f0e2d34b; main remains pinned at
ace0cfc4437fe91c20ccd24d69e0ee4bb335e871. N796 and N791 were reused with their
current scoped premises, not promoted by repository availability.

[Wu et al., author v2](https://arxiv.org/html/2511.19687v2) supports the actual
Ca+/CaOH+ recoil baseline and its limitations. The cat amplitude and recoil
visibility concern the original apparatus. Source pulses are not mutually
phase stabilized; the temporal duration is inferred assuming transform-limited
pulses. The absorption model misses absolute magnitude. The molecular lifetime
is estimated rather than a measured coherent T2. Actual new-sequence contrast,
transfer fidelity, pulse phase, survival and full-cycle throughput remain
unacquired.

The cited author Git blobs were fetched and their content SHA1 verified.
Selected model-source cells confirm average intensity 1.1e8 W/m², rate 1e5 Hz,
3783 cm^-1 and oscillator strength 3.7e-5. Their reduced dipole convention gives
4.81096e-31 C m. These are model inputs, not fitted experimental pulse strengths.
No author notebook outputs or experimental dataset was reproduced. The actual
carrier-coupling implementation confirms Laguerre/Debye-Waller dependence on
motion; ground-state carrier calibration cannot qualify a large cat.

The notebook's explicit dipole-squared formula contains a factor 3/2, whereas
the author manuscript's displayed oscillator-strength conversion contains 3.
Read literally with identical conventions, the dipoles differ by sqrt(2).
The packet consistently pins the code parameter and its driven-field convention;
that does not make it a measurement. Angular/field conventions should be
reconciled before interpreting absolute excitation or radiative predictions.

[CaOH+ photodissociation work](https://arxiv.org/html/2401.10854v2) explicitly
calculates B_e=.3655 cm^-1 and harmonic frequencies 747.4, 481.2 and 3949.9
cm^-1. They are cation theoretical parameters, not neutral CaOH line data or
measured excited-band B1. Setting B1=B0, neglecting hot-band shifts/IVR and
assuming a 300-K rotor remain declared reference-model assumptions. The
approximately .788 all-mode ground-state probability is harmonic thermal
arithmetic, not an acquired preparation distribution.

The scalar/vector/tensor structure in [the Ca+ polarizability paper](https://arxiv.org/html/1703.09950)
supports the leading J=1/2, linear-light symmetry. [Ground-spin-qubit work](https://arxiv.org/abs/0902.2826)
demonstrates related control, but its reported gate fidelity cannot be borrowed
for the proposed cat shelving sequence. [Spectator-mode measurements](https://www.nature.com/articles/s42005-025-02373-x)
show actual axial spectator effects in a related N2+/Ca+ quantum-logic system;
they do not measure this CaOH+ transfer. The packet's 20-us delay attenuation
and static-polarizability/Rayleigh numbers are reference-scale calculations,
not measured parked-memory coherence or chemical-loss bounds.

## What survives mathematically

The two-band strong-pulse theorem is correct under coherent phase covariance,
initial support in the ground band and the stated common corrected observation
functional. The first selected harmonic produces a G-E cross-block. The second
pulse has two terms, initially in E-E and G-G, weighted by exp(+/-i q2 s/2).
Subsequent arbitrary linear native evolution can act on those two origins.
The two-row inversion and third-port consistency relation follow. The proposed
5³ phase grid is alias-free for this two-band coherent model. Multiband or
branch-dependent open pulses require another phase/support/error contract.

The grating construction makes axial phase qKz independent of optical frequency;
this addresses the earlier carrier-only branch-phase approximation. It still
needs the entire used band to propagate and actual route waveforms, spectral
phase, diffraction losses and all-mode recoil to match. A mathematical Gaussian
has tails below the propagation threshold; at the retuned reference parameters
that tail is tiny, but any engineering band truncation must be specified. The
all-pulses transverse reference has different radial momentum from science.
The single-mode correction factors in the source do not acquire its full
instrument transfer.

A common trace-preserving channel acting solely on the molecule preserves
Tr K, even for non-Hermitian K. Thus molecular optical coherence need not persist
until fluorescence once the ancilla signal is encoded. Branch-resolving emitted
recoil, state-dependent trapping and chemical loss violate that simplification.
No favorable millisecond molecular coherence is inferred.

## New mathematical/physical synthesis

REFERENCE_AND_MOMENTUM_IDENTIFIABILITY.md contains the full restricted proofs.

* A loaded-reference instrument countermodel agrees on every calibration phase
  scan at C=.4 yet differs by .6 on a science-correlated hidden state. The
  reference remains a useful necessary test, but a state-uniform science
  correction needs a justified factorization or calibration-span/error bound.
  Equations (1)-(3) give that quantitative transfer contract by trace-norm
  duality. This also preserves N791's separate uniform-error requirement.
* With r+1 phase-covariant bands, the selected second-pulse harmonic can contain
  2r odd momentum frequencies. An exact nonzero three-band null function is
  invisible at q2=-1,0,+1. An explicit finite ladder mixture additionally passes
  the third-port check while retaining a computed leakage coefficient about
  .002753 under common four-pulse controls and static class detunings/dipoles.
  The mixture is a floating diagnostic; the coefficient-model nullspace
  is exact. Passing the consistency test cannot certify band closure.
* At least 2r nonaliasing complex ports identify arbitrary coefficients in that
  finite-band model. A doubled-pitch second-pulse grating conditionally supplies
  half-momentum ports for a three-band check. Its illustrative five-port
  condition number is about 99.3 at s=.702, compared with 2.731 in the original
  two-band matrix. No optical implementation or affordable noise performance
  is supplied by that conditional construction.
* A binomial-polynomial test vector proves a general fixed-phase-arc condition
  lower bound, asymptotically proportional to (sin A)^(-(2r-1)). Adding direction
  settings at fixed small cat separation cannot generically stabilize arbitrary
  multiband coefficient recovery. This is scoped to the stated linear direction
  interface and supplied finite-band model, not all spectroscopy.
* A concrete parking map uses a ground-Zeeman swap followed by the already
  allowed old-D-to-vacant-S shelving edge. It avoids the forbidden delta-m=3
  transition while preserving both labels in an ideal unitary. RF/Raman
  selectivity, phases, cat-dependent carrier response and the full return remain
  experimental obligations.
* Conditional weak-signal dose scaling shows why less fluence per attempt need
  not reduce total dose or replacements for a fixed nonlinear precision. The
  actual loss exponent and response must be acquired together; no optimum is
  invented from independent favorable assumptions.

## Numerical reproducibility: a material qualification

Both unmodified replay runtimes failed validate.py at the J70/J80 convergence
assertion. Both generate_reference.py runs exited zero while writing 40
nonfinite scalar fields. validate_extra.py passed. Failed outputs and stderr
remain in replay_py314 and replay. Their validation_results.json files are
merely copied source objects: the failed script never wrote a fresh one.
They must not be described as successful replay receipts.

The issue was localized numerically: for the Jmax80,M18 real dipole matrix,
default scipy.linalg.eigh driver evr returns an eigensystem with eigen residual
about 3.8e-15 but eigenvector orthogonality error .019984458. Using that basis
repeatedly in V exp(diag) V† loses unitarity. The independently compared evd,
evx and ev drivers give orthogonality around 1e-15. This observed numerical
failure does not refute the pulse equation or molecular mechanism; its library
root cause beyond these diagnostics is unconfirmed.

A separate repaired copy uses evd and rejects nonorthogonal/nonunitary/nonfinite
outputs. It passes the source validation and regenerates all 20 finite grid
cases, reproducing supplied reference magnitudes and convergence. Runtime
matmul warnings persist even where the invariants pass; stderr is retained.
The correction is separately labeled and shown in NUMERICAL_REPAIR.diff.
No original scientific file or supplied result was changed.

The independent checker imports no producer code. A small rotor is integrated
directly with DOP853 and compared with the repaired split propagator. It also
checks the reference countermodel, explicit ladder mixture, extra-port
conditioning, parking map and source resource arithmetic. These checks do not
validate the omitted molecular physics or general scientific originality.

## Consequential output and strongest comparisons

The proposed scientific target—distinguishing ground-origin rotational/Raman
beats from excited-origin dynamics—is more specific than observing a nonzero
two-level order signal. It remains contingent on closure/extrapolation,
calibration, actual molecular response and sufficiently affordable precision.

[Schindler's 2019 proposal](https://arxiv.org/html/1809.06776) already develops
recoil pump-probe/stimulated-return access to intramolecular redistribution.
[The 2026 N2+ paper](https://arxiv.org/html/2603.10553) demonstrates related
forbidden-transition population transfer on much slower chirped interrogation;
it does not qualify femtosecond CaOH+ pulses. [Gas-phase 2D IR](https://pubmed.ncbi.nlm.nih.gov/37871134/)
already uses four ultrafast pulses and tag-loss action readout on more complex
molecular ions. [Peptide work](https://pubmed.ncbi.nlm.nih.gov/40045165/) probes
coherent vibrational signatures, and [mixed-domain pulse shaping](https://pubmed.ncbi.nlm.nih.gov/41128312/)
already selects rephasing, nonrephasing and two-quantum pathways. Exact matched
precision, specimen, preparation, energy and complete-cycle comparisons remain
UNKNOWN. Generic pathway selection or pump-probe access is not novel here.

The source's corrected budget is appropriate for its specified estimator:
MSE<=4/(N C² sin²s), giving N>=100/(C² sin²s |X|²) for its five-standard-error
planning criterion. Phase-grid allocations are already inside N. A grid does
not multiply those counts by 500 again. The full loaded C=.4 and 50 independent
trials/s are assumptions. Retuned quarter-fluence |X_E|≈.001783 gives roughly
4.7e8 shots and 109 assumed-rate days for one coefficient; additional delays,
changes, controls and calibration add cost. Source rounding to .0018 gives
its 107-day table. Four full-fluence pulses spend four times the energy.

Allowing reproducible molecular replacements is a justified correction to the
earlier single-individual survival requirement. It still pays reloading, reset,
chemical-identity verification, drift and effective sample dependence. Neither
new q_loss nor an actual complete-cycle rate was measured.

The decisive next step remains the full parked-memory loaded return experiment,
followed by only a few preselected science points if the measured signal,
instrument-transfer error and attempted-shot budget support them. Reject an
unaffordable nonlinear claim at its declared budget; do not repair it by
assigning a longer T2, a larger noiseless cat or borrowed control fidelity.
