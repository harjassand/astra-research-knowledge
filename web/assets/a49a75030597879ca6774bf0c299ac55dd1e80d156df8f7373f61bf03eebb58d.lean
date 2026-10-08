import N33Affine.AffineCore
import Mathlib.Analysis.SpecialFunctions.Pow.Continuity

open Filter Topology Set

namespace N33Affine.NextTypeAsymptotic

open N33Affine

variable {ι : Type*} [Fintype ι]
variable {h : ℕ → ℝ} {q : ℝ} {p : ι → ℕ → ℝ}
variable {p₀ c : ι → ℝ} {d : ℝ → ℝ}

/-- Varying-exponent separation, with no restriction on the approximating
exponents. The positive scale tends to zero and the limiting exponent has a
strict gap. -/
theorem rpow_ratio_tendsto_zero_of_lt
    {p : ℕ → ℝ} {p₀ q : ℝ}
    (hh : Tendsto h atTop (𝓝[>] 0))
    (hp : Tendsto p atTop (𝓝 p₀))
    (hpq : q < p₀) :
    Tendsto (fun n => Real.rpow (h n) (p n) / Real.rpow (h n) q)
      atTop (𝓝 0) := by
  let gap : ℝ := (p₀ - q) / 2
  have hgap_pos : 0 < gap := by
    dsimp [gap]
    linarith
  have hbase0 : Tendsto h atTop (𝓝 0) := hh.mono_right nhdsWithin_le_nhds
  have hpow0 : Tendsto (fun n => Real.rpow (h n) gap) atTop (𝓝 0) := by
    simpa [Real.zero_rpow hgap_pos.ne'] using hbase0.rpow_const (Or.inr hgap_pos.le)
  have hpos : ∀ᶠ n in atTop, 0 < h n := by
    exact hh.eventually
      (show ∀ᶠ x in 𝓝[>] 0, 0 < x from self_mem_nhdsWithin)
  have hone : ∀ᶠ n in atTop, h n < 1 :=
    (tendsto_order.1 hbase0).2 1 (by norm_num)
  have hexponent : ∀ᶠ n in atTop, gap ≤ p n - q := by
    filter_upwards
      [(tendsto_order.1 hp).1 (p₀ - gap) (by dsimp [gap]; linarith)] with n hn
    dsimp [gap] at hn ⊢
    linarith
  have hnonneg : ∀ᶠ n in atTop,
      0 ≤ Real.rpow (h n) (p n) / Real.rpow (h n) q := by
    filter_upwards [hpos] with n hn
    exact div_nonneg (Real.rpow_pos_of_pos hn (p n)).le
      (Real.rpow_pos_of_pos hn q).le
  have hle : ∀ᶠ n in atTop,
      Real.rpow (h n) (p n) / Real.rpow (h n) q ≤ Real.rpow (h n) gap := by
    filter_upwards [hpos, hone, hexponent] with n hn0 hn1 hngap
    calc
      Real.rpow (h n) (p n) / Real.rpow (h n) q =
          Real.rpow (h n) (p n - q) := (Real.rpow_sub hn0 (p n) q).symm
      _ ≤ Real.rpow (h n) gap :=
        Real.rpow_le_rpow_of_exponent_ge hn0 (le_of_lt hn1) hngap
  exact squeeze_zero' hnonneg hle hpow0

/-- Composing a little-o witness at positive scale zero with a sequence tending
to zero from the positive side preserves convergence to zero. -/
theorem littleO_comp_tendsto_zero
    (hh : Tendsto h atTop (𝓝[>] 0))
    (hd : LittleO d q) :
    Tendsto (fun n => d (h n) / Real.rpow (h n) q) atTop (𝓝 0) := by
  exact hd.comp hh

/-- A finite sum of fixed-coefficient monomials, each having a
strict exponent gap above `q`, is negligible relative to `h^q`. Adding any
`o(h^q)` offset still tends to zero after division by `h^q`.

The result allows arbitrary fixed real coefficients, which is stronger than
the nonnegative-coefficient case needed for the next-type comparison. -/
theorem finite_rpow_sum_add_littleO_tendsto_zero
    (hh : Tendsto h atTop (𝓝[>] 0))
    (hp : ∀ i, Tendsto (p i) atTop (𝓝 (p₀ i)))
    (hpq : ∀ i, q < p₀ i)
    (hd : LittleO d q) :
    Tendsto
      (fun n =>
        (∑ i : ι, c i *
          (Real.rpow (h n) (p i n) / Real.rpow (h n) q)) +
          d (h n) / Real.rpow (h n) q)
      atTop (𝓝 0) := by
  have hTerm : ∀ i, Tendsto
      (fun n => c i *
        (Real.rpow (h n) (p i n) / Real.rpow (h n) q))
      atTop (𝓝 0) := by
    intro i
    simpa using (rpow_ratio_tendsto_zero_of_lt (h := h) hh (hp i) (hpq i)).const_mul (c i)
  have hSum : Tendsto
      (fun n => ∑ i : ι, c i *
        (Real.rpow (h n) (p i n) / Real.rpow (h n) q))
      atTop (𝓝 0) := by
    simpa using
      (tendsto_finset_sum (Finset.univ : Finset ι) fun i _ => hTerm i)
  have hOffset := littleO_comp_tendsto_zero (h := h) (q := q) (d := d) hh hd
  simpa using hSum.add hOffset

end N33Affine.NextTypeAsymptotic
