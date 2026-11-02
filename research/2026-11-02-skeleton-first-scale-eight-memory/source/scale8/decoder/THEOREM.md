# Componentwise contraction implies a consequential decoder threshold

## Main result

There is no need to make the smaller-sheet choice bounded-radius. It suffices to make it **component-consistent**, and to charge its entire connected active component. The resulting witness is a connected animal in space–scale, not a bounded-arity computation tree.

Here is a precise sufficient abstract theorem. Constants below are independent of system size and depth.

1. **Fixed ambient geometry and bounded intermediate costs.** There are levels 0,...,r, with one contraction macrostep per level. Each macrostep has a uniformly bounded number of layers, consisting of a halving layer and nonincreasing layers. Their relative lift costs are uniformly bounded; K below is measured per complete macrostep. There is one ambient space–scale graph, fixed independently of the syndrome, of uniformly bounded degree, containing every possible component shape, correction enlargement, and spatial/parent–child dependency connector, for every allowed sheet choice. Both forward and reverse dependency multiplicities are bounded. Every nonzero map output has an occupied input dependency (zero preservation), and the connectors have bounded size.
2. **Component charge, output accounting, and correction decomposition.** Each layer partitions its active syndrome into disjoint input components. A component C with m occupied checks has a connected shape, including its fixed enlargement and output attachments, of at most a m sites. The entire layer correction is the sum of its component corrections, each supported in this charged shape; there is no additional syndrome-dependent uncharged correction. Its contributed output support O(C) has size at most m/2 on halving layers and at most m on nonincrease layers. Either outputs have unique ownership, or ancestry selects all relevant contributors so that selected upper occupied inputs are covered by their contributed supports. The bound must hold componentwise before cancellation, not merely after summing all outputs.
3. **Component consistency and causal attachment.** Each layer is a deterministic function of its current syndrome, with no uncharged history state. Identical labeled components produce identical corrections and output. Active-graph changes are local functions of the syndrome. Explicitly, every changed component correction or output can be attached to an incoming discrepancy through the union of the two runs' charged component shapes and bounded connectors. Repeated attachments reach the initial fault neighborhood. A remote global tie-breaking bit is excluded.
4. **Common lifts, exact identities, and distance.** The principal theorem uses fixed lift operators common to both decoder runs. A correction supported on t sites at level i lifts to at most b K^i t physical qubits, K>=1. The chain/cochain identities make
   R_e(s)=e+D(s)+D(s+syndrome(e))
   a zero-syndrome operator. Every nontrivial logical operator has physical weight at least d. The terminal reference decoder is arbitrary but deterministic; identical inputs produce identical terminal corrections. A branch-dependent-lift variant is permitted only if *every* difference caused by lifting a common higher correction has an explicit decomposition into contributions attached to the same selected trace, with total level-i support at most b times its selected input mass and the same lift bound. Existence of a local homotopy identity alone is not this support hypothesis.
5. **Local perturbation and Gibbs inclusion bound.** A single-qubit error e changes at most k checks in a fixed bounded root neighborhood. Gibbs syndromes s obey P(T subset supp(s))<=q^{|T|} for every fixed set T.

Then constants A,B,c0>0 depending only on the local data exist such that, for any integer 1<=h<=r,

  P[R_e(s) is nontrivial logical]
    <= B (Aq)^{ c0 min{2^h, d/S_h(K)} - B }

where S_h(K)=sum_{i=0}^{h-1}(K/2)^i, whenever Aq is sufficiently below 1. Integer rounding and bounded exponents can be absorbed into B. The lift-growth consequences are:

- **K>2:** if r>=floor(log(d)/log(K)), choose h near log_K(d). Then P<=B exp[-c(q) d^alpha], alpha=log(2)/log(K).
- **K=2:** if depth permits h near log_2(d/log d), then P<=B exp[-c(q) d/log d]. This in particular implies every fixed stretched exponent alpha<1 for sufficiently large d.
- **1<=K<2:** if depth permits h near log_2(d), then P<=B exp[-c(q)d].

A simpler, weaker bound obtained by S_h<=constant K^h also gives exponent log(2)/log(2K), requiring only depth floor(log(d)/log(2K)). This can be useful if available depth is the limiting constraint.

No system-volume prefactor is needed. A union bound for instability somewhere introduces the usual number of qubits. If d grows as L^delta and K>2 with sufficient depth, the bound is stretched exponential in L with exponent delta log(2)/log(K).

## Proof: charged space–scale animals

Run the decoder simultaneously on s and s'=s+syndrome(e). Include every component whose correction or output differs, up to the first h levels. Connect these components to incoming discrepancies using assumption 3. This gives the forward influence trace rooted at the fault neighborhood. Components may be enormous; they are included whole.

Now close the trace under ancestors: whenever an included occupied check at level i+1 is produced by a component at level i, include that entire component's input syndrome and shape. Iterate downward. Every added shape attaches to a previously included object by a dependency edge. Consequently the union, including the bounded fault connector, is connected in the bounded-degree space–scale graph. The two runs can be represented by two graph copies joined by matching-site edges; degree stays bounded.

Let U_i^a be the occupied input sites selected by this closure in run a, a in {0,1}. It is crucial to include **all occupied inputs of each selected owner-component**, not merely one local dependency. Formally the closure is the downward fixed point: every selected occupied upper input has every required producing lower component selected, including that component's entire occupied input. Writing F_i^a for the selected disjoint lower components, componentwise contraction yields

  |U_{i+1}^a| <= sum_{C in F_i^a}|O(C)| <= (1/2)sum_{C in F_i^a}|input(C)| = (1/2)|U_i^a|

on halving macrosteps. Additional lower-layer components selected by the forward trace increase the available input mass; additional upper-layer components force their own downward ancestry. With intermediate nonincrease layers retained, total selected occupied space–scale mass is at most a constant times |U_0^0|+|U_0^1|. The same conclusion holds for any finite prefix of the trace.

Let M be the number of distinct base checks in this selected leaf union that are actually occupied in s. Since s and s' differ only on the k fault checks,

  |U_0^0|+|U_0^1| <= 2M+2k.

The component-shape hypothesis and fixed-size connectors therefore bound the connected animal's total size by C(M+k). This is the central amortization: a globally chosen sheet within a component costs the component's occupied syndrome mass, not a spurious constant-size gate. Repeated ancestry and merging do not create an h factor.

There are at most A0^n connected rooted animals of n vertices in a bounded-degree graph. Colorings, owner marks, layer types, and the choice of occupied leaf subset cost another constant to the n, not n! or h^n. Levels are already graph vertices; no free level labels are chosen. Summing n<=C(M+k) and leaf subsets yields at most A1^{M+k} possible witnesses with M distinct occupied Gibbs leaves. Here A1 already absorbs the factor of two from counting the two runs. Equivalently, if one instead indexes by the duplicated two-run base mass M0=|U_0^0|+|U_0^1|, the honest probability factor is q^{M0/2-k}, and the entropy-probability combination is (A0 sqrt(q))^{M0}, not (A0 q)^{M0}. Our distinct-leaf indexing is what gives the displayed (Aq)^M form. The assumed inclusion bound gives probability <=q^M per witness, with no need to remove any syndrome witness or preserve syndrome validity after removal. Summing over M>=m gives B(Aq)^m for small enough q.

There are two cases.

**Influence reaches level h.** Choose a discrepant occupied check there (in either run), and take its ancestor closure, together with the rooted influence trace needed to attach it. Its own ancestry already has at least 2^h occupied leaves in that run, so M>=2^h-k. Enlarging to the rooted trace cannot reduce that bound. This includes any possible terminal reference-decoder instability if h=r.

**Influence dies before level h.** The higher-level inputs and therefore all subsequent corrections are identical. R_e(s) is supported on the fault together with the lifted corrections of the affected components below h. Ancestor closure bounds the unlifted support at level i by C 2^{-i}(M+k); lifting gives

  |supp R_e(s)| <= 1+C(M+k) sum_{i<h}(K/2)^i = 1+C(M+k)S_h(K).

Intermediate nonincreasing layers change only C when their local lift norm is uniformly bounded. If R_e(s) is nontrivial logical, distance implies M>= (d-1)/(C S_h(K))-k. The connected witness estimate applies again.

Combining the two cases proves the stated bound. For K>2, S_h is comparable to (K/2)^h and balancing 2^h with d/S_h means K^h comparable to d. For K=2, S_h=h; for K<2 it is uniformly bounded.

## What must be checked in an actual ell=8 construction

- Bounded-degree **space–scale** incidence, not merely bounded degree separately at each spatial level. Both forward and inverse dependency multiplicities must be bounded. Fixed ell and bounded-local lifts/projections ordinarily supply this, but it is a checkable premise.
- A uniform connected shape bound for the *entire active component*, including alignment homotopies, correction supports, and sheet-to-sheet links.
- Disjoint/uniquely owned output support (or an explicit equivalent mass inequality). Cancellation can only help global contraction, but overlapping ownership can otherwise invalidate naive ancestor counting.
- Component-consistent smaller-copy tie-breaking and local construction of the active graph. A decision must not depend on an unrelated component, a component enumeration order, or a global parity bit.
- Exact correction/logical identities and a physical logical distance d. Syndrome contraction alone says nothing about logical instability.
- Lift constant K per **complete contraction macrostep**, and enough depth r. Fixed-size reference codes are allowed if the hierarchy has the required depth and the identities hold; a large reference distance is not itself necessary for this sufficient theorem because any changed reference input is counted as a bad event.

## Scope and limitations

This is a sufficient consequential theorem, not a proof that every vaguely described local hierarchy satisfies its premises. If available depth is too short, the unoptimized bound is the justified result. If one knows additional stability or distance properties of the reference decoder, the terminal bad event can be improved; no such improvement is presumed here.

The proof already uses mass amortization across levels, rather than bounding every lift by K^h. Additional geometric or code-specific support estimates may further improve the exponent, but are unnecessary for stretched-exponential suppression.

## Actual ell=8 applicability remains conditional

The supplied component facts do not by themselves verify the theorem for the full ell=8 quantum-memory family. In particular, the refinement Rep4 to two Rep3 auxiliary face projection can inflate one occupied check to two; the sheet P-squared nonincrease statement currently applies only to ordinary page pieces. Actual admissibility/metachecks or a different charged mass must pay for that inflation before the macrostep contraction hypothesis can be claimed. This theorem identifies a sufficient endpoint once those local family-specific hypotheses are established; it does not silently assume that unresolved verification.
