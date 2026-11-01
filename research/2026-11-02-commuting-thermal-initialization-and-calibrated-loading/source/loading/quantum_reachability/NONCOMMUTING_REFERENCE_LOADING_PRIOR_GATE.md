# Weak noncommuting loading from a low-temperature commuting reference

2026-11-01. Focused primary-source gate; not a historical priority assessment. Target: actual 3D recursive code with a constructive classical Gibbs-syndrome sampler, fixed-strength weak noncommuting perturbation, preferably preserving an unknown encoded input and its reference entanglement.

## Decision

**No inspected theorem closes the complete polynomial, physical, input-preserving loader. The closest established bridge is the Ma–Khemani–Sang phase-channel theorem; proving its hypotheses would earn a genuine deterministic local-channel existence result, but not by itself the requested polynomial native implementation.** Positivity of an operator or convergent expansion is not this implementation.

## 1. Strongest phase bridge

[Ma–Khemani–Sang, arXiv:2509.15204v3](https://arxiv.org/html/2509.15204v3), Theorem 1, Definition 2, Eq.13, Eq.17: stable clustering throughout a coupling path implies a locally reversible CPTP circuit between endpoint Gibbs states, with polylogarithmic range. Clustering tests an interior observable against an arbitrary exterior observable across an annulus, uniformly over a small coupling neighborhood. The elementary channel erases an interior and applies a rotated Petz recovery map built from the **target** marginal. At fixed inverse temperature, their radii can be chosen r1=O(log(L/error)) and r2=O(r1^D+log(L/error)). Section VI explicitly leaves efficient short-time dissipative implementation unresolved. Theorem 4's improved continuous-time construction is for commuting paths only. The paper also does not identify low-temperature analyticity with its stronger clustering assumption.

**Instance audit (our inference):** include the allowed perturbation operators in the fixed local interaction basis, and prove this annular, neighborhood-uniform estimate along H(s)=H0+sV. A diagonal syndrome Peierls bound alone is not that estimate. With D=3, the displayed construction can involve O(log^9(n/error)) spins per gate; dense synthesis is exp(polylog(n/error)), not polynomial. This is an upper-bound accounting obstacle, not a lower bound against better synthesis. Furthermore, the required target marginals are not supplied by a sampler for H0. Sparse cluster representations might help, but require a positive, implementable recovery construction rather than signed expectation evaluation.

Local reversibility on a specified mixed state is not automatically diamond-norm reversibility on every unknown logical input. One must prove a correctable-region/subsystem statement for each gate on the actual thermally encoded family (including a reference), and identify the resulting encoding with a state admitted by the storage theorem. A transformed encoding can be useful without being the original fixed logical-overwrite encoding; they must not be silently equated.

## 2. A genuine reference-to-target algorithm, with the wrong extensive cost

[Holmes et al., Quantum 6,825 (2022), arXiv:2203.08882v2](https://arxiv.org/pdf/2203.08882), Theorem 1.2 and Section 3.2: given a unitary U0 preparing a reference Gibbs purification, its inverse, and controlled Hamiltonian/work evolutions, amplitude amplification prepares the target purification. The round count is O(exp(sqrt(log(1/error))) exp(beta(Delta F-w_cut)/2)); the cutoff controls the exponentially weighted work tail. Corollary 1.7 gives generic local-system bounds still exponential in beta times the total perturbation norm. A useful nonequilibrium drive can improve the work cutoff, but must itself be constructed and charged.

**Instance audit (our inference):** fixed local strength epsilon allows ||V||=O(epsilon n), so the stated generic guarantee is not polynomial. Classical sampling of syndrome probabilities is not automatically coherent preparation of their square-root amplitudes with a reversible oracle. Purifying a reversible randomized sampler leaves seed/history garbage; equivalence to the particular purification required by the work construction must be shown. Splitting V into tiny steps does not make the total success probability free: successive postselection or nested preparation/reflection costs need an end-to-end bound. A tailored work-tail estimate and an efficient drive could change the verdict, but neither follows from weak local coupling alone.

## 3. Why the other familiar methods do not settle this instance

- [Hastings, Quantum Belief Propagation, arXiv:0706.4094v3, 7 February 2008](https://arxiv.org/pdf/0706.4094): the thermal perturbation evolution underlies a 1D numerical algorithm. Its useful quasi-locality is not a trace-preserving physical implementation of each normalized filter. Our inference: local filters with constant success cannot simply be multiplied across n regions without charging failures or proving local repair.
- [Brandao–Kastoryano, arXiv:1609.07877, retrieved PDF dated 13 February 2019](https://arxiv.org/pdf/1609.07877), Theorems 5–6: uniform clustering and approximate Markov properties are required for Gibbs states on all induced subgraphs, including noncontractible geometries. This is substantially stronger than the available syndrome sampler or full-volume Peierls bound and is specifically problematic for protected thermal topology. Their channel model also needs implementation accounting.
- [Smid–Meister–Berta–Bondesan, arXiv:2510.04954v1](https://arxiv.org/html/2510.04954v1), Theorem III.3: H0 is a sum of **on-site** qudit Hamiltonians; exponentially decaying weak interactions preserve rapid mixing when d^2 eta<Delta0. The bound is logarithmic in n/error with explicit temperature factors. This does not cover a strongly correlated commuting code reference. Our inference: globally diagonalizing stabilizers destroys the physical locality premise. A fast classical full-syndrome sampler likewise does not establish a local quantum Gibbs-generator gap.

## 4. Physical contract needed before claiming a closed gate

A sufficient next result would provide, for this actual code, a polynomial-size native circuit for each needed recovery/update, with an end-to-end trace-error bound and a reference-safe logical action. Charge Hamiltonian access/calibration, ancilla initialization, resets, routing, and all failures. A conservative global calibration budget scales with the sum of local coefficient errors; fixed per-site error does not automatically yield vanishing global Gibbs error. A weaker storage-admission norm may avoid this accuracy requirement, but needs its own proof.

If bath spins are part of the target, these algorithms require the stated controls/oracles on that enlarged finite system. Uniform storage bounds in bath volume do not provide uniform preparation cost or bath controllability. The root's conserved-sector stationary reference is a legitimate weaker target, but still needs accessible conditional preparation; it is not generated by the phase theorem for free.

**Most useful next target:** implementable, logical-reference-safe local conditional refresh for the weakly perturbed code, rather than another positivity argument. Stable clustering plus a polynomial recovery implementation would close an important gate using established phase machinery; either alone leaves an essential operation missing.

## Access record

All previously notified work-level stops preserved. New unsuccessful action: open https://arxiv.org/html/2504.02208v2 returned HTTP 404. Status: unavailable at that target, work left pending/uncertain; no alternate version or mirror attempted. Its Markov lemma was considered only as explicitly stated inside the successfully read Ma–Khemani–Sang source, not independently verified/imported. No external mutations.
