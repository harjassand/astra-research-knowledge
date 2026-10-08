import Mathlib.Analysis.Calculus.LocalExtr.Basic

noncomputable section

open Filter Topology

namespace N33Dynamics

/-- The pointwise minimum of a nonempty finite family of real-valued functions. -/
def finiteMinimum {ι : Type*} [Fintype ι] [Nonempty ι] (f : ι → ℝ → ℝ) : ℝ → ℝ :=
  fun x => Finset.univ.inf' Finset.univ_nonempty (fun i => f i x)

/-- If `g` is a pointwise lower envelope of a family, then at a point where a branch
attains the envelope and both are differentiable, their derivatives agree. In particular,
at every differentiability time of a finite minimum, every active branch has the same
derivative as the minimum. -/
theorem active_branch_derivative_eq
    {ι : Type*} {f : ι → ℝ → ℝ} {g : ℝ → ℝ} {d : ι → ℝ} {dMin x : ℝ}
    (hle : ∀ i y, g y ≤ f i y)
    (hf : ∀ i, HasDerivAt (f i) (d i) x)
    (hg : HasDerivAt g dMin x)
    (i : ι) (hi : f i x = g x) :
    d i = dMin := by
  have hlocal : IsLocalMin (fun y => f i y - g y) x := by
    change ∀ᶠ y in 𝓝 x, (f i x - g x) ≤ f i y - g y
    rw [hi, sub_self]
    filter_upwards [] with y
    exact sub_nonneg.mpr (hle i y)
  have hderiv := hlocal.hasDerivAt_eq_zero ((hf i).sub hg)
  have hzero : d i - dMin = 0 := by
    simpa using hderiv
  exact sub_eq_zero.mp hzero

/-- If a lower envelope is attained by at least one member at `x`, the derivative of the
envelope is the derivative of an active member. This is the finite-minimum derivative
identity in the form needed when a measurable trajectory and all its finitely many branch
functions are differentiable at the time under consideration. -/
theorem exists_active_branch_with_derivative
    {ι : Type*} {f : ι → ℝ → ℝ} {g : ℝ → ℝ} {d : ι → ℝ} {dMin x : ℝ}
    (hle : ∀ i y, g y ≤ f i y)
    (hattains : ∃ i, f i x = g x)
    (hf : ∀ i, HasDerivAt (f i) (d i) x)
    (hg : HasDerivAt g dMin x) :
    ∃ i, f i x = g x ∧ d i = dMin := by
  obtain ⟨i, hi⟩ := hattains
  exact ⟨i, hi, active_branch_derivative_eq hle hf hg i hi⟩

/-- At a differentiability point of a finite minimum, every active branch has the same
derivative as the minimum. The finite infimum itself supplies both the lower-envelope and
attainment conditions, so there is no hidden selector assumption. -/
theorem finite_minimum_active_derivative_eq
    {ι : Type*} [Fintype ι] [Nonempty ι]
    {f : ι → ℝ → ℝ} {d : ι → ℝ} {dMin x : ℝ}
    (hf : ∀ i, HasDerivAt (f i) (d i) x)
    (hMin : HasDerivAt (finiteMinimum f) dMin x)
    (i : ι) (hi : f i x = finiteMinimum f x) :
    d i = dMin := by
  have hle : ∀ j y, finiteMinimum f y ≤ f j y := by
    intro j y
    exact Finset.inf'_le (fun k => f k y) (Finset.mem_univ j)
  exact active_branch_derivative_eq hle hf hMin i hi

/-- A finite minimum is attained, and at a differentiability point an active branch carries
the derivative of the minimum. -/
theorem finite_minimum_has_active_derivative
    {ι : Type*} [Fintype ι] [Nonempty ι]
    {f : ι → ℝ → ℝ} {d : ι → ℝ} {dMin x : ℝ}
    (hf : ∀ i, HasDerivAt (f i) (d i) x)
    (hMin : HasDerivAt (finiteMinimum f) dMin x) :
    ∃ i, f i x = finiteMinimum f x ∧ d i = dMin := by
  obtain ⟨i, -, hi⟩ := Finset.exists_mem_eq_inf'
    (s := Finset.univ) (H := Finset.univ_nonempty) (fun j => f j x)
  refine ⟨i, ?_, ?_⟩
  · exact hi.symm
  · exact finite_minimum_active_derivative_eq hf hMin i hi.symm

end N33Dynamics
