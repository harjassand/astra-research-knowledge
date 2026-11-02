# Audit: private DAG timing and macrorestart

2 November 2026. Audits `../PRIVATE_DAG_TIMING.md`. No claim of recursive fault tolerance follows from this timing result.

## Verdict

Equations (1)–(4) are valid for a fixed finite DAG under the stated uniform conditional service contract, provided readiness and durable completion have their usual adapted, monotone meanings. Arbitrary correlations between sibling service times and shared Poisson clocks do not break the fixed-path moment argument.

The important implementation qualification is **bounded simultaneously eligible task multiplicity per physical module**, not merely a bounded spatial conflict neighborhood. A fixed local service word cannot give the same constant service probability to unboundedly many simultaneously ready tasks sharing finite-rate hardware. Resource-order edges or an explicit bounded-eligibility invariant must be charged.

Equation (5) is exact for instantaneous full restart with fresh independent stage/abort randomness. Finite rollback time makes this an optimistic benchmark, not a complete physical equality.

## 1. Precise hypotheses sufficient for the proof

Use a filtration `(F_t)` satisfying the usual conditions. The DAG is fixed in advance; its vertices and edges do not depend retrospectively on service durations. For every vertex:

1. `T_v` is its first durable-completion stopping time. Completion is persistent: a later honest event cannot retract it.
2. `A_v=max T_u` over the fixed predecessors (zero for sources) is a stopping time; `A_v<=T_v`.
3. From `A_v` until `T_v`, readiness cannot be invalidated by an honest transaction, reset, or resource competitor. Ready unknown inputs remain valid and available, even if service is interrupted.
4. On `{T_v>A_v+m*tau}`, conditional on `F_(A_v+m*tau)`, the probability of completion by `A_v+(m+1)*tau` is at least `v0`. Requiring this at every stopping time, as the draft does, is stronger than necessary but sufficient.

This requires actual durable causal records and quantum ownership. It does not follow merely because a raw ledger bit currently says `ready`.

## 2. Conditional service MGF

Let `G_v=ceil((T_v-A_v)/tau)`; zero is allowed if completion is instantaneous. Iterated conditional failure probabilities give

    P(G_v>m | F_Av) <= q^m,  q=1-v0.

Pointwise `S_v=T_v-A_v<=tau*G_v`. For `z=exp(theta*tau)` with `q*z<1`, the tail-sum identity gives

    E[z^Gv | F_Av]
       = 1+(z-1)*sum_{m>=0} z^m P(G_v>m | F_Av)
       <= 1+(z-1)/(1-q*z)
       = v0*z/(1-q*z).

Thus equation (1) holds exactly as written. Acyclic induction from source nodes also proves all completion times finite almost surely; no hidden assumption of finite service is needed.

## 3. Why shared clocks do not spoil path composition

For a fixed directed path `(v1,...,vk)`, each `T_vi<=A_v(i+1)`. Since `S_vi` is measurable at `F_Tvi`, all earlier path service durations are measurable at `F_Avk`. Therefore

    E[exp(theta*sum_{i<=k} S_vi)]
      = E[exp(theta*sum_{i<k} S_vi)
            E(exp(theta*S_vk) | F_Avk)]
      <= M(theta)*E[exp(theta*sum_{i<k} S_vi)].

Induction proves (2). Neither disjoint clocks nor independence is used. Overlap among *sibling* intervals is irrelevant to this calculation because the product uses only one causally ordered path.

Readiness monotonicity matters twice: it supports the interval-by-interval service trial, and it makes each predecessor completion a persistent authorization for successors. If completion can be revoked or an input can disappear, `T_v=max T_pred+S_v` may still be a tautological numerical definition but the service contract no longer follows from the earlier local-word argument.

A fixed graph also matters. Selecting a vertex/path after observing which delays were largest cannot be treated as a fixed-path estimate. For example, selecting the slowest of many source vertices after all finish does not preserve a one-node geometric MGF. Adaptive programs can be compiled into a fixed potential DAG, or require a separate predictable-selection argument; do not condition on a retrospectively selected realized DAG without proof.

## 4. Maximum-path and path-count steps

For nonnegative `S_v`, the recurrence `T_v=max T_pred+S_v` recursively gives the maximum source-to-v path sum. This remains true even if resource contention contributes to `S_v`.

With indegree at most `Delta`, depth at most `d>=1`, and `B` designated outputs, the draft's bound `B*max(2,Delta)^d` on relevant source-to-output paths is conservative and valid. Equations (3)–(4) follow. Take `x>=0`; a probability bound may optionally be capped at one.

Here `T_max` means completion of the designated outputs. To call it completion of the whole DAG, designate every sink or ensure every vertex is an ancestor of a designated output.

## 5. Hidden physical-resource condition

Suppose `m` simultaneously ready transactions share a physical commit server of total rate at most `lambda`, and one server event can commit at most one transaction. Uniform service in an interval `tau` would imply

    m*v0 <= sum_j P(transaction j commits within tau)
          = E[number of distinct commits within tau]
          <= lambda*tau.

Consequently `v0<=lambda*tau/m`. Bounded spatial range does not prevent `m` growing. Even a closed finite DAG may present arbitrarily many ready tasks to one module unless task eligibility includes resource ownership/order.

Two sound fixes:

- Prove a uniform bound on the number of simultaneously eligible transactions per bounded physical conflict neighborhood.
- Include resource-order/acquisition vertices or edges in the DAG; then charge the resulting depth and storage. A queue that has not acquired its service entitlement is not yet ready for the uniform service lemma.

This is an implementation qualification, not a counterexample to (1)–(4) once their hypotheses truly hold.

## 6. Macrorestart equality and physical correction

For `d` independent exponential stages of rate `gamma`, let `X~Gamma(d,gamma)` and let the independent abort time be `Y~Exp(mu)`, with `mu,gamma>0`. Then

    p=E[e^(-mu*X)]=(gamma/(gamma+mu))^d,
    E[min(X,Y)]=(1-p)/mu.

At failure, an instantaneous return to the identical fresh initial state gives the renewal equation

    E[T]=E[min(X,Y)]+(1-p)*E[T],

so the draft's exact formula follows:

    E[T]=((1+mu/gamma)^d-1)/mu.

The limit as `mu->0` is `d/gamma`. Self-loop aborts at stage zero do not invalidate the renewal derivation because exponential stages are memoryless.

If each failed attempt incurs additional nonnegative rollback/reinitialization duration `R`, and a fresh attempt really starts afterward, let `r=E[R | failure]`. Then, when finite,

    E[T]=((1+mu/gamma)^d-1)*(1/mu+r).

Further abort interference during rollback or uncharged quantum recovery can worsen this. Thus the zero-time formula is already sufficient to establish an exponential restart barrier, but should be labeled an optimistic ideal benchmark rather than an exact cost for finite-rate coherent rollback.

## Minimal edits recommended

1. Add: “The number of simultaneously eligible transactions per physical conflict neighborhood is uniformly bounded; otherwise resource-order edges are included and charged in d.”
2. State that the DAG is fixed/predictable, all completion/readiness times are stopping times, and designated outputs cover all sinks when whole-DAG completion is intended.
3. In the macro-abort paragraph, specify instantaneous fresh restart; mention positive rollback overhead only strengthens the lower-cost benchmark.

No independence repair, Finner inequality, or replacement of the fixed-path MGF proof is needed.

### Patch verification (05:40 UTC)

The parent file now incorporates fixed pre-exposed graph, bounded simultaneous eligibility/resource-order edges, and favorable instantaneous macrorestart assumptions. One consequential wording issue remains in its checkpointed-chain contrast: “at most k times ... value in (5)” is not a physical upper bound once positive rollback is charged. Use “k times the actual uniform fixed-module service mean, including rollback/reset costs,” or explicitly keep that comparison inside the zero-time ideal model.
