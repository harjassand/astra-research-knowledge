# Independent check: fixed-degree inverse-graph circuit over F₂(t)

**Verdict: the proposed divisor construction is valid under the stated polynomial-basis prefix convention.** It gives a fixed finite degree-2 lift dependency over F₂(t), and the same minimal dependency in every extension F₂^ℓ with ℓ > 2d. Consequently the fixed-r prefix girth cannot tend to infinity: all support points occur in one finite coefficient-label box. This is not a sampler result and the prefix threshold is enormous.

Let f₁,…,f_k be distinct monic irreducibles over F₂, set L=∏f_j, d=deg L, and let A range over the 3^k monic divisors of L². Write B_A=L²/A. Both A and B_A have degree at most 2d. Encode their coefficients in

    y_A = (coefficients(A), coefficients(B_A)) ∈ F₂^(4d+2).

For width w=4d+2, let Ψ_r(y) list the squarefree Boolean monomials of degree at most r, including 1; its length is M_r=Σ_{j=0}^r binom(w,j). If 3^k>M_r, the 3^k columns Ψ_r(y_A) are dependent. Choose a minimal-support dependency S, for example the lexicographically first circuit in this finite binary matrix. The support size is at most M_r+1 and is independent of any later extension degree.

The coefficient map is F₂-linear. For t an indeterminate it sends

    (A-coefficients, B-coefficients)
        ↦ (A(t), B(t)/L(t)²) = (u_A(t), u_A(t)⁻¹).

It is injective: a zero image forces A=0 and B=0 as polynomials. Hence it has an F₂-linear left inverse on its finite-dimensional image. An injective linear map preserves the kernel of the degree-at-most-r Boolean feature matrix: composition by the map sends degree-r Boolean polynomials to degree-r Boolean polynomials, while composition with a left inverse recovers every source polynomial of degree at most r. Squaring/reducing Boolean variables can only lower degree. Thus S remains a minimal degree-r dependency on the rational-function pairs. In the r=2 case, the cross-coordinate features also explicitly give

    Σ_(A∈S) A(t) ⊗ B_A(t) = 0,
    Σ_(A∈S) u_A(t) ⊗ u_A(t)⁻¹ = 0

in F₂(t)⊗_{F₂}F₂(t), the second equality following by multiplying the second tensor factor by L(t)⁻². The u_A(t) are nonzero and pairwise distinct because the A are distinct nonzero polynomials.

For any extension F₂^ℓ with an element α of degree ℓ>2d, evaluation of polynomials of degree at most 2d at α is injective. Also L(α)≠0. Therefore

    (A,B) ↦ (A(α), B(α)/L(α)²)

is again an injective F₂-linear map, and the same feature-kernel argument preserves S in both directions. All u_A(α) are nonzero and pairwise distinct: A(α)=A′(α) would make the nonzero polynomial A−A′ of degree at most 2d vanish at α. Their reciprocals are distinct as well. This holds for every sufficiently large prime ℓ, not just a subsequence.

For the standard initial enumeration by polynomial-basis bit labels 0,1,…, each u_A(α)=A(α) has label at most 2^(2d+1)−1 because no reduction modulo the degree-ℓ minimal polynomial is needed. Hence once the prefix includes that finite label box (for example, n≥2^(2d+1) is a safe threshold when zero is included at label 0), it contains the whole dependent support for every ℓ>2d. Thus a fixed-r prefix design has a uniform finite girth ceiling. The argument is conditional on this ordering; it does not transfer to a prefix in an unrelated ordering without a separate location bound.

Concrete counting checks for the stated small choices:

| r | factor degrees used | k | d | w | M_r | 3^k |
|---|---|---:|---:|---:|---:|---:|
| 2 | two degree-1, one degree-2, two degree-3, three degree-4 irreducibles | 8 | 22 | 90 | 4,096 | 6,561 |
| 3 | the above plus five degree-5 irreducibles | 13 | 47 | 190 | 1,143,326 | 1,594,323 |

The factor counts are exact: the numbers of monic irreducibles in degrees 1 through 5 are 2, 1, 2, 3, 6. For r=2, M₂=1+90+binom(90,2)=4,096. For r=3, M₃=1+190+binom(190,2)+binom(190,3)=1,143,326. These inequalities guarantee a circuit without enumerating the feature matrix; an exact finite elimination can recover a canonical support if an explicit list is required.

**Scope.** This falsifies unbounded girth for a fixed-r prefix of the specified coefficient-label order, including r=2 and r=3. It does not say the bound is practically reachable, supply a sampler, or rule out a different ordering or r growing with n. The finite-field specialization uses only ℓ>2d, so sufficiently large prime extension degrees are covered.
