import Mathlib

open Filter Topology

/-!
Sequential scale separation for varying real exponents.

The exponent sequence is only assumed to converge in `ℝ`; it is not required
that its terms lie in any prescribed cube. The positive-side hypothesis on the
scale sequence is expressed by convergence to `nhdsWithin 0 (Ioi 0)`.
-/

theorem rpow_ratio_tendsto_zero_of_lt
    {h p : ℕ → ℝ} {p₀ q : ℝ}
    (hh : Tendsto h atTop (nhdsWithin 0 (Set.Ioi 0)))
    (hp : Tendsto p atTop (nhds p₀))
    (hpq : q < p₀) :
    Tendsto (fun n => Real.rpow (h n) (p n) / Real.rpow (h n) q)
      atTop (nhds 0) := by
  let d : ℝ := (p₀ - q) / 2
  have hd : 0 < d := by
    dsimp [d]
    linarith
  have hbase0 : Tendsto h atTop (nhds 0) := hh.mono_right nhdsWithin_le_nhds
  have hpow0 : Tendsto (fun n => Real.rpow (h n) d) atTop (nhds 0) := by
    simpa [Real.zero_rpow hd.ne'] using hbase0.rpow_const (Or.inr hd.le)
  have hpos : ∀ᶠ n in atTop, 0 < h n := by
    exact hh.eventually (show ∀ᶠ x in nhdsWithin 0 (Set.Ioi 0), 0 < x from self_mem_nhdsWithin)
  have hone : ∀ᶠ n in atTop, h n < 1 :=
    (tendsto_order.1 hbase0).2 1 (by norm_num)
  have hgap : ∀ᶠ n in atTop, d ≤ p n - q := by
    filter_upwards
      [(tendsto_order.1 hp).1 (p₀ - d) (by dsimp [d]; linarith)] with n hn
    dsimp [d] at hn ⊢
    linarith
  have hnonneg :
      ∀ᶠ n in atTop, 0 ≤ Real.rpow (h n) (p n) / Real.rpow (h n) q := by
    filter_upwards [hpos] with n hn
    exact div_nonneg (Real.rpow_pos_of_pos hn (p n)).le (Real.rpow_pos_of_pos hn q).le
  have hle :
      ∀ᶠ n in atTop,
        Real.rpow (h n) (p n) / Real.rpow (h n) q ≤ Real.rpow (h n) d := by
    filter_upwards [hpos, hone, hgap] with n hn0 hn1 hngap
    calc
      Real.rpow (h n) (p n) / Real.rpow (h n) q =
          Real.rpow (h n) (p n - q) := (Real.rpow_sub hn0 (p n) q).symm
      _ ≤ Real.rpow (h n) d :=
        Real.rpow_le_rpow_of_exponent_ge hn0 (le_of_lt hn1) hngap
  exact squeeze_zero' hnonneg hle hpow0

theorem rpow_ratio_tendsto_atTop_of_lt
    {h p : ℕ → ℝ} {p₀ q : ℝ}
    (hh : Tendsto h atTop (nhdsWithin 0 (Set.Ioi 0)))
    (hp : Tendsto p atTop (nhds p₀))
    (hpq : p₀ < q) :
    Tendsto (fun n => Real.rpow (h n) (p n) / Real.rpow (h n) q)
      atTop atTop := by
  let d : ℝ := (q - p₀) / 2
  have hd : 0 < d := by
    dsimp [d]
    linarith
  have hpos : ∀ᶠ n in atTop, 0 < h n := by
    exact hh.eventually (show ∀ᶠ x in nhdsWithin 0 (Set.Ioi 0), 0 < x from self_mem_nhdsWithin)
  have hone : ∀ᶠ n in atTop, h n < 1 := by
    have hbase0 : Tendsto h atTop (nhds 0) := hh.mono_right nhdsWithin_le_nhds
    exact (tendsto_order.1 hbase0).2 1 (by norm_num)
  have hgap : ∀ᶠ n in atTop, p n - q ≤ -d := by
    filter_upwards
      [(tendsto_order.1 hp).2 (p₀ + d) (by dsimp [d]; linarith)] with n hn
    dsimp [d] at hn ⊢
    linarith
  have hpowTop :
      Tendsto (fun n => Real.rpow (h n) (-d)) atTop atTop :=
    (tendsto_rpow_neg_nhdsGT_zero (neg_lt_zero.mpr hd)).comp hh
  apply tendsto_atTop_mono' atTop ?_ hpowTop
  filter_upwards [hpos, hone, hgap] with n hn0 hn1 hngap
  calc
    Real.rpow (h n) (-d) ≤ Real.rpow (h n) (p n - q) :=
      Real.rpow_le_rpow_of_exponent_ge hn0 (le_of_lt hn1) hngap
    _ = Real.rpow (h n) (p n) / Real.rpow (h n) q := Real.rpow_sub hn0 (p n) q
