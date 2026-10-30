# Bounded-hop envelope recomputation flushes dirty minima

Status: exact finite-state computation lemma for a FIXED quarantined domain and frozen true boundary. This is a local implementation ingredient, not a new shortest-path algorithm, not a self-organizing purge theorem, and not an assumed reliable convergence flag.

## 1. Registers and actual local channel

Let H be a finite graph domain, with a nonempty fixed boundary B carrying frozen integer heights c_b. The classification H/B must be actual and fixed during this epoch: an unverified mutable auxiliary bit is NOT allowed to declare itself a new boundary source. Assume the c_b admit a1-Lipschitz extension. Let D bound the length of a shortest path from any x∈H to any boundary source that attains

    u(x)=min_(b∈B) [c_b+dist_H(x,b)].              (1.1)

For example D≥|H|+1 suffices in the finite connected case.

Each interior site stores either ⊥ or a tuple (v,d), with hop count0≤d≤D. Initially these tuples may be completely wrong, coherently superposed, and entangled with an arbitrary retained bath/reference. Boundary tuples are NOT read from a mutable auxiliary copy: a boundary read supplies its actual frozen value (c_b,0).

An update at x pinches its finite tuple read footprint and replaces its own tuple by the lexicographic minimum of

    (c_b+1,1) for adjacent boundary b,
    (v_y+1,d_y+1) for adjacent interior y with d_y<D. (1.2)

The order is first by value, then by hop count. If there are no candidates, write⊥. The snapshot is CURRENT at its linearization: native ownership of the entire read/write footprint is held from the read through the completed write. Arbitrary observe–delay–commit updates are excluded; stale pending snapshots can reintroduce old forged ranks after a sweep and invalidate §2. The old tuple at x is not included as a remembered minimum. The channel writes only x, so it has fixed nearest-neighbor read/write geometry. The exact native read-only/small-write compiler realizes this finite classical CPTP channel with actual onsite resolved resets. No DATA is altered by this auxiliary computation.

## 2. Forged low values cannot persist indefinitely

Call a tuple legitimate if it equals (c_b+length,length) for some actual boundary-to-site walk of that length≤D. Every candidate derived from a legitimate tuple is legitimate. An illegitimate candidate can only come from an illegitimate neighbor, and its hop count is one greater.

Define an asynchronous sweep as any interval in which every interior site completes at least one correct update (1.2). Extra updates and arbitrary ordering are allowed. After j complete sweeps, every remaining illegitimate tuple has hop count at least j. Proof: initially all ranks are≥0; during the next sweep an illegitimate output derives only from an illegitimate input of rank≥j, hence has rank≥j+1. This lower-rank property, once achieved, is invariant under further updates. Old local tuples are overwritten, not retained.

Therefore after D+1 sweeps no illegitimate tuple survives. In particular a forged very low value with a forged rank0 cannot circulate forever. A fake cycle would have to increase its rank every time its value propagates; there is no modular wrap or decrement of the hop count.

## 3. Exact envelope convergence after the flush

After the flush, every finite stored value is≥u(x). Let d_*(x) be the smallest distance among boundary sources attaining u(x). Along an optimal shortest path, a site's predecessor has the optimal pair with hop count one smaller.

Boundary sources are stable. Once all sites with d_*≤j have their optimal pair, these pairs remain stable forever: no legitimate candidate can have a smaller value, and the lexicographic hop tie-break chooses the minimal optimal distance. Within one further complete sweep, every site with d_*≤j+1 acquires its optimal pair. Hence after at most D additional sweeps all sites have the exact envelope u and the minimal optimal hop counts.

The total sufficient bound is2D+1 sweeps. It is uniform over all dirty auxiliary values and all fair orderings within those sweeps. This is not a statement that fairness alone bounds physical time.

## 4. Finite modulo alphabet without a trusted phase anchor

Store v modulo Q. Suppose the true boundary values have an integer lift with span S, and choose Q>2(S+D+1). All legitimate candidates lie in one integer interval of width at most S+D+1<Q/2. Their residues therefore have a unique cyclic order, obtained by cutting at the unique gap larger than Q/2 (one distinct value is unambiguous).

Use that cyclic order when it is unambiguous; if a dirty candidate set has no such gap, write⊥. The dirty-rank flush is unaffected, since an output is either a candidate with rank increased by1 or⊥. After the flush, the cyclic comparison agrees with the true integer comparison, and §3 applies. The integer lift/range premise itself must be earned from the frozen clock boundary; no auxiliary anchor is trusted.

## 5. Coherent input and real timing

Each update is a genuine classical measure-and-write channel on its tuple read footprint, not an instantaneous physical dephasing approximation. The native realization uses retained copied labels followed by separately resolved terminal discard. A complete sweep overwrites each target in the declared basis. The deterministic argument applies to every classical branch, so after2D+1 correct sweeps the auxiliary output is the exact prescribed basis configuration (conditional on the true frozen boundary), even for arbitrary initial auxiliary/bath/reference correlations. The bath and discarded labels remain in the joint comparison.

A native two-SUCCESS/clear-owner witness can certify correct completed updates in actual windows, but every required local update channel needs its own service test. Mechanical dirty first retirements are excluded or charged in the leading rectangle. A slow actual finite fill clock may make premature fill unlikely while those windows run. That is a paid scheduling event, not a noiseless completion flag. A physical fill operation must not simply trust a dirty 'converged' bit.

## 6. Explicit remaining obligations

This lemma does not create the quarantine, keep its whole collar frozen, merge overlapping epochs, validate arbitrary boundary lifts, or prove a quantum causal cut. It also does not solve an infeasible boundary. A bad physical boundary value is a new clock root, not an auxiliary minimum that this algorithm repairs.

The useful distinction is that read/write radius is local and fixed while D is only a finite onsite rank range and a service-time parameter. This can avoid an M-scale atomic snapshot, provided the separate purge geometry supplies a domain/range bound chosen noncircularly before M.
