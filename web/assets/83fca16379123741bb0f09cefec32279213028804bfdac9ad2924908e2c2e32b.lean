import RpowScaleSeparation

open Filter Topology Asymptotics

/-!
A positive fixed coefficient on a lower limiting exponent eventually dominates
both a higher-power scale and any little-o bump at that higher scale.
-/

theorem no_eventually_le_of_rpow_ratio_atTop
    {h p : ℕ → ℝ} {p₀ q c : ℝ} {bump : ℝ → ℝ}
    (hh : Tendsto h atTop (nhdsWithin 0 (Set.Ioi 0)))
    (hp : Tendsto p atTop (nhds p₀))
    (hpq : p₀ < q)
    (hc : 0 < c)
    (hbump : bump =o[nhdsWithin 0 (Set.Ioi 0)] (fun x : ℝ => Real.rpow x q)) :
    ¬ (∀ᶠ n in atTop,
      c * Real.rpow (h n) (p n) + bump (h n) ≤ Real.rpow (h n) q) := by
  intro hineq
  let ratio : ℕ → ℝ := fun n => Real.rpow (h n) (p n) / Real.rpow (h n) q
  let bumpRatio : ℕ → ℝ := fun n => bump (h n) / Real.rpow (h n) q
  have hratio : Tendsto ratio atTop atTop := by
    dsimp [ratio]
    exact rpow_ratio_tendsto_atTop_of_lt hh hp hpq
  have hbump0 :
      Tendsto (fun x : ℝ => bump x / Real.rpow x q)
        (nhdsWithin 0 (Set.Ioi 0)) (nhds 0) :=
    Asymptotics.IsLittleO.tendsto_div_nhds_zero hbump
  have hbumpSeq : Tendsto bumpRatio atTop (nhds 0) := by
    dsimp [bumpRatio]
    exact hbump0.comp hh
  have hratioLarge : ∀ᶠ n in atTop, 2 / c < ratio n :=
    hratio.eventually_gt_atTop (2 / c)
  have hbumpLower : ∀ᶠ n in atTop, -1 < bumpRatio n :=
    (tendsto_order.1 hbumpSeq).1 (-1) (by norm_num)
  have hpos : ∀ᶠ n in atTop, 0 < h n := by
    exact hh.eventually
      (show ∀ᶠ x in nhdsWithin 0 (Set.Ioi 0), 0 < x from self_mem_nhdsWithin)
  have hdenpos : ∀ᶠ n in atTop, 0 < Real.rpow (h n) q := by
    filter_upwards [hpos] with n hn
    exact Real.rpow_pos_of_pos hn q
  have hnormalized :
      ∀ᶠ n in atTop,
        (c * Real.rpow (h n) (p n) + bump (h n)) / Real.rpow (h n) q ≤ 1 := by
    filter_upwards [hineq, hdenpos] with n hn hden
    calc
      (c * Real.rpow (h n) (p n) + bump (h n)) / Real.rpow (h n) q ≤
          Real.rpow (h n) q / Real.rpow (h n) q :=
        div_le_div_of_nonneg_right hn hden.le
      _ = 1 := div_self hden.ne'
  have hdecomp (n : ℕ) :
      (c * Real.rpow (h n) (p n) + bump (h n)) / Real.rpow (h n) q =
        c * ratio n + bumpRatio n := by
    dsimp [ratio, bumpRatio]
    rw [add_div, mul_div_assoc]
  have hnormalized' : ∀ᶠ n in atTop, c * ratio n + bumpRatio n ≤ 1 := by
    filter_upwards [hnormalized] with n hn
    simpa only [hdecomp n] using hn
  have hlarge : ∀ᶠ n in atTop, 2 < c * ratio n := by
    filter_upwards [hratioLarge] with n hn
    have hmul := mul_lt_mul_of_pos_left hn hc
    have hcancel : c * (2 / c) = 2 := by
      field_simp [ne_of_gt hc]
    rw [hcancel] at hmul
    exact hmul
  have hsum : ∀ᶠ n in atTop, 1 < c * ratio n + bumpRatio n := by
    filter_upwards [hlarge, hbumpLower] with n hn₁ hn₂
    linarith
  obtain ⟨n, hn⟩ := (hsum.and hnormalized').exists
  exact (not_lt_of_ge hn.2) hn.1
