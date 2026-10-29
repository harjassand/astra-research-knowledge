# Final acceptance: robust observable proof and executable

29 October2026. Actual internal review completion. This addendum closes the
specific executable-validation gap recorded in ROBUST_OBSERVABLE_PROGRAM_REVIEW.md.
It does not add an external, formal, hardware or historical-priority endorsement.

## Accepted versions

* ROBUST_OBSERVABLE_PROGRAM.md:
  `5d6a08a91361f611ae2b36e5a91230bd262fb277c1854e9d86e0c509b818b440`
* check_robust_program.py:
  `83b6c629f20187609b26b32a97dfff60a9e784d0d93e021babcc62e96249fc75`
* Result JSON:
  `c0325af374f3d41e3f869a218a2514535be4c1c9dfe8e35961ec956cb4c55b2e`
* Patched signed-continuation proof remains accepted at:
  `658fc39e1a991ab34669cd702b37b8cf93216b2ca7fa35d2fd52d54d2cbafb2a`.

Exact snapshots and the replay receipt ROBUST_PROGRAM_REVIEW_RERUN.json are
preserved in this directory.

## Verdict: ACCEPT at the stated ideal-model/statistical interface

The robust proof now explicitly uses the average CONDITIONAL initial
Wasserstein distance in its general joint old-record extension. It retains
the correct zero initial distance for the same-start comparison and upper
bound1 for preparation. This resolves the only scope clarification requested
in the preceding review. No further correction was needed.

I inspected the complete executable, ran it independently at its prescribed
seed, and then unpacked every saved calibration array. All800000 synthetic
flip increments, their eight block hashes, their saved counts and the final
post-calibration state(0,0,0,1) agree. The declared initial states and call
ordering reconstruct the corresponding endpoint readouts from these packed
flip records. No reset to an assumed clean starting state is silently added
after calibration.

The estimator uses only the generated visible counts and the warranted
clipping intervals. True H values are used by the synthetic source and by
separate population-model verification; they are not used to select the
fitted mixture weights. Fitted low/high mixtures and nearest-dyadic rounding
are computed by Fraction arithmetic. The rounding error is checked exactly
against2^(-17), stronger than the governing conservative2^(-16) allowance.

The full fitted16-state matrix is stochastic and has a strictly positive
stationary vector obtained by an exact rational solve. Its stationarity is
checked exactly, as is the ideal target's stationarity. The256 configuration-
pair checks validate the ideal receiver's one-step Hamming contraction; its
maximum ratio is exactly rho. The64 local mean-equation checks also pass.
These checks concern the complete four-site fixture. The general conditional
and arbitrary-hidden-state claims continue to rest on the written proofs.

The all-deterministic-times bounds use the analytic calibration/rounding
certificate, not the unusually small realized population errors:

    magnetization: 0.05608221278901067,
    bond correlation: 0.09216442557802135.

The bond failure contribution correctly uses oscillation2. The replay also
reports stationary TV0.00031263385973400424 and stationary bond error
0.00023738104166040825; these are population calculations for the chosen
synthetic hidden vector and fitted data, not stronger confidence certificates.
Numerical transient curves through1000 steps are supplementary checks, not
the proof of uniform-in-time validity.

Calibration costs are800000 native calls,800004 endpoint reads and four
persistent devices. Deployment uses one or two native calls,16 fair selector
bits and, for this four-site uniform scan, two additional site-selection bits.
The exact fitted kernel averages those literal dyadic choices; the script
does not purport to run a hardware controller or simulate every later native
trajectory.

The retained limitations remain material: floating PRNG generation and
displayed logarithms are not outward-rounded metrology; physical execution
error is set to zero only in the ideal model; actual boundary timing,
isolation, sensors, clocks, actuators and implementation error still require
physical warrants. The confidence statement is frequentist over calibration,
not conditional assurance after arbitrary rare-data postselection. Complete
long-record TV and random-wall-time accuracy are outside the accepted receiver.

No remaining error was found in this requested final review.
