# Attained universal radial endpoint: final worker result

The previously open endpoint is attained. The result is stronger: for \(m\ge2\), \(R>0\), put
\[
 b_* = \log\frac{2}{R(m-1)}-1.
\]
There is one smooth, everywhere positive, radial, strictly log-concave scalar probability density \(p\), with every exponential moment, that positively regularizes every bounded self-adjoint tuple satisfying \(\|A(u)\|\le R|u|\), in every Hilbert dimension, and has
\[
 p(x)\sim C\exp\left[-\frac r{2R}
   (\log r+\log\log r+b_*)\right],\qquad r=|x|\to\infty.
\]
The coefficient \(1/(2R)\), the coefficient one of \(\log\log r\), and the fixed offset \(b_*\) are all optimal for the specified radial upper-envelope class. Any larger fixed offset is impossible by a finite-dimensional Clifford moment obstruction; the Pauli pair suffices when \(m=2\).

An explicit construction is
\[
 q_L(r)=\sqrt{L^2+r^2},\quad h(q)=q(\log q+\log\log q+b_*),
\]
\[
 p_L(x)=Z_L^{-1}\exp\{-[h(q_L(|x|))-h(L)]/(2R)\},
\]
with a fully specified, conservative sufficient \(L\) in Addendum 2, equation (3.3). The proof establishes pointwise positivity on all space and norm-integrable normalization, not just a necessary moment condition or finite-grid evidence.

The main analytic mechanism is an exact Taylor expansion of the local exponential-tilt remainder. Duhamel integration supplies two inverse powers of the tilt for every derivative of degree at least two. At the sharp constant, the quadratic term is kept explicitly; the radial insertion commutes with the tilted operator, and the transverse insertions determine the factor \(m-1\). The relative lower margin is positive at each finite point and tends to zero in the remote tail.

Read the saved proof chain in order:

1. `ENDPOINT_PROOF_v1.md`: endpoint and iterated-log theorem, uniform operator analytic estimate, compact-support evaluation, normalization, and Pauli tail bound.
2. `ADDENDUM_1_MOMENT_JUSTIFICATION.md`: general-noise/weak-POVM tilted moments justified directly from positive one-dimensional spectral convolutions.
3. `ADDENDUM_2_SHARP_CONSTANT_OFFSET.md`: matching Clifford necessity and attained sharp constant, with explicit conservative constants and the exact multiplicative tail asymptotic.

The first two files received an independent internal audit from `operator_adversary_v3`, which reported no material gap. The third received an independent internal audit from `anisotropic_domain_astra`, which reported PASS with no mathematical correction required; its detailed review is saved in that worker's `ENDPOINT_OFFSET_REVIEW.md`. These are internal independent proof reviews, not formal verification or external certification. `FINAL_RECEIPT.json` preserves the frozen hashes and review reports.

`SOURCE_COMPARISON.md` identifies inherited Weyl/Wigner and scalar-convolution machinery. Historical priority remains uncleared. Smaller tail corrections/prefactors and practical regularization scales remain open. No efficient measurement or information advantage is claimed.
