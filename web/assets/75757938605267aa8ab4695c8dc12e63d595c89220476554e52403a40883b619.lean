import N33Affine.StageLocalEstimate
import N33Affine.StageArchive

noncomputable section

open Filter Topology Set

namespace N33Affine

/-- A baseline label in the initial family is close on the minimum slice.
The first one-coordinate stage supplies the competitor that prevents any
coordinate from rising above its first threshold. -/
theorem baseline_label_local_approximation
    {m : ℕ} {a b t : ℝ} {E : (Fin m → ℝ) → ℝ}
    {hat : a ≤ t} {htb : t ≤ b} {Oracle : SliceOracle m a b t E}
    {Ffinal : BoxFamily m a b}
    (first : HeadInfo (m := m) (a := a) (b := b) (t := t) (E := E)
      (hat := hat) (htb := htb) (Oracle := Oracle) Ffinal 1 b
      (baseBoxFamily hat htb))
    (jbase : Ffinal.family.Index)
    (hbase : Ffinal.family.label jbase = baselineLabel t)
    (hSeq : ℕ → ℝ) (pSeq : ℕ → Fin m → ℝ) (p : Fin m → ℝ)
    (hactive : ∀ᶠ n in atTop,
      Active Ffinal.family.label jbase (hSeq n) (pSeq n))
    (hh : Tendsto hSeq atTop (nhdsWithin 0 (Set.Ioi 0)))
    (hp : Tendsto pSeq atTop (nhds p))
    (hpMin : AtMinSlice p t)
    (hE : ∀ r, InCube a b r → 0 < E r) :
    ∀ i, |p i - t| < E (fun _ : Fin m => t) := by
  cases first with
  | terminal hmEq =>
      have hmOne : m = 1 := hmEq.symm
      obtain ⟨i0, hi0⟩ := hpMin.2
      intro i
      have hii : i = i0 := by
        apply Fin.ext
        have hi := i.isLt
        have hi0' := i0.isLt
        omega
      have hpi : p i = t := by simpa [hii] using hi0
      have hcube : InCube a b (fun _ : Fin m => t) := by
        intro _
        exact ⟨hat, htb⟩
      have hpositive := hE (fun _ : Fin m => t) hcube
      simpa [hpi] using hpositive
  | next hk β hβt hβupper hmargin S stageMap stageLabels =>
      intro i
      have hple : p i ≤ β := by
        by_contra hnot
        have hip : β < p i := lt_of_not_ge hnot
        let e : Fin 1 ↪ Fin m :=
          ⟨fun _ => i, by intro x y hxy; exact Subsingleton.elim _ _⟩
        obtain ⟨jlocal⟩ := (S.input e).family.nonempty
        let stageJ := stageIndex S (Nat.le_of_lt hk) hat htb (le_of_lt hβt) e jlocal
        have hlabel : Ffinal.family.label (stageMap stageJ) =
            liftLabel t β e ((S.input e).family.label jlocal) := by
          calc
            Ffinal.family.label (stageMap stageJ) =
                (stageFamily S (Nat.le_of_lt hk) hat htb (le_of_lt hβt)).family.label stageJ :=
              stageLabels stageJ
            _ = liftLabel t β e ((S.input e).family.label jlocal) :=
              stageIndex_label S (Nat.le_of_lt hk) hat htb (le_of_lt hβt) e jlocal
        have hcomp : ∀ᶠ n in atTop,
            value (baselineLabel t) (hSeq n) (pSeq n) ≤
              value (liftLabel t β e ((S.input e).family.label jlocal))
                (hSeq n) (pSeq n) := by
          filter_upwards [hactive] with n hn
          have hle := hn (stageMap stageJ)
          rw [hbase, hlabel] at hle
          exact hle
        have hsupport : ∀ u : Fin 1, β < p (e u) := by
          intro u
          have hu : u = 0 := Subsingleton.elim _ _
          subst u
          simpa [e] using hip
        exact no_baseline_activity_when_all_exponents_above e
          ((S.input e).family.label jlocal) hh hp
          ((S.input e).littleO jlocal) hsupport hcomp
      have hmarginBase : β - t < E (fun _ : Fin m => t) := by
        have hmarg := hmargin PUnit.unit
        change β - t < E (fun _ : Fin m => t) at hmarg
        exact hmarg
      have hpit : t ≤ p i := hpMin.1 i
      have habs : |p i - t| = p i - t := abs_of_nonneg (sub_nonneg.mpr hpit)
      rw [habs]
      exact lt_of_le_of_lt (sub_le_sub_right hple t) hmarginBase

/-- Every label in a terminal family produced from the exact initial history
has the original local approximation property. The proof follows each label's
archive provenance: initial labels use the first-stage baseline bound; a stage
label uses its same-embedding lower family and the following stage (or the
one-coordinate terminal case). -/
theorem initial_stage_archive_local_approximation
    {m : ℕ} {a b t : ℝ} {E : (Fin m → ℝ) → ℝ}
    (hm : 0 < m) (hat : a ≤ t) (htb : t ≤ b) (htbStrict : t < b)
    (Oracle : SliceOracle m a b t E)
    (hE : ∀ r, InCube a b r → 0 < E r)
    {Ffinal : BoxFamily m a b}
    (A : StageArchive
      (exists_initial_stage_history hm hat htb htbStrict Oracle hE) Ffinal)
    (hSeq : ℕ → ℝ) (pSeq : ℕ → Fin m → ℝ) (p : Fin m → ℝ)
    (hh : Tendsto hSeq atTop (nhdsWithin 0 (Set.Ioi 0)))
    (hp : Tendsto pSeq atTop (nhds p))
    (hpCube : InCube a b p) (hpMin : AtMinSlice p t)
    (j : Ffinal.family.Index)
    (hactive : ∀ᶠ n in atTop,
      Active Ffinal.family.label j (hSeq n) (pSeq n)) :
    ∀ i, |p i - (Ffinal.family.label j).slope i| <
      E (Ffinal.family.label j).slope := by
  classical
  let jbase : Ffinal.family.Index := A.carry PUnit.unit
  have hbase : Ffinal.family.label jbase = baselineLabel t := by
    change Ffinal.family.label (A.carry PUnit.unit) = baselineLabel t
    calc
      Ffinal.family.label (A.carry PUnit.unit) =
          (baseBoxFamily hat htb).family.label PUnit.unit := A.carryLabels PUnit.unit
      _ = baselineLabel t := rfl
  rcases A.covers j with hInitial | ⟨R, hR, x, hx⟩
  · rcases hInitial with ⟨j0, hj0⟩
    have hbaseTarget : Ffinal.family.label j = baselineLabel t := by
      calc
        Ffinal.family.label j = Ffinal.family.label (A.carry j0) :=
          congrArg Ffinal.family.label hj0.symm
        _ = (baseBoxFamily hat htb).family.label j0 := A.carryLabels j0
        _ = baselineLabel t := by cases j0; rfl
    have htargetActive : ∀ᶠ n in atTop,
        Active Ffinal.family.label j (hSeq n) (pSeq n) := hactive
    have hbaseLocal := baseline_label_local_approximation A.first j hbaseTarget
      hSeq pSeq p htargetActive hh hp hpMin hE
    intro i
    have hcubeBase : InCube a b (fun _ : Fin m => t) := by
      intro _
      exact ⟨hat, htb⟩
    have hslope : (Ffinal.family.label j).slope = (fun _ : Fin m => t) := by
      rw [hbaseTarget]
      rfl
    simpa [hslope] using hbaseLocal i
  · have hcandidateEq : Ffinal.family.label (R.stageMap x) =
        Ffinal.family.label j := by
      exact congrArg Ffinal.family.label hx
    let S := R.system
    let G := stageFamily S (Nat.le_of_lt R.hkm) hat htb (le_of_lt R.hβt)
    let e : Fin R.k ↪ Fin m := x.1
    let jlocal : (S.input e).family.Index := x.2
    have hxIndex : stageIndex S (Nat.le_of_lt R.hkm) hat htb
          (le_of_lt R.hβt) e jlocal = x := by
      cases x with
      | mk e' j' => rfl
    have htargetLabel : Ffinal.family.label j =
        liftLabel t R.β e ((S.input e).family.label jlocal) := by
      calc
        Ffinal.family.label j = Ffinal.family.label (R.stageMap x) :=
          congrArg Ffinal.family.label hx.symm
        _ = G.family.label x := R.stageLabels x
        _ = G.family.label (stageIndex S (Nat.le_of_lt R.hkm) hat htb
              (le_of_lt R.hβt) e jlocal) := by rw [hxIndex]
        _ = liftLabel t R.β e ((S.input e).family.label jlocal) :=
          stageIndex_label S (Nat.le_of_lt R.hkm) hat htb
            (le_of_lt R.hβt) e jlocal
    let localMap : (S.input e).family.Index ↪ Ffinal.family.Index :=
      (stageIndex S (Nat.le_of_lt R.hkm) hat htb (le_of_lt R.hβt) e).trans R.stageMap
    have hlocalMap : ∀ u, Ffinal.family.label (localMap u) =
        liftLabel t R.β e ((S.input e).family.label u) := by
      intro u
      calc
        Ffinal.family.label (localMap u) = G.family.label
            (stageIndex S (Nat.le_of_lt R.hkm) hat htb (le_of_lt R.hβt) e u) :=
          R.stageLabels _
        _ = liftLabel t R.β e ((S.input e).family.label u) :=
          stageIndex_label S (Nat.le_of_lt R.hkm) hat htb (le_of_lt R.hβt) e u
    have hactiveMap : ∀ᶠ n in atTop,
        Active Ffinal.family.label (localMap jlocal) (hSeq n) (pSeq n) := by
      filter_upwards [hactive] with n hn
      have hsame : Ffinal.family.label (localMap jlocal) = Ffinal.family.label j := by
        calc
          Ffinal.family.label (localMap jlocal) = G.family.label
              (stageIndex S (Nat.le_of_lt R.hkm) hat htb
                (le_of_lt R.hβt) e jlocal) := R.stageLabels _
          _ = G.family.label x := by rw [hxIndex]
          _ = Ffinal.family.label (R.stageMap x) := (R.stageLabels x).symm
          _ = Ffinal.family.label j := hcandidateEq
      change ∀ u, value (Ffinal.family.label (localMap jlocal))
        (hSeq n) (pSeq n) ≤ value (Ffinal.family.label u) (hSeq n) (pSeq n)
      intro u
      rw [hsame]
      exact hn u
    cases R.following with
    | terminal hkmTerminal =>
        have hposE : 0 < E (Ffinal.family.label (localMap jlocal)).slope :=
          hE (Ffinal.family.label (localMap jlocal)).slope
            (Ffinal.slope_box (localMap jlocal))
        have hposELocal : 0 < E
            (liftLabel t R.β e ((S.input e).family.label jlocal)).slope := by
          rw [← hlocalMap jlocal]
          exact hposE
        have happrox := stage_local_approximation_of_terminal_stage
          S e Ffinal.family localMap hlocalMap jlocal jbase hbase R.hβt
          hkmTerminal hposELocal hSeq pSeq p hh hp hpCube hpMin hactiveMap
        simpa [htargetLabel] using happrox
    | next hkmNext q hqt hqUpper hmargin Snext nextMap nextLabels =>
        let nextFamily := stageFamily Snext (Nat.le_of_lt hkmNext)
          hat htb (le_of_lt hqt)
        let nextLabelMap : ∀ f : Fin (R.k + 1) ↪ Fin m,
            (Snext.input f).family.Index ↪ Ffinal.family.Index := fun f =>
          (stageIndex Snext (Nat.le_of_lt hkmNext) hat htb
            (le_of_lt hqt) f).trans nextMap
        have hnextLabelMap : ∀ (f : Fin (R.k + 1) ↪ Fin m) u,
            Ffinal.family.label (nextLabelMap f u) =
              liftLabel t q f ((Snext.input f).family.label u) := by
          intro f u
          calc
            Ffinal.family.label (nextLabelMap f u) = Ffinal.family.label
                (nextMap (stageIndex Snext (Nat.le_of_lt hkmNext) hat htb
                  (le_of_lt hqt) f u)) := by
              rfl
            _ = nextFamily.family.label
                (stageIndex Snext (Nat.le_of_lt hkmNext) hat htb
                  (le_of_lt hqt) f u) := nextLabels _
            _ = liftLabel t q f ((Snext.input f).family.label u) :=
              stageIndex_label Snext (Nat.le_of_lt hkmNext) hat htb
                (le_of_lt hqt) f u
        have hmarginCandidate : q - t <
            E (liftLabel t R.β e ((S.input e).family.label jlocal)).slope := by
          have hmarg := hmargin
            (appendRightIndex R.previous G
              (stageIndex S (Nat.le_of_lt R.hkm) hat htb
                (le_of_lt R.hβt) e jlocal))
          simpa [G, stageIndex_label] using hmarg
        have happrox := stage_local_approximation_of_next_stage
          S Snext e Ffinal.family localMap hlocalMap nextLabelMap hnextLabelMap
          jlocal jbase hbase hqUpper hqt hmarginCandidate hSeq pSeq p
          hh hp hpCube hpMin hactiveMap
        simpa [htargetLabel] using happrox

end N33Affine
