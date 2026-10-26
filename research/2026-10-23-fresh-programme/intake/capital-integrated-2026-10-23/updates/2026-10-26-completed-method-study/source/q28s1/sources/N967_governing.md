# Sharp intrinsic contraction for every subalgebra of a full matrix algebra

24 October 2026. Independent constructive verification. No historical novelty claim is made. The unitary-basis existence theorem used below is prior work, explicitly attributed in Section 3.

## 1. Statement and conventions

Let H_A = ⊕_i (A_i ⊗ B_i), with dim A_i = n_i and dim B_i = m_i, and let E be the ordinary-trace-preserving conditional expectation from B(H_A) onto

N = ⊕_i (B(A_i) ⊗ I_{B_i}).

Thus E first deletes off-diagonal sector blocks and then replaces each B_i factor by its normalized identity. Put C = Σ_i m_i². For C > 1 and 0 ≤ λ ≤ 1, define Φ_λ = λ id + (1−λ) E.

Allow arbitrary finite untouched references, and write E_R = E ⊗ id_R. Then the supremum conditional relative-entropy contraction and its restriction to E_Rρ = E_Rσ are both exactly

c_C(λ) = (C−1) λ² / [1+(C−2)λ].

The conditional divergence is J_E(ρ,σ) = D(ρ||σ) − D(E_Rρ||E_Rσ). Ratios are taken only for positive denominators. This is not the unrestricted full relative-entropy contraction, which is one when nontrivial fixed directions exist. For C = 1, E is the identity and J_E is identically zero, so the ratio formulation is excluded.

All sharpness limits can be realized by faithful pairs. Reference dimension (Σ_i m_i) C suffices for the upper-contraction supremum. This is a finite sufficient dimension, not a minimality assertion.

## 2. Independent proof of the complete index

The complete order index is the least c such that Z ≤ c(E⊗id_R)(Z) for every finite R and every Z ≥ 0. We prove it equals C.

For each diagonal block, the elementary partial-trace bound gives

Z_ii ≤ m_i I_{B_i} ⊗ Tr_{B_i}(Z_ii) = m_i² E_i(Z_ii).

Tensor factors may be reordered in this display. One proof decomposes Z_ii into rank-one operators, uses Schmidt rank at most m_i for each vector, and applies Cauchy–Schwarz in its Schmidt expansion. This argument is uniform in the reference dimension.

For a vector v = ⊕_i v_i, put a_i = ⟨v_i,Z_ii v_i⟩ and b_i = ⟨v_i,E_i(Z_ii)v_i⟩. Positivity of Z bounds every cross term by √(a_i a_j). Therefore

⟨v,Zv⟩ ≤ (Σ_i √a_i)² ≤ (Σ_i m_i√b_i)² ≤ C Σ_i b_i.

Thus the complete index is at most C.

For the reverse inequality, introduce R_0 = ⊕_i R_i, dim R_i = m_i, choose unit a_i in A_i, and let Φ_i be the normalized maximally entangled vector in B_i⊗R_i. Define

P = ⊕_i |a_i⟩⟨a_i| ⊗ I_{B_i} ⊗ I_{R_i},
ψ = Σ_i (m_i/√C) a_i ⊗ Φ_i.

Here P is supported only on matched physical/reference sectors i; it is an orthogonal projection of rank C on H_A⊗R_0. Direct partial trace gives E_{R_0}(|ψ⟩⟨ψ|)=P/C. Evaluating the order inequality in ψ forces c ≥ C. Hence C_cb(E)=C.

## 3. Governing prior unitary-basis theorem

Crann, Kribs and Pereira, “Orthogonal Unitary Bases and a Subfactor Conjecture,” Proceedings of the AMS 151 (2023), 3793–3799, Theorems 2.1–2.2, establish a unitary orthonormal basis for ⊕_i M_{m_i} with trace

φ(⊕_i X_i) = C^−1 Σ_i m_i Tr(X_i).

The theorem is stated using its trace-preserving representation ⊕_i I_{m_i}⊗M_{m_i} in M_C. Thus its weights are exactly those required here, not the generally different normalized trace inherited from the original physical representation.

Primary source: https://arxiv.org/html/2211.11732#S2 ; published DOI: https://doi.org/10.1090/proc/16346 . Theorem 2.2 is constructive. We use this existing basis theorem, not a new claimed existence result.

Let U_α = ⊕_i U_{iα}, α=1,…,C, be the resulting unitaries, satisfying φ(U_α*U_β)=δ_{αβ}.

## 4. Complete flat orthogonal code

Define

ψ_α = Σ_i (m_i/√C) a_i ⊗ (U_{iα}⊗I_{R_i}) Φ_i,
F_α = |ψ_α⟩⟨ψ_α|.

Their inner products are

⟨ψ_α,ψ_β⟩ = C^−1 Σ_i m_i Tr(U_{iα}*U_{iβ}) = δ_{αβ}.

Each vector lies in the rank-C range of P. Thus the F_α are orthogonal rank-one projections summing to P. E removes cross terms between distinct physical sectors. Within each sector, maximal entanglement gives the same reduced reference identity regardless of U_{iα}. Consequently

E_{R_0}(F_α) = P/C for every α,
E_{R_0}(P)=P.

This supplies the full flat code. An index-achieving vector by itself would not have proved this; the external unitary-basis theorem is the additional substantive input.

## 5. Exact classical-channel embedding and sharpness

For arbitrary positive reference blocks r_α on a further auxiliary S, encode the classical-block operator ⊕_α r_α as

Θ(⊕_α r_α) = Σ_α F_α ⊗ r_α.

This is an isometric orthogonal-sector embedding, preserving relative entropy. Furthermore,

E_{R_0S}Θ(r) = (P/C) ⊗ Σ_α r_α,
Φ_{λ,R_0S}Θ(r) = Θ(K_{λ,C} r),

where K_{λ,C} is the classical C-symbol uniform-reset channel. Therefore the conditional divergence and the equal-conditioned restriction both match their classical-label, quantum-reference versions exactly.

The established simplex construction for K_{λ,C}, with dim S=C, has equal reference marginals and approaches c_C(λ). Explicitly, choose unit regular-simplex vectors v_α in a (C−1)-dimensional subspace orthogonal to a vacuum |0⟩, set

s_α = (1−ε)|v_α⟩⟨v_α| + ε I_S/C,
X_α = |v_α⟩⟨0| + |0⟩⟨v_α|,
σ = C^−1 ⊕_α s_α,  H = C^−1 ⊕_α X_α.

The marginal tangent vanishes. With c=λ+(1−λ)/(C−1), the local BKM quotient is

(λ²/c) log[1+C(1−ε)c/ε] / log[1+C(1−ε)/ε],

which tends to c_C(λ) as ε decreases to zero. Faithful nearby pairs σ+tH and σ realize the metric limit as t tends to zero. The cases λ=0 and λ=1 follow directly.

The intrinsic-index upper bound in intrinsic_index_extension.md applies to all finite references and gives the reverse inequality. This proves the claimed equality.

If P is not the identity, encoded states are faithful on P⊗S only. Mix both hypotheses with the same positive-weight normalized identity on (I−P)⊗S. Because E(P)=P, this complementary blank is fixed by E and Φ_λ, and is orthogonal to the active block both before and after the channels. Every relevant conditional divergence scales by the same active weight; the quotient and equality of conditioned states are unchanged. The resulting states are faithful on the entire physical/reference space.

## 6. Relative comparison consequence and scope

For 0 < λ ≤ μ ≤ 1, the sharp upper relative conditional comparison is

J_E(Φ_λρ,Φ_λσ) / J_E(Φ_μρ,Φ_μσ)
≤ (λ/μ)² [1+(C−2)μ] / [1+(C−2)λ].

The intrinsic upper is proved in relative_two_sided_comparison.md, and the same embedded simplex family attains its supremum. For 0 < λ ≤ μ < 1 and C ≥ 3, the universal lower comparison

(λ/μ)² (1−μ)/(1−λ)

is also sharp, by embedding the classical construction with one dominant baseline symbol and tangent supported on two other symbols. No sharpness claim for this lower formula is made at C=2.

This theorem covers every trace-preserving inclusion into one full matrix algebra, regardless of n_i or unequal multiplicities m_i. It does not automatically settle all inclusions between arbitrary multi-matrix algebras that identify ambient central sectors. Nor does it give a minimal reference dimension, uniform well-conditioning of near-optimal witnesses, or a mutual-information coefficient for these general expectations.
