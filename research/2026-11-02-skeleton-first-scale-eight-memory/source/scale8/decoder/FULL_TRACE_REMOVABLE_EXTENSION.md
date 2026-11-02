# Full canonical traces: removable valid witnesses

## Status

This is a **conditional extension with explicit additional structural hypotheses**, not an inference from syndrome contraction alone. It aims to replace the all-subsets Gibbs inclusion input by a local-ratio bound for valid removable syndrome subsets. Actual family maps and local identities remain to be verified. It does not assert a hard-core polymer bijection.

## 1. Retained hypotheses and precise additional data

Retain the hardened component-contour theorem, including whole packet blocks where applicable, fixed bounded-degree space–scale geometry, component charge contraction, bounded intermediate costs, componentwise corrections, common fixed cochain lifts, and exact correction identities. Require additionally:

**F1. Canonical deletion-stable layer graphs.** A layer's active graph is a union of fixed bounded local stencils seeded by its occupied input blocks (or deterministic component-local data), with deterministic component-consistent decisions. Every component's entire input, correction, output, and relevant potential residual-row stencils are included. Deleting a union of whole active components leaves the active graph, decisions, and output on every remaining component unchanged. For a graph that is literally the union of fixed per-occupied-block stencils, this follows because a removed stencil intersecting or connecting a remaining component would have put both in the same component. If component-dependent extra stencils are used, this deletion property must be checked; generic determinism alone does not imply it.

**F2. Local row identities with complete operand stencils.** At each layer the actual computed variables satisfy a binary linear residual identity of the form

  sigma_i + J_i sigma_{i+1} + delta_i c_i = 0,

or a specified equivalent collection of local linear equations with auxiliary variables. J_i is fixed and compatible with the common lift, and the identities telescope. Every residual row's nonzero operands are connected in the full trace through its complete fixed bounded stencil. Include potential correction/output operands even when their actual value is zero. Any auxiliary term has its support and connectors charged and its own restriction/telescoping identity stated. An asserted identity that holds only after an unrecorded global operation is insufficient.

**F3. No recursive zero activation.** The full trace includes bounded stencils of charged components and nonzero computed variables. Incidental zero vertices in such stencils do not recursively activate every neighboring row or empty component. Every trace vertex/edge is charged O(1) times to the selected component input mass. In particular the full trace has at most C sum_i Q(sigma_i) vertices (plus a fixed root allowance when comparing runs). A zero row may be recorded, but cannot create an uncharged chain across the system.

**F4. Fixed finite terminal bag.** The reference code has a uniformly bounded number of sites and a fixed connected bounded-size terminal bag. Whenever sigma_r is nonzero, include this whole bag, all terminal input positions, and the terminal decoder correction. Thus every nonzero terminal input lies in one full-trace component. The terminal decoder satisfies D_r(0)=0 and delta_r D_r(sigma_r)=sigma_r for every valid terminal syndrome encountered. The bag is absent for zero terminal input. A growing reference code would require a separately proved charge/support substitute and is not covered by this finite-bag argument.

These conditions are deliberately stronger than merely having a contracted syndrome sequence. They are the additional removability interface to verify.

## 2. Definition of the full canonical trace

For a valid original syndrome sigma, compute the entire deterministic decoder history. At every layer include **every** nonempty active component, its whole input packet blocks, its charged correction/output stencils, and its complete residual-row operand stencils. Add all fixed dependency edges, packet-owner connectors, and the terminal bag prescribed above. This produces a fixed-rule graph T(sigma) embedded in the fixed bounded-degree ambient graph. It records zero-valued positions when they belong to a charged stencil.

The total trace size is bounded by C sum_i Q(sigma_i)<=C'Q(sigma), because each contraction macrostep halves charge and has only uniformly many bounded-cost intermediate layers. The same estimate holds for any union of whole connected trace components, with its own selected input mass at every level: upper selected inputs force their entire lower owners into the same union. Complete packet ownership gives Q_{i+1}<=Q_i/2 for that selected union.

Zero-valued overlap can merge trace components more than minimally necessary. This only makes witnesses larger and does not invalidate the bound, provided F3 holds. Never complete an arbitrary connected component of the entire ambient graph: complete only components of the charged trace that was actually constructed.

## 3. Restriction establishes validity BEFORE any removal argument

Choose a union A of whole connected components of T(sigma). Restrict every recorded variable to A: retain its actual value if its vertex belongs to A and set it to zero otherwise. Whole-block ownership ensures that packet states are restricted by whole blocks, not by arbitrary bit deletion.

Consider a linear residual row. All its nonzero operands belong to one full-trace component by F2. Restriction therefore keeps all nonzero operands or none. Its sum remains zero. Rows with no nonzero operands remain zero as well. Hence every local residual identity still holds on the restricted variables. This argument does **not** presuppose that the restricted input syndrome is valid.

At the terminal level, the restricted syndrome is either the entire original sigma_r or zero: all nonzero terminal inputs are in the fixed terminal bag. Retain the entire original terminal correction in the first case and zero in the second. Its coboundary is the restricted terminal syndrome. Telescope the restricted residual identities using the common fixed cochain lifts. The resulting physical correction has coboundary equal to

  tau_A = sigma restricted to the selected original level-0 inputs.

Thus tau_A is a **valid coboundary syndrome** and supp(tau_A) is a subset of supp(sigma). The complement sigma+tau_A is valid too. This establishes algebraic removability without assuming that the decoder can be run on an invalid restriction. There is no circular appeal to validity of each active component.

In particular every whole full-trace component, and every union of such components, has a valid level-0 syndrome. A component with no level-0 occupied input cannot carry a nonzero computed variable under the ancestry/zero-preservation hypotheses; purely incidental zero stencils have no independent mass.

## 4. Removing a whole trace union preserves the surviving decoder history

Now run the decoder on sigma+tau_A, which is valid by Section 3. At level 0, A contains a union of entire active input components; by F1 deleting them leaves the other decisions unchanged. Their outputs are exactly the old outputs outside A. Output ownership and the full dependency connectors prevent an output block from being partly removed. The same argument applies inductively at each later layer. The terminal input is either unchanged or zero, so F4 gives the corresponding surviving terminal correction.

Therefore deletion of A leaves the surviving computed history unchanged and does not create new occupied outputs or decisions. The resulting charged stencils are precisely the surviving ones, subject to removing any now-unseeded incidental zero vertices. No positive-cost new component appears. This is the constructive deletion property needed by a removable-witness argument.

This assertion depends on F1 and the charged stencil construction. A different canonical graph that propagates arbitrary zero support or depends on global component enumeration need not have this property.

## 5. Two full traces and a rooted removable witness

Let sigma'=sigma+syndrome(e), with fault-check set F of size at most k. Form two copies of T(sigma), T(sigma'). Join matching active/stencil vertices in the two copies by fixed edges. Add a fixed bounded root connector joining the physical fault and all coordinates of F. Let W be the entire connected component containing that root (or the union of root components joined by that connector).

A causal discrepancy induction shows that every difference between the two computed histories lies in W: changed layer components attach to an incoming discrepancy, and all initial discrepancies lie at the root. Outside W, the two runs' variables, components, and common lifted corrections agree. This is the original theorem's explicit causal attachment requirement, now applied to full traces, not a replacement for it.

Within each run W contains a union of **entire connected full-trace components**. Let tau be its original-run occupied base syndrome. By Section 3, tau is valid and removable. Let tau' be the corresponding perturbed-run occupied base syndrome. At any base coordinate outside F, the two syndromes have the same bit. If that bit is one and one copy is in W, the matching-site edge puts the other copy in W too. Consequently

  supp(tau+tau') is a subset of F,
  |tau'| <= |tau|+k.

For packet charges Q<=c Hamming,

  Q_0^original(W)+Q_0^perturbed(W) <= c(2|tau|+k).

The selected-union contraction inequalities and charged stencils therefore give |W|<=C(|tau|+k). This is the honest two-run mass accounting. No independence between the two histories is used.

## 6. Consequential size lower bound

Use occupied processing height H: the largest macrolevel with an occupied input in W. If H>=h, selected ancestor charge is at least 2^h in one run. Thus |tau|>=2^h/c-k. If one instead uses the maximum geometric vertex height of the full trace, an all-zero operand stencil may reach one level above its occupied source; with adjacent-level connectors the corresponding lower bound is 2^{h-1}/c-k. More generally a fixed stencil-height offset changes only a constant factor. Do not infer occupied ancestry from an arbitrarily high zero connector.

If H<h and h<=r, no differing terminal correction remains. All correction differences are charged below h, and common higher lifts cancel. Therefore

  weight(e+D(sigma)+D(sigma'))
    <=1+C(|tau|+k) sum_{i<h}(K/2)^i.

A nontrivial logical residual has weight at least d. Hence in every instability event there is a rooted trace witness W and a valid removable tau with

  |tau| >= c0 min{2^h, d/S_h(K)}-C0,
  |W| <= C(|tau|+k),
  S_h(K)=sum_{i<h}(K/2)^i.

One can equivalently classify by geometric height and absorb the one-layer ghost offset. The fixed-root, bounded-degree graph gives at most A^{m+O(k)} possible witnesses and designated base subsets tau of size m. Validity reduces the set of candidates; it never increases the entropy.

## 7. Gibbs local-ratio consumer, without all-subsets domination

Suppose the Gibbs syndrome law pi satisfies the following local-ratio statement for every fixed valid syndrome tau and every valid sigma containing its support:

  pi(sigma) <= z^{|tau|} pi(sigma+tau),  0<z<1.

More general native charge-weighted ratios can be substituted with the corresponding uniform comparison to |tau|. This is an explicit consumer assumption; no all-subsets stochastic domination is needed.

For a fixed valid tau, removal sigma -> sigma+tau on the event tau subset sigma is injective and remains in the valid syndrome space. Summing the displayed ratio gives

  P(tau subset sigma and any further witness conditions) <= z^{|tau|}.

The additional event restrictions can be dropped after the injective map. Even if the image no longer realizes the same two-run witness, this probability bound is unchanged. Sections 3–4 provide the stronger actual decoder removal statement, but algebraic validity plus this injection already suffices for the ratio estimate.

Summing over rooted witnesses yields

  P[fixed-qubit logical decoder instability]
    <= B exp[-c(z) min{2^h,d/S_h(K)}]

for sufficiently small z. The same optimized exponents as the earlier theorem follow. Unlike the all-subsets proof, every witness used here is a valid removable syndrome subset, so a native local-ratio theorem restricted to valid removals can consume it.

## 8. Boundaries and remaining obligations

- Local residual-row identities and their full charged operand stencils must be verified for the actual maps, including auxiliary correction and alignment variables. A chain identity on the unrestricted valid input is not alone a certificate that its support separates correctly.
- The finite terminal bag is essential to this proof of restriction validity; a large disconnected terminal decoder cannot silently replace it.
- Zero stencils may join nearby charged components but cannot recursively propagate without charge.
- Complete packet-block ownership and deletion-stable component construction must be verified. Finite-state charge contraction by itself gives neither.
- Common lifts are the clean version. Branch-dependent lifts need the fully charged homotopy support condition already stated in THEOREM.md, and those homotopy variables must also enter the restriction identities.
- A positive hard-core polymer representation would require a separate insertion/compatibility and bijection proof. Deletion closure and valid removable components alone do not establish that representation.

The actual ell8 and native local-ratio application remain conditional on these explicit interfaces. The full-trace construction is a route to a stronger consumer, not a declaration that the family-specific obligations are already solved.
