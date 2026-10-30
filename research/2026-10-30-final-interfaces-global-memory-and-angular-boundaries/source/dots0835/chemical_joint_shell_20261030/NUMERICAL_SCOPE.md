# Numerical scope and conventions

These scripts are exploratory screens, NOT recurrence certificates.

* joint_matrix.py freezes total N and keeps composition/phase dynamics. Its negative near-zero eigenvalues do not control actual interlevel shifts.
* arrival_matrix.py inserts exact predecessor-rate changes but freezes the profile's level argument. Positive near-zero eigenvalues show why those shifts cannot be discarded merely because rates have relative O(1/N) changes. Non-normal eigensolver outputs are not rigorous spectral enclosures.
* residual_matrix.py uses crude maximal-source offsets. Positive eigenvalues appear once a fixed absolute-tilt slack is added on larger phase strips.
* phase_heights.py computes exact phase-tree degrees using symbolic determinants. No networkx installation was available; no installation or permission workaround was attempted. The exact reflected-phase offsets for K=8 and12 are recorded in the scripts.
* tree_residual_matrix.py uses those exact tree offsets. Initial spectral screens are improved but do not prove Hurwitz stability for all levels, and do not prove the actual adjoint inequality.
* check_actual_joint.py constructs finite-level positive candidate vectors and evaluates the ACTUAL mass-action adjoint including neighboring residual levels, phase changes, and composition endpoints. Its results, including all failures, are saved separately.

All B-strip exits are treated as killing in these numerical models; incoming forcing and outgoing feedback from the complementary bulk have NOT been certified. No finite-grid success could by itself close that obligation.
