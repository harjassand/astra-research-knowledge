import WeightedDrift
import FiniteMinimumCaratheodory
import PlateauPrinciples

import Mathlib.Analysis.SpecialFunctions.Log.Basic

noncomputable section

open MeasureTheory Set

namespace N33Dynamics

open WeightedDrift

variable {d m : ℕ}

/-- Compose the universal full-affine-family theorem with the source's point tolerance and
the finite-family activity-margin theorem. The family and activity cutoff are constructed;
neither is supplied as a new premise to the trajectory interface. -/
theorem exists_affine_family_with_activity (D : ReactionDiagram d m) :
    ∃ F : N33Affine.BoxFamily d (-1) 1, ∃ hAct,
      N33Affine.FamilyLittleOAt F (-1) ∧
      N33Affine.FullApproximation (-1) 1 (pointTolerance D) F.family ∧
      0 < hAct ∧ hAct < 1 ∧ ActivityMargin D F hAct := by
  have hE : ∀ r, N33Affine.InCube (-1) 1 r → 0 < pointTolerance D r :=
    fun r _ => pointTolerance_pos D r
  obtain ⟨F, hLittle, hFull⟩ := N33Affine.exists_full_affine_family
    d (-1) 1 (pointTolerance D) (by norm_num) hE
  obtain ⟨hAct, hActPos, hActLtOne, hActivity⟩ :=
    exists_activity_margin D F hFull
  exact ⟨F, hAct, hLittle, hFull, hActPos, hActLtOne, hActivity⟩

local instance boxFamilyIndexNonempty (F : N33Affine.BoxFamily d (-1) 1) :
    Nonempty F.family.Index := F.family.nonempty

/-- The positive box used by the permanence proof. -/
def ReactionScaleBox (h : ℝ) (x : Vec d) : Prop :=
  ∀ i, h ≤ x i ∧ x i ≤ h⁻¹

/-- The exponent recovered from a positive state at scale `h`. -/
def logCoordinates (h : ℝ) (x : Vec d) : Vec d :=
  fun i => Real.log (x i) / Real.log h

/-- Every state in the positive logarithmic box is exactly a monomial scale point with
exponents in the unit cube. -/
theorem exists_box_log_coordinates {h : ℝ} (hh : 0 < h) (hh1 : h < 1)
    {x : Vec d} (hx : ReactionScaleBox h x) :
    ∃ p, x = scalePoint h p ∧ inExponentBox p := by
  let p := logCoordinates h x
  have hlog : Real.log h < 0 := Real.log_neg hh hh1
  have hxpos : ∀ i, 0 < x i := fun i => lt_of_lt_of_le hh (hx i).1
  have hpow : x = scalePoint h p := by
    funext i
    dsimp [scalePoint, p, logCoordinates]
    rw [Real.rpow_def_of_pos hh]
    have hne : Real.log h ≠ 0 := ne_of_lt hlog
    have hmul : Real.log h * (Real.log (x i) / Real.log h) = Real.log (x i) := by
      field_simp
    rw [hmul, Real.exp_log (hxpos i)]
  have hcube : inExponentBox p := by
    intro i
    dsimp [p, logCoordinates]
    constructor
    · rw [le_div_iff_of_neg hlog]
      have hlogUpper := Real.log_le_log (hxpos i) (hx i).2
      rw [Real.log_inv] at hlogUpper
      simpa using hlogUpper
    · rw [div_le_iff_of_neg hlog]
      simpa using Real.log_le_log hh (hx i).1
  exact ⟨p, hpow, hcube⟩

/-- Affine branches and their lower envelope at one fixed scale. -/
def reactionAffineBranch (F : N33Affine.BoxFamily d (-1) 1) (h : ℝ)
    (j : F.family.Index) (x : Vec d) : ℝ :=
  (F.family.label j).bump h + dot (F.family.label j).slope x

def reactionAffineEnvelope (F : N33Affine.BoxFamily d (-1) 1) (h : ℝ)
    (x : Vec d) : ℝ := by
  letI : Nonempty F.family.Index := F.family.nonempty
  exact Finset.univ.inf' Finset.univ_nonempty (fun j => reactionAffineBranch F h j x)

def reactionAffineCoefficients (F : N33Affine.BoxFamily d (-1) 1) :
    F.family.Index → Fin d → ℝ :=
  fun j i => (F.family.label j).slope i

def reactionAffineOffsets (F : N33Affine.BoxFamily d (-1) 1) (h : ℝ) :
    F.family.Index → ℝ :=
  fun j => (F.family.label j).bump h

def reactionAffineEnvelopeAlong (F : N33Affine.BoxFamily d (-1) 1) (h : ℝ)
    (x : ℝ → Vec d) : ℝ → ℝ := by
  letI : Nonempty F.family.Index := F.family.nonempty
  exact affineMinimumAlong x (reactionAffineCoefficients F) (reactionAffineOffsets F h)

private theorem dot_unitVector (r : Vec d) (i : Fin d) :
    dot r (unitVector i) = r i := by
  unfold dot unitVector
  rw [Fintype.sum_eq_single i]
  · simp
  · intro j hji
    rw [Pi.single_eq_of_ne hji]
    simp

def ReactionBranchActive (F : N33Affine.BoxFamily d (-1) 1) (h : ℝ)
    (j : F.family.Index) (x : Vec d) : Prop :=
  reactionAffineBranch F h j x = reactionAffineEnvelope F h x

@[simp]
theorem reactionAffineBranchAlong_eq {F : N33Affine.BoxFamily d (-1) 1} {h : ℝ}
    {x : ℝ → Vec d} {j : F.family.Index} {t : ℝ} :
    affineBranchAlong x (reactionAffineCoefficients F) (reactionAffineOffsets F h) j t =
      reactionAffineBranch F h j (x t) := by
  letI : Nonempty F.family.Index := F.family.nonempty
  rfl

@[simp]
theorem reactionAffineEnvelopeAlong_eq {F : N33Affine.BoxFamily d (-1) 1} {h : ℝ}
    {x : ℝ → Vec d} {t : ℝ} :
    reactionAffineEnvelopeAlong F h x t = reactionAffineEnvelope F h (x t) := by
  letI : Nonempty F.family.Index := F.family.nonempty
  rfl

private theorem reactionAffineBranch_eq_value_of_scale
    {F : N33Affine.BoxFamily d (-1) 1} {h : ℝ} {p : Vec d}
    (j : F.family.Index) :
    reactionAffineBranch F h j (scalePoint h p) =
      N33Affine.value (F.family.label j) h p := by
  simp [reactionAffineBranch, N33Affine.value, dot, scalePoint]
  <;> ring

/-- Weak activity in the affine envelope is exactly N33's weak activity predicate after
writing the state as `x_i = h^{p_i}`. This equivalence keeps every tied branch. -/
theorem reactionBranchActive_iff_labelActive
    {F : N33Affine.BoxFamily d (-1) 1} {h : ℝ} {p : Vec d}
    {j : F.family.Index} :
    ReactionBranchActive F h j (scalePoint h p) ↔
      N33Affine.Active F.family.label j h p := by
  letI : Nonempty F.family.Index := F.family.nonempty
  constructor
  · intro hj j'
    have hle : reactionAffineEnvelope F h (scalePoint h p) ≤
        reactionAffineBranch F h j' (scalePoint h p) := by
      unfold reactionAffineEnvelope
      exact Finset.inf'_le (f := fun k => reactionAffineBranch F h k (scalePoint h p))
        (Finset.mem_univ j')
    have hbranches : reactionAffineBranch F h j (scalePoint h p) ≤
        reactionAffineBranch F h j' (scalePoint h p) := by
      rw [hj]
      exact hle
    simpa only [reactionAffineBranch_eq_value_of_scale] using hbranches
  · intro hj
    apply le_antisymm
    · apply Finset.le_inf' Finset.univ_nonempty
      intro j' hj'
      have h := hj j'
      simpa only [reactionAffineBranch_eq_value_of_scale] using h
    · unfold reactionAffineEnvelope
      exact Finset.inf'_le (f := fun k => reactionAffineBranch F h k (scalePoint h p))
        (Finset.mem_univ j)
/- The class condition is the orthogonal characterization of membership in the
stoichiometric affine class. It is stated at the exact reaction-span interface consumed by
the proof: every vector orthogonal to every reaction annihilates `x-c`. -/
def ReactionClassOrthogonal (D : ReactionDiagram d m) (c x : Vec d) : Prop :=
  ∀ r, StoichPerp D r → dot r (x - c) = 0

def ReactionPlateau (F : N33Affine.BoxFamily d (-1) 1) (h : ℝ)
    (c x : Vec d) : Prop :=
  reactionAffineEnvelope F h x = reactionAffineEnvelope F h c

/-- Uniform activity prevents a nonzero coordinate of an active slope from being smaller
than the finite comparison margin. -/
theorem active_slope_coordinate_ge_margin
    {D : ReactionDiagram d m} {F : N33Affine.BoxFamily d (-1) 1}
    {hAct h : ℝ} (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    {p : Vec d} (hp : inExponentBox p)
    {j : F.family.Index} (hactive : N33Affine.Active F.family.label j h p)
    (i : Fin d) (hri : (F.family.label j).slope i ≠ 0) :
    slopeMargin D F ≤ |p i| := by
  let z : ComparisonIndex d m := Sum.inl i
  have hz : dot (F.family.label j).slope (comparisonVector D z) ≠ 0 := by
    simpa [z, comparisonVector, dot_unitVector] using hri
  have herr := hActivity h p hh hhAct hp j hactive z hz
  have herr' : |p i - (F.family.label j).slope i| ≤
      |(F.family.label j).slope i| / 2 := by
    simpa [z, comparisonVector, dot_unitVector] using herr
  have hmargin := slopeMargin_le_half_abs D F j z hz
  have hmargin' : slopeMargin D F ≤ |(F.family.label j).slope i| / 2 := by
    simpa [z, comparisonVector, dot_unitVector] using hmargin
  have htriangle : |(F.family.label j).slope i| ≤
      |p i| + |p i - (F.family.label j).slope i| := by
    calc
      |(F.family.label j).slope i| =
          |((F.family.label j).slope i - p i) + p i| := by congr 1 <;> ring
      _ ≤ |(F.family.label j).slope i - p i| + |p i| := abs_add_le _ _
      _ = |p i - (F.family.label j).slope i| + |p i| := by rw [abs_sub_comm]
      _ = |p i| + |p i - (F.family.label j).slope i| := by ring
  linarith

/-- If every exponent coordinate at a representative is smaller than the activity margin,
all active labels there have zero slope. -/
theorem active_slope_eq_zero_at_inner_representative
    {D : ReactionDiagram d m} {F : N33Affine.BoxFamily d (-1) 1}
    {hAct h : ℝ} (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    {p : Vec d} (hp : inExponentBox p)
    (hinner : ∀ i, |p i| < slopeMargin D F)
    {j : F.family.Index} (hactive : N33Affine.Active F.family.label j h p) :
    (F.family.label j).slope = 0 := by
  funext i
  by_contra hri
  have hbound := active_slope_coordinate_ge_margin hActivity hh hhAct hp hactive i hri
  exact (not_le_of_gt (hinner i)) hbound

/-- The finite minimum has a zero-slope active label at an inner representative. -/
theorem exists_zero_active_branch_at_scale
    {D : ReactionDiagram d m} {F : N33Affine.BoxFamily d (-1) 1}
    {hAct h : ℝ} (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    {p : Vec d} (hp : inExponentBox p)
    (hinner : ∀ i, |p i| < slopeMargin D F) :
    ∃ j, ReactionBranchActive F h j (scalePoint h p) ∧
      (F.family.label j).slope = 0 := by
  letI : Nonempty F.family.Index := F.family.nonempty
  obtain ⟨j, -, hj⟩ := Finset.exists_mem_eq_inf'
    (s := Finset.univ) (H := Finset.univ_nonempty)
    (fun i => reactionAffineBranch F h i (scalePoint h p))
  have hbranch : ReactionBranchActive F h j (scalePoint h p) := by
    simpa [ReactionBranchActive, reactionAffineEnvelope] using hj.symm
  have hlabel : N33Affine.Active F.family.label j h p :=
    (reactionBranchActive_iff_labelActive (F := F) (h := h) (p := p) (j := j)).mp hbranch
  have hzero := active_slope_eq_zero_at_inner_representative
    (D := D) hActivity hh hhAct hp hinner hlabel
  exact ⟨j, hbranch, hzero⟩

/-- A zero-slope active branch at `c` is a global ceiling for the envelope. -/
theorem reactionAffineEnvelope_le_representative_of_flat_branch
    {F : N33Affine.BoxFamily d (-1) 1} {h : ℝ} {c : Vec d}
    {j : F.family.Index}
    (hactive : ReactionBranchActive F h j c)
    (hflat : (F.family.label j).slope = 0) :
    ∀ x, reactionAffineEnvelope F h x ≤ reactionAffineEnvelope F h c := by
  letI : Nonempty F.family.Index := F.family.nonempty
  intro x
  have hle : reactionAffineEnvelope F h x ≤ reactionAffineBranch F h j x := by
    unfold reactionAffineEnvelope
    exact Finset.inf'_le (f := fun i => reactionAffineBranch F h i x) (Finset.mem_univ j)
  have hconst : reactionAffineBranch F h j x = reactionAffineBranch F h j c := by
    simp [reactionAffineBranch, hflat, dot]
  exact hle.trans (le_of_eq (hconst.trans hactive))

/-- The activity estimate constructs the source's global envelope ceiling once a positive
representative has all logarithmic coordinates strictly inside the finite margin. -/
theorem reactionAffineEnvelope_le_inner_representative
    {D : ReactionDiagram d m} {F : N33Affine.BoxFamily d (-1) 1}
    {hAct h : ℝ} (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    {p : Vec d} (hp : inExponentBox p)
    (hinner : ∀ i, |p i| < slopeMargin D F)
    {c : Vec d} (hc : c = scalePoint h p) :
    ∀ x, reactionAffineEnvelope F h x ≤ reactionAffineEnvelope F h c := by
  obtain ⟨j, hactive, hflat⟩ := exists_zero_active_branch_at_scale
    (D := D) hActivity hh hhAct hp hinner
  have hactiveC : ReactionBranchActive F h j c := by
    simpa [hc] using hactive
  exact reactionAffineEnvelope_le_representative_of_flat_branch hactiveC hflat

/-- Below the representative's plateau level in the same stoichiometric class, a weakly
active branch cannot have a slope perpendicular to every reaction vector. -/
theorem active_slope_not_perp_below_plateau
    {D : ReactionDiagram d m} {F : N33Affine.BoxFamily d (-1) 1} {h : ℝ}
    {c x : Vec d} {j : F.family.Index}
    (hclass : ReactionClassOrthogonal D c x)
    (hbelow : reactionAffineEnvelope F h x < reactionAffineEnvelope F h c)
    (hactive : ReactionBranchActive F h j x) :
    ¬ StoichPerp D (F.family.label j).slope := by
  letI : Nonempty F.family.Index := F.family.nonempty
  intro hperp
  have hclass' := hclass (F.family.label j).slope hperp
  have hdot := dot_sub_right (F.family.label j).slope x c
  have hsame : dot (F.family.label j).slope x = dot (F.family.label j).slope c := by
    linarith
  have hbranch : reactionAffineBranch F h j x = reactionAffineBranch F h j c := by
    simp [reactionAffineBranch, hsame]
  have hminle : reactionAffineEnvelope F h c ≤ reactionAffineBranch F h j c := by
    unfold reactionAffineEnvelope
    exact Finset.inf'_le (f := fun k => reactionAffineBranch F h k c) (Finset.mem_univ j)
  have hcontra : reactionAffineEnvelope F h c ≤ reactionAffineEnvelope F h x := by
    calc
      reactionAffineEnvelope F h c ≤ reactionAffineBranch F h j c := hminle
      _ = reactionAffineBranch F h j x := hbranch.symm
      _ = reactionAffineEnvelope F h x := hactive
  exact (not_lt_of_ge hcontra hbelow)

def reactionDriftMargin (D : ReactionDiagram d m)
    (F : N33Affine.BoxFamily d (-1) 1) (h κ : ℝ) : ℝ :=
  κ * slopeMargin D F * Real.rpow h (sourceBudget D)

/-- A finite explicit lower bound for the affine envelope throughout the logarithmic box. -/
def reactionAffineFloor (F : N33Affine.BoxFamily d (-1) 1) (h : ℝ) : ℝ := by
  letI : Nonempty F.family.Index := F.family.nonempty
  exact Finset.univ.inf' Finset.univ_nonempty (fun j =>
    (F.family.label j).bump h - l1 (F.family.label j).slope * h⁻¹)

/-- The source-shaped finite-entry horizon, using the explicit box floor. -/
def reactionEntryHorizon (D : ReactionDiagram d m)
    (F : N33Affine.BoxFamily d (-1) 1) (h κ a : ℝ) (c : Vec d) : ℝ :=
  a + (reactionAffineEnvelope F h c - reactionAffineFloor F h) /
    reactionDriftMargin D F h κ

private theorem reactionAffineBranch_ge_local_floor
    {F : N33Affine.BoxFamily d (-1) 1} {h : ℝ}
    (hh : 0 < h) {x : Vec d} (hx : ReactionScaleBox h x)
    (j : F.family.Index) :
    (F.family.label j).bump h - l1 (F.family.label j).slope * h⁻¹ ≤
      reactionAffineBranch F h j x := by
  have hterm : ∀ i : Fin d,
      -|(F.family.label j).slope i| * h⁻¹ ≤
        (F.family.label j).slope i * x i := by
    intro i
    have hxi : 0 ≤ x i := le_of_lt (lt_of_lt_of_le hh (hx i).1)
    calc
      -|(F.family.label j).slope i| * h⁻¹ ≤
          -|(F.family.label j).slope i| * x i :=
        mul_le_mul_of_nonpos_left (hx i).2
          (neg_nonpos.mpr (abs_nonneg _))
      _ ≤ (F.family.label j).slope i * x i :=
        mul_le_mul_of_nonneg_right (neg_abs_le _) hxi
  have hsum := Finset.sum_le_sum (s := (Finset.univ : Finset (Fin d)))
    (fun i hi => hterm i)
  have hsumEq : (∑ i, -|(F.family.label j).slope i| * h⁻¹) =
      -l1 (F.family.label j).slope * h⁻¹ := by
    unfold l1
    rw [← Finset.sum_mul]
    simp [Finset.sum_neg_distrib]
  have hdot : -l1 (F.family.label j).slope * h⁻¹ ≤
      dot (F.family.label j).slope x := by
    rw [← hsumEq]
    simpa only [dot] using hsum
  unfold reactionAffineBranch
  linarith

/-- The explicit finite floor lies below the actual affine lower envelope on its box. -/
theorem reactionAffineFloor_le_envelope_on_box
    {F : N33Affine.BoxFamily d (-1) 1} {h : ℝ}
    (hh : 0 < h) {x : Vec d} (hx : ReactionScaleBox h x) :
    reactionAffineFloor F h ≤ reactionAffineEnvelope F h x := by
  letI : Nonempty F.family.Index := F.family.nonempty
  apply Finset.le_inf' Finset.univ_nonempty
  intro j hj
  have hfloor : reactionAffineFloor F h ≤
      (F.family.label j).bump h - l1 (F.family.label j).slope * h⁻¹ := by
    unfold reactionAffineFloor
    exact Finset.inf'_le
      (f := fun k => (F.family.label k).bump h - l1 (F.family.label k).slope * h⁻¹)
      (Finset.mem_univ j)
  exact hfloor.trans (reactionAffineBranch_ge_local_floor hh hx j)

/-- The pointwise strict weighted-drift theorem expressed directly for an active branch of
the affine lower envelope at a state in the positive scale box. -/
theorem active_branch_reaction_drift_ge_margin
    {D : ReactionDiagram d m} (hEndo : AllEndotactic D)
    {F : N33Affine.BoxFamily d (-1) 1} {hAct h : ℝ}
    (hActLtOne : hAct < 1) (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    {x : Vec d} (hxbox : ReactionScaleBox h x)
    {j : F.family.Index} (hactive : ReactionBranchActive F h j x)
    (κ K : ℝ) (hκ : 0 < κ) (hκK : κ ≤ K)
    (k : Fin m → ℝ) (hk : ∀ e, κ ≤ k e ∧ k e ≤ K)
    (hsmall : K * reactionBudget D * Real.rpow h (slopeMargin D F) ≤
      κ * slopeMargin D F)
    (hnotPerp : ¬ StoichPerp D (F.family.label j).slope) :
    reactionDriftMargin D F h κ ≤
      dot (F.family.label j).slope (reactionField D k x) := by
  obtain ⟨p, hxp, hp⟩ := exists_box_log_coordinates hh
    (lt_trans hhAct hActLtOne) hxbox
  have hactiveScale : ReactionBranchActive F h j (scalePoint h p) := by
    simpa [hxp] using hactive
  have hlabel := (reactionBranchActive_iff_labelActive (F := F) (h := h)
    (p := p) (j := j)).mp hactiveScale
  simpa [reactionDriftMargin, hxp] using
    (weighted_drift_strict D hEndo F hAct hActLtOne hActivity h hh hhAct p hp j hlabel
      κ K hκ hκK k hk hsmall hnotPerp)

/-- Every active branch has nonnegative directional drift in the box. Perpendicular
slopes contribute exactly zero; all other slopes use the strict estimate. -/
theorem active_branch_reaction_drift_nonneg
    {D : ReactionDiagram d m} (hEndo : AllEndotactic D)
    {F : N33Affine.BoxFamily d (-1) 1} {hAct h : ℝ}
    (hActLtOne : hAct < 1) (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    {x : Vec d} (hxbox : ReactionScaleBox h x)
    {j : F.family.Index} (hactive : ReactionBranchActive F h j x)
    (κ K : ℝ) (hκ : 0 < κ) (hκK : κ ≤ K)
    (k : Fin m → ℝ) (hk : ∀ e, κ ≤ k e ∧ k e ≤ K)
    (hsmall : K * reactionBudget D * Real.rpow h (slopeMargin D F) ≤
      κ * slopeMargin D F) :
    0 ≤ dot (F.family.label j).slope (reactionField D k x) := by
  by_cases hperp : StoichPerp D (F.family.label j).slope
  · exact projected_drift_nonneg_of_perp D _ k x hperp
  · have hstrict := active_branch_reaction_drift_ge_margin hEndo hActLtOne
      hActivity hh hhAct hxbox hactive κ K hκ hκK k hk hsmall hperp
    have hmargin : 0 ≤ reactionDriftMargin D F h κ := by
      unfold reactionDriftMargin
      exact mul_nonneg (mul_nonneg hκ.le (slopeMargin_pos D F).le)
        (Real.rpow_nonneg (le_of_lt hh) _)
    exact hmargin.trans hstrict

private theorem affineSlopeDerivative_eq_dot
    {F : N33Affine.BoxFamily d (-1) 1} {x : ℝ → Vec d} {t : ℝ}
    (j : F.family.Index) :
    (∑ i, (F.family.label j).slope i * deriv (fun u => x u i) t) =
      dot (F.family.label j).slope (fun i => deriv (fun u => x u i) t) := rfl

private theorem dot_derivative_eq_dot_field
    {D : ReactionDiagram d m} {x : ℝ → Vec d} {t : ℝ}
    {k : Fin m → ℝ} (r : Vec d)
    (hODE : ∀ i, deriv (fun u => x u i) t = reactionField D k (x t) i) :
    dot r (fun i => deriv (fun u => x u i) t) =
      dot r (reactionField D k (x t)) := by
  unfold dot
  apply Finset.sum_congr rfl
  intro i hi
  simp [hODE i]

/-- The local weighted-drift estimate now composes with the actual a.e. chain rule for the
finite affine minimum along an absolutely continuous reaction trajectory. This statement is
conditional on the explicit ODE identity and pointwise box/class facts; it does not assume a
global solution theorem. -/
theorem reactionEnvelope_derivative_nonneg_ae
    {D : ReactionDiagram d m} (hEndo : AllEndotactic D)
    {F : N33Affine.BoxFamily d (-1) 1} {hAct h κ K a b : ℝ}
    (hActLtOne : hAct < 1) (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    (hκ : 0 < κ) (hκK : κ ≤ K)
    (hsmall : K * reactionBudget D * Real.rpow h (slopeMargin D F) ≤
      κ * slopeMargin D F)
    (x : ℝ → Vec d) (hx : AbsolutelyContinuousOnInterval x a b)
    (hbox : ∀ t, t ∈ uIcc a b → ReactionScaleBox h (x t))
    (k : ℝ → Fin m → ℝ)
    (hk : ∀ᵐ t : ℝ, t ∈ uIcc a b → ∀ e, κ ≤ k t e ∧ k t e ≤ K)
    (hODE : ∀ᵐ t : ℝ, t ∈ uIcc a b → ∀ i,
      deriv (fun u => x u i) t = reactionField D (k t) (x t) i) :
    ∀ᵐ t : ℝ, t ∈ uIcc a b →
      0 ≤ deriv (reactionAffineEnvelopeAlong F h x) t := by
  letI : Nonempty F.family.Index := F.family.nonempty
  apply affineMinimumAlong_ae_drift_lower_bound hx
    (reactionAffineCoefficients F) (reactionAffineOffsets F h)
  filter_upwards [hk, hODE] with t hkt hODEt
  intro ht j hj
  have hactive : ReactionBranchActive F h j (x t) := by
    simpa only [reactionAffineBranchAlong_eq, reactionAffineEnvelopeAlong_eq] using hj
  have hflux := active_branch_reaction_drift_nonneg hEndo hActLtOne hActivity
    hh hhAct (hbox t ht) hactive κ K hκ hκK (k t) (hkt ht) hsmall
  have hdot := dot_derivative_eq_dot_field (D := D) (x := x) (t := t)
    (k := k t) (F.family.label j).slope (hODEt ht)
  simpa only [affineSlopeDerivative_eq_dot] using hflux.trans_eq hdot.symm

/-- Below the representative level within the same reaction class, every active branch has
the uniform positive derivative margin. All weak ties are included. -/
theorem reactionEnvelope_derivative_ge_margin_below_ae
    {D : ReactionDiagram d m} (hEndo : AllEndotactic D)
    {F : N33Affine.BoxFamily d (-1) 1} {hAct h κ K a b : ℝ}
    (hActLtOne : hAct < 1) (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    (hκ : 0 < κ) (hκK : κ ≤ K)
    (hsmall : K * reactionBudget D * Real.rpow h (slopeMargin D F) ≤
      κ * slopeMargin D F)
    (x : ℝ → Vec d) (hx : AbsolutelyContinuousOnInterval x a b)
    (c : Vec d)
    (hbox : ∀ t, t ∈ uIcc a b → ReactionScaleBox h (x t))
    (hclass : ∀ t, t ∈ uIcc a b → ReactionClassOrthogonal D c (x t))
    (k : ℝ → Fin m → ℝ)
    (hk : ∀ᵐ t : ℝ, t ∈ uIcc a b → ∀ e, κ ≤ k t e ∧ k t e ≤ K)
    (hODE : ∀ᵐ t : ℝ, t ∈ uIcc a b → ∀ i,
      deriv (fun u => x u i) t = reactionField D (k t) (x t) i) :
    ∀ᵐ t : ℝ, t ∈ uIcc a b →
      reactionAffineEnvelope F h (x t) < reactionAffineEnvelope F h c →
      reactionDriftMargin D F h κ ≤ deriv (reactionAffineEnvelopeAlong F h x) t := by
  letI : Nonempty F.family.Index := F.family.nonempty
  have hchain := affineMinimumAlong_ae_active_derivative_eq hx
    (reactionAffineCoefficients F) (reactionAffineOffsets F h)
  filter_upwards [hchain, hk, hODE] with t hchainT hkt hODEt
  intro ht hbelow
  obtain ⟨j, -, hj⟩ := Finset.exists_mem_eq_inf'
    (s := Finset.univ) (H := Finset.univ_nonempty)
    (fun i => affineBranchAlong x (reactionAffineCoefficients F)
      (reactionAffineOffsets F h) i t)
  have hj' : affineBranchAlong x (reactionAffineCoefficients F)
      (reactionAffineOffsets F h) j t =
      affineMinimumAlong x (reactionAffineCoefficients F)
        (reactionAffineOffsets F h) t := by
    simpa [affineMinimumAlong] using hj.symm
  have hactive : ReactionBranchActive F h j (x t) := by
    simpa only [reactionAffineBranchAlong_eq, reactionAffineEnvelopeAlong_eq] using hj'
  have hnotPerp := active_slope_not_perp_below_plateau
    (hclass t ht) hbelow hactive
  have hflux := active_branch_reaction_drift_ge_margin hEndo hActLtOne
    hActivity hh hhAct (hbox t ht) hactive κ K hκ hκK (k t) (hkt ht)
    hsmall hnotPerp
  have hdot := dot_derivative_eq_dot_field (D := D) (x := x) (t := t)
    (k := k t) (F.family.label j).slope (hODEt ht)
  have hpath : reactionDriftMargin D F h κ ≤
      dot (F.family.label j).slope (fun i => deriv (fun u => x u i) t) := by
    calc
      reactionDriftMargin D F h κ ≤
          dot (F.family.label j).slope (reactionField D (k t) (x t)) := hflux
      _ = dot (F.family.label j).slope (fun i => deriv (fun u => x u i) t) := hdot.symm
  have hbranch : reactionDriftMargin D F h κ ≤
      ∑ i, (F.family.label j).slope i * deriv (fun u => x u i) t := by
    simpa only [affineSlopeDerivative_eq_dot] using hpath
  exact hbranch.trans_eq (hchainT ht j hj')

/-- One-scale finite entry for an actual absolutely continuous reaction trajectory. It derives
the positive lower-envelope derivative from weighted endotactic drift and the weak-active
finite-minimum chain rule, then integrates it up to the explicit floor-to-ceiling time. -/
theorem reactionEnvelope_enters_plateau_by_range
    {D : ReactionDiagram d m} (hEndo : AllEndotactic D)
    {F : N33Affine.BoxFamily d (-1) 1} {hAct h κ K a : ℝ}
    (hActLtOne : hAct < 1) (hActivity : ActivityMargin D F hAct)
    (hh : 0 < h) (hhAct : h < hAct)
    (hκ : 0 < κ) (hκK : κ ≤ K)
    (hsmall : K * reactionBudget D * Real.rpow h (slopeMargin D F) ≤
      κ * slopeMargin D F)
    (c : Vec d) (hcbox : ReactionScaleBox h c)
    (hupper : ∀ y, reactionAffineEnvelope F h y ≤ reactionAffineEnvelope F h c)
    (x : ℝ → Vec d)
    (hx : AbsolutelyContinuousOnInterval x a (reactionEntryHorizon D F h κ a c))
    (hbox : ∀ t, t ∈ uIcc a (reactionEntryHorizon D F h κ a c) →
      ReactionScaleBox h (x t))
    (hclass : ∀ t, t ∈ uIcc a (reactionEntryHorizon D F h κ a c) →
      ReactionClassOrthogonal D c (x t))
    (k : ℝ → Fin m → ℝ)
    (hk : ∀ᵐ t : ℝ, t ∈ uIcc a (reactionEntryHorizon D F h κ a c) →
      ∀ e, κ ≤ k t e ∧ k t e ≤ K)
    (hODE : ∀ᵐ t : ℝ, t ∈ uIcc a (reactionEntryHorizon D F h κ a c) →
      ∀ i, deriv (fun u => x u i) t = reactionField D (k t) (x t) i) :
    ∃ t, t ∈ Icc a (reactionEntryHorizon D F h κ a c) ∧
      ReactionPlateau F h c (x t) := by
  let M := reactionAffineEnvelope F h c
  let m₀ := reactionAffineFloor F h
  let δ := reactionDriftMargin D F h κ
  let T := reactionEntryHorizon D F h κ a c
  have hδ : 0 < δ := by
    dsimp [δ, reactionDriftMargin]
    exact mul_pos (mul_pos hκ (slopeMargin_pos D F))
      (Real.rpow_pos_of_pos hh _)
  have hfloorM : m₀ ≤ M := by
    dsimp [m₀, M]
    exact reactionAffineFloor_le_envelope_on_box hh hcbox
  have hab : a ≤ T := by
    dsimp [T, reactionEntryHorizon, M, m₀, δ]
    have hnonneg : 0 ≤
        (reactionAffineEnvelope F h c - reactionAffineFloor F h) /
          reactionDriftMargin D F h κ :=
      div_nonneg (sub_nonneg.mpr hfloorM) hδ.le
    linarith
  have hstartMem : a ∈ uIcc a T := by
    rw [uIcc_of_le hab]
    exact ⟨le_rfl, hab⟩
  have hmin : m₀ ≤ reactionAffineEnvelopeAlong F h x a := by
    have hpoint := reactionAffineFloor_le_envelope_on_box (F := F) hh (hbox a hstartMem)
    simpa only [reactionAffineEnvelopeAlong_eq] using hpoint
  have hmax : reactionAffineEnvelopeAlong F h x a ≤ M := by
    simpa only [reactionAffineEnvelopeAlong_eq, M] using hupper (x a)
  have hbarrierAC : AbsolutelyContinuousOnInterval
      (reactionAffineEnvelopeAlong F h x) a T := by
    simpa [T, reactionEntryHorizon, reactionAffineEnvelopeAlong] using
      affineMinimumAlong_absolutelyContinuous hx
        (reactionAffineCoefficients F) (reactionAffineOffsets F h)
  have hderivBelowRaw := reactionEnvelope_derivative_ge_margin_below_ae
    hEndo hActLtOne hActivity hh hhAct hκ hκK hsmall x hx c hbox hclass k hk hODE
  have hderivBelow : ∀ᵐ t ∂volume, t ∈ Icc a T →
      reactionAffineEnvelopeAlong F h x t < M → δ ≤
        deriv (reactionAffineEnvelopeAlong F h x) t := by
    filter_upwards [hderivBelowRaw] with t hraw
    intro ht hbelow
    have ht' : t ∈ uIcc a T := by
      simpa [T, uIcc_of_le hab] using ht
    have hbelow' : reactionAffineEnvelope F h (x t) <
        reactionAffineEnvelope F h c := by
      simpa [reactionAffineEnvelopeAlong_eq, M] using hbelow
    simpa [δ] using hraw ht' hbelow'
  have hhit := absolutelyContinuous_hits_level_by_range
    (a := a) (m := m₀) (M := M) (δ := δ)
    (by simpa [T, reactionEntryHorizon, M, m₀, δ] using hbarrierAC)
    hδ hmin hmax (by simpa [T, M, δ] using hderivBelow)
  obtain ⟨t, ht, hlevel⟩ := hhit
  have hupperT : reactionAffineEnvelopeAlong F h x t ≤ M := by
    simpa only [reactionAffineEnvelopeAlong_eq, M] using hupper (x t)
  refine ⟨t, ?_, ?_⟩
  · simpa [T] using ht
  · unfold ReactionPlateau
    exact le_antisymm (by simpa [M] using hupperT) (by simpa [T, M] using hlevel)


end N33Dynamics
