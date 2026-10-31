# Comparator and diagnostic notes
31 October 2026. Limited primary-source inspection; not a novelty review.

## Quantum trajectories
Borras and Marvian, Quantum 10,2063 (2026), arXiv2509.10425v2, Section3 uses a scalar total jump intensity: sum L_mu^dagger L_mu=Gamma I. This enables state-independent holding-time sampling. The common-loss reservoir considered here instead has sum J_i^dagger J_i=4lambda N; its state can coherently span number sectors. Their scalar-intensity construction therefore does not directly supply the present first-event procedure. This is only a model comparison, not a general impossibility or novelty claim. Source: https://arxiv.org/html/2509.10425v2 .

## General causal query compilation
Kitchen, arXiv2609.31312 (2026), gives time-dependent Lindblad query bounds governed by tau=T(alpha_H+sum alpha_mu^2), and local gate results under fixed-local-parameter assumptions. Its compiled-record occupation estimates include number-preserving operations and weighted tails, so those principles are not themselves new. Applying the displayed general oracle normalization directly to finite-cutoff physical jumps retains the microscopic damping scale. Whether its machinery can be specialized further to this structured source is not ruled out. Source: https://arxiv.org/html/2609.31312 .

## Executed diagnostic
check_graded_sector_bounds.py constructed a two-mode total-number cutoff3 with noncommuting system couplings, one non-Hermitian, plus Kerr and hopping terms. It checked the removal isometry, normalized raising sector bounds, R_plus R_plus^dagger<=g^2N, and commutation of H_f with N. Numerical residuals were below6e-16. A finite tilted-generator count moment was1.0078419722 against upper bound1.0391076608. These small-matrix computations are diagnostics, not a compiler implementation, practical benchmark or proof of the infinite-domain claims. Exact parameters and outputs are in the script/JSON.
