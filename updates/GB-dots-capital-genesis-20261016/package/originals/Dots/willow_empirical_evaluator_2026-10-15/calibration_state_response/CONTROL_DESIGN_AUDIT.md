# Calibration input-control design audit

## Finding
The 50,000 r13 shots contain **10 distinct 25-bit sweep configurations, each used exactly 5,000 times**. In stored row order, configuration k occupies indices [5000k,5000(k+1)) for k=0,...,9, with no recurrence elsewhere. Adjacent configurations form five bitwise-complementary pairs: (0,1), (2,3), (4,5), (6,7), (8,9).

These are facts about **file indices**, not evidence of wall-clock acquisition chronology. The data do not constitute 50,000 independently randomized 25-bit preparation frames. Whether the ten patterns were originally sampled randomly, and how acquisitions were interleaved or subsequently sorted, are not established here.

## Exact design algebra
Let S be the 10-by-25 matrix of unique configurations over GF(2), ordered by first file occurrence.

- rank(S) = 6.
- rank([1 | S]) = 6; affine span dimension = 5.
- dim ker(S) = 19: every linear parity has 2^19 different masks giving exactly the same values on the observed support, including itself.
- dim ker([1 | S]) = 20, including affine relations.

The JSON includes all unique configurations, frequencies and file runs; exact nullspace bases with bit indices; and verification that every reported basis vector maps to zero. This identifies equivalence on observed support, not equivalence for all possible preparations.

## Concrete alias of the strongest determined tag
The original parity is w=e22+e23. Its values on configurations 0,...,9 are:

1, 1, 0, 0, 0, 0, 1, 1, 1, 1.

Thus its tag0 and tag1 counts are 4×5000=20000 and 6×5000=30000. There are ten distinct minimum-weight alternative masks (all weight 2), each verified identical on all 50,000 actual sweep rows:

(1,13), (4,13), (6,23), (7,9), (7,16), (11,23), (12,13), (14,24), (17,19), (20,21).

For example, e1+e13 has exactly the same tag as e22+e23; their difference e1+e13+e22+e23 lies in ker(S). No weight-0 or weight-1 alternative exists. These are algebraic aliases of the preparation covariate, not claims about noise independence or competing physical mechanisms. The actual stabilizer circuit still identifies the ideal q49 check sign as e22+e23; the finite observed design cannot identify which preparation features explain the observed error-rate variation.

## Source documentation
The supplied dataset README's “sweep_bits.b8” section identifies sweep bits as initial data-qubit 0/1 configuration choices that turn conditional X instructions on or off. Its decoding-pathway description identifies 13-cycle data as calibration used in joint RL-prior optimization. Reading the complete README found no description of how preparation configurations were selected/randomized, how shots were batched/interleaved, or whether stored row order corresponds to acquisition chronology. Such claims must remain unknown, not invented.

Source: measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/README/README.md. Exact hash is recorded in control_design_audit.json.

## Qualification of the prior Fisher results
The measured rates, contingency tables, and arithmetically computed Fisher p-values remain unchanged. They describe pooled association for the observed ten-configuration mixture. A small p-value does not identify a local check-sign causal effect, distinguish aliased parities, or establish performance on unseen preparations. Configuration-associated gates, readout, other preparation features, or acquisition-batch conditions could account for differences. File contiguity alone does not establish drift.

Shot-level Fisher inference requires its sampling/exchangeability assumptions. Repeating each configuration 5,000 times does not by itself invalidate independent-shot testing of the fixed sampled mixture, but does not supply 50,000 independently randomized preparation assignments either. If unobserved shared batch effects or shot correlations exist, shot-level p-values can overstate inferential strength. Bonferroni controls multiplicity of the defined family under valid component tests; it cannot repair confounding or pseudoreplication. The design alone does not justify replacing the effective sample size by ten, because acquisition structure and correlations are unknown.

The observed-gauge-proxy tests use within-shot measured tags rather than deterministic sweep parities, so this exact parity-alias argument does not directly equate those proxy tags. Nevertheless, their pooled associations can still be influenced by configuration mixture and noisy-proxy effects. No additional outcome tests or stratified analyses were performed in this control-only audit.

These results cannot justify causal state-feedback interventions or claims of generalizable decoder gains. They can motivate a separately specified, independently evaluated predictive model or a properly randomized control experiment, subject to new authorization and a frozen design. There is no standalone RL-DEM refutation and no quantum-mechanism conclusion.

## Deliverables and scope
control_design_audit.json contains the exact audit; audit_controls.py is the own-code reproduction/check. Only r13 sweep bits and source README were opened by that script; it reads no raw measurements, detector events, observables, r50, reserved, or diagnostic arrays. No further outcome hypothesis tests, fitted decoder, or held-out access occurred.
