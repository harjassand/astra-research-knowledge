# Independent proof review of detector-kernel interface

28 October 2026. Reviewer: solver-instrument contributor, separate from the knowledge/comparator producer.

Reviewed file: `knowledge_and_comparator/DETECTOR_KERNEL_INTERFACE.md`.

SHA256: `d59eca11a43d10930566bc4d6b6f8149e3e4f6d33cfac2c4eefd97ec0dc1344f`.

**Decision: accepted at the stated mathematical scope.** This review checked the proof text; it did not replay the producer detector-kernel test program.

- Finite positive-kernel domination `0 <= sum D_r <= G` forces the D_r forms to vanish on the G-nullspace and remain bounded on the completed visited one-particle space. The bounded-form construction of E_r is valid. Consistency across finite lists is essential and is stated.
- `L u=(sqrt(E_0)u,...,sqrt(E_m)u)` is an isometry because the sum of effects is I, including E_0. No commutativity of the pulled-back E_r is needed.
- Second quantization of L maps a coherent input to product coherent output amplitudes. Vacuum projection in a subset of ports therefore yields `Gamma(I-sum E_r)` and the stated kernel.
- Inclusion-exclusion acts on commuting threshold projectors in the dilated port space. Multiplying the generally noncommuting pulled-back individual no-click operators would be incorrect; the producer explicitly avoids that error.
- The instrument coefficient `<alpha_b|Pi_z|alpha_a>` has the correct orientation. Positivity of Pi_z makes the kernel positive, so every record map is completely positive. The full input isometry condition makes the sum trace preserving. Arbitrary reference entanglement is consequently covered.

The result assumes a specified passive linear transfer and ideal on/off output ports with loss and efficiency included in their one-particle effects. Nonlinear saturation, finite detector recovery, dark counts, actual output-mode calibration and the P2 physical pulse are outside it. The scalar source phase density alone does not determine detector collection.
