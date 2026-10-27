# Nonflat two-mode success: noncommuting operator-bath corollary

Let C≥0 be a2-by-2 logical matrix, ψ any unit vector in C³⊗C², a₀,b≥0, and Y₀=a₀I₆+bP_ψ. Put T=P_Ω3⊗C+I₃⊗Y₀. For arbitrary finite PSD bath matrices U,V, with no commutation or order assumption,

Z=T⊗U+I₁₈⊗V
 =P_Ω3⊗C⊗U+I₃⊗[Y₀⊗U+I₆⊗V]

has Δ(Z)≥0.

Proof: for every t≥0 the actual scalar white curve T+tI₁₈ belongs to the whole family in `nonflat_two_mode_white_rank_one_reset_whole_value_theorem.md`, independently received in `nonflat_two_mode_white_reset_independent_audit.md`. Thus h(t)=Δ(T+tI₁₈)≥0 on the ENTIRE half-line. Apply the independently received exact spectral-mixture identity of `white_noise_stability_operator_bath_lifting_theorem.md`:

Δ(Z)=q'(0+)h(0)+∫_(0,∞)h(t)dq'(t), q(t)=Tr(tU−V)_+.

The measure is positive, with total mass TrU. This proof neither pinches the bath nor treats the actual source as a physically flagged mixture. It includes singular C,U,V.

For C>0 the scalar theorem gives h(t)>0 whenever Y₀+tI₆≠0. Consequently: if Y₀≠0, Δ(Z)>0 exactly when U≠0; if Y₀=0, equality holds exactly when UV=0. In the latter case use q'(0+)=Tr(P_kerV U); all measure is at zero exactly when U is supported in kerV. For singular C this note asserts positivity only and does not extrapolate this equality classification.

The physical marginal is [(TrC+TrY₀)TrU+6TrV]I₃. Divide by this scalar for TP Choi trace3, or by three times it for the normalized Choi state.

Scope: the main spectrum is the nonflat tensor product C⊗U and the reset is the displayed common-bath sum. Negative rank-one holes with nonflat C, arbitrary logical spectra with arbitrary coherent resets, and unrelated Kraus directions are not inferred.
