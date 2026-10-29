# Independent high-oracle source and diagnostic review
29 October 2026. Separate from the meta-selector theorem receipt.

## Physical source algebra
The source's A_m=Pi_m U satisfy sum A_m†A_m=I and A_0†A_1=0. The complete data-memory isometry sum_m P_m tensor |phi_m> tensor A_m therefore has unit normalization, not merely normalized Bell-branch probabilities. The subsequent flag-memory unitary preserves each orthogonal Pi_m memory range, so tracing retained memory eliminates the off-diagonal Pauli-label branches for every fresh independent input and every conditional memory state. Each resulting conditional channel is genuinely Pauli-plus-flag. Its branch flag operators need not be fixed or mutually commuting.

The conservative uniform fixed-X receiver bound in HIGH_ORACLE_SOURCE_v1 is correct. There is also an exact stronger identity. For C=exp(-i kappa Z tensor Q), the Heisenberg transform of X tensor I is cos(2kappa)X tensor I minus sin(2kappa)Y tensor Q (the sign is irrelevant here). Before C each branch is the product of the real pure flag |phi_m> and its unnormalized memory state. Its flag Y expectation vanishes. Since <X>_phi_m=(-1)^m sqrt(1-c²), the correct X-outcome probability, conditional on either branch, is exactly

    h_kappa = [1+sqrt(1-c²) cos(2kappa)]/2.

For c=.2 and kappa=.01 this equals .989799972232867 for every conditional history and branch prior. Thus one fixed receiver gives this exact fidelity uniformly; the conditional full-CPTP oracle is at least this good. It is not shown equal to this value: unequal priors or flag Y components can change the optimal Helstrom measurement. FIXED_RECEIVER_TERMINOLOGY_v3 correctly prevents result-field names from upgrading the fixed receiver to an actual conditional optimum.

## Executed diagnostic inspection
The program updates from only the acquired Bell label, role, flag setting/outcome or candidate/flag outcome. Simulator conditional memory and source coefficients are used to generate the process and evaluate benchmarks, not passed into its update. Its baseline initialization, q=.25, OGD step1/128 with shadow gradient8bW, EXP3 eta1/128 and gamma1/32 agree with the declared N1024 plan. Evaluation candidate selection is independent of the currently drawn Bell label, conditional on the past. Actual flag effects update the retained memory. The source construction is intentionally different from the prior negative fixture, which remains valid and unchanged.

The source and measurement simulation are floating, with probability normalization/clipping and numerical Dykstra iterates. They are not executions of the theorem's exact rational projection/finite arithmetic contracts. The plan's approximate minute timestamp is explicitly clarified rather than presented as exact creation-clock evidence.

## Independent replay and physical checks
check_high_oracle_v1.py copies the program and its projection dependency into a temporary directory and reproduces all3,072 stored records and the complete result JSON exactly, without rewriting originals. It independently assembles the full data-memory to data-flag-memory isometry and applies it to a reference-entangled input and50 fresh mixed memory states. Direct full-state Bell/flag measurement effects agree with branch simulation to1.12e-16; the common fixed-X score agrees with the exact formula to5.56e-16. The full isometry normalization and orthogonal branch ranges are checked independently of the output JSON.

The three conditional-path average learner scores near .795/.806/.804 and meta scores .593/.579/.611 exceed the identity baseline scores .508/.492/.516 in this deliberately favorable family. These are diagnostic path summaries, not confidence statements, expected-occupation oracle estimates or proof of empirical superiority. Meta adaptation is visibly slower than the learner; no favorable source/seed selection is used to supersede the negative benchmark. A conditional flag measurement steering norm and noncommuting memory-state trajectory illustrate the model's quantum instrument, not exclusion of every classical hidden-state reproduction.

Receive the scoped physical source algebra, conservative floor, exact fixed-X refinement, and reproducible floating diagnostic. Exclude hardware, real acquisition, a statistically certified improvement, an exact implemented online solver, unrestricted unknown-noise capability and multi-payload service.
