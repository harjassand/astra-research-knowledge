> Public selected edition of the 19 October audit. Original review SHA-256: `0f5ca65fcb5a2b2b8e05265ba864c4152d84da7a93d2f7a09e19afa85e3972d2`. Original scientific inputs are retained unchanged. Navigation and historical-receipt pointers are adapted to the selected public subset; mathematical statements, caveats and attribution are retained. Past private-audit statements describe that audit, before approved publication. Current reproduction and retained-file hashes are in the release README and FILES.json.

# Independent prior-art audit: finite-menu kinetic order ambiguity

19 October 2026, Australia/Brisbane. This is a bounded literature comparison, not a correctness audit or a novelty certificate.

**Historical priority remains UNKNOWN.** The strongest inspected identification incumbent already permits **finite generic endpoint tests**; it is inaccurate to contrast this candidate with prior work solely on the basis of finite versus infinite experiments, or endpoint versus continuous observations. The exact constrained counterexample was not found in the inspected primary sources, and no direct implication of it from their stated theorems was established. Neither finding establishes originality.

## Contract actually compared

The final claim in the private snapshot is
\[
\forall\,\mathcal D\subset(0,\infty)\text{ finite with distinct elements},\quad
\exists\, M_1,M_2\text{ and their waveforms}
\]
such that the models have four mandatory irreversible transient stages, different orders of the same anonymous pure-A/pure-B rate pairs, distinct positive rates at each pure level, and four pairwise unequal B/A response ratios. Each model has its own unknown outward and return waveform. Within a model and direction, one fixed normalized waveform is time-dilated across every member of \(\mathcal D\). The four rates remain bounded and strictly positive.

Preparation is stage one and the output is completion at a completed-operation boundary. Equality is for **all legal finite words** of arbitrary nonnegative A/B holds and complete ramps/returns with durations in \(\mathcal D\), including loops. Thus this is much richer than matching finitely many scalar data points. A smooth version matches the appropriate pure rates near the endpoints and glues to holds to every derivative order. Monotonicity, a prescribed pointwise envelope, one known scalar rate-response curve, and literal time reversal of the outward waveform are not supplied.

The existential pair may depend on \(\mathcal D\). The statement does not give one pair for all positive durations, an impossibility theorem for unrestricted adaptive acquisition of new durations, or equality of sub-ramp observations/full continuous-time records. It is a worst-case obstruction on a weighted-product resonance family near equal A/B response, with no fixed positive contrast floor. These details are decisive in comparing generic identification theorems.

Private files read: MAIN_RESULT.md; kinetic_frontier/THEOREM.md, particularly its realization, finite-menu, smoothing and word-equivalence sections; and, only after independent searching and primary retrieval, diffusion_audit/kinetic_priority/REPORT.md. No outputs from the other current verification reviewers were read. Snapshot hashes are in result.json.

## Strongest identification incumbent

**Sontag–Wang–Megretski (2006 preprint; stronger 2009 journal formulation).** The journal Section III-A, p.199, gives
\[
K=2(n^2+2n)+1
\]
generic pulse-width/observation-time pairs sufficient to determine the pulse response, and hence generic bilinear input/output behavior. Each datum is the output at one selected time after a known rectangular pulse. For state dimension four the displayed bound is 49. I checked the mathematical statement visually in the author-hosted journal PDF; this finite strengthening is absent from the 2006 preprint's corresponding statement.

Their Theorems 1–2 and Lemma 4.3 also supply pulse/step nonidentifiability and a transpose-similarity construction. Those are clear predecessors for hidden equivalence. They do not impose the candidate's mandatory positive serial pattern, pairwise response-ratio condition, or one unknown positive waveform shared by several dilations. Their positive identification statements concern generic finite-dimensional bilinear classes, not every structured resonant model. [Journal PDF, pp.199–201](https://www.sontaglab.org/FTPDIR/sontag_wang_megretski_inputs_tac_54_195_207.pdf), [2006 version](https://arxiv.org/abs/math/0610633v1).

The important distinction is the **input/model contract**, not just data quantity. A four-state ramp with four arbitrary unknown normalized rate functions is not automatically a four-state scalar-affine plant \(A+uN\) with a known pulse input. Even the candidate's finite-piece witnesses introduce additional waveform nuisance parameters; the general construction can increase their number with menu size. More fundamentally, an identification theorem recovering the behavior available under an interface does not promise to recover a physical order from two parameters that are already behaviorally equivalent on that interface.

The source-package priority report, line 23, correctly states generic identification by variable-width pulses and identifies the serial-pattern/shared-waveform gap. It **omits**, rather than contradicts, the finite generic endpoint formulation. It does not say that Sontag requires continuous records or infinitely many tests. This needs a literature-comparison clarification, not a theorem refutation. Its main target at lines 7–19 is the earlier two-duration mixed-surface claim; it also needs comparison against the final arbitrary finite-menu, all-word, smooth refinement.

**Sontag (2002).** The underlying analytic-response theorem gives \(2r+1\) generic experiments for an \(r\)-dimensional parameter family, separating every pair distinguishable by the allowed experimental family. It does not guarantee separation of intrinsically equivalent parameters. Its finite-dimensional analytic assumptions also cannot be silently transferred to an unrestricted unknown waveform class. This independently prevents an argument that “finite experiments inherently cannot identify kinetics.” Read: Section 1.2 and Theorem 1, pp.558–560, and response-map discussion. [Author-hosted primary PDF](https://www.sontaglab.org/FTPDIR/ident-experiments.pdf).

**Guo–Tan (2014).** Equations (1)–(2) use a known rectangular input with matrices constant at its levels. Section 2.2.2 employs several pulse durations and post-pulse scalar responses; Sections 2.2.2.1–3 distinguish a known on matrix, a known off matrix, and extra known matrix relationships when both are unknown. Section 2.3 explicitly withholds a global-identifiability guarantee for the fitting algorithm. These are strong prior recurrent-pulse/eigenbasis constraints, not a theorem that arbitrary unknown transition paths are determined by loops. The public primary-text transcription was inspected through Sections 2–3; the 2010 author slides corroborate the stated hypotheses. Publisher PDF retrieval failed. [Article DOI](https://doi.org/10.1016/j.biosystems.2014.02.001), [public article text](https://www.academia.edu/22269588/Identifiability_and_identification_of_switched_linear_biological_models), [2010 primary slides](https://inverseproblems.org/2010%20IPS/cd/Oral%20Presentations/Guo%20%20Tan%20-%20Switched%20Linear%20Systems.pdf).

## Positive realizations and phase-type predecessors

**Rizk–Burke–Walsh (arXiv v2, 23 July 2019).** Static hidden serial-order ambiguity is established prior art. The paper explicitly describes generalized-Erlang/hypoexponential representations as mandatory serial chains and explains that permuting their rates gives equivalent absorption laws. Its Theorem 1 states the initial-state/generator/exit-vector similarity criterion; Corollary 1 specializes the transformation to Coxian form, and Theorem 2 treats diagonal permutations. Thus neither static phase-order ambiguity nor a preparation/readout-preserving hidden similarity is a new principle here. Those results alone do not enforce the *same pair labeling across two pure environments* together with the shared-dilation transition constraints. Read: pp.2–4 and 9–13. [Primary v2](https://arxiv.org/abs/1901.03849v2).

**Lencastre–Raischel–Rogers–Lind (2015 preprint, associated 2016 paper).** Appendix A.1 gives a factorization realizing nonsingular triangular stochastic matrices with nonnegative time-inhomogeneous generators; A.3 discusses total nonnegativity. I checked the factorization, not just the abstract. Its elementary factors allow direct jumps from many states to a selected later state, with inactive rates zero. They do not retain the mandatory nearest-neighbor serial pattern with every stage rate strictly positive, and factorizing each target separately does not couple different duration targets to one dilated waveform. Hence even this constructive Markov-embedding predecessor does not close the exact realization obligation. The finite bounded-rate reading requires positive diagonal entries; singular boundary cases in the paper's unqualified statement are not being invoked. [Primary preprint, Appendix A, pp.10–11](https://arxiv.org/abs/1510.07282v1).

**Ahmad–Bladt–Bladt (arXiv v1, 22 July 2022).** Section 2, equations (2.1)–(2.4), already treats unknown time-dependent, noncommuting transient generators through product integrals, and Section 2.1 expresses piecewise-constant models by ordered matrix-exponential products. Section 3 develops absorption-time estimation with hidden paths. Consequently noncommuting positive segment models and their likelihood representation cannot be claimed as innovations. This fitting theory neither states nor forces the candidate's two-order equality across a shared dilation menu and arbitrary legal words. Read: introduction and Sections 2–3, particularly pp.4–5 and the general EM statements; not every numerical example. [Primary v1](https://arxiv.org/abs/2207.11303v1).

## All-word equivalence and finite ensemble control

**Petreczky (2005 hybrid report; 2011 switched realization paper).** The hybrid Section 5 defines mode-dependent linear morphisms intertwining both mode flows and event/reset maps, with the event relation \(T_B R=R'T_A\). Theorem 12 characterizes minimal realizations up to such isomorphism. The switched paper's Definition 3.3 and Theorem 3.3 give the corresponding common-similarity theory, including formal-series/word representations and constrained switching.

These are direct prior machinery for the candidate's telescoping proof once the physical ramp maps and gauges have been supplied. Calling a finite ramp a hybrid event at the observation boundary is a valid representation, but it does not demonstrate that its event matrices come from one admissible positive waveform at all chosen dilations. The all-word conclusion is an application of established realization algebra, not an independent new hidden-equivalence principle. Read: report Section 5 and Theorems 12–13; switched article Sections 2–3 and its morphism/minimality statements. [CWI MAS-R0502, August 2005](https://ir.cwi.nl/pub/10937/10937D.pdf), [2011 primary paper](https://www.numdam.org/item/10.1051/cocv/2010014.pdf).

**Agrachev–Baryshnikov–Sarychev (arXiv v1, 23 March 2016).** Section 3 and Theorem A establish generic exact controllability for finite ensembles driven by common controls. The proof uses the product system and Lie-rank generation. This is the correct established framework for treating a finite set of duration-scaled copies. The theorem allows signed controls and generic choices of vector fields; it does not automatically cover a constrained scaled-copy family, tied diagonal hazards, fixed positive clock seed, or nearest-neighbor Markov generators. It also does not assert regularity of the endpoint derivative at that particular constant control. Read: Sections 1.2–1.3, 3, and the relevant Appendix 7.1 proof, not the full continuous-ensemble theory. [Primary v1](https://arxiv.org/abs/1603.07133v1).

## Component versus exact consequence

| Candidate component | Prior status from this audit | What still has to be shown in this constrained model |
|---|---|---|
| Static serial phase permutation | Established | Nothing novel at this level |
| Hidden-state similarity and equality of every endpoint word | Established formalism | Admissible maps/gauges with the required physical labels |
| Unknown noncommuting inhomogeneous phase-type flow | Established model class | Coupled equality under the particular legal experiment interface |
| Simultaneous control at finitely many parameter values | Established ensemble framework | Rank for the structured scaled copies at the chosen positive seed |
| Exponential moments, Vandermonde separation, submersion/IFT | Standard machinery | Nonzero root-control coefficients and the exact tied-diagonal rank |
| Smooth interior-bump replacement, endpoint matching, positivity by openness | Standard local refinement once regularity holds | Preservation of the candidate targets in that finite-dimensional family |
| Nonclock equal-sum/product resonance branch with all four ratios unequal | No matching primary statement located | Exact residue identity and physical order constraints |
| Every preselected positive duration menu plus independent return words | No matching full constrained theorem located | Avoiding all finite frequency collisions and realizing each direction |

The **two application-specific bridges** are therefore the resonant residue branch and the positive local endpoint-map surjectivity with its shared-dilation constraints. The reported rank \(4+6k\) is a model-specific calculation using familiar controllability/moment methods. Once those bridges hold, choosing gaps outside finitely many collision conditions, applying finite-dimensional implicit functions, gluing smooth endpoints, and extending gauges to every word are natural consequences.

I did not establish that either bridge is historically new, or that a specialist would regard their combination as more than a routine constrained corollary. Conversely, generic controllability or a broad realization theorem is not a substitute for the missing application-specific hypotheses. **“Not shown to be an immediate corollary of the inspected sources” is the supported conclusion; “new theorem/novel mechanism” is not.**

## Operational significance and limits

Conditional on the mathematical construction being correct, identical all-word probabilities yield identical adaptive fresh endpoint-experiment distributions **within the same fixed menu**. This is exact structural ambiguity, not merely slow statistical convergence. It blocks a universal order-acquisition guarantee for that interface.

It does not establish poor generic identifiability, a failure of calibrated known-waveform protocols, an obstruction under every contrast floor, or equality under new durations/time-resolved/internal-state observations. Independent direction-specific return responses are a material freedom of the model. No physical assay, actuator calibration, costed informative acquisition, or practical advantage follows from an exact hidden counterexample. The explicit tiny-contrast witness is mathematical evidence, not a useful operating point. This literature review does not validate the proof or certificate.

## Retrieval and independence record

The independent first pass used known public paper IDs plus generic keywords for positive realization, pulse identification and ensemble control, before the local source-package priority report was opened. Subsequent public searches added Coxian nonuniqueness, general finite analytic experiment theorems, Markov embedding and ion-channel equivalence leads. No private theorem text, constants, proof details or source files were submitted to public services. No author was contacted.

Firecrawl returned HTTP 402 insufficient credits before searches executed, so retrieval continued through the web tool and direct public downloads. Publisher/CWI web-tool failures are recorded; CWI direct public download succeeded. Academia direct download returned 403, but the web tool supplied the article's primary-text transcription. Kienker (1989) was located only through abstract/metadata and is recorded as an unclosed full-text lead, not evidence for a direct exact precursor. No exhaustive citation-graph or specialist review was completed.

Source versions, URLs, read depth, successful download hashes and limitations are in result.json and receipts/. Only this review directory and public-source receipts were written. Original/source/repository/public artifacts were not edited.
