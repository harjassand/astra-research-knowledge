# Package dependency and topology review

## Required dependency chain
1. **Model/source:** authorized P2_DIRECT_CURRENT_COMPLETE_RETURN.txt (in package04), especially its fixed zero-coupling diagonal per plaquette, core A, filled augmented-component definition, heat-bath clocks, soft reservoir, actual B and native conductance. This recovered snapshot resolves the older topology-representation note's then-missing augmentation definition; do not use that old nearest-neighbor diagnostic as validation of augmented topology.
2. **Contour convention/normalizer:** same snapshot's physical perimeter count <=6n4^P and full-domain Peierls injection; inherited core definition and acquired normalization. Package must retain these as imported mathematical assumptions/results, not imply all were proved by the new finite scripts.
3. **Thermal fiber proof:** 03_reference_thermal_fiber_flow/RESULT.md sections1–4, including unrestricted global magnetization, companion fills disjoint from pins, field-tilt density bound, and geometry-only XOR path. Include check.py and its diagnostic caveat.
4. **Dynamic coverage and M6:** 02_dynamic_fiber_guard/RESULT.md plus THERMAL_FIBER_GUARD.md, including Z_M6/ZA, source-sensitive semigroup bound, unique outermost D, minus collar and companion separation. These establish inclusion of dynamic good states in the aggregate source envelope, not equality of their distributions.
5. **New aggregate proof:** RESULT.md, FINITE_CAPACITY_UPPER.md, independent flow scope, and executable finite-parameter checks. The global native voltage is essential: this is not the killed M6 voltage.
6. **Capacity lower:** needed for the inherited dynamic-current bad-visit estimates, but not for the bare new occupation Cauchy inequality. The finite M1 trial upper is separately needed for its numerical occupation corollary. Do not conflate upper/lower roles or change the source r/kappa.

## Explicit topology gates
- Fixed augmentation is planar triangulation with one diagonal per plaquette, not both diagonals/crossing connectivity. Zero coupling changes topology bookkeeping only, not the physical four-neighbor energy.
- A filled domain is the embedded outer disk of an augmented plus component, with thermal holes and nested spins retained. Filled area is not plus-site count.
- Outermost domains and their augmented collars must satisfy planar separation. A physically minus nearest-neighbor collar alone is not a substitute for the required augmented separation.
- Companion flips preserve pins; the separate D-normalizer flip changes those pins and maps only into unrestricted M6. It need not return to the same fiber or preserve M<0.
- For bootstrap closure, each occupied diagonal pair supplies both orthogonal two-neighbor additions. Physical connectedness then gives bounding-rectangle closure by a spanning-tree rectangle-growth argument. The bounding rectangle must embed before the torus-growth stage.
- M1 trial bound imports the same topological convention. New area cutoff R² changes the Peierls coefficient and u1; it does not create a new topology rule. A gate addition inside an existing filled disk cannot create a larger outer disk. An outside addition joining old components must pay the entire tuple of disjoint outer fills. Winding/nonembedding classification and the old-perimeter lower bound remain explicit structural proof steps, not consequences of the scalar check.

## Reproducibility addition
The copied thermal folder contained density.json but no standalone generator of its infinite-series arithmetic. Added check_density_dependency.py/json, using exact rational closed-form tails. It reproduces rho=1.4900526152562405e-6<1/500000. Include and run it. This certifies arithmetic, not topology or Peierls counting.

## Packaging verdict
Self-contained as a major partial theorem package if all above documents, executable checks, source snapshot, and limitations travel together. It must explicitly state that bad-set occupation / full exterior residence and efficient flow sampling remain open. No script simulates the exponential analytic time horizons or validates large-R dynamics experimentally.
