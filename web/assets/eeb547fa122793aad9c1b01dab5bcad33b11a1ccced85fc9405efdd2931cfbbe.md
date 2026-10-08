# Source and replay ledger

## Astra snapshot

Astra knowledge commit: 8ede33c2f09a8abe07b430892b3ac4bb71c27c83. The local file-path index reports this SHA at work/astra_prior/tree.json:2. All Astra raw-source URLs below pin this exact commit. The fixed base is:

https://raw.githubusercontent.com/harjassand/astra-research-knowledge/8ede33c2f09a8abe07b430892b3ac4bb71c27c83/

This is evidence retrieval, not a claim that the imported documents' results are externally certified. The P/U/R source maps are the navigation record.

## Retrieved cards and exact relevant ranges

| Record | Pinned raw path | Reconstructed use |
|---|---|---|
| N33 | cards/N33-endotactic-permanence.txt | Lines 1–10 give the deterministic measurable-rate interface, classwise common absorber quantifiers, no uniform entry time over an unbounded class, and internal/unreviewed status. |
| N34 | cards/N34-reaction-certificates.txt | Lines 1–6 distinguish finite local/chain certificates from all-scale global recognition; UNKNOWN and acquisition costs retained. |
| N35 | cards/N35-controlled-chemical-safety.txt | Lines 1–8 give the integer-complex stochastic interface, explicit exponential finite-horizon exit bound, and limit against all-time permanence. |
| N76 | cards/N76-factorial-reaction-boundary.txt | Lines 1–9 provide the source-reported falling-factorial potential boundary and explicitly say the argument does not prove recurrence. Full U proof packet unavailable. |
| N77 | cards/N77-stationary-tightness-counterexample.txt | Lines 1–9 summarize the exact counterexample, quantifiers, positive recurrence per component, and missing proof packet. |
| N50 | cards/N50-global-reaction-recognizer.txt | Lines 1–10 state that all-scale recognition is conditional on rational affine reconstruction and no general CAD service/cost bound is supplied. |

Card hashes (SHA-256):
- N33: 623ea4f8b0adc22efa07241e69a2eb7c89bafe26057fb013999220c6edfbae39
- N34: b31168df7ac1e79d938fdabc6efa8fc1353e4c58e944cd4b3ced6d82e1a7982c
- N35: 18e64e381e7a30ec19ef54a752fc1d978ed6f3ab372581514123d64c2d3aeddc
- N76: df45e22dc600f2c29b97d57e5bb317d3f60d5ad985629c4828c038f3caa28f91
- N77: b83784fda869be617da6ab54e68d425763a933e9e6ab53514522e6ec6a22cfdf
- N50: 3dd302678c7779f2e12ea1ead4ad0e1d31ff2916dcadc1375dc42e4b62d0264b

## Exact proof and report ranges from the pinned package

The P source map is work/agents/systems_metabolism/stochastic_safety/web-P-sources.txt:1–23. It identifies d-326696af15b5e02b as the exact UTF-8 source of updates/P/package/outputs/endotactic_permanence.tex, d-875b111adc8e6f6f as the certificate implementation, and d-2ec840427df7f89d as the example fixture.

The source page web/pages/d-326696af15b5e02b.html was extracted from its preformatted payload into evidence/endotactic_permanence.tex. Its original TeX line numbering is preserved:
- Lines 103–140: classwise deterministic theorem, assumptions, and its source/internal proof-status boundary.
- Lines 461–508: weighted essential-source domination, the strict drift lemma used by the deterministic candidate.
- Lines 537–675: global compact plateau, finite-affine-min chain rule, invariance, and finite-entry proposition.
- Lines 681–735: scale iteration that constructs the common absorber on an unbounded positive class; entry time depends on the initial point.
- Lines 1173–1216: stochastic jump-process legal interface and supplied initial buffer/coset constraints.
- Lines 1218–1234: factorial correction proof.
- Lines 1236–1309: explicit controlled exit theorem and complete stopped-generator proof.

Source page SHA-256: c46f4aa1459a06536aea788b1483517a147dd72ffa753f915cc77bf3463c6810.
Extracted TeX SHA-256: bbecea61cd373a787920bb4484494114b7d616d5f20ee096cae3831487707e9c.

The U source map is web-U-sources.txt:1–20. Lines 1–13 say the underlying archive, technical note, code, and logs were not supplied or located. The exact attached summary bytes are the payload of web/pages/d-14513a2bef6ac3df.html and are extracted into evidence/u_summary.txt (SHA-256 b28e6250dafe25ae85999a1a67e85841796cea13806771b40091a0b60ceb6d5e). Lines 156–220 of that summary state the deterministic/stochastic quantifier mismatch, network, classes, claimed stationary law, and limits. These are the ranges reconstructed independently in OBSTRUCTION.md.

The R source map is web-R-sources.txt:1–26 and its result summary is web-R-reports.txt:29–33. The full acquired-certificate report is extracted into evidence/global_reaction_recognizer.md; lines 1–9 state its conditional status and input/output; lines 27–76 give finite QE obligations, direct soundness proof, and conditional completeness. SHA-256: 16dde74d1c0a10dcbac877f964da718675a219b3bde60a1c2a0ae6a72040018b.

## Primary literature checks

- Craciun, Toric Differential Inclusions and a Proof of the Global Attractor Conjecture, arXiv:1501.02860. Primary HTML source: https://arxiv.org/html/1501.02860. The abstract states the complex-balanced compatibility-class result at lines 53–63; Theorem D states the global-attractor conclusion at lines 152–154.
- Anderson, A proof of the Global Attractor Conjecture in the single linkage class case, arXiv:1101.0761. Primary HTML source: https://arxiv.org/html/1101.0761. Corollary 28 at lines 576–584 covers a complex-balanced system with one linkage class.
- Anderson, Craciun, and Kurtz, Product-form stationary distributions for deficiency zero chemical reaction networks, arXiv:0803.3042. Primary HTML source: https://arxiv.org/html/0803.3042. Theorem 4.1 at lines 190–208 gives the product-Poisson stationary law on closed irreducible classes; the classical scaling and Theorem 4.3 appear at lines 224–254. Our phase-balance derivation is direct.
- Anderson, Cappelletti, and Kim, Stochastically modeled weakly reversible reaction networks with a single linkage class, arXiv:1904.08967. Primary abstract: https://arxiv.org/abs/1904.08967. Its recurrence result requires additional structural assumptions; no converse is inferred here.

## Bounded exact check

Command:
python3 work/agents/systems_metabolism/stochastic_safety/check_balance.py

Observed output:
PASS: 41107 exact Fraction identities; n=0..100, d=0..100
Scope: finite balance consistency only; no proof of the all-n claim or external validity.

The finite sweep checks phase edge fluxes, D birth/death ratios, and the full local balance at phase one. The argument for arbitrary n and d is the symbolic calculation in OBSTRUCTION.md. The check does not certify the deterministic global-attractor theorem, physical rate realization, historical novelty, or source-reported fixture totals.

These N33 ranges are retained as source candidate proof ranges, not as the basis of SS-1. They remain internally reconstructed and externally unvalidated as stated in the pinned manuscript and N33 card.
