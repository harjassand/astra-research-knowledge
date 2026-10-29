# Independent review: direct small-code star-loss transfer obstruction
2026-10-29. Accepted at stated pointwise mathematical scope.

The symmetric-sector phase U=I−2P_sym belongs to the supplied true collective algebra. Twisting alternate sites by Z leaves the candidate singlet code in fixed computational weight n/2, so its compression of P_sym is rank one, determined by a single Dicke vector.

The explicit four-spin singlet amplitudes give squared sum16/3, correctly yielding w=(4/3)2^(n/2)/binom(n,n/2) for a single logical block with singlet spectators, and w=(16/3)^h/binom(4h,2h) for the actual full h-block code. n4 has w8/9. These formulas were independently derived before reading the product extension.

For dimension K, compressed channel amplitude is I−2A; leakage effect is4(A−A²). The completed entanglement fidelity is (1−2w/K)^2+4Tr[tau(A−A²)]/K². Maximizing over reset state gives minimal error4w(K−1)/K², not the raw physical Bell loss. The sign and normalization of the replacement-channel term are correct.

The general exact-left-inverse extension is valid and resolves the distinction between global reset and actual product local decoders. If D_a E=c_a I, trace preservation implies sum c_a* D_a Pperp=0, eliminating the TOTAL code/leakage cross term. Rank-one leakage permits only one replacement state tau. Thus the same lower bound holds for every CPTP decoder exact on the original noiseless code. It does not restrict a source-informed recovery that changes that noiseless decoding action.

The commutator identity gives delta_i=2||[P_sym,S_i]||F²/D≤4(n+1)/D. Therefore the full-product-code error/loss ratio is at least(1−1/K)(8/3)^h/(n²−1), exponentially large. This disproves a polynomial POINTWISE transfer factor from the specified unweighted global star-loss bank to that direct small code, including its ordinary product decoder. It does not prove a statistical sample-complexity separation, a practical noise advantage, or an impossibility for other acquisition objectives/strategies/recoveries. Both absolute error scales decay exponentially, as the author explicitly states. The high-rate singlet full-path comparator remains available.

Executed evidence: replayed author's finite matrices for n4,6,8,10 and product h1,2,3. Independent `check_product_decoder_obstruction.py/.json` applies the ACTUAL tensor local canonical reset decoder: h1 error0.913580≥universal lower0.888889; h2 error0.329211≥lower0.304762. This distinguishes the physical completed channel from the raw-loss shortcut rejected during review.
