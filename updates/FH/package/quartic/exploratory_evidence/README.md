# Floating-point search evidence; not part of the proof

The stored run used an actual compatible Fourier gradient, cutoff 3, a 13x13 dealiased periodic grid, eight restarts and 800 Adam updates. Fourth gradient moment was normalized to one. The affine background was eliminated using the quartic expansion, with a 10^-12 identity regularizer in the numerical linear solve. The final field and background were reevaluated directly. The smallest directly evaluated gap was 0.018879241611086624. No negative gap was obtained.

The NPZ stores numerical `p`, `coef`, `background`, `k`, `grid`, and `gap`. The nine entries of `p` multiply `u^2,v^2,uv,w^2,uw,vw,qu,qv,qw` in that order. None of this is an exact rank-one certificate for the exploratory candidate or a lower bound over compatible fields.

Additional exploratory methods included arbitrary cubic heat corrections, variable real input metrics, output-rotating diffusion, pointwise polyconvex supports, and sums of a support-certified polyconvex part and a corrected-heat part. No universal cone inclusion was proved. Output-rotating diffusion did not demonstrate an advantage over real variable metrics in the retained successful comparisons. Residuals from unfinished numerical feasibility iterations were not treated as separations or counterexamples.
