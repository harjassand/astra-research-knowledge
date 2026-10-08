import N33Affine.StageEnvelopes
import N33Affine.StageArchive

noncomputable section

open Filter Topology Set

namespace N33Affine

theorem StageHistory.exists_terminal_envelope_archive
    {m : ℕ} {a b t : ℝ} {E : (Fin m → ℝ) → ℝ}
    {hat : a ≤ t} {htb : t ≤ b} {Oracle : SliceOracle m a b t E}
    {k : ℕ} {upper : ℝ} {F : BoxFamily m a b}
    (H : StageHistory m a b t E hat htb Oracle k upper F)
    (hFloor : FamilySlopesGe F t)
    (hBase : FamilyHasFlatBaseline (t := t) F)
    (hSmall : ∃ γ, t < γ ∧ FamilyLittleOAt F γ) :
    ∃ (upperFinal : ℝ) (Ffinal : BoxFamily m a b) (γ : ℝ),
      StageHistory m a b t E hat htb Oracle m upperFinal Ffinal ∧
      FamilySlopesGe Ffinal t ∧ FamilyHasFlatBaseline (t := t) Ffinal ∧
      t < γ ∧ FamilyLittleOAt Ffinal γ ∧
      Nonempty (StageArchive H Ffinal) := by
  induction H with
  | @done upper F =>
      obtain ⟨γ, htγ, hγ⟩ := hSmall
      let Hdone : StageHistory m a b t E hat htb Oracle m upper F :=
        StageHistory.done
      let A : StageArchive Hdone F := {
        terminalUpper := upper
        terminal := Hdone
        carry := Function.Embedding.refl _
        carryLabels := fun _ => rfl
        first := HeadInfo.terminal (m := m) (a := a) (b := b) (t := t)
          (E := E) (hat := hat) (htb := htb) (Oracle := Oracle) rfl
        stages := ([] : List (StageRecord (m := m) (a := a) (b := b)
          (t := t) (E := E) (hat := hat) (htb := htb)
          (Oracle := Oracle) F))
        covers := by intro j; exact Or.inl ⟨j, rfl⟩ }
      exact ⟨upper, F, γ, Hdone, hFloor, hBase, htγ, hγ, ⟨A⟩⟩
  | @step k upper F hkpos hkm hupper hupperB β hβt hβupper hmargin tail ih =>
      let S := Oracle.provide k hkpos hkm β hβt
        (lt_of_lt_of_le hβupper hupperB)
      let G := stageFamily S (Nat.le_of_lt hkm) hat htb (le_of_lt hβt)
      have hGFloor : FamilySlopesGe G t := by
        intro j i
        exact stageFamily_slopes_ge S (Nat.le_of_lt hkm) hat htb
          (le_of_lt hβt) j i
      have hAppFloor : FamilySlopesGe (appendBoxFamily F G) t :=
        appendBoxFamily_slopes_ge F G hFloor hGFloor
      have hAppBase : FamilyHasFlatBaseline (t := t) (appendBoxFamily F G) :=
        appendBoxFamily_has_baseline_left F G hBase
      obtain ⟨γold, htγold, hOldSmall⟩ := hSmall
      let γnew := (t + min γold β) / 2
      have htγnew : t < γnew := by
        have hmin : t < min γold β := lt_min_iff.mpr ⟨htγold, hβt⟩
        dsimp [γnew]
        linarith
      have hγnewOld : γnew < γold := by
        have hmin : min γold β ≤ γold := min_le_left _ _
        dsimp [γnew]
        linarith
      have hγnewβ : γnew < β := by
        have hmin : min γold β ≤ β := min_le_right _ _
        dsimp [γnew]
        linarith
      have hOldSmall' : FamilyLittleOAt F γnew := by
        intro j
        exact littleO_lower_exponent (hOldSmall j) hγnewOld
      have hGSmall : FamilyLittleOAt G γnew :=
        stageFamily_littleO_at_gamma S (Nat.le_of_lt hkm)
          hat htb htγnew hγnewβ
      have hAppSmall : FamilyLittleOAt (appendBoxFamily F G) γnew :=
        append_family_littleO_at F G hOldSmall' hGSmall
      obtain ⟨upperFinal, Ffinal, γFinal, hFinal, hFinalFloor,
        hFinalBase, htγFinal, hFinalSmall, hArchive⟩ :=
          ih hAppFloor hAppBase ⟨γnew, htγnew, hAppSmall⟩
      obtain ⟨A⟩ := hArchive
      let currentMap : G.family.Index ↪ Ffinal.family.Index :=
        ⟨fun j => A.carry (appendRightIndex F G j), by
          intro x y hxy
          apply (appendRightIndex F G).injective
          exact A.carry.injective hxy⟩
      have hcurrentLabels : ∀ j, Ffinal.family.label (currentMap j) = G.family.label j := by
        intro j
        change Ffinal.family.label (A.carry (appendRightIndex F G j)) = G.family.label j
        calc
          Ffinal.family.label (A.carry (appendRightIndex F G j)) =
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
      let rootArchive : StageArchive
          (StageHistory.step hkpos hkm hupper hupperB β hβt hβupper hmargin tail)
          Ffinal := {
        terminalUpper := A.terminalUpper
        terminal := A.terminal
        carry := ⟨fun j => A.carry (appendLeftIndex F G j), by
          intro x y hxy
          apply (appendLeftIndex F G).injective
          exact A.carry.injective hxy⟩
        carryLabels := by
          intro j
          calc
            Ffinal.family.label (A.carry (appendLeftIndex F G j)) =
                (appendBoxFamily F G).family.label (appendLeftIndex F G j) :=
              A.carryLabels (appendLeftIndex F G j)
            _ = F.family.label j := appendLeftIndex_label F G j
        first := HeadInfo.next hkm β hβt hβupper hmarginLabel S
          currentMap hcurrentLabels
        stages := R :: A.stages
        covers := by
          intro j
          rcases A.covers j with hinitial | ⟨Rfuture, hRfuture, x, hx⟩
          · rcases hinitial with ⟨x, hx⟩
            cases x with
            | inl x => exact Or.inl ⟨x, hx⟩
            | inr x => exact Or.inr ⟨R, by simp, x, hx⟩
          · exact Or.inr ⟨Rfuture, List.mem_cons_of_mem _ hRfuture, x, hx⟩ }
      exact ⟨upperFinal, Ffinal, γFinal, hFinal, hFinalFloor,
        hFinalBase, htγFinal, hFinalSmall, ⟨rootArchive⟩⟩

theorem exists_complete_stage_family_with_certificate
    {m : ℕ} {a b t : ℝ} {E : (Fin m → ℝ) → ℝ}
    (hm : 0 < m) (hat : a ≤ t) (htb : t ≤ b) (htb_strict : t < b)
    (Oracle : SliceOracle m a b t E)
    (hE : ∀ r, InCube a b r → 0 < E r) :
    ∃ (upperFinal : ℝ) (F : BoxFamily m a b) (γ : ℝ),
      StageHistory m a b t E hat htb Oracle m upperFinal F ∧
      FamilySlopesGe F t ∧ FamilyHasFlatBaseline (t := t) F ∧
      t < γ ∧ FamilyLittleOAt F γ ∧
      Nonempty (StageArchive
        (exists_initial_stage_history hm hat htb htb_strict Oracle hE) F) := by
  let H := exists_initial_stage_history hm hat htb htb_strict Oracle hE
  have hbaseSmall : FamilyLittleOAt (baseBoxFamily (m := m) hat htb) (t + 1) := by
    intro j
    exact littleO_zero_bump (t + 1)
  have hBase := baseBoxFamily_has_baseline (m := m) hat htb
  have hFloor := baseBoxFamily_slopes_ge (m := m) hat htb
  obtain ⟨upperFinal, F, γ, hFinal, hFinalFloor, hFinalBase,
    htγ, hSmall, hArchive⟩ := H.exists_terminal_envelope_archive hFloor hBase
      ⟨t + 1, by linarith, hbaseSmall⟩
  exact ⟨upperFinal, F, γ, hFinal, hFinalFloor, hFinalBase,
    htγ, hSmall, hArchive⟩

end N33Affine
