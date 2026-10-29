# Constant-record-memory growth of exact unknown-frame programs

2026-10-29. Author construction, receiving review requested. This is an alternative to the collective Schur decoder, using at most eight live label records per program. It avoids the exponentially small success of a single, non-retried eight-record projection. Correctness permits arbitrary correlated source memory; the quantitative readiness result below is for a specified informative memoryless source.

## 1. Support-preserving state machine
Use the accepted coherent commutator instrument to obtain minus labels in one fixed unknown W=c-perp⊂C9, c=vec(R)/sqrt(3), under its full-joint common-frame and protected-control assumptions. Maintain a block A in wedge^k W, initially empty. A first minus label starts k=1. For each subsequent minus label b, perform the EXACT Lüders measurement {P_(k+1), I−P_(k+1)} onto the antisymmetric subspace of A,b.

On success retain all k+1 labels. On failure discard only b and retain the old block A. This is valid because P_(k+1)<=P_k tensor I, hence the two projectors commute and the failure branch preserves the old antisymmetric support. Plus acquisition outcomes are discarded; their source calls and retained-memory backaction are counted. The invariant holds even when new labels are correlated with A and source memory. No reset or product input between the records is assumed for correctness.

At k=8 the block lies in the one-dimensional wedge^8 W. The accepted Hodge decoder yields the pure kernel program |conj(c)>, decoupled from every remaining system. Store it, reset the growth counter and repeat if a second program is needed. Stop at a public source-call cap; failure to obtain enough programs is reported, not converted into an assumed eventual success. A common occupied SINGLE-LABEL subspace of dimension<8 can make completion impossible. The protected-program bypass baseline remains: this is a capability to acquire an unknown frame gate, not a generic storage advantage over simply keeping a payload in the protected controller.

## 2. Exact Lüders measurement from known permutation controls
A successful projector-only Kraus operator is not sufficient: arbitrary failure branches could destroy the old block. The following construction implements both correct branches.

Let E embed the data with a known ancilla in |0>, and let U be the KNOWN permutation-LCU unitary with E†UE=P, where P is the antisymmetric projector. Since P is an orthogonal projector, unitarity implies UEP=EP, while UE(I−P) has ancilla orthogonal to |0>. Apply U, coherently copy the predicate 'ancilla is not all zero' into a fresh outcome qubit, then apply U† to the ancilla and data. The resulting isometry is
 E|psi> -> E[P|psi> tensor |0> + (I−P)|psi> tensor |1>].
Measuring the outcome qubit is exactly the desired Lüders instrument, including arbitrary entangled references. The inverse here is ONLY that of a known finite permutation-control circuit; no source/environment inverse is used.

For k+1<=8, use the previously explicit Fisher–Yates LCU: uniform selector registers of radices2,...,k+1, permutation parity phases, and addressed record swaps. At maximum size,17 selector qubits suffice. U and U† together use at most56 addressed four-qubit register transpositions, i.e.224 selector-controlled bit swaps, plus four selector preparation/unpreparation operations, sign gates and one known all-zero predicate copy. Reversible work qubits, routing, record storage, readout/reset and precision are charged. The known non-power-of-two uniform preparations require paid rotations. This is a concrete finite-control construction, not an assumed native high-rank measurement or exact Clifford+T claim.

Dense checks for (d,k)=(3,1),(4,2) construct U and U† explicitly and verify both Lüders Kraus maps and old-block support preservation. They are small-instance diagnostics of the general exact argument, not a full d9 physical circuit run.

## 3. Uniform growth bound for fresh iid records
Now assume a NEW record is independent of the maintained block and references, with normalized state sigma supported on W of dimension r=8 and sigma>=a P_W. This is an additional acquisition assumption, NOT implied by an observed marginal when source memory can correlate records.

For any normalized block state omega supported on wedge^k W, define the fermionic one-body matrix gamma=sum_(j=1)^k omega_j. It satisfies0<=gamma<=P_W and Tr gamma=k: occupation of any unit vector is a0/1 observable on an antisymmetric block. The antisymmetrizer coset identity gives
 p_grow = Tr[P_(k+1)(omega tensor sigma)]
        = [1−Tr(gamma sigma)]/(k+1)
        >= (r−k)a/(k+1).
The bound is uniform over all prior outcomes and the resulting block state. Thus successive failures need not be independent. A one-dimensional birth chain with these lower transition probabilities is stochastically slower than the actual counter process. This closes finite-call readiness using conditional hazards, not an unsupported iid assumption about waiting times.

## 4. Exact two-axis source and finite source-call cap
For the previously checked memoryless collective mixture exp(−i pi X/4)^tensor2 and exp(−i pi Y/4)^tensor2, equally weighted and arbitrarily locally twisted, the coherent-acquisition minus probability is4/9. The conditional label spectrum is{1,1,1,2,2,3,3,3}/16, so a=1/16. Each ordinary source call has the following conservative progress rates for counters k=0,...,7:
 4/9, 7/72, 1/18, 5/144, 1/45, 1/72, 1/126, 1/288.
At k=0 progress means acquiring the first minus record. At k>=1 it means both a minus outcome and successful growth. Source plus outcomes do not disappear from costs.

The expected ordinary-call count for one program is at most590.3357142857143. `exact_birth_chain.py` computes exact rational finite-cap bounds using integer dynamic programming. For TWO programs, readiness is at least0.9502105865823118 at2048 calls, at least0.9975986427856471 at3072, and at least0.9999037592261252 at4096. These are conservative rigorous ideal-model bounds for this memoryless family, not for arbitrary correlated noise. The unknown local twist does not affect the spectrum or rates, and the controller need not reconstruct it.

Two successful kernel programs can feed the accepted two-output quaternion transducer and a one-outcome gate-teleportation processor. With the original accepted success factors1/9 and1/4, this gives a nonzero exact one-use frame-gate capability without classical frame or environment reconstruction. The separately reviewed stronger four-output conversion may improve that conditional factor, but does not change the acquisition proof. Failed teleportation can damage an unknown input; no deterministic preservation or free retry is claimed.

## 5. Compressed nine-label simulation
For the IID example, covariance permits simulation in the unknown label state's eigenbasis as a DIAGNOSTIC coordinate choice, not as information supplied to the physical controller. Diagonal antisymmetric block states remain diagonal under the exact success map and the failed-new-label trace. `simulate_compressed_growth.py` implements those CP transition matrices on k-subsets (dimension at most70 within W) and samples source flags and measurement outcomes. It is a simulation of the quantum instrument in a justified compressed basis, not a native controlled-SWAP experiment. The exact finite-cap bound is independent of Monte Carlo outcomes.

## 6. Control noise, boundaries and prior machinery
Perfect support and known-control operations are load-bearing. Approximate symmetry and imperfect controls can produce false programs; no robustness/conditional-error amplification theorem is supplied here. All protected labels and work registers, coherent-acquisition circuitry, known permutation controls and finite timing/energy costs are additional resources. A protected controller can itself hold a small payload, so comparison must concern the unknown-frame operation or a separately specified constrained source port, not generic better memory.

Growing antisymmetric blocks and Schur processing are established representation-theoretic tools, not a novelty claim. A recent primary preprint, Brahmachari et al., arXiv:2610.02103 (2026), Algorithm2 and SecVI, develops a related random-block method and pairwise-SWAP implementation. The present fresh-record hazard proof and exact known-LCU Lüders construction are derived above independently; no unreviewed preprint complexity theorem is required for this packet. Historical priority, optimality and superiority to equally informed conventional quantum processing are unestablished.
