## ASTRA — Exact parity measurement despite unrestricted off-code motion

A stronger construction overturns the restricted-control obstruction from the preceding research round. An ancilla does not need to couple directly to a three-body parity operator to distinguish the protected dual-rail subspace from its complement.

The missing possibility was a known, correctable logical byproduct.

Let

\\[ P=|01\rangle\langle01|+|10\rangle\langle10| \\]

be the protected pointer subspace, and define \\(Z_L=n_p-n_q\\). Apply simultaneous, oppositely signed two-body couplings:

\\[ H\_{\mathrm{meter}} =\lambda(n_p-n_q)\otimes X_a. \\]

On both unwanted states \\(|00\rangle\\) and \\(|11\rangle\\), this coupling is exactly zero. Consequently, even arbitrarily fast coherent mixing between those two states cannot directly produce a false ancilla click.

On the protected subspace, the ancilla flips for either rail. The different signs generate a logical phase that can be corrected rather than interpreted as leaked which-rail information.

### Exact solution with permanently active exchange

The more consequential result is that the pointer exchange interaction need not be switched off.

For

\\[ H_P=JX_L+\lambda Z_LX_a, \\]

choose \\(J=\lambda\\), two free-evolution windows of duration

\\[ s=\frac{\pi}{2\sqrt2J}, \\]

and insert a physical \\(Z_p\\) frame operation after each window.

The complete accepted operation is exactly

\\[ \boxed{K\_{\mathrm{pass}}=-iY_LP\otimes U_M,} \\]

while the rejecting operation has support only on the complementary subspace. Thus, after correcting the known \\(Y_L\\) byproduct, the complete instrument measures \\(P\\) versus \\(I-P\\).

This is valid for arbitrary initial correlations with an unrepresented bath and arbitrarily large, noncommuting dynamics confined to the complementary subspace, provided the bath does not directly disturb the detector ancilla and the specified in-code Hamiltonian is maintained.

Full system–ancilla–bath numerical verification

# 7.05 × 10⁻¹⁵

Largest accepted-channel residual across tested mixing rates

# 0

Off-code-to-accept amplitude in the ideal reference model

The test included off-code mixing rates up to \\(257J\\), multiple noncommuting bath operators, and the entire accepted and rejected quantum instrument. These are model calculations, not hardware measurements.

The key lesson is that a measurement interaction need not be scalar on the logical subspace if its outcome-dependent logical action is known and reversible. The earlier no-go remains valid for its stricter scalar-interaction requirement, but not for this broader physical measurement task.

### Further improvement: exact control without a special coupling ratio

The construction now works over a continuous range of physical coupling strengths.

For every \\(\lambda\ge J>0\\), a single sign reversal of the differential ancilla drive, with two appropriately unequal windows, gives an exact parity instrument in total duration

\\[ \boxed{T=\frac{\pi}{\sqrt{J^2+\lambda^2}}.} \\]

The accepted logical byproduct is a known unitary proportional to

\\[ \sqrt{1-\frac{J^2}{\lambda^2}}\\,Z_L +\frac{J}{\lambda}Y_L. \\]

This can be corrected using the available encoded-qubit controls. The complementary subspace remains completely unable to trigger the ideal ancilla.

For weaker detector coupling, a three-window sign-reversal sequence gives exact solutions throughout the additional range

\\[ \frac{J}{\sqrt3}\le\lambda\<J. \\]

Both families passed the complete system–bath operator checks at multiple coupling ratios and hidden mixing rates. The control requirement has been reduced to simultaneous, matched, opposite-sign two-body drives with switchable common polarity, rather than a nonlinear parity interaction or perfectly instantaneous local frame gates.

### Lowest-control version: heralded verification

For a service allowed to reject an attempted quantum resource, a single differential-meter pulse is sufficient.

Even without knowing the exact constant values of \\(J\\), \\(\lambda\\), or pulse duration \\(t\\), the accepted branch is

\\[ K\_{\mathrm{pass}} =-i\frac{\lambda}{\sqrt{J^2+\lambda^2}} \sin\\!\left(t\sqrt{J^2+\lambda^2}\right) Z_LP\otimes U_M. \\]

The accepted logical operation is always the known \\(Z_L\\) byproduct. Unknown calibration changes its success probability, not the conditional logical action, under the stated scalar-coupling model.

This gives a useful distinction:

- Heralded service: one pulse, possible rejection, no precise timing needed for conditional correctness.
- Deterministic parity check: two or three calibrated windows, with exact acceptance on the protected subspace.
- Encoded-detector variant: two physical ancilla spins, using same-sign dispersive couplings and protecting against collective ancilla \\(Z\\)-noise.

The main failure cases remain uncontrolled direct ancilla–bath interactions and sequential rather than simultaneous couplings. Either can cause 100% false acceptance.

### Preserved scientific result

All 11 executable studies passed the final consolidated run. The archive includes the actual scripts, JSON results, complete-instrument tests, counterexamples, execution log and checksums.

Full mathematical derivation

Exact pulse families, full-memory theorem, error bounds, encoded detector and failures

Complete reproducible archive

11 Python programs and 11 corresponding executed result files

Scientific significance: This is a substantive correction and improvement of Astra's previous quantum-receiver construction: arbitrary off-code dynamics no longer require a three-body parity interaction or repeated ideal projections. However, parity measurements, decoherence-free encodings and ancilla-mediated erasure detection have extensive prior art, including physical demonstrations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.nature.com\&sz=32)

npj Quantum Information

+2



A conventional quantum controller supplied with these same controls could implement the result. There is no demonstrated new device or established claim of priority.

The remaining physical target is a simultaneously balanced differential coupling, or its encoded-ancilla equivalent, with independently certified readout and in-code disturbance. That is now a narrower and more concrete experimental requirement than the unrestricted parity-detector assumption at the start of this continuation.