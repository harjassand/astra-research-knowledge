# Destination, ordinary priors, total costs and scope

The destination is transport-floor qualification of porous designs before fabrication. The constructed operation supplies an all-direction minimum-flow guarantee under an explicit geometric tolerance. This could be useful for screening filters, catalyst supports or flow-electrode geometries. Manufactured geometry, wall law, fluid properties and representative-volume status are separate admission inputs.

The mathematical ingredients are established. What is constructed here is the complete finite interface: support erosion, retained winding currents, compact continuous lifting, exact local energy, exact tree repair of approximate currents, and a rational full-tensor certificate without validating the large solve. Historical priority and a practical discovery-multiplier advantage remain UNKNOWN. This is not a new homogenization principle or first solenoidal spline method.

## Primary operations recovered before implementation

- [Evans–Hughes, primary ICES report 12-15](https://www.ices.utexas.edu/media/reports/2012/1215.pdf), sections 3-5, develops divergence-conforming B-splines as smooth Raviart–Thomas generalizations. Our quadratic-normal/linear-transverse field belongs to that established architecture. We derive its compact-support/current-to-certificate interface explicitly.
- [Bignonnet 2020](https://doi.org/10.1016/j.cma.2020.113237) supplies an efficient image-grid variational upper-permeability method with an energy-consistent Green discretization. We did not implement it or acquire an upper/relative continuum error enclosure. It is a strong complementary ordinary operation.
- [Bignonnet–Dormieux primary 2014 conference account](https://congress.cimne.com/iacm-eccomas2014/admin/files/fileabstract/a1961.pdf) and [journal paper](https://doi.org/10.1002/nag.2278) already give image-linked FFT variational bounds. General variational bounds and meshing avoidance are not new here.
- [Vondrejc–Zeman–Marek 2015](https://doi.org/10.1016/j.cma.2015.09.003) gives guaranteed FFT-Galerkin upper/lower bounds in a scalar elliptic setting. We did not silently transfer that result to incompressible infinite-contrast Stokes flow.
- [Official OpenPNM example](https://openpnm.org/examples/applications/network_extraction.html) provides the public binary Berea fixture, pore convention and nominal 5.345-micrometre voxel size. Its full-sample permeability numbers are not used to validate our different cropped/periodized model.

Selective Astra searches at then-current pins b354d60874c165312fd33b5c031570c6983801e8 and 2bdc6a88e7ce0966ba259728267c3d318f70e009 are preserved in SOURCE_SEARCH_RECEIPTS.json. They did not retrieve a qualified porous-Stokes premise to consume; this is not a proof of corpus absence. N38/N417 were navigation guards against rediscovering positive-Gaussian sampling; none of their science was reused. The alternative N757 Coulomb candidate was screened through its complete packet and set aside because its actual microscopic closure is not paid by a supplied continuum tensor. The selected construction consumes the primary flow operations above, not a resemblance to an unrelated Astra card.

An initial manufacturing screen also recovered an actual [2026 16-channel controlled-breakdown nanopore implementation](https://doi.org/10.1039/D6LC00216A). Generic array fabrication/current-threshold feedback was therefore not promoted as an invention. These screens ended before substantial implementation and are not the research endpoint.

## Failure that changed the representation

The first six-face local polynomial lift was conforming and looked good on a one-cell duct. FAILED_LOCAL_LIFT.md proves its whole-space permeability is <=h^2/pi^2 because it imposes tangential zeros on every interior grid face. It vanishes under fixed-geometry refinement. Larger solves or arithmetic precision do not fix this. RT-plus-mollification preserves tangential transport and nonzero means, while explicitly paying a support buffer.

## Acquired data and comparison

The official public OpenPNM fixture was fetched through the read-only GitHub connector and decoded locally:

    PMEAL/OpenPNM, tests/fixtures/berea_100_to_300.npz, dev at fetch
    Git blob SHA: 3f1796cd3c5f6e854ebeb3316692e10f8a6c0c57
    SHA256: 0c55fa043b95724000f2c56d9d947409932ba72230413ed5d738410c86838d66
    362973 bytes; Boolean im, 200^3, pore=True, mean 0.19871525

One predeclared centered 48^3 crop, indices 76:124 in each fixture axis, was periodically tiled. No crop search, parameter grid, synthetic pore fixture or physical flow fit was used. Its porosity differs from the larger sample, so no RVE status follows. The ordinary spline-Stokes solve and exact consumer receive the SAME geometry, erosion, basis and forcings. The ordinary baseline is the real saddle system [E D^T;D 0], not an empirical porosity proxy. Existing conforming FEM and rigorous FFT are competent alternatives. No superiority over them was measured. An ordinary solver may adopt this postprocessor; that does not establish that this exact consumer pre-existed.

## Measured complete costs

The case has 110592 nominal cubes, 36945 pore cubes, 20462 active cubes, 54912 current edges and 21 graph components, with three winding directions. The KKT system has 75353 unknowns and 2213036 nonzeros. Direct LU has 206522700 numerical nonzeros: float64 values ALONE require 1652181600 bytes, before indices/workspace/materialized copies. Peak memory was not measured; no low-memory/scalability claim is made.

Producer timings: 0.6205 s geometry/assembly, 58.2162 s ordinary factor/solve, 0.0344 s exact repair, 60.1383 s total. The separate consumer first completed in 0.7452 s, then was run twice only as a derived tensor-floor consequence and robust-geometry metadata were added. The final execution is recorded in TRANSPORT_CERTIFICATE.json, about 0.70 s. There was ONE image case and ONE large solve. No physical shots, paid compute, public writes or invented observations occurred.

The certificate differs from the SAME ordinary trial-space point matrix by 4.88014e-14 relatively in Frobenius norm. This measures postprocessing loss, NOT error relative to the true continuum permeability. Erosion can remove important narrow connections; no universal quality ratio/convergence rate is claimed. The exact consumer imports no producer code, independently integrates piecewise polynomials and checks all integer currents/support. It trusts no floating-solve residual.

## Concrete decision and unpaid physical admission

Exact Sylvester tests give K_lower >=0.01I in voxel-squared units, hence the all-force model floor K>=(h^2/100)I. Its nominal SI value is 2.8569025e-13 square metres. This is a derived algebraic consequence, not a preregistered empirical selection criterion.

The SAME bound holds for every coercive periodic geometry containing the nominal pore union eroded by a cube of half-width h/2. It is a real tolerance receiver requiring no new PDE solve for admitted perturbations. Physical admission needs a warranted signed-distance/inner-pore inclusion, not visual similarity or Hausdorff proximity permitting hidden internal barriers. The nominal conditional tolerance is 2.6725 micrometres. Neither that tolerance, a periodic specimen nor the continuum model inputs have been acquired. A direct Darcy experiment is a strong ordinary physical comparator once a specimen exists.

A reusable computational certificate was materially constructed and executed. Actual physical qualification, an unprecedented fabrication action, practical advantage and a civilisation-level discovery multiplier are NOT_ACHIEVED. Independent review status is recorded separately in FINAL_RECEIPT.json and any reviewer-authored note.
