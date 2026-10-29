# Strong qubit endpoint comparator and budgeted direct learning

28 October2026. Author derivation and reproducible numerical/sampling pilots; independent review pending. The oracle is standard qubit-channel theory, not an Astra novelty claim. Original storage files are unchanged.

## Full-CPTP final-decoder oracle

Let a trace-preserving qubit endpoint channel have affine Bloch form r↦Ar+t. Let a candidate CPTP final decoder have form r↦Br+u. The entanglement fidelity with the identity for maximally mixed input is

    F_e(R∘N) = [1+Tr(BA)]/4.

Neither translation enters this objective. A source-informed oracle may inspect A; an operational learner may not.

**Why a unitary decoder attains the full CPTP optimum.** Let S be qubit spin flip, S(r)=−r. Although S is not completely positive, S∘R∘S is CPTP whenever R is: if R has Kraus operators K_i, the conjugated map has Kraus operators σ_y K_i* σ_y. Its affine data are (B,−u). Averaging it with R gives a unital CPTP decoder (B,0), with exactly the same objective. Every unital qubit CPTP map is a convex mixture of unitary channels. One elementary proof brings B to diagonal form by proper input/output rotations; complete positivity then gives the four nonnegative Pauli-channel probabilities. Therefore a linear objective over these decoders attains its maximum at a unitary channel.

This conclusion agrees with Theorem1 of V. Karimipour, F. Benatti and R. Floreanini, *Quasi inversion of qubit channels*, arXiv:1909.06118v5 (2019), https://arxiv.org/html/1909.06118 . Their average-fidelity objective is equivalent to entanglement fidelity for a qubit. The calculation here uses a direct Procrustes derivation rather than the paper's separate canonical-transform remarks.

Write A=U diag(s1,s2,s3)V^T with s1≥s2≥s3≥0. The optimal proper rotation is

    B*= V diag(1,1,det(VU^T)) U^T,
    F_e^* = [1+s1+s2+det(VU^T)s3]/4.

When s3=0 the orientation sign has no effect on the optimal value. This optimizes over **all** CPTP terminal qubit decoders, not merely a selected unitary family. It does not optimize the per-round control schedule, initial code, extra quantum memory, or joint multi-site processing. The physical final unitary's synthesis/error/time remains a one-off interface.

The program verifies identity, rotations, complete erasure, dephasing, and universal-NOT-channel examples and challenges the oracle with10,000 independently generated random CPTP decoders. Those finite tests supplement the proof, rather than prove global optimality.

## Correction to interpretation of the first endpoint-fitting pilot

`oracle_and_endpoint_fit_v1.py/.json` evaluates the above oracle for the prior ideal-idle baseline and available clocked baselines. Its optional fitted endpoint pilots retain the already acquired inverse **inside every round**. Consequently their stated20480/102400 native-use endpoint budgets are **additional endpoint acquisition**, not the total cost of a new standalone method. The pre-existing selected inverse used4096 shots/site, and the full original pilot consumed102400 calibration exposures and2068480 total physical-noise exposures including holdouts. None of those earlier costs is erased.

Those version1 files are retained verbatim as useful additional-calibration diagnostics. They must not be cited as proving an equal-total-budget direct endpoint method. The correction is interpretive, not a change to their simulated channels or sampled counts.

## Standalone alternative: no learned inverse inside rounds

`direct_endpoint_no_per_round_inverse_v2.py/.json` instead uses the raw stationary native channel at every step and **no acquired per-round inverse**. A horizon-specific terminal unitary is learned directly from ordinary endpoint experiments. No previous frame training or oracle channel parameter enters the fit. This is a genuinely different conventional mechanism and avoids silently granting inherited calibration for free.

The source generator applies the chosen endpoint channel to±X,±Y,±Z preparations and simulates ordinary X/Y/Z binary measurements. Settings receive balanced allocations. The estimator sees only the18 pairs of counts, estimates each Bloch entry by the difference of the matched±preparation empirical means divided by two, then applies proper Procrustes. Source truth is used only to generate Born data and score the resulting fixed decoder. The true simulator score is not a statistical confidence certificate.

All five sites, T∈{1,8,32}, and the two budgets are fixed in `DIRECT_ENDPOINT_PLAN_v2.json` before this pilot's draws. There is no favorable-site selection, seed search or source-informed correction of the fitted matrix. Each listed pilot is a separate counterfactual experiment; their combined costs exceed any one budget. No high-fidelity hypothesis test is claimed.

For a total calibration budget B native-source uses across five sites, each receives

    N_endpoint = floor[B/(5T)] shots,
    actual native uses = 5 T N_endpoint ≤ B.

At T32 this is128 endpoint shots/site for B20480, and640/site for B102400. Longer horizons cannot be called equally cheap merely because the number of final readout bits is small.

## Clock costs

For the default clock, native plus control phase is2 reference units and the EC-equivalent background window is201; each endpoint shot at horizon T therefore occupies203T reference units, before endpoint preparation/readout and final recovery-pulse time. The alternative identity per-round control replaces the learned inverse but retains the declared native/control phase duration; the separate background model is the one specified by the clocked parent calculation, not an invented continuous-time relation to native noise.

The results report both aggregate qubit-channel elapsed acquisition time and an ideal five-site-parallel acquisition time. The latter assumes all five experimental sites operate simultaneously. These are not measured laboratory wall-clock costs. For a different measurement/feedback-duration scenario, the corresponding clock window must be substituted. Endpoint preparation/readout and final-pulse overhead remain separately uncharged rather than concealed.

Equal native exposure budgets do **not** imply equal wall-clock calibration time, equal total control count or equal hardware resources. The oracle is source-informed and infeasible without knowledge; sampled direct endpoint fitting is operational in the declared model but needs horizon-specific data. The code-based architecture instead acquires local frames once and can reuse them across horizons. Neither advantage is promoted beyond these interfaces.

## Consequential baseline change

The former fixed-control unencoded infidelities0.382–0.910 at T32 are not the best possible terminally corrected unencoded memories. The same endpoint channels admit full-CPTP final-oracle infidelities0.14308–0.21171. Any storage comparison must retain this much stronger benchmark. Whether the physical clocked code beats a given oracle/scored direct learner is a separate numerical comparison, not evidence of a new code or universal superiority.
