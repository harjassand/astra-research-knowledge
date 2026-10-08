import FiniteMinimum
import Mathlib.MeasureTheory.Function.AbsolutelyContinuous
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.Prod

noncomputable section

open Filter MeasureTheory Set
open scoped NNReal Topology

set_option maxHeartbeats 1000000

namespace N33Dynamics

/-!  A finite-dimensional path is supplied with its genuine Mathlib interval absolute
continuity hypothesis.  The scalar coordinate hypotheses used below are derived by composing
with the 1-Lipschitz coordinate projections. -/

private theorem absolutelyContinuousOnInterval_comp_lipschitz
    {X Y : Type*} [PseudoMetricSpace X] [PseudoMetricSpace Y]
    {f : ℝ → X} {g : X → Y} {a b : ℝ} {K : ℝ≥0}
    (hf : AbsolutelyContinuousOnInterval f a b) (hg : LipschitzWith K g) :
    AbsolutelyContinuousOnInterval (fun t => g (f t)) a b := by
  rw [absolutelyContinuousOnInterval_iff] at hf ⊢
  intro ε hε
  obtain ⟨δ, hδ, hsum⟩ := hf (ε / ((K : ℝ) + 1)) (by positivity)
  refine ⟨δ, hδ, ?_⟩
  intro E hE hlen
  have hbound :
      (∑ i ∈ Finset.range E.1, dist (g (f (E.2 i).1)) (g (f (E.2 i).2))) ≤
        (K : ℝ) * ∑ i ∈ Finset.range E.1, dist (f (E.2 i).1) (f (E.2 i).2) := by
    calc
      _ ≤ ∑ i ∈ Finset.range E.1,
            (K : ℝ) * dist (f (E.2 i).1) (f (E.2 i).2) := by
        apply Finset.sum_le_sum
        intro i hi
        exact hg.dist_le_mul _ _
      _ = (K : ℝ) * ∑ i ∈ Finset.range E.1,
            dist (f (E.2 i).1) (f (E.2 i).2) := by rw [Finset.mul_sum]
  have hinput := hsum E hE hlen
  have hmul :
      (K : ℝ) * ∑ i ∈ Finset.range E.1,
        dist (f (E.2 i).1) (f (E.2 i).2) ≤
      (K : ℝ) * (ε / ((K : ℝ) + 1)) :=
    mul_le_mul_of_nonneg_left hinput.le (by positivity)
  have hfinal : (K : ℝ) * (ε / ((K : ℝ) + 1)) < ε := by
    have hK : (K : ℝ) < (K : ℝ) + 1 := by linarith
    calc
      (K : ℝ) * (ε / ((K : ℝ) + 1)) <
          ((K : ℝ) + 1) * (ε / ((K : ℝ) + 1)) :=
        mul_lt_mul_of_pos_right hK (by positivity)
      _ = ε := by field_simp
  calc
    _ ≤ (K : ℝ) * ∑ i ∈ Finset.range E.1,
          dist (f (E.2 i).1) (f (E.2 i).2) := hbound
    _ ≤ (K : ℝ) * (ε / ((K : ℝ) + 1)) := hmul
    _ < ε := hfinal

private theorem absolutelyContinuousOnInterval_abs
    {f : ℝ → ℝ} {a b : ℝ}
    (hf : AbsolutelyContinuousOnInterval f a b) :
    AbsolutelyContinuousOnInterval (fun t => |f t|) a b := by
  rw [absolutelyContinuousOnInterval_iff] at hf ⊢
  intro ε hε
  obtain ⟨δ, hδ, hsum⟩ := hf ε hε
  refine ⟨δ, hδ, ?_⟩
  intro E hE hlen
  calc
    (∑ i ∈ Finset.range E.1,
        dist (|f (E.2 i).1|) (|f (E.2 i).2|)) ≤
      ∑ i ∈ Finset.range E.1,
        dist (f (E.2 i).1) (f (E.2 i).2) := by
          apply Finset.sum_le_sum
          intro i hi
          simpa only [Real.dist_eq] using
            (abs_abs_sub_abs_le_abs_sub (f (E.2 i).1) (f (E.2 i).2))
    _ < ε := hsum E hE hlen

private theorem absolutelyContinuousOnInterval_const
    {a b c : ℝ} :
    AbsolutelyContinuousOnInterval (fun _ : ℝ => c) a b := by
  unfold AbsolutelyContinuousOnInterval
  convert (tendsto_const_nhds :
    Tendsto (fun _ : ℕ × (ℕ → ℝ × ℝ) => (0 : ℝ))
      (AbsolutelyContinuousOnInterval.totalLengthFilter ⊓
        𝓟 (AbsolutelyContinuousOnInterval.disjWithin a b)) (𝓝 0)) using 1
  funext E
  simp

private theorem absolutelyContinuousOnInterval_min
    {f g : ℝ → ℝ} {a b : ℝ}
    (hf : AbsolutelyContinuousOnInterval f a b)
    (hg : AbsolutelyContinuousOnInterval g a b) :
    AbsolutelyContinuousOnInterval (fun t => min (f t) (g t)) a b := by
  have hid : (fun t => min (f t) (g t)) =
      fun t => (1 / 2 : ℝ) * (f t + g t - |f t - g t|) := by
    funext t
    rcases le_total (f t) (g t) with h | h
    · rw [min_eq_left h, abs_of_nonpos (sub_nonpos.mpr h)]
      ring
    · rw [min_eq_right h, abs_of_nonneg (sub_nonneg.mpr h)]
      ring
  rw [hid]
  have hdiff : AbsolutelyContinuousOnInterval (fun t => f t - g t) a b := hf.sub hg
  have habs := absolutelyContinuousOnInterval_abs hdiff
  have hadd := hf.add hg
  exact (hadd.sub habs).const_mul (1 / 2 : ℝ)

private theorem absolutelyContinuousOnInterval_finset_inf
    {ι : Type*} {s : Finset ι} {f : ι → ℝ → ℝ} {a b : ℝ}
    (hs : s.Nonempty)
    (hf : ∀ i ∈ s, AbsolutelyContinuousOnInterval (f i) a b) :
    AbsolutelyContinuousOnInterval
      (fun t => s.inf' hs (fun i => f i t)) a b := by
  classical
  revert hf
  induction hs using Finset.Nonempty.cons_induction with
  | singleton i =>
      intro hf
      simpa using hf i (Finset.mem_singleton_self i)
  | cons i s hi hs ih =>
      intro hf
      have hmin := absolutelyContinuousOnInterval_min
        (hf i (Finset.mem_cons_self i s))
        (ih (fun j hj => hf j (Finset.mem_cons_of_mem hj)))
      have hEq : (fun t =>
          (Finset.cons i s hi).inf' (Finset.cons_nonempty hi) (fun j => f j t)) =
          (fun t => min (f i t) (s.inf' hs (fun j => f j t))) := by
        funext t
        rw [Finset.inf'_cons hs]
      rw [hEq]
      exact hmin

private theorem absolutelyContinuousOnInterval_sum
    {ι : Type*} (s : Finset ι) (f : ι → ℝ → ℝ) {a b : ℝ}
    (hf : ∀ i ∈ s, AbsolutelyContinuousOnInterval (f i) a b) :
    AbsolutelyContinuousOnInterval (fun t => ∑ i ∈ s, f i t) a b := by
  classical
  induction s using Finset.induction_on with
  | empty =>
      simpa using (absolutelyContinuousOnInterval_const (a := a) (b := b) (c := 0))
  | @insert i s hi ih =>
      simp only [Finset.sum_insert hi]
      exact (hf i (Finset.mem_insert_self i s)).add
        (ih (fun j hj => hf j (Finset.mem_insert_of_mem hj)))

private theorem absolutelyContinuousOnInterval_affineBranch
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    (x : ℝ → (Fin m → ℝ)) (a b : ℝ)
    (coeff : ι → Fin m → ℝ) (offset : ι → ℝ) (i : ι)
    (hcoord : ∀ j, AbsolutelyContinuousOnInterval (fun t => x t j) a b) :
    AbsolutelyContinuousOnInterval
      (fun t => offset i + ∑ j, coeff i j * x t j) a b := by
  have hsum := absolutelyContinuousOnInterval_sum Finset.univ
    (fun j t => coeff i j * x t j) (a := a) (b := b)
    (fun j hj => (hcoord j).const_mul (coeff i j))
  exact (absolutelyContinuousOnInterval_const (a := a) (b := b) (c := offset i)).add hsum

private theorem coord_absolutelyContinuous
    {m : ℕ} {x : ℝ → (Fin m → ℝ)} {a b : ℝ}
    (hx : AbsolutelyContinuousOnInterval x a b) (j : Fin m) :
    AbsolutelyContinuousOnInterval (fun t => x t j) a b := by
  have heval : LipschitzWith 1 (fun y : Fin m → ℝ => y j) := by
    apply LipschitzWith.mk_one
    intro y z
    exact dist_le_pi_dist y z j
  exact absolutelyContinuousOnInterval_comp_lipschitz hx heval

/-- Fixed affine branches pulled back along a finite-dimensional absolutely continuous path.
The finite index type is nonempty, but no uniqueness of an active branch is assumed. -/
def affineBranchAlong
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    (x : ℝ → (Fin m → ℝ)) (coeff : ι → Fin m → ℝ) (offset : ι → ℝ) :
    ι → ℝ → ℝ :=
  fun i t => offset i + ∑ j, coeff i j * x t j

/-- The pointwise minimum of a fixed finite family of affine branches along a path. -/
def affineMinimumAlong
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    (x : ℝ → (Fin m → ℝ)) (coeff : ι → Fin m → ℝ) (offset : ι → ℝ) :
    ℝ → ℝ := finiteMinimum (affineBranchAlong x coeff offset)

/-- A finite nonempty affine lower envelope preserves absolute continuity of the trajectory.
The hypothesis is actual Mathlib interval absolute continuity of the vector-valued path. -/
theorem affineMinimumAlong_absolutelyContinuous
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    {x : ℝ → (Fin m → ℝ)} {a b : ℝ}
    (hx : AbsolutelyContinuousOnInterval x a b)
    (coeff : ι → Fin m → ℝ) (offset : ι → ℝ) :
    AbsolutelyContinuousOnInterval (affineMinimumAlong x coeff offset) a b := by
  have hcoord : ∀ j, AbsolutelyContinuousOnInterval (fun t => x t j) a b :=
    fun j => coord_absolutelyContinuous hx j
  have hbranch : ∀ i, AbsolutelyContinuousOnInterval
      (affineBranchAlong x coeff offset i) a b := by
    intro i
    exact absolutelyContinuousOnInterval_affineBranch x a b coeff offset i hcoord
  unfold affineMinimumAlong
  change AbsolutelyContinuousOnInterval
    (fun t => Finset.univ.inf' Finset.univ_nonempty
      (fun i => affineBranchAlong x coeff offset i t)) a b
  exact absolutelyContinuousOnInterval_finset_inf Finset.univ_nonempty
    (fun i hi => hbranch i)

private theorem affineBranchAlong_hasDerivAt
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    {x : ℝ → (Fin m → ℝ)} {coeff : ι → Fin m → ℝ} {offset : ι → ℝ}
    {i : ι} {t : ℝ}
    (hx : ∀ j, DifferentiableAt ℝ (fun u => x u j) t) :
    HasDerivAt (affineBranchAlong x coeff offset i)
      (∑ j, coeff i j * deriv (fun u => x u j) t) t := by
  have hsum : HasDerivAt (fun u => ∑ j, coeff i j * x u j)
      (∑ j, coeff i j * deriv (fun u => x u j) t) t := by
    exact HasDerivAt.fun_sum (u := Finset.univ)
      (fun j hj => (hx j).hasDerivAt.const_mul (coeff i j))
  change HasDerivAt (fun u => offset i + ∑ j, coeff i j * x u j) _ t
  exact hsum.const_add (offset i)

/-- At every common differentiability time, every weakly active affine branch has the same
time derivative as the lower envelope. Ties are all retained by the universal `∀ i` premise. -/
theorem affineMinimumAlong_active_derivative_eq
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    {x : ℝ → (Fin m → ℝ)} {coeff : ι → Fin m → ℝ} {offset : ι → ℝ}
    {t : ℝ}
    (hx : DifferentiableAt ℝ x t)
    (hmin : DifferentiableAt ℝ (affineMinimumAlong x coeff offset) t)
    (i : ι)
    (hi : affineBranchAlong x coeff offset i t =
      affineMinimumAlong x coeff offset t) :
    (∑ j, coeff i j * deriv (fun u => x u j) t) =
      deriv (affineMinimumAlong x coeff offset) t := by
  have hxcoord : ∀ j, DifferentiableAt ℝ (fun u => x u j) t :=
    (differentiableAt_pi.mp hx)
  have hmin' := hmin.hasDerivAt
  have heq := finite_minimum_active_derivative_eq
    (f := affineBranchAlong x coeff offset)
    (d := fun k => ∑ j, coeff k j * deriv (fun u => x u j) t)
    (dMin := deriv (affineMinimumAlong x coeff offset) t)
    (x := t) (fun k => affineBranchAlong_hasDerivAt
      (x := x) (coeff := coeff) (offset := offset) (i := k) hxcoord)
    (by simpa [affineMinimumAlong] using hmin') i hi
  exact heq

/-- The path, every affine branch, and their minimum are simultaneously differentiable almost
everywhere on the compact time interval. This is derived from interval absolute continuity; it is
not an assumed a.e.-differentiability premise. -/
theorem affineMinimumAlong_ae_common_differentiable
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    {x : ℝ → (Fin m → ℝ)} {a b : ℝ}
    (hx : AbsolutelyContinuousOnInterval x a b)
    (coeff : ι → Fin m → ℝ) (offset : ι → ℝ) :
    ∀ᵐ t : ℝ, t ∈ uIcc a b →
      DifferentiableAt ℝ (affineMinimumAlong x coeff offset) t ∧
      (∀ i, DifferentiableAt ℝ (affineBranchAlong x coeff offset i) t) ∧
      DifferentiableAt ℝ x t ∧
      (∀ j, DifferentiableAt ℝ (fun u => x u j) t) := by
  have hminAC := affineMinimumAlong_absolutelyContinuous hx coeff offset
  have hminAE := hminAC.ae_differentiableAt
  have hcoord : ∀ j, AbsolutelyContinuousOnInterval (fun t => x t j) a b :=
    fun j => coord_absolutelyContinuous hx j
  have hcoordAE : ∀ j, ∀ᵐ t : ℝ, t ∈ uIcc a b →
      DifferentiableAt ℝ (fun u => x u j) t := fun j => (hcoord j).ae_differentiableAt
  have hbranchAC : ∀ i, AbsolutelyContinuousOnInterval
      (affineBranchAlong x coeff offset i) a b := by
    intro i
    exact absolutelyContinuousOnInterval_affineBranch x a b coeff offset i hcoord
  have hbranchAE : ∀ i, ∀ᵐ t : ℝ, t ∈ uIcc a b →
      DifferentiableAt ℝ (affineBranchAlong x coeff offset i) t :=
    fun i => (hbranchAC i).ae_differentiableAt
  have hbranches : ∀ᵐ t : ℝ, ∀ i, t ∈ uIcc a b →
      DifferentiableAt ℝ (affineBranchAlong x coeff offset i) t := by
    exact ae_all_iff.2 hbranchAE
  have hcoords : ∀ᵐ t : ℝ, ∀ j, t ∈ uIcc a b →
      DifferentiableAt ℝ (fun u => x u j) t := by
    exact ae_all_iff.2 hcoordAE
  filter_upwards [hminAE, hbranches, hcoords] with t hmin hbranches hcoords
  intro ht
  have hcoordAt : ∀ j, DifferentiableAt ℝ (fun u => x u j) t :=
    fun j => hcoords j ht
  exact ⟨hmin ht, fun i => hbranches i ht,
    differentiableAt_pi.mpr hcoordAt, hcoordAt⟩

/-- The active-branch derivative identity holds almost everywhere for an AC finite-dimensional
trajectory, with its affine directional derivative expressed as the coefficient dot product with
the coordinatewise path derivative. -/
theorem affineMinimumAlong_ae_active_derivative_eq
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    {x : ℝ → (Fin m → ℝ)} {a b : ℝ}
    (hx : AbsolutelyContinuousOnInterval x a b)
    (coeff : ι → Fin m → ℝ) (offset : ι → ℝ) :
    ∀ᵐ t : ℝ, t ∈ uIcc a b → ∀ i,
      affineBranchAlong x coeff offset i t = affineMinimumAlong x coeff offset t →
      (∑ j, coeff i j * deriv (fun u => x u j) t) =
        deriv (affineMinimumAlong x coeff offset) t := by
  have hcommon := affineMinimumAlong_ae_common_differentiable hx coeff offset
  filter_upwards [hcommon] with t ht
  intro htmem
  rcases ht htmem with ⟨hmin, hbranches, htraj, hcoords⟩
  intro i hi
  exact affineMinimumAlong_active_derivative_eq
    htraj hmin i hi

/-- If every weakly active branch has drift at least `δ` almost everywhere, the AC lower
envelope has derivative at least `δ` almost everywhere. -/
theorem affineMinimumAlong_ae_drift_lower_bound
    {m : ℕ} {ι : Type*} [Fintype ι] [Nonempty ι]
    {x : ℝ → (Fin m → ℝ)} {a b δ : ℝ}
    (hx : AbsolutelyContinuousOnInterval x a b)
    (coeff : ι → Fin m → ℝ) (offset : ι → ℝ)
    (hbranchDrift : ∀ᵐ t : ℝ, t ∈ uIcc a b → ∀ i,
      affineBranchAlong x coeff offset i t = affineMinimumAlong x coeff offset t →
      δ ≤ ∑ j, coeff i j * deriv (fun u => x u j) t) :
    ∀ᵐ t : ℝ, t ∈ uIcc a b →
      δ ≤ deriv (affineMinimumAlong x coeff offset) t := by
  have hactive := affineMinimumAlong_ae_active_derivative_eq hx coeff offset
  filter_upwards [hactive, hbranchDrift] with t hactive hdrift
  intro ht
  obtain ⟨i, hi⟩ := Finset.exists_mem_eq_inf'
    (s := Finset.univ) (H := Finset.univ_nonempty)
    (fun k => affineBranchAlong x coeff offset k t)
  have hi' : affineBranchAlong x coeff offset i t =
      affineMinimumAlong x coeff offset t := by
    simpa [affineMinimumAlong] using hi.2.symm
  have hderiv := hactive ht i hi'
  exact (hdrift ht i hi').trans_eq hderiv

end N33Dynamics
