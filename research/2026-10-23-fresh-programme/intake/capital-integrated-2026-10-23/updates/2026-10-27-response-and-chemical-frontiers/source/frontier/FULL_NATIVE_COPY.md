## Astra Chemistry — New obstruction: authenticating a donor is not the same as selecting the current instruction

The previous two-key PNA model assumes that candidate donors compete for one active recognition site. Its favourable long-programme calculations are valid under that assumption, but they do not establish that a long DNA template exposes only one site to donor binding.

If downstream addresses can also bind their matching donors, those donors may survive the same wash and become chemically active before the growing peptide reaches them.

This is a fundamental distinction:

- Identity authentication: Is this donor correctly matched to this DNA address?
- Instruction authentication: Is this address the next one the growing molecule must execute?

A donor can pass the first test and fail the second.

The experimental comparator is substantial. Meng and colleagues' autonomous DNA assembler already demonstrated programmed covalent synthesis, while the later mechanism proposed by Bath and Turberfield explicitly addresses chemical-reaction-dependent instruction progression. Neither establishes the independent, retryable peptide synthesis operation sought here.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

Nature Chemistry+1



The new target is therefore to make donor authentication depend jointly on its DNA address and the position of the chemically growing product, without allowing that recognition event itself to count as a successful peptide bond.

## Exact result: future-address exposure creates a quadratic burden

I extended the previous donor-loading model to include every unused downstream address and all retries after missed incorporation.

Let \\(q\\) be the probability an unused address retains an activatable donor after washing, and \\(\chi\\) the probability that such a retained donor causes a fatal incorrect reaction during one activation pulse. Suppose the current intended reaction succeeds with probability \\(p\\), makes an irreversible wrong bond with probability \\(w\\), and the parent suffers independent damage with probability \\(\delta\\).

For \\(L\\) required incorporations, the exact eventual all-correct probability is

\\[ \boxed{ F_L=\prod\_{m=0}^{L-1} \frac{p(1-\delta)(1-q\chi)^m} {1-(1-p-w)(1-\delta)(1-q\chi)^m}. } \\]

Here \\(m\\) counts unused downstream addresses. This assumes fresh, independently loaded donors at each attempt, and treats off-site irreversible bonds as fatal.

In the low-error regime, the downstream contribution to the failure exponent is approximately

\\[ -\log F_L\big|\_{\mathrm{downstream}} \approx \frac{q\chi}{2p}L(L-1). \\]

Thus downstream donor authentication can create the same quadratic scaling problem previously found for obsolete upstream addresses. The important missing operation is restricting activation to the actual chemical growth frontier.

### Numerical comparison

Using the previous hypothetical PNA rates, 180-second donor loading and a 240-second wash:

Unused address with two DNA contacts

# 64.10%

Retained activatable donor

Unused address with one DNA contact

# 0.0463%

Retained activatable donor

Assuming \\(p=0.6\\), \\(w=10^{-6}\\), \\(\delta=10^{-5}\\) and \\(\chi=10^{-5}\\):

| Programme            | Two contacts at every future address | Second contact available only at frontier |
| -------------------- | ------------------------------------ | ----------------------------------------- |
| 4 incorporations     | 99.986%                              | 99.993%                                   |
| 64 incorporations    | 97.75%                               | 99.88%                                    |
| 1,024 incorporations | 0.367%                               | 97.74%                                    |

These are mathematical outcomes under the specified nonlocal side-reaction model, not chemical yields.

The full-stage calculation and an independently sampled 100,000-trajectory short-programme check agree.

This establishes a potentially valuable design target: a chemically growing terminus should determine where the second authentication contact is available. Adding more static DNA recognition sites alone does not supply that property.

## The strongest alternative survives under more realistic spatial assumptions

The dramatic difference above assumes each future donor has the same opportunity to cause a wrong reaction regardless of its distance from the active terminus.

I challenged that assumption by allowing incorrect chemistry to decline with distance \\(r\\) as \\(r^{-\alpha}\\).

Correct completion across 1,024 incorporations

| Spatial decay \\(\alpha\\) | Static two-key template | Frontier-scoped authentication |
| -------------------------- | ----------------------- | ------------------------------ |
| 0 — no decay               | 0.37%                   | 97.74%                         |
| 1                          | 91.39%                  | 98.14%                         |
| 1.5                        | 95.50%                  | 98.14%                         |
| 2                          | 96.40%                  | 98.14%                         |

All rates remain hypothetical.

At \\(\alpha=1.5\\), the extra controller's advantage disappears if it introduces an additional fatal failure probability of only approximately \\(1.59\times10^{-5}\\) per pulse.

This changes the mechanism decision. Frontier-scoped authentication is worth pursuing, but only if its extra chemical operations are exceptionally reliable.

## A generic terminal-cysteine key fails an important specificity test

One potential shortcut is to use reversible 2-formylphenylboronic-acid recognition of the N-terminal cysteine as the frontier-specific second key.

Such recognition is experimentally established. However, it binds the chemical functionality required for NCL, and its stable complexes can retain donors after their DNA contacts have dissociated.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

pmc.ncbi.nlm.nih.gov+1



An exact equilibrium calculation shows that a generic second key which binds correct and incorrect donors equally does not improve their relative recognition specificity.

Worse, a kinetic counterexample allows a mismatched donor with a DNA-arm dissociation rate ten times faster than the correct donor to remain bound almost as effectively through its terminal-cysteine contact.

| Hypothetical terminal-key release rate | Correct donor retained after 240 s | Wrong donor retained after 240 s |
| -------------------------------------- | ---------------------------------- | -------------------------------- |
| 0.0001 s⁻¹                             | 99.87%                             | 98.20%                           |
| 0.03 s⁻¹                               | 68.93%                             | 0.47%                            |

The wrong donor is assumed to have acquired both contacts initially; its formation probability must be measured separately.

Furthermore, releasing the terminal key before ligation creates another competition between NCL and donor departure. The exact first-passage model shows that slow ligation can lose most of the apparent benefit of the initial two-contact recognition.

I therefore reject a generic terminal-cysteine binder as the leading implementation of the second key.

## Strongest surviving molecular construction

Product-scoped recognition, chemical-bond-controlled progress

Current product carries recognition key \\(H_i\\)

A DNA address \\(A_i\\) and product-attached \\(H_i\\) jointly recruit the intended, chemically latent donor.

Native chemical ligation

The donor may form a permanent amide, a temporary thioester, or no bond. Recognition alone advances nothing.

Unconditional donor-contact disassembly

Chemical exchange and DNA displacement must clear unsuccessful donors while preserving permanent peptide products.

New chemically active frontier

A correct product carries \\(H\_{i+1}\\) near its protected successor terminus. A stalled parent keeps \\(H_i\\) and retries.

This construction does not require the DNA controller to diagnose a peptide bond directly. It uses temporary recognition to bring reactants together, then relies on their covalent chemical fate to determine what survives cleanup.

There is relevant experimental precedent for templated PNA-directed NCL and selective activation of peptide-thioester precursors. CAPTN has already demonstrated three-segment peptide assembly, and the newer traceless sortase-ligation system provides another substantial comparator. Neither establishes the proposed autonomous, independently retriable relay.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://onlinelibrary.wiley.com\&sz=32)

Wiley Online Library+2



The new quantitative constraint is that, in the illustrated 1,024-step model, no more than approximately 0.51% of unused downstream positions may prematurely acquire an effective second key, given the chosen incorrect-reaction and damage probabilities.

The deepest unresolved chemistry is still the simultaneous requirement to resolve temporary thioesters, remove noncovalently retained donors and preserve the product's correct next recognition position. Old product-associated recognition handles and incorrect permanent amides remain unsolved failure paths.

The appropriate physical discriminator is a short, mixed-programme system in which one molecule advances and another misses its reaction, followed by common cleanup and a second addition. Correct and incorrect amide junctions, thioesters, downstream donor occupancy and preserved stalled-parent competence must all be separately identified.

## Preserved scientific work

The derivations and executable calculations have been saved and checked:

- Complete scientific findings, proofs, physical assumptions and counterexamples
- Executable kinetic, spatial-interference and chemical-release model
- Numerical verification results

The checks include 100 independent kinetic ODE comparisons, 500 absorbing-chain inversions, 100 equilibrium-selectivity identities, 50 spatial-limit checks and 100,000 stochastic trajectories.

The substantive advance is the separation of donor identity from instruction identity, with an exact calculation showing why static two-key templates may fail at scale and why product-specific authentication could help. The proposed physical mechanism remains unbuilt, and no new general-purpose molecular manufacturing capability has yet been established.