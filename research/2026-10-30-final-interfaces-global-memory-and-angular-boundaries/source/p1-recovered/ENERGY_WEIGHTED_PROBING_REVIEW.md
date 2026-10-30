# Receiving review: energy-weighted probing and active-index convergence

2026-10-30. Focused actual-file check by the existing record-geometry role. This receives the completed theorem, including its new Section 5, separately from the earlier proposal check. No simulation or source retrieval was performed.

## Inputs and preserved snapshots

1. ENERGY_WEIGHTED_PROBING_AND_FINITE_MEMORY_ENCOUNTERS.md
   - SHA256: 8a179fd78e32264962d1b8caf4f2e983a11167c5bbf74daa43e65177634eca00
   - Snapshot: ENERGY_WEIGHTED_PROBING_AND_FINITE_MEMORY_ENCOUNTERS_8a179fd78e32.reviewed.md
2. Corrected BOUNDED_TASK_LEARNING_WITH_PERSISTENT_MEMORY.md
   - SHA256: 9793a0791b03713ced9fce30010f93f70b0632e70c927ec668a1e768a1283b5d
   - Snapshot: BOUNDED_TASK_LEARNING_WITH_PERSISTENT_MEMORY_9793a0791b03.reviewed.md

**Finding: accepted at the stated deterministic nonincreasing activity schedule and corrected complete supplier. No new binding mathematical error was found.** Section 5 closes active-SGD convergence for \(p_i\asymp i^{-a}\), every \(0<a<1\), including \(a=1/3\), without asserting finite total flags in that regime.

## 1. Weighted energy and finite encounters

The conditional energy inequality can be multiplied by any deterministic nonnegative nonincreasing \(q_i\). Its expected storage terms telescope with interior coefficients \(q_i-q_{i-1}\le0\); nonnegative terminal energy has a favorable sign. This proves (4).

For a nonincreasing activity schedule, taking \(q_i=p_i\) and using the fresh current gate gives (5). The equality \(E[B_ie_i]=p_iE[e_i]\) requires that \(e_i\) be defined before the gate, as the actual source decomposition ensures. There is no independent-state sample hidden in this step.

With divergent \(\sum p_i\) and finite \(\sum p_i^2\), independent fresh gates give infinitely many actual observations, whereas (3)--(5) give finite expected total active guard mass. For \(U>0\), every positive flag statistic has a fixed positive minimum, so the actual number of guarded active pairs is finite almost surely. The stronger rail margins make every actual clipping event imply a guard. The source correctly avoids interpreting the future-dependent last observed flag as a stopping time after which the conditional bias is known to vanish.

The nonincreasing-schedule condition used in (5) is retained here when invoking Section 3. The source does not establish its weighted bound for arbitrary nonmonotone or outcome-dependent activity policies.

## 2. The new Section 5 summability argument

Write \(P_{i-1}=\sum_{t<i}p_t\). The choice
\[
 q_i=\frac{p_i}{1+P_{i-1}}
\]
is nonincreasing because its numerator decreases and denominator increases. For \(p_i\asymp i^{-a}\), \(0<a<1\),
\[
 q_ip_i\asymp i^{-1-a}
\]
in the tail. Equation (4) therefore proves \(\sum_iq_iE[e_i]<\infty\).

The Bernoulli lower-tail bound
\[
 {\mathbb P}\{K_{i-1}<P_{i-1}/2\}\le e^{-P_{i-1}/8}
\]
is valid for independent, nonidentically distributed fresh gates. It does not require the hidden energy or clipping bias to be independent of the past activity count. This distinction matters.

On the good-count event,
\[
 (K_{i-1}+1)^{-1}\le2/(1+P_{i-1}).
\]
Using the energy-based bound \(\|h_i\|\le K_be_i\) and dropping that event yields the first term in (13). On its complement use only the uniform bias bound
\[
 H_{\max}=\sqrt d\,R_z/\kappa+U+\|b\|.
\]
The regularizer cancels in this bound. Freshness of the current \(B_i\), rather than independence of the old field and old count, then gives the second term in (13). Thus there is no illicit decoupling of correlated hidden state and waiting history.

The exponential-tail sum is finite. For example \(p_i\le1\) gives
\[
 \sum_i p_i e^{-P_{i-1}/8}
 \le e^{1/8}\sum_i p_i e^{-P_i/8}
 \le e^{1/8}\int_0^\infty e^{-x/8}\,dx
 =8e^{1/8}.
\]
This establishes (13) with explicit finite constants if desired.

Mapping calendar indices to realized active indices gives exactly
\[
 \sum_i\frac{B_i\|h_i\|}{K_{i-1}+1}
 =\sum_k\frac{\|h_{t_k}\|}{k}.
\]
Its finite expectation makes it finite almost surely. The SGD step \(2/[\lambda(k+1)]\) is bounded by \(2/(\lambda k)\), so the required step-weighted bias is summable. The active gradient is uniformly bounded, making squared-step noise summable as well.

## 3. Active filtration, optimization and measured completion

The instruction to reveal the current physical state is an enlargement of the mathematical conditioning filtration, not a proposed hidden-state sensor. The pre-sign filtration includes the realized waiting interval and \(B_{t_k}=1\). Fresh signs and ADC dither are drawn afterward. The active update is measurable before the next such enlarged history; keeping the numerical iterate fixed through idle periods gives the usual projected-distance recursion.

Its strong-convexity drift and the preceding summability give \(u_k\to u_*\) almost surely by the nonnegative almost-supermartingale argument. Uniform active averages converge too.

The same good-count/bad-count proof applies to the actual nonnegative flags. On a good count use \(F_i\le K_Fe_i\) on active rounds; on a bad count use \(F_i\le C_F\). This yields \(\sum_kF_k/(k+1)<\infty\) almost surely, despite \(F_i\) being observed after the signs and ADCs. The harmonic-tail argument then gives \(K^{-1}\sum_{k\le K}F_k\to0\).

For completeness, measured residual convergence also follows directly. Equation (13) makes the average conditional bias vanish by the same harmonic-tail argument. Bounded active martingale differences have \(\sum_kE\|M_k\|^2/k^2<\infty\), so their averages vanish almost surely. Therefore the average reported gradient approaches the true gradient at the average input. This probability-one conclusion does not rely on interpreting one fixed confidence event as certain.

At dyadic active-count checkpoints, the flag logarithmic offset divided by \(K\) vanishes. For the observed-square radius, \(b_K=R_z/\kappa\) is fixed and the actual square sum is at most \(Kb_K^2\); its variance-grid logarithms grow only logarithmically in \(\log K\). Hence that radius divided by \(K\) vanishes. The projected fixed-point certificate consequently reaches every fixed positive tolerance under indefinite valid operation.

## 4. Two different scheduling objectives

The source correctly keeps these conclusions distinct:

- \(a=1/3\): convergence, vanishing average flag debit and useful finite-accuracy scaling; no claim of finitely many total flags.
- \(a=1/2\): logarithmic expected total flag debit, still infinite in the displayed upper bound.
- \(1/2<a<1\): finite expected total guard mass and finitely many actual guards almost surely, at slower calendar acquisition.

The table is explicitly an expected-count/expected-budget comparison, not a ratio-of-random-quantities confidence proof. The proof of \(P_N=o(\sqrt N)\) under square summability is correct and confines that resource limitation to this sufficient scheduling route.

## 5. ADC correction and implementation scope

I compared the corrected bounded-source file against the earlier preserved input. Its revised equation (4) conditions on the complete pre-read physical/instrument record, current signs and commands, and earlier ADC randomizations. It explicitly supplies fresh independent dither. This excludes the previously preserved \(\widehat z=\Delta_z\tau\) counterexample and closes that binding qualification.

The additional sentence retaining the absolute ADC error interval when allowing a conditional mean defect is also correct: guard thresholds are pathwise statements and must be changed if that interval changes. Exact convergence in Section 5 uses the exact conditional mean contract. A nonzero calibrated mean-error allowance instead retains the stated accuracy floor.

For the fixed-calendar implementation described in Section 8, conditioning on the complete activity schedule can validate its confidence calculation when that schedule was generated independently of the initial source and all sign/dither random seeds, and the source/controller does not use future keys. The source path itself depends on past activity, so this is independence of the primitive inputs, not independence between the schedule and the entire resulting trajectory. Conditional on the schedule, the sign/dither martingales survive. The unconditional weighted-energy proof should not be silently reinterpreted as a conditional statement for every fixed future schedule.

I did not inspect or rerun the matched implementation in this receiving task. Its reported numerical errors, certificate radii and energy totals remain under the physical role's implementation receipt. The present acceptance covers the mathematical source, its active-index inference chronology, and the actual ADC wording correction. No practical speedup, free idle time, all-future hidden preparation or finite apparatus lifetime is certified.
