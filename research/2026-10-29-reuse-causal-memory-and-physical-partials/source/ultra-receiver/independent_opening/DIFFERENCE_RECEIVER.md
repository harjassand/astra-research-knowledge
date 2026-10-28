# A difference-image control variate, and what it actually repairs

This supplements PROOF.md. Generic image differencing and image structure
functions are established methods, notably Cerbino--Trappe, PRL100,188102
(2008), DOI10.1103/PhysRevLett.100.188102. This is a query-specific composition
with holomorphic moments, not a new claim to differential dynamic microscopy.

## 1. Exact zero controls

Write Q(I,J) for the population bilinear harmonic covariance functional in
PROOF.md (5.2). In the full-aperture Poisson/radial model,

    Q(I0,I0)=Q(I1,I1)=0.                                      (D1)

This extension requires BOTH endpoint blur disks to avoid the pole. The
forward-only theorem allowed an endpoint PSF with merely finite second
moment; that weaker contract does not suffice for the Laurent weights now
also used on the endpoint image.

Indeed the single-particle contribution is the same separate-PSF average of
K(x+xi,x+eta); its value is K(x,x)=0. Within one image the mixed brightness
moment is E B_j^2 rather than E B0 B1, but it multiplies zero. The two PSF
integrations are independent integration variables even when the PSF profile
is the same. A pixel-diagonal photon or independent-pixel electronics
covariance also vanishes because K(z,z)=0. General spatially correlated
electronics do NOT vanish automatically. Quantized weights leave the explicit
finite arithmetic errors in the consumer.

Consequently

    -Q(I1-I0,I1-I0)/2
      = [Q(I0,I1)+Q(I1,I0)]/2                               (D2)

in expectation. This acquires the symmetrized finite-lag current

    Fsym = E [K(x,y)+K(y,x)]/2.

It is not exactly the forward finite-lag current. If speed <=U, material
acceleration <=A, ||S||<=Smax and the spatial Lipschitz constant of S is LS on
the particle segments, then its difference from the start-time quadratic
current after division by delta^2 is at most

    Smax [U A delta + A^2 delta^2/4] + LS U^3 delta/2.

This follows by PROOF.md (7.2) for the forward term and by
|D^T[S(y)-S(x)]D|<=LS |D|^3 for the reverse-minus-forward term. For the
annular tensor, Smax<=|beta|/amin^2 and LS<=2|beta|/amin^3 when all segments
stay at radius >=amin. No time-reversal symmetry of the flow is used.

The implementation computes eight real harmonic/polynomial sums plus a total
on EACH image, or eight sums on the signed difference plus the two totals.
The difference query still has four real covariances. A covariance
normalizer is a fifth query and remains a separate positive-denominator gate.
Acquiring only the ten sums used for the original forward query does not
automatically supply this eighteen-sum-per-pair implementation.

## 2. Precise static-pattern cancellation

For a variance comparison ONLY, grant the favorable interface of iid Poisson
particle configurations with expected count lambda, common unit brightness in
the two frames, full capture, radial PSFs satisfying the support contract,
and no camera/photon noise. Invariance holds particle by particle for all
eight weighted image sums. Their values equal the corresponding sums of
the unblurred point particles, even if the two radial PSF profiles differ.
Population means and lambda are granted here to isolate the estimator's
noise; acquiring them is not free in the public-data receiver.

For (D3)--(D7), the Poisson measure is on the MATCHED-PAIR space, with one
fixed intensity lambda nu, where nu is a probability law of the complete
pair (x,y). A deterministic flow applied to Poisson initial locations is a
sufficient example. An unconditioned mixture over a common random flow is
generally a Cox/mixed process instead. The expectation-only common-flow
extension in PROOF.md section5 is not imported into these variance formulas;
it would require separate conditioning and total-variance/mean terms.

For a centered Poisson measure Ntilde of intensity lambda nu and any finite
bilinear kernel k(x,y), the fourth-cumulant identity gives

    Var integral k(x,y) Ntilde(dx) Ntilde(dy)
       = lambda integral k(x,x)^2 nu(dx)
         + 2 lambda^2 integral sym(k)(x,y)^2 nu(dx)nu(dy),     (D3)

after subtracting its mean. This follows by expanding the three pairings and
the one fourth cumulant; no Gaussian approximation is used.

For a static particle cloud and the original K, K(x,x)=0. The normalized
known-mean estimator based on n independent records therefore has variance

    2 integral sym(K)^2 dnu dnu / n,                         (D4)

independent of lambda. Increasing the number of particles does not remove
its unmatched-particle term. For uniform area measure on 1<|z|<2, beta=4/3,
angular integration and elementary radial integrals give the exact value

    [160 log(2)/27 - 26/9] / n > (6/5)/n.                   (D5)

Details: with t=|y|/|x| and q=arg(y)-arg(x),

    sym K = beta/2 [(t^-2-t^2) sin(2q)+2(t-t^-1) sin q].

Its squared angular mean is beta^2[(t^2-t^-2)^2+
4(t-t^-1)^2]/8. Here E r^2=5/2, E r^4=7, E r^-2=2log2/3,
E r^-4=1/4. Substitution yields (D5). Dividing a displacement query by
delta^2 thus amplifies this static-pattern variance by delta^-4. This is an
estimator limitation, not an information lower bound on all image methods.

The difference operation cancels this term exactly for a static cloud,
record by record. More generally let both endpoints obey a0<=|x|,|y|<=b0
and |y-x|<=d. Exact complex factorization gives

    |Delta z^-1| <= d/a0^2,
    |Delta z^-2| <= 2 b0 d/a0^4,
    |Delta z| <= d,             |Delta z^2| <= 2 b0 d.

Thus the bilinear kernel kDelta made from the changes in the eight
single-particle features obeys

    |kDelta| <= C d^2,
    C=|beta| [4 b0^2/a0^4 + 2/a0^2].                        (D6)

The centered quadratic estimator -Q(Delta I,Delta I)/2 has diagonal
kernel equal to [K(x,y)+K(y,x)]/2. Equation (D3) implies, after normalizing
by lambda and averaging n independent known-mean records,

    Var <= C^2 d^4 [1/(4 lambda)+1/2]/n.                    (D7)

If d<=U delta, division by delta^2 leaves a bound independent of delta.
An ordinary unbiased sample covariance or disjoint-record U-statistic can
estimate the means rather than granting them, with its additional finite
sample variance. This is a demonstrated algebraic cancellation of one
specific noise mechanism, not a proven gain in native measurement work.

## 3. Resources not canceled

Common unit brightness is needed for the small-displacement variance
cancellation, although not for the expectation identity (D2). Uncalibrated
pulse-to-pulse gain changes or particle-specific photometric changes add a
nonvanishing feature-difference component at zero displacement. Independent
photon/electronics noise can leave a variance floor even when its expectation
is canceled. The number of photons, gain monitoring and readout covariance
must therefore be charged before claiming favorable delta scaling.

Masking and PSF tails are also not removed by subtraction. With common
brightness, denote the cross-query good-event loss by epsilon=epsilon0+
epsilon1. If the same bounded kernel magnitude M applies to all cross/self
queries, the two self-query tail biases add at most epsilon M times the full
positive pair mass. Combining with PROOF.md (6.1) gives the conservative
normalized bound

    epsilon (2M+Mtrue)/(1-epsilon).                          (D8)

Unequal brightness second moments require their explicit ratios
E B_j^2/E B0B1 in this bound. Integrated-pixel errors likewise apply to
each of the four cross/self positive measures before their signed
combination, rather than treating the difference image as a positive law.

## 4. Actual public-data boundary

The consumer executed all500 published H015 frames, pairing adjacent
nonoverlapping frames into250 records. The exact empirical total-intensity
cross covariance is

    -28011124984208/6225 = approximately -4.4997791139e9.

Every one of the ten contiguous25-pair block covariances is negative too.
The record is a temporally correlated rectangular jet experiment, not iid
resets. These values are not a population impossibility or a calibrated
PSF diagnosis. They do mean that the receiver cannot produce the proposed
positive normalized pair-law output from this supplied record. No sign flip,
gain normalization, frame re-pairing or denominator replacement is silently
used to turn the failed gate into success.

The finite-record unnormalized forward and difference statistics remain
arithmetically acquired, including their dyadic rounding enclosures. The
difference statistic is NOT a torque measurement. A noise-qualified practical
advantage over single-pixel PIV, differential dynamic microscopy or a
query-specific moment method is NOT_ESTABLISHED.
