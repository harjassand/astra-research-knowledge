## New result: bounded control of an invariant law despite hidden memory

I developed a general operation that **gives the actual physical endpoint a prescribed invariant law, with a sharp bound on the number of native operations required**. It works without learning the transition probabilities or constructing a finite predictive model.

The consequential opening is now broader than the contractive ring: **local programs for interacting continuous systems, including strong interactions, whose hidden dynamics remain unknown and may retain infinite predictive rank.**

The completed snapshot contains the proofs, code, constructive alternatives, actual reviews and corrections. All **201 files from the preceding snapshot remain byte-for-byte unchanged**.

[:chatgpt-content-reference{index="4"}](https://chatgpt.com/library?file_id=libfile_3d63086ea5908191921f484248ea7ec7&account_id=personal)

### 1. The operation and its sharp resource bounds

Suppose an actual native operation has microscopic Markov kernel \(P\) and preserves a probability law \(\mu\). The microscopic state includes hidden memory affecting subsequent calls. Neither that state nor \(P\)’s transition probabilities need be known.

A noninvasive visible label supplies a positive integer weight \(W\). Write

\[
m=\min W,\qquad M=\max W,\qquad Z=\int W\,d\mu.
\]

The desired invariant law is

\[
\nu(dx)=\frac{W(x)}{Z}\,\mu(dx).
\]

The controller is small:

1. At the current state, draw an integer counter uniformly from \(0,\ldots,W(x)-1\).
2. Execute one actual \(P\) call.
3. Advance the counter by \(m\), modulo \(M\).
4. Read the new weight. Finish if the counter is below it; otherwise repeat.

Every output is the **current physical state**. The construction uses endpoint sensing, random selection and repeated native calls. Its stopping rule satisfies

\[
\boxed{1\leq \tau\leq \left\lceil M/m\right\rceil}
\]

on every path, regardless of the unknown kinetics.

The endpoint kernel preserves \(\nu\). Reversibility is unnecessary for this invariance statement. When \(P\) is reversible, choosing the counter direction with a fair sign also makes the compiled endpoint kernel reversible.

The proof lifts the process to “microscopic state plus counter.” The product law \(\mu\times\mathrm{Uniform}\) is stationary. Restricting it to the accepted counter positions gives microscopic marginal \(\nu\); the controller implements its positive first-return kernel. The counter geometry guarantees a return within the stated cap. The watched-chain identity is established mathematics; the bounded return construction supplies the operation here. :chatgpt-content-reference{index="0"}

Two matching limits make this more than a working construction:

- **Sharp universal cap.** For the stated interface—one unknown native kernel, endpoint observations and the same controller across an unknown lazy-kernel family—no universal controller can improve on \(\lceil M/m\rceil\).
- **Optimal stationary mean, with a necessary premise.** Starting at \(\nu\),
  \[
  \mathbb E_\nu\tau=\frac{M}{Z}.
  \]
  If \(P\) has a unique stationary probability, no controller that must execute at least one native call and output its actual stopped state can have a smaller stationary mean. Reducible sources require a componentwise statement.

The governing argument is in :chatgpt-content-reference{index="5"}[BOUNDED_STATIONARY_CHANGE_OF_MEASURE.md](producer-workspace/BOUNDED_STATIONARY_CHANGE_OF_MEASURE.md).

### 2. The ordinary alternative changed the claim

The constructive comparison was decisive. The **Rejection Markov chain** already obtains stationary reweighting from an unknown stationary source by accepting endpoints with suitable probabilities. That capability is a predecessor, including its extension beyond reversible sources. :chatgpt-content-reference{index="1"}

Ordinary endpoint thinning has the **same stationary mean cost** as this construction. Its tail is generally unbounded, and it lacks a universal deterministic call cap. The counter supplies that cap without increasing the stationary mean.

One exact comparison in the saved code illustrates the distinction:

| Quantity | Ordinary endpoint thinning | Counter operation |
|---|---:|---:|
| Native stationary masses | \((1,2,3,4)/10\) | Same |
| Target weights | \((1,2,4,8)\) | Same |
| Stationary mean calls | \(80/49\) | \(80/49\) |
| Probability of exceeding eight calls in the checked kernel | Approximately \(0.0155350\) | Exactly zero |

Correlated acceptance uniforms and wrapped auxiliary-coordinate updates also have close predecessors, including Neal’s construction. Historical priority for the complete assembly has **not** been established. The candidate addition is the bounded current-state implementation, its matching resource limits, and the demonstrated hidden-state composition. :chatgpt-content-reference{index="2"}

The existing physical-mechanism helper also developed genuine holds, return-based rejection, rate-controlled gates and initialization alternatives. Those remain valid competitors when their additional controls are supplied.

### 3. A consequential receiver: interacting continuous systems

I extended the construction to a continuous physical model with:

- visible signs of coordinates \(x_1,\ldots,x_d\);
- a shared, evolving hidden coordinate \(z\);
- a conserved hidden parameter \(h\);
- unknown mobilities and interactions among hidden magnitudes.

The supplied native controls are addressed divergence-form diffusions. Their common energy is invariant under each separate sign flip, so every conserved sector has the same uniform joint baseline sign law. An operation updates \(x_i\) and the shared hidden coordinate while keeping the other visible coordinates fixed.

This structural interface permits a desired positive rational factor law,

\[
\pi(y)\propto \prod_a\psi_a(y_a),
\]

to be implemented through local compiled operations. Each local operation preserves the corresponding **full microscopic tilted law**. Prescribed scans and independently selected, state-independent scans preserve that law as well.

For integer local energies measured in units of \(\log 2\), the relative weights are powers of two. With bounded local energy changes, both the native-call cap and selector-bit requirement stay bounded independently of the number of sites. The family includes strong ferromagnetic interactions, frustration and positive softened constraints. Collective mixing barriers remain.

This advances the scope beyond the earlier contraction example. It supplies an interacting continuous family even where the sharp readout cannot belong to an exact finite invariant predictive feature space.

The receiving review found an actual mathematical correction: with cross-coupled mobility, the reflecting boundary must be **conormal**,

\[
n\cdot A_i\nabla_i f=0,
\]

with the corresponding reflected-SDE boundary term. Ordinary normal reflection would not justify the claimed reversible operator. The corrected version is accepted and preserved alongside the original review and its counterexample.

The complete consequence is in :chatgpt-content-reference{index="6"}[CONNECTED_DIFFUSION_AND_LOCAL_FACTOR_PROGRAMS.md](producer-workspace/CONNECTED_DIFFUSION_AND_LOCAL_FACTOR_PROGRAMS.md).

### 4. What this changes about learning—and what remains costly

The important separation is:

> **Exact control of an invariant law can require less information than exact prediction of the dynamics producing it.**

The binary specialization fixes an invariant odds ratio while leaving its mobility unknown. With a frozen continuum of kinetic parameters, the resulting observable process still has infinite linear predictive rank. Thus the control theorem does not obtain its effect by secretly learning or erasing all the hidden memory.

This changes the role of calibration. Within an **already warranted common stationary family**, calibration can choose a faster operation and freeze that choice before deployment. Kinetic estimation error then need not enter the target ratio. It still affects throughput, and the calibration record still changes the conditional initial state. Finite observations do not establish unrestricted hidden stationarity exactly.

Several boundaries remain load-bearing:

**Completion times and ordinary clock times differ.** The proof gives

\[
\mathbb E_\nu\!\left[\sum_{j=0}^{\tau-1}
\mathbf 1_{\{X_j\in dx\}}\right]
=\frac{M}{Z}\mu(dx).
\]

For one native kernel repeated back-to-back, its native occupation law remains \(\mu\). The endpoint law is tilted at operation completions. A local network changes the subsequent actuation schedule, but its wall-time law needs separate analysis.

**Invariance does not prepare the initial state.** Convergence, retained histories, post-calibration conditioning and conserved-sector weights remain real issues. The preserved unequal-sector example still gives \(7/10\) where an unjustified global-tilt inference predicts \(3/4\). The continuous receiver resolves that particular problem by supplying the same visible baseline in every sector.

**Small local errors do not guarantee correct phase weights.** The complementary construction shows that a coherent field error of order \(1/n\) can produce vanishing local row error while leaving a nonzero limiting magnetization. The error can be conservative. Strong-interaction claims therefore cannot inherit the earlier contractive program’s observable guarantees automatically.

**A native-call cap is not automatically a laboratory deadline.** Exact selection for general integer weights can have unbounded randomizer time. Power-of-two weights supply bounded fair-bit selection. Actual deadlines additionally require compatible sensing, computation, switching and native-call durations.

Addressability, isolation and noninvasive sensing are supplied controls of the continuous mathematical model. An apparatus providing them, with an end-to-end precision budget, has not been demonstrated.

### 5. Review status and the next substantive frontier

Both existing complementary roles independently accepted the main theorem. The corrected diffusion consequence also received an acceptance addendum. Exact rational checks cover full hidden kernels, irreversible sources, occupation and cost identities, local composition and deliberately incorrect controllers. They are population-model checks, not physical experiments.

The saved record retains the useful failures: the first low-mobility pair, incorrect return horizons, incorrect initial counter phases, the frozen-sector obstruction, the failed multilabel return repair, and phase sensitivity to vanishing local errors. The previous acquired constructions, signed-continuation theorem, uniform-time observable program and their reviews remain intact.

The new opening is **structurally exact target control with bounded completion despite unresolved hidden kinetics**. The next consequential connection is a compatible physical interface—or a demanding computational consumer—for which that bounded completion and target precision change what can actually be accomplished. Preparation speed, apparatus feasibility and a practical advantage remain open; the theorem now makes the capability and its required suppliers precise.