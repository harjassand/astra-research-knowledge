# First rare event: finite joint time, terminal-state and recent-path sampling

The supplied theorem constructs a finite sampler for a **quantized joint first-event record** of a declared succinct finite rational Markov model. It permits nonreversible stationary currents and any efficiently supplied initial law. It avoids simulating a mean-lifetime-long unsuccessful path, provided rare stationary counting/conditioning, forward/reverse updates and a certified mixing margin are actually available and paid. It is a conditional computation capability, not acquisition of an unknown physical model.

Read the complete [PDF](package/Astra_First_Event_Simulation.pdf), [main TeX](package/next4_root/first_event_report.tex), [block replacement proof](package/next4_root/block_completion.tex), [finite compiler](package/next4_root/finite_compiler.tex) and [geometric-clock proof](package/next4_root/geometric_clock.tex).

| Destination | Direct route |
|---|---|
| Main theorem, actual inputs and construction | This page |
| Executed four-state paths, finite-bit clock, exact baseline and costs | [Execution and certification scopes](finite-execution.md) |
| Independent completed acquisition/preparation/intervention route | [Finite experiments and exposure obstruction](active-acquisition.md) |
| Independent completed fixed-law prediction route | [Interpolation, dimension and sharp envelope](fixed-law-prediction.md) |
| Independent stricter thermal ambiguity realization | [Fixed reciprocal mechanics and active-port equivalence](fixed-mechanics-thermal.md) |
| Complete original material | [ZIP](original/Astra_First_Event_Research_Package.zip), [captured return](P3_FIRST_EVENT_20261105_RETURN.txt), [provenance](SOURCES.json) |

## Exact model and target

The input is an irreducible finite rational CTMC Q with full-support invariant law pi, efficiently encoded states and a nonempty proper target B. Its whole ergodic continuation, including B, is supplied even though output stops at the first hit. A genuinely absorbing physical catastrophe requires such a continuation with correct pre-hit dynamics; it is not automatically a valid input.

Let `p=pi(B)>0` and a supplied rational floor `pi(x)>=zeta>0`. Choose `R>=2 max_x[-Q(x,x)]`, normalize time by R and use `P=I+Q/R`. Stationary reversal `P*(x,y)=pi(y)P(y,x)/pi(x)` must be efficiently available. In nonreversible models it is generally different from P. The additive symmetrization must have a certified gap `0<g<=1`; ordinary eigenvalue real parts of a nonnormal generator do not substitute for this dissipative bound.

The static interfaces supply relative Count estimates/confidence intervals for p and independent finite-work unconditional-TV samples from `pi(.|B)`. State weights/ratios, predicate, rational arithmetic, forward/reverse kernels and initial-law draw are supplied at their actual costs. They are not hidden free oracles.

For normalized window H and dyadic precision s, output records the rounded first time, terminal state, window-start state and chronologically ordered changes in the last H time units, with rounded ages. Physical window/mesh are H/R and `2^-s/R`. The target is the **same quantized record**; no discrete output is claimed TV-close to an unrounded continuous time. Earlier uneventful history is not printed.

With calibration confidence `1-delta`, one compiled sampler is epsilon-close in joint TV simultaneously for every exactly supplied initial law. Compilation and each draw have prescribed finite work polynomial in the succinct/access input, `log(1/zeta)`, numerical `1/g`, **value** of H, s, `1/epsilon` and `log(1/delta)`, including all static/update costs at the requested tolerances. No additional inverse-p or mean-lifetime simulation factor is introduced. An exponentially small gap, difficult static interface, huge aggregate rate or long window can remain expensive.

## Conditional paths and the long wait

A stationary length-L uniformized path is proposed by marking either its initial state or a potential event in B, drawing that state from `pi(.|B)`, and running backward with P* and forward with P. Its density relative to the stationary path law is `N_B/[p(1+L)]`, where N_B counts all marked-eligible visits including null events/time zero. Accepting `1_G/N_B`, with `G={first hit in(H,L]}`, gives the exact G-conditioned path and bounded-mean probability estimate. Under the supplied parameter choice, acceptance is at least g/8; overlapping visits are corrected explicitly.

Mixing buffers make each selected block's starting density multiplicatively close to pi. Collapse a failed block to one symbol while keeping the full path on success. Per-cycle replacement error is **eta q_G**, so summing to first success costs at most `eta/(1-eta)`, without inverse rarity. Genuine hits hidden in discarded prefixes/buffers are charged jointly before conditioning on failed-block outcomes. An observed initial segment plus an unnormalized survivor bound handles arbitrary starts without equilibrium-safe physical preparation.

The failed-block index is sampled by a finite-bit geometric compiler; it is not iterated over. Capped rational Poisson/categorical primitives, finite timestamp meshes, acceptance limits and arithmetic budgets make the proof a finite construction. The independent [event-law check](package/next4_physical/02_EVENT_LAW_CHECK.txt) and [final compiler audit](package/next4_physical/03_FINAL_COMPILER_AUDIT.txt) support that actual scope. A generic CTMC/Gibbs software engine is not supplied; the [executed diagnostic](finite-execution.md) has narrower primitive guarantees.

## Composition and limits

The prior [correlated Gibbs construction](../2026-11-05-p3-correlated-reliability/README.md) supplies static access only at its declared fixed logarithmic-contrast, explicit rational-factor and all-pinning sampler scope, with work `v^O(c)` for fixed c. A supplied pi-invariant directed local circulation can be added to its heat-bath backbone; reverse moves and aggregate rate are paid and the additive-symmetrization gap retained. Physical factors/rates, hidden mechanisms and metrology are not learned by this theorem.

Joint TV controls bounded event-record observables. It is not relative accuracy for tiny deadlines, rare subtypes or survival tails, and the old changing-law CDF certificate does not automatically certify marked-path TV under fitted dynamics. The earlier equilibrium-safe relative whole curve and independent-edge all-working point query remain distinct operations.

Established Jackson overflow conditional/reversal algorithms, reverse-time SMC, weighted ensemble/splitting, quasistationary parallel replica, rare exponential laws and exact finite-state reduction are credited in the [comparisons and source record](package/next4_root/consequences_and_sources.tex). The small exact solver is the stronger diagnostic baseline; historical firstness and universal practical superiority are not claimed. All 123 predecessor source files are retained byte-identically. No science code, supplied native binary, solver, PDF compiler, new audit or large retrieval build ran for publication. Generated current retrieval remains unchanged.
