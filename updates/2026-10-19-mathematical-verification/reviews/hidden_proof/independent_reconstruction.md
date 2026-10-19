# Reconstruction recorded before reading the source proofs

Before this reconstruction, full reads of `hidden_state/proof.tex` were restricted to lines 1–56, 90–97, 110–137, and 193–224. An initial heading/keyword search also exposed isolated source line 149 (the advertised linear entropy bound) and line 162 (the epsilon definition), plus proof labels/conclusion snippets. Thus this was not fully blinded to those two scalar expressions, which were also specified in the assigned task. No proof paragraphs, geometric-density argument, Schur-complement derivation, or pre-existing independent audit had been read. This file records the independently reconstructed mathematical route before the full proof comparison.

## H1

Complete the isometry V to an orthogonal basis, and write the positive matrix T as [[S,B],[B*,D]]. Then U=S²+BB*, so Δ=BB*≥0. For λ>0 the upper-left block of (T+λI)^−1 is at least (S+λI)^−1. The other Schur-complement formula gives their difference as

Rλ=(S+λI)^−1 B [D+λI−B*(S+λI)^−1B]^−1 B*(S+λI)^−1.

Because T≥0 and S>0, D−B*S^−1B≥0. Hence the square bracket is ≥λI, and

0≤Rλ≤λ^−1(S+λI)^−1 Δ (S+λI)^−1,

so ||Rλ||≤||Δ||/[λ(a₀+λ)²]. The fractional-power integral gives

S^α−V*T^αV=(sin πα/π)∫₀∞ λ^α Rλ dλ≥0.

Its norm is at most ||Δ||(sin πα/π)∫₀∞ λ^(α−1)/(a₀+λ)² dλ=(1−α)a₀^(α−2)||Δ||. Here the integral is a₀^(α−2)Γ(α)Γ(2−α), and Γ(α)Γ(1−α)=π/sin πα. No hidden-dimension or hidden-rate parameter appears.

For a reversible CTMC, T^α=e^(ατH) is entrywise nonnegative, as is V. Therefore the compressed T^α has nonnegative entries, and a negative off-diagonal entry of S^α has magnitude bounded by the same gap norm. This proves H1 independently.

## H2 path comparison

Use row-generator convention, q*_(ij)=μ_j q_(ji)/μ_i for i≠j, and Qbar=(Q+Q*)/2. Stationarity gives sum_(j≠i)q*_(ij)=sum_(j≠i)q_(ij), so Q, Q*, and Qbar have identical escape rates. They all preserve μ, and Qbar is reversible.

For stationary finite-CTMC path densities f,g,h over [0,t] under Q,Q*,Qbar, respectively, identical escape factors and the arithmetic-geometric-mean inequality for each jump give h≥sqrt(fg). Also (f+g)/2≥sqrt(fg). Thus, with TV equal to half the L1 distance,

TV((f+g)/2,h)≤1−∫sqrt(fg)≤1−exp(−D(f||g)/2)≤tσ(Q)/2.

The middle step is Jensen applied to E_f exp[−(1/2)log(f/g)]. The stationary all-even path reversal identity gives D(f||g)=tσ(Q), with σ summed over unordered pairs as in the statement. If σ=∞ the desired positive finite lower bound is automatic; finite σ ensures mutual jump support.

At each of t=τ,2τ the specified observed endpoint law is symmetric because P and P² are reversible. The observation pushforwards of f and g are then equal, so the same bound applies between the Q endpoint law and the Qbar endpoint law. For the joint-law difference J−Jbar, normalized kernel difference has norm at most ||J−Jbar||_(entrywise 1)/p_min=2TV/p_min. Consequently, putting ε=τσ/p_min,

||S−Sbar||≤ε, and ||S²−Ubar||≤2ε.

All four endpoint-normalized matrices needed here are contractions in operator norm. In particular

||Ubar−Sbar²||≤2ε+||S²−Sbar²||≤4ε.

If ε<a₀/2 then λ_min(Sbar)≥a₀/2. For positive A,B≥bI, the same fractional-power integral and resolvent identity imply the operator-Lipschitz estimate

||A^α−B^α||≤αb^(α−1)||A−B||.

Indeed its scalar integral is (sin πα/π)∫₀∞ λ^α/(b+λ)²dλ=αb^(α−1). Applying H1 to Qbar yields

m_α(S)≤||S^α−Sbar^α||+m_α(Sbar)
≤[α(a₀/2)^(α−1)+4(1−α)(a₀/2)^(α−2)]ε=C_α ε.

If instead ε≥a₀/2, that branch already supplies ε≥a₀/2. Combining branches gives H2 exactly as stated. This route relies on finite stationary homogeneous CTMCs, deterministic memoryless observation, and ordinary all-even reversal; it does not prove an infinite-state extension or an experimental inference claim.
