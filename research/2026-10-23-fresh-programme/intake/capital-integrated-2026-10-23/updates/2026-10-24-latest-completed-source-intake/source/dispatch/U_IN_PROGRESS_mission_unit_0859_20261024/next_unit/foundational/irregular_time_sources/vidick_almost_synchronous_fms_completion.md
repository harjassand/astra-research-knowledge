# Vidick almost-synchronous theorem for the ordinary FMS completion

## Verdict

For a finite-dimensional tensor-product strategy on the ten common settings
`Z = X ⊔ Y`, the answer is **yes**: small average same-setting mismatch gives
an input-independent convex ensemble of projective maximally-entangled
(tracial) strategies whose **full fine correlation table** is close on an
arbitrary input-pair law with the same two marginals. Taking that law to be
`ν × ν` covers all 100 ordered setting pairs, including the otherwise
unconstrained distinct same-side pairs. This is precisely the ordinary
synchronous completion; it does not rely on an already-tracial FMS strategy.

The result is finite-tensor only. It does not establish the analogous claim
for arbitrary commuting-operator strategies.

## Primary result and hypotheses

Thomas Vidick, “Almost synchronous quantum correlations,”
[arXiv:2103.02468v3](https://arxiv.org/abs/2103.02468), Theorem 3.1 and
Corollary 3.3 (especially equations (19)–(21) and the proof of Corollary 3.3).
The paper defines `C_q` using finite-dimensional tensor-product Hilbert spaces
and finite setting and answer sets (Introduction, lines 50–56; Section 2,
Definitions 2.1–2.2). Its defect is

\[
\delta_{\rm sync}(C;\nu)
 = \mathbb E_{z\sim\nu}\sum_{a\ne b} C_{z,z,a,b}.
\]

This is exactly the same-question disagreement probability averaged under the
diagonal test law `ν` (Introduction, equation (4)).

Corollary 3.3 states that if `S=(|ψ⟩,A,B)` is projective, then for **any** law
`\tildeν` on `Z × Z` with both marginals `ν`, its correlation `C` and the
ensemble correlation satisfy

\[
\mathbb E_{(x,y)\sim\tilde\nu}\sum_{a,b}
\left|C_{x,y,a,b}-\int C^\lambda_{x,y,a,b}\,d\mu(\lambda)\right|
 = \operatorname{poly}(\delta_{\rm sync}).
\]

The ensemble terms are PME correlations: each `|ψ_λ⟩` is maximally entangled
on a finite-dimensional subspace and each local measurement is projective.
The error polynomial is universal and dimension-independent; the paper also
states that the main approximation has no dependence on setting or answer-set
size (Theorem 3.1 and discussion immediately after it). The theorem's
spectral-cut ensemble depends on the reduced shared state, not on the input.
For a finite-dimensional state, the integral can be written as a finite
convex sum (Theorem 3.1, discussion following equation (20)).

Corollary 3.3 assumes projective measurements, but says this is without loss
of generality: local Naimark dilations realize the same correlation as a
projective strategy (its paragraph immediately after equation (21)). The
original five answer labels remain the labels of the dilated POVM; no new
answer needs to be exposed.

The rounded blocks come from the canonical shared-state spectral cut. In the
proof, `P_λ = 1_[λ,∞)(ρ)` and `dμ(λ)=Tr(P_λ)dλ`; the block state is
`ρ_λ=P_λ/Tr(P_λ)`, maximally mixed on that support, and the associated shared
vector is maximally entangled there (proof of Theorem 3.1, equations (34)–(35)
and preceding construction). Thus this is a genuine shared-state-based,
input-independent ensemble, not a separately selected block for each input.

## Application to the specified completion

Take `Z=X ⊔ Y`, with `|X|=|Y|=5`, and identify the two players' answer
alphabets with the same five typed labels. For a finite-tensor strategy define
`ν` as the law used to test the diagonal settings `z=z`; then the mismatch
specified in the question is exactly `δ_sync(C;ν)`. Naimark-dilate the
strategy if necessary, without changing its complete table. Apply Corollary
3.3 with

\[
\tilde\nu=\nu\otimes\nu.
\]

If `ν` has full support on the ten labels (in particular, if it is uniform),
this law covers every ordered pair. Therefore the result approximates the
fine probabilities on all 100 cells, not only the FMS cells `X×Y` and their
transpose `Y×X`; leaving the other distinct same-side cells unconstrained
does not affect the theorem. For uniform `ν`, the average in Corollary 3.3 is
the uniform average of the 100 per-cell `ℓ₁` errors. Consequently every
individual cell error is at most `100·poly(δ_sync)` as a simple fixed-size
conversion. A bounded payoff under any other pair law `π` is controlled by
the corresponding change-of-measure factor; if `π` is the equal mixture of
uniform `X×Y` and uniform `Y×X`, that factor relative to uniform `ν×ν` is 2.

If the diagonal test law is uniform and the full completion game assigns
diagonal-query mass `η`, then its diagonal loss is exactly `ηδ_sync`.
Because the other losses are nonnegative, a total game loss `ε` implies
`δ_sync ≤ ε/η`. This is only the direct diagonal-loss accounting; it is not
needed when `δ_sync` itself is supplied.

## Scope limits

- The guarantee is average `ℓ₁` table error under a selected coupling, not a
  worst-case cell estimate independent of the ten-setting conversion.
- It gives a convex mixture of max-ent strategies, not closeness of the
  original pure shared state to one maximally entangled state. Vidick notes
  this distinction explicitly after Theorem 3.1.
- The source treats finite-dimensional tensor-product correlations. Do not
  promote it to the commuting model without a separate argument.
- If `ν` omits a setting, `ν×ν` does not control table cells involving that
  setting; full-table coverage requires the diagonal law to have full support.

