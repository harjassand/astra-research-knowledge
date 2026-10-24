# Whole review of canonical projected-fermion contraction

24 October 2026. Independent Sol review in the existing learning owner slot.
Constructor files and earlier learning proofs were not edited. No observations,
physical trials, or additional workers were used.

## Verdict and exact scope

I read both complete proof notes, rather than accepting their summaries:

- `fermion/CANONICAL_CONTRACTION.md`, SHA-256
  `39276a90bbaffb48f33a4110a40993e16791a5e1ca3d4db40a6ed9d269e6f0cc`.
- `fermion/BLOCK_CANONICAL_OBSERVABLES.md`, SHA-256
  `93ef3765d1b8c8b3daa161fc0037ecd57c414482803e1805130d350d718f90f9`.

**The four load-bearing arguments pass this review at their stated fixed-parameter
scope.** I found no substantive counterexample to the hard-endpoint scalar-root
theorem, canonical coefficient algorithm, heterogeneous strongly resonating block
bound, or merged marked-observable construction. The conclusion is a conditional
deterministic evaluator for explicitly supplied matrices passing the stated
certificates. It is not an executed asymptotic KP implementation, a sampler, or a
physical preparation theorem.

One notation clarification is needed for literal use of the marked outer test:
the `d_*` in its `3^d_*` factor must bound **all** blocks of the new partition,
including unmarked blocks. The first definition in section 6 says only that it
bounds the merged block. Set

```
d_* = max(degree B_merged, max_(unmarked B) degree B_B),
```

or simply use `floor(r_O b/2)` for a nonempty support of `r_O>=1` old blocks.
That conservative size bound already bounds every new block. Recompute `t`,
`h'`, `S'` and the tests with it. This is a local definition repair preserving
the fixed-support complexity and nonempty sufficient class, not a counterexample
to the construction with its conservative enlarged block-size interpretation.
The distinction matters if an implementation instead takes a small *actual*
merged degree while an untouched block has larger degree: the stated per-block
inequality `exp(2 V_B)<=3^d_*` would then have no justification.

## 1. Scalar negative roots: direct derivation

For arbitrary complex `F`, the chiral matrix
`H=[[0,2F],[2F*,0]]` is Hermitian. In `H[U_A union V_(A^c)]`, a nonzero principal
minor uses equal numbers `k` of U and V indices. For labels `I subset A`,
`J subset A^c`, its determinant is

```
(-1)^k 4^k |det F[I,J]|^2.
```

The even principal-minor order contributes no additional characteristic sign.
Every disjoint ordered `(I,J)` occurs in `2^(n-2k)` choices of `A`, and no
nondisjoint pair occurs. Thus the normalized average is exactly

```
2^-n sum_A det(xI-H[S_A])
 = sum_k (-1)^k c_k x^(n-2k) = x^n Z(-1/x^2).
```

Hermitian determinant stability can also be seen without importing an averaging
principle: a null vector for `diag(y)-H` when every `Im y_j>0` contradicts its
strictly positive imaginary quadratic form. The proof's positive-direction
derivative is valid. Introduce a new variable `w`, replace the two selected
coordinates by `y_U+w,y_V+w`, differentiate in `w`, then specialize `w=0`.
This is precisely coordinate differentiation and real boundary specialization
of a stable polynomial. This auxiliary-variable step is already explicit in
the reviewed file, so it is not an outstanding repair. Repeating over pairs
selects one complementary index per pair. The top monomial gives `2^n x^n`
before normalization and rules out the zero polynomial at every stage.

Consequently the displayed average is real-rooted. If `z!=0` is a zero of `Z`,
either solution of `x^2=-1/z` is a nonzero zero of that average and hence real;
therefore `z<0`. Since `c_0=1`, zero itself is not a zero of `Z`. Missing high
coefficients only add roots at `x=0` to the averaged characteristic polynomial.
No invertibility of `F` or symmetry beyond the physical state's stated input
is needed for this scalar identity.

This yields a Poisson-binomial tilted charge law with at most `m` Bernoulli
factors. The near-mean estimate does not assume its factors are supplied. If a
mode is left of `k`, put `L=m-k+1`. Unimodality gives

```
E K <= k-1 + sum_(j=k)^m (j-k+1) p_j
    <= k-1 + L(L+1)p_k/2 <= k-1+L^2 p_k.
```

Together with `E K>=k-1/4` this proves `p_k>=3/[4(m+1)^2]`.
Reflection handles a mode to the right, and a mode at `k` has mass at least
`1/(m+1)`. Rank-deficient and endpoint cases cause no hidden division by zero.
This review endorses the reconstructed **hard-endpoint scalar** statement;
it does not independently extend it to extra onsite weights or multivariate
physical occupation stability.

## 2. Fixed-density coefficient reconstruction and complexity

The signed partial-matching gas is exact. A nonzero bra/ket term has the same
occupied sites, so it has an integer fugacity degree. Every active reference
dimer contributes at least two weak incidences across both copies, hence an
`s`-dimer component has at least `s` weak factors. Actual local weights keep
all interference signs; the absolute estimate is taken afterward.

I also read the connected-support/Mobius implementation in the governing
`independent_opportunity_a/DIMER_CONTRACTION.md` sections 3--5. Give each activity
the marker `u^|C|`. A connected log cluster has connected union support, and its
degree is at least that union's size. Mobius extraction isolates each union;
the formal logarithm retains repeated polymers. Enumerating supports of size
below `L`, their subset DPs, and their finite matching-pair activities takes
`m exp(O_(D,Delta)(L))` arithmetic. This does not assume a smaller conditional
partition oracle.

The per-vertex tilted activity sum is the stated
`S=x^2/[4D(1-x)]`. The zero-weight singleton test in the standard KP theorem
bounds log clusters meeting a vertex by `S`; summing over vertices gives
`mS`. The size tilt gives the tail `m exp(-4L)` uniformly on the larger
logarithmic neighborhood. Cauchy's estimate therefore controls *the derivative
of that same analytic tail*, including the mean calculation.

The two positive dimer endpoints really bracket the desired density. The
derivative estimate `d mu/dr<=m/(4r_lo)` and certified sign updates justify the
finite bisection rule. The declared estimator error `1/32`, acceptance window
`1/8`, and final bracket width all give mean error below `1/4` in
`O_delta(log m)` evaluations.

The `(m+1)`-node discrete Fourier formula is exact for degree at most `m`.
Nonnegative global coefficients give `|Z(re^(i theta))|<=Z(r)`; relative errors
at inner nodes therefore create absolute errors in the normalized Fourier
sum. The proved mass `a_m` converts these to relative coefficient errors.
The outer omission uses an absolute bound through negative-reference zeros,
not a log evaluator at such a zero. The conservative rational test
`2^-floor(delta m/8)<=epsilon a_m/64` is valid. If it fails,

```
m = O_delta(log(m+1)+log(1/epsilon)+1)
  = O_delta(log(1/epsilon)+1).
```

Thus the charged `9^m` exact fallback is polynomial in `1/epsilon`. This is
essential to arbitrary requested accuracy and is actually present in the proof.

For fixed block/degree/density parameters, a size-`O(L)` rational activity and
its derivatives have polynomial bit length in the explicit input and precision.
Formal-log divisions only have orders up to `L`; subset sums and Mobius signs
add polynomial overhead. Certified roots of unity need angular error
`O(eta/m)`, since `|z Z'(z)|<=m Z(r)`; a small radial rounding error has the same
bound up to a constant. Known reference products can be evaluated with relative
precision using the explicit sector lower bounds. Exponentially small
intermediate magnitudes require polynomially many bits, not constant precision.
These costs are included. No root, mean, exact-transcendental or sampling oracle
is concealed in the algorithm.

## 3. Nonuniform strongly resonating blocks

For each native block, negative roots give
`B_B(z)=product_j(1+z/beta_Bj)`, with `beta_Bj>0`. For `u>=0` and
`|theta|<=2pi/3`,

```
|1+u exp(i theta)|^2 - (1+u)^2/4 >= 3(u-1)^2/4 >= 0.
```

Multiplication gives `|B_B(z)|>=2^-d_B B_B(|z|)` without uniform block roots,
small internal amplitudes, or positive individual matching overlaps.

Every native reference block has even parity. A nonzero bra/ket matrix element
has an even total number of cross incidences on each active block, counted
across both copies. Thus it has at least two per active block, and an `s`-block
component has at least `s` edge factors. Cauchy uses the actual positive-radius
reference norms `B_B(|z|)`; the edge norm is at most two, and the actual bra/ket
subset count is at most `2^(b Delta s)`. Division by analytic sector reference
polynomials costs at most `2^(sum d_B)`. These are exactly the resources paid in
`h^s`. The constants reserve enough room for one marked filter.

For the outer arc the exact gas is left **unnormalized**. A fixed union of
active blocks injects into canonical rooted forests, at most `(D+1)^s` of
them. This gives the product `product_B[u_B+(D+1)h]` even when an inactive
reference factor vanishes. Poisson-binomial characteristic functions give

```
u_B <= exp[-2 V_B sin^2(theta/2)],
exp(2 V_B)<=3^d_max.
```

The heterogeneous variance sum suffices; no minimum variance per individual
block is needed. At a factor-two tilt every Bernoulli variance changes by a
factor in `[1/2,2]`, so `V0(r)>=nu M/2` throughout the bracket. The outer
exponent is in fact at most `-7nu M/16`, stronger than the claimed `-nu M/4`.
For the mean bracket, endpoint displacement is at least
`nu M/4-1/64`, while the perturbation is at most `nu M/128`. The exceptional
small `M` range is finite at fixed `nu` and is explicitly enumerated.

The reference coefficient DP and its tilt search are paid ordinary polynomial
operations. Positive nonzero rational coefficients have polynomial encoding
bounds, so power-of-two bracketing does not require an uncharged real oracle.
Threshold partition search is a sound search for its stated separated class,
not complete recognition or an optimal partition algorithm. An arbitrary
useful state or low-susceptibility sector can correctly return `UNKNOWN`.

## 4. Marked filtered canonical mass and outer contours

Merging all touched blocks is the correct operation for an even distant
hopping/pair observable. Its finite Fock matrix and fermionic permutation
signs must be computed. There is no replacement by independent endpoint
averages. Include every native edge internal to the merged union; recompute
the actual coarse graph and certificate. Norm certification alone does not
guarantee every observable passes this stronger test.

For `||O||<=1`, charge conservation gives sectorwise
`(1-t)^2 c_k <= c_k^pm <= (1+t)^2 c_k` and exact polarization. With
`t=2^(-d_*-5)`,

```
(2t+t^2)2^d_* = 1/16+2^(-d_*-10) < 1/8.
```

Hence the marked analytic denominator is at least `7/8` of the native
denominator. Its local norm overhead is bounded by
`(1+t)^2(8/7)2^d_* < 2^(d_*+1)`, within the reserved `2^(d_*+2)`.
The inserted matrix is `A_pm^dagger A_pm` **after** cross-edge creators; it is
not commuted through them. Evenness preserves the incidence parity argument.
Calling these mathematical norm filters is appropriate; their operator norm
may be `1+t`, so no physical Kraus operation or success rate is proved.

The full unfiltered tilt is retained. Applying both coefficient and grand-norm
bounds gives exactly

```
Pr_(r,pm)(K=k) >= ((1-t)/(1+t))^2 Pr_r(K=k).
```

No marked real-rootedness assumption or new tilt search is used. Ignore the
marked reference characteristic factor, bounded by one by nonnegative
coefficients. Removing `r_O` old blocks loses at most `r_O d_max/4` of native
reference variance. At the same tilt the remaining variance is computed and
checked, not guessed. Its lower test and the recomputed outer error give

```
-V_u + M'[S'+(D'+1)h'3^d_*] <= -3nu M'/16,
```

with the global degree-bound clarification above. This handles negative-axis
zeros and the potentially non-real-rooted marked reference. A direct sufficient
size condition for the variance test, using only the coarse bounds, is
`M>=r_O d_max/nu-r_O+1`; actual smaller cases can use their exact rational test
or finite fallback. The same outer-tolerance/fallback argument remains
polynomial at fixed `b,r_O,nu`.

Finally the two numerator errors are bounded by
`sigma(c_k^+ + c_k^-) <= 2 sigma(1+t)^2 c_k`; denominator perturbation adds at
most `sigma/(1-sigma)` because `|<O>|<=1`. This gives the displayed bound (11).
`sigma=epsilon t/16` is conservative for `epsilon<=1`. Fixed support makes
`1/t` a fixed cost, while a growing support or shrinking `nu` would change the
complexity and is correctly excluded from the uniform claim. The numerical
energy-accuracy dependence on `sum |h_a|/epsilon_E` is explicitly retained.

## 5. Bounded executable and source checks

I inspected the repaired graded tensor shuffle in `check_block_observables.py`.
I did not rerun its output-writing main function. In a bytecode-disabled Python
process I independently tested the exact creator-product and norm-gas identities
for partitions `((0,2),(1,3))`, `((0,3),(1,2))`, and
`((0,2,4,6),(1,3,5,7))`, with rational nonzero bridges. The respective full
Fock states had 15, 15 and 135 nonzero terms; all six identities passed. These
are algebraic diagnostics of the repaired sign path, not new observations or
evidence that an asymptotic KP evaluator has been executed. The theorem review
keeps graded signs independently of these tests.

I reopened primary Borcea--Branden, *Applications of stable polynomials to mixed
determinants*, [arXiv:math/0607755v5](https://arxiv.org/html/math/0607755v5),
Propositions 2.2 and 2.4 and their proofs, and Mann--Minko, *Algorithmic Cluster
Expansions for Quantum Problems*,
[arXiv:2306.08974v2](https://arxiv.org/html/2306.08974), sections II.2--II.4 and
Theorem 2. The first supplies the closure facts used in the independently
derived scalar identity; the second explicitly gives the signed-polymer KP and
dummy-test bound. No whole-archive retrieval or novelty-clearance inference was
used.

The four existing Luna supports separately checked scalar stability,
coefficient complexity, nonuniform blocks, and marked filters. Their bounded
notes were read in full; all critical inequalities above were rederived by this
Sol reviewer. Their agreement is corroboration, not a substitute for those
derivations. Constructor hashes were unchanged at the end of this read/check
phase. The review does not alter the constructor's conventional-method tie,
small sufficient-coupling scope, or absence of physical validation.

## Literal review assignment, retained once

> Learning checkpoint is stable; my nonmutating exact replay independently passes its 240 intervals, 180 bounds, source scoring and costs with zero observations. Use this same Sol owner slot for an adversarial whole review of deep_continuation/fermion/CANONICAL_CONTRACTION.md and BLOCK_CANONICAL_OBSERVABLES.md, focusing scalar negative-root derivation, fixed-density coefficient reconstruction, nonuniform strong-block resonance, and marked filtered canonical mass/outer contours. Read actual proofs rather than inheriting summaries. There is a known finite-code fermionic shuffle bug on interleaved blocks being repaired by constructor; theorem claims retain all graded signs. Check completeness/complexity and identify actual gaps, not requests for novelty clearance. No new workers, data collection, or report apparatus; one ordinary scientific review note and concrete counterexample/repair if found. You may use your existing four Luna supports only for bounded checks that materially help.
