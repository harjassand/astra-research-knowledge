# Finite-rate clock projection gives a uniform local completion mechanism

Status: constructive clean-sector theorem for the explicitly augmented generator. It is NOT a proof for the unmonitored coherent scheduler, and NOT an arbitrary-defect theorem until repair paths are supplied. All clock projections below act as identity on syndrome/workspace and quantum data.

## Structural assumptions

1. Every hub has <=k resources, in ANY fixed local order, and a finite reversible circuit path of <=ell steps after acquiring all resources.
2. Acquisition/reversal changes its counter and the selected resource's ownership tag by a unique two-site transition, of nonzero amplitude >=g_min. Reverse acquisition requires only the resource currently owned, never a new resource.
3. Reverse circuit steps are unitary on data/workspace and require only already-owned resources. No other term has the same selected clock transition block with a cancelling amplitude.
4. The summed no-jump loss is clock-diagonal (in particular it has no selected a-to-b clock block). Terminal reset has bundled intensity kappa_h times the terminal clock projector, uniformly over the workspace sector covered by the theorem; kappa_h>=kappa_min>0. Summing its Kraus outcomes is complete on that sector.
5. Old-epoch locks have a finite data-trivial path owned-old <-> Z -> free. Clean Z states reset regardless of other resource availability. New cycles reacquire every support resource before the next epoch flip.
6. Each resource belongs to <=q hubs; all local dimensions, supports, coupling norms, and jump rates are bounded independently of system size.
7. Initial clock support is in the clean legal span (arbitrary coherent superpositions and arbitrary data/reference state within that span). The monitor extension preserves this span.

## Bounded local path: global colors are unnecessary

For target h, let A be all hubs whose supports intersect the target support, including h. There are M<=kq such hubs. Let Gamma contain their hub sites and ALL their resource sites. Its size n is bounded by M(k+1), up to fixed register-placement conventions.

Starting from ANY legal clock basis configuration:

- Roll each hub in A backwards along its circuit path, then backwards along its held acquisition prefix, to counter zero. This takes <=k+ell steps per hub. Crucially, NONE of these steps acquires a fresh resource, so other hubs cannot block the chosen reverse path.
- Clear each remaining old-epoch or Z lock on the target's resources through its cleanup path. The owner lies in A. At most two selected steps per target resource suffice. Current-epoch locks were removed by rollback; clean stale/Z tags are exactly the enabled cleanup cases.
- Acquire all target resources, run its circuit path, and perform its terminal reset.

The total number of selected elementary steps is bounded by

 L=M(k+ell)+3k+ell+1.

Padding with idle checks makes a common L. Outside hubs may occupy non-target resources in Gamma, but rollback never needs those resources unless already owned. Every hub that can compete for a TARGET resource is in A. Thus outside activity cannot invalidate the chosen path's eligibility at its recorded intermediate configurations.

This argument does NOT use increasing global colors. Fixed per-hub orders, including orders admitting classical wait cycles, suffice because the selected path uses backtracking to resolve contention. Global coloring remains useful only for a separate simultaneous wait-chain statement, not for this completion proof.

## Ideal projected one-step estimate, without a Zeno limit

Temporarily insert mathematical joint projective measurements of Gamma's clock labels between steps. These are an analysis device to be replaced below by finite-rate events.

Gamma means COMPLETE PHYSICAL SITES, including all data/workspace factors of the desired gates, not merely their clock factors. Let B bound the sum of norms of Hamiltonian terms touching Gamma plus half the norm bound for the summed no-jump loss of ordinary reset channels on Gamma. Include all additional clean/repair terms touching the region. Define the outside-only CPTP semigroup by retaining terms disjoint from Gamma. The remaining conditional no-ordinary-jump generator V has diamond norm <=2B, uniformly in total system size.

For a desired clock transition a->b, outside-only dynamics commutes with its clock projectors and local gate U_ab. The local off-diagonal block is uniquely P_b H P_a=g_ab U_ab P_a; local no-jump losses are clock-diagonal. Expand the full conditional evolution by the Dyson series about the outside-only CPTP semigroup, then project initially onto a and finally onto b. The zero- and first-order terms vanish. The second-order term has trace exactly g_ab^2 delta^2 for every normalized eligible initial state: only one Hamiltonian insertion on each side survives, and outside dynamics is trace-preserving and commutes with the desired local gate. The trace-norm remainder is bounded by

 (2B delta)^3 exp(2B delta)/6.

Thus choose

 delta <= min{1/(16B), g_min^2/(16 B^3)}.

Each selected Hamiltonian step, with no other ordinary local reset, has probability at least p_H=g_min^2 delta^2/4, uniformly in the conditional outside/data state. This argument uses only bounded local perturbations of an outside CPTP semigroup, not a global Hamiltonian norm or an inverse dissipative interaction picture.

For a selected reset step, require exactly that bundled reset and no other ordinary local resets during delta. Its zeroth-order insertion has probability kappa_h delta by Kraus completeness, and the perturbative correction is at most kappa_h delta[exp(2B delta)-1]. Hence p_J>=kappa_min delta/4 is safe. Idle padding also has positive probability; p_0=min{p_H,p_J,1/4} is safe for the displayed small delta.

The ideal projected path therefore succeeds with probability >=p_0^L for EVERY recorded legal initial configuration. Summing over the initial joint measurement outcomes gives the same bound for arbitrary initial coherent legal states. Choosing a path as a function of the first record is only a disjoint union of successful trajectory events in the analysis, not feedback applied to the actual generator.

## Replace ideal measurements by finite Poisson dephasing

Add at every physical clock site the one-site channels sqrt(gamma) P_c for its clock labels c. Their total jump intensity is gamma I, so attempt times are state-independent Poisson processes. Each event exactly projects the current clock label. Do NOT resolve syndrome/Kraus workspace.

In each measurement window of duration epsilon, require exactly one attempt at every Gamma clock site, in a prescribed site order, and no other attempts there. Its probability is

 w = exp(-n gamma epsilon) (gamma epsilon)^n/n!.

Require no dephasing attempts in the L intervening transition windows; this contributes exp(-n gamma L delta). During a measurement window also select no ordinary local resets. Conditional on the chosen attempt schedule, the resulting recorded instrument differs from the ideal simultaneous joint clock measurement (with outside-only evolution retained) by at most 4B epsilon in trace/diamond norm, for B epsilon small. This is a telescoping diamond-norm bound for the COMPLETE quantum-classical recorded instrument: each projective-measurement instrument, including its classical outcome register, is CPTP and norm-one, and each bounded local-evolution replacement costs at most 2B dt exp(2B epsilon). Summing durations yields <=4B epsilon. Thus there is no multiplication by the number of outcomes or initial configurations.

There are L+1 measurement windows. Choosing

 epsilon <= min{1/(16B), p_0^L/[8B(L+1)]}

makes the full successful-record probability, after factoring out the independent attempt-schedule probabilities, at least p_0^L/2. Therefore by the fixed time

 T=L delta+(L+1)epsilon,

one has the explicit, size-independent bound

 inf_(legal rho) P_rho[target completed at least once by T]
 >= c_path,
 c_path=(p_0^L/2) w^(L+1) exp(-n gamma L delta)>0.

All rates, delta, and epsilon are FINITE fixed constants. There is no infinite-rate dephasing or adiabatic elimination. The number is deliberately terrible.

## Consequences and boundaries

- The same bound applies after any prior record leaving the state in the legal span, so a single target's completion-time tail is exponentially bounded in multiples of T.
- The previous finite-support Lyapunov-polynomial method becomes a plausible route to a joint marked-set stall law once this local bound is formalized for the final complete generator and local support convention. Do not silently assume the full-Hilbert-space version: current eligibility paths use legal clock consistency.
- Arbitrary counter/epoch/tag corruption is NOT covered. The exact matching-epoch self-orphan counterexample remains until owner-counter consistency repair supplies bounded paths for every defective local sector.
- Clock projections preserve clean data-channel semantics because their projectors commute with the history isometry; they do change the clock law and require an explicitly priced physical resource.
