# U kinetic binary port: passive equivalence, active work and atomic return — corrected documentation, 24 October 2026

This corrected copy resolves two documentary/source-scope statements in the original [README](README.md). The original source payloads and initial checkpoint remain preserved; no scientific replay or physical validation was performed.

This selected kinetic unit preserves a finite three-state model, its binary passive-path comparator, a saved profile-based work certificate and a separate conditional atomic-return test. It adds a concrete example alongside the existing N713 passive/active and kinetic-access capital; it does not establish that broader distinction as new or update N713's scientific status. The source packet and versions are preserved in [SOURCE_RECEIPT.json](source/SOURCE_RECEIPT.json) and inventoried in [source_manifest.json](source_manifest.json). No scientific code or proof replay was run by this intake.

## Port convention and interventions

The model uses probability columns, `p'=Qp`, `kBT=1`, interaction energy `-h f`, and work **on** the system

`W_on = -integral h'(t) f(X_t) dt`.

For the triangle, `f=(1,0,0)` and the source supplies a positive-rate finite generator `Q0` and stationary vector. Its calibrated geometric action is

`q_ij(h)=q0_ij exp[h(f_i-f_j)/2]` for target `i`, source `j`, with repaired column diagonals.

This keeps the symmetric prefactors on each edge fixed, while allowing their baseline values to differ across edges. The cycle affinity in the stated orientation is `log(3/64)`. The separate source-clock comparator is `Q_clock(h)=Q0 diag(exp(-h f))`; it is not the geometric intervention. The full matrices, rules and work convention are in the retained [construction](source/opportunity_kinetics/lead/CONSTRUCTION.txt).

## Matched passive laws and the finite active example

The producer construction reports that the driven triangle and a reversible three-state star have the same complete A-started and stationary binary path laws under passive observation, including waiting-time and many-time statistics. Under the same geometric action, the triangle's reported response delivers work through the field port. The reversible star's instantaneous generator remains detailed-balanced at every fixed control value; its driven state need not track instantaneous equilibrium. It is passive over the stated closed state-distribution/control cycles. This is a finite-model indistinguishability example under the stated calibration and hidden-energy assumptions.

For `h(t)=0.3 cos(0.01t)` (period `200 pi`), the saved 8192-interval profile is retained byte-for-byte at [binary_cycle_certified.profile.json](source/opportunity_kinetics/lead/binary_cycle_certified.profile.json), with SHA-256 `b55a3338be688da94a99ac6d95abd7f2790a60a284c7eee0b762f2c1ff990a7c`. The producer's [lead certificate](source/opportunity_kinetics/lead/binary_cycle_certified.json) reports an exact-periodic `W_on` enclosure of `[-0.000843880568, -0.000648656748]`, hence negative work on the system within this stipulated finite model. It reports chemical input about `3.099733884` and output/fuel ratio `0.00024075`; actuator hardware cost is excluded. The separately retained source-clock run reports `W_on=+0.000713423104` for the same command. A 4096-interval output is retained separately at [binary_interval_independent.json](source/next_unit/root/binary_interval_independent.json); it is not blended with the 8192-interval lead certificate.

The [audit narrative](source/opportunity_kinetics/fast_rotation/BINARY_CERTIFICATE_AUDIT.md) reports an independent interval check, but its pinned code and certificate hashes (`011bc3fc…`, `a61d2b75…`) differ from the retained current lead code and certificate hashes (`a3dd775c…`, `3b0fd3c1…`). The receipt explicitly records this mismatch. The audit and audit program are preserved as historical source evidence; this intake does not treat them as an independent audit of the current lead version.

## Separate atomic-return test and unresolved source-clock claim

The [atomic-return test](source/opportunity_kinetics/controlled_benchmark/ATOMIC_RETURN_TEST.md) gives a separate conditional source-clock null test. It requires a nondisturbing herald for exactly one complete microscopic state at a protocol-period boundary, a known control phase, a repeated closed protocol, and exact work or a valid one-sided work bound. A timeout sets the truncated statistic `Z` to zero. For the source's mixed factor `F=1-lambda+lambda*Z`, the timeout factor is `1-lambda`. The next attempt begins only after the system is actually re-heralded. Its anytime guarantee is across these atomic returns, not arbitrary stopping times within an excursion. A coarse-block herald does not satisfy the proof.

The construction also asserts a broader passivity claim for closed state-distribution/control cycles in a source-clock family, but its complete Gibbs-tilt relative-entropy derivation was not located in the retrieved sources. The [fixed-horizon source-clock IFT](source/opportunity_kinetics/controlled_benchmark/SOURCE_CLOCK_IFT_TEST.md) assumes a stationary initial law and a predeclared horizon; it is a distinct result and does not fill that derivation gap. The broad claim remains source-reported and not independently verified. This gap is separate from preserving the finite triangle example, reversible-star comparator and scoped atomic-return argument.

## Relation to N713 and evidence boundary

The existing [N713 dossier](../../../../../../frontier/dossiers/N713.txt) already records the broad passive-versus-active distinction and geometric-versus-source-clock kinetic-access obstruction. This intake contributes the concrete triangle/star passive-law match and the conditional atomic-return test. It does not reprove N713, close its [independent-review gate](../../../../../../frontier/gates/G-EC-N713-INDEPENDENT-REVIEW.json), or promote its source-derived-unreviewed status.

The work is modelled state-energy work, not a complete device ledger. The source reports no acquired physical experiment or actuator hardware; the small output/fuel ratio establishes no useful device efficiency. Novelty, historical priority and physical advantage remain unestablished. The source receipt also records the audit-pin and profile-version boundaries; the unit-specific files are preserved as received, while unrelated native receipts and separate three-state source artifacts are outside this intake.
