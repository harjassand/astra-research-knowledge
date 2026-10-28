# Finite external coils for the exact irrational reference tube

An explicit finite filament-coil representation has been constructed and numerically evaluated for the reference paraboloidal field of [Sengupta et al., 2610.28466v1](https://arxiv.org/html/2610.28466v1). With 256 coils on `psi-psi_axis=.25`, the maximum relative vector-field error over 725 declared interior test points is **5.0456e-5**. This supplies a replayable finite implementation of the source field. It does not establish preserved magnetic topology, particle confinement, manufacturable conductors, novelty of current-potential theory, or an advantage over ordinary optimized stellarator coils.

## Acquired geometric and current interface

The source member has `K'/K=5/2`, `v0=delta=0`, `u0=acosh(sqrt(5)*sech(2*pi/5))`, and exactly constant irrational transform `1/sqrt(5)`. The complementary worker's complete-tube argument in `../../sengupta_constructive_bridge/MATHEMATICS.md` closes a prerequisite that a sampled surface alone would not close. The parent read the argument and its entire interval verifier, checked the flux-label monotonicity and explicit inverse, and independently replayed the interval calculation in this folder's runtime.

The parent also read and independently reran the complete `web_and_label_identities.py`: exact rotated-map/inverse, flux-label Hessian and full field-label tangency identities pass, using the stated real Jacobi addition/quartic identities. The replay is `runtime/results/web_and_label_identities.json`. These are algebraic checks plus the domain argument, rather than merely a small numerical `B dot grad(psi)` residual.

On the axis-connected tube `0 <= psi-psi_axis <= 1/4`, the profile coordinates satisfy `|kappa*(u-u0)|, |kappa*v| < .731`, `u-|v| > .00325081429`, and `D > 1.1505363e-5`. The map is globally injective on `u>|v|`: in rotated Cartesian coordinates it reduces to `X+=p*cos(t), X-=-q*sin(t)`, with positive `p,q`. Eliminating them gives a strictly decreasing scalar equation for `sin(t)^2`, with the endpoint cases also uniquely recoverable. Thus this is a complete embedded torus. The replay is in `runtime/results/reference_tube_certificate.json`; this acceptance concerns that geometric statement, conditional on the printed analytic source formulas, rather than the entire source article or its forthcoming companion.

For the source harmonic field `B=grad(Phi)` tangent to this torus, the ordinary Maxwell sheet current `K=-n_out x B/mu0` gives the exact interior field and zero exterior field. Its potential has circulation

`C = 4*pi/(kappa*k) = 63.77936271196601`.

The phase `alpha=2*pi*Phi/C mod 2*pi` is a primitive circle map on the surface. Its level sets are closed meridional current loops, although the magnetic field lines themselves have irrational transform. Discretize these equipotentials at `alpha=2*pi*(j+.5)/N`, carrying `I=C*B_star*L_star/(mu0*N)` each. Coarea converts the sheet into a continuous average of these loop currents; its Riemann sums converge uniformly on a compact interior target region separated from the sheet. No usable numerical uniform-error constant has been certified here.

The implementation evaluates the source logarithmic Jacobi potential, unwraps its two phases, solves each surface radius by bisection, inverts the phase numerically, and differentiates the periodic physical loop by Fourier differentiation. The map has **negative** determinant `det(DX)=-P*D`; current therefore follows decreasing coordinate theta. The initial increasing-theta run approached `-B`, was corrected, and remains in `INITIAL_ORIENTATION_FAILURE.json`. This was an implementation sign failure, not evidence against the source field.

## Declared finite tests and independent controls

The 725 targets use surface shifts `0,.025,.1`, twelve poloidal phases where off-axis, and 29 offset toroidal phases. These are deterministic held-out geometry points, not a uniform enclosure or random sample.

| Coils | Maximum sampled relative vector error |
| ---: | ---: |
| 32 | .408900 |
| 64 | .0915570 |
| 128 | .00713549 |
| 256 | .0000504560 |

At 256 coils the RMS error is `1.77604e-5`; the sampled axis maximum is `2.04e-11`, while the outer target surface controls the overall error. Reporting only the axis would hide the actual limitation. Doubling loop/phase grids from `256/1024` to `512/2048` at fixed 128 coils changes computed fields by at most `4.73e-8` relative to the source. Maximum equipotential tangency residual at the final grid is `3.84e-9`; surface-label residual is `3.02e-14`.

An independently coded exact straight-segment Biot-Savart formula, using successively finer polygons of the same Fourier curves, was tested on 66 declared control targets. Its maximum differences from the smooth-curve quadrature were `1.376e-5, 3.440e-6, 8.601e-7` for 512, 1024, 2048 polygon segments respectively. This separates finite shape error from the original smooth quadrature and shows the expected refinement behavior. Independent source-gradient pullback residual is `2.40e-14`; direct axis circulation is `63.779362711966`, agreeing with the analytic circulation. These are numerical controls, not directed interval field integration.

## Costs, comparison and remaining decision

The final 256 loops have lengths `1.49748` to `1.51161` in source length units, totaling `385.20306*L_star`, with per-loop current `0.24913814*B_star*L_star/mu0`. Increasing coil count lowers each current while increasing conductor length and reducing available spacing. Finite conductor cross-section, global self-clearance/reach, current-density limits, field metrology, forces, supports, thermal/quench behavior and full manufacturing costs have not been acquired. No physical coil was built.

The final five-case spectral construction took about 41 seconds locally; the independent segment control took 2.30 seconds. The retained orientation failure and earlier spline-tangent run add about 53 seconds. These figures exclude source retrieval, mathematical derivation and tool overhead. They are not an advantage claim or full research cost.

Ordinary current-potential/optimized-coil methods remain the appropriate comparator. No free-shape REGCOIL or matched ordinary optimized stellarator design was executed here. The exact field's strong magnetic mirror/action variation is a separate problem: a small coil field error cannot repair a source confinement defect, and the reference's zero shear does not justify invoking a nonzero-twist KAM theorem. The meaningful next decision is whether a finite-volume member with useful action closure survives an equally informed confinement-and-coil comparison; merely increasing coil count has low marginal scientific value now.

Replay `construct.py`, then `controls.py`, with one BLAS thread and `PYTHONDONTWRITEBYTECODE=1`. `RESULTS.json`, `CONTROLS.json` and `finite_coils.npz` retain actual curves, fields and costs. The copied source module has SHA-256 `d2ca141a06950c964bcd099625a9f7b6d9bee7facdf6893bc8e75a04e530ae72`. Civilisation-changing technology: **NOT_ACHIEVED**.
