# Iron one-port graph access: six fixed-contract runs — 24 October 2026

This selected computational unit compares opposed-face graph through-flow with one-port two-species reaction access on six supplied 128^3 binary center crops. It is a finite graph result, not a physical redox or oxide-placement finding. The [source manifest](source_manifest.json) pins the two method-contract versions, outputs, per-run logs, crop records and exact derived input arrays. The source implementation is preserved but was not run by this intake.

## Frozen graph construction and result

The crops come from three 192^3 images using the centered `[32:160]^3` slice. The reported voxel edge is 30 nm. `rawA` (`value != 0`) and its complement `rawB` (`value == 0`) are both retained because pore/solid polarity is unresolved. The calculation uses six-neighbour links, axis 0 for opposed-face through-flow, and axis 0/side 0 as an **assumed mathematical** single reservoir for reaction access. The one-port model fixes `rho=1`, `Da_face=1`, plus an exact perfect-kinetics capacity. It tests all internal walls, a seeded equal-area random 25% assignment, and an equal-area remote 25% assignment. These are synthetic surface labels, not phase maps.

In `rawB`, from 100 s to 600 s opposed-face conductance falls from `89.0428` to `36.4844`, while all-wall reaction response rises from `997.917` to `2161.248` and random-25% response rises from `655.100` to `1233.423`; remote-25% response falls from `52.748` to `19.455`. Across all six cases, changing only the equal-area surface assignment changes the response substantially. The source reports converged solves and small residual/source-flux mismatches. This is a conditional graph-level counterexample to permeability as a sufficient statistic for one-port reaction response under these fixed assumptions.

## What the six runs do not identify

The crop faces lie inside a tomography lamella and are not verified exterior pellet boundaries; registration is not independently checked. `rawA` versus `rawB` polarity, reacting phase, actual reservoir access, species mobilities and reaction kinetics are unknown. Conductances and rates are normalized graph quantities, not dimensional iron-reduction rates. No physical phase polarity, external reservoir, mobility, kinetics, or redox mechanism is established. The run does not identify an Fe/FeO shell or validate pressure-pulse or shallow-redox hypotheses in the separate [iron-shell update](../2026-10-24-iron-shell-model-boundary/README.md).
