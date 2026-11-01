# Fixed-controller nonequilibrium Lyapunov prior gate

2026-11-01. Purpose: compare fixed graph-local downhill cooling plus unknown bounded-incidence local coherent perturbation, not just Gibbs dynamics.

## Closest inspected primary sources

1. Liu–Lieu, *Dissipative phase transitions and passive error correction*, PRA109,022422 (2024); inspected arXiv2307.09512v2, 3Aug2023, https://arxiv.org/pdf/2307.09512 . §V uses local 4D toric syndrome-conditioned dissipators, and §V A/Fig8 compares thermal rates with majority-rule rates violating detailed balance. Evidence for the latter is numerical stabilizer autocorrelation and arguments/expectations about protected quantum steady states, not a theorem uniform over unknown coherent perturbations. Appendix F explicitly proposes a coherent-drive topological model as speculation. This is direct architectural precedent for fixed nonequilibrium syndrome cooling; thermal equilibrium is not itself the novel departure.

2. Shtanko et al., *Bounds on Autonomous Quantum Error Correction*, Quantum9,1804 (22Jul2025), arXiv2308.16233v2 (5Jul2025), https://quantum-journal.org/papers/q-2025-07-22-1804/pdf/ . Theorem1 assumes uniform exponential recovery convergence (Eq6), exact correction on error-radius subspaces (Eq8), and no increase in bra/ket error weights (Eq9). Its noise model Eq2 is a sum of dissipators; it does not state arbitrary coherent Hamiltonian perturbations. Eq18 uses eta=(chi+1)Delta||L_E||/kappa, with total norm generally growing with system size. This does not establish bounded-local-rate scalable protection. Their global-decoder lower bound must not be promoted into a no-go for extensively parallel local cooling. Discussion explicitly identifies stronger local-decoder bounds as an opportunity.

3. Rojkov–Zapusek–Reiter, *Scalable dissipative quantum error correction for qubit codes*, arXiv2507.12534v2 (18Mar2026; HTML title date24Aug2026), https://arxiv.org/html/2507.12534v2 . Already proposes fixed-rate trickle-down correction with polynomially many jump operators. Eq4 contains sums of exponentially many error-subspace projectors; the repetition example explicitly disregards nonlocality. Setting uses purely incoherent noise/correction. Repetition performance is numerical for n=3,5,...,13; implementation uses global motional modes and resonant weight selection. This does not earn bounded-incidence local generators or arbitrary coherent-perturbation logical-memory bounds. Generic fixed-rate weight reduction is prior; physically local decidability and complete coherent robustness are the consequential distinctions.

## Judgment and decisive remaining test

No inspected result supplies the complete proposed contract. This is not a novelty certification. The hard new theorem must attach the Lyapunov drift to an actual fixed bounded-support generator, not a global minimum-weight/error-class oracle. A decoding algorithm which eventually finds an improving move does not imply that a constant fraction of local clocks are simultaneously improving. Likewise, syndrome energy occupation alone does not identify logical history; a censored-basin or equivalent recovery argument must control logical coherences, including entangled inputs. Expander graph locality must be charged as long-range physical connectivity, not Euclidean locality.

The useful capability, if established, is a quantum-memory threshold with fixed controller, finite per-site rate, no clean classical layer, and robustness to an unknown coherent perturbation. Lyapunov methods or cooling alone are not that capability.

## Access ledger addition

https://www.nature.com/articles/s41467-024-55570-7 opened once: nonretryable500 redirect to idp.nature.com authorization, inaccessible. STOPPED; no PMC/PDF/arXiv alternate retrieved. Primary search extract only supports Gibbs/time-reversal-symmetric scope; cannot assess full theorem.

Inherited stop retained: s41467-026-75465-z 'Universal energy-space localization...' had parent auth500; no full-text/alternate retrieval. Search engine surfaced its excerpt incidentally; no theorem comparison made from it. Other inherited stops unchanged.
