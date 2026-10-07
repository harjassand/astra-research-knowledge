# W10 cross-result mechanism audit

**Scope.** This is a repository-level bridge map, not a new theorem or a claim of novelty. Source status is retained: cards are source-derived/unreviewed except where their cards say otherwise; several source packages/checks are only reported or conditional. A mechanism appearing in two cards is not itself a valid transfer.

## Transfer rule

For any proposed transfer, identify (i) the object being encoded or sampled, (ii) the exact input/output interface, (iii) which information is supplied and which service must be acquired, (iv) the cost charged on both sides, and (v) a lemma whose failure would end the transfer. In particular, total Hilbert/memory dimension, expected photon/reset count, hard support energy, conditional event probability, and total variation error are different resources. The cards explicitly warn against exchanging them without a bridge theorem.

## Three candidate bridges

### C1. Posterior-volume lower bounds as a reusable memory converse

**Cards:** N07/N30 (Gaussian memory), with N46 (intrinsic classicality) and N61 (copy-ladder boundary) as prospective applications or controls.

**Aligned interface.** N07 and N30 both encode a single observation `X` while the unknown parameter is not shown to the encoder; all input-dependent retained data count toward `D`, and the decoder emits a fresh output. Their converse uses the same structural inequality: a decoder POVM has total trace mass at most `D`, so posterior small-ball success is at most `D sup_y Pr_X[A(X,y)]`. N30 strengthens this to joint product-posterior volume for anisotropic weak/strong coordinates. This is a genuinely reusable proof pattern for lower-bounding memory from a target loss, provided the target has a suitable posterior score and small-ball geometry.

**Conditional hypothesis.** For another one-shot experiment with a finite-spanning prior, if one can exhibit an injective posterior statistic `m(x)` whose posterior covariance is bounded below on an event of positive probability, and if the output loss controls `E||m(Y)-m(X)||²`, then arbitrary quantum/hybrid memory `D` still forces a polynomial `D` lower bound by the same trace-mass argument. For Gaussian models N07 supplies these pieces; N30 shows how a scale-dependent proper loss repairs the weak-signal curvature and how joint volume yields a product rather than a max-coordinate bound.

**Paid inputs/costs.** The prior/mean geometry, covariance or radii, and loss are supplied. `D=sum_j d_j` includes every input-dependent register; no free entangled reference/side register or retained real record. N30's Gaussian model comparison, finite-bit compiler, and growing-dimension constants are not supplied by this mechanism. A transfer to N46 would also need a covering/net acquired at the relevant accuracy and the `b log N(a)` complexity term; N46's mixture modulus is qualitative and does not give an efficient channel acquisition.

**Blocking lemma.** Prove a loss-to-posterior-score inequality uniform over all decoder outputs for the proposed experiment, plus a positive-probability region with uniformly nondegenerate posterior Jacobian/covariance. Without this, the trace-mass step has no useful volume bound. For an N46 application, additionally prove that the channel's fidelity/broadcast loss controls this score loss and bound the net/mixture modulus quantitatively.

**Falsifier.** An explicit experiment in the proposed target class where the loss tends to zero but posterior-score distortion stays bounded away from zero, or where score small-ball volume is concentrated on a vanishing-probability set, defeats the transfer. N61 is a required stress test: it shows that small pair gap and two-receiver marginal broadcast error alone do not imply small EB reconstruction error across unrestricted growing families. It does not refute the geometry-conditioned lemma above.

### C2. A relative-count service might remove rare-event rejection in a passive Gaussian subclass

**Cards:** N71/N72/N73 (spectral passive-loss Gaussian count sampling), N42/N43 (positive-kernel rare heralds), and N64 (general phase Gaussian herald tails).

**Aligned interface.** Both branches concern Gaussian optical states and count outputs. N71 provides an approximate *unconditional* full count law for a known passive contraction with independent bounded squeezed vacua, with error controlled by `Tr[(T*T)^3]`; N42 instead asks for counts conditional on a specified subset event and targets worst-case bit complexity without inverse herald probability, under an entrywise-nonnegative rational Bargmann representation and an exact-zero/relative perfect-matching counting service. The possible bridge is a numerator/denominator service: use a passive-loss sampler or covariance certificate to organize a specialized count calculation, then prove a relative estimate for the heralded numerator and exact zero handling.

**Conditional hypothesis.** In the intersection where a passive squeezed-vacuum output admits N42's nonnegative rational Bargmann kernel and the selected herald can be represented by its positive marginal-count weights, a model-specific spectral bound may let one replace some generic marginal enumeration with a passive covariance-based service. It could improve constants or provide an additional exact-covariance baseline; it does not yet remove the need for relative counting.

**Paid inputs/costs.** N71 requires known `T`, squeezed parameters bounded by `rmax`, vacuum environments, and charges expected reset count `E0`, active rank, and survival/inversion arithmetic; its dense real sampler is ideal real arithmetic. N42 requires the physical positive kernel and OA113-style relative FPRAS with exact-zero detection and worst-case bit bounds; it charges numerical `E,h` and model representation. N73's separate candidate accepts rational inputs and has polynomial bit-complexity bounds, but its full high-precision engine was not executed and a large fixture reaches a 216,696-bit precision schedule. No uncharged conversion between covariance data and the exact integer kernel is available.

**Blocking lemma.** For the intersection class, construct an exact rational positive-kernel representation from the passive covariance data and show that the event-conditioned count numerator and denominator can each be approximated *relatively*, with exact-zero detection and costs polynomial in input bits, `E`, `h`, and `1/eps`, independently of the event probability. An additive TV bound on the unconditional law cannot establish this.

**Falsifier.** Find an allowed herald with probability below the unconditional approximation error, or a passive covariance whose induced Bargmann coefficients have signs/phases or bit growth that violate N42's nonnegative rational premise. Either makes conditioning amplify error or destroys the counting interface. N64's quadratic energy tail for arbitrary phases is a warning that N71's no-herald cubic spectral control does not automatically handle general heralds.

### C3. Positive count kernels as a restricted classical-output channel, not full quantum classicality

**Cards:** N42/N95/N96 (positive-kernel/count and replica mechanisms), N46 (EB reconstruction), N98 (positive-kernel limits), N61 (broadcast counterexample).

**Aligned interface.** N42 and N96 supply probability laws over specified count events or diagonal count pins, with positive weights and explicit marginalization/prefix structure. N46 asks for one entanglement-breaking channel that reconstructs an entire uniformly trace-covered quantum experiment on the full algebra; its equivalence with broadcasting uses a compatible `Lp` finite-mixture lemma, but the mixture modulus is qualitative. The overlap is only the restricted experiment where all relevant inputs and losses factor through the same specified count measurement. There, a positive count sampler could acquire classical output statistics for that measurement family.

**Conditional hypothesis.** If a quantum experiment is known to be block-diagonal in an acquired count basis, its admissible losses depend only on those count labels, and a positive-kernel sampler approximates the *whole* induced label law uniformly, then the sampler is a candidate finite-mixture/EB reconstruction service for that restricted experiment. The theorem would concern the restricted measurement algebra, not arbitrary POVMs or quantum states.

**Paid inputs/costs.** The count basis, positive representation, legal measurement family, energy/cutoff, and event set must be supplied or acquired and charged. N42 charges numeric photon/degree bounds and relative-counting cost; N96 additionally charges support acquisition, prefix counts, phases and reversible coherent preparation. N46's full-algebra net and uniform trace-total bound do not come free from diagonal count data. N98 explicitly shows trace-distance accuracy does not protect relative purity and that finite moments do not determine entropy in a black-box spectrum.

**Blocking lemma.** Show that the proposed experiment is operationally sufficient through the count algebra: for every legal input and every loss/measurement in scope, replacing the original output by the sampled count label changes risk by at most `eps`, uniformly. If the claim is full N46 classical reconstruction, also construct an EB channel on the full algebra and prove uniform trace-norm error; diagonal count matching alone cannot do this.

**Falsifier.** A pair of states with identical count laws but different expectations for an allowed off-diagonal measurement immediately refutes extension beyond the count algebra. Or, for a full quantum claim, a faithful family with small broadcasting error and large EB error of the N61 type defeats any complexity-free inference. N98's purity example independently falsifies attempts to infer relative spectral quantities from a trace-close output.

## Three rejected bridges

### R1. “N71's passive-loss sampler gives N42 rare-herald sampling for free.”

Rejected. N71 controls unconditional count-law TV by an `S3` covariance/spectral quantity and uses a centered reset sampler with expected reset count tied to `E0`. N42 conditions on a specified event and requires relative numerator/denominator control plus exact-zero detection; conditional error can scale like unconditional error divided by event probability. The premise sets also differ: N42's entrywise nonnegative rational Bargmann kernel and counting reduction are not implied by a passive covariance contraction. See N71, N72, N42, N64.

### R2. “N42/N96 positive count kernels establish N46 full-algebra entanglement-breaking reconstruction.”

Rejected as stated. N42 samples specified count outcomes; N96's coherent compiler only covers the acquired local positive polynomial cone and specified pins. Neither provides arbitrary later measurements, a full-algebra EB channel, or purification/independent-copy preservation. N46 needs its full-algebra, uniform trace-covering interface; N61 demonstrates why marginal broadcasting alone cannot replace complexity control. Restriction to a supplied diagonal count algebra remains the candidate C3 above.

### R3. “N30 Gaussian memory's continuous-output theorem is a finite-bit or physical quantum memory compiler.”

Rejected. N30 proves matching dimension orders for a supplied one-draw Gaussian location experiment and arbitrary quantum/hybrid encoders, with a classical positive-hat upper bound; its own card says the upper is a measurable continuous-output channel, not finite-bit runtime/preparation. It leaves physical quantum comparison/preparation, finite-bit compiler, growing-dimension constants, and acquisition unresolved. N07 likewise explicitly separates its continuous-output upper from finite-bit runtime. N73's fully separate rational optical sampler cannot fill this gap because it has a different input law, output interface, and charged precision schedule.

## Decision

The strongest near-term reusable object is the posterior-volume lemma in C1: it is already visible in N07/N30 and has a clear checklist for safe reuse. C2 and C3 are interface probes only; their blockers are exact relative conditioning and full-output sufficiency, respectively. No candidate bridge upgrades source status, proves priority, or closes the listed acquisition/implementation gaps.
