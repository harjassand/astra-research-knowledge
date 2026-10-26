## ASTRA — Protecting the coherent symmetry checker

The strongest new construction protects the check ancilla itself, rather than requiring detailed knowledge of the uncontrolled quantum interaction.

The previous eight-gate checker could eliminate arbitrary symmetry-breaking errors, but only while its single check qubit preserved coherent interference. An interacting bath that learned which check path was taken could defeat the certificate.

### New construction: an encoded check flag

Replace that single check qubit with two physical qubits:

\\[ |0_F\rangle=|01\rangle,\qquad |1_F\rangle=|10\rangle. \\]

These states form a decoherence-free subspace against collective \\(Z\\)-noise. For an arbitrary bath operator \\(B_M(t)\\),

\\[ (Z\_{f_1}+Z\_{f_2})\otimes B_M(t) \\]

acts as zero on both encoded states.

The existing controlled-Pauli checks can use \\(f_1\\) as their physical control without leaving the protected subspace. Therefore, no additional controlled-Pauli gates are required.

More importantly, this protection is exact even when the collective noise is arbitrarily strong, changes with time, and does not commute with the bath's own dynamics.

### Executed full-memory checks

64-dimensional quantum reference calculation

| Collective coupling strength | Complete operator residual |
| ---------------------------- | -------------------------- |
| 0                            | 2.51 × 10⁻¹⁶               |
| 5                            | 3.09 × 10⁻¹⁶               |
| 40                           | 6.27 × 10⁻¹⁶               |
| 250                          | 8.96 × 10⁻¹⁵               |

The encoded checker reproduces the original ideal symmetry-filter operation, including the retained bath. This was also verified while collective noise acted during finite-duration control pulses.

The result removes a potentially unbounded collective-noise term from the checker’s error budget. It does not remove differential noise, flag leakage, target-gate errors or readout imperfections.

### Stronger result: fourth-order suppression of flag leakage

The encoded checker has another useful property. If an unwanted Hamiltonian only couples the valid flag subspace to states outside it, the final encoded readout rejects first-order leakage.

Let

\\[ L=\int_0^T\\|Q_FH(t)P_F\\|\\,dt, \\]

where \\(P_F\\) projects onto the encoded flag and \\(Q_F=I-P_F\\). Assuming the reference evolution preserves this code and the perturbation has no in-code component, the accepted operation differs from the ideal checker by at most

\\[ \boxed{\\|\Delta K\_{\rm accepted}\\|\le L^2/2.} \\]

Consequently, a previously forbidden accepted fault has an operator-effect bound

\\[ \boxed{W\_{\rm forbidden}\preceq L^4I/4.} \\]

This is a fourth-order fault-probability guarantee, although the probability of a detected flag erasure remains second order.

A separate bound covers simultaneous differential noise. If its integrated in-code norm is \\(D\\), the accepted-amplitude allowance becomes

\\[ \\|\Delta K\_{\rm accepted}\\|\le D+\frac{L^2}{2}. \\]

The result places no bound on the Hamiltonian acting entirely outside the flag code.

Nonzero coherent-leakage witness · Interaction duration 0.8

| Leakage strength | Actual forbidden fault weight | Proven ceiling |
| ---------------- | ----------------------------- | -------------- |
| 0.04             | 6.53 × 10⁻⁸                   | 2.62 × 10⁻⁷    |
| 0.08             | 1.04 × 10⁻⁶                   | 4.19 × 10⁻⁶    |
| 0.16             | 1.67 × 10⁻⁵                   | 6.71 × 10⁻⁵    |

The numerical witness shows that fourth-order behavior is achievable but not exact cancellation. In contrast, differential noise inside the code gives an accepted error probability \\(\sin^2 D\\), so the same improvement cannot be claimed for it.

## Further attack: protection against all three collective noise axes

I extended the construction to arbitrary collective \\(X/Y/Z\\) noise using three physical flag spins.

Their spin-\\(\tfrac12\\) noiseless subsystem contains a protected logical qubit and a separate gauge qubit. The bath may disturb the gauge while the logical check remains coherent.

An encoded singlet-controlled Pauli operation gives the same ideal symmetry filter. In a 128-dimensional full-memory reference calculation, its maximum discrepancy was \\(2.56\times10^{-14}\\), even with noncommuting collective noise of strength 150.

However, the implementation study found a decisive obstacle: none of the 27 independent single-flag-spin-to-target Pauli couplings commutes with the complete collective \\(SU(2)\\) noise algebra, except the zero combination. The linear-algebra check had rank 27 out of 27.

The three-spin approach therefore needs a more complex encoded interaction. Its stronger noise protection is not currently justified by Astra's existing physical ports.

### Scientific decision

The two-spin encoded checker remains the strongest credible continuation because it has a much smaller control overhead:

- One additional physical flag qubit.
- No additional data-controlled two-qubit gates.
- Encoded exchange and differential-\\(Z\\) preparation/readout.
- Exact immunity to arbitrary collective flag dephasing.
- Fourth-order undetected-fault bound for purely out-of-code flag leakage.

These are conditional mathematical guarantees, not evidence that the corresponding physical noise symmetry has been acquired. Decoherence-free subsystems and coherent Pauli checking have substantial established prior art.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

Phys. Rev. Lett.

+2



### Preserved research

Complete derivations and counterexamples

Full-memory proofs, fourth-order bound, two-spin and three-spin constructions, control-algebra no-go

Reproducible scientific archive

Seven executable Python studies, seven numerical result files, completed validation log and checksums

All seven validation programs passed the final consolidated run.

Remaining decisive obstacle: establish a physically justified bound on differential flag–bath coupling and on errors during the encoded control gates. The present theorem shows that large collective disturbances need not matter; it does not establish from finite observations that a real device's disturbances are collective.

That distinction determines whether the protected checker becomes a usable quantum observation interface rather than another conditional control theorem.