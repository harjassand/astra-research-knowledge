# Stronger repair: the BARE physical graph-state data inherit the sparse-syndrome law

2026-10-29, 20:41 UTC. Independent data-semantics derivation. This removes a real output-interface gap for this particular graph-state factory. It does not certify the separate combined-flag healing/polynomial proof, and does not extend to arbitrary channels.

## Statement

Use the graph-recovery Stinespring completion and commuting dressings U_x in the root `GRAPH_STATE_DATA_BRIDGE.md`. Let U=product_x U_x. Let d_y=(I-S_y)/2 be the graph-syndrome projector on the **bare physical data** (identified with the same data coordinates in the dressed frame). In the dressed frame B_y is the clock-only bad projector: ready is good; an excited clock is good precisely when its label is1 and every adjacent update clock is ready. Set

    C_y=I-(I-d_y)(I-B_y)=d_y OR B_y.

Then, on the whole Hilbert space,

    U^dagger d_y U <= C_y <= A_y.                         (1)

Consequently, for every finite S,

    U^dagger [product_(y in S) d_y] U <= product_(y in S) A_y. (2)

If the actual state rho has the root combined-flag bound in the dressed frame, the bare reduced data state rho_D=Tr_(controllers,bath)rho obeys

    Tr[rho_D product_(y in S) d_y] <=p^|S|.               (3)

Thus no physical U^dagger decoder, dressed measurement, controller drain, or empty-clock postselection is needed to obtain the sparse DATA-syndrome resource-state specification.

## General proof, not merely a finite check

1. For x!=y, graph stabilizers S_x commute with S_y. Also Z_x commutes with S_y because S_y has its only X factor at y. Therefore all data blocks P_x+, P_x-, Z_x P_x-, and -Z_x P_x+ in U_x commute with d_y. Its clock guards also commute. Thus [U_x,d_y]=0 for every x!=y. Since the U_x commute with one another,

       U^dagger d_y U=U_y^dagger d_y U_y.

2. On the subspace (I-d_y)(I-B_y), there are only two possible local clock cases. If y is ready, U_y acts identically by definition. If y is excited, B_y=0 forces label1 and all its neighboring update clocks ready. For d_y=0 the local Stinespring completion maps

       |psi>|1> -> P_y+|psi>|1> + Z_y P_y-|psi>|2>
                    =|psi>|1>.

   Thus U_y is identity on that whole subspace, including arbitrary entanglement with other degrees of freedom. Therefore d_y U_y(I-C_y)=0. This is a kernel containment between orthogonal projectors and proves U_y^dagger d_y U_y<=C_y. The inclusion C_y<=A_y follows because y belongs to the radius-two set R_y.

3. The projectors E_y=U^dagger d_y U commute among themselves; the A_y commute among themselves. From E_y<=A_y, the intersection of all selected E_y ranges lies inside the intersection of all selected A_y ranges. Hence product E_y<=product A_y. This does NOT require every E_y to commute with every A_z. Conjugation preserves products and yields (2).

4. Apply (2) to rho_tilde=U^dagger rho U and use the root joint A bound. This gives (3) for actual bare data.

The proof only needs the specified graph-recovery completion. A generic arbitrary-channel Stinespring frame does not preserve the good-data subspace and still needs a genuine physical output decoder.

## What operational benefit follows

The sparse-syndrome factory can now be stated directly for bare physical data. The coherent-syndrome caveat remains: (3) does not itself dephase the data in the graph basis. The stabilizer twirl in `GRAPH_FACTORY_DATA_SEMANTICS_AUDIT.md` can be applied directly to bare data, without a U^dagger decoder, to produce exactly a p-bounded stochastic Z-error graph-state ensemble. It requires only on-site random Paulis and bounded-neighborhood classical parity information.

Preparing/storing the random bits and applying/reading out the output Paulis and subsequent measurements still incur physical noise. The factory's always-on dynamics during any finite-duration output process must still be accounted for. However, the previously identified **entangling frame-decoder control requirement is eliminated**, not merely deferred.

An instantaneous bare-state specification at time t already follows from (3) without turning off the generator. Exporting that state to another device, preserving it during downstream computation, or establishing a universal threshold remains additional work. No unknown-payload memory result or practical advantage is inferred.

## Exact regression

`check_bare_graph_syndrome.py` extends the root's exact rational 36D two-data-qubit/two-three-level-clock model. All seven exact matrix checks pass, including each bare syndrome projector's containment in its physical combined flag and the joint two-syndrome containment. The regression is subordinate to the general argument above, not a replacement for it.

## Optional direct quantum-resource witness, without twirling

The bare marginal bound already certifies nonclassical entanglement at a fixed local error density, without high global fidelity. For an edge (x,y) of the graph,

    <S_x+S_y> >=2-4p.

For any state separable across a bipartition separating x from y, the restrictions of S_x and S_y anticommute on each side of that cut. For each product state across the cut, the two local expectation-value vectors have Euclidean norm at most1 (the usual two-anticommuting-observable uncertainty bound). Cauchy–Schwarz therefore bounds <S_x+S_y><=1; convexity extends this to separable mixtures across the same cut. Thus p<1/4 proves that the bare factory output is entangled across every bipartition separating x and y. For a connected graph, choosing a crossing edge for each nontrivial cut certifies entanglement across **every fixed bipartition**.

This is a bounded-support observable witness: only the union of the two stabilizer supports is measured. It remains valid with coherent syndrome errors and retained-bath correlations because it is a statement about the reduced bare-data state. It is NOT a claim of genuine multipartite entanglement against arbitrary mixtures over different cuts, distillability, universal measurement-based computation, or a logical threshold. It supplies a simple operational quantum-data consequence of the proved syndrome contract.
