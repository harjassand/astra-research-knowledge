# Exact integer multiplication boundary

Contributor: `/root/exact_kernel`, 21 October 2026.
Scope: one arithmetic kernel and independent bounded tests. No complete owner
matrix experiment, new scientific programme, dependency installation, or external
source retrieval was performed.

## Operation

`src/exact_matmul.py:exact_dot(A,B)` accepts two-dimensional NumPy arrays having
either exactly `int64` dtype or object dtype containing only integer scalars.
Object scalar values are converted to Python integers before arithmetic; this is
necessary because a NumPy integer kept inside an object array can still overflow.
Booleans, floats, strings, other fixed-width dtypes, incompatible dimensions and
nonarrays are rejected. The return value has object dtype and Python integer
entries. `return_info=True` also returns dimensions, radix, limb counts, number of
integer matrix products and the explicit overflow bound.

An input already wrapped by a caller before entry cannot be repaired or detected
in general. The caller must validate its own coefficient construction before
casting to `int64`. This operation never interprets a floating approximation as
an exact integer.

## Proof of exactness

Let the inner dimension be `k` and let `L=2**63-1`. The kernel chooses the largest
integer `b<=31` satisfying

    k * (2**b-1)**2 <= L.

Each integer entry is represented by signed-magnitude radix-`2**b` digits. Thus
each digit lies in `[-(2**b-1),2**b-1]`; an entry's sign multiplies all its digits.
For `int64` input, unsigned arithmetic is used only to obtain the nonnegative
magnitude safely, including the exceptional `INT64_MIN` magnitude `2**63`.
For object inputs, all magnitude operations are arbitrary-precision integer ones.

For every digit-matrix product, each scalar product has absolute term sum at most
the displayed bound. Each product and every possible partial sum therefore fit
in signed 64-bit arithmetic. NumPy's integer matrix multiplication computes that
integer product without overflow; its accumulation order does not affect this
argument. No floating-point BLAS multiplication is used.

The kernel collects limb-pair products by their total radix degree and reconstructs
the result using Horner evaluation with Python arbitrary-precision integers.
All conversion of a guarded intermediate to object integers is exact. Consequently
the result equals the mathematical integer product entry by entry. Zero inner
dimension, zero entries, and zero outer dimensions give the ordinary zero product.

The implementation trusts Python integer arithmetic and NumPy's documented
fixed-width integer multiplication on values whose complete intermediate ranges
are inside the dtype range. This is executable numerical verification, not a
proof-assistant or processor verification.

## Cost

If the maximum input bit lengths are `a` and `c`, there are at most
`ceil(a/b)*ceil(c/b)` guarded integer products of the original shapes, plus
arbitrary-precision reconstruction over each output entry. This cost is paid
explicitly; the construction does not turn many wide integer products into one
unaccounted floating matrix operation. It can use more memory than an ordinary
double-precision product because limb arrays and Python-object outputs coexist.

`checks/check_exact_matmul.py` passed 29 complete small fixtures against a separate
naive Python-integer implementation. These include mixed signs, 90- and 130-bit
object inputs, the signed 64-bit extremes, zeros, empty dimensions and NumPy
integer objects. Ten malformed-input cases were rejected. Three scaling probes
also checked a complete row and column independently; those sampled comparisons
are diagnostics, not substitutes for the general proof above.

The test body took 0.06306016300004558 seconds wall, 0.063062265 seconds process
CPU, and had a process peak RSS of 25,620,480 bytes. Its kernel-only scaling
measurements for 29-bit times 59-bit square integer matrices were:

| Order | Limb products | Kernel wall seconds |
| --- | ---: | ---: |
| 32 | 3 | 0.0003735710015462246 |
| 64 | 6 | 0.003524805997585645 |
| 128 | 6 | 0.020133594000071753 |

These are one-run bounded diagnostics, not a performance prediction or advantage
over the owner's dense comparator. Library imports occur before the body timer.
Proof development, authoring, tool latency and model inference are unmetered.
No failed test execution or algorithmic tuning sweep occurred in this scoped task.
The raw receipt is `results/exact_matmul_checks.json`.

## Unimplemented alternative

One can in principle use smaller integer limbs in IEEE binary64 matrix
multiplication when every absolute partial sum is below `2**53`; products and sums
then remain exact in binary64 under the assumed arithmetic. This may access a
faster GEMM implementation, but introduces a floating-kernel execution assumption
and demands its own explicit range and implementation audit. It is not used in
this kernel or any result claimed by this contributor.
