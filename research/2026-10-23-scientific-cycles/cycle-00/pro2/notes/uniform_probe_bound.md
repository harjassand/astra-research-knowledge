# Uniform Gaussian spectral-distribution bounds

Local lemma work for the parent PRO2 spectral-CDF construction, 21 October 2026.
The proof below is mathematical. The companion simulations are implementation
diagnostics, not a certificate of a tail probability or a scientific benchmark.

## 1. Objects and exact scope

Let A be a fixed real symmetric n by n matrix, n >= 1. Let g_1,...,g_s be
independent standard Gaussian vectors in R^n, independent of A, with a fixed
positive integer sample count s. Put P(t) = 1_{A <= t} and

    F(t) = rank P(t) / n,
    F_raw(t) = (1/(n s)) sum_l g_l^T P(t) g_l.

All thresholds t are covered by the same probability event. Thus a threshold
selected after inspecting the probes is allowed. No spectral gap, bounded
condition number, known support interval, simple spectrum, or eigenvalue
computation is required for the probability statements.

The Gaussian and independence hypotheses matter. They are not interchangeable
with arbitrary isotropic probes. The fixed-A condition can be replaced by
conditioning on a random A independent of the probes. It cannot be dropped
when A is chosen using the same probes. A fixed-probe statement does not by
itself cover an adaptively chosen number of probes.

## 2. Unnormalised uniform theorem

For every x > 0,

    Pr{sup_t [F_raw(t)-F(t)] > 2 sqrt(x/(ns)) + 2x/(ns)} <= exp(-x),

    Pr{sup_t [F(t)-F_raw(t)] > 2 sqrt(x/(ns))} <= exp(-x).

Consequently, for delta in (0,1), with probability at least 1-delta,

    sup_t |F_raw(t)-F(t)|
       <= 2 sqrt(log(2/delta)/(ns)) + 2 log(2/delta)/(ns).       (U)

There is no multiplicative n in the failure probability and no log n in this
bound. Notice that F_raw(+infinity) is random; F_raw is not a probability CDF.

### Proof

Choose an orthonormal eigenbasis of A, ordered by eigenvalue. Rotational
invariance of a standard Gaussian makes all coordinates in this basis
independent N(0,1). For each eigen-direction i, define

    W_i = sum_l (g_l)_i^2,   X_i = W_i-s,
    S_k = sum_{i=1}^k X_i,   S_0=0.

The W_i are independent chi-square_s variables. For a threshold t whose spectral
projector has rank k,

    F_raw(t)-F(t) = S_k/(ns).

If eigenvalues repeat, the available k form a subset of {0,...,n}; bounding all
prefixes therefore remains valid, with no division by a spectral multiplicity.

The exact log moment generating function is

    log E exp(lambda X_i)
       = s[-lambda-(1/2)log(1-2lambda)],  lambda < 1/2.

For 0 < lambda < 1/2, the power series yields

    -lambda-(1/2)log(1-2lambda)
       = sum_{j>=2} (2^{j-1}/j) lambda^j
       <= lambda^2/(1-2lambda).

For lambda >= 0,

    log E exp(-lambda X_i)
       = s[lambda-(1/2)log(1+2lambda)] <= s lambda^2.

The latter inequality follows because the derivative of
lambda^2-lambda+(1/2)log(1+2lambda) is 4lambda^2/(1+2lambda), and the expression
vanishes at zero.

For fixed lambda in (0,1/2), the process

    M_k = exp(lambda S_k - k s lambda^2/(1-2lambda))

is a nonnegative supermartingale starting at one. Stop it at its first crossing
of a positive constant, or at n if no crossing occurs. The elementary optional
stopping/Markov argument gives Pr{max_{k<=n} M_k >= c} <= 1/c. Therefore

    Pr{max_{k<=n} S_k >= a}
       <= exp[-lambda a + ns lambda^2/(1-2lambda)].

Set r=sqrt(x/(ns)), lambda=r/(1+2r), and a=2sqrt(ns x)+2x. Direct substitution
makes the exponent -x. This proves the upper-tail claim.

The same argument for exp(-lambda S_k-k s lambda^2), with
lambda=sqrt(x/(ns)) and a=2sqrt(ns x), proves the lower-tail claim. Take their
union and x=log(2/delta), then divide by ns. This proves (U).

The chi-square mgf and sub-gamma constants are standard; this proof explicitly
adds the maximum over ordered eigen-directions, instead of taking a union bound
over n separate pointwise projector estimates. No historical novelty claim for
that standard maximal-martingale argument is intended.

## 3. Stronger bound after normalising the aggregate

Define

    T = sum_l ||g_l||^2,
    H(t) = [sum_l g_l^T P(t) g_l] / T.

T>0 almost surely. H is a probability CDF. This is the norm-squared-weighted
average of the individually normalised probe CDFs:

    H(t) = sum_l alpha_l [v_l^T P(t) v_l],
    v_l = g_l/||g_l||,   alpha_l=||g_l||^2/T.

It is **not** the equal-weight average (1/s)sum_l v_l^T P(t)v_l. The two laws
must not be conflated.

### Theorem for an even number of real Gaussian probes

Suppose n>=2 and s=2m is a positive even integer. Then for every epsilon>0,

    Pr{sup_t |H(t)-F(t)| > epsilon}
       <= 2 exp[-(ns-2) epsilon^2].                           (D)

Thus a simultaneous radius at failure probability delta is

    epsilon_D = sqrt(log(2/delta)/(ns-2)).                    (D-radius)

It may be clipped to 1 because both functions are probability CDFs. For n=1,
H=F exactly for every positive probe count, so no radius is needed.

### Proof

The weights W_i/2 from the preceding proof are independent Gamma(m,1)
variables. Their normalised vector has the Dirichlet(m,...,m) distribution.
Here is the specific order-statistic representation needed below.

Let M=nm and let E_1,...,E_M be independent exponential variables of mean one.
Their normalised vector E_j/sum E has uniform density on the (M-1)-simplex.
To verify this, change variables from E to total r and the first M-1 normalised
coordinates; the Jacobian is r^(M-1), so integrating exp(-r)r^(M-1) over r>0
gives the constant (M-1)!.

The spacings (U_(1), U_(2)-U_(1),...,1-U_(M-1)) of M-1 independent Uniform(0,1)
order statistics have that same density: the order-statistic density is
(M-1)! on the ordered simplex, and the spacing transformation has Jacobian one.

Group the E_j into n disjoint blocks of m variables. Their block sums are
independent Gamma(m,1), and their normalised cumulative block sums therefore
have the joint law

    (sum_{i<=k} W_i / sum_{i<=n} W_i)_{k=1,...,n-1}
          =_law (U_(km))_{k=1,...,n-1}.                      (S)

Write N=M-1. The empirical KS distance of these N uniforms is

    D_N = max_{1<=j<=N} max{j/N-U_(j), U_(j)-(j-1)/N}.

For each j, its plotting position j/(N+1) lies between (j-1)/N and j/N.
It follows deterministically that

    |U_(j)-j/(N+1)| <= D_N.

In particular, for j=km, j/(N+1)=k/n. Applying the classical two-sided
Dvoretzky-Kiefer-Wolfowitz-Massart inequality

    Pr{D_N > epsilon} <= 2exp(-2N epsilon^2)

to (S) gives (D), since 2N=ns-2. The available spectral ranks are again a subset
of these prefixes if A has repeated eigenvalues. This proves the theorem.

### Interpretation and limitations

The improvement over (U) is a real improvement in the available bound, with a
different normalisation of the same Gaussian probes. It is not evidence that
norm-weighted SLQ universally outperforms equal-weight spherical SLQ. For a fixed
rank fraction p=k/n, the two exact variances are

    Var[H(t)] = p(1-p)/(ns/2+1),
    Var[(1/s)sum_l v_l^T P(t)v_l] = p(1-p)/(s(n/2+1)).

The equal-weight spherical estimator has smaller pointwise variance when s>1.
The advantage of (D) is an elementary simultaneous confidence guarantee with
no threshold-count factor, not a blanket variance or runtime advantage.

For odd s, the integer-spacing proof above does not apply. One may use (U),
choose an even probe count before sampling, or supply an additional independent
probe and account for its cost. Do not state (D) for odd s without another proof.

Even (D) is not a cheap exact-rank certificate. Making its two-sided radius
smaller than 1/(2n) by this formula requires ns-2 > 4n^2 log(2/delta). This is a
sample-budget implication of this particular sufficient bound, not an
information-theoretic lower bound or a proof that every rank-estimation method
requires linearly many probes.

## 4. Adaptive probe count requires an explicit correction

Fix a deterministic increasing schedule of even counts s_j, j=0,1,... . Reuse
the growing prefix of one iid Gaussian sequence and set

    delta_j = 6delta/[pi^2(j+1)^2],
    epsilon_j = sqrt(log(2/delta_j)/(n s_j-2)).

The probabilities of failure sum to at most delta. A union bound, requiring no
independence between stages, therefore proves

    Pr{for every j and every t, |H_j(t)-F(t)| <= epsilon_j} >= 1-delta.

Any finite stopping stage selected from the observed results is then covered.
With a doubling schedule this adds a log log s term inside the logarithm.
This is a simple spending construction, not a claim of an optimal confidence
sequence. For unnormalised probes, the same spending scheme applies with (U).

Adaptive threshold, quadrature depth or perturbation-margin choices at a fixed
probe count need no additional sampling union bound if the corresponding
deterministic enclosure is valid for every such choice on the same Gaussian
event. Adaptive matrix selection using the same probes is not covered.

## 5. Deterministic robustness to stored-probe perturbation

Flatten the ideal Gaussian block G=[g_1 ... g_s] into a nonzero vector in R^(ns),
and similarly flatten a stored block Gtilde !=0. Suppose a coupling supplies
the deterministic bound ||G-Gtilde||_F <= r. For every orthogonal projector P,

    | ||PG||_F^2/||G||_F^2
       - ||PGtilde||_F^2/||Gtilde||_F^2 |
        <= min{1, r/||Gtilde||_F}.                           (R)

Indeed, normalise the two flattened vectors to u and v. The Hermitian matrix
uu^T-vv^T has nonzero eigenvalues plus/minus sqrt(1-(u^T v)^2). Therefore the
absolute difference of expectations of any orthogonal projector is at most
that sine of the angle. The distance from Gtilde to span(G) equals
||Gtilde||_F times this sine and is no greater than ||Gtilde-G||_F. This proves
(R), including the trivial cap at one.

The relevant projector on the flattened block is I_s tensor P(t), so the same
deterministic slack holds uniformly over t. Add it to (D-radius) when a valid
Gaussian-to-stored-block coupling is provided. A generic PRNG library call
does not by itself certify that coupling. The simulation below assumes the
usual pseudo-random numerical Gaussian/chi-square model and does not claim
verified continuous-randomness generation.

## 6. Consequence for bounded-variation observables

On the event sup|H-F|<=epsilon, integration by parts gives

    |integral f dH - integral f dF| <= TV(f) epsilon

for every bounded function f of finite total variation, with the usual
right/left conventions for its Stieltjes representation. In particular, a
monotone function taking values in [a,b] has error at most (b-a)epsilon.
The same event covers functions selected after observing the probes, provided
their stated variation bound is valid. This is a standard deterministic
consequence of a uniform CDF bound, not a new concentration theorem.

## 7. Numerical diagnostics and resource receipt

Run:

    python3 restore_pro2/notes/check_uniform_probe_bound.py

The recorded run used NumPy 2.3.5 and seed 202610210731. It checked six
(n,s) cases, each with 50,000 independent numerical chi-square vectors, at
nominal delta=0.1. Raw-bound exceedance fractions ranged from 0.0025 to 0.01708.
For the five eligible even-s cases, normalised-bound exceedance fractions
ranged from 0.00008 to 0.07732. Five additional grouped-spacing experiments,
5,000 repetitions each, checked the deterministic inequality against the
ordinary KS statistic; none violated it. A 5,000-repetition tied-spectrum
index-set check found no increase in the prefix maximum.

Observed script-body wall time: 0.42444781999984116 seconds.
Observed script-body CPU time: 0.951605322 seconds.
Peak whole-process RSS on the Linux runtime: 41,725,952 bytes.
These are diagnostics for this local lemma. Search, proof development and
model inference costs were not measured. No baseline speedup is claimed.
Complete numeric outputs are in uniform_probe_diagnostics.json; the replay
script rewrites that diagnostic JSON with the new run's measured resources.

## 8. Primary-source dependencies and attribution

The raw theorem above is proved from the Gaussian mgf and a bounded stopping
argument. Laurent and Massart's well-known chi-square concentration constants
are related background, not an unproved imported step here:

* B. Laurent and P. Massart, "Adaptive estimation of a quadratic functional by
  model selection", Annals of Statistics 28(5), 1302-1338 (2000).
  DOI https://doi.org/10.1214/aos/1015957395 .

The normalised theorem imports the classical two-sided DKWM bound. The
Dirichlet/grouped-spacing reduction is proved explicitly above.

* P. Massart, "The Tight Constant in the Dvoretzky-Kiefer-Wolfowitz Inequality",
  Annals of Probability 18(3), 1269-1283 (1990).
  DOI https://doi.org/10.1214/aop/1176990746 .
* H. W. J. Reeve, "A short proof of the Dvoretzky-Kiefer-Wolfowitz-Massart
  inequality", arXiv:2403.16651v1 (2024), primary proof source read for the
  concentration statement and its scope:
  https://arxiv.org/html/2403.16651v1 .
  Reeve proves stronger one-sided/local variants; those refinements have not
  been transferred to the spectral construction here.

The Project Euclid original-paper endpoints returned an iframe wrapper to the
available browser/search parser. Bibliographic identity was confirmed, but
their original full texts were not falsely represented as inspected.
No historical-priority claim is made for the spectral Dirichlet/DKW application;
the parent's dedicated closest-literature check governs novelty assessment.
