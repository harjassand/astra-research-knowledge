# Independent constant tightening

2026-10-29. Reviewer derivation; optional strengthening of the accepted author bound. It uses the same estimator, good event, and single-use exact covariant twirl.

For diagonal entry i, the one-record variance is `sigma_ii-sigma_ii^2`. For off-diagonal entry ij, the halved measurement outcome has variance `(sigma_ii+sigma_jj)/4-sigma_ij^2`. The squared Frobenius error counts off-diagonal entries twice. Hence, using Tr(sigma)=1 in dimension9,

`m E||sigmahat-sigma||F^2 = sum_i(sigma_ii-sigma_ii^2) + 2 sum_(i<j)[(sigma_ii+sigma_jj)/4-sigma_ij^2] = 5-Tr(sigma^2) <= 44/9`.

For this physical family, `Tr(sigma^2)=(8+eta^2)/(8+eta)^2`; the identity is orientation independent. Twenty-four rational fixtures verify the exact variance from the actual three-outcome measurement probabilities.

The author's good event gives `||Rhat-R||F^2 <= (128/3) E^2/g^2`, with `E=||sigmahat-sigma||op`. On the bad event `E>g/4`, the universal squared rotation error bound8 is itself at most `128 E^2/g^2`. Thus the single pointwise inequality

`||Rhat-R||F^2 <= 128 E^2/g^2`

holds on both events. There is no need to add the two event constants. Taking expectations and using the exact covariant-twirl identity `halfdiamond=MSE/8` yields

`halfdiamond <= 16[5-Tr(sigma^2)]/(m g^2) <= 704/(9m g_L^2) = 3520/(N g_L^2),  N=45m`.

The author's constant432 is therefore valid but can be replaced by704/9 in the same finite-interface additive budget. These remain loose sufficient constants; no optimization or minimax claim is made. All conditioning, independence, payload and averaging limitations of the governing review continue to apply.
