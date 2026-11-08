# Governing dependency map

All directories below are under `proofs/`. Preserve their relative layout when running the diagnostics. Original manifest identities are recorded in SOURCE_PROVENANCE.json rather than distributing stale, nonportable manifests. The release-root `MANIFEST.sha256` and `VERIFY_MANIFEST.py` are the authoritative integrity check.

## 1. Finite-patch noise/spatial estimate

`b_many_region_transfer_20261108/REPORT.md` gives the trace-normalized finite-patch estimate: erasure, low-Pauli-weight counting, physical hypercontractivity and noise decay, with full volume factors. Its two audits and diagnostics are included.

**Correction:** for two-body multi-site targets, the governing geometric proof is the later `b_global_activities_20261108/FIRST_DISCOVERY_PROOF.md`, including its physical-probe corollary. It replaces the defective literal source alphabet import; do not resurrect that import from earlier reports.

## 2. Exact global compatible activities and their bound

- `b_global_activities_20261108/EXACT_EXPANSION.md`: edge-subset Möbius inversion, exact component factorization and isolated positive baselines.
- `FIRST_DISCOVERY_PROOF.md`: explicit two-body first-discovery language, full-noise interval resummation, shared classical labels and physical-path count. It retains causal roundtrips after final support disappears.
- `SPATIAL_RESPONSE_CANDIDATE.md`: dense/sparse marked-set split, interface packing, normalization and exponentially small activities. Its historical title is not a current “unreviewed” status.
- `FINITE_ALGORITHM.md`: connected-cluster enumeration, Ursell subset recursion, approximate log normalization and sequential output sampling.
- `ALL_TIME_COST_BOUNDARY.md`: adaptive b, radius and cutoff, giving patch volume O_rho(tau^2 + tau L).
- `second_audit/INDEPENDENT_AUDIT.md` and `b_global_activity_audit_20261108/REPORT.md`: earlier independent proofs/checks and correction history.

**Superseded material:** `WORD_LIFT_LEMMA.md` is retained for history, not as the governing multi-site proof. The original termwise input precision of order 2^(-m^2) in `FINITE_ALGORITHM.md` is replaced by the pinned-KP perturbation estimate below. The classical Ursell integers still need O(m^2) bits; that arithmetic cost is paid separately.

## 3. Physical scalar precision: pinned KP derivative

`b_time_composition_audit_20261108/REPORT.md` proves the sufficient perturbation contract

    |delta w_C| <= [delta_log/(10n)] exp(-b |C|).

The doubled activity envelope remains in the KP region, and the pinned derivative is bounded by exp(|C|). This costs O(log(n/delta_log) + b|C|) input bits, not O(m^2) bits of **quantum scalar accuracy**. `b_pauli_activity_evaluator_20261108/REGULARITY_LEMMA.md`, Section 9, records the dependency. Both new end-to-end reviews recheck it. The newer clipped-activity refinement is not needed for this release's theorem.

## 4. Compact warm-boundary representations

`b_pauli_activity_evaluator_20261108/REGULARITY_LEMMA.md` proves the changing-exponent coefficient bound, weighted coefficient-2 bound and two-sided scalar pairing. The two warm operators are smoothed inside the noisy dynamics. Product physical boundaries supply the normalized Schatten estimates; supplied sparse lists are not assumed free. Its independent audit and exact/float diagnostics are included.

For fixed rho_0, a common executable choice is

    d=63, k=2, J_bound=gamma max(rho_0,1),
    a_0=1/[252 max(rho_0,1)],
    p=2/(1+a_0), u=a_0/2, theta=a_0/4.

## 5. Constructing and propagating those lists

- `b_pauli_discovery_20261108/DISCOVERY_LEMMA.md`: rational tetrahedral product probes, attenuated Walsh coefficients, bounded prefix-energy sampling, signed leaves, clipping and work caps.
- `SPARSE_PROPAGATION.md`: allocated local Pauli maps, Trotter error, thresholding, common-dyadic finite precision and all-outcomes norm budgets.
- `RECURSION.md`: the original fully paid physical scalar recursion, product-boundary closure, executable time thresholds, retiled deleted-edge patches and all-outcomes guards.
- `independent_audit/REPORT.md`: original discovery/construction audit. The final new end-to-end audit rederives these parts rather than merely citing its verdict.

**What is reused versus replaced:** the new construction uses one level of this discovery/propagation operation. Its child log budget L' <= A_rho L is paid. Repeated warm-time descent and its log-star accumulated precision factor are replaced by the next step. The historical log-star bound is not silently relabeled as polynomial.

## 6. New direct static-patch evaluator and one-level closure

`b_static_patch_mpo_20261108/PROOF_DRAFT.md`:

1. deterministic tilted slicing with maximum layer size O(N^(3/4));
2. mixed coordinatewise Taylor remainder using complete local Lindblad generators and CPTP backgrounds;
3. coefficientwise phase/cut rank accounting with growing local layer dimension;
4. explicit exact-rational suffix/prefix interpolation sweeps and bounded integer coefficient gauges;
5. subexponential patch cost and substitution on child patches of size O_rho(L log L).

`THEOREM_AND_COST.md` consolidates the full input scope, cutoff and uniform bound. `independent_audit/AUDIT.md` checks the new evaluator, including its exact arithmetic. The two final full-chain audits are listed in `START_HERE.md`.

## 7. Full output and time uniformity

The late mixing shortcut first caps relevant numerical action at O(L). Hamiltonian/noise normalization uses L/gamma at dimensionless time, so a tiny encoded gamma does not introduce a hidden numerical 1/gamma cost. Child scalar queries remain exact experiments with product boundaries on deleted-coupling geometry; they are not correlated-state restarts.

Per-prefix scalar accuracy, failure and random-bit budgets are allocated uniformly. At each actual history, sequential coupling pays the next-bit kernel difference. No global conditioning on all successful estimates is used. The final unconditional TV guarantee is therefore part of the theorem, not merely a conditional-on-oracle-success claim.
