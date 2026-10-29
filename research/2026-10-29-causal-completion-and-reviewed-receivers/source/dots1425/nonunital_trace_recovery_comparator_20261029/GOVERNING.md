# Direct trace comparator survives zero EB weight and failed entropy comparison
2026-10-29. Candidate theorem; receiving review pending.

## Setting and result
Let Φγ=Ad_X∘ADγ, 1/2≤γ<1, η=1−γ, and σ=diag(η/(1+η),1/(1+η)). The channel is self-compatible, σ-preserving, and has no positive-weight CPTP EB component (the rank-two Choi-support proof in the obstruction packet applies for every0<η≤1/2). Let Δ be computational dephasing, an explicit EB channel.

For every state ρ_AR and arbitrary finite reference R,
T(ρ_AR,(Δ⊗id)ρ_AR) ≤ (1/γ)√L(ρ_AR),
L(ρ)=D(ρ||σ⊗ρ_R)−D((Φγ⊗id)ρ||σ⊗ρ_R).
Thus coefficient2 works uniformly over this self-compatible family, independently of the reference dimension and the smallest eigenvalue of σ. This is a direct trace/fidelity theorem, NOT an entropy-comparator inequality.

For a finite ensemble with stationary barycenter σ (or σ⊗ω_R in the complete version), Jensen gives e_avg(Δ)≤γ^−1√δ≤2√δ, where δ is the actual-prior Holevo loss under Φγ. For a nonstationary barycenter the same derivation instead includes κ=D(barρ||τ)−D(Φγbarρ||τ); κ is not deleted. Reference pinching remains on A only.

## Proof using actual universal recovery
Use Junge–Renner–Sutter–Wilde–Winter, arXiv:1509.07127v3 Theorem2.1/Remark2.2, with reference σ and channel Φγ. The universal recovery is the β0-average of rotated Petz maps, β0(t)=π/[2(cosh(πt)+1)]. Choose the equivalent symmetric convention
R_t(Y)=σ^(it/2) R_0(σ^(−it/2)Yσ^(it/2)) σ^(−it/2),
R_0(Y)=σ^(1/2) Φγ†(σ^(−1/2)Yσ^(−1/2)) σ^(1/2).
(The opposite sign convention produces the same average because β0 is even.)
Its fidelity bound is L(ρ)≥−2log F(ρ,(Rbar∘Φγ⊗id)ρ). Tensoring a reference state ω_R into σ makes its modular factors cancel on the identity reference channel, so the recovery is Rbar⊗id. Restrict to the support of ρ_R if needed. Fuchs–van de Graaf yields T(ρ,Ψρ)≤√(1−exp(−L))≤√L, Ψ=Rbar∘Φγ⊗id.

The Kraus matrices K0=[[0,√η],[1,0]], K1=√γ|1><1| obey σ^(1/2)Kj†σ^(−1/2)=Kj. Hence R0=Φγ exactly. Φγ sends |0><1| to √η|1><0|, reversing modular phases. Direct substitution therefore gives
(R_t∘Φγ)(|0><1|)=η exp(it logη)|0><1|,
and the adjoint matrix unit receives the conjugate factor. Diagonal inputs remain diagonal. Averaging yields a real multiplier z=ηκ, κ=∫β0(t)cos(t logη)dt, |κ|≤1.

Let O=(id−Ad_Z)/2 on A, tensored with id_R. Triangle inequality and unitary invariance imply ||O(X)||1≤||X||1. Also O(ρ)=ρ−Δρ and O(ρ−Ψρ)=(1−z)Oρ. Since |1−z|≥1−η=γ,
T(ρ,Δρ)≤γ^−1 T(ρ,Ψρ)≤γ^−1√L.
No inverse of an unknown channel, environment tomography, or physical implementation of the recovery map is asserted. Recovery is an analytical witness; the actual comparator Δ is the ordinary two-outcome projective measure/reprepare channel.

## Boundaries and evidence
The previous exact reference-activation family makes D(ρ||Δρ)/L diverge, so this direct trace mechanism genuinely bypasses that failed intermediate inequality. It does not solve unrestricted N371, arbitrary nonstationary priors, arbitrary nonunital self-compatible channels, or tensorization over many noisy qubits. No historical novelty claim is made; universal recovery and trace-norm projection are established ingredients. The construction to check is their explicit combination for this zero-EB-weight family.

Dependency: https://arxiv.org/pdf/1509.07127 (v3), theorem read in full earlier in this research window. The obstruction packet is producer-workspace/nonstationary_coverage_obstruction_20261029; its original and stronger Choi proofs do not establish the recovery theorem above.
