# Causal query compression: strongest ordinary route and the remaining interface

31 October 2026. Focused comparison, not a literature-exhaustion or novelty claim.

## Primary source actually inspected

Jacob Kitchen, *Causal Query Compression for Lindblad Dynamics: Optimal Queries and Nearly Linear Local Simulation*, https://arxiv.org/html/2609.31312 , version 1, 25 September 2026. I read Sections 2 and 5, the occupied-input assumptions and proof in Section 6.2, and the gate-resource qualification preceding Section 5.

Concise source statement: Theorem 2.3 converts a chronological query-history tail into an initialized-isometry approximation. Definition 2.4 and Theorem 2.5 provide sufficient weak-cell conditions. Section 5 uses worst-branch normalization action, not expected trajectory action, and permits oracle-independent dissipation. Lemma 6.3 concerns sparse inputs to distinct cell baths, with each bath untouched after its cell. The general query theorem leaves routing and bath-storage gates unbounded without further structure; the later local-lattice theorem supplies specialized structure. These are powerful prior tools, not missing general compression machinery. [Primary source](https://arxiv.org/html/2609.31312).

## Our direct application, and what it actually earns

Consider our joint system/source generator

    L_lambda = lambda L_0 - i[H_0 + sqrt(lambda) K_x, .],

with a known source preparation psi, pure projector P, Q=I-P, and ||K_x||<=b. Here x denotes a possible coupling oracle input; it is not the classical source state. If the source generator and H_0 are oracle independent, assign them to the free part. A direct application of the ordinary action receiver then pays a coupling normalization of order sqrt(lambda)bT rather than charging lambda T for the whole source. This is a materially stronger comparison than simply plugging every joint-generator term into one total norm. It still does not give rate-independent coupling queries. If source access itself is an oracle resource being counted, it must also be charged.

Declaring all supplied operators known and therefore query-free cannot establish a gate theorem: the work implementing those known operations remains. Likewise, the finite explicit dimension of the joint Markovian system makes the abstract representation legitimate, but says nothing about efficient work on a succinctly represented source.

The restriction to a pure initial reservoir is compatible with an initialized input-subspace formulation. Prescribed system interventions can be retained coherently, with their actual costs or external-instrument convention. The old reservoir is part of the joint workspace; fresh output environments may be retained and never reused. Thus there is no blanket semantic incompatibility between our controlled-process task and a causal query compiler. The unresolved issue is quantitative acquisition, not merely the words 'non-Markovian reduced system'.

## An acquired source bypass, but not a coupling bypass

For an actual unitary W fixing an explicitly known input vector, querying W only on its orthogonal complement reproduces W exactly. More generally a known initialized-isometry output may first be mapped back by a known unitary. A top-block identity or eigenvalue alone is insufficient: failure flags and the full unitary column must be controlled. In particular a contraction equation with an eigenvalue of modulus below one is not a unitary fixed-vector certificate.

Our shuffle source has the stronger acquired property. Its Stinespring map has Kraus operators T_c/sqrt(n), with T_c psi=psi. It maps psi to psi tensor the known uniform color state. Unpreparing that color makes its full unitary act identically on psi with initialized work. Thus source queries can indeed bypass this known vector; this observation is constructive, not a missing-oracle excuse.

But the physical driving operator generally has Q K_x P != 0. A rule querying it only on an incoming Q sector would remove the excitation which produces the signal. Decomposing K_x into its PQ, QP and QQ blocks does not make the off-diagonal block known or free. Any replacement must earn the primitive coupling-query amplitudes and count all source, coupling, inverse, and controlled uses. The reflection about P is acquired, but it does not solve this problem by itself.

## Why physical jump tails are not yet the required tail

Our finite-return Lyapunov certificate controls positive physical output histories after fixing a dark jump realization. A query circuit is a different object: it also has coherent no-jump scattering, work flags, inverse queries, and absorbed paths. Changing the quantum realization or its unitary implementation can change these primitive histories without changing the physical channel or its jump statistics.

A useful exact diagnostic is the following. If a source query has been bypassed on P, weighting that active port by a scalar z inserts P+zQ. Its density action includes

    P rho P + z Q rho P + conjugate(z) P rho Q + |z|^2 Q rho Q.

This is not the physical jump-count tilt, which multiplies only jump recycling terms and leaves the no-jump part unchanged. In particular coherent cross terms are altered. Consequently the already-proved jump MGF cannot simply be relabeled as a query-history MGF.

Even an established bound on the sum of ordinary port probabilities would only be a first-history-weight statement. The desired polylogarithmic precision conclusion needs control of the higher chronological histories on the initialized input, not an identification of physical emissions with every primitive call. A purely formal change of normalization does not establish that control.

Nor can the persistent source-Q sector be identified with sparse occupancy of fresh cell baths. A single surviving source excitation can encounter arbitrarily many subsequent cells. The number of fresh occupied bath registers and the number of visits to that retained sector are different quantities.

## Exact missing interface for this alternative

A complete derivation through the causal query receiver would need all of the following.

1. An explicit finite source/drive cell circuit, with primitive active projectors, master SELECT, initialized work, and retained bath registers. Its approximation to the physical joint generator must be uniform over the allowed input states and controls.
2. A rate-independent deformed-port or chronological-history bound for that circuit, on the pure-source input subspace. It must cover PQ/QP driving, QQ scattering, source queries, adjoints, and all absorbed prefixes/suffixes, not only the actual positive physical paths.
3. An acquired implementation of the oracle-independent transducer routing, reflections and record manipulation with polynomial logarithmic-rate/precision cost. A fine mesh with lambda T cells is not made gate-cheap solely by reducing master queries.
4. A complete error allocation for controlled interventions, source/coupling encodings, cell approximation and the retained-source output. Exact recovery of a chosen physical unraveling is unnecessary if only the controlled system output is claimed, but cannot be assumed for free if promised.

The finite-return potential is a plausible starting point for item 2: one might establish a discrete weighted contraction for the explicitly port-deformed source/drive circuit. That would be a new receiving argument to be proved, not a direct consequence of our current physical MGF. The newly acquired scaled fast kernel and first-event machinery provide another route to earning these costs, rather than proving that causal compression cannot do so.

## Scoped conclusion

The inspected primary theorem is a serious ordinary alternative and already supplies the abstract causal compression and adaptive query-receiving machinery. I have not derived the same rate-independent, precision-efficient, paid-gate source-channel guarantee from it plus our pure-return certificate alone. The exact missing interface is primitive coherent query-history control together with efficient free routing. This is not an impossibility statement and does not establish originality. If those interfaces are supplied, the ordinary theorem should be credited as a viable compiler, rather than dismissed by quoting its default total normalization.
