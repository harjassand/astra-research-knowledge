import Mathlib.Analysis.SpecialFunctions.Pow.Real

open Filter Topology Set

namespace N33Affine

noncomputable section

variable {m : ℕ}

/-- Coordinatewise membership in the exponent cube. -/
def InCube (a b : ℝ) (p : Fin m → ℝ) : Prop :=
  ∀ i, a ≤ p i ∧ p i ≤ b

/-- The limiting exponent has minimum coordinate exactly `t`. -/
def AtMinSlice (p : Fin m → ℝ) (t : ℝ) : Prop :=
  (∀ i, t ≤ p i) ∧ ∃ i, p i = t

/-- A slope together with its scale-dependent affine offset. -/
structure Label (m : ℕ) where
  slope : Fin m → ℝ
  bump : ℝ → ℝ

/-- The affine label evaluated at the generalized monomial scale point. -/
def value (ℓ : Label m) (h : ℝ) (p : Fin m → ℝ) : ℝ :=
  (Finset.univ.sum fun i => ℓ.slope i * Real.rpow h (p i)) + ℓ.bump h

/-- Weak activity against every label; equality therefore keeps every tied minimizer active. -/
def Active {ι : Type*} (family : ι → Label m) (j : ι) (h : ℝ)
    (p : Fin m → ℝ) : Prop :=
  ∀ j', value (family j) h p ≤ value (family j') h p

/-- `bump = o(h^α)` as the positive scale tends to zero. -/
def LittleO (bump : ℝ → ℝ) (α : ℝ) : Prop :=
  Tendsto (fun h => bump h / Real.rpow h α) (𝓝[>] 0) (𝓝 0)

/-- The exact sequential conclusion for one fixed active label at a minimum-coordinate slice.
Approximating exponent vectors are unrestricted; only their limit lies in the cube. -/
def LocalApproximation {ι : Type*} (a b t : ℝ) (E : (Fin m → ℝ) → ℝ)
    (family : ι → Label m) (j : ι) : Prop :=
  ∀ (hSeq : ℕ → ℝ) (pSeq : ℕ → Fin m → ℝ) (p : Fin m → ℝ),
    Tendsto hSeq atTop (𝓝[>] 0) →
    Tendsto pSeq atTop (𝓝 p) →
    InCube a b p → AtMinSlice p t →
    (∀ᶠ n in atTop, Active family j (hSeq n) (pSeq n)) →
    ∀ i, |p i - (family j).slope i| < E (family j).slope

end

end N33Affine
