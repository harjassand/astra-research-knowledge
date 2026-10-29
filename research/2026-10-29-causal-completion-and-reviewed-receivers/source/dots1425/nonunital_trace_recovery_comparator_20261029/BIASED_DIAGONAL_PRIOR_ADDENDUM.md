# Actual-prior extension without stationarity or barycenter penalty
2026-10-29. Additive candidate; independent review pending.

For Φγ=Ad_X∘ADγ, 1/2≤γ<1, retain computational dephasing Δ. Let a finite ensemble have ANY diagonal barycenter σ_p=diag(p,1−p), 0<p<1. Set η=1−γ and ν=Φγσ_p=diag(r,1−r), r=η(1−p). Use the actual universal recovery based on σ_p and Φγ, not the channel's fixed state.

The unrotated Petz map is R0(Y)=σ_p^(1/2)Φγ†(ν^(−1/2)Yν^(−1/2))σ_p^(1/2). Direct calculation on the off-diagonal matrix unit gives
(R0Φγ)(|0><1|)=a_p |0><1|,
a_p=η√[p(1−p)/(r(1−r))]=√[η p/(γ+η p)]≤√η.
Diagonal inputs stay diagonal. For the symmetric rotated convention,
R_t(Y)=σ_p^(it/2)R0(ν^(−it/2)Yν^(it/2))σ_p^(−it/2),
the multiplier becomes a_p exp(it θ), θ=(log[p/(1−p)]+log[r/(1−r)])/2. The even β0-average therefore has real multiplier z with |z|≤a_p.

Universal recovery now supplies, for EACH ensemble state,
T(ρ_x,RbarΦγρ_x)≤√ℓ_x,
ℓ_x=D(ρ_x||σ_p)−D(Φγρ_x||ν).
The same off-diagonal projection argument as the governing theorem yields
T(ρ_x,Δρ_x)≤√ℓ_x/(1−a_p).
Because σ_p is the ACTUAL barycenter, Σp_xℓ_x=δ exactly. Jensen gives
**e_avg(Δ)≤√δ/(1−a_p)≤(2+√2)√δ.**
No stationarity and no additive κ are required. The identical complete argument holds if the ensemble barycenter on AR is σ_p⊗ω_R, since recovery factors on R. This is not a statement for an arbitrary correlated barycenter or an arbitrary coherent qubit barycenter. At p=0 or1 every ensemble state equals that pure diagonal barycenter, so disturbance is zero; the formula need not be extended by singular Petz inverses.

This is an explicit measure/reprepare comparator for a nonunital self-compatible family with no EB CP-mixture component. It uses established universal recovery as a mathematical witness; no implementability of Rbar is needed to perform Δ. No historical novelty claim or unrestricted N371 closure is made.
