# Integer-only finite singleton operation at rational time

29 October2026. Root construction; independent review PENDING. It consumes
the exact24-state Bernstein program already independently checked in
check_finite_program.py. This closes the DISCRETE ROTATION-DRAW bit interface,
not the entire velocity sampler, initial-moment arithmetic or quantized output.

Input is finite nonnegative RATIONAL time t, encoded as integer numerator
and denominator, and an iid FAIR-BIT source. Output is the exact signed-
permutation group index with probability p_t(g). No continuous real output,
transcendental call, floating number, matrix exponential or Choi operation
is used by fairbit_singleton.py's draw. Seeded PRNG executions are explicitly
only diagnostics of the algorithm under a different literal randomness source.

## 1. Ordinary exact exponential coin, actually implemented

For rational0<=x<=1 generate independent lazy binary uniforms U1,U2,... .
Let K be the maximal descending run x>U1>...>UK. Return whether K is even.
Since Pr(K>=k)=x^k/k!, its success probability is sum_k(-1)^k x^k/k!=e^-x.
The run terminates almost surely and has factorial tails. This is the
established von Neumann descending-run operation, not a new exponential
sampling discovery. Primary modern description and lazy-digit implementation:
[Karney1303.6257v2,Section2](https://arxiv.org/html/1303.6257v2).

Lazy uniforms retain only bits that a comparison requires. To compare two,
read lexicographically until the first differing bit, preserving already
read prefixes. To compare a uniform to rational p/q, its depth-k dyadic
interval is entirely below/above p/q once the integer cross-products decide
that fact. Equality has probability zero; no approximate comparison is used.

For any rational x=m+r>=0, m integer and0<=r<1, lazily require m independent
e^-1 coins, then an e^-r coin. Stop at the first failure. The resulting
probability is exactly e^-x. Although m may be enormous in binary, the mean
number of unit coins is <=1/(1-e^-1)+1<3. Input integer arithmetic and the
rare long successful path are charged. There is no loop through all m on
every call and no underflow to zero.

## 2. Uniform expected bit and arithmetic bounds

For two unconditioned independent binary uniforms, the first differing-bit
index B has Pr(B>k)=2^-k and E B^2=6. Extra bits in their lazy comparison are
at most2B, even if one prefix is already present. At descending comparison
k>=2 the chance of reaching it is <=1/(k-1)!. Independence of that event
from B is NOT assumed: Cauchy--Schwarz bounds expected charged bits by
2sqrt(6)/sqrt((k-1)!). The first rational comparison uses <=2 bits in mean,
since at depth k at most one dyadic interval straddles its threshold.

The elementary bound j!>=2^(j-1) gives sum_(j>=1)1/sqrt(j!)<4. Hence one
unit coin consumes <24 expected fair bits. The lazy-product extension uses
<72 expected bits uniformly over ALL finite rational x>=0. The same
geometric/factorial argument pays every polynomial moment of comparison
depth, run length and integer-counter length. Arithmetic therefore has
expected cost polynomial in the input bit length, with potentially
unbounded worst-case work. There is no unit-cost arbitrary integer premise.

## 3. Exact finite-group draw

Draw FOUR independent coins of mean exp(-t/4) by Section1. Their sum K has
the exact Binomial(4,exp(-t/4)) law. Select g using column K of the exact
Bernstein table, with denominators24,96,48,8,1. Ordinary fair-bit uniform-
integer rejection costs <14 expected bits for any of those denominators.
The positive-column identity independently verified in
EXACT_PROGRAM_REVIEW.json then gives exactly p_t(g) for every rational t.

Four exponential coins and one integer draw cost <302 expected bits;512 is
a conservative displayed bound. Fixed table lookup/permutation work and
arithmetic input length are retained. At t0 no randomness is needed and the
output is identity. As t grows, the algorithm still performs exact rational
comparisons; it never replaces a tiny positive exp probability by zero.

The consumer pins the exact program SHA256 in FAIRBIT_EXECUTION.json. Its
single seeded run uses only integer/Fraction operations in draw_group_index,
unit_exp_coin,exp_coin,Uniform and Bits. Float exp appears ONLY afterward in
the diagnostic reference statistics, never in the drawn law.

## 4. What remains unpaid

The fair-bit law is a theorem conditional on iid fair bits; a seeded Python
PRNG is not certified as that source. The operation outputs a finite rotation
index, not an exact continuous velocity or a sampled material cross section.
The complete marked density/factory algorithm still needs certified initial
queries, Gaussian/Poisson primitives, arithmetic comparisons and a declared
quantized/observation-law output. This component result does not silently
promote the existing floating full-law consumers to finite-bit exactness.
