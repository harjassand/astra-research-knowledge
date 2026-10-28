# Simultaneous intervention order and the precision of a retained response law

28 October 2026. This extends the dark-channel example to every finite
intervention order and gives a complementary finite-accuracy boundary.
The source class and total physical dose language are exactly those of
`UNNORMALIZED_REPRESENTATION.md`.

## 1. Representation and actual experiment order

For c0>0, g in R^n and B positive semidefinite, the response is

    J(u)=c0+g^T P(I+PBP)^(-1)Pg,
    P=diag(sqrt(u)), u>=0, sum_i u_i<=delta.

The native scalar reaction is `R(u)=r0+J(u)` for a calibrated known r0.
Thus two J values differ by exactly the same amount as their raw R values.

An experiment has order at most k when the **complete actual command** u
has at most k nonzero coordinates. A dense shifted reference counts as part
of that command. Adding one new control on top of a dense active reference
is not an order-one experiment in this definition. Source resets, full
settings, actuation, settling, readout and return precision remain charged.

## 2. Every finite order misses some joint intervention

Fix k>=1, let m=k+1, and take n=m. Choose d>2a>0 and c0=1. Set

    g=e1+em,
    B_plus=dI+a A_path,

where A_path is the adjacency matrix of the path 1--2--...--m. B_minus
is identical except that the final off-diagonal pair (m-1,m),(m,m-1)
has value -a instead of +a. Both matrices are strictly positive definite:
Gershgorin gives a uniform lower eigenvalue bound d-2a>0. Their diagonals
are identically d. They are legal Schur families, with the canonical positive
source realization supplied by the unnormalized theorem.

**All lower-order responses agree.** For every proper support S subset of
{1,...,m}, and for every nonnegative command supported on S,

    J_plus(u)=J_minus(u).                              (1)

To prove this, restrict to S: zero command coordinates have no influence in
the P representation. The induced path is a forest of disjoint path segments.
Since S is proper, no component contains both bright endpoints 1 and m.
Two signings of a tree are related by a diagonal sign gauge. The free global
sign on each component can be chosen to fix its unique bright endpoint, if
it has one. Therefore a diagonal sign matrix D_S satisfies

    B_minus[S,S]=D_S B_plus[S,S] D_S,
    D_S g[S]=g[S].

It commutes with P[S,S], so (1) follows. The proof covers every amplitude,
not just a finite rational design. In particular infinitely many exact,
adaptive k-sparse experiments cannot identify the all-action response law.
For n>m, inactive independent controls can be appended without changing the
obstruction.

The zero entries of g in the path interior are essential to this construction.
It does not refute pair acquisition theorems under additional nonzero-coupling,
sign, landmark or effective shifted-reference premises. A shift can supply
the missing higher-order operation, but its complete physical dose/support
must be counted.

## 3. Exact full-support separation

Choose the full command u=t*1 with t=delta/m. Define

    D_m=det(I+t B_plus)=det(I+t B_minus)>0.

The determinants agree because the full signings are diagonally gauge-related.
They can be evaluated without numerical eigenvalues using

    D_0=1, D_1=1+dt,
    D_j=(1+dt)D_(j-1)-(at)^2 D_(j-2), j>=2.           (2)

The (1,m) inverse entry of the tridiagonal positive-sign matrix is

    [(I+t B_plus)^(-1)]_(1m)
        =(-1)^(m-1)(at)^(m-1)/D_m.                   (3)

The last-edge sign change leaves the two endpoint diagonal inverse entries
unchanged and reverses their cross entry. Because g has one at both endpoints,

    J_plus(t1)-J_minus(t1)
       =4(-1)^(m-1) a^(m-1)t^m/D_m.                 (4)

This is nonzero for every m and every positive dose. The same expression is
the raw R difference; no reciprocal conversion or unknown hidden field is
being substituted for the measured reaction.

### A concrete finite decision

Let J_low and J_high be the smaller and larger full-command responses. Set
the joint-action cost to

    C=(J_low+J_high)/2-c0.

The action menu contains zero intervention, with net improvement zero, and
the full command, with net improvement `J_full-c0-C`. The latter is
`-Delta_m/2` or `+Delta_m/2`, where

    Delta_m=4 a^(m-1)(delta/m)^m/D_m.

The two indistinguishable lower-order sources require opposite choices.
Any deterministic choice based only on the old record therefore has regret
Delta_m/2 on one source. A single additional full-support raw reading
distinguishes this two-source family whenever `2 eta<Delta_m`, where eta
is its absolute raw error. Comparing a reported interval directly with the
raw midpoint threshold succeeds for **every** allowed error whenever
`4 eta<Delta_m`. The saved tests take eta=Delta_m/8 and exercise the worst
errors toward the threshold.

These are precise one-extra-query statements for the displayed two-source,
two-action ambiguity. They do not assert one-query recovery of the full
source or a physical error budget that has actually been attained.

## 4. The small-dose exponent is the first unseen order

For this positive B source, all eigenvalues of I+tB are >=1, so D_m>=1.
Hadamard's determinant inequality also gives D_m<=(1+dt)^m. Consequently

    4 a^k [delta/(k+1)]^(k+1)/(1+d delta/(k+1))^(k+1)
       <= Delta_(k+1)
       <=4 a^k [delta/(k+1)]^(k+1).                  (5)

For each fixed k, the hidden full-action difference is of order
delta^(k+1) as delta tends to zero. The constants depend strongly on k.
This is not a matching theorem in k or in dimension, and it does not claim
that high-order effects remain easily measurable at a fixed total dose.

## 5. Uniform upper bound from positivity and total dose

Now consider any two sources with the same number of controls satisfying

    B,B'>=0, max_i B_ii,max_i B'_ii<=kappa,
    max_i |g_i|,max_i |g'_i|<=G,
    u>=0, sum_i u_i<=delta.

Suppose their exact responses agree for **every** command of support size
at most k, with k>=1. This includes equality at zero, so c0=c0'. Let
q=delta*kappa. For q<1,

    sup_u |J(u)-J'(u)|
       <= delta G^2 q^k/(1+q).                       (6)

The finite identity below remains valid without q<1, but then this upper
bound need not decrease with k. There is no factor two in (6): positivity
puts the two remainders on the same side of their common Taylor polynomial.

### Proof of the common polynomial

Although P contains square roots, J is analytic near u=0 through

    J(u)=c0+g^T U(I+BU)^(-1)g.

Its polynomial through total degree k is

    T_k(u)=c0+sum_(j=0)^(k-1) (-1)^j g^T U(BU)^j g. (7)

The jth displayed term has total degree j+1. Every monomial of degree <=k
has support size <=k. On the coordinate face given by that support, the two
response functions agree on a positive open set, and their analytic Taylor
coefficients at zero consequently agree. Therefore the two T_k polynomials
are identical. This argument uses only physical nonnegative data; analytic
extension near zero is a proof device, not a negative-dose operation.

### One-sided remainder and the factor-one improvement

Let x=Pg and K=PBP>=0. The exact finite inverse expansion is

    (I+K)^(-1)=sum_(j=0)^(k-1)(-K)^j
                    +(-1)^k K^k(I+K)^(-1).

Thus

    J(u)-T_k(u)=(-1)^k A_k(u),
    A_k=x^T K^k(I+K)^(-1)x>=0.                       (8)

The trace bound gives `||K||<=tr K<=kappa sum u_i<=q` and
`||x||^2<=G^2 sum u_i<=delta G^2`. For k>=1, the scalar function
`lambda^k/(1+lambda)` is increasing on lambda>=0. Functional calculus gives

    0<=A_k(u)<=delta G^2 q^k/(1+q)=E_k.              (9)

The same bound holds for the second source and both use the same parity.
If k is even, both J and J' lie in `[T_k,T_k+E_k]`; if k is odd, both lie
in `[T_k-E_k,T_k]`. Their difference is at most E_k, proving (6).

The actual-dose refinement replaces delta by t=sum u_i and q by t*kappa.
If kappa=0 then both B matrices vanish and first-order data already determine
every response, consistent with the zero right-hand side for k>=1.

## 6. What this precision boundary does and does not acquire

For each fixed k, (5) and (6) have the same small-dose power delta^(k+1).
This links simultaneous intervention order to the precision demanded of a
complete law. Under q<1, sufficiently high-order ambiguity is uniformly small;
to make the ideal-information bound <=epsilon it suffices that

    k >= log[delta G^2/((1+q)epsilon)] / log(1/q),

with k>=1 and the integer ceiling understood. This is a statement about what
an exact complete k-sparse record can distinguish, or about a genuinely
acquired common polynomial with its coefficients certified.

It is **not** a finite-sample acquisition algorithm. A finite noisy set of
responses does not give derivatives or T_k for free. Higher differences can
be badly conditioned, the number of mixed coefficients can grow rapidly,
and the raw precision needed to expose (4) decreases quickly with m. Any
finite procedure must pay its calibration, scalar readouts, per-action dose,
number of actuators active and written, reset/settling time, arithmetic and
future use. Finite-noise compatibility must retain coefficient uncertainty
in addition to the remainder (9). A rank or polynomial-order threshold is
not an exact source-class certificate.

The conventional comparator receives exactly the same sparse or full-support
interventions, raw readings, priors and precision. No classical estimator can
distinguish the exact sparse twins. A conventional solver can also use the
same positivity/Neumann envelope and the same distinguishing full-support
query. The result supplies a representation-level information boundary, not
exclusive computational, photon or hardware superiority.

## 7. Exact tests and source realization

`dark_intervention_order_checks.py` uses d=1, a=1/4, delta=1/5 and m=2,...,8.
For each path signing it constructs a rational Gram factor: one feature per
edge with entries +/-1/2 at its endpoints, plus `4-degree(i)` private
features of value 1/2 at each node. Every diagonal is exactly one and every
path cross entry is the desired +/-1/4. There are 3m+1 latent coordinates;
adding the port gives a canonical Q0=I source of dimension 3m+2.

The tests check the Gram factors, the complete canonical source on the full
command, the determinant/cofactor formula, all proper supports at two legal
amplitude patterns, the common degree-k polynomial, the signed remainder
and the factor-one upper bound. They save exact raw reactions, thresholds,
precision requirements and cases. The all-amplitude and all-k claims rest on
the proofs; the finite checks do not promote themselves to a general audit.

### Check-count correction

The 140 seeded random remainder cases allow zero coordinates. They contain
107 full-support and 33 proper-support commands. Together with the seven
designated full-support commands, there are 147 remainder checks, of which
114 have full support. The earlier saved metadata label incorrectly called
all 140 random cases full-support. The code and saved JSON now count the
actual supports. The tested commands, pass conditions and theorems are
unchanged.
