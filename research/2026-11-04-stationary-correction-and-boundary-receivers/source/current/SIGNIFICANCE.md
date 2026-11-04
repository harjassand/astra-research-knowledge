# Scope and significance of the nonplanar receiver

4 November 2026. Read with PROOF.md and the independent AUDIT.md.

## Enabled operation

Train on independent boundary-spin snapshots from isolated, otherwise unknown finite ferromagnetic planar blocks. For a known assembly joining these blocks, the proof gives a randomized polynomial-time approximation to its normalized partition response, together with approximate sampling of its coarse high-temperature currents. The known assembly may be nonplanar, may identify ports, and may use consistent positive fields at arbitrary vertices. Its full size and rational coupling description are charged.

This removes the earlier receiver's planarity and cofacial-field restrictions for partition response and current sampling. It does not remove those restrictions for the earlier physical-spin sampler: no general physical-spin sampling procedure is proved here.

## Essential construction

The true coarse factors have an established winding structure and a polynomial mixing guarantee, even though their hidden graphs are unknown. Empirical factors can be negative; clipping makes them usable probabilities but need not preserve that mixing structure.

The proof therefore does not claim that the clipped chain mixes. Instead it bounds the total weight error over all perfect and two-defect current states. A warm-start annealing construction then compares finite runs of the implemented chain with finite runs of the true chain. This supplies a usable approximate receiver without reconstructing a positive hidden physical model.

## Strong assumptions and costs

- The block law is promised to be a finite zero-field ferromagnetic planar Ising boundary law with known cyclic boundary order.
- Training data are independent full-boundary equilibrium observations of isolated blocks, not uncontrolled embedded measurements.
- Assembly attachments and activities are known. Couplings are ferromagnetic and fields have one consistent sign.
- Training precision depends on the intended assembly size and accuracy. Reusing one learned block counts its error once per occurrence.
- The polynomial bounds have large unoptimized exponents. No practical running time or favorable acquisition cost has been demonstrated.
- Physical mixing, measurement, decorrelation and model validation are not made free by an interface-level complexity statement.

## What remains excluded

The outputs are relative to isolated block normalizations, with the proof's explicit equality-factor convention. Unknown absolute bulk free energies, physical spin sampling, hidden connectivity, arbitrary opposing fields, antiferromagnetic couplings, infinite-volume claims and experimental deployment are not supplied.

## Prior boundary

Exact-factor winding, explicit-graph ferromagnetic approximation, boundary Pfaffian formulas and approximate-kernel Monte Carlo are established. The specific earned result is their rigorous use with noisy, potentially nonphysical empirical boundary factors and an integrated sector-error bound. Novelty of that assembled guarantee is unresolved. It should be presented as a substantive conditional mathematical extension, not as a new general Ising solver or a demonstrated transformative scientific capability.
