# A componentwise entrance certificate survives later conditioning

New construction in this continuation. This file derives the relative
certificate computed by relative_gauss_entrance.py. The positive mixture being
certified is the already retained 24-site law: its exact rational weights,
local probabilities, and unnormalized mass were checked unchanged. This is an
upgrade of the usable evidence attached to that law, not a recovered historical
implementation or a newly refined mixture.

## 1. Source and retained-state contract

There are finitely many independent local blocks. Block i has a finite silent
CTMC generator Q_i, a strictly positive stationary probability row mu_i, and
nonnegative diagonal killing D_i after an autonomous controller opens once.
The controller's only transition is 0 -> 1 at rate gamma > 0. Selected reaction
hazards are disabled before opening; silent generators are unchanged by the
opening. Put A_i=Q_i-D_i. At exactly observed first-event time t>0, mark j has
a fixed nonnegative local hazard/reset operator J_j. Its reset is specified.

The retained state is the complete post-event Markov state required for later
operations: the leaf configuration and known post-event controller state.
It is not the unobserved opening time or the whole pre-event history. The
product-mixture labels below are representation indices, not an asserted
total-variation approximation of a continuous latent opening time. A later
operation that needs omitted historical state is outside this contract.

Write A for the Kronecker sum of the A_i and mu for their product row. The
true unnormalized marked entrance density is

    M = integral_0^t g(u) du,
    g(u) = gamma exp[-gamma(t-u)] mu exp(Au) J_j.

All factors except the controller scalar are products of local rows or the
fixed local marked reset. At every u, g(u) is a positive product measure.
The finite output coordinates that J_j never reaches are structural zeros.
All remaining output coordinates are strictly positive for every u in [0,t],
because every mu_i is strictly positive and exp(A_i u) has positive diagonal.
Thus support is independent of u. Numerical ratios will only be formed on
this common positive support; structural zeros must remain exactly zero.

The implementation specializes this source to binary blocks with positive
rates alpha_i, beta_i, kappa_i, stationary law
(beta_i,alpha_i)/(alpha_i+beta_i), killing diag(0,kappa_i), and resetting the
marked block to state 0. The theorem is finite-block algebra; the executable
numerical bridge is not claimed to cover recurrent controllers or arbitrary
multistate blocks.

## 2. Obtain relative derivative bounds from local matrices

For r=0,...,8, compute using local arithmetic

    b_i,r = max_x |(mu_i A_i^r)(x)| / mu_i(x).

The positive denominator is a substantive assumption. Since exp(A_i u) is
nonnegative and A_i commutes with its exponential,

    |(d^r/du^r) [mu_i exp(A_i u)]|
      = |mu_i A_i^r exp(A_i u)|
      <= |mu_i A_i^r| exp(A_i u)
      <= b_i,r mu_i exp(A_i u)

componentwise. The product derivative formula and the positivity of J_j now
give |g^(r)(u)| <= B_r g(u), where

    B_r = sum_{r0+r1+...+rn=r}
            r!/(r0!r1!...rn!) gamma^r0 product_i b_i,ri.

These are obtained by truncated multinomial convolution; no product-state
matrix is formed. For fixed derivative order the arithmetic uses local matrix
products and O(n r^2) scalar convolution operations. Rational inputs give
exact rational b_i,r and B_r. Local dimension and arithmetic bit costs remain
part of the work.

## 3. Control variation within a quadrature cell

Let d_i,min and d_i,max be the smallest and largest diagonal entries of D_i.
Stationarity gives

    v_i'(u) = mu_i A_i exp(A_i u) = -mu_i D_i exp(A_i u),
    -d_i,max v_i(u) <= v_i'(u) <= -d_i,min v_i(u).

Consequently, for Delta >= 0,

    exp(-d_i,max Delta) v_i(u)
      <= v_i(u+Delta)
      <= exp(-d_i,min Delta) v_i(u).

Multiplication by the other positive rows and J_j preserves these inequalities.
The scalar controller factor contributes exp(gamma Delta). A safe two-sided
componentwise log-Lipschitz constant is

    L = gamma + sum_i d_i,max.

Thus, on every common supported coordinate, the ratio of any two integrand
values within a cell of width h is at most exp(Lh). A smaller usable constant
is max(|gamma-sum_i d_i,min|,|gamma-sum_i d_i,max|); the implementation uses
the displayed safe L.

## 4. Relative positive Gauss certificate

Let G be composite four-point Gauss integration of g, with uniform cell width
h. Its nodes and weights are positive. The eighth-order Gauss Peano kernel is
nonnegative and has total mass C4 h^9 on a cell, with

    C4 = (4!)^4/[9(8!)^3] = 1/1778112000.

For every supported output coordinate x,

    | integral_cell g_x(u) du - G_cell,x |
       <= C4 h^9 sup_cell |g_x^(8)(u)|
       <= C4 h^9 B_8 sup_cell g_x(u)
       <= C4 h^8 B_8 exp(Lh) integral_cell g_x(u) du.

The last step bounds the supremum by exp(Lh) times the cell average. Summing
the nonnegative cell integrals yields the componentwise full-measure bound

    |M-G| <= delta M,
    delta = C4 h^8 B_8 exp(Lh).

This is a relative bound on the whole hidden-state entrance measure, including
rare coordinates. It is not a norm or marginal comparison. Require delta<1.

### Outward node evaluation

For each exact Gauss term, outward interval evaluation produces positive
product measures L_r and U_r with L_r <= G_r <= U_r. Suppose the coefficient
and each supported local entry have strictly positive lower endpoints. Then

    c_r = (upper coefficient/lower coefficient)
          product_i max_supported_x (upper local entry/lower local entry)

gives U_r <= c_r L_r componentwise. Set c_round=max_r c_r, using outward
arithmetic for every ratio and product, and Lhat=sum_r L_r. It follows that

    Lhat <= G <= sum_r U_r <= c_round Lhat.

An upper/lower pair (0,0) is a structural zero, not a ratio. A positive upper
endpoint with a zero lower endpoint is rejected as insufficient numerical
precision; it cannot silently receive a finite relative certificate.

Combining the two bounds gives the final unnormalized sandwich

    a Lhat <= M <= b Lhat,
    a = 1/(1+delta),    b = c_round/(1-delta).

The spread R=b/a is invariant under rescaling either measure. The exact
decimal lower factors are rational, so normalization produces a completely
specified rational product mixture. The actual-law file retains its exact
weights, local probabilities and unnormalized mass, as well as rational a,b,R.

## 5. Why later rare conditioning does not enlarge this certificate

Let T be any common positive linear operation on the retained state: a
specified transition kernel, survival propagation, mark likelihood, reset,
likelihood-weighted observation, or a composition of these. Finite positive
linear combinations and integrations are also allowed. Then

    a (Lhat T) <= M T <= b (Lhat T).

When the output has finite nonzero total mass, both sides can be normalized.
The sharp bound that follows from such a sandwich is

    TV( M T / (M T 1), Lhat T / (Lhat T 1) )
       <= (sqrt(R)-1)/(sqrt(R)+1),    R=b/a.

For completeness, write the density ratio relative to the normalized lower
measure as Z/E[Z], where a<=Z<=b. Convexity bounds its expected absolute
deviation by that of the endpoint-valued distribution with the same mean m.
The resulting TV is at most (b-m)(m-a)/(m(b-a)); its maximum over m in [a,b]
is attained at m=sqrt(ab), giving the displayed expression. The case a=b is
equality of the normalized laws.

No probability of the later record appears in this bound. The sandwich
guarantees matching zero/nonzero record support, and an arbitrarily small
positive record likelihood does not amplify the projective spread. A long
record is one composed positive operation, so the source spread is not paid
again at every observation. New numerical approximation during subsequent
execution has its own error and must be certified separately. The statement
does not compare different physical models or condition on information not
contained in the retained state.

## 6. A class-wide obtaining bound without high derivatives

The same log-Lipschitz argument gives a simpler existence and obtaining result.
Let Q be the positive composite midpoint sum, with maximum cell width h. On
each cell every integrand value is within exp(+-Lh/2) of its midpoint value.
Integration and summation therefore give

    exp(-Lh/2) Q <= M <= exp(Lh/2) Q.

Ignoring a separately bounded numerical node spread, R<=exp(Lh), and the
posterior TV under every later common positive operation is at most

    tanh(Lh/4).

For epsilon in (0,1), a uniform midpoint mixture with

    N >= L t / [4 atanh(epsilon)]

positive product terms therefore suffices. This bound has no event-density
denominator and no silent-switching-rate factor. Total killing and exposure
time remain; when local killing is uniformly bounded, the rank bound scales
linearly with the number of blocks and inversely with small epsilon. Local
matrix evaluation, support and bit-precision costs are not removed. Certified
relative evaluation of positive local factors may need higher precision for
small probabilities. The much faster eighth-order Gauss certificate is the
implemented acquisition; the midpoint construction supplies a wider explicit
obtaining guarantee, not a claimed competitive numerical choice at 1e-9.

## 7. Available numerical evidence

The saved 24-site source has gamma=7/10, t=3/2, mark 0, and for i=0,...,23,

    alpha_i=3/5+i/100,
    beta_i=2/5+(i mod 5)/50,
    kappa_i=3/2+(i mod 3)/10.

The already retained 64-cell, 256-term Gauss law is unchanged. Exact rational
comparison checked every normalized weight, every local probability, and its
unnormalized mass. The new certificate is

    delta <= 9.2732841603278692463527383085506040667e-10,
    c_round <= 1 + 2.67e-42,
    all-later-operation posterior TV <= 4.6366420801639346242e-10.

The supported outputs have firing site 0 in state 0; all other sites admit
both states. The 2^25 controller/leaf state space was not enumerated.

An independent three-leaf check formed its 16-state killed generator using
exact rational arithmetic and propagated it by a 74-term uniformization
series. The omitted Poisson mass is at most 2.969e-33. Every one of the four
positive post-reset coordinate enclosures lies strictly inside its relative
sandwich; the other four reset-support zeros are exactly zero. This reference
also uses an outward enclosure of the scalar exponential. It is a separate
coordinatewise check, not the source of the compiler's certificate.

Artifacts:

* relative_gauss_entrance.py — source-computable relative bounds and check.
* relative_correlated_entrance_24sites.json — actual retained probability law
  with exact rational projective sandwich and explicit retained-state scope.
* relative_gauss_entrance_results.json — numerical certificate and independent
  small expanded coordinate check.

Positive conditional factorization and positive-operator filtering have
incumbents. In particular, Celikkaya and Shelton's TTOP paper, page 5, already
describes a positive expansion with substochastic A and nonnegative B:
https://proceedings.mlr.press/v32/celikkaya14.pdf . Positivity alone is not the
distinction. The sharp TV/Hilbert-distance inequality appears in Cohen and
Fausti, Theorem 5.1 and Corollary 5.2.1,
https://arxiv.org/html/2309.02413v2 . Hilbert-metric filtering stability and
uniform approximation are treated by Le Gland and Oudjane, Annals of Applied
Probability 14(1), 144-187 (2004), DOI 10.1214/aoap/1075828050,
https://projecteuclid.org/journals/annals-of-applied-probability/volume-14/issue-1/Stability-and-uniform-approximation-of-nonlinear-filters-using-the-Hilbert/10.1214/aoap/1075828050.full .
No historical priority is asserted for the projective inequality.
The constructive object here is the source-obtained relative entrance
certificate, its explicit support and obtaining conditions, and the retained
law to which it applies.
