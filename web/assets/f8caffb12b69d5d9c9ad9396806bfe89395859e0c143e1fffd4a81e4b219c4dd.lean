import N33Affine.AffineInduction
import N33FiniteGlue
example {N m : ℕ} (families : Fin N → N33Affine.FiniteFamily m)
    (q : ℕ → ℝ) (hN : 0 < N) (j : Fin N) (k : (families j).Index) :
    (N33Affine.GluePlacement.shiftedUnion families q hN).label ⟨j, k⟩ =
      N33Affine.Glue.taggedLabels (fun j k => (families j).label k) q ⟨j, k⟩ := by
  rfl
example {N m : ℕ} (families : Fin N → N33Affine.FiniteFamily m)
    (q : ℕ → ℝ) (hN : 0 < N) (j : Fin N) (k : (families j).Index) :
    (N33Affine.GluePlacement.shiftedUnion families q hN).label ⟨j, k⟩ =
      (N33Affine.Glue.gluedFamily families q hN).label ⟨j, k⟩ := by
  rfl
