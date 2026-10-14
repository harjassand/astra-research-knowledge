# FH escape audit: acquired cycle law and source-complete certificate

**Checkpoint:** 14 October 2026  
**Scope:** independent read-only audit and replay in this directory. Original sources and `../astra-capital` were not modified. No repository edits, commits, publication, or external messages were made.

## Finding

The source demonstrates a substantial but conditional result: for a declared zero-field ferromagnetic Ising cycle with a specified heat-bath law and local reaction hazard, it derives a two-mode/global-complement relaxation bound and certifies the full equilibrium source response using an exact rational residual identity. The n=24, t=1000 interval is about `[144878.2730, 156850.6574]` (ratio `1.08263754`) with 554 trial states and a 10,178-state residual neighborhood rather than 16,777,216 states. Independent exact finite checks support the implementation identities at n=4 and n=5. The acquisition interface is synthetic exact rational Boltzmann weights; the global pairwise class and microscopic kinetic law are premises, not facts established by the finite probes. No molecular mobility or physical predictive advantage follows.

A proposed shared balanced-tree energy learner was independently audited in `query_tree_audit.py` and replayed with exact rational weights in `query_tree_exact_replay.py`. With the specified child-excluding-target rule and the full cache `{empty, V, all singletons, V\{0}}`, it recovered all edges in 101 exact n=24 relabelings, plus 25 source-like exact fixtures at `t=1000,r=1`. Across 5,000 seeded random cycle labelings, unique energy-mask calls were 183–223 (median 208, mean 207.585), versus 301 pair probes; the natural order used 173. The deterministic cache bound is 289 for n=24: at most 47 tree-node masks, 240 `A+i` masks, and the two bootstrap masks outside the tree. At n=6 it uses 28 masks versus 22 pair probes, so the finite-size benefit is not universal. More importantly, one configuration energy query maps to one classical additive induced-edge query after constant-size calibration, and primary prior work provides an asymptotically linear `O(dn)` nonadaptive baseline for maximum-degree-`d` graphs. The shared tree is a useful reduction against the source's specific pairwise-probe baseline, but it is not asymptotically strongest and does not establish a new graph-query primitive (see [PRIMARY_READ_LEDGER.md](PRIMARY_READ_LEDGER.md)).

## Acquired versus supplied

The source's word “acquisition” refers to a synthetic oracle returning exact rational `W(S)` values for selected binary configurations. Within the global pairwise, uniform-ferromagnetic-cycle model, the learner infers the coupling, uniform field, and cycle adjacency/order. For the hard-trap spectral run it then requires the recovered field parameter to equal its symmetric value.

The following remain supplied or assumed: the global absence of higher-order energy terms; the one-dimensional cycle class; heat-bath transition law and uniform attempt frequency `nu`; the local reaction form and coefficient `kappa`; the designated target coordinate; and the validity of the conversion from a physical system to the elementary binary coordinates. The finite-error estimate is an analytic perturbation bound, not an implemented physical energy-measurement protocol. `nu` and `kappa` are not inferred from energy values. The source explicitly recognizes that equilibrium energy alone leaves symmetric kinetic conductances undetermined.

An exact n=6 countermodel shows why the global class premise matters: multiplying one unqueried three-bit configuration's weight by 1000 leaves all 22 empty/singleton/pair probes unchanged. The richer balanced-tree learner also never queries that state: all 28 energy masks and its full adaptive transcript are unchanged. The corresponding reversible killed mean is about 121.54 times the baseline mean and exceeds the baseline certificate's upper endpoint by about 64.98 times. A separate same-energy clock countermodel slows the target attempt frequency to 1/1000; equilibrium closed mass remains 1/2 and the mean has a rigorous lower bound of 500, far above the uniform-clock certificate.

## Replays and controls

Fresh guarded runs used the copied source snapshot, the recorded FE-hidden-gate virtual environment (`NumPy 2.5.3`, `SciPy 1.18.1`, `SymPy 1.14.0`), and one BLAS thread. The n=24,t=1000 rerun reproduced 301 source acquisition calls, 554 trial states, a 10,178-state residual neighborhood, and ratio `1.082637541960041`; internal end-to-end runtime was 0.314 s in this environment. The separate all-closed point-preparation certificate has ratio `1.0826295552`; its equilibrium endpoints match to displayed precision. Under the source's assumed per-energy error `delta=10^-5` and independent 0.2% `nu,kappa` intervals, the n=24,t=1000 interval widens to `[144034.9374,157769.6611]`. The t=1200 interval under the same assumptions is `[207439.1314,221924.2264]`, leaving a model-to-model ratio above 1.31482. These are propagated declared uncertainties, not calibrated physical measurements. Other representative outcomes include:

- n=16,t=10: ratio `23.5971`, a clear negative control against a 10% target.
- n=32,t=1000: ratio `1.31419`, also outside 10%.
- n=16,t=100: ratio `2.20645`; expanding the two-wall trial to four walls narrows it to `1.00118`, but this is a specialized small-n result and a much larger trial.
- n=24,t=1000 all-closed preparation: independently rerun interval matches the equilibrium interval to floating display; the separate point-initial ratio is `1.08262956`.

The explicit source local-window comparator was freshly replayed: at n=24 its window-width ratios remain between about 15,756 and 185,172, far outside 10%. Full sparse references at n≤12 are extremely tight (n=12 ratio about `1.000000018`) but use all 4,096 states and do not provide a same-size comparison. See `replay/independently_replayed_comparators.json`; no optimized WE, TAMMBER, AIMMD, or strong tensor implementation was run.

All fresh exact certificates remain valid. Exact rational endpoint strings differ in several cases because SciPy's floating solve proposes dyadic trial witnesses; rounded endpoints and interval ratios agree to displayed precision. This is a proposal/runtime reproducibility difference, not a failed certificate. Detailed comparisons and timings are in [replay/source_difference_summary.json](replay/source_difference_summary.json), the guarded receipts, and [DIFFERENCES_AND_TIMINGS.md](DIFFERENCES_AND_TIMINGS.md). The long wall-cut size extension was stopped after resource growth; it produced no result and is not presented as evidence.

## Independent checks and limitations

`independent_checks.py` rebuilds the finite generator, Gibbs law, killed operator, minorant, and exact inverses without calling the source certificate implementation. At n=4,t=2 and n=5,t=10, exact LDL checks give the complementary minorant PSD, the full exact lifetime lies in the interval, the residual is exactly one outside the one-flip neighborhood, and an independently assembled full-matrix `C^{-1}` agrees with the compact formula.

The finite-energy-error statement assumes a deterministic absolute error `delta` for each dimensionless energy reading. A four-energy contrast has error at most `4 delta`; the bootstrap estimate of `log q` has error at most `2 delta`. For a child count `k <= 2`, nearest-integer decoding has error bounded by `8 delta/(2 log(t)-2 delta)`. Thus `delta < log(t_min)/10`, with `t_min>1`, is sufficient (the direct inequality only requires `< log(t_min)/9`). This bound does not test whether the real oracle belongs to the pairwise class.

The source's detailed residual and preparation arguments are read and checked at the level recorded in the ledgers; neither the full proof nor its physical premises have external verification. Strong tensor, weighted-ensemble, TAMMBER, and AIMMD implementations were not run head-to-head. Nothing here establishes an advantage over them or a physical molecular prediction.

## Provenance

The writable work area is this directory only. A read-only source snapshot contains 51 files, and all snapshot SHA-256 values match `../FH-sources/escape/` and `../FH-sources/escape_PASTED_SOURCE.txt`; receipt: `replay/source_snapshot_hash_receipt.json`. The pasted source digest is `e78dab8a4fc9a8f106d687b058ed380c2151104df735d06e59458b093bdbe602`. The read-only capital repository was at `74a1ab09ba75324bc3d2a14f05ce6196f43ffd77`; the pinned parent is `ace0cfc4437fe91c20ccd24d69e0ee4bb335e871`. No changes were made there.

Use [PROOF_AND_COUNTERMODELS.md](PROOF_AND_COUNTERMODELS.md) for proof sketches and exact countermodels, [READ_LEDGER.md](READ_LEDGER.md) for local-source reads, and [PUBLICATION_MANIFEST.json](PUBLICATION_MANIFEST.json) for the frozen, non-release artifact selection.
