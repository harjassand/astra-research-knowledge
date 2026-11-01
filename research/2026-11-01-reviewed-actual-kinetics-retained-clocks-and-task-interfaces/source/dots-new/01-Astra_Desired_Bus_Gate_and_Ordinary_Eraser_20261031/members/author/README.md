# Desired-operation bus: ordinary quantum erasure first

Author candidate, not independently accepted and not hardware. Unlike the preceding nuisance-source receiver, this bus itself supplies the useful maximally entangling ZZ gate. The winner is ordinary closed-trajectory geometric control plus no-knowledge homodyne/local correction.

- Exact global displacement factorization and full-access erasure even for a warm, initially correlated linear apparatus.
- Finite-slew sin² drive, actual passive single-pole filter, finite observation tail, finite ADC/local correction, and continuing data noise.
- Exact complete diamond formula and small-loss minimax optimality against arbitrary deterministic postprocessing on data plus the same collected field.
- Exact force-energy / entangling-phase / unobserved-exposure lower bound. Within the fixed-B vacuum force class, reoptimizing an unmonitored pulse under the same cap/time cannot reach the supplied target.
- β=8 receiver supplied-model bound 0.007417123668633808, versus an all-closed-pulse unmonitored lower bound 0.1614815538202856. β=1,2,4 failures remain in the certificate.

Read `CLOSED_BUS_ERASURE_CANDIDATE.md` for exact assumptions and limits. A matched-mode homodyne instrument, drive/LO/receiver calibration, physical linearity, controlled shutdown and the residual 0.001 complete-error allowance are supplied services, NOT acquired capabilities. Finite filter linewidth does not certify ideal homodyne electronics. The finite-efficiency error budget is vacuum-specific; arbitrary warm lost modes need their actual quadrature law/energy. No source Markov admission or classical simulation theorem is being rebranded as a physical bath.

Run `python certify_bus.py` and `python test_bus.py` in a COPY of this directory. The first is an exact dyadic/rational interval certificate (standard library only); the second uses NumPy, SciPy, SymPy and mpmath for 72 checks, including six finite-Fock diagnostics. Cutoff convergence is not an infinite-mode proof. The global linear model is solved analytically, without an adiabatic limit.

The useful selection result is that ordinary machinery already supplies this task. No novelty or broad architectural advantage is claimed. Encoded, multi-mode, squeezed-input, variable-B, coherent-reuse and avoidance architectures remain alternatives. The original energy-admission machinery can help only after a genuinely necessary non-Gaussian/continuing physical component is identified and its extra service is received; further symbolic coverage by itself is not the next capability.
