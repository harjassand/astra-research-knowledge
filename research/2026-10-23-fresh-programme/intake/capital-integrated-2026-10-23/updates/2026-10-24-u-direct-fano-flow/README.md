# Direct classical-information bound for chiral QCA records

This later selected handoff preserves the complete producer-frozen [direct classical-information/Fano source](source/DIRECT_CLASSICAL_INFORMATION_FLOW_BOUND.txt). It follows the frozen [QCA and finite-patch causal-resource update](../2026-10-24-pro-qca-causal-resource/README.md) and the earlier [common-filter/QCA handoff](../2026-10-24-u-common-filter-qca/README.md). Those earlier updates and their source statements are unchanged. The [source manifest](source_manifest.json) records the capture and review scope.

The dispatcher receipt identifies one 11,194-byte source capture, marked “producer-frozen internally reviewed theorem/source comparison”; its scope is exact pin preservation and byte readback only. This integration verified the captured file against the receipt hashes. It did not replay a proof or perform a full independent proof audit, novelty review, or physical validation. The source's report of internal algebra/source challenges is retained as producer-reported status, not newly certified here.

## Entropy and finite-collar claim

The captured source first derives a two-sided conditional-entropy inequality for the outcomes `X,Y` of fixed local basis measurements on any finite bipartite state:

`S(rho_A) - S(rho_B) <= H(X|Y)` and `S(rho_B) - S(rho_A) <= H(Y|X)`.

Its displayed proof uses relative entropy of coherence and joint convexity; it also records an alternative purification/Holevo argument. It claims no new general entropy principle.

For a strict-radius-`r` one-dimensional QCA on `D`-dimensional cells, the source uses the finite canonical tracial Choi marginal around a cut. Its two crossed partitions `A=L1' R1` and `B=L1 R1'` each contain `2r` cells. With `epsilon_i` the paired classical input/output label mismatch rate and `f_D(e)=h(e)+e ln(D-1)` in nats, the source derives

`2 |ln ind(alpha)| <= sum_(i in S) f_D(epsilon_i)`.

The imported index identity is for an exact QCA. The Choi state is a proof device; the observed tag probabilities coincide with its diagonal data only under the stated product-tracial preparation. This is a classical local-mismatch statement, not a global-record-distance guarantee, coherent A-shift certification, or index assignment to an unknown noisy channel.

## Translation signature and stronger collar threshold

For a strict-radius-`R0` QCA `Omega` on joint `A_i B_i` cells, let `sigma` be the reference right shift on A and identity on B, and set `alpha=sigma^-1 composed with Omega` with safe radius `r=R0+1`. The tested signature compares A input at `i-1` with A output at `i`, and B input at `i` with B output at `i`. It does not require an exact A-only channel or one-site translation invariance.

If `Omega` has index one, then the relative automorphism has index `1/d_A`, so each finite collar must satisfy

`sum_(i in S) f_D(epsilon_i) >= 2 ln(d_A)`.

Let `t_r` be the smallest solution in `[0,1-1/D]` of `f_D(t_r)=ln(d_A)/r`. The captured result concludes that every collar has both mean mismatch and maximum mismatch at least `t_r`; a strict maximum error below `t_r` excludes index one, while equality is not an exclusion. For fixed dimensions and large `r`, it reports

`t_r = [ln(d_A)/(r ln r)] (1+o(1))`.

It applies at every translated cut without translation invariance. The source says this Fano mechanism improves the earlier `O(r^-6)` sufficient maximum-error threshold under the matched tracial premises. A frozen uniform selector still has `O(1/r)` maximum mismatch, so a logarithmic lower/upper gap remains. Its additional quantum-encoder mean lower bound `1/(2L)` applies only to an isolated-qubit block-code/countershift architecture, not to general overlapping QCAs.

The source requires a product-tracial marginal on both rails over a finite region containing the backward cones, and a dynamics fixed independently of the sampled labels. Maximally mixed one-site marginals with unknown intersite correlations do not suffice. If only separate A/B component rates are measured, they must be combined using the source's componentwise bound; a ceiling on each individual label mass is not itself a component-total error rate.

## Physical boundary and named priors

The source allows use of an index-one circuit approximant only inside the already specified finite-patch causal-resource envelope and with its previously charged local-observable error budgets. The observed tags do not establish that envelope. It claims no affordable finite-shot assay, fixed-time gate synthesis, physical benefit, or general noisy-process index.

The captured source names [Ranard, Walter, and Witteveen (arXiv:2012.00741v2)](https://arxiv.org/html/2012.00741v2) for the QCA index/finite-collar identity, [Baumgratz, Cramer, and Plenio (arXiv:1311.0275v3)](https://arxiv.org/html/1311.0275v3) for the relative-entropy-of-coherence ingredient, and [Duschatko, Dumitrescu, and Potter (arXiv:1804.02004)](https://arxiv.org/pdf/1804.02004) as a measurement comparator. Their access and target contracts differ: the comparator uses nondynamical ancillas and chiral mutual information, while this source's Choi state is a proof device and its target is a narrower classical translation/index-one exclusion. No automatic dominance or low-cost assay follows. The primary citations were consulted for bibliographic/locator context only; no comprehensive literature or novelty review was done.

The earlier `DIRECT_FANO_OPENING.txt` named by the captured source is not copied in this update. The previous QCA handoff remains frozen with its original scope and pending independent-challenge header. No scientific script, numerical replay, experiment, or claim promotion accompanied this integration.
