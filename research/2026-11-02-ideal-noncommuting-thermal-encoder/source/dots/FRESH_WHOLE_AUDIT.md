# Fresh whole-interface audit: filtered thermal encoder

2026-11-01. Independent skeptical pass over the actual candidate and its governing component arguments, not an inference from their PASS labels. **Verdict: the narrowly quantified IDEAL finite-accessible-bath construction survives this pass. The final reviewed main-join appendices incorporate the essential precision/domain corrections identified below. No fatal circularity or exponential oracle was found.** This is a mathematical audit, not peer review, an implemented full encoder, or a new proof of every inherited source construction.

## 1. Exact conclusion that the arguments support

Fix the actual random-embedding RX/RZ family, its matched protected decoder, fixed microscopic/construction constants and a compact low-temperature beta interval. Require a known efficiently computable bounded-body, bounded-incidence physical Hamiltonian, sufficiently small local V, a supplied encoded input, and all N=n+N_B qubits accessible with ideal controls/reset. For a fixed polynomial bath bound, sufficiently large n, and an algorithmic error parameter delta obeying

    L = C log(N/delta) < L0 = floor((d_n-1)/b0),

there is a preparation algorithm with classical and elementary quantum cost polynomial in N/delta. Its reference-safe preparation error relative to the EXACT actual-H thermal overwrite is bounded by

    C delta + C(1+beta N) eta_n + C sqrt(delta_tw),
    eta_n = C n q_*^L0.

Here delta_tw is the actual-Gibbs versus logical-twirl bound from the storage construction. Different fixed constants may occur. The quoted polynomial is NOT polynomial in log(1/delta). Its constants and degrees need not be remotely practical.

This yields inverse-polynomial target error asymptotically, and a limited smaller-error range; it is NOT an arbitrary-precision sampler/encoder for a fixed n. Increasing the scalar-cluster cutoff past distance is not justified. The ensemble/transport remainders remain even if simulation error is driven to zero. The original main join did not state this important restriction although its Gram component does.

After preparation, exact-H storage contributes its original storage error additively. Contractivity of the common subsequent channel bounds propagation of preparation error without multiplying it by hold time.

## 2. Gap dependency is noncircular, with an explicit bath completion

The kernel calculation establishes only rank two: invertibility gives ker F_a(s)=exp(-sH/2)ran B_a. It does NOT itself establish a gap. A separate chain supplies the gap:

1. Actual two-sheet/cohomology contractions give anchored logarithmic filling in the ancestry host. Internal-to-descendant-leaf matching has load at most two, by the excess of leaves over internal nodes in every subtree. Projected paths cannot lengthen. No physical qubits or Hamiltonian checks are invented.
2. Paired completion gives BOTH connectivity implications between real check sets and real qubit supports. It is not enough merely to enlarge two unrelated metrics. The stronger all-support filling statement applies to the extra connected sets introduced by the shortcuts.
3. The De Roeck et al proof is extended, not literally applied with its graph definitions silently changed. I inspected the primary PDF and the saved proof text at Sections 2, 3, 5.1, 8, and Appendix B. Word algebra remains actual incidence algebra; ghost and relative-boundedness estimates consume anchored filling and ball growth. Both norm conversions consume the paired connectivity facts. The receipt's more conservative reverse norm conversion correctly avoids the suppressed support-weight factor in the displayed Appendix B constant.
4. Root-connected imaginary-time expansion gives a small exponentially connected-SIZE-weighted interaction for F_a(s)-F_a(0), uniformly in a and s. To meet the source Pauli norm, a k-label operator must pay its Pauli expansion factor at most 4^{c(k+1)} and its cover factor exp(mu c(k+1)). These are fixed exponentials, so choose q sufficiently small AFTER fixing the new graph/TQO constants and the required mu. Small bare local V alone without this choice is not an adequate norm check.
5. Stability gives an isolated low band of multiplicity two. Positivity and the independently exact two-dimensional zero kernel identify this whole band with the zero eigenspace. Thus the uniform gap is genuinely earned, not assumed from numerical continuity.

For the finite bath, explicitly add the actual onsite bath projectors to the reference parent. In a known onsite eigenbasis they are signed single-qubit Z checks, including when the physical onsite energy is degenerate. The physical H_B need not be gapped; the engineered parent projectors are. Lift physical memory/bath neighbor edges to incident-check pairs before paired completion. This preserves bounded degree. Product bath stabilizers do not reduce logical distance. A stabilizer supported in supp(S) splits into a memory stabilizer filled by the all-support theorem and bath Z factors filled onsite. Hence TQO-II holds for the combined graph. Check the source distance condition against log N, not log n; the fixed polynomial bath bound makes this follow asymptotically. This completion is elementary but should not be left implicit in the final theorem.

Valid syndrome parents are Pauli-conjugate to the unsigned one; onsite basis changes handle bath labels. Support and norm constants are unaffected even when the representative is extensive. No exponentially many syndrome-by-syndrome gap checks are needed.

## 3. No uncharged exponential compilation identified

The parent linked coefficient MUST enumerate sets C for which C union {Q_j} is connected, not require C itself connected. Two perturbation branches can meet different parts of Q_j. The independent consumer correction is substantive and governs any implementation.

For each retained set, only the root, its perturbation supports and incident reference stars enter the exact restricted conjugation. The omitted commuting reference terms cancel. This is O(k) qubits, not the volume of a radius-k collar. Subset Mobius inversion sums all repetitions/orderings. Its 2^k work and dense 2^{O(k)} local matrices remain polynomial at k=O(log(N/epsilon)). Pairwise products for L_j dagger L_j keep O(k) support and polynomially many terms. Numerical conditioning is exp(O(beta k)), not exp(O(beta N)). Rooted re-anchoring can cost additional fixed exponentials; absorb them before choosing q.

The analogous scalar-potential calculation uses local restricted traces, Pauli decomposition, and binary stabilizer row reduction. It does not tabulate 2^{|D_U|} envelope assignments. Polynomial physical filling is used for dependence/moment bounds, while row reduction computes characters. The matched decoder representative is reconstructed polynomially as specified in the inherited sampler; an arbitrary representative with an uncontrolled logical gauge is not an acceptable substitute.

The trace-gas birth/death chain plus bath heat baths has the stated sufficient contraction condition theta_h+(4B+1)epsilon_Phi<1. In particular bath bits need not be dilute. Truncation, potential evaluation, finite clock cap, transition precision and quantum simulation require separate allocations within delta. Conservative constants must be instantiated from graph/filling/activity bounds; calling an unspecified O(beta,V) a numerical input would not be an implemented algorithm. This is constants/implementation work, not evidence for a hidden exponential marginal oracle.

## 4. Gram and reference-safe logical interface

The component expansion cannot replace V by its syndrome diagonal. Instead its generous graph ensures disconnected components cannot cancel syndrome transitions. Components below distance compress to scalar logical operators; bath-only components are scalar even when large. Exceptional memory-touching components are bounded in operator norm before any logical trace, with memory anchoring. This supplies the necessary uniform two-dimensional relative Gram bound, rather than just diagonal weights or an average good-sector statement.

The transport issue is resolved without a derivative bound on the relative Gram error. In an instantaneous eigenbasis of G, the canonical connection has off-diagonal elements

    K_ij = G'_ij (sqrt(lambda_j)-sqrt(lambda_i)) /
           [2 sqrt(lambda_i)sqrt(lambda_j)(sqrt(lambda_i)+sqrt(lambda_j))].

Also G'=-A dagger H A. Therefore ||K||<=C eta_n ||H|| and the integrated isometry error is O(beta N eta_n). The logical unitary obeys a unitary differential equation, so there is no exponential Gronwall penalty. This uses FIXED H and a beta-only path, not arbitrary Hamiltonian holonomy. Exact scalar Gram gives zero connection. The main join's language about a derivative estimate still needing to be earned is obsolete.

The ensemble weights are Tr G_a/Z, with no extra half. Matched frames give sum_a B_a rho B_a dagger = rho_L tensor I. Removing Gram normalizers costs O(eta_n); the remaining sandwich map is compared to overwrite using Hilbert-Schmidt square-root continuity. The supplied operator-from-gauge construction bounds arbitrary reference inputs without a hidden factor of gauge/bath Hilbert dimension. The sandwich map need not be exactly trace preserving for this comparison. Sampling TV error costs twice that error in channel norm.

## 5. Actual fixtures and their evidentiary limit

I read and reran actual_host_quotient_test.py with only its final JSON overwrite suppressed. Actual seed/RX3/RZ3 sizes were n=5,60,1336; host size 2895, maximum degree 85; children 2 through 66; quotient load 2; real check degree 58. Every connectivity/nonexpansion assertion passed. My completed qubit degree was 268 rather than the receipt's 273; this does not violate either bound or any structural assertion. The exact finite graph statistics can depend on construction/selection ordering and should not be treated as canonical invariants without deterministic normalization.

These are genuine actual-incidence checks, not evidence for fabricated level-two Euclidean positions. They do not prove all-level filling. The separate root_filtered_parent_test.py explicitly uses the unrelated standard [[5,1,3]] code; I inspected it and did NOT count its numerical gap as evidence for the actual family. The all-level argument remains the actual contraction/host proof, and the source geometric embedding hypotheses remain required even though the algebraic two-sheet fixture works at ell=3.

## 6. Scope, novelty, and remaining obligations

The prior-capability gate appropriately credits existing filtered parents, weighted filtered ensembles and connected-set compilation. I do not independently certify historical priority from this whole audit. The plausible added result is the actual-code binding plus a coherent unknown-logical-input channel, not a generally new thermal-preparation architecture.

Required qualifications are explicit accuracy floor and cutoff; root-connected sets; total N in resource/transport bounds; product-bath graph completion; smallness in the converted intensive norm; finite-size/source-distance qualification. The final reviewed main-join appendices now supply the first four and the log N distance requirement. The norm-conversion smallness is supplied by the component proof together with Section 2 above. Stale conditional component-status and derivative-estimate wording can be updated, but that is not itself proof.

No remaining fatal mathematical join was found under those qualifications and the inherited actual decoder-trace/geometry inputs. This pass has not newly re-derived every lemma of the source code/trace-gas construction, and should not be portrayed as such. Full software implementation, conservative constants, practical resource estimates, and publication-level independent checking remain distinct work. Generic noisy release, inaccessible reservoirs and passive preparation remain outside the claim; supplied encoded input and accessible controlled bath are explicit resources, not grounds to reject the stated ideal capability.

No external contact/publication occurred. The stopped Nature and two stopped arXiv HTML sources were not accessed or retrieved through alternatives. Only the permitted 2411.02384v3 PDF was reopened, in addition to supplied local artifacts.

## Snapshot SHA256 manifest

The following hashes identify the reviewed files; later candidate edits require a diff review rather than silently inheriting this verdict.

- `producer-workspace/ROOT_FILTERED_THERMAL_ENCODER_JOIN.md`: `aba16bd65f05a6450de639d9f3b6a9dca0fd6d4f18735a5f45d2c0f1957e7a01`.

- `producer-workspace/GRAM_SAMPLER_ENSEMBLE_BRIDGE.md`: `925068e35494672683cda159d42a05d935bbd18049afac1cc7f1a82d94c0b595`.

- `producer-workspace/INDEPENDENT_GRAM_SAMPLER_ENSEMBLE_AUDIT.md`: `c4ac496e20e88a526df1970533aba8532bdd9189f339a7f5480f8191991e8a7a`.

- `producer-workspace/PRIMARY_PRIOR_CAPABILITY_GATE.md`: `aa25ea2f9794a10b801bab640be77b2db713c3d22ab291805cfab538c0bd6afc`.

- `producer-workspace/root_filtered_parent_test.py`: `66e7551eaa9e1649475d6b4daa94ef5be586558c0f75a368476b75dd1143d0ff`.

- `producer-workspace/filtered_parent_consumer.md`: `1d3b1ac59e14881f9d2051d3588afa3ec3f514f70cc79936582042f8cfaf65a4`.

- `producer-workspace/FILTERED_PARENT_CONSUMER_AUDIT.md`: `8ff59d5d73f3bff95400b4d93d2f11ee087b5c8f3155366f15534a00b90b139c`.

- `producer-workspace/SUPERGRAPH_PROOF_GATE_RECEIPT.md`: `892a20db7de66f8f04349f24ed03204e392a25d07cab2b942a1ad72c9dac0444`.

- `producer-workspace/ACTUAL_HOST_BINDING_RECEIPT.md`: `01fdda928fb366786e2a694091dfc50c584f2b02fa4cfaee5a96fb2066da02fd`.

- `producer-workspace/2411.02384v3.pdf`: `c9c9dbd97bfab8a05f7825035a63e1d4b124bed969067693af486b31eee5a218`.

- `producer-workspace/source.txt`: `a454335ad02cebe47f90db11f04a4cee733aa0b2177d73783f1fab590479d03f`.

- `producer-workspace/actual_hierarchical_host_filling_v2.md`: `3ac1009ce21d0c9d7c4eba1266d46821858c8e10f5a0e036b2f8cb062e50af14`.

- `producer-workspace/actual_host_quotient_test.py`: `6defdf5c4889bd488353fb8a588845b4b6dc7a37d4d60a38590393d4bada728c`.

- `producer-workspace/actual_host_quotient_results.json`: `3c7dcfbb69e3936c2ce6fc76c662318eff4275324307a614f2b689a6617064a0`.

- `producer-workspace/two_sheet_contraction_addendum.md`: `7a18df5e5c6eeaaee63aff2455256ad3b7048fb75ded030dbac2093c36593f29`.

- `producer-workspace/polynomial_filling_theorem_candidate.md`: `e653d035699ed69febcb61eacdf23efba93e912b4187e4ce00c175e9863fc186`.

- `producer-workspace/EXACT_SPIN_ENVIRONMENT_PHASE_THEOREM.md`: `cf76fc3fa3ee42a28446340f7df85c0d683dbe0877f9a5caf4f81b2368212e38`.

- `producer-workspace/polymer_bridge.md`: `87a8035d1fb353c95ee887b1bfef34dcf87211a6858d48735995dd0c63ed4456`.

- `producer-workspace/ROOT_RECURSIVE_THERMAL_SAMPLER_JOIN.md`: `a28c7243fd3136019e4df64e7ffaa7da1912573e43e6587412c3c157fc7e3879`.

## Final candidate diff review

At 21:55 UTC I reread the complete candidate including its new Accuracy and compilation, Finite-bath gap completion, Explicit final accuracy, and Strongest inspected predecessors sections. The current candidate hash is `aba16bd65f05a6450de639d9f3b6a9dca0fd6d4f18735a5f45d2c0f1957e7a01`. These additions correctly close the material statement omissions identified in this pass. The final C[epsilon+beta N eta_n+sqrt(delta_tw,n)] formula agrees with Section 1 above because beta has a fixed positive lower bound and N>=1. The remaining older conditional status/derivative wording is conservative/stale, not an unclosed mathematical gate. This verdict binds to this current version and the listed component snapshots.
