# P2 matter operations — selected source-bound update, 23 October 2026

This append-only update supplements the earlier P2 thermal/conversion intake. The source packet is pinned and selected files are byte-checked in `source_manifest.json`. The archive CRC and selected-member hashes establish transport integrity only. Capital did not run the scientific scripts or independently reconstruct the proofs.

## Compatible finite-pitch path in a one-dimensional model

The source derives a cell-average gate from one positive compatible electrostrictive/piezoelectric energy. For a continuous one-dimensional bar, under the stated coexistence assumptions and positive margins `gamma = kappa*pi^2/ell^2 - lambda_m > 0` and `mu > 0`, it reports

`F[q] - F[p] >= min(mu, gamma) * integral (q-p)^2 / 2`

for every admissible `H1` configuration and amplitude. This is a global path certificate for a selected homogeneous state in that model, not a finite-grid search. The operation is known-input polarization transfer `-B -> +B`; the piezo bridge endpoints can return, but this is not an unknown-input NOT and does not establish reset of every screening-electrode charge. Three-dimensional contacts, a matched specimen, thermal retention and practical advantage remain open.

The exact reset analysis also bounds the result: on a connected one-dimensional bar with `|q| <= B`, returning every bridge to its original polarized state forces `q^2 = B^2` everywhere and continuity forces one uniform sign. The same reset contract therefore does not support nonuniform pattern writing. Conditional pattern certificates are not physical pattern demonstrations.

## Synthetic finite-time cycle and direct-pulse comparison

The coupled source-port simulation uses one fixed synthetic parameter tuple, twelve actuator cells, and a 100-unit passive terminal hold with both external source voltages set to zero. The refined outputs report:

| Driven duration | Terminal result | RMS error from `+B` | Calculated heat |
| --- | --- | ---: | ---: |
| `T=2` | fast cycle falls to the central phase | `0.8660254` | `4.3130734` |
| `T=20` | positive basin | `0.00019927` | `0.2584217` |
| `T=100` | positive basin | `1.63e-7` | `0.0254254` |

Heat is per cross-sectional area in synthetic model units. These are deterministic simulations; temperature noise and a retention lifetime are not included. Mesh refinement supports these examples only.

A same-parameter direct-field `sin^2` pulse is one unoptimized comparator. At `T=20` its calculated heat is `0.1340926`, below the gated cycle; at `T=100` it is `0.2736096`, above the gated cycle. The field peaks and controller resources are not matched, and this pulse is not optimized. The comparison blocks a general advantage claim; it does not establish a lower bound for conventional switching.

## Source and version corrections

The first terminal implementation forced internal field `h=0` despite nonzero series resistance, which required active source work and was not a zero-control hold. The governing version instead sets external source voltages to zero and lets internal field and charge relax through their terminal circuits; residuals are retained. The earlier implementation is superseded.

The source-reset audit records an earlier code hash with an incomplete, unused sparsity mask. The final pinned `coupled_cycle.py` has the bias-state dependencies in that mask; the run uses the analytical Jacobian. The handoff says the mask correction changed neither the governing rates/Jacobian nor saved trajectories. The old audit note is version-specific and does not describe the final source.

## Selective-locking jam in a finite graph model

A four-junction finite-state model shows that perfect local rejection of defective loops can still strand one when other links lock first. In the typed model, at the synthetic rate ratio `k/nu=1`, the exact jam probability is `8424/30125` (about `0.279635`). The separate untyped model gives `4460672/19202265` (about `0.232299`) under a different transition set; these probabilities must not be averaged together. Both are graph-model outputs, not measured reaction rates or chemical yields.

A loop-free feasibility guard removes that jam but still permits disconnected outcomes. A connected-completion guard gives eventual completion only under the declared full positive-rate mixing model and requires global component information. At twice that model's own mean completion time, the source reports connected-target mass `0.934605629` and unfinished mass `0.065394371`. The guard is not a free local sensor or actuator.

The molecular interface remains a proposal, not an acquired operation. No validated force-bearing geometry, loaded reaction rates, same-partner retention or executed test is supplied. Fuel, unlocking/reset resources, and retained stiffness or toughness after temporary links are removed remain unresolved. The result changes the next attack from increasing a local lock rate to preserving repair reachability or supplying a real, costed selective-unlock interface. Graph connectedness alone does not establish useful mechanical performance.

## Evidence boundary

No material measurements, hardware operation or physical experiment were performed. Novelty, material feasibility, and practical advantage remain `UNKNOWN`. The exact selected source bytes and excerpt ranges are recorded in `source_manifest.json`; the large trajectory files, unrelated prior-thermal package, routing/usage records and full molecular construction audit are not included.
