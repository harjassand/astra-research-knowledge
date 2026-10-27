# Coherent control does not rescue this finite on-axis model

**Executed conditional model; new physical operation NOT_ACHIEVED.** This
extends the focus diagnostic to arbitrary complex superpositions of nine probes
and counts every Cr atom. It does not establish a measured displacement law.
Source: published CrSBr CIF from [the pinned author repository](https://github.com/KleinAtomLab/Mesoscale-atomic-engineering/tree/6844cc568271d448704a0eb6ee55ddfd5246d242).

Model: abTEM1.0.11,200keV,32mrad aperture,pristine6x4x16 periodic supercell,
256x256 grid,1Å slices. All768Cr atoms on32 distinct depth planes are counted;
the target column has16Cr. Incoming fields are sampled immediately before each
atom's containing slice. Each atom receives a periodic .4Å-radius disk mean
of |psi|². A common local-flux displacement coefficient is **unacquired**.
Other species, correlations, damaged-state feedback, phonons and inelastic
processes are omitted. Disk flux is not measured damage probability.

Focus values are -128,-96,...,128Å. For entrance modes psi_a define
G_ab=sum conj(psi_a)psi_b. M_j is target disk response; M sums all768Cr.
Coefficients c give incident power c*G c, target density c*M_j c, total
competing density c*M c. The largest generalized eigenvalue of (M_j,M)
optimizes target/total over this finite span. This is ordinary linear algebra.
Nonnegative time mixtures cannot beat the best ratio in the fixed independent
first-event model.

Built probes have squared array norm about1/65536. Assuming unit array norm
or pricing coefficient norm would misprice dose. Whitening with G charges
specimen-plane incident norm including interference; G condition number is
about1880. Probe preparation, aperture loss, coherence and control bandwidth
remain additional costs. Arbitrary coherent superpositions are an optimistic
enlargement, not a demonstrated hardware menu.

|Layer|Best single focus,target/allCr|Best coherent ratio|Target efficiency at best ratio|
|---|---:|---:|---:|
|1|.15384|.32976|.21783|
|8|.15094|.15942|.46390|
|16|.17450|.32605|.24968|

Across16 layers, coherent maxima span .15691–.32976 versus .11531–.17450 for
individual focuses in the same library. Efficiency is target density relative
to its maximum at equal incident norm in the same coherent span. Maximizing
selectivity sacrifices about40–78% of that density. Saved support points for
target density minus collateral penalty expose this tradeoff; a nearly dark
field is not a free selective write.

These floating-point calculations are not outward interval certificates or
all-field optima. They do not exclude tilt, a larger basis, recovery or
state-dependent control. They are also not a physical no-go: the microscopic
move law remains unacquired. The result closes only this attempted escape from
the focus failure. Acquiring a different write interface or a function needing
only column patterns has greater marginal value than further surrogate tuning.

A separate saved-matrix calculation checked20,000 seeded complex coefficient
vectors against all16 computed maxima. Target and collateral matrices were
positive semidefinite to the inspected numerical precision; maximum relative
generalized-eigen residual was4.27e-15. This checks matrix optimization scope,
not the physical response model or multislice convergence.

`coherent_depth.py` regenerates `COHERENT_MATRICES.npz`/`COHERENT_RESULTS.json`
using the read-only abTEM environment in ../../empirical_operation_invention/.
Root-owned caches remain local. Execution6.63s excluding runtime import, no
experiment, external write or dependency installation. Full matrices and
parameters are retained; no historical priority or practical advantage claimed.
