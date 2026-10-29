# Conditional continuous law and literal quantized output

PROOF gives an exact conductance draw. Its conditional field distribution is a
normalized Gaussian and must be paid, not treated as the already executed output.
The sibling quantized_field.py implements this completion using outward Arb.

For the rational positive-definite covariance C=L_x^(-1), an exact rational LDL
factorization gives C=T D T^T, with T unit lower triangular and D strictly positive.
Fresh independent Box--Muller pairs

    Z_1=sqrt(-2 log U) cos(2 pi V),
    Z_2=sqrt(-2 log U) sin(2 pi V)

give the required independent real normals. Each field component is T sqrt(D) Z.
The output is the componentwise floor on a SUPPLIED positive rational grid width.
It is the normalized full field law pushed through this quantizer, with the pinned
site omitted. It is not an exact finite string representing a continuous real.

Every U,V is a persistent lazy fair-bit interval. Increase its precision and use
outward elementary functions and arithmetic until every floor is unique. No
floating midpoint, accepted tolerance, Gaussian cutoff, or resampling of ambiguous
fields governs the result. The executable pseudorandom source is diagnostic only;
the probabilistic theorem assumes iid fair bits and correct outward operations.

For a fixed finite input, termination and finite expected requested precision can
be justified without assuming independent adaptive precisions. At depth p, exclude
U outside [2^(-p/3),1-2^(-p/3)] for ALL radial uniforms. This event has probability
O(nr 2^(-p/3)). On the complement the Box--Muller map has a deterministic derivative
bound growing at most O(poly(p) 2^(p/2)); input intervals of width 2^-p therefore
give exponentially shrinking field intervals, after charging the finite LDL norm.
Working precision can be enlarged to pay elementary rounding as well.

For each nonzero-variance marginal Gaussian X and fixed grid width delta, the
wrapped density sum sum_k f_X(k delta) is finite (and bounded, for example, by
1/delta+2 sup f_X). Therefore the probability that an output coordinate lies within
w of ANY grid boundary is at most O(w(1/delta+sup f_X)), with a harmless enlargement
of the constant for w<delta/4. Union over finitely many coordinates proves an
exponentially decaying unresolved-depth tail. This argument is unconditional over
U,V and holds separately for every conductance state. There are finitely many such
states, so uniform finite constants exist; no independence between the requested
precision and the random output is presumed.

Thus the ideal elementary-interval algorithm has finite mean requested random bits
and finite mean elementary evaluation precision. Rational graph/determinant bounds
control the finite LDL coefficient sizes. This does NOT certify a general expected
CPU bit-complexity theorem for the installed python-flint/Arb implementation or
claim that dense LDL is the fastest Gaussian sampler. All field precision and
factorization operations are included in the actual execution receipt.
