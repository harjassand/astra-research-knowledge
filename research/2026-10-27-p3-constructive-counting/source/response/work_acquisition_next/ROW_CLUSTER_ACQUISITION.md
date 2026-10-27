# Polynomial acquisition from hidden row diversity

27 October 2026. This is a proved restricted-family extension, not a general repair of low-rank acquisition. Its metric-clustering component is established prior work. Exact counting uses the saved local-phase theorem and quadratic-refinement compiler.

## Theorem

Let B be a raw alternating binary n by n matrix. Suppose, without supplying the witness, B=off(D)+S, where D is symmetric with at most c distinct rows and S has at most M unordered edges. There is a deterministic polynomial-time algorithm returning a symmetric C with at most c distinct rows, hence rank at most c, and an exact residual B=off(C)+S' with at most 40M+20n edges. No coordinates are deleted, and neither the partition, diagonal, completion nor errors are supplied.

The guarantee has no product restriction cM=o(n^2). Its stronger structural assumption is small row diversity: a rank-r binary matrix can have 2^r row types. If c=o(n) and m+M=n^{1+o(1)}, combining the acquired representation with the saved local-phase theorem gives exact phase counting in poly(L+n)2^{o(n)} time and polynomial space, conditional on the governing replacement-form manuscript. All added residual factors have arity two.

## Raw algorithm and cost

Compute Hamming distances between observed rows. Start with any c row indices as facilities. Repeatedly replace one facility by another observed row whenever this strictly reduces the sum of each row's distance to its nearest facility. Stop at an exact one-swap local optimum. Assign rows to nearest facilities with deterministic tie-breaking; remove empty classes. For every unordered pair of classes, including a class paired with itself, fill that block by the majority bit of its raw B entries, choosing zero on ties. This defines C. Verify symmetry, block constancy, binary rank and the exact residual.

The objective is an integer between zero and n^2, so at most n^2 swaps occur. With nearest and second-nearest distances, each proposed swap costs O(n) arithmetic operations, at most cn swaps are considered per round, and total time is O(c n^4) plus polynomial preprocessing. Space is polynomial. A simpler implementation can use a higher polynomial. The budget c need not be supplied: running c=1,...,n adds a polynomial factor, and each output is independently checked. Also include the zero completion.

## Proof

Let epsilon_i=dist(B_i,D_i), including the diagonal. Their sum E is at most 2M+n. In each hidden equal-row class A, choose an observed row j minimizing epsilon_j. The triangle inequality gives dist(B_i,B_j)<=epsilon_i+epsilon_j. Summing yields cost at most 2 sum_(i in A)epsilon_i. Therefore the optimum observed-row c-median cost is at most 2E.

### One-swap local search costs at most five times optimum

This is the classical Arya--Garg--Khandekar--Meyerson--Munagala--Pandit locality-gap theorem. A short standard exchange proof is included.

Let F be the local solution and O an optimal set, both of size c. Map each o in O to a nearest facility phi(o) in F. Pair every facility of F with exactly one preimage with that preimage. Pair the remaining optimal facilities with zero-preimage facilities of F, closing each at most twice. Such pairing exists: if a optimal facilities remain and b facilities have at least two preimages, then b<=a/2 and there are a-b>=a/2 zero-preimage facilities.

For each selected swap f to o, send clients whose optimum facility is o to o. A client j whose current facility closes and whose optimum is some other o_j can be sent to phi(o_j), which remains open. If F_j,O_j denote current and optimum distances, then dist(j,phi(o_j))<=2O_j+F_j by triangle inequalities. Sum the nonnegative local swap changes. Every optimum facility opens once and every current facility closes at most twice, giving 0<=sum_j(O_j-F_j)+4sum_j O_j. Thus cost(F)<=5cost(O). If an optimum facility is already open, the formal swap is null or only removes a facility, so its non-improvement follows from monotonicity. The proof also applies to duplicate observed rows (a pseudometric).

The acquired assignment therefore has row cost K<=10E.

### Symmetric block rounding

Let X repeat each assigned facility row on its whole class. Then dist(B,X)=K and, because B is symmetric, dist(B,X^T)=K. Fix an ordered block A x T. Write R,Q for its contributions to these two distances. Choose a uniform u in A and v in T. Filling the entire block by B_uv incurs expected error at most 2R+2Q: use

    [B_ij != B_uv] <= [B_ij != B_uj] + [B_uj != B_uv],

then X_ij=X_uj for the first comparison and X^T_uj=X^T_uv for the second. Summing and averaging bounds each term by twice the corresponding block discrepancy. The majority constant does no worse. Summing ordered blocks gives dist(B,C)<=4K.

Transposed blocks have the same majority, so C is symmetric. Let U be the class-indicator matrix and H the symmetric table of block-majority bits, including diagonal blocks. Then C=UHU^T and rank(C)<=c. Off-diagonal errors count twice in full matrix distance, hence edges(B+off(C))<=2K<=20E<=40M+20n. This proves acquisition.

## Exact reconstruction

Apply the saved fourth-root quadratic refinement to C=UHU^T. Its latent function on at most c parity summaries has 2^c Walsh characters, with polynomial-time Gaussian-integer coefficients per character. Every character modifies only original-variable unary phases. The residual contributes at most 40M+20n quadratic factors. The local-phase theorem applies whenever this plus the foreground factor count has n^{o(1)} density. Reconstruct exact integral cyclotomic coordinates before division by 2^c.

The companion program actually acquires partitions and completions from raw matrices and validates exact phase sums. Its inner phase backend is exhaustive enumeration; no asymptotic solver execution or practical speedup is claimed.

## Scope and ancestry

Small row diversity is a graph blow-up / neighborhood-diversity type promise, substantially stronger than small binary rank. This construction combines known metric clustering, an elementary symmetric rounding bound and the acquired phase interface. It removes the cM restriction for this family but does not establish first priority or a foundational breakthrough. Matrices with low rank and many distinct rows fall outside the promise.

There is a decisive explicit failure of promoting it to arbitrary low rank. Let n=2^r, index rows and columns by all vectors of F_2^r, and set D_uv=u.v. Then rank(D)=r, yet all n rows differ and every two distinct rows have Hamming distance n/2. For any approximation C with at most c distinct rows, let A be one equal-row class. If its size s is at least two, summing pairwise triangle inequalities around the common approximating row gives dist(D[A,:],C[A,:])>=sn/4. At least n-c rows belong to nonsingleton classes, so dist(D,C)>=(n-c)n/4. Removing D's diagonal changes at most n entries, and the off-diagonal residual therefore has at least n(n-c-4)/8 edges. Thus c=poly(r) leaves a quadratic number of errors, although the generic free-diagonal rank-r compiler handles the original matrix with M=0. These are incomparable structural promises, not a generic low-rank improvement. The program executes this failure family through n=256.

Arya et al., Local Search Heuristics for k-Median and Facility Location Problems, SIAM J. Comput. 33(3), 544--562 (2004), Sections 2--3, proves the one-swap factor five. The source uses thresholded improvements for arbitrary metric bit complexity; bounded integral Hamming costs here permit exact strict-improvement termination in polynomial time.

https://www.cse.iitd.ernet.in/~pandit/lsearchSICOMP.pdf

https://doi.org/10.1137/S0097539702416402

Binary clustering / few-row-type matrix editing already occurs in Fomin--Golovach--Panolan, Parameterized Low-Rank Binary Matrix Approximation, ICALP 2018 and the 2020 journal version. This is not a new clustering problem.

https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2018.53
