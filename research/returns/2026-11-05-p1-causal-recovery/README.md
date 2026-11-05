# General memory obstruction for a homogeneous weak quantum stream

The supplied construction evaluates a previously missing all-prefix singular-loss bound and joins it to a general instrument converse. At fixed weak angle and the accepted acquisition collision count it proves **Omega_theta(N/log N) peak coherent memory**, with the all-output decoder giving N+O(1). It leaves a logarithmic gap: N/log N is still sublinear. No matching linear-memory theorem, sublinear causal decoder or jointly controlled weak-angle/error/processing endpoint is claimed.

Read the complete [PDF](package/output/pdf/causal_recovery_research_note.pdf), [TeX report](package/output/pdf/causal_recovery_research_note.tex), [crossing proof](crossing-and-prefix-bound.md), [loss/erasure companion](erasure-and-loss.md) and [candidate/verification record](instrument-and-verification.md). The [original ZIP](original/causal_recovery_research.zip), [captured return](P1_CAUSAL_RECOVERY_20261105_RETURN.txt), [package guide](package/README_research.txt) and [provenance](SOURCES.json) preserve every supplied artifact.

## Fixed operation and quantifiers

An arbitrary source qubit and arbitrary reference meet fresh independent I/2 carriers once each through the same known `U=cos(theta)I+i sin(theta)SWAP`, with `0<theta<pi/2`. There are no carrier purifiers, preparation keys, return interactions or changed emitter programme; the final source is discarded. Errors are half diamond norm. Quantum memory counts every retained coherent register, including pure workspace and waiting carriers; classical history may be unlimited. Measurements, resets, feedback and arbitrary causal instruments are permitted in the general converse.

The accepted full-output recovery error remains `3(1-sin(theta)^4)^N/4`, with collision count `Theta(theta^-4 log(1/epsilon))` in the weak regime. At fixed theta, this is `Theta_theta(log(1/epsilon))`. Source forgetting at the quadratic scale is not output acquisition. A direct source full SWAP would solve a different action budget.

The all-prefix estimate and memory conversion are analytic proofs, not fits to short-prefix spectra. For peak q qubits they imply

```text
liminf_(epsilon->0) q loglog(1/epsilon)/log(1/epsilon) >= 1/4
```

at fixed nonzero finite `cot(theta)`, with the prefix condition stated in the [proof page](crossing-and-prefix-bound.md). Constants are angle dependent; this is **not uniform as theta tends to zero**. It excludes arbitrarily accurate fixed-memory recovery at fixed angle, but it does not claim a large error at every fixed practical tolerance or solve the joint angle/count/error law.

## Relation to the earlier prefix result

The earlier [P2 general spectral-profile converse](../2026-11-05-p2-weak-stream-memory/prefix-spectral-bound.md) remains valid at its original scope. This return adds a proved all-prefix positive singular gap, explicit constants, and a sharper logical-qubit recovery budget using Renes's existing inequality. It also preserves the full density-profile and variable-branch occupancy route. The proved minimum-gap bound decays as `exp[-4n log n-O_theta(n)]`; an exponential-in-n bound or a sufficiently strong low-energy profile could close the remaining logarithmic gap, but neither is established here.

The [exact carrier-loss theorem](erasure-and-loss.md) has a physical decoder and matching-order loss tolerance within its stated erasure model. Erasing carriers before processing is distinct from coherent processing and then discarding them. The [four-outcome receiver candidate](instrument-and-verification.md) is genuinely CPTP and fails by an exact distinguishability loss; its failure is not a general receiver no-go.

Supplied independent channel/algebra audits check the logical Petz witness, crossing/interpolation constants, recovery inequality, finite-prefix coefficients and erasure extension. [Sharp profile audit](package/channel_constructor/sharp_profile_and_gap_audit.txt), [crossing audit](package/channel_constructor/crossing_gap_audit.txt), [separate recovery audit](package/algebra_constructor/renes_profile_audit.txt). The failed exponential **fixed-point**-defect route is retained and is not substituted for a singular-loss bound. Established Petz/Renes, R-matrix/crossing, transfer-matrix and tensor-network compression machinery is credited; no exhaustive priority or new physical law is asserted.

No scientific programme, eigensolver, SymPy calculation, PDF builder or fresh Capital audit ran for publication. Earlier acquisition and programmed-emitter results retain their own scopes. Generated current retrieval was not rebuilt; these proofs and result pages are directly available on GitHub.
