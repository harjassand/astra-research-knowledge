# Bounded gate: a deterministic uniform-forcing proof

Pin: 3e8a972f2924272e1a89859d2f556b5b1f91d501. Scope: the implication B_(z,n)=0 and phi(zeta_n shifted z)=1 imply zeta_(z,n+1)=1. This is the earliest model-specific deterministic bridge from the asynchronous envelope to the coarse eroder. Neither a small marginal bad probability nor domination alone would supply this bridge.

## Inspected source and limits

Sources: the canonical THEOREM_AND_PROOF.md, the located original sweep/MONOTONE_ENVELOPE.md, and lead/STOPPED_TORUS_REPLAY.md at the pinned revision. The latter adapter assumes exactly this block-forcing property; it does not prove it. The homology summary likewise depends on whole-slab coverage and small components. This note reconstructs the uniform-forcing gate. Internal audit verdicts are not used as premises below.

All three original files are under updates/FZ-positive-memory-genesis-20261016/package/derived/located_prior_capital/research/2026-10-15-autonomous-frontier-v2/ in the public repository.

## Exact deterministic hypothesis

Translate the target cell and slab to C0={0,...,b-1}^4 and [0,Delta]. Take the canonical b>=4, C>10log(8), R>=ceil(280eC)+10 and m=floor(Rb/2). The pathwise implication below only needs R>=6, but that weaker condition alone does not guarantee that the good event can occur. Let G_a be the union of coarse cells with infinity norm at most a. Its fine vertex box is [-ab,(a+1)b-1]^4.

Use precisely the source's old-state simultaneous envelope update. At a clock centered at v, the center becomes its old bit AND the OR of the four old immediate predecessor bits; each opposite corner v+e_i+e_j becomes its old bit OR the AND of the other three old face corners. Face faults set their corners to one.

Assume a locally finite, tie-free schedule inside the primitive guard. The source's good event imposes:

1. No face fault has any vertex in G_(R+2).
2. The reset lower-halfspace clearance certificates for every target vertex finish by Delta. These certificates are defined below solely from this slab's clocks.
3. No length-m strictly backward-time structural clock/input word starts from any target vertex at any slab time.

The third condition ranges over every structural input choice, including self-retention choices, not merely currently active syndrome paths or paths selected after observing the input. Arbitrary initial infection bits and arbitrary permitted exterior histories are allowed.

## Step 1: a finite dependency tree, not an assumed finite speed

For an output bit at w, a potentially updating event is either its own clock at w, with input set {w,w-e_1,...,w-e_4}, or a clock at w-e_i-e_j, with inputs {w,w-e_i,w-e_j,w-e_i-e_j}. Each input and the corresponding clock center is at infinity distance at most one from w. There are 5+6*4=29 structural event/input choices.

Compute a target bit backwards: at the most recent relevant event, replace the output by its monotone Boolean expression in old inputs and recursively inspect each input just before that event. If there is no such event, the input is an initial bit. No birth can terminate a branch inside G_(R+2), by condition 1.

Each branch has strictly decreasing event times because all outputs read the old state. A single event's other output cannot be reused as an input at that same time. If any branch had m clock events, its first m choices would violate condition 3. Thus all branches have fewer than m clock events. The branching is finite, so the whole computation tree is finite. This argument needs no ordering of all events in infinite space and makes no assumption that Poisson dynamics have a deterministic speed limit in general.

After j backward choices, both the selected input and the current clock center are within infinity distance at most j of the initial target. Since m<=Rb/2, all explored input vertices and clock centers lie in [-m,b-1+m]^4, strictly inside G_R. In particular a branch cannot reach an exterior birth or exterior initial datum without first providing the excluded structural prefix. Local finiteness makes every latest relevant local mark well-defined. Self-retention loops can only add strictly earlier marks; they cannot bypass the depth bound.

Therefore, on a fixed good schedule, every target output is a monotone Boolean function solely of the input bits within G_R and the fixed local clock marks. Two inputs ordered within G_R give ordered target outputs, regardless of their exterior values. The same conclusion holds at every time in the slab under the source's whole-slab chain exclusion.

For complete deterministic precision, the reference comparisons below can be run on the finite box G_R, freezing boundary/exterior inputs to their specified halfspace values and using only the finite relevant clock schedule. When an event would also update an exterior output, retain that output's fixed boundary value. The bounded dependency tree never consults this boundary or an omitted exterior event for a target output, so its target evaluation agrees with the same local monotone circuit. No globally well-ordered infinite clock schedule or existence assertion about arbitrary infinite-volume exterior histories is needed.

## Step 2: the four coordinate references

For i=1,...,4 let the reference start healthy on {x_i>=0} and infected elsewhere, with no births. This healthy halfspace is invariant. A center update never creates infection. Any upper-corner addition into that halfspace has a required old input with the same i-th coordinate as the output: use v+e_i if i is a paired direction, otherwise use v. That input is healthy, so the required AND is zero; the output's retained self is also zero.

If all cells in A_i={w:||w||_infinity<=R,w_i>=0} are initially healthy, the actual input is at most this reference throughout G_R: every reference-zero fine vertex has floor(x_i/b)>=0 and lies in such a cell. Elsewhere the reference is one, automatically bounding the actual bit. The target C0 is in the invariant healthy halfspace. Step 1 consequently proves it is healthy at the endpoint (indeed throughout the slab), uniformly in the actual input outside those cells.

## Step 3: the oblique reference and genuinely permanent clearance

Let h(x)=sum_i x_i and start the no-birth reference healthy on h(x)<=-b, infected elsewhere. This lower halfspace is invariant: every nonself input of an upper addition at x has strictly lower height, and center updates cannot create infection.

For a target vertex x, take its finite predecessor cone down to the plane. Put T_y=0 for h(y)<=-b; above the plane put

T_y = first own-site clock at y strictly after max_i T_(y-e_i).

Here unfinished certificates are infinity if the required predecessor or ring is unavailable by Delta. Equivalently, initialize the base plane as certified and scan only local marks through Delta, certifying a site when all predecessors have already been certified. No future mark is requested.

Induct up the finite height DAG. Once all four predecessors of y are permanently healthy in the reference, every upper addition into y has an immediate predecessor among its required inputs, so cannot reinfect it. At the next own-site ring, the predecessor OR is zero and y clears; it is then permanently healthy. Thus T_y certifies permanent clearance, not merely the first observed clearance of an arbitrary actual state.

For x in C0, rank h(x)+b<=5b-4. All cone sites are within fine l1 distance at most 5b of the target, hence within the available fixed guard for R>=6. Condition 2 therefore makes all target reference bits zero by Delta.

If every cell in A_5={w:||w||_infinity<=R,sum_i w_i<=-1} is healthy initially, the actual input is at most this reference in G_R. Indeed x=bw+r with r_i in {0,...,b-1} and h(x)<=-b implies b sum_i w_i<=h(x)<=-b, hence sum_i w_i<=-1. Step 1 transfers the reference's endpoint zeros to the actual target.

## Deduction and universal quantifier

If phi=1, at least one of the five forcing alternatives holds. Steps 2-3 handle each alternative on the very same good schedule. Hence B=0 implies zeta_target(Delta)>=phi(zeta_initial shifted to target). This is a deterministic assertion simultaneous over all initial inputs and exterior histories; no input-specific exceptional event or conditioning on the actual syndrome is introduced.

For a torus, take the source's sufficiently large M so that the primitive guard and its local offsets lift injectively (M>2R+7 is sufficient for these guards). Perform the local dependency computation in this lift. The reference halfspaces are analytical infinite-lattice configurations, not periodic global halfspaces. No independence of periodically repeated clocks is assumed.

## A nonvacuity check and a rejected small-guard shortcut

The source's large R is relevant even to consistency of its good-event definition. The corner x=(b-1,b-1,b-1,b-1) has rank H=5b-4. Completing its predecessor certificate necessarily exhibits a strictly time-ordered predecessor path with H own-site rings. Thus clearance and the no-length-m condition cannot both hold when m<=H. In particular an attempted simplified choice R=6,7,8 with b>=4 would give a vacuous good event. This is not a counterexample to the canonical much larger R.

For a constructive consistency check under the canonical margin, take the finite union of all target predecessor cones above h=-b. Give each cone vertex exactly one ring, with all rings at lower height before any at higher height. Put no other rings in the primitive guard and no births there. Every target certificate finishes by Delta if these finitely many rings are assigned disjoint subintervals inside the slab.

A structural backward path through this schedule has nonincreasing clock-center height. At a fixed height, a self-retention input at an upper corner may pass through up to six distinct lower-corner clocks affecting the same output. A nonself input forces the next available center height to decrease: an own clock at the same center would be the already consumed mark, and an own clock at a higher input height occurs later and cannot be used backwards. At an own-site output, any further available clock similarly has lower center height. Thus each height contributes at most six marks, and the whole path has length at most 6H. Here each site rings only once and simultaneous updates read old state.

Consequently m>6H makes this schedule good. The canonical R easily satisfies this inequality for all b>=4; the displayed source recipe has R=17360 and m=8680b, whereas 6H<30b. Requiring each prescribed clock count/order in open time intervals and silence for the other finitely many primitive streams has strictly positive probability under the independent Poisson law. The local depth barrier also prevents arbitrary exterior events from extending a target path through the silent margin. This establishes nonvacuity only, not the high-probability estimates used by the lifetime argument.

## What this establishes, and what it does not

The pathwise uniform-forcing gate is proved under the literal canonical flags and exact old-state map. No legal-clock counterexample to those hypotheses was found. No finite simulation is used as evidence for the universal conclusion.

The proof does not establish the numerical probability estimates for the certificate/fast-word events, HT's cluster theorem, stopped torus replay, whole-slab connected-component conversion, historical homology or the quantum/bath transfer. Those remain separate deductions. In particular replacing structural words by actual-state-selected paths, using actual first-clearance times instead of reset permanent certificates, permitting same-event new-state cascades, or allowing unflagged interior faults would remove a stated hypothesis and invalidate this proof route.


