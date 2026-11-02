# Contact-completed canonical trace gas

Root construction, 2026-11-02. New representation proposed at the annealed-source gate; independent audit pending. This is stronger than merely using valid removable witnesses and is not silently imported from the prior package.

## Explicit repair to the representation

Let T(sigma) be the full charged trace of the actual deterministic decoder, including both-branch potential stencils before component decisions, complete residual operands, cancellation gates and whole packet owners. Its degree and vertex count are bounded by fixed constants times occupied top-level mass. Let G be its fixed bounded-degree space-scale ambient graph.

Define Tplus(sigma) by retaining exactly the vertices and recorded values of T(sigma), and adding every edge of G whose two endpoints are present. No new vertex is added. Zero vertices do not seed further gates or layers. Decoder component choices are NOT recomputed after this graph completion.

Each connected Tplus component is a union of whole old T components, hence its top syndrome tau is valid by the old full-trace algebraic restriction theorem. This preserves every quantitative charge bound: only at most degree(G) edges per already charged vertex are added. The construction does not change the physical code, decoder, map or measured observables.

## Needed exact assembly statement

For a valid tau, call Tplus(tau) a polymer if it is nonempty and connected. Two polymers are compatible precisely if their charged vertex sets are disjoint and have no ambient edge between them.

Forward: decompose Tplus(sigma) into components. Restricting to one component retains a union of whole old layer components, their entire inputs/owners, decisions and outputs. The old deletion-stability induction therefore preserves the entire seeded trace on this restriction. Any incidental vertex that survives in the selected component must be seeded by a retained nonzero operand or retained whole component; a removed contribution at the same vertex would have belonged to the same original connected component. Consequently the recomputed Tplus(tau) should equal the selected component exactly.

Reverse: for a compatible finite collection {Tplus(tau_i)}, their top supports are disjoint, so sigma=xor_i tau_i is valid. At level zero the union of fixed per-input stencils has no new cross-component collision. Complete potential stencils include all operands that could alter a branch choice or output. Thus the actual layer input components and their deterministic component-local choices are unchanged. Inductively the same is true at every later level. Terminal-reaching polymers cannot coexist because each includes the same finite terminal bag. The full recorded trace is the disjoint union of the given traces, and contact completion adds no cross-edge by compatibility. This would establish a bijection, rather than deletion alone.

The independent audit must check the actual declared stencil/decision conventions support every step above. In particular generic deletion stability by itself is insufficient for reverse assembly; the fixed union construction and pre-choice potential-collision closure are essential premises.

## Commuting reference consequence if assembly passes

For H0=-J sum_a S_a, all valid syndrome sectors have the same logical dimension. The reduced syndrome partition function is therefore exactly

    Xi = sum_{compatible collections C} product_{gamma in C} exp(-2 beta J m_gamma),

where m_gamma is its top occupied syndrome count. Logical multiplicity and the ground scalar factor cancel in normalized expectations. X and Z sectors can be treated separately and then jointly with their actual independent valid syndrome spaces.

The trace-size bound and bounded ambient degree give exponential rooted polymer counting. At sufficiently low temperature, ordinary hard-core polymer KP and cumulant bounds follow. This supplies a possible reference measure for annealed quantum source expansion, stronger than a two-point clustering assertion. It does NOT already factor time-ordered quantum insertions or prove generic perturbation stability.

A truncated high-dilution polymer sampler could also be implemented by enumerating and validating connected traces of O(log(n/epsilon)) mass, with the potentially large polynomial exponent charged. This is a different engineered generator, not rapid mixing of physical single-site Glauber dynamics. The prior ideal-preparation machinery already offers related operations for other admitted families; no new native quantum Gibbs preparation or noisy WRITE follows just from this representation.
