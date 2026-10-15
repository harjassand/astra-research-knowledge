# ASTRA ULTRA — Foundational Capability Genesis

15 October 2026, Australia/Brisbane. **MISSION: NOT_ACHIEVED.** The strongest substantive result is an internally proved, separately audited finite-horizon memory law. No investigated mechanism established an experimentally validated new physical operation, exceptional foundational significance, or a complete-resource technological advantage. Mathematical correctness review, historical priority, physical demonstration and practical superiority have separate statuses throughout this packet.

## Strongest surviving result: a sharp phase-memory law

Fix the computable phase `alpha=(sqrt(5)-1)/2` and terminal probabilities

    p_k = (1+cos(2 pi alpha k))/2.

A classical model has an arbitrary initial distribution mu, an arbitrary homogeneous n-state stochastic transition matrix P, and a readout f in [0,1]^n; its terminal probability is `g_k=mu P^k f`. It receives k identical wait commands and one terminal read command. Both models know alpha; the readout is not additionally handed the integer k or an external lookup table. Transient, reducible, nonnormal and real-parameter stochastic models are all admitted.

For every fixed `0<epsilon<1/4`, the minimum classical state count satisfying `|g_k-p_k|<=epsilon` at every integer `0<=k<=T` is

    N_alpha(T,epsilon) = Theta_(alpha,epsilon)(T^(1/3)).

At exactly zero error a distinct argument gives `T<=N_alpha(T,0)<=T+1`. An ideal qubit generates the terminal probabilities exactly by repeated rotation and a final measurement. The result concerns terminal probabilities, not a repeatedly measured undisturbed qubit, a joint stationary output process, or a physical ticking clock.

The lower-bound mechanism is unusually robust to approximation. Stochastic positivity makes an approximate unit-modulus eigenvector place its n coordinate values near n+1 successive phase points. Two coordinate values must coincide, forcing a short approximate phase return. This proves

    ||(zI-P)^(-1)||_infinity <= 8n / min_{1<=q<=n}|1-z^q|^2.

A finite Fourier witness and the phase's Diophantine return bound then give, for any badly approximable alpha with `||q alpha||>=kappa/q`,

    n^3 >= kappa^2 [(T+1)(1/2-2epsilon)-1/|1-z^2|],
    z=exp(2 pi i alpha).

The matching construction mixes two cyclic shifts at a continued-fraction denominator. Its phase is exact and radial loss is O(n^-3), so its terminal error remains bounded through O(n^3) steps. The zero-error argument instead uses Cayley–Hamilton at two consecutive times.

The continuing foundational investigator owns the theorem and construction. A fresh Sol Max auditor checked the complete proof, made the shift weights explicit and contributed the zero-error boundary; root independently reconstructed both arguments. Five finite construction diagnostics passed, including exact rational distribution propagation at T=30 and analytic rounding budgets. Checks at T<=10,000 covered every lag; the million-step case sampled at most 2,000 lags and relied on the written analytic bound for the full horizon. These are internal analytic reviews and bounded computations, not formal or external validation.

Closest competitors already establish the irrational-rotation mechanism and qualitative finite-state obstruction: [positive realization theory](https://sites.math.rutgers.edu/~sussmann/papers/res-farina-tutorial-positive-realization.pdf), [unary quantum/probabilistic automata](https://arxiv.org/abs/1502.01462), and [Karpelevich stochastic eigenvalue geometry](https://arxiv.org/abs/1611.06970). Bounded primary-literature searches did not locate the exact finite-horizon cube-root formulation. **Historical novelty remains UNKNOWN.**

The consequence is a quantitative benchmark for finite stochastic representations, with a sharp distinction between fixed positive error and exact prefix reproduction. It does not establish extraordinary computing. The state address uses only Theta(log T) classical bits; an ordinary counter and cosine evaluator also use O(log T) bits. Both the classical construction and quantum gate require parameter precision growing as O(log(T/epsilon)) bits; physical coherence, calibration, preparation, reset and readout remain charged and unacquired. The next decisive mathematical step is specialist prior-art/proof review, followed by a separately authored formalization if justified.

Evidence: [proof](workers/foundational_math/PHASE_CLOCK_THEOREM.md), [separate audit](workers/foundational_math/audit/AUDIT.md), [branch report](workers/foundational_math/REPORT.md), [root reconstruction](root/INDEPENDENT_REVIEW.md).

## Physical invention: use survival information to select and retain an isotope

The independent physical lead proposed selective light-carbon ejection followed by natural-carbon refill in graphene. A primary experiment observed displacement and next-frame filling in one 95 kV setup, rather than in two unrelated regimes. It did not identify the incoming atom or provide a complete ejection/reset record. Its supplementary table gives central pristine-lattice cross sections 56.6 and 2.1 millibarn for light and heavy carbon; the asymmetric errors are standard errors, not simultaneous confidence limits. [Susi et al., 2016](https://www.nature.com/articles/ncomms13040)

Root derived a fixed-dose obstruction: with independent natural-feed refills of heavy fraction p, the ideal blind writer cannot exceed

    q_star = p sigma_L/[p sigma_L+(1-p)sigma_H].

At planning p=.01109 and those central estimates, q_star≈.2321. The result permits arbitrary vacancy-dependent refill timing but requires the same deterministic cumulative fluence at each attempted site and unconditioned occupied output. The separate audit confirmed this quantifier and supplied a bounded adaptive counterexample. An overly broad bounded-dose formulation was rejected before publication.

That counterexample changed the invention. Root's renewal operation irradiates a fresh atom until ejection or a screening fluence d; an ejection causes a fresh refill and restart, while a complete survivor is accepted and protected. Its ideal accepted heavy probability is

    q(d)=p exp(-sigma_H d)/[p exp(-sigma_H d)+(1-p)exp(-sigma_L d)].

It approaches one even at finite selectivity. Every site eventually outputs in the ideal model, while failed attempts, dose and refills are counted. At the nominal 95 kV rates, 90% accepted composition costs about 105 attempts, 104 refills and 1.959e13 electrons/nm² expected target fluence. Attempt/dose tails are unbounded; finite caps reduce yield. The corresponding 0.298 J/nm² is incident electron kinetic energy per uniformly addressed area, not absorbed heat, per-site energy or wall-plug cost.

The essential physical requirements have **not** been jointly obtained: a same-atom no-ejection record despite between-frame replacement; independent fresh refill with known incorporated composition; the same local cross sections after repair; control of vulnerable neighbors and cumulative beam tails; and protection of accepted sites. The physical lead's collateral model demonstrates why pristine selectivity cannot simply be assigned to a damaged lattice. An independent adversary constructed a same-atom-return/local-redistribution model consistent with the observed filling but with no guaranteed isotope exchange.

The closest competitors are substantial: isotope-controlled CVD already makes 6 nm-period superlattices, and [Senga et al., 2022](https://www.nature.com/articles/s41586-022-04405-w) demonstrated nanometre isotope-domain formation and imaging in a different catalysed crack/high-temperature process. Those operations do not acquire the renewal interface, but they prevent crediting generic local isotope writing as new. The potential downstream output here is a narrowly qualified isotope specimen for separating mass and chemical/structural effects. Energy abundance, scalable purification and a quantum-device benefit are not established.

The decisive experiment first measures source-labelled exchange, missed ejections, same-atom return, neighbor damage and the event detector under one frozen process. Only a qualified event/reset channel justifies blinded natural-feed renewal trials and a matched final-pattern/device comparison. Further ideal-model elaboration cannot acquire those data. [Operation and proof](root/ISOTOPE_RENEWAL_OPERATION.md) · [physical report](workers/physical_path/REPORT.md) · [decisive experiment](workers/physical_path/DECISIVE_EXPERIMENT.md).

## Computational transfer and its measured failure to win

Astra N610 inspired a direct subgroup version of exact local stationary sampling. For finite abelian group G, strict triangular layer depth c, parent bound k, m requested coordinates and Haar-reset probability s, the derived expected fresh-category bound is

    E Q <= (lambda(G)m/s) sum_{j=0}^{c-1}(1+lambda(G)kc²/s)^j,
    lambda(G)=Omega(|G|).

Uniform noise masks an ancestor only when its homomorphic image lies inside the accumulated subgroup and the required independence holds. Descending-time processing, delayed noise values and a shared category oracle preserve that independence. Strict subgroup growth replaces field rank; no nonunit inverse is used. The cyclic-ring prototype uses exact HNF and local callable descriptors. Acquisition/address/circuit and subgroup bit costs are charged; this is an expected bound, not a finite worst-case runtime guarantee.

Root found the stronger comparator: prime-power arithmetic already fits N610 through base-p digit layers. Thus the direct representation improves a stated conservative upper bound at fixed original depth, not the accessible output class for prime powers. It proves no lower bound on an optimized digit implementation. Mixed-prime CRT comparisons must preserve joint forcing/categories.

The auditor independently reconstructed the proof, checked 5,184 exact finite conditional distributions, and checked 10,368 exact HNF memberships. It caught and helped correct an O(N) validation scan and an uncounted descriptor re-query. Root replayed the final scripts from copies. In the same 3,000-draw Z/4 fixture, root observed 5.760 fresh events and 3.195 s for subgroup HNF, versus 7.013 events and .405 s for the digit incumbent. Fewer random events did not produce a practical win. A million-site succinct local-oracle example exercised the software interface, not real acquisition. Prior art and performance gates stay open. [Construction](workers/capital_routes/N610_AUDIT.md) · [independent audit](workers/abelian_sampler_audit/REPORT.md).

## Other preserved substantive results

| Route | Result and resulting decision |
|---|---|
| Optical loss attribution | Identical accessible optical instruments can deposit energy in different internal sinks; even adaptive external control cannot acquire the hidden sink label. A passive-resonator counterexample defeats equating total-loss change with target absorption. A two-finite-power saturable-loss focusing theorem survives only fixed delivery, full control and a qualified single-pass response. Existing scalar nonlinear focusing/iTRAN are strong incumbents; no new demonstrated capability. |
| Dual-rail quantum gates | Established erasure encoding and the 2026 SWS gate are positive evidence for co-design. Root's worker proposed a coupler-inclusive monitor but found that the published delayed-check decoder is already a strong comparator; timing, which-path dephasing and monitor-induced loss remain coupled gates. Credit belongs to the primary experimental authors. |
| Branchwise rank collapse | Exact binomial exterior-power cutoff and a sharp trace-preserving family were derived. Established automata/exterior-algebra overlap stopped it as the main lead. Exhaustive restricted binary searches killed an all-dimension extrapolation at d=6; no arbitrary-matrix no-go was inferred. |
| Hidden transfer spectrum | Two exact fair-iid QHMM presentations have full distinct collision-transfer spectra {1/2} and {1/2,1/4,1/8}. Root read the precise v2 theorem hypotheses and reconstructed the counterexample. This refutes the unrestricted full-spectrum invariance statement in that version, while preserving observable scalar poles as invariants. It is a scoped realization correction, not a review of the entire paper. |

Full evidence and source boundaries are in the corresponding worker reports. No other worker's activity or agreement is treated as experimental evidence.

## Collaboration, costs and preservation

The first allocation was three independent Sol Max invention leads and one Luna Max physical-model challenger, with a Luna Capital scout. Follow-ups concentrated on one physical candidate, the independent phase proof, and a specific Capital transfer. Eleven distinct workers participated: five gpt-6.1-sol max and six gpt-6-luna max, plus root. One initial scientific-operation turn ended without an inspectable result and was reassigned; it is not counted as a discovery or a second worker. Continuing investigators retained their constructions. The full contribution map and resource ledger record actual settings and UNKNOWN telemetry.

Collaboration changed the invention: blind isotope replacement became event-conditioned selection; a broad scheduling claim was narrowed by an actual counterexample; the phase auditor supplied the separate exact-error regime; the sampler's digit competitor and total-work accounting defeated an apparent speedup; and independent physical/optical critiques kept missing interfaces visible. The allocation was productive in these observable senses. Discovery gain per token/dollar and individual inference shares are UNKNOWN without telemetry and a controlled allocation experiment.

Root's copy-first replay ran eight selected scripts successfully in 12.729 s with four subprocess slots, followed by a separate .654 s HNF/local-access check. These clocks measure bounded computation under concurrent load, not model inference, physical experiment time, or total research cost. The d=6 exhaustive rank search is producer evidence; root replayed d=4 only. Model tokens, pure inference time, inference energy, aggregate worker compute and monetary cost were unavailable. No lab experiment, paid job, purchase or external message was performed.

Capital was initially retrieved at 25fc24509a59aabee340b36b588c9e59a144253d, with freshly fetched main first observed at 846f185763ed3a27310fad4ce9471ba324d1e5f4. Preservation uses a separate branch from subsequently current main b7cada92d2eb304578be5ed974f1e44b10a89928 after reading N840–N842 and their gates. Publication receipts are separate appendices. Authored results, proofs, failures, dependency provenance and bounded replays are preserved; raw third-party papers/data remain local. Repository validation, hashes, commits and PRs establish their recorded integrity/dissemination scopes only.
