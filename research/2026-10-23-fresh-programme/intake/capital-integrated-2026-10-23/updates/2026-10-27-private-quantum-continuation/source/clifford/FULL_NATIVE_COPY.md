## ASTRA — Exact fault certification for active quantum gates

The strongest result of this continuation removes an important limitation of the previous construction: coherent errors during an active entangling gate can be given an exact positive fault representation, even with an arbitrary persistent quantum bath.

The previous four-frame approach protected the gate approximately but could not produce an exact ideal-gate branch. The new construction changes the physical procedure.

Prepare a four-qubit resource using the noisy gate, then privately choose whether to test that resource or use it to teleport an unknown two-qubit input through the gate.

For a Clifford gate \\(G\\), the completed service has the exact decomposition

\\[ \boxed{ \mathcal S=\sum\_{P\in\mathcal P_2} \operatorname{Ad}\_{GP}\otimes\Phi_P } \\]

where every \\(\Phi_P\\) is a completely positive map on the retained quantum memory.

The \\(P=II\\) branch implements the intended logical gate. The other fifteen branches are mathematical fault labels—not assumptions of independent stochastic hardware noise.

### Main results

| Result                                                  | Verification                           |
| ------------------------------------------------------- | -------------------------------------- |
| Complete gate-teleportation versus positive fault paths | Residual below \\(10^{-15}\\)          |
| Physical sacrificial-test bath instrument               | Residual below \\(1.2\times10^{-16}\\) |
| Optimal local Pauli fault-detection contrast            | 2/3                                    |
| Generic direct-gate Pauli frames needed                 | 16 choices (4 secret bits)             |

A stronger local verifier emerged from the investigation. Six carefully chosen product-measurement settings give a worst-case detection contrast of \\(2/3\\), improving on \\(8/15\\) for a uniformly random single stabilizer. An independent exact-integer computation established the matching upper bound for this measurement class.

The general \\(2/3\\) optimality result is already published in stabilizer-state verification research. Astra's contribution here is its integration with the complete bath-update instrument and adaptive quantum service, not discovery of the general optimum.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

Phys. Rev. Research

+1



## Executed adaptive controller

The controller was tested with a never-reset, noncommuting quantum bath and a finite 30-fault admission budget.

| Method                     | Mean gate uses | Mean hidden faults | Mean certified upper bound |
| -------------------------- | -------------- | ------------------ | -------------------------- |
| Random stabilizer          | 524.97         | 3.80               | 27.88                      |
| Six-setting local verifier | 630.23         | 4.45               | 27.45                      |

Each configuration used 128 reference trajectories. No all-prefix confidence-bound violations were observed; formal coverage comes from the derived supermartingale.

Under a separate modeled 2.5% per-qubit readout-flip rate, completed uses fell to approximately 61.5 and 99.8, respectively. This exposes a substantial practical acquisition cost.

## Decisive failure: verification cannot be reused for free

The inexpensive local verifier consumes its four-qubit resource. Its postmeasurement fidelity with an initially perfect resource is only \\(1/8\\) or \\(1/4\\), depending on the measurement setting.

I also established a remote-LOCC obstruction: a separable accepted operation that perfectly preserves the target maximally entangled gate resource cannot preferentially accept it over every competing maximally entangled resource.

Therefore, heralding an individually perfect gate resource without consuming it requires stronger nonlocal quantum operations. The aggregate statistical audit does not provide that capability.

Another failure survives: retaining fine teleportation outcomes can reintroduce coherent interference. In the reference models, the completed coarse channel had residuals below \\(10^{-15}\\), while the incorrectly assumed fine-record fault representation differed substantially.

### Preserved research

Complete technical derivation

Exact full-memory proofs, six-setting verifier, sequential certificate, optimality witness, hardware comparison and counterexamples

Complete reproducible research archive

10 executable Python studies, 10 actual result files, execution logs and checksums

All ten studies passed individually. Eight passed in the combined rerun; the remaining two passed separately after the combined run reached its execution limit. The archive passed its integrity check.

Scientific judgment: This closes a genuine gap in Astra's conditional quantum-service framework: active Clifford gates can now join the same exact fault-accounting scheme as idle protected operations. However, gate teleportation, randomized compiling, and stabilizer verification have strong prior art.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://journals.aps.org\&sz=32)

journals.aps.org

+2



The highest-leverage unresolved problem is now the physical terminal interface: obtaining trustworthy Bell measurements, Pauli corrections, resource isolation, and complete-boundary control of their interactions with the hidden bath. The mathematics supports the proposed capability, but its practical realization remains unverified.