# A constructed response operation fails the strong ordinary comparator

**Outcome:** the candidate is a useful exact supplied-model operation, but
its central construction is established block-exponential machinery. A
strong ordinary implementation can execute precisely the same kernel;
ordinary derivative jets can also reduce the small-perturbation integer
cost. No new consequential scientific capability is established. This wave
is complete as a decisive scoped failure, rather than an idea ranking.

The initial assumption inversion, source screen and concrete construction
were developed independently of the capability-inversion worker. The
quartic programme was not extended. All new files are confined to this
owned directory. `CONTRACT.md` fixes the inputs, outputs, competitors and
12 cases before acquisition. `SOURCES.md` preserves current Astra sources
and affirmative primary prior-art collisions.

## 1. The hidden assumption and the actual operation

Many engineering decisions compare two nearly equal simulated responses.
Computing each O(1) response separately to resolve their O(eta) difference
may cost precision proportional to1/eta. The candidate instead evolves a
normalized response directly, carrying the small perturbation only in the
operator and the final multiplication.

Let Q be a supplied finite conservative Markov generator, acting on column
observables, so Q is Metzler and Q1=0. Let D be a supplied nonnegative
diagonal matrix, b>=0, c>=0, t>=0, eta>0. The desired normalized response is

    r_eta(t)=c^T[e^(tQ)-e^(t(Q-eta D))]b/eta.                (1)

The physical difference is eta*r_eta. The output contract is a rational
interval of prescribed ABSOLUTE width for r_eta. This is not relative
accuracy when r_eta is arbitrarily small. All model coefficients, b,c,
D,eta,t and a uniformization rate are supplied equally to every method.
They are not learned from experiments, passive data, or a free oracle.

Put A_eta=Q-eta D. Solve

    u'=Qu,       u(0)=b,
    z'=A_eta z+Du,       z(0)=0.                            (2)

Subtracting the equations for u=e^(tQ)b and v=e^(tA_eta)b proves
u-v=eta*z, so (1)=c^Tz exactly. Equivalently,

    z(t)=integral_0^t e^((t-s)A_eta)D e^(sQ)b ds.            (3)

All integrands are nonnegative. If B=||b||inf and d=||D||inf, then
0<=z<=Bdt componentwise because both semigroups are substochastic.

This would transfer a computed response certificate across positive
transport, reliability, network dynamics and linear-control models. It
does not acquire their generators, calibrate their noise, or demonstrate a
physical implementation. Those missing tasks remain outside the contract.

## 2. Positive uniformization gives an exact finite certificate

Choose lambda>0 such that

    P0=I+Q/lambda>=0,
    Peta=P0-eta D/lambda>=0.

Both matrices are substochastic. With mu=lambda*t, define

    U_0=b, Z_0=0,
    U_(k+1)=P0 U_k,
    Z_(k+1)=Peta Z_k+(D/lambda)U_k.                         (4)

Then

    z(t)=e^(-mu) sum_(k>=0) mu^k/k! Z_k.

The augmented matrix in(4) is nonnegative but need NOT be substochastic;
we do not incorrectly apply a Markov norm bound to that full block.
Expanding its upper-right block instead proves

    Z_k=sum_(j=0)^(k-1) Peta^j(D/lambda)P0^(k-1-j)b,
    0<=Z_k<=k Bd/lambda.

Therefore, after terms0 through m, the omitted response is bounded by

    B d t ||c||_1 Pr[Poisson(mu)>=m].                       (5)

The truncation degree required for a prescribed normalized absolute error
does not depend on eta. This is an iteration-count statement, not a bit-
cost statement: propagating a rational eta can still create large integers.

All input coefficients in the implementation are rational. The state
vectors are propagated as integer numerators with a common denominator,
and the scalar weighted sums use exact Fraction arithmetic. A rational
interval for e^(-mu) is obtained by enclosing the positive exponential
series for e^mu and inverting its endpoints. Its remainder is bounded by
the first omitted term divided by1-mu/(k+2), after k+2>mu. A Poisson tail
after m is bounded similarly by

    e_hi * mu^(m+1)/(m+1)! / [1-mu/(m+2)].                  (6)

Equations(5)-(6) and the exponential endpoints provide rational lower and
upper bounds. No PRNG, empirical confidence interval, floating matrix
positivity or numerical solver status is a proof premise.

## 3. The central construction is exactly an ordinary operation

Equation(3) is the upper-right block of

    exp(t [[A_eta,D],[0,Q]]).

It is precisely the unequal-diagonal-block convolution in Van Loan1978,
Theorem1, rather than a new transform. The general operator and modern
efficient algorithms are explicit in Al-Mohy arXiv2410.03575v2. Sparse
exponential action is also established, including Al-Mohy--Higham2011.
See `SOURCES.md` for exact versions and read scopes.

An independently assembled generic sparse block implementation is included
as a real comparator. In EVERY saved case its rational partial sum and
both interval endpoints are IDENTICAL to the candidate's fused recurrence.
Factoring the common denominators and fusing the two vector updates is
available to the ordinary block method too. Consequently the ordinary
method may execute the identical fused kernel, with identical arithmetic
counts and precision contract on every admissible input. A speed gain over
separate response evaluation cannot establish a new operation here.

## 4. Stronger ordinary control: positive derivative jets

The comparator also exploits ordinary perturbation coefficients. Set

    f_0'=Qf_0, f_0(0)=b,
    f_j'=Qf_j+D f_(j-1), f_j(0)=0, j>=1.

For the finite CTMC X with generator Q and
L_t=integral_0^t D(X_s)ds, the Feynman--Kac expansion gives

    f_j(t)_i=E_i[b(X_t)L_t^j]/j!,
    r_eta=sum_(j>=1)(-eta)^(j-1)c^T f_j(t).                 (7)

The exponential Taylor remainder on the nonnegative random variable
eta L_t proves, for truncation at K,

    |remainder|<=eta^K B ||c||_1 (dt)^(K+1)/(K+1)!,         (8)

with sign(-1)^K. This sign holds for every eta>=0; no small-eta convergence
premise or monotonicity guess for empirical coefficients is needed.

All f_j are nonnegative. Uniformize their triangular coefficient system
using P0 and D/lambda. Its kth discrete coefficient for level j is bounded
by binom(k,j)B(d/lambda)^j. Thus the omitted coefficient after m terms is

    B(dt)^j/j! * Pr[Poisson(mu)>m-j].                      (9)

Each coefficient interval is combined with the exact alternating weight
(-eta)^(j-1) and the signed remainder(8). This method propagates only the
unperturbed denominator. eta enters the final scalar arithmetic instead of
every state-vector coefficient. It retains the input bit-length cost, but
can avoid multiplying that length by the propagation depth. This is an
ordinary differentiated-uniformization/perturbation method, not a new
capability claim. Its recurrences and certificates are proved here directly.

## 5. All predeclared cases and their cost

`compare_responses.py` constructs and writes the FULL explicit input,
then each method separately reads, validates and processes that input.
There is no free full-matrix oracle. The12 cases are n=64,512,4096 crossed
with eta=10^-2,10^-8,10^-14,10^-20. All use normalized tolerance10^-12,
lambda=2,t=4, the declared cyclic sparse transition, nonconstant positive b,
four killing locations and readout c=e_0. Exact input files have2212,
18519 and162490 bytes respectively. Input generation and writes are charged
in the query-wave time; every method's timing includes fresh model reading,
validation, its own setup and exact propagation/certificate calculation.

All48 method evaluations produced rational intervals of width<=10^-12.
Every group of four intervals has a common intersection. The candidate and
generic ordinary block endpoints are exactly equal, not merely overlapping.

The candidate uses38 terms for every eta. Separate exact exponentials need
39,48,55,62 terms respectively. That is a real conditioning cost of the
separate-evaluation formulation. But ordinary jets need orders7,2,1,1,
and avoid the perturbation-dependent integer growth. At n4096:

| eta | candidate seconds | generic ordinary block seconds | ordinary jets seconds | separate exact responses seconds |
| --- | --- | --- | --- | --- |
| 10^-2 | .08715 | .08040 | .24802 | .10494 |
| 10^-8 | .10000 | .09278 | .10109 | .16274 |
| 10^-14 | .11720 | .11890 | .07076 | .25930 |
| 10^-20 | .14011 | .16275 | .07228 | .43728 |

These are single-run shared-host acquisition records, not statistically
validated speed ratios or a universal performance theorem. The strongest
ordinary method is allowed its identical fused block kernel as well as the
generic implementation and jets. It therefore cannot lose merely because
we gave the candidate better Python loop organization. The saved derived
best-ordinary statistic takes the minimum of these three allowed choices.

At eta10^-20 the candidate's largest final integer has2643 bits for n4096,
versus119 bits for the ordinary first derivative and4309 bits for separate
responses. The observed jet speedup reflects a real recorded precision
cost, though no asymptotic performance claim is inferred from12 fixtures.

The full declared12-case/four-method query wave took2.777228s. It includes
input generation, writing, repeated reading/validation, all propagation,
exact arithmetic, result serialization and loop overhead. It excludes
startup and the shared initial scalar exponential enclosure. A separate
fresh-process prefix measurement, without repeating the query wave, charges
those omitted phases at0.0255312s; see `PREFIX_COST.json`. These are separate
measurements, not a fabricated single end-to-end sample. Source retrieval,
scientific reasoning/token/monetary cost and unknown-system identification
are not folded into an unsubstantiated overall efficiency claim.

## 6. Independent reconstruction and limits

`verify_response_values.py` imports no producer code and propagates actual
Fraction vectors rather than common-denominator integer vectors. For n64
at eta10^-2 and10^-20 it independently reconstructs all four truncated
sums and all endpoints, including jet orders7 and1. It checks the exact
discrete Duhamel identity eta*Z_k=U_k-V_k at EVERY step,40 and63 steps
respectively. It independently bounds e^(-8) by raising an alternating
exp(-1) series enclosure to the eighth power, rather than reusing the
producer's inverse positive-series construction. It also checks saved
precision and best-comparator arithmetic in all12 cases. This consumer
took0.405178s after imports. This is an independent code-path replay in
the same worker, not a separate peer acceptance or new empirical evidence.

The bounded mission here closes as **NO_NEW_CAPABILITY / SCOPED_FAILURE**:
the stable response operation was constructed, certified and compared at
its complete supplied-model contract; established ordinary machinery
already supplies it, and a stronger ordinary refinement wins the small-
perturbation precision comparison. The failure is specific to this claimed
operation. It is not an impossibility theorem for all task-directed
response computation, all generator acquisition, or all scientific methods.
