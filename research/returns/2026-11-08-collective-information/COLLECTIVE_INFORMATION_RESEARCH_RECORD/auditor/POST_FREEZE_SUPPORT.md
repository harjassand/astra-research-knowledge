# Post-freeze supporting checks

The independently frozen initial report remains ../initial/auditor.md with SHA256 a873c6ad44620e3f16d5e27035c41e352b8f3498aec2ee969f0f822d4db1750e. This file records subsequent primary-source completion and finite diagnostics; it does not alter that report.

## Source completion: Zenodo 22722557

The initial file download was incomplete, and a retry of its API content link returned HTTP 403. A subsequent public-record file download succeeded. The downloaded 19-page primary PDF has SHA256 1b6c8648b2fa6ad1fe4e1f2aed77da99c666478ddb375896a866a0d8ef918b9d; 381260 bytes. See source/zenodo-22722557.pdf and its extracted text.

The paper is Kosuke Watanabe, *Mori–Zwanzig Perspective on Neural Representation Dynamics: Coarse-Graining via Short-Memory Closure*. It explicitly treats a local resolved–unresolved linear surrogate around a trained-network operating regime:

a_(ell+1)=M a_ell+N xi_ell,
xi_(ell+1)=P a_ell+Q xi_ell.

Proposition 1 gives exact elimination within this surrogate, K_tau=N Q^(tau-1) P and initial force eta_ell=N Q^ell xi_0. Proposition 2 assumes ||Q||<=1-gamma, ||N||<=delta_N and ||P||<=delta_P and derives ||K_tau||<=delta_N delta_P (1-gamma)^(tau-1), total mass <=delta_N delta_P/gamma and lag-L tail <=delta_N delta_P(1-gamma)^L/gamma. These follow directly by submultiplicativity and geometric summation. Neither the rank/dimension nor decay assumptions are derived for arbitrary physical many-body models. Appendix A.4 explicitly presents a geometry argument as informal rather than a complete theorem for arbitrary nonlinear networks. The empirical closure score is held-out next-stage prediction R^2 across selected finite neural tasks. There is no need to refute the valid linear-algebra identity; the missing physical acquisition/control/uniformity operation remains separate.

Primary record: https://zenodo.org/records/22722557 .

## Finite diagnostics

checks/check_obstructions.py constructs the four-state generators independently, checks symmetry, positivity, row sums and both generator-observable identities across 16 parameter pairs, and verifies the exact propagated response formula at five times each. It also checks the positive lift's contraction and a 1000-segment changed-drive numerical robustness example. These are finite diagnostics supplementing the analytic proof, not a substitute.

The resulting four-state gap at gamma=.1,u=.75,t=1 is 0.17101050612759605. The thermodynamic kinetic-clock gap is 0.2362351968552887. The rare-clock gap is 0.11701964434787852. Exact enumeration through N=8 verifies the detector-parity channel formula and its preservation under count compression. All checks pass; full result is checks/check_obstructions_result.json.

No physical experiment was performed; no historical novelty or practical advantage is established.

## Governing file pins

- outputs/REUSABLE_INTERVENTION_PREDICTION_RESEARCH_DOSSIER.md: SHA256 0d8e4683aa41a6ca5ac7827db8c4d34220d1d0f20ac5782755c23f68fb32c51d.
- outputs/RESEARCH_TO_PUBLICATION_WORKFLOW.md: SHA256 251d8f54bfba73600a126749a27218d02d9dce692c40a88ea57f026775b618ab.
- AGENTS.md: SHA256 b34ee3b263d2ad31cc8fa1be2331a19d9d78a32ce9c131cf97ed398deb2ae68b.
