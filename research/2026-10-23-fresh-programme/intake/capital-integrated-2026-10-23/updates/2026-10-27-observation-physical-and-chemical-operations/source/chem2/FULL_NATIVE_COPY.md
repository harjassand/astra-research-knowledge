## Astra Chemistry — A missing failure pathway in the current relay

I reproduced the previous six-anchor reaction-and-wash model, including its reported 96.35% conditional completion probability for 1,024 additions with 5% displacement spillover.

The next attack identifies a potentially important omission: the model allows an unreacted donor to remain chemically active during washing, but does not allow that donor to form a new irreversible wrong bond during that interval.

This matters because native chemical ligation is not stopped merely by beginning a wash. Reactive peptide thioesters can continue participating in exchange reactions, including reactions involving internal cysteine residues. A 2025 study of NCL catalysts explicitly identifies branched thioesters on internal cysteines as competing products and investigates their reversal.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

PMC



Thus donor disappearance and chemical harmlessness are separate properties. The existing 96.35% result is valid for its stated model but cannot be interpreted as the fidelity of an integrated peptide assembler unless reactions occurring during donor clearance are also charged.

### Exact result: how much incorrect chemistry can occur during donor clearance?

I added irreversible wrong-bond transitions to the existing chemical-and-anchor reaction network. The extended model retains the same retry dynamics and actual anchor-docking states; it does not reset stalled molecules to a favourable configuration.

For the previous hypothetical six-anchor benchmark, with 5% displacement spillover and 250-second washes:

| Wrong-bond hazard while donor is bound | Correct completion of 1,024 additions |
| -------------------------------------- | ------------------------------------- |
| Zero (previous model)                  | 96.74%                                |
| \\(1\times10^{-6}\ \mathrm{s}^{-1}\\)  | 96.53%                                |
| \\(3\times10^{-6}\ \mathrm{s}^{-1}\\)  | 96.12%                                |
| \\(5\times10^{-6}\ \mathrm{s}^{-1}\\)  | 95.71%                                |
| \\(1\times10^{-5}\ \mathrm{s}^{-1}\\)  | 94.70%                                |
| \\(3\times10^{-5}\ \mathrm{s}^{-1}\\)  | 90.75%                                |

The exact 95% threshold in this model is

\\[ \boxed{x\_{\mathrm{bound}}\leq8.51\times10^{-6}\ \mathrm{s}^{-1}.} \\]

For a 64-addition programme with otherwise identical parameters, the threshold is approximately \\(3.70\times10^{-4}\\,\mathrm{s}^{-1}\\)—over 40 times less restrictive.

This is a direct argument for modular assembly. Short programmes are not merely easier to complete; they can tolerate substantially more residual chemistry during a shared wash.

The extended model passed 300 independent absorbing-Markov-chain tests and reproduced the previous reaction model exactly when the new wrong-bond hazards were set to zero.

## A stronger alternative: proofread donors before forming the permanent bond

The published kinetic-proofreading literature offers a different intervention. Mukherjee and colleagues demonstrated fuel-driven DNA strand-displacement proofreading that improves molecular recognition during templated dimerization. Aoyanagi and colleagues subsequently demonstrated inherited proofreading in DNA ligation-based information replication. Neither establishes peptide-NCL proofreading, but both provide stronger physical precedent than a hypothetical DNA sensor for a completed peptide amide.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubs.acs.org\&sz=32)

ACS Publications

+1



The proposed change is to keep incoming peptide donors chemically latent during DNA-based proofreading, discard incorrectly recognized donors, and activate the retained donors only after proofreading and cleanup.

I derived the fidelity–resource trade-off for \\(n\\) recognition rounds:

\\[ P_n= \left[ \frac{p\\,s_C^n} {p\\,s_C^n+w\\,s_W^n+\delta} \right]^L, \\]

where \\(s_C\\) and \\(s_W\\) are the correct- and wrong-donor survival probabilities per round, \\(w\\) is the initial wrong-reaction probability, and \\(\delta\\) is irreversible parent damage per attempt.

An illustrative model with \\(p=0.6\\), \\(w=0.001\\), \\(s_C=0.8\\), \\(s_W=0.1\\), and \\(\delta=10^{-5}\\) gives:

| Proofreading rounds | Correct 1,024-step completion | Mean attempts per step |
| ------------------- | ----------------------------- | ---------------------- |
| 0                   | 17.87%                        | 1.66                   |
| 1                   | 79.09%                        | 2.08                   |
| 2                   | 94.81%                        | 2.60                   |
| 3                   | 96.40%                        | 3.26                   |
| 4                   | 95.88%                        | 4.07                   |
| 5                   | 94.92%                        | 5.09                   |

The optimum is finite. Too little proofreading permits wrong permanent bonds; too much proofreading discards correct donors, increasing exposure to damage.

For constant per-attempt damage, the continuous optimum is exactly

\\[ \boxed{ n^\*= \max\left\\{0, \frac{\ln\\!\left[ \frac{\delta\ln(1/s_C)} {w\ln(s_C/s_W)} \right]} {\ln s_W} \right\\}. } \\]

For this example, \\(n^\*=2.969\\), so three integer rounds are optimal. I verified the optimum against 1,000 randomized parameter sets.

This is a conditional mathematical improvement, not an experimental peptide-yield prediction. The published DNA proofreader does not establish the assumed eightfold per-round discrimination for Astra's peptide donors.

### The decisive constraint: the wrong donor must not react before proofreading ends

The pre-commit approach only works if incorrect donors remain chemically inactive until they have passed recognition.

I extended the model to allow a wrong donor to form an irreversible bond prematurely during each proofreading round.

For the three-round, 1,024-addition example:

| Assumption                                             | Maximum premature wrong-bond probability per round for 95% completion |
| ------------------------------------------------------ | --------------------------------------------------------------------- |
| Fixed damage \\(10^{-5}\\) per attempt                 | 0.397%                                                                |
| Additional damage \\(10^{-6}\\) per proofreading round | 0.125%                                                                |

If each round lasts 60 seconds, the second case requires a premature wrong-bond hazard below approximately

\\[ \boxed{2.09\times10^{-5}\ \mathrm{s}^{-1}.} \\]

A hypothetical unprotected reaction occurring at \\(0.0016\\,\mathrm{s}^{-1}\\) would produce a 9.15% probability of reacting within 60 seconds, far outside this limit.

This is why true chemical latency is indispensable. DNA proofreading alone cannot prevent a wrong covalent bond that forms before the recognition process finishes.

### An impossibility result for downstream DNA-only correction

I also established a scoped limitation on all the earlier product-address controllers.

Suppose a correct native amide and an incorrect stable attachment have identical DNA/PNA recognition structures and undergo identical future DNA-controller transitions. Any subsequent DNA-only selection procedure must accept them with identical probabilities. Consequently, it cannot improve their relative chemical correctness.

For initial correct and incorrect irreversible probabilities \\(p\\) and \\(w\\), final fidelity therefore cannot exceed

\\[ \left(\frac{p}{p+w}\right)^L \\]

under those indistinguishability assumptions, however sophisticated the downstream DNA motor becomes.

This does not rule out chemically selective verification. It shows why another DNA latch, fuel cycle or address-cleavage operation cannot universally repair incorrect stable peptide bonds.

## Strongest construction after comparison

I now favour pre-commit chemical proofreading as the higher-upside research direction, alongside the simpler protected-terminus relay as its experimental comparator.

The candidate uses a chemically latent peptide donor, fuel-driven DNA rejection of incorrect candidates, shared activation of retained donors, NCL, simultaneous chemical exchange and physical donor clearance, and a protected successor terminus. Its distinctive goal remains independent progression after successful chemistry, including recovery from missed reactions.

CAPTN demonstrates relevant thioester activation and multisegment peptide synthesis, while nonenzymatic DNA kinetic proofreading is experimentally established. Their integration, particularly chemical latency under shared proofreading conditions, is not.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

PMC

+1



The most important next discriminator is not another 1,024-step simulation. It is a two-programme chemical system showing that mismatched donors can be rejected while rooted parents remain competent, before any irreversible wrong amide forms, followed by independently correct advancement under the same shared reagents.

The research is preserved in the following executable files and derivations:

- Complete scientific derivations and mechanism comparison
- Wrong-bond chemistry during washing
- Chemical quenching and physical escape model
- Independent quenching-model verification
- Optimal pre-commit proofreading
- Premature-reaction counterexample

The calculations passed their reported independent numerical and finite-state checks. The new result is a sharper separation between two fundamental requirements: preventing active-donor errors during cleanup and rejecting chemically wrong candidates before irreversible commitment. Neither requirement is yet experimentally satisfied by an integrated Astra assembler.