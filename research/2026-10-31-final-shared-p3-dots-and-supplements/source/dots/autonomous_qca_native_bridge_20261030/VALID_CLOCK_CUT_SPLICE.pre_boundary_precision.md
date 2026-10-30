# Valid counter corruption is a finite open-cut splice

Status: new exact semantic lemma for the explicitly defined periodic-circuit clock model below. It is NOT an assertion that every underspecified modulo-clock rule has this property. Invalid-clock healing and its physical/noise cost remain separate.

## 1. Explicit clean asynchronous model

Take a fixed finite-depth brickwork circuit repeated in periods. Let h label a spatial gate location together with its layer type. Its CPTP channel Φ_h is fixed; it may act on both quantum DATA and classical control/workspace registers. Gate locations sharing any noncommuting/read-write support are connected in a dependency graph. Their distinct within-period layer order orients each edge g→h from the earlier to the later gate.

Store a separate event counter n_h (modulo Q physically) at each gate location. On an integer lift, a valid cut obeys

    n_g−n_h∈{0,1} for every g→h.                  (1.1)

An attempted update at h executes Φ_h and increments n_h exactly when the increment preserves every incident constraint. Equivalently, earlier-layer neighbors have already completed the next period, and later-layer neighbors have completed the previous period. The native transaction locks the entire DATA/control/counter read-write footprint before evaluating this condition. Rejected attempts are identity.

The event poset has vertices (h,k), k∈Z, with the obvious same-period and preceding-period dependency edges. The set {(h,k):k≤n_h} is a down-set exactly when (1.1) holds. Every accepted update adds an available next vertex. Hence every clean execution is a linear extension of the same open circuit. Different available updates have disjoint or commuting supports by construction. No quantum state is copied. Classical current/old buffers, if needed to compile a parallel classical rule, are explicit circuit wires/gates rather than an unproved read convention.

This model expands each brickwork layer type into its own gate-clock vertex. It is a concrete alternative clean clock interface, not an unannounced change to the paper's literal NE repair.

## 2. Locally valid corruption has bounded virtual thickness

Let n be a valid integer cut. An arbitrary event changes counter residues only on a finite set S, leaving all counters outside S unchanged. Suppose the new residues obey (1.1) modulo Q, and Q>2(|S|+1). Each component of S must have an unchanged boundary (the statement excludes corruption of an entire unanchored synchronization component).

Then the new cut has a unique integer lift n' matching n outside S. One way to see this is to propagate the difference δ=n'−n from the unchanged boundary: along each edge, the difference of the two0/1 edge increments lies in{−1,0,1}. A path inside S to the boundary has length≤|S|+1. Any alternative path discrepancy is a multiple of Q with magnitude< Q, hence vanishes. For each vertex,

    |δ_h|≤distance(h,S^c)≤|S|,
    Σ_h |δ_h|≤|S|².                              (2.1)

Thus the two down-sets differ at only O(|S|²) event vertices, independent of the synchronization diameter M and of the elapsed absolute computation time. For a single changed gate clock, the difference is at most one event.

## 3. Quantum interpretation: leave the splice open

The two cuts agree outside the finite circuit region consisting of their symmetric difference and the fixed support halos of those event vertices. Remove that region and leave its quantum/classical boundary ports open. The rest is exactly the same circuit tensor network before and after the counter change. The physical DATA state need not equal the ideal state on the new cut: place its discrepancy, the actual local counter fault and all retained auxiliary/bath correlations into the open splice tensor.

This does not apply an inverse to a nonunitary channel, copy DATA, or supply an ideal recovery. The splice can be an arbitrary retained comb; no chronological independent-fault decomposition is asserted. Correctness follows only if the common decoder corrects the resulting open-port span and the global signed fault expansion controls the tensor's norm. This is the interface of the separate open-tensor correctness work.

In particular, later correct reads of a valid but shifted counter do not create a new fault each time. They are simply later vertices of the new valid cut. The entire mismatch lies in the finite splice. This statement is special to event counters with the causal constraints (1.1); it is false for a generic persistently wrong classical source bit.

## 4. Exact limitation: sequential read-only fanout

Let one classical source c be flipped once. Let m clean, sequential, mutually exclusive readers each copy c and write a fresh target t_j. The resulting error is X_c∏_j X_(t_j). Ownership and nondemolition read conservation both hold, yet one root has m target descendants.

Therefore `READ_ONLY_CLASSICAL_CLOCK_COMPILER.md` controls immediate label writes of a dirty owner, not the entire subsequent semantic history. The present finite-cut lemma is one way to exclude that counterexample for ALREADY VALID clocks. Invalid clocks still require a genuine containment/repair/progress theorem; reducing the cavity overlap exponent to current-owner multiplicity without it is invalid.
