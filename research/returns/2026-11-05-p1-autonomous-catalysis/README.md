# Autonomous catalytic energy routing: exact models and an unresolved physical endpoint

The supplied research builds complete conditional kinetic constructions for routing reaction energy into later chemistry. Its principal interpretive result is an exact matched comparison: useful routing can coexist with **thermal conditional gate populations and zero net gate-bath dissipation**, because routing removes a kinetic deficit of the disabled comparator. This does not identify the reported PtCo/calixarene mechanism or establish a new physical law or realised civilisation-scale capability.

Read the complete [research narrative](package/next_science/research_report.txt), [PDF](package/output/pdf/autonomous_catalysis_research.pdf), [exact relay construction](package/next_science/transfer/THERMAL_RECYCLING_COUNTEREXAMPLE.txt), [original program](package/next_science/transfer/thermal_recycling_counterexample.py) and [recorded results](package/next_science/transfer/thermal_recycling_counterexample_results.json).

| Distinct result | Direct route |
|---|---|
| Matched autonomous relay, physical interpretation and uncertainty bill | This page |
| Finite thermal-projection/entropy certificate and comparator repair | [Projection theorem and finite-gate algorithm](thermal-projection.md) |
| Transient energy, signed turnovers and reversible full-cycle accounting | [Pulse/Poisson/72-state results](full-cycle-response.md) |
| Acquired reversible geometry, capacity and the actual passage-time target | [Finite brackets and Poisson-target boundary](capacity-and-passage-time.md) |
| Atmospheric observations and dual-isotope inference limits | [Methane data, covariance and retained negative result](methane-inference.md) |
| Complete original material | [ZIP](original/autonomous_catalysis_research.zip), [captured return](P1_AUTONOMOUS_CATALYSIS_20261105_RETURN.txt), [provenance/hashes](SOURCES.json), [third-party notices](package/THIRD_PARTY_ATTRIBUTIONS.txt) |

## Exact relay and both physical comparators

The synthetic four-state model has chemical empty/adsorbed state and a binary energetic mode. Bath switching obeys thermal detailed balance. Captured adsorption transfers chemical free energy into the mode; a separate reversible product channel consumes it. These two parallel channels must remain **separate in the entropy/reward ledger** even when their endpoints agree. The product affinity supplies chemical work; the collapsed channel is illustrative, not a literal elementary four-electron ORR event.

With `q=exp(-E/kBT)`, bath down-rate gamma, product affinity A and `z=exp(-A)`, the exact capture-on stationary state has conditional hot probability `q/(1+q)` at both chemical configurations. Bath net flux and bath-link entropy vanish, while net captured energy `E J` supports positive product current and total entropy `A J`.

The matched capture-off system changes captured adsorption to ordinary adsorption with its proper reverse rate, leaving product and bath channels unchanged. Both systems have the **same thermally projected chemical generator and reward**. For the positive quantities D0,C defined in the full proof,

```text
J_on=J_thermal=(1-z)/D0,
J_off=(1-z)/(D0+C/gamma),
J_on/J_off=1+C/(gamma D0).
```

The on system is thermal conditionally, yet routing causally improves current by removing the off system's waiting deficit. A one-device bound on `J-J_thermal` therefore cannot alone bound `J_on/J_off`. The [two-comparator certificate](thermal-projection.md) retains both sides. This is not free energy from an equilibrium bath or a claim that all catalysts benefit from routing.

## Lifetime, lineage and actual output precision

The recorded example uses synthetic `E=.126 eV`, 298 K and chemical rates 100/s. The source's single-point excitation energy does **not** acquire this thermodynamic gate free energy. At the conditional 41 ns lifetime, gain is only `1.00000404044` and the fraction of forward products whose latest excitation came from captured adsorption is about `8.20e-6`. At a hypothetical 100 s lifetime, gain is `9855.741609`, the retained-origin fraction about `.99995`, but cold stalls average 3.76 hours. That long lifetime is not observed in the reported catalyst.

A large stationary mean gain is not inexpensive precise output. The exact Poisson variance ledger gives Fano factors about `.986` and `19137.9` in those two on cases. A single unit's **asymptotic** time for 1% relative standard error is approximately 13,621 seconds versus 8.38 years, before finite-confidence and mixing requirements. Independent parallel units trade time for proportional material/resource cost; independence cannot be assumed for interacting units. Net energy flow alone does not reveal retained-energy lineage; the construction includes a separate trajectory label observable.

## Empirical anchor and what remains unacquired

The motivating [Liang et al. catalyst report](https://doi.org/10.1021/jacs.5c15936) and supplied official supporting information describe vibration-coupled enhancement. The package acquires the abstract and SI, not the full main article, and retains the authors' mechanism as their account. Its digitization, model calculations and alternative explanations do not independently establish or refute that mechanism.

The source's `.126 eV`, 41 ns annotation and barrier values are not automatically a measured gate free-energy gap, bath relaxation law or same-potential forward/reverse generator. Readiness-conditioned capture, reverse adsorption, actual donor graph, transport, site population, solvent/potential dependence and excitation distribution remain to be acquired. Reported site-normalized and total currents differ; transport/coordination changes are not removed by fitting one barrier. [Thermal competition and scope](package/next_science/root_construction/catalysis/THERMAL_COMPETITION_AND_SCOPE.txt), [source/measurement manifest](package/next_science/observation2/SOURCE_AND_RESULT_MANIFEST.txt).

The complete [72-state reversible model and pulse calculations](full-cycle-response.md) retain canceled contributions, thermal competition and unfavorable lifetime regimes. The report also preserves primary-art challenges and early deductions that already have close predecessors, rather than renaming them new principles. [Selection record](package/next_science/SELECTION_AND_QUESTION.txt), [construction/prior-art record](package/next_science/invention/CONSTRUCTION_AND_PRIOR_ART.txt), [second challenge](package/next_science/invention/SECOND_CONSTRUCTION_AND_PRIOR_ART.txt).

The earlier [clocked-grid result](../2026-11-05-p1-clocked-grid-scheduling/README.md), complete ZIP and supplied text are retained in `package/prior_clocked_grid/`, including its failed later-week replay and original attribution. No scientific program, high-precision solve, PDF build or new Capital audit was run. The package retains its [mixed third-party licenses](package/THIRD_PARTY_ATTRIBUTIONS.txt), including CC BY-NC SI; no blanket relicensing or endorsement is asserted. Generated current retrieval is unchanged; the complete source and these pages are public directly on GitHub.
