# A universal service envelope for the completed two check rule

Principal construction, 16 October 2026. Status: internally derived conditional extension. The ticket invariant, certificate and fixed guard steps survived targeted adversarial checks; the complete principal deduction and global interfaces are in PRINCIPAL_PAIR_THEOREM.md. External correctness and priority remain unestablished. The initial pending version is preserved in history/. The intended two check geometry has Pastawski, Clemente and Cirac as an antecedent, with the Pauli-label caveat recorded in the principal theorem. This construction supplies a location and clock only envelope for its physical pair clocks; a syndrome dependent virtual clock coupling alone would not establish that property.

## Generator and the required stronger quantifier

For each vertex v and pair a={i,j} of its four positive directions, set Pi_(v,a) to the product of the two violated outgoing edge check projectors, Q_(v,a) to the Pauli flip on their positive plaquette, and

    C_(v,a)(rho) = Q_(v,a) Pi_(v,a) rho Pi_(v,a) Q_(v,a) dagger
                   + (I-Pi_(v,a)) rho (I-Pi_(v,a)).          (1)

This channel has 11 qubit support. Use the static generator kappa sum_(v,a,sector)(C_(v,a)-Id). It has six independent rate kappa physical pair proposal clocks per vertex per sector, 12 L^4 channel streams in total. There are two Kraus dissipators per channel, hence 24 L^4 jump terms. The original two check generator has only the active dissipator per pair, 12 L^4 terms, and differs on syndrome coherences. The original whole vertex sweep has 14 L^4 active jumps; its aggregated inactive completion has 16 L^4 dissipators. These are distinct resource counts.

We need one event in physical clock and fault location space that corrects every supported Pauli history. A coupling which chooses a virtual base action from the actual outgoing syndrome establishes a classical law but does not give this quantifier across coherent branches sharing a physical clock schedule. The envelope below uses only the actual six pair clocks.

## Finite service ticket state

Use a SEPARATE envelope and ticket copy for each CSS sector, on its primal or dual vertex lattice. Only that sector's six pair clocks may service its tickets. Opposite sector correction clocks do not tick or reset this copy: their Pauli action and check functions commute with its stabilizers. A fault proposal resets both copies on their respective possible boundary boxes. A single shared ticket serviced by both sectors would be false; the exact counterexample is preserved in workers/compiler_adversary/TICKET_CHECKS.md.

The following definitions and proof concern ONE fixed sector. Let Omega be the six unordered direction pairs in it. At each vertex use state 0, or (r,S) with r in {1,2} and nonempty S subset Omega. Here r is the number of coupon phases still required, and S lists the pair marks still needed in the current phase. Define the maximum state top=(2,Omega). Order states by phase number first, with 0 below all others; within the same r use subset inclusion on S. Larger means less service has been completed. There are 1+2(2^6-1)=127 analytical states per vertex per sector. No such register is implemented.

At a physical pair clock a at w in THIS sector, compute all outputs in this copy from its old state. At the center:

    0 remains 0;
    if center is positive and any predecessor w-e_i is positive, reset to top;
    otherwise apply tick_a to the center.

For a positive state (r,S), tick_a does nothing if a is absent from S. If a belongs to S and S minus {a} is nonempty, replace S by S minus {a}. If S={a}, replace (2,S) by (1,Omega), or (1,S) by 0.

For every pair {i,j}, if the three old states at w, w+e_i and w+e_j are positive, reset w+e_i, w+e_j and w+e_i+e_j to top. This conservative downstream reset is performed at every physical pair proposal, regardless of its label a or actual action. All other states persist. A fault proposal resets to top every vertex in a fixed box covering the possible syndrome boundaries of every Pauli on its patch.

The state maps are monotone in this partial order. Tick preserves inclusion when phase numbers agree; if one state completes a phase, it falls below every state remaining in that phase. Across phases, a phase two state can fall only to the maximum phase one state, which still dominates the tick of every phase one state. The predecessor and three source predicates are increasing, and resets go to the maximum. The maps read only old states within infinity norm distance one, so one clock mark cannot cause an instantaneous cascade.

## Universal support domination

Consider any Pauli history at the fault proposal locations, and its actual legal two check corrections at the physical pair clocks. We show that every incident syndrome vertex has a positive service state for this same envelope. Faults reset every possibly affected vertex to top. An actual correction at w has both outgoing checked edges occupied, so w and the two side vertices are incident before the event. By induction their envelope states are positive, and the three source predicate resets both sides and the opposite corner to top. Every possible change away from the center is covered.

At the center, the correction removes two outgoing edges and never changes its incoming edges. A null center action leaves the actual syndrome unchanged. Resetting to top is safe. The only issue is a service phase completing while the center has no occupied envelope predecessor.

Between any two resets of a center to top, no fault or upstream correction can change an edge incident to it without causing such a reset: a fault is covered directly; an upstream correction puts it at a side or opposite corner, and the preceding argument supplies the reset. Thus during a center coupon phase the outgoing set can only decrease by the center's own actual pair corrections. At every center tick which makes progress, all predecessors are healthy, hence all actual incoming edges are absent and outgoing degree is even. A complete coupon phase has seen every one of the six pair labels since its start. If the initial outgoing set had at least two edges and no pair correction occurred, a pair contained in that unchanged set would have been visited and would have acted, a contradiction. Therefore a complete phase removes at least two edges if any remain, or leaves an already empty set empty. Starting with at most four outgoing edges, after the first completed phase at most two remain; after the second none remain. At the final progress tick the incoming edges are absent as well. Clearing the envelope center therefore never omits an actual incident syndrome.

This argument applies simultaneously to every Pauli history because the ticket resets and progress use no Pauli labels, no actual syndrome, and no Kraus outcome. It permits null fault actions and either CSS sector, with one shared support box for faults affecting both.

A predecessor can become positive and clear between two center marks without resetting the center's old coupon mask. This is safe precisely because every event which can add an actual incident edge at the center resets the entire mask and both phases. Mere envelope infection of a predecessor need not change any actual center edge. No step assumes that predecessors stayed zero throughout a coupon phase; zero predecessors are required at the progress marks, and the between-reset incident-edge invariant controls the intervals between those marks.

## Healthy halfspaces and clearance

The healthy coordinate halfspaces x_i>=a are invariant. A new far corner crossing such a halfspace would require the corresponding side vertex already positive inside it. Side resets require that same side already positive. The lower height halfspaces sum_i x_i<=a are invariant because new sites are strictly downstream. Center maps keep zero healthy.

Once all four predecessors of a site are permanently healthy, no upstream side or far reset can reach it. Its state then clears after at most two complete coupon collections from its own six pair streams. At the time its predecessors clear, those streams are independent of all predecessor certificate streams in the increasing height DAG. Fresh residual waiting times for all six labels are independent Exp(kappa). A coupon collection lasts max_(a in Omega) E_a, bounded by sum_a E_a. The strong Markov property gives fresh residual streams after its first coupon collection. Therefore a dominating site service D has

    E exp(kappa D/2) <= 2^12=4096.                         (2)

For a predecessor directed path of H sites, the moment is at most 4096^H. There are at most 4^H such paths; summing path lengths up to H gives a conservative certificate tail

    P(delay>t) <= 2 (16384)^H exp(-kappa t/2).              (3)

These are independent certificate services, not a claim that actual clearance times are independent.

## Fixed guard forcing and probability transfer

Use the same five coordinate and lower height forcing sets, coarse cell side b, and slab duration Delta=Cb/kappa as the preserved sweep proof. The healthy indicator is one when all ticket states in a cell are zero. Choose s=1, C>10 log(16384), and fixed R>=4096 e C+10. Every output target has at most 11 influencing clock anchors, at most six labels per anchor, and at most five old state inputs per label; 512 is conservative. All such reads move by infinity norm at most one.

The three primitive bad flags are a fault birth meeting the enlarged guard, a truncated current slab lower height service certificate failure, and a strictly ordered m event backward dependency chain ending at a target at any time in the slab, m=floor(Rb/2). A safe marginal bound for a patch radius q and total fault proposal rate nu per owner cell is

    delta <= 2 b^4 exp((5 log(16384)-C/2)b)
             + b^4 (512 kappa Delta)^m/m!
             + nu Delta [ (2R+5)b + 2(q+3) + 3 ]^4.        (4)

Fix C,R,q and the coarse dependence guard before choosing the LSS tolerance and increasing b. The moment and ordered chain terms can then be made arbitrarily small; choose nu/kappa small afterwards. This is the same parameter order as the inherited proof, with different constants. The fixed finite alphabet ticket state changes none of the needed monotonicity, halfspace or local dependency facts. The attractive coarse eroder is unchanged.

The fixed anchor stopped torus replay and whole slab halo argument therefore apply to the native coarse process. Before coarse escape, every Pauli branch has small syndrome components at every event time. Bounded patch transitions and the component filling decoder preserve the entire accumulated homology. Conditional on one good physical proposal schedule, expand local fault Kraus operators in Paulis and use the same decoder. Every recovered Kraus operator is scalar on all six logical qubits, and conditional trace preservation gives the exact identity channel. Averaging schedules yields

    ||Dec_L exp(TG) Enc_L-Id||_diamond
        <= min(2,A_q L^4(1+kappa T)exp(-c_q L))             (5)

for arbitrary local CPTP fault proposals below the fixed total rate ceiling, a compatible family L=b_q M, and the inherited ideal encoding and decoding assumptions. The complete conditional deduction, including the explicit global interfaces and external review obligations, is in PRINCIPAL_PAIR_THEOREM.md. The targeted finite checks exercise local claims and are not premises of the asymptotic proof.

The matched Pauli noise compiler and exact local Choi admission criterion can then be applied to this completed pair generator, giving the same structured coherent tolerance on 11 qubit correction support. They still do not apply to its uncompleted original generator via this argument. Quantitative thresholds remain existential and these more conservative service constants can worsen the sufficient bound.
