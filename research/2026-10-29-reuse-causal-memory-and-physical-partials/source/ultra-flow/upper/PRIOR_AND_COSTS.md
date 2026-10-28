# Established method, actual comparison and charged costs

## Closest established operation

[Lederer and Merdon, Guaranteed upper bounds for the velocity error of pressure-robust Stokes discretisations, arXiv:2008.05816v2](https://arxiv.org/pdf/2008.05816), introduction and section2, gives the relevant established pseudostress/equilibrium and Prager–Synge framework. Its pressure-independent formulation uses deviatoric stresses, and it develops efficient local flux constructions. We consume the elementary exactly equilibrated special case, deriving the periodic-solid boundary and sign conventions explicitly in PROOF.md. No unknown interpolation constant is borrowed from that paper. Our sign div sigma=f is opposite to its usual stress sign.

Equilibrated FEM, mixed-stress methods and energy-consistent porous-flow FFT methods are strong ordinary comparators. The frozen lower package's PRIOR_AND_COSTS.md records its earlier primary spline and porous-flow FFT screening, including Bignonnet's 2020 variational energy-consistent construction. Those methods are not assumed to be weaker than this prototype. Historical priority for this particular image-specific integer receiver is UNKNOWN; the variational, RT0 and hypercircle principles are established.

The selective Astra search for Stokes equilibrated stress/complementary-energy permeability did not supply an extra qualified scientific premise. The existing original image and its scale are reused from the frozen lower package. No current-corpus freshness or additional physical calibration is claimed by this continuation.

## Equal-information ordinary comparison

All methods receive the same original periodic 48^3 Boolean image, voxel size, continuum Stokes/wall-law model, three forces and local compute. The lower package already paid an ordinary divergence-conforming spline Stokes solve. Its separate exact consumer turns retained admissible currents into a rational lower tensor; agreement with that solver is not continuum accuracy.

For this upper the implemented ordinary choices are a grounded scalar-Poisson flux initializer and a matrix-free mixed deviatoric-stress optimization. Both become valid continuum uppers after the same exact force repair and energy receiver. The scalar solve takes 24 preconditioned CG iterations. Its isotropic upper is 1.8556044293307536 I, and its deviatoric tensor satisfies U_init <= 151.24 L. The final repaired stress tensor satisfies U <= U_init and U <= 11.55 L by exact rational principal-minor tests. This is a genuine tighter all-force bracket than the implemented initializer at greater solve cost; it is not an incumbent speed or accuracy advantage.

A sufficiently informed ordinary equilibrated Stokes solver can use the same deviatoric freedom, exact source correction, algebraic preconditioner and image. More efficient local equilibration or richer stress spaces may outperform our capped global solve. No such external implementation was benchmarked and no universal accuracy/cost comparison follows.

## Executed work ledger

No new numerical producer run was made during finalization or root review. No large factorization was made for the upper. The sole numerical upper run has three force solves, each capped at 800 MINRES iterations with info=800. Their KKT residuals are recorded, not used as rigorous error bounds. Exact integer repair supplies every fluid source afterward.

| Completed computation | Recorded wall seconds | Qualification |
| --- | ---: | --- |
| Frozen lower producer | 60.138259 | Includes its ordinary factorization, repair and artifact output |
| All three frozen lower consumers | 2.144243 | Includes earlier metadata/floor updates; one retained numerical lower solve |
| New upper producer | 60.421907 | One scalar initializer plus 3 capped stress solves, exact repair and artifact output |
| New upper exact consumer | 1.248836 | One execution; integer interface, symbolic integration, exact tensor and factor |
| Recorded completed-computation total | 123.953246 | No unchanged rerun for review |

Within the new producer, hierarchy/geometry setup was .129878 seconds, scalar CG and source repair .157152 seconds, the three stress solves 18.966354/18.797989/21.123160 seconds, and final stress repair .220913 seconds. These are substage timings within the producer total, not extra charges to add again. The exact consumer's .702610 seconds of input/force checks, .040204 seconds of symbolic cell integration and .506021 seconds of exact energy/tensor work likewise belong to its 1.248836 seconds.

There are 36945 original fluid cells, 120019 oriented faces, 360057 stress unknowns and 110835 equilibrium multipliers. The symmetric algebraic aggregate hierarchy has 36945,5595,959,173,27 cells; only the final 27-by-27 matrix is dense. These are preconditioner aggregates of the SAME original equations, not additional physical grids or fixtures. The code uses linear-size vectors and sparse hierarchy matrices; peak resident memory was not measured and is not asserted. The frozen lower factorization remains charged: 206522700 LU numerical nonzeros, with 1652181600 bytes for float64 values alone and an unmeasured higher peak.

The dyadic stress denominator is 2^32. The largest stored absolute numerator is 123537432917. Integer divergence repair is guarded against overflow; the independent force consumer and energy contractions use Python integers. The exact receiver requires no validated 470892-dimensional inverse, floating solve optimality or posterior residual constant. All reported factors and tensor entries are rational certificates.

The totals exclude interpreter startup, network/source acquisition, literature reading, software/proof development and review wall time. Those exclusions prevent interpreting the table as a full researcher-effort benchmark. The prior decoded dataset has 362973 bytes, already acquired by the lower package; actual prior network wire bytes/time were not measured. New physical shots, paid compute, external writes, images and crops are zero.

## Remaining bridge

The exact same-image continuum bracket is acquired and substantively root reviewed. Its relative factor 11.55 remains broad. Physical two-sided transport additionally requires a warranted inner/outer geometric sandwich, representative/periodic boundary admission, scale and flow-law calibration. None follows from image segmentation, the nominal half-voxel lower buffer, a converged discrete solve or the present rational algebra. No new practical matter-qualification capability is claimed until that acquisition interface is paid.
