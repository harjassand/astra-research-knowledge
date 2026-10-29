# Metric-tree equilibrium closure: bounded primary-source comparison

29 October 2026. Review by `controlled_realization_frontier` for the root construction in `COMPLETE_EQUILIBRIUM_INFORMATION.md` and the accompanying `history_realization/METRIC_TREE_EQUILIBRIUM_CLOSURE.md`.

## Finding

No direct statement of the assembled equivalence was found in the inspected primary passages:

> Consistent positive observed extensions to every rational metric tree, including subdivision, are equivalent to rational-cylinder approximation by stationary finite reversible CTMC observations.

Nor did the inspected entropy or compatibility papers establish the associated complete finite-word test family for positivity of the robust all-even entropy floor over unbounded hidden dimension and rates. This is a bounded collision assessment, not a historical-priority certificate.

Several broad descriptions would nevertheless overclaim. Hidden Markov representation of invariant infinite-degree tree processes is classical. Positive-extension hierarchies, finite incompatibility witnesses, and complete LP tests with unrestricted latent cardinality also have direct precedents. Additive reversibilization as an information projection is explicitly established. The candidate addition is the particular **metric-subdivision and finite-CTMC closure bridge**, followed by the robust-dissipation consequence, with its all-even physical class and observation topology stated.

## Closest primary results

### Aldous 1985: the invariant-tree representation is already a theorem

[David J. Aldous, *Exchangeability and related topics*, Saint-Flour 1983 lectures, LNM 1117 (1985)](https://www.stat.berkeley.edu/~aldous/Papers/me22.pdf), Theorem 13.5, printed p. 111; associated remarks on p. 114.

Theorem 13.5 represents every invariant process on the countably infinite-degree tree as a coordinatewise measurable observation of an invariant Markov tree process. The displayed proof idea constructs branch directing measures from exchangeability. The adjacent remarks distinguish the infinite-degree result from finite-degree trees, for which its conclusion can fail.

This directly covers the uncolored representation mechanism. The present proof must retain attribution even though its empirical-moment construction is a different presentation. What the inspected theorem does not state is a rational edge-length semigroup enforced by subdivision, approximation by finite CTMCs, or an entropy-inference consequence. Countably colored compatibility and the dense branch algebra are extensions needed for that assembled interface.

Reading receipt: the author-hosted PDF fetch timed out; its own indexed passages containing Theorem 13.5 and the relevant remarks were read through the search service. References `turn605search12`, `turn600search16`. This is not a claim of complete PDF retrieval.

### Freedman–Lovász–Schrijver: connection algebra and finite-state reconstruction

[M. Freedman, L. Lovász and A. Schrijver, *Reflection positivity, rank connectivity, and homomorphism of graphs*, JAMS 20 (2007), 37–51](https://homepages.cwi.nl/~lex/files/hom-final.pdf), definitions in §2 and Theorem 2.4.

Their theorem reconstructs a finite weighted target graph from reflection positivity together with an exponential connection-rank bound. The paper explicitly uses commutative finite-dimensional algebras. It is a direct antecedent to identifying finite branch-algebra rank with a finite hidden realization.

The hypotheses concern graph parameters on all finite graphs and bounded rank connectivity; edge weights may be real rather than Markov transition probabilities. The proposed closure theorem instead has only tree-extension data, probability consistency, no rank bound, and a compatible family indexed by positive rational duration. Their theorem cannot simply be cited as already proving that statement, but finite algebra reconstruction is not a new primitive here.

Reading receipt: original definitions, Theorem 2.4 and surrounding proof setup; `turn599view1`, `turn600view0`.

### Lovász–Szegedy: complete positivity criteria for model closure are also established

[L. Lovász and B. Szegedy, *Limits of dense graph sequences*, arXiv:math/0408173v2 (2004)](https://arxiv.org/pdf/math/0408173), Theorem 2.2 and discussion immediately following it.

The theorem equates graph-density closure, representation by a symmetric measurable graphon, and normalized multiplicative reflection-positive parameters. It also gives an equivalent family of nonnegative transformed graph parameters. The paper explicitly interprets its characterizations as complementary membership and nonmembership descriptions.

This is a strong precedent for the general strategy of a positive extension/connection hierarchy characterizing a closure without bounding the number of latent states. It is not the metric-tree CTMC statement: its objects are dense-graph homomorphism densities with a bounded symmetric kernel, indexed by all finite graphs, and it has neither physical clocks nor an entropy rate. Broad language presenting complete positive hierarchies themselves as the invention should be avoided.

Reading receipt: §2.5, Theorem 2.2, remarks, and the construction/consistency implications around §§5.7–5.9; `turn604view2`, `turn602view2`.

### Backhausz–Szegedy: reversible kernels as symmetric couplings

[Á. Backhausz and B. Szegedy, *Action convergence of operators and graphs*, Canadian Journal of Mathematics 74 (2022), 72–121](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/F5900CA5BE554C9F4DEAAB518962D2DD/S0008414X2000070Xa.pdf/action-convergence-of-operators-and-graphs.pdf), DOI 10.4153/S0008414X2000070X, Theorem 6.3 and Remark 6.5.

They represent selfadjoint positivity-preserving graph operators by symmetric measures on the product space. For a Markov graph operator, this is a symmetric self-coupling of its stationary probability space; disintegration gives the kernel. The following section studies finite partition quotients.

This directly precedes the symmetric endpoint-coupling and disintegration step. The selected theorem starts from one operator or coupling. It does not recover a common continuous-time semigroup from arbitrary compatible observed metric-tree tables, nor characterize a passive observation law's finite-CTMC closure. No stronger negative statement about the entire operator-convergence literature is intended.

Reading receipt: Theorem 6.3, Remarks 6.4–6.5, start of §7; `turn604view1`.

### Kunszenti-Kovács–Lovász–Szegedy: unrooted Markov-tree propagation and marginals

[D. Kunszenti-Kovács, L. Lovász and B. Szegedy, *Subgraph densities in Markov spaces*, arXiv:2206.04493v2 (2023)](https://arxiv.org/pdf/2206.04493), DOI 10.1016/j.aim.2023.109414, §§4.1–4.2, Lemma 4.2 and equation (21).

Starting from a Markov space, they construct random mappings of trees by conditional propagation. Lemma 4.2 establishes independence from the chosen search order/root, using symmetry; equation (21) gives consistency on connected subtrees. These are direct precedents for the easy direction from a reversible kernel to compatible unrooted tree laws.

The examined sections assume the Markov space. They do not give the inverse reconstruction from observed path tables, common real-time subdivision identities, or finite-rate CTMC approximation of the observations. Their later graph-subdivision constructions concern assembling graph measures, not the temporal identity `K_(s+t)=K_s K_t` claimed here.

Reading receipt: §§4.1–4.2 and §5.1's subdivision definition; `turn604view0`, `turn603view2`.

### Wolfer–Watanabe: the reversible information projection is a direct collision

[G. Wolfer and S. Watanabe, *Information Geometry of Reversible Markov Chains*, Information Geometry 4 (2021), 393–433](https://doi.org/10.1007/s41884-021-00061-7), Theorem 7 and Remark 6.

Theorem 7 explicitly identifies `(P+P*)/2` as the KL m-projection onto reversible kernels and supplies a Pythagorean identity. It also gives the opposite-direction projection using a geometric mean followed by stochastic rescaling. The additive projection preserves the stationary law; the other generally does not.

Thus selecting additive reversibilization as the closest full-state model is established. Continuous-time path comparison obtained by its generator analogue should be presented as a transfer tool, not a new information geometry. The paper fixes a finite underlying state space and does not characterize unbounded hidden observation models. The root's new question is the observable closure and complete robust detection, not the additive projection formula.

Reading receipt: Theorem 7, proof and interpretation, Remark 6; `turn597view0`, `turn597view1`.

### Navascués–Wolfe: complete LP compatibility with unrestricted latent spaces

[M. Navascués and E. Wolfe, *The Inflation Technique Completely Solves the Causal Compatibility Problem*, Journal of Causal Inference 8 (2020), 70–91](https://doi.org/10.1515/jci-2018-0008); [primary preprint v3](https://arxiv.org/pdf/1707.06476), §3 equations (7)–(10), §4.2 and Theorem 1.

Inflation gives complete LP compatibility tests without prescribing latent state spaces. Its de Finetti argument proves convergence and finite detection of every incompatible distribution; it also supplies a quantitative approximation rate for its finite causal scenario. This is a direct antecedent to the broad methodological claim of positive extensions, symmetry, LP duality and latent-dimension-independent completeness.

The distinction is substantive. Its inflation marginals are fixed to tensor powers of the observed law, so dual witnesses are generally polynomial in that law. The root's equilibrium class includes mixtures and has linear extension constraints, yielding one linear statistic on a single observed time grid. Inflation also does not itself supply a reversible continuous-time semigroup or entropy-production transfer. Its quantitative convergence theorem cannot be imported to the new hierarchy.

Reading receipt: introduction, equations (7)–(10), Theorem 1 and §4.2; `turn606view0`, `turn607view0`.

## What remains distinctive in the current statement

The following package was not located as one theorem in the bounded primary reading:

1. The actual input is a stationary finite-alphabet law on rational time cylinders, with a memoryless sensor.
2. The latent certificate consists of **positive probability tables for all finite metric trees**, not merely Gram or CP matrices at reflected path cuts.
3. Leaf consistency and metric subdivision act on all attached branches. The dense branch algebra converts the latter into one semigroup on a common hidden probability space.
4. Poissonization followed by sensor-refining finite partitions bridges that semigroup to finite reversible CTMC **observation closure**, while allowing dimension and clocks to grow.
5. Compactness and rational linear separation then give a complete finite LP family. Additive reversibilization transfers a strict observable separation to a positive robust all-even entropy floor.

The first four items specify the representation class and topology. The last item turns it into an inference consequence. The proof is an assembly of classical existence mechanisms with this specific interface. This review does not establish that any individual representation primitive is new, nor that the resulting hierarchy is practically efficient.

## Strongest equally informed comparisons

The relevant conventional benchmark depends on information actually given.

- With a known finite hidden topology, state count or clock cap, constrained hidden-model minimization can exploit that information and give a stronger numerical entropy bound. The uncapped closure result does not supersede it.
- With the full hidden generator, additive reversibilization and its information projection already apply. The hierarchy is unnecessary.
- With only acquired passive word probabilities and the all-even physical class, the complete tree family addresses an uncapped compatibility question. Finite levels remain ordinary LPs, and the KL-distance variant remains ordinary convex optimization.
- Established time-asymmetry, correlation and CP witnesses can be cheaper. Current Astra N507 shows why reflected-history CP is incomplete, but it is retained only at its existing source and internal-review scope. No new counterexample or numerical advantage is claimed here.

No inspected source gives a tight numerical entropy estimator from the proposed full hierarchy. The current conclusion is **complete detection of a strictly positive robust floor**, not equality between a hierarchy value and the exact-model entropy infimum. The exact/closure distinction and arbitrary hidden rates must remain in the headline statement.

## Retrieval limits

Seven closest primary sources were read selectively, chiefly their named theorems and decisive definitions. No archive was preloaded. Targeted searches did not reveal the exact metric-tree/finite-CTMC observation equivalence or its complete entropy-test consequence. Absence from this search is not evidence of absence from the literature.

An adjacent lead, Abel Klein's *A Generalization of Markov Processes* (1978), was accessible only as an iframe in the primary service and its PDF fetch failed. Secondary snippets were used only to identify that lead; no claim in the comparison rests on an unread Klein theorem. Its OS-positive-semigroup setting would need a separate focused check if used as a load-bearing antecedent. This task does not re-audit the accepted Astra CP obstruction.

No numerical sweep, new fixture, physical acquisition, or operational advantage claim was added.
