# Finite certificate for an actual coherent-prior EB comparator
2026-10-29. Candidate construction; independent receiving review pending.

## General certificate mechanism
Fix a channel Φ and faithful prior σ with faithful ν=Φσ. Let Ψ=Rbar_(σ,Φ)Φ be the actual universal averaged rotated-Petz recovered channel. It fixes σ. Choose an explicit EB channel E that also fixes σ. For qubits define real3×3 matrices
M_ij=Tr[σ_i(id−Ψ)(σ_j)]/2,
N_ij=Tr[σ_i(id−E)(σ_j)]/2,
where σ_i are Pauli matrices. If M is invertible, set T=NM^−1. Define the linear map L on qubit operators by L(I)=0 and L(σ_j)=Σ_iT_ijσ_i. Then
id−E=L(id−Ψ)
on ALL operators: it holds on traceless operators by construction, and both deficits vanish on σ; every operator decomposes into a multiple of σ and a traceless remainder. The same identity tensors with any reference.

Each map A↦σ_i Tr(σ_j A)/2 has diamond norm1 (trace norm of outputσ_i is2; norm of the input linear functional Trσ_j· is1). Therefore ||L||diamond≤Σ_ij|T_ij|=:C. Universal recovery gives T(ρ,Ψρ)≤√ℓσ,Φ(ρ), so
T(ρ,Eρ)≤C√ℓσ,Φ(ρ).
For any ensemble with ACTUAL mean σ, Σp_xℓσ,Φ(ρ_x)=χ(E)−χ(ΦE)=δ. Jensen gives e_avg(E)≤C√δ with no barycenter penalty. The complete statement holds for ensemble mean σ⊗ω_R because recovery factors on the unchanged reference. No statement is made for arbitrary correlated AR barycenters.

This is a finite sufficient certificate, not a claim every channel has invertible M or a uniformly bounded C. It is useful when an explicit E fixes the actual prior and a validated inverse exists. E itself is implemented by its measurement/repreparation rule; the recovery map is an analytical witness, not a required unknown-source inverse.

## Executed coherent-prior instance
Φ=Ad_X∘AD_(1/2), σ=[[1/2,1/4],[1/4,1/2]].
Choose E=R_(σ,Δ)Δ, where Δ is computational dephasing. Explicitly measure Z; on outcome j prepare σ^(1/2)|j><j|σ^(1/2)/σ_jj. This is a two-outcome EB channel and Σ_jσ^(1/2)|j><j|σ^(1/2)=σ, so Eσ=σ exactly.

The universal rotated map is evaluated by spectral projectors P_i of σ and Q_a of ν. If R0 is the unrotated Petz map,
Rbar(Y)=Σ_(i,j,a,b) κ([log s_i−log s_j−log v_a+log v_b]/2) P_i R0(Q_aYQ_b) P_j,
κ(x)=x/sinh x, κ(0)=1.
The kernel follows directly from β0(t)=π/[2(coshπt+1)]: y=e^(πt) transforms its Fourier integral into ∫_0∞y^(ix/π)/(1+y)^2dy=B(1+ix/π,1−ix/π)=x/sinh x. Thus no time quadrature approximation is used.

The prior eigenvalues are1/4,3/4 and the output eigenvalues1/2±√6/8, with explicit projectors. certify_one_prior.py evaluates all matrix operations, logarithms, exponentials, and the adjugate inverse using45-digit outward interval arithmetic. It proves detM>0 and
Σ|T_ij|∈[4.3686449267162265023763955878814707761410534654104,
           4.3686449267162265023763955878814707761410553690744] <5.
Consequently, **e_avg(E)≤5√δ** for every ensemble with this coherent barycenter, including the specified product-barycenter quantum-reference extension. The bound can of course be truncated at1.

The runtime/interval implementation is trusted numerical infrastructure, not a formal proof-assistant certificate. Independent interval replay is requested. The generic378-point floating sweep in explore.py merely motivated the instance and proves no universal bound.

## Dependencies and limits
Universal recovery: Junge–Renner–Sutter–Wilde–Winter, arXiv:1509.07127v3 Theorem2.1/Remark2.2, https://arxiv.org/pdf/1509.07127. Standard recovery, Petz transpose, Fourier/Beta identity, and diamond norm estimates are not claimed new. The exact obstruction packet establishes this channel has zero CPTP EB minorization weight and can fail complete entropy intermediate comparisons. Neither that obstruction nor this one-prior finite certificate resolves unrestricted N371, arbitrary coherent priors, or tensorization over many noisy qubits. No practical acquisition advantage or learned-prior guarantee is claimed.
