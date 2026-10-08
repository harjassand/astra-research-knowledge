# Astra frontier session handoff — 2026-10-08

Start from `00_START_HERE.txt` and `01_CORE.txt`, then this small pointer file, not the full historical corpus.

## Research state made today

**New highest-upside mathematical candidate (quantum thermal states).** Read `state/2026-10-08-thermal-character-temperature-scaling/RESULT_AND_RESTART.md` and its `NUMERICAL_UPDATE.md`. Contains a fully written derivation of the spin-j thermal character moment-generating identity, uniform subGaussian sector bound, Hoeffding spin-irrep tail, arbitrary fully separable angular Poisson-binomial anti-concentration, and the quantitative full separability distance inequalities. For occupation nu_N=N^alpha, it gives D(rho_N,SEP_N)->1 if alpha<1/2 and ->0 if alpha>1/2. The sharp polynomial scaling exponent is 1/2; the constant critical window nu=c sqrt(N) remains UNRESOLVED. The result is *internally proved as a candidate*, and is not expert-reviewed or priority-cleared. Reproducible 448-character and 15-sector numeric checks are included.

**Decisive established-literature obstruction (group rings).** Read `state/2026-10-08-formanek-frontier/RESEARCH_STATE.md`. The 2007 Bartels-Luck-Reich application paper explicitly invokes Formanek to show F[K] has only 0/1 idempotents for EVERY field F if K is torsion-free hyperbolic. Hence no OA197 characteristic-two non-direct-finiteness witness can coexist with torsion-free hyperbolicity, nor survive as a finite multiplication table in that class; this also excludes torsion-free hyperbolic direct limits and yields a nontrivial residual-kernel corollary. The theorem is OLD, not a breakthrough found by Astra. Does NOT refute nonsofic hyperbolic constructions not asserting group-ring witness. The prior N47 K0-only argument failed correctly; Formanek is independent of that.

**Conditional classical quantum sampler.** Revisit `state/ACTIVE_CONTEXT.txt`, N109-N111, and Chen-Liu arXiv 2610.06724v1. A 135-case finite Hamiltonian gap/Perron stress test passed. No actual end-to-end Chen-Liu FPRAS/compiler has been run; worst-case explicit sufficient schedules are huge and not evidence of immediate hardware practicality.

## One urgent frontier question
Analyze the scaling window `nu=c sqrt(N)` for the stationary sector-preserving collective bath. Is there a nontrivial limiting trace distance from the full-SEP set, an exact critical constant c, or an explicit separable approximant? DO NOT infer it from trace distance to I/2^N alone. The exact Schur-Weyl spin-sector computation provides an upper bound only.

## Independent priority/adversarial checks
Consult Mo-Altman-Garratt, *Thermal entanglement transitions from strong SU(2) symmetry* arXiv:2610.00826; Mathe-Usui-Guhne-Vitagliano, *Estimating the best separable approximation of non-pure spin-squeezed states*, Quantum 10 (2026) 2078; and earlier Li-Xu collective thermal work. These concern related but not identical model/metrics; no exhaustive novelty conclusion established.
Check physical model conditions: unnormalized collective J±, exactly fully mixed initial state, sector weights preserved, known bath occupation, arbitrary fullSEP adversary. Global distance-from-fullSEP does not prove genuine multipartite entanglement or nondistillability across every grouped bipartition.

Research provenance levels: (A) Formanek established; (B) elementary ring corollaries proven here, priority unknown; (C) thermal bounds with written proof, independent specialist review required; (D) finite numerical checks executed, not theorems; (E) implementation/critical-window conjectures OPEN. Do not merge these labels in summaries.
