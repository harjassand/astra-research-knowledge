# Exact removal of bridge-Q coherence for full Z-output sampling

Internal theorem candidate, with exact finite checks. This is a circuit-output identity, NOT equality of local channels or intermediate conditional quantum states. It follows from the reset-record incidence/cycle-space observation developed jointly with the fluid researcher. Novelty is not assessed.

## Assumptions and graph

Fix the sampled physical category at every scheduled pair: diagonal D, rare QD, or fully mixed pair reset. Category sampling is state-independent and retains the requested probabilities. Input is a specified computational-basis string (a diagonal mixture may be sampled first). Final outputs are measured in Z. For each physical reset, retain its OLD two Z-measurement outcomes and its two freshly prepared uniform basis bits in the mathematical trajectory expansion.

A vertex is a wire segment from input/reset preparation to the next reset measurement/final Z measurement. Each ACTUAL rare Q occurrence is one undirected edge connecting its two endpoint segments. Distinct occurrences are distinct edges, including PARALLEL edges. A pair reset ends two vertices and begins two new vertices. Ordinary D does not create graph edges because it is diagonal.

Two rare uses of the same physical pair without an intervening reset are parallel edges and form a cycle of length2. They are NOT bridges. A simple-graph implementation that merges them is incorrect.

## Statement

For every bridge occurrence e of this multigraph, replace its coherent Q channel by

C_e(rho) = (144/169)rho + (25/169)(X_u X_v)rho(X_u X_v).

Keep D, every other rare Q, every reset and final Z readout unchanged. Replace all bridges simultaneously if desired. The joint distribution of final Z outputs and all physical reset old/new bits is EXACTLY unchanged. Averaging over sampled categories preserves the original full output law.

C_e is sampled as an ordinary Bernoulli product-Pauli flip. It creates no entanglement by itself. This is not a claim that C_e=Ad(Q) on arbitrary states or for non-Z output measurements.

## Proof by ket/bra incidence constraints

Expand every Q as aI−ib X_uX_v, a=12/13,b=5/13. A ket history chooses binary flip variables z_e; a bra history chooses z'_e. Diagonal gates contribute phases but do not change basis bits. At each wire segment, the initial ket/bra bit is the same fixed input/preparation bit, and the terminal bit is fixed by the same Z readout/reset measurement record. Therefore the XOR of mismatch variables d_e=z_e xor z'_e on all incident Q edges must vanish:

H d=0 over GF(2),

where H is the segment-edge incidence matrix. Thus every contributing mismatch is an Eulerian subgraph.

For a bridge e, remove it and take one resulting component S. Sum its incidence equations. Internal edges cancel twice and the sole boundary edge gives d_e=0. Hence every cross term with z_e != z'_e at that occurrence contributes zero to the joint record/output probability. Keeping only the z_e=z'_e terms replaces Ad(Q) by a²Id+b²Ad(XX), exactly. The same reasoning applies to every bridge simultaneously. Diagonal phases can couple arbitrary paths and graph components, but cannot undo the incidence constraint.

Physical resets must be represented with their measured old bits in this proof. Omitting those boundaries from the graph, treating a reset as deleting all prior correlations, or assuming output equality for a fixed sampled auxiliary bridge-flip path is invalid.

## Correct scope of further simulation

Only nonbridge Q occurrences require coherent treatment after this reduction. However ordinary D can couple quantum states associated with different cyclic graph blocks. Those blocks are NOT automatically independent samplers. Neither the number of cyclic blocks nor cycle rank alone is a polynomial-time guarantee. The full cycle-coset rejection method has overhead exponential in cycle rank, which is extensive at the harder benchmark.

Bernoulli bridge flips must be propagated through the circuit. A site already known in Z has its classical bit flipped; an unknown site receives the local Pauli X. Terminal-Q early measurement may ignore bridge flips as coherence-generating gates only if their subsequent bit flips and all induced diagonal phases are tracked. These monomial operations do not justify ignoring classical feedforward.

Bridge finding costs O(n+M) time and memory with an edge-ID-aware multigraph traversal, where M is the explicit pair-slot count. This is preprocessing cost only; remaining quantum simulation costs must be measured/proved separately.

## Exact checks

check.py/json verifies all final probabilities using rational density matrices on overlapping three-site circuits, including a genuine cycle coupled by D to a bridge. Bridge replacement is exact. Replacing ALL Q in that example is NOT exact (TV17355744/120670225). Two consecutive same-pair Q gates are parallel-cycle edges; incorrectly dephasing both changes TV by7200/28561. Inserting a reset between them makes their graph edges bridges, and replacement then is exact.

prevalence.py/json measures bridge fraction, remaining2-core, cycle rank, largest nonbridge blocks and actual preprocessing time on unfiltered independently seeded16x16 and32x32 depth100 records at r=.03, epsilon=.02/.05. Those finite graph statistics are not a scaling theorem or sampler accuracy test.
