# Faithful fixed states do not imply pinching CP coverage
2026-10-29. Exact technique obstruction, not a counterexample to N371.

Let |u±>=(√3/2, ±1/2) and define the entanglement-breaking qubit channel
Ψ(ρ)=ρ00 |u+><u+|+ρ11 |u−><u−|.
It has an explicit full-domain symmetric extension: measure Z and prepare |u±><u±| on each of two outputs. Its affine Bloch action is (x,y,z)↦(√3 z/2,0,1/2).

Its unique fixed state is σ=[I+(√3/4)X+(1/2)Z]/2, with determinant9/64>0. Let Δσ be spectral dephasing of σ. Its axis is n=(√3,0,2)/√7.

Use normalized Choi convention J(Ψ)=(id⊗Ψ)(|Φ+><Φ+|). The vector w=|0>⊗(−1/2,√3/2) has <w|J(Ψ)|w>=0. However Δσ(|0><0|) has computational populations11/14 and3/14. Since |<u+ perpendicular|u−>|²=3/4,
<w|J(ΨΔσ)|w>=(1/2)(3/14)(3/4)=9/112.
Thus J(Ψ−αΨΔσ) has a negative quadratic form for every α>0. No positive CP coverage coefficient exists, despite faithfulness, stationarity, and self-compatibility. The exact symbolic program also verifies ranks2 and4, respectively.

Consequences: the thermal packet's positive coefficient uses actual channel structure; it cannot be generalized merely from a faithful stationary state and broadcast compatibility. This does not refute an entropy comparison, prior-dependent EB recovery, or N371: Ψ is already EB. It does show why replacing a general recovered σ-preserving channel by its spectral-pinching CP decomposition is not automatically legal. No novelty assertion is made.
