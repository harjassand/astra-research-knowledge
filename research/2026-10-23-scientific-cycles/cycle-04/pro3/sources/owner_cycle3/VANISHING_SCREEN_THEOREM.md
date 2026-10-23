# Uniform robustness when a fixed screen vanishes across runs

Owner: Astra PRO3. Scientific date: 22 October 2026, Australia/Brisbane.
Status: new owner construction; the uniform upper proof passed an independent
source-bound internal challenge, and the principal accepted the independently
constructed lower proof after direct inspection. Historical originality and external acceptance are not
asserted. This file supersedes the future question in the unchanged Cycle2
source. It does not revise the old safe-local theorem.

## 1. Question, information contract and results

For every finite labelled space let pi,q be strictly positive probability
vectors, with D(pi||q)<=K, where K>0 is fixed. Let Q be a fixed symmetric
stochastic matrix; it may be reducible. Write W=pi/q, fix alpha in (0,1),
beta=1-alpha, and let G be independence Metropolis-Hastings with proposal q.
The local kernel L_eta uses Q and the two-factor acceptance

    min(1,(q(y)/q(x))^eta)
       min(1,(pi(y)/pi(x))(q(x)/q(y))^eta).

The kernel and initialization are

    C_eta=(I+alpha G+beta L_eta)/2,       X_0~q.

Set R_eta(n)=sup TV(q C_eta^n,pi) over precisely this class. Its support size,
probabilities and Q may vary across the supremum. Each individual run uses
one fixed eta,Q,alpha. Eta may be selected as a function of a requested
deterministic horizon or accuracy before the run. It is never changed in
response to observations. The target normalizer is unknown; all ratios are
invariant under a common rescaling of raw target values. K is a population
certificate, not a fitted loss. EXPERIMENT_CONTRACT.md states counted access.

The received fixed-eta theorem proves log(n) R_eta(n)->K for every fixed
eta>0; it did not claim uniformity as eta approaches zero. The present
construction quantifies exactly that missing boundary for eta in (0,1].

**Theorem A (uniform finite certificate).** Fix h in (0,1/2). Define

    H2(h)=-h log h-(1-h)log(1-h),
    delta_h=exp(-(K+H2(h))/(1-h)),
    rho_h=1-alpha delta_h/2,       kappa_h=-log rho_h,
    rho_g=1+beta/2,
    a_h*=kappa_h/(kappa_h+log rho_g).

Choose any a in (0,a_h*). For eta in (0,1] put

    e=min(eta,1/2),    theta=a e,
    S=1+beta^(-a) rho_g^a/(1-rho_g^a rho_h^(1-a)).

For integer n>=2, N=floor(n/2), R>exp(1), set

    M=exp(2K+1),   Jbar=2/[alpha(2(n-N)+1)],
    A_R=min(1,K/(log R-1)).

Then, uniformly over the entire finite class and eta in (0,1],

    R_eta(n) <= A_R + rho_h^N
        + S[(A_R/R)^theta + ((M/h+1)Jbar)^theta]
        + sqrt((M+R)Jbar).                              (1)

The bound can of course be truncated above by 1. Constants h,a,S,M depend
only on fixed K,alpha and the declared proof choices, not eta, support size,
minimum state probability, Q or n. R,h,W are proof devices and are not
computed by the sampler.

**Theorem B (exact convergence criterion).** For any deterministic sequence
eta_n in (0,1],

    R_{eta_n}(n)->0  if and only if  eta_n log n->infinity. (2)

**Theorem C (sufficient sharp-rate scale).** Put

    kappa_0=-log(1-alpha exp(-K)/2),
    Lambda_*=1+log(1+beta/2)/kappa_0.

If liminf eta_n log n/loglog n > Lambda_*, then

    log(n) R_{eta_n}(n)->K.                             (3)

Lambda_* is a sufficient constant, not a proved sharp transition. The
three-state and growing-path lower constructions below show that some
constant-order screening on the scale loglog n/log n is genuinely necessary
for (3). Thus a bad upper estimate is not being mistaken for an obstruction.

The direct accuracy-policy consequences are proved in Section 7. The exact
finite-constant crossover remains open. Pure IMH already has coefficient K.

## 2. What is inherited and what changes

The received conjugation proof fixes the exponent min(eta,1/2) rather than
repeatedly replacing it by eta^j. The received telescoping proof uses the
actual mass-one reset of the independence proposal. Combining these gives
the sharper affine moment estimate in Section 3.

The new step is to interpolate the exponentially decreasing mass of EACH
original first-hit submeasure with its growing moment bound, making their
norms summable uniformly in eta. Each submeasure is then smoothed for its
own remaining horizon. We do not first propagate all those submeasures to a
growing common burn-in and lose a growing norm there. Different anchor
averages are legitimate because each comparison subtracts the same mass
times pi. All paths after the first hit, including every return, remain in
the actual unmodified semigroup.

We reuse the entropy envelopes and spectral anchor from the old source and
the received proofs. The earlier binomial near-harmonicity lemma remains
accepted capital but is not required directly by the present argument.

## 3. Uniform affine moment estimate

Let mu_j=q C_eta^j and p_e=1/(1-e). We claim

    ||mu_j/q||_{L^{p_e}(q)} <= B_j:=(rho_g^j-alpha)/beta
                            <=rho_g^j/beta.             (4)

Indeed min(1,z^eta)<=z^e for z>0 and 0<e<=eta. Off diagonal,
L_eta(x,y)<=Q(x,y)(q(y)/q(x))^e and G(x,y)<=q(y).
Set D=diag(q^e), u=q^e and v=q^(1-e). Diagonal probabilities are at most
one, so entrywise

    D C_eta D^(-1) <= I+(alpha u v^T+beta Q)/2.

For the row y_j=mu_j D^(-1) this yields

    y_{j+1} <= y_j(I+beta Q/2)+(alpha/2)v^T,             (5)

because y_j u=sum_x mu_j(x)=1. Q is doubly stochastic and contracts every
counting-measure l^p norm. Also ||v||_{p_e}=1 and
||y_j||_{p_e}=||mu_j/q||_{L^{p_e}(q)}. Thus the moment is at most
rho_g times the preceding moment plus alpha/2. Its initial value is 1;
solving this recurrence proves (4). Crucially the rank-one term in (5)
uses the actual law's mass, not the mass of a dominating measure.

## 4. First hit, mass interpolation and summability

Let A_h={W<h}. If b=q(A_h) and d=pi(A_h), then d<=h. Binary data processing
and h<1/2 give

    K>=D_bin(d||b)>=-H2(h)-(1-h)log(1-b).

Thus q(W>=h)>=delta_h. Until tau=inf{j>=0:W(X_j)>=h}, a global branch
with a proposal in {W>=h} accepts with certainty. Consequently

    P(tau>s)<=rho_h^s.                                 (6)

Define the unconditioned first-hit submeasure

    nu_j(F)=P(tau=j,X_j in F),       m_j=nu_j(Omega).

It is supported on {W>=h}, satisfies nu_j<=mu_j, and

    m_0<=1,       m_j<=rho_h^(j-1) for j>=1.

Put p_theta=1/(1-theta). Since theta=a e,
1/p_theta=(1-a)+a/p_e. Interpolation between L^1(q) and L^{p_e}(q),
applied to the NONNORMALIZED density nu_j/q, gives

    ||nu_j/q||_{L^{p_theta}(q)}
        <= m_j^(1-a) B_j^a=:D_j.                      (7)

For zero mass the expression and density are zero. Since
rho_g^a rho_h^(1-a)<1 by a<a_h*, the geometric series gives

    sum_{j>=0} D_j
      <=1+ beta^(-a)rho_g^a/[1-rho_g^a rho_h^(1-a)]
      =S<infinity.                                    (8)

Both the exponent a and the total S are independent of eta. This is the
load-bearing new uniformity estimate.

## 5. Smooth the individual submeasures at their remaining times

Detailed balance of L_eta follows from the symmetric flow

    pi(x)L_eta(x,y)=Q(x,y) min(q(x)^eta,q(y)^eta)
                           min(pi(x)/q(x)^eta,pi(y)/q(y)^eta).

Thus C_eta is pi-reversible and lazy, with spectrum in [0,1]. Define
A_0={W<=M}, s_0=pi(A_0)>=1/2, with M=exp(2K+1). The high-tail entropy
envelope is a_R:=pi(W>R)<=A_R and q(W>R)<=a_R/R. For a bounded test
g=C_eta^t 1_F, let z=pi(g 1_{A_0})/s_0. Then 0<=g,z<=1 and

    integral (g-z)^2/max(W,M) dpi
         <=1/[alpha s_0(2t+1)]<=2/[alpha(2t+1)].        (9)

For completeness, the IMH Dirichlet form equals half the pi-by-pi integral
of (g(x)-g(y))^2/max(W(x),W(y)). Restrict its y leg to A_0 and use Jensen
to lower bound it by (s_0/2) times the left side of (9). The mixture form
dominates alpha/2 times this form. Finally the variance of 1_F is at most
1/4 and (1-lambda)lambda^(2t)<=1/(2t+1) on [0,1]. Combining these facts
proves (9). Entropy gives the envelope because the binary divergence on
{W>R} is at least a_R(log R-1); at R=M it gives s_0>=1/2.

Fix n,N as in Theorem A. For EACH j<=N, use

    t_j=n-j, g_j=C_eta^{t_j}1_F,
    z_j=pi(g_j 1_{A_0})/s_0.

All t_j>=n-N, so (9) is bounded above by Jbar. On h<=W<=R,

    integral (g_j-z_j)^2 dq <=(M/h+1)Jbar.

Because 1/theta>=2 and |g_j-z_j|<=1, Holder and (7) give

    integral_{h<=W<=R}|g_j-z_j| dnu_j
        <=D_j[(M/h+1)Jbar]^theta.                     (10)

On W>R, Holder gives nu_j(W>R)<=D_j(a_R/R)^theta. There is no initial
nu_j mass on W<h. In the comparison measure m_j pi we include ALL W<=R,
not only W>=h. Weighted Cauchy-Schwarz and (9) give

    integral_{W<=R}|g_j-z_j| dpi <=sqrt((M+R)Jbar),

and the remaining pi tail costs a_R. Since nu_j and m_j pi have the
same total mass, and pi g_j=pi(F), these bounds imply

    |nu_j C_eta^{n-j}(F)-m_j pi(F)|
      <=D_j[(a_R/R)^theta+((M/h+1)Jbar)^theta]
           +m_j[a_R+sqrt((M+R)Jbar)].                 (11)

Each z_j cancels in its own equal-mass comparison. They need not be equal.

The exact deterministic-horizon decomposition is

    q C_eta^n = sum_{j=0}^N nu_j C_eta^{n-j}+sigma_n,
    sigma_n(Omega)=P(tau>N)<=rho_h^N,

where sigma_n is the actual law at n restricted to paths with tau>N.
It includes late hits and paths with no hit. Its difference from the same
mass times pi has TV at most that mass, not twice that mass. Sum (11), use
(8) and sum m_j<=1, then take the supremum over F. Replace the instance
tail a_R by the class envelope A_R in its monotone occurrences. This proves
(1), retaining all transitions and returns after every hit.

## 6. Horizon-dependent consequences and the common lower family

Take R=n/(log n)^4 for all sufficiently large n. Then

    A_R=K/[log n-4loglog n-1],
    sqrt((M+R)Jbar)=O((log n)^(-2)),
    log((M/h+1)Jbar)=-log n+O(1),
    log(A_R/R)=-log n+3loglog n+O(1).

Thus if eta_n log n->infinity, theta_n log n->infinity, and all terms in
(1) tend to zero. This proves the sufficient half of (2).

For necessity use the positive three-state family in
reviews/vanishing_lower_proof.md. For fixed
0<b<1-exp(-K), its proposal-start TV has a strictly positive lower limit
along any subsequence with eta_n log n bounded. Any failure of divergence
has such a subsequence, and a further subsequence converges to a finite
u>=0. The family gives the lower limit

    b beta exp(-u)/[alpha(1-b)+beta exp(-u)]>0.         (12)

Its fixed Q swaps the reservoir and rare terminal state; pi,q stay positive
and D(pi||q)->log(1/(1-b))<K. Section 8 records the precise provenance of
that lower construction. The accepted full companion proof completes (2).

Next suppose liminf eta_n log n/loglog n>Lambda_*. Since h can be fixed
arbitrarily small, kappa_h->kappa_0, so one may fix h and a<a_h* with
1/a below that liminf. The last two exponential transport terms in (1)
are then o(1/log n). The cap e=min(eta,1/2) causes no problem: when eta
exceeds 1/2 those terms decay polynomially in n. It follows that

    limsup log n R_{eta_n}(n)<=K.

The matching lower bound is independent of eta. Set Q=I, fix c in (0,K),
and take two states with terminal pi mass p=c/log n and terminal proposal
mass q_*=p/[n(log n)^2]. Then D(pi||q)->c, W_*=n(log n)^2, and
C_eta=(1-alpha/2)I+(alpha/2)G for EVERY eta. The nontrivial eigenvalue is

    1-(alpha/2)q_*/p=1-alpha/[2n(log n)^2],

so the exact terminal deficit at n is

    (p-q_*)[1-alpha/(2n(log n)^2)]^n
          =(c+o(1))/log n.

Let c increase to K. This proves (3), and also supplies the K lower
coefficient in every accuracy-policy comparison. No finite-time ordering
of different local kernels is inferred.

## 7. Accuracy policy: direct inversion with eta fixed during each run

Let eta(epsilon) in (0,1] be specified before a run. Define

    T_policy(epsilon)=sup_instance inf{n>=0:
          TV(q C_{eta(epsilon)}^n,pi)<=epsilon}.

For each fixed epsilon the kernel is unchanged, and distance to stationarity
is nonincreasing in n. Hence the uniform risk crossing controls this
worst-case first sufficient time. The diagonal sequence R_{eta_n}(n) itself
need NOT be monotone; we never invert it as if it were.

Write d_epsilon=eta(epsilon)/[epsilon log(1/epsilon)]. If it tends to
d in (0,infinity), then the finite certificate and the three-state lower
give

    max(K,1/d) <= liminf epsilon log T_policy(epsilon)
       <=limsup epsilon log T_policy(epsilon)
       <=max(K,Lambda_*/d).                           (13)

If d_epsilon->infinity, both bounds give the exact limit K. If
d_epsilon->0, epsilon log T_policy(epsilon)->infinity. These statements
are sharpened, where applicable, by the growing-path lower in Section 8.

Here is the direct proof. For A>K set n=ceil(exp(A/epsilon)) and
R=n/(log n)^4. The entropy term in (1) is (K/A+o(1))epsilon.
For fixed admissible h,a, the transport terms are
exp[-a eta(epsilon)log n+o(eta(epsilon)log n)]
=epsilon^{a A d+o(1)} when d is finite and positive. Choose a with
a A d>1, possible whenever A d>Lambda_*. All other terms are o(epsilon).
Since K/A<1 there is strict error margin. This proves the upper bound
by letting A decrease to max(K,Lambda_*/d). For d=infinity the same
argument works for every A>K; the capped e also diverges relative to
epsilon log(1/epsilon), so no exception occurs.

For the lower, at n=floor(exp(A/epsilon)) with A d<1, the three-state
capture probability is epsilon^{A d+o(1)}, exceeding epsilon. Its target
terminal mass can be chosen as (log n)^(-m), m>2, so the subtracted target
mass is negligible. For d=0 this works for every finite A>0. The Q=I
two-state family supplies the separate K lower; combine the two families
by taking their maximum, not by adding their KL budgets. This proves (13).

In particular eta(epsilon)=d epsilon log(1/epsilon) with d>Lambda_*/K
retains the exact K coefficient. On each individually fixed finite positive
instance, this policy's local acceptance tends to ordinary MH(Q,pi), since
eta(epsilon)->0. That pointwise convergence is not uniform over the
support-varying class. It establishes a robustness tolerance for weakening
the screen, not a practical speedup.

## 8. Accepted adverse families and a stronger critical obstruction

The full lower proof is reviews/vanishing_lower_proof.md, constructed by the
distinct lower contributor and directly checked by the principal. Its
finite-horizon bounds count actual path events; numerical matrix powers are
diagnostics only. Source hashes and root acceptance are in
LOWER_ACCEPTANCE.md and the lower contributor's receipt.

### 8.1 The three-state event used in Theorem B

Fix b in (0,1-exp(-K)), let L=log n, p=L^(-m) with fixed m>2, and set

    q_A=p/(n L^2), q_B=b, q_*=1-b-q_A,
    pi_A=p, pi_B=p/n^4, pi_*=1-p-p/n^4.

Q swaps A,B and fixes *. All vectors are positive eventually and their
forward KL tends to -log(1-b)<K. Let r=(q_A/b)^eta. The actual probabilities
from B to A and * are x=(alpha q_A+beta r)/2 and y=alpha q_*/2, and

    d=x+y=[alpha(1-b)+beta r]/2,
    e=1-C(A,A)=alpha(1-p)/(2nL^2)+beta r/(2n^4).

The event starting at B, first leaving B for A at time j<=n, and staying
at A until n has exact mass

    E_n=b x sum_{j=1}^n (1-d)^(j-1)(1-e)^(n-j).

Since d>=alpha(1-b)/2 and ne=O(L^-2),
E_n=(b x/d)(1+O(L^-2)) relatively, uniformly in eta>=0.
For u=eta log n in [0,C loglog n], any fixed C<infinity,

    r=exp(-u)[1+O((loglog n)^2/log n)],
    E_n=F_b(u)(1+o(1)),
    F_b(u)=b beta exp(-u)/[alpha(1-b)+beta exp(-u)].

TV is at least E_n-p. Taking m>C+2 makes the target-mass subtraction
negligible uniformly on that range. For bounded u this proves (12), and
therefore the necessary half of Theorem B. At u=loglog n+d+o(1), it gives

    liminf log n R_eta(n)>=(beta/alpha)(exp(K)-1)exp(-d).

This is a lower bound for the supremum, not an exact worst-class crossover.

### 8.2 Repeated local captures improve the lower threshold

Define the structural constant

    d_*=2 alpha exp(-K)/beta,
    chi=1 if d_*>=1;
    otherwise chi is the unique r in (0,1) satisfying
        d_*=r(1-r)^((1-r)/r).                         (14)

For every sequence with

    eta_n log n/loglog n -> lambda in (0,1/chi),

the new admitted path family proves

    log n R_{eta_n}(n)->infinity.                     (15)

This necessary multiplier 1/chi is not asserted to be the exact threshold.
Here is the explicit construction and finite probability mechanism. Fix
b<1-exp(-K), v>0, let u=eta_n log n, and take a path of
m=max(1,floor(u/v)) edges plus a state *. For u tending to infinity with
u=O(loglog n), m=O(loglog n). With L=log n, p=L^(-M_0), M_0>2, set

    z=(p/(b n L^2))^(1/m),
    q_i=b z^i,      pi_i=p n^(-2(m-i)),       0<=i<=m,

and give * the remaining positive mass in each vector. Q has probability
1/2 on each adjacent edge, diagonal probability 1/2 at path endpoints,
zero internal diagonal, and Q(*,*)=1. It is symmetric and target independent.
KL tends to -log(1-b)<K uniformly in this growing support. The terminal
weight is nL^2; all preceding path weights tend to zero. Forward local
acceptance is s=z^eta; reverse acceptance is s/n^2.

A marked local forward transition occurs with probability f=beta s/4.
The total nonself exit probability at every transient path state is between
D and E, where, writing S_q=bz/(1-z),

    D=alpha(1-b-S_q)/2,
    delta=alpha[S_q+b n^-2/(1-n^-2)]/2+beta/(4n^2),
    E=f+alpha(1-b)/2+delta.

For sufficiently large n these bounds hold with D>0. Global exits, global
returns and local reverse exits are all included in the unfavorable total;
they are not silently removed from the chain. If h_n=floor(n/(2m)),
the probability of a next marked exit within h_n steps is at least
(f/E)(1-exp(-D h_n)). Requiring this success successively at each state,
then retaining the terminal state, gives the finite event lower bound

    R_eta(n)>= b(f/E)^m [1-m exp(-D h_n)]_+
                   [1-alpha/(2L^2)-beta/(4n)]_+ - p.  (16)

The terminal global escape is alpha(1-p)/(2nL^2) and local escape is
beta s/(4n^2). Hence the retention factor in (16) is valid. Its timing
and retention corrections are multiplicative relative to capture.

Put d_b=2alpha(1-b)/beta and phi_d(v)=log(1+d exp(v))/v. The logarithm
of the capture factor in (16) is

    log[b(f/E)^m]=-phi_{d_b}(v) u+O(1).

When u/log L->lambda and M_0>lambda phi_{d_b}(v)+2, (16) implies
R_eta(n)>=L^(-lambda phi_{d_b}(v)+o(1)). For d>=1, inf_v phi_d(v)=1.
For 0<d<1 its unique minimizer has value r in (0,1) characterized by
d=r(1-r)^((1-r)/r). This follows by differentiating: at the stationary
point r=d exp(v)/(1+d exp(v)) and rv=-log(1-r). The derivative changes
sign once because v d exp(v)/(1+d exp(v))-log(1+d exp(v)) is strictly
increasing from -log(1+d) to -log d. Finally let b approach 1-exp(-K)
from below; for every strict lambda<1/chi there are fixed b,v with
lambda phi_{d_b}(v)<1. This proves (15).

At K=1,alpha=1/2, the implicit constant is chi=0.91870999842712... and
1/chi=1.08848276573897.... An exact example avoids reliance on those
decimals: b=63/100, v=log16, M_0=4, lambda=27/25. It is admitted since
exp(1)>65/24>100/37, and its capture exponent is

    27 log(321/25)/(25 log16)=0.994294790283846...<1,

certified by the integer inequality 321^27<25^27 16^25. Thus lambda=1.08
still has log n R_eta(n)->infinity. A single-trap prediction of a universal
critical multiplier 1 is false. The small exponent gap means finite examples
do not by themselves visibly establish this divergence.

### 8.3 Sharpened accuracy-policy lower

For d_epsilon->d in (0,infinity), the path lower replaces (13)'s 1/d by
1/(d chi):

    max(K,1/(d chi)) <= liminf epsilon log T_policy(epsilon)
       <=limsup epsilon log T_policy(epsilon)
       <=max(K,Lambda_*/d).                           (17)

Indeed take n=floor(exp(A/epsilon)). Then u/loglog n->A d. Whenever
A d<1/chi, choose fixed b,v with A d phi_{d_b}(v)<1; (16)'s capture
mass is epsilon^(A d phi+o(1)), which exceeds epsilon. The target terminal
mass is O(epsilon^{M_0}) and is negligible. Monotonicity for this single
fixed eta(epsilon) gives T_policy(epsilon)>n. Let A increase to 1/(d chi)
and combine with the eta-independent K family. The endpoint d=0 remains
handled by the three-state uniform crossover, while d=infinity gives K.

For K=1,alpha=1/2 and eta(epsilon)~epsilon log(1/epsilon), the rigorous
coefficient interval is therefore [1.0884827657...,3.3129027138...]. The
lower endpoint strictly exceeds pure IMH's 1. This is a real worst-class
step-complexity penalty, with no claim about a particular applied target.

## 9. Limits, comparisons and unresolved question

This is a finite-space, forward-population-KL, proposal-start result for the
lazy random mixture with fixed reversible kernels. It is not a statement
about deterministic LG/GL scheduling, adaptive online tuning, nonreversible
local kernels, empirical training losses, or finite-precision sampling.
The finite certificate is deliberately sufficient and can be numerically
conservative; its computed time is not actual minimax time.

The sampler is established delayed acceptance. The new construction is an
analysis of its nonuniform robustness. Off-diagonal acceptance increases as
eta decreases, but finite-time proposal-start TV need not improve. A weaker
first screen passes at least as often, so it does not by itself save target
evaluations. Pure IMH already has sharp K and is the ordinary comparator.
Every target query/proposal/cache entry is counted in the companion contract.

The precise next question is the finite-constant crossover when
eta(epsilon)/(epsilon log(1/epsilon))->d in (0,infinity). Can the summable
transport exponent be matched to an admitted capture network, giving a
sharp coefficient, or can a stronger transport representation exclude the
current bound's loss? This is a distinct joint-limit problem; the fixed-eta
gap remains closed. No new empirical application search is proposed.
