# Support ceiling for any same-frontier posterior occupation

Every posterior mean and every updated conditional-tree helper is a convex combination of the fixed frontier outcomes. Therefore the entire changed positive occupation, including the posterior diffusion and its new finite completion, is supported in that frontier's convex hull H (and the retained six S3 images). These hulls lie strictly inside the physical PSD domain and cube, so this mechanism cannot directly cancel the cube-face/edge negative completion terms. The old removed prefix occupation also lies in H and was never credited in the current upper bound.

The receiver constructs exact supporting planes from rational frontier triples and checks all frontier points lie on the retained side. In3D, every actual polytope facet has three affine-independent vertices, so the complete supporting-triple enumeration covers all facets. Duplicate planes are harmless. The planes are exact integer inequalities, not floating convex-hull tests.

Let f be the exact represented finite141 scalar volume polynomial and If its continuous tensor nodal hat interpolant on mesh h=1/128. The inherited Fourier Gram certificate gives

    3 ||f-If||_L1(cube) <= 3 sqrt(8)||f-If||_L2(cube) <= vg.

The same entire vg therefore bounds the error over ANY measurable subset H; no local source/error independence is assumed. Since t ->(-t)_+ is1-Lipschitz and convex,

    3 integral_H (-f)_+ <= 3 integral_H (-If)_+ + vg
                            <= 3 h^3 sum_{nodes whose hat support meets H}(-f(node))_+ + vg.

For each node, its tensor hat support is a cube of radius h. If that support intersects a polytope with plane a.x<=b, necessarily a.node<=b+h||a||_1 for EVERY plane. The receiver uses these necessary conditions to select an OUTER cover; it never asserts they are jointly sufficient for intersection. Union all six S3 hulls and deduplicate selected nodes. The exact upward dyadic nodal sum includes the existing2^-29 field guard at every selected node. Boundary nodal zeros and full h^3 weights only enlarge the estimate.

Thus the receipt bounds the maximum possible finite scalar-volume negative trace that ANY positive occupation supported in these hulls can remove, even granting unlimited incoming mass and perfect Loewner cancellation. All original analytic/source/cubic/Gram fees remain unchanged; the entire vg is paid separately for each reported support ceiling. This is a ceiling on credit available in the existing finite-volume ledger, not a lower bound on trueN and not a barrier to deeper frontiers or other source laws.

Results: root-frontier ceiling3.3370348649e-5, negative-helper ceiling3.3659350032e-5, their union4.0449265918e-5. Both small-frontier mechanisms are therefore below the materiality threshold regardless of covariance selector or simulated occupation trace. A large occupation trace concentrated in these small negative pockets does not imply a comparable negative-mass reduction.
