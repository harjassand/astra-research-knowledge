# Transactional quantum DATA bridge: exact result and remaining gap
2026-10-29. New construction; previous reviewed files are unchanged.

## Subsequent stronger result
`FULL_HILBERT_FOREST_GAUGE.md` supplies an exact full-Hilbert local-frame conjugacy: all payload Hamiltonian edges become scalar controller hops, and all DATA actions become instantaneous terminal/abort instruments. This improves on the preliminary count-only conclusion below. It still retains quantum controller memory and requires a dressed finite-time output; it does not assert a classical independent schedule or threshold.

## Useful result first
The repaired architecture admits a **reset-first, one-way transactional variant** with an exact, full-reset-instrument bound: a single bounded-support arbitrary CPTP kick can contaminate computation episodes at only a bounded number of hubs, and at most one computation episode per such hub before its first subsequent terminal/abort reset. During that episode its actually owned data resources cannot be released or newly acquired. This assertion is valid without measuring history-defect projectors and without conditioning on a Hamiltonian clock path.

This is NOT yet the requested circuit DATA-fault norm reduction. In particular, the full physical instrument bound below is not a proof that its marked episodes can be replaced by boundedly many ordinary faulty data-channel locations in a data-independent classical schedule. That quantum serialization/instrument factorization is the remaining missing lemma. No quantum-memory threshold or civilisation-changing foundation is claimed.

## Generator changes
Use the alphabet, supports, consistency tests, ownership-checked gates, complete label-resolved resets, and finite-rate workspace-blind clock monitors of `producer-workspace/REPAIRED_GENERATOR.md`, with these replacements:

1. Acquisition phases are A_0,...,A_k and computation phases are **distinct** C_0,...,C_L. Acquisition remains reversible within A only.
2. Introduce complete one-way commit channels

   J_commit,s = sqrt(kappa_c) |C_0,0><A_k,s|.

   There is NO Hamiltonian A_k↔C_0 edge and no C→A reset. Sum_s J†J=kappa_c |A_k><A_k| tensor I_W. Never coherently sum the s channels.
3. Computation gates connect only C_t↔C_(t+1), with the projector onto actual ownership o_h on every target. C_t requires all k own tags in its consistency predicate.
4. Terminal channels reset C_L,W→Q_0,0. Abort channels reset every R_(p,j),W→Q_0,0. Their existing label-resolved complete overwrite convention remains mandatory.
5. **Disable coherent lock cleanup in every abort phase R.** Cleanup is allowed only in Q, or in A at an unclaimed resource. Thus an abort may coherently reverse to its original C phase, but cannot release any o_h tag before its workspace has been completely reset to Q_0. The unconditional z_h→free reset remains: z_h was never usable ownership for a C gate.
6. A/Q refresh and Q_k→A_0 ready resets remain as before. No new all-resource projector or epoch is introduced.

Two-body support and fixed local dimension are preserved in the original hub/resource-qudit convention. This is an effective driven model using maintained reset resources, not a microscopic passive thermal construction.

## Exact ownership lemma
Let D_h consist of C phases and the abort labels R_(C_t,j) attached to them. In the absence of another kick, while h remains in D_h:

* the projector onto lock label o_h at every resource commutes with every allowed Hamiltonian term and every non-exit reset;
* no other owner's acquisition changes o_h;
* h cannot acquire a free resource;
* the only exit from D_h is a complete terminal/abort workspace reset into Q_0.

Therefore on every coherent ownership block, the set of usable resources is constant throughout a computation episode, even when the initial phase and lock registers are in superposition. This is an operator invariant, not an inference from a sampled path. Non-owned resources may change between other owners/free, but all h gates vanish there. A malformed episode can use a strict subset of R_h, never a replenished or rotating set.

Disabling R cleanup is substantive. In the old rule C→R→cleanup→C could release a resource before reset. Merely separating A_k from C_0 would not establish this lemma.

## Full-Hilbert history invariants survive
Use P_h=|0><0|_W in consistent A/Q blocks, and P_h=V_t |0><0|_W V_t† in consistent C_t blocks, including V_0=I. Set P_h=0 in inconsistent blocks and in R; B_h=I-P_h. Exactly the original blockwise proof gives commuting B_h and [H,B_h]=0. Removing R cleanup cannot break an intertwining identity.

For the new commit reset, consistent A_k and C_0 have identical ownership requirements. Each J_commit,s maps the good input into good output (or annihilates it), and its complete bundled loss commutes with all B_h. Thus every reset preserves each good sector; all joint defect products obey L_clean*(product B_h)≤0. The individual instrument range statement, not only this expectation inequality, is used below.

A clean C episode now heals through forward gates and terminal reset, not by returning to A_k. The previous reverse-to-A workspace-refresh healing path must NOT be reused unchanged. Establishing a new uniform finite-rate healing constant requires its own monitor/path audit.

## One-kick, full-instrument episode count
Assume the pre-kick physical state lies in every good sector, possibly entangled with an arbitrary reference. Let the arbitrary CPTP kick K have physical support X. Define

   H_X={h : support(B_h) intersects X},   m=|H_X|.

With bounded geometry, m is a size-independent constant for bounded X. For h outside H_X, K commutes with its good-sector projector, so that sector remains good under the entire later clean reset instrument, not merely on average.

Retain the actual terminal/abort reset time/location records. Mark each hub h in H_X until its first such post-kick reset into Q_0. This is classical postprocessing of an existing physical record; it does not measure B_h, select a clock path, or modify the dynamics. At retirement its workspace is exactly zero, Q_0 is consistent for every lock configuration, and that hub's good sector is then invariant forever in the one-kick experiment.

Before retirement, a marked hub can enter the C/R(C) component at most once. The only entrance from A is an irreversible commit jump; the only exit is the very terminal/abort reset that retires it. An initial coherent superposition of A/Q/C does not evade the count: a commit jump annihilates its C component, while any branch initially in C has no return to A. No-jump evolution has no A–C coupling. Other abort components R(A), R(Q) carry no payload gates.

Consequently **all non-history computation episodes occur within at most m marked episodes**, each with data-gate support contained in fixed R_h. The direct kick may additionally touch payloads in X. This is an exact structural property of the complete quantum instrument; arbitrary numbers of coherent forward/backward gate excursions inside one episode are allowed. It is not a claim of a bounded number of elementary physical Hamiltonian interactions.

## Honest norm statement
For any finite observation horizon, append a classical register containing the real reset record and the retirement marks above. Including a no-retirement-yet outcome makes the instrument complete. For the single-kick experiment its map I_K is CPTP, hence

   ||I_K||_diamond=1,
   ||I_K-I_id||_diamond≤2.

Here both maps use the same physical clean evolution and record interface; id means omission of the kick. These statements include arbitrary reference entanglement. Projection onto a record event is CP trace-nonincreasing and preserves the unnormalized bound ≤2. Dividing by the event probability is not allowed in this estimate.

For independent Poisson CPTP kicks, the probability of the physical marked kick set supplies ordinary Poisson weights. None of the above converts a physical kick's occurrence probability into a norm bound per specified **completed-data-update index**. In particular, there is no identification of a conditioned clock path with a fresh data map.

## Exactly what is still missing
To finish a bounded DATA-burst theorem in circuit currency, prove an explicit factorization/dilation of this entire instrument into clean intended recovery channels and at most m+O(|X|) faulty bounded-arity **data instruments**, with:

1. a single compatible serialization for overlapping transactions, including coherent malformed lock/clock sectors;
2. the classical schedule, timing and all syndrome outputs retained, or a specified justified coarse-graining;
3. a complete sum over record alternatives, with a norm bound independent of their number and probabilities;
4. a finite-horizon output interface for in-flight clean and marked transactions, or a rigorously analyzed drain;
5. for many kicks, a composition/cluster rule that remains valid when kicks overlap a still-marked episode.

The ownership lemma makes such a factorization plausible: no clean external hub can use an o_h-held resource during its marked episode. It does not itself prove it. In particular, a kicked clock can carry coherence correlated with data; clock/lock checks and later records can expose that information. Replacing them by an independently sampled schedule would silently discard part of the faulty instrument.

There is also no deterministic duration bound: a finite-rate computation/abort reset has no bounded latest jump time. Thus a claim that one kick affects only a bounded number of fixed physical-time cells is false without a probabilistic tail argument. Even a one-dimensional endpoint with reset rate kappa has nonzero no-reset weight e^(-kappa T) for every finite T.

## Comparison with conventional scheduling
A conventional externally clocked circuit already has fixed gate locations, explicit idle/storage locations and a data-fault insertion norm. Here the construction adds a local autonomous arbitration/reset mechanism and bounds the number of potentially malformed transaction episodes, but the data-instrument serialization and wall-clock storage exposure are extra obligations. It has not yet improved on a conventional threshold theorem, removed the need for active entropy export, or proved an autonomous code threshold. The earlier physical-time inclusive fault norm remains valid; the earlier long-wait data-exposure counterexample remains relevant to any attempted update-index conversion.

## Regression evidence
`check_transactional_flags.py` exhaustively checks 29,160 arbitrary clock/lock configurations for two overlapping hubs: 143,676 transitions preserve Boolean no-creation, and 98,172 computation-component continuation checks preserve every actually owned tag. Every computation-component exit is a terminal/abort Q_0 reset. This supports the clock algebra; it is explicitly not a numerical quantum-instrument factorization test.
