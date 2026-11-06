# Valid Cauchy coefficient formula, higher-mode counterexample and evidence

The [returned source](P1_GLOBAL_CORRELATIONS_20261106_RETURN.txt) separates a valid special computation from an attempted extension that fails. It does not invalidate the pinned counting theorem or all determinant methods.

For an ordinary Cauchy matrix`C_ij=1/(a_i−b_j)`, Borchardt's identity gives `per(C)=det(C^∘2)/det C` under its nonvanishing conditions. Coalescing repeated **simple** columns yields a valid coefficient formula. For`Σβ_j=L`, distinct row nodes, distinct active column nodes and no poles, set

`D_(i,(j,r))=(a_i−b_j)^(−r−1)` and `N_(i,(j,r))=(r+1)(a_i−b_j)^(−r−2)`, `0≤r<β_j`.

Then `[Z^β]∏_(i=1)^L(Σ_j Z_j/(a_i−b_j))=det N/[det D∏_jβ_j!]`. Common Vandermonde factors cancel in confluence, with repeated-column permutation factors retained. Explicit rational nodes allow exact determinant arithmetic with polynomial bit cost in matrix dimension/node descriptions. This is not free division by a nonunit modulo`2^p`, and **not** the assertion `per(D)=det(D^∘2)/det D` for the higher-power matrix itself.

The actual source appendix has different powers of Cauchy denominators. The retained failure chooses even`a≥4`, `L=2^a`, `T=2L+1`, `C(T)=∏_(q=−L)^(L−1)(T−q)` and`g=C(T)/C′(0)`. At the specified source node/local tile/row slots, its mode coefficient matrix is

`M_(r,b)=g·2^b/(T+2r)^(b+1)`, `r,b∈{0,1,2}`.

The desired coefficient is`per(M)`, while the proposed quotient differs by

`det(M^∘2)/det M−per(M)=16g³/[T²(T+2)²(T+4)²]`.

Source scaling gives`v₂(g)=a+1`, so discrepancy valuation is`3a+7` and it survives precision`p=3a+8`. The first retained instance`a=4,L=16,T=33,p=20` has true permanent residue`524,288` versus quotient residue0. This is an exact failure, not numerical fitting. The source's active-call precision exceeds that threshold, so its precision rule does not automatically discard the discrepancy.

The example falsifies **that replacement on the higher-mode formula**. It does not disprove ordinary Borchardt/confluent coefficient identities, the accepted counting theorem, every determinant technique, or prove that every deterministic layout realizes the chosen local three-row configuration. Source parameters, rational descriptions and precision remain paid; no efficient unrestricted coefficient evaluator is inferred.

The [package source register](package/SOURCES.json) pins accepted N1118 at`78ff1e3a865e3d0a05af901f77eb1ffd128b00d4` and counting-source revision`7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, with exact quantitative-contraction/reduction blob identities. Prior acceptance conditions remain; the theorem is neither reproved nor relabelled polynomial. Primary determinant comparators are Ishikawa–Kawamuko–Okada and Han–Krattenthaler at the specific Cauchy identities they establish. No universal higher-mode formula is attributed to them, and Capital performed no new literature audit or source fetch.

| Producer-reported exact finite checks | Cases |
|---|---:|
| Finite-ring invariant factors/separation | 150 |
| Explicit conditional-count CNFs | 8 |
| Uniform compiler/scaled-count recovery | 38 |
| Global algorithm versus generic variable elimination | 30 |
| Repeated zero-order Cauchy coefficients | 105 |
| Source higher-mode failures | 3 |
| Gauge identities | 6 |
| Local normalisation | 25 |

The CNF fixtures cover empty/contradictory/tautological/repeated-literal/unused-variable/wide-clause/equality-tree cases. The reference contractor receives explicit factors, not the satisfying count, and records intermediate table sizes. Its worst-case variable-elimination cost is exponential. Exact finite tests check implementation fidelity; proofs carry the quantified claims.

[verify.py](package/verify.py), [results](package/results.json), [network fixtures](package/NETWORK_FIXTURES.json) and [object-only failures](package/TRANSFER_OBJECTS.json) are delivered unchanged. Capital checked bytes/manifest only and ran none. The state count for unrestricted SAT, polynomial conditional marginal acquisition or a different full SAT construction remains missing; no all-algorithm lower bound is earned.
