# Same-attempt rare-label domination: classical interface

Status: reconstructed candidate extension, 2026-10-15 19:40 UTC.
This is a new bounded-interface lemma, not a claim about arbitrary continuous coherent noise.

## Verdict and precise assumptions

The proposed comparison works, without thinning the ideal correction rate, under the following hypotheses.

1. Independent homogeneous Poisson correction streams of rate kappa are sampled exogenously, independently of the initial memory/bath/reference input. Their future increments cannot be read by the instruments. The ideal correction is executed at EVERY attempt.
2. After that correction, an instrument on a fixed bounded memory patch and persistent bath produces a good/bad label. For every fixed realized causal clock history/current mark and every normalized conditional joint state, the bad probability is <=p. Equivalently its bad effect is <=p I. This is a pointwise causal-instrument bound, not only a schedule-averaged probability.
3. A good label preserves every encoded Pauli orbit, possibly with syndrome-dependent bath coefficients; it adds no Pauli error support. A bad label has only the prescribed bounded-patch Pauli support. These statements may be implemented through an operator expansion rather than an actual hidden classical Pauli draw. The same label-supported envelope must dominate every surviving summand.
4. Instrument choices may depend on previous clock history and retained bath records but may not change the clock law. The bounded patch family, its placement and incidence bound are fixed or conservatively enclosed in a fixed patch attached to each clock type.
5. The event order at an attempt is ideal correction, THEN possible fault birth. Both are retained as ordered subevents. Final decoder, initialization and the universal history/homology hypotheses are unchanged.

The joint-twirl construction supplies a mechanism for hypotheses 2–3: fresh discarded joint-frame averaging, a uniform bad-effect bound and orbit-preserving good sectors. This note verifies only the classical probability interface once these properties hold. Its frame/norm claims require the separate quantum proof.

## 1. Conditioning on the full exogenous clocks

Fix a finite torus and horizon. Almost surely there are finitely many attempts, with distinct times. Let H denote their complete locations/times and L_i the bad bits in chronological order.

For each fixed H=h, the instrument circuit at each prefix uses only that prefix's clocks and its current quantum state. Future locations do not enter the map. Because the clocks are exogenous, fixing h does not postselect quantum outcomes or initial quantum input. Given previous labels, averaging unobserved records gives a normalized conditional state (when the history has nonzero probability). The pointwise effect inequality therefore gives

q_i(h,l_1,...,l_(i-1))=P(L_i=1 | H=h,L_<i=l_<i) <=p.

The statement remains true when all earlier quantum outcomes are retained and conditioned; coarser conditioning is a mixture. Dependence through the persistent bath does not invalidate it.

This conclusion needs causality/exogeneity, not merely an unconditional probability bound. For example, setting a first bad bit equal to the indicator that a future exponential clock gap is below its p-quantile gives probability p before observing the future but conditional probability 1 for some complete clock realizations. Such a future-reading instrument is excluded. Conditioning on observed quantum outcomes is also different from fixing the externally sampled clock schedule.

## 2. Conditional monotone coupling

For fixed h, construct recursively with independent U_i uniform on [0,1]:

L_i=1{U_i<=q_i(h,L_<i)},  Xi_i=1{U_i<=p}.

This samples the true conditional label law and iid Bernoulli(p) reference labels, with L_i<=Xi_i simultaneously. The U_i can be chosen independent of H. Therefore the unconditional reference is exactly the original independent Poisson clock field, independently marked at each attempt with Bernoulli(p). This coupling may depend on the initial input through q_i, but the reference marginal and all resulting probability upper bounds do not.

For countably many streams the construction can be made by finite windows/cylinder consistency. The finite torus/horizon construction already suffices for the physical event comparison; the infinite reference process used in replay is defined directly from independent marked packets.

## 3. Increasing envelopes and flags

For fixed clocks, increasing bad labels can only enlarge the location envelope: the ideal correction map is monotone, and at a labeled attempt the extra birth map is an OR with its patch support. Hence the complete correction-then-birth update remains monotone in both incoming envelope and label.

Define the robust block flag B from:
- the original slow-certificate failure, using ALL original correction clocks;
- the original structural-fast-word event, also using ALL those clocks;
- existence of any bad label on an attempt whose fixed fault patch touches the guarded region.

For fixed H, these flags are increasing in labels. Thus B(L)<=B(Xi). A coarse process initialized all healthy and driven by B has more zeros as B increases. The event that any k-connected zero component reaches the escape diameter through a fixed horizon is increasing too; a zero component can only enlarge or merge under added zero vertices. It follows pathwise that the actual robust first-escape event is dominated by the iid-mark reference event.

No monotonicity in the clock configuration is needed or asserted. Slow and fast flags can respond oppositely to added clocks; the coupling preserves the SAME clocks.

## 4. Marked reference packets and probability bound

The reference birth at an attempt is correlated with the correction clock at exactly that event. This is harmless. Spatially disjoint clock/mark packets are independent, and packets in disjoint deterministic slabs are independent. Thus the robust flags have the same kind of fixed-range dependence needed by the replacement domination lemma.

Within one block, no independence between slow, fast and birth flags was ever required: (B) is a union bound. Slow and fast estimates are unchanged because corrections still run at rate kappa, with all original marks counted.

Let N_guard be an upper bound on the number of correction streams whose fault patches touch the primitive guard; each has rate kappa. Independent Bernoulli marking makes their bad substream marginally Poisson of total rate kappa p N_guard. Consequently

P(reference guarded birth) = 1-exp(-kappa p N_guard Delta)
                         <= kappa p N_guard Delta.

If there are nu stream types per lattice cell and each fault patch is enclosed in a fine-coordinate box of fixed radius a around its stream center, a conservative count is

N_guard <= nu ((2R+5)b+2a+3)^4.

Use the actual incidence geometry if different. Primal and dual attempts capable of corrupting a given sector must BOTH be charged. Additional independent face noise adds its previously established birth term. The new bound is

delta <= delta_slow + delta_fast
        + kappa p N_guard Delta
        [+ external face-noise contribution].

Choose fixed patch geometry and guards first, then C,R, the coarse death/dependence target, b, and finally sufficiently small p>0 (and any external rate). Since kappa Delta=Cb, the new birth term is p C b N_guard. A positive p threshold follows, though no useful numerical rate is claimed. Enlarged patch guards must be included when choosing the coarse dependence degree. There is no correction-rate factor (1-p): the ideal correction was not deleted at bad attempts.

## 5. Simultaneous marks, forcing and whole-slab cover

The actual update is two ordered subevents: apply the old-state correction, then infect the fault patch if labeled bad. A backward dependency through the correction reads only its pre-correction state; it cannot use the later birth as an input to that same correction. A bad birth is an external leaf, not an extra reusable correction mark.

On a good block flag there is no touching bad birth. All local corrections therefore agree with the original no-birth forcing argument; the same certificate and fast-word exclusion establish uniform forcing. A birth outside the guard can influence a target only by the same strictly ordered earlier-clock dependency chain. The structural m-word count continues to count distinct correction marks; no equal-time cascade is introduced.

Whole-slab occupancy must include the state after the correction and before the birth as well as after the birth. The source's deterministic tree argument applies with this lexicographic subevent order. Bad blocks are covered by their next-layer coarse zero regardless of transient cancellation. Thus every physical or expanded Pauli-support history remains covered at all needed pre-event times.

## 6. Stopped replay and homology

Apply stopped replay to the iid-mark reference, not to the actual bath-correlated field. In a deterministic prospective-anchor patch, copy each primitive packet jointly as clock time PLUS independent mark. This preserves the same-event correction/birth correlation and keeps the lifted reference law exact. Copying clock and birth fields independently would be wrong.

The robust B rule is the same local function on torus and lift; the first-crossing closed zero ancestry therefore replays exactly as before. Its proof never required independence between event types inside a primitive packet. Guard radius must include the enlarged birth patches.

Microscopic support and accumulated homology proceed through the two subevents. The ideal correction is always legal. A following bounded-patch Pauli term is a local chain F; the common-box argument uses its fixed patch diameter and requires sufficiently large L. The before/after correction states and before/after fault states are all included. Repeated attempts, merges and torus wraps introduce no new topological step.

Hence the source exponential coarse-tail estimate supplies a uniform bound on actual bad-schedule/support events through the monotone coupling, even though the actual label field itself need not have fresh slabs or finite dependence.

## Quantum interface warning

With input-dependent instrument labels, conditioning on a good/bad label sequence is generally trace-decreasing. One must not reuse the earlier proof step saying a channel conditioned on all such labels is CPTP. The classical result supplies a uniform probability bound for a genuine instrument decomposition. The separate quantum argument must factor the recovered good Kraus operators and control the summed bad CP effect uniformly. The good map may be subnormalized and bath-dependent.

Fresh discarded twirl coins, no retained frame record, orbit preservation, and the norm-to-bad-effect estimate are quantum hypotheses outside this classical proof. This comparison does not by itself justify coherent continuous noise, skipped corrections, or feedback-modified attempt rates.

