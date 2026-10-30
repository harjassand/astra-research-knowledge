# Exact-source comparator and constructive next interface
2026-10-29. Addendum, not a replacement for INDEPENDENT_WINDOW_AUDIT.md.

## Governing sources (limited summaries, exact locations)

**Dünnweber–Styliaris–Trivedi, v2.** [§III.1–III.2](https://arxiv.org/html/2601.20818v2) constructs local CPTP attempts with generator sum gamma(Phi-I), including resets and repairs. §III.2 describes state-independent Poisson attempt clocks and independent local unitary-noise clocks. Its finite synchronization neighborhoods give a constant lower bound on next-step progress; the ensuing effective discrete fault-strength claim feeds an exRec recursion. The [Discussion](https://arxiv.org/html/2601.20818v2) explicitly characterizes the continuous-time argument as an outline and defers a detailed proof. It also identifies constant encoding rate as an open extension. The discrete-time theorem already protects noisy control and supports autonomous computation in two dimensions. Therefore neither autonomous QEC nor noisy-control protection is a new capability of our comparator. A counterexample to converting arbitrary waiting-time marginals into product fault tails would expose an insufficient inference, not refute the complete construction. Their exact finite-neighborhood setup must be respected. (Verified HTML lines 121–125, 1387–1415.)

**Selub–Bhardwaj–Lake, v2.** [§1.1 and §2](https://arxiv.org/html/2609.11457v2) assume noiseless classical operations. The asynchronous marching-soldiers guarantee applies to code-capacity decoding. §2 explicitly distinguishes phenomenological streaming noise: the asynchronous conversion is not pursued. Their streaming architecture has bounded-speed local classical processing and constant resource density; its global reliable-clock and noiseless-processor assumptions are identified in §1.3. This is considerably more than a static decoder, but it does not supply our noisy asynchronous controller interface. Conversely our ideal SSF comparator does not supply their geometric locality, streaming primitives or full fault-tolerant computation. (Verified HTML lines 175–180, 308–316, 349–351.)

**Fawzi–Grospellier–Leverrier.** [Proposition 14, Lemmas 15/17, §4](https://arxiv.org/html/1808.03821) provide the candidate-mass, confinement and reduction inputs, plus a parallel SSF analysis. The paper assumes fast error-free classical processing and makes an additional assumption on storage noise accumulated during decoding. Its parallel witness framework does not by itself analyze an uncontrolled physical-time stream of faults interspersed with random hub attempts. Our proof substantially reuses its combinatorial structure; it should not be advertised as an unrelated new threshold mechanism. (Verified HTML lines 53, 68–78, 388–421.)

## What the audited proof actually adds
The defensible result is a **model-specific rigorous bridge**: constant-duration physical blocks of ideal, independently attempted atomic SSF map a small locally stochastic Pauli residual class into itself, despite ongoing bounded-rate local Pauli arrivals, with exponentially small-in-distance failure probability. It permits high-rate expander-code storage on a bounded-degree interaction graph without a global sweep. Unlike merely knowing a mean completion rate, its fixed-window witnesses control arbitrary surviving support sets and compose without conditioning on success.

This is not an immediate invocation of any of the three inspected theorems: the asynchronous physical-time support-tail statement is an additional argument. It is nevertheless a natural adaptation of established SSF witness/percolation techniques. These sources alone cannot establish publication-level novelty, optimality, or that no other standard theorem implies it. The novelty search must include partial/constant-time SSF and noisy asynchronous cellular-automaton results before making stronger claims.

The genuinely useful remaining target is the conjunction **constant encoding rate + noisy autonomous finite-duration local controllers + continuous unknown bounded local noise + operational output**, with graph locality distinguished from geometric locality. The present comparator delivers only the first property and an idealized version of the third. It does not yet deliver that conjunction.

## Constructive next lemma: physical-window local records, not update-index noise
Here is a precise route that avoids the questionable inference from individual waiting-time tails to joint update-index faults.

Assume every unresolved beneficial hub has a fixed finite driving-clock neighborhood B_h. Give hub neighborhoods a conflict graph of maximum degree d: disjoint neighborhoods share no driving clocks. Suppose a physical time interval of length t0 has an event A_h, determined only by the independent intended-update/repair clock records in B_h, independent of the dominating physical-fault clocks, with probability at least rho>0, such that **for every legal exterior history and every local DATA/controller state** it either:

1. completes a genuinely fresh, correctly serialized SSF evaluation of h; or
2. exposes a bounded-support bad event explicitly charged to the fault count.

If the candidate remains unresolved and no charged bad event occurs, A_h is impossible. In L successive subintervals, define the clock-only obstruction indicator I_h by absence of A_h in all L trials. Independent fresh increments imply P[I_h=1] <= q=(1-rho)^L. For any fixed set H of k hubs, color the conflict graph and select a color containing at least k/(d+1) hubs. The corresponding driving neighborhoods are disjoint, giving

  P[all h in H are clock-obstructed] <= q^[k/(d+1)].

Consequently, for any fixed containing hub set H(W), the generating-function expansion yields

  E[t^(sum_{h in H(W)} I_h)]
  <= (1+q^[1/(d+1)](t-1))^|H(W)|.

For actual missed candidates, charge every hub with a realized A_h but no correct resolution to a recorded bad event in B_h. Bounded incidence gives M(W) <= sum I_h + c Q_fresh(W^+), for a constant-size neighborhood enlargement W^+ and constant c. Thus Q+M is bounded by (1+c)Q_fresh+sum I_h. The audited §9 argument survives with q replaced by q^[1/(d+1)], and the fault-support/graph constants enlarged to pay for this charging. Raw misses cannot simply be identified with clock obstruction when the alternative (2) occurs. A bounded spatial dependence cost does not destroy a constant threshold. Independence from the dominating physical-fault clocks is required for the unchanged product-moment calculation. If the record event itself includes a no-physical-fault requirement, the fault and miss majorants become correlated: use a joint moment bound (for example Cauchy–Schwarz with doubled moment arguments and a correspondingly weakened exponent), not the independent product formula. This is a conditional lemma, not a claim that the existing controller supplies A_h.

### Important instrument distinction
For a specified record of *attempts* of state-independent CPTP channels, conditioning on that record leaves the chronological CPTP composition; the record probability is independent of the DATA state. This remains true for entangled input. In contrast, conditioning on selected Kraus outcomes or on successful control observations need not leave a trace-preserving or input-independent DATA instrument. The proposed lemma requires the former, or an independently proved uniform instrument statement. Entanglement is not itself an obstacle to clock-record independence; hidden outcome selection is.

### Exact next experiment/proof obligation
For one finite compiler neighborhood, enumerate a bounded attempt word that (i) safely initializes workspace, (ii) establishes full read-footprint exclusion, (iii) extracts current stabilizers, (iv) applies the prescribed accepted correction, and (v) releases/reset resources. Prove its clean DATA action for every allowed initial controller state and legal boundary history. Enlarge B_h to include every external channel that can interfere, and include a finite no-interference record in A_h. The word probability then has a constant lower bound from Poisson rates, independent of N. This would establish the missing hypothesis constructively; showing only flag repair or a favorable path in a controller-only graph would not.

If arbitrary initial controller states cannot safely execute such a word, first classify the obstructing states as damage with a joint spacetime tail. That is the precise blocker, not a generic shortage of mixing or clock progress.

## Status
The source comparison does not supersede the accepted independent proof review. No external mutations or denied accesses occurred. The local-record lemma is established conditionally; instantiating its uniform clean-instrument hypothesis remains open.
