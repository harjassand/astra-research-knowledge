# Independent audit: full canonical traces and valid removals

**Reviewer task:** `producer-workspace/audit_component_contour_proof`  
**Date:** 2026-11-02  
**Reviewed file:** `FULL_TRACE_REMOVABLE_EXTENSION.md`  
**SHA-256:** `6e1fec2cebdfa4bc70f0c74596be94e9afce6aff72e93a1288aacee1a143288e`

## Verdict

I found no fatal counterexample under the explicit retained hypotheses and F1–F4. The new restriction-before-rerun argument supplies the validity interface that was not supplied by syndrome contraction alone. The result remains a conditional abstract theorem: it does not establish these interfaces for the actual family or prove the native Gibbs ratio.

In particular, the local-ratio probability argument does not require the removed syndrome to regenerate the same witness, and it does not claim a polymer bijection. Those would be unnecessarily strong requirements for the stated union bound.

## 1. Restriction is algebraic and noncircular

For any whole connected-component union A of one recorded full trace, consider a residual row on the actual recorded history. F2 puts all its actual nonzero operands in one trace component. Restricting to A therefore either retains every nonzero term of that row or removes all of them. The row remains satisfied in both cases. Zero operands do not affect this argument.

The reasoning is performed on an already computed valid history. It never invokes the decoder on the restricted input before establishing validity. The fixed terminal bag then makes the terminal restriction either the full original terminal syndrome/correction or the zero pair. Consequently the restricted local equations telescope to an actual physical correction with boundary tau_A. This proves tau_A is a valid syndrome. Since it is a support restriction of the original syndrome, the complement is valid as well.

This proof uses the strong, explicit F2 condition on **every row containing a nonzero computed operand**, with all variable species and their identities recorded. A statement merely asserting a global chain identity or bounded stencils without joining the actual nonzero operands would not suffice. The extension explicitly requires the stronger condition. Distinct variable species at a geometric site should be understood as distinct tagged vertices/ports of the fixed ambient graph; bounded local type multiplicity changes constants only.

## 2. Zero activation is not needed for equation closure

One need not activate every row incident to an incidental zero vertex. Any row whose actual operands are all zero remains satisfied after restriction. Every row with a nonzero operand is handled by F2. Thus adding the finite stencils incident to the charged nonzero variables can supply the necessary row connections without iterating indefinitely through zeros.

F3 remains essential as a geometric assumption: it rules out a canonical construction that recursively fills an arbitrarily long zero path, or includes an uncharged component of the full ambient graph. The proof does not derive F3 from contraction. Zero-valued intersections may merge charged trace components, but their merged size is still bounded by the sum of their charged input masses.

## 3. Selected full-component unions have the claimed mass recurrence

A selected occupied upper input belongs to a complete selected packet block. Its producer connections lead to its whole lower owner component in the same trace component union. Therefore the already audited whole-owner recurrence applies to the selected union, not merely to the total history. The entire selected union has size O(selected base charge), including terminal-bag overhead when present.

Residual-row edges may merge more components than output ancestry alone would merge; this only enlarges the selected union. All its newly selected upper inputs require their own ancestors, so the recurrence acquires no uncharged additive source.

## 4. Constructive removal follows after validity

Once Section 3 proves validity, F1 permits an actual rerun on the complement. Each removed trace union contains entire layer input components. Deletion stability leaves the remaining component decisions unchanged, while complete output-block ownership prevents partial nonlinear block removal. Induction proceeds layer by layer. The finite terminal decoder sees either its unchanged original input or zero, so D_r(0)=0 closes this induction.

This would fail for a globally enumeration-dependent component rule or a graph construction that recursively activates zeros. Such cases violate F1/F3 rather than refute the conditional proof.

The constructive decoder-removal result is stronger than what Section 7 needs. For that probability estimate, algebraic validity of tau and the stated local-ratio inequality already suffice. This distinction is stated correctly in the extension.

## 5. The two-run root union is removable and honestly charged

A connected component of the graph formed by joining two full traces intersects each run in a union of entire components of that run. Otherwise an edge in the original connected trace component would leave the purported union component. Hence the original-run base subset tau is valid by the one-run restriction argument.

At an initially occupied check outside the fault set, both runs contain that check and its matching-site edge. If one copy is in the root union, the other is too. Thus tau and tau' differ only on the at-most-k fault checks, which gives |tau'| <= |tau|+k. Combining this with Q<=c Hamming and the selected-union recurrence gives |W|<=C(|tau|+k), not a fictitious two-sample probability charge.

The explicit causal attachment premise ensures every changed component/correction lies in the root union. Whole-trace completion may bring in unchanged components as well, but the size accounting already pays for them. No bounded influence radius is assumed.

## 6. Height and correction support

Using the greatest level of a selected **occupied input** avoids incorrectly charging ancestry to a zero-valued high stencil vertex. An occupied level-h block has positive charge and forces at least 2^h base charge in one run. The original-run leaf count then differs by at most the fault allowance.

If no occupied selected input reaches h, with h<=r, the root union contains no nonzero differing terminal input or correction. All lower correction differences are supported in their charged selected shapes. Common fixed lifts give the stated S_h(K) support estimate, and distance yields the second lower bound on |tau|.

The optional geometric-height restatement is valid only with the stated uniform stencil-height offset. A bounded number of vertices alone would not bound scale displacement if arbitrary long-level edges were allowed; the occupied-height formulation does not need that inference.

## 7. The native local-ratio consumer is a valid injection argument

Fix a valid candidate tau. On any subset E of valid syndromes containing its support, the map sigma -> sigma+tau is injective and has valid image. Therefore

    sum_(sigma in E) pi(sigma)
      <= z^|tau| sum_(sigma in E) pi(sigma+tau)
      <= z^|tau|.

It is immaterial whether the image still realizes the same trace witness. No equality of witness events, reverse insertion map, or polymer compatibility statement is needed. The original event has already provided a fixed valid tau and bounded-size rooted witness. Enumerating candidate rooted animals and marked tau subsets costs exponentially in |tau|+O(k); applying the injection separately to each valid candidate gives the claimed convergent union bound for sufficiently small z.

The ratio must really hold for every fixed valid tau and every valid containing sigma used by this argument, or for a precisely stated class that includes these trace-restriction witnesses. Its status is explicitly an external consumer hypothesis, not a consequence of F1–F4.

## Scope of sign-off

The conditional proof is internally consistent under its strong stated interfaces. No full-family conclusion follows until the actual residual equations, bounded charged row stencils, deletion-stable owner closure, terminal bag, common lifts, and native ratio are verified. No hard-core polymer representation has been established or is needed here.
