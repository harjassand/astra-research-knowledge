# Independent microscopic support gate

## Result

PASS for the stated ideal sweep rule and physical Pauli histories, including both CSS sectors, all inactive outcomes, face faults, and bounded-patch Pauli faults when their entire possible syndrome support is infected. This is a deterministic one-event and event-sequence result, not a proof of the stochastic lifetime or a hardware claim.

Directly fetched and read pinned source `sweep/MONOTONE_ENVELOPE.md` at research commit `3e8a972f2924272e1a89859d2f556b5b1f91d501`, blob SHA `6482ec43addde303cb899a1eca2cd022680ff46d`, under `updates/FZ-positive-memory-genesis-20261016/package/derived/located_prior_capital/research/2026-10-15-autonomous-frontier-v2/`. Also read the acquired original theorem and persistent-bath theorem. This conclusion is reconstructed from the maps, not their audit verdicts.

## Universal local argument

Work over F_2 on the ordinary cubic lattice or a sufficiently large periodic quotient (L>=3 suffices for these distinct local vertices). Write s for the actual edge syndrome, S for its vertex support, and assume S is contained in eta. Let I and O be the incoming and outgoing occupied edge sets at clock vertex v.

1. If I is nonempty, v and at least one predecessor v-e_i lie in S. Therefore eta'_v=eta_v AND OR_i eta_(v-e_i)=1. The physical event is inactive; every other envelope coordinate is unchanged or increased. All of S remains covered, even if O has odd size.
2. If I is empty, the cycle identity boundary(s)=0 implies |O| is even. If O is empty, v is absent from S, so clearing the envelope there is harmless; the physical event is inactive.
3. If I is empty and O has size two or four, partition O into disjoint pairs. For each pair (i,j), add the boundary of the positively based square with vertices v, a=v+e_i, b=v+e_j, c=v+e_i+e_j. Its two edges incident to v are precisely the paired old occupied outgoing edges. Every such edge is toggled exactly once, no incoming edge is changed, and all syndrome incident to v disappears. The side vertices a,b were already in S before the event. The only potentially new support vertex is c, and eta_v=eta_a=eta_b=1 in the OLD configuration, so eta'_c=1. For four outgoing edges the two squares have disjoint direction sets and share only v; the same argument applies simultaneously. Arbitrary preexisting upper edges and cancellations do not change this support containment. Pairing need not be consecutive for this argument; any complete pairing works.
4. No other edges change. Every vertex outside v and the six possible opposite corners retains its old envelope bit. Thus every possible post-event syndrome vertex is covered.

These cases exhaust all eight incident-edge patterns satisfying even central degree. They do not assume the syndrome consists of vertex-disjoint loops, simple loops, contractible loops, or small components. Vertices of degree 4,6,8 and globally winding cycles are allowed. Only closedness is needed. For actual Pauli histories started in code space, s is the boundary of the accumulated face 2-chain; boundary squared equals zero, and every correction/fault preserves this. Closedness alone is stronger than needed physically, since non-boundary cycles also satisfy this local lemma.

The assumption is essential: a lone outgoing occupied edge with no incoming edge has odd degree. The prescribed inactive behavior leaves that defect at v, whereas a minimal envelope has no occupied predecessor and erases v. Such an open string endpoint is not a legal physical syndrome in this model. Measurement errors, altered checks, and arbitrary non-cycle syndrome inputs are therefore not silently covered.

## Faults and CSS sectors

A face fault replaces s by s plus the face boundary, so its new vertex support is contained in old S union the four face corners. Setting all four corners to one covers additions, cancellations, and no-effect fault outcomes. Arbitrary Pauli faults on a fixed patch have syndrome supported in the union of boundaries of its constituent faces; infecting the union of all those corners gives one support envelope valid simultaneously for every patch Pauli, including identity and products with cancellations.

For the Z-error component, this is the primal face-to-edge boundary map. For the X-error component, a physical qubit is identified with its complementary dual face and the identical proof applies in dual coordinates. Corrections in the opposite CSS sector commute with the relevant checks and do not alter its syndrome. A Y fault contributes in both sectors, so both relevant four-corner sets must be infected at that common fault mark. The two sector histories can be correlated; the deterministic containment does not require their independence. An arbitrary patch Pauli decomposes into X and Z components and obeys both versions simultaneously.

For completed correction proposals, exactly one legal active branch or the inactive branch survives on any Pauli code orbit. Inactive outcomes with incoming syndrome are handled in case 1; empty syndrome in case 2. Odd no-incoming local patterns cannot occur on those orbits. The argument does not permit arbitrary failures or arbitrary choices to skip a legally active correction while still executing the clearing envelope map.

## Old-state map, monotonicity, and no mark reuse

Every output is a positive AND/OR expression in old bits; hence the entire simultaneous map is monotone, even though its v-output can decrease. The fault map is monotone too. Consequently containment at one event propagates by induction through any ordered finite sequence, and every supported Pauli history uses the same location-only envelope. Finite torus Poisson schedules have finitely many events on bounded intervals and almost surely no ties; prescribed ties can instead be given an explicit total order.

All output dependencies of a mark (v,t) land on the state immediately BEFORE t. A backwards dependency through that mark cannot next use another output of the same mark: that output belongs to the AFTER state. The next contributing mark must have strictly earlier time. In particular an upper-corner addition must still read the old eta_v even if the event clears v. This establishes no same-event cascades at the microscopic level. It does not establish any stochastic causal-chain tail by itself.

The old-state qualification is necessary. Take the syndrome to be the perimeter of the 2-by-2 square in directions e_1,e_2, with v one corner, and eta its exact vertex support. Then v has the active outgoing pair, its predecessors are healthy, and the interior vertex v+e_1+e_2 is initially healthy. Correcting the lower unit square creates syndrome at that interior vertex while removing v. A sequential implementation which first clears eta_v and then uses that new value for additions misses this newly created syndrome vertex. The stated simultaneous map covers it.

## Independent exhaustive check

`check_microscopic_envelope.py` constructs the 20 local edges consisting of the eight central incident edges and the twelve upper edges of all six positive squares. Their endpoints comprise v, four predecessors, four successors and six opposite corners. It enumerates all local edge subsets with even central degree, performs the actual XOR boundary correction selected by sorted pairing, computes the resulting vertex support, and compares it with the simultaneous envelope of the old support.

Results in `microscopic_check_results.json`:

- 524,288 correction configurations checked: 28,672 active, 491,520 inactive with incoming edges, 4,096 empty central patterns.
- 245,760 Boolean cover pairs checked for monotonicity on all 2^15 local envelope states.
- 6,291,456 face-fault configurations checked, including all six orientations and every local edge subset without parity restriction.
- Zero failures.

This enumeration permits arbitrary upper-edge occupation and imposes parity only at v, so it checks a superset of restrictions of global cycles. External edges cannot affect the central incident pattern because all eight incident edges are included. They can only add old support at other vertices, which the envelope never erases in this event. Monotonicity then extends the minimal-support check to every eta superset and every external completion. This explains the finite test's universal local coverage rather than treating sampling as proof.

## Scope remaining

The source's microscopic support-domination gate closes under these precise assumptions. Probability constants, coarse forcing, domination imports, torus transfer, accumulated homology, and quantum factorization are separate obligations assessed elsewhere. No result here licenses missing correction attempts, syndrome measurement faults creating non-cycles, leakage, uncharged memory interactions, sequential in-place envelope updates, or extension of the original uncompleted Lindblad generator to arbitrary coherent noise.
