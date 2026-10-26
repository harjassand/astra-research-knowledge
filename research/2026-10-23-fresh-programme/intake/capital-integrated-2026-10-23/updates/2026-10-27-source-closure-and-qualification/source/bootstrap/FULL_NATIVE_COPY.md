## Astra XH2 — Bootstrapping cooperative organisation from a fresh founder

### 1. A stronger obstruction: circular dependencies can demand multiple founding capabilities

The previous site-instructed construction assumed that an unfinished material exposes addresses telling new workers what to become. But after a fresh descendant starts from scratch, those addresses may not yet exist.

I extended the model to capture this problem precisely.

Each biological role can be created only when one of its permitted sets of prerequisite structures is already present. The founder directly manufactures a limited set of initial pioneer structures, after which the rest of the construction develops through local interactions.

The central result is a bootstrap certificate.

Call a group of roles \\(U\\) self-blocking if every possible way to create any role in \\(U\\) requires at least one role already in \\(U\\). Then:

\\[ \boxed{ \text{Complete development is possible} \iff \text{the initial founder-made seeds intersect every self-blocking set.} } \\]

This equivalence holds for finite, monotone AND/OR prerequisite systems. It follows by induction: an entirely unseeded self-blocking set can never initiate, while any incomplete construction necessarily leaves such a set behind.

The mathematics is related to established bootstrap-percolation and target-set-selection theory. Its application here identifies what a founder must regenerate before site-directed development can begin.

#### Exact computational tests

I compared two 12-role developmental systems.

| Developmental dependency                                            | Minimum founder-made roles needed | Distinct minimal founding programmes |
| ------------------------------------------------------------------- | --------------------------------- | ------------------------------------ |
| One circular chain, each role needing its predecessor               | 1                                 | 12                                   |
| Four independent three-role groups, each role needing both partners | 8                                 | 81                                   |

Both systems contain circular dependencies. Yet one needs only a single pioneer role, while the other requires eight.

The distinction is that mutually dependent roles can form an AND barrier. Simply detecting cycles or supplying one seed per strongly connected component is insufficient.

I exhaustively checked all 4,096 candidate seed sets in each system and separately tested the certificate on 60 randomly constructed seven-role dependency systems. No contradictions were found.

Scientific implication: the inherited genome must reproduce a sufficient starting repertoire, not merely the worker functions needed after the material has already assembled.

### 2. Even genetically sufficient seeds can fail through transient loss

The next result is more restrictive.

Suppose a three-role cooperative structure has two pioneer roles present. Those pioneers are lost independently at rate \\(\lambda\\), while the third role matures at rate \\(\gamma\\).

If losing either pioneer before maturation irreversibly aborts that attempt, the probability of completing the group is exactly

\\[ \boxed{P\_{\rm mature}=\frac{\gamma}{\gamma+2\lambda}.} \\]

For four independent groups rebuilt across 20 fresh generations, the probability that every attempt succeeds under this restrictive model is

\\[ \boxed{ P\_{\rm continuous} = \left(\frac{\gamma}{\gamma+2\lambda}\right)^{80}. } \\]

| Maturation-to-loss rate ratio | Probability all 20 reconstructions succeed |
| ----------------------------- | ------------------------------------------ |
| 10                            | 0.000046%                                  |
| 100                           | 20.51%                                     |
| 1,000                         | 85.23%                                     |
| 4,000                         | 96.08%                                     |

Achieving 95% reliability requires approximately

\\[ \boxed{\gamma/\lambda\geq3{,}118.3.} \\]

The rates are synthetic, and this calculation deliberately excludes retries, replacement and continuing pioneer production. It is a stringent baseline, not a biological performance forecast.

Nevertheless, it changes the mechanism worth investigating. The founder's initial addresses must not merely form; they must persist until downstream construction no longer depends on them.

That leads to a stronger operation than unregulated nucleation: retain a founder-produced temporary structure until an independently verified replacement has taken over its function.

### 3. Feedback can greatly reduce the cost of regenerating the starting structure

I compared two strategies for manufacturing the eight pioneer roles required by the four cooperative groups.

In the first, the founder produces a predetermined number of pioneer attempts without checking whether they worked.

In the second, it produces one pioneer attempt, obtains a local confirmation, and moves to the next necessary pioneer only after a positive result.

Each pioneer attempt has a synthetic 95% probability of working.

Probability of completing 20 independent fresh reconstructions

| Founder strategy                             | Maximum pioneer attempts per reconstruction | Reliability |
| -------------------------------------------- | ------------------------------------------- | ----------- |
| Open-loop, one attempt for every role        | 12                                          | 55.87%      |
| Optimized open-loop allocation               | 16                                          | 80.31%      |
| Optimized open-loop allocation               | 19                                          | 93.22%      |
| Optimized open-loop allocation               | 20                                          | 97.98%      |
| Feedback-guided, two confirmation readings   | 13                                          | 96.72%      |
| Feedback-guided, three confirmation readings | 14                                          | 97.86%      |

The feedback-guided mechanism requires only 8.95 pioneer attempts on average in the two-reading case, plus approximately 17.9 sensor readings.

This is a genuine resource trade-off, not a free improvement. In the synthetic cost model, the two-reading strategy uses fewer total resources than the 20-attempt open-loop strategy only if each sensor reading costs less than approximately 62% of one pioneer attempt.

The result also depends on the ability to discard failed attempts and test distinct pioneer roles separately.

A 0.3% probability of a shared false-confirmation event reduces the two-reading strategy's 20-generation reliability from 96.72% to 94.20%.

Thus, local confirmations can make founding more efficient, but only when they measure actual physical seed formation rather than reporter activity or material occupancy.

### 4. A more important result: physical replacement is not hereditary replacement

The strongest conceptual finding came from challenging what it means for a pioneer to become unnecessary.

Consider three roles A, B and C. Each needs the other two to initiate. The founder can directly manufacture A and B, allowing C to form.

After all three exist, the material may no longer need the original temporary A structure. Removing that temporary structure could leave a fully functioning construction.

But suppose a genetic mutation eliminates the founder's ability to manufacture A.

The existing material can remain perfectly functional, while a fresh descendant starting with only the ability to make B cannot initiate either A or C.

Therefore,

\\[ \boxed{ \text{Pioneer no longer needed by parent} \\;\not\Rightarrow\\; \text{Pioneer instruction no longer needed by descendants}. } \\]

This creates a direct evolutionary failure mechanism.

In a synthetic example, maintaining the complete pioneer-producing genotype carries a 10% reproductive cost. A deletion mutant starts at 1% frequency and performs equally well while an ancestral scaffold remains available.

After 60 idealized transfers, the cheaper mutant rises to approximately 84.9% of the population.

Once the ancestral scaffold is removed, those mutants fail to regenerate the structure.

This is a route by which selection can actively destroy acquired developmental competence while every parental functional test appears successful.

The necessary correction is two distinct forms of retention:

Physical pioneer structures may be removed after verified downstream maturation. However, their genetic manufacturing instructions must remain protected unless a fresh descendant can independently reconstruct the function without them.

This makes source-closed reconstruction a requirement for evaluating mutations that simplify an inherited construction programme.

### 5. Can the unknown complexity of a developmental bootstrap be measured?

I pursued another consequence of the bootstrap certificate.

Suppose every possible pioneer role independently appears with probability \\(p\\). If the smallest successful seed set contains \\(m\\) roles, then at low \\(p\\),

\\[ P(\mathrm{successful\ bootstrap}) = N_mp^m+O(p^{m+1}), \\]

where \\(N_m\\) counts the successful seed sets of minimum size.

Consequently,

\\[ \boxed{ \lim\_{p\to0} \frac{d\log P(\mathrm{bootstrap})}{d\log p}=m. } \\]

This suggests a way to infer the minimum number of cooperating pioneer functions from end-to-end experiments, even without knowing their individual identities.

However, the experiment becomes extremely expensive for highly cooperative structures.

In the four-group model, the theoretical bootstrap order is eight. At spontaneous seed probability \\(p=0.05\\), successful reconstruction occurs with probability only \\(2.76\times10^{-9}\\).

Approximately 36 billion independent reconstructions would be required to observe even 100 expected successes.

At higher seed probabilities, the outcome becomes easier to measure, but the observed logarithmic slope can substantially underestimate the true bootstrap order.

The mathematics can reveal hidden cooperative complexity, but sparse whole-system outcomes alone may not provide an experimentally efficient method. Local functional probes remain valuable because they reveal intermediate information.

### 6. A stronger biological candidate for manufacturing the first addresses

The literature comparison suggests prioritizing genetically manufactured pioneer material rather than supplying chemically prepatterned structures indefinitely.

A 2026 De Novo Autogenic Engineered Living Functional Materials study demonstrated engineered E. coli producing extracellular curli-like protein fibres, with genetically grafted binding domains and tunable material properties. This is evidence that an organism can manufacture structural material carrying programmed functionality.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://advanced.onlinelibrary.wiley.com\&sz=32)

Wiley Online Library



The 2025 Programming cellular condensates for living materials using an intrinsically disordered protein display platform study demonstrated sequence-dependent aggregation and segregation of engineered bacterial populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

PMC



The 2026 Synthetic circuits for cell ratio control study demonstrated the complementary genetic operation of deriving differentiated cooperative populations from a single founder.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

Nature



Together, these suggest a candidate architecture in which the founder first makes a small, genetically specified extracellular seed matrix. The matrix recruits and organizes specialized descendants, which subsequently produce the durable functional material.

But the key connections remain unproved. None of these studies demonstrates a founder-produced address that instructs the correct worker fate, a completion signal that prevents premature pioneer removal, or an acquired developmental programme reconstructed over repeated fresh generations.

The strongest experimental comparison is a deliberately simple three-role dependency cycle. One system would receive externally prepared starting addresses. The other would need to manufacture its own starting addresses from a protected source genotype. Both would receive identical feed, functional tests and opportunities for source selection.

An equally informed external controller could supply the appropriate pioneers more reliably. Its results provide the necessary benchmark. The potential new biological capability is eliminating recurring externally specified structural starting conditions, not outperforming an electronic controller at inference.

### Research conclusion

The most consequential construction emerging from this continuation is hereditary pioneer escrow.

A complete founder must retain enough basal manufacturing capability to initiate the dependency network from fresh feed. Those basal structures can support temporary cooperation while additional roles develop. Physical seed removal must wait for verified replacement, and genetic seed-programme removal must wait for successful fresh reconstruction by descendants.

The analysis now supplies an exact bootstrap-sufficiency condition, a characterization of how cooperative dependencies suppress spontaneous nucleation, optimized finite-resource pioneer production, and a quantitative obstruction from premature seed loss.

It also identifies a potentially dangerous evolutionary failure: a material can become progressively better at maintaining its present structure while selection erases the instructions needed to reproduce that structure.

This sharpens the assigned scientific objective. The desired capability is not merely self-assembly or self-repair. It is the acquisition and faithful hereditary regeneration of a useful cooperative construction process, including its own starting conditions.

The resulting mathematical construction is verified within its assumptions. The integrated biological system, source-correct functional memory and independently regenerated physical starting structures remain experimentally unresolved.

The derivations and executable tests are preserved in bootstrap closure, pioneer escrow and counterexamples, executable bootstrap and resource-allocation analysis, and numerical reliability checks.