# Independent qualification: signed shuffle on the full binary register

31 October 2026. I read the complete `SHUFFLE_FULL_REGISTER_BINDING.md` and matched its SHA-256 `6c87691c20314bebbeaeddc7f2675a9813636e398d7e64bdc83a1b6e08e6b98f` (3,513 bytes). The qualification is sound and is binding when instantiating the full-register pure-return theorem with the signed-shuffle example.

An arbitrary invalid-codeword unitary/channel extension does not inherit the valid-subspace return bound. The proposed extension instead pinches the valid/invalid cross blocks by an orthogonal private flag. On invalid inputs it transfers the entire old register to an environment and prepares the known uniform valid state. This is an acquired isometry with a unitary extension and inverse, not irreversible erasure; validity checking, register transfer and state preparation have polynomial circuit descriptions and are paid.

Because the prepared valid state is fixed, every invalid contribution has zero Q survival after the first channel application. Thus the displayed m-step adjoint identity and full-Q bound follow. The good-input coefficient state has only the valid flag, so its overlap contraction annihilates the invalid subspace. The sign reset then gives the same full-register bound for the tensor source. The conservative horizon n ceil(log_2(16n)) is sufficient since log_2(16n)>=ln(16n).

Zero extension of the diagonal coupling on invalid labels preserves its norm, exact sign centering and intended process on valid stationary inputs. This does not interpret arbitrary quantum source interventions as classical controls.

PASS as a concrete encoding qualification. It repairs no abstract theorem: the independently reviewed abstract whole receiver already requires the full operator return certificate. The earlier valid-subspace shuffle proofs remain valid, but they must not be paired with an unspecified invalid-state extension when claiming that abstract full-register interface.
