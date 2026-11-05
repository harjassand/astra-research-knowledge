# Transient excitation must be priced in signed complete catalytic cycles

The source supplies finite pulse/renewal constructions, an exact Poisson performance-difference identity and a reversible 72-state model. Read the [main narrative](package/next_science/research_report.txt), [full-cycle source](package/next_science/observation2/WHOLE_CYCLE_RESULT.txt), [transfer checkpoint](package/next_science/transfer/CATALYSIS_FULL_CYCLE_CHECKPOINT.txt) and [complete model](package/next_science/invention/CATALYTIC_FULL_CYCLE_CONSTRUCTION.md). All material numbers below are **conditional synthetic inputs**, not an acquired catalyst generator.

An assumed exponentially decaying barrier reduction gives integrated excess rate multiplier `I=tau[Ei(c)-EulerGamma-log(c)]`, `c=DeltaE0/kBT`. At `.192 eV`, 298 K and 41 ns, I is about 11.5311 microseconds; a specified maximum-height rectangular envelope gives 72.3841 microseconds. These are excess exposures, not excitation lifetimes or net added products.

For an irreversible serial cycle with a valid integrable pulse envelope, no superadditive overlaps and received-event rate nu, the exact occupancy ledger bounds `J/J0<=1+nu I`. If productive donors additionally ensure `nu<=m J`, then `G<=1/(1-m J0 I)` when the denominator is positive. This already allows favorable timing and does not assume independent Poisson arrivals. It depends on the **productive donor budget**: gross reversible adsorption can be far larger than net turnovers.

A supplied reversible recrossing counterexample defeats exporting that serial rule from total affinity alone. The same pulse's signed extra production differs by roughly a thousandfold between an unconditioned stationary start and a reaction-ready state. Autonomously producing that readiness correlation needs actual dynamics and reverse/work accounting; a prescribed state selector is not free.

For general baseline Q0, signed increments d, reward r0 and current J0, solve `Q0 h=J0-r0`. A finite perturbation followed by full relaxation has extra expected product

```text
integral sum_ij p_i(t) delta_q_ij(t)
         [d_ij+h(j)-h(i)] dt.
```

The bracket includes future loss or gain; counting only positive immediate reactions can be wrong. Parallel channels and signed reverse counts remain separate. This is established Markov reward/performance-difference machinery, not a new chemical law.

The two-site six-stage/binary-mode model has 72 states, mass-balanced chemistry, thermal reverse switching and chemical channels satisfying local detailed balance. Capture **replaces** its ordinary channel rather than adding free energy. At other forward rates 100/s and 41 ns, one pair-current change is only about `1.7593e-8/s`, despite a positive capture-ledger term about `3.23971291445/s`; the replaced ordinary path contributes almost its negative. Omitting that term creates spurious gain. Faster synthetic chemistry and longer lifetimes produce different gains but do not fit the reported slow/nanosecond material regime. A weak-binding stress case retains gross adsorption over a million times net turnover and a slowdown.

The independent renewal calculation propagates gate state through each chemical phase, including arrival readiness and residence, instead of using one global hot fraction. The [72-state results](package/next_science/invention/catalytic_cycle72_results.json), [signed-response record](package/next_science/transfer/catalytic_cycle_response_results.json), [renewal results](package/next_science/observation2/full_cycle_renewal_results.json) and [gross-activity stress](package/next_science/transfer/reversible_source_stress_results.json) retain all variants. High-precision stationary, equilibrium, energy and entropy checks were producer executions, not Capital reruns or empirical fits.

Thermal excitation is a real competing path, not an always-cold default. Single-edge positive-observable sensitivity has known tree-theorem bounds, but signed net currents near stall, multiple perturbed edges and joint donor/recipient transitions need their own ledger. Excitation energy is not automatically thermodynamic free energy, and a source annotation is not a measured bath lifetime. [Thermal competition and limitations](package/next_science/root_construction/catalysis/THERMAL_COMPETITION_AND_SCOPE.txt). No mechanism identification, universal kinetic exclusion or practical breakthrough is claimed. [Original package and hashes](SOURCES.json).
