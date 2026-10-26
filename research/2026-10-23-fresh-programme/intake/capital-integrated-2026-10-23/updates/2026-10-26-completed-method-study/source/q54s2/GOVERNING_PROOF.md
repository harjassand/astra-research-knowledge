# Stage 2 governing proof and adversarial stress

Stage1 is unchanged. All measurements below are mathematical noisy-query models. No hardware measurement or new instrument is asserted.

## A. Sequential stopping: a stronger ordinary incumbent

Let the two stage1 laws have safe mean separation `h(x)`, with `0<=h(x)<=epsilon=h(a)`. A policy chooses any safe `X_t` from the full history and independent randomness, stops at a possibly random `N`, and decides a hypothesis. Suppose both error probabilities are at most `p<1/2` and both expected sample counts are finite.

**Theorem A1.** Under either hypothesis,

`E_j N >= 2*sigma^2*kl(p,1-p)/epsilon^2`,

where `kl(p,1-p)=(1-2p)*log((1-p)/p)`.

**Proof.** For the same history, one scalar observation has conditional KL `h(X_t)^2/(2*sigma^2)<=epsilon^2/(2*sigma^2)`. Sampling, randomization and stopping decisions are the same history-dependent kernels under either law and add no conditional KL. Chain rule for the stopped transcript gives

`D(P_0^T || P_1^T) <= epsilon^2*E_0 N/(2*sigma^2)`.

One can obtain the statement by truncating at finite horizons and taking the increasing stopped-record sigma fields, so an unproved optional-stopping identity is not required. Map the final record to its decision. If `alpha=P_0(decide 1)` and `beta=P_1(decide 0)`, data processing gives KL at least `kl(alpha,1-beta)`, which is at least `kl(p,1-p)` when `alpha,beta<=p<1/2`. Reverse the hypotheses for the second expectation. QED.

Since `epsilon<=A*delta*exp(-(c-a)/delta)`, **every** such adaptive procedure still requires

`E_j N >= 2*sigma^2*kl(p,1-p)*exp(2*(c-a)/delta)/(A^2*delta^2)`.

This covers a genuine conventional improvement omitted from a fixed-n cost reading. It does not equate expected and maximum budgets or assert an exact finite-sample expected-cost optimum.

**Conventional positive mechanism.** Measure at `a`, retain the cumulative log likelihood `S_n`, and stop at the first crossing of `+q` or `-q`, with `q=log((1-p)/p)`. Gaussian increments have means `+/-epsilon^2/(2*sigma^2)` and variance `epsilon^2/sigma^2`. This is the classical SPRT, not a new algorithm.

For this symmetric known Gaussian pair, its two errors are equal by reflecting every sample around the midpoint mean. Write that common error as `r`. On the upper crossing, the terminal likelihood ratio is at least `exp(q)`, hence `1-r>=exp(q)*r`, so `r<=1/(1+exp(q))=p`. Almost-sure termination and finite expectation follow, for example, from a strictly positive history-uniform probability of a Gaussian jump large enough to exit the bounded likelihood interval. No zero-overshoot approximation is used in this error bound.

The stage1 stochastic-degradation construction can also simulate a variable-length safe-query policy sequentially from an endpoint stream, stopping after the same number of consumed endpoint records. Thus adaptively choosing the force-query location is not the improvement; allowing data-dependent stopping is.

The executable comparison reports mean, quantiles and maximum observed counts. In particular, a mean of roughly 92 readings is not a promise to finish within 92. The original fixed-n formula remains correct in its declared scope.

## B. Remove the stiffness-boundary explanation

Let `eta∈(0,(L-m)/2)`, `k=(m+L)/2`, `A_eta=L-m-2*eta`, and

`H(x)=A_eta*delta*[sp((x-c)/delta)-sp(-c/delta)]`.

Use the symmetric pair

`f_-(x)=k*x-H(x)/2`, `f_+(x)=k*x+H(x)/2`.

Both are real analytic, vanish at zero, and their derivatives lie in the common fixed interval `[m+eta,L-eta]`. Their difference is `H`. The stage1 Gaussian simulation kernel works with `f_-` as its baseline and `H(x)/H(a)` as its ratio, so all exact binary comparison claims and the sequential bound apply with `A_eta`. A fixed margin from the declared stiffness limits therefore does not remove the exponential barrier. It reduces its force amplitude by an explicit amount.

### Endpoint optimality is not universal over the whole class

Consider instead

`g0(x)=3*x`, `g1(x)=3*x+0.5*tanh(x)*tanh(x-a)`, with `a=0.5`.

Both vanish at zero and are real analytic. The derivative of the added product has absolute value at most `1`, so both derivatives lie in `[2,4]`, strictly inside `[1,5]`. The laws agree exactly at `a`, but differ at `a/2` and at `b=1`. Consequently endpoint-only readings have zero information for this pair; an interior reading can be informative.

This delimits the interpretation of stage1. Its endpoint dominance theorem was for its explicit known pair, whose safe difference is monotone and maximal at `a`. It was not an optimal sampling theorem for every possible analytic family. For two known Gaussian mean laws in general, any location maximizing the absolute mean separation is an experiment dominator; the maximizing location need not be the boundary. More than two unknown candidates can require a genuinely different design.

## C. Stronger positive representation: exact compatible-task certificates

The acquisition goal remains new-regime use. Instead of committing to an unmeasured law, attempt the strongest certificate available from the same data and physical prior. This is ordinary set-membership/optimal-recovery inference; the following derivation makes its exact scope and analytic witnesses explicit.

Let safe positions `0=x0<x1<...<xn<=a` have force intervals `[y_i-r_i,y_i+r_i]`, with the anchor interval `[0,0]` at zero. Put `g(x)=f(x)-m*x`, `A=L-m`,

`l_i=y_i-r_i-m*x_i`, `u_i=y_i+r_i-m*x_i`.

The closed response class is the set of globally nondecreasing `A`-Lipschitz `g` with `g(0)=0`. Define, for any `x>=0`,

```
L_data(x) = max_i [l_i - A*max(x_i-x,0)]
U_data(x) = min_i [u_i + A*max(x-x_i,0)].
```

**Theorem C1.** The finite record is feasible exactly when `L_data(x_i)<=u_i` for every observation, including the anchor. If feasible, both displayed envelopes are feasible nondecreasing `A`-Lipschitz interpolants of the interval record, and every feasible `g` lies between them. Thus they are the sharp pointwise extrema in the closed class.

**Proof.** Monotonicity and the one-sided Lipschitz inequality imply each individual cone bound for any feasible `g`. Their max/min are nondecreasing and `A`-Lipschitz: maxima and minima preserve those two common scalar bounds. `L_data(x_i)>=l_i`; the stated feasibility test supplies the upper constraints, including its zero anchor. Thus `L_data` itself is a feasible witness. Every feasible witness lies below `U_data`, and at each data node `U_data(x_i)<=u_i`, so `U_data` is also feasible. The same argument establishes extremality. QED.

For `b>=a`, the exact closed-class target interval is

```
f(b) in [m*b+max_i l_i, m*b+min_i (u_i+A*(b-x_i))].
```

For a force ceiling `T`, certify `SAFE` if its upper endpoint is at most `T`, `UNSAFE` if its lower endpoint is greater than `T`, and otherwise return `UNKNOWN`. This operation does not recover a hidden law, but it can certify a specific new-regime decision without recovering the full law.

Here `SAFE` denotes only the mathematical force predicate `f(b)<=T`, not general physical safety or permission to exceed the interrogation limit. Sharpness of the closed interval implies optimal positive-margin threshold decisions: every threshold strictly between the analytic infimum and supremum has compatible analytic witnesses on both sides. Equality with a nonattained endpoint can require separate attainment analysis; the displayed rule is conservative there.

### Analytic near-extremizers: the closed-class answer is sharp under positive slack

**Theorem C2.** Assume the finite intervals have a feasible witness strictly inside every non-anchor measurement interval. Then the infimum and supremum at `b` over **real-analytic** laws with `f(0)=0`, `m<=f'<=L`, and the same interval data equal the closed-class endpoints above. They need not be attained. This assumption cannot be silently dropped.

**Constructive proof.** Include `b` as a final knot. Sample an extremal envelope at the finite knots and linearly interpolate; continue with slope zero for `g` outside the extreme knots. Its slopes all lie in `[0,A]`, it respects the data and has the exact target endpoint. Mix it with a strictly feasible piecewise-linear witness by any weight `t>0`. The mixture has data slack at least `t*tau`, for some `tau>0`, and its target differs from the extremum by at most `t*A*b`.

Convolve this globally Lipschitz function with a Gaussian of standard deviation `s`, then subtract its convolved value at zero. The result is real analytic, remains nondecreasing and `A`-Lipschitz, and has zero anchor. Its uniform error from the mixture is at most `2*A*s*sqrt(2/pi)`. Choose `s<t*tau/(4*A*sqrt(2/pi))`, so the smoothing keeps every data interval. Let `t,s→0` to approach the endpoint. Adding `m*x` gives the desired passive analytic laws.

This is explicitly executable: a continuous piecewise-linear `g` is a finite hinge sum. The Gaussian smoothing of `(x-t)_+` is

`(x-t)*Phi((x-t)/s)+s*phi((x-t)/s)`.

Its derivative is `Phi((x-t)/s)`. The code builds both analytic near-extremizers and checks all data constraints; the convolution argument proves the derivative bounds on the full real domain. QED.

**Necessary exceptional case.** If exact noiseless data give `f(a)=m*a`, then `integral_0^a (f'-m)=0`; nonnegativity forces `f'=m` on that interval, and analyticity forces `f(x)=m*x` everywhere. Closed-class piecewise-linear extrapolation would miss this rigidity. This is why C2 requires positive data slack and why exact analytic uniqueness must not be mistaken for stable finite-precision recovery.

### Irreducible outside-regime uncertainty and confidence

For the closed class, `L_data(b)=L_data(a)` and `U_data(b)=U_data(a)+A*(b-a)`. Therefore every feasible target interval has width at least `(L-m)*(b-a)`, even with arbitrarily dense safe observations. Under the positive-slack hypothesis, the same statement holds for analytic infimum/supremum. The strongest certificate can preserve this uncertainty; it cannot remove it.

With `n` fixed-budget safe scalar Gaussian readings at possibly adaptive positions, use radii `sigma*Phi^-1(1-alpha/(2*n))`. Conditional on any chosen history/position, that observation exceeds its radius with probability `alpha/n`. A union bound makes all measurement intervals valid with probability at least `1-alpha`, and then all compatible target decisions are valid together. This is a **per-record** probability statement, not a 99% simultaneous promise across 200 independent records. No stochastic material law prior is assumed.

## D. What has been completed

The stage1 obstruction survives full-domain stress, including interior stiffness margins and arbitrary finite-expected-count stopping procedures. An ordinary sequential method improves its constants; endpoint optimality is explicitly limited to the proper candidate pair. The stronger positive construction produces exact task certificates, constructive analytic near-extremizers, and an independent LP comparison across withheld response families. It agrees with the strongest ordinary set-membership incumbent rather than outperforming it.

No civilisation-changing discovery or validated new capability has been supplied. The precise remaining obstacle is still a supported transition-sensitive measurement/allowed target interrogation or justified quantitative structural prior. The positive certificate sometimes avoids needing that operation for a coarse task; it does not acquire the missing constitutive law or solve the unresolved tasks.
