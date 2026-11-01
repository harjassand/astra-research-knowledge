# Weighted-rate FLAG-XOR / Poisson-sensor mean join

2026-11-01. Uses the actual source generator and corrected armed-mask identities in `producer-workspace/POISSON_SENSOR_ADMISSION.md`. Those identities are earned ONLY on the collision-safe legal-clock sector. The derivation below preserves that restriction. No access-stopped work was retrieved.

## 1. Registers, rates and exact leakage counts

Let W be the witness potential evaluated on the dressed TRUE stabilizers and virtual FLAG-XOR witnesses. Let e_s be the mismatch projector of physical sensor cache s against its dressed true stabilizer, and r_s its corrected armed/unmarked probe defect. Let E=sum_i w_i e_i^B sum BOOLEAN-DAG consistency violations only; the quantum sensor-root mismatch is not included as a native gate repair.

Choose finite positive DAG weights with
 delta_i = w_i-sum_(direct children k) w_k >0.
A gate-output repair at its actual rate gamma_i leaves W and all sensor prices unchanged and contributes
 L_i(E) <= -gamma_i delta_i e_i^B.

Let R_i count permission outputs that a violation at Boolean gate i can corrupt, and R_s the permission outputs downstream of cached syndrome s. A wrong output requires at least one Boolean violation or an erroneous actual sensor root. Consequently
 N_false_positive,N_false_negative
 <= sum_i R_i e_i^B + sum_s R_s e_s.
The statement is pointwise in the commuting witness/cache/Boolean-label algebra and hence an operator inequality. It does not declare probes or arbitrary noise classical.

At rate kappa per candidate, flag actuation has at least cW true improving opportunities. Let D bound |Delta W|, and B_act bound |Delta E| under one flag flip. Choose a Boolean price epsilon>0 with
 a0=1-epsilon B_act>0, A0=D+epsilon B_act.
Actuation then obeys
 L_act(W+epsilon E)
 <= -kappa a0 cW + K_act[sum_i R_i e_i^B+sum_s R_s e_s],
 K_act=kappa(a0+A0).

Crucially: flag flips change W's virtual witnesses but do NOT change actual stabilizers, sensor clock/mark variables, probe prefixes, caches, e_s or r_s. They therefore change NO sensor-price term. There is no actuator debt proportional to t_max or xi_max.

## 2. Cache-overwrite leakage requires an extra Poisson reward

Let B_s bound the increase of E when physical cache s flips; explicitly it is no more than the sum of weights of Boolean constraints directly reading that cache. Let lambda_s(x) be the ACTUAL total hazard of accepted target-s readout from source state x in the finite source generator. Set
 h_s(x)=epsilon B_s lambda_s(x).

At an accepted readout the probability/operator for changing the cache is
 (I-Z_cache X_probe)/2 = e_s+r_s-2e_s r_s <= e_s+r_s.
This uses the source's accepted-branch identity Sbar_s=S_s and commuting e_s,r_s. Thus
 L_cache(epsilon E) <= sum_s h_s(x)(e_s+r_s).

The original sensor price t e+xi r cancels its own g r gain but does NOT automatically cancel this extra Boolean leakage. Discarding the r_s term would be incorrect. Price it with the SAME specified finite killed generators, using new reward vectors as follows.

## 3. Actual weighted Poisson equations

Choose target sensor restoring coefficients A_s>0 and optional probe-restoring coefficients H_s>=0. Solve on the actual legal source state space
 t_s = -K_(A,s)^(-1) [A_s+h_s],
 g_s(x)=sum_(accepted x->y) q_xy t_s(y),
 xi_s = -K_(D,s)^(-1) [g_s+h_s+H_s].
The last reward is restricted to the armed-unmarked domain; xi_s=0 outside it. K_A and K_D are EXACTLY the finite killed generators already specified by the sensor source. Positivity/transience give finite nonnegative coefficients. In particular
 t_s=A_s t_s^(0)+[-K_A^(-1)h_s],
so this is a computable weighted-rate join, not an assumption of a universal minimum sensor gamma.

For P_s=t_s e_s+xi_s r_s, the source transport, accepted-readout and preparation identities yield
 L_source P_s
 = -(A_s+h_s)e_s -(h_s+H_s)r_s + b_s(x) I,
 b_s(x)=sum_(preparation x->y) q_xy epsilon_p,s xi_s(y).
Here epsilon_p,s is the actual probe-preparation impurity; it is not the Boolean price epsilon. The gain g_s uses POST-readout t_s(y), not the source value.

Adding Boolean cache leakage cancels both h_s e_s and h_s r_s exactly in the inequality. For independent readout flip probability eta_s<=1/2, add the upper floor
 eta_s[g_s,max+h_s,max].
The first term prices the sensor error and the second Boolean cache leakage. General detector/helper noise is not replaced by this independent-flip model.

An explicit conservative per-sensor floor is
 f_s = lambda_prep,s^max epsilon_p,s xi_s,max
       + eta_s(g_s,max+h_s,max).
The actual state-dependent b_s may be used for a sharper bound.

## 4. Full legal-sector mean join at heterogeneous rates

Define the positive physical potential
 Q = W + epsilon E + sum_s P_s.
It includes all physical flags, Boolean wires, sensor clocks, caches and probe defects through their stated energies; no clean controller is presumed. Combining the ACTUAL generators gives, on the admitted legal sector,

 L_ideal Q <= -kappa a0 cW
 -sum_i [epsilon gamma_i delta_i-K_act R_i] e_i^B
 -sum_s [A_s-K_act R_s] e_s
 -sum_s H_s r_s + (sum_s f_s) I.

This is the requested direct weighted-rate inequality. Sufficient explicit choices for margins rho>0 and sigma_s>0 are
 gamma_i >= [K_act R_i+rho w_i]/(epsilon delta_i),
 A_s >= K_act R_s+sigma_s.
No quantum source rate is required to exceed these gamma_i. Slower sources instead produce larger computed t_s and xi_s through their killed-generator inverses.

If H_s>0, put
 lambda = min{ kappa a0 c, rho/epsilon,
                min_s sigma_s/t_s,max,
                min_(s:xi_s,max>0) H_s/xi_s,max }.
Then positivity implies the legal-sector Foster inequality
 L_ideal Q <= -lambda Q + (sum_s f_s) I.
Terms with zero price coefficient are omitted. Choosing H_s=0 suffices for the preceding exact W/E/cache inequality but generally does NOT give -lambda Q, because a currently hidden probe defect can have positive xi_s r_s while e_s=0. The optional H_s reward explicitly fixes this issue and increases its preparation floor accordingly.

## 5. Physical noise and the illegal-sector gate remain explicit

Write the ACTUAL generator, without inventing a classical fault process, as
 L_actual Q <= -lambda Q + (sum_s f_s) I
                 + R_illegal + R_hardware.
R_illegal contains precisely the unproved invalid-clock/interference/mask effects from the source admission, now with the larger actual t_s,xi_s. This note does NOT dominate it or replace invalid states by legal phase labels. A separate positive illegal-state penalty and actual repair estimate are still required.

R_hardware is the adjoint action of the actual additional local Hamiltonian/dissipative terms, including noisy flag actuators and Boolean gates, on Q. If local termwise bounds give R_hardware<=nu_Q n I, the admitted legal mean floor is sum_s f_s+nu_Q n. A miscalibrated jump's difference includes bilinear cross terms; it must be bounded as the actual generator difference, not declared a positive added dissipator. Large prices increase these local norm bounds.

The P_s can fail to commute with one another on illegal overlap states. No global commuting-potential exponential argument is asserted. Mean Foster drift alone is not exponential memory protection; the illegal-sector and exponential rare-event interfaces remain real proof gates.

## 6. Do large sensor prices destroy the density allowance?

Not automatically, but they reduce the available operating region. Let the safe boundary be Q<beta n and choose an interior target theta n with theta<beta. A necessary mean-scale operating inequality is
 [(sum_s f_s)/n+nu_Q]/lambda < theta.
Initial sensor/Boolean preparation also needs the appropriate density/tail admission; mean control is not a tail theorem. For example, a finite density q of sensor defects with price t_max can already contribute O(t_max q n) to Q. Raising t_max while holding q fixed can violate the same beta cutoff. One cannot simply increase the cutoff beyond the inherited safe-W threshold because W<=Q is the link protecting that component.

There is a useful rate tradeoff. If all sensor-generator rates are scaled by r_s, then K_A,K_D scale by r_s. For fixed reward A_s, t_s and xi_s have A_s/r_s contributions. h_s scales as epsilon r_s B_s, so its contribution to t_s is O(epsilon B_s), not O(1/r_s). Choosing A_s,sigma_s,H_s=O(kappa) and epsilon=O(kappa/gamma_classical) makes source prices roughly O(kappa/r_s)+O(kappa B_s/gamma_classical). Thus slowing the flag actuation relative to the sensors can prevent huge sensor weights, without demanding fast quantum measurements. The finite graph/circuit constants must still be inserted; this is scaling algebra, not a favorable numerical estimate.

The tradeoff is NOT free: lambda is at most O(kappa), so fixed nonzero hardware noise must remain below the resulting kappa-dependent budget. One cannot take kappa->0 while keeping an arbitrary fixed physical noise rate and claim protection. Finite preparation/readout floors also remain and must meet the density inequality above. Faster classical repair can be used selectively via the actual gamma_i formula rather than imposing that rate on every quantum sensor.

## 7. Same-resource comparison and earned scope

The active Tanner comparator receives the same physical syndrome sensors, their acceptance hazards/purity, all flags/wires, connectivity and classical rates. The potential distinction is an autonomous whole-apparatus mean admission; no resource advantage has been established.

Earned here: the explicit weighted Poisson re-pricing, cancellation of both cache-mismatch and bad-probe Boolean leakage, heterogeneous-rate generator inequality, and the necessary price/noise/density tradeoff. Unclosed: illegal source sectors, global exponential lifting, microscopic native synthesis beyond the admitted primitive list, and useful finite constants. The frozen clock and prior flag-XOR artifacts are unchanged.
