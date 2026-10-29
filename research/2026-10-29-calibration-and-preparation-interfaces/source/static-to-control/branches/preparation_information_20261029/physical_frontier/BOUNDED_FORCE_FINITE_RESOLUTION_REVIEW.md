# Independent review: bounded-force finite-resolution equilibrium closure

29 October 2026. Reviewed by the physical-frontier branch.

Reviewed root file: `BOUNDED_FORCE_FINITE_RESOLUTION_EQUILIBRIUM.md`.

Exact reviewed SHA256:

    c81bcb2e9c36e7eb2e61e63a20364e49b7183b70da6589fb3534f20f9d86e16d

An independent ordinary proof is preserved in
`BOUNDED_FORCE_WEAK_CLOSURE_INDEPENDENT_PROOF.md`, SHA256

    964fed77c8f00b9679ace3638711b0b729886286e79019643b1d5aadb8858fc1

## Verdict and scope

The stated bounded-force weak closure theorem and the fixed-record TV
consequences are valid at the specified source interface. No fatal gap was
found. The missing occupation-compactness bridge has an ordinary proof;
the limiting process is identified as the actual native kinetic equation,
and its conservative force follows from the stationary Maxwell equation.
No uniform force derivative bound, acquired hidden contraction or presumed
Markov closure is needed. The proof is qualitative, and supplies neither
physical acquisition nor an effective rate.

This does not restore full path TV: the prior bounded oscillatory shear
counterexample remains valid. Setwise convergence of each selected
subsequence means convergence on each fixed measurable path event, not
uniform convergence over source-dependent events.

## Load-bearing checks

1. **Conditional terminal variance.** Formula (6) is the correct Schur
   complement. Its bracket has value zero at u=0 and derivative
   `2(1-exp(-u))^2`, hence is positive for every positive smoothing time.
   Arbitrary initial position laws therefore produce a uniformly bounded
   free endpoint density relative to uniform position times Maxwell.

2. **Endpoint L2 bound.** The square of the conditional-likelihood mean
   is bounded by the conditional second moment. One factor of the free
   density is bounded by C_delta before integrating. This yields exactly
   (9), with one C_delta, not an unsupported pointwise bound on the forced
   heat kernel.

3. **Compact occupation.** On the separated-time region, the position-pair
   density is uniformly bounded, including after multiplication by
   conditional bounded signed g factors. Its integral kernel is therefore
   Hilbert--Schmidt. The removed diagonal strip has bilinear operator norm
   at most `2 T epsilon ||g||_infinity^2` by Cauchy--Schwarz and the two
   uniform position marginals. Thus A_g* A_g is compact and hence A_g is
   compact. The same proof permits a fixed bounded time-dependent g, so
   restriction to [s,t] in the martingale argument is legitimate.

4. **Weak likelihood and setwise limits.** The Girsanov second-moment
   estimate is conditional on the initial state; hence multiplication by
   r_j(Z_0) is controlled by the initial L2 norm. Weak L2 compactness then
   produces a nonnegative normalized density R. Every bounded measurable
   path function is in L2 of the free reference law, which is exactly what
   yields setwise convergence. No continuity of that test is required.

5. **Moving force in the martingale problem.** For fixed compactly
   momentum-supported smooth phi, the derivative g=partial_p phi is
   bounded. The moving term vanishes by compact A_g applied to weak L2
   force convergence, followed by the uniform likelihood L2 bound.
   The bounded past multiplier causes no additional compactness demand.

6. **Bounded Borel force uniqueness.** The force perturbation lies entirely
   in the directly forced momentum directions and is bounded. Girsanov
   constructs a weak solution from free Kramers. For any martingale-problem
   solution, coordinate localization gives its momentum Brownian motion;
   inverse bounded Girsanov removes F and gives the unique free law with
   the same initial distribution. Reweighting that common free law gives
   uniqueness. Degeneracy of position noise does not obstruct this argument
   because the altered drift has no component outside the noise range.

7. **Stationarity and Gibbs identification.** The entire smoothed-start
   path law is TV-close to the stationary source, so stationarity passes
   to the setwise limit. The small conditional entropy gives the product
   state nu M. Testing phi(q)p_i gives grad nu=(F/tau)nu in distributions.
   Positive periodic mollification supplies |grad nu_e|<=A nu_e/tau;
   connected compactness and normalization give positive uniform density
   bounds. Thus U=-tau log nu is periodic Lipschitz and F=-grad U a.e.
   This step does not multiply two unidentified weak limits.

8. **Smooth same-bath approximation.** Mollifying the potential preserves
   the gradient amplitude ceiling and gives strong L2 force convergence.
   The limiting Gibbs density is bounded above and below. Consequently the
   initial KL and finite-window Girsanov energy both tend to zero in (17).

9. **Record consequences.** For fixed countable output, convergence of
   every probability gives discrete Scheffe convergence. For a fixed
   dominated kernel, the asserted pointwise boundedness in the path
   variable lets setwise convergence act on each output density; ordinary
   Scheffe then gives TV. For a uniformly TV-Lipschitz family the event
   probability functions have supremum <=1 and Lipschitz constant <=C,
   so the stated max(1,C) factor against d_BL is correct.

## Optional clarification, without changing the theorem

The Gaussian sensor-family sentence should be read with a uniform
Lipschitz gain bound on every reported state feature, a positive noise
floor and finite observation budget. Fixed gain alone, if it does not
bound spatial feature sensitivity, does not supply that property. Passive
adaptive settings based on previous noisy reports are permitted: when
comparing conditional report kernels at a common history, those settings
are identical. A physical feedback force remains outside the theorem.

The numerical positive-density bounds in Section 6 use densities relative
to normalized uniform position measure; with unnormalized Lebesgue density
they acquire the torus-volume factor. No proof step depends on that
normalization convention.

## Additional valid consequence

The independent proof also gives convergence in Wasserstein-2 for the
unbounded uniform path metric along the identified subsequences, hence
vanishing distance to the same smooth Gibbs class in that metric. Bounded
forces give uniform stationary momentum moments of every fixed order by
the OU variation-of-constants formula (or a polynomial Lyapunov test),
and corresponding finite-window supremum moments. Weak convergence plus
uniform integrability then gives Wasserstein-2 convergence. The root
bounded-Lipschitz statement does not need this strengthening.

## Literature status

The proof uses established Gaussian logarithmic Sobolev, Girsanov,
Hilbert--Schmidt compactness, martingale-problem and Scheffe machinery.
A targeted primary-source search returned general kinetic Fokker--Planck
well-posedness and entropy-current papers; it did not settle priority for
this exact low-dissipation, bounded-force, native-Gibbs, fixed-record
closure conjunction. The theorem is therefore supported by the ordinary
proof, without a priority claim or a claim of a new Gaussian kernel.
