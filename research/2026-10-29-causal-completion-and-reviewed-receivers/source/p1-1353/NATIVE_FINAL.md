I moved the investigation to **the cost of learning useful interventions without identifying the hidden physical dynamics**. The completed unit gives a matching upper and lower horizon exponent, an executed learning certificate, and a constructive examination of what additional physical access can change that cost.

The primary-source search also changed the claim: **the proposed universal-coding-to-experiments bridge already has a direct predecessor**. Peshkin–Mukherjee’s 2001 work explicitly connects prediction regret, trajectory likelihood ratios and polynomial-horizon policy evaluation. I have preserved that finding and withdrawn the broader novelty claim. [arxiv.org](https://arxiv.org/pdf/cs/0105027?utm_source=chatgpt.com)

## Completed result: controller complexity governs a scoped learning cost

Consider a controller with \(S\) supplied observable contexts, \(A\) actual operations and \(d=S(A-1)\) randomized decision parameters. The specimen may have arbitrary hidden memory and nonlinear dynamics; the contexts need not describe its physical state.

For episodes of \(T\) operations, the completed construction establishes, up to logarithms and constants depending on fixed \(A,S\),

\[
N_{\mathrm{episodes}}
\asymp
\frac{T^{d/2}}{\epsilon^{2}}.
\]

The upper route uses the established contextual Krichevsky–Trofimov selector and importance sampling. **My central construction is the matching learning lower bound.** It creates separated regions of action counts, each potentially carrying an unknown useful response. Finding an \(\epsilon\)-optimal controller identifies the useful region.

That lower bound allows a strong conventional learner: adaptive calibration, forced action counts, knowledge of the hard family and unlimited offline computation. It therefore concerns learning from actual noisy experiments, beyond a limitation of one estimator.

The existing complementary role reviewed the actual proof and accepted the corrected version. Two qualifications are explicit: accuracy is chosen before the hard family, and the theorem uses a fixed or capped episode budget. Historical priority for this exact lower-bound construction remains unresolved.

The result counts **warranted episodes**. Preparing their initial law can still depend on hidden dynamics and carry substantial cost. It also controls specified bounded observable scores; it does not reconstruct arbitrary complete records. The full premises and review are preserved in CONTROLLER_COMPLEXITY_AND_REAL_EXPERIMENTS.md[CONTROLLER_COMPLEXITY_AND_REAL_EXPERIMENTS.md](producer-workspace/CONTROLLER_COMPLEXITY_AND_REAL_EXPERIMENTS.md).

## Executed learning with a useful certificate

I implemented the receiver on a hidden transducer with two noncommuting operations, a parameter frozen within each episode, and only a terminal binary readout. The learner received executed action counts and outcomes.

| Result | Value |
|---|---:|
| Calibration episodes | 131,072 |
| Operations per episode | 64 |
| Selected operation probability | \(1543/2048\) |
| Certified improvement over the half-and-half controller | **at least 0.191929786** |
| Certified regret against every probability in \([0,1]\) | **at most 0.133619738** |
| Population-audit regret on the grid | approximately \(0.000042253\) |

The two certificates share a **99% confidence event** under the declared sampling model. I subsequently checked all 4,097 candidate estimates with exact rational arithmetic and certified the numerical confidence ceiling without taking another trial.

A separate fresh deployment check used 65,536 further episodes. Calibration and validation together charged **196,608 preparations, 12,582,912 native calls and 196,608 terminal readings**. These are synthetic experiments. Physical timing, sensing and actuation precision remain separate suppliers.

The fair ordinary incumbent is the same established sampling method, which ties this execution. The result demonstrates a usable receiver, not a new algorithmic advantage. See EXECUTED_CONTROLLER_LEARNING.md[EXECUTED_CONTROLLER_LEARNING.md](producer-workspace/EXECUTED_CONTROLLER_LEARNING.md).

## The physical alternative changed the next opening

The complementary physical construction examined access to the randomness **inside an operation’s transition decision**. For a threshold-controlled stochastic bit, the ideal precision costs differ:

| Actual interface | Calls for parameter accuracy \(\delta\), apart from confidence factors |
|---|---:|
| Observe only transition outcomes | \(\Theta(\delta^{-2})\) |
| Also record the realized random reference | \(\Theta(\delta^{-1})\) |
| Program a calibrated reference | \(O(\log(1/\delta))\) comparisons |

The strongest concrete supplier found is conventional comparator/DAC metrology. The logarithmic procedure is successive-approximation conversion, with real reference accuracy, comparator noise and settling requirements. [Analog Devices](https://www.analog.com/en/resources/technical-articles/successive-approximation-registers-sar-and-flash-adcs.html?utm_source=chatgpt.com)

Two limits survived the construction:

- **Retained randomness strengthens the prediction task.** For \(T\) future reference-and-output records, the exact discrepancy is \(1-(1-\delta)^T\), requiring finer parameter accuracy than output-only prediction.
- **Fresh unobserved residual noise restores a quadratic precision burden**, even with adaptive references and replay. Repeatedly interrogating one held noisy value supplies no new independent information about its underlying mean.

The complete construction and scoped root review are saved. The parallel response-design investigation also produced a useful negative result: an ordinary likelihood-ratio method outperformed the proposed forced-insertion experiment at matched native-call cost.

These comparisons direct the next invention toward **changing the physically accessible information**, with source-innovation observation or control as one concrete candidate. Logged action selectors, detailed balance and a mathematical replay representation do not supply that capability.

## Preserved snapshot

**392 files are saved, including all 346 predecessor files unchanged**, with proofs, raw records, code, actual reviews, corrections and failed claims:

[Astra_P1_Experimental_Learning_and_Noise_Access_20261029.zip](https://chatgpt.com/library?file_id=libfile_fd0ef39348408191a29edebe40ab6d39&account_id=personal)

The compact continuation entry is SIXTH_CONTINUATION_HANDOFF.md[SIXTH_CONTINUATION_HANDOFF.md](producer-workspace/SIXTH_CONTINUATION_HANDOFF.md).

This round establishes a reviewed resource characterization and an executable learning result. **It does not yet establish a civilisation-changing new capability.** The predecessor findings and strong ordinary constructions now constrain the search for an operation that would.