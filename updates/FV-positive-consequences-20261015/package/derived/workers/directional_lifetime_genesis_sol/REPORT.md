# Directional lifetime reduction: a certified molecular result, no established new computational power

The missing occupation interface in the supplied computation record can be closed on a fully supplied reversible network. This tranche derives and implements a mass-carrying contraction with a directional-mean certificate, including weak-trap protection and outward numerical arithmetic. It executes the complete public LJ38 source-table model for singleton minimum 1 to singleton minimum 7 at reduced temperature 0.2.

The final certificate is

    490944.5700353262923265962844767568
        <= E_1[tau_7]
        <= 491952.8208931220659617448268094499

in reduced Lennard-Jones harmonic-transition-state-theory time units. Its relative interval width is 0.0020536959146390481, or 0.2053696%. The interval is conditional on the exact archived decimal rate model and documented Python Decimal rounding. It does not enclose uncertainty in the physical harmonic model, missing pathways or the energy-landscape archive.

This is a useful resolution of the source's mathematical/numerical obstruction. The foundational mission remains NOT_ACHIEVED: the general certificate is known complementary-energy mathematics, the local specialization has no established priority, and the strongest executed classical method is faster with the same outward certificate. The candidate loses the decisive equal-guarantee comparison.

## Exact operation and the important repair

Ground the singleton target t and let A be the conductance Laplacian, a=e_s, b=(w_i)_{i!=t}. The directional MFPT is the positive bilinear Green output

    T=a^T A^{-1}b.

Contract connected clusters, aggregate every mass, and retain their intercluster conductances. Solve the two coarse RHS for a and b using one coarse factorization. Lift the trial potentials x,y, both zero at t. Form the complete original-graph residuals r_a=a-Ax and r_b=b-Ay. Route these residuals on a stored spanning tree. This is a full-input scan and tree traversal, not a reconstruction of the full kinetic solution.

For each graph cycle block B, let E_a,B and E_b,B be the squared routed-flow energies and J_B their mutual energy. The rigorously corrected center and radius are

    center = a^T y+x^T r_b
             +sum_bridge_blocks J_B+sum_cyclic_blocks J_B/2,
    radius = (1/2) sum_cyclic_blocks sqrt(E_a,B E_b,B).

The output lies between center minus/plus radius. PROOF.md proves this by the weighted gradient orthogonal projection. It also gives the local forest/deleted-edge form, a sharp unbounded-error example for an unadorned contracted graph, and a uniform interval-arithmetic argument.

The block decomposition is essential, not decorative. The first global Cauchy product mixed a tiny source residual in the main network with a huge, irrelevant mass flow on weak pendant edges. That produced a 27.3% width on a favorable synthetic example. The graph's cycle space decomposes across biconnected edge blocks; a bridge is exactly in the gradient subspace. Separating those blocks reduced the same synthetic width to 2.32e-9. The weak-heavy source leaf and target leaf return their exact distinct means, independently of the weak conductance. This is a structural repair that retains the leaf's correct occupation contribution.

The reduction is adaptive. It starts from a terminal-protected strong-edge forest and splits contracted forest edges with the largest contribution to the source/mass error budget. Its scores are heuristic; the final directed-arithmetic interval alone decides acceptance. It returns UNKNOWN if the prescribed core limit does not meet the target. There is no universal small-core guarantee.

## What was executed

All 100,000 minimum rows and 138,888 saddle rows of the acquired official archive were parsed. Removing 616 self-transition rows gives 138,272 nonself saddle rows across 12,830 components. The requested singleton endpoints are in the largest component: 71,887 states, 122,971 saddle edges including parallel saddles, and 119,853 distinct pairs. Other components are unreachable from the specified initial state and cannot affect this directional mean. No largest-component equilibrium flux is silently substituted for a whole-archive flux.

For exact decimal energy E, Hessian log-product S, and positive symmetry order o, the supplied model uses the reversible masses and saddle conductances

    w_i=exp[-beta(E_i-E_0)-(S_i-S_0)/2]/o_i,
    c_TS=exp[-beta(E_TS-E_0)-(S_TS-S_0)/2]/o_TS.

Parallel saddle contributions are retained individually by the verifier and summed by the coarse sparse matrix. The omitted common 1/(2*pi) conductance prefactor is restored in the reported time using exact alternating-series bounds for pi. Here beta=5 and the exact decimal temperature is 0.2. The common normalization shift cancels from T.

Minimum IDs 1 and 7 are explicit singleton endpoints. The independent benchmark worker cross-checked their coordinates and the primary paper's FCC/lowest-icosahedral energies. This report does not promote these two states to a basin partition or treat the archive's unannotated min.A/min.B sets as funnel labels. The whole hosted archive is not a proven exhaustive physical landscape.

The decisive experiment has the following outcomes:

| Method / selection | Retained states | Retained distinct edges | Result |
|---|---:|---:|---|
| Absolute conductance contractions | 100 / 1,000 / 5,000 | 135 / 1,360 / 6,770 | Rejected: lower bound zero |
| Source/mass residual refinement | 5,120 | 44,098 | Certified 0.2053696% directional interval |
| Full equilibrated sparse solve with the same verifier | 71,887 | 119,853 | Certified relative width 1.63e-21 |
| Classical positive star-mesh with all mass retained, separate worker | Full input, reduced exactly in real arithmetic | Fill and back-substitution paid | Faster with the same outward verifier; certified width 1.87e-26 |

The candidate's final LU factor has 1,915,958 stored entries versus 13,508,860 for the full sparse factor. That is a recorded fill comparison, not a memory-complexity breakthrough. The candidate's global-product radius would still be 172,128 raw time units, which cannot meet 1%; cycle-block localization reduces it to 80.2341. On this real input the trap repair is decisive for certification.

The full sparse verifier obtains the exact-source raw-time enclosure

    [78218.5403713443241402250249686670,
     78218.5403713443241403524472899783],

and, after the prefactor conversion,

    [491461.583610263973371235323416948,
     491461.583610263973372035941474017].

This is much narrower than requested and establishes that the requested mean was already obtainable from the same full input by an established selected-output solve plus the same classical certificate. It does not become a candidate-only capability.

## Complete costs and strongest competitor

The claim-bearing controlled run is lj38_T02_1_to_7_controlled.json. It sets VECLIB_MAXIMUM_THREADS=1, OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1. On this macOS arm64 runtime, NumPy longdouble is 64 bits and has the same epsilon as float64. Diagnostic calculations called longdouble in earlier receipts therefore had no extra mantissa precision. Prior timings are preserved as configured measurements; their earlier two thread variables alone did not establish an Accelerate thread limit.

| Paid phase | Candidate wall / CPU seconds | Full sparse + same verifier wall / CPU seconds |
|---|---:|---:|
| Complete parsing, component selection and 80-digit source-coefficient enclosures | 10.558714 / 10.488804 | 10.558714 / 10.488804 |
| Selection/refinement or full solve, residual/routing certificate, witness work | 7.879229 / 7.785378 | 10.593263 / 10.507914 |
| Total | 18.437943 / 18.274182 | 21.151977 / 20.996718 |

The candidate verifier itself takes 2.11647 seconds. The full verifier takes 2.36913 seconds. The combined process peak RSS is 581,074,944 bytes; this includes both pipelines and shared coefficient storage, so it is not attributed to either method. These are single-run implementation measurements. Imports/startup and the separately shared archive download/extraction are excluded from both timed pipelines; the acquisition receipt preserves that prior shared acquisition. No microscopic acquisition cost has been eliminated.

The separate benchmark worker's controlled classical positive star-mesh/mass-transfer pipeline, starting from the raw tables, takes 3.58294 seconds and 3.549 CPU seconds for the same singleton task. Its result is 491461.5836102763. It includes positive sparse elimination, bounded dense rank-one updates, all mass transfer and fill. It is an approximate float64 result, with no directed-rounding certificate; it must not be relabelled certified because it agrees with our interval. Pinned PyGT was also exercised by that worker, including exact classical preprocessing and a full-input timeout scope; see that worker's report. A small-core representation is already supplied by classical graph transformation.

The decisive equal-guarantee comparison was then executed by the independent benchmark worker. Standard positive graph transformation, recorded elimination/back-substitution to full trial potentials, and the same source-Decimal interval verifier finish in **15.99555 seconds end to end**, including 10.12429 seconds of interval-model construction, versus the candidate's 18.43794 seconds. CPU time is 15.919 seconds and process peak RSS 822.9 MB for that baseline. Its certified HTST interval is

    [491461.5836102639733715044256069851,
     491461.5836102639733715044347958233],

with relative width 1.869696e-26. The exact receipt is ../lj38_benchmark_sol/CERTIFIED_CLASSICAL_T0.2_1_7.json. That worker constructed its classical potentials independently and used the repaired certificate as a common postprocessor. This directly defeats a candidate-only certification or practical-speed claim on the selected task.

The two runs' coefficient-enclosure phase times differ slightly. Charging both methods the same 10.558714-second shared model phase gives 16.42997 seconds for the classical method versus 18.43794 for the candidate. Thus the ordering is not caused by the shared model-construction timing difference. These remain bounded single-run measurements, not a general benchmark claim.

The comparison establishes a modest single-run improvement over one full sparse pipeline with identical source enclosures and verifier, but a loss against the equally certified classical positive method. No generic asymptotic or expected-time improvement is proved. Selection is O(m log m), each verification/refinement scan is O(n+m), and the core factorization's fill and precision remain paid. Worst case the coarse graph is the full graph plus overhead.

## Validation, corrections and priority

One hundred independent Fraction Gaussian-elimination checks on random small rational graphs passed the outward verifier, including random contractions, parallel edges and non-tree deletions. The exact source-leaf, target-leaf and internal-bottleneck examples also pass. They test the mathematics and implementation; they do not replace the executed molecular case.

Two adversarial API failures were found after the first normal-path molecular run: ungrounded trial vectors and a forged all-bridge cache could give false point intervals. Both are preserved in API_VALIDATION_FAILURES.json and the immutable pre-repair code snapshot. The current verifier enforces grounding and coefficient/tree validity, recomputes Tarjan's real edge blocks and rejects fake caches. Both rejections and a repeated 100-case exact check pass. The full molecular calculation was rerun after repair, then rerun once under the requested controlled thread settings. No failed check was deleted or reclassified as success.

The final witness is lj38_T02_1_to_7_controlled_witness.npz. verify_saved_witness.py can recheck it from the source tables without a coarse or full solve. The witness stores trial vectors, topology and routing tree; exact decimal coefficient bands must still be reloaded from source. The default no-band API certifies only its exact supplied binary64 graph.

A final metadata audit found that a mass-band-only call used its supplied bands correctly but reported the binary64-only scope label. The label now reports supplied_coefficient_bands when either mass or conductance bands are supplied. The prior code at SHA-256 0ab3f8f9d8e642f7cf214fb0a9c0b503afc9ac561eeb8e22f85b9821cb25f1c3 is preserved in terminal_mass_certificate_pre_scope_metadata_repair.py; the two-state [2,3] mass-band counterexample and corrected label are preserved in SCOPE_METADATA_FAILURE.json and SCOPE_METADATA_CORRECTION.json. The molecular cases used both band families, so no benchmark rerun or numerical change was needed. The singleton-ground scope is also explicit: a target set must first be wired into one ground and its multigraph blocks recomputed; original bridge blocks cannot be reused after deleting multiple target rows.

The general half-product corrected-output theorem is already [Parés et al. (2021), Theorem 1, equations (10)-(12)](https://arxiv.org/html/2106.10945v1#S3.SS1), and follows the complementary-energy tradition. Existing graph transformation retains waiting times/masses, and exact Schur/Kron elimination already preserves selected outputs with the right RHS information. The particular stored-forest, cycle-block and adaptive mass-budget combination has not received an exhaustive priority search or external review. It is candidate numerical research capital, not an established foundational discovery.

The fastest classical method's matched certification gate is now passed by the incumbent, so it is no longer a missing experiment that could support this candidate. Redirect the retained mechanism to **common output verification and contraction rejection**: it can cheaply diagnose an invalid coarse lifetime and certify a chosen solver's output, but the certificate does not belong exclusively to the reduction. The remaining computational opening would require removing dominant model-acquisition/precision work, proving useful small-core guarantees on harder cyclic networks, or changing the access contract with justified bounds on unseen pathways. None is achieved here. Broader task families, physical rate and missing-landscape uncertainty, and any deadline/tail output remain unresolved. The present certificate concerns a directional mean only.

## Saved state

PROOF.md contains the exact theorem and hypotheses. terminal_mass_certificate.py is the repaired active implementation. terminal_mass_certificate_pre_api_validation.py is evidence of the rejected API version and must not be used as the active verifier. The exact/random diagnostics, rejected real-data selection, refined diagnostics, pre-repair normal-path certificate, repaired replay, final controlled result, and witnesses are all retained. The Astra worktree was read at a6190a1083f688a7e4bf64adbc5244ef150ff2c4; no repository files were changed. All writes in this subtask are under this worker directory.
