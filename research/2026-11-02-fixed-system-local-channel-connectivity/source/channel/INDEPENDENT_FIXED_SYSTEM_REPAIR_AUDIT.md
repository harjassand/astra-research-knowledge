# Independent audit: fixed-system covariance/Petz repair

2026-11-01. Fresh review of FIXED_SYSTEM_MKS_REPAIR.md and COVARIANCE_REPAIR_AUDIT.md, consuming the previously audited physical-cone covariance representation and inherited actual-code inputs. Primary MKS source Sections III.1–III.3, Lemmas 1–3 and Appendix E were inspected directly.

## Verdict

**The fixed-system endpoint-channel repair is valid under its explicit covariance/actual-code premises, and removes the persistent-work-register model objection. The claimed gatewise reversibility needs the parallel-layer error correction in Section 3 below. The conservative offline exp(polylog) computational claim is defensible with the full state-source intrinsic error floor and positivity/consistency safeguards.**

This is a proof-level construction with arbitrary finite CPTP block gates on the actual bounded-dimensional data systems. Fresh disposable environments inside a gate do not introduce a persistent inter-gate work register. It is not bounded-density microscopic hardware synthesis, polynomial elementary runtime, a phase-separation invariant, or a transfer of the fixed-decoder storage lifetime to a different logical frame.

## 1. No covariance/circuit circularity

Growing local work registers are admissible as a MATHEMATICAL representation to bound physical output correlations. Disjoint deterministic backward cones, product local work inputs, and exact small-region/exterior factorization of the source code prove a dimension-free physical covariance inequality. The resulting inequality is a property of rho_H; it does not import the work resources into any later channel.

Microscopic variation cores suffice. In LPPL the expanded core has radius O(r_1), and the correlation proof expands it by another O(log^q(N/zeta)); both remain polylogarithmic. Their combined physical volume is below polynomial distance at inverse-polynomial accuracy. Selecting r_1 with a generous constant ensures the covariance cone is substantially smaller than the separation r_1/2. There is no need to certify macroscopic inner annuli or literal exponential MKS stable clustering.

Uniformity over partial coefficient hybrids is indispensable. A strict finite-incidence interaction box within the accepted low-activity/gap/potential margins supplies this, whereas a theorem only on homogeneous couplings would not. The proposed convex-box restriction addresses it. Known finite-dimensional geometry and bounded density suffice for the physical LR/cover estimates; an embedding into regular cells may be used analytically, with unused product sites factored out of the recovery gates.

## 2. Actual-data Petz gates and endpoint circuit

LPPL bounds the exterior marginal difference for one bounded microscopic coefficient change. The local Gibbs Markov bound then recovers the erased core and first buffer from the second buffer. At fixed temperature, choosing r_2=O(r_1^3+log(NG/epsilon)) controls its volume-dependent exponential. The square root in the recovery error only changes the constants/logarithmic precision allocation.

R_new composed with partial trace is one CPTP map on the actual data block. Its Stinespring workspace is disposable inside that gate. Such a map is permitted in the standard arbitrary-block channel model; no Poisson timestamp or copied syndrome persists between gates. Endpoint error telescopes by channel contractivity.

The term ordering can be chosen color-by-color, with disjoint blocks inside a color. Maps in one color commute exactly even when their mathematical definitions use sequential hybrid Gibbs states. This validates endpoint parallelization and its polylogarithmic depth-times-diameter. It does NOT alone validate the stated gatewise-reversibility bound on the common pre-layer state.

## 3. Required correction: sequential reversibility versus parallel layers

The original Section 4 estimate establishes reversal on the sequential actual prefix immediately before a gate. MKS gatewise local reversibility is instead evaluated on the state BEFORE THE ENTIRE LAYER. Earlier same-color CPTP maps can discard information. Their disjointness does not allow pulling a trace-norm estimate backwards for free. Citing the displayed step in MKS Appendix E does not supply the missing estimate for these sequentially specified marginals.

There is a simple conservative repair, costing only a polynomial accuracy factor. Let rho_j be ideal hybrid states; let E_j and R_j be forward and reverse gates with respective ideal-state error at most delta; let sigma_j=E_j...E_1(rho_0). Contractivity gives ||sigma_j-rho_j||_1<=j delta. Thus

    e_j := ||R_j E_j(sigma_(j-1))-sigma_(j-1)||_1 <= 2j delta.

For a gate m in a color beginning after gate b, let P=E_(m-1)...E_(b+1), and Q be the corresponding reversed sequence of R gates. Reverse telescoping gives

    ||Q P(sigma_b)-sigma_b||_1 <= sum_(j=b+1)^(m-1) e_j.

E_m and R_m commute with P and Q because their supports are disjoint. Therefore

    ||R_m E_m(sigma_b)-sigma_b||_1
       <= 2 sum_(j=b+1)^(m-1) e_j + e_m
       <= 4 G^2 delta.

Choose computational/local-recovery tolerances delta_comp<=epsilon/(8G^2), not merely epsilon/G if the final LR budget is epsilon. A fixed intrinsic local error C eta_n then produces a floor O(G^2 eta_n). Both G=O(N) and G=O(N log(N/epsilon)) are polynomial, so this floor remains negligible asymptotically and all radii remain polylogarithmic. Endpoint error is no worse than G delta. Constants can be adjusted generously. The originally asserted universal 2E_total bound needs either this redefinition of the error budget or a sharper independent proof.

## 4. Commuting cooling and the zero-temperature endpoint

The commuting segment is well designed: all dimensionless check coefficients remain above a fixed low-temperature threshold, even for heterogeneous hybrids. Increasing them lowers each trace activity, giving uniform proposal/contraction/tail domination by the threshold model. There is no need to extend the noncommuting smallness condition beta v exp(C beta J) to logarithmic beta at fixed v; doing so would be invalid.

The DOS bound is valid without independent checks: all valid sectors have equal dimension, and the number of valid weight-k syndromes is at most binom(M,k). Hence excited relative partition weight is at most (1+exp(-beta J_min))^M-1. Logarithmic beta makes the finite-temperature state close to P_0/2. Commuting shielded Gibbs states have exact annular Markov recovery, so the second buffer need only exceed interaction range. Even a conservative LR velocity proportional to the largest coefficient remains polylogarithmic here.

Heating from P_0/2 instead of the finite-beta endpoint changes all subsequent state errors by contractivity, and local-reversibility errors by at most twice the initial trace error. This proves a memory-only ground connection, not an unqualified unique-ground-state assertion for arbitrary degenerate baths. The finite-beta qubit-bath endpoint statement remains separate.

## 5. Offline marginal computation is chargeable, with qualifications

For X a gate block, separate H into H_out and H_touch, K=||H_touch||=O(|X|). Applying scalar Jensen in vectors |psi_X> tensor |E_out> gives the stated numerator lower bound exp(-beta K)Z_out. Eigenvalue/partition comparison bounds Z_H by dim(X)exp(beta K)Z_out. Thus

    lambda_min(rho_X) >= exp(-2 beta K)/dim(X).

This is valid for noncommuting H and uses no false operator monotonicity of exp. At polylog block volume and beta<=O(log N), the condition number is exp(polylog), not exponential in the full system volume.

Full state tomography of the larger block to exp(-polylog) accuracy costs exp(polylog) samples and processing. Each sample must itself have systematic trace error smaller than the tomography tolerance. The accepted ideal encoder at maximally mixed logical input approximates actual Gibbs only up to its FULL intrinsic floor, which includes any logical-twirl/ensemble comparison error, not just eta_n. Those errors are stretched exponential in n and therefore below exp(-polylog N) asymptotically. Retain this condition explicitly; do not assert arbitrary precision at fixed n. Known stabilizer encoding supplies repeated code-state resources for offline tomography, charged in its gate count.

Project the estimated larger density matrix into trace-one PSD matrices with eigenvalue at least a conservative fraction of the proved lower bound, and use its EXACT partial trace as the smaller reference. This guarantees consistency. For such a full-rank pair, each rotated Petz map is exactly CP and TP: trace preservation follows by moving the larger powers through the trace and using Tr_A rho_AB=rho_B. A finite convex combination with nonnegative weights summing to one remains CPTP. Quadrature tails, matrix powers, inverse conditioning, and Stinespring approximation can all be allocated exp(-polylog) precision; finite-dimensional continuity bounds cost polynomial factors in dimension, inverse minimum eigenvalue and integration cutoff, hence exp(polylog) total overhead. Tomography failures can be union-bounded over G gates.

This is a randomized OFFLINE compiler, succeeding with declared high probability, after which gate descriptions are fixed. It does not supply globally shared runtime randomness or a free Gibbs-marginal oracle. Generic exp(log^a N) cost should be written exp(polylog N); calling it a small practical quasipolynomial budget would obscure potentially enormous fixed a.

## 6. Source and final scope

The source [Ma–Khemani–Sang, 2509.15204v3](https://arxiv.org/html/2509.15204v3) supplies local-perturbation, local-Markov and recovery lemmas, plus the distinction between endpoint conversion and gatewise reversibility. Here those lemmas are consumed on microscopic cores with restricted covariance, rather than invoking its all-annulus stable-clustering theorem verbatim. The extra parallel-layer argument above is supplied independently.

After the LR budget correction, this is a defensible standard actual-system block-channel connection to the memory code projector with specified-state local reversibility. It does not identify the transported logical frame with the fixed original decoder, prove the earlier exact-H lifetime for that frame, establish nontriviality against product phases, or yield native noisy release. Those restrictions are appropriate, not cosmetic.

## Reviewed snapshot hashes

- `FIXED_SYSTEM_MKS_REPAIR.md`: `b1c4020523f3f9047caa7c49a87db2e4046cc537a43f4d312b62c33d68ead195`.

- `COVARIANCE_REPAIR_AUDIT.md`: `2fbf49a0e320e63fb9defcff8bd951765ef87894fdf2cd0d28cd129989043434`.

- `INDEPENDENT_WHOLE_PHASE_AUDIT.md`: `564aa0c458c4050de9466d7ec85065d8e0f9a21caec1d7bf5f450098c74a9e2b`.

## Final frozen-version diff binding — 23:16 UTC

I read the complete diff against `history/FIXED_SYSTEM_MKS_REPAIR_b1c4020523f3.md` and checked the current file hash:

- Corrected `FIXED_SYSTEM_MKS_REPAIR.md`: `8ca281ca9a99a531910d6e7ea6cf7eba2c2276b6787ede264a83cb1c94f70627`.
- Historical pre-correction snapshot: `b1c4020523f3f9047caa7c49a87db2e4046cc537a43f4d312b62c33d68ead195`.

The corrected text implements the independent common-layer reversibility lemma, uses delta_comp=epsilon/(8G^2), and clearly defines G as the number of local recovery BLOCK gates rather than elementary synthesis gates. It retains endpoint O(epsilon+G eta_n), common-layer reversibility O(epsilon+G^2 eta_n), and separate cold-ground/numerical errors. It also retains the full offline state-source floor, including beta N eta_n, square-root logical-twirl comparison, and logical-twirl distance, with the requisite fixed-n precision restriction. These edits close the substantive issues identified in this audit.

**Final verdict for the corrected hash: accepted as a standard actual-data arbitrary-block-channel connectivity construction, with specified-state approximate gatewise local reversibility and the explicit inherited hypotheses/error floors.** The earlier work-register circuit remains only a correlation proof device. No native hardware runtime, fixed logical-frame identification/lifetime transfer, product-phase separation, practical constants, or independent peer review is implied.

I also read and reran `root_petz_and_layer_checks.py`, suppressing only its JSON overwrite. It returned trace-preservation residual 7.13e-16 for consistent rotated Petz maps, positive Choi minimum eigenvalue 1.30e-6, TP failure 0.0319 for an inconsistent marginal, and reduced-state minimum eigenvalue 0.00259 above the proved bound 0.000379. Its two-bit example returned zero sequential-prefix error but common-layer error one, illustrating why the replaced inference was invalid. These are finite channel-plumbing checks, NOT tests of the actual recursive-family phase theorem, all-level geometry, or asymptotic resource claims.

Fixture source SHA256: `5aef2d1c4e788558782756e9e0cede9e449a960bbb20561335d7aaeed03c4032`.
