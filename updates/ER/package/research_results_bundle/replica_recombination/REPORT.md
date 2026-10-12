# Three-replica local recombination: a constructive audit

## Decision

**No candidate from this investigation qualifies as a historic scientific or technological breakthrough.** The concrete operation below is valid, but it relocates the difficult sampling problem into a frustrated three-state model. This is a useful exact diagnostic and a restricted computational primitive, not a new general solver. No novelty claim is made for replica recombination, cluster moves, or tree-based dynamic programming.

The investigation also screened autonomous local quantum-error decoding. Primary literature already implements the wavefront/cluster idea that initially looked promising, so that direction was not claimed as an invention. The concrete mathematical work here concerns a different operation: recombining configurations of a frustrated material without paying an exponentially small acceptance probability for an arbitrary global proposal.

## Intended capability and proposed operation

Intended capability: obtain genuinely new, equilibrated low-energy configurations of a frustrated many-body system without waiting for local thermal dynamics to cross its barriers.

Let a binary-spin model on a graph have

H(x) = -sum_(ij in E) J_ij x_i x_j - sum_i h_i x_i.

Keep three replicas at the same inverse temperature beta. At each vertex independently, allow its three spin values to be reassigned among the three replicas. This preserves the sitewise multiset, but can assemble new full configurations from portions of the old ones. The ambitious proposed step was to resample the entire assignment jointly, conditional on these multisets. If achievable cheaply, it would be a rejection-free, highly nonlocal recombination operation.

This is different from merely permuting entire replicas or their temperatures. A whole-replica permutation makes no new configurations.

## Exact constructive identity

A vertex is unanimous if all three spins agree. Otherwise it has a majority sign s_i in {-1,+1}, and one minority replica label c_i in {0,1,2}. At a mixed vertex,

x_i^(a) = s_i [1 - 2 1(a = c_i)].

For an edge joining two mixed vertices,

sum_a x_i^(a) x_j^(a) = s_i s_j [-1 + 4 1(c_i = c_j)].

Every local-field term is constant under recombination. Every edge incident on a unanimous vertex is also constant. Therefore, on the graph induced by mixed vertices,

sum_a H(x^(a)) = C - 4 sum_(ij) J_ij s_i s_j 1(c_i = c_j).

Consequently, exact conditional recombination is precisely a signed three-state Potts sampling problem with coupling K_ij = 4 J_ij s_i s_j.

This gives a complete algorithm whenever that conditional Potts model is tractable. Resample its labels and reconstruct all three replicas. Since the step is a heat-bath update on a partition of the joint state space, it preserves the joint equilibrium law of the three replicas. It can be combined with any other equilibrium-preserving updates. The recombination operation alone is not generally ergodic.

### Constructive leverage that survives

If the mixed-vertex graph is a forest, arbitrary signed couplings pose no difficulty. Compute messages toward a root:

M_(i->j)(c_j) = sum_(c_i) exp(beta K_ij 1(c_i=c_j)) product_(k child of i) M_(k->i)(c_i).

Sample the root from its normalized message product, then each child conditional on its parent. There are three labels and nine pair combinations per edge. This is linear work in the mixed forest size, plus the cost of reading the replicas and graph. Bounded-treewidth mixed subgraphs similarly give a cost exponential in their treewidth, rather than in their number of vertices.

Thus a large nonlocal move is constructively available when the *observed conditional interaction graph* is structurally simple. However, that favorable structure has not been shown for the scientifically difficult systems motivating the operation. This is not an improvement over existing general dynamic-programming principles.

## Decisive barrier, shown constructively

Put the multiset {+1,+1,-1} at every vertex and set every J_ij = -1. Then s_i = +1 and

sum_a H(x^(a)) = -|E| + 4 times the number of monochromatic edges of c.

A minimum-energy recombination has total energy -|E| exactly when the input graph has a proper three-coloring. Thus an efficient unrestricted zero-temperature recombination solver would directly solve graph three-coloring. At positive temperature the conditional problem remains a frustrated Potts model; no general mixing improvement follows from the change of representation.

This is not an impossibility theorem for every useful recombination algorithm. It identifies the actual work still owed: construct a cheap assignment update that creates materially new configurations in the difficult regime, rather than silently assuming an exact conditional solver.

Two additional failures prevent easy escalation:

1. If the replicas agree at every vertex, there is only one possible recombination. The operation cannot discover absent local alternatives.
2. Increasing replica count expands the available assignments but also expands the conditional alphabet. For m binary replicas, a site with k negative spins has binomial(m,k) assignments. At independent unbiased sites, the fraction of mixed vertices is 1 - 2^(1-m): 1/2 for m=2, 3/4 for m=3, and 1023/1024 for m=11. More replicas do not automatically create a sparser conditional graph.

## Full resource accounting

For m replicas, N vertices and E supplied edges:

- Input acquisition: at least O(mN + E) values must be supplied or already stored; constructing the conditional graph is not free.
- Storage: O(mN + E), plus conditional messages or tables.
- Explicit output: O(mN) if all updated configurations are returned. Updating only changed sites can reduce internal writes, not the cost of requesting all spins.
- General exact three-replica enumeration: 3^u assignments for u mixed vertices. The provided audit intentionally pays this cost on a tiny instance; it is not advertised as a scalable solver.
- Forest case: O(u + E_mixed) arithmetic operations after acquisition, with constants corresponding to a three-state alphabet. For treewidth t, tables have order 3^(t+1) entries.
- Numerical precision: energy identities in the audit use integer arithmetic and are exact. Reported Gibbs-probability comparisons use ordinary double precision. A guaranteed total-variation error epsilon for a sequential sampler requires controlling cumulative conditional errors, for example to epsilon/u per step; probabilities cannot be treated as cost-free exact real numbers. Log-domain arithmetic and adequate precision are required for large beta times coupling magnitudes.
- Physical feasibility: this is a classical software operation. It assumes neither an analog ground-state oracle nor uncharged physical equilibration. It makes no claim about physical fabrication or experimental implementation.

## Reproducible check

Files:

- check_recombination.py: standalone Python 3, standard library only
- results.json: complete generated output

Run:

python3 check_recombination.py results.json

The fixed eight-vertex, ten-edge signed instance has five mixed vertices. Exhaustive evaluation of all 243 distinct recombinations gave:

- Maximum integer energy-identity error: 0
- Maximum direct-versus-reduced Gibbs-probability error: 0.0 in double precision
- Sitewise multiset preservation: true

Independent exhaustive coloring checks gave:

- Triangle: 27 assignments; minimum total energy -3; six ground assignments; proper three-coloring exists
- K4: 81 assignments; minimum total energy -2, versus the unattainable proper-coloring target -6; every assignment has at least one monochromatic edge

These checks verify the algebra and implementation. They do not measure useful thermodynamic mixing, establish an asymptotic sampling gain, or validate novelty.

## Selective primary-source checks

The initial local-decoding idea is already substantially represented by:

- Ziad et al., Local Clustering Decoder: a fast and adaptive hardware decoder for the surface code: https://arxiv.org/abs/2411.10343
- Herold et al., Cellular-automaton decoders for topological quantum memories: https://arxiv.org/abs/1406.2338

Replica permutations themselves are also established machinery:

- Itoh and Okumura, Replica-Permutation Method with the Suwa-Todo Algorithm beyond the Replica-Exchange Method: https://arxiv.org/abs/1210.6505

That last reference concerns replica/parameter permutations, not a priority determination for the exact sitewise identity developed above. The literature check was selective and does not establish novelty of that identity. The derivation and executable audit stand on their own.

## Unfinished obligation and stopping point

To admit this as a consequential new capability, one would need a demonstrably cheap, nontrivial conditional reassignment method for large frustrated systems, together with charged end-to-end evidence that it discovers new relevant configurations and improves the scaling of mixing. A treewidth assumption or an exact-Potts oracle does not meet that obligation. No such method was found in this round. The investigation is stopped here as requested.
