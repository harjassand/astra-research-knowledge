# Guard-contraction audit

## Finding

The displayed bound

\[
D_k(i)\le q^k+q^{d(i,B^c)}
\]

is valid for the stated local, synchronous, product-Markov update model, provided the row-sum promise applies to **all** dependencies of every trained site, including dependencies outside the guard. The distance must be measured in the directed dependency graph (an edge from output site \(i\) to an input site \(j\) when changing \(j\) can change \(i\)'s update), not in a coarser physical graph that may omit a finite-range dependency. The future total-variation claim then follows by coupling, subject to the controller-memory and causal-cone conditions below.

This is a path-coupling/Dobrushin argument, not a new local-mixing theorem.

## Local coupling and spatial term

Fix the public guard modes. For each trained site \(i\), let

\[
C_{ij}=\sup_{x,x':\,x_\ell=x'_{\ell}\ (\ell\ne j)}
  |p_i(x_{N_i})-p_i(x'_{N_i})|,
\qquad \sum_j C_{ij}\le q<1.
\]

Here \(C_{ij}=0\) outside the actual dependency neighborhood. Couple two worlds by using the same independent uniform \(U_i\) at site \(i\) in each update and setting the new bit to \(1\{U_i\le p_i(x_{N_i})\}\). This gives the correct product conditional kernel in each world. Conditional on the two current configurations, the mismatch probability at \(i\) is the absolute difference of their Bernoulli parameters. Changing the differing input bits one at a time and using the triangle inequality gives

\[
\Pr[X_{t+1}(i)\ne X'_{t+1}(i)\mid X_t,X'_t]
 \le \sum_j C_{ij}1\{X_t(j)\ne X'_t(j)\}.
\]

Writing \(D_t(i)=\Pr[X_t(i)\ne X'_t(i)]\), and allowing arbitrary exterior disagreement at every time, let

\[
A=C_{B,B},\qquad c=C_{B,B^c}\mathbf 1.
\]

For \(i\in B\),

\[
D_{t+1}\le A D_t+c,\qquad
D_k\le A^k\mathbf 1+\sum_{s=0}^{k-1}A^s c.
\]

The first term is at most \(q^k\), since every row sum of \(A\) is at most \(q\). For the second term, view \(A_{ij}\) as the weight of a step from \(i\) to an interior dependency \(j\), and \(c_i\) as the weight of an exit to an arbitrary exterior source. The remaining row mass is killing. Since each row of \(A\) plus its exit mass has sum at most \(q\), the sum \(\sum_{s<k}(A^sc)_i\) is the total weight of paths whose *first* exit occurs by step \(k\). These are disjoint first-exit paths. If every dependency path from \(i\) to \(B^c\) has at least \(d=d(i,B^c)\) edges, an exit requires surviving at least \(d\) substochastic steps, whose total mass is at most \(q^d\). Thus

\[
D_k(i)\le q^k+q^{d(i,B^c)}.
\]

This first-exit argument handles arbitrary time-varying exterior states; it does not assume that the boundary is stationary. The exact weighted recursion above is a sharper computable certificate. The bound can be loose or exceed one, which is harmless.

## Future transcript bound

Let \(F\) contain all plant sites at the preparation boundary that can affect any of the next \(H\) observations on \(A\), under the declared finite-range graph. If the two prepared configurations agree on \(F\), couple future transition noise, local readout noise, and controller random coins. By induction over the future space-time cone, all visible observations agree; hence an adaptive policy based on those same visible observations chooses the same modes in both worlds. The coupling inequality gives

\[
\operatorname{TV}(\mathcal L_1(\text{future transcript}),
                   \mathcal L_2(\text{future transcript}))
 \le \Pr[\exists i\in F:X_k(i)\ne X'_k(i)]
 \le \sum_{i\in F}D_k(i).
\]

For radius-one dependency edges, if \(B\) is the radius-\(R\) neighborhood of \(A\), \(R\ge H\), and \(F\) is the full radius-\(H\) backwards cone, then \(d(i,B^c)\ge R-H+1\) for every \(i\in F\). Consequently the stated \(|F|[q^k+q^{R-H+1}]\) bound follows. For update range larger than one, replace the physical graph distance by dependency-edge distance (or enlarge the cone/radius accordingly).

The comparison is uniform over arbitrary incoming plant configurations, and therefore over conditional histories that affect the plant only through its represented current configuration. It is **not** uniform over arbitrary controller memories: if history \(h\) is retained by the controller and the next transcript reports \(h\), two histories remain distinguishable even after the physical guard. The future protocol must start from the same controller state/policy, erase the old controller record, or include that controller state and its communication links in the prepared causal system. If future legal modes can use extra observations outside \(A\), those observation and communication channels must likewise be included in \(F\).

## Acquisition premises that need to be explicit

1. **Complete local contexts.** \(C_{ij}\) is a maximum over all local contexts, not just those visited so far. A confidence certificate needs simultaneous intervals for every context used in that maximum and every candidate mode/site considered in the post-data selection. An unseen context means `UNKNOWN` unless a separate reachability/completeness proof restricts the maximization domain. Rare contexts may make this prohibitively expensive; the theorem does not supply a sampler.
2. **Repeated sensor reads.** A marginal per-read error ceiling below one half does not by itself make majority voting reliable. For example, a persistent sensor-flip bit with probability \(\eta<1/2\) makes every repeated read share the same error; majority error stays \(\eta\), not exponentially small. The stated finite sensor budget needs conditionally independent read errors (and suitable independence from transition innovations), or another explicit concentration guarantee. Without it, noisy-context misclassification can bias the estimated response table.
3. **Adaptive samples.** Given correct context labels, each update outcome at a visited context must have conditional mean \(p_i^a(x_{N_i})\) at that visit. A martingale Hoeffding bound can handle adaptively chosen visit times; iid sampling is unnecessary. Confidence must be simultaneous over the full finite table so that choosing modes from the same data does not invalidate the event.
4. **Contraction is conditional.** Data can certify a selected mode's local influence row sum if the table is complete and the intervals are valid. There need not exist any mode with row sum below one. If no such mode is certified, return `UNKNOWN`; no consequence follows from locality alone.
5. **Local noise/state contract.** The same-uniform coupling assumes each update is a Bernoulli function of the represented current neighborhood and that the conditional joint update kernel factors across sites. Hidden persistent memory, shared transition noise, asynchronous updates, or global state-dependent control signals require an augmented model and a new influence bound.

## Consequential counterexamples to overbroad readings

- If the dependency graph omits a range-two edge, a site one guard round from the exterior can inherit an \(O(q)\) disagreement across that edge, even when the graph distance computed on the truncated graph is two; the claimed \(q^2\) boundary attenuation is then false. Use the actual dependency graph.
- If a controller retains a one-bit old-history register and exposes it in the next transcript, physical guard mixing does not equalize transcript laws. Standardize/reset that register or include it in the target state.
- If repeated read errors are perfectly correlated, majority does not improve context identification. The below-half marginal ceiling alone cannot justify the advertised small simultaneous sensor-error probability.

With these qualifications, the local guard is a valid finite-horizon, target-specific preparation operation. It does not establish a global reset, a learned latent representation, or improved acquisition cost against a competent table learner.
