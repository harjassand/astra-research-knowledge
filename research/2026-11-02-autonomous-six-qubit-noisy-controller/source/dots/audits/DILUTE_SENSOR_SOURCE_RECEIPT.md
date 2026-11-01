# Independent source audit: dilute unflagged Poisson compiler

2026-11-01. Read root `ROOT_DILUTE_SENSOR_POISSON_COMPILER.md`, SHA256 d0984f052e29e1faf76263b6f6b32e0d4a30f9699de047061c2ffc268a760e21, and `FLAG_FREE_SOURCE_ADMISSION.md`, SHA256 652fd12e71aee823c361015f887badbb58ad97cc155db6bf2f1a5adf9b93ed9a, including its superseding physical-phase-count correction.

## Judgment

**PASS for the stated full-valid-clock source operator bound, exact pair-occupation cancellation, and a genuinely tunable source barrier budget.** This includes arbitrary overlaps and coherent clock/probe/data states within the valid physical cycle subspace. It is NOT yet a whole noisy-native-clock/Boolean-controller theorem: malformed-transition domination, weighted Boolean coupling, and actual rate-proportional hardware noise remain explicit joining gates.

## 1. Clock closure is an operator identity

A phase instrument must be trace-preserving on all its quantum data/probe/cache inputs, must advance on every outcome, and must have hazard depending only on its own clock phase. Under these hypotheses its adjoint on any diagonal clock observable is exactly the corresponding classical transition generator. This remains true for entangled data and coherent clock states: off-diagonal clock amplitudes do not change that adjoint identity.

Thus private clocks have a product generator on their clock-observable algebra even when their quantum gate actions overlap. The actual transient clock distribution need NOT factor. The product stationary busy fraction f_p f_q is used only to center a Poisson equation for that exact pair generator, not substituted for the current occupation probability.

The physical return cycle must use the corrected count D=D_eff=2M+1 of fast holding phases. T_cycle=1/r+D/k. In particular t(post-readout)=T_cycle; t(idle) is generally smaller. Preparation is slow; readout occurs before return; the partial Pauli prefix remains the completed check throughout return/idle and resets to I at preparation. Applying the earlier no-return t(idle)=T_cycle formula here would be wrong.

## 2. Exact own-clock and collision terms

Let e_p=(I-Z_cache,p Sbar_p)/2 and r_p=1_armed(I-X_p P_p)/2. All own factor gates must be the actual controlled check factors in their stated order; for the standard tensor-Pauli check they act on distinct data sites and transport X_pP_p exactly. Extra native phases may not simply be added to D unless their quantum action has the claimed transport property or is separately bounded.

Own readout-killed t solves K_A t=-1. The gain is k t(POST-readout), so it is kT_cycle. The second reward price xi=T_cycle on armed phases, zero after readout and on return, exactly cancels the ordinary readiness gain. Preparation creates readiness expectation epsilon I at rate r, giving floor epsilon rT_cycle=epsilon(1+Dr/k), NOT k epsilon/r.

For a neighbor q gate C_q(R), anticommutation of P_p with R changes readiness by

    1_armed,p X_pP_p(I-Z_q)/2.

Its norm is at most one and the event requires both p and q to be nonidle. At a legal q phase only one exit instrument is enabled, so one must not multiply by its number of outcome branches. Neighbor readout and reset do not change r_p: they act on different probe/cache registers and are TP; quantum correlations do not alter this Heisenberg fact.

At p's own readout the actual dressed check is S_p Z_extra. The overwrite mismatch differs from (I-X_pS_p)/2 by exactly

    X_p S_p(I-Z_extra)/2.

It vanishes if every neighbor is idle, because completed/idle prefixes commute with the complete check. Its positive part is bounded by the sum of busy-neighbor projectors. This includes arbitrarily entangled probe states; no assertion that individual reports are correct is made.

All other probe hops transport dressed check observables, and completed readout/reset removes only a dressing exponent already equal to zero. Therefore, on the ENTIRE valid-cycle subspace,

    L V_p <=-e_p+epsilon rT_cycle I_idle,p
                    +2kT_cycle sum_(q neighbor p) I_pq,
    V_p=t(x_p)e_p+T_cycle r_p.

The factor two covers neighbor factor-hop damage and own decorated-readout damage. Neither collision flags nor collision independence appear. Controller operations must leave the physical checks/probes alone as stipulated; any additional cache writer or nontransporting helper operation needs its own term.

## 3. Pair Poisson potential and uniform height

For each ordered overlapping pair solve

    Q_pair h=-(I_pq-f^2),   f=Dr/(k+Dr),

and shift h to have minimum zero. Adding 2AkT_cycle h cancels the ACTUAL operator occupation remainder pointwise and leaves exactly

    2AkT_cycle f^2=2AD^2(r/k)/(1+Dr/k).

This is not a forbidden-collision probability accumulated over storage time.

The uniform span proof is valid. For Dr/k<=1, use common start/progress Poisson ticks for two copies of the pair chain. In a block 2D/k, no starts for either component has probability >=exp(-4), and at least D progress ticks for each has probability >=1/4. The event sends every initial phase pair to idle/idle, after which the copies coalesce. Therefore expected coupling time is <=8exp(4)D/k, and the Poisson representation for a [0,1] observable gives the same bound on span(h). This applies also to the corrected return cycle: D fast ticks with no start drain any phase into idle.

As an algebraic special-case check, for one busy phase and k=1, min-normalized h has h(00)=0, h(01)=h(10)=r/[2(1+r)^2], and h(11)=(1+3r)/[2(1+r)^2]. This solves the pair equation and stays bounded as r→0. The multiplied price, not h itself, grows as A/r.

Independent readout bit flips of probability eta can also be centered: their source is eta kT_cycle times the readout-phase indicator, whose stationary occupation is 1/(kT_cycle), giving floor A eta per check. Its positive own-clock price is O(A eta/r). This conclusion is specific to the stated bit-flip model; arbitrary detector/helper errors need their actual operator admission.

## 4. Explicit source height/floor tradeoff

Let N_checks<=L_s n and the number of ordered neighbor pairs be <=L_e n. For Dr/k<=1, T_cycle<=2/r. The unweighted projectors have norm <=1 even when different readiness operators do not commute. Hence the positive scaled source and pair potentials obey

    0<=Z_src<=Z_* (A/r)n I,
    Z_*=4L_s+32exp(4)D L_e.

The mean source floor obeys

    b_src<=A[2L_s epsilon+2D^2 L_e(r/k)],

plus separately admitted detector floors. These constants depend on the actual finite check/circuit family, not on r,A,n.

If the FULL joined controller earns restoring coefficient c>=c_* A with c_*>0 independent of r and A, then

    b_src/c <=(2L_s/c_*)epsilon+(2D^2L_e/c_*)(r/k),
    z_src <=Z_* A/r.

These are independently tunable ratios. For example fix k=1, take r=t and A=t^2, and take preparation impurity sufficiently small. Both collision floor relative to restoring drift and positive source-height density then tend to zero with t. Thus the source does supply a possible STRICTLY POSITIVE barrier margin; it is stronger than merely proving finite coefficients.

But the premise c>=c_*A and the other joined contributions must actually be proved. Boolean overwrite/rearm costs, sorter residuals and apparatus noise cannot be hidden in constants that secretly grow as k/r or 1/A in b/c. The preparation floor does not vanish by dilution alone.

## 5. Positive ground offset and full exponential criterion

The shifted pair h need not vanish in the chosen ground clock configuration. This is not fatal and must not be ignored. Write the whole potential V=W+Z with 0<=Z<=z n and [V,W]=0, and suppose the ACTUAL all-apparatus operator inequality is

    L V<=-cW+b n.

Then L V<=-cV+(b+cz)n. The exact noncommuting local expansion yields a Foster cutoff theta whenever

    z+b/c+(C2/c)a < theta < beta.

For an encoded W=0, P-supported input, the uniform initial moment is <=exp(a z n), so the same strict margin pays initialization even when the source ground offset is nonzero. Using the killed CP transfer gives a W-boundary tail and protected-output bound, provided actual finite bandwidth and PHP/PJP/PJ†JP flatness are separately established.

The sensor terms commute with the dressed base W by the previously checked probe/data sign cancellation; diagonal pair prices also commute. Noncommutation among different readiness terms is irrelevant to the local exponential expansion. The underlying component projector must still commute with V, not merely its scalar W.

## 6. Unresolved global physical gates

The source bound above concerns all VALID private-cycle configurations, including all overlaps, not all bit strings in a physical clock encoding. The proposed sorting-clock extension still must verify every mode/end/reset transition on malformed states, that sorting preserves the decoded phase AND its quantum dressing, and that deviations are operator-supported on the claimed inversion debt. A classical diagonal check alone does not cover an unexamined off-diagonal clock coupling.

The root correctly notes that malformed native microgates can change base W by O(1) at rate O(k), independently of A. Therefore their domination requires a real sorting penalty/rate inequality, not the small source price alone. A large sorting rate also brings actual noise; arbitrary fractional-error noise at that rate is not made harmless merely by naming a small penalty. The same caution applies to Boolean repair rates and sensor/readout hardware.

No global native-clock result is accepted from the source proof alone. If the separately active clock and Boolean audits earn their inequalities with total z+b/c<beta and the stated noise contract, the source calculations here are sufficient inputs to the already received killed/noncommuting exponential consumer. Otherwise finite t,xi,h by themselves do not establish memory.

## Conclusion

Accepted: the corrected legal-cycle source operator remainder, all pair interactions, TP clock closure for coherent states, centered Poisson cancellation, uniform O(1/k) span, O(A/r) positive price, and a constructive source-only hierarchy that can leave a positive barrier margin. Still pending: the all-malformed-clock and weighted-controller/operator join with actual noise and initialization/readout costs. No physical source experiment, useful hardware threshold, or global native memory is claimed by this receipt.
