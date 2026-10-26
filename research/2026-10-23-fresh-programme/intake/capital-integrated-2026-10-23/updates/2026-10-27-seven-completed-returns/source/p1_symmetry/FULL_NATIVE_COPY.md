## ASTRA — Stronger result: quantum fault certification from a conserved symmetry

The differential parity meter has a more useful protection mechanism than precisely matched exchange and detector strengths.

Define the combined rail–ancilla symmetry

\\[ S=X_L Z_a, \\]

where \\(X_L\\) exchanges the two logical rails and \\(Z_a\\) acts on the detector ancilla.

If the complete in-code Hamiltonian satisfies

\\[ [H(t),S]=0 \\]

throughout the operation, then every successful detector branch contains only logical \\(Y\\) and \\(Z\\) terms, even when the bath strongly and noncommutatively modulates the physical couplings.

The resulting successful operation has the form

\\[ K\_{\rm pass}=Y_L\otimes A_M+Z_L\otimes B_M. \\]

No bath dimension, reset, mixing-time or scalar-coupling assumption is needed for this identity.

### A particularly useful consequence

If the detector processes one half of a fresh Bell pair and the actual unknown input is teleported only after success, completed teleportation automatically removes the interference between these two terms.

After a known logical \\(Z_L\\) correction, the delivered operation admits exact positive branches:

\\[ \mathcal T(\rho) = (I\otimes\Phi\_{\rm good})(\rho) + (X_L\otimes\Phi\_{\rm bad})(\rho). \\]

The bath remains present in both completely positive maps.

A destructive measurement of just \\(Z_RZ_L\\) on a sacrificial Bell pair identifies the matching fault effect. No additional secret Pauli-frame randomization is required in this entanglement-first arrangement.

Full-memory numerical validation

| Completed teleportation versus positive paths      | \\(2.64\times10^{-16}\\) |
| -------------------------------------------------- | ------------------------ |
| One-basis test versus actual bath fault instrument | \\(1.71\times10^{-16}\\) |
| Uncorrected coherent direct-use discrepancy        | 0.1172                   |

The model contains four time-dependent Hamiltonian segments with noncommuting bath couplings and an input initially correlated with both the bath and an untouched reference.

The distinction matters: a direct unrandomized use can retain coherent error interference, but the completed teleportation task removes it physically. This is conditional mathematics, not an experimental demonstration or an independent claim of novelty.

### New availability theorem — and its unavoidable limitation

A successful herald must occur often enough to make the service useful. Exact symmetry protects correctness but says nothing about how frequently the detector succeeds.

I derived a separate short-pulse theorem. Suppose the intended detector coupling \\(\Lambda\\) has minimum singular value \\(\ell>0\\), the total controllable interaction has norm at most \\(v\\), and the coupling varies in the bath's interaction picture at a rate bounded by \\(\kappa\\).

Then a pulse of duration \\(t\\) has a state-independent success probability of at least

\\[ \boxed{ P\_{\rm herald}\ge \left[ \ell t-\frac{\kappa+v^2}{2}t^2 \right]\_+^2. } \\]

This bound covers arbitrary incoming bath states and references. It does not depend on the bath's full Hamiltonian norm.

In the executed noncommuting-bath example, a duration of \\(0.30463\\) gave a worst-case simulated success probability of 2.818%, compared with the rigorous lower bound of 0.702%.

For fresh independent Bell candidates and a valid bound at every attempt, the probability of \\(m\\) consecutive rejections is consequently at most \\((1-s_0)^m\\), where \\(s_0\\) is the uniform lower bound. The bath need not reset between attempts.

A counterexample establishes why the regularity assumption is essential. With an invertible detector coupling \\(\Lambda=Z_M\\) but an arbitrarily fast bath Hamiltonian \\(\Omega X_M\\),

\\[ P\_{\rm herald} = \frac{\sin^2(t\sqrt{\Omega^2+1})}{\Omega^2+1}. \\]

The success probability can approach zero as \\(\Omega\\) increases, even though the coupling never loses its spectral gap.

This separates the two physical resources that the construction needs: a conserved symmetry for integrity, and a quantitative interaction-timescale condition for availability.

## Executed adaptive operation

The revised controller includes a 2.5% test-report flip probability, adaptive control settings, private late test/use choices, and an unrepresented, never-reset quantum bath.

80 trajectories per configuration · 99% all-prefix confidence · 75-fault budget

| Symmetry-breaking amplitude | Mean completed uses | Mean hidden faults | Mean certified upper bound |
| --------------------------- | ------------------- | ------------------ | -------------------------- |
| 0                           | 175.7               | 32.2               | 67.8                       |
| 0.04                        | 176.2               | 32.0               | 69.9                       |
| 0.10                        | 153.1               | 29.4               | 73.5                       |

No confidence-bound violations occurred in the 240 simulated trajectories. The theorem supplies the confidence guarantee; these runs only check its finite-dimensional implementation.

A further physical improvement survived: the unwanted pointer subspace can tolerate strong ancilla–bath dephasing, provided that interaction conserves the ancilla's measured \\(Z\\) observable. Forty random, strongly interacting symmetry-preserving Hamiltonians passed the operator checks. The strongest tested Hamiltonian had norm approximately 26.45, without introducing forbidden logical components.

The meaningful comparison is with a conventional controller given the same ports. Under exact symmetry, the single \\(ZZ\\) test detects the relevant fault with contrast 1, versus \\(2/3\\) for a uniformly random three-axis test. Both controllers can exploit this. When symmetry cannot be physically justified, full Bell testing is the safer alternative.

### Preserved technical state

Complete mathematical derivation

Symmetry theorem, complete-memory teleportation identity, sequential certificate, liveness bound, proofs and counterexamples

Reproducible research archive

Six Python research programs, executed numerical results, validation scripts, logs, checksums and compact Pro1 handoff

The five short numerical studies passed the consolidated validation. The full 240-trajectory ensemble was executed separately and its saved output independently audited; a later combined rerun exceeded its execution window.

Scientific assessment: This replaces detailed knowledge of the bath-modulated coupling strengths with a conserved physical symmetry, while retaining exact task-relative fault certification. The component methods have extensive prior art in parity measurement, teleportation and dual-rail quantum control, including demonstrated hardware.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

npj Quantum Information

+2



The strongest next physical target is to establish a complete-boundary bound on violations of \\(S=X_LZ_a\\), including finite pulse transitions and readout backaction. That would test whether this lower-control architecture can be implemented without losing the quantum-memory guarantee.