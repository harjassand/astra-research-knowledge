# Primary comparison: do not relabel standard stopping-time machinery

Checked 2026-10-30. This narrows novelty claims; it is not a full novelty search.

- Laurence and Robert, *Scaling Methods for Stochastic Chemical Reaction Networks*, arXiv:2310.01949v3, published in SPA194 (2026): https://arxiv.org/html/2310.01949v3 . Section2.4 states Filonov's stability criterion. The paper explicitly advocates looking at stopping times rather than one jump to avoid local Lyapunov gluing difficulties, and applies that approach to several chemical-network examples, including a bimodal model. Therefore using random-time drift or obtaining recurrence through a trace is conventional prior machinery, not a new principle introduced by this project.
- Athreya, Kolba and Mattingly, *Propagating Lyapunov Functions to Prove Noise-induced Stabilization*, arXiv:1111.1755: https://arxiv.org/abs/1111.1755 . Its construction propagates Lyapunov functions through Poisson equations. Therefore constructing a Lyapunov function as an expected stopped cost is likewise not itself novel.
- Kozyakin, *Hourglass alternative and the finiteness conjecture for the spectral characteristics of sets of non-negative matrices*, arXiv:1507.00492: https://arxiv.org/abs/1507.00492 . Independent-row uncertainty is established positive-matrix machinery. The finite-policy common-resolvent argument here has been proved directly, but should not be advertised as a new general control principle.

What has actually been earned in the present candidate is the explicit infinite-background estimate: exact finite-head exit exponents, summable killed-fiber absorption without mixing, controlled coefficient handling, and complete coupling of two noncompact residual targets with the chemical boundary function. Whether that particular combination/result is new remains unverified.

The primary SPA page returned HTTP403 on direct open; no access workaround was attempted. The public arXiv version supplied the comparison. Earlier general-2D and deterministic-permanence comparisons remain in force and are not displaced by this note.
