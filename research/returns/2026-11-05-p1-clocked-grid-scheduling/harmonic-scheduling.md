# Deterministic phase assignment for heterogeneous selected harmonics

This independent [complete mathematical construction and error audit](package/math_note_harmonic.txt) assigns one fixed phase to each indivisible recurring waveform and bounds selected aggregate Fourier components using at most `2K` individual-device variance contributions. It complements the [whole-response energy construction](README.md), and uses established Shapley–Folkman convexification plus conditional-expectation rounding. It is not a field deployment or a discovery of those methods.

## Exact finite construction

Write each real periodic signature as `p_i(t)=c_i0+2 Re sum_(k>=1)c_ik exp(i k omega t)`, `omega=2pi/T`. Phase `tau_i` gives `S_k=sum_i c_ik exp(-i k omega tau_i)`. For K chosen harmonics and known nonnegative weights w_k, let `B_i^2=sum_k w_k |c_ik|^2`. Unweighted retained-band RMS is `sqrt(2 sum_k |S_k|^2)` and band peak is at most `2 sum_k |S_k|`; the complex-coefficient factors of two matter.

With M uniformly allowed phases and `M>K`, every device's `2K`-dimensional real harmonic vectors average to zero. Start with uniform fractional assignments. Repeatedly select `2K+1` fractional devices, find a linear dependence among differences of two active options per device, and move to a nonnegative boundary while preserving all device simplex sums and aggregate zero. Each step removes an active weight; at most `N(M-1)` eliminations leave at most `2K` fractional devices.

Round those devices deterministically by conditional expectation. If `b_i` is a fractional mean vector, the exact squared aggregate satisfies

```text
sum_k w_k |S_k|^2
 <= sum_(i in F)(B_i^2-||b_i||^2)
 <= sum_largest_min(N,2K) B_i^2,
|F|<=2K.
```

In particular `||S||_w<=sqrt(2K) max B_i` and unweighted RMS is at most `2sqrt(K) max B_i`. Report the actual recomputed residual as well as the conservative bound. This is a selected-band statement; coherent unselected harmonics can still scale with fleet size and worsen absolute peaks.

Independent uniform fixed phases instead have expected squared weighted amplitude `sum_i B_i^2`. Their ensemble mean vanishes but one realized fleet remains periodic. Per-cycle randomization changes sidebands and deadline analysis. For identical common-template waveforms, ordinary equally spaced or weighted-midpoint interleaving already has stronger simple whole-waveform guarantees. The present specialization earns waveform heterogeneity and multiple monitored outputs, not an advantage over optimal common-template interleaving.

## Actual phase freedom, precision and errors

Device-specific phase restrictions need a separate convex feasibility test: zero must belong to the sum of their allowed-vector convex hulls. A separating vector certifies an unavoidable coherent residual when infeasible. For example, aligned positive fundamentals confined to one common phase window of width `W<T/2` retain at least `cos(pi W/T)sum_i |c_i1|`. Randomization cannot remove that access restriction. A nonzero feasible target can instead be preserved and rounded with its own best-relaxation-plus-variance bound.

A rational coefficient mesh, centered within each device, preserves exact fractional feasibility and adds an explicit aggregate error of order `N sqrt(2K) h` plus the individual norm correction. A direct final bounded-error certificate is necessary; arbitrary floating-point nullspace cancellation is not an exact proof of the measured operating response. The current demonstration scans its full support array each elimination, with arithmetic upper bound `O((NM)^2+NM(2K)^3)`. The better active-support construction count is not a runtime or exact bit-complexity claim for that unoptimized code. Measurement coefficients, fractional weights, device state, communication and numerical precision remain paid.

For calibrated `chat_ik`, coefficient radii `e_ik`, relative timing error at most `delta_i` and missing devices D, a sufficient actual harmonic bound adds

```text
E_k=sum_(i not in D)e_ik
   +sum_(i not in D)|chat_ik| min(2,k omega delta_i)
   +sum_(i in D)|chat_ik|.
```

New arrivals need their own allowance. Common clock shifts rotate all terms without changing magnitude; common harmonic gains preserve cancellation. Worst-case differential errors do not: for exactly canceled equal-amplitude fundamentals C, permitted per-device timing signs can create residual at least `(2/pi)N C |sin(omega delta)|`. Fixed arbitrary coefficient errors can likewise align linearly in N. Fixed absolute accuracy therefore needs improving precision, a justified shared/aggregate error structure or paid corrective reserve, not a fixed independent tolerance alone.

Changing jitter creates sidebands; static Fourier lines do not certify all spectral energy. Smooth-waveform derivative bounds cannot be applied to square edges without justification. Calibration sampling, meter bias, state dependence, full recharge response and drift need explicit errors. Known network transfer factors can be stacked across monitored outputs, increasing the real dimension to `2KL`, but their uncertainty is additional. Source cancellation at one boundary is not a feeder-voltage or universal grid-stability proof.

## Recorded evidence and deployment boundary

The [recorded harmonic replay](package/harmonic_results.json) and [original code](package/harmonic_replay.py) include a **fabricated** population of 200 replicated measured templates, K=3 and 20 phases. Six fractional devices remain before rounding; final band RMS is 133.684 W against a 1338.191 W independent-random RMS reference, while full sampled RMS remains 741.459 W. Replicas are not observed devices or independent experimental units. A separate small synthetic elimination/rounding check and adversarial timing example are reported in the proof note; neither is field validation or a new Capital run.

Published weekly three-building profile optimizations and frozen-offset failures are described on the [measurement page](measurements-and-evidence.md). Those are counterfactual aggregate-profile shifts, not acquired device-level firmware access. Deadlines, recovery intervals, transition reserves, reboot persistence, membership changes and actual clock control retain the [main construction's costs](README.md). Priority of the full specialization remains unestablished; converter interleaving, DESYNC and power-system Shapley–Folkman work are explicitly credited in the complete note. [Original package and provenance](SOURCES.json).
