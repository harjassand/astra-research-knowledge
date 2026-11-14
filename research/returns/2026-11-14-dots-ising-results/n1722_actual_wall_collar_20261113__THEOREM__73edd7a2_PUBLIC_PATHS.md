# Short actual physical phase walls: reviewed finite-volume occupation theorem

**Status:** coordinated proof independently reviewed by bridge and GKP, with no additional gap found in the stated short-span integration. Exact finite receipts and an explicit new-sector Gibbs baseline are available. This is not a delivered package and not the full exit theorem.

Keep the original Ising Hamiltonian, fixed core A, actual soft source, heatbath per-site clock, target B={M>=0}, voltage v and capacity C_kappa. Let L=8R and theta4, with the previously certified finite source/capacity instances.

Define H as the union of non-target configurations having an actual noncontractible wall gamma, of physical length p<=2L-8, in fluid's deterministic physical-plus-resolution encoding. This auxiliary zero-energy encoding does NOT redefine A. The length bound forces axial homology since any other primitive homology has physical length at least2L.

## Coordinated geometry contract
Fluid's documents:
- `ising_physical_phase_boundary_20261113/CONSTRUCTION.md` (physical-plus encoding, visible actual label),
- `ising_right_only_bootstrap_20261113/HOLE_FIRST_AUDIT.md` (connected essential right-minus prefixes),
- `ising_physical_phase_boundary_20261113/SHORT_SPAN_COMPLETION.md` and `PIN_CANCELLATION.md`.

The main plus collar D is NN-connected and essential with P(D)<=2p. A deterministic right-only, hole-first sequence first flattens with only >=2-neighbor additions, then grows straight columns until actual B. It preserves every plaquette bit used by gamma's adaptive encoding. The reference geometric order is independent of arbitrary extra source plus bits; those cause skips only.

Physical dual horizontal span is at most(p-L)/2. The inclusive plus-collar width is at most(p-L)/2+2<=L/2-2. After forming its rightmost full plus column, at most L/2-1 further full columns force majority. This leaves room before periodic collar pins. This argument is NOT valid for the previously proposed wider p<2.45L range.

At each queried prefix the main plus pins and right-minus pins remain connected essential sets. Frozen bounded pockets and left-side constants not adjacent to erased variables are canceled identically from the ratio. A suitable auxiliary triangulation is chosen once per prefix and frozen throughout its partition sum, preserving gamma. These details are essential, not cosmetic.

## Pointwise fiber and actual source current
For each native edge and visible gamma, the site index determines the processed geometric prefix even when source plus sites were skipped. The lower and upper endpoints have a relative erased-bit partition bounded by the connected-pin lemma in `CONNECTED_PIN_PARTITION.md`.

During >=2-neighbor flattening the reference perimeter is the exact pinned minimum: replaying remaining additions from any compatible subset never increases perimeter. Thus mincut gap g=0 and moving reference perimeter m<=p. During straight growth, essential pins give minimum p+L, whereas the reference is at most p+L+2; hence g<=2.

The connected-pin lemma splits the other essential contours into ONE versus at least THREE and pays all contractible loops with ordinary pressure. It yields, uniformly,

    J <= 202 n exp(16) 3^p exp[n/6553710000].

This is a pointwise sum over all erased thermal assignments, not a Gibbs-average replacement for the actual current. Every edge has at most2n/L=2L visible noncontractible wall labels; canonical roots remove duplicate root choices. Both endpoint ratios are paid. The original coordinate-current cut lemma gives

    N_H = sum_(x in H) w(x)v(x)
        <= 4 n L J C_kappa.

It is unnecessary to sum over all possible geometric wall words: labels are recovered as actual wall components at the native edge. No assumption that low path barrier alone controls congestion is used.

## Verified finite quantitative outcome
`short_conditional_scalar.py/json` verifies the scalar calculation with exact rational exponential lower receipts and the original capacity exponents. The four bounds are

    R80:    N_H/ZA <= exp(-94),
    R200:   N_H/ZA <= exp(-567),
    R1000:  N_H/ZA <= exp(-3858),
    R10000: N_H/ZA <= exp(-41368).

The geometric contract and cancellation were independently inspected in BRIDGE_INDEPENDENT_REVIEW.md; GKP separately checked the partition decomposition. The receipts include all original clock factors and source normalizers.

## What this would and would not add
This family allows arbitrary other spins and actual rough physical interfaces, without prescribing a full line, an explicit digital anchor, or a low-roughness seed word. It does not cover diagonal-only original-core winding, all long physical interfaces, no-winding-wall high-mass configurations, or the full exit/occupation problem. The independently proved large winding-perimeter Gibbs tail is complementary but does not close the interval between p≈2L and p≈2.45L or all other sectors. No North Star breakthrough is claimed.


## Deterministic reconstruction conventions
Choose the native-coordinate lexicographically least dual vertex as the root of each resolved cycle, orient with plus on the designated growth side, and use a fixed axis isometry for horizontal versus vertical cycles. This is a coordinate convention only: the deterministic physical-plus encoding remains the native one, not a newly recomputed encoding after rotation. Lift the rooted cycle continuously to its proper strip. At every reference step choose the lexicographically first eligible vertex whose removal preserves connection of the right minus region to its untouched exterior; the hole-first lemma proves one exists whenever flattening is unfinished. Once flat, visit new columns in order, with a fixed row order. All tests and tie choices depend on gamma's geometry, not on arbitrary source bits. Native extra plus spins merely cause skipped additions, and every path stops at its first actual B visit.

## Independent and computational checks
BRIDGE_INDEPENDENT_REVIEW.md records a full independent inspection of visibility, ratio cancellation, topology, reconstruction, partition and constants. Fluid's integration.py/json checks 74 actual phase-wall schedules from100 seeded12x12 states,4167 reference prefixes and1719 actual upward flips, with every retained label and target test passing. Our mincut_check.py/json independently performs150 exact integer mincut calculations across8 such actual-wall schedules: bootstrap gap0 and straight gap<=2 hold throughout. These are finite diagnostics supporting the proof, not large-system trajectory simulations.

## Same-new-sector baseline
NEW_SECTOR_BASELINE.md constructs a translated stepped-annulus family with no full lines or diagonal winding and with every plus winding path length at least approximately4L/3. It is therefore outside the earlier short/low-roughness plus-seed routes, yet has an actual eligible wall of length approximately5L/3. Its Gibbs mass normalized by ZA exceeds .022,.14,32million/3,3.2billion/3 at the four instances. These are core-normalized masses, not full-Gibbs probabilities. They establish that the new occupation bounds are not a direct rare-Gibbs-mass estimate on the newly added sector.
