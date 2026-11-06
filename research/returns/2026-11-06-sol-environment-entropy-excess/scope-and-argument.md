# Exact conditional scope and the missing effective scale

The [full authored note](original/ENVIRONMENT_ENTROPY_EXCESS_OBSTRUCTION.md) fixes any stationary process of consistent ordinary finite input states`ρ_n`. Receiver`B^n` and **true complementary environment**`E^n` have entropy rates`h_B,h_E`. The process need not have a known finite memory dimension, be Markov or mix, or supply a physical stationary resource at Bob. The input prefixes are ordinary physical states, without assisted capacity resources.

Stationarity/subadditivity give nonnegative block excesses and the exact signed identity

`I_c=n(h_B−h_E)+e_B(n)−e_E(n)`.

An upper bound on`e_E` alone therefore suffices; replacing both excesses by absolute memory bounds discards the favourable receiver contribution.

The structural lemma assumes a **computable family** of finite rational channels`N_z` with an undecidable promise `Q(N_z)=0` on no instances and `Q(N_z)>0` on yes instances. It does not create, reprove or strengthen such a family. Suppose a proposed construction supplies a computable`g_z>0` and, on every yes instance, an existential stationary ordinary input with `h_B−h_E≥g_z`. Suppose it also supplies a computable integer`n_z` satisfying `e_E(n_z)≤n_zg_z/2` on yes instances. Then

`Q^(1)(N_z^⊗n_z)/n_z ≥ g_z/2` on yes, and equals0 on no.

The note uses computability of maximising coherent information over the finite block's compact physical-state space, with certified entropy-continuity nets. Approximation to`g_z/8` separates the promises. It is not necessary to construct/acquire the witness process: the state is used existentially inside a maximisation over all finite-block physical inputs. The entire block description, dimensions and precision cost are paid; **computable is not polynomial or practical**.

The forbidden combination is an effective positive entropy-rate gap **plus** an effective true-environment boundary scale on the assumed hard family. Examples that would supply the latter include a computable uniform bound`e_E(n)≤K_z` (take`n_z≥2K_z/g_z`), a sublinear envelope with an actual computable way to reach the required ratio, or an effective environment conditional-entropy convergence estimate whose cumulative error provides such an envelope. Computable exponential prefactors/rates would be more than sufficient. A merely asymptotic bound without an effective scale is not silently upgraded to an algorithm.

A bound such as`2log D` with unknown noneffective witness dimension`D` does not compute the needed block. A positive-rate construction could retain that genuinely noneffective scale. Conversely, a strong history-convergence estimate could hold while its proposed positive bulk rate fails. Neither isolated property substitutes for the required signed entropy-rate inequality.

A dimension-independent Hilbert–Schmidt spectral gap for retained memory or decaying bounded-observable two-point correlations is **not** the same as convergence of environment conditional entropies against arbitrarily long quantum history. True environment history includes transmitted mixer purifiers and erasure flags. The read N1680 Bell-chain example already defeats automatic telescoping; the new authored deduction identifies the one output whose effective excess would furnish a finite certificate and applies across stationary-source representations. This is not a theorem that all mixers, catalysts or stationary encoders fail.

The lead compares Beigi–Tomamichel arXiv2609.11771v1, Theorems1–2/section5, at the scope stated in the original: a projective-norm-controlled channel-image projector for low-to-high-fidelity conversion and an above-capacity fidelity result. Those statements do not supply this environment scale, a below-capacity activation cutoff or a terminating capacity upper evaluator. Capital has not performed a new primary-source verification or criticism of that theorem.

The [unchanged common question](original/COMMON_QUESTION.md) asks for a total algorithm approximating ordinary unassisted capacity to`1/4` bit for every valid explicit finite rational-complex normalised Choi matrix, or a proof that no such algorithm exists. Dimensions vary; there is **no time-complexity promise**. A fixed-quarter evaluator would allow arbitrary precision by finite tensor amplification, which remains distinct from efficient computation. The method constraint settles neither alternative. Zero-versus-positive behaviour with a noneffective tiny gap, restricted assisted results, QMA-hardness, finite-block nonadditivity and a failed proposed evaluator are not substituted for the full answer.

The note/common context preserve accepted N675 and available N1677/N1680 originals at their actual conditions; unavailable packages and failed original-PDF routes remain unavailable. The source's role-directory-only write and no-onward-spawning rules apply to the pilot researchers. Capital's separately authorised publication copies the completed note through the existing route, without editing their originals, contacting constructors, reconstructing held sources or building retrieval. The pilot and the other constructors' work remain ongoing.
