import N33Affine.AffineCore
import N33Affine.SliceFamily

noncomputable section

open Filter Topology Set

namespace N33Affine

/-- Data at the first step of a history segment. Besides the next threshold,
it retains the whole next-type family as mapped into the eventual terminal
family. This is the direct competitor interface needed by the local B2 step. -/
inductive HeadInfo {m : ℕ} {a b t : ℝ} {E : (Fin m → ℝ) → ℝ}
    {hat : a ≤ t} {htb : t ≤ b} {Oracle : SliceOracle m a b t E}
    (Ffinal : BoxFamily m a b) :
    (k : ℕ) → (upper : ℝ) → BoxFamily m a b → Type 2
  | terminal {k upper F} (hk : k = m) : HeadInfo Ffinal k upper F
  | next {k upper F} (hkm : k < m) (β : ℝ) (hβt : t < β)
      (hβupper : β < upper)
      (hmargin : ∀ j, β - t < E (F.family.label j).slope)
      (S : SliceSystem m k t β b E)
      (map : (stageFamily S (Nat.le_of_lt hkm) hat htb (le_of_lt hβt)).family.Index ↪
        Ffinal.family.Index)
      (labels : ∀ j, Ffinal.family.label (map j) =
        (stageFamily S (Nat.le_of_lt hkm) hat htb (le_of_lt hβt)).family.label j) :
      HeadInfo Ffinal k upper F

/-- A named stage together with its embedding into the common terminal family. -/
structure StageRecord {m : ℕ} {a b t : ℝ} {E : (Fin m → ℝ) → ℝ}
    {hat : a ≤ t} {htb : t ≤ b} {Oracle : SliceOracle m a b t E}
    (Ffinal : BoxFamily m a b) where
  previous : BoxFamily m a b
  k : ℕ
  hkm : k < m
  β : ℝ
  hβt : t < β
  system : SliceSystem m k t β b E
  stageMap :
    (stageFamily system (Nat.le_of_lt hkm) hat htb (le_of_lt hβt)).family.Index ↪
      Ffinal.family.Index
  stageLabels : ∀ j, Ffinal.family.label (stageMap j) =
    (stageFamily system (Nat.le_of_lt hkm) hat htb (le_of_lt hβt)).family.label j
  following : HeadInfo (m := m) (a := a) (b := b) (t := t) (E := E)
    (hat := hat) (htb := htb) (Oracle := Oracle) Ffinal (k + 1) β
    (appendBoxFamily previous
      (stageFamily system (Nat.le_of_lt hkm) hat htb (le_of_lt hβt)))

/-- Archive of the terminal labels: the initial family and every future stage
have label-preserving embeddings into the same finite family, and these images
cover all terminal indices. -/
structure StageArchive {m : ℕ} {a b t : ℝ} {E : (Fin m → ℝ) → ℝ}
    {hat : a ≤ t} {htb : t ≤ b} {Oracle : SliceOracle m a b t E}
    {k : ℕ} {upper : ℝ} {F : BoxFamily m a b}
    (H : StageHistory m a b t E hat htb Oracle k upper F)
    (Ffinal : BoxFamily m a b) where
  terminalUpper : ℝ
  terminal : StageHistory m a b t E hat htb Oracle m terminalUpper Ffinal
  carry : F.family.Index ↪ Ffinal.family.Index
  carryLabels : ∀ j, Ffinal.family.label (carry j) = F.family.label j
  first : HeadInfo (m := m) (a := a) (b := b) (t := t) (E := E)
    (hat := hat) (htb := htb) (Oracle := Oracle) Ffinal k upper F
  stages : List (StageRecord (m := m) (a := a) (b := b) (t := t)
    (E := E) (hat := hat) (htb := htb) (Oracle := Oracle) Ffinal)
  covers : ∀ j : Ffinal.family.Index,
    (∃ i, carry i = j) ∨ ∃ R, R ∈ stages ∧ ∃ i, R.stageMap i = j

theorem StageHistory.exists_archive {m : ℕ} {a b t : ℝ}
    {E : (Fin m → ℝ) → ℝ} {hat : a ≤ t} {htb : t ≤ b}
    {Oracle : SliceOracle m a b t E} {k : ℕ} {upper : ℝ}
    {F : BoxFamily m a b}
    (H : StageHistory m a b t E hat htb Oracle k upper F) :
    ∃ (upperFinal : ℝ) (Ffinal : BoxFamily m a b),
      Nonempty (StageArchive H Ffinal) := by
  induction H with
  | @done upper F =>
      refine ⟨upper, F, ⟨?_⟩⟩
      refine {
        terminalUpper := upper
        terminal := StageHistory.done
        carry := Function.Embedding.refl _
        carryLabels := fun _ => rfl
        first := HeadInfo.terminal rfl
        stages := []
        covers := ?_ }
      intro j
      exact Or.inl ⟨j, rfl⟩
  | @step k upper F hkpos hkm hupper hupperB β hβt hβupper hmargin tail ih =>
      let S := Oracle.provide k hkpos hkm β hβt
        (lt_of_lt_of_le hβupper hupperB)
      let G := stageFamily S (Nat.le_of_lt hkm) hat htb (le_of_lt hβt)
      obtain ⟨upperFinal, Ffinal, hA⟩ := ih
      obtain ⟨A⟩ := hA
      let currentMap : G.family.Index ↪ Ffinal.family.Index :=
        ⟨fun j => A.carry (appendRightIndex F G j), by
          intro x y hxy
          apply (appendRightIndex F G).injective
          exact A.carry.injective hxy⟩
      have hcurrentLabels : ∀ j, Ffinal.family.label (currentMap j) = G.family.label j := by
        intro j
        change Ffinal.family.label (A.carry (appendRightIndex F G j)) = G.family.label j
        calc
          Ffinal.family.label (currentMap j) =
              (appendBoxFamily F G).family.label (appendRightIndex F G j) :=
            A.carryLabels (appendRightIndex F G j)
          _ = G.family.label j := appendRightIndex_label F G j
      have hmarginLabel : ∀ j, β - t < E (F.family.label j).slope := by
        intro j
        exact hmargin _ (Finset.mem_image.mpr ⟨j, Finset.mem_univ j, rfl⟩)
      let R : StageRecord Ffinal := {
        previous := F
        k := k
        hkm := hkm
        β := β
        hβt := hβt
        system := S
        stageMap := currentMap
        stageLabels := hcurrentLabels
        following := A.first
      }
      refine ⟨upperFinal, Ffinal, ⟨?_⟩⟩
      refine {
        terminalUpper := A.terminalUpper
        terminal := A.terminal
        carry := ⟨fun j => A.carry (appendLeftIndex F G j), by
          intro x y hxy
          apply (appendLeftIndex F G).injective
          exact A.carry.injective hxy⟩
        carryLabels := ?_
        first := HeadInfo.next hkm β hβt hβupper hmarginLabel S
          currentMap hcurrentLabels
        stages := R :: A.stages
        covers := ?_ }
      · intro j
        calc
          Ffinal.family.label (A.carry (appendLeftIndex F G j)) =
              (appendBoxFamily F G).family.label (appendLeftIndex F G j) :=
            A.carryLabels (appendLeftIndex F G j)
          _ = F.family.label j := appendLeftIndex_label F G j
      · intro j
        rcases A.covers j with hinitial | ⟨Rfuture, hRfuture, x, hx⟩
        · rcases hinitial with ⟨x, hx⟩
          cases x with
          | inl x =>
              apply Or.inl
              refine ⟨x, ?_⟩
              exact hx
          | inr x =>
              apply Or.inr
              refine ⟨R, by simp, x, ?_⟩
              exact hx
        · apply Or.inr
          exact ⟨Rfuture, List.mem_cons_of_mem _ hRfuture, x, hx⟩

end N33Affine
