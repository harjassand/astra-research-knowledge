# Primary-paper novelty ledger: energy queries and graph reconstruction

**Search date:** 14 October 2026. This is a targeted novelty audit, not an exhaustive historical priority search. Only original research papers are listed below; secondary surveys and third-party manuscripts were not used as novelty evidence.

| Primary work | Primary record | Relevant result/model | Implication for FH acquisition |
|---|---|---|---|
| Vladimir Grebinski and Gregory Kucherov, “Reconstructing a Hamiltonian cycle by querying the graph: Application to DNA physical mapping,” *Discrete Applied Mathematics* 88 (1998), 147–165. DOI [10.1016/S0166-218X(98)00070-5](https://doi.org/10.1016/S0166-218X(98)00070-5). | Publisher record/abstract: [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0166218X98000705). | The authors model multiplex-PCR genome mapping as several combinatorial group-testing query models for finding an unknown Hamiltonian cycle and give efficient algorithms matching the information-theoretic lower bound. | Hamiltonian-cycle recovery from subset/count queries is old prior art. The FH shared-tree rule should not be described as a new graph-reconstruction primitive. The source's energy oracle is a way to realize an established count query inside a strong pairwise class. |
| Vladimir Grebinski and Gregory Kucherov, “Optimal reconstruction of graphs under the additive model,” *Algorithmica* 28(1) (2000), 104–124. DOI [10.1007/S004530010033](https://doi.org/10.1007/S004530010033). | Original conference version/publisher abstract: [Springer ESA ’97 chapter](https://link.springer.com/chapter/10.1007/3-540-63397-9_19). | The abstract defines additive combinatorial graph reconstruction and states that bounded-degree graphs of maximum degree `d` can be reconstructed nonadaptively using `O(dn)` queries, asymptotically matching the information-theoretic lower bound. It also gives `O(n²/log n)` for general graphs. | For degree two, a linear-query graph-reconstruction baseline predates the proposed `O(n log n)` tree learner. This is a query-model comparator only; its exact constants and an apples-to-apples number of FH energy masks were not reconstructed here. |
| Sung-Soon Choi and Jeong Han Kim, “Optimal query complexity bounds for finding graphs,” STOC 2008, 749–758; journal version *Artificial Intelligence* 174 (2010), 551–569. DOI [10.1145/1374376.1374484](https://doi.org/10.1145/1374376.1374484) / [10.1016/j.artint.2010.02.003](https://doi.org/10.1016/j.artint.2010.02.003). | Primary publisher abstract record: [ScienceDirect journal version](https://www.sciencedirect.com/science/article/pii/S0004370210000251). | The paper treats additive queries (edge count/weight inside a vertex set) and cross-additive queries (edge count/weight between disjoint sets) for hidden-graph reconstruction. | The FH ratio `log R_i(A)` is precisely the cross-additive count between `{i}` and `A` in the homogeneous equal-coupling graph. The query primitive is therefore in an established model. The original publisher page was inaccessible to the web reader; only its indexed abstract was available. |
| Sung-Soon Choi, “Polynomial Time Optimal Query Algorithms for Finding Graphs with Arbitrary Real Weights,” COLT 2013, PMLR 30:797–818. | Original proceedings page and abstract: [PMLR](https://proceedings.mlr.press/v30/Choi13.html). | Defines additive and cross-additive weighted-graph queries and gives randomized polynomial-time algorithms with optimal query complexity for arbitrary real edge weights. | Stronger evidence that graph support/weight reconstruction via additive information is an established research area. The source's exact cycle query decoder is specialized to its model and finite-size cache accounting; no novelty claim should extend to additive graph learning. |

## Exact relationship to the proposed energy learner

For a pairwise homogeneous cycle and `i notin A`,

`D_i(A) = E(A)+E(i)-E(A+i)-E(empty) = log R_i(A) = 2 log(t) · |N(i)∩A|`.

Thus, after the coupling scale is calibrated, one such energy contrast returns the exact integer number of edges crossing from the singleton `{i}` to subset `A`, up to a known scale. In the established cross-additive model this is a star-restricted quantitative count query. It can be viewed as quantitative group testing of a degree-two neighborhood. The new contribution, if any, is limited to engineering a balanced shared set-mask cache for this energy API and its end-to-end integration with the FH certificate. It is not a new graph-query model or a new group-testing principle.

There is also a stronger theoretical baseline mapping. A single energy query on configuration `S` gives

`s(S) = [log W(S)-|S| log r]/log t = n-cut(S)`.

For a 2-regular graph, `cut(S)=2|S|-2e(S)`, hence

`e(S)=|S|-(n-s(S))/2`.

After constant-size calibration of `t` and uniform `r`, each classical additive induced-edge query can therefore be simulated by one energy-mask query. The Grebinski–Kucherov bounded-degree theorem has `O(dn)` nonadaptive additive queries, giving an `O(n)` theoretical query baseline at `d=2`; this is asymptotically stronger than the proposed adaptive `O(n log n)` tree traversal. Calibration overhead is constant under the same class promise. We did not reconstruct their exact separating-matrix design, extract its finite-n constant, or run it against the FH mask oracle, so this is a query-model baseline, not a matched finite-size head-to-head.

## Audit boundary

The citation audit does not compare the exact constants or physical preparation/calibration costs of the proposed mask cache against the classical separating-matrix algorithms. The observed 183–223 energy-mask calls at n=24 are a valid synthetic count for the present algorithm, but are not a head-to-head operational advantage. The literature search did not find or establish novelty of the full combination of FH spectral complement bound, full-source residual closure, preparation conversion, and uncertainty treatment. No historical priority claim is supported.
