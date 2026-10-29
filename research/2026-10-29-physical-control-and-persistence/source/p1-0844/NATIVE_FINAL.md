## This continuation produced a stronger physical-control theorem and a nonvacuous finite-data program

The central advance is now a precise distinction between **acquiring information about a device** and **acquiring a control that changes what the device can accomplish within a fixed time**. I also completed a constructive route from calibration to predictable bulk observables over arbitrarily long runs.

[:chatgpt-content-reference{index="4"}](https://chatgpt.com/library?file_id=libfile_91bef0a282c481919d9f47337de7958a&account_id=personal)

The package contains the proofs, code, synthetic readouts, independent reviews, and useful failures. All **148 files from the preceding archive remain byte-for-byte unchanged**.

### 1. A control obstruction that survives continuous observation and feedback

The new **signed-continuation theorem** strengthens the source-B exclusion substantially.

For the specified source-B generators, no controller can produce a nonzero, hidden-parameter-independent probability of changing the actual physical bit within any deterministic physical deadline. The controller may continuously observe the trajectory, switch among the generators, compute, randomize, and stop adaptively. Even allowing a failure flag does not permit an exact, nondegenerate target distribution conditional on successful completion by that deadline.

The proof uses a mathematical continuation of the uncertain parameter to a value where every allowed jump rate becomes negative. At that value:

- Every trajectory ending in the opposite part of the physical state graph has negative weight.
- Every trajectory ending in the original part has positive weight.
- Feedback and randomization combine these trajectory weights with nonnegative controller weights.

A bounded-time physical probability has an analytic continuation. An exact target identity on the physical parameter interval would therefore have to hold at the continued value, where the signs contradict it. **Negative rates are a proof device, never a proposed physical operation.**

This establishes a stronger consequence for the acquired cross-response construction. Source A and source B retain identical complete isolated-operation baseline path laws. Yet source A’s opposing responses permit useful exact stochastic gates in one fixed-duration call, while source B cannot reproduce that capability using arbitrary bounded-time observation and switching within its declared menu.

The distinction concerns the **actual terminal physical state**. Polynomial coin simulations and impossibility results for passive interruptible sampling are established predecessors; the candidate addition is this controlled physical-state witness, including its continuous-time and heralding scope. :chatgpt-content-reference{index="0"}

The governing proof is :chatgpt-content-reference{index="5"}[SIGNED_CONTINUATION_CONTROL_THEOREM.md](producer-workspace/SIGNED_CONTINUATION_CONTROL_THEOREM.md).

### 2. The strongest ordinary alternatives remain constructive

The new theorem does not remove the ordinary routes the user identified. They now have explicit constructions and costs.

| Route | What it achieves | Material boundary |
|---|---|---|
| Observe until a chosen target is reached | Exact physical endpoint control without estimating the hidden parameter | Completion time is unbounded; the joint endpoint-and-clock law retains hidden dependence |
| Calibrate the actual deployment device | Useful fitted transitions and a positive model of exposed keys, intermediate reads, and durations | Finite accuracy; requires unchanged device kinetics during calibration and service |
| Wait under mode 3 | Uniformly accurate visible preparation | Does not supply a hidden-independent model of all native observations |
| Use an actual baseline initializer or replacement specimen | A legitimate bypass where that resource is available for deployment | Its initialization time, locality, hidden-state effects, and other costs must be included |

The waiting comparison is particularly important. With an actual identity return and unobserved native interiors, a nine-call long branch gives a **100-macro marked-record TV bound of 0.007564423**, using at most **540 expected native calls**. The chosen word and its duration may remain exposed.

That is much cheaper than the conservative calibration route for this limited approximate task. It prevents the exact separation from being misreported as a general practical advantage.

### 3. The positive construction now implements a physical network

I extended the source-A compiler to an addressed spin ring. With the explicitly supplied site isolation, neighbour reads, and boundary controller, each local update uses:

- One native fixed-duration call.
- Five fresh private fair bits.
- The acquired opposing-response mixtures.

The actual visible update is exactly

\[
\frac{11}{20}I+\frac{9}{20}\,\text{heat-bath update},
\]

with conditional refresh probabilities \(3/8,\ 1/2,\ 5/8\), according to the neighbouring spins. Every site’s hidden parameter may remain frozen, and those parameters may be correlated.

This produces familiar solvable Gibbs dynamics from raw operations whose frozen-disorder correlations have infinite predictive rank. For \(d\) sites, the mean spins obey the closed equation

\[
m_i(t+1)
=
\left(1-\frac{9}{20d}\right)m_i(t)
+
\frac{9}{160d}\bigl(m_{i-1}(t)+m_{i+1}(t)\bigr).
\]

The ordinary solver is a valid consumer of the compiled physical process. Gibbs dynamics and contraction methods are established machinery; the construction supplies the physical operations to which that machinery applies. :chatgpt-content-reference{index="1"}

The added addressability, isolation, and timing premises are explicit. A finite selector-bit count does not establish a hardware timing contract: actual decision-time evolution must enter the operation model or be protected by a real hold.

### 4. Finite data now support a useful guarantee that does not deteriorate with run length

The vacuous long-record certificate changed the receiving objective.

For the fixed random-scan network, I proved a guarantee for **bulk observables at every deterministic macrostep**. If each implemented local row has error at most \(\delta\), then normalized-Hamming Wasserstein error satisfies

\[
W_t
\le
\rho^t W_0
+
\frac{80}{27}\delta(1-\rho^t),
\qquad
\rho=1-\frac{27}{80d}.
\]

The error approaches a precision floor rather than accumulating indefinitely.

An actual finite-data supplier works even in source B: calibrate modes 0 and 3 on each unchanged deployment specimen, then choose between the physical words \(T_0\) and \(T_3T_3\) using a fitted dyadic probability. Each deployed update takes at most two native calls. The confidence event is uniform in the actual hidden parameters, so it handles calibration–deployment correlation without importing an unconditional ensemble-density assumption.

The completed synthetic exercise used four persistent devices:

| Quantity | Result |
|---|---:|
| Native calibration calls | **800,000** |
| Calibration endpoint reads | **800,004** |
| Calibration failure allowance | **0.01** |
| Fresh selector bits per deployed update | **16**, plus site selection |
| Normalized-Hamming error floor including failure allowance | **0.0280411** |
| Magnetization expectation error bound at every deterministic macrostep | **0.0560822** |
| Bond-correlation expectation error bound at every deterministic macrostep | **0.0921644** |
| Largest computed magnetization discrepancy through 1,000 steps | **0.00048584** |

All 800,000 synthetic flip increments are saved. The fitted controller uses their counts and the warranted intervals; it does not receive the simulation’s hidden parameters. Exact rational calculations verify the fitted transition matrix and stationary law. The transient discrepancies are model calculations after synthetic calibration, not physical measurements.

This guarantee concerns the specified observables and program. It does **not** assert full-record TV accuracy, arbitrary adaptive stopping, arbitrary feedback, or accuracy at a randomly chosen wall time.

The complete construction is :chatgpt-content-reference{index="6"}[ROBUST_OBSERVABLE_PROGRAM.md](producer-workspace/ROBUST_OBSERVABLE_PROGRAM.md).

### 5. The failed attacks and reviews materially changed the result

The first attempted extension—monotonicity—failed. Although every primitive source-B flip probability increases with the hidden parameter, state-dependent feedback makes the terminal derivative negative after six calls. The sign argument survives that failure and led to the continuous-time theorem.

The complementary acquisition investigation also produced a valid stronger experiment: repeated returned trials on persistent specimens can improve near-zero squared-residual certification from a \(v^{-2}\) dependence to \(v^{-1}\), up to logarithms. Its conservative numerical fixture nevertheless requires **1.39 billion returned trials and 786,336 independent specimens**, before return costs. I preserved it as a useful theorem and a failed practical route. Adaptive sampling of unknown coin populations has substantial primary predecessors. :chatgpt-content-reference{index="2"}

Both complementary reviewers accepted the corrected signed-continuation theorem. The robust program received separate mathematical and physical-interface reviews. Its executable was independently rerun, and the saved readouts, counts, post-calibration state, and all fitted selectors were reconstructed independently.

The exact checks include **40,805 bounded feedback trees**, **1,298 heralded trees**, **256 detailed-balance checks**, **256 contraction checks**, and **64 closed mean-equation checks**. The reviewed corrections concerning controller latency, endpoint–clock dependence, and conditional initial information are incorporated.

The resulting opening is concrete: **engineer physical dynamics into a useful predictable program while hidden memory persists, and acquire the information required by that program’s actual precision objective.** The remaining physical frontier is a consequential actuator family with compatible isolation and timing, and useful targets beyond the strongly contractive ring. No apparatus, practical speedup, or civilisation-scale breakthrough is claimed.
