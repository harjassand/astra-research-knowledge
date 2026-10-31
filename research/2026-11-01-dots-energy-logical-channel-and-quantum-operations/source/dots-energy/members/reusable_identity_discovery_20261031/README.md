# Acquired bilinear identities: tested negative fixture

## Outcome

This is **not a new scientific or computational capability**. A known flip-graph
mechanism independently acquires a seven-product 2 x 2 GF(2) multiplication
identity from the schoolbook task. Exact verification succeeds, but its compiled
15-XOR circuit merely matches the standard-basis Strassen--Winograd baseline.
The retained packed Four-Russians implementation is faster at every tested size.
Strong published alternative-basis methods are more demanding baselines still.

## Reproduce

```
python discover.py --out acquired_scheme.json
python compile_and_test.py > run.log
```

Only Python's standard library is required. No fast identity is supplied to the
discovery program. The explicit Winograd identity appears only in the separately
identified comparator. `acquired_scheme.json` preserves the first run and its
complete search counters. Re-running overwrites timings; exact coefficients and
counters are deterministic for seed zero.

## Observed acquisition and verification

* 940 attempted flips; 78,960 candidate pair/axis checks and 78,972 reduction
  pair/axis checks, including all non-improving search steps.
* 0.0447892 seconds in the search loop. No failed walk preceded the success.
* Independent expansion of all 64 tensor coefficients: 448 term/coefficient
  checks, 0.00006824 seconds.
* 84 coefficient payload bits. JSON and code storage are additional, not free.
* Initial linear forms use 24 block XORs. Shared-subexpression compilation
  reduces these to 4 + 4 + 7 = 15, costing 0.00008898 seconds.
* 347 exact execution cases, including every pair of binary 2 x 2 matrices and
  recursive noncommutative blocks through size 64, passed against a separate
  classical product. All 84 one-bit certificate corruptions were rejected.

The final coefficient comparison is an ordinary finite proof of the bilinear
identity: expanding each product gives the coefficient tensor, which agrees
entrywise with matrix multiplication. Because the left-input factor always
precedes the right-input factor, the identity holds over every characteristic-2
ring, including noncommuting matrix blocks. It does **not** assert a real-valued
identity; `compiler_results.json` includes a characteristic-3 counterexample.

## Execution comparison (median of three, milliseconds)

| n | Packed classical | Packed Four Russians | Acquired, best recursive cutoff tested |
|---:|---:|---:|---:|
| 32 | 0.0633 | 0.0386 | see complete results |
| 64 | 0.3085 | 0.1209 | see complete results |
| 128 | 1.0973 | 0.4288 | see complete results |
| 256 | 5.0010 | 1.5208 | 3.3389 |
| 512 | 22.2468 | 6.1644 | 10.3690 |

At n=512, retained Winograd at cutoff 256 took 10.6069 ms; that small timing
difference is not evidence of a scientific improvement. All methods receive the
same inputs, use exact packed GF(2) rows, and retain their implementations and
chosen schedules. Every new matrix pair is different; Four-Russians lookup
tables for the new right operand are built inside its timed execution. Input
generation is excluded equally. Tuning trials, validation, process startup,
engineering and research costs are **not** contained in the small search-loop
time; no all-in payoff claim is made. The candidate already loses before those
positive acquisition costs are added.

These are transparent Python prototypes, **not** state-of-the-art hardware
benchmarks. We did not benchmark AlphaTensor/AlphaEvolve, modern native M4RI,
or published alternative-basis kernels. Their absence weakens any possible
positive claim, not the demonstrated failure to beat this already-available
retained baseline.

## Strong prior art and why this fixture stops

* Fawzi et al., [AlphaTensor, Nature 2022](https://www.nature.com/articles/s41586-022-05172-4):
  learned and exactly verified bilinear identities, including a 47-product
  4 x 4 GF(2) scheme. This already supplies the broad mechanism tested here.
* Kauers and Moosbauer, [Flip Graphs for Matrix Multiplication](https://arxiv.org/abs/2212.01175):
  the local-search identity used by this implementation is their known approach.
* Novikov et al., [AlphaEvolve](https://arxiv.org/abs/2506.13131):
  a stronger algorithm-discovery comparator, not run locally.
* Karstadt and Schwartz, [Matrix Multiplication, a Little Faster](https://doi.org/10.1145/3364504),
  and Schwartz and Vaknin, [Pebbling Game and Alternative Basis](https://epubs.siam.org/doi/10.1137/22M1502719):
  changing basis reduces internal additions to 12, with conversion and memory
  costs that must also be paid. Fifteen is not an unrestricted optimum.
* [The rank of 3 x 3 matrix multiplication over F2 is 23](https://arxiv.org/abs/2610.11823)
  is a recent October 2026 preprint claiming computer-assisted, Lean-checked
  optimality. We have not independently reviewed its full proof or run its
  checkers. It is a reason to check the frontier before blindly searching for
  rank 22, not a result established by this package.

No new lower bound, universal learning theorem, historical novelty, or
civilisation-level consequence follows from this fixture. Its retained capital
is a small exact acquisition/verifier harness and an honest strong-baseline
failure. Do not repackage field restrictions, storage accounting, or ordinary
shared-subexpression elimination as the missing discovery.
