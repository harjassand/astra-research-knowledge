# A genuinely cheaper alternative when the infinity-norm leaks are affordable

This is a separate elementary alternative, not an assertion that L2 stochastic
operators contract. Let A and P be stochastic, P²=P, Q=I−P, and let
e_out ≥ ||PAQ||∞. For q in range(Q),

    ||QAq||∞ ≤ ||Aq||∞ + ||PAq||∞ ≤ (1+e_out)||q||∞.

Thus the positive-projection theorem needs no independently acquired complement
norm if we choose α=1+e_out. With e_in ≥ ||QAP||∞ and task-compatible endpoints,
the usual two-sided scalar error is bounded by

    ||ell||1 ||b||∞ e_in e_out sum_{k=0}^{L−1} sum_{j=0}^{k−1}(1+e_out)^j
    ≤ ||ell||1 ||b||∞ e_in e_out L(L−1) exp(L e_out)/2.

The sharper capped recurrence in POSITIVE_PROJECTION_ROUTE.md also applies.
The shortcut pays a horizon-squared, rather than a mixing-gap-dependent,
factor. It can be better than acquiring a spectral norm, particularly for
moderate horizons. It does NOT automatically bound the mixed L2 discarded
channel: a row-stochastic matrix can have arbitrarily large L2 norm.
Both routes must pay their actual leakage observations and certificates.
An L2 return-row upper bound sqrt(n)||WAQ row||2 also upper bounds its L1
norm, but the incoming *average* Frobenius bound does not certify worst-row
incoming infinity norm.

## First-action boundary for a microscopic initial distribution

For physical chronological controls a_1,...,a_L, the requested scalar is
μ A_{a_1}...A_{a_L} b. Do not force μ=μP when it is false. For every first
action a learn the finite row k_a=μ A_a Z and a return residual
η_a ≥ ||μ A_a Q||1. Then

    μ A_a x = k_a W x + μ A_a Q x.

For x=A_{a_2}...A_{a_L}b and b=Pb, if the discarded recurrence gives
||Qx||∞ ≤ ||b||∞ t_{L−1}, the boundary residual is at most
η_a ||b||∞ t_{L−1}. An estimated stochastic row k_hat_a adds
||k_a−k_hat_a||1 ||b||∞, and the remaining coarse-model error is multiplied
by ||k_hat_a||1=1. All m boundary rows and their fresh residual validations
must be paid. An arbitrary μ may still produce an order-one return residual;
the lemma is not a promise of cheap microscopic initial states. The empty
word and length-one word have separate direct task values/boundary formulas.

This allows a finite boundary interface rather than a singleton block when
the actual first transition spreads the source sufficiently. It is a paper
construction here; the large executable below uses a uniform learned-block
initial distribution. No claim of historical novelty is made for these
projection identities.
