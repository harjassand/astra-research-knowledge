## Astra Chemistry — A more consequential constraint on pre-commit proofreading

The previous model treated each proofreading round as an irreversible rejection of incorrect donors. That assumption needs to be made physical.

Mukherjee and colleagues' 2024 DNA proofreading system uses a fuel-driven pathway that converts rejected monomers into waste while returning the template to a usable state. It is not merely a reversible DNA binding-and-unbinding cycle.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubs.acs.org\&sz=32)

ACS Publications



This distinction is essential for Astra.

If a rejected wrong donor remains chemically competent and can repeatedly rebind, rejection may only delay its eventual incorporation. In a finite-state system with a nonzero chance of reaching the reactive state on each attempt, indefinitely repeated attempts eventually reach that state with probability one, unless the donor can be irreversibly removed, neutralized or destroyed first.

The leading mechanism therefore needs a physical wrong-donor sink, not only improved DNA recognition.

There is a useful chemical starting point: CAPTN demonstrated selective activation of latent peptide-thioester precursors. In particular, its Nbz and hydrazide precursor strategies permit different peptide segments to be activated in stages. But CAPTN required controlled reagent and pH changes, and did not demonstrate fuel-driven selective activation of different donors sharing one bath.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

PMC



The unresolved construction becomes more specific: can DNA proofreading irreversibly reject the wrong peptide donor while leaving the rooted parent competent, and can the retained correct donor subsequently be activated without also activating the rejected material?

### New mathematical result: when a passive wash can outperform kinetic proofreading

I derived a useful mechanism-selection theorem.

Suppose correct and incorrect donors differ only in their dissociation rates, \\(k_C\\) and \\(k_W\\), with \\(k_W>k_C\\). A detached donor is permanently removed. A proposed multistep proofreader requires a random completion time \\(T\\), independent of donor identity, before admitting a still-bound donor.

Its survival probabilities are

\\[ s_C=\mathbb E[e^{-k_CT}],\qquad s_W=\mathbb E[e^{-k_WT}]. \\]

Writing \\(r=k_W/k_C>1\\), Jensen's inequality gives

\\[ \boxed{s_W\ge s_C^r.} \\]

Equality is attained by a fixed-duration wash.

Therefore, at the same correct-donor retention, a deterministic waiting interval rejects at least as many mismatched donors as a proofreader whose only discrimination comes from surviving a random number of waiting periods.

For illustration, let \\(k_C=0.001\\,\mathrm{s}^{-1}\\), \\(k_W=0.03\\,\mathrm{s}^{-1}\\), and require three exponential gate transitions at rate \\(0.01\\,\mathrm{s}^{-1}\\):

| Recognition method      | Correct retention | Wrong retention |
| ----------------------- | ----------------- | --------------- |
| Three exponential gates | 75.13%            | 1.5625%         |
| Fixed 285.9-second wash | 75.13%            | 0.01882%        |

The fixed wash rejects approximately 83 times more wrong donors at identical correct retention.

This theorem does not refute the experimentally demonstrated DNA proofreading mechanism. Real fuel-driven proofreading can introduce additional chemically distinct discard pathways; the theorem concerns only mechanisms differing through constant dissociation rates and a donor-independent waiting-time distribution. It also does not account for throughput or energy costs.

Its consequence for Astra is that a complicated fuel-powered controller must demonstrate an advantage beyond the simpler alternative of chemically latent donors, differential DNA dissociation and physical removal before activation.

### Physical donor escape substantially changes the conclusion

I extended the passive-wash model to distinguish three states:

\\[ \text{DNA-bound donor} \ \rightleftarrows\ \text{locally detached donor} \ \longrightarrow\ \text{physically escaped donor}. \\]

A locally detached donor can rebind before it leaves the reactor. At activation, I conservatively count an incorrect donor that is still locally present as potentially harmful, even if it is not currently hybridized.

Using hypothetical rates \\(k_C=0.001\\,\mathrm{s}^{-1}\\), \\(k_W=0.03\\,\mathrm{s}^{-1}\\), local rebinding \\(0.03\\,\mathrm{s}^{-1}\\), parent damage \\(3\times10^{-8}\\,\mathrm{s}^{-1}\\), initial correct-event weight \\(p=0.6\\), wrong-event weight \\(w=0.001\\), and other irreversible damage \\(10^{-5}\\) per attempt:

| Physical escape rate | Best 1,024-step correctness | Optimal latent wash |
| -------------------- | --------------------------- | ------------------- |
| 1.0 s⁻¹              | 96.21%                      | 221 seconds         |
| 0.1 s⁻¹              | 95.63%                      | 292 seconds         |
| 0.05 s⁻¹             | 94.88%                      | 380 seconds         |

The exact 95% threshold in this illustrative model is a physical escape rate of approximately \\(0.0543\\,\mathrm{s}^{-1}\\).

I independently checked the analytical bound/detached/escaped solution against matrix exponentiation and the complete stage recurrence.

There is an important assumption behind these favourable numbers: the initial \\(p/w=600\\) ratio already gives strong donor discrimination before the latent wash. It does not follow from the dissociation rates alone.

For example, with equal association rates and a simple equilibrium binding model, the chosen 30-fold dissociation-rate difference supplies only a 30:1 bound-occupancy ratio. Replacing \\(w=0.001\\) with \\(w=0.02\\), while holding the other hypothetical rates fixed, increases the physical escape rate needed for 95% completion to approximately \\(0.397\\,\mathrm{s}^{-1}\\).

This makes the actual competitive binding matrix essential evidence. Treating the initial wrong-donor fraction and mismatch dissociation rate as independently favourable assumptions would overstate the construction's feasibility.

## Further result: chemical waste and donor recycling can defeat proofreading

A rejected DNA duplex is not necessarily a chemically neutralized peptide.

Suppose a three-round proofreader retains correct donors with probability \\(s_C^3\\) and incorrect donors with probability \\(s_W^3\\). Let \\(\eta\\) be the probability that a rejected incorrect donor still creates a fatal bond following global chemical activation.

Then, under the independent-attempt renewal model,

\\[ \boxed{ F_L= \left[ \frac{p s_C^3} {p s_C^3+w\\{s_W^3+\eta(1-s_W^3)\\}+\delta} \right]^L. } \\]

For the previous hypothetical parameters \\(p=0.6,\ w=0.001,\ s_C=0.8,\ s_W=0.1,\ \delta=10^{-5}\\):

| Rejected wrong-donor chemical risk \\(\eta\\) | Correct 1,024-step completion |
| --------------------------------------------- | ----------------------------- |
| 0%                                            | 96.40%                        |
| 0.1%                                          | 96.08%                        |
| 0.4%                                          | 95.12%                        |
| 0.5%                                          | 94.81%                        |
| 1%                                            | 93.24%                        |

Achieving 95% requires \\(\eta\leq0.4393\\%\\) in this model. Additional DNA proofreading cannot necessarily correct this: it may reject more wrong donors while leaving a larger pool of chemically activatable waste.

### Exact recapture–leakage obstruction

There is also a more fundamental failure if rejected donors remain near their original rooted molecule.

Let a wrong donor attempt \\(n\\) proofreading transitions at rate \\(g\\). At every transition stage, it can dissociate at rate \\(k\\) or prematurely form a wrong permanent bond at rate \\(\ell\\). After dissociation, it returns to the same site with probability \\(r\\).

Write

\\[ s=\frac{g}{g+k+\ell}. \\]

The exact probability that this wrong donor eventually forms a permanent incorrect bond is

\\[ \boxed{ P\_{\rm wrong} = \frac{ s^n+\dfrac{\ell}{k+\ell}(1-s^n) }{ 1-r\dfrac{k}{k+\ell}(1-s^n) }. } \\]

As proofreading depth increases,

\\[ \boxed{ \lim\_{n\to\infty}P\_{\rm wrong} =\frac{\ell}{\ell+(1-r)k}. } \\]

For example, with hypothetical \\(g=0.01,\ k=0.09,\ \ell=10^{-5}\\,\mathrm{s}^{-1}\\), three proofreading stages give:

| Probability rejected donor returns | Eventual wrong-bond probability |
| ---------------------------------- | ------------------------------- |
| 0%                                 | 0.111%                          |
| 90%                                | 1.10%                           |
| 99%                                | 10.01%                          |
| 99.9%                              | 52.65%                          |

In the limiting case \\(r=1\\), with a nonzero premature-reaction rate, the eventual wrong-bond probability is one. The physical sink is indispensable in this model.

I checked this expression against independently constructed continuous-time Markov generators over 500 parameter sets.

## Another negative result: a shared activation clock eliminates the benefit of a mere waiting gate

If every peptide precursor is activated at the same global time \\(\tau\\), and a DNA gate independently admits fraction \\(G\\) of both correct and wrong donors without changing their chemistry or dissociation rates, then

\\[ C=pG e^{-k_C\tau},\qquad W=wG e^{-k_W\tau}. \\]

The ratio \\(W/C\\) is independent of \\(G\\). Such a gate does not improve selectivity; it merely discards some otherwise productive correct donors.

Under the hypothetical 1,024-step benchmark at \\(\tau=214.6\\) seconds, gate readiness \\(G=0.8\\) reduces correct completion from 96.26% to 95.42%, once irreversible parent damage is charged.

Thus a useful fuel-driven proofreader must do something more physically consequential than delaying activation: preferentially inactivate incorrect donors, change their binding or discard pathways, or produce a chemically meaningful retained state.

## Strongest construction selected

The leading lower-complexity mechanism is now latent-donor sorting before irreversible NCL chemistry:

1\. Present chemically latent peptide donors

Correct and incorrect precursors compete for the rooted molecule's current DNA/PNA recognition site

2\. Reject and physically remove mismatched donors

Use differential dissociation, adding fueled proofreading only if it demonstrably improves chemical rejection

3\. Activate retained precursors and ligate

Correct permanent amides acquire a protected successor terminus

4\. Resolve thioesters and clear remaining donors

Unsuccessful rooted parents retain their original competent terminus

The strongest experimental supports are CAPTN's staged latent peptide-thioester chemistry and the high sequence discrimination demonstrated for specially designed DNA-templated PNA ligation. Neither establishes the full independent-progression mechanism.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://onlinelibrary.wiley.com\&sz=32)

Wiley Online Library

+1



The crucial compatibility gap remains substantial. Established hydrazide activation can require acidic nitrite chemistry and subsequent thiolysis; the rooted terminal cysteine, DNA/PNA hybridization, reversible anchors and subsequent NCL must all survive the actual shared processing conditions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://academic.oup.com\&sz=32)

Oxford Academic

+1



The next discriminating construction is a two-programme, two-addition experiment comparing passive latent washing directly against fueled wrong-donor discard. It must distinguish a permanently incorrect amide from a temporary thioester, identify chemically active rejected precursors, and confirm that the deliberately stalled parent remains competent.

The longer 1,024-addition calculation remains a stress test, not a projected manufacturing capability: even the favourable passive-wash scenario entails approximately 130 hours of washing alone.

### Preserved executable research

The work is saved and verified in the current environment:

- Full derivations, chemical assumptions and scoped counterexamples
- Executable latent-donor sorting, proofreading, recycling and Markov models
- Reproduced numerical results and checks

The tests include 800 independent wash-generator comparisons, 500 gate-generator inversions, 300 stage-network comparisons, 200 Jensen-inequality cases, and 300 common-clock gate checks.

Research conclusion: The strongest gain is a simpler physical and mathematical criterion for deciding when molecular proofreading is worth its cost. A chemically latent precursor plus a selective, irreversible disposal pathway may be more useful than another DNA controller. The central unresolved operation is making that disposal pathway compatible with correct peptide-bond formation and genuinely independent molecular retry.