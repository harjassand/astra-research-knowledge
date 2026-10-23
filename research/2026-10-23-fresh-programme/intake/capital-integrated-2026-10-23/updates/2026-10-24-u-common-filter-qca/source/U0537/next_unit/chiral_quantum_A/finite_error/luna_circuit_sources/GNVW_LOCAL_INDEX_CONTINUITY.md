# A finite-band operator-norm continuity radius for the 1D QCA index

## Statement

Let the infinite chain have identical onsite Hilbert-space dimension `q`. Let `α,β` be QCA automorphisms whose Heisenberg images of any local observable are supported within `R` sites of its support. Assume `R≥1`, and put

`s=R`, `D=q^s`.

Group sites into blocks `C_0=[1-s,0]`, `C_1=[1,s]` immediately across a cut, each with algebra `M_D`. Let `e^j_ab` be any fixed matrix-unit basis of the algebra on `C_j`, for `j=0,1`, and define the finite-band discrepancy

`δ = max_{j=0,1; a,b=1,...,D} ||α(e^j_ab)-β(e^j_ab)||_op`.

If

`δ < 1 / ((D+1) D^(11/2))`,

then `ind(α)=ind(β)`. This is a sufficient (conservative) radius, not an optimized one. The norm is only required for the two block algebras adjacent to one cut; there is no global automorphism norm. Both outputs are supported in the common physical-site window `[-2s+1,2s]` (4s sites), so the matrix-unit discrepancy is a finite-window operator norm.

Equivalently, if the stronger block-action bound

`sup_{x in M_D, ||x||≤1} ||α(x)-β(x)||_op ≤ ε_cell`

is available on both `C_0,C_1`, it suffices that

`ε_cell < 1 / ((D+1) D^4)`.

For a radius-zero QCA the action is onsite and its index is 1, so the nontrivial case is `R≥1`.

## Derivation from GNVW §7.6

Gross–Nesme–Vogts–Werner Proposition 13, Eq. (44), gives for this nearest-neighbor grouping

`ind(α) = n_α/m_α`,

where `n_α=η(α(A_{C_0}),A_{C_1})` and `m_α=η(α(A_{C_1}),A_{C_0})`. Their Lemma 12, item 6, states that if `γ` is an automorphism and `||γ(x)-x||≤ε||x||` on a matrix algebra `B_1≅M_D`, then

`|η(γ(B_1),B_2)-η(B_1,B_2)| ≤ ε D^2`.

Use `γ=β∘α^{-1}`. For `y=α(x)`, the cell-action bound gives

`||γ(y)-y|| = ||β(x)-α(x)|| ≤ ε_cell ||y||`.

Apply Lemma 12 first with `B_1=α(A_{C_0}), B_2=A_{C_1}`, then with `B_1=α(A_{C_1}), B_2=A_{C_0}`. Thus both numerator and denominator change by at most `Δ=ε_cell D^2`.

Each overlap is at least 1 (Lemma 12, item 2) and at most `D`: the projections onto the two `M_D` subalgebras in the tracial GNS Hilbert space each have rank `D^2`, so `Tr(P_1P_2)≤D^2` and `η=√Tr(P_1P_2)≤D`. Therefore

`|ind(α)-ind(β)| ≤ (D+1) Δ = (D+1)D^2 ε_cell`.

Theorem 9 says the reduced numerator and denominator of each index divide every grouped-cell dimension, hence each is at most `D`. Distinct possible indices differ by at least `1/D^2`, since for distinct `p/q,p'/q'` with `p,q,p',q'≤D`, `|p/q-p'/q'|=|pq'-p'q|/(qq')≥1/D^2`. A strict ratio difference below `1/D^2` forces equality, yielding the stated block-action radius.

To pass from matrix-unit discrepancies to a block-action bound, write `x=Σ_{a,b}x_{ab}e_{ab}`. For `||x||_op≤1`,

`Σ_{a,b}|x_{ab}| ≤ D ||x||_F ≤ D^(3/2)`.

Hence `ε_cell≤D^(3/2)δ`. Substitution gives the stated matrix-unit threshold `δ < 1/((D+1)D^(11/2))`.

The support sizes follow directly from the radius assumption: `α(A_{C_0})` is supported in `[-2s+1,s]`, and `α(A_{C_1})` in `[-s+1,2s]`; the same holds for `β`. Their union is the advertised 4s-site band. The data required are the two complete matrix-unit images on `C_0` and `C_1`, not a global comparison of automorphisms.

Primary source: [GNVW, *Index theory of one dimensional quantum walks and cellular automata*, §7.6, Lemma 12 and Proposition 13, Eq. (44), Theorem 9](https://arxiv.org/html/0910.3675). In particular, see Lemma 12(6) for the explicit `εD²` overlap bound and Proposition 13 for the cut-local quotient.

## Scope correction for the frozen prior note

The factorization `W=S_A⊗V_B` from exact return with full-rank `τ_B` does not require a product state. The subsequent simple-spectrum/index contradiction does: narrow that claim to `τ_B=⊗_i τ_i`, diagonal in an onsite product eigenbasis, with a simple finite-volume product spectrum. Simplicity of an interacting global `τ_B` only makes `V_B` diagonal in its global eigenbasis; it does not make its conjugation action fix the onsite diagonal algebra needed for GNVW Proposition 10. In particular, a translation-invariant interacting Gibbs operator can commute with the translation even when a finite-volume spectrum is simple. The exact product-catalyst argument does not apply to that case. The earlier note is left frozen as instructed; this records the correction for its next revision.
