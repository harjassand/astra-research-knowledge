# Principal review and decisions

15 October 2026. This is root's current-campaign reconstruction, not external review or formal verification.

## Phase-clock theorem

Root read all of `workers/foundational_math/PHASE_CLOCK_THEOREM.md` and reconstructed its three steps:

1. For a row-stochastic n-state matrix P, a unit-modulus phase z, and delta=min_{1<=q<=n}|1-z^q|>0, an approximate eigenvector with infinity norm one has residual at least delta^2/(8n). Markov expectation bounds give n+1 approximations to successive phase points using only n state values; two values coincide. This proves the resolvent bound without diagonalization, a stationary distribution, or a condition-number premise.
2. The terminal probability sequence mu P^k f has a finite Fourier sum bounded by 16n/delta^2. The target cosine's corresponding sum grows at least (T+1)(1/2-2epsilon)-1/|1-z^2|. A badly approximable phase gives delta>=4kappa/n and therefore the cubic lower bound on n.
3. At a continued-fraction denominator N, mixing two neighboring cyclic shifts aligns the phase exactly and loses radius only O(N^-3). The terminal cosine readout then has error at most 2 pi^2 T/N^3. Bounded ratios of consecutive denominators give the matching state-count upper law.

No gap was found in this reconstruction. The proof applies to arbitrary initial distributions and stochastic matrices, including reducible, transient and nonnormal models. The output is one terminal probability after k identical waits; it is not a claim about repeated measurements of an undisturbed qubit or an autonomous stationary binary output process. The external controller may supply a terminal read command, but supplying the elapsed k to the readout would change the task and defeat this finite-state comparison.

The phase is supplied equally. The exact quantum rotation is an ideal input. Physical gate precision/coherence/reset/readout costs have not been acquired. The classical construction's transition precision also grows as O(log(T/epsilon)) bits. Counting stochastic states is distinct from binary memory: n=Theta(T^(1/3)) is Theta(log T) state-address bits. A conventional counter plus numerical cosine evaluation remains a serious comparator for ordinary computing. This result does not establish extraordinary technology or historical novelty.

The next mathematical step is an independent specialist comparison with unary probabilistic/quantum automata, positive-realization theory, and stochastic resolvent bounds, followed by formal or separately authored proof review. This is a finite-horizon quantitative theorem and should not be presented as a newly discovered qualitative quantum/classical separation.

## Isotope operation

Root derived the fixed-dose ceiling and then found the survival-screen escape. The independent audit in `workers/model_challenger/ISOTOPE_BOUND_AUDIT.md` confirms the corrected quantifiers and gives a separate bounded-dose adaptive counterexample. The controller acquires information even without observing an isotope label: different ejection hazards make survival informative.

Root visually inspected Susi 2016 supplementary Table 1, page 4, from the locally acquired PDF rendering. Its asymmetric uncertainty entries are described as standard errors. Neither those entries nor ratios of central estimates are treated as covered same-process parameters. The table's experimental 95 kV values, 56.6 and 2.1 millibarn, were transcribed into the root arithmetic script. The 85 kV heavy-isotope experimental cross section is absent; model-only extrapolations must not be substituted for it.

At the chosen planning p=.01109 and those central 95 kV estimates, ideal 90% renewal output needs about 105 attempts, 104 fresh refills and 1.959e13 e/nm^2 expected target fluence. These are conditional calculations, not measured performance. The corresponding 0.298 J/nm^2 is incident electron kinetic energy per uniformly addressed area, not absorbed sample heat, total apparatus energy, or per-site energy; a real focused-beam profile and tails are required for those conversions.

Actual beam microscopy does not yet supply the complete same-atom survival record, independent fresh refill, unchanged rate law, neighbor-damage control, or accepted-site shielding required by the renewal proof. Observing occupancy in consecutive frames does not exclude replacement between frames. The source-supported refill countermodel is decisive. Further unqualified stochastic models cannot close this gate; use the source-labelled exchange/flag experiment in the root operation and physical-path reports.

## Sampler comparator correction

Root identified a stronger incumbent before the composite-ring sampler was promoted. A Z/p^aZ state can be expanded into base-p digits: its same-digit update is F_p-affine and carries depend only on lower digits. Original N610 therefore already applies at expanded depth ac for prime-power moduli. The proposed direct subgroup representation may improve complexity or implementation cost, but prime-power arithmetic alone does not acquire a previously inaccessible stationary output. For mixed prime powers, a CRT comparator must preserve joint categories and cross-component forcing; independent component runs are insufficient. Literal inclusion in the original single-field theorem is not claimed for every mixed-prime group. The continuing constructor and separate auditor were both told to test the prime-power same-information comparator.

## Allocation decision

Initial searches stayed independent. Follow-up capacity was spent on exact physical coupling/competitors, an independent isotope quantifier audit, the phase theorem, and the sampler representation. Existing erasure-qubit gates are evidence for co-design, but are credited to their primary authors. Loss-only optical measurements need a target-specific absorption interface; known total-loss control does not acquire one.

The strongest completed positive theorem is the phase-clock state law, pending final audit. Physical isotope rewriting remains a sharply specified experiment. The mission has not been achieved by an experimentally validated new operation or a complete-resource advantage.
