# Retirement with finite control errors: parity and ordinary absorption

29 October 2026 (Australia/Brisbane). Root composition of the acquired
second-moment, mode-misalignment and sequential-retirement results. Detailed
proofs, exact arithmetic, actual reviews and source limitations are separate
artifacts. This is a complete-output MODEL comparison, not a device error rate.

## 1. Stronger common schedule

Use the full two-continuum schedule in `TWO_CUT_CONTINUUM_SCHEDULE.md`,
with the witness clarification in `TWO_CUT_WITNESS_CLARIFICATION.md`.
For the present extension disable ALL source-bath couplings in both control
windows [-1/2,-1/4] and [1/2,3/4]. In particular remove bath-1 use on the
second window. Source-only operations can continue. This is an explicit
change in the control schedule. The earlier schedule allowed bath 1 there
because its interaction commuted with the CORRECT bath-2 selector. That
argument is unavailable for a selector that might overlap bath 1.

Removing that coupling support only lowers the previously acquired future
exposure envelope W. The two actual smooth preparations are unchanged.
The correct-selector intermediate process has E_i<=E at each cut and
F_i^2<=W, D_i<=W/2 over the whole remaining horizon. The exact reduced
retained state, including both source qubits, surviving active continua,
references and every actual controller record, is carried through each
compiled deletion. The remaining active dynamics is still to be solved.

The complete bath starts in vacuum. The full sine coupling has norm-square
v=21/10 for its one-particle vector whenever nonzero. Before the two isolated
control windows the total source-bath actions are at most 1 and 5/2.
The separately derived graph-domain/two-annihilation-row estimate gives

    M2_1=<N_total^2>_upper=987/50,
    M2_2=<N_total^2>_upper=22449/64.                       (1)

These are TOTAL moments across both continua, not just retired occupations.
Correct and incorrect passive phase operations preserve them on every
control-replacement hybrid. The comparator's passive vacuum-dump channels
contract both annihilation-row moments, as proved in
`PASSIVE_ABSORPTION_COMPARATOR.md`; hence the same conservative envelopes
also hold on all of its hybrids. No moment is inferred from trace closeness.

## 2. Required order of comparisons

First compare the actual mode-misaligned controls to controls with the
intended fixed selectors, keeping the SAME actual phase/swap angles and,
for parity, the same coin probabilities. This is a complete joint-channel
comparison on the common full bath. All future operations contract it,
even if a later wrong selector touches a formerly targeted factor.

Only after every mode error has been replaced apply the occupied-factor
retirement theorem. The correctly aligned future operations then act
trivially on earlier retired factors except for the explicitly budgeted
source-bath interaction. This avoids discarding a factor before a later
wrong-mode operation can touch it.

For each control let its fixed actual selected space be obtained by
W_i=exp(-iG_i) with ||G_i||<=theta_i. The generator and this selector are
constant in the declared interaction picture during the isolated pulse.
This is a geometric calibration requirement, not a measured hardware fact.

## 3. Hidden parity option

At each cut use a fresh independent hidden coin with

    |p_i-1/2|<=10^-5,
    actual phase area pi+delta_i, |delta_i|<=10^-7.

The finite C1 pulse and identity branch reserve the same quarter-unit window.
The fixed-mode theorem and (1) give total mode-replacement charge

    epsilon_mode_parity <=(1+2*10^-5)
                       [theta_1 sqrt(987/50)+theta_2 sqrt(22449/64)].

The aligned schedule's exact two-cut direct-deletion allowance is
8.44541216008203629344008058088859425838e-7. This includes the acquired
occupied states, the entire remaining exposure, finite angle and coin errors;
it is not the error for full-state vacuum replacement.

For theta_1,theta_2<=5*10^-9, adding the complete mode-replacement charge
gives the total bound reported in `controlled_retirement_certificate.json`,
strictly below 9.605e-7 and therefore below the chosen 10^-6 model budget.

## 4. Conventional vacuum-dump option

Instead supply one fresh vacuum dump oscillator per cut and couple it
passively to the selected retired mode in the same isolated windows.
The area is pi/2+epsilon_i with |epsilon_i|<=10^-3, so the retained
intensity transmissivity is eta_i=sin^2(epsilon_i)<=10^-6. Dumps are
inaccessible and never return. There is no random seed and no count output.

The complete selected-mode channel preserves the exact retained marginal
and contracts retired mean to eta_i E. The accepted general occupied-mode
bound supplies

    epsilon_loss_i <= W+2sqrt(eta_i E W)
           +(1+sqrt(2))eta_i E sqrt(W)+eta_i E W/2.

The two complete mode-replacement charges, now without a coin weight, are
at most 2theta_1 sqrt(987/50)+2theta_2 sqrt(22449/64). The exact arithmetic
with theta_i<=5*10^-9 gives a total strictly below 9.066e-7, also within
the same model budget. Finite C1 coefficient peak/slew and both exact
comparison components are saved in the receipt.

This conventional construction is better on these sufficient error bounds
and needs a looser pulse-area tolerance. It spends a fresh vacuum dump and
removes occupation; parity spends two independent hidden bits and can leave
occupation unchanged. Neither resource is free. There is no demonstrated
parity hardware advantage, nor a global superiority claim for the dump.

## 5. What has become possible

The result is a finite schedule for removing occupied bath factors from a
complete correlated process model with explicit control-area, mode-selection
and timing conditions. Its uniform error survives source preparation, joint
source controls, actual intermediate records and feedback across the two
windows. The mathematical instrument can choose the mechanism compatible
with the available mode control and vacuum resources, or retain the mode
when that is better. The stronger conventional comparator changes the
mechanism decision without abandoning the scientific objective.

A general-purpose ingredient is the lift from a one-particle passive
control discrepancy to a reference-complete multiphoton channel allowance.
The full nonlinear evolution supplies the required number moments through
an explicit domain-safe action bound. This avoids an unjustified finite
photon truncation or global unconstrained channel norm when calibrating
passive controls on the reachable process.

All bounds concern the explicitly defined models and final interface.
Selected-mode access, correct interaction-picture generators, pulse delivery,
the stated calibration tolerances, fresh vacuum or independent hidden seeds,
and isolation are physical conditions still to acquire. Active-field loss,
thermal dump noise, nonlinear pump noise, source leakage, readout and new
return channels need their own terms if present. The remaining margin to
10^-6 is not evidence that these omitted channels meet it. The chosen
10^-6 budget is a test specification, not a fault-tolerance threshold.

Ordinary arithmetic uses exact fractions and directed integer roots. No
retained dynamics solver error, general discretization allowance, physical
noise rate or total computing-workload error is included by implication.
