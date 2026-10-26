## Astra Chemistry — A new way to control interference between independently progressing molecules

The strongest candidate remains a chemically self-indexed NCL relay with a protected successor terminus. Successful ligation creates the next growth terminus, initially protected; a failed reaction leaves the original terminus competent to retry. DNA/PNA recognition supplies programme identity.

I investigated a different way to reduce incorrect donor incorporation: control the order in which donor families are exposed, rather than introducing another DNA-cleavage controller.

This matters because irreversible wrong-site reactions cannot be repaired merely by improving the handling of temporary thioesters. Recent NCL studies confirm that reversible branched thioesters and permanent backbone amides must be distinguished experimentally.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubs.acs.org\&sz=32)

ACS Publications

+1



### New theorem: donor concentration tuning has a spectral selectivity limit

Suppose several differently programmed molecules are simultaneously ready for different donors. Define \\(k\_{ij}\\) as the effective irreversible reaction-rate coefficient of donor \\(j\\) on a molecule that actually requires donor \\(i\\).

If all donor species are continuously present at fixed positive concentrations, the correct reaction hazard for programme \\(i\\) is \\(k\_{ii}c_i\\), and its incorrect reaction hazard is \\(\sum\_{j\ne i}k\_{ij}c_j\\).

Define

\\[ M\_{ij}= \begin{cases} k\_{ij}/k\_{jj},&i\ne j,\\\ 0,&i=j. \end{cases} \\]

For an irreducible nonnegative matrix \\(M\\), I obtain the exact minimax identity

\\[ \boxed{ \inf\_{c_i>0}\ \max_i \frac{\sum\_{j\ne i}k\_{ij}c_j}{k\_{ii}c_i} =\rho(M) } \\]

where \\(\rho(M)\\) is the spectral radius.

The proof uses the Collatz–Wielandt characterization of the Perron eigenvalue. This is an application of established mathematics, not a claim to have discovered a new spectral theorem.

The consequence is significant for Astra: if the measured cross-reaction matrix has too large a spectral radius, changing donor concentrations cannot make every simultaneously active programme sufficiently selective.

However, this limitation applies to stationary shared mixtures. It does not rule out changing the order of donor exposure.

### Ordering donor pulses can beat stationary mixing

I built a finite-state reaction model where a correctly incorporated molecule becomes chemically protected until the next shared deprotection cycle. A stalled molecule remains reactive and can encounter other donors.

Under a deliberately asymmetric hypothetical cross-reaction matrix,

\\[ K= \begin{pmatrix} 1 & 0.2\\\ 10^{-6} & 1 \end{pmatrix}, \\]

donor B reacts incorrectly with unfinished A much more readily than donor A reacts incorrectly with unfinished B.

For two differently programmed active molecules, using a total donor-exposure duration of 20 model time units and an irreversible damage rate of \\(10^{-4}\\) per unit:

| Donor-delivery strategy                   | Probability both eventually complete their current steps correctly |
| ----------------------------------------- | ------------------------------------------------------------------ |
| Optimised stationary A+B mixture          | 98.79%                                                             |
| Sequential A, then B; optimised durations | 99.60%                                                             |
| Sequential B, then A; optimised durations | 95.79%                                                             |

The model allows unfinished parents to retry on later shared cycles. It charges chemical damage during every cycle and irreversible off-target bonds. The rates are hypothetical, not biochemical measurements.

The result establishes a practical design rule: when cross-reactivity is strongly directional, donor order can be an error-control mechanism. Success makes one lineage temporarily inert before the reagent most dangerous to it is introduced.

The calculation was reproduced using an independently constructed continuous-time Markov model, with 400 randomized parameter checks and maximum numerical disagreement below \\(1.2\times10^{-14}\\).

### A stronger bound: even an ideal controller cannot always prevent cross-reactions

I tested the best possible donor schedule under an extremely favourable assumption: a controller instantly observes every successful reaction and changes donor identity without delay.

For a set \\(S\\) of unfinished molecules, the exact optimum satisfies

\\[ V(S)=\max\_{j\in S} \frac{k\_{jj}V(S\setminus\\{j\\})} {k\_{jj}+w_j+\sum\_{i\in S\setminus\\{j\\}}k\_{ij}+\sum\_{i\in S}d_i}. \\]

Here \\(w_j\\) represents incorrect chemistry from the intended donor and \\(d_i\\) irreversible parent damage.

This yields a useful result: under the specified linear reaction clocks, there is no benefit to mixing donor species while an ideal controller waits for its next observed successful reaction. A pure-donor schedule is optimal. I verified the recurrence against exhaustive order enumeration on 175 randomized reaction matrices.

Three differently programmed molecules, hypothetical chemistry

| Cross-reaction network                 | Maximum probability all three react correctly |
| -------------------------------------- | --------------------------------------------- |
| Acyclic, correctly ordered             | 100%                                          |
| Directed cycle, wrong-rate ratio 0.02  | 98.04%                                        |
| Symmetric cross-reactivity, ratio 0.02 | 94.27%                                        |

These are optimistic upper bounds with no chemical damage, no donor-switching overhead and perfect observation.

They reveal a structural distinction: a directional cross-reaction network can sometimes be neutralized through ordering, whereas a strongly cyclic network retains a fidelity penalty even under ideal feedback.

The actual molecular relay has no demonstrated perfect observer. Its attainable performance must be lower or equal to this ideal bound.

## New obstacle: long programmes accumulate unavoidable reactor exposure

I then attacked the strongest surviving ordered-pulse architecture with two failures that do not disappear when correct ligation becomes faster.

First, donor carryover. Residual active donor B can survive cleanup and enter the next A pulse, attacking a molecule that is still waiting for A.

In the hypothetical asymmetric two-donor model, after optimizing pulse durations, retaining 95% correctness requires:

| Programme length | Maximum residual active-donor fraction |
| ---------------- | -------------------------------------- |
| 64 additions     | 0.642%                                 |
| 1,024 additions  | 0.0270%                                |

The two calculations use different stated damage rates (\\(10^{-5}\\) and \\(10^{-6}\\) per model time unit respectively), with 15 time units of donor exposure per cycle. These thresholds concern sustained active-donor carryover during the next pulse, not the total amount of inactive PNA material remaining bound.

This reinforces the earlier physical result: chemical quenching and physical donor displacement are separate requirements.

Second, product aging. If every rooted molecule remains exposed to irreversible damage rate \\(d\\) for the full duration \\(T\\) of each required macrocycle, then

\\[ \boxed{P\_{\mathrm{correct}}\leq e^{-dTL}.} \\]

This bound holds even if intended incorporation becomes arbitrarily fast.

For \\(d=10^{-5}\\) and \\(T=15\\), a 1,024-addition programme cannot exceed 85.76% correct survival in that model. A 64-addition programme has an upper bound of 99.04%.

It is therefore not enough to improve coupling kinetics. Long programmes require either less damaging processing, shorter cycles, protected storage or fewer independently required operations.

### A further test: persistent slow molecules

I incorporated molecule-specific competence that remains correlated across repeated cycles. Using a hypothetical Gamma(3, 1/3) distribution of correct-reaction rate multipliers, with mean one:

| Programme       | Uniform competence | Persistent heterogeneous competence |
| --------------- | ------------------ | ----------------------------------- |
| 64 additions    | 98.92%             | 88.46%                              |
| 1,024 additions | 84.03%             | 59.81%                              |

The heterogeneous calculation integrates each molecule's entire chain-completion probability before averaging over molecules. It does not assume that a slow molecule becomes fast on the next pulse.

These are stress tests, not fitted biochemical predictions.

## The physically stronger construction

The results favour a protected-successor, donor-ordered modular NCL relay over another complex DNA address-erasure device.

The chemical scheme is to keep successfully extended molecules protected throughout a shared schedule of donor mini-pulses, resolve temporary NCL thioesters, physically remove active donors, and only then expose the next reactive terminus. Stalled molecules retain their old terminus and retry. The schedule is chosen from measured asymmetric cross-reactivity, rather than assuming that every donor is perfectly orthogonal.

This preserves the central Astra objective of independent progress in a shared environment without adding a hypothetical perfect bond sensor. An explicit two-lineage transition model confirms that one programmed molecule can stall while another advances, and both can later resume from their respective positions. That is a conditional state-machine result, not yet a chemical demonstration.

A useful recent primary precedent is the 2026 PNA-tagged one-pot reaction-screening system of Kohyama, Barluenga and Winssinger, which screened 64 and then 143 substrate combinations. It offers a way to identify troublesome reaction pairs, but its MALDI readout does not by itself establish irreversible wrong-amide kinetics or junction identity.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubs.rsc.org\&sz=32)

pubs.rsc.org



For actual peptide manufacture, the strongest experimentally established alternatives remain CAPTN and automated SPPS incorporating NCL. They demonstrate useful synthetic operations without proving Astra's asynchronous shared-bath mechanism.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

pmc.ncbi.nlm.nih.gov

+1



The next decisive chemical discriminator is therefore a two-programme reaction containing one deliberately stalled and one advanced parent, with the donor pulse order reversed in a matched comparison. It must establish junction-specific stable amides, successful retry, preserved terminal protection, physical donor removal and the actual cross-reaction matrix. If that matrix is nearly symmetric or badly cyclic, the ordered-pulse mechanism loses its principal advantage.

The analytical work and executable tests are saved:

Derivations, assumptions and chemical counterexamples

Ordered-pulse reaction model

Exact ideal-controller bound

Donor carryover, clearance and heterogeneity tests

Independent two-lineage progression model

Substantive outcome: reaction ordering can provide a mathematically demonstrable advantage without assuming a new molecular bond detector. The same analysis identifies conditions—cyclic cross-reactivity, chemically active donor carryover and accumulated product damage—under which that advantage fails. The major physical blocker remains preserving correct positional donor registration across independently progressing molecules.