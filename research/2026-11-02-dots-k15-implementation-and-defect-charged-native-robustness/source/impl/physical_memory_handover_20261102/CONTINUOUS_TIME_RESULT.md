# Continuous-time continuation: earned result and remaining gate

## Useful result

The private transaction mechanism now has an explicit finite Poisson service word, a contact-fault estimate in deterministic physical-time boxes, durable exactly-once guards checked over 46,656 finite states, and a dependency-path timing proof requiring no independence across siblings. These are actual finite-rate operations and estimates, not an ideal global clock assumption.

The construction is a **nonequilibrium autonomous alternative**. It does not prepare the native Hamiltonian's certified thermal basin and does not prove a scalable autonomous memory by itself.

### Earned components

1. `CONSTRUCTOR_RESULT.md`: interleaved same-code, reference-safe encoded WRITE avoids routing n separately growing blocks. Signed syndrome frames are included; the Steane instance was checked in 512 branches. Its physical residual class is local-stochastic around a sampled syndrome, not silently identified with actual joint Gibbs.
2. `TRANSACTIONAL_LOCAL_SERVICE.md`: finite private acquire-all, reversible prefix abort, commit-forward for consumed unknown payload, durable output/epoch records; explicit service word. Arbitrary small engineered contact/reset GKSL errors and coherent local V admit a fixed-time-bin fault-set norm estimate. The local graphical version combines imperfect attempt maps with bounded-neighborhood schedule failures.
3. `transaction_durable_check.py/.json`: 46,656 states verify clearing preserves durable records, fresh requests commit once, and stale/absent requests are not replayed. Does not certify global epoch wraparound or a trusted higher-level record.
4. `PRIVATE_DAG_TIMING.md`: conditional geometric service yields exponential physical-time tail O(depth + log outputs) for a valid closed DAG, despite sibling correlations. A whole-macrotransaction abort at fixed rate instead costs ((1+mu/gamma)^d-1)/mu in mean time, so only fixed-size local work may be restarted freely.
5. `async_primary_gate/`: primary synchronous/noisy-controller theorem versus continuous-time outline audited; clean finite-island asynchronous clock repair tail derived from Cook–Gacs–Winfree. Neither source was promoted to an unproved perpetual-noise local-service theorem.

## Strongest comparator and scope

[Duennweber, Styliaris, and Trivedi, v3](https://arxiv.org/html/2601.20818v3) is the relevant synchronous noisy-controller component, not a finished proof for arbitrary imperfect continuous-time contacts. [Shtanko et al.](https://quantum-journal.org/papers/q-2025-07-22-1804/pdf/) gives a complementary warning: their globally Poisson-timed decoder model can have size-independent lifetime at fixed correction rate. That restriction is not a no-go theorem for private local correction.

The same-resource active comparator receives every dissipator, reset supply, encoded record, ancilla, interaction, and control used here. It may run the identical autonomous evolution. No reliability or energy advantage over that comparator has been proved; autonomy is a scheduling capability, not free cooling.

## Actual unresolved operation

A protected recursive executor must maintain encoded request/epoch/consumed records and quantum ownership with local noisy hardware, prevent one raw physical flag from authorizing a logical operation, and let inner EC finish while an outer transaction waits. A damaged durable record cannot merely be erased: that would replay an irreversible quantum operation. A higher-level acquire/commit cannot be declared a constant-range primitive. Timing liveness of already-valid DAGs does not supply this causal/noise-confinement theorem.

For the original passive native-H target, a second distinct gate remains: prove that the physically produced extensive noisy residual state lies in a long-lived basin of the actual perturbed H, or implement a Gibbs-compatible writer satisfying the root average-output domination condition. The present local transaction and timing estimates do not establish either. No denial or unavailable hardware is blocking the analysis; these are missing mathematical construction/proof steps, and no full positive solution is claimed.
