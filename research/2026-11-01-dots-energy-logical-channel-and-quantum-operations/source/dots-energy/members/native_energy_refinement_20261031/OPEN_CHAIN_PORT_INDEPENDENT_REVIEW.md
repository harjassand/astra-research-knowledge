# Independent local review: acquired open-chain P/Q coupling port

31 October 2026. Verdict: PASS as a local operator-circuit construction with the stated acquired input access. This is not acceptance of a refined complete compiler, a practical resource advantage, or a generic small-norm block-encoding oracle.

## Source binding

I read the entire `OPEN_CHAIN_VARIANCE_NORMALIZED_PORT.md` and verified SHA-256 `be8c471821bad1bb0e4ae4652984f6ce1f4d7572b7f75af7ae3edb5ff764abdc`. The dense alternative mentioned by the source is not load-bearing for this review. The previously accepted native compiler and its resource audit remain unchanged.

## 1. Coordinates, signs and recurrence

In first-spin/domain-wall coordinates the positive open zero-field reference factors into |+> and bond states phi_j. The stated real orthogonal bond matrix has second column phi_j_perp = (sqrt(1-p_j), -sqrt(p_j)); this phase choice gives Z phi_j = t_j phi_j + sqrt(1-t_j^2) phi_j_perp even when t_j is negative or zero. The prefix-XOR coordinate map makes physical Z_i the product of the global Z and the preceding bond Z operators. There is no hidden sign or reversed path convention.

Every w_j has global |->. If j < ell, its bond ell is phi_ell whereas the corresponding bond of w_ell is phi_ell_perp. Their overlap is therefore zero regardless of the earlier bond overlaps. All w_j have norm one. Expanding the next bond gives v_1 = w_0 and v_(i+1) = t_i v_i + sqrt(1-t_i^2) w_i.

With row labels j = 0,...,n-1 and column label i-1 for physical spin i, the resulting synthesis matrix is exactly D_index (I-S)^(-1), with S|i> = t_i|i-1> for i >= 1. Left multiplication by D is the correct order. The displayed frame coefficients and zero-based factorization agree. Its Gram matrix is the usual path-product correlation matrix, so the stated row-sum norm bound is valid. The acquired normalization chi = 40/39 is slightly more conservative than the abstract norm bound sqrt(41/39); it is chosen because it has a direct circuit construction.

As a diagnostic only, I independently checked W^dagger W = I and W R = [Z_i psi] for 40 small dense cases, n = 1,...,8, with independently sampled positive and negative t_j in [-1/40,1/40]. The maximum matrix residual was 1.74e-15. These numerical checks are not the proof or an implemented quantum circuit.

## 2. Acquired index-to-source isometry

Index erasure is justified by a specific support property, not orthogonality alone. Before applying U_psi, j > 0 is encoded as a definite 1 at bond j, arbitrary earlier bond superpositions, and zeros at every later bond. The highest occupied bond is therefore exactly j on each supported computational basis vector. For j = 0 all bonds are zero and the empty marker convention gives index zero. Compute this marker reversibly, XOR it into the old index, and uncompute the marker workspace while the source is unchanged. Only then apply the bond rotations and coordinate map. This maps |j>|0_source> to |0_index>|w_j> on the valid index subspace with clean work.

The procedure is a composition of reversible gates on the full registers. Invalid binary indices require the stated persistent failure flag and contribute zero to the successful operator block; they are not mapped nonunitarily into a valid w_j. The global input bit is set to 1 so that the global Hadamard produces |->, not |+>. The n = 1 case reduces correctly to this global operation with no bond markers.

A scan over the n bond positions, comparisons with the binary index and controlled known rotations implements the construction with polynomial bit/gate cost. In fact the source's near-linear n count up to routing, coefficient-bit and logarithmic factors is supported by these scans. No arbitrary-label erasure, unknown inverse fibre, or QRAM primitive has been supplied for free.

## 3. Finite Neumann block and errors

The weighted shift is nilpotent of order n and has norm at most tstar = 1/40. A known signed acceptance amplitude t_i/tstar followed by a successful index decrement gives a normalization-one block for S/tstar. Index zero has zero acceptance. The failure flag remains available, so the decrement is not asserted to be a unitary left shift by itself. Negative signs occur in SELECT amplitudes, not in probability weights. D_index is a known diagonal contraction.

The finite geometric LCU with probabilities tstar^ell/chi and a zero arm gives D sum_(ell=0)^L S^ell / chi. Products use fresh success flags, and the LCU index is unprepared only after SELECT. Thus unsuccessful factors cannot reenter the successful product block. The unnormalized coefficient sum is at most chi; equivalently the normalized probabilities sum to at most one, which is the precise reason the zero-arm padding is nonnegative.

The discarded unnormalized operator tail is bounded by tstar^(L+1)/(1-tstar); division by chi can only improve this bound. Taking the stated logarithmic L, capped at n-1, suffices. If capped at n-1 there is no truncation error at all. No division by a small t_i occurs, and exactly zero t_i is harmless.

The coefficient list, geometric probabilities and index scans are known finite data. Allocating an absolute unitary/block synthesis error to each of the explicitly capped operations and telescoping products yields the claimed operator error, uniformly on inputs and references. There is no dimension-times-entrywise error conversion: the argument concerns the actual composed block unitaries and their operator norms. The tail bound and synthesis budget should each receive a fixed fraction of the requested final tolerance, an ordinary constant-factor budget adjustment. No unpriced singular-value amplification or dense n-dimensional unitary synthesis is needed for this Neumann implementation.

## 4. System stack and full operator identity

For individually acquired Hermitian A_i/alpha_i, prepare amplitudes alpha_i/q_A, where q_A^2 = sum_i alpha_i^2, and retain the label through SELECT. The successful rectangular block is sum_i |i>A_i / q_A. Its normalization is valid because sum_i A_i^2 <= q_A^2 I, without requiring the A_i to commute. Certified zero-normalization terms are omitted. If all terms vanish, the port is zero and this positive-q_A construction is unnecessary.

On arbitrary system/source input, first apply U_psi^dagger to the source and mark its all-zero subspace as a block success condition. On that branch it supplies the bra <psi| and a clean source register. Apply the retained-index system stack, R/chi, and the actual W index-to-source isometry. The successful operator is

 sum_i A_i tensor |Z_i psi><psi| / (chi q_A) = Q K P / (chi q_A).

The Q identity holds because all output frame vectors have global odd spin while psi has global even spin. This is a linear block-encoding identity on every input, not a normalized postselection protocol. All failure flags, including the input-source projection and invalid-index flag, are included in the successful-block definition. Reversing the full unitary obtains the adjoint port with the same normalization and error.

Attenuating by one half gives the stated slack block. Comparing chi q_A with the already acquired coherent LCU normalization b permits the better of two actually available circuits, with rho = min(b, chi q_A). For rational supplied alpha_i the comparison can also be made by squaring positive quantities; more general refinable normalizations need the ordinary certified comparison/padding conventions. This does not turn an unrelated opaque K/b oracle into individually accessible A_i. The source's explicit SELECT and record-lookup costs must remain in any downstream resource calculation.

## 5. Scope of acceptance

The operation is earned specifically for the open zero-field independent-domain-wall source and the individually supplied A_i. Periodic boundaries, fields, generic Gibbs states or a single generic coupling oracle do not inherit this access result. A norm certificate alone still does not implement a small-normalization port. Likewise, the acquired offdiagonal block does not remove QQ interaction costs, source decay conditioning, jump normalization, initial energy or control costs.

No load-bearing correction is required to the source. The small normalized-versus-unnormalized weight distinction above is merely an explicit interpretation of its existing formulas. Any claimed improved complete simulator still requires a separate positive-sector, first-event, numerical-budget and resource receiving proof. The frozen billions-of-slots audit is not changed by this local PASS.
