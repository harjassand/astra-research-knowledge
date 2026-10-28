# A concrete boundary for transferring learned dynamics to feedback control

28 October 2026. New local derivation/diagnostic of a known type of information-interface limitation; no historical novelty claim. This is not a no-reset learner or a new main programme result.

## Primary-science comparison

Zhang et al., *Learning and forecasting open quantum dynamics with correlated noise*, Communications Physics8,29 (18 January2025), https://www.nature.com/articles/s42005-025-01944-2, was read through its model/training and experimental sections. It learns an effective system-memory model from randomized-benchmarking data and demonstrates forecasting in a superconducting system/environment setup. Crucially, the authors explicitly warn that incomplete unitary-sequence data and nonlinear fitting need not identify the full process tensor and may fail on intervention sequences involving measurements. Their representation may also need growing memory even for dissipative Markovian dynamics when restricted to unitary system-memory evolution. These are actual comparator limits, not a claim that ordinary approaches reconstruct every microscopic environmental degree of freedom.

Bennink–Lougovski, *Quantum Process Identification*, https://arxiv.org/abs/1803.02438v3, abstract inspected only, is a prior effective-environment/system-identification baseline. No theorem beyond the inspected material is imported here. A requested HTML version of arxiv2203.01492v3 returned404; that source was not read or used as a premise.

## Exact two-time construction

A source begins each episode by discarding its input and preparing either omega_B=|Phi+><Phi+| on an accessible qubit S and hidden memory E, or omega_P=I_SE/4. The experimenter applies a chosen intervention on S. The source then SWAPs S and E, releases S as final output, and discards E. Memory dimension is two; no source environment is supplied to the experimenter.

For EVERY trace-preserving intervention A on S,

    Tr_S[(A tensor id_E)(omega_h)] = Tr_S omega_h = I_E/2.

Consequently every unconditional final output is I/2 for BOTH sources. Arbitrarily many independent episodes of unitary-only calibration, even with adaptively chosen unitaries and arbitrary final measurements, have exactly identical records. In fact the equality holds for any deterministic CPTP intervention whose instrument outcomes are discarded. Extra numerical fitting accuracy cannot resolve this information loss.

Now perform the actual Z measurement instrument with outcomes b=0,1 before the SWAP and RETAIN b. For the Bell source the released output is |b><b| with probability1/2 each. For the product source it is I/2 independently of b. Measuring output Z and comparing it to b gives agreement probability1 versus1/2. Thus feedback-relevant process records distinguish the sources by an elementary ordinary intervention, with no environmental tomography or protected reference. With N independent episodes, the rule that rejects the Bell model upon any mismatch has zero Bell false-rejection and product false-acceptance 2^-N. All N source episodes and both measurements per episode are paid.

The accessible output and retained instrument record are jointly essential. The result does not forbid control learning with a richer experiment set, and it does not show that any particular published experiment is misidentified. It isolates the information that a transfer theorem must acquire.

## Minimal repair in this fixed two-qubit preparation/SWAP family

Choosing a Pauli measurement j on S, retaining its +/- result, and measuring Pauli k on the released output determines Tr[omega(sigma_j tensor sigma_k)]. The two marginals are acquired similarly. Nine correlation settings plus marginal data therefore acquire the complete two-qubit initial state in this special family with ordinary measurement records. Standard bounded-mean concentration pays O(epsilon^-2 log(1/beta)) episodes per fixed setting. This is conventional small-state tomography, not a scaling breakthrough; there is no hidden general-process guarantee.

For a genuine new predictive-history framework, the obligation is to acquire only the instrument directions needed by the eventual controller while proving validity under its changing policies and paying memory/horizon/conditioning. The present construction shows why a unitary-only fit cannot discharge that obligation. It does not yet offer stronger leverage than the active fast-recovery and pooled-local-algebra constructions, which remain primary.

## Reproducible evidence

instrument_blindness_check.py/.json checks the two laws on100 random unitary matrices and the exact measurement-record contrast, with numerical residual below5e-16. This is an algebraic model diagnostic with ZERO source samples, not an empirical acquisition experiment. The partial-trace identity above is the all-intervention proof. No internal independent review of this new note is claimed.
