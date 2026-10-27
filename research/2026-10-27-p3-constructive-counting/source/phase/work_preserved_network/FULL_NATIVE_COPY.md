## Astra Pro3 — Removing the rank-one model assumption

The strongest next construction is a model-independent intervention audit within a broader physical class. Instead of reconstructing the source's internal matrices, the learner uses new scalar measurements to certify whether a proposed intervention is close to optimal.

### New conditional theorem

Let

\\[ Z(u)=e^\mathsf{T}Q(u)^{-1}e,\qquad G(u)=Z(0)-Z(u)-c^\mathsf{T}u. \\]

Assume that the unknown physical matrix \\(Q(u)\\) is uniformly positive definite and matrix-concave in the intervention doses. Unlike the previous work, \\(Q(u)\\) need not be affine, its actuators need not be rank one, and its dimension need not be known.

Suppose independently justified physical bounds give

\\[ Q(u)\succeq mI,\quad \\|\partial_i Q(u)\\|\le L_i,\quad \\|\partial\_{ii}Q(u)\\|\le B_i. \\]

Then \\(G\\) is globally concave, and each coordinate has the curvature bound

\\[ -M_i\le \partial\_{ii}G(u)\le0, \qquad M_i=\\|e\\|^2\left(\frac{2L_i^2}{m^3}+\frac{B_i}{m^2}\right). \\]

For any feasible proposed intervention \\(x\\), leave a small dose margin \\(h_i\\) and measure just \\(Z(x)\\) and \\(Z(x+h_ie_i)\\).

The true marginal benefit must lie in

\\[ \boxed{ \frac{G(x+h_ie_i)-G(x)}{h_i} \le \partial_iG(x) \le \frac{G(x+h_ie_i)-G(x)}{h_i} +\frac{M_ih_i}{2}. } \\]

Raw sensor-error intervals can be propagated through these inequalities without assuming independent noise.

Once all marginal benefits are enclosed, concavity gives a global regret certificate over every continuous intervention satisfying the dose constraint, using the same simplex optimization bound as the preceding Astra construction.

For 128 actuators, one audit requires 129 scalar reactions, provided there is sufficient dose margin. It does not need the previous 510-reaction Gram reconstruction.

This is a conditional extension of established finite-difference and convex-optimization principles, not a historically novel optimization theorem. Related zeroth-order optimization methods are well established.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://ojs.aaai.org\&sz=32)

ojs.aaai.org+1



### Executed result: 128 controls, no reconstructed network

I implemented the audit using exact-rational four-node network calculations. The source contains nonlinear saturating conductances and some rank-two actuator effects, so the earlier affine rank-one reconstruction theorem does not apply.

Total distinct reactions

# 290

Controls

# 128

Certified global regret

# 0.0002044

The first task included 129 screening readings, 32 task-directed proposal readings and 129 audit readings. All 128 hidden-source gradients were contained in the independently computed intervals.

The certificate applies to all allowed continuous dose allocations, not just the interventions tested.

When a later task changed the intervention prices, the retained readings initially gave a regret certificate of approximately 0.01638. Targeted line-search experiments and fresh audits reduced this to 0.0003003. The cumulative source cost reached 932 scalar reactions.

This demonstrates two distinct capabilities: transferring earlier scalar evidence to a new objective, and acquiring precisely the additional information that a changed objective requires. Unlike the earlier source-expiry results, this latter operation requires continuing access to the source.

### Decisive obstruction: hidden threshold activations

I then constructed 124 alternative physical sources that remain exactly indistinguishable across all 932 historical experiments.

Each alternative includes an initially invisible, monotone conductance activation of the form

\\[ 50\bigl(u_j-0.1\bigr)\_+^3. \\]

These sources remain passive and positive definite, and satisfy the same declared first- and second-derivative magnitude limits. They violate the global matrix-concavity assumption.

Because the total allowable dose is 0.2, an experiment can activate at most one such hidden threshold at a time.

The exact construction gives:

- 124 activation positions still untested above threshold.
- A full-dose scalar-reaction difference of exactly 0.05 when the hidden position is tested.
- A worst-case regret lower bound of 0.0005089 for any single intervention policy over these compatible alternatives, using the established reward bound for the baseline source.

Consequently, passivity, monotone actuation and derivative magnitude limits do not suffice to retain the 0.0003003 global certificate.

This is a physical-excitation information limit: no more sophisticated algebraic reconstruction can distinguish an activation that every allowed historical experiment has failed to excite.

### Next executed attack: changing the physical measurement capability

The threshold obstruction suggests an intervention-design opportunity: increase the allowable dose so that multiple candidate actuators can be tested together.

I tested this on the exact-rational four-node model, assuming at most one hidden activation and an additional trusted predictor for the gate-free reaction.

| Total dose budget | Positions tested together | Reactions to rule out all 124 gates |
| ----------------- | ------------------------- | ----------------------------------- |
| 0.2 — original    | 1                         | 124                                 |
| 0.4               | 3                         | 42                                  |
| 0.6               | 5                         | 25                                  |
| 1.0               | 9                         | 14                                  |

At an individual test dose of 0.101, the hidden activation produces a raw-reaction difference of \\(5\times10^{-8}\\), exceeding twice the specified sensor-error allowance. The grouped detection procedure therefore works under deterministic bounded error for this finite candidate family.

The larger budgets and trusted baseline predictor are additional capabilities, not features of the original experiment. The result does not evade the original 124-query lower bound. It identifies the physical change needed to make pooled discovery possible.

### Verification and preserved research

An independently implemented determinant/Cramer's-rule verifier reproduced all 932 scalar observations, six global intervention certificates, 768 gradient inclusions and the 124-source indistinguishability construction.

The full result and executed programmes are preserved:

Complete scientific arguments and findings

Physical assumptions, conditional theorems, experiment costs, counterexamples and proofs of the information limits.

Source-only acquisition · Adaptive intervention research

Independent verifier · Verification results

Dose-pooling experiment · Executed results

The strongest unresolved scientific problem is now precise: how to acquire or independently warrant global physical response-shape constraints cheaply enough that future interventions can be certified without exhaustive high-dose testing.

The construction broadens the operational scope of Astra's reusable learning, but it does not establish a new physical law, a general model-class discovery algorithm or a civilisation-level breakthrough. The Astra GitHub repository has not been modified.