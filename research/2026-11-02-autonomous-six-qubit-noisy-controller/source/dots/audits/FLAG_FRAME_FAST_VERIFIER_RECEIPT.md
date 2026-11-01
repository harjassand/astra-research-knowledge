# Independent whole-mechanism receipt: flag frame and fast physical verifier

2026-11-01. Reviewed root `ROOT_FLAG_FRAME_FAST_VERIFIER.md`, SHA256 9891c4058793a1466349b995a5d43a3e27e7776b7c3762e6750c085f38fd9750, and `producer-workspace/05_flag_xor_fast_verifier_proof.md`, SHA256 4f6832354fd6967c65e10aaf2b2adc1e684955a955d87b893abc1c26d1350bc1.

## Result

**Conditional mathematical PASS for the generator mechanism and its full protected-memory join under the explicit conditions below.** No rearm/stale-permission counterexample survives the displayed fast-repair inequality. This does not supply a fully native two-body quantum device: actual QND stabilizer sensing, physical dissipative gate primitives, finite local circuit constants, noise admission, initialization and ideal readout remain explicit resources. The theorem is not accepted under unspecified sensor rates or uncharged sensing errors.

## 1. Physical XOR flags and local circuit assumptions

For every fixed candidate witness mask x_j, the CNOT frame F_flags sends physical roots (a,b) to virtual witness y=a XOR M b. A single physical X_bj is therefore an old witness-mask X_xj times an auxiliary flag flip after undoing this frame. There is no stored sequence or finite history buffer to overflow. All relevant masks commute as witness-X operators; overlap does not require a transaction mutex.

For a fixed Tanner degree and local selector, the candidate mask list, masks touching each witness, circuit size/depth, fanout, truth-table weights, and physical support can all be finite constants independent of n. They may be enormous. This bounded-family requirement is essential: an n-growing shared verification DAG would not earn a constant-rate/constant-overhead theorem. One may use separate local bounded-fan-in circuits and copies rather than assuming a free global one-hot selector.

Every true permission must use the ACTUAL physical stabilizer labels and virtual witnesses. Cached syndrome inputs are ordinary physical wire variables with their own repair constraints. E=0 then implies the intended predicates by induction through the DAG; this is not a trusted-input assumption.

## 2. Repair and permission accounting

Choose weights w_i>=1+sum_(direct children)w_child, counting each child affected by the output flip. Repairing a violated output changes no roots and lowers E by at least one. At most one parent-pattern repair jump at a gate is enabled in a configuration. Thus sum e_i>=E/w_max yields L_repair E<=-gamma E/w_max when every repair, INCLUDING syndrome-input repair, has rate at least gamma.

If actual sensor rates are slower than Boolean-gate rates, the proof must use the applicable minimum rate or the exact weighted sum of per-gate repair contributions. Fast classical gates alone cannot substitute for the assumed fast sensor term. Equivalently one may slow kappa relative to a fixed sensor rate; that remains a charged potentially terrible constant. No free acceleration of quantum measurement follows.

If a terminal output differs from the ideal DAG evaluated on the actual roots, at least one of its ancestor constraints is violated. Let R bound how many permission outputs can be descendants of one violation in the actual circuit layout. Then both false-positive and false-negative counts are <=R sum e_i<=R E. Therefore correct enabled count is >=cW_v-RE. This inequality is still usable when its right side is negative, because its coefficient in the drift bound is negative.

Let B bound the change of E under a flag flip and D bound the change of W_v. B counts only actually changed local constraint inputs, with their actual weights, including XOR preprocessing. Choose epsilon B<1 and put a0=1-epsilon B, A0=D+epsilon B. Correct enabled flips lower Q=W_v+epsilon E by at least a0; false positives raise it by at most A0. The exact mean bound follows:

    L*Q <=-kappa a0 c W_v
       -[gamma epsilon/w_max-kappa R(a0+A0)]E.

Since a0+A0=D+1, the strict condition is gamma epsilon/w_max>kappa R(D+1). A reverse toggle caused by a stale permission is a false positive already counted here. Nothing assumes each erroneous actuation is downhill.

## 3. Exact exponential drift—not a mean-only argument

Each branch is a single conditional Pauli/bit flip L=sqrt(rate)T Pi on a commuting label algebra. Hence L†FL-L†LF equals its diagonal source rate times exp(alpha Q_after)-exp(alpha Q_before). For quantum syndrome-input repairs the same identity holds using actual commuting check projectors, with support weight(S)+1.

For F=exp(alpha Q), define

    u=kappa c(1-exp(-alpha a0)),
    v=gamma(1-exp(-alpha epsilon))/w_max
       -kappa R[(1-exp(-alpha a0))+(exp(alpha A0)-1)].

The exact pointwise and therefore operator inequality is

    F^-1/2 L_ideal*F F^-1/2 <=-u W_v-v E.

The strict mean-rate condition implies v>0 for sufficiently small fixed alpha>0 by its derivative at zero; u>0 as well. Let mu=min(u,v/epsilon)>0. Then L_ideal*F<=-mu QF throughout the old safe virtual basin, for ALL coherent wire/flag/gauge states. No time-accumulated microscopic approximation or stochastic replacement of coherent external noise has been made.

This direct diagonal computation is stronger and simpler here than importing the noncommuting-current exponential expansion. It is valid because Q, source projectors and the actual stabilizer/register labels commute.

## 4. Ground mapping is correct, but new stabilizer structure is unnecessary

Applying U_DAG† in reverse topological order maps every arbitrary wire assignment to its ORIGINAL violation bits: parents have not yet been changed when their child's inverse gate is applied. Hence E=U_DAG(sum_i w_i n_i)U_DAG†. U_DAG leaves roots and actual stabilizers fixed and commutes with W_v. The displayed identity

    Q=U_DAG F_flags [W+epsilon sum_i w_i n_i]F_flags†U_DAG†

and its ground-space consequence are correct, including coherent states. U_DAG may be non-Clifford. Its optional distance claim is conditional on a bounded-depth/support/incidence circuit and uses arbitrary-operator support expansion, not preservation of Paulis. No new Pauli stabilizer code should be inferred merely from this identity.

For the lifetime join there is a safer direct route. Undo ONLY F_flags. Physical local Paulis then become old system/witness Paulis times flag/wire Paulis, with a bounded old-system support expansion determined by actual masks/incidence. Define the old admitted alphabet to include these projected operators and the ideal branches' components. All these supports remain fixed with n; the previous old-component barrier proof still applies with the updated support constants and sufficiently large n.

The new below-Q-cutoff connected component projects into the old below-W component because W_v<=Q along every path. Old protected flatness therefore handles every projected edge. Boolean repairs change only auxiliary wires. Their controls become functions of old actual stabilizers, witness Z operators, and auxiliary records. In the old low component, these bounded-support operators act only on syndrome/gauge, not protected information. Actual stabilizers and witness Z may measure gauge values; they need not be central as long as this already-earned logical triviality is retained. Sensor branches obey the same rule. Flag actuation projects to an admitted old witness mask. Thus ALL reflected branches are protected-logical identity tensor syndrome/gauge/record operations.

This proves the needed coherent logical statement without pretending U_DAG conjugates a physical Pauli into one Pauli or requiring a new minimum-weight oracle.

## 5. Censoring uphill ideal branches is legitimate

Let P select the full connected component below Q<B_n=beta n, with the complete admitted Pauli alphabet. P and F commute. An actual edge leaving P must have endpoint Q>=B_n; otherwise it would belong to the same component. Its source is below cutoff, so the outgoing edge is UPHILL in Q.

For a conditional-Pauli branch T Pi, J†J is diagonal and its source partitions into retained and exiting configurations. Censoring the exit removes its positive exponential increment. Therefore the reflected ideal generator obeys the SAME or a stronger exponential drift inequality. This is not the assertion that the original ideal and reflected generators coincide—they generally do NOT, because wrong flag actuations can exit (the stated repair branches themselves are downhill).

Consequently the actual/reflected comparison MUST include every ideal boundary-producing branch. Define the charged bound

    Gamma_ideal n >= sum_(all ideal branches) ||L_branch||^2.

For a two-input Boolean repair there are at most four parent-pattern branches; a syndrome-input repair has two check-sign branches; each permission actuator is one branch. Thus the actual finite gate/sensor/flag counts give a finite O(n) Gamma_ideal, including their gamma/kappa rates. This constant can be enormous. An average enabled-rate count cannot silently replace this conservative norm sum in the comparison.

For external local Hamiltonian and dissipative noise with budgets h n and Gamma_noise n, and maximum local Q increment b_Q, the previous general TWO-step-shell proof gives

    ||rho_actual(T)-rho_ref(T)||_1
      <=n[2h+4(Gamma_ideal+Gamma_noise)]
           integral_0^T sqrt(p_shell(t))dt,

with shell Q>=beta n-2b_Q. This safe bound applies to all ideal branches too; special conditional branches could admit a tighter one-step estimate, but no such improvement is required. References and the previously qualified bath extensions are included.

## 6. Full Foster/noise/lifetime conditions

Take fixed 0<theta<beta. The reflected ideal inequality -mu QF implies

    L_ref,ideal*F<=-mu theta n F
                    +mu theta n exp(alpha theta n)I.

Let the ACTUAL coherent/bath and dissipative perturbations earn a weighted bound nu(alpha)n F, including all new flags, wires, sensors and their supports. For this commuting Q one may directly use the earlier Pauli-increment bounds with b_Q and explicitly paid coefficient sums. Alternatively the general local-conjugation bounds suffice. Require nu(alpha)<=mu theta/2. Then k=mu theta/2 gives

    L_ref*F<=-k n F+2k n exp(alpha theta n)I.

For a properly encoded Q=0 input, the initial F moment is one and

    p_shell(t)<=3 exp[-alpha((beta-theta)n-2b_Q)].

Thus decoded error is at most

    sqrt(3)n[2h+4(Gamma_ideal+Gamma_noise)]T
      exp(alpha b_Q) exp[-alpha(beta-theta)n/2].

This supplies an exponentially long interval with vanishing error at fixed family/rate constants. It is a FULL conditional theorem statement, not merely a positive mean drift result. Other initialization is allowed only with a proved initial logical admission and component/exponential-moment tail bound; arbitrary hot or correlated metadata is not automatically covered.

Noise proportional to fast repair rates is NOT free. Either the displayed weighted budget must be checked for that physical model, or finer wire-specific Q-increment bounds must be proved. The small epsilon can reduce wire-energy injection, but the two reviewed drafts do not by themselves establish an arbitrary fixed fractional gate-error model uniformly over changes in gamma. In particular no practical rate/accuracy advantage follows just by increasing gamma.

## 7. Initial preparation, terminal consumer, and resource contract

The exact ground mapping supplies an ideal encoded initial subsystem, but preparation of its flags and consistent physical circuits is a charged operation. The lifetime theorem does not encode an unknown input or manufacture consistent quantum syndrome caches for free.

Terminal logical readout can undo F_flags, then apply the already received old witness-frame Clifford and source Tanner ideal decoder, discarding the verifier wires and flags. Inverting nonlinear U_DAG is unnecessary for protected information: after the flag frame it acts only on old gauge/syndrome and auxiliary records. The old decoder-radius shrink must use the updated projected move support/component constants. This remains an IDEAL terminal consumer, not noisy hardware readout.

Quantum-check repair still acts on weight(S)+1 physical qubits and must be available at its stated rate and noise level. The same service is granted to the active comparator. Classical repair uses at most three-bit dissipative primitives and actuation uses two-bit primitives; this is not a proof that every quantum interaction or reservoir has become native two-body. Hardware count, gate incidence, reset resources, QND backaction, routing, and all noise on those resources remain charged. No Euclidean-locality or useful finite-code claim is earned.

## Numerical check and closure

Independently ran the provided `check_flag_verifier.py`: all 4096 configurations passed, including stale reverse toggles and the inverse-DAG identity. Its mean/exponential comparisons use FLOATING-POINT arithmetic with tolerance 1e-9 despite the printed word 'exact'; this receipt treats it as finite numerical enumeration, not an exact-arithmetic proof. The operator and generator arguments above are the proof. No physical source experiment or lifetime simulation was performed.

The mechanism is mathematically different from a transaction verifier demanding every wrong commit be downhill. Small consistency energy plus sufficiently fast REAL repair closes that obstruction at the generator level. Acceptance is conditional on the explicit quantum-sensor service, finite local circuit constants, weighted physical-noise admission and initialization/ideal-readout contract stated above. Within that contract, no remaining algebraic or logical-join blocker was found. Practical implementation and matched-comparator advantage remain unearned.
