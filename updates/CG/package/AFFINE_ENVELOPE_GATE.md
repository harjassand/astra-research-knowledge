# Native envelope gate: affine stratification can require exponential size

This is an obstruction to one proposed acquisition mechanism, not to the dual-kernel law and not to all compact representations. In fact its test family has an exact product sampler. That multiplicative escape is essential to interpreting the result.

## 1. Test family and exact mass

Over `F_2`, take

    A_lambda=diag(lambda_1,...,lambda_m).

Then `rank A_lambda=wt(lambda)`, and the dual weight is

    f(lambda)=2^(-wt(lambda)),      Z=sum_lambda f(lambda)=(3/2)^m.

The normalized target is just a product of independent bits with probability `1/3` of being one. The matrices are given natively, no hidden minimum-rank oracle is involved, and low-rank witnesses are easy to find.

## 2. Uniform-rank affine pieces

Suppose a proposal is formed from `K` affine subspaces `L_j` that cover the whole coefficient space. On `L_j`, use one valid uniform rank lower bound `R_j<=min_(lambda in L_j) wt(lambda)`. The envelope contribution is `1_(L_j) 2^(-R_j)`; overlapping pieces are allowed and their positive masses add.

If `d_j=dim L_j`, then

    min_(lambda in L_j) wt(lambda) <= m-d_j.              (1)

Proof: choose an information set of `d_j` coordinates on which the affine subspace projects bijectively. Some element is zero on those coordinates and has weight at most `m-d_j`.

Consequently its proposal mass is at least `2^(2d_j-m)`. Since the pieces cover all `2^m` vectors, `sum_j 2^d_j>=2^m`. Cauchy-Schwarz gives

    C >= 2^(-m) sum_j 2^(2d_j) >= 2^m/K,
    C/Z >= (4/3)^m/K.                                   (2)

Thus polynomial rejection overhead needs exponentially many such affine pieces. The result holds for arbitrary affine spaces, not just coordinate subcubes or the particular refinement order of a low-rank witness algorithm.

The same proof allows fractional covering coefficients `a_j in [0,1]` with `sum_j a_j 1_(L_j)>=1`, replacing Cauchy-Schwarz by its weighted version. Coefficients above one can be reduced to one without harming this covering condition. It does **not** assert that every conceivable scalar mixture must satisfy the per-piece rank-bound covering construction. The next result addresses arbitrary positive affine mixtures separately.

For `F_q`, the same argument gives

    Z=(2-1/q)^m,
    C/Z >= [q^2/(2q-1)]^m/K.

## 3. Stronger gate: arbitrary positive mixtures of uniform affine laws

Let `pi(lambda)=f(lambda)/Z`, the Bernoulli-`1/3` product law. Suppose `Q` is *any* mixture of uniform distributions on at most `K` affine subspaces of `F_2^m`, with arbitrary nonnegative mixture probabilities. Suppose it dominates the target sufficiently for rejection sampling:

    pi(lambda) <= rho Q(lambda)   for every lambda.

The overhead `rho` is bounded below without assuming any particular per-piece rank certificate.

Fix integers `D,t`, with `0<=D<m`. Two facts hold.

- An affine space of dimension at most `D` has target probability at most `(2/3)^(m-D)`. Use an information set and condition on its coordinates; each remaining dependent bit has conditional probability at most `2/3` under the product law.
- On an affine space of dimension greater than `D`, the information-set coordinates are independent unbiased bits under its uniform law. Thus the chance its total weight is at most `t` is at most `Pr[Binomial(D+1,1/2)<=t]`.

Remove the union of the low-dimensional mixture components from the set `T={wt<=t}`. The remaining set has target mass at least

    Pr[Binomial(m,1/3)<=t] - K (2/3)^(m-D),

but proposal mass at most `Pr[Binomial(D+1,1/2)<=t]`. Therefore

    rho >= [Pr(Binomial(m,1/3)<=t)-K(2/3)^(m-D)]
            / Pr(Binomial(D+1,1/2)<=t),                 (3)

whenever the numerator is positive.

For an explicit asymptotic form, take `D` near `7m/8` and `t` near `3m/8`. Standard binomial tail bounds imply exponentially growing `rho` when `K` is polynomial in `m`. For multiples of 8, one convenient, slightly weakened bound is

    rho >= [1-exp(-m/288)-K(2/3)^(m/8)] exp(m/112).

Rounding can be handled directly by the exact finite formula (3). Hence even an arbitrary polynomial-size positive mixture of uniform affine laws is insufficient for polynomial-overhead domination of this elementary product target.

## 4. Exact checks and scale

`check_affine_envelopes.py` verifies (1) for *every* affine subspace of `F_2^m` for `m=1,...,6`, including all 26,387 affine subspaces for `m=6`. It verifies coordinate-partition envelope formulas with exact fractions.

The exact rational formula (3), evaluated without simulation, yields these example lower bounds (rounded only for display):

- `m=100`, `K=100`: overhead at least 14.589
- `m=250`, `K=62,500`: overhead at least 1,778.57
- `m=500`, `K=250,000`: overhead at least 1,170,693,280

All exact fractions and optimizing integer parameters are stored in `AFFINE_ENVELOPE_RESULTS.json`.

## 5. Multiplicative escape and its next closure test

This family is **not hard to sample**. Its weight factors as `product_i 2^(-lambda_i)`, and independently drawing each bit with bias `1/3` is exact. The conclusion is solely that additive affine-piece proposals are the wrong compact operation even for this easy family. More low-rank witnesses and more affine branching do not cure that representational mismatch efficiently.

An obvious repair is to retain multiplicative rank contributions. But it needs its own acquisition/composition theorem. Already

    A_lambda=diag(lambda_1,lambda_2,lambda_1+lambda_2)

has exact dual law `(4/7,1/7,1/7,1/7)` on `(00,01,10,11)`, whereas the independent-bit rule gives `(4/9,2/9,2/9,1/9)`. The third factor couples the two coordinates. More generally `diag(B lambda)` gives a weighted linear-code model. This identifies the next problem rather than solves it.

No inference of general counting hardness is made from this tiny example, and no novelty is claimed for code weight models, matroid partition functions, or product sampling. A new representation would need a natively certified method to sample the coupled positive factors without reinstating an exponential contraction problem.
