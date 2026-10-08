import N33Affine.GlobalAffineComposition

noncomputable section

open Filter Topology Set

namespace N33Affine

/-- Sequential affine approximation is uniform over cube points and labels at
all sufficiently small positive scales. The fixed tolerance is evaluated at a
fixed label slope, so no continuity of `E` is needed. -/
theorem exists_uniform_activity_cutoff
    {m : ℕ} {a b : ℝ} {E : (Fin m → ℝ) → ℝ}
    (F : BoxFamily m a b)
    (hFull : FullApproximation a b E F.family) :
    ∃ hAct : ℝ, 0 < hAct ∧ hAct < 1 ∧
      ∀ h, 0 < h → h < hAct → ∀ p, InCube a b p →
        ∀ j : F.family.Index, Active F.family.label j h p →
          ∀ i, |p i - (F.family.label j).slope i| < E (F.family.label j).slope := by
  classical
  by_contra hNo
  have hBad : ∀ n : ℕ, ∃ h : ℝ, ∃ p : Fin m → ℝ,
      ∃ j : F.family.Index, ∃ i : Fin m,
        0 < h ∧ h < 1 / ((n : ℝ) + 1) ∧ InCube a b p ∧
          Active F.family.label j h p ∧
          E (F.family.label j).slope ≤ |p i - (F.family.label j).slope i| := by
    intro n
    let δ : ℝ := min (1 / ((n : ℝ) + 1)) (1 / 2)
    have hδpos : 0 < δ := lt_min (by positivity) (by norm_num)
    have hδlt1 : δ < 1 := lt_of_le_of_lt (min_le_right _ _) (by norm_num)
    have hNotGood :
        ¬ (∀ h, 0 < h → h < δ → ∀ p, InCube a b p →
          ∀ j : F.family.Index, Active F.family.label j h p →
            ∀ i, |p i - (F.family.label j).slope i| < E (F.family.label j).slope) := by
      intro hGood
      apply hNo
      exact ⟨δ, hδpos, hδlt1, hGood⟩
    push_neg at hNotGood
    obtain ⟨h, hhpos, hhδ, p, hpCube, j, hjactive, i, hbad⟩ := hNotGood
    exact ⟨h, p, j, i, hhpos,
      lt_of_lt_of_le hhδ (min_le_left _ _), hpCube, hjactive, hbad⟩
  choose hSeq pSeq jSeq iSeq hhPos hhSmall hpCube hActive hBadCoord using hBad
  let tag : ℕ → F.family.Index × Fin m := fun n => (jSeq n, iSeq n)
  obtain ⟨tag0, hInf⟩ := Finite.exists_infinite_fiber tag
  have hUnbounded : ∀ N : ℕ, ∃ n > N, tag n = tag0 := by
    intro N
    have hInfSet : {n : ℕ | tag n = tag0}.Infinite := by
      rw [← Set.infinite_coe_iff]
      simpa only [Set.mem_preimage, Set.mem_singleton_iff] using hInf
    obtain ⟨n, hnMem, hn⟩ := Set.Infinite.exists_gt hInfSet N
    exact ⟨n, hn, hnMem⟩
  obtain ⟨φ, hφMono, hφTag⟩ := Nat.exists_strictMono_subsequence hUnbounded
  let hSub : ℕ → ℝ := fun n => hSeq (φ n)
  let pSub : ℕ → Fin m → ℝ := fun n => pSeq (φ n)
  have hEps : Tendsto (fun n : ℕ => (1 : ℝ) / ((n : ℝ) + 1)) atTop (𝓝 0) := by
    simpa using (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ))
  have hZero : Tendsto hSeq atTop (𝓝 0) := by
    apply tendsto_of_tendsto_of_tendsto_of_le_of_le tendsto_const_nhds hEps
    · intro n
      exact (hhPos n).le
    · intro n
      exact (hhSmall n).le
  have hWithin : Tendsto hSeq atTop (𝓝[>] 0) := by
    apply tendsto_nhdsWithin_iff.mpr
    refine ⟨hZero, Filter.Eventually.of_forall ?_⟩
    exact hhPos
  have hSubWithin : Tendsto hSub atTop (𝓝[>] 0) := by
    dsimp [hSub]
    exact hWithin.comp hφMono.tendsto_atTop
  have hCubeCompact : IsCompact {p : Fin m → ℝ | InCube a b p} := by
    have hset : {p : Fin m → ℝ | InCube a b p} =
        Set.Icc (fun _ : Fin m => a) (fun _ => b) := by
      ext p
      constructor
      · intro hp
        constructor
        · intro i
          exact (hp i).1
        · intro i
          exact (hp i).2
      · intro hp i
        exact ⟨hp.1 i, hp.2 i⟩
    rw [hset]
    exact isCompact_Icc
  have hpSubCube : ∀ n, pSub n ∈ {p : Fin m → ℝ | InCube a b p} := by
    intro n
    change InCube a b (pSub n)
    exact hpCube (φ n)
  obtain ⟨p₀, hp₀Cube, ψ, hψMono, hpSubTendsto⟩ :=
    hCubeCompact.tendsto_subseq hpSubCube
  let hFinal : ℕ → ℝ := fun n => hSub (ψ n)
  let pFinal : ℕ → Fin m → ℝ := fun n => pSub (ψ n)
  have hFinalWithin : Tendsto hFinal atTop (𝓝[>] 0) := by
    dsimp [hFinal]
    exact hSubWithin.comp hψMono.tendsto_atTop
  have pFinalTendsto : Tendsto pFinal atTop (𝓝 p₀) := by
    dsimp [pFinal, pSub]
    exact hpSubTendsto
  have hFinalActive : ∀ᶠ n in atTop,
      Active F.family.label tag0.1 (hFinal n) (pFinal n) := by
    filter_upwards [] with n
    have htag := hφTag (ψ n)
    have hj : jSeq (φ (ψ n)) = tag0.1 := congrArg Prod.fst htag
    simpa [hFinal, hSub, tag, hj] using hActive (φ (ψ n))
  have hp₀Cube' : InCube a b p₀ := hp₀Cube
  have hApprox := hFull tag0.1 hFinal pFinal p₀ hFinalWithin pFinalTendsto hp₀Cube' hFinalActive tag0.2
  have hBadTendsto : Tendsto
      (fun n => |pFinal n tag0.2 - (F.family.label tag0.1).slope tag0.2|)
      atTop (𝓝 |p₀ tag0.2 - (F.family.label tag0.1).slope tag0.2|) := by
    have hEval : Tendsto (fun n => pFinal n tag0.2) atTop (𝓝 (p₀ tag0.2)) :=
      (continuous_apply tag0.2).continuousAt.tendsto.comp pFinalTendsto
    exact (continuous_abs.comp (continuous_id.sub continuous_const)).continuousAt.tendsto.comp hEval
  have hBadEventually : ∀ᶠ n in atTop,
      E (F.family.label tag0.1).slope ≤
        |pFinal n tag0.2 - (F.family.label tag0.1).slope tag0.2| :=
    Filter.Eventually.of_forall fun n => by
        have htag := hφTag (ψ n)
        have hj : jSeq (φ (ψ n)) = tag0.1 := congrArg Prod.fst htag
        have hi : iSeq (φ (ψ n)) = tag0.2 := congrArg Prod.snd htag
        simpa [hFinal, hSub, pFinal, pSub, tag, hj, hi] using hBadCoord (φ (ψ n))
  have hBadLimit :
      E (F.family.label tag0.1).slope ≤
        |p₀ tag0.2 - (F.family.label tag0.1).slope tag0.2| :=
    isClosed_Ici.mem_of_tendsto hBadTendsto hBadEventually
  have hStrict := hApprox
  exact (not_lt_of_ge hBadLimit hStrict)

end N33Affine
