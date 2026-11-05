# Independent practical-QEC decision audit

5 November 2026. Status: completed independent correctness audit of the direct sizing construction.

## Completion addendum

The fresh direct constructor has now passed independent full-table, distance-potential, circuit-projection and stopped-trajectory audits at d19 and d23. All original precommit hashes are unchanged. Exact midpoint probability rounding and its full TV expansion are included. The optional stopping uses a genuine uniform-beta likelihood-ratio confidence sequence, not a repeatedly inspected Clopper-Pearson interval.

The original direct intervals reject d19 and pass d23. For conservative reporting across the recorded parallel-construction family, an explicitly allocated error budget can retain the same conclusion: assign alpha=1/6000 to each fresh direct run, alpha=1/12000 to each of the two historical d21 intervals, and reserve alpha=1/12000 for each of constructor2's six distance-by-method intervals. The sum is exactly 1/1000. The resulting direct d19 lower bound is 1.99685218138964e-12, historical tuple d21 lower bound is 1.52253364148037e-12, and direct d23 upper bound is 9.88298197899396e-13. All displayed decimal values summarize exact rational inequalities.

This finite-family accounting includes the identified alternative constructor outputs rather than selecting favorable intervals without correction. It remains conditional on an exhaustive inventory of decision-eligible outputs; it is not a universal guarantee against unrecorded data selection. Choosing a threshold after viewing a valid full confidence interval is not itself an additional pointwise-testing problem: its coverage event controls every threshold. Choosing among different intervals is the relevant issue. No earlier d23 statistical artifact was found in the searched QEC directories; the separate joint-decoder worker confirmed it did no d19/d21/d23 sampling. Constructor2's new samples are explicitly reserved in the budget.

Checks performed: 406,832 original Pauli-generator forward propagations across 151,190 original noise channels, 200 independent stabilizer spot checks, all fresh proposal table inequalities, every fresh distance-potential inequality, every proposal outcome in the stopped trajectories, and all 681 decoder residual/L0 checks. The source routines assume the minimum-weight decoder contract beyond tested syndromes; the confidence theorem assumes ideal IID random bits.

The fresh d19/d23 acquisition-to-decision pipelines cost 99.8863 and 270.8589 seconds, respectively; their sum is 370.7451 seconds, not one uninterrupted wall-time benchmark. Their sampled process-tree memory peaks were below 0.81 GiB. Reusing the existing d21 result does not erase its earlier preparation cost. Independent review used additional measured work, recorded in FINAL_AUDIT.json. No hardware-level or joint-X/Z reliability claim follows.

The older sections below record the initial reasoning and remain background; the completion addendum and FINAL_AUDIT.json are authoritative for the completed new checks.



## Decision contract

The defensible target is the failure probability of one public Stim `surface_code:rotated_memory_z` experiment at exact rational p=1/1000, d rounds, all four generator noise knobs equal p, a specified selected detector sector, and a hash-frozen deterministic integer-cost minimum-weight decoder. Candidates are d=19,21,23. The event is the discrepancy between L0 and the decoder prediction from its permitted syndrome record, including preparation/reset and final readout errors.

A smallest feasible candidate d requires an upper bound U_d <= 1e-12 and lower bounds L_j > 1e-12 for every earlier candidate j. No monotonicity is assumed. If a smaller candidate is unresolved, a passing larger candidate is only the smallest *certified* one, not proven smallest feasible. Failure of all three permits “none of the specified candidates passes,” not a statement about every larger distance.

Independent per-candidate coverage at 99.9% does not give a joint 99.9% selection claim. Three predesignated fixed-n intervals at alpha=1/3000 give joint coverage at least 99.9% by a union bound; independence across candidates is unnecessary. If there are further looks, decoder choices, estimator branches or selected historical runs, include them in error accounting or use a genuinely anytime-valid procedure. A predeclared fixed-n interval must not be carried over to a partial or optionally stopped run. Repeated exact replays of the same PRNG trajectory are not additional independent samples.

There is no finite fixed budget guaranteed to classify a probability arbitrarily close to the threshold. An explicit inconclusive output is essential unless the problem supplies a separation promise.

## New independent result: historical d21 remains excluded

The source-reported fault-tuple run has n=10,000 and x=55. I independently evaluated exact binomial tail inequalities, rather than importing its confidence routine. With alpha=1/3000 and 24-bit outward acceptance endpoints, I obtained

- acceptance endpoints: 54175/16777216 and 145518/16777216;
- circuit-failure interval approximately [1.6099225629634e-12, 4.3257767219727e-12];
- exact lower endpoint strictly greater than 1/10^12, after the full supplied conversion-TV expansion.

A separate exact geometric bound on the binomial upper tail under the threshold null is less than 1e-10. This shows the d21 rejection is robust to modest further multiplicity, but does not by itself validate unknown selection from an unbounded search history. The confidence theorem remains conditional on ideal independent random bits and the frozen decoder contract. Python Mersenne Twister reproducibility is not a proof of the IID premise.

Exact fractions, operation counts, source hash and the checking script are in `audit_results.json` and `audit_decision.py`. This check builds on the already independent graph/table/sampler audits in `canonical_qec_circuit_audit_20261105`, `qec_score_d21_audit_20261105` and `qec_fault_tuple_audit_20261105`; it does not pretend those historical checks were newly rerun here.

## Noise semantics and counterexamples to broader claims

1. Uniform depolarizing errors can be exactly transformed to independent mechanisms. Calling every Stim DEM conversion a correlation approximation is false. For k-qubit depolarization projected onto a rank-r binary image, all nontrivial Fourier characters equal lambda = 1 - 4^k p/(4^k-1). Independent factors on all nonzero image vectors with (1-2q)^(2^(r-1))=lambda reproduce that image law exactly. The previous exact rational factor enclosures correctly control the generally irrational q values.
2. Exact circuit p=1/1000 is not literal binary64 .001. The acquisition explicitly interprets the original channels at rational p and uses Stim floating output only as a diagnostic. Do not treat DEM decimal printing as exact circuit probabilities. The model conversion budget must include graph rounding used by sampling; the historical d21 total is about 3.818e-16.
3. Preserving one detector sector plus L0 preserves correlations *within that selected record*. It does not preserve the joint X/Z detector law. Ignoring the other sector is a decoder definition, not a solution to joint correlated-Pauli decoding. In particular the existing Astra N1730 joint-fault issue is not resolved by this sizing experiment.
4. A logical Z channel can leave every memory-Z experiment unchanged while completely reversing a stored |+> state. Thus an excellent memory-Z number alone never certifies arbitrary-state quantum storage. Claims about both sectors, joint logical failure or logical gates need their own argument.
5. One d-round terminal parity is not “any failure occurred during d rounds,” nor exactly a per-round rate. Even independent per-round logical flips at rate r give terminal error (1-(1-2r)^d)/2, with possible cancellation. The present target is legitimately a per-block terminal error only.
6. The default generator has noise knobs defaulting to zero. “Circuit level at p=.001” alone is underspecified; all four values, final readout treatment, rounds, generator version, circuit bytes, detector subset, observable, decoder costs and ties must be pinned.
7. Quantization can be part of the specified decoder and is not by itself a statistical bias. But the majority-cost witness proof needs an actual exact minimum under those quantized costs. Tests on observed syndromes do not prove that contract for every possible syndrome. Library/source trust must be stated or replaced by a suitable per-decode optimality certificate.

## Physical and computational resource scope

Independent direct circuit enumeration with Stim 1.16.0 gives:

- d19: 361 data + 360 ancillas = 721 qubits, 19 rounds, 25,992 CNOTs, 54,453 original noisy locations.
- d21: 441 data + 440 ancillas = 881 qubits, 21 rounds, 35,280 CNOTs, 73,583 original noisy locations.
- d23: 529 data + 528 ancillas = 1,057 qubits, 23 rounds, 46,552 CNOTs, 96,737 original noisy locations.

The d23/d21 qubit ratio is about 1.200; the qubit-round volume ratio is about 1.314, excluding preparation/readout timing. Ancillas still belong to the physical experiment even if their detector sector is discarded by the decoder. These are circuit counts, not a hardware layout or real-time latency budget. This memory block includes no lattice surgery, state injection, factories, logical gates, routing, leakage suppression, device calibration or classical control hardware.

A performance comparison must include cold acquisition, graph construction, floating proposal preparation, rational repair/certification, compilation, serialization and I/O, every proposal and decoder call, exact confidence computation, and any verifier required to accept the result. Charge tuning and research separately rather than calling them zero. Measure both CPU and wall time, peak memory, hardware/software versions, thread count, and a common final decision/confidence target. A sum of separately timed stages is not a single uninterrupted benchmark. Reusing setup can be reported as an amortized second use but cannot replace first-use totals.

Direct zero-failure sampling would require about 8.006e12 shots for a one-sided alpha=1/3000 upper bound at 1e-12 (about 8.700e12 for an equal-tailed two-sided interval). A rare-event method can do much better, but one must measure its full cost rather than compare only against infeasible brute force.

## Prior-art boundary

The benchmark worker is inspecting stronger current ScaLERQEC IID/profile methods with finite-grid sequential bounds. A claim that all competitors depend on unproved Markov mixing is therefore untenable. Important primary comparators include:

- Bravyi and Vargo, rare-event QEC splitting (2013): https://arxiv.org/abs/1308.6270
- Beverland et al., failure spectra, min-weight onset and multiseeded splitting (2025): https://arxiv.org/abs/2511.15177
- Mullan, Weippert and Brown, malignant-core pruning and subregion MCMC (2026): https://arxiv.org/abs/2607.27153
- Mayer et al., circuit-noise splitting, published 15 October 2026: https://quantum-journal.org/papers/q-2026-10-15-2237/ . Its section 6.1.1 explicitly leaves confidence and convergence open, so it is not a ready substitute for finite-confidence certification.
- Haruna and Murakami, locally balanced/cluster MCMC, 26 October 2026: https://arxiv.org/abs/2610.35498

The broad coverage/conditional-event mixture principle is old (Karp–Luby–Madras; path-reliability sampling; ALOE), and a previous local prior-art audit already documents these overlaps. The possible useful contribution is a complete, selection-valid model-specific sizing result with measured end-to-end costs, or an independently useful new construction. Merely reaching 1e-12, obtaining an IID estimator, or ignoring one syndrome sector is not enough.
