PASSIVE HAMILTONIAN CALIBRATION AND FINITE RELIABILITY CURVES
Astra construction, 5 November 2026

MAIN COMPLETED CAPABILITY

For a static local Hamiltonian with a known complete Pauli candidate list,
fixed locality k and candidate degree d, and actual calibrated vacuum-input
Pauli ports L_i,a=sqrt(r) sigma_i,a/2, all coefficients can be learned from
one continually evolving source through finite classical photon counts.
No direct source preparation/control/readout, coherent output collector, or
receiver quantum memory is used for CALIBRATION. Source/model completeness,
port axes/phases/rate, calibrated positive detection efficiency and stable
dynamics over the full exposure remain premises.

The preferred receiver mixes each port with a finite matched coherent local
oscillator. Its two signed jumps are proportional to the Pauli projectors;
its total detected flux is kappa*r/2 per port, independent of window width.
Adjacent-window correlations minus their time reversals cancel all even
Hamiltonian orders. A positive diagonal kernel, a certified nonlinear inverse
and a rooted connected-SET forward compiler complete the mathematical
operation. The window width is independent of target accuracy. Counter range,
sampling, source forgetting, fixed detector deadtime, timing, optical phase,
loss, local-oscillator photons, routing and classical computation are paid.

The passive lower bound uses admitted coefficients +/-2 eta, requiring
2 eta<=J and eta<=r/8. Even a receiver given all fields, final source and
initial purifiers needs exposure Omega((r/eta^2) log(n/confidence_failure)).
The match concerns precision and simultaneous learning at fixed local/access
ratios, not every loss/weak-port constant or classical runtime.

WHAT THE NUMBERS ESTABLISH

Two million raw event-driven blocks were executed for EACH of two finite
oscillator settings on the same interacting two-qubit Hamiltonian, including
40% collection loss. The stronger oscillator (mu=1 detected photon/window)
used 29,992,217 simulated source+LO events and reached maximum coefficient
error .0307006. The matched oscillator (mu=.15) used 9,596,361 such events and
reached error .0594418. Both runs remain in the record. They have exact-model
stationary initialization; physical burn-in, deadtime, clock errors, dark
counts, clipping and spectral detector response were not simulated.

The exact-regression inverse reached 3.0631e-11 maximum error after eight
iterations. These are floating-point diagnostics. Their useful w=.25 setting
is OUTSIDE the conservative uniform inverse certificate.
The sampled two-qubit iterations omit the feasible-set projection; they
demonstrate the response correction, not an execution of the uniform theorem.

The generic rooted-set/Mobius compiler structure was also implemented and
executed on one three-qubit, five-term case at cutoff L=3. Two responses
differed from a separate full density-matrix calculation by 7.33e-8 and
1.37e-7, below loose analytic truncation bounds .0548 and .00863. It enumerated
26 and 20 rooted sets and executed 196 sparse exponential actions. All
operation counters are saved. The floating expm backend is not the theorem's
certified finite-arithmetic implementation.

At the preceding coefficient target eta=1.4526409921e-5, a different rationally
certified schedule uses w=.006, kappa=.6, matched mu=.0036, rho<=.238930,
response accuracy 4.92445e-9, counter cap 9, about 10^26.1731 raw shared blocks,
and 10^27.2162 model time units before extra service. This improves the prior
10^39.12 sufficient raw-trial bound by about thirteen orders, but remains
impractical. Neither number is a lower bound. Different observations and
access bills prevent interpreting this as a demonstrated device speedup.
The old bounded-neighborhood no-burn-in construction is retained separately.

The new classical learner can replace calibration inside the preserved
correlated-calibration first-input recovery theorem. It does NOT remove the
separate coherent archive, its lossless ingress, protected storage over the
whole acquisition/computation interval, or P1's growing hardware. A fixed
aggregate optical passband and microscopic finite-band completion are not
established. No general natural-noise model is inferred from photon flux.

The detector array handles busy time only. It does not remove a fixed
timestamp-jitter floor. The allocated timestamp tolerance must be physically
available; a direct clock implementation pays frequency of order its inverse
and the actual detector latency/bandwidth requirement. Further receiver
service and reference calibration may add accuracy-dependent cost. The
inverse-square statistical exposure comparison is not an optimality claim
for the full hardware bill.

INDEPENDENT COMPLETED RELIABILITY COMPANION

next2_reliability/PROOF.md closes the previously unfinished whole-CDF
computation for succinct reversible dynamics, product invariant law,
equilibrium-safe start, certified gap and explicitly costed static all-terminal
failure counting/sampling. One finite confidence event covers every positive
rational deadline at relative width 1+epsilon. Genuine Poisson uniformization
preserves CTMC deadlines; a distinct discrete theorem handles actual endpoint
ticks. Work is polynomial in numerical inverse gap and inverse accuracy,
with no inverse GLOBAL failure-probability/lifetime factor.

The companion proves changing-invariant-law uncertainty:
  exp(-(alpha+2 Delta)) F0(t) <= F1(t) <= exp(alpha+2 Delta) F0(t)
under the specified killed-conductance and diagonal-mass log bands.
Its auxiliary conductances are explicitly reversible under fitted weights.
Local rare-rate/weight acquisition and conditional implementation errors keep
their own costs. Exact/multiplicatively controlled safe initialization, or a
minimum deadline, is essential for continuous-time physical relative claims.

The executed 24-component diagnostic used 2,926,345 ordinary kernel draws
at stationary failure probability 1e-24. Short paths estimated probabilities
near 1e-25; a 448-unit reverse window supported a deadline of 1e24.
Generic Karger counting is IMPORTED AND PRICED, NOT IMPLEMENTED here.
Generic whole-curve preprocessing was NOT EXECUTED: its literal conservative
allocation exceeds 1.21e15 bounded trials and 6.21e19 path updates before
additional work. The diagnostic has a 25-state symmetry quotient and an
ordinary exact finite-state solver is better for it.

next2_root/early_allworking_bridge_notes.txt supplies a completed chosen-
deadline mathematical extension for independent binary exponential edges,
with forced snapshots, component bridges, finite rational path approximation
and a late-time stationary comparison. It is not implemented; it is not a
single precomputed all-working curve or an interacting-port theorem. An
omitted common-cause rate can dominate arbitrarily early all-working failure
probabilities, so the equilibrium-safe implementation bound is not exported.

DIRECTORY GUIDE

Astra_Passive_Hamiltonian_Calibration.pdf : detailed standalone report.
next2_continuous_quantum/ : complete response/inverse/lower-bound proof,
                           scalar response calculations, and any explicitly
                           labelled connected-set compiler diagnostic.
next2_root/ : raw photon trajectory code and all saved runs, resource arithmetic,
              time-reversal derivation, figure code, report source, the
              all-working point-query construction, and source snapshots.
next2_reliability/ : full finite proof, acquired-model companion, executable
                     rational query primitives, diagnostic and raw evidence.
next2_alternatives/ : completed independent hardware/response review and the
                      explicitly incomplete thermodynamic route.
preserved_deferred_calibration/ : 47 files copied BYTE-FOR-BYTE, including the
                                 nested full control-speed/effusion package.
SOURCE_REGISTER.txt : primary comparison and exact governing URLs.
ENVIRONMENT.json : versions actually used.
SHA256SUMS.txt : hashes of every other included file.

REPRODUCING THE EXECUTED WORK

Run from the package root with Python 3, numpy, scipy, mpmath, matplotlib and
Pillow installed. Source counts are synthetic, not laboratory measurements.

python3 next2_root/passive_photocount_demo.py --trials 2000000 --seed 20261105 --mu 1 --iterations 8 --output next2_root/passive_photocount_results.json
python3 next2_root/passive_photocount_demo.py --trials 2000000 --seed 20261105 --mu 0.15 --iterations 8 --output next2_root/matched_photocount_results.json
python3 next2_root/evaluate_passive_resources.py
python3 next2_continuous_quantum/response_constants.py
python3 next2_continuous_quantum/connected_set_demo.py
python3 next2_reliability/diagnostic.py
python3 next2_root/make_figures.py

The generic theorem's certified arithmetic and resource caps are specified in
the proofs. Floating-point scipy matrix exponentials in demonstrations are
not silently promoted to directed-arithmetic certificates. New local timing,
deadtime and optics models must satisfy the stated bounds before using the
physical guarantee. The output source remains static for the full exposure.

PRESERVED KNOWLEDGE

All earlier full classical-feedback all-strength acquisition, separate
corrected global-budget, fixed-order parity/GHZ, finite-slew and calibration
results remain unchanged. The effusion operation retains its thin-shell
geometry, force/clearing interface and remaining exposure costs. The full
deferred first-input recovery, correlated-calibration composition, distinct
bounded-neighborhood construction and reliability operator/CDF sensitivity
results remain unchanged. Earlier incomplete proposals remain labelled;
this package supplies new completion files where a proof is now complete.

Primary existing output-learning, finite-response Lindbladian-learning,
polyspectral, static reliability, regenerative and spectral approaches are
compared in the report. Historical firstness, broad practical superiority and
civilisation-changing deployment have NOT been established. The completed
objects are conditional constructive theorems with explicit acquisition and
execution bills, plus the limited implementations stated above.
