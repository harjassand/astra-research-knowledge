# A conditional constant-block scaffold algorithm

This is an explicit acquisition-and-verification procedure with polynomial dependence on m WHEN the listed observable algebraic tests pass. It is not proved to pass generically, and the fixed-size seed algebra can be expensive. In particular this is not yet a practical complete generic binary learner.

## Actual binary schedule

Choose a five-node seed K, n=m−5 remaining nodes. Query every T∪U with T⊆K and U⊆[m]\K, |U|≤2. This costs exactly

32[1+n+C(n,2)]

distinct scalar settings. For m≤5 simply acquire all states. No continuously valued control is requested. The schedule includes baseline and all singletons, hence fixes f0 and a. Assume a_i≠0; otherwise this particular weighted-transpose check is inconclusive.

## Exhaustive constant-size reconstruction stages

1. Solve the seed's full 32-state polynomial system in its 20 directed B entries, saturating/clearing only with explicit nonzero determinant conditions. Enumerate ALL real solutions. If the valid seed fiber is positive dimensional, report inconclusive. Empty fiber is model/data inconsistency. A zero-dimensional fiber has a number of solutions bounded by a constant independent of m: degrees are ≤5, and a coarse fixed-dimensional algebraic bound suffices. The generic seed fiber is finite by the exact full-rank witness in RESULTS.md.

2. For each seed solution C, and each outside node i, solve all seed-context observations g(T∪{i}) for the 10 directed seed–node entries. Enumerate all real extensions satisfying the original nonsingular rational equations. A positive-dimensional extension fiber makes this seed branch unresolved; report inconclusive unless independent constraints rigorously eliminate that entire branch. An empty extension list eliminates the seed branch. Each finite list has size bounded by a constant independent of m because there are ten variables and fixed degrees ≤6. Even though the actual seed has generically finite extensions, no claim here ensures every spurious seed branch does.

3. For every pair of outside nodes i,j and each pair of their extension candidates, use contexts ∅,{k0},{k1}, where k0,k1 are fixed distinct seed nodes, in the exact 3×3 pair formula of RESULTS.md. For this conservative version, require every such matrix to be invertible; otherwise report inconclusive rather than discarding a possibly true branch. Recover x,y,z; require z=xy, then check all 32 pair-context rational readings and their nonzero denominators. Passing combinations define a binary compatibility relation R_ij on the two constant-size extension lists. A failing combination is rigorously impossible under the model. Entries x,y for a passing combination are unique.

No assumption of an unknown minimum singular value is used to select a branch. These are exact-equality tests; finite precision would require rigorous enclosures and exclusion tests and can remain inconclusive.

## Checkable star rigidity avoids the exponential product

For each surviving seed branch choose an outside reference node r. Require this property:

For every candidate c of r and every outside i≠r, at most ONE candidate of i is compatible with c under R_ri.

The property is directly checked from the finite tables. A zero-compatible count invalidates that reference candidate. Otherwise c determines one candidate at every node. Check ALL pair constraints on this proposed assignment, not just the reference edges. Retain precisely the assignments passing them all. There are at most D assignments per seed, with D the constant candidate-list bound. Any globally compatible assignment contains one reference candidate and, by star rigidity, must be among those tested. Thus this enumeration is complete, with no exponential Cartesian product.

If no reference node satisfies the property, the procedure reports inconclusive. One may check each possible reference node in polynomial time. The compatibility problem without this property is a dense finite-domain binary CSP; constant alphabet alone does not make arbitrary such problems easy. Its special algebraic structure might support stronger propagation, but that is not assumed here.

## Certifying the ENTIRE binary map

Each retained assignment constructs a complete B: seed edges, seed–outside edges, and uniquely recovered outside-pair edges. Every model compatible with the acquired data is represented in this finite list, provided all exhaustive stages and rigidity tests succeeded.

Choose one retained matrix B*. Check that every retained matrix is either exactly B* or diag(a)^−1 (B*)ᵀ diag(a). If not, report inconclusive (do not assume matched low-order readings imply matched future states). If yes, all compatible models predict the same response for EVERY binary subset by weighted-transpose invariance. In particular the true promised model is in the list, so B* predicts its full binary map. The same argument transfers all-subset nonsingularity from the promised true model; an exponential inverse check is unnecessary. No claim of feasibility is made if the data fail the supplied-model premise.

This is a sufficient certificate of identification, not merely a good fit or held-out error test. Some inequivalent matrices can conceivably encode the same complete map; rejecting them is conservative.

## Cost and unresolved questions

With k=5 fixed, the number of seed candidates C and per-node extension candidates D are constants bounded independently of m. Conditional on exhaustive finite solution lists, all subsequent work is O(C D² m²) constant-sized arithmetic (or O(C D² m³) if scanning all reference nodes naively). Prediction is one m-dimensional solve. Exact fixed-dimensional real algebraic solving is theoretically available, but its constants and bit costs may be substantial. Inputs must have a supported exact representation; idealized arbitrary real readings are not ordinary finite-bit data. Numerical optimization with many starts is not an exhaustive solver and cannot certify these lists.

The seed-solving cost is fixed in m, unlike enumerating 2^m binary states offline. This removes one asymptotic obstacle conditionally, but it does NOT establish practical preprocessing or a uniform finite-noise stopping time. There is no proof yet that all the finite-list, nonsingular-pair, star-rigidity, and final equivalence tests hold on a nonempty Zariski-open set for this schedule. That is the decisive missing theorem. A successful exact synthetic instance would establish only pointwise success; a physical measured-data gate remains separate.

Known-block numerical experiments in extension_fit.py used random moderate couplings and 50 least-squares starts at each k=3,4,5,6. At each size, only the true extension was found among near-zero-residual solutions; several starts stalled at nonzero residual. extension_fit.json records these outcomes. This suggests a useful algebraic uniqueness conjecture but proves neither complete real-root enumeration nor generic uniqueness and must not be used as the certificate's solver.

### Exact-output representation caveat

The reconstructed matrix should be returned as compact local algebraic representations, with a scalar prediction expressed as an algebraic arithmetic circuit or a numerically evaluated solve. Local compatibility tests involve bounded-degree compositions of only a seed and a constant number of extensions. A global predicted scalar can lie in an algebraic extension whose minimal-polynomial degree grows exponentially with m. The arithmetic-operation count is not a polynomial Turing-time guarantee for expanded exact scalar output. Rigorous approximate prediction additionally requires precision and conditioning analysis.

### Executed exhaustive attachment certificate

exact_extension.py and exact_extension_receipt.json give a rational three-known-anchor example. Seven actual binary marginal responses determine the six directed connections of one new node uniquely. Singleton equations solve each v_i rationally in u_i. The remaining three pair-context equations and one triple-context equation have total degrees 3,3,3,4. Exact rational Gröbner elimination yields a triangular basis with two candidate u vectors. One is the true extension (u=(1/10,1/11,1/12), v=(1/13,1/14,1/15)); the other lies at all three singleton-elimination poles with nonzero equation numerators and is excluded. The script verifies the true solution in every original nonsingular rational equation, and proves that no solution was lost by division at a singleton pole. Thus the extension list is exhaustively a singleton, not a multistart optimization result.

This proves nonvacuity of the attachment/rigidity component when this anchor block is already known. It does NOT certify acquisition of the unknown five-node seed, and is not a complete pass example for the end-to-end schedule. No generic uniqueness conclusion is inferred from a single Gröbner specialization; other branches could escape to infinity under specialization.
