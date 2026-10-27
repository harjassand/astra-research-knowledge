# Value-only affine cloud reuse at the statistical precision scale

27 October 2026. This is an explicit high-dimensional benchmark for the new reuse interface. It uses an unknown affine conservative field and an unknown noisy center. It is not a solution for nonlinear sources and does not claim historical novelty over ordinary matrix-polynomial Gaussian simulation.

## 1. Inputs and goal

An available cloud is X=theta+tau Z, Z standard Gaussian in R^d. The vector theta is not supplied. An oracle returns g(v)=A v+c for a fixed unknown symmetric matrix A, with ||A||op<=L. A, c, and derivatives are not supplied; only values are available. Take S>tau L and q=tau L/S<1.

We construct a new retained cloud, independent of a child Gaussian observation, at the substantially smaller statistical precision cost:

    X_new ~ N(theta, (tau^(-2)I-S^(-2)A^2)^(-1)),
    Y     ~ N(A theta+c, S^2 I).

Their joint law is the target. This charges covariance inflation of the retained center. For the original Gaussian-mean problem at center zero, affine g is trivial because g(0) gives its mean. That fact does not implement the present unknown-center channel: theta is only observed through X.

## 2. Exact analytical channel

Let W be fresh standard Gaussian, independent of X. Set

    B=(S^2 I-tau^2 A^2)^(1/2),
    Y=g(X)+B W,
    X_new=X-tau^2 A B^(-1) W.

Both means are correct. Since A and B commute, their cross covariance is tau^2 A-tau^2 A B^(-1) B=0. Their joint law is Gaussian, so they are independent. The retained covariance is

    tau^2 I+tau^4 A^2 B^(-2)
      =(tau^(-2)I-S^(-2)A^2)^(-1).

No exact matrix or matrix-square-root oracle will be used at runtime. The next section constructs the actions from values.

## 3. Finite acquired implementation

Query c=g(0) once. Any action Uv for U=A/L is then obtained with one value as (g(v)-c)/L. Query g(X) once. Draw W and generate U^j W for j=0,...,2n+1 by sequential value actions. Maintain two accumulators, using the shared sequence:

    p_n(U)=sum_{k=0}^n binom(1/2,k)(-q^2)^k U^(2k),
    b_n(U)=sum_{k=0}^n [binom(2k,k)/4^k] q^(2k) U^(2k).

Return

    Y_n=g(X)+S p_n(U)W,
    X_n=X-(tau^2 L/S) U b_n(U)W.

Exactly 2n+3 oracle values are used on every execution: one at zero, one at X, and 2n+1 actions. This also counts repeated zero inputs if a power vanishes; no data-dependent stopping is needed. Arithmetic is O(nd), working storage O(d), and scalar coefficients are formed by elementary recurrences. There is no source fitting or matrix reconstruction.

The source offset cancels exactly in every matrix action. Gaussian seeds and exact returned reals have the model's ideal-real convention. A finite-bit implementation would need its own commonly rounded-target primitive-error budget.

## 4. Full joint-law bound

For 0<epsilon<=1/2, choose n>=0 so that

    q^(2n+2)/(1-q^2) <= epsilon/(3 sqrt(d)).            (1)

Then

    TV(Law(X_n,Y_n), Law(X_new,Y)) <= epsilon.          (2)

This is a joint Gaussian law certificate, not a moment test.

Proof. In an eigenvector of A let lambda=tau a/S, so |lambda|<=q. Normalize the retained coordinate by tau and the child coordinate by S. The exact and finite linear transformations of the two independent standard Gaussian coordinates (Z,W) are

    N_*=[[1,-lambda/sqrt(1-lambda^2)],
         [lambda,sqrt(1-lambda^2)]],

    N_n=[[1,-lambda b_n(lambda^2)],
         [lambda,p_n(lambda^2)]].

Here b_n(z)=sum_{k=0}^n binom(2k,k)z^k/4^k and p_n(z) is the corresponding square-root truncation. The coefficient magnitudes of both series are at most one. Writing h=q^(2n+2)/(1-q^2), each scalar truncation error is at most h. Also N_* N_*^T=diag((1-lambda^2)^(-1),1), so the norm of N_*^(-1) is at most one.

After whitening the exact Gaussian covariance, the perturbation E of the linear transformation satisfies ||E||op<=sqrt(2)h and ||E||F<=sqrt(2d)h. The orientation of the whitening product does not matter for these singular-value bounds. Condition (1) implies ||E||op<=sqrt(2)/6<1/4.

The relative covariance is I+D=(I+E)(I+E)^T up to an orthogonal change of basis. Thus ||D||op<=2||E||op+||E||op^2<=9/16 and ||D||F<=9||E||F/4. For |x|<=9/16,

    x-log(1+x) <= x^2/[2(1-9/16)].

The Gaussian KL formula gives KL<=81||E||F^2/28 < 6d h^2. Pinsker yields TV<=sqrt(3d)h<=3sqrt(d)h, proving (2). The loose constant 3 leaves a margin.

An explicit deterministic order is

    n=max(0, ceil(log(3sqrt(d)/((1-q^2)epsilon))/(-2log q))-1).

At fixed q<1, the query count is O(log d+log(1/epsilon)). No unknown center, mean, derivative, or conditional-law operation is assumed.

## 5. What this demonstrates and what it leaves open

This constructs the statistical-cost cloud update for the only mean families admitting an exact fixed-noise Gaussian channel. It shows that the much larger physical seed-gauge precision cost is not intrinsic in the affine case. Ordinary matrix-polynomial Gaussian simulation is the strongest equally informed competitor and can reproduce this construction; no algorithmic superiority is claimed.

For a nonlinear conservative source, replacing A by a random unbiased action or a local secant is invalid: the output need not be jointly Gaussian, and nonlinear center response reintroduces the Fourier obstruction. Extending this channel requires a proved full-law remainder, acquired nonlinear source operations, and a retained actual-law representation. An assumed local affine approximation or Hessian oracle does not supply those ingredients.

The companion script hides A and theta from the runtime function, counts all value calls, and evaluates the exact joint Gaussian KL from the known test matrix only in a separate verifier. Floating execution is a consistency check; equations (1)-(2) are the law proof. No raw affine matrix is passed to the runtime.
