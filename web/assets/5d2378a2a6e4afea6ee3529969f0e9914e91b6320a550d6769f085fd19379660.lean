import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic

noncomputable section

open Filter Set

namespace N33Dynamics

/-- The logarithmic size of the uncapped `n`th square-root scale. -/
def cappedScaleMagnitude (A P : ℝ) (n : ℕ) : ℝ :=
  max (A / (2 : ℝ) ^ n) P

/-- Closed form of the scale sequence `h_(n+1) = min (sqrt h_n) h_P`.
The variables `A` and `P` are the positive logarithmic magnitudes of `h₀` and `h_P`. -/
def cappedSqrtScale (A P : ℝ) (n : ℕ) : ℝ :=
  Real.exp (-(cappedScaleMagnitude A P n))

theorem cappedScaleMagnitude_succ {A P : ℝ} (hP : 0 < P) (n : ℕ) :
    cappedScaleMagnitude A P (n + 1) =
      max (cappedScaleMagnitude A P n / 2) P := by
  let x : ℝ := A / (2 : ℝ) ^ n
  have hpow : A / (2 : ℝ) ^ (n + 1) = x / 2 := by
    dsimp [x]
    rw [pow_succ]
    field_simp
  change max (A / (2 : ℝ) ^ (n + 1)) P =
    max (max (A / (2 : ℝ) ^ n) P / 2) P
  rw [hpow]
  by_cases hx : x ≤ P
  · have hx2 : x / 2 ≤ P := by linarith
    have hP2 : P / 2 ≤ P := by linarith
    simp only [show A / (2 : ℝ) ^ n = x by rfl,
      max_eq_right hx, max_eq_right hx2, max_eq_right hP2]
  · have hPx : P ≤ x := le_of_not_ge hx
    simp only [show A / (2 : ℝ) ^ n = x by rfl, max_eq_left hPx]

private theorem exp_neg_max (a b : ℝ) :
    Real.exp (-max a b) = min (Real.exp (-a)) (Real.exp (-b)) := by
  rcases le_total a b with hab | hba
  · rw [max_eq_right hab, min_eq_right]
    exact Real.exp_le_exp.mpr (by linarith)
  · rw [max_eq_left hba, min_eq_left]
    exact Real.exp_le_exp.mpr (by linarith)

private theorem sqrt_exp_neg (x : ℝ) :
    Real.sqrt (Real.exp (-x)) = Real.exp (-x / 2) := by
  rw [Real.sqrt_eq_iff_eq_sq (Real.exp_nonneg _) (Real.exp_nonneg _)]
  rw [pow_two, ← Real.exp_add]
  congr 1
  ring

theorem cappedSqrtScale_succ {A P : ℝ} (hP : 0 < P) (n : ℕ) :
    cappedSqrtScale A P (n + 1) =
      min (Real.sqrt (cappedSqrtScale A P n)) (Real.exp (-P)) := by
  change Real.exp (-(cappedScaleMagnitude A P (n + 1))) =
    min (Real.sqrt (Real.exp (-(cappedScaleMagnitude A P n)))) (Real.exp (-P))
  rw [cappedScaleMagnitude_succ hP]
  rw [exp_neg_max, sqrt_exp_neg]
  rw [show -(cappedScaleMagnitude A P n / 2) =
      -cappedScaleMagnitude A P n / 2 by ring]

theorem cappedSqrtScale_eq_cap_of_le {A P : ℝ} (n : ℕ)
    (h : A / (2 : ℝ) ^ n ≤ P) :
    cappedSqrtScale A P n = Real.exp (-P) := by
  simp [cappedSqrtScale, cappedScaleMagnitude, max_eq_right h]

/-- The source's capped square-root schedule, written in terms of the initial and target
scales. It is defined by a closed formula so finite arrival at the cap is explicit. -/
def permanenceScale (h₀ hP : ℝ) (n : ℕ) : ℝ :=
  cappedSqrtScale (-Real.log h₀) (-Real.log hP) n

theorem permanenceScale_zero {h₀ hP : ℝ} (hh₀ : 0 < h₀)
    (h₀P : h₀ ≤ hP) :
    permanenceScale h₀ hP 0 = h₀ := by
  have hlog : Real.log h₀ ≤ Real.log hP := Real.log_le_log hh₀ h₀P
  simp [permanenceScale, cappedSqrtScale, cappedScaleMagnitude,
    max_eq_left (by linarith : -Real.log hP ≤ -Real.log h₀),
    Real.exp_log hh₀]

theorem permanenceScale_cap {h₀ hP : ℝ} (hhP : 0 < hP)
    (hh₀ : 0 < h₀) (hhP1 : hP < 1) (h₀P : h₀ ≤ hP) :
    ∃ N : ℕ, permanenceScale h₀ hP N = hP := by
  have hPlog : 0 < -Real.log hP := by
    have := Real.log_neg hhP hhP1
    linarith
  have h₀log : 0 < -Real.log h₀ := by
    have hlog : Real.log h₀ ≤ Real.log hP := Real.log_le_log hh₀ h₀P
    linarith
  have hpow : Tendsto (fun n : ℕ => (2 : ℝ) ^ n) atTop atTop :=
    tendsto_pow_atTop_atTop_of_one_lt (by norm_num)
  obtain ⟨N, hN, hlarge⟩ :=
    exists_lt_of_tendsto_atTop hpow 0 ((-Real.log h₀) / (-Real.log hP))
  have hden : 0 < (2 : ℝ) ^ N := pow_pos (by norm_num) _
  have hmul : -Real.log h₀ < (2 : ℝ) ^ N * (-Real.log hP) := by
    have hmul' := (div_lt_iff₀ hPlog).mp hlarge
    simpa [mul_comm] using hmul'
  have hratio : (-Real.log h₀) / (2 : ℝ) ^ N ≤ -Real.log hP :=
    le_of_lt ((div_lt_iff₀ hden).2 (by simpa [mul_comm] using hmul))
  refine ⟨N, ?_⟩
  rw [permanenceScale, cappedSqrtScale_eq_cap_of_le N hratio]
  simp [Real.exp_log hhP]

theorem permanenceScale_succ {h₀ hP : ℝ} (hhP : 0 < hP)
    (hhP1 : hP < 1) (n : ℕ) :
    permanenceScale h₀ hP (n + 1) =
      min (Real.sqrt (permanenceScale h₀ hP n)) hP := by
  have hPlog : 0 < -Real.log hP := by
    have := Real.log_neg hhP hhP1
    linarith
  simpa [permanenceScale, Real.exp_log hhP] using
    (cappedSqrtScale_succ (A := -Real.log h₀) (P := -Real.log hP) hPlog n)

/-- The logarithmic box at scale `h`: `h ≤ x_i ≤ h⁻¹` for every coordinate. -/
def ScaleBox {d : ℕ} (h : ℝ) (x : Fin d → ℝ) : Prop :=
  ∀ i, h ≤ x i ∧ x i ≤ h⁻¹

/-- Smaller scales give larger boxes. -/
theorem scaleBox_mono {d : ℕ} {hSmall hBig : ℝ} (hSmallPos : 0 < hSmall)
    (hSmallBig : hSmall ≤ hBig) {x : Fin d → ℝ} :
    ScaleBox hBig x → ScaleBox hSmall x := by
  intro hx i
  have hinv : hBig⁻¹ ≤ hSmall⁻¹ :=
    (inv_le_inv₀ (hSmallPos.trans_le hSmallBig) hSmallPos).2 hSmallBig
  exact ⟨hSmallBig.trans (hx i).1, ((hx i).2).trans hinv⟩

/-- A plateau inside the square-root box at the old scale is inside the next scale's
box whenever the capped schedule has `hNext ≤ sqrt h`. No nesting of plateaux is used. -/
theorem plateau_subset_nextScaleBox {d : ℕ} {h hNext : ℝ}
    (hNextPos : 0 < hNext) (hNextSqrt : hNext ≤ Real.sqrt h)
    {K : Set (Fin d → ℝ)}
    (hK : K ⊆ {x | ScaleBox (Real.sqrt h) x}) :
    K ⊆ {x | ScaleBox hNext x} := by
  intro x hx
  exact scaleBox_mono hNextPos hNextSqrt (hK hx)

/-- Finite scale entry composes without any nesting assumption on the intermediate
plateaux. `P n t` is membership in the `n`th plateau at time `t`; each transition may
use its own (measurable-rate-independent) waiting bound `W n`. -/
theorem finite_absorber_chain {N : ℕ} (W : ℕ → ℝ) (P : ℕ → ℝ → Prop)
    (hbase : P 0 0)
    (hstep : ∀ n < N, ∀ s, P n s →
      ∃ t, s ≤ t ∧ t ≤ s + W n ∧ P (n + 1) t) :
    ∃ t, 0 ≤ t ∧ t ≤ ∑ n ∈ Finset.range N, W n ∧ P N t := by
  induction N with
  | zero =>
      refine ⟨0, le_rfl, ?_, hbase⟩
      simp
  | succ N ih =>
      have hstep' : ∀ n < N, ∀ s, P n s →
          ∃ t, s ≤ t ∧ t ≤ s + W n ∧ P (n + 1) t := by
        intro n hn
        exact hstep n (Nat.lt_trans hn (Nat.lt_succ_self N))
      obtain ⟨s, hs0, hsbound, hsP⟩ := ih hstep'
      obtain ⟨t, hst, htbound, htP⟩ :=
        hstep N (Nat.lt_succ_self N) s hsP
      refine ⟨t, le_trans hs0 hst, ?_, htP⟩
      rw [Finset.sum_range_succ]
      linarith

/-- Conditional common-plateau entry for the capped square-root schedule. The only
dynamical premise is the one-scale entry rule in `hstep`; scale arithmetic and the total
rate-path-independent waiting-time sum are proved here. -/
theorem permanenceScale_absorber_entry {h₀ hP : ℝ} (hhP : 0 < hP)
    (hh₀ : 0 < h₀) (hhP1 : hP < 1) (h₀P : h₀ ≤ hP)
    (W : ℕ → ℝ) (K : ℝ → ℝ → Prop)
    (hbase : K h₀ 0)
    (hstep : ∀ n s, K (permanenceScale h₀ hP n) s →
      ∃ t, s ≤ t ∧ t ≤ s + W n ∧
        K (permanenceScale h₀ hP (n + 1)) t) :
    ∃ N t, permanenceScale h₀ hP N = hP ∧ 0 ≤ t ∧
      t ≤ ∑ n ∈ Finset.range N, W n ∧ K hP t := by
  obtain ⟨N, hcap⟩ := permanenceScale_cap hhP hh₀ hhP1 h₀P
  have hchain : ∀ n < N, ∀ s, K (permanenceScale h₀ hP n) s →
      ∃ t, s ≤ t ∧ t ≤ s + W n ∧
        K (permanenceScale h₀ hP (n + 1)) t := by
    intro n _ s hs
    exact hstep n s hs
  obtain ⟨t, ht0, htbound, htK⟩ :=
    finite_absorber_chain W (fun n t => K (permanenceScale h₀ hP n) t)
      (by simpa [permanenceScale_zero hh₀ h₀P] using hbase) hchain
  exact ⟨N, t, hcap, ht0, htbound, by simpa [hcap] using htK⟩

end N33Dynamics
