# Independent receiving: retired-record polar inverse

28 October 2026. **PASS for the exact corrected source bound in the companion receipt.** This is a one-use record-averaged canonical inverse guarantee, not a record-wise decoder guarantee, a reversal of irreversible noise, or a new full recovery oracle. The independently restarted training and independence of the later service from the retired fit are load-bearing.

## Main derivation

The actual signed-Pauli probe matrix Z=9Yvu^T is unbiased for B even with affine translation c, because averaging the independent signed input removes c. Its squared Frobenius norm is exactly 81 on every outcome. Consequently the displayed finite-horizon second moment (81-||B||F²)/N is exact for independent probes.

For B=RS and Q(M) the nearest proper rotation, the good event ||M-B||F<=a/2 implies positive determinant and smallest singular value at least a/2. Thus the proper factor is the ordinary unique polar factor. Adding its two optimality gaps proves ||Q-R||F<=2||M-B||F/(sigma_min(M)+a), which is stronger than the source's looser 2||M-B||F/a.

Writing F=R^T(M-B), O=R^TQ and K=O-I, stationarity of the polar fit gives symmetry of O^T(S+F). Orthogonality gives K^T=-K-K^TK. Substitution yields exactly

    S(K-Omega)+(K-Omega)S=-F^TK+K^TF-K^TKS.

The inverse Sylvester norm is at most 1/(2a), and ||S||<=1. The resulting bound is 2||E||F²/a²+2||E||F²/a³, no larger than 4||E||F²/a³. Thus the claimed quadratic remainder is valid without isotropy or a covariance-symmetry assumption.

The Sylvester solution Omega is linear in E and mean zero at a fixed independently chosen horizon. On the bad event, proper Q remains unitary, ||K||F<=2sqrt(3), and ||Omega||F<=||E||F/a. Markov and the event's lower norm threshold give the stated bad-event probability and first-moment bounds. Adding good and bad contributions yields the coefficient 4+8sqrt(3)+2<20 for a<=1, hence 1620/(a³N). This includes every bad fit rather than conditioning away failures.

The averaged residual is a physical unital channel. Its DIFFERENCE from identity satisfies L(I)=0; the corrected source now uses that precise terminology. Pauli orthogonality gives normalized Choi Frobenius norm ||T||F/2 and trace norm at most ||T||F. The input-dimension-two Choi bound therefore gives the displayed half-diamond estimate. Tensoring arbitrary references or composing with an independent joint service map does not increase it. No classical error-branch decomposition is required.

## Independence, retirement and conditioning pilot

The trusted decoder may privately use its fitted program to apply Q-dagger, but neither fit/program nor any correlated accessible copy belongs to the returned service interface. The service input, initial memory and causal source cannot depend on the final random fit. If a record is returned, or unreset training memory carries it into service, averaging cannot be moved outside the adversarially correlated process and the proof does not apply. Conditioning on a fixed unknown channel is harmless; conditioning on the final estimator is not.

The separate pilot's coordinate Hoeffding radius is correct for samples in [-9,9]: nine coordinates and Frobenius-to-coordinate conversion give r0=27 sqrt(2 log(18/beta)/N0). A rigorously separated positive determinant/singular-value interval supplies a valid lower bound on the good pilot event. A fresh independent final bank has a fixed chosen N conditional on that pilot record, so its unbiasedness is intact. The invalid-pilot mass is separately charged. Exact-boundary or insufficient-budget cases abstain. Conditional-on-acceptance bounds require division by the acceptance probability. Reusing an adaptively stopped final fit is explicitly not licensed.

## Finite physical operations

A nearest proper rotation for rational M is a finite fixed-dimensional real-algebraic construction with deterministic tie choices, including singular and reflected estimates. Its unitary representative is physical on every record. Finite control synthesis is separately paid and is not asserted executed by this review.

The corrected source adds bounded ternary rejection for both signed-Pauli axis choices: at most N_total(4L+2) bits, plus the declared cap-failure/record discrepancy debit. Thus an ideal uniform-six description does not silently require an unbounded per-execution random sampler. The original source is preserved separately. Private interface, sampler debit and the L(I)=0 terminology were clarified before receipt; no load-bearing mathematical correction to the polar remainder was required.

## Independent checks

`ordinary_retired_record_polar_independent_check_20261028.py/.json` enumerates all 72 exact Born events for a genuine nonunital, anisotropic amplitude-damping channel followed by a proper rotation. It verifies exact estimator mean, normalization and single-record variance 49569/625. The first-order skew solution is solved exactly over rational matrices. Eight numerical good-event polar fits in an unequal-weight, mean-zero, nonisotropic perturbation family satisfy the exact-identity residual and quadratic remainder; averaged bias divided by perturbation scale squared stabilizes near 0.1686. Numerical SVD tests include zero, singular and reflected estimates and always return a proper orthogonal fallback.

A separate exact two-record fixture has opposite rational unitaries. Its retired-record average has half-diamond error u², while exposing the record gives error |u|. This confirms the operational distinction on which the theorem depends. These are source-disabled exact/numerical checks, with zero source outcomes and zero RNG draws. The author's saved count simulation is distinct evidence; this review does not claim to have independently replayed those samples.

## Accepted scope and open work

Receive the finite ordinary-probe O(1/N) averaged complete inverse bound for independently restarted stationary det-positive nonsingular qubit channels; the separate conditioning pilot; all-record proper unitary output; and independent one-use complete service transfer with retired private records. Do not import a noncommuting repeated-reuse theorem, calibration-correlated-memory guarantee, practical advantage, historical novelty, or reversal of dissipative noise. The constant and conditioning power are conservative upper bounds, not optimality claims.
