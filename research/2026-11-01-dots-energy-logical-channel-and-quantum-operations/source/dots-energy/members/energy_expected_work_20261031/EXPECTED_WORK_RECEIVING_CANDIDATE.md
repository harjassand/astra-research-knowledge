# Receiving energy flow as an actual expected execution budget

31 October2026. Root candidate, pending independent review. This is a resource-accounting corollary of an ALREADY ACQUIRED complete first-event algorithm. The elementary energy inequality alone does not construct that algorithm. No practical crossover, free dilation, free preparation or thermodynamic-energy identification is asserted.

## 1. Elementary all-rate energy estimate

Let G=sum_j D[L_j], H=sum_j L_j†L_j/2, and G†H<=-kappa H. Consider lambda G-i[H_comm+sqrt(lambda)V,.], with every additional Hamiltonian in H_comm commuting with H. Let C be an actually certified upper bound on ||sqrt(H)V||. For a joint state, including arbitrary reference,

E=Tr(H rho),
|Tr(i[V,H]rho)|<=2 C sqrt(E).

Purification and Cauchy-Schwarz in the H^(1/2) form prove this directly. Young's inequality therefore gives

E'<=-(lambda kappa/2)E+2C²/kappa.

At prescribed controls require a paid source-energy budget: the sum of positive changes in expected H is at most D_ctrl. Sufficient uniform certificates are C_j†(H)<=H+d_j I with nonnegative d_j and D_ctrl=sum_j d_j. System-only trace-preserving instruments have d_j=0, including their retained outcome records. Outcome-conditioned feedback must obey the stated uniform budget; conditioning on rare outcomes is not free.

The physical jump compensator is 2lambda E. Integrating over the intervals and discarding nonnegative final energy gives

E N(T)<=Xi_C:=4[E(0)+D_ctrl]/kappa+8C²T/kappa².

At lambda=0 the actual count is zero. This estimate is valid without a high-rate assumption. It is a count of the chosen Lindblad unraveling, not a count of classical Glauber flips or an accessible heat record. H is the declared Lyapunov operator; it need not be a physical thermodynamic Hamiltonian. C must come from an actual structural bound or paid operator access; its optimal value is not an oracle.

## 2. Stronger high-rate injection certificate when available

Under the separately reviewed energy-form inputs r_E and a_E, and sqrt(lambda)>=8a_E/kappa, the tilted weight W=I+4uH/kappa satisfies the accepted native count drift for u=e^theta-1<=min(1,kappa/(16h)). If the initial source energy is bounded by E0 and each control has the operator injection bound d_j,

E exp(theta N(T))
 <=(1+4u E0/kappa) product_j(1+4u d_j/kappa)
       exp(32u r_E²T/kappa²)
 <=exp(u Lambda_E),
Lambda_E=4(E0+D_ctrl)/kappa+32r_E²T/kappa².

This uses C_j†W<=W+(4u d_j/kappa)I<=(1+4u d_j/kappa)W. Differentiating the right-sided inequality at theta=0 is legitimate for the finite bounded-source model and gives E N<=Lambda_E. Alternatively, a direct differential proof at the weaker threshold sqrt(lambda)>=2a_E/kappa gives E N<=8(E0+D_ctrl)/kappa+32r_E²T/kappa². The different hypotheses/constants must not be conflated.

The global all-rate C estimate and the stronger high-rate r_E estimate have different costs and regimes. Use the best actually certified bound Xi; do not claim uniform domination. Choose an allowed theta and an integer guard M so that Pr(N(T)>=M)<=epsilon/8; adding one to the upward-rounded Chernoff threshold suffices. The exact comparison freezes on the Mth jump, so the event is >=M, not merely >M. The generic frozen native cap may also be retained as a valid, possibly looser, guard. These bounds concern energy-limited inputs if E0<h; the arbitrary-input case is recovered by E0=h and worst permitted control charges.

## 3. The existing operational interface is load-bearing

Assume the native or energy-resolved first-event receiver has actually been acquired with all its source reflections/preparation, jump stack, kernel, interaction ports, finite clocks, coherent word preparation and complete-isometry amplification. A call outputs a private event/no-event decision, the post-event source/system state and private source color; it never resets the source. Its physical count cap M and deterministic window count W give a finite bound S=M+W+2 on executed first-event calls.

The simulator measures its private event/time record after each COMPLETE amplified call, as already allowed by the received construction. It can therefore stop executing calls when the physical horizon is reached. This is classical adaptive execution of a finite CPTP algorithm, not a claim that coherent virtual words have their expected rather than padded cost. Every inner word routine still has its fully paid finite cap, precision and circuit size.

A source jump adds at most one executed call, and fixed no-event window completions add at most W; short-window skips only reduce actual work. Thus actual calls <= private jump counter + W +2. Only that INTEGER jump counter is used in the error proof. We do not compare full private timestamp distributions in TV, nor introduce a discontinuous count of algorithmic skips into a time-Lipschitz claim.

## 4. Explicit counter accuracy gives an expected-cost bound

First fix M using the physical overflow budget epsilon/8, and fix the window schedule. This fixes S before choosing synthesis accuracy. Compare the exact process frozen at M jumps with the finite simulator, retaining the bounded integer jump counter as part of the analysis output. The already received counter-augmented future-channel hybrid applies to this output, with the same generator norm bounds.

Set the total finite-simulation trace error for this augmented channel to

delta_sim=min(epsilon/4,1/[4(1+S)]).

Instantiate ALL counter-affecting implementation tolerances from this delta_sim, not from the original epsilon alone. This includes encodings, first-event/word/clock circuits, synthesis and approximate controls relative to the energy-certified ideal controls. No such error may be left only in an O(epsilon) output budget, because its possible counter-expectation effect is M times that error. This costs additional logarithmic precision; it is not an uncharged assertion that the approximate process has the exact MGF. The count cap itself is not recomputed from delta_sim, so there is no circular definition. An alternative safe convention is to compare against the ACTUALLY executed external instruments and certify their energy charges directly. Only under that convention may a remaining discrepancy from desired target controls be charged separately to the final output rather than delta_sim.

The exact frozen counter is min(N,M), whose expectation is at most Xi. Data processing gives TV distance <=delta_sim/2 between its final counter distribution and the simulator's counter. Since the counter lies in[0,M],

E N_sim <= Xi+(M/2)delta_sim <= Xi+1/8.

Hence

E executed first-event calls <= Xi+W+3.

The final accessible-channel error is at most 2*(epsilon/8)+delta_sim, plus only any remaining target-control discrepancy under the explicitly energy-certified actual-control convention. Allocate that discrepancy to remain <=epsilon; no counter-affecting implementation error is omitted from delta_sim under the default ideal-control comparison. The private integer counter may then be discarded. Full continuous/discrete timestamp TV, which can equal one, is never used.

If a call has an actual worst-case resource vector c_call (queries, arithmetic gates, rotations, fresh work preparation, and any per-call classical angle/clock recompilation as the private remaining window changes), its expected total is at most c_call*(Xi+W+3), plus genuinely one-time paid preprocessing and prescribed controls. Per-call classical acquisition is inside c_call, not silently counted only once. This is an upper bound for a measured adaptive implementation. A padded fixed-depth circuit still has its S-call worst bound. Neither is a lower bound on every simulator, and the two must not be interchanged in a benchmark.

## 5. Worst-window accounting can also price expected H0 action

For a high-rate energy-resolved model let B_off be the ACTUAL acquired crossing normalization squared times T/g. For the accepted slack port QKP/(2rho), this is B_off=4rho²T/g, not rho²T/g. Choose a normalized dyadic window with

D=128B_off+Xi+p+4,   1/(2D)<=tau_max<=1/D.

It satisfies the accepted scalar envelope condition and has W<=ceil(1/tau_max)+p+1. Therefore

(Xi+W+3)tau_max<=1+(Xi+p+5)tau_max,

which is at most 9/4 because D>=Xi+p+4>=4. Charge every padded H0 slot in a call at its WORST duration T*tau_max. The expected H0 query action is then O(alpha_0 T*d_A*(Kcap+1)), plus all per-piece synthesis overhead. This is not a realized-path-duration shortcut: it multiplies a fixed per-call upper cost by the proven expected number of actually executed calls.

Kernel and source costs remain their actual per-call values. Gaussian specialization, geometric clocks, scalar arithmetic or fixed-point amplification may be used only when separately acquired and bound. No gate count is obtained by assigning each kernel slot one unit gate.

## 6. Useful scope, and what is still missing

For an independent stationary CLASSICAL source, preparing psi instead of diag(pi) is a valid representative only under the previously proved source-diagonal adjoint algebra, matching initial system state and permitted classical controls/readout. Its preparation is paid. It is not a replacement for arbitrary correlated CQ inputs or arbitrary quantum-source tasks. For that restricted representative E0=0. System-only instruments add no source-energy charge. The expected-count bound can then depend only on the injected interaction resource, but source size, kernel conditioning, access and precision costs remain.

The work proof receives energy flow only AFTER a complete operational algorithm exists. It does not derive a coherent simulator from a mean count, remove coherent virtual padding by expectation, supply a desired dilation, infer a physical model from data, or transfer a certificate between generators. The current small dense/effective-model comparators still win their fixtures. A useful practical or civilisation-level consequence remains to be established on a fully priced task.
