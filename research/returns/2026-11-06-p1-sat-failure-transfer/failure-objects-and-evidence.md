# Explicit failure objects and finite evidence

These objects are supplied in the [object-only packet](package/TRANSFER_OBJECTS.json), with complete proofs in the [research note](package/RESEARCH_NOTE.txt) and [visible return](P1_SAT_FAILURE_TRANSFER_20261106_RETURN.txt). No unrestricted SAT lower bound follows.

For a prism graph with `v=2k` vertices and `e=3k` edges, put a variable on each edge and a degree-three parity constraint at each vertex. Four 3-clauses encode each vertex. All-even charges give SAT; one odd charge gives UNSAT. There are `3k` variables, `8k` exactly-three-literal clauses, eight occurrences per variable, and binary length `Θ(k log k)`.

With violated-clause count `E`, equal to violated vertex constraints, their partition functions are `2^(e−v)[(1+q)^v±(1−q)^v]`. Their difference vanishes to order `v` at `q=1`; derivatives/factorial and ordinary violation-count moments through order `v−1` coincide, despite opposite zero-energy satisfiability. The nine-variable/24-clause `k=3` pair has histograms `[16,0,240,0,240,0,16]` and `[0,96,0,320,0,96,0]`, with first five moments equal. Selector variants have the same branch-restricted summaries but low-temperature marginal difference `((1−q)/(1+q))^v>1/4`, defeating an additive-`1/8` readout based **only on that shared summary**.

The falsified claim is universal recovery of zero-violation satisfiability or those marginals from a truncated order `r<v` violation-moment/Taylor summary. It does not exclude processing original clauses, other statistics or higher-order data. These parity instances themselves have efficient linear-algebra algorithms.

The second family is `T_k=(s∨a)∧(s∨¬a)∧∧_i(¬s∨¬x_i)`, with `k+2` variables/binary clauses and no units. Exactly two assignments satisfy: `s=1,x=0`, arbitrary `a`. Energy is1 for `s=0`, otherwise `|x|`. At `q=2^(−2k−6)`, `A={s=0}` has equilibrium mass at most `2^(−k−6)`, but uniform initialization puts mass1/2 there. For random-scan exact single-site heat-bath updates, reflected-chain escape satisfies `φ_k≤2^(−k)`. For integer `t≤2^(k−2)`, selector error remains at least `3/8−2^(−k−6)>1/4`.

Thus this particular uniform-start local sampler cannot uniformly acquire the required marginal in polynomially many updates, even using exact transition probabilities. The bound is exponential in `k` and superpolynomial in complete `Θ(k log k)` input length. Binary-clause padding `(C∨z_C)∧(C∨¬z_C)` preserves violated-clause count for every padding assignment, yielding exactly-three-literal examples. This does not exclude preprocessing, nonlocal moves, new representations or arbitrary SAT algorithms; the unpadded family is efficiently solvable 2-CNF.

| Producer-reported exact check | Finite scope |
|---|---:|
| Conditional rounding under bounded adversarial estimation errors | 3,444 small CNFs plus4 edge cases |
| Prism moment / selector moment pairs | 3 /3 |
| Local Gibbs traps / energy-preserving padding | 10 /4 |
| Known-witness marginal identities | 55 |
| Functional gate truth-table cases | 16 |
| Parsimonious3-CNF examples | 2,048 original assignments each |

The supplied [checker](package/verify.py) uses exact integers/fractions and **exhaustive enumeration** to obtain reference marginals, with no external SAT solver. Passing finite tests verifies those identities/fixtures at that scope, not general correctness or polynomial complexity of a missing estimator. Capital preserves [results](package/results.json), [known-witness instances](package/KNOWN_WITNESS_INSTANCES.json), [all member hashes](package/MANIFEST.json), and the original ZIP unchanged, without executing the code.

The source reports no peer transfer. The packet omits preferred fixes/proof narratives for a potential coordinator-routed first transfer. Availability in public retrieval is permitted by the original nonblind experiment; it is not evidence that another role received or used the packet, that a treatment occurred, or that the coordination method works. The unrestricted target remains `NOT_RESOLVED`.
