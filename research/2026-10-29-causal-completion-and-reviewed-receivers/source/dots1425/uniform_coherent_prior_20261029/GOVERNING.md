# Uniform all-prior trace reconstruction from strict contraction
2026-10-29. Analytic construction; receiving review pending.

## Main result
Let Φ be a quantum channel whose state trace-distance contraction coefficient is c<1:
T(Φρ,Φτ)≤c T(ρ,τ) for all input states. For every finite ensemble with actual barycenter σ, define δ=χ(ensemble)−χ(Φ ensemble). Then the explicit EB channel Eσ(A)=Tr(A)σ satisfies
**Σ_x p_x T(ρ_x,σ)≤√δ/(1−c).**
This is an actual-prior conclusion for EVERY barycenter, not only diagonal or stationary ones. Its content is stronger than a nontrivial measurement in this strictly contracting regime: if Holevo loss is small, the ensemble itself is concentrated near its mean.

For Φγ=Ad_X∘ADγ on a qubit, c=√(1−γ), since its Bloch linear part is diag(√η,−√η,−η), η=1−γ. Thus for1/2≤γ<1,
**e_avg(Eσ)≤(2+√2)√δ, uniformly over ALL coherent or incoherent priors.**
This chooses a simpler EB mechanism than the previous retrodicted-dephasing candidate. Self-compatibility is true for this family but is NOT required by the general strict-contraction theorem.

## Proof: recovery plus contraction, not entropy iteration
For faithful σ and faithful Φσ use the universal averaged rotated-Petz recovery R=R_(σ,Φ), which satisfies RΦσ=σ and
T(ρ,RΦρ)≤√ℓ(ρ),
ℓ(ρ)=D(ρ||σ)−D(Φρ||Φσ).
This follows from the proved universal fidelity remainder, −2logF≤ℓ, and T≤√(1−F²). The same R works for everyρ. Its complete positivity and trace preservation imply
T(RΦρ,σ)=T(RΦρ,RΦσ)≤T(Φρ,Φσ)≤cT(ρ,σ).
Triangle inequality gives (1−c)T(ρ,σ)≤√ℓ(ρ). Averaging and Jensen finish because Σp_xℓ(ρ_x)=δ exactly for the actual mean. There is no stationarity assumption and no additive barycenter penalty.

The argument works in any finite input dimension provided a known state contraction coefficient c<1 is available. Support-restricted recovery handles singular output or input means; alternatively regularize all ensemble states by a common faithful state and pass by finite-dimensional entropy/trace continuity. For a pure qubit mean, all ensemble states equal that mean and the conclusion is immediate.

## Uniform stabilized qubit version
Suppose A is a qubit, Φ has state contraction c<1, and the ensemble on AR has product mean σ_A⊗ω_R. R is arbitrary finite-dimensional and need not be classical. The universal recovery factors as R_(σ,Φ)⊗id_R. Write Ψ=RΦ and let B be its real3×3 Bloch linear part. Trace contraction gives ||B||2≤c: Φ contracts byc and R contracts by≤1.

Consequently M=I−B is invertible, with ||M^−1||2≤1/(1−c), by the convergent Neumann series. Define a linear qubit map L(I)=0 and L(σ_j)=v_j·σ, where v_j is columnj of M^−1. Then
id−Eσ=L(id−Ψ).
Indeed it holds on traceless operators, and both deficit maps annihilateσ; every operator is a multiple ofσ plus a traceless operator. This identity tensors with id_R.

Each component A↦(v_j·σ)Tr(σ_j A)/2 has diamond norm||v_j||2 (output trace norm2||v_j||2 times functional norm1 divided by2). Therefore
||L||diamond≤Σ_j||v_j||2≤3||M^−1||2≤3/(1−c).
Using the stabilized universal-recovery remainder and Jensen gives
**Σ_xp_x T(ρ_AR,x,σ_A⊗ρ_R,x)≤[3/(1−c)]√δ.**
For XADγ withγ≥1/2, the coefficient is at most3(2+√2). This is uniform over all faithful coherentσ and all finite reference dimensions. Eσ⊗id_R is EB on A only; it is NOT globally EB across an untouched quantum reference. The product-mean hypothesis is substantive. This is not a tensorization theorem over many noisy qubits.

## Scope relative to earlier packets
The finite coherent-prior certificate remains valid and sharper for its particular complete case (coefficient5 versus uniform3(2+√2)). The diagonal-prior dephasing theorem remains sharper as a complete bound and preserves useful diagonal information. The uniform theorem removes the arbitrary-coherent-prior existence obligation for XAD without a prior-specific matrix inversion. It does not provide a uniform bound for all self-compatible channels: channels with c=1, or c→1, are not covered uniformly. No unrestricted N371 closure is asserted.

The reference-activation obstruction does not conflict: relative entropy and two-step loss ratios diverge, while direct trace distance scales as the square root of one-step loss. No monotonicity of successive entropy losses, EB CP-mixture component, or unrotated-Petz remainder is assumed.

## Dependencies and priority
Universal recovery: Junge–Renner–Sutter–Wilde–Winter, arXiv:1509.07127v3, Theorem2.1/Remark2.2 and stabilization discussion. https://arxiv.org/pdf/1509.07127
Strictly contractive quantum channels are established prior machinery: Raginsky, Phys. Rev. A65,032306(2002), arXiv:quant-ph/0105141. https://arxiv.org/pdf/quant-ph/0105141
The result is an elementary synthesis using known recovery and contraction principles. No historical novelty claim is made. Its role here is to close a concrete all-prior scientific obligation after rejecting overstrong entropy intermediates. Preparing the replacementσ assumes the actual prior is specified; no finite-data prior-learning or hardware advantage is claimed.
