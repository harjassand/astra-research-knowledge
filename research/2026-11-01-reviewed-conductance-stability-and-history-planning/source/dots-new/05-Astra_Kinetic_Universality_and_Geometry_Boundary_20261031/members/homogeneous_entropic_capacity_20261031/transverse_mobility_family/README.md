# Unknown transverse mobility: exact range and finite family receiving

Status: NEW source-frozen construction; independent mathematical/whole review
pending. All earlier accepted isotropic/parallel/finite files and ZIPs are unchanged.

The question is no longer only to calculate one fully specified diffusion. Given
an acquired homogeneous potential, what conductances are possible when the
constant transverse relaxation matrix is entirely unidentified?

The candidate theorem proves that, over ALL fixed finite SPD transverse matrices
with unit longitudinal mobility and zero cross mobility, the attainable
capacity/mass values form exactly the OPEN interval (k_parallel,k_free). It proves
both mobility limits, strict endpoints and continuous strict interpolation along
every shape path gamma*B. Its endpoints are independent of the angular potential
within the stated homogeneous family. Actual fixed-M rates need not be equal.

The receiver does NOT claim to compute that exact lower endpoint or a realizing
matrix. It uses the accepted finite-Jensen operation to produce a computable
closed OUTER enclosure of the entire exact range. Its raw 513D example encloses
every member in approximately

    [2.369045057852262e-37,2.384988210037886e-37],

meeting the externally requested ratio 1.01. No matrix entries are supplied or
estimated, because the task is explicitly universally quantified—not because a
particular actual physical kinetic model has been authenticated from F alone.

## Operation

Python standard library. Preserve the sibling accepted engine directories:

    python -B receive_family.py       # paid raw 513D producer
    python -B check_family.py         # scope/type checks and full 513D replay

The new module hashes BOTH the exact range proof and the accepted finite engine
before import. It has a distinct schema, observable and numerical enclosure field,
and strictly binds the entire family descriptor and exact-range characterization.
It rejects stale isotropic/radial scope fields. Model-family dictionaries are
fresh on each call, preventing returned data from mutating later expected scope.

The family task is exactly `all_fixed_transverse_SPD`. There is no M argument or
matrix acquisition. Passing an actual matrix does not turn this into a specific-
model calibration service. A separate known-M constructor would need to read and
check that matrix; it is not implemented here. An application must justify the
actual block-SPD/FDT structure externally.

## Scientific and computational boundaries

For m>=2, each nonproportional SPD shape can be scaled to realize any interior
rate. Hence a measured conductance alone does not identify matrix SHAPE. If the
angular potential and shape B are already known, the scalar gamma is unique;
we do not claim otherwise or provide an inverse solver. The theorem's weak
compactness/limit proof gives no free numerical gamma or convergence modulus.

Cross mobility, changed longitudinal mobility, variable/singular matrices,
nonreversible drift, time-dependent controls, arbitrary basins and nonhomogeneous
potentials remain outside the family. So do arbitrary-start passage times,
angular mixing times, finite-time Markov projection and physical calibration.
Current numerical results are finite exact certificates, not measured rates.

MOBILITY_FAMILY_CANDIDATE.md preserves the earlier simpler universal bound.
EXACT_MOBILITY_RANGE_CANDIDATE.md is the complete stronger proof. COSTS_AND_SCOPE.md
separates information access from unearned actual-model promises. Source-bound
accepted dependencies are listed in DEPENDENCIES.json. The current source freeze
and author tests do not replace an independent whole receipt.
