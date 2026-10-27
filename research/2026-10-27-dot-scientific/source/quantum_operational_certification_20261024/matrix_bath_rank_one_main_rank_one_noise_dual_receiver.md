# Rank-one main Gram and rank-one noise: exact dual one-column receiver

In the scalar-leg balanced matrix-bath family, suppose T and Q both have rank one. Up to their zero cases, write normalized bath vectors f,g and nonnegative coefficients d,h,q so that

 psi=sqrt(d)|k,f>+sqrt(h/2)(|i,r_i>+|j,r_j>),
 A=|psi><psi|+q|i,g><i,g|+q|j,g><j,g|,

where r_i,r_j are orthogonal to the bath and to one another. The bath vectors f,g may be nonorthogonal. This is a genuine nonaligned source family.

Purify A with environment flags 0,1,2:

 Psi=psi tensor|0>+sqrt(q)|i,g> tensor|1>+sqrt(q)|j,g> tensor|2>.

Tracing the original reference yields the sum of populations h/2 on |i,0> and |j,0>, and a correlated coefficient matrix on

 span{|k,0>, (|i,1>+|j,2>)/sqrt2}.

In this ordered basis its diagonal entries are d and 2q, and its offdiagonal is sqrt(2dq)<g,f>, with conjugation adjusted according to the chosen bra-ket convention. The Gram is positive because |<g,f>|<=1.

This is EXACTLY the source class proved in `wh3_one_column_rank_two_kernel_boundary_entropy_theorem.md`: a general correlated 2x2 Gram on a product vector and a matched coherent pair, plus two arbitrary populations in the product vector's reference column. Therefore the dual source has nonnegative Delta, and accepted WH3 purification duality proves Delta(A)>=0.

The conclusion allows every overlap between f and g and does not require a top-anchor sign. For higher-rank Q, purification creates a matrix-valued paired reference sector; the scalar-leg receiver above cannot be assumed to persist. The separate operator-valued shared-Gram theorem correctly preserves that larger sector.
