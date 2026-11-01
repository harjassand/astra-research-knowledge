# Independent review: stable neutral-path model and bounded-profile obstruction

**Disposition: PASS for the stated model, finite-horizon no-service result, and
bounded-comparability geometric-Foster obstruction.** This is not an instability
result. The quantitative extension below is a new result of this review and needs
its own independent review before being called accepted.

Reviewed source: `neutral_return_obstruction_root_20261101/STABLE_PATH_NETWORK_BOUNDED_PROFILE_OBSTRUCTION.md`.
SHA-256: `0f6a4405e9566b070100322606f004ea1f58dda08fd7ea46d03cec1da8d3e478`.
The source was read and hash-checked before and after the independent checks; it
was not edited. Review is by the separately tasked return-path construction agent.
No external sources were retrieved.

## 1. Model, stationary law, and communication

The six binary complexes are 2A, AB, AC, AD, AE, CD. The five undirected edges
in the source form a connected tree. Every A+satellite arm occurs. All constants
are one and falling-factorial propensities are used. For every directed pair
u -> v, at enabled x and y=x-u+v,

  [1 / product_i x_i!] (x)_u
    = 1 / product_i (x_i-u_i)!
    = [1 / product_i y_i!] (y)_v.

Thus the product of five Poisson(1) measures satisfies pairwise detailed balance,
including the 0 <-> A port. Binary complex paths give 2A -> A+Xi, and actual port
deaths give singleton production and removal. Translation of these enabled paths
proves irreducibility. Constant immigration bounds the total count above by its
initial value plus a rate-one Poisson process, proving nonexplosion. The stated
positive recurrence and all finite stationary exponential moments follow.

## 2. Dominant process and stopping are legitimate

In the dominant process, exactly immigration, AB -> CD, CD -> AB, and CD -> AE
remain. Direct checking of every retained jump proves

  C+A = D+A = 1+I,
  B = N-I+A-E,

with E nondecreasing and equal to the number of CD -> AE jumps. Before immigration
number m+1, its intensity CD is at most (m+1)^2. Stop this counting process there;
its count by T is stochastically dominated by Poisson(T(m+1)^2). This establishes
the two stated tail terms without conditioning intensities on a future event.
The actual and dominant processes can be constructed with the same clocks until
the first suppressed (bad) event. An exit through the count bounds before that
event is therefore covered by the dominant tail bound.

## 3. Full-generator audit

The exact A drift of the **full** process is

  L A = 1-A-3A(A-1)+A(C+D)+2CD-AB.

The cancellation of +AE (AE -> 2A) with -AE (AE -> CD) is exact; the source's
coarser upper bound did not need this cancellation. The exact bad intensity is

  q_bad = A+3A(A-1)+A(C+D+2E).

For S=A+C+D+E<K and B>N/2 these imply the source's inequalities

  L A <= 1+2K^2-(N/2-K)A,
  q_bad <= (1+5K)A.

Stopped Dynkin is valid: the stopped pre-jump states are bounded in the relevant
coordinates, and the total-count Poisson bound supplies all other integrability.
Its terminal value A(stop) is nonnegative, which gives the claimed integral-A
bound with the correct direction. Counting the first bad event by its compensator
then gives equation (1). No post-success trajectory, failed attempt, or death
channel has been omitted. The m,ell then N order of limits yields equation (2).

## 4. MGF and Foster contradiction

Total count equals N+2+I-D_A pathwise. The difference between the immigration MGF
and the actual exponential-count increment is bounded by

  E[r^I 1_{D_A>0}] <= (E r^(2I))^(1/2) P(D_A>0)^(1/2).

No independence is required. For fixed T this proves equation (3). For any
nonnegative finite-valued geometric Foster function, localized integrating-factor
Dynkin and Fatou give the expectation inequality; bounded comparability makes
integrability particularly immediate here. Dividing that inequality by r^(N+2)
and taking N -> infinity gives exactly

  c exp(T(r-1)) <= C exp(-zeta T).

The allowed arbitrary fixed T yields the claimed contradiction. The conclusion
properly concerns the geometry of W, not the already established stationary
moments or recurrence.

## 5. Checks and limits

`check_obstruction.py` independently constructs the raw model and checks 1,808
integer states, all detailed-balance channels at those states, 325 dominant
invariant instances, the connected-tree claim, and 100 exact constant checks.
These finite tests corroborate algebra; the proofs above and in the quantitative
addendum, not the tests, establish the infinite-state assertions.

The root source is accepted by this review at its exact hash. The quantitative
N^(1/6) addendum is separate new author work. No blanket general-path theorem,
sharp time-scale claim, scalar acquisition shortcut, or external novelty claim
is made.
