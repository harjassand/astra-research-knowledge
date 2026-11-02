# Explicit ell=8: central-cube cleanup certificate

Status: a proved local mechanism in the actual unperturbed interior of the Section 6 doubling unit; **not** a completed lifetime proof, and not a claim that all downstream host hypotheses hold.

Primary source: Balasubramanian–Davydova–Lin, arXiv:2605.10943v1, Sections 2.4, 6.2.2 (Example 6.5/Figure 14), 6.2.3, 6.2.6. Download retained as source.html. The source's explicit construction is different from its proven random-embedding family. No certificate is transferred between those families.

## Actual operation used

The flat square is refined to 8 by 8. Its translated copy is displaced by (1,1,1). Attaching bands occupy x=4,5 and y=4,5, with their intersections identified. In X doubling the new degree-3 and degree-4 junctions carry repetition sheaves. In Z doubling they carry parity sheaves. Perturbations are confined near the inherited boundaries; the central rib pattern persists.

## Lemma: blue central cube can be cleaned without increasing final syndrome weight

The region [4,5] x [4,5] x [0,1] has six physical faces: bottom b, top t, and four sides s_1,...,s_4. Let C denote these six face-syndrome bits. Their sum mod 2 is a metacheck. Indeed every edge incident on C has either zero or two incident C faces. A blue repetition generator flips every incident face; its overlap with C is therefore even, including at a vertical degree-4 junction. Ordinary degree-2 generators also have even overlap. Consequently every globally valid coboundary syndrome restricts to an even-weight pattern on C. This is a local metacheck, not a conjectured large-scale confinement law.

Use only the eight horizontal cube edges. The generator at the b/s_j edge flips b+s_j+u_j; the generator at the t/s_j edge flips t+s_j+v_j. Here u_j and v_j are the exterior sheet faces adjacent to that edge. These are actual source-geometry repetition-sheaf correction columns, not newly introduced couplings.

The graph on C supplied by these generators is K_{2,4}, of diameter two. Pair the occupied central faces deterministically. Join each pair by a shortest path in K_{2,4} and apply its edge generators. Internal path vertices cancel. Every pair of central defects disappears and produces at most two exterior defects. Hence all C syndrome can be removed with final exterior weight at most its original central weight. In the presence of arbitrary pre-existing exterior syndrome eta,

    |eta + deposited| <= |eta| + |deposited| <= |eta| + |sigma restricted to C|.

Thus cleanup is weight-nonincreasing at completion. Intermediate individual Pauli moves need not be weight-nonincreasing; that is not needed for a mathematical coarse-graining decoder.

The finite script exhausts all 32 admissible central syndromes and all 256 subsets of these eight physical edge generators, choosing a canonical minimum-output-weight correction. Every case passes. It uses no stochastic sampling or assumed coarse map.

## Why this is the two-rib mechanism

All noncentral sheet regions in the flat unit reach an outer collar. The open rib-arm face strips do too. Within a degree-2 connected region, pair flips permit transportation/cancellation to an anchor in that collar without increasing final weight. The only bounded interior face components isolated by blue rib junctions are the six central faces. Their exact metacheck supplies the pairing needed above. This explains a genuine route for the source's claimed interior cleanup, rather than an independent barrier argument.

This argument does NOT yet handle the boundary perturbation gadgets, inherited red/blue seams, or the identification of collar syndrome with the chosen coarse embedding map.

## Decisive local test for witness restriction

The even syndrome b+t is admissible: apply the two horizontal edge generators through any side s_j; they produce b+t+u_j+v_j, so with those exterior faces it is an actual coboundary. Restricting this valid syndrome to a proposed witness component containing b but not the other three support faces can yield a singleton b, which violates the cube metacheck and cannot be a coboundary. Thus spatial/face connectivity alone is not a removable-witness criterion. A dependency graph must include all relevant cleanup dependencies (or explicit metacheck closure), so that a component restriction remains admissible. This is a test against the actual removable-syndrome step of the source's strongest route, NOT a no-go for the actual family or its proposed decoder.

A simple local fix is to place the six central faces and the eight exterior output faces in one constant-size dependency bag. The canonical table above depends on all six input bits, vanishes on zero, and has support in that bag. Such bags preserve constant-degree witness counting. Full component compatibility still requires the boundary schedule and coarse-map identity below.

## Exact remaining gates

1. Supply actual chain/cochain maps for all Section 6 refinement/doubling gadgets, including degree-4 crossings, coincident sheets, and degenerate triangular/pentagonal boundary cells; establish cohomology preservation and bounded support.
2. Give a finite-depth boundary cleaning schedule that glues the flat-unit certificates without spending syndrome weight twice. The invariant must include arbitrary *admissible* boundary traces, not only isolated clean-boundary units.
3. Prove residual collar syndrome equals the image of a legitimate coarse syndrome, and establish per-step contraction 1/2 in X doubling, 1 in Z doubling, **componentwise**, together with the chain-map correction identity.
4. Establish the decoder's single-qubit stability trigger and removable witness construction, not merely global syndrome contraction.
5. Analyze actual Z errors. Section 2.4's Theorem 2.2 gives sheaf duality for logical/code/expansion/decoder data; immediately after Eq.44, lifetime extension is described as expected. Section 6 invokes this duality in its sketch. A bounded-local chain-homotopy transfer retaining physical syndrome weights and witness removability, or a direct transposed decoder proof, is still needed here. This observation is confined to the explicit Section 6 route; it does not impugn the separate random-family CSS proofs.
6. Polynomial distance and polynomial local stabilizer filling for this same explicit family must separately be established before invoking the earned native-host construction.

## Scope

The local certificate is useful positive progress: it establishes the essential even-parity paired evacuation of the central cage and shows exactly how to include it in a bounded dependency graph. It does not earn an exponential lifetime, a practical complete memory architecture, or a perturbatively protected physical host by itself.

## Red-junction interior variant

For the same central cube in a red doubling, a degree-3 edge's parity sheaf allows any even pair of its incident faces. Thus the horizontal edge supports b+s_j and b+u_j (or t+s_j and t+v_j) as separate permitted syndrome columns. All six central faces can be connected to a fixed outside face through these pair columns. Routing each central defect to that fixed face removes all central syndrome and leaves at most one exterior defect, with no admissibility parity assumption. This is a direct local sheaf-cochain statement, not a transfer to physical Z errors by assumed lifetime duality.

## Dependency representation that makes the local certificate safe

Implement the central table as one deterministic gate with six input face bits, eight possible output faces, and eight correction bits. Give this gate one bounded-size dependency bag containing its entire support. If it fires, mark its full bag, including zero-syndrome sites. Adjacent active bags that overlap are joined. Restricting a syndrome to a connected component then either retains all nonzero inputs to this gate or none: the canonical rule is unchanged in the first case and outputs zero in the second. This is the relevant component compatibility, not naive connectivity of occupied syndrome faces.

More generally this construction works for a bounded-depth bounded-arity deterministic cleaning circuit, with bounded local neighborhood size. The number of marked bags is bounded by a constant times the number of nonzero input bits: zero-preservation plus bounded light cones provides a charging map to those inputs. Therefore this representation would retain a Peierls entropy bound once the *actual* full-gadget circuit satisfies the coarse correction identity and componentwise contraction. It does not prove those pending identities.

## Sharp local budget test, not a family no-go

`full_cube_edge_test.py` additionally enumerates all 4096 subsets of the **twelve** physical blue cube-edge generators. The four vertical edges each flip two central side faces and two exterior rib-arm faces. The admissible pattern consisting of all four central side faces has minimum exterior output weight exactly four under this full edge-star correction set. All six occupied cube faces have minimum exterior output weight four. Thus central evacuation has no universal factor-two slack. The source only promises nonincrease at this stage, so this does not refute it; it identifies a sharp test any complete boundary schedule must respect. Spending extra defects at inherited seams cannot be charged to a nonexistent strict interior contraction. Corrections farther out in the collar are not included in this optimization, so the lower bound is not asserted for a full gadget or full code decoder.

## Scope amendment: alternate product-Gibbs probability bound

Root subsequently supplied a valid alternative: any binary-linear syndrome space with restricted product Gibbs weights obeys Pr(T occupied)≤∏_{i∈T}q_i even when T itself is not a valid syndrome. See independently verified `PRODUCT_GIBBS_ALTERNATIVE.md`. Thus the singleton-metacheck example above blocks a removable-component construction, not every commuting Peierls route. Decoder contraction and dependency control still need proof; this alternative does not automatically extend to the native/generically perturbed model.
