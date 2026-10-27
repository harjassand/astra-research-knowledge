# Peak2 pointwise reverse-logdet route: diagnostic status

27 October2026. No sign theorem is claimed here.

Target: for every actual physical-qutrit Hermitian A with EA=0 and ||A||≤1, prove or falsify

2logdet(I−T_A A/2)−logdet(I+A)≥0.

Root supplied the source-native Bregman integral showing that this pointwise inequality would pay whole relative peak2 with arbitrary marginal conditioning. The test variables below are actual A matrices, not independently chosen spectra.

Analytic-gradient L-BFGS searches on the norm sphere gave no negative candidate. Real Hermitian: reference dimensions2,3,4,6, ten seeded starts each, norm.999. Best values were about.13500167661 for reference2 and.11145994961 for references≥3. Complex Hermitian: references3,4,6, radii.25,.75,.999999, five seeded starts each. Best values matched positive isotropic directions, with additional larger positive negative-isotropic stationary points. These are finite floating diagnostics, not global minima certificates.

For reference≥3 the repeatedly observed small positive pattern is A=r(9P_Φ−I9)/8, padded by zero on unused reference dimensions. Its exact logdet difference is

F(r)=4log(1−r/8)+6log(1+r/4)−log(1+r),
F'(r)=9r(r−2)/[(r−8)(r+1)(r+4)].

Thus F(r)≥0 on−1<r≤1, with equality only at0. In particular F(1)≈.111588556827>0. This exact family check does not prove the general determinant target.

The pointwise functional is not convex: on this actual line F''(1)=−351/4900<0. A convexity lift from extreme matrices therefore cannot be assumed. Singular input/output endpoints need a separate supported or limiting interpretation; the searches use faithful interior approximations.

Reproducible scripts are relative_peak_two_logdet_real_diagnostic.py and relative_peak_two_logdet_complex_diagnostic.py. They write floating best-candidate arrays under /tmp and do not promote numerical evidence to a theorem.

## Stronger inverse-trace route, still unproved

Define R(A)=Tr(I+A)^(-1)−2Tr(I+NA)^(-1)+3d. Then

d/dr [2logdet(I+rNA)−logdet(I+rA)]=R(rA)/r.

Thus R≥0 on the same actual EO=0 norm ball would imply the pointwise determinant target by radial integration. This is a rational matrix inequality, not an independently-sampled-spectrum condition.

A second complex analytic-gradient scan, references3,4,6, radii.25,.75,.999999, five starts each, found no negative candidate. It again approached the positive isotropic pattern, whose limiting R at norm1 is9/70. Some optimizer starts approached high positive singular-boundary values rather than the small pattern; no global optimization certificate is claimed. Reproducible code: relative_peak_two_inverse_trace_diagnostic.py.

The physical channel has no strict operator-norm contraction on EO=0: A=(3F−I)/4 has ||A||=||NA||=1. Its three input-zero eigenvalues versus one output-zero eigenvalue explain the positive logdet divergence. Any proof requiring ||NA||≤c||A|| with c<1 on this subspace would be false.
