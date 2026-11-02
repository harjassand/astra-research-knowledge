# Independent adversarial audit

Audited 2026-11-02: `THEOREM.md`, `AUDIT.md`, and `WEIGHTED_EXTENSION.md`.

## Verdict

I found **no counterexample to the sufficient abstract theorem under the exact interpretations explicitly imposed in AUDIT.md**. In particular, non-bounded-radius minimum-copy decisions do not by themselves defeat this argument. Its replacement for bounded-radius causality is a connected charged component witness, and that replacement survives the main possible merging, ancestry, and two-run objections.

This is a mathematical audit of the abstract argument, not verification of an actual ell=8 hierarchy. The unresolved auxiliary-check inflation remains unresolved.

For a standalone theorem, I recommend importing the precise fixed-ambient-graph interpretation and correction-support interpretation from the audit directly into its numbered hypotheses. Otherwise readers can reasonably interpret the numbered statement more weakly than the proof requires. The verdict below does not assert the theorem under those weaker interpretations.

## 1. Selected mass: the potentially dangerous inequality is valid

Let F_i^a be the selected input components at layer i in run a, and let U_i^a be the union of their occupied inputs. Downward closure must mean the following fixed-point condition:

> Every selected occupied input at layer i+1 has all required producing components at layer i selected, including every occupied input of each such component.

At a halving layer, write O(C) for a component's actual contributed output support. Because the selected upper inputs are covered by outputs of selected lower components,

    |U_(i+1)^a| <= sum_(C in F_i^a) |O(C)|
                 <= (1/2) sum_(C in F_i^a) |input(C)|
                  = (1/2) |U_i^a|.

The final equality uses disjoint input components within one run. This proof does not assume that all selected lower components arose from upper ancestry: additional forward-selected components only increase the available right-hand mass. Conversely, a component selected at an upper layer is not free: its entire input goes into U there and forces downward ancestry. Thus there is no missing additive source term in the recurrence.

For overlapping output contributions, the displayed argument still works if the selected nonzero upper support is covered by the selected contributors and the component bound applies to each contributed output support. A bound only on the globally canceled output would not suffice. The unique-owner version avoids this ambiguity.

After grouping a uniformly bounded number of intermediate nonincrease layers into one contraction macrostep, the total selected occupied mass is O(|U_0^0|+|U_0^1|). One must not add arbitrarily many uncharged nonincrease layers per macrostep.

## 2. Connectivity survives ancestry closure, with the stated causal hypothesis

Start with the forward changed-component trace. Every changed component must attach through charged component shapes/connectors to an incoming discrepancy; recursively these attachments end at the bounded initial fault neighborhood. Matching-site edges between the two run copies permit attachments across the two histories. Their degree is uniformly bounded.

Adding an ancestor component preserves connectedness: a selected upper occupied check already in the trace attaches to its producing lower component through its charged dependency connector. Include that component's whole connected shape. Repeat downward. Merges and repeated ancestors only identify or duplicate a bounded number of run-copy vertices; they do not introduce a separate entropy factor.

This uses the **explicit causal attachment requirement**, not just the words “deterministic” or “component-consistent.” The fixed enlargement must contain the relevant output attachment and correction support. It is not necessary to propagate forward the outputs of components added solely for ancestry.

## 3. The probability charge counts genuinely distinct Gibbs checks

Let L = U_0^0 union U_0^1 after identifying the two copies of each base check, and let M count those sites in L occupied in the original syndrome s. Outside the initial fault-check set F, the two base syndromes agree. Therefore

    |U_0^0| + |U_0^1| <= 2 M + 2 |F|.

No independence between the runs is used or available. A selected set of M distinct original occupied checks has probability at most q^M by the stipulated inclusion bound. Correlated or constrained syndromes do not invalidate this step.

The original text correctly warns that duplicated leaf mass would instead give a square-root-q activity. Distinct-leaf indexing legitimately restores the stated (Aq)^M notation after changing constants.

## 4. Animal entropy has no hidden depth or volume factor

The counting graph must be fixed before sampling the syndrome, uniformly bounded degree across both spatial and vertical edges, and contain every possible charged shape and connector. Root its two-run version at the fixed fault neighborhood. Each selected component of mass m contributes O(m) vertices, including its enlargement and attachments. Hence the entire witness has at most C(M+k) vertices.

For fixed maximum degree, rooted connected vertex sets of n vertices admit an exponential upper bound c^n. Finite run/type/selection markings and a choice of base-leaf subset also cost only an exponential factor. Summing over n <= C(M+k) remains exponential in M+k. Layer indices are already part of the fixed vertices and must not be counted again as freely chosen labels.

Only the animal and its occupied original leaf subset are needed for the probability union bound; no exhaustive encoding of the decoder's component partitions or decisions is needed. Thus there is no necessity for an n! owner-label factor. Counting impossible animals or leaf sets only overcounts.

A merely realized, syndrome-dependent bounded-degree graph would not establish this enumeration. AUDIT.md explicitly excludes that weakening.

## 5. Reaching the cutoff and dying below it

If the input syndromes differ at level h, one of the two runs has an occupied discrepant check there. Its full ancestor closure has at least 2^h base occupied inputs in that run. The bounded initial fault removes at most k from the distinct original Gibbs-leaf count. Attaching this ancestry to the rooted forward trace cannot reduce its mass. Thus reaching level h costs M >= 2^h-k.

If the inputs agree at a level below h, determinism with no hidden state makes every subsequent input and correction agree. Fixed common lifts then cancel these common higher corrections physically. The residual is the single fault plus the lifted **changed lower corrections**. Selected component shapes dominate their support, and the mass recurrence yields

    weight(R_e) <= 1 + C (M+k) sum_(i<h) (K/2)^i.

The distance implication is then correct. A coarse-syndrome extinction argument alone would not suffice, but the supplied proof does not make that mistake.

This support statement requires that all syndrome-dependent correction differences at a step are sums/unions of its component corrections, supported in the charged enlargements. A separate global logical correction or a branch-dependent lift of a large common terminal correction is not covered. The common-lift alternative is clean. The branch-dependent-homotopy alternative should explicitly require its total charged support and mass bounds, not merely the existence of a local identity.

An arbitrary deterministic terminal decoder causes no extra gap. If its input agrees, its correction cancels under the common lift; if it differs, the level-r event has already been charged. This does not prove shallow terminal stability, and the depth-limited formula correctly reflects that.

## 6. Optimization and weighted extension

For K>2, balancing 2^h against d/(K/2)^h gives K^h of order d and exponent log(2)/log(K). For K=2 the denominator is h, giving d/log d at sufficient depth. For K<2 it is bounded, giving linear-in-d exponent. Floors and small d are absorbed by constants. I found no error in these optimizations.

With uniformly positive bounded type weights, repeat the same selected-component inequality using W. Then W(U_i) <= rho^i W(U_0), and base mass converts to distinct original Gibbs leaves with the factor 2 w_max. Shape size remains O(W) by hypothesis. The claimed S_h = sum (K rho)^i and resulting exponent log(1/rho)/log(K) when K rho>1 follow.

For an unrestricted nonnegative exact transfer matrix, a strictly contracting positive left weight exists precisely when the spectral radius is below one. Restricting to a rigorously established admissible cone can weaken the required inequalities. Neither statement supplies such a cone or weighting for the concrete family.

## Recommended wording hardening

1. State explicitly in the numbered theorem that the ambient space–scale graph is fixed independently of syndrome and contains every possible shape, correction enlargement, and dependency connector.
2. State explicitly that step corrections decompose componentwise with all syndrome-dependent support charged to these enlargements.
3. Define ancestor closure by the fixed-point condition in section 1 and write its one-line mass inequality; this removes the most plausible apparent objection about forward-added components.
4. Say that intermediate layers per macrostep and their relative lift costs are uniformly bounded, and that K is per complete contraction macrostep.
5. For the branch-dependent-lift variant, state the same selected-mass support bound for every added homotopy contribution. Otherwise retain only the fixed-common-lift version in the principal theorem.

These are precision improvements to the stated sufficient endpoint, not a newly discovered family-specific proof or a fatal counterexample to the audited exact assumptions.
