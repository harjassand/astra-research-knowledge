# Independent whole-theorem receipt: native dilute-sensor join

2026-11-01. **Mathematical PASS for the stated fixed-parameter, bounded-arity engineered-GKSL memory theorem**, subject to the already received specified Tanner-family imports and the explicit encoded-input/ideal-output/noise contract. No remaining algebraic or composition gap was found in this review. This is not a microscopic two-body, useful hardware, or laboratory-threshold certification.

## Frozen inputs and executions

- `NATIVE_DILUTE_SENSOR_MEMORY_JOIN.md`: SHA256 9cf5a250d443a632852327fef40cf854ba5d3f615a0a64dd3c9e91e3116724cf, including section 7's concrete parameter witness.
- `07_dilute_sensor_closed_join.md`: SHA256 c67e6bb137d94d88be80996b4d51f235b50d5f90cebca87ef346f8ae699ff9ab.
- `SMALL_QUBIT_SENSOR_CLOCK_RECEIPT.md`: SHA256 25232396911fc23256961f8664636203fc2123a978551d09e5138035bf00e7d6.
- The previously reviewed flag-frame, dilute source, exact noncommuting exponential, old protected-component, and killed-subchannel derivations.

Independently reran the 180 own/pair/detector Poisson cases and all 16,380 clock configurations for M=1,...,12: both passed. The Poisson script uses numerical linear algebra/tolerances, not exact arithmetic despite some printed wording. The clock combinatorics are finite exact bit/integer checks. These executions supplement the proofs below; neither is a hardware or lifetime simulation.

## 1. Weighted source/Boolean cancellation is exact

For the ACTUAL readout location q and its return phases, the displayed t table satisfies K_A t=-(A_s+h), h=epsilon B_s k at q. Its post-readout value is A_s tau+epsilon B_s. The armed killed equation for g+h gives xi_s=A_s tau+2epsilon B_s, not the unweighted price.

Thus the noncollision source contribution is

    -A_s e_s-h(e_s+r_s)+p_s r xi_s I_idle.

At readout the cache-flip operator is bounded by e_s+r_s plus busy-neighbor indicators. This is an operator inequality: away from overlap the two commuting error projectors give their XOR exactly; on overlap the discrepancy is bounded by identity. Therefore epsilon E's cache-overwrite contribution cancels both negative h terms, including the readiness term that cannot simply be dropped.

Neighbor controlled gates cost k xi_s per busy pair. The decorated readout plus Boolean leakage costs k(t_post+epsilon B_s)=k xi_s. Hence the total collision coefficient is exactly bounded by 2k xi_s per ordered pair. All phase outcomes advance and their instruments are TP, so hazards are not multiplied by the number of Kraus outcomes. These statements cover coherent clocks/probes/data, not merely classical error trajectories.

With epsilon=a/k and the stated gamma_i,

    epsilon gamma_i delta_i
       >=a[(1+D_W)R_i+w_i],

so the Boolean terms leave -aE. Taking A_s=a[(1+D_W)R_s+1] leaves -a sum e_s. The actuation coefficient is at least a c0/2 because epsilon B_act<=1/2. Thus the legal decoded join indeed gives the claimed -cW with c=a c0/2, without requiring the quantum sensors to run at Boolean repair rates.

## 2. Improved Poisson bounds and density constants check

For a pair of private cycles, the sum of remaining busy transitions is <=2D. Until idle/idle is hit, at least one fast transition decreases it at rate k; departures add at most 2Dr. For r<=k/(4D), its drift is <=-k/2. Optional stopping gives mean hitting time <=4D/k. The centered reward's absolute value is <=1, so its normalized hitting solution has magnitude <=4D/k; shifting its minimum gives 0<=H_pair<=8D/k. The equation at idle/idle follows from stationarity and the centered reward, not an extra assumption. The analogous own-clock bound gives H_q<=2D/k.

I checked every term of the displayed C_z,C_p,C_col:

- own source height: t_max+xi<=((5/2)C_A a/r)+3aB/k;
- pair height: 16D xi<=20D C_A a/r+32D aB/k;
- detector height: 2D eta xi, bounded as stated;
- preparation/detector floors: <=a C_p(p+eta);
- pair floor: <=a C_col(r/k), with the extra (r/k)^2 Boolean part conservatively bounded by r/k.

Boolean height epsilon E<=C_E a/r since r<=k. Therefore the stated constants really are independent of a and r, and z<=C_z a/r+z_clk is valid as an operator bound even though readiness terms do not commute mutually. The corrected D=2M+1 and actual post-readout location are used throughout.

## 3. Malformed physical clocks are now paid, not declared legal

The 100 wall guard has exactly one legal successor; endpoint x_M=1 fires on a legal clock only at all ones. Mode flipping complements decoded bits and restarts the next leg at rank zero. The whole legal cycle has 2M+2 states, readout before return, and only the initial preparation departure is slow.

On malformed strings, adjacent 01 sorting preserves rank/mode and lowers inversion I by exactly one. I<=floor(M^2/4)N01, and all positive inversion changes from wall/mode moves originate in malformed states. The bounds |Delta I|<=M-1 for wall flips and <=floor(M^2/4) for mode flips are correct.

Crucially, each separately labelled native clock map is injective on its source configurations. For any clock-diagonal operator-valued potential, its adjoint therefore has no cross terms between distinct physical clock sources. This proves the blockwise estimates on arbitrary coherent clock states, not just diagonal states. The source-labelled decoded reference uses separate full-source Kraus labels; it is analysis-only and need not be a native local operation.

On every legal source, actual and decoded adjoints agree. On every malformed source, the at most M+1 actual channels and one reference channel cost at most D_g=(M+2)k B_g, where B_g uses ONLY affected bounded local terms, including neighboring readiness/pair prices. It must not use ||W||=O(n). Sorting leaves every decoded-phase-dependent term of V0 unchanged. Its negative inversion drift and the stated nonsorting inversion increase give exactly the displayed domination inequality for nu a_clk/C_M.

Thus, after choosing that finite rate, the malformed remainder is nonpositive on ALL apparatus states. Genuine collisions of legal clocks were separately paid by the Poisson price; they were not misclassified as malformed. Legal-to-legal physical faults that skip a gate remain in the noise admission. This closes the former all-malformed-state gap at the stated GKSL level.

## 4. Concrete parameter witness has a strict positive margin

After k=1, section 7 bounds each of

    C_z a/r, z_clk, (2/c0)C_p(p+eta),
    (2/c0)C_col r, (2/c0)nu_V/a

by beta/40. Their sum is therefore <=beta/8. The first two also give z<=beta/20. The bound a<=1/(4B_act) is stronger than the required actuation condition; r<=1/(8D) is stronger than the Poisson condition. Absent terms may be omitted without dividing by zero.

Choose the clock penalty height first, then its finite sorting rate, and evaluate actual perturbation bounds AFTER all those choices. For every resulting finite local hierarchy, generator action on the finite-norm local potential is continuous in local Hamiltonian/jump perturbations. Thus a sufficiently small positive uniform perturbation neighborhood exists. This does not say that a fixed laboratory error-per-sort meets the bound, or that rates can be increased without increasing physical noise.

The actual full mean inequality is consequently

    L*V<=-cV+(b_ideal+nu_V+cz)n,
    (b_ideal+nu_V)/c+z<=beta/8.

The exact noncommuting local expansion, with C2 computed for the ACTUAL selected full generator, permits fixed alpha>0 satisfying C2 alpha/c<=beta/8. Hence f(alpha)<=beta/4. With theta=beta/2, the initial exponent z<=beta/20 and moment ratio theta/(theta-f)<=2 give total moment prefactor <=3. All choices remain independent of n, although their constants and required n can be enormous.

This is a real positive formal barrier margin, not merely finiteness of prices or a mean-decay statement.

## 5. Non-Clifford dressing, component commutation and J†J

For each physical clock configuration assign its actual decoded Pauli prefix. The clock-controlled prefix unitary is local on that clock, probe and bounded check patch. A fixed coloring of the bounded-overlap graph implements their chosen ordering in finite depth. Overlap contributes probe CZ phases, but these commute with later controlled-Pauli gates and complete-check observables; conjugation of each complete stabilizer is exactly Sbar_s. The frame may be non-Clifford because its clock control is nonlinear. Its support light cone is nevertheless a fixed finite constant.

After also undoing the flag frame, W is exactly the old Tanner-witness potential tensored with unused apparatus. Let P be the transported old good-component projector with identity on free apparatus. The sign cancellation makes each readiness term commute with ALL dressed base checks; it also commutes witness/flag Z labels. Clock-diagonal coefficients commute those labels. Boolean, cache, occupation and inversion terms preserve them too. Thus [P,V]=[W,V]=0 globally, including malformed clock configurations, and V>=W.

For any ACTUAL local H, J, or FULL J†J, conjugation by the finite-depth frame yields an operator supported on a fixed expanded old-system/apparatus neighborhood. Expand only its old-system part in Paulis; coefficients may be arbitrary apparatus operators. Enlarge the old admitted alphabet to these actual components. The previous low-component barrier proof depends on their bounded support, not on Cliffordness of the new frame. For sufficiently large n, every old Pauli component with endpoints in the component satisfies the received canonical-representative weight inequality and is protected-logical identity tensor gauge.

This establishes protected factorization for PHP, PJP AND PJ†JP. It is not the false inference that ordinary spatial locality alone implies logical flatness. The full product J†J is essential for the killed-channel completion.

The same expanded support gives a fixed old-W increment bound b_W. Deep-interior one/two-component paths cannot leave the old component, proving the required one- and TWO-step shell annihilation identities. Apparatus coefficients do not change old W after decoding. No one-step anticommutator shortcut is used.

## 6. Exponential output bound and input/readout scope

Killed CP compression therefore inherits the actual exponential Foster inequality. Its subnormalized two-step-shell mass is at most

    3 exp(2alpha b_W) exp(-alpha beta n/2).

The actual-minus-killed comparison counts ALL ideal and noisy terms capable of crossing the cut. Bath-only terms commuting with V and P contribute zero and need not be charged by an infinite environment norm. Finite-system local terms may be counted conservatively. Full protected factorization gives the positive logical deficit even with logical-gauge correlations, so the factor-two output estimate is exactly

    2sqrt(3) n(2h_all+3Gamma_all)T
       exp(alpha b_W) exp(-alpha beta n/4).

Fixed independent bath input gives the usual restricted-code channel statement; correlated input baths retain the previous pointwise joint/output qualification. Bounded time-dependent admitted perturbations are compatible with the same uniform estimates when the actual propagator is well defined.

The uniform initial moment bound covers arbitrary free-apparatus states only in the ENCODED W=0 subsystem, because V<=W+zn and [V,W]=0. It does not authorize attaching arbitrary unencoded hot clocks/flags to previously encoded data. Preparation/initial truncation must earn its actual admission.

Undoing the explicit probe/flag frames followed by the received old witness-frame/Tanner ideal decoder provides the terminal consumer, with the old decoder-radius shrink retained. The readout corrects the coherent low-component span; new clock/probe/flag states may remain arbitrary and be discarded. This is ideal terminal decoding, not a noisy finite-duration readout theorem.

## Accepted capability and remaining limits

The whole formal join closes autonomous syndrome acquisition, physical faulty clocks, and classical correction at the specified at-most-six-qubit engineered-GKSL primitive level, without trusted timing, collision flags, or a full-check input-repair primitive. Ordinary references to the old conditional source proof are not being used to bypass the new all-string audit.

This result still assumes the received particular Tanner family, an ideal encoded input and ideal terminal consumer, sufficiently small actual local perturbations after the rate hierarchy, and real reset/readout reservoirs. It does not supply microscopic two-body realization, useful finite code constants, Euclidean wiring, a practical threshold, or superiority over an active decoder granted identical resources. Physical apparatus count and degree may be enormous fixed constants and must be retained in any cost claim.

The requested independent whole-theorem audit is closed with this qualified mathematical acceptance. Earlier failed mechanisms and narrower receipts remain preserved; they are not retroactively reclassified as successful.
