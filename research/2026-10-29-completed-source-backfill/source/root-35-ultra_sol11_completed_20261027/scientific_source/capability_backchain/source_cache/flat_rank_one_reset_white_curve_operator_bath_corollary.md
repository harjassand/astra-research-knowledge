# Noncommuting operator-bath lift of the whole flat-main / rank-one two-level reset family

Status: direct corollary of the whole scalar white-curve theorem and the independently received positive spectral-mixture lifting identity; awaiting receipt of this assembly.

## Actual source
Fix finite r, a unit ψ in C³⊗Cʳ, and a₀≥0, a₀+b≥0. On physical C³ and base reference R₀=C³⊗Cʳ define

Y₀=a₀I_(3r)+b|ψ><ψ|,
T=P_Ω3⊗I_r+I₃⊗Y₀.

Let U,V≥0 be arbitrary finite matrices on an additional reference bath, with NO commutation or order assumption. Then

Z=T⊗U+I_(9r)⊗V
 =P_Ω3⊗I_r⊗U + I₃⊗[Y₀⊗U+I_(3r)⊗V]

satisfies Δ(Z)≥0.

The new main logical spectrum is I_r⊗U and need not be flat. The reset is the displayed structured common-bath sum; it is not an arbitrary PSD matrix with that main. Singular U,V are allowed. This construction retains the original source; it is not a filter iteration or measurement of a hidden label.

## Exact receiving
For every scalar t≥0,

T+tI=P_Ω3⊗I_r+I₃⊗[(a₀+t)I+b|ψ><ψ|]

lies in the whole family of `flat_mixed_success_arbitrary_rank_one_two_level_reset_theorem.md`. Hence h(t)=Δ(T+tI)≥0 on the ENTIRE half-line, not just at t=0.

The received identity in `white_noise_stability_operator_bath_lifting_theorem.md`, with q(t)=Tr(tU−V)_+, gives

Δ(Z)=q'(0+)h(0)+∫_(0,∞)h(t)dq'(t).

The measure is positive and its total mass, including the atom at zero, is TrU. This proves the corollary for arbitrary noncommuting U,V. It does not assert the original state is physically a flagged mixture of the scalar seeds.

## Strictness and zero cases
If Y₀≠0 and U≠0, then h(t)>0 at every finite t≥0 by the scalar theorem. A positive measure of nonzero total mass therefore gives Δ(Z)>0. If U=0, Z is reset-only and Δ(Z)=0.

If Y₀=0, h(0)=0 and h(t)>0 for t>0. In this case equality holds exactly when UV=0 (including either zero matrix). Indeed the measure is supported only at zero exactly when q'(0+)=TrU. The finite-dimensional one-sided derivative is q'(0+)=Tr(P_kerV U), so equality forces U to be supported in kerV; positivity makes this equivalent to UV=0. Conversely orthogonal supports give q(t)=tTrU and hence only the zero atom. No branch of an instrument is being ignored in this equality argument.

## Normalization and scope
The physical marginal of Z is
[(r+TrY₀)TrU+3rTrV]I₃.
When nonzero, division by that scalar gives the unnormalized TP Choi operator (trace3); division by three times that scalar gives its normalized Choi state. Homogeneous VALUE is unchanged in sign.

This operator-bath family genuinely permits nonflat logical main eigenvalues and bath noncommutation. It does not include arbitrary C and Y on a covered space, arbitrary reset-projector rank, or arbitrary mixed-main directions. It uses the received all-white-noise curve, not mere positivity of one base source. The earlier endpoint and finite-instrument failures remain valid.
