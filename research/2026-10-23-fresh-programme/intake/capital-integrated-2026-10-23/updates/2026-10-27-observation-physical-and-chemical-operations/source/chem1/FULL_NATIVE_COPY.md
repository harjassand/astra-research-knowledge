## Astra Chemistry — A stronger benchmark changes the research target

A significant correction emerged from the literature review: autonomous, DNA-programmed formation of non-DNA polymers has already been demonstrated.

Meng and colleagues published An autonomous molecular assembler for programmable chemical synthesis in Nature Chemistry in 2016. Their DNA machinery autonomously produced oligomers with programmed olefin or peptide bonds and recorded the synthesis sequence in DNA. An earlier DNA walker demonstrated autonomous multistep amine acylation in a shared solution.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

Nature Chemistry

+1



Astra therefore cannot claim novelty merely by making a DNA-directed chemical assembler, a moving molecular instruction, or an autonomous sequence of peptide-forming reactions.

The distinctive unresolved capability is narrower and more demanding:

Multiple independently programmed products should advance only after the required permanent bond forms, remain at their current instruction after a harmless missed reaction, and continue correctly under common reagents without requiring individual observation.

The existing delayed-contact NCL construction remains a candidate, but it must outperform these established mechanisms on that exact capability—not just produce another programmed oligomer.

### New result: slow chemical intermediates can defeat an otherwise reliable instruction gate

The 2016 assembler paper identifies precisely the failure Astra is trying to overcome: its DNA machinery can progress before the intended covalent reaction finishes. The authors observed truncated products and identified premature DNA progression or reagent degradation as possible causes. Their mechanism did not require the DNA step to wait for the corresponding bond.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://users.ox.ac.uk\&sz=32)

users.ox.ac.uk



I tested whether Astra's chemical-cleanup interval could supply that missing qualification.

Suppose a donor pulse produces a correct amide with probability \\(p\\), a temporary thioester with probability \\(z\\), and an irreversible wrong product with probability \\(w\\). Let the thioester's total resolution rate vary across molecules, denoted \\(\Lambda\\).

After a chemical chase of duration \\(t\\), the unresolved fraction of the temporary intermediates is

\\[ S_T(t)=\mathbb E[e^{-\Lambda t}]. \\]

A controller that opens the next instruction while those intermediates remain covalently attached can mistake them for completed bonds.

The crucial result is

\\[ \boxed{ \mathbb E[e^{-\Lambda t}] \ge e^{-\mathbb E[\Lambda]t}. } \\]

Thus replacing heterogeneous reaction rates with their average systematically understates the number of unresolved intermediates. This follows from Jensen's inequality; it is an established mathematical principle applied here to the relay.

If just a fraction \\(f\\) of thioesters have resolution rates no greater than \\(\lambda_s\\), then

\\[ \boxed{S_T(t)\ge f e^{-\lambda_s t}.} \\]

Even a small slow-reacting fraction can determine long-programme reliability.

This matters chemically because measured NCL rearrangement kinetics are sensitive to junction structure, including steric hindrance. No evidence yet establishes a uniform lower bound on all relevant resolution rates in Astra's proposed chemistry.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubs.acs.org\&sz=32)

ACS Publications



### Exact feasibility obstruction

Assume identical independent incorporation stages, no recovery after a false instruction advance, and an irreversible whole-product damage rate \\(d\\) throughout every wash.

For a target probability \\(F_L\ge1-\epsilon\\) across \\(L\\) additions, define

\\[ \theta_L=(1-\epsilon)^{-1/L}-1. \\]

Two necessary conditions emerge:

\\[ \boxed{ t\ge \frac1{\lambda_s} \log\frac{zf}{(p+z)\theta_L} } \\]

when the logarithm is positive, and

\\[ \boxed{ t\le \frac{-\log(1-\epsilon)}{Ld}. } \\]

The first requires enough time to eliminate misleading temporary bonds. The second limits how long the entire product can survive repeated processing.

If the lower bound exceeds the upper bound, no fixed chemical-chase duration can satisfy the desired reliability within this model, even with perfect DNA address recognition.

For example, with explicitly hypothetical \\(p=0.6\\), \\(z=0.004\\), a 10% slow-intermediate fraction, \\(\lambda_s=10^{-4}\\,\mathrm{s}^{-1}\\), and \\(d=3\times10^{-8}\\,\mathrm{s}^{-1}\\):

| 1,024-addition target, 95% fidelity                    | Required duration |
| ------------------------------------------------------ | ----------------- |
| Minimum chase to control unresolved slow intermediates | 7.17 hours        |
| Maximum chase allowed by product aging                 | 27.8 minutes      |

The two requirements are incompatible. A separate exact renewal-model optimization, including both fast and slow intermediate populations, gave a maximum correct-completion probability of approximately 51.65% for this hypothetical 1,024-step system.

This is a conditional obstruction, not a finding that real NCL chemistry necessarily has such a slow fraction.

### A viable conditional repair requires two coupled operations

I extended the model to distinguish a chemically released donor that remains PNA-bound from one that has physically escaped.

The reaction sequence is

\\[ T \xrightarrow{r} H \xrightleftharpoons[b]{u} U \xrightarrow{c} E, \\]

where \\(T\\) is the temporary thioester, \\(H\\) is a released but hybridized donor, \\(U\\) is an undocked donor, and \\(E\\) is the recovered parent. Competing \\(T\to P\\) forms a permanent amide, and \\(H\to T\\) represents re-acylation.

I evaluated the complete continuous-time Markov chain, including a hypothetical 10% slow-intermediate subpopulation.

Illustrative 1,024-addition completion, with rapid re-acylation

| Cleanup intervention                        | Maximum modeled correctness |
| ------------------------------------------- | --------------------------- |
| Neither intervention                        | 45.86%                      |
| Faster chemical exchange alone              | 65.59%                      |
| Faster PNA displacement alone               | 49.67%                      |
| Exchange and moderate displacement          | 90.85%                      |
| Stronger exchange and moderate displacement | 98.31%                      |

All values are optimized over cleanup duration. The baseline re-acylation rate is \\(1\\,\mathrm{s}^{-1}\\); the moderate displacement increment is \\(0.3\\,\mathrm{s}^{-1}\\), while the two chemical-exchange increments are \\(0.01\\) and \\(0.1\\,\mathrm{s}^{-1}\\). These are hypothetical effective rates, not measured reagent performances.

The key finding is that accelerating thioester exchange without removing the hybridized donor can leave the molecular parent trapped in repeated re-acylation.

I also compared simultaneous versus sequential use of the two cleanup operations with equal total modeled reagent exposure. At a 300-second total chase and the high-re-acylation benchmark:

| Protocol                                 | Correct completion |
| ---------------------------------------- | ------------------ |
| Exchange and displacement simultaneously | 98.23%             |
| Exchange first, displacement second      | 70.59%             |
| Displacement first, exchange second      | 68.95%             |

This large difference follows from reaction ordering: displacement cannot remove a donor while it is covalently connected through the thioester, and a chemically freed donor can reattach before a later displacement phase.

The model passed independent matrix-exponential and numerical differential-equation checks. Experimentally, PNA–DNA displacement rates can be tuned by toehold geometry and sequence, but the published measurements do not establish these hypothetical rates under compatible NCL conditions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

PMC



### The integrated model reveals a second blocker: donor removal can erase molecular position memory

The preceding calculation treated strand displacement as helpful to donor clearance. But product-attached PNA handles may also be displaced, potentially destroying the correct growth register.

I therefore combined the chemical reaction network with explicit docking states for every one of the newest product-attached anchors. Successful incorporation introduces a new anchor; failed incorporation preserves the existing docking configuration. No controller is allowed to restore all anchors automatically.

Let \\(\gamma\\) denote the fraction of the additional donor-displacement rate that also affects product-attached anchors.

Correct 1,024-addition completion, 300-second shared washes

| Recent product anchors | No displacement spillover | 1% spillover | 5% spillover |
| ---------------------- | ------------------------- | ------------ | ------------ |
| 4                      | 22.90%                    | 11.97%       | 0.098%       |
| 5                      | 93.15%                    | 90.29%       | 67.58%       |
| 6                      | 98.05%                    | 97.92%       | 96.35%       |

Under the same hypothetical chemistry, five anchors cannot reach 95% at this wash duration even with perfectly selective donor displacement. Six anchors provide greater tolerance.

With six anchors, the exact joint model requires \\(\gamma\\) below approximately 6.50% to achieve 95% correct completion at 300 seconds.

This is a rate-selectivity requirement for the specified model, not proof that a reagent can achieve it. Product rebinding, donor escape and chemical resolution were all represented explicitly.

A second finding is that the previously chosen wash duration is not optimal after these mechanisms are combined. For six anchors with 5% displacement spillover, a 250-second wash produces approximately 96.74% correct completion, compared with 96.35% at 300 seconds.

The significant architectural lesson is that the donor-removal mechanism and the product-positioning mechanism cannot be designed independently. They exploit related PNA–DNA interactions and can undermine one another.

### Final constraint: premature instruction activation

Even the favourable six-anchor result excludes a separate failure: an unincorporated donor might expose its secondary DNA contact before the chemical cleanup is complete.

Suppose a missed reaction can create such a premature contact with probability \\(\phi\\), and that contact causes irreversible false advancement with conditional probability \\(g\\).

An optimistic bound on correct completion is

\\[ F_L\le \left(\frac{p+z}{p+z+q\phi g}\right)^L, \\]

where \\(q=1-p-z-w\\) is the harmless-miss probability before considering premature activation.

For the hypothetical parameters above, retaining at least 95% correctness imposes:

| Programme       | Maximum \\(\phi g\\)    |
| --------------- | ----------------------- |
| 64 additions    | \\(1.22\times10^{-3}\\) |
| 1,024 additions | \\(7.64\times10^{-5}\\) |

These are necessary, not sufficient, conditions. They optimistically treat every temporary thioester as eventually forming the correct amide, so they do not double-count the chemical-chase failures already modeled.

### Construction selected

The strongest surviving candidate is a modular NCL relay with a protected successor terminus, a delayed secondary DNA contact, simultaneous chemical exchange and donor displacement, and a small rolling set of product-attached anchors.

The new calculations identify three operations that must work together: resolving temporary thioesters, physically clearing failed donors, and preserving product positioning. Improving one while neglecting another can reduce overall reliability.

The most demanding comparator is CAPTN, which has already demonstrated traceless, selectively activated multisegment peptide synthesis, including ribosomal proteins S16 and S17. Astra's additional capability would be independent, retryable progression by differently programmed molecules under shared operations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://onlinelibrary.wiley.com\&sz=32)

Wiley Online Library



The decisive unresolved chemistry is whether a donor can be cleared aggressively while its correctly incorporated successor retains local registration, without a temporary thioester or incorrect permanent bond triggering advancement.

I preserved the mathematical derivations and executable models:

- Integrated scientific derivations and decisive failure cases
- Slow-intermediate survival and cleanup-window model
- Coupled NCL exchange, re-acylation and donor escape
- Exact joint model of chemistry and rolling product anchors

The substantive advance is an integrated feasibility criterion, with independently checked numerical models and a concrete counterexample to optimizing chemical cleanup in isolation. The best next physical target remains a two-programme, two-addition demonstration, deliberately including a stalled parent and a temporary-thioester control. The mathematics does not yet establish an integrated molecular manufacturing capability.