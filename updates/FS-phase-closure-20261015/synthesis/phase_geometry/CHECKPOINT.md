# phase_geometry continuation checkpoint

Date: 15 October 2026.

## Completed core, frozen before late work

`CORE_MANIFEST.json` pins the following five files by SHA-256:

* `REDUCED_PHASE_OBSTRUCTION.md`: complete analytic counterexample to convexity
  of the phase value **after full fixed-mass amplitude minimization**. The
  periodic version uses N=32. The affine-boundary version uses N=1024, common
  boundary `u=delta e1`, common fourth mass one, positive trial amplitudes, zero
  winding, and phases in a half-plane chart. The integrand is convex `|A|^4`.
  Endpoint reduced energies are at most 2381/144<17; midpoint value is >=17
  (strictly >17 if using the supplied attainment theorem). No QC counterexample.
* `TRANSLATION_GAUGE_AND_SOFT_OPERATOR.md`: exact projective chart and fixed-mass
  variational limit as target translation R tends to infinity. It converges
  to scalar row minimization with a zero-mean constraint. A small phase chart
  retains arbitrary transverse gradients after its necessary scaling.
* The same note gives G's singular reduced acoustic symbol at I and the exact
  compatible potential expansion for `phi=((2/3)v_y,v_x)`.
* `verify_phase_geometry.py` and `exact_checks.json`: eight exact finite groups
  passed. These check constants/algebra, not the analytic variational proofs.
* `SOURCE_LEDGER.json`: repository pin, immutable input hashes and primary sources.

The root reports having fully read the main reduced-phase proof and checked
its analytic constants. This is same-team review, not external validation.

## Late work kept separate

`LATE_RESONANCE_STATE.md` preserves two additional exact obstructions:

1. No determinant-affine tangent support exists in any neighborhood of I for G.
   The unique quadratic correction is `+det(H)/2`; an explicit rank-two path
   makes its corrected Bregman remainder negative at arbitrarily small scale.
2. The cubic soft-potential term cannot be controlled by the quadratic cost and
   quartic terms in p,q alone. A fixed exact resonant potential under anisotropic
   scaling proves that r=v_yy, or an equivalent nonlocal norm, is indispensable.

`verify_late_resonance.py` and `late_exact_checks.json` passed four independent
exact groups, including direct Laurent zero-mode integration of selected triads.

`probe_soft_triads.py` and `soft_triad_probe.json` contain ONE bounded discovery
probe, with 328 noncollinear cosine triads and 1711 squared-amplitude grid points
per triad. Maximum observed `C^2/(4QD)` was about 0.00089293. The selected ratio
is exactly 398644400/446444401849<1/1000. No negative witness was found. This is
not a continuum bound, an exhaustive search, or evidence of general QC.

No further triad grids or generic alternating phase searches are warranted by
the result. The `nonlocal_compensation` worker is pursuing a complementary
many-mode genuinely resonant construction; it has the exact potential formula.

## Precise unresolved mathematical obligation

For arbitrary smooth periodic v, let p=v_xx, q=v_xy, r=v_yy and K be the exact
quartic in Section 6 of the core note. Determine the sign of

    (5s^2/12)<p^2> -(5s^3/162)<q(9p^2+4q^2)> +s^4<K>.

Neither `<K>>=0` nor the needed compensated cubic bound against `<p^2><K>` is
established. The original arbitrary-phase affine-boundary QC comparison also
remains unresolved. Any negative candidate requires exact compatible Fourier
integration or an independently verified continuum certificate.

Historical novelty, external mathematical correctness and full planar QC are
UNKNOWN / NOT_ESTABLISHED. No original input, existing repository history, or
old worker artifact was modified. All outputs are confined to this directory.

## Replays

    python3 verify_phase_geometry.py
    python3 verify_late_resonance.py

The optional exploratory probe uses NumPy:

    python3 probe_soft_triads.py

Its coefficients are rational; grid arithmetic is floating point. Running it
again is unnecessary unless the implementation changes or a concrete new
candidate justifies a different family.
