# Audit: acquired low-rank-plus-sparse quadratic backgrounds

27 October 2026. This audits the parent's repaired acquisition algorithm, including the distance-pruning step that removes the earlier 2^(r^2) coefficient search. The structural lemma is unconditional. The final counting consequence is conditional on the separately audited phase-product extension of the governing manuscript.

## Finding

The repaired argument is valid. It deterministically acquires an exact alternating low-rank-plus-sparse representation after deleting a bounded input set. It requires neither a supplied decomposition nor incoherence, bounded maximum error degree, or a favorable graph decomposition. The Boolean unary correction in Section 4, explicit entropy accounting, and streaming requirement are necessary.

## 1. A clean column code exists after a small unknown erasure

Let B be an explicitly given alternating n-by-n matrix over F_2. Suppose there exist alternating A,S such that

    B=A+S, rank A<=r,

and S has at most M unordered nonzero off-diagonal entries. Neither A nor S is supplied. If S is described as an undirected error graph, alternation of A follows automatically from B=A+S.

Fix an integer Delta>=1. In the hidden error graph let H contain vertices of degree greater than Delta. Its degree sum is at most 2M, so |H|<=2M/Delta. Choose a basis of the columns of A[H^c,H^c], indexed by I with |I|<=r. Let J be all error-neighbors of I within H^c. Then |J|<=r Delta. Set

    E0=H union J,   s0=floor(2M/Delta)+r Delta,   R0=E0^c.

The raw columns B[R0,I] are exactly A[R0,I], and their span contains every column of A[R0,R0]. This remains true even when I meets E0: the columns are read from the original B, not required to be retained variables. Restricting a valid basis relation on H^c proves the span assertion.

## 2. Distance pruning removes coefficient-matrix enumeration

For a candidate I,E0, compute a full-column-rank basis U of B[R0,I]. View its column span as a binary linear code on R0. While this code has a nonzero word of weight at most 2Delta:

1. Find such a word by enumerating its at most 2^r coefficient vectors.
2. Delete the word's support from the current retained coordinates R.
3. Restrict the code and compute a new column basis.

The selected nonzero word lies in the kernel of the restriction map, so the code dimension strictly drops. There are at most r rounds. Each deletes at most 2Delta coordinates. The final deleted set E therefore satisfies

    |E| <= floor(2M/Delta)+3r Delta.

Every choice of a qualifying word works; no backtracking on that choice is needed.

For the correct initial witness I,E0, each column of the true restricted A remains in the restricted code after every deletion. Also all retained vertices lie outside H, so every column of the remaining error matrix has weight at most Delta. At termination the nonzero code distance is greater than 2Delta. Therefore each column of B[R,R] has a unique codeword within Hamming distance Delta, namely its true A-column.

Decode each column by enumerating the codewords. If any column has no close codeword, reject the candidate. Finally verify that the decoded matrix C is symmetric with zero diagonal, has rank at most r, and that B[R,R]+C has at most M unordered edges. These are polynomial-time exact checks. Wrong initial witnesses cannot cause an incorrect accepted representation. The correct witness necessarily succeeds and recovers the true A[R,R].

No alternating coefficient matrix K is guessed. Once C is decoded, one can either Gaussian-eliminate C directly or compute K=L_U C L_U^T for a left inverse L_U of the retained full-rank U. Then C=U K U^T and K is alternating. The earlier 2^[r(r-1)/2] enumeration has genuinely disappeared.

## 3. Complete discovery cost and the larger admissible range

Enumerate all I with |I|<=r and all E0 with |E0|<=min(s0,n). The pruning and decoding for each candidate cost poly(n)2^r time and polynomial space. All codewords are generated sequentially, not stored as an exponential table.

The acquisition bound is

    poly(n) 2^[O(r log(en/r)+s0 log(en/s0)+r)],

with endpoint conventions and caps at n. The output branch set has size

    s <= floor(2M/Delta)+3r Delta.

For r>=1, choosing Delta=max(1,ceil(sqrt(2M/(3r)))) gives

    s <= 2sqrt(6rM)+3r.

Using the simpler ceil(sqrt(2M/r)) changes only constants. For r=0, take the sparse matrix directly, with no erased set or code search. If M=0, ordinary rank checking is an optional immediate fast path.

If

    r=o(n),   rM=o(n^2),

then s0,s=o(n). Both entropy terms are o(n), including when r is much larger than n^o(1). Thus acquisition itself is subexponential in n and polynomial-space. In particular M=O(n) allows EVERY r=o(n).

The parameters r,M may be search budgets rather than a supplied representation. If a fully parameter-free algorithm is desired, their polynomially many integer possibilities can be dovetailed or ordered by explicit worst-case work bounds, with polynomial overhead relative to the best successful budget. An uncontrolled sequential search that spends excessive time on an earlier failed budget would not prove that assertion.

## 4. Necessary unary correction and exact Walsh reconstruction

For an alternating matrix C define q_C(x)=sum_(i<j) C_ij x_i x_j. If C=U K U^T, it is generally FALSE that q_C(x)=q_K(U^T x) as Boolean polynomials. Substitution can create unary terms. The correct identity is

    q_C(x)=q_K(U^T x)+ell·x,
    ell_i=q_K(row_i U).

Both sides have the same polar form; their difference is linear and evaluation on coordinate vectors gives ell. A concrete counterexample to omitting it is U with rows (1,1),(1,0),(0,1) and K=[[0,1],[1,0]]. Then C is the triangle adjacency matrix, but

    q_K(U^T x)=x1+x1x2+x1x3+x2x3.

For a in F_2^d, where U has d<=r columns, compute the integer quadratic Walsh sum

    W_K(a)=sum_z (-1)^[q_K(z)+a·z]

by exact polynomial-time Gaussian elimination. Then

    (-1)^q_C(x)
      =2^(-d) sum_a W_K(a)(-1)^[(Ua+ell)·x].

At most 2^r characters are needed. Stream them and compute their Gaussian coefficients individually; a stored 2^r-entry table is not polynomial space when r grows. Sum W_K(a) times the corresponding exact inner signed counts as integers, and divide by 2^d only after finishing that sum. The division is exact. Intermediate integers have O(n+r) bits.

## 5. Exact original-input counting

Consider sum_x (-1)^[q_B(x)+P(x)], where P is a program of m explicitly local, fixed-degree phase factors on the original n variables. For each assignment to the acquired deleted set E, interactions of E with R become unary phases and the E-E interaction is a known constant. These are computed from B itself. Restrict P by the same assignment; factor locality does not increase.

On R the accepted representation is C plus at most M sparse quadratic factors. Walsh expansion of C adds only unary phases, including ell. Every inner phase-counter call therefore has at most

    m+M+O(n)

local factors. If m+M=n exp(o(log n)) and r=o(n), rM=o(n^2), the retained input count n-|E|=(1-o(1))n stays comparable to the original n. The phase-product theorem computes each exact inner signed sum in 2^o(n) time and polynomial space.

Total time is

    poly(L+n) 2^[O(r log(en/r)+s0 log(en/s0)+r)+s+r+o(n)]
      = poly(L+n)2^o(n).

The E assignments are disjoint original-input branches and are summed without normalization. Only the known Fourier denominator is divided out, after exact reconstruction. This proves the stronger conditional regime with arbitrary sublinear r when the sparse error count is linear.

## 6. Prior-art positioning

Subexponential acquisition of unknown near-low-rank binary matrices is established parameterized-algorithm machinery. Fomin, Golovach and Panolan, *Parameterized Low-Rank Binary Matrix Approximation* (ICALP 2018), give Low GF(2)-Rank Approximation in

    2^[O(r^(3/2) sqrt(k log k))] (nm)^O(1).

Primary sources: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2018.53 and https://arxiv.org/abs/1803.06102 . Thus the earlier n^o(1)-rank acquisition scale should not be presented as the first subexponential rigidity-recovery principle.

The current construction deliberately solves a different intermediate task: exact alternating recovery after a small erased vertex set, followed by branching those original bits. It has an elementary polynomial-space proof and admits r=o(n), rM=o(n^2). A direct import of general matrix approximation would require checking alternation and space guarantees; naive symmetrization over F_2 is invalid. The final original-input phase-counting theorem composes this acquired representation with the new phase-product counter.

## Audit conclusion

No gap was found in the repaired acquisition argument or its conditional counting consequence. Its useful representation is found and independently validated. The theorem remains restricted by rank-plus-sparse rigidity; it does not solve arbitrary dense quadratic backgrounds combined with nonlinear phases.

## Executed independent checks

`lowrank_sparse_audit_checks.py` implements its own streamed column-code pruning and radius decoder. Its decoder receives only B and a candidate I,E0,Delta,M,r; hidden matrices are used only in the separate existence-witness tests. It also runs complete candidate searches on small raw matrices without passing their hidden decomposition to the search.

The executed run passed 25 hidden-witness fixtures, four complete unknown-decomposition searches, 17 exhaustive mixed quadratic/cubic phase counts, and 3,268 exact Walsh/substitution identities. It exercised 29 strict code-rank-drop pruning steps. Thirteen fixtures deleted one or more basis-column indices; one explicit fixture deletes BOTH basis indices before decoding and still recovers the nonzero retained rank-two matrix. The triangle fixture verifies that the unary correction is actually nonzero and necessary.

The larger representation-only fixtures have up to 100 variables, including a dense rank-two component plus concentrated extra rank directions that trigger pruning. Their representations and sampled exact algebra identities are checked; no exhaustive 100-variable count or practical speed claim is made. Actual results are in `lowrank_sparse_audit_results.json`. Finite phase sums use exhaustive enumeration and do not execute the source's asymptotic counter.
