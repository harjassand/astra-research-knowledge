# Independent audit: noncommuting-spectator sampled recovery pilot

28 October 2026. **PASS for reproducible simulated acquisition, recorded floating comparisons and actual receiver scoring, at the versions bound in the receipt.** This is not receipt of a successful statistical acceptance test, exact interval SDP, rational compiled control, hardware experiment or broad practical advantage.

## What was executed and independently checked

The source is one fixed qubit-to-two-qubit CPTP channel. It mixes two amplitude-damping orientations correlated with noncommuting emitted gauge states and applies a fixed dense hidden output mixer. It is not a simulation of a time-evolving retained-memory process. The learner's numerical routines receive only the count-derived signed contrasts and independent optimizer seeds. True V, gauge states, damping parameters and exact channel contrasts enter only the source generator and post hoc/noiseless scoring. No private-source leakage into fitted candidates was found.

All 12 raw banks replay exactly from the saved seeds: 344,064 individually RNG-simulated setting/outcome draws, one logical preparation and two output Pauli measurements per block. There are 688,128 simulated output readouts. The three N values are fresh banks rather than prefixes. Count tensors contain the complete sufficient sampled records used by these learners. Replaying them is not new acquisition or additional statistical evidence. The physical Born law, source Choi positivity/trace preservation and expected shadow contrasts were checked independently to floating residual at most 1.12e-16; the source's analytic Kraus construction is CPTP.

The original result binds the preserved `run_pilot_before_sdp_rounding.py`. The current program adds only an optional return of the fitted recovery Choi matrix. Convex rounding reuses the original raw banks with zero new source calls. Both program versions and their adverse outcomes remain intact.

## Objectives and physical operations

The unitary search evaluates only an empirical objective. Its commutator gradient is the derivative of that objective under actual unitary conjugation. Each candidate is a physical Pauli triple up to floating arithmetic, regardless of whether a local optimization convergence flag is reached. A small gradient/local fit is not a proof of a global optimum. In the independent rerun only 6 of 48 starts reached the numerical gradient tolerance; iteration-limited or otherwise stopped starts remain reported.

For a TP decoder with unnormalized output-first Choi J, the full-CPTP empirical objective is Q=sum_j sigma_j tensor C_j^T/4. Bell fidelity equals 1/4+Tr(QJ); hence the reported loss .75-Tr(QJ) is correctly normalized. The input-independent affine contribution is constant by trace preservation, so the three signed contrasts are sufficient for this objective. This conventional decoder sees the same information and source budget as the proposed inverse search.

The primal TP correction, small identity shift and normalization are algebraically correct. The dual is I_2 tensor Y>=Q with objective Tr Y. The observed minimum eigenvalues, TP residuals and primal-dual gaps are numerical checks, not directed-rounding certificates. In the ORIGINAL sampled runs all 12 primal success flags were true but only 2 of 12 dual success flags were true. The repaired numerical gaps were nevertheless at most 1.52e-7. These flags must not be hidden or relabeled as twelve successful exact SDP solves. Our independent optimizer rerun had a maximum numerical gap 2.21e-7.

The recovered adjoint images use the correct Choi transpose/order. Rounding first takes a reflection X, then the X-odd part of the Z image and its sign, and sets Y=iXZ. The nonzero odd gap and anticommutation make this a physical Pauli triple in exact algebra; the saved numerical triples satisfy the stated small residuals. Scoring uses the literal three-controlled-reflection unitary and mixed receiver ancilla. No arbitrary unital CP image is silently treated as a unitary gate.

The virtual worst-gauge score is computed from the correct gauge effect. It is a post hoc Bell/reference diagnostic using the known simulator V, not a learner-observed certificate or a demonstrated complete-memory service guarantee. No unknown payload was sampled.

## Replay precision and an additional reproducibility correction

All integer banks reproduce exactly, but unconstrained floating optimizer reruns did not reproduce every reported score to a strict 1e-11 tolerance. In our rerun, differences reached 8.14e-8 for native/variational scoring and 9.14e-7 for rounded receiver scoring. The original instructions use single-threaded BLAS; our independent rerun used the environment's default setting. More generally the eigensolver/optimizer's last digits and selected near-optimal candidate are numerical, not exact artifacts. The failed tight-score replay is preserved explicitly in the audit metadata, rather than tightening a conclusion around it.

The author then preserved a separate SAME-BANK refit with its actual numerical U, contrast matrices, recovery Choi matrices and rounded controls in `replayed_models.npz`. This does not replace the original results or add source data. `independent_rescore_saved_models.py` reconstructs physical receiver Kraus operators and computes fidelity by Kraus trace composition, independently of the original matrix-unit scorer. It checks 65 saved decoder-method instances across all 12 banks, matching their saved native/worst-gauge scores within 1.0e-15 WITHOUT optimizer re-execution. These saved matrices now make the audited numerical receivers directly reproducible. Our own numerical rerun controls are separately preserved and explicitly labeled as such.

## Findings and limits

On this one source, rounded convex recovery and the four-start unitary search approach native Bell loss .19 as the source budget grows. The equally informed full-CPTP decoder achieves essentially the same native scores. At N=65,536, mean rounded native loss is approximately .190674, not an improvement over that strong conventional decoder. The proposed usefulness is examining/rounding a recovered algebra and its virtual gauge behavior, not demonstrating a superior native optimizer.

Raw signs, scalar common-factor whitening and operator whitening have persistent noiseless biases outside their respective hypotheses. Operator whitening also rejects seven of the eight smaller-budget banks due to nonpositive empirical operator Gram matrices. These are useful mechanism failures and are preserved. They do not prove those methods fail under their own stated source classes.

Most importantly, ALL 12 proposed uniform-inverse confidence tests fail target delta=.1. Independently recomputing the later quadratic native-oracle guard also finds ALL 12 fail the .01 regret target; the largest-budget bounds remain above two before clipping. Small scored error and positive floating fitted gaps do not override the conservative statistical allowance. No exact rational controller or physically accepted accurate decoder was established by this pilot.

The audit therefore receives the raw-record execution, source/learner separation, ordinary comparator, physical scoring mechanism and numerical observations at their stated scope. It does not receive a successful confidence certificate, hardware result, useful threshold, generic scaling claim or advantage over the best equally informed adaptive method.
