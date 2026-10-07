# Restart: collective thermal bound entanglement

Research state dated 8 October 2026. All mathematical advances are internally derived candidates, not externally reviewed or priority-cleared results. No independent subagents were available.

1. Read [AUDIT_UPDATE.md](AUDIT_UPDATE.md) first. It records decisive Li-Xu prior art, actual fresh execution, corrected filter convention, a new uniform mixing bound, and an explicit all-size finite-time singleton-PPT preparation bound. Its execution counts and hashes supersede those in the older checkpoint.
2. Read [RESULT_AND_RESTART.md](RESULT_AND_RESTART.md) for the detailed stationary-state, singleton-separability, LOCC anti-concentration, regularized-relative-entropy, depth, marginal, noise, extraction, and obstruction arguments, subject to the audit update's precedence.
3. Run [certify_finite_time.py](certify_finite_time.py) with Python 3.10+ and SymPy. It certifies the N=4, nu=1/5, Gamma*t=8 instance by exact rational arithmetic with a rigorous uniformization tail bound. It emits certificate.json. This is not proof-assistant verification.

Main candidate: from the full-space maximally mixed state, ideal collective thermalization yields stationary states separable across every singleton cut above the exact threshold, yet asymptotically at trace distance one from full separability. Regularized relative entropy grows logarithmically despite depth two. Strict-interior bath occupations admit actual finite-time singleton-PPT, strongly non-fully-separable states at a conservative O_nu(N)/Gamma time under unnormalized jumps. Group distillation is possible only with specified joint operations and charged postselection.

The numerical threshold (sqrt(15)-3)/6 and the two-qubit bath-induced effect are already in Li-Xu quant-ph/0505216; do not claim those as new. No NPT-bound-entanglement solution, genuine N-party depth, practical quantum advantage, or robustness to symmetry-breaking noise during preparation is claimed.

The conversation deliverables also include an 11-page research note, numerical diagnostics with source and outputs, actual replay logs, dependencies and an integrity manifest. This repository state preserves the decisive proof arguments and portable exact certificate independently of those attachments.
