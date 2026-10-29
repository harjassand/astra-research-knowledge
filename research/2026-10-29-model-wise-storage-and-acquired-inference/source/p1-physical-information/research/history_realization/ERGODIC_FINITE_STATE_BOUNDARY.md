# A bounded-clock ergodic process requiring infinitely many exact hidden states

29 October 2026. Auxiliary construction from the history-realization attack. This is a scope example, not the main advance and not a claim of historical novelty.

The retrieved Astra T13 source already gives a nonergodic countable mixture of binary reversible chains which passes every reflected CP test and has no finite reversible realization. The construction below removes the conserved mixture label and strengthens the exclusion to every finite hidden CTMC. It still has an explicit countable reversible realization, so it does not refute the infinite-state converse. Astra N507 supplies that stronger, different obstruction.

## Construction

The state space consists of the finite subsets S of the positive integers. For each n:

- If n is absent, add n at rate alpha_n = 4^{-n}.
- If n is present, remove n at rate beta_n = 2^{-n}.

The escape rate from every S is at most sum_n beta_n = 1, because alpha_n <= beta_n. Uniformization therefore constructs a nonexplosive countable-state CTMC with one common finite clock ceiling.

Set r_n = alpha_n/beta_n = 2^{-n} and

    Z = product_{n>=1}(1+r_n),   pi(S) = Z^{-1} product_{n in S} r_n.

The product Z is finite, since log Z <= sum r_n = 1. The sum over finite subsets equals that product. Equivalently pi is the law of independent Bernoulli coordinates with occupation probabilities r_n/(1+r_n); the sum of these probabilities is finite, so only finitely many coordinates are occupied almost surely.

For every n not in S,

    pi(S) alpha_n = pi(S union {n}) beta_n.

Thus pi is stationary and reversible. Every finite subset is reachable from every other by finitely many positive-rate changes. The chain is irreducible and positive recurrent, and its stationary process is ergodic.

Observe only

    Y_t = 1_{S_t is empty}.

This is a deterministic binary state observation. The observation is càdlàg and has no more jumps than the hidden uniformized process. Every finite reflected-half-history probability matrix is classically CP by conditioning on the hidden state at the cut. The countable Gram sum lies in the finite-dimensional CP cone because that cone is closed.

## Exact observable covariance

Write a = pi(empty) = Z^{-1} and lambda_n = alpha_n+beta_n. A single coordinate started absent is absent at time t with probability

    (1+r_n exp(-lambda_n t))/(1+r_n).

Coordinate independence therefore gives

    Pr(Y_0=1,Y_t=1) = a^2 product_n(1+r_n exp(-lambda_n t)).

After expanding the absolutely convergent product,

    c(t) = Cov(Y_0,Y_t)
         = a^2 sum_{empty != F finite}
             (product_{n in F} r_n) exp[-t sum_{n in F} lambda_n].

All coefficients are positive, and their sum is a-a^2. Dominated convergence gives c(t) -> 0.

But the singleton terms have distinct rates lambda_n = 2^{-n}+4^{-n} decreasing to zero. For every kappa>0, select n with lambda_n<kappa. Then

    exp(kappa t)c(t)
    >= a^2 r_n exp[(kappa-lambda_n)t] -> infinity.

The covariance tends to zero more slowly than every exponential bound.

Any stationary finite-state CTMC observation has a covariance given by finitely many matrix-exponential modes, with polynomial factors allowed when its generator is not diagonalizable. Its zero eigenvalue is semisimple, and every other contributing mode has strictly negative real part. If its covariance tends to zero, the constant term vanishes; the remaining finite sum is bounded by C exp(-epsilon t) for some C,epsilon>0. It cannot equal c(t).

Thus no stationary finite hidden CTMC, reversible or otherwise, produces this exact binary law.

## Finite-horizon approximation remains easy in principle

Retain only coordinates 1,...,K. This is a reversible 2^K-state CTMC with the same clock ceiling one. Start it in the product stationary law and couple its first K coordinates to the full process.

The two observed paths agree on [0,T] whenever the omitted coordinates start absent and none is born during that interval. Hence their path-law total variation is at most

    sum_{n>K} r_n + T sum_{n>K} alpha_n
    = 2^{-K} + (T/3)4^{-K}.

Exact infinite-state necessity therefore coexists with finite reversible approximation at every finite accuracy and horizon. A clock ceiling does not bound exact hidden dimension. This example is fully consistent with the metric-tree closure construction.

No data acquisition, mixing-independent sampling guarantee, or favorable comparison against a structure-informed analytic evaluation is claimed. The formulas already specify the structure that makes the approximation available.
