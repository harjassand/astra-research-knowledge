# Sources and verification

The finite-window comparison uses the exact singleton F from imperfect_refresh_product/PROOF.md and the private-parity tester construction from causal_refresh_product/PROOF.md. Both delivered prerequisite packets are included unchanged.

The causal positive-domination theorem is established mathematics: Gutoski and Watrous, *Toward a General Theory of Quantum Games* (2007), Theorem 9, printed p.13, https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf . The new application here is the specific finite-controller embedding and local action comparison, not a claim to invent the general all-pass product theorem.

The projective-angle comparison is proved in the artifact from bounded generator speed and the triangle inequality. It is a standard state-distance argument, not a newly claimed general speed-limit theorem.

The parent and a separate internal mathematical reviewer independently checked the privacy/reference commutation, purified adaptive-strategy comparison, complex-coherence phase absorption, angle lift, and the need to leave the random controller outside the H0 interaction picture. These are internal mathematical checks, not external validation or peer review.

check_finite_window.py is newly authored deterministic Python/NumPy code. Six fixed cases directly exponentiate the simultaneous private controller plus odd Hamiltonian on three levels and compare the purified actual/reference states. They cover zero concurrent action, nonzero action, a complex phase average, a saturated certificate, and zero outside action. No optimization or acquired code is used. State angle is computed from the phase-aligned chord to avoid arccos loss of precision at coincident states. Largest observed probability-minus-bound residual is 2.23e-16, consistent with roundoff; all charged-angle and singleton checks pass.

Replay from the extracted root: python finite_private_z_refresh/check_finite_window.py .

The exact sample-dependent phase-cancellation example in the proof demonstrates a real failure when controller privacy is dropped. It is deliberately outside the theorem, not a counterexample to it.

Scope remains an exact mathematical control contract. Isolated reduced-memory calibration does not certify it; no device bandwidth, private-randomness isolation, crosstalk, physical parity accessibility, wall power, or finite-window optimality is established.
