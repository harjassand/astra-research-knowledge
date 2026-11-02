# Native two-body thermal memory

Read construction/ROOT_NATIVE_THERMAL_MEMORY_JOIN.md first, then construction/FRESH_NATIVE_CLOSURE_AUDIT.md.

This package contains an exact bounded-qudit two-body clock construction, full low-temperature auxiliary trace proof, actual-code witness transfer, and specified Davies thermal-memory consumer. All thermal clock levels are included. Parameters are fixed in volume but potentially extreme. Ideal Gibbs encoding/readout and exact Hamiltonian structure are assumptions. No generic calibration robustness, practical hardware, or microscopic finite-coupling exponential-time theorem is claimed.

The previously delivered ideal-encoder/actual-code geometry package is included under prerequisites/ideal_encoder for source binding and deterministic fixtures. Its ideal preparation theorem does not automatically prepare this new native model. Earlier proof-target and conditional files remain for history; the root join and final audit govern current scope.

Reproduction uses Python3 with numpy/scipy. Run construction/check_clock.py, root_seed_clock.py, root_finite_beta_winding.py, check_oy_local.py. For construction/root_actual_incidence.py set ASTRA_HOST_FIXTURE to the absolute path of prerequisites/ideal_encoder/host/actual_host_quotient_deterministic_test.py. These are finite corroborations, not substitutes for the family proofs.

Prior machinery: Koenig0901.1333 clock gadgets; Ocko–Yoshida1107.2697 nonperturbative gadgets; Ueltschi math-ph/0304003 signed continuum cluster theorem; Chesi–Loss–Bravyi–Terhal0907.2807 thermal criterion; actual 3D family2605.10943v1. Novelty beyond the explicit comparison has not been established.
