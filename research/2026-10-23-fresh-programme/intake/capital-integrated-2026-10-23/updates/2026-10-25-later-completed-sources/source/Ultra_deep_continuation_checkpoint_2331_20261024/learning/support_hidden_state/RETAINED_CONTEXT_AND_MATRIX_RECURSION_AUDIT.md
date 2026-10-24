# Retained-context acquisition and matrix-recursion audit

## 1. Operational reproducibility versus a specified target

The one-trajectory acquisition protocol does not need an initializer: it can begin in the actual unknown field, apply the fixed public exploration schedule, and retain only noisy reads and response counts. On a run where every required site–mode–context row is completed, the finite-table confidence event can certify a useful local influence bound. The protocol has no coverage guarantee: rare, frozen, inaccessible, or schedule-missed contexts lead to `UNKNOWN`. No data-derived claim should turn the supplied graph, local-state sufficiency, update range, or Markov structure into an empirically certified fact.

The guard theorem is best interpreted as **small future-observable diameter**. Let \(\mathcal P(x,\beta)\) be the law of the next \(H\)-round transcript on \(A\) after the public guard, from plant configuration \(x\) and an admissible exterior evolution/boundary input \(\beta\). The coupling bound says every pair of such laws has TV at most the certificate, when all physical dependencies are in the stipulated graph and noise is unobserved. Therefore any one actual anchor \((x_*,\beta_*)\), even if unknown to the learner, may be used as a **mathematical reference witness**; all admissible futures in the declared observation interface are close to its law.

This does not certify or synthesize a learner-known exact target law. In general there is no autonomous kernel on \(B\) alone: its updates can depend on the time-varying exterior boundary. The reference must be the full plant evolution under the same guard operation and an actual admissible exterior process, or else the boundary process must be explicitly modeled as an input. The guarantee is a pairwise operational statement, not a globally prepared state, nor an assertion that the learner can calculate the anchor's full law. If future records include old controller memory, that memory must be standardized, erased, or included in the state/interface; otherwise an old one-bit history can distinguish transcripts independently of the plant guard. Future modes may be adaptive to the declared observations on \(A\), provided both compared runs use the same policy and common policy randomness, and the causal cone includes every channel by which those observations affect later actions.

Arbitrary exterior cell trajectories are handled by the existing boundary term, which pessimistically allows exterior disagreement at every guard round. “Arbitrary” does not include unmodeled direct signals into interior update rules, history-dependent interior modes that bypass the public guard word, or a hidden memory variable not represented by the supplied local state.

## 2. Sound capped finite-matrix recursion

Condition on the simultaneous confidence event that the actual coefficients satisfy \(0\le C_{ij}\le\bar C_{ij}\) for all tested rows and all local contexts in the certified table. The upper coefficients should be formed from the full response intervals. If \(p_i^a(z)\in[L_i^a(z),U_i^a(z)]\), one valid bound for a parent \(j\) is

\[
\bar C_{ij}^a=\min\!\left(1,
 \max_{z\triangle_j z'}\max\{U_i^a(z)-L_i^a(z'),\ U_i^a(z')-L_i^a(z)\}\right),
\]

where \(z\triangle_j z'\) means that the two local contexts differ only at \(j\). If any required context is missing, this maximum is not certified; the operation must return `UNKNOWN` (or use a separately proved restricted reachable-context domain).

For a fixed guard mode vector, set

\[
A=\bar C_{B,B},\qquad b=\bar C_{B,B^c}\mathbf1,
\qquad \Delta_0=\mathbf1_B,
\]

and iterate componentwise

\[
\Delta_{t+1}=\mathbf1_B\wedge(A\Delta_t+b),
\]

where \(\wedge\) denotes componentwise minimum. Then \(D_t\le\Delta_t\) for every pair of incoming configurations and every allowed boundary evolution. Induction: \(D_0\le\mathbf1_B\); if \(D_t\le\Delta_t\), the local coupling inequality and \(C\le\bar C\) give

\[
D_{t+1}\le C_{B,B}D_t+C_{B,B^c}\mathbf1
          \le A\Delta_t+b.
\]

Also every disagreement probability is at most one. Hence \(D_{t+1}\le\min(\mathbf1_B,A\Delta_t+b)=\Delta_{t+1}\). The cap is therefore sound even when an interval row sum is too loose and the linear expression exceeds one.

If the public guard uses time-varying fixed modes, the same proof gives \(\Delta_{t+1}=\mathbf1\wedge(A_t\Delta_t+b_t)\). If every row of \(\bar C\) has sum at most \(q<1\), the uncapped expansion is

\[
\Delta_k^{\rm lin}=A^k\mathbf1+\sum_{s=0}^{k-1}A^s b.
\]

The path/first-exit proof bounds this componentwise by \(q^k+q^{d(i,B^c)}\). Thus the capped matrix result is no worse than the scalar bound under the same row-sum and dependency-distance assumptions, and can be much tighter because it retains actual spatial weights and boundary locations. For example, take two interior sites with only \(\bar C_{12}=0.6\) and an exterior influence \(\bar C_{2,o}=0.1\). Row sums are at most \(q=0.6\), site 1 has dependency distance two from the exterior, and at one guard step the matrix recursion gives \(\Delta_1(1)=0.6\); the scalar estimate gives \(0.6+0.6^2=0.96\). A site with no path to the exterior gets zero boundary contribution in the matrix recursion, even if a coarse geometric distance bound is unavailable.

The matrix calculation does not certify the architecture. It is conditional on supplied cell variables, causal graph/range, conditional Markov rule, and physical transition channel. Counts can estimate the local probabilities and interval influence weights for those stipulated rows; they cannot rule out omitted long-range influence, hidden persistent memory, an incorrect wiring graph, or a different boundary-to-interior channel.

## 3. Retained-trajectory acquisition check

The acquisition claim is valid as an **unconditional failure-and-return** statement under the amended sensor/time contract in `RETAINED_CONTEXT_ACQUISITION.md`:

- All needed pre-update context labels are read before the update, and the public mode assignment is predictable from the past. On the event all majority labels are correct, visits routed to row \((i,a,z)\) are true visits to that row.
- At each such visit, conditional on the entire pre-update history and current context, the post-update bit has fixed mean \(p_i^a(z)\). The row's first \(m\) outcomes form a bounded martingale-difference sequence about that mean, even when visit times are adaptive. A stopped-martingale or synthetic-unused-tape argument bounds the event “row completed and empirical mean is wrong” without conditioning on completion.
- The finite cap ensures a finite union bound. On completion, all rows have \(m\) samples; on noncompletion, return `UNKNOWN`. The probability of a returned invalid table is bounded by the read-misclassification union bound plus \(2M e^{-2mw^2}\). It is not valid to divide this bound by the probability of completion and call it a confidence conditional on success.

The deterministic parallel schedule must actually offer each required site–mode pair enough rounds; global alternation covers two modes, while a larger candidate set needs an explicit finite schedule. Context coverage itself is still generated by the uncontrolled/stipulated plant trajectory, not forced. A visitation lower bound is needed for a uniform expected acquisition-time claim, and none is present. Thus “zero initializer calls” is an achieved interface reduction, not a bound on starts, rounds, or cost needed before successful return.

The confidence event relies on the supplied conditional sensor-error ceiling and transition law. The majority Hoeffding–Azuma bound is valid because the conditional error probability at every repeated read is bounded by \(e_s<1/2\); no cross-read independence is needed. The post-update outcome concentration relies on the stipulated constant conditional transition mean at a correctly identified row. These conditions do not establish that the local physical model is complete.
