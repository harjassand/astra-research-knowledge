import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Pow.Continuity
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import N33Affine.AffineCore
import N33Affine.SliceFamily
import N33Affine.NextTypeAsymptotic
import N33Affine.B2Mechanism

noncomputable section

open Filter Topology Set
open scoped BigOperators

namespace N33Affine.GluePlacement

variable {N m : ℕ}

def shiftPrefix (q : ℕ → ℝ) (j : Fin N) (h : ℝ) : ℝ :=
  ∑ k ∈ Finset.range j.val, Real.rpow h (q k)

def shiftedLabel (families : Fin N → FiniteFamily m) (q : ℕ → ℝ)
    (j : Fin N) (k : (families j).Index) : Label m :=
  ⟨(families j).label k |>.slope,
    fun h => ((families j).label k).bump h - shiftPrefix q j h⟩

noncomputable def shiftedUnion (families : Fin N → FiniteFamily m)
    (q : ℕ → ℝ) (hN : 0 < N) : FiniteFamily m := by
  classical
  letI : Fintype (Σ j : Fin N, (families j).Index) := inferInstance
  refine ⟨Σ j : Fin N, (families j).Index, inferInstance, ?_,
    fun x => shiftedLabel families q x.1 x.2⟩
  let j : Fin N := ⟨0, hN⟩
  obtain ⟨k⟩ := (families j).nonempty
  exact ⟨⟨j, k⟩⟩

lemma value_shiftedLabel (families : Fin N → FiniteFamily m)
    (q : ℕ → ℝ) (j : Fin N) (k : (families j).Index)
    (h : ℝ) (p : Fin m → ℝ) :
    value (shiftedLabel families q j k) h p =
      value ((families j).label k) h p - shiftPrefix q j h := by
  simp [value, shiftedLabel, shiftPrefix]
  ring

lemma value_sub_baseline {m : ℕ} (ℓ : Label m) (c h : ℝ)
    (p : Fin m → ℝ) :
    value ℓ h p - value (baselineLabel c) h p =
      (∑ i : Fin m, (ℓ.slope i - c) * Real.rpow h (p i)) + ℓ.bump h := by
  unfold value
  simp only [baselineLabel]
  have hsub :
      (∑ i : Fin m, ℓ.slope i * Real.rpow h (p i)) -
          (∑ i : Fin m, c * Real.rpow h (p i)) =
        ∑ i : Fin m, (ℓ.slope i - c) * Real.rpow h (p i) := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  linear_combination hsub

private lemma finset_sum_mul_div {ι : Type*} [Fintype ι]
    (a b : ι → ℝ) (d : ℝ) :
    (∑ i, a i * b i) / d = ∑ i, a i * (b i / d) := by
  classical
  rw [div_eq_mul_inv, Finset.sum_mul]
  apply Finset.sum_congr rfl
  intro i hi
  ring

lemma shiftPrefix_succ (q : ℕ → ℝ) (k : ℕ) (hk : k + 1 < N) (h : ℝ) :
    shiftPrefix q ⟨k + 1, hk⟩ h =
      shiftPrefix q ⟨k, Nat.lt_trans (Nat.lt_succ_self k) hk⟩ h +
        Real.rpow h (q k) := by
  simp [shiftPrefix, Finset.sum_range_succ]

lemma shifted_value_sub_baseline
    (families : Fin N → FiniteFamily m) (q : ℕ → ℝ)
    (j jbase : Fin N) (k : (families j).Index)
    (kbase : (families jbase).Index) (h : ℝ) (p : Fin m → ℝ)
    (c δ : ℝ)
    (hbase : (families jbase).label kbase = baselineLabel c)
    (hprefix : shiftPrefix q jbase h = shiftPrefix q j h + δ) :
    value (shiftedLabel families q j k) h p -
        value (shiftedLabel families q jbase kbase) h p =
      (∑ i : Fin m, (((families j).label k).slope i - c) *
        Real.rpow h (p i)) + ((families j).label k).bump h + δ := by
  rw [value_shiftedLabel, value_shiftedLabel, hbase]
  have hv := value_sub_baseline ((families j).label k) c h p
  rw [hprefix]
  linear_combination hv

def slabLower (a : ℝ) (q : ℕ → ℝ) (j : Fin N) : ℝ :=
  if j.val = 0 then a else q (j.val - 1)

def slabUpper (b : ℝ) (q : ℕ → ℝ) (j : Fin N) : ℝ :=
  if j.val + 1 < N then q j.val else b

/-- Global weak activity pins the limiting minimum into the selected tag's
closed cut slab. The strict-side contradictions use varying real exponents,
arbitrary finite slopes, and only local little-o offsets. -/
theorem active_minimum_in_slab
    (a b : ℝ) (hN : 0 < N)
    (centers gamma : Fin N → ℝ)
    (families : Fin N → FiniteFamily m)
    (q : ℕ → ℝ)
    (hcenterBox : ∀ j, a ≤ centers j ∧ centers j ≤ b)
    (hcenterGamma : ∀ j, centers j < gamma j)
    (hcuts : ∀ k (hk : k + 1 < N),
      centers ⟨k, by omega⟩ < q k ∧
      q k < centers ⟨k + 1, hk⟩ ∧
      q k < gamma ⟨k, by omega⟩)
    (hfloor : ∀ j k i, centers j ≤ ((families j).label k).slope i)
    (hbumps : ∀ j k, LittleO ((families j).label k).bump (gamma j))
    (hbase : ∀ j, ∃ k, (families j).label k = baselineLabel (centers j))
    (j : Fin N) (k : (families j).Index)
    (hSeq : ℕ → ℝ) (pSeq : ℕ → Fin m → ℝ) (p : Fin m → ℝ) (s : ℝ)
    (hh : Tendsto hSeq atTop (nhdsWithin 0 (Ioi 0)))
    (hp : Tendsto pSeq atTop (nhds p))
    (hpCube : InCube a b p) (hslice : AtMinSlice p s)
    (hactive : ∀ᶠ n in atTop,
      Active (shiftedUnion families q hN).label ⟨j, k⟩ (hSeq n) (pSeq n)) :
    slabLower a q j ≤ s ∧ s ≤ slabUpper b q j := by
  classical
  have has : a ≤ s := by
    obtain ⟨i, hi⟩ := hslice.2
    have := (hpCube i).1
    calc
      a ≤ p i := this
      _ = s := hi
  have hsb : s ≤ b := by
    obtain ⟨i, hi⟩ := hslice.2
    have := (hpCube i).2
    calc
      s = p i := hi.symm
      _ ≤ b := this
  obtain ⟨kb, hbaseEq⟩ := hbase j
  have hlo : slabLower a q j ≤ s := by
    by_cases hj : j.val = 0
    · simpa [slabLower, hj] using has
    · let jp : Fin N := ⟨j.val - 1, by omega⟩
      by_contra hnot
      have hnot' : ¬ q (j.val - 1) ≤ s := by
        simpa [slabLower, hj] using hnot
      have hslt : s < q (j.val - 1) := lt_of_not_ge hnot'
      obtain ⟨kbp, hbasep⟩ := hbase jp
      have hactivePrev : ∀ᶠ n in atTop,
          value (shiftedLabel families q j k) (hSeq n) (pSeq n) ≤
            value (shiftedLabel families q jp kbp) (hSeq n) (pSeq n) := by
        filter_upwards [hactive] with n hn
        exact hn ⟨jp, kbp⟩
      obtain ⟨i0, hi0⟩ := hslice.2
      have hpcoord : Tendsto (fun n => pSeq n i0) atTop (nhds (p i0)) := by
        simpa using ((continuous_apply i0).tendsto p).comp hp
      have hprevBound : j.val - 1 + 1 < N := by omega
      have hjFin : (⟨j.val - 1 + 1, hprevBound⟩ : Fin N) = j :=
        Fin.ext (Nat.sub_add_cancel (Nat.one_le_iff_ne_zero.mpr hj))
      have hcenterPrev : centers jp < centers j := by
        calc
          centers jp < q (j.val - 1) := by
            simpa [jp] using (hcuts (j.val - 1) (by omega)).1
          _ < centers j := by
            simpa [hjFin] using (hcuts (j.val - 1) (by omega)).2.1
      have hqcenter : q (j.val - 1) < centers j := by
        simpa [hjFin] using (hcuts (j.val - 1) (by omega)).2.1
      have hc : 0 < ((families j).label k).slope i0 - centers jp := by
        linarith [hfloor j k i0]
      have hbumplittle : LittleO ((families j).label k).bump (q (j.val - 1)) := by
        exact littleO_lower_exponent (hbumps j k)
          (lt_trans hqcenter (hcenterGamma j))
      have hnotEventual := no_eventually_littleO_competition hh hpcoord
        (by simpa [hi0] using hslt) hc hbumplittle
      apply hnotEventual
      have hpos : ∀ᶠ n in atTop, 0 < hSeq n := by
        exact hh.eventually
          (show ∀ᶠ x in nhdsWithin 0 (Ioi 0), 0 < x from self_mem_nhdsWithin)
      filter_upwards [hactivePrev, hpos] with n hle hn
      have hpref : shiftPrefix q jp (hSeq n) =
          shiftPrefix q j (hSeq n) + -Real.rpow (hSeq n) (q (j.val - 1)) := by
        have hsucc := shiftPrefix_succ q (j.val - 1) hprevBound (hSeq n)
        have hsucc' : shiftPrefix q j (hSeq n) =
            shiftPrefix q jp (hSeq n) + Real.rpow (hSeq n) (q (j.val - 1)) := by
          rw [← hjFin]
          simpa [jp] using hsucc
        linarith
      have hdiff := shifted_value_sub_baseline families q j jp k kbp
        (hSeq n) (pSeq n) (centers jp)
        (-Real.rpow (hSeq n) (q (j.val - 1))) hbasep hpref
      have hsum : 0 ≤ ∑ i : Fin m,
          (((families j).label k).slope i - centers jp) *
            Real.rpow (hSeq n) (pSeq n i) := by
        apply Finset.sum_nonneg
        intro i hi
        apply mul_nonneg
        · linarith [hfloor j k i]
        · exact (Real.rpow_pos_of_pos hn _).le
      have hsingle := Finset.single_le_sum
        (f := fun i : Fin m =>
          (((families j).label k).slope i - centers jp) *
            Real.rpow (hSeq n) (pSeq n i))
        (fun i _ => mul_nonneg
          (sub_nonneg.mpr (le_of_lt (by linarith [hcenterPrev, hfloor j k i])))
          (Real.rpow_pos_of_pos hn _).le)
        (Finset.mem_univ i0)
      have hle0 :
          (∑ i : Fin m,
            (((families j).label k).slope i - centers jp) *
              Real.rpow (hSeq n) (pSeq n i)) +
            ((families j).label k).bump (hSeq n) -
              Real.rpow (hSeq n) (q (j.val - 1)) ≤ 0 := by
        have hle' := sub_nonpos.mpr hle
        rw [hdiff] at hle'
        exact hle'
      have hbad :
          (((families j).label k).slope i0 - centers jp) *
              Real.rpow (hSeq n) (pSeq n i0) +
            ((families j).label k).bump (hSeq n) ≤
              Real.rpow (hSeq n) (q (j.val - 1)) := by
        linarith [hsingle, hle0]
      exact hbad

  have hhi : s ≤ slabUpper b q j := by
    by_cases hj : j.val + 1 < N
    · let jn : Fin N := ⟨j.val + 1, hj⟩
      have hqgamma : q j.val < gamma j := (hcuts j.val hj).2.2
      have hbumplittle : LittleO ((families j).label k).bump (q j.val) :=
        littleO_lower_exponent (hbumps j k) hqgamma
      obtain ⟨kbn, hbasen⟩ := hbase jn
      have hactiveNext : ∀ᶠ n in atTop,
          value (shiftedLabel families q j k) (hSeq n) (pSeq n) ≤
            value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n) := by
        filter_upwards [hactive] with n hn
        exact hn ⟨jn, kbn⟩
      by_contra hnot
      have hnot' : ¬ s ≤ q j.val := by
        simpa [slabUpper, hj] using hnot
      have hqmin : q j.val < s := lt_of_not_ge hnot'
      have hpcoord : ∀ i : Fin m, Tendsto (fun n => pSeq n i) atTop (nhds (p i)) := by
        intro i
        exact ((continuous_apply i).tendsto p).comp hp
      have hsmall := NextTypeAsymptotic.finite_rpow_sum_add_littleO_tendsto_zero
        (h := hSeq) (q := q j.val) (p := fun i n => pSeq n i)
        (p₀ := p) (c := fun i => ((families j).label k).slope i - centers jn)
        (d := ((families j).label k).bump)
        hh hpcoord (fun i => lt_of_lt_of_le hqmin (hslice.1 i)) hbumplittle
      have hnormalized : Tendsto
          (fun n =>
            (value (shiftedLabel families q j k) (hSeq n) (pSeq n) -
              value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n)) /
                Real.rpow (hSeq n) (q j.val)) atTop (nhds 1) := by
        have hpos : ∀ᶠ n in atTop, 0 < hSeq n := by
          exact hh.eventually
            (show ∀ᶠ x in nhdsWithin 0 (Ioi 0), 0 < x from self_mem_nhdsWithin)
        have heq : (fun n =>
            (value (shiftedLabel families q j k) (hSeq n) (pSeq n) -
              value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n)) /
                Real.rpow (hSeq n) (q j.val)) =ᶠ[atTop]
            (fun n =>
              (∑ i : Fin m,
                (((families j).label k).slope i - centers jn) *
                  (Real.rpow (hSeq n) (pSeq n i) /
                    Real.rpow (hSeq n) (q j.val))) +
                ((families j).label k).bump (hSeq n) /
                  Real.rpow (hSeq n) (q j.val) + 1) := by
          filter_upwards [hpos] with n hn
          have hpref := shiftPrefix_succ q j.val hj (hSeq n)
          have hdiff := shifted_value_sub_baseline families q j jn k kbn
            (hSeq n) (pSeq n) (centers jn) (Real.rpow (hSeq n) (q j.val))
            hbasen (by simpa [jn] using hpref)
          rw [hdiff]
          have hden : Real.rpow (hSeq n) (q j.val) ≠ 0 :=
            (Real.rpow_pos_of_pos hn _).ne'
          rw [add_div, add_div, finset_sum_mul_div]
          have hrpow : Real.rpow (hSeq n) (q j.val) /
              Real.rpow (hSeq n) (q j.val) = 1 := div_self hden
          rw [hrpow]
        have h := hsmall.add_const (1 : ℝ)
        have h' := h.congr' heq.symm
        simpa using h'
      have hposhalf : ∀ᶠ n in atTop,
          (1 : ℝ) / 2 <
            (value (shiftedLabel families q j k) (hSeq n) (pSeq n) -
              value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n)) /
                Real.rpow (hSeq n) (q j.val) :=
        (tendsto_order.1 hnormalized).1 (1 / 2) (by norm_num)
      have hbad : ∀ᶠ n in atTop,
          value (shiftedLabel families q j k) (hSeq n) (pSeq n) -
            value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n) ≤ 0 := by
        filter_upwards [hactiveNext] with n hn
        exact sub_nonpos.mpr hn
      have hposSeq : ∀ᶠ n in atTop, 0 < hSeq n := by
        exact hh.eventually
          (show ∀ᶠ x in nhdsWithin 0 (Ioi 0), 0 < x from self_mem_nhdsWithin)
      obtain ⟨n, ⟨hposn, hbadn⟩, hposh⟩ := ((hposhalf.and hbad).and hposSeq).exists
      have hden : 0 < Real.rpow (hSeq n) (q j.val) :=
        Real.rpow_pos_of_pos hposh _
      have hfrac : 0 <
          (value (shiftedLabel families q j k) (hSeq n) (pSeq n) -
            value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n)) /
              Real.rpow (hSeq n) (q j.val) := by linarith
      have hdeq :
          (value (shiftedLabel families q j k) (hSeq n) (pSeq n) -
            value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n)) =
          ((value (shiftedLabel families q j k) (hSeq n) (pSeq n) -
            value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n)) /
              Real.rpow (hSeq n) (q j.val)) * Real.rpow (hSeq n) (q j.val) := by
        field_simp [ne_of_gt hden]
      have hposDiff : 0 <
          value (shiftedLabel families q j k) (hSeq n) (pSeq n) -
            value (shiftedLabel families q jn kbn) (hSeq n) (pSeq n) := by
        rw [hdeq]
        exact mul_pos hfrac hden
      exact (not_le_of_gt hposDiff) hbadn
    · simpa [slabUpper, hj] using hsb
  exact ⟨hlo, hhi⟩

end N33Affine.GluePlacement
