# Root main receiving: joint growing-selector and decoder learning with retained memory

2026-10-28. **Scoped PASS** at source SHA256 `ead2aaf47370e5fa0882cf90802325e0c914b8d25cbb05f86981f91a02cd6d4e`, `ordinary_joint_selector_decoder_prequential_20261028.md`. The separate statistics receipt is complementary, not presumed by this note. No source samples, practical advantage or hardware evidence are added.

## Load-bearing construction

1. The source's full CP instrument assumption, fixed unknown U and CP-order identity dominance imply that the same D_* is full-CPTP optimal for every current memory state and every real selector. This is a supplied structural property, not learned from the probes. Its decoder excess is a nonnegative real quadratic in x. Therefore its largest eigenvalue is bounded by its trace, giving the exact factor-m anchor domination. No positive generator contrast or gauge eigenvalue floor is inserted.

2. Each query role samples fresh coins after the same pre-call classical history. The factor-two role weights therefore provide unbiased estimates of two DIFFERENT objectives: uniform-anchor decoder mismatch and the selector effect for the frozen current decoder. Correlation of current output records with retained quantum memory changes later histories but not this conditional calculation. The fourth-design sampler uses actual return bits; the decoder role uses actual local output Pauli outcomes. Neither is an expectation oracle.

3. Separate feasible projected-gradient regrets combine by adding and subtracting the actual current decoder at a fixed comparison selector. The positive excess matrix supplies the missing uniform transfer. The result compares with the best FIXED real selector and the common pointwise-optimal decoder on the controller's actual mixed-probe occupation. It does not solve generic joint nonconvex optimization, dynamic-selector regret or counterfactual-policy regret.

4. The one-terminal payload channel is exactly the mixture over private T, preceding two-role histories, and the current rational selector ensemble. Before T no future datum has interacted with the source. Equality is at the channel level and preserves a reference initially independent of source memory and acquisition randomness. Same physical port, role/timing privacy, trusted holding and isolated output remain real requirements. This is not a future-decoder certificate.

## Finite controls and constants

Reviewed the selector PSD/trace repair directly. The trace correction is at most delta in trace norm; its corrected matrix has norm at most 1+4m delta, and the final positive mixture changes it by at most 9m delta. The source's 10m delta bound and delta allocation leave ample objective slack. The Choi projection uses the received finite solver/repair contract only, not its iid acquisition theorem.

Independently verified the final denominator clarification. A solver grid denominator Q and delta=1/(65536mN^2) yield a repaired selector common denominator dividing K=mQ(65536N^2+3). If B=KX and a_i are its leading principal determinants, unit-diagonal LDL columns have entries with denominator a_i, while pivots are a_i/a_(i-1). Thus each ensemble weight denominator divides K a_(i-1)a_i, and J=K a_m product_(i<m)a_i^2 is a common sampling denominator. Hadamard bounds J<=K^(m^2+1). The claimed pre-outcome random-bit cap and paid O(m) amplitude preparation are therefore genuine; no eigenbasis or logarithmic-in-m state synthesis is assumed free.

Both convex sets have squared center radius at most one and diameter at most sqrt(2). The two gradient bounds and received approximate-projection argument give the stated 4G0 sqrt(N), 4m^2 sqrt(N) regrets. Multiplication by 3/2 and factor m yields 6(m^2+mG0)/sqrt(N). The least-power-of-four horizon gives N<576(m^2+mG0)^2/epsilon^2 and the displayed d^5 expansion. Complete implementation error is charged once against the declared ideal-controller occupation; it does not move the comparator to new imperfect histories for free.

## Independent physical checks

`joint_selector_root_check_20261028.py/.json` constructs 24 complex CP selector/gauge sources, selector dimensions 2,3,4 and output dimension 4, with noncommuting memory/gauge operators. It verifies the physical Bell-block comparator, the PSD excess quadratic and trace domination, and the actual six-state/fourth-design moment. Random, exact-oracle and near-oracle decoders are included. Largest residual is below 1.4e-15; tiny negative numerical eigenvalues occur only at zero-excess roundoff scale. These are independent deterministic algebra checks, not sampled learner execution.

The explicit noisy-anchor example is correct: a perfect selector coexists with uniform-anchor oracle loss (3/4)(1-1/m). A first-order bound on raw noisy anchor loss cannot be substituted to claim fast excess. The accepted result honestly retains epsilon^-2. The separately audited adverse N512 bandit pilot is different evidence and provides no practical advantage for this construction.

No correction requested to the frozen final source. Original pre-clarification bytes and all received predecessor theorems remain intact.
