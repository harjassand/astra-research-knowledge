# Independent check of the finite-duration start-clock bridge

2026-10-15. This check reconstructs the new interfaces, conditional on the previously proved ideal support, forcing, homology and HT imports. It does not infer validity from the author's verdict.

## Result

The proposed reduction closes under the stated **joint serializability and fresh-reset** interpretation. I find no extra factor of the gate count, no requirement to bound the length of conflict components, and no missing factorization of a bad channel through a correction. The quantitative budget is correct. The following precision requirements should be explicit:

1. Every clean attempt actually receives fresh reset local ancillas, with all prior correlations removed, or an equivalent joint-input implementation guarantee. Merely proving the isolated circuit with initially clean ancillas is insufficient if later attempts can reuse contaminated ancillas without resetting.
2. The terminal flag is a **local candidate-start intersection** with [T-tau,T]. One may add its uniform N kappa tau bound to every marginal, but must not define every slab's flag using the same unrestricted global terminal event.
3. delta_ideal here contains the slow-certificate and fast-word terms only. Ordinary noise is counted in the displayed F nu term. Using the old three-term expression without adjusting the bookkeeping double-counts noise (conservative, but not the asserted exact decomposition).
4. Bound the enlarged coarse spatial packet radius and the full spacetime dependency degree before choosing b. Their upper bounds must not grow with b. N and F may grow with b and are fixed afterward.
5. For prospective-anchor replay, copy primitive increments through the maximum right endpoint of all witness flag windows, including beyond the anchor layer endpoint. Copying only the old disjoint slabs is insufficient.

These are implementable proof definitions, not new physical realization claims.

## Exact endpoint reduction

Fix all exogenous starts/noise and a finite endpoint T. A clean completed attempt has no overlapping resource-touching operation. Move its gates to its start by adjacent commutations with disjoint channels. This identity holds on jointly entangled inputs: channels on disjoint tensor factors commute even when their input is entangled. Clean attempts with intersecting resources have disjoint intervals, so their original order is preserved. There is no cyclic ordering obstruction. Reset local ancillas and trace their private outputs so the resulting operation on data and every exterior reference is precisely C_i tensor identity.

A clean circuit cannot be replaced by its reduced channel while secretly retaining an input-correlated auxiliary output that later interacts outside the claimed model. Fresh reset/discard or an explicitly verified joint instrument handles this issue. The stated no-shared-controller and joint-serializability premise excludes the usual counterexample.

Leave bad gates at their original times. In particular a pending prefix is never completed. Expand each retained Kraus operator as sum_P P tensor B_P, with P supported on the data part of its fixed patch. B_P may contain persistent ancillary records, arbitrary earlier correlations, and causal controls. Chronological coefficient multiplication is retained. This is an operator expansion, not an independent Pauli sampling argument.

An arbitrarily long conflict chain only increases the number of such local events. On a finite torus and finite time interval the start count is almost surely finite and each attempt has at most g gates, so the expanded history is finite. No union-of-chain patch is used. Simultaneous prescribed gates of bad attempts need a well-defined physical execution order or a joint local operation with an allowed bounded patch; the premise that the actual circuit is locally well-defined is essential.

## Skips and topology

For an omitted correction, put G_i = sat_(S_i) composed with F_i. Since F_i is identity outside S_i and saturation is one inside it, G_i(eta) >= eta for every eta. Both maps are monotone. Thus if physical support is bounded by eta before the skipped start, it remains bounded afterward. The compound update is atomic for support comparison: the fictitious intermediate F_i state need not contain physical support before its immediate saturation.

The physical error chain is unchanged by this reference event. Actual good corrections and actual Pauli terms of bad gates remain bounded-patch transitions. Therefore the local contractible-box proof applies to every actual transition and no virtual correction is inserted into the homology sum. Local ancilla-only errors have identity data Pauli but can alter later B_P coefficients; later touching bad gates remain covered. No post-C factorization is required or valid in general.

On a good primitive schedule, the same envelope argument certifies every expanded history, including all omitted corrections and all allowed patch Paulis. The fixed decoder consequently sends each history operator to a scalar logical identity, and ordered ancillary coefficients sum to a logical identity tensor an ancillary channel. Trace preservation of the full conditional circuit, not of individual expansion terms, gives the norm bound after averaging schedules.

## Probability calculation

Let I=[a-tau,a+Delta] intersect [0,infinity), and count ordered distinct start pairs with first start at a candidate location in I and second at a conflict neighbor within tau. Campbell's factorial measure gives

E pair count <= N D kappa^2 |I| (2 tau)
             <= 2 N D kappa^2 tau (Delta+tau)
             <= 2 N D kappa^2 tau (Delta+2tau).

The formula includes distinct points of the same Poisson stream. A point paired with itself must be excluded; the factorial measure does that. Ordered overcounting is harmless. Truncation at zero decreases the expectation.

Every dirty candidate has a noise event in [a-tau,a+Delta+tau] on one of the counted patch locations. The union intensity is at most F nu (Delta+2tau). This also pays for direct guarded physical noise. The argument does not separately charge each gate or each dirty attempt.

For the terminal flag use candidates whose execution interval contains T, equivalently starts in I intersect [T-tau,T] (with harmless endpoint conventions). Its probability is at most N kappa tau. For early slabs not intersecting this start window the event is empty. If I includes only nonnegative starts, no startup cost is needed. Future Poisson increments may be sampled to define the analysis flags; no actual policy may depend on those future marks.

## Full spacetime dependence and replay

The conflict-partner search uses clocks in [a-2tau,a+Delta+tau]; the other flags use subsets of this window. Assume tau <= Delta. For a=nDelta this lies in [(n-2)Delta,(n+2)Delta]. Thus a conservative dependency graph joins temporal indices within four and spatial cells within twice a fixed coarse packet radius q. One possible bound is

D_dep <= 9 (4q+1)^4 - 1,

with a fixed sector factor if sectors are represented as separate graph vertices. This is distinct from the gadget conflict-neighbor count D. Beyond graph neighbors the entire primitive unions are disjoint, so the needed conditional-probability premise follows, not merely pairwise independence. The domination lemma applies to this whole spacetime graph at once. No slab-independent coupling is asserted.

A fixed fine patch diameter a_* gives a coarse enlargement bounded by, for example, ceil(a_*/4)+a fixed offset for every b>=4. Fix that enlargement, q, the coarse connectivity and D_dep before choosing b. This avoids circular threshold choices.

For a deterministic prospective first-crossing anchor (x,n), copy an injective deterministic spatial patch containing the witness and all flag resource guards. Copy each actual primitive stream once over the union of all required time windows, not once per overlapping flag. A safe deterministic temporal range is [0,nDelta+tau] for flags through transition n-1. Extend the remaining primitive field independently. This preserves independent Poisson laws and agrees on all witness flags, including correlations across slab boundaries. The endpoint T is a deterministic parameter in both copies. The zero-ancestor closure and induction forcing the lifted witness then proceed unchanged. Spatial inhomogeneity of implementation geometry can be handled by fixed worst-case guards or by the same bounded-degree inhomogeneous domination statement.

## Rate budget and quantifier order

Write x=kappa tau, y=nu/kappa, Delta=Cb/kappa. The extra marginal bound is

F y (Cb+2x) + N x [2D(Cb+2x)+1].

For 0<=x<=1 this is at most A0 y+B0 x with

A0=F(Cb+2), B0=N[2D(Cb+2)+1].

No term proportional to g appears: the flag excludes the entire attempt's possible local births. Choose fixed geometry, C,R, coarse rule/connectivity and D_dep first; choose an allowed iid-death density and its domination tolerance; then b to make slow+fast small; then choose x,y to fit the remaining tolerance. This order is consistent. N,F and A0,B0 can be extremely large but are finite and independent of L,T. Require tau<=Delta separately, or use x<=1 and Cb>=1.

For fixed nu,tau, minimizing A0 nu/kappa+B0 kappa tau gives 2 sqrt(A0 B0 nu tau), with the stated optimizer when nu,tau>0. Degenerate zero-rate cases are interpreted as infima or direct limits. The optimizer must satisfy all admissibility constraints. Consequently failure of the displayed product condition blocks only this sufficient numerical recipe, not all implementations.

## Scope of conclusion

Subject to the named original imports and these exact implementation premises, the result is pointwise in every deterministic T with one fixed ideal decoder. Classification can change with T. It gives neither a simultaneous classical syndrome trajectory during coherent clean executions nor a noisy-clock, finite-controller, autonomous Lindbladian or hardware threshold theorem. The paper's stated limitations are substantive and must remain attached to its conclusion.
