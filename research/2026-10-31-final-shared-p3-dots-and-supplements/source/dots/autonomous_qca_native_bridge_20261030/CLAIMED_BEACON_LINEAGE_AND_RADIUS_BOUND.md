# Claimed beacon lineage and a noncircular finite-cluster radius

Status: new candidate control skeleton with exact CLASSICAL basis-path invariants. It is not yet a coherent inclusive-fault theorem or a whole purge implementation. In particular it does not replace the cavity theorem's read-overlap K by a write-weight K.

## 1. Prevent sequential-reader fanout at its source

A persistent wrong source can be read sequentially by arbitrarily many healthy owners. Exclusive ownership and read-only conservation alone do not stop this. For invalid-clock repair, add an actual claim register for each clock-constraint edge e. It has FREE and one fixed beacon-owner label b_e. The beacon's program phase is a separate physical register, not part of a native hub's disposable clock/workspace.

The following are finite classical attempted channels, compiled with complete footprint ownership and small explicit write sets:

* START_e reads the two numerical clock labels and claim_e. If the constraint is invalid and claim_e=FREE, it writes claim_e=b_e and requests beacon b_e. Otherwise it does nothing.
* WAKE_e sees claim_e=b_e and restarts that SAME beacon if its program phase is idle/malformed. It does not allocate a new beacon identity.
* RELEASE_e writes FREE only after the actual edge is valid and every repair-provenance/erasure marker owned by b_e in its fixed declared patch has been cleared. It does not trust an old completion bit or merely the beacon's claimed phase.
* A nominal ⊥/provenance write carries the actual originating beacon identity (implemented as a fixed relative address in the finite local alphabet). An orphan marker wakes that SAME identity, not a new nearby detector.

The full relevant predicate footprint must be held from read through write. Native private W/rail resets leave these program/claim/marker registers alone; a dirty DATA retirement that changes them is a new charged root, not nominal garbage collection.

A clean ordinary clock update never creates an invalid edge. A nominal purge changes clocks to⊥, which is not treated as a new numerical-invalidity trigger. A nominal fill writes a value compatible with every currently numerical incident clock, so it creates no new invalid edge. An erasure marker is cleared only after a compatible fill.

## 2. Exact lineage statement, at its proper scope

On a classical basis path with isolated arbitrary write insertions, each initially invalid edge can allocate at most its one fixed beacon identity. Keeping its claim until genuine validity prevents an endless sequence of fresh allocations from the same persistent source. Nominal purge/fill/WAKE operations propagate existing beacon identities but do not invent new ones.

Consequently the set of distinct beacon identities ever activated lies in the union of:

1. owners of initially invalid edges;
2. owners of edge predicates whose numerical values/claims are directly changed by a root;
3. beacon identities explicitly introduced into program or erasure-marker fields by a root.

For a fixed bounded-degree small-write primitive, the number of new identities per such root is bounded by a constant. A root's label can be wrong or point to an unexpected nearby owner; it still names one owner per classical branch. This is a lineage cardinality invariant, not a guarantee that every beacon terminates or that its repeated DATA actions are bounded.

Arbitrary coherent root maps can superpose many such identities. To use this invariant in a threshold, one must prove a common-span/inclusive-norm transfer, not sum the union of possible supports as though it were one classical path. That transfer remains OPEN. Nor does this lemma control a generic program-bit fanout; it is specific to the explicit invalid-edge/owner-marker activation contract.

## 3. Geometry recomputed from centers, never trusted from a radius field

A single beacon has a hardwired base ball of radius B, independent of M. A mutable beacon phase may not claim an arbitrary large radius. Given the actual finite set of active beacon centers, compute cluster geometry by a fixed deterministic merge procedure:

1. start with radius-B balls at individual centers;
2. whenever current repair balls overlap, merge their center sets;
3. replace a merged cluster A by a canonically centered enclosing ball of radius at most C[diam(A)+B], for a fixed C≥2;
4. repeat until disjoint.

Every merge consumes at least two previously distinct clusters. If there are at most k beacon centers in a connected merge component, its final radius is bounded by B·C_0^k for a fixed constant C_0 depending only on C and the metric. For example, when two balls of radii r,s overlap, their centers are at distance≤r+s; the merged center diameter is at most a fixed multiple of r+s, so its new radius is≤C_1(r+s+B). Induction on the merge tree gives the exponential-in-k bound.

Thus a fixed k-root contract can reserve an enormous but finite radius R_k before the quantum code/synchronization scale M is chosen. A false single beacon gets only the base ball; it cannot forge k distinct physical centers through a single radius bit. Purge markers retain their actual owner lineage rather than spawning new centers merely because the resulting hole is large.

This geometry alone does not establish a threshold. If k must be chosen larger than a norm-overlap exponent that itself grows with R_k, circularity remains. The present cavity bound still has that problem for a large-read implementation. A truly local distributed implementation or an independently proved semantic write-weight fault estimate is needed before claiming otherwise.

## 4. Remaining actual controller obligations

* Common component/collar freeze must survive a corrupted phase or partial release; actual provenance marks and fresh quiescence predicates, not cached ACKs, are required.
* Fill and release must handle orphan/overlapping epochs without releasing part of a still-active component's collar.
* A DATA purge requires actual retirement of every conflicting native owner, including inverse-B paths; no instantaneous frame inversion is supplied.
* The bounded-hop envelope algorithm can flush dirty auxiliary minima in a fixed frozen domain. It does not establish that the domain or boundary-source classification is correct.
* Native clocks and shared-bath noise must be included in the same physical generator and inclusive norm accounting. No fictitious nominal record is appended to an arbitrary perturbed generator.

These are the next construction tasks, not assumptions hidden inside the lineage or radius lemmas.
