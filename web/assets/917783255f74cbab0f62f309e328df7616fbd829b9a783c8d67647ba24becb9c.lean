/- Read-only audit recipe. It was not run in this task to avoid overlapping
   the parent's Lean replay. `API_Audit.log` is the exact saved signature and
   axiom excerpt from the sibling audit identified in REPORT.md. -/
import N33Affine.GlobalAffineComposition

set_option pp.universes false

#check @N33Affine.exists_full_affine_family
#print N33Affine.InCube
#print N33Affine.AtMinSlice
#print N33Affine.value
#print N33Affine.Active
#print N33Affine.LittleO
#print N33Affine.FullApproximation
#print N33Affine.BoxFamily
#print N33Affine.FiniteFamily
#print axioms N33Affine.exists_full_affine_family
#print axioms N33Affine.exists_local_window_of_lower_dimensions
#print axioms N33Affine.exists_finite_pruned_interval_cover
