## Astra Chemistry — A chemically grounded simplification

I reproduced the saved latent-donor sorting calculations, including the predicted failure when rejected donors repeatedly rebind or remain chemically activatable. The mathematical model is internally consistent within its stated reaction assumptions.

A more useful chemical option has emerged from primary experiments: Fmoc-protected N-terminal cysteine combined with a latent peptide-thioester precursor.

Kar and colleagues demonstrated that Fmoc-protected cysteine survives conditions used to activate peptide hydrazide and o-aminoanilide thioester precursors. They subsequently removed Fmoc in aqueous solution within seven minutes using 20% piperidine at pH 11 and performed further native chemical ligation. This was demonstrated in multisegment protein synthesis, not in a DNA/PNA-controlled autonomous relay.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

pmc.ncbi.nlm.nih.gov

+1



This offers a more concrete combination for Astra than several previously proposed hypothetical protecting groups: a donor's future reactive terminus can remain chemically protected while its current thioester precursor participates in synthesis.

There is an important qualification. The published reactions used conditions including 6 M guanidinium hydrochloride, MPAA catalysis and substantial pH changes. Compatibility with the proposed DNA/PNA recognition structures, rooted templates, and repeated shared washing has not been demonstrated. Successful peptide synthesis in those conditions does not establish an operational Astra relay.

The strongest opportunity is therefore to combine this experimentally grounded protection chemistry with a physical selection mechanism that removes rejected donors before activation, rather than assuming that DNA rejection also makes their chemical precursors harmless.

## New construction: separate donor authentication from instruction advancement

The strongest candidate from this round is a two-key, chemically latent peptide donor.

An incoming donor would carry two short PNA recognition arms that jointly identify its intended DNA-template position. During an initial nonreactive phase, incorrect donors are rejected and physically removed. The retained donor is then chemically activated for NCL.

Crucially, these two contacts would authenticate the incoming donor but would not operate the instruction-advancement mechanism. That distinction avoids the earlier failure in which a second DNA contact could falsely signal that a permanent peptide bond had formed.

Cooperative PNA recognition has experimental precedent, including multistrand DNA invasion and mismatch-sensitive recognition. Its integration with chemically latent peptide donors has not been demonstrated.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://pmc.ncbi.nlm.nih.gov\&sz=32)

pmc.ncbi.nlm.nih.gov

+2



### 1. Exact result: two weak contacts can create strong residence-time discrimination

Let \\(B_2\\) be a correctly docked donor with two PNA contacts, \\(B_1\\) the same donor with one contact, \\(U\\) a locally detached donor, and \\(E\\) a donor physically removed from the reaction region.

Candidate-donor authentication

B₂

Two contacts

B₁

One contact

U

Undocked

E

Escaped

If each bound arm detaches at rate \\(u\\), the remaining arm recloses at rate \\(v\\), a fully undocked donor can locally rebind at rate \\(b\\), and physical escape occurs at rate \\(c\\), the exact mean escape times are

\\[ \mathbb E[T\_{\rm single}]=\frac{b+c}{uc}+\frac1c \\]

and

\\[ \boxed{ \mathbb E[T\_{\rm double}] = \mathbb E[T\_{\rm single}] +\frac1{2u} +\frac{v(b+c)}{2u^2c}. } \\]

The extra residence time can grow proportionally to \\(v/u^2\\), rather than requiring a single extremely stable PNA duplex.

Under hypothetical rates \\(u=0.03\\), \\(v=1\\), \\(b=0.03\\), \\(c=1\\), all in s⁻¹:

| Donor after a 240-second wash | Fraction remaining bound |
| ----------------------------- | ------------------------ |
| Correct, two-contact donor    | 68.10%                   |
| Incorrect, one-contact donor  | 0.0926%                  |

The exact continuous-time reaction-network results were independently verified against numerical differential-equation solutions.

### 2. Finite loading exposes the remaining failure

I then removed a favourable assumption: correctly matched donors do not automatically arrive with both contacts formed.

Instead, correct and incorrect donors compete from an initially empty recognition site. Both must first associate through one arm, after which their respective second arms may close at different rates.

The exact five-state loading model includes the empty template, singly and doubly attached correct donors, and singly and doubly attached wrong donors.

For a 1,024-addition hypothetical programme, with intended secondary-contact closure \\(v_C=1\\,\mathrm{s}^{-1}\\), the optimized predictions are:

| Wrong donor's secondary closure \\(v_W\\) | Correct completion |
| ----------------------------------------- | ------------------ |
| 0 s⁻¹                                     | 98.65%             |
| 0.01 s⁻¹                                  | 98.01%             |
| 0.03 s⁻¹                                  | 96.49%             |
| 0.05 s⁻¹                                  | 94.45%             |

These values charge finite loading, wash-time damage and an additional per-attempt loss probability, but exclude errors of instruction advancement and final tag removal.

The 95% feasibility boundary occurs at approximately

\\[ \boxed{\frac{v_W}{v_C}\leq0.0452} \\]

for the specified rates.

A fully matching but incorrectly assigned two-contact donor is more damaging than a weak secondary mismatch. If its future binding kinetics are identical to those of the intended donor, residence-time sorting cannot distinguish the two at all.

This is why avoiding false two-key authentication is more important than simply maximizing binding affinity.

## 3. The stronger experimental comparator nearly matches it

I compared the new system against a simpler architecture using one longer, more stable PNA probe. Both models were given equal initial pseudo-first-order association rates and finite loading periods.

Hypothetical 1,024-addition comparison

| Architecture                  | Best correct completion | Mean attempts per addition |
| ----------------------------- | ----------------------- | -------------------------- |
| One longer recognition probe  | 97.94%                  | 3.46                       |
| Two weak cooperative contacts | 98.65%                  | 2.31                       |

The single-probe example assumes a correct dissociation rate of \\(0.0026\\,\mathrm{s}^{-1}\\) and wrong-donor rate of \\(0.03\\,\mathrm{s}^{-1}\\). This is not a measured matched comparison.

The apparent two-key improvement is fragile. Under these assumptions, an additional irreversible failure probability of only

\\[ \boxed{3.09\times10^{-6}\text{ per attempt}} \\]

would erase its advantage over the single-probe alternative.

The two-key design therefore does not deserve to replace conventional PNA recognition until its additional chemical and linker failure rates have been measured.

## 4. Another exact counterexample: one shared wash may be impossible

I constructed two individually viable peptide programmes with different donor-binding and parent-aging kinetics.

For 64 additions and a 95% fidelity target:

| Programme                           | Permitted shared-wash timing |
| ----------------------------------- | ---------------------------- |
| A: needs mismatch removal           | At least 537.7 seconds       |
| B: loses productive donors and ages | At most 139.6 seconds        |

Each programme can independently achieve 95% in the mathematical model. No single common wash duration can satisfy both.

The best shared timing yields only approximately 63.1% worst-programme completion.

This is a scoped impossibility result for a fixed shared-wash protocol, not for molecular manufacturing generally. Better recognition-sequence selection, local shielding or fueled discrimination may remove the conflict.

It provides a specific justification for investigating more elaborate proofreading only when the actual programme kinetics exhibit incompatible passive-wash windows.

## Physical conclusion

The most promising near-term mechanism is a short, rooted NCL relay using chemically latent donors, two-key PNA authentication, actual physical donor removal, and the experimentally established Fmoc-protected successor chemistry.

The critical unresolved operations are maintaining registration as the product grows, resolving temporary thioesters before terminal unmasking, preventing false two-contact binding between separate rooted programmes, and ensuring the entire chemistry survives repeated shared treatment. Successful candidate authentication alone does not establish any of these.

There is also a substantial throughput problem. Even the favourable hypothetical two-key 1,024-addition calculation entails approximately 268 hours of washing alone, excluding donor loading, ligation, deprotection and recovery. CAPTN and existing multisegment NCL remain stronger practical synthesis methods until an actual advantage in asynchronous progress is demonstrated.

The smallest decisive chemical experiment is two differently programmed rooted parents, with correct two-contact donors, single-contact mismatches, a deliberately false two-contact donor, and an intentionally stalled parent. The outputs must distinguish real permanent amides, temporary thioesters, incorrect stable bonds and preserved parent competence.

### Preserved scientific work

- Detailed proofs, chemical assumptions, construction and counterexamples
- Competitive donor binding, library-size and physical-clearance model
- Two-contact kinetic authentication and escape model
- Finite competitive loading and full washing model
- Two-programme shared-wash impossibility example
- Matched single-probe comparator and break-even calculation

All five executable models passed their specified numerical or independent-equation checks.

The substantive result is a more discriminating construction and a set of exact feasibility boundaries. Separating pre-commit donor authentication from chemical instruction advancement removes one important logical failure of the previous designs, while exposing the physical requirements that must be satisfied before it becomes a real molecular manufacturing capability.