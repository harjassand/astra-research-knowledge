# Private transactional DAGs: physical-time closure and the restart barrier

2 November 2026. These are new timing lemmas, not a claim that the recursively protected executor has been built.

## Result first

A correctly initialized, closed quantum-safe DAG of private transactions has linear-in-depth physical completion with an exponential tail, even when siblings share arbitrarily correlated local service delays. One needs conditional service from the moment an input becomes ready, not independent completion times. Along a directed path the service intervals occur in order, so conditional moment bounds compose without a Finner assumption.

Conversely, applying a fixed-rate abort to an entire growing reversible macrotransaction is exponentially expensive. Progress must be committed locally. Thus the finite clearing-word lemma is useful at fixed physical scale but cannot be substituted for a recursive protected executor.

## 1. Causal and quantum contract

Fix a finite DAG and its source/output sets before exposing its service clocks. The theorem below is for this fixed path family; adaptively selected or newly generated task graphs need an additional predictable-exposure proof. Each vertex v is a fixed-support transaction with one output per quantum wire. A quantum input has exactly one authorized consuming transaction; there is no copying. Tasks may have several predecessors, but readiness is monotone after their durable commits. The known-state/workspace portions of a partially completed task may be reset, whereas a consumed unknown input must be rolled back coherently or committed forward as in `TRANSACTIONAL_LOCAL_SERVICE.md`.

The node starts service at A_v=max_{u predecessor v} T_u, where T_u is the durable completion time. Source nodes have A_v=0. Define S_v=T_v-A_v. Local private EC or honest competitors may interrupt service; the finite clearing word restores their uncommitted prefixes and eventually reserves the requested task. Persistent epoch, ownership, and output records are not erased by clearing.

The number of simultaneously eligible transactions per physical module/port is bounded by a fixed constant. A bounded spatial neighborhood alone does not imply this: if m ready tasks share one rate-lambda commit server, any claimed common interval guarantee v0 must obey m v0 <= lambda tau. Unbounded queues therefore cannot be called ready under the same constant-v0 contract. Add resource-order/queue-head dependencies to the DAG, or impose one outstanding request per fixed-degree port; the resulting extra edges and delay count toward d. Resource-order edges may be chosen forward in a fixed topological ordering, so they do not create cycles, but their potentially increased depth is a real cost.

This section assumes valid causal records and ready inputs. No availability lemma can infer that a corrupted durable bit represents a legitimate earlier quantum operation. Record faults are addressed only by a future encoded-controller/damage proof, not by this timing lemma.

## 2. Uniform geometric service is enough

Assume that at every stopping time t at which v remains ready, conditional on the entire physical past, the next service interval of duration tau has probability at least v0>0 to commit v. The concrete abort/clear/acquire/forward/commit Poisson word supplies this property for a fixed physical module and its bounded conflict neighborhood. Honest events outside the neighborhood cannot invalidate ready inputs or the word.

Let G_v be the number of service intervals needed. Iterated conditional probabilities imply

    P(G_v > m | F_{A_v}) <= (1-v0)^m.

Hence S_v <= tau G_v stochastically conditionally on F_{A_v}, and for

    0 < theta < -log(1-v0)/tau,

one has the history-uniform moment bound

    E[exp(theta S_v) | F_{A_v}] <= M(theta)
      := v0 exp(theta tau)/(1-(1-v0) exp(theta tau)).        (1)

No independence among different nodes is assumed.

## 3. Directed-path composition

For any fixed directed path pi=(v_1,...,v_k), T_{v_i}<=A_{v_(i+1)}. Thus every earlier service duration is measurable before the next interval begins. Applying (1) repeatedly by the tower property gives

    E[exp(theta sum_{v in pi} S_v)] <= M(theta)^k.         (2)

This is not true for an arbitrary set of concurrently waiting siblings. Their common delay is exactly the shared-stall counterexample in the companion note. It is true along the ordered intervals of a dependency path.

Because T_v=A_v+S_v, the DAG completion time is exactly the maximum over source-to-output paths of the sum of S_v along that path. Suppose every path has at most d vertices, the indegree is at most Delta, and there are B designated output vertices. The number of paths is at most B D^d for D=max(2,Delta). Markov's inequality and (2) therefore yield

    P(T_max > t) <= B [D M(theta)]^d exp(-theta t).       (3)

In particular, with probability at least 1-exp(-x),

    T_max <= [d log(D M(theta)) + log B + x]/theta.       (4)

All constants depend only on the finite private transaction and its conflict neighborhood. There is no factorial fault-strength replacement and no implicit external clock: the time intervals are an analysis partition of stationary Poisson-driven dynamics.

### What this legitimately closes

It closes ideal physical-time liveness for a correctly initialized finite closed DAG, using an explicit local service word. It also gives a useful tail for a hierarchical finite DAG *if* the requisite valid causal state and local service contracts have actually been implemented at every level.

It does not promote availability on arbitrary damaged local ledgers to global exactly-once semantics; does not bound the damage of corrupted encoded epoch records; and does not make a macroscopic atomic acquire or commit local. Those are still construction obligations.

## 4. A fixed-rate macro-abort is exponentially bad

Consider a d-stage reversible chain. Stages complete at rate gamma and a separate rate-mu clock restarts the whole chain from stage 0. All ideal aborts are logically harmless. To give restart the most favorable timing, assume its rollback/reset takes zero physical time and each new attempt has fresh independent stage and abort clocks. A real reversible rollback has positive duration and cannot improve this benchmark. Let X~Gamma(d,gamma) be the duration of one uninterrupted execution and Y~Exp(mu) the time to abort. The attempt succeeds with probability

    p_s = E[exp(-mu X)] = (gamma/(gamma+mu))^d.

Under that favorable instantaneous-restart model, the mean attempt duration is

    E[min(X,Y)] = (1-p_s)/mu.

Renewal at failure gives the exact expected total completion time

    E[T_d] = E[min(X,Y)]/p_s
           = ((1+mu/gamma)^d - 1)/mu.                  (5)

Thus a growing depth d=T0^l has doubly-exponential-in-l mean service at fixed mu/gamma. Harmlessness of an abort is not enough. Taking a giant success word at every concatenation level has the same failure mode.

By contrast, if each **fixed-size** d0-stage transaction commits a durable prefix, only its own incomplete part restarts. A chain of k such tasks has mean at most k times its actual uniform fixed-module service mean, including positive rollback/reset costs, and its high-probability behavior is controlled by (4). Formula (5) is only the optimistic instantaneous-rollback benchmark. If the conditional failed-attempt rollback has mean r and the attempts renew, the corresponding actual mean is ((1+mu/gamma)^d-1)(1/mu+r). Such checkpoints must contain protected quantum ownership and commit state, not just a raw high-level counter.

## 5. The actual missing operation

The difficult join is now precise: implement the durable DAG headers, epochs, and consumed/output records through the same self-similar fault-tolerant machinery as the quantum payload, while permitting private inner EC regardless of outside payload readiness. A single physical bit must neither authorize a logical gate nor disable correction of an entire growing block forever. The established synchronous noisy-controller construction is a natural component; its continuous-time outline alone is not this join.

The local private module and (1)-(4) remove a timing obstacle. They do not establish a passive Gibbs basin, a continuous autonomous threshold, or superiority over the same-resource active comparator. All independent Poisson services, finite-purity resets, encoded classical records, ancillas, and ongoing heat/work throughput are resources provided equally to that comparator.


Independent audit: `async_primary_gate/PRIVATE_DAG_TIMING_AUDIT.md` verifies the fixed-path filtration argument and records the bounded-eligibility and actual-rollback-cost qualifications incorporated above.
