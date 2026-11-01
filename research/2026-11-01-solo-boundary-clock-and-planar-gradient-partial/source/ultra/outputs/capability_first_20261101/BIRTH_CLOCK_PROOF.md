# Can one linear reservoir stabilize an arbitrary conservative module?

The capability sought is a topology-level stability guarantee: for a finite
weakly reversible conservative mass-action module, does adjoining the sole
reservoir pair `0 <-> A` make every closed irreducible class positive recurrent?
Full success would remove the need to supply an equilibrium, a mixing theorem,
or a separate boundary service assumption for each module. This is a mathematical
count-chain question. No physical control or chemical implementation follows.

The broader weak-reversibility recurrence question remains the reference target.
The reservoir question isolates an important primitive inside it. This document
constructs access to that primitive and proves two population-uniform boundary
escape estimates. It does not prove the universal recurrence assertion.

## 1. The actual immigration-clock operator

Let the internal reactions preserve a positive integer weight `w.x`. Let
`0 -> A` have rate lambda and `A -> 0` rate mu*x_A, with fixed positive rational
rates throughout. Write `Q` for the internal-plus-death generator, without
immigration, and `U f(x)=f(x+e_A)`.

Between immigration events, `w.x` never increases. Hence from x the exact
accessible set is contained in the finite set `w.z <= w.x`. Enumeration of that
whole set, followed by solving a finite rational linear system, constructs

    R_lambda f(x) = E_x[f(Y_E)],       E ~ Exp(lambda), independent,
    (lambda I-Q) R_lambda f = lambda f.

Here Y retains every internal reaction and true-death clock. The chain sampled
immediately after immigration has operator

    P = R_lambda U.

For K immigration events, set `g_0(x)=w.x` and `g_k=R_lambda U g_(k-1)`.
Then `g_K(x)` is the exact expected weight just after the Kth immigration.
All states used satisfy `w.z <= w.x+K*w_A`. This is finite access without a
stationary fiber, a reflecting boundary, a discarded overflow channel, or an
assumed conditional law. The work is real: enumeration, sparse/dense elimination,
and rational bit lengths grow with that finite state set.

With equal weights, shell n has binomial(n+d-1,d-1) states; the downward death
blocks permit solving shells in increasing n. The executable uses this recursion
for three species. The construction above also specifies the weighted case.

### Certified numerical access

On a finite downward sublevel, `(lambda I-Q)^(-1)` is nonnegative and its infinity
norm is `1/lambda`: its stochastic integral representation has row sum exactly
`1/lambda`. For a rational approximate solution v with residual r, therefore

    ||v-R_lambda f||_infinity <= ||r||_infinity/lambda.

If the previous-birth right side has uniform error e, the next error is at most
`e+||r||/lambda`. The executable converts every stored binary floating-point
number to its exact rational value and evaluates every residual row with
`Fraction`. The bound includes all downward shells and all K stages. A finite
result is not an asymptotic recurrence proof.

## 2. What a uniform service estimate would buy

Suppose for one fixed K, `0<c<=1`, finite C and all sufficiently large states in
a closed class,

    g_K(x) <= (1-c) V(x)+C,            V=w.x.                 (1)

Nonexplosion already holds: `V(X_t) <= V(X_0)+w_A Poisson(lambda*t)` and finite
weight sublevels have bounded rates. Put `b=K*w_A` and `Delta=V(X_TK)-V(x)`.
Then `-V <= Delta <= b`. The convex chord inequality gives, for theta>0,

 E exp(theta*Delta)
 <= ((b-E Delta)/(V+b))*exp(-theta*V)
    +((V+E Delta)/(V+b))*exp(theta*b).

Inserting (1) makes the limiting upper bound at most
`(1-c)*exp(theta*b)`. Choose theta small enough that this is <1 (any theta if
c=1). Thus `P^K exp(theta V) <= rho exp(theta V)` outside a finite head, with
rho<1. Inside the head the expectation is finite because upward jumps are bounded.
This proves positive recurrence for a closed irreducible skeleton class and a
stationary exponential weight moment. One may construct an invariant probability
for P by averaging the K phase shifts of an invariant probability for P^K;
`P^j exp(theta V) <= exp(theta*j*w_A) exp(theta V)` preserves the moment.

To return to actual continuous time, start at a post-immigration state with
stationary law eta for P and define

    pi(f)=lambda E_eta integral_0^E f(Y_s) ds = eta R_lambda f.

The identity `R_lambda Q=lambda(R_lambda-I)` and `eta R_lambda U=eta` give
`pi[Q+lambda(U-I)]=0`. Also `pi(exp(theta V)) <= eta(exp(theta V))`, since weight
cannot increase before the next birth. Thus (1), if constructed, yields the
actual-time invariant law and moment. No clock conversion is assumed free.

A negative constant drift instead of (1) is also a usual positive-recurrence
route, but does not by itself establish the exponential-moment conclusion above.

## 3. A non-complex-balanced test of the missing boundary service

Use falling-factorial propensities and the directed cycle

    2A+B --1--> 2B+C --2--> A+2C --3--> A+B+C --5--> 2A+B,
    0 <-> A, both reservoir rates one.

The internal stoichiometric rank is two. With the separate reservoir linkage,
the whole network has six distinct complexes, two linkage classes,
and rank three, hence deficiency one. (The four cubic complexes plus 0 and A
are the six.) Its complex-balance equations, for positive a,b,c, require

    a^2 b = 2 b^2 c = 3 a c^2 = 5 a b c.

The first and last give `a=5c`; the third and last give `b=3c/5`;
the second and last give `b=5a/2`. These are inconsistent. Thus the ordinary
complex-balanced product-Poisson construction does not apply. Failure of those
equations does not prove absence of every possible product form.

Write its four internal rates as

    r1=A(A-1)B, r2=2B(B-1)C, r3=3AC(C-1), r4=5ABC.

The three-complex equal-rate cycle retained in the computation is a deficiency-
zero product-Poisson control, not a new recurrence result.

## 4. Uniform escape from the B face, including the physical clocks

Fix integer N0>=1000, H=N0/100, and J=A+3C. Start with N=N0 and
`2<=J<H`. Stop at the first of `N<=N0/2`, `J>=H`, or `J<=1`; call the time tau.
Before stopping, B>.49 N0>=10, A/B<=1/32 and C/B<=1/96. Consequently

    r3 <= (5/9216) r2,       r4 <= (25/288) r2,
    A <= r1/10 + r2/180.                                    (2)

For the last inequality, if A>=2 use r1>=AB; if A=1 then activity means C>=1
and r2>=180; if A=0 it is immediate. Terms with C=0 vanish and are covered.

The J jumps are `+1,+4,-3,-2` for the four reactions, `-1` for true death,
and `+1` for immigration. Direct application of the actual generator gives

    L(2^-J)/2^-J
      = -r1/2-15r2/16+7r3+3r4+A-1/2
      <= -(r1+r2)/4-1/2.                                  (3)

All constants in this comparison are rational. On `J>=2`,

    L log J >= [(2/3)r1+(4/3)r2-(21/4)r3-4r4-2A]/J
            >= (r1+r2)/(3J) >= B/6 >= N0/13.               (4)

The logarithm bounds follow from `log(1+t)>=t/(1+t)` and
`log(1-t)>=-t/(1-t)`. A -3 jump requires J>=7; a -2 jump requires J>=4.
For the final inequality in (4), `r1+r2 >= BJ/2` follows by splitting
`A>=2`, `A=1,C>=1`, and `A=0,C>=1`.

All exit states have `1<=J<=H+4`. Localized Dynkin and (4) therefore give

    E tau <= 13 log(H+4)/N0.

The nonnegative supermartingale in (3) gives

    P(J_tau<=1) <= 2^(1-J_initial).

Thus a seed `A=2,C=0` escapes to macroscopic `A+3C` or loses half the initial
population, with probability at least 1/2, in expected time O(log N0/N0).
Immigration and last-copy death were included in the calculation.

## 5. Uniform escape from the C face

Use J=3A+B and the same H and stopping rules. Before stopping C>.49 N0,
A/C<=1/96, B/C<=1/32. Now

    r1 <= r4/480,       A <= r3/270.

The J jumps are `-5,+1,+1,+3`, true death gives -3, immigration gives +3.
Consequently

    L(2^-J)/2^-J
      =31r1-r2/2-r3/2-7r4/8+7A-7/8
      <= -(r2+r3+r4)/4-7/8.

Use log(J+1), since last-copy death can take J=3 to zero. Its drift obeys

    L log(J+1)
      >= [r2/2+r3/2+r4-(35/3)r1-9A]/J
      >= (r2+r3+r4)/(3J) >= C/3 >= N0/7.

A -5 jump requires J>=7 and a -3 death requires J>=3. Also
`r2+r3+r4>=CJ` on every active state J>=2 (split B>=2 and B<=1).
All exit states have `0<=J<=H+3`. Therefore

    E tau <= 7 log(H+4)/N0,
    P(J_tau<=1) <= 2^(1-J_initial).

In particular the single immigrant seed `A=1,B=0` has J=3 and success
probability at least 3/4. This explicitly pays its last-copy death hazard.

## 6. The remaining obstruction

An escape to macroscopic A+3C or 3A+B is not a port-occupation estimate.
Even reaching A>=epsilon N is insufficient: internal rates can be O(N^3),
whereas death is O(N), so one activation does not ensure a molecule is removed.
The missing step is a population-uniform lower bound on accumulated actual
A-occupation, with returns, failed seeds, and competing clocks included, strong
enough to establish (1) or an adequate weaker drift. The exact resolvent constructs
this quantity for each finite input; the analytic face estimates cover two
nontrivial boundary entries; neither supplies the universal asymptotic bound.

For the general reservoir question one must also obtain a classwise norm when
there are unbounded conserved parameters across different classes. A single
global total-count head cannot be assumed to work across all such classes.

## Governing comparison

The strongest received Astra reference used here is N1612 at commit
db0969a8586afaa38137a4371b3457c5576fadea (1 November 2026): the completed whole
audit accepts all graphs in its specified reversible, square-free binary
one-port hub/arm architecture, with one acquired exponential moment. Its source
theorem's historical pending header is superseded by the scoped whole audit.
It does not assert arbitrary conservative-module stabilization. The earlier
cooperative theorem in this workspace is retained; no extra instance of it is
the objective here.

Ordinary references: Anderson–Craciun–Kurtz, [product-form theorem](https://arxiv.org/abs/0803.3042),
and Anderson–Cappelletti–Kim, [weakly reversible recurrence criteria](https://arxiv.org/abs/1904.08967).
The former disposes of the deficiency-zero control. The latter's binary and
single-linkage sufficient conditions do not by themselves give the universal
reservoir assertion. Resolvents, embedded chains and Foster drift are ordinary
Markov-chain machinery; no historical novelty is claimed for those operations.
