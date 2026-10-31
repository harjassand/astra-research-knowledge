# Independent imperfect-observation/replay and sparse-frontier review

31 October 2026. Reviewer: challenge_graph_profile_compiler. **Scoped mathematical and research-prototype PASS**, under the explicit stochastic-model, observation-coverage and fresh-validation protocol premises. This is separate from the previously frozen exact-input review. No data-provenance certification, new general learning theorem, or superiority over equally informed ordinary retained methods is inferred.

## 1. Full-read source binding

All following sources were read in full and their hashes checked:

| Source | SHA-256 |
|---|---|
| PROOF.md | ff0dfab8dd3e246572844c5265e462ccd7321d069245b03f7a8cd940ff459e18 |
| TASK_WEIGHTED_ACQUISITION.md | 1f9217976746016ae994bce6e1ef0ced35093b11a7787db956de4de3eeef7926 |
| robust_replay.py | 78ecc56dded4dac4df6e5dc60cd298893226a2a28d5e098fc09b5271ba35b2c8 |
| check_replay.py | b7b2c9c0d83eb66b57750989da0ddfce4746e04c6760445934b2336ebfadb1bb |
| risk_frontier.py | 4a3591831b0e660116ce6b1e5d67efdcb9381fafc4a3321f69e7d069092bed32 |
| composition_check.py | 4d9956706f6fc8ab47ee8409303af254ce03aedac2cb23984f277385cc224f1a |

## 2. Mixed-norm theorem: no fictitious common equilibrium

The acquired positive probability vector h need not be invariant. True stochastic matrices contract the infinity norm, so every full trajectory has H norm at most M=||b||_infinity. H-orthogonal projections therefore give ||p_j||_H,||q_j||_H<=M even when the full matrices are expansive in H. The starting vector lies in P and q_0=0.

The exact complementary recurrence gives ||q_(j+1)||<=alpha||q_j||+e_in M; the independent full-trajectory bound permits the cap t_(j+1)=min(1,alpha t_j+e_in). Comparing the P component to the separately G-contractive stored replay gives one previous error plus dM+e_out M t_j. Pairing with H^-1 ell in P removes q_j. The stated C M[l d+e_out sum t_j] follows without an exponential perturbation factor. It remains valid when alpha>1, although then its capped bound may be too weak for admission.

The exact center/stabilization discrepancy is load-bearing: B is not silently treated as PAP. Rounding coefficients and scaling a proposed block by a certified upper norm do make a contraction, but their bias is charged in d. The rank may be full, and an arbitrary poor geometry need not admit any useful accuracy. INCONCLUSIVE remains a sound possible outcome.

The weighted Frobenius uncertainty formula follows by conjugating by H^(1/2). Orthogonal projection does not enlarge its induced norm. The nonstationary complement certificate is also correct: A=m*1*h^T+(1-m)R, Jensen bounds ||R||_H squared by (kappa-m)/(1-m), and Q kills both the constant range and h^T. Hence ||QAQ||_H squared <=(1-m)(kappa-m). At m=1, every consistent row is h^T, so the complement vanishes.

The default executable uses the stronger modular route: stochastic centers C are exactly feasible within each box, and infinity-norm telescoping bounds observation error by ||ell||_1 M l eta_inf. The mixed-norm theorem is then applied to these known centers, not falsely to exact hidden matrices. Both terms are paid. Uniform coverage of the entire supplied observation set permits fitting geometry on those same data and later choosing arbitrarily many realized words of length <=L. It does not compare different feedback policies that choose different words after different answers.

## 3. Bounded-bit replay and actual checking

The rounding grid has per-coordinate error <=2^(-p-1); diagonal G gives the stated per-step norm bound. Contraction accumulates initialization plus l step errors linearly. Output pairing has dual norm C, and the final scalar rounding is separately included.

I flagged the earlier complexity wording for arbitrary per-entry rational denominators. The frozen proof now explicitly pays common-denominator acquisition and its bit growth. The implemented backend converts each actual operator and output row to integer numerators over a common positive denominator. For grid integer state z, the exact sum is rounded by floor((2 sum+D)/(2D)), correctly implementing nearest rounding with ties toward +infinity, including negative values. Output is then divided by the fixed grid scale. Stored online state denominators no longer grow with word length; accumulator and acquired coefficient sizes still count. Arbitrary supplied denominators may enlarge their common lcm, and that enlargement is not hidden in the bit budget.

The exact PSD elimination handles zero pivots by requiring their remaining row entries to vanish. Norm upper bounds are finally checked by exact PSD inequalities. Float spectral directions in the comparison are only proposals; their rounded rational bases and replay blocks face the same exact certificate. The verifier recomputes the task/constant span, positive orthogonal Gram, block contraction, observation, compression and execution bounds from external boxes/b/ell. It requires external expected horizon and tolerance, so a self-declared easier task cannot substitute for the request.

Verification does not establish that supplied boxes contain physical truth, that sampling was authentic, or that a timing ledger is accurate. It is a mathematical certificate for the supplied finite data. Research code and imported exact routines are not a claim of hardened untrusted-service security or complete bit-operation instrumentation.

## 4. Sparse task-weighted observation theorem

The Bellman envelope uses C on the left of the error recurrence and true shorter-word values bounded by the centered task range. Thus no unknown true occupancy is supplied. The cap at 2 is valid because both true and center values lie in the same bounded range. Maximization over state-dependent actions is a conservative overapproximation of all open-loop words, not an optimal-word oracle. Signed ell is handled by |ell|; for the executable probability-initialization fixture and task range width <=1 the numerical bound is risk/2. An arbitrary larger task oscillation must multiply it; the code does not infer a task bound from an unseen function.

Unobserved rows may be assigned an identity center and radius 2. Their actual transitions are not assumed absent. Potential unseen mass is paid through the predecessor's radius. The final finite center graph must be closed under its stored transitions; the composition constructs exactly that graph from the saved samples, not a hidden true graph.

For fresh validation, the trained support plus one outside bin has a simultaneous Hoeffding event. Moving empirical outside mass to an anchor costs the stated (|S|+1)zeta+2 qhat bound; clipping at 2 is always safe. The base-two logarithm upper bound is conservative because ln(2)<1. The telescoping call allocation sums to delta over all adaptively selected calls.

Statistical validity requires the support and validation sample count to be fixed nonanticipatingly before that validation batch, with genuinely fresh conditionally iid outcomes. The frozen acquisition follows that rule. The record verifier checks the resulting algebra and sample-size inequalities, not temporal provenance or independence. Authentic outcomes from an iid stream with outcome-dependent stopping do not by themselves satisfy this batch argument. With support and N fixed, choosing a larger zeta afterward is harmless because the checked inequality enforces the predetermined minimum valid radius; no unnecessary restriction on that enlargement is imposed here.

On the simultaneous event the same uncertainty certificate covers all later requested words; failure probability is an acquisition-event statement, not a posterior guarantee for each selected rare transcript. Aggregated multinomial simulation in the executable is not measured physical acquisition time, and all implied individual draws are charged.

The routing-tree lower bound is correctly scoped to algorithms required to achieve accurate successful admission on every model with probability >=1-delta. Under the null, distinguishing each single-leaf alternative forces its standard expected log-likelihood cost; summing yields the stated K/epsilon dependence at small epsilon. An algorithm allowed to always return INCONCLUSIVE is not constrained in this way. This is an information/coverage lower bound, not computational hardness or a lower bound on lazy learning for only queried leaves.

## 5. Independent execution and actual comparison

I reran all three frozen harnesses in a separate `/tmp` working directory, leaving author JSONs unchanged:

- 501 replay/geometry/uncertainty/rounding checks passed.
- 4,124 sparse-frontier checks passed, including all 4,096 length-12 binary words in the synthetic fixture.
- 35 composition checks passed.
- 415 additional exact checks passed for random stochastic families with arbitrary positive nonstationary H, signed b and ell, zero b/ell, short exhaustive words, integer/rational replay equality, task/alias tampering, negative rounding ties and singular PSD cases.

The repeated frontier run acquired seven center labels from initial label 17, using 84 updates and 15,778,976 charged synthetic iid draws. Its observation bound is 3/32. Composition remains FULL rank seven, with common-denominator coefficient bit budget 41. The complete bound is
232302605715645145063693881 / 2475880078570760549798248448 < 1/10.
This demonstrates an end-to-end finite-data interface, not a further rank-reduction win over ordinary sparse center replay.

For the separate 12-state fixture, ordinary retained full-space, bidirectional Krylov, randomized joint range and pooled-normal spectral proposals all receive the same observed boxes, bound and precision tuning. In my run their retained ranks were 12, 4, 5 and 6. All cached 1,032 prefixes. Full-space retained-state payload was 51,619 bytes, versus 13,644, 16,012 and 18,250 bytes for the reduced representations, respectively. Online arithmetic benefited in this small fixture; acquisition, certificate storage, model discovery and the observation oracle remain separately paid. Timings are illustrative and not a universal amortization or practical-win theorem. Full-entry observation cost can dominate these savings.

## 6. Prior and verdict

Primary abstracts directly inspected: Pulch, stability-preserving Galerkin reduction, https://arxiv.org/abs/1711.02912 ; Jin et al., reward-free exploration and significant-state coverage, https://arxiv.org/abs/2002.02794 . These establish strong ordinary antecedents; this review does not claim theorem-by-theorem novelty comparison from abstracts. Stable reduction, simulation-error telescoping, confidence sets and Bellman coverage are ordinary machinery available to equally informed retained competitors.

PASS for the supplied mixed-norm uncertainty theorem, finite integer replay, conditional fresh-batch sparse confidence and their demonstrated composition. No exact hidden-law recovery, posterior data validation, optimal sample complexity, general planning oracle, or historical novelty follows.

## Artifact hashes

`replay_checks.json`: `4194669ba2d927e90f6dd1cafa25e0735f95594d67633393edcabf28a3d6af88`

`replay_certificate.json`: `ccb7e055ee3d22a7c048702dcf6c81ea6b5460de5c434bb12e31c21835e02d03`

`observation_fixture.json`: `e29ef860796972763a099df26636f52ad36440c469ef8040f417a318b27e5801`

`risk_frontier_results.json`: `662ff2af140e7a839f8bde3ac61ef4e153218fdb4c468921fe637081f23b096d`

`composition_results.json`: `be81c85d3e6e94eefdb1955a2a2771bc57a00b838b06bbea82844efb64ba777b`

`composed_replay_certificate.json`: `18ea348b5a8d436277d0b7736bf7679e4db6e6c1d0d69a54d534776a4c487cfa`

`independent_checks.py`: `43edf28f232d529f90935363ba6f8bedabb14b2ced77054374c896021c74adf9`

`independent_checks.json`: `dea63e1b13de6c7f377250311f4cfaff1faca3c4acbac016c9b34ad35cb87c13`

