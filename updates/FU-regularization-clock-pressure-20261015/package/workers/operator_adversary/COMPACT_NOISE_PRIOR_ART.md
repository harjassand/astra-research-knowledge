# Compact-noise theorem: limited primary-source check

Status: exact historical priority UNKNOWN. This is a targeted source comparison, not an exhaustive search or a novelty certificate.

The primary paper [Schwonnek and Werner, The Wigner distribution of n arbitrary observables](https://arxiv.org/html/1802.08342), arXiv:1802.08342v2 dated 8 July 2020, was opened in HTML. Its Section III.1, Proposition 1, establishes compact support inside the joint numerical range using an operator exponential bound and Paley-Wiener-Schwartz. Section III.2, Proposition 2, states a noiseless finite-dimensional positivity/commutativity equivalence for a full-rank state. These are direct antecedents. Neither inspected proposition states the existence-versus-commutation criterion for compact scalar convolution noise on an arbitrary Hilbert space.

The proof saved as `COMPACT_NOISE_PROOF_PL.md` needs the stronger exact multiplier contract for every real direction and every state. It does not follow merely from compatibility or incompatibility of the noisy coordinate marginals. A bounded joint POVM can measure unsharp versions of noncommuting observables under weaker contracts; that observation is consistent with the theorem.

Targeted web searches included the phrases “Weyl functional calculus positive convolution”, “joint measurement compact support observables”, “Wigner bounded noise observables”, “compactly supported noise noncommuting”, and “joint measurement all linear combinations noise compact”. No directly matching primary theorem was located in those returned results. This absence is not evidence of novelty.

Search results also surfaced work on approximate position/momentum joint measurements and signed particle approximations of generalized Wigner distributions. Their displayed scopes differ from this bounded-observable exact scalar multiplier contract. They were not used as proof premises, and uninspected full text is not excluded as prior art.

The saved proof uses classical characteristic-function uniqueness, positive spectral marginals, Duhamel differentiation, a quadrant Phragmen-Lindelof argument proved explicitly by maximum modulus, Liouville's theorem, and the commuting joint spectral theorem. The mathematical mechanism may have older functional-calculus, ordered-kernel, or exponential-family antecedents that these limited searches did not resolve.
