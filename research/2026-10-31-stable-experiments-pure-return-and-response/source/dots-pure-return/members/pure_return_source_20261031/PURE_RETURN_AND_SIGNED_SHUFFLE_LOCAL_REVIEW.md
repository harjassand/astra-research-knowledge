# Independent local review: pure return and acquired signed shuffle

31 October 2026. Scoped mathematical PASS for the local interfaces below. This is not acceptance of a whole first-event compiler.

## Source binding and read scope

I read both complete files in the original workspace and matched their SHA-256 values:

* `PURE_RETURN_COMPILER_OPENING.md`: `f8f9171554f327c9b324e8a6fd2c4fe93ba5009ff8c5e5248bedd07e0f747f36`.
* `SIGNED_SHUFFLE_ACQUIRED_MODEL.md`: `3169ae86dfff2e0985a9961868f9bc7b84342e4d46926533a1dbd3caaec63a94`.

The shuffle source receives the actual insertion-isometry, uniform-state preparation and normalized coalescence proof in `markov_source_realization_20261031/ACQUIRED_SHUFFLE_MULTISTEP_RETURN.md`, SHA `62bc85a2a0726ec85f304ee2bfc1108d0b5c5db29615f81a5a58bed54b20e9ef`. The separately reviewed scaled kernel is the final `GROUPED_POISSON_KERNEL_CONSTRUCTION.md`, SHA `150152b77d81cb47781d97d600f55d0b8d0d0a9c35a0891009cce58936792b4a`. Diagnostics are not substitutes for these mathematical interfaces.

## 1. Return certificate really gives the power certificate

The acquired Stinespring operation and known coefficient state supply the contraction A=(<c| tensor I)W, not just a proposed matrix. A fixes psi, and contraction implies A† fixes psi; hence P reduces A. In the m-step dilation the projection onto c in each fresh output environment has system block A^m. For an input in Q, the norm of its projected Q output is bounded by its total Q-output probability. This proves ||A^m Q||² <= ||(Phi†)^m Q|| <= 1/16. No source-state enumeration, spectral diagonalization or implication from an unrelated mixing norm is used.

## 2. Exact generator, signs, and jump access

With Kraus operators K_j and coefficients c_j, A=sum conjugate(c_j)K_j. Subtracting c_j I makes every L_j dark. Expanding their dissipators gives Phi-I plus 1/2[A†-A, .]. The Hamiltonian H_env=i(A-A†)/2 contributes the opposite commutator. Thus the proposed Lindbladian is exactly Phi-I, with C=2I-A-A† and no-jump generator A-I. The signs in the source are correct.

The stacked jump W-|c> tensor I has normalization at most 2 and is acquired by coherent addition of supplied operations. Individual Kraus enumeration is not required. A physical jump can return to either P or Q; nothing in this local pass permits resetting its output to psi.

Centering PKP=0 is a real restriction. It avoids hiding an uncharged sqrt(lambda) mean Hamiltonian; it is not obtained by assuming efficient computation of an unknown average. For diagonal classical-source observables and diagonal coupling, the system-valued diagonal observable algebra stays invariant. With the matching initial diagonal probabilities, all prescribed system-instrument experiments consequently agree with the specified classical source. Private source/jump records are not physical monitored records.

## 3. Finite potential and actual count bound

Pure invariance gives 0 <= (Phi†)^j Q <= Q. Therefore Q <= V <= mQ and (Phi†-I)V <= -15Q/16. The weaker -Q/2 used in the proof is valid and leaves its displayed slack.

For Z=I+32 kappa V, kappa<=1/(32m), the fast drift is at most -16 kappa lambda Q. Since C<=4Q, the extra tilted recycling is at most 8 kappa lambda Q. The QQ Hamiltonian commutator costs at most 64 kappa sqrt(lambda)b m; the stipulated sqrt(lambda)>=16bm absorbs this in 4 kappa lambda Q. The remaining PQ coefficient is at most 32 kappa sqrt(lambda)b m. Completing the square against the remaining 4 kappa lambda Q leaves at most 256 kappa b²m²P, and hence the stated upper bound by 256 kappa b²m²Z.

This proves the physical dark-jump MGF and its mean/cap consequences with the stated small positive tilt. System-only trace-preserving interventions, including records, leave the source-only weight unchanged. No normalized rare-postselection or algorithmic query-history bound follows. In particular this count MGF must not be substituted for coherent primitive-port bounds in a different compiler.

## 4. Factor two is correctly assigned in the Dyson majorant

The acquired normalized Q propagator is F, while the physical Q propagator is 2 exp(-a' lambda t)F. In a Dyson word the initial interval has its input-sector factor, and every insertion is followed by its destination interval factor. Thus P-to-Q and Q-to-Q insertions have weight 2c0, Q-to-P has weight c0, and an initial Q contributes 2. This gives exactly exp(Mt) diag(1,2), with M as displayed. Diagonal similarity gives S exp(Msym t)S; it is not an equality of physical sector dimensions.

The high-rate threshold yields r0>=8c0 and delta=r0-2c0>=3r0/4. The slow Perron root is at most 2c0²/delta, which is below the stated 4b²/a' bound. Endpoint factors are constant, while repeated Q-dwell factors have been absorbed into the actual positive generator rather than ignored. Every interaction still needs its exact -i phase. A conditional fast-residence insertion source and complete first-event normalization remain to be proved in the whole receiver.

## 5. Signed physical model and its acquired centering

The specified source is top-to-random on permutations, with a fair sign refreshed at each source event. It is a different physical model from arbitrary unsigned permutation noise. The quantum permutation channel's diagonal adjoint has this orientation; its overlap matrix is the random-to-top pullback. These two orientations must not be interchanged.

Resetting the sign to |+> and transferring the old sign to a private environment is an acquired isometry. Together with permutation insertion it has 2n Kraus labels and coefficient vector 1/sqrt(2n). The coupling Z_sign tensor the controlled B_pi family is exactly centered because <+|Z|+>=0, independent of the unknown or difficult operator average over permutations. Its controlled circuit must actually execute and pay for the supplied gate list, selection and inverse; no n! table is assumed.

For m>=1 the sign reset has already occurred. The normalized coalesced permutation branch is a reset to the uniform pure state, and the remaining CP part has scalar trace effect delta_m. Hence the tensor channel's Q survival is bounded by delta_m Q, with delta_m<=n exp(-m/n). This also holds for inputs initially orthogonal to |+> in the sign sector: the sign reset removes that distinction, rather than creating an extra nondecaying sector. The choice m=max(1,ceil(n log(16n))) supplies the required 1/16 certificate. Its overlap is Pi_plus tensor P_perm, as claimed.

## Verdict and boundary

The two local bodies are coherent and their load-bearing signs, operator certificates, source orientation, centering and factor-two accounting check. They supply an explicitly acquired succinct example and a dimension-independent local kernel/activity interface with polynomial dependence on the earned return horizon. They do not yet supply a complete first-event instrument, conditional source/cap theorem, finite-bit private-time error allocation, or whole controlled-process resource theorem. Those joins remain pending. No novelty, practical advantage, source-learning benefit or generic pi_min-free theorem is inferred.
