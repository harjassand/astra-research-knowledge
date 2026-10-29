# Adaptive one-carrier comparison

2026-10-28. Author theorem and calculations; independent review requested. Governing proof: `adaptive_single_carrier_bound_v1.md`.

This replaces neither a received theorem nor a dataset. It adds a stronger comparator than final-decoder optimization: arbitrary perfect adaptive single-qubit instruments, full classical memory, exact source knowledge and ideal final control, provided every required noise interval acts on the sole retained quantum carrier. The benchmark has fewer hardware resources than the standard redundant code; it is not a claim against equally resource-rich conventional coding.

At 32 mandatory native uses and equal total controller-window time:

| Integrated background per round | Simulated encoded F_e | All allowed single-carrier F_e upper bound |
|---|---:|---:|
|0.001|0.980223|0.912653|
|0.003|0.972590|0.887071|
|0.01|0.938210|0.809392|
|0.03|0.796645|0.663140|
|0.1|0.368335|0.517368|

The first four comparisons survive the stronger ideal adaptive comparator. The last does not; moreover the feasible classical measure/store/reprepare F_e=0.5 beats that encoded point. Hence the useful operating window is not universal robustness.

The analytic upper bound is (1 + (399/401)^T exp(-T integrated))/2, using the best native damping site. A numerical replay JSON records every clocked sweep and timing case, input hashes and 500 random stress tests. Two primitive-channel characteristic-polynomial identities and the rational native survival amplitudes are checked symbolically. The encoded side remains the existing finite-dimensional numerical model, not a new acquisition, hardware measurement, certified interval computation or accepted code review.

The improvement is comparator rigor. It does not invent an entanglement law, a code or a new error-correction mechanism, and it does not establish a physical mandatory-noise interface beyond the declared model.
