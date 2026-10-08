import N33Affine.AffineInduction
import N33Affine.B2GluePlacement
import N33FiniteGlue

noncomputable section
open Filter Topology Set

namespace N33Affine

/-- The full arbitrary-tolerance affine approximation statement by dimension
induction, local slice construction, and ordered finite gluing. -/
theorem exists_full_affine_family :
    ∀ m (a b : ℝ) (E : (Fin m → ℝ) → ℝ), a ≤ b →
      (∀ r, InCube a b r → 0 < E r) →
      ∃ F : BoxFamily m a b,
        FamilyLittleOAt F a ∧ FullApproximation a b E F.family := by
  intro m
  induction m using Nat.strong_induction_on with
  | h m ih =>
      intro a b E hab hE
      by_cases hmzero : m = 0
      · subst m
        let F : BoxFamily 0 a b := baseBoxFamily (m := 0) le_rfl hab
        refine ⟨F, ?_, ?_⟩
        · intro j
          exact littleO_zero_bump a
        · intro j hSeq pSeq p hh hp hpCube hactive i
          exact Fin.elim0 i
      · have hm : 0 < m := Nat.pos_of_ne_zero hmzero
        have OracleHyp : ∀ k, 0 < k → k < m → ∀ β, β < b →
            ∀ E₀ : (Fin k → ℝ) → ℝ,
              (∀ s, InCube β b s → 0 < E₀ s) →
              ∃ F : BoxFamily k β b,
                FamilyLittleOAt F β ∧ FullApproximation β b E₀ F.family := by
          intro k hk hkm β hβb E₀ hE₀
          exact ih k hkm β b E₀ (le_of_lt hβb) hE₀
        let W : ∀ t : Set.Icc a b, LocalWindowData a b E (t : ℝ) := fun t =>
          Classical.choice
            (exists_local_window_of_lower_dimensions hm t.property.1 t.property.2
              OracleHyp hE)
        let radiusAt : Set.Icc a b → ℝ := fun t => (W t).radius
        have hradiusAt : ∀ t, 0 < radiusAt t := fun t => (W t).radius_pos
        obtain ⟨S, hScover, hSpruned⟩ :=
          exists_finite_pruned_interval_cover hab radiusAt hradiusAt
        have hSnonempty : S.Nonempty := by
          obtain ⟨t, ht, _⟩ := hScover a le_rfl hab
          exact ⟨t, ht⟩
        let Selected : Type := {t : Set.Icc a b // t ∈ S}
        letI : Fintype Selected := Fintype.ofFinite Selected
        have hSelectedNonempty : Nonempty Selected := by
          obtain ⟨t, ht, _⟩ := hScover a le_rfl hab
          exact ⟨⟨t, ht⟩⟩
        let N : ℕ := Fintype.card Selected
        have hN : 0 < N := by
          dsimp [N]
          exact Fintype.card_pos_iff.mpr hSelectedNonempty
        let order : Fin N ≃o Selected := Fintype.orderIsoFinOfCardEq Selected rfl
        let centers : Fin N → ℝ := fun j => ((order j).val : ℝ)
        let radii : Fin N → ℝ := fun j => radiusAt (order j).val
        let gammas : Fin N → ℝ := fun j => (W (order j).val).gamma
        let families : Fin N → FiniteFamily m := fun j => (W (order j).val).family.family
        have hcenterBox : ∀ j, a ≤ centers j ∧ centers j ≤ b := by
          intro j
          exact (order j).val.property
        have hradii : ∀ j, 0 < radii j := by
          intro j
          exact hradiusAt (order j).val
        have hcenterOrder : ∀ i j : Fin N, i.val < j.val → centers i < centers j := by
          intro i j hij
          have hij' : order i < order j := order.strictMono hij
          exact hij'
        have hpruned : Glue.Pruned centers radii := by
          intro i j hij hsub
          have hneq : (order i).val ≠ (order j).val := by
            intro heq
            apply hij
            exact order.injective (Subtype.ext heq)
          have hpr := hSpruned (order i).val (order i).property
            (order j).val (order j).property hneq
          apply hpr
          simpa [Glue.leftEnd, Glue.rightEnd, centers, radii, radiusAt] using hsub
        have hcover : ∀ x, a ≤ x → x ≤ b →
            ∃ j : Fin N, Glue.leftEnd centers radii j < x ∧
              x < Glue.rightEnd centers radii j := by
          intro x hax hxb
          obtain ⟨t, htS, hxt⟩ := hScover x hax hxb
          let y : Selected := ⟨t, htS⟩
          obtain ⟨j, hj⟩ := order.surjective y
          have hcenter : centers j = (t : ℝ) := by
            dsimp [centers]
            have hv : (order j).val = t := congrArg Subtype.val hj
            exact congrArg (fun u : Set.Icc a b => (u : ℝ)) hv
          have hradius : radii j = radiusAt t := by
            dsimp [radii]
            have hv : (order j).val = t := congrArg Subtype.val hj
            rw [hv]
          refine ⟨j, ?_⟩
          simpa [Glue.leftEnd, Glue.rightEnd, hcenter, hradius] using hxt
        obtain ⟨q, hcuts, hcutOrder, hfirst, hlast⟩ :=
          Glue.exists_cover_gluing_data a b N hN centers radii
            hcenterBox hradii hcenterOrder hpruned hcover
        have hplacementCuts : ∀ k (hk : k + 1 < N),
            centers ⟨k, by omega⟩ < q k ∧
            q k < centers ⟨k + 1, hk⟩ ∧
            q k < gammas ⟨k, by omega⟩ := by
          intro k hk
          have hc := hcuts k hk
          refine ⟨hc.1, hc.2.2.1, ?_⟩
          have hr := hc.2.2.2
          change q k < centers ⟨k, by omega⟩ + radii ⟨k, by omega⟩ at hr
          exact lt_trans hr (W (order ⟨k, by omega⟩).val).window_lt_gamma
        have hfloor : ∀ j k i, centers j ≤ ((families j).label k).slope i := by
          intro j k i
          exact (W (order j).val).slope_floor k i
        have hbumps : ∀ j k, LittleO ((families j).label k).bump (gammas j) := by
          intro j k
          exact (W (order j).val).offsets_small k
        have hbase : ∀ j, ∃ k, (families j).label k = baselineLabel (centers j) := by
          intro j
          obtain ⟨k, hk⟩ := (W (order j).val).has_baseline
          exact ⟨k, by simpa [centers] using hk⟩
        let F : FiniteFamily m := GluePlacement.shiftedUnion families q hN
        have hbox : ∀ j, InCube a b (F.label j).slope := by
          rintro ⟨j, k⟩
          change InCube a b ((families j).label k).slope
          exact (W (order j).val).family.slope_box k
        let Fbox : BoxFamily m a b := ⟨F, hbox⟩
        have hlocalRadius : ∀ j k,
            LittleO ((families j).label k).bump (centers j + radii j) := by
          intro j k
          have h := (W (order j).val).offsets_small k
          apply littleO_lower_exponent h
          exact (W (order j).val).window_lt_gamma
        have hsmallGlue : ∀ j k,
            LittleO ((Glue.gluedFamily families q hN).label ⟨j, k⟩).bump a :=
          Glue.gluedFamily_offsets_littleO_of_cover a b N hN centers radii families q
            hcenterBox hradii hcuts hlocalRadius
        have hsmall : FamilyLittleOAt Fbox a := by
          intro x
          rcases x with ⟨j, k⟩
          exact hsmallGlue j k
        have hLocal : Glue.LocalNeighborhoodGuarantee a b E
            (fun j k => (families j).label k)
            (Glue.leftEnd centers radii) (Glue.rightEnd centers radii) := by
          intro j k hSeq pSeq p s hh hp hpCube hslice hslo hshi hactive
          exact (W (order j).val).neighborhood k hSeq pSeq p s hh hp hpCube
            hslice hslo hshi hactive
        have hFull : FullApproximation a b E F := by
          intro tag hSeq pSeq p hh hp hpCube hactive
          rcases tag with ⟨j, k⟩
          have hminIndex : (Finset.univ : Finset (Fin m)).Nonempty :=
            Finset.univ_nonempty_iff.mpr ⟨⟨0, hm⟩⟩
          obtain ⟨i0, hi0, hmin⟩ :=
            Finset.exists_min_image (Finset.univ : Finset (Fin m)) p hminIndex
          let s : ℝ := p i0
          have hslice : AtMinSlice p s := by
            refine ⟨?_, ⟨i0, rfl⟩⟩
            intro i
            exact hmin i (Finset.mem_univ i)
          change ∀ᶠ n in atTop,
            Active (GluePlacement.shiftedUnion families q hN).label ⟨j, k⟩
              (hSeq n) (pSeq n) at hactive
          have hslab := GluePlacement.active_minimum_in_slab a b hN
            centers gammas families q hcenterBox
            (fun j => (W (order j).val).center_lt_gamma)
            hplacementCuts hfloor hbumps hbase j k hSeq pSeq p s hh hp
            hpCube hslice hactive
          have hactiveLocal : ∀ᶠ n in atTop,
              Active (Glue.taggedLabels (fun j k => (families j).label k) q)
                ⟨j, k⟩ (hSeq n) (pSeq n) := by
            filter_upwards [hactive] with n hn
            exact hn
          intro i
          exact Glue.finite_family_active_label_inherits_from_cut_slab
            a b E families q centers radii hN hfirst hlast hcuts hLocal
            j k hSeq pSeq p s hh hp hpCube hslice hslab.1 hslab.2 hactiveLocal i
        exact ⟨Fbox, hsmall, hFull⟩

end N33Affine
