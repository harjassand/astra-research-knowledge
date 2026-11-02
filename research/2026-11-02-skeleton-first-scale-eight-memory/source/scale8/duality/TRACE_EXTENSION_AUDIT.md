# Independent audit of the joined removable-trace transfer

2026-11-02. Reviewed `REMOVABLE_TRACE_EXTENSION.md` together with `producer-workspace/FULL_TRACE_REMOVABLE_EXTENSION.md` and its retained `THEOREM.md`. Coordinated a fresh abstract-interface review with `producer-workspace/audit_component_contour_proof`.

## Verdict

**The joined conditional proof passes.** It establishes a physical valid-removal witness, without any all-subsets local-stochastic hypothesis, provided the full-trace F1–F4 interfaces and the retained charge/causality/lift assumptions actually hold. It is not actual-family admission. The native Gibbs ratio and the dynamical thermal theorem remain separate premises.

Two implementation details should be made explicit in the joined presentation:

1. Matching-site edges between the two runs apply to the **entire augmented trace, especially physical base leaves**, not just the dual trace. This is needed for the original/perturbed physical-leaf mass comparison. The abstract companion already states full matching; apply that convention after augmentation.
2. The bounded root joins the original physical fault-check set `supp(d_A e)` and all needed dual fault/prepass neighborhoods. Tag different variable species and operand ports even at the same geometric site. Uniformly bounded type multiplicities and fixed local-map radius preserve bounded degree and root cost.

These clarify the existing sufficient interpretation rather than repair a failed algebraic identity.

## 1. Bottom cancellation rows are essential and sufficient

For an occupied physical input s, every occupied contributor to a fixed F² row is connected to that row's gate, including when its XOR is zero. Selecting a union of whole augmented components therefore retains all occupied contributors to each row or none. A nonzero row output is connected to its dual input leaf. Consequently `F²τ=u_C` exactly, where τ is the selected physical occupied input and u_C is the selected original dual input. For a zero-output row its selected sum is still zero. This establishes the relation before asserting either restriction is a valid syndrome.

Joining zero-output gates to already charged dual stencil ports can merge components, but cannot create a partial row selection. It is safe for both algebra and charge accounting. An incidental zero port must not recursively activate further rows or empty components. Every newly included stencil must instead have a bounded charge to an occupied input/nonzero computed variable or an already charged component.

Exhaustive extra test `audit_trace_prepass.py` checks all binary 3×3 maps and inputs and all complete prepass-component selections: **9,726 selections pass**. Its negative control uses `L=[1 1]`, `s=[1 1]`: dropping the zero-output row gate permits selection `[1 0]`, whose image is nonzero although the original dual input was zero.

## 2. Restriction validity is genuinely noncircular

Inside the dual original trace, F2 connects all actual nonzero operands of each residual row. Whole-component restriction therefore retains every nonzero term in that row or none, preserving the row equation. Zero operands stay zero. This uses the computed original history, not a decoder call on an unproved-valid restricted syndrome.

The terminal bag forces the selected terminal input to be the entire original terminal input or zero. Retaining its original terminal correction in the first case and zero in the second closes the telescoping identities. Thus the restricted dual correction r_C satisfies `d_B r_C=u_C` without assuming u_C valid in advance. If correction contributions overlap and cancel, the operand/contributor stencils must record the contributions needed for this restriction argument; merely recording a canceled aggregate variable without its dependencies is not F2.

The joined three-term top-degree identity holds on all A² vectors:

```
I + G² F² = d_A¹ H².
```

It follows that

```
d_A¹(G¹ r_C + H²τ)
  = G² d_B¹r_C + d_A¹H²τ
  = G²F²τ + (I+G²F²)τ
  = τ.
```

This is the physical-validity proof. It does not insert a hidden assumption `τ∈im d_A`, does not require dual Gibbs laws, and does not need the second homotopy. The full homotopy equivalence remains useful for logical equivalence, but this validity step needs only the displayed top-degree identity and the cochain property of G.

A kernel-only prepass component has u_C=0 and physical correction H²τ, so cancellation components are covered rather than discarded. In a longer complex, the omitted H³d_A²τ term would matter; the present proof correctly restricts to a three-term complex with top degree 2.

## 3. Deletion and terminal closure

After physical validity is established, the complement s+τ is valid. The exact prepass relation gives its dual input u+u_C. F1 and complete nonlinear component closure then reproduce the complementary dual run, layer by layer. Whole packet ownership must survive restriction. Component consistency alone is not enough if graph construction or tie-breaking depends on deleted remote data; the additional deletion stability is indispensable and explicitly assumed.

The finite terminal bag is charged whenever it contains nonzero terminal input; its constant size can be paid for by that input. A growing or arbitrarily globally processed terminal problem is outside this argument. Zero-input terminal correction must be zero. No global decoder action may be omitted from the recorded correction/telescoping equations.

## 4. Joined two-run mass and entropy

Construct the root component in two complete augmented traces joined at matching tagged sites, including physical occupied base leaves. Its intersection with either run is a union of entire components of that run. Therefore its original physical leaf set τ is valid by the preceding argument.

Outside the fixed physical fault-check set, the two input bits agree. If an occupied leaf from either run lies in the selected root component, its matching edge selects the other copy too. Hence `supp(τ+τ')⊆supp(d_Ae)` and `|τ'|≤|τ|+k_A`.

For either selected run, `|u_C|≤c_F|τ|`. Selected dual trace mass is bounded by its selected dual base charge, and this charge is uniformly comparable above to input Hamming mass under the retained packet assumptions. The prepass adds O(|τ|) sites. Thus the total root animal has size O(|τ|+k_A), with constants depending only on the fixed interfaces. Selecting larger whole components changes the mass being charged; it does not justify a bound in terms of an earlier ancestor skeleton. The documents make this distinction correctly.

Bounded row/column norms supply bounded prepass degree. Fixed local radius supplies bounded physical root connectors; sparsity alone would not guarantee geometric locality. The terminal bag and bounded stencil/variable types preserve a uniformly bounded-degree fixed ambient graph. Rooted animals plus base-leaf marks then have entropy exponential in |τ|+O(k_A), not in system volume or hierarchy depth.

## 5. Height and physical correction support

Occupied height, rather than the highest incidental zero port, supplies the selected-ancestor lower bound. The bottom F² layer is a constant-cost noncontracting layer; it changes charge comparisons by constants but does not count as an additional halving macrostep. High dual occupied inputs force exponentially many physical leaves after the constant column-weight comparison.

In the low-height case, common higher lifts cancel. Apply G to the already selected lifted dual correction differences algebraically. Its bounded column norm multiplies their physical support bounds by a constant. The physical fault and H discrepancy add bounded support. Thus the same S_h(K) estimate and physical logical distance lower bound apply up to constants. No expanded G-correction support is needed in the animal.

Counting every fully lifted physical G correction as trace sites would be unjustified: a level-i correction can have K^i physical support. The explicit refusal to do so is necessary, not a technical convenience. H may be handled algebraically too; optional H prepass stencils are safe only when they obey the same bounded charge/nonrecursive-zero rules.

## 6. Native ratio endpoint

Fix a candidate physical leaf set τ produced by a witness. Its validity is now proved independently of the Gibbs estimate. On any event requiring `supp(τ)⊆supp(s)`, deletion `s↦s+τ` is injective and stays in the valid syndrome space. The assumed native ratio bounds the event by `z^|τ|`. No preservation of the witness under deletion and no reverse insertion construction are needed for this probability estimate.

For additive nonnegative excitation energies and the corresponding syndrome Gibbs weights, the energy drop is precisely the weight of τ. For a more general native model, the local-ratio statement must be explicitly verified on these particular valid removals; it is not implied by the abstract decoder trace. Frustrated affine spaces, nonadditive energies or arbitrary degeneracy factors are not silently covered.

The exponentially bounded witness enumeration then combines with this per-valid-witness ratio. There is no step asserting inclusion bounds for arbitrary, possibly invalid subsets and no local-stochastic pushforward requirement.

## Scope

No fatal counterexample found under the stated joined hypotheses. The outstanding actual-family checks remain: row identities and operand/contributor stencils; all boundary/junction data; whole packet/component ownership; uniform contraction and lift constants; fixed finite terminal processing; local radius and bounded ambient degree; and native ratio/bath applicability. This audit does not certify those data for ell=8 or establish a polymer bijection.
