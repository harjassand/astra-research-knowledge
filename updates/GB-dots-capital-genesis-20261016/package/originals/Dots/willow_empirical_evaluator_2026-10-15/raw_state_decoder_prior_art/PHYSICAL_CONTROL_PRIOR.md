# Physical feedback versus frame tracking: closest prior and missing causal test

Read-only primary-source continuation, 2026-10-15. No measured-row inspection, simulation, fitting, hardware intervention, or outreach.

## Bottom line

The operation family already exists: adapt the ancilla measurement mapping so the likely syndrome maps to a less error-prone ancilla state; or physically stabilize a preferred parity sector rather than only tracking it in software. The physical distinction under asymmetric noise is real and has both theoretical and small-system experimental precedents. It does not establish benefit for Willow, and the new observational association does not identify the useful intervention.

The most direct superconducting experiment is Andersen et al. (2019), comparing feedback stabilization with Pauli-frame updating. The particularly close surface-code proposal is O’Brien et al. (2017), which adapts the ancilla's final rotation sign to suppress excited-state dwell. Cramer et al. (2016) gives an actual logical-QEC experiment optimizing syndrome-to-ancilla readout assignment. These should precede any new “sector engineering” claim.

## 1. Exact surface-code control proposal, with a modest simulated gain

[O’Brien, Tarasinski, DiCarlo, *Density-matrix simulation of small surface codes under current and projected experimental noise* (2017)](https://www.nature.com/articles/s41534-017-0039-x), Results around Fig. 3:

Their Surface-17 circuit does not reset ancillas between rounds. Because excitation increases relaxation exposure, they maintain an estimated parity bit per ancilla and choose the sign of its terminal Ry(pi/2) rotation so the likely outcome leaves it in the ground state. This is physical readout-map adaptation, not merely relabeling a recorded bit. It can avoid a separate corrective pulse by changing an existing rotation.

The simulated logical-error improvement is only 0.05 percentage points per cycle. The authors explicitly question whether this warrants implementation complexity. They do not propose data-qubit feedback for this purpose, noting the entangled logical states' equal susceptibility to T1 in their setting.

Transfer caveat: Willow resets ancillas and uses a different echoed extraction circuit. The same numerical benefit and timing mechanism cannot be assumed.

## 2. Closest actual feedback-versus-frame experiment

[Andersen et al., *Entanglement stabilization using ancilla-based parity detection and real-time feedback in superconducting circuits* (2019)](https://doi.org/10.1038/s41534-019-0185-4); [author preprint, especially Appendix E and Fig. 10](https://arxiv.org/pdf/1902.06946).

Repeated XX and ZZ parity checks plus conditional data-qubit rotations stabilize a Bell state near 74% fidelity through 12 cycles. A Pauli-frame-update comparison instead shows declining fidelity. Importantly, the PFU arm still actively resets the ancilla; it removes physical data correction, not every feedback operation.

Their explanation: without even-sector stabilization, the ancilla spends more time excited. Relaxation during feedback delay can propagate into subsequent cycles, while residual ZZ coupling adds phase error. Measurement-induced leakage is a possible explanation for additional experimental decline, not an independently isolated causal mechanism. Four CPMG pulses mitigate idle dephasing/ZZ interaction.

This is direct evidence that physical sector control can differ from frame bookkeeping on a superconducting device. It stabilizes a known Bell state, not an arbitrary distance-5 logical qubit. Added feedback delay and gate errors remain costs; it is not a theorem that active correction wins.

## 3. Actual noise-aware syndrome-to-readout assignment in logical QEC

[Cramer et al., *Repeated quantum error correction on a continuously encoded qubit by real-time feedback*, Nature Communications 7, 11526 (2016)](https://doi.org/10.1038/ncomms11526); [author-accessible text](https://escholarship.org/uc/item/81x1c6n0).

In an NV electron/nuclear-spin three-qubit phase-flip code, readout is asymmetric: the reported ancilla state fidelities are approximately 0.890 and 0.988. They assign the better-readout state to the most probable no-error syndrome, instead of averaging assignments. With that optimization, error correction beats leaving the already-encoded qubit idle over a range of injected error rates. This is not end-to-end improvement over an unencoded qubit because preparation/encoding/stabilizer costs remain.

This is particularly close precedent for exploiting a syndrome distribution through physical measurement assignment rather than trying to make all data qubits physically cold.

## 4. Willow-specific reasons to stop short of causal claims

[Willow supplementary information §V, Fig. S12](https://arxiv.org/html/2408.13687v1) describes ten initialization strings per condition: five random bitstrings plus complements, with 5,000 repetitions each. It also explicitly inserts X echoes on all qubits between the middle CZ layers and includes measurement/reset. Consequently, the reported 20,000-versus-30,000 split can reflect four-versus-six preparation strings, not independently varied parity controls.

The supplied new calibration result is 692/20,000 versus 1,610/30,000 for the q49/t3 tag sweep22 XOR sweep23, a +1.91 percentage-point difference in detector frequency. This result was provided by the parent and was not recomputed here. Thirty-one significant known-preparation tag tests exclude the explanation that every association is just an erroneous first-measurement proxy. They do not exclude:

- Other preparation bits changing jointly with the selected parity; the ten-string support may lack a matched intervention contrast.
- Gate/path differences from preparation pulses, local transient noise, or residual correlations with batch/time.
- Echo-induced changes of physical signs during the circuit, such that a static initial tag does not specify which state occupies a noisy interval.
- A readout-channel effect rather than improved data-qubit storage.
- Significant detector-rate changes without logical-error improvement, or with a compensating increase elsewhere.

The ten-string restriction is a concrete identifiability obstacle. Conditioning on all preparation bits makes the tag deterministic, so it does not magically create within-configuration causal variation. More shots of the same ten settings reduce sampling noise but do not create the missing control contrasts.

## 5. Why physical and virtual corrections can differ, and what cannot be concluded

Own elementary derivation: frame equivalence through a noise channel requires the relevant covariance. For a Pauli P, one needs E(P rho P) = P E(rho) P after accounting for the ideal circuit. Amplitude damping fails X-covariance: damping a physically excited state can decay it, whereas damping the ground state does not. A virtual X label does not interchange actual populations. This proves possible physical inequivalence, not usefulness for an encoded state or any particular feedback policy.

Many stabilizer-code states have maximally mixed single-qubit marginals. Selecting stabilizer signs need not reduce data-qubit excitation or damping susceptibility. The clearest existing lever is ancilla outcome mapping/dwell, which must be distinguished from active data-sector correction and from ancilla reset. Echoes may equalize relevant dwell times; Markovian energy relaxation is not simply undone by reversing a pulse sign.

## 6. Minimum missing causal experiment, if hardware work is ever separately authorized

This is a proposed identification design, not an action taken or a claim of feasibility:

1. Specify the physical intervention: change a terminal ancilla mapping pulse, physically correct a selected data-sector sign, or alter preparation. These are different treatments.
2. Construct matched ideal circuits preserving the same logical task and correctly transform detector/observable definitions. Compare against pure output relabeling as a bookkeeping control.
3. Randomize treatment within preparation configuration and short acquisition blocks. Include both logical eigenvalues, multiple preparation backgrounds, echo phases, and round parities. Use expanded preparation support if the chosen treatment cannot vary within the existing support.
4. Match timing where possible; separately report the realistic latency/gate-cost comparison. An artificially padded control is not the only operational baseline.
5. Measure ancilla population/readout confusion/leakage where available and a held-out logical failure endpoint, counting intervention faults. Detector suppression alone is insufficient.
6. Compare to existing adaptive mapping and feedback schemes; an improved decoder with unchanged hardware is a different comparison. Keep the prior AQ1/AQ2 comparator limitation explicit.

Conclusion: the literature already establishes the principle and closely related controls. The missing result is a controlled, net-beneficial, Willow-specific intervention with a demonstrated mechanism and logical endpoint. The observational association alone does not justify advancing a hardware-advantage claim.
