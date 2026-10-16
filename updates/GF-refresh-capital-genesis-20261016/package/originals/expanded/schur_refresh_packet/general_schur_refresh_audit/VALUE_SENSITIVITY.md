# Dimension-independent sensitivity of the sharp value

For two valid specified Schur correlation matrices C,C' on the same fine resolution, write c,B and c',B' for their blocks. At fixed p,q and h=sqrt(pq(1-p)(1-q)), the exact optimizer implies

|F_C-F_C'| <= 2h ||c-c'||_infinity + pq max_{j,k}|B_jk-B'_jk|.

Indeed every feasible z has ||z||_1<=1, so the linear objective difference is at most 2h||c-c'||_infinity and the quadratic difference is at most pq max|B-B'| (sum_j |z_j|)^2. The absolute difference between maxima cannot exceed the uniform absolute difference of their objectives.

This is a dimension-independent sensitivity bound for the already-specified mathematical channel value. It is not a diamond-norm channel qualification, does not certify persistent-environment privacy, and does not license inference of the full joint channel from reduced-state or Ramsey measurements. No additional experiment or physical implementation is claimed.
