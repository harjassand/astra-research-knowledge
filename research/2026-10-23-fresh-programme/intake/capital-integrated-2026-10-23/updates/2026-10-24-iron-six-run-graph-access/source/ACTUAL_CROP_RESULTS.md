# Fixed-contract runs on the shared center crops

**Status:** computational graph results only. These runs do not validate
physical phase polarity, external reservoir access, species transport
mobilities, reaction kinetics, or a redox mechanism.

## Provenance and frozen settings

Read-only inputs were the three files listed in
`work/next_unit/iron_shell/data/center192/crop_manifest.json`. From each
`192^3` array, the derived subcrop was the centered local slice
`[32:160,32:160,32:160]` (`128^3`, array axes `z,y,x`, voxel edge 30 nm as
reported by the manifest). Each source contained only 0 and 255. The primary
interpretation requested for this run is rawA (`v != 0` as pore); rawB
(`v == 0`) is a separate complement sensitivity case. The manifest says the
polarity is unresolved and registration is not independently verified. It
also identifies the crop as an arbitrary internal computational region, not a
physical inlet/outlet. No files were written under `center192/`.

Every result uses array axis 0, side 0 as the *assumed* one-port face and axis
0 opposed faces for through-flow. Only internal pore/solid voxel faces are
eligible for reaction. The fixed normalized case is `rho=1`,
`k_face/g_W,edge=1`; the other rate result is the exact perfect-kinetics
capacity. Surface cases are all internal wall, seeded random equal-area 25%,
and remote equal-area 25% (the farthest graph-distance faces). There are no
phase labels, so random/remote/all-wall are mathematical assignments only.

## Results

`G` is total opposed-face graph conductance; `D_eff/D` is normalized by the
128-voxel length and gross `128 x 128` cross-section. `C` is total one-port
two-species reaction response at the fixed finite condition; `C∞` is its
perfect-kinetics transport limit. These are normalized graph units, not
dimensional rates.

| Mask | Pore fraction | Source-connected voxels | Internal wall faces | `G` | `D_eff/D` | All-wall `C / C∞` | Random25 `C / C∞` | Remote25 `C / C∞` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 s rawA | 0.199100 | 387,066 | 58,618 | 6.96662 | 0.054427 | 359.679 / 559.965 | 197.083 / 332.506 | 9.387 / 9.432 |
| 200 s rawA | 0.270562 | 520,472 | 131,258 | 8.46401 | 0.066125 | 834.868 / 1283.172 | 478.387 / 812.810 | 10.577 / 10.685 |
| 600 s rawA | 0.469524 | 971,830 | 298,517 | 26.30756 | 0.205528 | 1467.991 / 2299.513 | 818.278 / 1441.900 | 20.737 / 20.873 |
| 100 s rawB | 0.800900 | 1,679,576 | 84,582 | 89.04276 | 0.695647 | 997.917 / 1342.035 | 655.100 / 937.983 | 52.748 / 53.730 |
| 200 s rawB | 0.729438 | 1,529,740 | 175,796 | 77.78309 | 0.607680 | 1583.303 / 2272.159 | 956.239 / 1481.511 | 45.635 / 46.027 |
| 600 s rawB | 0.530476 | 1,111,996 | 313,921 | 36.48438 | 0.285034 | 2161.248 / 3282.506 | 1233.423 / 2049.577 | 19.455 / 19.541 |

All six solves converged to relative residuals around `1e-11`. Through-flow
inlet/outlet flux mismatches were at most `1.3e-8`; reaction source-flux
discrepancies were at most `3.2e-8`. Through potentials stayed in `[0,1]` up
to printed precision; reaction affinity ranges were within roughly
`[-3e-12,1]`. The per-run text logs retain each residual, flux balance,
affinity range and source-distance contribution profile:

- `insitu02_700C100s_rawA_axis0_side0.txt`
- `insitu03_700C200s_rawA_axis0_side0.txt`
- `interval00_700C600s_rawA_axis0_side0.txt`
- `insitu02_700C100s_rawB_axis0_side0.txt`
- `insitu03_700C200s_rawB_axis0_side0.txt`
- `interval00_700C600s_rawB_axis0_side0.txt`

Each corresponding `*_crop_record.json` records the derived mask path and
SHA-256. The executable and frozen method are in `reactive_geometry.py` and
`BENCHMARK_CONTRACT.md`.

## What these runs discriminate

For every mask, moving from all-wall to an equal-area remote assignment
changes finite `C` substantially: factors of about 38 (100 s rawA), 79 (200 s
rawA), 71 (600 s rawA), 19 (100 s rawB), 35 (200 s rawB), and 111 (600 s
rawB). The remote cases are almost at their transport-capacity limits,
whereas all-wall values depend strongly on the near-boundary interface
assignment. For rawA at 100/200/600 s, `G` and all three scenario responses
rise together. For rawB, however, `G` decreases from 100 to 600 s while
all-wall and random25 `C` rise; remote25 `C` decreases with `G`. Thus the
through-flow ordering does not determine one-port reaction-response ordering
across the frozen surface scenarios even within the rawB computational
interpretation.

That is a conditional graph-level failure of permeability as a sufficient
statistic, not a physical finding about oxide placement. The polarity is
unresolved, one-port and opposed boundaries are crop planes in an internal
region, registration was not independently checked, and `k`/mobility are
normalized. The result supports only the need for actual phase/surface labels,
physical boundary access, and compatible transport/kinetic data before a
reaction prediction or physical ranking can be made.
