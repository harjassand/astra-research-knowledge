# One-port reaction access versus two-face permeability

**Status:** executable mathematical comparator and toy falsifier. The Paul
tomography crop, phase map, reservoir boundary, species mobilities, and reaction
kinetics have not been supplied to this directory. No geometry-specific or
chemical-performance result is claimed yet.

## Question and scope

For a single acquired binary pore geometry, compare (i) ordinary steady
through-permeability with reservoirs on two opposing crop faces and (ii) a
linear-response, two-species reaction response with one accessible reservoir
boundary. Both calculations use the *same pore voxels and six-neighbour pore
throats*. They answer different boundary-value problems. The first measures a
spanning path. The second measures stoichiometric countertransport to reactive
surface accessible from one boundary.

Paul et al.'s 2025 nano-XCT is an internal lamella region, not an imaged
external pellet boundary. Therefore a crop-face reservoir is an explicitly
chosen mathematical condition, not evidence that the face is physically
exposed. The pore mask does not encode which solid phase reacts or a chemical
rate. No surface label or kinetic constant is inferred from it. See the
[paper](https://doi.org/10.1016/j.xcrp.2025.102729) and public
[data/code record](https://doi.org/10.5281/zenodo.15751094).

## Frozen discrete contract

Input is a 3-D Boolean array (`True` pore, `False` solid); each voxel is a cube
of side `delta`. Pore-pore six-neighbour links have water-mobility conductance
1. A selected open crop face couples a pore voxel to its reservoir through a
half-voxel link of conductance 2. Thus a completely open rectangular slab has
`D_eff/D = 1` under the opposed-face calculation. The code's conductances are
normalized; physical chemical-potential mobility would be
`g = D c_ref A/L`, including the relevant susceptibility. No physical scale,
species ratio, or rate can be recovered from this normalization.

For through-flow, clamp unit potential on the selected source face and zero on
the opposite face, solve the scalar graph Laplacian, and report total
conductance `G` and geometric `D_eff/D = G * N_axis / A_cross_section`.
Components touching neither port are omitted. Components touching only one
port carry zero steady through-current.

For reaction access, the same selected face is the *only* exterior reservoir:
hydrogen potential is 1 and water potential is 0 there; other crop faces are
no-flux. With proportional mobilities `L_H = rho L_W`, set the one fixed
illustrative case `rho = 1`, hence `alpha = rho/(1+rho) = 1/2`, and solve

```text
(alpha L + K) a = alpha b,       C = sum_i k_i a_i,
```

where `a = u-v` is affinity, `L` is the one-port Dirichlet graph Laplacian,
`b = L 1` is its source-boundary vector, and `K=diag(k_i)`. The executable
uses one finite kinetic condition, `k_face / g_W,edge = 1` for every selected
solid-interface face. This is a single dimensionless Damkohler condition,
not an empirical iron-reduction rate. It also computes the exact
perfect-kinetics limit by fixing active reaction voxels to zero affinity and
solving the remaining transport network. This is an upper capacity for the
specified graph/ports/surface assignment, not a predicted rate.

Only pore components connected to the imposed reaction reservoir are kept,
even if a disconnected node is assigned positive `k`. The implementation
checks that finite reaction equals source influx. Internal pore/solid voxel
faces are eligible surface; exterior crop-cut planes are never counted as
reactive surface. Reservoir-facing crop voxels can still be reactive through
their *internal* pore/solid faces, which represents a possible parallel
surface path at that assumed boundary.

## Three frozen surface assignments

1. **All internal wall:** every eligible pore/solid face is reactive. This is
   an all-wall upper scenario, not a phase-identification claim.
2. **Random equal-area subset:** a seeded random 25% of eligible interface
   faces is reactive (`seed=20261024`).
3. **Remote equal-area subset:** the same number of faces as scenario 2 is
   assigned to the largest geodesic distances from the reservoir. If labels
   are absent, this is only a remote/deep-phase *geometry proxy*, not a claim
   about actual phase placement.

No parameter grid is run. The finite-rate condition and exact
perfect-kinetics limit above are the only rate cases. If a compatible
phase-labelled geometry is later obtained, it should replace the proxy as an
additional labelled scenario with the provenance and reactive-face rule
recorded; it must not be silently fit to the desired ranking.

For each finite-rate scenario, the executable also reports the fraction of
`C` contributed by pore nodes within 1, 3, and 10 six-neighbour graph steps of
the selected source face, plus the contribution-weighted median graph depth.
This diagnoses sensitivity to the imposed crop boundary; it is not a physical
oxide-front depth.

## Acceptance criteria for an acquired crop

1. Record source file/hash, voxel size and crop dimensions; preserve the
   original mask. Identify the chosen source axis and side as an assumed
   boundary condition, since the XCT region is internal. Do not assign
   reaction to cut planes.
2. Run both operators on the same crop. State the number of source-connected
   voxels, internal interface faces, `G`, `D_eff/D`, `C` at `Da_face=1`, the
   perfect-kinetics capacity, and `C/C_infinity` for each of the three frozen
   scenarios. Verify finite source-flux balance numerically.
3. Treat phase placement as unknown unless the actual data carry a compatible
   solid-phase label. A robust through-flow surrogate requires the ordering
   of reaction response to agree with the ordering of `G` across matched
   acquired geometries and across all frozen phase/surface cases, at both the
   finite condition and capacity limit. A single crop can test sensitivity
   to surface assignment, but cannot establish a cross-geometry ranking.
4. Report a rank reversal, a broad overlap, or scenario dependence as failure
   of permeability alone to predict reaction access. Do not convert a
   dimensionless graph response into a physical reduction rate without
   measured transport susceptibilities and reaction kinetics.

## Executable falsifier

From this directory, run:

```sh
python3 reactive_geometry.py --self-test
```

The checks verify (a) the exact open-slab permeability limit, (b) the
`1/9` geometric `D_eff/D` of a single-voxel channel in a `3 x 3` gross cross
section, and (c) a same-geometry/equal-area wall relocation result. In the
channel, opposed-face `G=1/8` and `D_eff/D=1/9` stay fixed, while one-port
reaction access is `0.25` for one wall patch one step inside the inlet and
`0.0714286` for an equal-area patch six steps inside. The two-species block
equations agree with the affinity reduction. This is a finite-graph
counterexample to treating through-permeability as a sufficient statistic for
one-port reaction access; it is a code falsifier, not an observation about
Paul's specimen.

Once a read-only `.npy` Boolean crop is supplied, invoke for example:

```sh
python3 reactive_geometry.py path/to/crop.npy --axis 0 --source-side 0
```

The script prints the frozen scenario outputs and checks the source-flux
identity. `path/to/crop.npy` is a placeholder; this unit has not fetched or
created a tomography crop.
