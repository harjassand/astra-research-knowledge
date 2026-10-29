# Independent review: streaming antisymmetric growth

2026-10-29. **ACCEPT** exact conditional support-preserving growth, the known-control Lüders implementation, the fresh-record hazard bound, and finite-call readiness at the stated memoryless-source scope. No native d9 circuit, approximate-support robustness, broad-source readiness, or physical-control advantage is accepted.

## Exact instrument and retained block

The compression-to-projector lemma is correct. If E†UE=P=P²=P† and U is unitary, then for v in im(P), E†UEv=v has the full norm of UEv. Consequently UEv=Ev. For v in ker(P), UEv has zero overlap with the ancilla-zero subspace. Thus Q0UE=EP and (I−Q0)UE=UE(I−P). Coherently flagging those ancilla subspaces and then applying U† produces E P and E(I−P), with the flag retained. This is an exact Lüders instrument, including entangled references. The reverse operation is the inverse of a supplied known-control circuit, not an inverse of the unknown source or environment.

The whole proof needs the *projector* compression; a generic successful Kraus operator does not give these branches. The supplied permutation-LCU has precisely the antisymmetric projector as its compression. Uniform selector preparation, controlled permutations, signs, predicate copy and uncomputation are actual required known controls. At size8 the stated two-network count56 addressed record transpositions/224 four-qubit bit swaps is a compositional upper-level count, not a native two-qubit gate compilation; state preparation, predicates and work/routing/protection remain charged.

Because P_(k+1)≤P_k⊗I, both Lüders projectors commute with and preserve the old-support projector. Discarding only the new record after failure therefore leaves the maintained block in wedge^k W, even for arbitrary old/new/bath correlations. At size8, wedge^8 W is one-dimensional, so Hodge decoding gives a pure kernel program decoupled from all other systems. Repeated extraction preserves the earlier pure program. The current growing block uses at most8 records, but previously stored outputs, acquisition ancillas and control/workspace are additional protected quantum systems.

**Useful counterexample:** performing only the LCU, measuring its selector, and discarding a failed selector is not equivalent. For an antisymmetric two-record block on labels0,1 and a new label2, the naive failure instrument leaks old antisymmetric support with probability1/3. Our independently constructed dense circuit reproduces this. The author's flag-plus-inverse construction removes the failure leakage. This validates why its additional operation is load-bearing.

## Conditional hazards and source-memory boundary

For a normalized antisymmetric k-record state, the number operator for a chosen one-particle vector has spectrum0,1. Hence its one-body density satisfies0≤gamma≤P_W and trace(gamma)=k. For a **fresh independent** record sigma, the antisymmetric coset identity gives

p_grow=[1−Tr(gamma sigma)]/(k+1).

Since sigma≥a P_W and P_W−gamma≥0, p_grow≥(r−k)a/(k+1). This bound holds for every conditional old-block state, so previous failures need not be independent. Conditional waiting hazards are bounded below; coupling with fresh uniforms or iterated conditional survival bounds gives domination by the sequential geometric birth chain. The actual failure state is retained, not reset to a favorable state.

Freshness is essential. The correlated state sum_i |ii><ii|/r has both marginals I_W/r (full rank), but zero antisymmetric growth at k=1. A source can repeat one hidden classical label forever while preserving these full-rank unconditional marginals. This is an explicit counterexample to replacing the fresh-product promise by a marginal occupation estimate. It does not refute the author, who excludes precisely this extrapolation. General memory-bearing sources retain exact conditional correctness but may never finish.

For the declared memoryless two-axis example, every source call is paid. The first progress probability is4/9; later ones multiply that minus probability by the growth bound. The listed eight rational rates are correct. I independently reproduced all12 finite-cap rows using successive geometric probability-mass convolutions rather than the author's per-call progress update. Mean calls per program≤590.3357142857143 and readiness for two programs at2048 calls≥0.9502105865823118 are valid ideal-model bounds. These are source-call budgets, not wall-clock acquisition guarantees under control latency or source drift.

## Actual CP simulation and independent checks

All source files were copied before replay. Core hashes verify. The dense known-unitary author checks and exact DP replay pass. The2000 compressed trajectories reproduce1991 ready, mean799.836 calls and353.3895 growth measurements; only runtime differs. The observed0.9955 readiness is a finite simulation frequency, not the rigorous bound.

Independently reconstructed dense CP maps for r=4,k=1,2,3 agree with the proposed diagonal subset success/failure matrices within6.67e−16. In particular failure is not simply retaining the old diagonal state unchanged: it contains the partial trace of the projected-success term, producing the stated transitions between subsets. Diagonal preservation follows from phase covariance. The eigenbasis used for this simulation is a diagnostic coordinate choice, not a controller capability.

Further independent results in `INDEPENDENT_CHECKS.json`:
- correct full Lüders failure operator residual2.63e−15;
- failure support residual for arbitrary correlated old/new/bath dimension5 fixture2.06e−16;
- naive failure old-block leakage1/3;
- correlated full-rank-marginal growth probability0;
- all12 exact finite-tail rows and exact expectation reproduced.

## Prior machinery and acceptance scope

[The October2026 primary preprint](https://arxiv.org/html/2610.02103v1), Algorithm2 and its antisymmetric-measurement sections, was inspected. It supplies a closely related random-block growth framework and discusses approximating the full post-measurement instrument with pairwise SWAP tests. The present receipt does not inherit its convergence/complexity theorem: the author's fresh-record hazard and exact known-LCU argument are independently checked here. No historical novelty or optimality is inferred.

Accepted capability is a finite capped, exact unknown-frame program-acquisition route under a fixed common kernel and supplied protected trusted controls, with concrete informative-IID readiness. This is meaningfully different from a one-shot rare eight-record exterior event, while giving a weaker bound than the separately accepted collective Schur route on the example. Equal-information conventional quantum processing can use the same operations. The protected-controller payload-storage bypass remains a valid comparator; no generic memory advantage is established.

Finite synthesis/calibration errors, imperfect common support, label decoherence, false heralds, timing, routing and memory protection require new budgets. Gate teleportation failures can damage unknown inputs; acquisition completion is not safe payload recovery. This receipt does not require or verify the separate stronger quaternion conversion. The independently accepted symmetrized two-output transducer may be composed separately with its own receipt and conditional probabilities, without changing the acquisition result.
