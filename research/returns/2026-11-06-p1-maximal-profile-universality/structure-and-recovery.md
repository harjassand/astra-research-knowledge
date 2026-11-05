# Finite structure and the exact recovery price

All statements on this page are the [unreviewed P1 return's claims](P1_MAXIMAL_PROFILE_UNIVERSALITY_20261106_RETURN.txt), preserved without a new Capital proof audit. They concern equality with the **identity channel's** complete maximal-information profile, rather than a general evaluator for all channel comparisons.

For a channel `Φ: M_d → M_b`, let `k=rank JΦ` be its Choi rank, choose a minimal Kraus list `K_i`, set `W=[K_1 … K_k]` and `S=Φ(I_d)`. The proposed whole-channel criterion is

`Φ has the perfect complete maximal profile ⇔ rank S = d rank JΦ ⇔ W is injective`.

On its effective output support, the normal form is `Φ(X)=W(I_k⊗X)W†`, with an invertible congruence. The maximal-perspective identity then gives the scalar and reference-valued preservation statements; injectivity is preserved under tensor products. The reverse direction uses perfect RLD equality, the Schwarz defect of the normalized unital CP map and its multiplicative domain. This equality mechanism has substantial prior history credited to Hiai–Mosonyi Theorem 3.34. The claimed contribution is its whole-channel rank specialization combined with the subsequent construction and cost theory.

With a **minimal complementary environment**, the response gives the equivalent finite condition `J_(Φ^c)>0`, using the Kraus Gram matrix up to transpose and factor permutation. For exact rational channel matrices, the rank test is finite exact matrix arithmetic. It is not N1690's general complete maximal-order evaluator, and gives no generic SLD/Umegaki comparison algorithm.

Let `G=W†W`. The optimal input-independent success probability of an exact CP trace-nonincreasing decoder is claimed to be

`p_*(Φ) = max { Tr H : H≥0, H⊗I_d ≤ G }`.

For `G>0` its matching dual is

`p_*(Φ) = min { Tr(GZ) : Z≥0, Tr_(C^d) Z ≥ I_k }`,

with attained optima and no duality gap. Every successful decoder's composite Kraus operators must be scalar multiples of the identity; their coefficient Gram matrix gives `H`. Conversely every feasible `H` constructs such a decoder on the range of `W`. This is an exact successful input/output contract, without assuming the failed branch preserves the unknown input.

The response deduces `p_* ≥ k λ_min(G)>0` for perfect-profile channels, and `p_*=1` exactly when `G=H⊗I_d` for a density matrix `H`. There is no uniform positive lower recovery probability over the class. After successful inversion, a supplied implementable target channel can be applied at its own cost; the uniform best guarantee over all targets is `p_*`, since the identity is among those targets. It is not free implementation of arbitrary channels.

For nontrivial input dimension `d≥2`, two claimed sharp consequences are:

| Statement | Exact scope |
|---|---|
| Minimum output dimension `b≥d²` | Perfect-profile channels approaching an input-independent replacer in one fixed output space; the complementary-depolarizing family attains the threshold |
| `p_*(Φ) ≤ min{1, δ/(1−d^−2)}` | Any channel within half-diamond distance `δ` of a replacer; a sharp supremum even inside the perfect-profile class |

The latter supremum can be approached in output dimension `d+d²` by an orthogonally flagged mixture of identity transmission and a complementary-depolarizing branch. For power-of-two `d` and rational distance budgets, the response states the approximating channels can be rational. The statements do not claim an optimum is attained at every parameter or that a generic optimal-recovery SDP solver was implemented.

[Construction and costs](construction-costs-and-prior-art.md) · [Overview](README.md)
