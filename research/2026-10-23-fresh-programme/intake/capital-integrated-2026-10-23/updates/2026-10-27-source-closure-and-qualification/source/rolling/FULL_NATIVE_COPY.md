## Astra Chemistry — A hidden failure in the previous construction

The previous locally reanchoring NCL relay has an important inconsistency.

It assumes that product-attached PNA handles maintain a local growth frontier, but its cleanup procedure also calls for denaturing the PNA–DNA hybrids to remove unreacted donors.

A fully denaturing wash removes the DNA-bound state of both free donors and product-attached handles. Covalent attachment preserves the product's handles, but does not preserve their positions on the template.

Consequently, the earlier constant-reaction-rate model is justified only after demonstrating that the product can regain its correct local register sufficiently quickly. Covalent retention alone is insufficient.

The distinction suggests a better operation: remove untethered donors through dissociation and physical escape, while allowing product-attached handles to dissociate and rapidly rebind locally. The two populations can have identical recognition sequences; their different covalent topology creates the potential separation mechanism.

This does not require a new bond sensor, but it does require a quantitatively adequate difference between free-donor escape and rooted-handle recovery.

### 1. Exact recovery mechanism: a small rolling set of anchors

I modeled the most recent \\(m\\) product-attached PNA handles as reversible molecular anchors. Each docked handle detaches at rate \\(u\\); each detached handle can rebind at rate \\(v\\), provided at least one other local anchor remains correctly registered.

Losing the final anchor destroys the fast local register, though the chemically intact peptide may still recover by slower rehybridization from the root.

In parallel, an unreacted donor can detach from DNA and escape into the flowing wash solution. Unlike the product-attached handle, an escaped donor has no covalent path back to its original rooted molecule.

The resulting finite-state model gives the probability of maintaining local registration throughout cleanup, followed by restoration of the complete local anchor set.

Illustrative 1,024-cycle relay, 10 bound donor molecules to clear per cycle

Assumed rates: PNA detachment 0.03 s⁻¹ for both product and donor; local product rebinding 1 s⁻¹; free-donor rebinding 0.03 s⁻¹; physical donor escape 1 s⁻¹. No irreversible product aging in this comparison.

| Recent product anchors | Best calculated full-programme probability |
| ---------------------- | ------------------------------------------ |
| 1                      | Effectively zero                           |
| 3                      | Effectively zero                           |
| 4                      | 28.4%                                      |
| 5                      | 94.4%                                      |
| 6                      | 99.75%                                     |
| 7                      | 99.99%                                     |

The probabilities require every specified free donor to escape and the product to retain or recover its fast local registration during all 1,024 cycles. They exclude bond-formation errors, incorrect addresses and subsequent chemical processing.

This is a meaningful conditional advance over demanding that every historical tag remain bound. A small overlapping set of recent anchors can act as a renewable molecular position memory without permanently locking thousands of old addresses.

The model passed 250 independent donor-escape formula comparisons, 720 first-passage recurrence checks, and 60,000 stochastic wash-and-recovery trajectories.

### 2. Correcting the model for missed reactions changes the engineering target

The open-loop model carries the actual docking state forward without waiting for a perfect reattachment signal. It also allows each donor pulse to produce correct incorporation with probability \\(p\\), permanent wrong chemistry with probability \\(w\\), or harmless nonprogress.

If \\(P\\) is the transient transition matrix for a shared wash, \\(S\\) is the operation that introduces a new product-attached anchor after successful incorporation, and \\(g\\) is the probability of clearing the free donors, then the exact matrix for reaching the next correct addition after any number of missed pulses is

\\[ \boxed{ H=[I-(1-p-w)gP]^{-1}pgPS. } \\]

For \\(L\\) additions, the probability of completing the correct chemical sequence while retaining fast local registration and satisfying the modeled cleanup requirements is obtained from \\(H^L\\).

This removes the previous assumption of a perfect controller that waits for all anchors to dock. I checked the recurrence against scalar renewal solutions and independent no-miss transition calculations.

With hypothetical \\(p=0.6\\), \\(w=10^{-6}\\), ten initially bound donors per wash, six recent product anchors, and the rate parameters above:

| Product damage rate during washing | Conditional completion of 1,024 correct additions |
| ---------------------------------- | ------------------------------------------------- |
| 0 s⁻¹                              | 99.10%                                            |
| \\(10^{-8}\\) s⁻¹                  | 98.22%                                            |
| \\(3\times10^{-8}\\) s⁻¹           | 96.47%                                            |
| \\(5\times10^{-8}\\) s⁻¹           | 94.76%                                            |

These entries use a fixed 525-second wash after each pulse, including missed pulses. They are not experimental yields. They exclude address misregistration and any molecular damage outside washing.

The cost remains substantial: at 60% mean incorporation probability, a 1,024-addition lineage needs approximately 1,707 pulses in the absence of failures. At 525 seconds of washing per pulse, that is about 249 hours of washing alone, before counting coupling, deprotection, fragment preparation or final tag removal.

Thus the mathematical viability of a long relay does not yet imply a useful manufacturing process.

## 3. A stronger obstruction: accumulated handle damage

The next calculation changes the long-chain assessment.

Even if only six recent PNA handles are required for accurate positioning, a 1,024-addition product may still retain 1,024 chemically attached handles until final cleanup.

Suppose each retained handle has an independent irreversible damage hazard \\(h\\) that permanently damages the intended peptide. At stage \\(j\\), there are \\(j\\) handles exposed during every pulse, including unsuccessful pulses.

With correct incorporation probability \\(p\\), irreversible wrong chemistry \\(w\\), and pulse duration \\(t\\), the exact probability of completing all \\(L\\) stages without this damage is

\\[ \boxed{ F_L=\prod\_{j=1}^{L} \frac{p e^{-jht}} {1-(1-p-w)e^{-jht}}. } \\]

For negligible \\(w\\) and small \\(h\\),

\\[ -\log F_L\approx \frac{ht}{2p}L(L+1). \\]

The accumulated exposure is quadratic in programme length.

Maximum per-handle fatal damage rate compatible with 95% survival

Hypothetical \\(p=0.6\\), 525-second processing intervals; this failure mechanism alone.

| Number of additions | Maximum \\(h\\)                           |
| ------------------- | ----------------------------------------- |
| 16                  | \\(4.31\times10^{-7}\ \mathrm{s}^{-1}\\)  |
| 64                  | \\(2.82\times10^{-8}\ \mathrm{s}^{-1}\\)  |
| 1,024               | \\(1.12\times10^{-10}\ \mathrm{s}^{-1}\\) |

I combined this hazard with the exact open-loop anchoring and retry model. For 1,024 additions, six recent anchors, product damage rate \\(3\times10^{-8}\\,\mathrm{s}^{-1}\\), and all previous illustrative parameters, preserving at least 95% correctness requires

\\[ \boxed{h\leq3.35\times10^{-11}\ \mathrm{s}^{-1}.} \\]

This is a severe conditional constraint.

There is an important distinction: damage to a disposable PNA tag need not damage the final peptide. If old tags can degrade or detach tracelessly, the quadratic bound does not apply to those harmless events. An operation that removes obsolete tags while preserving the small set of active frontier anchors could therefore be exceptionally valuable. None of the previously examined address erasers has yet established that operation.

## 4. Combining errors exposes another failure

Using the previously derived \\(r^{-3/2}\\) positional-interference model, with nearest off-target reaction ratio \\(10^{-5}\\), gives approximately 97.48% correctness over 1,024 additions from that error source alone.

But the latest wash-and-retry construction achieves only 96.47% under the specified nonzero product-aging parameters.

Combining the two independent modeled hazards gives

\\[ 0.96472\times0.97484\approx\boxed{94.04\\%}. \\]

Both mechanisms individually clear 95%. Together, they do not.

To obtain 95% combined correctness with six recent anchors, the nearest-site incorrect-to-correct hazard ratio must fall below approximately

\\[ \boxed{6.03\times10^{-6}}, \\]

before charging any irreversible handle damage.

There is also an upper bound independent of anchor redundancy: with \\(p=0.6\\), \\(w=10^{-6}\\), ten bound donors requiring clearance per pulse and the chosen escape rates, a uniform product-aging hazard above approximately \\(5.10\times10^{-8}\\,\mathrm{s}^{-1}\\) prevents 95% eventual completion in this entire wash-and-retry model, even with perfect product reanchoring.

## 5. Mechanism choice

The strongest surviving candidate is a rolling-avidity peptide relay.

A free donor initially has a single PNA recognition contact. Correct NCL incorporation covalently connects that donor's handle to a product already carrying neighbouring handles. The product can consequently gain multivalent local rebinding, while an unincorporated donor eventually dissociates and escapes during a mild wash.

This makes molecular topology perform a useful sorting function. It is closer to a physically specified operation than an assumed perfect bond sensor.

However, temporary NCL thioesters can also produce transient multivalent connections. They must be chemically resolved before the next reactive terminus is exposed. Wrong stable amides are not rejected by this mechanism.

The chemical components have genuine experimental precedents: PNA-directed NCL with removable handles, CAPTN's selectively activated peptide joining, and DNA strand-displacement schemes that reduce product inhibition. Their integration into this independently progressing relay remains untested.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubmed.ncbi.nlm.nih.gov\&sz=32)

pubmed.ncbi.nlm.nih.gov

+3



The strongest practical alternative remains externally staged peptide assembly using established NCL chemistry. Astra's design would need to demonstrate an advantage in asynchronous recovery, programme multiplexing or synthetic scope after including all reagent, linker, template, purification and recovery costs.

The immediate target should be a two-programme relay with two to four peptide modules, not an assumed 1,024-step assembler. It should show that chemically completed products acquire stronger recoverable template association than free donors, that temporary thioesters do not produce false advancement, and that deliberately stalled molecules preserve their original donor identity. Shorter modular programmes have a much less severe cumulative-damage burden.

The derivations and executable work are preserved:

- Full scientific analysis and counterexamples
- Donor clearance and multivalent reanchoring
- Exact open-loop asynchronous retry model
- Full-denaturation and root-to-tip rehybridization comparator
- Cumulative handle aging and combined fidelity model

The computational checks passed. The substantive new result is a conditional mechanism for distinguishing product-attached and free molecular instructions through kinetic recapture, together with explicit scaling limits showing where it fails. No integrated chemical capability or verified discovery of a new physical principle has yet been established.