# BRAVE comparison scope
Read 2026-10-29. Primary source: Guatto et al., arXiv:2509.03974v2, https://arxiv.org/html/2509.03974v2, Sections II.2–II.3, III.2 and Appendix D.1–D.3.

The paper separates circuit discovery from online variational retuning. The inspected discovery reward uses Knill–Laflamme terms; BRAVE chooses between keeping parameters and Nelder–Mead retraining using logical-fidelity feedback. Appendix D.3 analyzes a differential-equation approximation and discusses nonstationary reward trajectories in a high-sampling regime. These are meaningful prior adaptive-QEC mechanisms.

This does not establish historical priority for Astra. The particular obligations being checked here are finite physical feedback, retained quantum-memory accounting, exact finite controller arithmetic and an accepted-operation correctness map. Those are not interchangeable with a simulated fidelity improvement or a scheduler-regret curve.

A Nelder–Mead or SLSQP fit to Astra's same empirical bank is a legitimate equally informed optimizer comparison, but is not a reproduction of the complete BRAVE pipeline. Our SOS branch itself uses an ordinary optimizer to propose its upper-bound candidate. Its additional product is a verified global lower bound, not necessarily a better candidate or greater protected yield.
