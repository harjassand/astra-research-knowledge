# Sharp local-to-global compatibility via packing and reference-state broadcasting

This package preserves the supplied research note as an independent finite-dimensional marginal-compatibility family. It is not merged into the channel-order manuscripts: the note's matching, stable-set, broadcasting, and star-gluing arguments use distinct interfaces and assumptions.

## Source-reported contents

The [original Markdown note](global_compatibility_gluing_research_note.md) gives five main claims:

1. A fractional matching in a graph matching polytope yields a global extension for locally consistent edge marginals that dominate the corresponding product reference states.
2. A centered interaction decomposition yields a stable-set-polytope sufficient condition for gluing downward-closed observed marginal families; a coloring gives a stronger, easy-to-check certificate.
3. The universal product-domination radius on `K_n` is claimed to be `1/(n−1)` for even `n` and `1/n` for odd `n`.
4. The state-centered replacement channel `D_{τ,t}(X)=tX+(1−t)Tr(X)τ` is claimed to have universal `k`-self-compatibility threshold `1` for `d=1`, `2/(1+√(4k−3))` for `d=2`, and `1/k` for `d≥3`.
5. A star of consistent pair marginals is claimed to admit an exact global extension at the same dimension-dependent radius, with that uniform constant sharp even for full-rank center states.

The note also reports a qubit-star MPO bond-dimension bound of 54, with local inverse-filter conditioning depending on the least eigenvalue of the central marginal. This is an existence/construction claim under the stated model, not a uniform conditioning, dense-observable, or general compatibility algorithm guarantee.

## Scope and limitations

The note is unsubmitted and unaudited. It reports no external proof review, formal verification, or priority clearance. Its finite `k=2…5` Choi/marginal tests are stated in the note but were not supplied as runnable artifacts or replayed here. General quantum marginal compatibility, complexity separations, and exact compatibility for arbitrary given marginals remain outside its stated scope. The note itself flags the related inverse-golden-ratio threshold in bosonic pure-loss work and names prior-art routes requiring review.

Although the note mentions Astra cards N190–N193, N635, and N637, it explicitly states that those EPR determinant/gluing constructions are separate and that none of their open acquisition/variance gates is closed. No graph edge or transfer is inferred from the shared word “gluing.”

No existing frontier claim was modified and no new frontier card was created. The full note is the mathematical source; this guide is only retrieval and scope metadata. Exact source integrity is recorded in [`SOURCE_MANIFEST.json`](SOURCE_MANIFEST.json).
