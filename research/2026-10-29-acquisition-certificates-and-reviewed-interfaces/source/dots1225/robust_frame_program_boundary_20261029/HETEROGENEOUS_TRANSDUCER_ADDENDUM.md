# Heterogeneous history-conditioned program inputs

2026-10-29. Root additive extension, independent review pending. The identical-v law is not silently applied to time-biased capped outputs.

For independent inputs tau_(v1) and tau_(v2) sharing the same unknown c, the same exact coefficient matrices apply. Input-swap symmetry of T implies the two cross terms have the same one-output partial trace, each C1/2. Consequently
 p(v1,v2)=[405v1v2-360(v1+v2)+512]/864,
 w(v1,v2)=3[31(v1+v2)-9v1v2]/[405v1v2-360(v1+v2)+512].
For0<=v1,v2<=8/9, success is nonincreasing in either error and remains>=2/9. Retained-program error is increasing in either variable: up to the positive3/denominator² factor, derivative with respect tov1 is
 15872-4608v2-9315v2²,
which is decreasing on[0,8/9] and has endpoint value4416>0. Thus v1,v2<=v_U implies p>=p(v_U),w<=w(v_U), with the identical-input formulas on the right.

A complete classical batch transcript can change each actual vi. Conditional independence given complete separate transcripts, a common fixed unknown frame and the memoryless source is enough. Conditioning only on a shared/coarsened success schedule need not yield product states; instead apply the bound on each full-transcript component and use convexity. Within a quartet the retained single program remains the safe interface. Common frame c is a fixed parameter, not an averaged unknown random variable entangling batches.

This extension combines with the independently received history-uniform growth/purification envelope without assuming that timeout acceptance preserves the uncapped average vi. It does not assert independence for a general retained-memory source.
