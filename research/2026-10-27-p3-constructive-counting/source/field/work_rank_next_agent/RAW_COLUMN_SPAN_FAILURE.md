# Why sublinear raw-column oversampling does not acquire the needed code

27 October 2026. This is a restriction on a particular acquisition architecture,
not a lower bound for counting or arbitrary matrix recovery. In fact the
matrices below have only a perfect matching of sparse errors, and are covered
by the earlier generic acquisition theorem.

## 1. A deterministic coding lemma

Let n and r be even. Let U be an n by r binary full-column-rank matrix with
code distance

\[
d_C=\min_{a\ne0}\operatorname{wt}(Ua),
\]

and dual distance

\[
d_\perp=\min\{\operatorname{wt}(w):w\ne0,\ U^\top w=0\}.
\]

Take an invertible alternating r by r matrix K, set D=UKUᵀ, and let P be
the adjacency matrix of any perfect matching. Thus P is a coordinate
permutation, P²=I, and preserves Hamming weight. The raw matrix

\[
B=D+P
\]

is alternating and differs from rank-r D in exactly n directed entries,
or n/2 undirected edges.

Choose any set I of k raw column indices. For every j outside I and every
coefficient vector z supported on I, put w=e_j+z. The approximation
residual for column j by the chosen raw-column combination is Bw.
There are two cases:

1. If Uᵀw=0, then Dw=0 and wt(Bw)=wt(Pw)=wt(w)≥d_perp.
2. Otherwise Dw is a nonzero codeword in im U, so
   wt(Bw)≥wt(Dw)−wt(Pw)≥d_C−k−1.

Consequently,

\[
\operatorname{dist}(B_j,\operatorname{span}\{B_i:i\in I\})
\ge \min(d_\perp,d_C-k-1).
\]

Any matrix X whose columns all belong to that raw-column span therefore has

\[
\operatorname{Ham}(B,X)
\ge(n-k)\min(d_\perp,d_C-k-1).
\]

The chosen coefficients can be arbitrary and individually optimal. The
lower bound applies to every selection of raw columns; it is not a failure
of greedy selection or a particular decoder.

## 2. An asymptotic family with a severe loss

For r=o(n) with r sufficiently larger than log n, there are binary
matrices U simultaneously satisfying

\[
d_C\ge n/3,\qquad
d_\perp=\Omega\!\left(\frac{r}{\log(en/r)}\right).
\]

Here is a direct existence proof. Draw all entries of U independently
uniformly. For fixed nonzero a, Ua is uniform on F₂^n. The union bound
over fewer than 2^r such a, followed by the usual binomial-volume estimate,
shows d_C≥n/3 except with probability at most

\[
2^r\,2^{-n[1-H_2(1/3)]}.
\]

For a fixed nonzero w, Uᵀw is uniform on F₂^r. Therefore the probability
of a nonzero dual word of weight less than t is at most

\[
2^{-r}\sum_{j=1}^{t-1}\binom nj.
\]

For a sufficiently small fixed positive constant c, take
t=floor(c r/log₂(en/r)). The binomial-volume bound makes this less than
2^(-Ω(r)). Both conditions therefore hold together for large n.
The first also guarantees that U has full column rank.

If k=o(n), the preceding lemma gives

\[
\operatorname{Ham}(B,X)
=\Omega\!\left(\frac{nr}{\log(en/r)}\right)
\]

for every raw-column-span approximation X using at most k columns.
The true low-rank completion has only n directed errors. When
r≈n/log n, every sublinear raw-column subset leaves on the order of
n²/(log n log log n) errors, which is much larger than n^(1+o(1)).

This defeats the proposed repair "select somewhat more noisy raw columns
and decode in their span." Even an arbitrary sublinear oversampling
budget does not give the near-linear residual needed by the local-phase
counter on this family.

It does not defeat nonlinear manufacture of a new code, erasure-based
acquisition, the new polynomial-annihilator mechanism, or arbitrary
low-rank approximation.

## 3. The free diagonal does not trivialize the example

Choose one endpoint of each matching edge as L and the other as R. Then

\[
B[L,R]=D[L,R]+I_{n/2}.
\]

This cut matrix has rank at least n/2−r. Every diagonal completion of B
has the same L-by-R submatrix, so its rank is at least n/2−r. Thus
the example is not merely an unknown diagonal hiding an immediately
low-rank raw matrix. Its true rank-r-plus-matching representation matters.

## 4. Comparison with column-subset literature

Column subset selection over F₂ is established. Dan, Hansen, Jiang,
Wang and Zhou, Low Rank Approximation of Binary Matrices: Column Subset
Selection and Generalizations, MFCS 2018, prove a worst-case
approximation ratio

\[
r/2+1+r/[2(2^r-1)]
\]

for selecting r columns, with an asymptotically tight construction.

https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2018.41

The lemma above records the particular obstruction needed here: a symmetric
alternating matrix, only a perfect matching of corruptions, and a lower
bound that holds for every sublinear raw-column oversampling budget.
It is an elementary coding argument. It is not asserted to be a
historically new general CSS lower bound.

## 5. Executed checks

The file raw_column_failure.py constructs explicit binary code matrices
using finite-field power columns. It does not rely on a claimed coding
distance: it enumerates the primal code and determines dual distance by
an exact small-subset syndrome search, including a witness at the next
weight.

The tested matrices include n=14,r=4; n=30,r=10; n=62,r=18; and
n=254,r=8. Their exact primal/dual distances are stored in
raw_column_failure_results.json. All raw subsets of size zero through
two are checked for n=14. Larger examples use explicitly recorded
sampled subsets, including 16 raw columns against the rank-eight
completion at n=254. Every selected span is exhaustively decoded.

The asymptotic statement covering all sublinear column subsets is proved
above; the finite sampled runs are not represented as exhaustive searches
over all larger subsets.

The execution checked 349 column subsets and 12,094 unselected-column
distances. At n=254 the primal/dual distances were 127 and 3. Selecting
16 raw columns against the true rank-eight model left 864 directed
errors in the examined optimal span approximation, compared with 254
directed errors for D. This is a finite validation of the failure
mechanism, not an asymptotic or practical-speed benchmark.
