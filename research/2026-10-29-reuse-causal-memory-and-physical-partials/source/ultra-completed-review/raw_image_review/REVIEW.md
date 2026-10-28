# Independent whole intake of the raw-image mechanical query

**ACCEPTED at the corrected conditional mathematical and finite-record scopes.**
This is a whole scientific/code intake of `independent_opening/PROOF.md`,
`DIFFERENCE_RECEIVER.md`, `LITERATURE.md`, `RESULT.md`, `consume_images.py`,
`replay_record.py`, their saved inputs/outputs, the source description and the
parent pixel interface. It reconstructs the mathematical chain and reads the
entire consumer. It is not a second run of the 131-million-pixel computation.
The public images are real experimental input. A normalized positive pair-law
query and a physical annular torque measurement remain **NOT_ACQUIRED**.

The producer incorporated two premise clarifications raised during this intake:
the brightness marks have finite second moments, and displayed random image
sums lie in L2; and the favorable variance theorem uses a fixed Poisson law on
the matched-pair space. A finite mixed brightness moment alone would not make
the image covariances exist. Poisson initial locations followed by an
unconditioned shared random flow need not give the fixed pair-space Poisson
law required for the fourth-cumulant calculation. The corrected proofs state
both limitations. No numerical source or protocol was changed.

## 1. What is actually invariant

For `f(x,y)=(y-x)^T S(x)(y-x)`, I independently obtain

    Delta_y f=2 trace S,
    Delta_x f=(y-x)^T Delta S (y-x)-4 div S dot(y-x)+2 trace S.

Circle averages of every sufficiently small radius give necessity of separate
harmonicity, and the harmonic mean-value theorem gives sufficiency on disks
contained in the harmonic domain. Vanishing of the polynomial in `y-x` gives
`trace S=div S=Delta S=0`. In two dimensions, writing
`S=[[a,b],[b,-a]]` turns the first two conditions into the Cauchy--Riemann
equations for `a-i b`, so the last follows. This establishes exactly the
declared quadratic family, not arbitrary estimators or arbitrary unknown blur.

For `S=sym grad w` with `div w=0`, `div S=Delta w/2` is the needed link.
The annular field `w=(alpha+beta/r^2)Jx` has the two required rotational wall
values and is incompressible and componentwise harmonic. At the real point
`z=r`, its off-diagonal strain is `-beta/r^2`; this independently fixes the
sign and factor in

    D^T S(z)D=-beta Im(D^2/z^2).

The proposed translating annular trace has the unique componentwise harmonic
extension `(log(R/r)/log(R/a),0)`, with nonzero divergence. Thus translation is
excluded in this field/kernel mechanism. The parent's stronger arbitrary-domain
obstruction is also sound; a separate independent derivation is in
`FORCE_REVIEW.md`. It does not exclude force measurement by other mechanisms.

For the optical identity, `E eta=E eta^2=0` uses a *complex square*, not
`E|eta|^2=0`. After averaging the endpoint PSF, the start variable occurs in a
holomorphic function on its full support disk. That disk must avoid the
Laurent pole. Finite second endpoint moment is sufficient for the forward
quadratic endpoint average. The difference/self controls additionally use
Laurent weights on the endpoint image, so BOTH endpoint disks must avoid the
pole. A Gaussian of unrestricted support is not automatically an admitted
start PSF; neither is an unknown tail or a square pixel.

## 2. Particle law and the five real covariance queries

Under the declared linear-imaging, fixed matched-pair Poisson model, finite
brightness/image moments and independent between-frame electronics, Campbell's
identity gives the connected image covariance as a positive matched-pair
measure. The mark factor is the common mixed moment `E B0 B1`. Cross-particle
terms cancel against the product of means. Arbitrary common pulse gain, a
common-flow mixture with changing conditional means, nonlinear camera response,
unmatched entry/exit, tracer/out-of-plane losses and correlated electronics
are not silently in that model.

The complex convention is **bilinear, without conjugation**:

    Im Cov(A,B)=Cov(Re A,Im B)+Cov(Im A,Re B).

Consequently the consumer's index/coefficient list

    (A2r,B2i,-1), (A2i,B2r,-1),
    (A1r,B1i, 2), (A1i,B1r, 2)

is exactly `-Im Cov(A2,B2)+2 Im Cov(A1,B1)` at beta=1. These are FOUR real
numerator covariances. A positive normalization adds ONE real total-intensity
covariance. There is no hidden conjugation or missing imaginary contribution.
The minimal forward feature access uses four real start weights, four real
endpoint weights and two totals. The executed difference/diagnostic consumer
actually acquires eight weights plus one total on EACH frame; it does not
pretend the original ten summaries already supply those eighteen summaries.

With full capture and the stipulated brightness law, the population
normalizer is positive and proportional to expected matched particle count.
It is not an observed particle count, nor a guaranteed positive finite-sample
covariance. Positive empirical normalization is a necessary admission gate of
this implemented normalized output, not a population confidence theorem.

## 3. Aperture, pixels and mechanical interpretation

The normalized tail estimate follows by writing the population numerator and
mass as `pG F+b` and `pG+q`, with `pG>=1-epsilon`, `q<=epsilon` and
`|b|<=q M`. The stated bound
`epsilon*(M+Mtrue)/(1-epsilon)` is correct. It requires a bounded implemented
kernel that agrees with the analytic query on the good event, true-pair guard
regions, and the stated independent shift-invariant radial laws/tail bounds.
An unobserved tail is not estimated by the finite camera itself. Excluding
near-wall material changes the target; the producer correctly charges its
current/mass using an extra bound rather than just its area.

I checked the parent derivatives directly:

    Lx=2|beta|(b0^2/a0^3+b0/a0^2),
    Ly=2|beta|(b0/a0^2+1/a0).

They give the claimed integrated-photon pixel-center error, without assuming
uniform mass inside a pixel. Discontinuous mask boundaries require a separate
strip argument. The declared rectangle's general bound is approximately
0.0258898 before any lag-squared conversion. This loose upper bound is not an
actual pixel error or a physical accuracy certificate. Signed difference
images require applying the positive-measure error bound before subtraction.

For the mechanical sign, the auxiliary field equals `Jx` only on the inner
wall. Integrating steady, unforced incompressible momentum against it gives
the traction torque on the FLUID as `-rho integral uu:S +2mu integral Du:S`.
The body torque has the opposite sign. A second integration yields
`2mu integral Du:S=4pi mu beta(Omega_i-Omega_o)`, giving the producer's (7.1).
Pure Couette flow has no convective term and the resulting body torque
resists the imposed relative rotation, which independently checks the sign.
The image term supplies an excess over this known viscous wall contribution,
not the whole scalar torque by itself.

The corrected formula explicitly assumes no body force and a steady or
stationary-mean balance. Known forcing adds `rho integral w dot b` and a
nonstationary balance adds `-rho integral w dot partial_t u`. Full-volume
coverage, no penetration, wall velocities, material parameters, uniform
spatial seeding and omitted-region/endcap corrections remain necessary.
A planar slice of a finite-height experiment does not acquire them.

The finite-lag bound follows from material acceleration:
`|D/delta-u(0)|<=A delta/2`. For the difference estimator the extra endpoint
tensor difference pays `LS U^3 delta/2`. No time-reversal symmetry is required.
The bounded-speed/acceleration model, physical pixel scale and lag are not
acquired merely from the two images. The executed rectangular-jet statistic
has beta=1 and an artificial pole outside the picture; it is not converted
into an annular experiment by that coordinate choice.

## 4. Difference control and what its variance theorem means

In the admitted full-aperture radial model the self queries have expectation
zero: the independent PSF integration variables average the diagonal kernel
to `K(x,x)=0`. Pixel-diagonal shot/electronics contributions also have zero
analytic kernel diagonal; spatially correlated noise does not automatically
cancel. Therefore

    -Q(I1-I0,I1-I0)/2 = (Q(I0,I1)+Q(I1,I0))/2

in expectation. It measures the SYMMETRIZED finite-lag current, rather than
identically the original forward current.

For the fixed matched-pair Poisson law of intensity `lambda*nu`, the Poisson
fourth cumulant and pair contractions give

    Var integral k dNtilde dNtilde
      =lambda integral k(t,t)^2 dnu(t)
       +2lambda^2 integral sym(k)(s,t)^2 dnu(s)dnu(t).

The mean-square contraction is subtracted. This proves the literal formula;
there is no Gaussian particle approximation. For a static uniform annulus,
`E r^2=5/2`, `E r^4=7`, `E r^-2=2log(2)/3`, `E r^-4=1/4` reproduce
`[160log(2)/27-26/9]/n`, approximately `1.21865/n`. The particle count cancels
from this unmatched-particle variance term. Here **n is a number of independent
configuration/record draws**, and lambda is expected particles per draw.
Neither is the number of pixels or the actual record's claimed effective
sample size.

For common unit brightness and noiseless linear full capture, radial blur
preserves all eight single-particle features exactly. A static cloud then has
zero feature difference record by record, even if the two radial profiles
differ. For displacement at most d, the four feature-difference inequalities
give `|kDelta|<=C d^2`; including the control's factor `-1/2` gives exactly
`C^2 d^4*(1/(4lambda)+1/2)/n`. These constants and the favorable lag scaling
are sound at the explicit ideal variance contract.

That is not a variance formula for the actual random ratio Qhat/Nhat, for a
Cox/shared-flow mixture, or for a noisy brightness-varying record. Exact means
and lambda are granted in this comparison. Unknown means, gain/pulse changes,
photon/electronics noise and their acquisition can restore a floor. Generic
DDM already supplies static-image differencing; this composition is a useful
specific control identity, not an established native-work advantage.

The difference tail bound also checks: each same-frame tail has at most twice
its single-frame tail mass, and the factor 1/2 makes their combined extra
numerator at most `epsilon M`. Combining with the forward normalized bound
gives `epsilon*(2M+Mtrue)/(1-epsilon)`. Unequal brightness second moments need
the ratios explicitly named by the producer.

## 5. Exact consumer and native record boundary

I read the full source-to-output consumer. Its coordinate denominators,
Laurent real/imaginary signs, exact polynomial weights and 32-bit rounding
formula are correct. Each compiled rational weight is checked within half a
unit. The absolute-product bound below 2^62 pays NumPy int64 dot products;
chunk totals are accumulated as Python integers. The polynomial weights are
exact because their dyadic denominators divide 2^32.

The sample covariance is the ordinary unbiased algebraic expression at the
level of saved finite records; unbiasedness for a population still needs an
appropriate record law. Its rounding enclosure is valid because covariance
is linear in the rounded Laurent feature and the polynomial feature is exact.
For a difference image the error uses its actual L1 pixel difference, rather
than granting cancellation of rounding errors. The four-query triangle bound
and the exact rounded difference identity are correct. Floating centers are
displays; rational endpoints carry the arithmetic claims.

The standard-library `inspect_native.py` independently checked the archive's
500 consecutively numbered members, ALL 250 saved pair-label mappings, and
four existing TIFF IFDs (first three and last). Those four are single-page
512-by-512, 16-bit, one-channel TIFFs. This addresses an actual possible
single-frame/multipage ambiguity; it does not assert independent header or
pixel decoding of the other 496 members. The producer's complete read/CRC and
weighted-sum stage is accepted through its code/input/receipt scope, not
represented as a second reviewer pixel implementation.

The paired records are literally `(B00001,B00002)`, `(B00003,B00004)`, ...,
`(B00499,B00500)`. The primary database description says time-series mode;
it does not grant IID resets or a per-file calibrated lag/gain. The native
sample headers inspected here contain no timestamps. The author-host source
is a rectangular jet and supplies images/reference PIV data, not a torque
truth or full annular volume.

Independent integer recomputation from the supplied totals gives

    Cov(total0,total1)=-28011124984208/6225<0.

All ten declared 25-pair blocks give the same negative signs and exact values
recorded by the producer. There are no normalized-output keys in the receipt.
Thus the failed admission is genuine for the declared record/pairing. It is
not a positive normalized physical output, and not a finite-sample population
model rejection. No sign flip, pulse-gain correction, alternative re-pairing
or replacement denominator is inferred or performed.

The original consumer's final display KeyError occurred after both full
receipts were written. The corrected optional-key guard is correct. Its
history remains in EXECUTION_NOTE; no source rerun was used merely to conceal
the display failure. The producer's O(n^2) saved-moment replay is accurately
described as an arithmetic route, not independent image decoding.

## 6. Strong ordinary comparison and scientific disposition

The controlling single-pixel stress paper directly estimates normal/shear
stresses from image-correlation shapes and explicitly pays image-diameter and
gradient broadening. I read its primary sections 2.1--2.3 and 3.1, including
the finite-pixel integration and autocorrelation-based diameter correction.
It is a much stronger competitor than mandatory particle tracking or a dense
P-by-P covariance construction. [Scharnowski, Hain and Kähler](https://link.springer.com/article/10.1007/s00348-011-1184-1).

The acquired primary DDM text already uses image differences to remove static
contributions and analyze dynamics, while the aperture paper gives a concrete
boundary artifact and an apodization repair. Windowing changes this harmonic
target and so still needs a correction; the ordinary method receives that
option. [Cerbino--Trappe](https://arxiv.org/pdf/1507.01344),
[Giavazzi et al.](https://arxiv.org/pdf/1707.07501).
Flusser et al.'s acquired primary section 5.4 establishes radial/complex
moment antecedents, so generic radial-blur invariance is not a new claim.

The retained operation is an exact compatibility classification and a
query-specific finite-bit raw-image covariance/control compiler, with a real
record that discriminates an unpaid gate. A source-aware ordinary method may
combine the same moment identities, covariance statistics and weak mechanics.
Neither historical priority nor a practical/civilisation-level advantage is
established. The existing record fails the required positive-normalizer
admission and lacks the other native optical/mechanical/statistical inputs.
This is an appropriate completed conditional construction and a decisive
source-scope failure, not an acquired torque instrument.

Costs remain charged: the producer's raw ZIP retrieval, all failed/partial
acquisitions, 3.194323 seconds of pre-serialization source computation, eight
weighted sums per frame, storage/hash/list memory and its saved-record replay.
The independent metadata/normalizer check here took 0.0054303 seconds after
imports, with no new dataset, trajectory, physical action or full producer
rerun. The initial attempt to use Pillow failed because it is absent in this
worker runtime; no package was installed. Direct web access to the two native
PIV URLs also failed, so the previously acquired primary bytes were read
locally rather than silently claimed as newly fetched. There are no open
mathematical or consumer corrections at the corrected stated scope.
