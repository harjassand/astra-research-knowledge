## Astra Chemistry — A simpler route to independent chemical progress

A useful alternative to the DNA erase-and-disarm controller is now supported by a directly relevant experimental precedent.

Silva and colleagues demonstrated that O-salicylaldehyde esters (OSAEs) can reversibly protect N-terminal cysteine while allowing chemical modification of internal cysteine residues. Subsequent acidic treatment can restore the original reactive N-terminal cysteine. This was demonstrated on peptides, not within Astra's relay.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

pmc.ncbi.nlm.nih.gov

+1



This offers a potentially important construction principle: distinguish a failed molecule from a successful molecule using the chemical environment of its cysteine, rather than a separate DNA instruction counter.

After native chemical ligation:

- An unsuccessful parent still possesses its original N-terminal cysteine.
- A successful product has converted that cysteine into an internal residue and possesses a new, protected N-terminal cysteine on the incorporated fragment.
- Both molecules could undergo reversible terminal protection, selective internal-thiol treatment and terminal restoration under shared conditions.

This exploits a chemical distinction created by the backbone bond itself. It potentially avoids the previous controller's single-strand-nicking problem and its cumulative DNA cleavage stubs.

The main limitation is that NCL already tolerates internal cysteines in many circumstances; their existence does not automatically prevent subsequent ligation. The justification for chemically modifying them must be a measured reduction in nonproductive donor capture or incorrect chemistry—not merely their presence.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

pmc.ncbi.nlm.nih.gov

+1



## New result: the physical arrangement of old addresses determines whether erasure is necessary

The simplified NCL relay has another failure mode: even if an old cysteine cannot form a new backbone amide, its retained DNA/PNA address may still recruit an incorrect donor close enough to react with the current N-terminal cysteine.

I derived an exact competing-reaction model that separates this positional interference from internal-thiol chemistry.

Let \\(a\\) be the intended joining rate, and let an old address \\(r\\) positions behind the active frontier contribute a wrong-joining hazard \\(b_r\\). At step \\(j\\), the total wrong hazard is

\\[ B_j=\sum\_{r=1}^{j}b_r. \\]

For independent exponential reaction clocks, with no other damage,

\\[ \boxed{ F_L=\prod\_{j=0}^{L-1}\frac{a}{a+B_j}. } \\]

This gives a useful scaling distinction when \\(b_r=b_1r^{-\alpha}\\):

| Decay of old-address interference | Leading accumulated hazard exposure |
| --------------------------------- | ----------------------------------- |
| No decay, \\(\alpha=0\\)          | \\(O(L^2)\\)                        |
| \\(\alpha=1\\)                    | \\(O(L\log L)\\)                    |
| \\(\alpha>1\\)                    | \\(O(L)\\)                          |

The last case matters physically. Contacts between distant sites of an ideal flexible polymer in three-dimensional dilute solution decay approximately as \\(r^{-3/2}\\). That is an established polymer-physics result, though not a measured law for this specific PNA–peptide construction.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubs.acs.org\&sz=32)

ACS Publications

+1



Illustrative 1,024-addition programme

Assume \\(b_1/a=10^{-5}\\), with otherwise perfect chemistry.

Entirely correct completion under alternative contact geometries

Illustrative mathematical probabilities, not measured yields.

0%25%50%75%100%Uniform contactSlow decay, α=1Ideal coil, α=1.5Rapid decay, α=2

The important insight is that permanent address removal may not be necessary to avoid quadratically increasing interference, provided obsolete addresses become sufficiently ineffective at recruiting donors near the active frontier.

This does not solve long-chain fidelity: even linear accumulation of small errors eventually becomes prohibitive. It instead identifies a less complex architectural option worth testing before introducing restriction enzymes and DNA erasers.

## Further result: reversible incorrect chemistry is not necessarily fatal

I constructed a first-passage model for donors temporarily trapped at old internal cysteines.

Let \\(a\\) denote the correct ligation rate, \\(d_A\\) the irreversible damage rate at the active terminus, \\(b\\) the reversible trapping rate per old internal cysteine, \\(r\\) the escape rate from a trapped state, and \\(x,d_T\\) the irreversible wrong-reaction and damage rates while trapped.

With \\(j\\) old internal cysteines, the exact probability of a correct next amide before irreversible failure is

\\[ \boxed{ P_j= \frac{a}{ a+d_A+jb\frac{x+d_T}{r+x+d_T} }. } \\]

The important limiting case is \\(x=d_A=d_T=0\\). Every stage then succeeds eventually, regardless of how many old internal cysteines are present. Reversible trapping only increases the expected time:

\\[ \mathbb E[T_L]=\frac{L}{a}+\frac{bL(L-1)}{2ar}. \\]

This establishes a useful distinction: internal cysteines can create a quadratic slowdown without necessarily creating irreversible sequence errors.

It means additional chemical capping is justified only when its reduction in trapping, permanent wrong chemistry or parent aging exceeds the damage and processing overhead it introduces.

### The masking alternative fails an important long-chain screening test

The published OSAE half-lives are approximately nine hours at pH 7 and 42 minutes at pH 4.5 for the studied conjugates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

pmc.ncbi.nlm.nih.gov



Consider the earlier illustrative 1,024-step programme with correct pulse probability \\(p=0.6\\), irreversible wrong probability \\(w=10^{-6}\\), and a target of 95% correct completion. The maximum allowable probability of destroying a stalled parent during each otherwise harmless missed pulse is approximately

\\[ \boxed{\delta\_{\max}=7.26\times10^{-5}.} \\]

If every spontaneous terminal unmasking during a 30-second thiol-capping pulse is fatal, the measured nine-hour half-life gives an unmasking probability of approximately \\(6.42\times10^{-4}\\). Under that particular model, final correct completion falls to 64.4%, even with perfect initial masking.

This does not rule out faster recapture, gentler capping or alternative protecting groups. It does rule out treating that measured protecting group as a lossless long-chain operation.

## The next decisive physical requirement

For a 1,024-step programme and the ideal-chain interference model \\(\alpha=1.5\\), achieving 95% correctness from positional fidelity alone requires

\\[ \boxed{\frac{b_1}{a}\leq2.013\times10^{-5}.} \\]

If correct and incorrect joining were the only two competing outcomes, establishing this rate ratio through a zero-error assay with perfect detection would require at least 148,843 independent observations for a one-sided 95% confidence bound. Real assays with missed detections or correlated samples require more evidence.

That is why observing a few correct peptide products would not establish the proposed capability.

The strongest next molecular test is a mixed reaction containing one stalled parent and one already advanced parent whose old barcode remains present. Their intended next donors differ. The decisive outcome is whether the advanced parent can reject donor recruitment by its obsolete address while both parents retain their own correct reaction competence.

### Mechanism selected

The leading construction is now NCL with a chemically self-indexed growing terminus, a protected successor terminus, explicit removal of reversibly attached donors, and no per-bond DNA eraser.

Compared with the previous BbvCI controller, it requires fewer unestablished chemical operations and does not generate DNA cleavage stubs after every addition. Compared with the original protected-PNA relay, it offers a plausible route to joining chemically diverse peptide fragments, although the protected-PNA relay remains better grounded for repeated extension of PNA products. PNA-templated peptide ligation and programmable PNA polymerization both have experimental precedents.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pubmed.ncbi.nlm.nih.gov\&sz=32)

pubmed.ncbi.nlm.nih.gov

+1



The remaining obstacle is positionally correct donor selection in the presence of retained old addresses. The mathematical locality condition identifies when that interference could be manageable, but its actual rate and polymer-contact behaviour have not been acquired.

I saved and executed the revised models, including independent first-passage checks, matrix-exponential/ODE comparisons, stochastic simulations and exhaustive abstract two-lineage transition tests.

Scientific derivations, source assumptions and counterexamples

Chemical-frontier, aging and terminal-protection model

Positional-interference and polymer-locality verifier

The mathematical models passed their specified checks. No integrated molecular manufacturer has yet been demonstrated, and neither experimental advantage nor novelty has been established.