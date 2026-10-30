# Staged capture by retractions and parameter sharpening
30 October 2026. Deterministic/operator construction skeleton. The NOISY RESET/COPY receiving lemma and joint bad-record norm decomposition remain open; this file does not silently promote them to a theorem.

## 1. Physical graph, no port rewiring or unprotected fanout
Use NESTED_GRAPH.md's geometric-layer prefixes G_k. Their union has bounded degree, every prefix has the required strong fixed spectral ratio after a fixed power, and the same root p is the actual read port throughout. A new layer's parent map retracts G_(k+1) onto G_k, identity on old vertices, with uniformly bounded fiber. Each newly introduced vertex copies its parent once; each vertex has four children in its NEXT layer and is never used for unbounded fanout. New-layer edges project to old edges or loops. The entire finite scheduled acquisition has O(log n) stages, O(n) sites, and O(n) copy gates. Fixed graph degree/body constants may be extremely large but do not grow with n.

Prefix acquisition does change local majority tables near the growing frontier. This is declared finite scheduling, not autonomous graph acquisition or a whole autonomous scheduler. Once final size is reached, the majority memory and read interface are time independent.

## 2. A precise rooted-animal pullback lemma
Let H_k be compatible mixed graphs for the majority syndrome, chosen with fixed powers so the physical retraction induces a map on dummy/check features of bounded fiber M and bounded dilation. A new occupied check must map to an old occupied check under ideal copying; checks mapping to loops are unoccupied. Complete an image of each rooted animal A to a connected old rooted animal B by fixed paths. There is a constant C such that

 |B|<=C|A|,  |A intersection sigma_new|<=M |B intersection sigma_old|,

and A is contained in a fixed-fiber inverse image of B. Enlarge M to bound all such fibers and path bookkeeping. Consequently no more than 2^(M|B|) A's can be assigned to B. These graph-map assertions must be checked for the FINAL chosen full-read mixed graph, not merely for the data graph.

For f_A(theta,u)=theta^(u|A|-occupied(A)), define

 theta_sharp=theta^M,  u_sharp=u/(2CM).

For each assigned pair,

 f_A(theta,u) <= theta^(u|B|/C-M occupied(B))
              <= theta^(u|B|/(2C)) f_B(theta_sharp,u_sharp).

Choose theta small enough that 2^M theta^(u/(2C))<=1. Summing proves the exact ideal-copy pullback

 C_k^* V_(k+1)(theta,u) C_k <= V_k(theta_sharp,u_sharp)           (C1)

on the fresh-zero-ancilla subspace. This is a diagonal operator inequality and therefore covers coherent old-record/bath coefficients, not merely classical probabilities. The corresponding W bound has another fixed factor M. No blocksize factor occurs.

## 3. Constant-time sharpening, rather than degraded parameters every level
Both endpoints (theta,u) and (theta_sharp,u_sharp) obey the rooted drift proof if u was chosen sufficiently small and theta sufficiently small. Along a fixed compact parameter path, let gamma_min>0 be the worst earned coefficient. For an animal,

 |d f_A/dt| <= [ |u'| |log theta| + (1+u)|theta'/theta| ] |A| f_A.

Traverse the path slowly enough that the bracket is <=gamma_min/4. This takes a fixed time independent of k,n. The native negative rooted drift pays the increase of the test observable during sharpening, with room for HP noise and port-read perturbations. Parameters are analysis parameters; changing them is NOT a hardware computation.

After sharpening, ideal constant-fanout acquisition returns the potential to the ordinary (theta,u) by (C1). Thus one does not replace u by u/C forever or accumulate eta log n from an unprotected fanout tree. A fixed extra refresh period supplies affine contraction of initial moments if needed. The root's logarithmic inequality (R4) in ROOTED_EXPANDER_PORT_CONSTRUCTION.md controls products of Z factors, so this must be done as a joint moment, not by summing per-record gentle errors.

The same root p serves the quantum memory throughout. Copy gates use old vertices as computational-basis controls and do not change their Z values. Their ideal action therefore does not disturb the read bit. Scheduling majority pause/ownership during a copy stage is permitted only as part of the declared finite capture schedule; its lost drift and ongoing read/noise costs must be paid. One possible method reserves a SECOND stronger parameter interval and relaxes it during the constant-time copy. This is not yet a completed receiving estimate.

## 4. The actual noisy step still to prove
(C1) assumes fresh target zeros and ideal copy. The intended actual step is bounded-strength scheduled local reset plus bounded-depth CNOT copying, with arbitrary incident HP noise and shared bath. The needed lemma is NOT a perfect initialization or a classical trajectory assumption. It must combine:

* the accepted positive subset-moment reset/source machinery for fresh targets;
* the root-weighted test involving already-retained parent errors and quantum controllers;
* partial-circuit conjugation, whose local support enlargement is constant;
* a parameter-slack estimate absorbing C eta W and the fixed read injection while old majority service is paused or altered.

A reset's unconditioned target defect probability alone is insufficient if those defects correlate with large old V. One needs the joint weighted receiving estimate or an actual instrument/norm factorization. This is the remaining local acquisition lemma.

## 5. Initial seed and permanently bad captures
The first seed has a FIXED size n0, chosen independently of final n and horizon. Its raw-input fanout has fixed depth, physical degree and duration. A bounded local-noise norm source failure O(eta^a) is acceptable here, jointly across records, and can mark permanently bad record blocks. Good seed capture is exact consensus or an explicitly admitted small rooted moment. A bad seed need not be a stable flipped bit: its entire internal dynamics can be treated as bath, with only O(1) bounded port couplers reaching the quantum memory, using the accepted strong fixed-support noise budget.

Later phase exits must be jointly norm-controlled and marked similarly. It is invalid to sum O(eta^a) gentle errors over every raw record. A multi-record norm fault decomposition or one actual positive final support projector with local tails is needed, then one good-source gentle cut. The local source dictionary can fold final m'-m on marked records into ATG f, but storage is compared to the ORIGINAL raw baseline m during the intervening quantum evolution.

## 6. Honest conclusion
The nested graph and ideal rooted pullback remove two concrete obstructions: growing physical degree at a fixed port, and loss of control parameters under repeated block growth. The constant-time parameter-sharpening argument is a direct operator calculation. They do not yet establish the actual noisy acquisition lemma or the multirecord phase-exit classification. Full capture remains conditional on those named steps; fixed-rate atomic retention/read has a much more explicit proof route than before.
