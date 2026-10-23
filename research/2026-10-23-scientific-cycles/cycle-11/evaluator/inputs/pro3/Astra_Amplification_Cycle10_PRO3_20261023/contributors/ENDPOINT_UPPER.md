# Critical endpoint upper under fixed positive discrepancy

Bounded contribution by `/root/cycle10_endpoint_upper`, Astra PRO3 Cycle10.
Scientific date: 23 October 2026, Australia/Brisbane.

This note proves a new endpoint upper and its one-information-budget
allocation. It does not claim native attainability of the transport
prefactor or resolve the possible discrete-depth effect. The accepted
Cycle9 logarithmic theorem is not reproved.

## 1. Exact scope and source bindings

Use precisely the finite native class in Cycle9: positive probability
vectors pi,q on a finite labelled space, D(pi||q)<=K with fixed K>0;
alpha in (0,1), beta=1-alpha; q initialization; fixed target-independent
row-stochastic Q with reciprocal off-diagonal support and actual log
asymmetry <= public A_n. The public powers satisfy 0<eta_n<1,
kappa_n>=0 and remain fixed within each run. The actual factorized
Hastings acceptance, completing rejection diagonal and
C=(I+alpha G+beta L)/2 are unchanged. All returns count. Support can grow.

The main finite dependency is `SHARP_DISTORTION_RATE.md`, Sections 2--5,
26,911 bytes, SHA256
`5f76de8b2e7567cadae8ae06d272de8e1bdbae1e6e29ddf1a34800f090e5ce2f`.
It reproduces the exact accepted finite operation from Cycle8
`ASYMMETRY_BUDGET_THEOREM.md`, 28,265 bytes, SHA256
`eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1`.
The source copies were read, and these identities checked. No source was
modified and no old scientific suite was run.

Set

    ell=log n, L=log ell, u=eta_n ell,
    r=alpha exp(-K)/beta,
    c0=c(d)=inf_{a>=0} log(1+r exp(a))/(d+a).

Fix d>0 with c0<1. Assume the exact public discrepancy D_n=d and

    c0 u = L+s+o(1)

for a fixed real s. This includes all d>=d_*=(1+r)log(1+r)/r, equality
included, and the interior branch with c(d)<1. It excludes the separate
c(d)=1 regime. No limit of A_n or mismatch sign is required.

Let b_max=1-exp(-K), and let R_n denote the original full-chain minimax TV.

**Theorem.** Under these assumptions,

    limsup (log n) R_n <= max{K, b_max exp(-s)}.                 (1)

Consequently, using the accepted Q=I information-tail lower,

    b_max exp(-s)<=K  ==>  (log n) R_n -> K.                   (2)

For larger transport amplitude, this note proves only an upper bound.
Even at d>d_* it does not infer a matching lower from the scalar envelope.

## 2. The inherited finite full-chain operation

For proof cutoffs choose

    h=ell^-2, R=n/ell^4, xi=ell^-2,
    N=ceil(8L/(alpha exp(-K))),
    M0=exp(2K+1), J0=2/[alpha(2(n-N)+1)].

All formulas below are for n sufficiently large that h<min(1/2,1/e),
log R>1 and N<n. Write W=pi/q,

    A={W<h}, b=q(A), k=-log(1-b), a=pi(W>R).

The finite-space positivity makes b<1. Empty A is allowed and gives zero
first-hit contribution. Choose theta=c0 eta_n and p=(1-theta)^-1. Eventually
theta<=1/4 and theta<=eta_n. Define

    tau=p(1-c0), U=exp(d c0 p),
    H_theta=sup_{0<z<=1}(U z^tau-z),
    Delta=[beta H_theta-alpha(1-b)]_+,
    Gamma(e)=1/2+2^(p-1)/2 (1+Delta+alpha e).

The true full-chain first-hit interface gives

    TV(q C^n,pi)
      <= a + sqrt((M0+R)J0)+xi+ebar+b rho^N
           + b^(1-theta) ebar^theta Gamma(ebar)^(N/p),         (3)

where

    rho=1-alpha(1-b)/2,
    ebar=min{1-b, a/R+(N+1)(M0/h+1)J0/xi^2}.

The proof process absorbs first hits and kills other exits without row
normalization. Equation (3) propagates first hits with the ORIGINAL C;
it retains every later return. It is not an alternative implementable
sampler or extra access to a normalized target.

The accepted binary information inequalities give

    a<=K/(log R-1),
    k<=(K+H2(h))/(1-h)=K+delta_h,
    delta_h=[K h+H2(h)]/(1-h),                              (4)

where H2 is binary entropy with natural logs. Thus

    1-b>=exp(-K-delta_h).

Define an explicit uniform first-hit set-size bound

    E_n=min{1, K/[R(log R-1)]+(N+1)(M0/h+1)J0/xi^2}.        (5)

Then ebar<=E_n and E_n=O(ell^6(L+1)/n), with constants depending only
on K,alpha. In particular E_n<1 eventually.

## 3. Endpoint control pays the accumulated multiplier

By the accepted scalar characterization of c(d),

    H_0:=sup_{0<z<=1}(exp(d c0) z^(1-c0)-z)=r.              (6)

The equality is legitimate because c0<1; it is the actual scalar maximum,
not substitution into a previously strict contraction estimate.

Here is an explicit finite perturbation bound. Put m=d c0 and

    C_H=2m exp(4m/3)+2 exp(m)/e.

For theta<=1/4, p-1<=2theta, U<=exp(4m/3), and

    |U-exp(m)|<=2m exp(4m/3) theta.

Since tau>=tau0:=1-c0>0 and
sup_{0<z<=1} z^tau0 |log z|=1/(e tau0), the mean value theorem gives

    sup_z |z^tau-z^tau0| <= 2theta/e.

Combining these bounds and taking suprema yields

    |H_theta-r| <= C_H theta.                              (7)

This argument includes d=d_*. At that joining point it does not require
a uniformly positive distance from the two scalar branches.

Equations (4) and (7) give

    Delta <= beta C_H theta + alpha exp(-K) delta_h.         (8)

The positive part may be nonzero. It must be paid, not suppressed. For
theta<=1/4, 2^(p-1)<=2 and 2^(p-1)-1<=4theta log 2, so

    log Gamma(e)
       <= (2 log 2+beta C_H)theta
              +alpha exp(-K)delta_h+alpha e.               (9)

Put C_Gamma=2 log 2+beta C_H and define the nonnegative explicit error

    epsilon_n = theta [log(n E_n)]_+
             + N[C_Gamma theta+alpha exp(-K)delta_h+alpha E_n]. (10)

Using ebar<=E_n in the first-hit term of (3), and N/p<=N, gives the finite
endpoint inequality

    b^(1-theta) ebar^theta Gamma(ebar)^(N/p)
          <= b^(1-theta) exp(-c0 u+epsilon_n).              (11)

At the assumed critical scale,

    theta=(L+s+o(1))/ell,
    N=O(L), delta_h=O(L/ell^2),

and consequently epsilon_n=O(L^2/ell)+o(1)->0. In particular the whole
accumulated multiplier has been controlled. The false implication
Gamma->1 => Gamma^N->1 is not used.

For completeness, put

    rho_max=1-alpha exp(-K-delta_h)/2,
    B_n=sqrt((M0+R)J0)+xi+E_n+rho_max^N.

Then B_n=O(ell^-2) uniformly over the admitted class, and (3),(11) give
the concrete finite upper

    TV(q C^n,pi)
       <= a+B_n+b^(1-theta) exp(-c0 u+epsilon_n).            (12)

Moreover sup_{0<=b<=1}|b^(1-theta)-b|<=2theta/e, by the mean value theorem
in the exponent. Hence the endpoint first-hit contribution multiplied by
ell is at most b exp(-s)+o(1), uniformly in b. Alone, (12) would only
suggest a sum of two budgets. The next step is necessary to obtain MAX.

## 4. A single three-cell information allocation

Let T={W>R}; A and T are disjoint. Write

    t=pi(A)<=h, a=pi(T), e=q(T)<=a/R,
    c=1-t-a, q_rest=1-b-e.

Log-sum on these three cells and positivity give

    K >= t log(t/b)+a log(a/e)+c log(c/q_rest).

The convention at zero cell mass is by continuity. Since t<=h<1/e,

    t log(t/b)>=t log t>=-h log(1/h).

Also a log(a/e)>=a log R, and q_rest<=1-b, so

    c log(c/q_rest)>=c log c+c k>=-(a+t)+(1-a-t)k.

The last inequality uses (1-x)log(1-x)>=-x for x in [0,1]. Rearranging,

    k+a log R <= K+(a+h)(k+1)+h log(1/h).                  (13)

This is one KL allocation, not addition of independent binary estimates.
Using (4), log R=ell-4L and the upper bound for a in (4) gives the explicit
uniform consequence

    k+ell a <= K+delta_joint,n,                            (14)

    delta_joint,n = (h+K/(ell-4L-1))(K+delta_h+1)
                 +h log(1/h)+4K L/(ell-4L-1) ->0.

Thus an instance whose low-W mass spends essentially all K cannot also
carry a leading high-W information tail.

## 5. The exact MAX argument

Take any sequence of admitted instances. Since 0<=k<=K+o(1), every
subsequence contains a further subsequence with k->k_infty in [0,K].

If k_infty=K, (14) implies ell a->0. Then (12), epsilon_n->0,
ell B_n->0 and b->b_max yield

    limsup ell TV(q C^n,pi) <= b_max exp(-s).               (15)

If k_infty<K, define r_infty=alpha exp(-k_infty)/beta>r.
Because c0<1, continuity of

    H_d(c)=sup_z(exp(dc)z^(1-c)-z)

allows a fixed c' with c0<c'<1 and H_d(c')<r_infty. Reapply the SAME
finite certificate with theta'=c' eta_n. For large n the actual positive
part is zero, since H_theta'->H_d(c') and alpha(1-b)/beta->r_infty.
Its accumulated multiplier tends to one as before. Consequently,

    ell * first_hit_term
        <= exp[L-c'u+o(1)] ->0,

because u=(L+s+o(1))/c0 and c'/c0>1. Equation (14) now implies the
stronger subsequential statement

    limsup ell TV(q C^n,pi) <= K-k_infty <= K.              (16)

Equations (15)-(16) exhaust all subsequences. To pass to the class
supremum, for each n choose an admitted instance within ell^-2 of R_n;
such approximate maximizers exist by the definition of supremum. The same
subsequence argument applies and proves (1). No attainment of the finite
supremum is assumed.

The accepted Q=I two-state information-tail lower lies in every public
policy class and gives liminf ell R_n>=K. It combines with (1) to give
(2), including equality b_max exp(-s)=K.

## 6. What remains open, and why this bound does not decide it

For d>d_*, c0=log(1+r)/d. The upper's transport term is b_max exp(-s).
An actual pure path may pay an O(1) excess in capture cost from integer
depth or final attenuation. Exponential L^p energy at the endpoint gives
no assertion that this excess is avoidable, or that it is unavoidable for
all native geometries. In particular:

- A path lower below this upper does not prove a minimax phase oscillation.
- The endpoint upper is valid even if heterogeneous native geometry can
  fill the apparent path loss.
- A scalar one-step extremizer is not a reachable retained-mass proof.
- The inherited three-cell inequality supplies the correct information
  accounting but does not optimize the actual transport geometry.

An interior-minimizer lower may remove rounding by adjusting attenuation
slightly at each horizon; that is a separate native construction obligation.
No lower or amplitude claim beyond (2) is made in this contribution.

## 7. Scientific and resource boundary

The theorem concerns exact-real original-chain TV under the stated native
contract. It does not grant the sampler a normalizer, full table, KL
estimator, free reverse-Q evaluation, index oracle or absorbed simulator.
An arbitrary huge support or tiny atom retains its actual preparation,
proposal, target-evaluation, caching and precision costs. Ordinary IMH
retains its minimax amplitude K and the inherited favorable same-input
comparison. This upper is a robustness result, not an implementation gain.

No numerical jobs, new fixtures or old-suite replays were performed for
this contribution. Local reads, writes and hashes are provenance work.
Inference, design and total discovery costs are unknown. Historical
originality, external acceptance and formal verification are unestablished.
Principal integration and acceptance are separate from this bounded note.
