# Result: a conditional raw-image current operation, with an honest source failure

The substantive construction is a query-specific radial-blur invariant,
not a physically qualified torque measurement. It identifies exactly which
quadratic virtual-field queries survive radial blur, derives the rotational
annular query, supplies a difference-image control that removes static
unmatched-particle variance, and executes the finite-bit operation on all500
frames of a real public particle-image record. That record fails the
positive-normalizer gate. No physical or practical advantage is established.

## Acquired mathematical operation

For f(x,y)=(y-x)^T S(x)(y-x), invariance under every sufficiently small radial
blur in both variables is equivalent to trS=divS=DeltaS=0. A solenoidal
virtual field therefore needs to be harmonic as well. On an annulus,
w=(alpha+beta/r^2)Jx realizes a unit inner rotation and zero outer rotation;
the translational full-Dirichlet counterpart is incompatible. The resulting
finite-lag current kernel is

    K(z,zeta)=-beta Im[zeta^2/z^2-2zeta/z].

Two complex bilinear correlations implement it: four real covariances plus
one real normalization covariance. Support disks avoiding the Laurent pole,
full aperture or calibrated tails, linear imaging and the positive connected
particle-pair law are necessary inputs. Arbitrary unknown PSF support is not
covered. PROOF.md gives finite-aperture, integrated-pixel, boundary-strip and
finite-lag obligations rather than granting them.

The simpler full-image covariance has a real statistical cost: for a static
uniform cloud in1<r<2, even with exact means and particle-count normalization,
its variance is [160ln2/27-26/9]/n>1.2/n, independent of particle count.
Subtracting same-frame zero-expectation harmonic controls yields the exact
symmetric current -Q(I1-I0,I1-I0)/2. Under a fixed Poisson matched-pair law,
common per-particle brightness and no camera/photon noise its variance is
O(displacement^4/n), so division by
lag^2 does not incur that particular lag^-4 variance penalty. DDM already
supplies generic image differencing; this is an explicit query specialization.
Different endpoint PSF profiles remain allowed, but BOTH blur disks now must
avoid the pole. Gain mismatch and detector noise can restore a variance floor.

## Actual acquired record and result

The public H015 ZIP has111,703,963bytes and500 512-by-512 uint16 TIFFs.
Its SHA256 is2a1e5b41f44e57c315f1e62ad56e44e6dc6c76eb03171c4cf30735b16562c00c.
The native source is a rectangular turbulent jet. No annulus, torque truth,
calibrated PSF-tail bound or iid reset interface was acquired.

The consumer read every frame, paired adjacent nonoverlapping frames into250
records, and computed the declared query with a pole outside the rectangular
image. It checked every compiled dyadic weight by exact integer arithmetic,
used overflow-qualified signed integer dot products, and enclosed the finite
record's rounding error. Eight real weighted sums plus a total were computed
per frame. The actual maximum pixel value was996.

The full-record empirical normalizer is exactly

    Cov(total I0,total I1)=-28011124984208/6225<0.

Every one of the ten contiguous25-pair block normalizers is also negative.
This is an empirical admission failure, not a population theorem or a PSF
falsification from time-correlated data. A positive normalized particle-law
query is NOT_ACQUIRED. The unnormalized rounded forward statistic is
51,641,645.6612 with arithmetic radius426.6745; the difference-control
statistic is21,728,442.6645 with arithmetic radius95.0903. These are intensity
statistics in declared normalized pixel coordinates, not forces or torques.
The large same-frame controls are retained as diagnostics, not assigned a
population significance without a sampling model.

No after-the-fact sign flip, photometric normalization, alternative pairing,
or replacement denominator was used to turn this record into success.

## Costs and verification scope

Full raw-ZIP acquisition took44.1806seconds. The consumer's recorded
pre-serialization computation took3.194323seconds after imports:
0.070873 for hashing,0.617846 weight compilation,1.799540
TIFF/CRC decoding,0.641121 moment work and0.003262 statistic assembly. It read
131,072,000pixels and used1,048,576,000 weighted scalar multiplications.
The integer weight bank is16,777,216bytes; it retains O(P) weights and only
constant-size sufficient statistics per record. Compilation checks2,097,152
weights; polynomial weights are exact and Laurent weights have32fractional
bits. Overall peak RSS was not measured. The whole-ZIP hash loads111.7MB
before the weight-bank stage, and Python lists during compilation also count
against practical memory. These costs are not just an oracle-call count.
Imports, final JSON serialization and the failed final display are outside
that recorded computation timer; full process latency was not separately
measured. It is not presented as an end-to-end speed comparison.

A separate O(n^2) pair-difference covariance replay matched all six saved
finite-record values and the difference identity in0.058481seconds. It also
certified the static-annulus variance coefficient using rational log bounds.
This replay does not independently decode the images or verify their weighted
sums. Parent's deterministic pixel derivative interface is reused with credit.
The receiver's original final display raised a KeyError after writing both
complete receipts because it assumed a positive normalizer. The guard was
fixed; no full source rerun was used to hide that execution history.

Failed acquisitions also count: Figshare file endpoints returned504s,
several4TU pages timed out, and a631,477-byte remainder of the Neal2015 PDF
timed out after49.9742seconds. Cambridge fallback metadata and65,536 ZIP-tail
bytes cost4.4544+2.6857seconds but yielded no consumed images. The full native
database-description PDF cost6.2311seconds. Exact individual receipts are
preserved; no single total wall-clock budget was measured for all web-tool
search/reading and adaptive research, so one is not invented.

## Strong comparison and remaining boundary

Established single-pixel PIV already obtains Reynolds stresses from raw
correlation shapes, including particle-image and gradient corrections.
Established DDM/variance methods already avoid tracking and reject static
patterns. Established blur-invariant moments provide the mathematical
invariance resource; established virtual-work/pressure-free identities provide
mechanics. An equally informed query-specific ordinary implementation can
combine these tools and use the same moment sums. Historical priority and a
whole-cycle practical separation are NOT_ESTABLISHED.

The useful retained link is an exact mechanical-query/blur compatibility
classification and a concrete finite-bit covariance/control compiler with a
discriminating real-record gate. It has not supplied the desired new physical
discovery multiplier. The next scientifically unpaid operation would be a
native full-volume or rigorously guarded image record with radial-tail,
photometric/noise, matched-particle and temporal qualification sufficient to
admit the query and its torque interpretation. This package does not assume
that access or propose an unauthorized physical experiment to obtain it.

Governing files: PROOF.md, DIFFERENCE_RECEIVER.md, LITERATURE.md,
consume_images.py, DATA_RECEIPT.json, DATA_MOMENTS.json, replay_record.py and
RECORD_REPLAY.json. All earlier research packages were left frozen.
