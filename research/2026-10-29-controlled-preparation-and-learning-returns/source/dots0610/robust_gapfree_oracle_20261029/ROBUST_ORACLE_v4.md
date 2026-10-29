# Robust task-loss oracle inequality for gap-free quantum encoder learning
2026-10-29. New additive theorem; does not modify the accepted v1–v3 files. Receiving review pending.

## Scope and inherited interfaces
Use the same finite rational star-frame experts, actual product-Pauli probe bank, physical permutation orbit, matching validation and arbitrary-error outer corrector as the accepted gap-free construction. All current candidate draws and role/key choices remain private and independent of the pre-call source map. The source can retain arbitrary causal quantum memory, be nonunital and change over time. No exact collective-algebra promise is imposed in this theorem.

Instead compare with ONE fixed tuple C* of relative site rotations, fixed independently of the realized records and coins. Losses below are evaluated on the ACTUAL conditional source-memory histories induced by the learner, not the histories that a different controller would have induced. This is not policy regret, environment identification, or competition with the best encoder's actual fidelity.

The earlier positive source-exposure-rate example n=4log2 B is explicitly a scalable FAMILY OF PORTS. It is not a capacity/rate theorem for one fixed-n physical port. The present fixed-n robustness thresholds are finite-operation statements; they do not silently supply an arbitrary-length fixed-alphabet outer-code compiler.

## Positive loss and arbitrary-source memory effects
For each star edge i and candidate C let S_i(C) be its Hermitian unitary twisted swap. At actual observed history H_t, let K_{t,a} be the complete data-memory source Kraus operators. Define the positive memory operator
 E_{i,t}(C)=(1/(2D)) Tr_X sum_a [K_{t,a}, S_i(C) tensor I]†[K_{t,a}, S_i(C) tensor I], D=2^n.
For the actual pre-call memory marginal sigma_t,
 delta_{i,t}(C)=Tr[sigma_t E_{i,t}(C)] in[0,2].
The probe estimator remains unbiased for this quantity. The already established Poincare/orbit inequality holds for arbitrary source Kraus operators:
 H_bad(C) <= alpha_n sum_i E_{i,t}(C_i), alpha_n=D/d.
Consequently it applies even when current outer logical symbols are correlated with source memory. No exact symmetry is used for this transfer or for the matching inequality q_match<=p_raw.

## Approximation inequality without a common zero
Write Delta S=S_i(C)−S_i(C*). The commutator vectors in the Hilbert direct sum of Kraus Hilbert-Schmidt spaces, weighted by sigma_t, obey the triangle inequality. Their normalized squared norms are the losses. Trace preservation gives
 (1/(2D)) sum_a ||[K_{t,a},Delta S tensor I](I_X tensor sqrt(sigma_t))||_F²
 <=2||Delta S||op² <=(9/2)||C−C*||_F².
This can also be seen by taking the reduced CPTP channel for sigma_t and applying the ordinary Kraus commutator bound. Thus for every gamma>0,
 delta_{i,t}(C) <=(1+gamma)delta_{i,t}(C*)
                  +(1+1/gamma)(9/2)||C−C*||_F².
No action-dependent comparator or exact zero is required.

Take a fixed nearest net point Cbar_i for each C_i*, of radius epsilon. Define
 Gamma_T(C*) = E sum_{t<=T,i} delta_{i,t}(C_i*),
 A_T=(9/2)(n−1)epsilon²T.
Use the same zero-loss mathematical continuation after stopping as in v3; neither future source access nor physical extra calls are introduced. Summing the preceding inequality and optimizing gamma gives
 E sum_{t,i} delta_{i,t}(Cbar_i) <=(sqrt(Gamma_T)+sqrt(A_T))².
When Gamma_T=0 this follows by the exact-zero bound or gamma→infinity. One may instead keep any predetermined gamma if a simpler fully rational upper bound is wanted.

## Finite learner oracle inequality
The exact rational multiplicative-weight learner from v2 gives per edge regret
 R_T=45[ln M/eta+eta T/p], eta<=p/2,
relative to every fixed net comparator, on this adaptive but nonanticipating actual history. Therefore
 E sum_{t,i} delta_{i,t}(C_{i,t})
 <= G_T(C*) := Gamma_T +2sqrt(Gamma_T A_T)+A_T+(n−1)R_T.  (1)
All physical controls, exact integer updates and capped sampling remain as charged in v2. The capped exact sampler can be handled directly on actual stopped histories. Conditional on the current integer weights, each binary rejection attempt accepts a uniform integer in the weight-sum interval; its accepted integer is independent of its rejection count. Thus the cap-abort event is independent of the accepted candidate index. This holds edge by edge and hence jointly. Equivalently draw the candidate-independent abort/count coins first, then draw candidates only if all caps succeed. Abort is a neutral stop, with zero loss and no feedback thereafter. The same online proof applies to this stopped loss process, and Gamma_T therefore refers to the actual capped protocol, not an unbounded counterfactual continuation. The separate probability of sampler-abort is at most delta_sampler and is charged in readiness. No conditioning on success is used to infer unchanged unconditioned loss expectations.

The inequality holds for each fixed comparator. Hence it also holds with the infimum over deterministic comparator choices of the RIGHT-HAND EXPECTATION. It does not imply a bound against the random hindsight minimum E[min_C sum_t delta_t(C)], nor against a data-selected frame without further uniform concentration. The actual-history source process in Gamma_T is the learner's process for every such comparison.

Set epsilon=T^(−1/4) and the finite learning rate of v2. Then A_T=O((n−1)sqrt T) and R_T=O(sqrt(T logT/p)+logT/p). If Gamma_T<=gT with fixed n and p, G_T/T<=g+O(sqrt(g)T^(−1/4))+O(sqrt(logT/T)). Thus exact-zero is a special case, while approximate symmetry gives an asymptotically faithful aggregate-loss comparison.

For a sharper robust excess rate when the defect is nonzero, choose epsilon=T^(−1/2) instead. Then A_T=(9/2)(n−1), M=O(T^(3/2)), and the excess over Gamma_T is O(sqrt(Gamma_T)+sqrt(T logT)) for fixed n,p. Since Gamma_T<=2(n−1)T, this is O(sqrt(T logT)) uniformly. The price is a larger finite net and larger exact arithmetic. The smaller original net remains preferable for its exact-zero computational advantage; neither implementation is claimed optimal.

## Operational consequences: same guard, broader readiness condition
For the v3 roles p+a+s=1, capT, targetJ services and failure budgetb,
 E validation failures <=a alpha_n G_T,
 E virtual bad services <=s alpha_n G_T.
If J<=sT/2, the identical Markov and private-role Chernoff argument gives
 Pr[ready by cap] >=1−a alpha_n G_T/(b+1)−exp(−sT/8)−delta_sampler. (2)
Clip the lower bound at zero. A valid deterministic upper budget on Gamma_T may be substituted into this monotone formula. The competing-risk guard and accepted-map soundness remain MODEL FREE and unchanged; low defect is used only for readiness. Source control/calibration error budgets remain separate unless explicitly included in the complete source Kraus map at the declared interface.

For a desired non-readiness allowance xi, put
 V_T=(b+1)[xi−exp(−sT/8)−delta_sampler]/(a alpha_n)−(n−1)R_T.
Whenever V_T>=A_T and the bracket is positive, it is sufficient that
 Gamma_T <=(sqrt(V_T)−sqrt(A_T))². (3)
This is a finite-cap fixed-n defect tolerance, with no asymptotic outer-code assumption. Rational conservative square-root bounds can evaluate it without an exact real oracle.

To interpret rather than assert a new coding theorem, suppose b≈nu B,T=cB and J=B<=sT/2 for an available compatible outer code. If Gamma_T<=gT, (2) has asymptotic failure term a alpha_n c g/nu. A sufficiently small CONSTANT g yields a positive readiness lower bound bounded away from zero; it does NOT yield readiness tending to one. For readiness tending to one under this argument, the average defect must tend to zero. Extending this limit at fixed n requires its own unbounded-length fixed-alphabet outer-code family, not the inherited full-field construction with growing n.

## What the oracle objective does not measure
A channel can act perfectly on the intended singlet subspace while having large star commutator loss elsewhere. Since these losses are normalized over the entire physical data space, (1) can be conservative. It is not a comparison against the best actual logical fidelity, best recovery, or optimal quantum memory architecture. An arbitrary future source can become high-defect after a benign training period; this theorem concerns the guarded actual operation and does not certify that future source.
