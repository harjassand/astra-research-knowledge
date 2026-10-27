# Actual-implementation audit and diagonal-completion repair

27 October 2026. This supplements `LOW_RANK_SPARSE_AUDIT.md`; it does not repeat that proof. The files audited are the root implementations `work_mixed_root/mixed_quadratic_compiler.py` and `work_mixed_root/diagonal_completion_compiler.py`.

## 1. Actual alternating implementation

No mathematical or implementation error was found in its documented input domain: a raw alternating binary matrix, nonnegative budgets, and valid variable supports. Symmetric rows correctly serve as columns. Every accepted candidate has an independently checkable exact equality on the retained variables. The optional removal caps restrict the search and do not have the unrestricted completeness guarantee.

The compact factorization uses an invertible row minor of the retained column generators. Its unary correction is present. The exact finite counter includes constants from fixed variables, all fixed-to-retained quadratic interactions, the residual sparse quadratic phase, and the correction from changing quadratic coordinates. It reconstructs each cyclotomic coordinate as an integer before dividing by the Fourier denominator. It also works when the retained code dimension exceeds the rank of the recovered quadratic matrix.

The focused executable `root_mixed_focus_checks.py` passed seven full-rank boundary fixtures, replayed 46 punctures, checked twelve rejection assertions, and independently evaluated sixteen exact phase sums. The rejection paths include failed radius decoding, nonsymmetric decoding, nonzero decoded diagonal, an excessive residual edge count, and an imposed removal cap.

### Full-rank boundary

For even n, take B=J+I over F_2 and all n columns as the pivot set. B is invertible. After any coordinate deletion its restricted column span is the entire remaining coordinate space. If any coordinate remains, that space has a word of weight one. Therefore puncturing until the nonzero distance exceeds two must delete every variable. The actual implementation does so.

This is not a counterexample to the theorem: r=n lies outside its sublinear-rank regime. It identifies a real limitation of that representation and supplied candidate code.

## 2. An acquired diagonal changes the relevant rank

Allow a hidden symmetric matrix D, with unrestricted diagonal, and a hidden sparse alternating S such that

    B = offdiag(D) + S,   rank(D)<=r,   edges(S)<=M.

Neither D nor its diagonal is supplied. Fix decoding radius delta>=1. Let H be the vertices of S-degree at least delta. Then

    |H| <= floor(2M/delta).

Choose a column basis I of D on H^c. The other vertices have sparse degree at most delta-1. Erase H, the sparse neighbors of I, and I itself. This last set removes every unknown diagonal error in the chosen columns. The initial erasure budget is therefore

    s0 = floor(2M/delta) + r delta.

On the remaining rows the raw columns B[:,I] are clean columns of D and span its retained columns. A target column differs from its true D-column in at most delta positions: at most delta-1 sparse errors and its one diagonal position.

The same short-word puncturing now uses threshold 2 delta and deletes at most 2r delta additional coordinates. Unique radius-delta decoding recovers D for the existence witness. Arbitrary candidates are accepted only after symmetry and the OFF-DIAGONAL residual edge budget are verified. The final budget is

    s <= floor(2M/delta) + 3r delta.

No diagonal vector is enumerated. The old entropy and polynomial-space bounds remain unchanged. In particular, choosing delta=max(1,ceil(sqrt(2M/(3r)))) gives

    s <= 2 sqrt(6rM) + 3r.

The root implementation uses `threshold=delta-1`; zero is a valid threshold. Its default parameter selection and floor in the initial bound agree with this improved proof. The rank-zero direct sparse case correctly bypasses radius decoding.

## 3. The exact fourth-root identity

For a symmetric binary matrix D define its classical quadratic refinement

    Q_D(x) = sum_i D_ii x_i + 2 sum_(i<j) D_ij x_i x_j   (mod 4).

Its polarization on the binary vector group is

    Q_D(x+y)-Q_D(x)-Q_D(y) = 2 x^T D y   (mod 4).

Here x+y means binary addition. If D=U K U^T, K is symmetric, and v_i=D_ii, then

    Q_D(x) = Q_K(U^T x) + 2 ell.x   (mod 4),
    ell_i = [D_ii-Q_K(row_i(U))]/2   (mod 2).

The numerator is even. The two forms have the same polarization, so their difference is an additive map into {0,2}; evaluating it on coordinate vectors gives ell. Consequently

    (-1)^q_offdiag(D)(x)
      = i^Q_K(U^T x) (-1)^(ell.x) i^(-sum_i v_i x_i).

This is why an arbitrary symmetric decoded diagonal is valid. Discarding that diagonal without the extra fourth-root unary factors would be incorrect.

Expand the latent function i^Q_K by binary Walsh characters. Its coefficients

    G_K(a) = sum_z i^[Q_K(z)+2a.z]

are Gaussian integers. The Fourier denominator is 2^d, where d is the number of retained generators. The source phase-product counter already admits fixed power-of-two root order, so promoting an originally real phase to root order four costs only a fixed algebra dimension. All added phases on original variables are unary. For order eight the Gaussian-integer weights are multiplied in the integral basis 1,zeta_8,zeta_8^2,zeta_8^3, with i=zeta_8^2.

The implementation performs this coordinate multiplication exactly and checks divisibility before the denominator is removed. It handles negative coefficients and cancellations, including final sums with several nonzero cyclotomic coordinates.

### Polynomial Gaussian evaluation

Write the current fourth-root form as sum_i a_i z_i + 2 sum_(i<j) B_ij z_i z_j. If a_i is odd and L is the parity of its active neighbors, summing z_i gives

    1+i^a_i (-1)^L = (1+i^a_i) i^(-a_i L).

Modulo four, a parity L equals the sum of its variables minus twice their pairwise products. Thus eliminate i by multiplying the Gaussian-integer prefactor by 1+i^a_i, subtracting a_i from every neighboring linear coefficient, and toggling the clique among those neighbors. Once all linear coefficients are even, the remaining sum is an ordinary binary quadratic Gauss sum. Each elimination and its exact integer arithmetic has polynomial cost.

The root `gaussian_i_sum` implements this identity correctly. Its update order, signs, removed-coordinate handling, and final binary-Gaussian call were checked independently.

## 4. What this repair removes, and what puncturing still cannot promise

For B=J+I, the diagonal completion D=J has rank one even when B has rank n. The raw search acquires it after deleting one vertex, without receiving the diagonal or the completion. Our executable verified this through n=32; it also checked mixed nonlinear phase sums at orders two, four, and eight on the smaller fixtures.

The repair absorbs an entire old obstruction family. Partition n=rL coordinates into r nonempty equal blocks, let U contain their indicator columns, and take an invertible alternating K. Put

    A=U K U^T,
    S=disjoint union of cliques within the blocks.

Then S=U U^T+I and

    B=A+S=U(K+I)U^T+I.

The old representation has M=r L(L-1)/2, so rM is of order n^2 when L grows. Its clean-column existence witness can erase almost everything: every basis uses a column from each block, whose sparse neighbors cover the other block vertices. The new symmetric completion U(K+I)U^T has rank at most r and ZERO sparse off-diagonal errors. Its parameters therefore satisfy the new theorem whenever r=o(n). No modular partition needs to be supplied to the general search.

There is still a precise worst-case limit to the generic distance-pruning subroutine. For a code spanned by r disjoint block indicators of block length L<=2delta, every nonempty retained block contributes a nonzero word of weight at most 2delta. Reaching distance greater than 2delta forces the deletion of every coordinate. When L is proportional to delta, this is Omega(r delta) deletions. Thus the subroutine has no uniform o(r delta) erasure bound over all binary linear codes.

Together with the sharp degree-sum estimate O(M/delta), this explains the square-root budget in the current generic proof. It does NOT establish a lower bound for exact counting, for recovering an alternative completion, or even for all candidates examined by this acquisition algorithm. The preceding diagonal repair itself shows why such a stronger inference would be false: a different representation can change both r and M drastically. Further progress should seek a cheaper acquired code or absorb structured residuals into a more permissive algebraic phase, rather than assert that rM=o(n^2) is a computational barrier.

`puncture_boundary_checks.py` executed nine disjoint-block code obstructions and six block-clique repair fixtures, with up to 96 variables. The old clean-column witnesses erased all n variables. The symmetric-completion witnesses erased only r vertices and left zero sparse errors. These latter comparisons deliberately use the two explicit existence witnesses; they are not represented as full unknown-decomposition searches. They also passed 576 sampled exact quadratic-refinement identities. Results are retained in `puncture_boundary_results.json`.

## 5. Executed independent checks of the symmetric implementation

`diagonal_completion_focus_checks.py` passed:

- Eight complete raw searches on full-rank J+I matrices, all acquiring rank one after one erasure.
- Ninety-six replayed punctures for deliberately supplied full-rank codes.
- Twelve hidden-witness fixtures, including odd completion rank, mixed diagonals, concentrated errors, and 40-variable representation tests.
- Thirty-six independently evaluated exact mixed phase sums at orders two, four, and eight.
- 1,659 quadratic-refinement identities.
- 144 additional exhaustive Gaussian checks in dimensions five through ten.
- 48 Gaussian magnitude/cancellation checks in dimensions 24, 40, and 64.
- Four rejection paths and a retained code whose dimension exceeds the recovered rank.

The larger Gaussian checks independently use the identity |G_K(a)|^2=0 when Q_K(z)+2a.z is nonzero on the radical of K, and otherwise |G_K(a)|^2=2^(n+dim(radical)). Small checks compare the full signed complex value, not just its magnitude. Exact script outputs and source hashes are retained in `diagonal_completion_focus_results.json` and `root_mixed_focus_results.json`.

These are checks of real code and exact reconstruction. The phase backend remains finite exhaustive enumeration; no practical speedup or execution of the asymptotic replacement-form engine is claimed.

## 6. Prior-art boundaries

Free diagonal binary minimum rank is an established graph/matrix parameter. Jason Grout's *The minimum rank problem over finite fields* characterizes the finite-field minimum-rank graph families. The present acquisition proof should not present this parameter as new: https://journals.uwyo.edu/index.php/ela/article/view/805 .

Classical quadratic forms modulo four and their polynomial-time Gauss evaluation are also established. Relevant primary sources include Dehaene and De Moor, *The Clifford group, stabilizer states, and linear and quadratic operations over GF(2)*, https://arxiv.org/abs/quant-ph/0304125 , and Guan and Regan, *Stabilizer Circuits, Quadratic Forms, and Computing Matrix Rank*, especially Sections 3–4, https://arxiv.org/abs/1904.00101 .

The claim to assess is the complete acquired representation and its composition with the separately proved local phase-product engine, including its original-input complexity and bit costs. This audit does not establish priority over all possible existing minimum-rank approximation algorithms.
