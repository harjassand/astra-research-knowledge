# Repeated-measurement feasibility gate

Committed before the following result is run/read, 2026-11-05.

- Standard unrotated planar code of spatial distance21,841 physical qubits,21 data-noise rounds,20 noisy syndrome observations, and perfect initial/final syndrome closure.
- Each data-Z error and each syndrome-bit error is independently Bernoulli1/1000. This is a phenomenological graph model, NOT circuit-depolarizing noise or acquired hardware noise.
- Same deterministic minimum-weight matching and canonical residual-path selector as the validated2D code.
- Every left-to-right nonbacktracking path of length<=150 in the space-time graph is represented by exact integer DP. Longer witnesses have an exact rational degree6 Chernoff bound.
-10,000 trials; seed2026110521; one99.9% exact-integer, outward20-bit Clopper-Pearson interval. No early stopping.
- Uniform Bernoulli edge noise is now vectorized using uint16 rejection from Python randbytes. This is exactly uniform integer arithmetic under ideal bits; the seeded PRNG is still not certified physical randomness.
- Record full setup, sampling and exact-confidence timing before JSON serialization.
- General graph polynomial complexity is NOT claimed. An independent serial-diamond counterexample shows exponentially poor acceptance is possible. Standard square-code and repeated-measurement scaling must be measured and compared with strong published importance/splitting methods.
