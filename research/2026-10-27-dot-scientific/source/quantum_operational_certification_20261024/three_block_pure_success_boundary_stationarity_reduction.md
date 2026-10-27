# Exact exclusion of proper saturated-overlap faces

Consider the actual pure-success three-physical-block reset source of `three_block_pure_success_dual_star_interface.md`. Fix p in (0,1). Write d=p/3, x_i=q w_i, c_i=sqrt(d x_i r_i), with positive x_i and sum x=q.

Every negative global minimum, if one exists, must have all x_i>0 and all 0<r_i<1. This is a reduction, not a whole value theorem or a stationary exclusion for the interior.

## Paid boundary pieces

If x_i=0, the source is the received two-physical-block class. If r_i=0, the reset sector physical label i tensor v_i is orthogonal to the success support and all other physical reset labels. The source, reference, and WH output split along this reference sector. That isolated reset summand has zero homogeneous deficit. The remaining normalized TP source has at most two physical reset blocks and is received. Homogeneity therefore pays the original source. This argument also covers intersections of these boundaries.

If all three r_i=1, all logical reset vectors are the success vector up to phases, so the source is the received logical-rank-one arbitrary-qutrit mixed reset class (`arbitrary_qutrit_mixed_reset_value_theorem.md`).

## Proper saturated faces cannot minimize

Suppose exactly one or two overlaps equal one. Lower each saturated overlap from one to 1-t, fixing all other variables, with t>0. Use the exact dual input/reference/output blocks from the interface, with normalized output O_ij. Spectators are fixed.

For each saturated i the 2x2 input block T_i has one zero eigenvalue at t=0. It opens as

lambda_i(t)=h_i t+O(t^2), h_i=d x_i/(d+x_i)>0.

The reference arrowhead has Schur complement p(1-(r_1+r_2+r_3)/3)>0, and hence is strictly positive because not all overlaps are saturated. An output pair O_ij is singular precisely if both r_i=r_j=1, as its scalar-central Schur complement is d(1-(r_i+r_j)/2). Thus there is no singular output pair in the one-saturated case, and exactly one in the two-saturated case.

For a pair of saturated overlaps i,j, its unique zero eigenvector is proportional to

(1,-sqrt(3d/(2x_i)),-sqrt(3d/(2x_j))).

Reducing both overlaps to 1-t opens the zero eigenvalue as

lambda_ij(t)=h_ij t+O(t^2),
h_ij=d/[1+(3d/2)(1/x_i+1/x_j)].

Because f(lambda)=lambda log lambda, all other eigenvalues contribute O(t), so the actual deficit has the exact asymptotic form

Delta(t)=Delta(0)+C t log t+O(t),

where C=h_i in the one-saturated case and C=h_i+h_j-2h_ij in the two-saturated case. Both are strictly positive. Indeed

1/h_ij=1/d+(3/2)(1/x_i+1/x_j)
        >(1/2)(1/h_i+1/h_j),

so h_ij is smaller than the harmonic mean of h_i,h_j, which is at most their arithmetic mean. Since t log t<0, Delta(t)<Delta(0) for sufficiently small positive t. No point on a proper saturated-overlap face can therefore be a local minimum, whether its value is positive or negative.

## Consequence for the remaining research problem

The source parameter domain at fixed p is compact, and the deficit is continuous. If a negative value exists, a negative global minimum exists. The paid zero-weight/zero-overlap boundaries and the paid fully saturated corner cannot contain it. The calculation above excludes every other saturated-overlap boundary. Therefore a negative global minimum must be fully interior and satisfy all three overlap stationarity equations and both independent physical-weight stationarity equations. This does not establish that such stationary points are absent or nonnegative.

The all-three-saturated corner must not be included in the exclusion calculation: its reference also has a zero eigenvalue, producing an additional t log t term whose sign need not match the proper-face coefficient.
