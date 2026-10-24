# Exact prefix-fibre sampler: quotient rejection and the remaining boundary

This note is an independent mathematical extension of `FIRST_CONSTRUCTION.md`.
It assumes the same acquired object: the first `t` coordinate polynomials
`F=(Q_1,...,Q_t)` of a bijective quadratic map `Q:F_2^n -> F_2^n`. It does
not give the learner `Q`, its coefficients, or a sampler. Coefficients must
first be acquired by the comparison procedure; all linear algebra, random
bits, recurrence evaluations, and oracle comparisons below are costs of the
learner. It also does not claim that recognizing the promised class is free.

## The quotient sampler

Write the quadratic part of coordinate `F_i` as a bilinear polar form `B_i`,
and let

```
L = intersection_i rad(B_i),       dim(L)=n-r.
```

Choose a complement `R` so every input has a unique representation `Rz+v`,
where `z in F_2^r` and `v in L`. The restriction of `F` to each coset of `L`
is affine in `v`: for one computable linear map `A:L -> F_2^t`,

```
F(Rz+v) = F(Rz) + A v.
```

Let `a=rank(A)`, `W=im(A)`, and `s=t-a`. Let `pi:F_2^t -> F_2^t/W` be the
quotient map and define the acquired quadratic map

```
G(z) = pi(F(Rz)).
```

For target prefix `y`, a core point `z` is feasible exactly when
`G(z)=pi(y)`. Every feasible `z` has exactly `|ker A|=2^(n-r-a)` lifts `v`
with `F(Rz+v)=y`.

Since `F` is a prefix of a bijection, it is onto and each fibre has exactly
`2^(n-t)` points. Therefore, for every `q in F_2^t/W`,

```
|G^{-1}(q)| = 2^(n-t) / 2^(n-r-a) = 2^(r-s).
```

Thus `G:F_2^r -> F_2^s` is a balanced surjection and `r>=s`. This is an
all-size statement; no genericity or random-coefficient assumption is used.

There are two exact ways to sample a point from `F^{-1}(y)`:

1. **Enumerate the core.** Evaluate `G(z)` on all `2^r` core points, select
   uniformly among the `2^(r-s)` matches using exactly `r-s` random bits,
   then select uniformly from the affine solution set of `A v=y-F(Rz)` using
   `n-r-a` random bits.
2. **Reject in the quotient.** Draw uniform `z in F_2^r`, accept when
   `G(z)=pi(y)`, and then draw the same uniform affine lift `v`. Acceptance
   probability is exactly `2^-s`; the accepted `z` is exactly uniform on the
   fibre. This sampler terminates almost surely and uses `2^s` core
   evaluations in expectation. A capped implementation with
   `M=ceil(2^s ln(1/delta))` proposals reports explicit failure if none is
   accepted; its failure probability is at most `delta`.

Choosing the cheaper route gives expected core evaluations
`2^min(r,s)`, rather than always `2^r`. The sampler is polynomial in `n` on
any acquired prefix for which `min(r,s)=O(log n)`. In particular, if `A` is
onto the prefix space (`s=0`), every core point is feasible and the large
polar-core enumeration disappears entirely. This is a checkable algebraic
condition after the prefix coefficients have been learned, not a supplied
latent feature.

The exact entropy accounting is consistent: enumeration uses
`(r-s)+(n-r-a)=n-t` random bits, the minimum needed for a uniform point in a
fibre of size `2^(n-t)`. Rejection uses `r` bits per proposal in expectation
`2^s` times, plus `n-r-a` lift bits; those extra bits are the charged cost of
finding a feasible core, not hidden sampler access. Gaussian elimination to
find `L`, form `A`, and sample its kernel, and each evaluation of `G`, must
also be charged. With explicit ANFs, these are ordinary finite-field
operations (at most polynomial in `n,t` per evaluation after the matrices
are built); storing the acquired coefficients is `O(t n^2)` bits in a dense
quadratic representation.

## Direct full-prefix boundary, and how to avoid it for inversion

For the full prefix `t=n`, bijectivity makes `A` injective on `L`: if
`v in L` and `A v=0`, then `Q(x+v)=Q(x)` for every `x`, hence `v=0`.
Consequently `a=dim L=n-r` and `s=n-a=r`. A *direct* full-prefix sampler
therefore has `2^r` worst-case cost; its quotient map
`G:F_2^r -> F_2^r` is itself a quadratic permutation. This is a boundary of
that direct method, not a necessary cost for the inverse query.

Every prefix of length `n-1` has exactly two inputs. Once its exact sampler
is available, an inverse query for full target `y` can avoid the `t=n`
sampler: draw `x` uniformly from `F^{-1}(y_{1:n-1})`, evaluate the already
acquired last coordinate `Q_n(x)`, and keep `x` if `Q_n(x)=y_n`. The two
points in the prefix fibre have different last bits, because `Q` is
bijective, so acceptance is exactly `1/2` and the expected number of prefix
samples is two. This is an exact algorithm. A capped version must report
failure explicitly.

The same two-point fact gives exact labels while acquiring `Q_n`. For any
input `x`, use the acquired prefix sampler for `F=Q_{1:n-1}` to draw until
both distinct points of `F^{-1}(F(x))` have appeared. This takes three
prefix samples in expectation (a two-point coupon collector). The points
are `x` and its unique partner; one comparison orders them, and equality of
the represented input vectors identifies which is `x`. Their order is
exactly the last output bit, so this supplies an exact value oracle for
`Q_n(x)`. Quadratic interpolation at `0`, `e_i`, and `e_i+e_j` then
recovers `Q_n` exactly. These evaluation and comparison costs are paid; no
last-bit sampler or hidden state label is supplied.

It follows that the sequential acquisition and inverse route need prefix
samplers only for lengths `0<=t<n`. Define the acquired, data-dependent
runtime parameter

```
kappa(Q) = max_{0<=t<n} min(r_t, s_t),
```

where `r_t` and `s_t=t-rank(A_t)` are computed from the learned prefix
coefficients (and `t=0` is the trivial uniform cube sampler). Core work per
prefix sample is at most `2^kappa` in expectation, plus polynomial
finite-field work. This replaces a supplied global `b(Q)` bound with a
checkable a-posteriori parameter; it does not promise a small value for all
quadratic permutations. The learner does not need `b` as input, but its
runtime may still be exponential in `kappa`.

For a concrete separation from the full-map polar rank, let `n=2m+1` and

```
Q(x_0,...,x_{n-1}) =
  (x_0,...,x_{n-2}, x_{n-1} + sum_{j=0}^{m-1} x_{2j}x_{2j+1}).
```

This is a bijective quadratic shear. The final coordinate has polar rank
`n-1`, so the common radical of all output-coordinate polars has codimension
`b(Q)=n-1`. Yet every strict prefix is linear: `r_t=0`, `rank(A_t)=t`,
and `s_t=0`. Thus `kappa(Q)=0`; the acquired-prefix sampler and inverse
filter have polynomial cost despite arbitrarily large full-map `b(Q)`. This
is a structural example, not a hardness result or a comparative benchmark.

The extension still proves no computational hardness theorem for the
remaining worst case where `kappa` grows linearly with `n`. Any equally
informed comparator can use the same sampler after acquiring the same
prefix coefficients.

## Finite-grid median check for the comparison-to-label step

The median estimate in `FIRST_CONSTRUCTION.md` has a simple all-size
justification. In one prefix fibre, let `N=2^(n-t)` and draw
`K=2m+1` independent uniform ranks with replacement. Couple each discrete
rank to `ceil(N U_j)` for iid continuous `U_j~Uniform[0,1]`. The normalized
sample-median rank differs from the continuous order statistic
`U_(m+1)` by at most `1/N`. The latter has the symmetric beta law
`Beta(m+1,m+1)`, mean `1/2`, and variance `1/[4(K+2)]`. Hence its expected
absolute displacement is at most `1/[2 sqrt(K+2)]` by Cauchy-Schwarz. The
fraction of fibre points whose threshold labels disagree is the median
rank's displacement from the true half-fibre threshold, so

```
e <= 1/(2 sqrt(K+2)) + 1/N.
```

This is an average over a uniform point in each fibre; it is not a uniform
pointwise guarantee for every input. Seven-corner quadratic self-correction
then has error at most `7e` by a union bound, since every nonempty affine
corner is marginally uniform even though the seven are dependent; use fresh
independent sampler/label randomness for each queried corner. For small
`N`, exact fibre enumeration can remove the `1/N` grid term, but it must use
the acquired sampler and pay its core-search cost; enumeration is not free.

These refinements improve the conditional-sampling operation and validate
the finite-grid term. They do not change the comparison-query order, do not
establish a speed advantage over a retaining learner, and do not validate
the quadratic-permutation promise from comparison transcripts.
