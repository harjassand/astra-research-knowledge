# Independent review: parity projection and local thermalization

29 October 2026. Reviewer: producer-workspace/different_consequential_opening.
Reviewed root file: REVERSAL_PROJECTION_AND_LOCAL_THERMALIZATION.md.
SHA256: 19537e32a489dd0703d380133fb1dbf1c98c3ffa5d6dc53ecd034a7a4888336d.

## Finding and scope

The finite-state generalized stationary-flux projection, its full-horizon
Pythagorean identity, the weighted scalar quarter inequality, and the
Hellinger/JS local-thermalization receiving step are correct as stated.
No substantive gap was found in those ordinary proofs.

The diffusion receiving statement is correct under its declared common noise,
physical reversal, existence, stationarity and Girsanov assumptions. This review
does not prove existence/nonexplosion for every formally constructed drift,
nor a same-calibrated-thermal-class realization.

## Scalar quarter inequality

With the root's variables, the weighted Jensen gap is s D_B(r||alpha).
Differentiating its displayed J gives exactly

    J''(r)=4/[r(1-r)]+(2r-1)^2/[r^2(1-r)^2],
    D_B''(r)=1/[r(1-r)].

At r=alpha, J-4D_B and its derivative vanish. The convexity proof therefore
holds for unequal p,q as well; the quarter is not an equal-weight convention.
Limits cover zero rates using extended divergences.

The summation uses equality of the two stationary reversal-related rates,
not equality of their pointwise integrands. That equality is valid because
physical path reversal is an involution: D(P||RP)=D(RP||P). Initial reversed
KL boundaries also agree, leaving equal rates. The argument similarly applies
against a reversal-invariant projected path law.

## Generalized flux projection and Pythagoras

The parity-transpose transform of a balanced edge flux remains balanced.
Its average F generates a stationary chain with mu. Flux symmetry plus
mu symmetry gives the paired holding-rate equality needed for path reversal.

The delicate source-state logarithm h(z)=log(nu_z/mu_z) is parity even.
Its f-weighted outgoing average equals its F-weighted average since

    sum_w g_zw=sum_w f_{theta w,theta z}
              =sum_w f_{theta z,w},

by original flux balance; relabeling z to theta z uses h(theta z)=h(z).
The proof therefore does not assume rho itself is parity symmetric.

The edge log(F/G) is parity-transpose even, and the holding-rate difference
is parity even. Both averaging replacements are valid. Initial-law Pythagoras
follows from the even log(mu/nu). The exact full-horizon identity identifies
one minimizer for every positive horizon on the supplied state set/parity.
No optimization over unknown hidden realizations or thermal classes follows.

## Local form and JS/Hellinger

The commuting symmetric form splits into orthogonal even/odd sectors. Its
odd gap controls f-Uf without an even-sector gap. All root constants follow.

The scalar JS and Hellinger generators have second derivatives
1/[2t(1+t)] and 1/[4t^(3/2)], respectively. Their ordering is equivalent to
2 sqrt(t)<=1+t. Both generators and first derivatives vanish at one, so
JS<=1-affinity has the stated normalization. No KL boundary bound is inferred.

## Qualified diffusion extension

The density-weighted drift average is the Markov projection of the equal
stationary forward/reverse path mixture. Stationarity follows from linearity
of rho b and rho D; physical reversibility follows by reversing that mixture.

The sum of projected Girsanov rates is

    (1/4) integral rho q/(rho+q) |b-bR|^2_(D^-1),

whereas the sum of relative reversal rates is

    (1/4) integral (rho+q) |b-bR|^2_(D^-1).

The pointwise quarter bound and equality of the reversal-related rates give
the result. For state-dependent diffusion, "common diffusion" includes the
parity covariance D(z)=Theta D(Theta z) Theta^T. This is currently implicit
in the shared forward/reverse noise; stating it explicitly could improve clarity.

Kinetic position drifts agree, so drift differences lie in the momentum
diffusion range. The range condition is appropriate. Well-posedness and
integrability remain substantive analytic premises.

## Exact executable control

check_parity_projection.py uses rational arithmetic and prime-log coefficient
identities for a four-state parity-asymmetric source. An independently chosen
reversible H has a different stationary distribution. Exact residuals vanish
for initial Pythagoras, rate Pythagoras, reversal-rate symmetry and projected-rate
symmetry. I/sigma is approximately 0.2410869536772747.

Those floats are descriptive, not interval certificates. The ordinary proof
establishes the uniform scalar inequality. An initial attempted checker required
an unavailable symbolic package; it was replaced with a dependency-free
fractions implementation before the reported successful execution.

## New same-class challenge

HIGH_FREQUENCY_THERMAL_COUNTEREXAMPLE.md constructs bounded transverse forces
A sin(kx) in kinetic Langevin dynamics. Entropy tends to zero while every native
same-bath equilibrium remains at full-path KL rate at least A^2/(8 gamma T).
The free equilibrium is the exact best native equilibrium at each horizon.
The one-time density nevertheless converges to free Gibbs in KL.

Root independently reached this same family before receiving this derivation.
Its additional score/TV and path-Wasserstein extensions are reviewed in the
counterexample note. Neither result claims historical priority.

