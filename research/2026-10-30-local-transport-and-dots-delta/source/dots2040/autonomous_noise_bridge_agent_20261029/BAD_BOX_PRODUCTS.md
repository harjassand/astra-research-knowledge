# All-box joint defect bound: independent check of root's strengthened projectors
Date: 2026-10-29. Root construction; algebra, inequality, and constants independently checked here.

Define P_x=V_xV_x†, G_x=Π_{y~x}P0_y, and
B_x=Q_x−P_xG_x.

Every B_x is a projector. All B_x commute. To see this, block-diagonalize by the set U of occupied ancillas. On that sector B_x is zero if x is absent, identity on the sector if x has an occupied neighbor, and R_x=Q_x−P_x if x is isolated in U. The isolated occupied boxes are pairwise disjoint, so all remaining R factors commute. The guarded Hamiltonian commutes with every B_x.

For any finite S, put B_S=Π_{x∈S}B_x. The clean adjoint satisfies on the FULL physical Hilbert space

L_clean*(B_S) ≤ −(Σ_{x∈S}κ_x) B_S.

For a reset y∈S the jump contribution is zero because the output has y ready, and the anticommutator loss is exactly −κ_y B_S. For a reset y∉S, examine each occupation sector: deleting y leaves the surviving B factors unchanged or changes identity factors into R_x for newly isolated occupied neighbors. These newly isolated boxes are mutually disjoint and disjoint from every previously isolated occupied box. Thus the pulled-back post-reset projector is a subprojection of the old B_S; reset y contributes a negative semidefinite operator. This proves the inequality without independence or a dilute-clock assumption.

## General local Markov noise
Suppose Σβ Nβ are local trace-preserving generators. Set νβ=||Nβ*||∞→∞. If each region β touches at most b B supports, and λ=sup_x Σβ touching suppBx νβ, then from a clean initial state

Tr(B_Sρ_t) ≤ a^|S|,  a=(λ/κ_min)^(1/b)≤1,

for every S,t and system size. The proof in DEFECT_SPARSITY.md now applies to all boxes, not just separated ones. Overlapping supports cause no problem: untouched B factors commute with all noise operators and with touched B factors, so the local generator factors through them. Its Hermitian norm bound then gives the same operator-order estimate.

## Coherent bath strengthening
Allow an arbitrary common bath with arbitrary H_bath, and bounded local system-bath couplings hβ. 'Local' means each term touches only a bounded physical region of the simulator, but its bath operator can be shared and long-memory. H_bath commutes with B_S. Let h=sup_x Σβ touching suppBx ||hβ|| and keep λ for additional local Markov generators; suppose each perturbation touches at most b B supports. For Tβ⊂S touched by hβ, Cauchy–Schwarz gives

|Tr(ρ i[hβ,B_S])| ≤ 2||hβ|| sqrt(m_S m_{S\Tβ}),

since B_{S\Tβ} commutes with hβ and B_S≤B_{S\Tβ}. Consequently the invariant barrier m_S≤a^|S| holds provided

κ_min a^b ≥ λ+2h a^(b/2).

Choosing

a = [(h+sqrt(h²+κ_min λ))/κ_min]^(2/b) ≤ 1

satisfies this equality. Initial system-bath correlations are allowed if the initial bad-box moments obey the barrier; in particular a clean encoded simulator tensored or correlated with a bath has zero bad-box moments. This statement concerns simulator defect occupancy, not logical data correctness.

## Numerical regression
bad_projector_check.py uses the 108-dimensional physical x−y−z model with nonunitary maps and checks all B_x projectors/commutators and all seven nonempty products. Largest eigenvalues of L*(B_S)+|S|B_S are ≤5.3e−16, consistent with negative semidefiniteness.

## Important limitation
This is an actual uniform-size/runtime joint **equal-time defect** bound, including finite reset rates and general local nonunitary noise, and can be stronger than a marginal defect-density statement. It is not a bound on spacetime data-fault paths. A perturbation can apply a data error without leaving any B defect, and a reset can clear the defect while preserving the damage already done to data. The two-body reduction and data fault-cluster law remain unproved.
