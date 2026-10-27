# Audit: low-rank completion after acquisition of bounded cubic blocks

27 October 2026. This is a mathematical comparison, not an execution report.
The block-acquisition/centroid step is assumed to be the parent's separately
audited compiler. Nothing here assumes that a rank completion is supplied.

## Verdict

The proposed alternating-completion search is a valid-looking constructive
certificate search, based on a standard Schur-complement identity. However,
its stated evaluation family is already covered by directly computable
cut-rank methods once the bounded blocks have been acquired. There is a
faster exponential-space algorithm and a polynomial-space algorithm with
the same subexponential parameter regime. Completion need not be searched
for, and no general rank-width recognition routine is needed.

Consequently the completion search should not be presented as removing an
algorithmic obstruction for this family. It can be retained as an independent
representation certificate or implementation alternative. Any remaining
scientific contribution must be located in acquisition of the blocks or in
the subsequent sparse-plus-low-rank interface, not in this counting corollary.

## Setting

Partition the variables into blocks `V_1,...,V_s`, each of size at most `b`,
and let

    Z = sum_x (-1)^{Q_cross(x)} product_i F_i(x_{V_i}),

where `F_i` is any exactly evaluable block function, including its cubic,
quadratic and linear phases. Let `B` record the prescribed cross-block
quadratic coefficients. Within-block entries are immaterial because they
can be absorbed into `F_i`.

Suppose there exists a symmetric alternating completion `B*` over `F_2`
with rank at most `r`, agreeing with every prescribed cross-block entry.
For every union `S` of whole blocks,

    B[S, V\S] = B*[S, V\S],
    rank B[S,V\S] <= r.                                  (1)

These cross-cut matrices are fully specified in the input, independent of
the unknown diagonal-block completion. Every displayed rank can be computed
by ordinary Gaussian elimination.

## Stronger time comparator: direct signature dynamic programming

Order the blocks arbitrarily. For a processed prefix `S` with remaining
variables `T`, the only dependence of its assignments on the future is

    sigma = B[S,T]^T x_S.

Store the aggregate internal weight `D_S[sigma]`. There are at most
`2^{rank B[S,T]}` states. When adding the next block `W` and choosing
`z in F_2^W`, the transition is

    D_{S union W}[sigma|_{T\W} + B[W,T\W]^T z]
      += D_S[sigma] F_W(z) (-1)^{sigma|_W . z}.            (2)

This identity follows by separating the new block's internal weight from
its interactions with the already processed variables. It does not depend
on a completion or on the form/degree of the local block function.

Define the actual measured prefix parameter

    w = max_prefix rank B[S,V\S].

Precompute it in polynomial time. The algorithm takes

    poly(n,L) 2^{w+b} time,
    poly(n,L) 2^w space.                                 (3)

If a rank-r completion exists, `w<=r` by (1). Thus this already beats
`binom(n,r) 2^{br}` completion search in time. The algorithm can simply run
using its measured `w`; it need not decide whether a low-rank completion
exists.

### Exact prior comparator

De Colnet et al., *Quadratic Sums-of-Powers for Fixed-Parameter Tractable
Quantum-Circuit Simulation*, arXiv:2605.29944v1, Section 4, explicitly uses
the boundary signature `x_S^T B[S,V\S]`. Theorem 2 gives exact evaluation in
`2^{O(k)} poly(n)` time and exponential-in-k working space on a supplied
rank decomposition. The block version above changes the leaf initialization
from two assignments to at most `2^b` assignments. Its join/signature
invariant is unchanged. For a path of blocks, equation (2) is the simpler
one-block-at-a-time specialization.

Primary source, relevant algorithm and proof read:
<https://arxiv.org/html/2605.29944v1>

This block transfer is proved above; the paper should not be quoted as
literally stating that exact block formulation. In the present family the
needed layout is constructed by any ordering of the already acquired
blocks, so “a decomposition must be supplied” is not a separation from it.

## Polynomial-space comparator: recursive Fourier splitting

The space distinction does not rescue the qualitative subexponential claim.
Here is an explicit streaming algorithm, derived directly from the
bilinear-character identity.

Split a collection of whole blocks into two balanced parts `A,D`. Factor
its fully specified cross matrix

    C = B[A,D] = L R^T,

where `d=rank(C)`, `L` has `d` independent columns and so does `R`.
For `p=L^T x_A`, `q=R^T x_D`, orthogonality gives

    (-1)^{p.q}
      = 2^{-d} sum_{u,v in F_2^d}
                  (-1)^{u.v + u.p + v.q}.                (4)

Indeed, summing `u` first forces `v=p` and leaves `2^d(-1)^{p.q}`.
Consequently, for any accumulated unary character `ell`,

    Z_{A union D}(ell)
      = 2^{-d} sum_{u,v} (-1)^{u.v}
            Z_A(ell_A+Lu) Z_D(ell_D+Rv).                 (5)

Each child has the same local block functions and internal quadratic
interactions; the only alteration is a unary character. Thus (5) may be
applied recursively without introducing a new global constraint or
increasing the structural parameter. Every submatrix rank is at most `r`
when the proposed completion exists.

Construct the balanced block tree and compute its cross ranks in polynomial
time; let their maximum be `w_bal`. Stop recursion once a node contains
`O(w_bal+b)` variables and evaluate that leaf by enumeration. Streaming the
character pairs, without memoization, gives

    T(N) <= 2 * 4^{w_bal} T(N/2 + O(b))
              + poly(n,L) 4^{w_bal},

and hence

    T(n) = poly(n,L)
           2^{O((w_bal+b) log(2+n/(w_bal+b)))}.           (6)

For fixed `b` and `r>=1`, the coarser bound is
`poly(n,L) 2^{O(r log(2+n/r)+b log n)}`; either suffices.
When `r=0`, simply multiply the independent block sums.
The recursion stack, cut factorizations and counters occupy polynomial
space. Exact arithmetic uses the same fixed cyclotomic field as the input;
the only new divisions are powers of two. Partial accumulator magnitudes
and denominator exponents have polynomially many bits. Therefore every
`r=o(n)` completion family is evaluated in `2^{o(n)}` time and polynomial
space, without acquiring the completion.

No specific prior paper is being credited with formula (6) as stated here.
It is an elementary time-space transfer from the same cut-rank structure,
and it prevents a claim that the completion-search method is the only
polynomial-space route to this regime.

## The completion formula itself

For a symmetric matrix of rank `r` with invertible principal submatrix
`A=B[I,I]`, reorder the matrix as

    [ A  D ]
    [ D^T E].

Block Gaussian elimination gives

    rank(B) = r + rank(E-D^T A^{-1}D).

Thus rank exactly `r` forces `E=D^T A^{-1}D`, equivalently

    B = B[:,I] B[I,I]^{-1} B[I,:].                        (7)

This is the standard exact skeleton/Schur-complement identity. Alternating
matrices have even rank and admit a nonsingular principal submatrix of
that rank, by alternating Gaussian elimination. In the parent's missing
diagonal-block pattern, guessing `I` and the unknown entries incident with
its rows then gives the proposed bound, after validating all prescribed
entries and alternation. Searching all even ranks up to the budget is
needed when rank-at-most rather than exact rank is intended.

For primary ancestry of skeleton decompositions and the symmetric Nyström
form, see Chiu–Demanet, *Sublinear randomized algorithms for skeleton
decompositions*, Sections 1.1–1.3:
<https://arxiv.org/pdf/1110.4193>
That numerical paper is not being cited for the exact finite-field
bounded-block search. I did not locate an earlier statement of precisely
that search in this targeted lookup. The identity, rather than this
particular enumeration bound, is what is standard.

## A strict separation in the other direction

Arrange b=3 blocks in a path. Put an arbitrary cubic phase in each block
and quadratic edges only between one designated variable in consecutive
blocks. Every prefix cut has rank at most one, so (3) is polynomial time.
But the cut separating odd from even blocks has rank linear in the number
of blocks. No within-block correction changes that cut matrix, so every
completion has linear rank. Hence the cut-signature method covers families
that low global completion rank does not. This is a mathematical family
comparison, not an executed benchmark.
