# Sharp constant-stage law and the slower-control improvement

[Return guide](README.md) · [Finite-stage proof](package/invention_geometry/finite_stage_rotation.txt) · [First-variation proof](package/invention_variation/slower_loop_derivation.txt) · [Independent audit](package/invention_holonomy_audit/audit.txt)

## A specified number of constant forces

For an attenuated rotation `exp(-s)R_theta`, `0<|theta|<=pi`, using at most `n` constant symmetric positive-control stages, the supplied theorem gives

```
s_n = n acosh(cos(pi/n)/cos((pi+|theta|)/n))
reachable iff n > 2+2|theta|/pi and s >= s_n
T_min,n = (s+s_n)/Lambda
kappa_max,opt = exp(2s_n/n).
```

With `ell=s_n/n` and `delta=sgn(theta)(pi+|theta|)/n`, the positive factors

```
H_j = R_(j delta) diag(exp(-ell),exp(ell)) R_(-j delta)
```

multiply to `R_theta`. Scaling each by `exp(-s/n)` makes physical contractions realizable by constant admissible controls. The construction attains both the time bound and the optimum worst factor condition number.

Normalized positive factors form a hyperbolic polygon whose area records rotation and whose perimeter records total strain. Classical polygon isoperimetry and a convexification argument cover self-intersections and extra winding. The geometry is credited to established mathematics. The known factorization paper already gives minimum counts and examples; its illustrative condition number is not treated as a lower bound against its method. For five factors producing a 180-degree rotation, the exact optimum is about `25.3770021071485`.

The stage bound also applies to local response at a common stationary minimum of stagewise fixed nonlinear `C^2` convex potentials with the same Hessian cap there. Moving minima and trajectories through varying Hessians are outside that extension.

## The stronger all-duration objective fails

At least possible contraction `s=L_theta`, every admissible shape must be shortest; slowing or pausing adds positive covariance. The fastest construction is therefore radially optimal across all durations at that boundary.

For every nonzero principal angle and every `s>L_theta`, the source instead constructs a smooth admissible deformation preserving the exact same target matrix with

```
Delta tr(Q) = -c epsilon + O(epsilon^2), c>0
Delta T = O(epsilon^2)
Delta W_net = O(epsilon^2).
```

Thus any objective with positive mean-square-noise weight and finite nonnegative time/work weights improves for a sufficiently small deformation. The fastest point remains Pareto efficient: the improvement costs extra time and work. The full slower-time optimum is not solved, and improvement of every radial tail is not claimed.

At the supplied illustrative `theta=pi/2`, `s=L_theta+0.05`, `D=Lambda=1`, duration rises from `7.074814731` to `7.076363501` while `tr(Q)` falls from `5.815416499` to `5.783020919`. These are model calculations rather than measurements.

The [finite-stage recorded checks](package/invention_geometry/finite_stage_checks.json) and [slower-loop example](package/invention_variation/slower_loop_counterexample_results.json) accompany the analytical proofs. The source reports 45 high-precision stage attainments, 120 independent polygon checks and an independently audited all-angle first-variation proof. Capital preserved the files without rerunning them.
