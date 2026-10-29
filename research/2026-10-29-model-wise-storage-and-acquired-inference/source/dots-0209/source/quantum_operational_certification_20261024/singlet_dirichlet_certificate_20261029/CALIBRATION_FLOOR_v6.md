# Calibration floor and resource caution
2026-10-29. Consequence of the already explicit test-bias budget, not a new noise-resilience theorem.

The preferred weighted test has C_P=(d0/K)(n−1)<2(n−1). If the entire actual preparation/test/readout instrument has half-diamond deviation b_test from its specified implementation, the certificate floor is C_P b_test. This is an actual systematic floor and does not disappear with more source samples.

For a pessimistic gate-by-gate budget with G(n) operations, each half-diamond error≤ξ, telescoping gives b_test≤G(n)ξ. Pair-singlet preparation, frame rotations and routing already make G(n) at least order n (and potentially n² on a restrictive layout). Thus maintaining an ε-sized certificate can require ξ=O(ε/n²), or O(ε/n³) under quadratic routing, using only this worst-case bound. Parallel depth does not remove accumulated whole-state error. Better hardware-specific calibration models or fault-tolerant control may improve the budget, but are not proved here.

The fixed four-qubit seed is constant-size, not perfect for free. Uniform permutation sampling, gates, reset, source-repeatability and readout need independent control evidence. No theorem here tolerates an unknown adversarial SPAM channel while inferring source quality from the same data.

`validation_scaling_v6.json` gives exact Catalan/power-of-two code sizes and conservative ideal zero-failure shot counts at two target confidence/error pairs. These counts exclude discovery, physical routing, storage horizon multiplier T, actual faults and compiler deployment. They are not experimental performance, a promised acceptance rate, or a demonstrated advantage. Direct logical 2-design validation remains a serious comparator, and corrected qubit Schur synthesis can be much better than a loose polynomial upper bound.
