# Fixed-column unbiased pruning: polynomial rational construction
2026-10-28. This closes the explicit bit-complexity obligation in CONSTRUCTION_v1 Section 4 at the finite rational-input level. Independent review pending.

Let F_1,...,F_m be fixed nonzero rational PSD effects summing to I_r, all with encoding length at most L. Never replace these columns during elimination. Maintain rational nonnegative weights w_i, initially 1, with sum_i w_i F_i=I. Vectorize the Hermitian matrices as r^2 real rational coordinates. At a stage with more than r^2 active weights, choose a nonzero INTEGER null vector v on the active columns. Standard exact Gaussian elimination and clearing denominators provide v with coefficient bit length polynomial in m,r,L, uniformly at every stage, because the columns are always subsets of the ORIGINAL fixed columns. One may choose a dependent subset of at most r^2+1 columns. Trace positivity implies v has both positive and negative entries.

The feasible interval for w+t v>=0 has
 t_+=min_{v_i<0} w_i/(-v_i)>0,
 t_-=-min_{v_i>0} w_i/v_i<0.
Choose t=t_+ with probability -t_-/(t_+-t_-), and otherwise t=t_-. Each branch eliminates at least one active weight, preserves positivity/completeness, and has E[w'_i|w]=w_i. At most m-1 stages suffice. The final effects w_i F_i form a POVM with at most r^2 nonzero outcomes; their expectation is the original POVM, including labelwise effects.

Bit complexity is controlled explicitly. Store all weights over one common positive denominator D: w_i=a_i/D. If an endpoint is reached at k, t=-a_k/(D v_k). The update is
 w'_i=(a_i v_k-a_k v_i)/(D v_k),
with signs adjusted to keep the denominator positive. Thus the common denominator bit length grows by at most log2|v_k| per step, NOT by the encoding length of every current weight. At most m steps give polynomial total denominator length. Also 0<=w_i Tr F_i<=r, so every surviving weight is bounded by r/min_i Tr F_i; the logarithm of this bound is polynomial in r,L. Numerator bit lengths are therefore polynomial as well. Gaussian elimination, endpoint comparisons and rational coin probabilities all have polynomial bit complexity in m,r,L.

Endpoint sampling probabilities are exact rationals of polynomial bit length. Draw an integer uniformly below its denominator using fixed-bit rejection, with an announced finite retry cap. Since acceptance is at least 1/2 per retry, for at most m stages a cap R yields total failure at most m 2^-R. On exhaustion implement any declared physical fallback; its contribution is at most that probability to complete operational discrepancy. The number of stages is bounded by m, so both total coin cost and runtime have deterministic polynomial caps. No exact irrational coin or infinite expected-time loop is needed.

This algorithm samples a compact realization but does NOT construct a polynomial-length list of all possible realizations. No such list is needed for a single terminal physical execution. The same principle is standard convex decomposition; its purpose here is to discharge the actual compressed-decoder implementation obligation, not claim a new convex-geometric theorem.
