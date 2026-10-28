# Finite sparse acquisition of an approximate complete intervention law

28 October 2026. Scoped construction for the positive quadratic-form source
class. It converts the prior ideal-information result into a finite,
bounded-error acquisition protocol. No individual bright or dark coupling
is divided by. Interpolation and inverse polynomial approximation are
conventional tools; no novelty or superiority claim is made.

## Governing sources and physical premises

Read directly: `p1_next/theory/UNNORMALIZED_REPRESENTATION.md`, sections
1--5 and 7, and `p1_next/theory/DARK_INTERVENTION_ORDER.md`, sections 1--6.
They establish, for `u>=0`, `sum u_i<=delta`,

    J(u)=c0+g^T P(I+PBP)^(-1)Pg,
    P=diag(sqrt(u)), B>=0, c0>0.

Assume warranted bounds `max |g_i|<=G`, `max B_ii<=kappa`, and write
`q=delta*kappa`. The native calibrated reaction is `R=r0+J`. We interpolate
R directly; a shared additive constant is reproduced exactly. Converting
R to J requires the corresponding offset calibration/enclosure. The source
class, controls, dose, receiver stability, calibration and reset are physical
premises, not consequences of fit quality. Arbitrary PSD Gram realizability
does not establish realization by an arbitrary restricted apparatus.

## 1. Finite nodes and an acquired representation

Fix integer k>=1 and barycentric coordinates

    lambda_0=1-sum_i u_i/delta, lambda_i=u_i/delta, i=1,...,n.

For every nonnegative integer vector alpha of length n+1 and sum k, acquire
one reaction at `u_alpha=(delta/k)(alpha_1,...,alpha_n)`. There are
`M=binom(n+k,k)` nodes, each with at most k active physical controls. Alpha_0
represents unused dose. The zero source node is included once.

Let the acquired report satisfy
`|y_alpha-R(u_alpha)|<=epsilon_alpha`, including actual actuation and
calibrated receiver error. Define falling-factorial binomials, with
`binom(t,0)=1`, and

    L_alpha(u)=product_(i=0)^n binom(k lambda_i,alpha_i),
    Rhat_k(u)=sum_alpha L_alpha(u)y_alpha.             (1)

At node beta, any alpha!=beta has some alpha_i>beta_i, making its integer
binomial factor zero; for alpha=beta every factor is one. The M cardinal
polynomials have total degree at most k. Since M is the dimension of this
polynomial space, the nodes are unisolvent and the basis reproduces every
degree-k polynomial. In particular `sum L_alpha=1`.

Equation (1) is an acquired whole-law representation whose coefficients are
the acquired reports. It assumes no hidden Taylor coefficients, g, B,
nonzero-coupling threshold or low rank.

## 2. Dimension-independent noise amplification

For every n and every point in the simplex,

    Lambda(u):=sum_alpha |L_alpha(u)|
        <=C_k:=binom(2k-1,k).                        (2)

For t>=0, `|binom(t,j)|<=t(t+1)...(t+j-1)/j!`. The right side has generating
function `(1-z)^(-t)`. Apply this coefficientwise with `t_i=k lambda_i`
and `sum t_i=k`: the coefficient of z^k in their product is the coefficient
in `(1-z)^(-k)`, namely C_k. This proves (2).

This constant is sharp over all dimensions for this lattice. At the
barycenter in N=n+1 dimensions, t_i=k/N and, for fixed j>=1,
`|binom(k/N,j)|=k/(Nj)+O(N^-2)`. Consequently the coefficient through degree k
in `[sum_j |binom(k/N,j)|z^j]^N` tends to the corresponding coefficient of
`exp(k sum_(j>=1) z^j/j)=(1-z)^(-k)`. Thus Lambda tends to C_k. Independent
adversarial errors matching the signs of L attain `epsilon Lambda(u)`.
This is conditioning of this rule, not an all-algorithm information bound.

The noise radius at u is `sum |L_alpha(u)|epsilon_alpha`, bounded by
`C_k epsilon`, where epsilon is the maximum node radius. A truly shared
additive calibration error b contributes exactly b, since the weights sum
to one, and should not be multiplied by C_k. Joint gain/offset uncertainty
can likewise be retained. Independent interval propagation is conservative
when correlations are ignored; errors need not be stochastic or independent.

## 3. Taylor-comparator whole-law certificate

The prior theorem supplies an unknown degree-k T_k and one-sided remainder

    J(u)=T_k(u)+(-1)^k A_k(u),
    0<=A_k(u)<=E_k:=delta G^2 q^k/(1+q).             (3)

The finite identity holds for all q>=0. Interpolation reproduces T_k, so
using it as a proof comparator does not assume it was measured. At u,
the positive/negative Lagrange masses are `(Lambda+1)/2`, `(Lambda-1)/2`.
Interpolating numbers in [0,E_k] lies in
`[-(Lambda-1)E_k/2,(Lambda+1)E_k/2]`. Subtracting A_k(u) gives

    sup_u |R(u)-Rhat_k(u)|
      <=C_k epsilon+(C_k+1)E_k/2.                   (4)

The factor one-half uses the shared remainder sign. Actual-dose bounds at
nodes can tighten the interval further. Exactly dark g_i and singular B
are covered. C_k grows exponentially: fixed nonzero bounded error cannot
be suppressed indefinitely by increasing k. Even at zero noise this bound
has geometric decay only for 4q<1, up to polynomial factors. That limitation
belongs to this bound and does not show nonidentifiability at larger q.

## 4. Stronger spectral comparator without hidden coefficient access

For q>0, put `a=(2+q)/q` and let Tcheb denote first-kind Chebyshev polynomials.
Define

    r_k(x)=Tcheb_k((2x-q)/q)/Tcheb_k(-a),
    s_(k-1)(x)=(1-r_k(x))/(1+x).

Since r_k(-1)=1, s is a polynomial of degree at most k-1. For x in [0,q],

    |1/(1+x)-s_(k-1)(x)|<=1/Tcheb_k(a).              (5)

The difference is r_k(x)/(1+x); its numerator is at most 1/Tcheb_k(a) and
the denominator is at least one. Let z=Pg, K=PBP. Then `0<=K<=qI` and
`||z||^2<=delta G^2`, so

    H_k(u)=c0+z^T s_(k-1)(K)z,
    |J(u)-H_k(u)|<=F_k:=delta G^2/Tcheb_k(a).         (6)

The term z^T K^j z is `g^T U(BU)^j g`, of degree j+1; hence H_k has degree
at most k. Its coefficients need not be known. Polynomial reproduction and
the triangle inequality give a second acquired-law certificate,

    sup_u |R(u)-Rhat_k(u)|
      <=C_k epsilon+(C_k+1)F_k.                     (7)

Report the smaller of (4) and (7). For q=0 the law is affine and both model
biases are zero. Writing
`rho=(sqrt(1+q)-1)/(sqrt(1+q)+1)` yields
`1/Tcheb_k(a)=2rho^k/(1+rho^(2k))`. Thus the model-bias bound in (7)
decays geometrically if 4rho<1, equivalently q<16/9. This sufficient
condition is not necessary; fixed-noise amplification remains.

For delta=1/5, G=kappa=1, k=3: C_k=10, a=11, Tcheb_3(11)=5291. The
Taylor bias bound is `11/1500=0.007333333...`; the spectral bias bound is
`11/26455=0.000415800...`. At n=12 the cost is 455 source reactions.
The prior m=4 path twins agree at all these nodes yet differ at a dense
action by `16/49765969`; this is an approximate law, not exact source recovery.

Classical best absolute-error inverse polynomials can improve (6), and
optimized simplex nodes can improve conditioning. Both are available to
the equally informed conventional comparator. The displayed residual is
used because its proof is explicit and all coefficients are rational for
rational q.

## 5. Positive Bernstein alternative: noise gain one

Use the same acquired nodes with nonnegative multinomial weights

    W_alpha(u)=k!/product_i alpha_i! * product_i lambda_i^alpha_i,
    Bhat_k R(u)=sum_alpha W_alpha(u)y_alpha.

The weights sum to one. Bhat is a degree-k polynomial but does not
interpolate general node data. Its bounded-error noise gain is exactly one.
For the present source class,

    0<=J(u)-B_k J(u)<=C:=delta^2 kappa G^2/k.         (8)

**Proof avoiding a dimension penalty.** The governing constrained-energy
form is `J(u)=c0+min_y F_u(y)`, where
`F_u(y)=||y||^2+sum u_i(g_i+b_i^T y)^2` and `b_i^T b_j=B_ij`.
Let y_u be its minimizer and `r_i=g_i+b_i^T y_u`. Draw k independent
categorical indices with probabilities lambda_0,...,lambda_n, and set
`V=(delta/k)sum_l e_(I_l)`, where e_0=0. Then E V=u and
`B_k J(u)=E J(V)`. Concavity proves the lower inequality in (8).

The quadratic F_V has Hessian at least 2I. Completing the quadratic around
y_u gives

    F_V(y_u)-min_y F_V(y)
      <=||sum_i(V_i-u_i)b_i r_i||^2.

Taking expectations and using multinomial variance gives

    J(u)-B_kJ(u)
      <=(delta/k)sum_i u_i B_ii r_i^2
      <=(delta kappa/k)sum_i u_i r_i^2
      <=delta^2 kappa G^2/k.

The final step uses `sum u_i r_i^2<=F_u(y_u)<=F_u(0)<=delta G^2`.
This proof covers exactly dark couplings, singular B, and the finite-control
coercive Hilbert setting in the governing representation.

Consequently, for epsilon=max epsilon_alpha,

    Bhat_k R(u)-epsilon <=R(u)<=Bhat_k R(u)+epsilon+C. (9)

The midpoint has symmetric error at most epsilon+C/2. At a query, use the
sharper noise radius `sum W_alpha epsilon_alpha`. Intersect this interval
with (4)/(7) at no additional source cost. Errors are not assumed to average
away. Multinomial Monte Carlo can estimate this operator at one requested
action using fresh support-at-most-k interventions, but those are new paid
measurements with a separate sampling error. A random subset of nodes is
not an acquired complete reusable law.

## 6. Compliance tasks from the same record

Suppose the baseline supplies a warranted acquired lower bound c_lo>0 on
c0. For every acquired native interval `[R_lo,R_hi]`, intersect
`[R_lo-r0,R_hi-r0]` with the positive source constraint and invert to obtain
an interval for `-Z=-1/J`. No further physical reaction is needed.

The original Woodbury identity gives

    -Z(u)=-z0+h^T P(I+P A P)^(-1)Ph,
    z0=1/c0, h=g/c0, A=B+gg^T/c0>=0.

Therefore all the above acquisition/certification arguments apply to -Z
with

    G_Z=G/c_lo, kappa_Z=kappa+G^2/c_lo,
    q_Z=delta*kappa_Z.                              (10)

The negative constant -z0 is harmless: the proofs reproduce an arbitrary
constant exactly and all approximation/variance bounds concern the gain.
The actual unknown c0 must not be substituted for c_lo. Baseline uncertainty
is acquired, not removed by this transformation. Compliance-reduction-minus-
price differs from `-Z(u)-c^T u` by the same unknown baseline for every
action, which cancels in comparisons and regret. Error units for R and Z
are different; separate certified bounds must be reported.

## 7. Value-only global task certificates

First, the positive operator gives an immediate bound for any affine price:

    max_u [R(u)-c^T u]
      <=max_alpha [R_hi,alpha-c^T u_alpha]+C.        (11)

This follows because the Bernstein weights are nonnegative, sum to one,
and reproduce affine functions. Choose the node with the largest acquired
lower reward. Its all-continuous-simplex regret is at most `C+2epsilon`.
There is no gradient identification, unverified optimizer convergence or
unpaid source access. Equation (11) also applies to the -Z construction.

For a stronger certificate, transform the acquired polynomial p=Rhat_k to
Bernstein coefficients b_alpha of degree k. Then

    max_u [p(u)-c^T u] <=max_alpha[b_alpha-c^T u_alpha].

If `|R-p|<=E` uniformly, the true global upper bound is

    U=max_alpha[b_alpha-c^T u_alpha]+E.              (12)

For any legal candidate x with acquired or surrogate-based lower bound
`L<=R(x)-c^T x`, `max(0,U-L)` certifies its regret. The error sign in U is
**plus E**. One may intersect U with (11). A finite action menu is evaluated
without new reactions; future physical application still costs preparation.

### Exact transform using small face blocks

At a node whose nonzero barycentric support is S, only Bernstein coefficients
on subsets of S contribute. Solve first the vertex coefficients, then edge
interior coefficients, and then increasing face sizes. For a support of size
s, its interior block has order `binom(k-1,s-1)`, independent of n. All
lower-face coefficients are already known. Unisolvence and this block
triangular ordering prove each block is nonsingular. The transform uses only
acquired nodal reports, not hidden source coefficients. The saved exact
implementation `code/simplex_law.py` follows this construction and reports
its face-block counts.

### A finite offline optimization closure, with its actual cost

Let b denote the price-adjusted acquired coefficients. For an integer m>=k,
degree elevation gives

    b_beta^(m)=sum_(alpha<=beta,|alpha|=k)
        [product_i binom(beta_i,alpha_i)/binom(m,k)] b_alpha,
    |beta|=m.                                      (13)

The weights are nonnegative and sum to one. They are the counts of k samples
without replacement from a population of m labelled items, with beta_i
items of category i. In contrast, evaluating p at lambda=beta/m averages
b_alpha under k samples with replacement from that same population. Couple
the ordered samples until a repeated item occurs. The collision probability
is at most `k(k-1)/(2m)` by the union bound. For
`range(b)=max b-min b`, this proves

    |b_beta^(m)-p(beta/m)|
      <=range(b) k(k-1)/(2m).                       (14)

This is dimension-independent and depends only on acquired coefficients.
Take the best polynomial value over the degree-m offline lattice. Its true
continuous-simplex regret is at most

    2E+range(b) k(k-1)/(2m).                        (15)

Indeed (13) bounds the polynomial's continuous maximum by its largest
elevated coefficient, and (14) bounds that by the largest feasible lattice
value plus the displayed term. Add E for each true-versus-polynomial value.
The exact coefficient upper bound (12) after elevation can be sharper than
(15). No new physical data are acquired by degree elevation.

This closes finite value-only optimization in principle but does not assert
efficiency: it evaluates `binom(n+m,m)` offline nodes/coefficient locations,
which can be prohibitive. The coefficient range includes the specified
price. For k=1, the polynomial is affine and vertices already optimize it.
A future dense candidate has its own setting cost and DAC error. Evaluate
the lower-bound predictor at the actual deployable command, or add a
separate justified rounding loss; the acquisition support limit k does not
automatically apply to the future physical command.

## 8. Complete acquisition and use costs

The source count is `M=binom(n+k,k)`, plus calibration, drift checks and any
repeats actually required. Requested nonzero setting writes sum to
`n binom(n+k-1,k-1)`: count the nodes with alpha_i>=1 for each physical i.
Individually clearing each active setting pays the same number of reset
writes. Every source reaction pays preparation, settling, integration and
reset. The total ideal programmed dose is `M delta n/(n+1)` and the maximum
per-experiment dose is delta. No timing or energy is invented. Setting reuse
is possible but no credit is taken without a declared implementation.

For downward DAC step h, the actual node u_tilde remains legal and has
`||u_alpha-u_tilde||_1<=min(n,k)h`. From the governing derivative bound,

    ||grad R||_infinity<=L:=G^2(1+q)^2,

add `L||u_alpha-u_tilde||_1` to its calibrated interval (or the conservative
`L min(n,k)h`). ADC half-step, gain/offset uncertainty and warranted drift
are separate terms. Distinct requested nodes may even collapse on a coarse
DAC; the interval theorem remains correct, but its attained precision may
then be poor. Exact rational requested settings are not assumed to be
exactly applied.

Storing the nodal law costs O(M) coefficients. Direct evaluation costs
O(kM+nk) arithmetic with sparse indices/precomputed scalar binomials.
Coefficient transforms, task maxima, degree elevation or subdivision have
their own offline cost and are not hidden in the reaction count. The saved
checks use exact rationals. Floating implementations must enclose numerical
evaluation error. Calibration renewal and physical use/verification remain
paid, even when surrogate evaluation requires no fresh measurement.

## 9. Conventional comparators and limits

An equally informed conventional method can run exactly this interpolation,
calibration propagation, Bernstein transform and task certificate. The
construction closes a finite-acquisition gap in the prior theorem; it makes
no exclusive computational, photon or hardware advantage claim. Its main
capability is a reusable all-action approximation and task bound without
normalizing weak or dark couplings. It retains combinatorial acquisition,
degree-dependent conditioning, precision costs and physical source premises.

Primary sources checked for stronger conventional alternatives:

- Tobin Isaac, *Recursive, parameter-free, explicitly defined interpolation
  nodes for simplices*, arXiv:2002.09421v2 (2020),
  <https://arxiv.org/abs/2002.09421v2>. It provides recursive simplex nodes
  and the reference `recursivenodes` implementation. The implementation
  documentation and displayed recursive source were inspected at
  <https://tisaac.gitlab.io/recursivenodes/>. Such nodes are relevant
  competitors to the deliberately simple equispaced lattice.
- Gerlind Plonka and Manfred Tasche, *Fast computation of best approximation
  polynomials for the reciprocal function*, Numerical Algorithms (2026),
  <https://doi.org/10.1007/s11075-026-02364-1>. It provides classical
  absolute/relative minimax inverse polynomials and stable evaluation
  algorithms. The Chebyshev residual used here is established machinery.

The local source-class inequalities are proved above. Finite exact checks
support only their tested scope and are not an independent whole-proof audit.
No equipment operation, purchase, outreach or external write is involved.

## 10. Saved finite algebra checks

Run `python p1_dark_acquisition/code/simplex_law_checks.py`. The exact output
is saved in `theory/SIMPLEX_LAW_CHECKS.json`. The tested scopes are:

- 5,778 cardinal-matrix entries, 200 recovered Bernstein coefficients,
  75 polynomial evaluation equalities and 640 degree-elevation point bounds,
  over n=1,2,3 and k=1,...,5.
- 207 canonical source/node identities and 120 source query checks, including
  120 one-sided Bernstein bounds and 120 spectral-comparator bounds, over
  delta=1/5,1,2 and k=1,...,4. The delta=1 and 2 cases test the general
  mathematical theorem and are not claims under the prior device budget.
- 60 compliance representation identities and 9 acquired-law compliance
  intervals, using the declared lower bound c_lo=1/2 even when the synthetic
  source has larger c0.
- Four path-twin cases, k=1,...,4, whose complete degree-k lattice records
  agree and whose dense responses differ but remain enclosed by the law.
- Exact barycenter Lebesgue diagnostics for k=1,...,6 and increasing
  dimensions, consistent with the analytic sharp-in-dimension limit.

The count labels record actual tested cases. All pass criteria use rational
arithmetic; floating values are display diagnostics. The main calibrated
finite-setting acquisition run is separate and is not duplicated here.
