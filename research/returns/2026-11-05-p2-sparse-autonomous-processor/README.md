# Sparse autonomous quantum processors under Pareto bursts

For ambient dimension `d>=2`, Pareto radius exponent `alpha>d+1` and `r=alpha-d>1`, the supplied report derives matching polynomial exponents for retaining an unknown reference-entangled qubit through horizon `T` at one fixed sufficiently small positive burst intensity. It uses static sparse patterned hardware and the same synchronous constant-depth local channel each tick. All mutable data, controller, program, counter, vote, flag and I/O records receive the declared corruption model.

| Charged resource | New upper scaling | Matching lower exponent |
|---|---|---|
| Installed registers | `T^(1/r+o(1))` | `N=Omega((lambda T)^(1/r))` |
| Device diameter | `T^(1/r+o(1))` | `L=Omega((lambda T)^(1/r))` |
| All-register time, including idles | `T^(1+1/r+o(1))` | `U>=NT` |

The error target is fixed and nontrivial, at most `1/4`, and delivery occurs at a declared tick `t_T=T(1+o(1))`. Raw input and output retain an `O(lambda)` error floor. The new register and work exponents improve the preceding dense reusable construction; its diameter exponent was already attained. Matching exponents do not assert matching constants or practical thresholds.

**6 November continuous-time converse:** [P2 now proves a linear-hardware timing/readout cost](../2026-11-06-p2-autonomous-local-readout/README.md) for bounded-strength time-independent local Lindblad dynamics delivering an unknown qubit at a fixed compact port at a predetermined late time. The proof grants known/perfect startup and is separate from arbitrary-junk restart. It includes coherent terms via actual-source replacement noise, but does not construct clock repair, a matching processor or a completion-event receiver. This accepted synchronous construction and its resource exponents remain unchanged at their stated scope.

## Governing proofs and reusable machinery

| Read | Role |
|---|---|
| [New report and proofs](package/report.txt) | Model, sparse compiler, matching lower bound, requested handoff, restart theorem, full costs and comparators |
| [Accepted reusable predecessor](package/accepted_reusable_report.tex) | Complete preceding reusable processor and actual-source strong compiler, imported at its original scope |
| [Sparse execution and resource limits](sparse-execution-and-resources.md) | Live-register compiler, fixed-intensity asymptotics, known noisy commissioning and full accounting |
| [Restart and quantum handoff](restart-and-requested-handoff.md) | Stronger arbitrary-junk contract, causal selection and finite raw exchanges |
| [Original ZIP](original/sparse_autonomous_processor.zip), [package guide](package/README.txt), [member manifest](package/MANIFEST.json) | All eight original members, with seven supplied member checksums |
| [Recovery return and activity](P2_INTERRUPTED_RECOVERY_9952_20261105_RETURN.txt), [source map](SOURCES.json) | Exact supplied recovery assignment, human continuations, interrupted activity and available response |

The original ZIP and every member are unchanged. The included accepted predecessor is retained as machinery, without a new proof requirement. The new report calls these research derivations rather than previously published or independently peer-reviewed theorems. The recorded finite checks test adapter and transaction identities; they do not simulate the complete physical code or measure a threshold. Capital did not execute them.

## Model and consequence

Poisson marks have intensity `lambda dx dt nu(dR)` and tail `Pr(R>=u)=u^-alpha` for `u>=1`. Each mark permits arbitrary joint CPTP corruption inside its spatial region; fault values may share an environment and memory. The sparse memory result retains that generality of fault values. Geometry has the declared independent Poisson source sets. Marks cause instantaneous spatial damage; persistent damage would be a changed model.

The finite layout is input-independent and can depend on `T`. It has bounded degree, local dimension, register density and interaction range. Static wiring, patterned immutable update laws and synchronous ticks remain premises. Known controller words require actual noisy product writes over a horizon-dependent prescribed region, with distributed spatial access and cost. Only the unknown input seed is fixed and compact. Sparse positions are absent hardware rather than free mutable vacuum cells.

Autonomous quantum processing itself is established prior machinery. The report's direct QCA comparator has stronger translation symmetry and different local-noise assumptions. Pareto damage does not directly satisfy an exponentially small specified-fault-set condition; preservation of the completed Poisson-source compiler under sparse execution is the supplied compatibility bridge. No thermal, asynchronous, translation-invariant, fabrication, energy-optimal or experimental realization is inferred.

The [separate continuous-time noisy-controller dossier](../2026-11-05-autonomous-quantum-correction-opening/README.md) retains its open global gate-order/protected-idle theorem. Fixed synchronous patterned execution here does not establish that different operating contract. Earlier Gibbs results are unchanged.
