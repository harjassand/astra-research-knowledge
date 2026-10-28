# Positive determinant representation and factorial intervention tails

28 October 2026. Ordinary construction and proof, developed from the retained
unnormalized response theorem. This is a representation/precision theorem;
it does not acquire its coefficients from a finite noisy transcript for free.

## 1. Source contract and the obstruction removed

For a fixed affine-SPD rank-one source, retain

    J(u)=c0+F(u),
    F(u)=g^T P(I+PBP)^(-1)Pg,
    P=diag(sqrt(u)), B>=0, c0>0,
    u>=0, sum u_i<=delta,
    |g_i|<=G, B_ii<=kappa.

The acquired native reaction is R=r0+J. The scalar r0, calibration, fixed
source class, reset/settling, dose language, and bounds G,kappa remain
warranted physical inputs. Dark or arbitrarily weak g_i are permitted.

The preceding Neumann bound controls effects beyond intervention order k by
`delta G^2 q^k/(1+q)`, q=delta*kappa. That bound is useful when q<1, but
does not decay for q>=1. The positive determinant representation below gives
a factorial tail for every finite q, without dividing by g_i, identifying
latent poles, assuming low hidden rank, or using negative physical doses.

The auxiliary Poisson variables used in the proof are algebraic tools. They
are not a model of detector noise, photons, repeated trials, or physical
randomness, and establish no statistical/metrological advantage.

## 2. Two multiaffine polynomials with nonnegative coefficients

Define

    D(u)=det(I+B diag(u)),
    N(u)=det(I+(B+gg^T)diag(u))-D(u).

The determinant lemma gives the exact identity

    F(u)=N(u)/D(u).                                  (1)

For a subset S of controls, write u_S=product_(i in S) u_i. Expansion in
principal minors yields

    D(u)=sum_S d_S u_S, d_empty=1,
    N(u)=sum_(S nonempty) n_S u_S,
    d_S=det(B_SS)>=0,
    n_S=det(B_SS+g_S g_S^T)-det(B_SS)>=0.              (2)

Thus both polynomials are multiaffine, of degree at most n. The difference
of determinants in (2) is nonnegative because adding g_S g_S^T preserves
PSD order and determinant is monotone on the PSD cone. Equivalently,
`n_S=g_S^T adj(B_SS)g_S`, including singular B_SS by polynomial continuity.
The adjugate of a PSD matrix is PSD. Cauchy-Binet on augmented Gram factors
gives the same nonnegative coefficients as sums of squared minors.

Useful coefficient bounds, with s=|S|>=1, are

    0<=d_S<=kappa^s,
    0<=n_S<=s^2 G^2 kappa^(s-1).                     (3)

Hadamard proves the first. Every diagonal adjugate entry is at most
`kappa^(s-1)`; PSD then bounds each off-diagonal magnitude by that same
number. Summing `|g_i g_j|` proves the second. For kappa=0, interpret s=1
separately: n_{i}=g_i^2, while all coefficients of higher degree vanish.
These are bounding inequalities, not a statement that arbitrary coefficients
within the boxes are realizable by one PSD source.

## 3. A positive spectral counting identity

Fix any nonnegative u. Put

    K=PBP, x=Pg, L=||x||^2=sum_i u_i g_i^2,
    q_u=tr K=sum_i u_i B_ii<=delta*kappa.

Choose eigenvalues lambda_j>=0 of K and coordinates z_j of x in an
orthonormal eigenbasis. Scaling this fixed command by a formal scalar t gives

    D(tu)=product_j(1+t lambda_j),
    N(tu)=t sum_i z_i^2 product_(j!=i)(1+t lambda_j). (4)

This identity is valid also for zero eigenvalues and singular B. No
eigenvalues are supplied to an acquiring learner.

Define p_j=lambda_j/(1+lambda_j). Each normalized factor is

    (1+t lambda_j)/(1+lambda_j)=(1-p_j)+p_j t.

It is the probability generating polynomial of a Bernoulli variable with
success probability p_j. Its use merely names nonnegative polynomial
coefficients. The variables can be coupled explicitly as

    X_j=1{Y_j>=1}, Y_j independent Poisson(log(1+lambda_j)).

Then X_j has the required Bernoulli law and `sum X_j<=sum Y_j` pointwise.
The total Poisson parameter is

    sum_j log(1+lambda_j)=log D(u)<=sum_j lambda_j=q_u.

Consequently the sum of these Bernoulli variables is stochastically bounded
by a Poisson variable of parameter q_u. Dropping any factors preserves the
bound. Combining the factors of two sources gives parameter at most
`q_u+q'_u`.

**Important guard.** The argument does not claim domination by a Poisson
variable having parameter `sum p_j`. That stronger mean-matching assertion
is false in general. The correct coupling uses `log(1+lambda_j)`, and only
then bounds their sum by the trace.

Write

    T_k(q)=Pr{Poisson(q)>=k}
          =1-exp(-q) sum_(j=0)^(k-1) q^j/j!, k>=1,
    T_0(q)=1.                                       (5)

T_k is nondecreasing in q and nonincreasing in k. In particular T_k(0)=0
for k>=1.

## 4. Single-source rational truncation theorem

Let D_r and N_r retain the terms of (2) with total degree at most r. For
r>=0, D_r>=1. The ratio F_r=N_r/D_r is a globally defined nonnegative
rational function on the whole dose simplex. Define the rational function

    H_r(q)=[q^r/r!]/[sum_(j=0)^r q^j/j!], H_0(q)=1.

For q=0 and r>=1 set H_r(0)=0. The stronger one-sided conclusion is

    0<=F(u)-F_r(u)<=F(u) H_r(q_u)
                   <=L H_r(q_u)
                   <=delta G^2 H_r(delta*kappa).    (6a)

In particular, for r>=1,

    F_r(u)<=F(u)<=F_r(u)/(1-H_r(q_u)).               (6b)

There is also the convenient, slightly weaker Poisson-tail bound

    |F(u)-F_r(u)| <= L T_r(q_u)
                   <= delta G^2 T_r(delta*kappa).    (6)

If r>=n, the error is exactly zero.

### Proof of the stronger rational bound

Let e_j^(i) be the elementary symmetric polynomial of degree j in the
eigenvalues excluding lambda_i. Equation (4) gives

    D_r=(1+lambda_i) sum_(j=0)^(r-1)e_j^(i)+e_r^(i).

Therefore the following error identity is exact:

    F-F_r=sum_i [z_i^2/(1+lambda_i)] e_r^(i)/D_r.    (6c)

It proves the error is nonnegative. For any nonnegative eigenvalue list of
sum at most q_u,

    (j+1)e_(j+1)<=q_u e_j.

Indeed, expand e_j and sum the as-yet-unused eigenvalues over each j-subset.
Every (j+1)-fold product is counted j+1 times, and the unused sum is at most
q_u. If e_r>0 and q_u>0, iteration yields

    e_j>=e_r r!/[j! q_u^(r-j)], 0<=j<=r.

Since D_r>=sum_(j=0)^r e_j^(i), it follows that

    e_r^(i)/D_r<=H_r(q_u).

Zero cases follow directly. The weights in (6c) sum to F<=L. Finally H_r
is nondecreasing in q: its reciprocal is a sum of nonpositive powers of q
with positive coefficients. This proves (6a), and rearrangement proves
(6b). This proof and its computed bound require only rational arithmetic
when the source specifications are rational.

### Independent derivation of the Poisson-tail bound

Write D=D_r+D_tail and N=N_r+N_tail. Equation (4) gives

    D_tail/D = Pr{sum_j X_j>=r+1},
    N_tail/D = sum_i [z_i^2/(1+lambda_i)]
                         Pr{sum_(j!=i) X_j>=r}.     (7)

The weights in the second line sum to F<=L. Therefore

    D_tail/D <= T_(r+1)(q_u),
    N_tail/D <= F T_r(q_u) <= L T_r(q_u).            (8)

Also F_r<=L. To see this directly, expand (4) by degree. With e_j denoting
elementary symmetric polynomials in the eigenvalues,

    N_r=sum_i z_i^2 sum_(j=0)^(r-1) e_j(lambda without i)
        <=L sum_(j=0)^(r-1)e_j(lambda)
        <=L D_r.

For r=0 the assertion follows from N_0=0. Finally,

    F-F_r = N_tail/D - F_r D_tail/D.                 (9)

The two terms on the right are nonnegative before subtraction. The absolute
value of their difference is at most their maximum, not their sum. Equations
(8)-(9), `F_r<=L`, and `T_(r+1)<=T_r` prove (6).

This bound approximates an entire multivariate response law. It is not just
an approximation on one fixed ray: the same coefficient truncation D_r,N_r
works simultaneously for every nonnegative u in the simplex.

### Sharpness for this truncation, not for every possible representation

Fix q>0, delta>0 and G>0. For n>r, take

    u=(delta/n) 1, g=G 1,
    B=[q n/(delta(n-1))](I-11^T/n).

This is PSD with diagonal kappa=q/delta. The matrix K has eigenvalue zero
in direction x and eigenvalue q/(n-1) with multiplicity n-1. Thus
`F=L=delta G^2`, while

    (F-F_r)/L = [binom(n-1,r)(q/(n-1))^r]
                /[sum_(j=0)^r binom(n-1,j)(q/(n-1))^j].

As n tends to infinity at fixed r,q, this converges to H_r(q). Consequently
the coefficient in (6a) cannot be uniformly reduced for this particular
determinant truncation using only L and q. This does not lower-bound the
error of every alternative rational approximation or acquisition algorithm.

## 5. Stronger all-sparse-record indistinguishability bound

Let two sources satisfy the same G,kappa,delta bounds and agree exactly on
every command of support size at most k, k>=1. Equality at zero gives the
same c0. Then, for every later allowed command,

    |J(u)-J'(u)|
       <=max(F(u),F'(u)) T_k(q_u+q'_u)
       <=delta G^2 T_k(2 delta*kappa).              (10)

The first expression is a mathematical sharpening; the unknown values
F,F',q_u,q'_u are not handed to the learner. The last expression is the
uniform bound from supplied specifications.

### Proof of support cancellation

Let A=N D' and C=N' D. They have nonnegative coefficients and total degree
at most 2n; each coordinate has degree at most two. Since D,D'>=1,

    J-J'=(A-C)/(D D').                              (11)

On every face with at most k active controls, A-C vanishes identically on a
positive open subset of that face. Every polynomial coefficient whose
support has size at most k must therefore vanish. The corresponding
coefficients of A and C agree.

Let A_high and C_high retain only monomials whose support has size greater
than k. Then A-C=A_high-C_high and, at nonnegative u,

    |A-C|<=max(A_high,C_high).                       (12)

Such monomials have total degree at least k+1. Therefore A_high is at most
the total-degree tail of N(tu)D'(tu) above degree k, evaluated at t=1.
Normalize that generating polynomial by D(u)D'(u). Equation (4) expresses
it as

    t sum_i [z_i^2/(1+lambda_i)]
       product_(j!=i)[(1-p_j)+p_j t]
       product_l[(1-p'_l)+p'_l t].                  (13)

The leading t uses one degree. Thus its tail above degree k is bounded by
`F T_k(q_u+q'_u)` using the explicit Poisson coupling of Section 3. Swapping
the sources bounds C_high analogously by `F' T_k(q_u+q'_u)`. Equations
(11)-(13) prove (10).

No finite set of noisy sparse readings supplies the exact face equality
premise. The arbitrary-order dark path pair remains a valid lower-bound
example: its first differing full-support response is nonzero at order
delta^(k+1). The new upper bound has the same fixed-k small-dose power,
but still does not establish matching constants as k or dimension grows.

## 6. Safe computable bounds and comparison with the earlier theorem

For fixed q and k tending to infinity, T_k(q) has factorial decay. Whenever
k+1>q,

    T_k(q)<=min(1,exp(-q) [q^k/k!]/[1-q/(k+1)])
           <=min(1,[q^k/k!]/[1-q/(k+1)]).            (14)

Review correction (28 October 2026): the probability cap by one must be
applied to the exponential majorant before the second inequality. The
uncapped intermediate quantity exceeds one, for example at q=9/2, k=4.
This corrects the displayed chain only; the final rational bound is unchanged.

The final expression is rational for rational q. For a sharper exact
arithmetic enclosure, bound exp(q) by a positive Taylor sum and its
geometrically bounded remaining tail, invert its positive endpoints, and
use (5). The executable checks use rational lower and upper enclosures;
no floating eigenvalues or numerical exponential decides a pass.

The rational single-source factor satisfies H_r(q)<=T_r(q). For a Poisson
variable Y, H_r(q)=Pr(Y=r)/Pr(Y<=r); and
`Pr(Y<=r)Pr(Y>=r)-Pr(Y=r)=Pr(Y<r)Pr(Y>r)>=0`.

For q<1, retain both bounds and take their minimum:

    |J-J'|<=delta G^2 min(q^k/(1+q), T_k(2q)).        (15)

The older Neumann bound can be better at small k. The determinant bound
eventually improves it, and continues to decay with k for every finite q.
For q=0, first-order data already determine the full law. Nothing here
removes the scale warrant: without a finite kappa, the earlier raw-response
saturation obstruction still prevents a scale-uniform finite-query result.

## 7. Implication for acquisition, without assuming its success

For a chosen degree r, store positive coefficients of D_r,N_r. Equation (6)
or the sharper (6a) provides a uniform or actual-dose truncation allowance E_r.
Subtracting a
shared calibrated baseline from each raw R reading gives an interval
`F(u_j) in [ell_j,h_j]`. Hence the true truncated coefficients obey

    (ell_j-E_r(u_j)) D_r(u_j) <= N_r(u_j)
                          <= h_j D_r(u_j).           (16)

The one-sided upper endpoint follows from F_r<=F. For r>=1, the relative
bound (6b) additionally gives the linear lower constraint

    [1-H_r(kappa sum_i u_ji)] max(0,ell_j) D_r(u_j)
                                                     <=N_r(u_j).

This particular relative constraint needs the kappa warrant but does not
divide by any measured weak response or require a positive lower g_i.

These constraints are linear in the unknown coefficient arrays. Together
with the boxes (3), `d_empty=1`, and `n_empty=0`, they give a bounded
polyhedral outer family containing the true truncated ratio. PSD/common-Gram
relations have been relaxed; a feasible coefficient vector need not itself
be a physical source. At any future u, minimizing/maximizing N_r(u)/D_r(u)
over this polytope is a linear-fractional program, reducible to an LP because
D_r(u)>=1. Add E_r(u) to the upper response endpoint only, then add the
baseline c0 interval, to obtain a sound response interval. Equation (6b)
can also bound the upper endpoint multiplicatively. A verified LP dual or outward arithmetic is
needed before treating a numerical solver output as a certificate.

There are `sum_(j=0)^r binom(n,j)` monomials per retained polynomial. This can
be expensive, despite being independent of microscopic source dimension.
The theorem supplies no promise that a few selected reactions make the
polytope narrow, no free acquisition of coefficients, and no convergence
claim for an adaptive query policy. Full-law acquisition and its complete
measurement/actuation/arithmetic cost remain separate work. An equally
informed conventional positive-rational/set-membership method can use the
same representation, bounds and LP; no superiority claim is made.

## 8. Prior machinery and status

Positive determinant generating functions and spectral Bernoulli cardinality
identities are classical; see Kulesza and Taskar, *Determinantal Point
Processes for Machine Learning*, Section 2, arXiv:1207.6083. Conductance
ratios of positive tree-generating polynomials are also classical; see
Brylawski, *A Determinantal Identity for Resistive Networks* (1977),
doi:10.1137/0132036. The present derivation applies these identities to the
specific unnormalized intervention law, coefficient truncation, and
all-sparse-record precision question. Historical novelty is not established.

The proof should be challenged at its actual source/model assumptions.
Finite exact examples support only their checked scope; they are not an
independent audit of every governing proof or an acquired physical contract.

The companion `inference_determinant_tail_checks.py` and saved results check
coefficient positivity, native-source identities, both truncation bounds,
the relative enclosure, sparse sign twins, and the invalid mean-matched
Poisson shortcut. Spectral aggregate fixtures additionally exercise growing
rank and the sharpness construction. These are finite exact checks, not a
finite-noisy acquisition implementation.
