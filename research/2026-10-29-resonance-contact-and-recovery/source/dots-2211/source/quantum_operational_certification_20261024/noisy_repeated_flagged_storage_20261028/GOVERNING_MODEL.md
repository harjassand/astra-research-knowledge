# Actual coherent-noisy flagged EC reused between native channel rounds

28 October2026. Deterministic numerical channel construction; independent review pending. No new sampled acquisition, experiment, threshold or novel-code claim.

## Data and source provenance

The fixed inverse on each of the five physical sites is taken from the received `five_qubit_acquired_frame_pilot_20261028/models.npz`, using its already selected **4096 calibration shots per site** model, not an oracle inverse or a new fit. The full earlier pilot tested both4096 and16384 and includes its own calibration/holdout costs; none is rerun here. The learner remains source-blind. This calculation, as scorer, imports the same stationary non-Pauli/nonunital native Kraus sources from `code_and_channels.py`. Source SHA256s are in results. Each source is an oriented amplitude-damping channel followed by its stationary physical frame. The acquired onsite inverse is reused unchanged every round. Its implementation is ideal apart from the already existing learned-frame misalignment; no additional inverse-gate synthesis error is silently included.

Native noise on the five sites is a tensor product, and source environments are freshly discarded each round. This is a closed finite-tile Markovian CPTP model, not a hidden bath, leakage, drifting source or nonlocal crosstalk model.

## Actual EC instrument

The physical flagged circuit is the received Chao–Reichardt-derived implementation with H/CX/H parity decomposition, early exit after first flag/nontrivial syndrome, one fresh full unflagged pass, and physical conditional Pauli correction. It does **not** decode/re-encode between rounds. For each check, the program constructs its full6- or7-qubit unitary, projects the prepared ancillas and measured outcomes into32×32 data Kraus operators, then composes the actual adaptive branches. There are193 branch Kraus operators for the declared pure/coherent model. Records are discarded after their correction has physically acted; old records cannot affect later controls.

**Total controller completion:** the original one-fault flag tables contain8 of16 syndromes. When actual multi-fault noise produces an undefined flag/syndrome pair, this simulation uses the ordinary minimum-weight Pauli correction. This choice is fixed, deterministic and trace preserving; it is not postselection or evidence-dependent tuning. It leaves the checked zero/one-fault behavior unchanged. Other total completions can differ at higher order and are not asserted equivalent.

The coherent control model is fixed in time, with one signed angle eta reused at every declared noisy operation:

- after each CX, a two-qubit ZZ rotation exp(−i eta ZZ/2);
- after each H, a local X rotation;
- after each native ancilla preparation, a local Y rotation;
- before syndrome Z measurement, a local Y basis rotation;
- before flag X measurement, a local Z basis rotation;
- after each physically executed correction Pauli, a local X rotation.

Idles, classical readout, controller logic and conditional dispatch are ideal in this first control-noise family. Native |+> preparation and X measurement remain native interfaces. All positive and negative signed-angle challenges are explicitly listed in the program; no favorable sign is selected as an operational guarantee. Small favorable interference with an existing calibration error can occur and must not be interpreted as a general benefit of adding noise.

The maximum actual branch costs remain40CX,32H,12preparations,12measurements, up to3physical Pauli corrections and12readout slots, plus the declared conservative idle locations. The mathematical full unrolling has751 gate/readout/idle locations. In this specific noise family only101 potential local operations carry coherent errors (56 across flagged checks,40 across fresh checks,5 conditional correction sites). A conservative full physical diamond bound is

    ||F_eta−P||_diamond ≤ min(2,101 * 2 |sin(eta/2)|).

It becomes too loose for a useful small-error theorem well before all numerically simulated angles. Idles being ideal is a limitation, not a claim that their physical duration/energy cost vanishes. Five source uses and five acquired inverse operations are required per encoded round; unencoded site baselines require one of each per site per round. Initial code injection and the final ideal decoder are one-off assumed interfaces, not demonstrated fault-tolerant hardware.

## Physical state propagation and observable

For each of four logical Pauli input operators, encode once into a32×32 physical operator. Every round applies the five native-plus-acquired-inverse channels and the actual noisy adaptive EC superoperator. The resulting physical operator is carried unchanged into the next round. Only at each requested diagnostic terminal time T is a copy ideally decoded to obtain its complete4×4 logical Pauli transfer matrix. No such decoding modifies the ongoing stored operator.

Results include entanglement infidelity, normalized Choi trace distance, Choi positivity/trace diagnostics, physical code-space weight on maximally mixed logical input, and the difference from the **incorrect alternative** of powering the one-round decoded logical channel. The latter is explicitly a diagnostic counterfactual, not the simulated evolution. Normalized Choi trace distance is not labeled diamond distance; for a qubit it supplies a lower bound on half-diamond distance and twice it supplies a general upper bound (capped at one).

The ideal-control eta=0 implementation is checked against the full ideal EC superoperator on all physical operators, and its one-round logical channel against the original frozen pilot model. Each constructed noisy EC instrument is checked trace preserving. Numerical tolerances and exact model assumptions are distinct from a proof or statistical confidence certificate.

## Comparison and actual significance

Matched unencoded baselines reuse the exact same acquired inverse and native source at each site for the same number of time steps. The eta=0 standard-code baseline isolates control cost. This demonstrates operation of **standard flagged protection** with fixed sampled calibration and actual noisy repeated physical recovery, rather than an advantage over a strong equally informed fault-tolerant-code alternative. It is not evidence that Astra has invented a new code or experimentally beaten a laboratory memory.

The reusable advance in this package is closing an architecture/evaluation gap: retained physical syndrome leakage and coherent systematic controller errors are now present in the calculation instead of being removed by an uncharged ideal decoder after every step. Whether the numerical advantage survives a specific hardware idling, crosstalk, injection/readout and energy/timing model remains unresolved.

## Floating norm diagnostic, not outward-rounded certification

With the same193 classical branch labels, let K_j(eta) and K_j(0) be actual and ideal EC Kraus operators. Phase-align each ideal branch using the complex overlap when nonzero (zero ideal branches remain zero), and form D_j=K_j(eta)−exp(i phi_j)K_j(0). The common-Stinespring inequality gives

    (1/2)||F_eta−P||_diamond
      ≤ ||stack_j D_j||op = sqrt(lambda_max(sum_j D_j† D_j)).

The program computes this32×32 Gram eigenvalue in floating arithmetic. Phase alignment is a permitted environment unitary, not a change to either channel; no optimality is claimed. The displayed bound has mathematical justification but the computed number is **a floating diagnostic**, lacking outward rounding/error intervals. It must not be described as a certified diamond value. The native full-channel bound diagnostic sums qubit normalized-Choi upper bounds; the one-cycle logical b diagnostic uses twice its normalized Choi trace distance. These values feed the separated F N reuse formula only as a numerical diagnostic.

For provenance, the earlier complete pilot consumed102400 sampled calibration exposures and2068480 total simulated physical-noise exposures including logical and unencoded holdouts. The selected4096/site model does not erase the full pilot's costs. This new deterministic run adds zero sampled acquisition or holdout records, but evaluates many complete channel compositions computationally.
