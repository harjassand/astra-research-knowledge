# A computable certificate interface for the actual kinetic evaluator

Status: mathematical interface only. No actual eight-site approximate trajectory, small residual, useful probability interval, or speedup has been obtained here. This combines established Markov-semigroup stability, weighted Cauchy–Schwarz, and tensor contraction. No novelty claim.

## Exact target contract

Use the acquired 2-by-4 Schlögl generator, initial counts all50, time horizon1. Retain counts0 through162. Collapse FIRST entry into the all-counts-at-most15 set into a success sink; collapse FIRST count163 into a failure sink. Both sinks are absorbing. Let A be the forward generator on the continuation states and these two sinks. It has nonnegative off-diagonals and zero column sums. Its semigroup is an l1 contraction, including on signed vectors.

The true uncapped success probability differs from this capped success probability by at most the separately proved overflow probability. Add that budget only once.

For any differentiable, possibly signed approximate trajectory q(t), define r(t)=q'(t)-Aq(t). Variation of constants gives

    ||q(T)-p(T)||_1 <= ||q(0)-p(0)||_1 + integral_0^T ||r(t)||_1 dt.

Every success-sink coordinate error is bounded by the right side. If q is normalized and its initial error and residual have zero total mass, one can exploit the sharper total-variation factor1/2; this is OPTIONAL and must be established rather than assumed.

## Product weights remove an explicit state-count prefactor

Choose ANY strictly positive normalized mass mu on this finite space. It need not be stationary or approximately stationary. Weighted Cauchy–Schwarz gives

    ||r||_1 <= sqrt(sum_x r(x)^2 / mu(x)).

On the grid, choose mu(n)=a product_i mu_i(n_i), with normalized positive one-site masses and a>0. Assign positive masses to the two scalar sinks with total1-a. Unused target-grid coordinates can have residual zero; their positive weight merely wastes part of the bound, not validity. A bound derived on this enlarged indexing set is valid on continuation states.

For a tensor-train residual, its weighted squared norm is a double-layer contraction. This does not require enumerating163^8 states. This observation does NOT guarantee that the contraction or resulting bound is small: tensor ranks, dynamic range, cancellation, weight mismatch and arithmetic precision are charged. In particular, a product mass badly matching a correlated residual can yield an enormous bound even though no explicit square-root-of-state-count factor is written.

No approximate residual compression may be silently treated as exact. Either form the residual tensor exactly from the supplied trajectory and operator, or charge a separately certified compression error. One may contract all pairwise cross terms of an uncompressed sum of operator-action tensors instead of fusing them into an expensive large-rank tensor.

## Time coverage without sampling between times

On a segment of length h, keep mu fixed and use a supplied polynomial trajectory. The residual is then polynomial because A is time independent. Cauchy–Schwarz in time gives

    integral_segment ||r(t)||_1 dt
       <= sqrt(h * integral_segment sum_x r(t,x)^2/mu(x) dt).

The inner integral is an integral of a polynomial. It can be evaluated exactly for rational coefficients and rational weights, or with outward-rounded bounds. Sampling residuals at a few times is NOT a replacement. A polynomial q can be represented as a finite sum of tensor trains; all temporal cross terms must be included.

Sum these segment bounds. If segment trajectories jump at a joining time, also charge the l1 norm of every jump. An acquired TDVP endpoint sequence alone does not supply a certified continuous trajectory: interpolation and all its residuals must be charged.

## Choosing weights is a finite convex problem, but not a free shortcut

For a fixed residual (or its time-integrated squared coefficients), put nonnegative coefficients c(n). Minimizing sum_n c(n)/product_i mu_i(n_i) over positive normalized one-site masses is convex jointly in their positive entries: each reciprocal-product term has positive-semidefinite Hessian. Strict lower bounds on weights can enforce full support and finite conditioning.

With other factors fixed, define C_i(k)=sum_{n:n_i=k} c(n)/product_{j!=i}mu_j(n_j). Without lower-bound constraints, a nonzero block has optimum mu_i(k) proportional to sqrt(C_i(k)); zero entries require a positive-support safeguard. Marginals C_i can be contracted from the same tensor representation. These formulas are only a possible weight-selection mechanism. An optimizer's output is not needed for soundness: any explicit admissible weights give a valid bound.

## Decisive next evidence

Acquire or construct a matched forward trajectory for the actual eight-site first-hit generator, then evaluate the COMPLETE time-integrated weighted residual and initial/jump errors, with rigorous arithmetic. A useful error budget must be small compared with the source-reported probability scale (~3.8e-8), and the independent overflow budget (~7.57e-10) remains included. Until that execution exists this is an exact certification interface, not a solved rare-event benchmark or a new computational capability.
